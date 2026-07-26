# project-path: tools/validate_advanced_quality_review_analyzer_runtime_foundation_v1.py
"""Focused validation for Advanced Quality Review analyzer runtime foundation v1."""
from __future__ import annotations

import ctypes
import os
from pathlib import Path
import shutil
import sys
import threading
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (
    AnalysisExecutionStatus,
    AnalyzerAuthorityRole,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_capability_preflight import (
    preflight_analyzer_capabilities,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_environment_contract import (
    ANALYZER_RUNTIME_FOUNDATION_FEATURE_ID,
    AnalyzerCapabilityMode,
    AnalyzerLockEntry,
    build_analyzer_environment_lock,
    build_analyzer_runtime_identity,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_process_runtime import (
    BoundedProcessRequest,
    CancellationToken,
    ProcessProgressEvent,
    run_bounded_process,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
    analyzer_cache_root,
    analyzer_cache_root_blockers,
    analyzer_engine_cache_root,
    daily_work_root,
    project_support_root,
)

FEATURE_ID = ANALYZER_RUNTIME_FOUNDATION_FEATURE_ID
SOURCE_MODULES = (
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_environment_contract.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_capability_preflight.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_process_tree.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_process_runtime.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_project_support_paths.py",
)


def main() -> int:
    """Run deterministic contract, runtime, cleanup, and ownership validation."""
    fixture_root = daily_work_root(PROJECT_ROOT) / "release2_analyzer_runtime_validation"
    _reset_fixture_root(fixture_root)
    _validate_environment_identity(fixture_root)
    _validate_capability_preflight(fixture_root)
    _validate_output_limits(fixture_root)
    _validate_timeout(fixture_root)
    _validate_cancellation(fixture_root)
    _validate_progress_observability(fixture_root)
    _validate_process_tree_cleanup(fixture_root)
    _validate_cache_ownership()
    _validate_source_contracts()
    print("ADVANCED_QUALITY_REVIEW_ANALYZER_RUNTIME_FOUNDATION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _validate_environment_identity(fixture_root: Path) -> None:
    expected = f"{sys.version_info.major}.{sys.version_info.minor}"
    entry = AnalyzerLockEntry(
        engine_id="python_probe",
        executable=sys.executable,
        version_args=("--version",),
        expected_version=expected,
        authority_role=AnalyzerAuthorityRole.MANDATORY,
        capability_mode=AnalyzerCapabilityMode.AUTHORITATIVE,
        configuration_source="controlled_validator",
        cache_routing_supported=True,
    )
    lock = build_analyzer_environment_lock((entry,))
    identity = build_analyzer_runtime_identity(lock)
    assert len(lock.lock_hash) == 64
    assert len(identity.identity_hash) == 64
    assert identity.analyzer_lock_hash == lock.lock_hash
    assert identity.python_executable
    print("ANALYZER_ENVIRONMENT_IDENTITY_IMMUTABLE: PASS")


def _validate_capability_preflight(fixture_root: Path) -> None:
    expected = f"{sys.version_info.major}.{sys.version_info.minor}"
    entries = (
        AnalyzerLockEntry(
            engine_id="python_probe",
            executable=sys.executable,
            version_args=("--version",),
            expected_version=expected,
            authority_role=AnalyzerAuthorityRole.MANDATORY,
            capability_mode=AnalyzerCapabilityMode.AUTHORITATIVE,
            configuration_source="controlled_validator",
            cache_routing_supported=True,
        ),
        AnalyzerLockEntry(
            engine_id="missing_probe",
            executable="kanda_missing_analyzer_executable_7f1c",
            version_args=("--version",),
            expected_version="0.0",
            authority_role=AnalyzerAuthorityRole.ADVISORY,
            capability_mode=AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE,
            configuration_source="controlled_validator",
            cache_routing_supported=True,
        ),
    )
    evidence = preflight_analyzer_capabilities(
        build_analyzer_environment_lock(entries),
        cwd=fixture_root,
    )
    by_id = {item.engine_id: item for item in evidence}
    assert by_id["python_probe"].available
    assert by_id["python_probe"].compatible
    assert by_id["python_probe"].execution_status is AnalysisExecutionStatus.SUCCEEDED
    assert not by_id["missing_probe"].available
    assert by_id["missing_probe"].execution_status is AnalysisExecutionStatus.UNAVAILABLE
    assert by_id["missing_probe"].capability_mode is AnalyzerCapabilityMode.UNAVAILABLE
    print("ANALYZER_CAPABILITY_PREFLIGHT_NO_SILENT_INSTALL: PASS")


def _validate_output_limits(fixture_root: Path) -> None:
    code = (
        "import sys;"
        "sys.stdout.write('A'*50000);sys.stdout.flush();"
        "sys.stderr.write('B'*40000);sys.stderr.flush()"
    )
    result = run_bounded_process(
        BoundedProcessRequest(
            engine_id="output_limit_probe",
            argv=(sys.executable, "-c", code),
            cwd=str(fixture_root),
            timeout_seconds=10.0,
            max_stdout_bytes=1024,
            max_stderr_bytes=2048,
        )
    )
    assert result.status is AnalysisExecutionStatus.SUCCEEDED
    assert result.stdout_bytes_observed == 50000
    assert result.stderr_bytes_observed == 40000
    assert result.stdout_truncated and result.stderr_truncated
    assert len(result.stdout_text.encode("utf-8")) <= 1024
    assert len(result.stderr_text.encode("utf-8")) <= 2048
    print("ANALYZER_OUTPUT_LIMITS_BOUNDED: PASS")


def _validate_timeout(fixture_root: Path) -> None:
    result = run_bounded_process(
        BoundedProcessRequest(
            engine_id="timeout_probe",
            argv=(sys.executable, "-c", "import time; time.sleep(5)"),
            cwd=str(fixture_root),
            timeout_seconds=0.3,
        )
    )
    assert result.status is AnalysisExecutionStatus.TIMED_OUT
    assert result.cleanup.requested
    assert result.cleanup.root_process_reaped
    print("ANALYZER_TIMEOUT_BOUNDED: PASS")


def _validate_cancellation(fixture_root: Path) -> None:
    token = CancellationToken()
    timer = threading.Timer(0.2, token.cancel)
    timer.start()
    try:
        result = run_bounded_process(
            BoundedProcessRequest(
                engine_id="cancel_probe",
                argv=(sys.executable, "-c", "import time; time.sleep(5)"),
                cwd=str(fixture_root),
                timeout_seconds=5.0,
            ),
            cancellation_token=token,
        )
    finally:
        timer.cancel()
    assert result.status is AnalysisExecutionStatus.CANCELLED
    assert result.cleanup.requested
    assert result.cleanup.root_process_reaped
    print("ANALYZER_CANCELLATION_BOUNDED: PASS")


def _validate_progress_observability(fixture_root: Path) -> None:
    events: list[ProcessProgressEvent] = []
    result = run_bounded_process(
        BoundedProcessRequest(
            engine_id="progress_probe",
            argv=(sys.executable, "-c", "print('ok')"),
            cwd=str(fixture_root),
            timeout_seconds=5.0,
        ),
        progress_callback=events.append,
    )
    assert result.status is AnalysisExecutionStatus.SUCCEEDED
    phases = [event.phase for event in events]
    assert phases[0] == "STAGE_START"
    assert phases[-1] == "STAGE_TERMINAL"
    print("ANALYZER_LIVE_STAGE_OBSERVABILITY: PASS")


def _validate_process_tree_cleanup(fixture_root: Path) -> None:
    scripts_root = fixture_root / "tree_fixture"
    scripts_root.mkdir(parents=True, exist_ok=True)
    _write_tree_scripts(scripts_root)
    token = CancellationToken()
    watcher = threading.Thread(
        target=_cancel_when_tree_ready,
        args=(scripts_root, token),
        daemon=True,
    )
    watcher.start()
    result = run_bounded_process(
        BoundedProcessRequest(
            engine_id="process_tree_probe",
            argv=(sys.executable, str(scripts_root / "parent.py"), str(scripts_root)),
            cwd=str(scripts_root),
            timeout_seconds=10.0,
        ),
        cancellation_token=token,
    )
    watcher.join(timeout=2.0)
    assert result.status is AnalysisExecutionStatus.CANCELLED
    pids = [
        int((scripts_root / name).read_text(encoding="utf-8").strip())
        for name in ("parent.pid", "child.pid", "grandchild.pid")
    ]
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline and any(_pid_alive(pid) for pid in pids):
        time.sleep(0.1)
    survivors = [pid for pid in pids if _pid_alive(pid)]
    assert not survivors, "PROCESS_TREE_SURVIVORS:" + ",".join(map(str, survivors))
    print("ANALYZER_PROCESS_TREE_DESCENDANTS_REAPED: PASS")


def _validate_cache_ownership() -> None:
    cache = analyzer_engine_cache_root(
        PROJECT_ROOT,
        engine_id="ruff",
        engine_version="probe-version",
        config_hash="abc123",
        analysis_key="analysis-key",
    )
    assert not analyzer_cache_root_blockers(PROJECT_ROOT, cache)
    assert cache.is_relative_to(analyzer_cache_root(PROJECT_ROOT))
    assert not cache.is_relative_to(PROJECT_ROOT)
    assert not cache.is_relative_to(project_support_root(PROJECT_ROOT))
    print("ANALYZER_CACHE_TRANSIENT_GARBAGE_ONLY: PASS")


def _validate_source_contracts() -> None:
    for relative in SOURCE_MODULES:
        path = PROJECT_ROOT / relative
        data = path.read_bytes()
        data.decode("utf-8", errors="strict")
        assert not data.startswith(b"\xef\xbb\xbf"), relative
        text = data.decode("utf-8")
        assert all(ord(character) < 128 for character in text), relative
        line_count = len(text.splitlines())
        assert 101 <= line_count <= 499, f"MODULE_SIZE:{relative}:{line_count}"
    runtime_text = (PROJECT_ROOT / SOURCE_MODULES[3]).read_text(encoding="utf-8")
    assert "shell=False" in runtime_text
    assert "subprocess.Popen" in runtime_text
    assert "terminate_process_tree" in runtime_text
    tree_text = (PROJECT_ROOT / SOURCE_MODULES[2]).read_text(encoding="utf-8")
    assert '"taskkill", "/PID"' in tree_text
    assert "os.killpg" in tree_text
    print("ANALYZER_RUNTIME_SHELL_FREE_PROCESS_CONTRACT: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("MODULE_SIZE_POLICY_101_499: PASS")


def _reset_fixture_root(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, onerror=_clear_readonly_and_retry)
    path.mkdir(parents=True, exist_ok=True)


def _clear_readonly_and_retry(function: object, path: str, exc_info: object) -> None:
    os.chmod(path, 0o700)
    function(path)


def _write_tree_scripts(root: Path) -> None:
    grandchild = """from pathlib import Path\nimport os\nimport sys\nimport time\nroot = Path(sys.argv[1])\n(root / 'grandchild.pid').write_text(str(os.getpid()), encoding='utf-8')\nwhile True:\n    time.sleep(1)\n"""
    child = """from pathlib import Path\nimport os\nimport subprocess\nimport sys\nimport time\nroot = Path(sys.argv[1])\n(root / 'child.pid').write_text(str(os.getpid()), encoding='utf-8')\nsubprocess.Popen([sys.executable, str(root / 'grandchild.py'), str(root)])\nwhile True:\n    time.sleep(1)\n"""
    parent = """from pathlib import Path\nimport os\nimport subprocess\nimport sys\nimport time\nroot = Path(sys.argv[1])\n(root / 'parent.pid').write_text(str(os.getpid()), encoding='utf-8')\nsubprocess.Popen([sys.executable, str(root / 'child.py'), str(root)])\nwhile True:\n    time.sleep(1)\n"""
    for name, text in (
        ("grandchild.py", grandchild),
        ("child.py", child),
        ("parent.py", parent),
    ):
        (root / name).write_bytes(text.encode("utf-8"))


def _cancel_when_tree_ready(root: Path, token: CancellationToken) -> None:
    deadline = time.monotonic() + 5.0
    required = (root / "parent.pid", root / "child.pid", root / "grandchild.pid")
    while time.monotonic() < deadline:
        if all(path.exists() for path in required):
            time.sleep(0.2)
            token.cancel()
            return
        time.sleep(0.05)
    token.cancel()


def _pid_alive(pid: int) -> bool:
    if os.name == "nt":
        process_query_limited_information = 0x1000
        still_active = 259
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(process_query_limited_information, False, pid)
        if not handle:
            return False
        exit_code = ctypes.c_ulong()
        ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
        kernel32.CloseHandle(handle)
        return bool(ok and exit_code.value == still_active)
    proc_stat = Path("/proc") / str(pid) / "stat"
    if proc_stat.exists():
        try:
            parts = proc_stat.read_text(encoding="utf-8", errors="replace").split()
            if len(parts) > 2 and parts[2] == "Z":
                return False
        except OSError:
            pass
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


if __name__ == "__main__":
    raise SystemExit(main())
