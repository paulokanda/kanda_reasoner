# project-path: tools/validate_fire_shield_manage_workflows_test_execution_isolation_v2c.py
"""Validate OS-isolated Manage Workflows pytest/unittest execution v2c."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import shutil
import sys
import tempfile
import venv
from pathlib import Path
from typing import Any

FEATURE_ID = (
    "kanda-reasoner-fire-shield-manage-workflows-test-execution-isolation-v2c"
)


def require(condition: bool, marker: str) -> None:
    """Print one PASS marker or fail closed."""
    if not condition:
        raise RuntimeError(marker + ": FAIL")
    print(marker + ": PASS")


def _sha(path: Path) -> str:
    """Return SHA-256 for one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _anchor_validator_import_root(root: Path) -> None:
    """Make validator-owned KANDA imports independent of script location."""
    root_text = str(root)
    remaining: list[str] = []
    for item in sys.path:
        try:
            same_root = Path(item or ".").resolve() == root
        except OSError:
            same_root = False
        if not same_root:
            remaining.append(item)
    sys.path[:] = [root_text, *remaining]
    require(
        Path(sys.path[0]).resolve() == root,
        "OS_FIRE_SHIELD_V2C_VALIDATOR_PROJECT_ROOT_IMPORT_ANCHOR",
    )
    __import__("kanda_reasoner_app")
    print("OS_FIRE_SHIELD_V2C_KANDA_PACKAGE_IMPORT: PASS")


def _function_source(path: Path, name: str) -> str:
    """Return exact source segment for one function."""
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    lines = text.splitlines()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            end = int(node.end_lineno or node.lineno)
            return "\n".join(lines[node.lineno - 1 : end])
    raise RuntimeError("FUNCTION_NOT_FOUND:" + name)


def _static_validation(root: Path) -> None:
    """Validate v2c source ownership and routing contracts."""
    help_root = root / "kanda_reasoner_app/manage_workflows/manage_workflows_help"
    command_path = help_root / "workflow_command_runner.py"
    test_path = help_root / "workflow_test_runner.py"
    manifest_path = (
        root / "kanda_reasoner_app/manage_workflows/manage_workflows_help.json"
    )

    command_text = command_path.read_text(encoding="utf-8")
    test_text = test_path.read_text(encoding="utf-8")
    run_tests = _function_source(command_path, "run_tests")

    require(
        "return _run_project_tests(root, discovered, cfg)" in run_tests,
        "OS_FIRE_SHIELD_V2C_COMMAND_RUNNER_DELEGATES_TEST_OWNER",
    )
    require(
        "execute_command(" not in run_tests,
        "OS_FIRE_SHIELD_V2C_TEST_FACADE_NO_ORDINARY_COMMAND_RUNNER",
    )
    require(
        "run_project_python_probe(" in test_text,
        "OS_FIRE_SHIELD_V2C_FROZEN_V2B_RUNNER_REUSED",
    )
    require(
        "subprocess.run(" not in test_text,
        "OS_FIRE_SHIELD_V2C_NO_DIRECT_SUBPROCESS_LAUNCH",
    )
    require(
        '"-p",\n                "no:cacheprovider"' in test_text,
        "OS_FIRE_SHIELD_V2C_PYTEST_CACHE_PROVIDER_DISABLED",
    )
    require(
        (
            '"-m",\n                    "unittest",\n                    "discover"'
            in test_text
        ),
        "OS_FIRE_SHIELD_V2C_UNITTEST_ROUTED",
    )
    require(
        'env["PYTHONDONTWRITEBYTECODE"] = "1"' in test_text,
        "OS_FIRE_SHIELD_V2C_BYTECODE_WRITE_DISABLED",
    )
    require(
        "shell=True" not in test_text and "shell = True" not in test_text,
        "OS_FIRE_SHIELD_V2C_NO_SHELL_STRING_EXECUTION",
    )
    require(
        "E:\\" not in command_text and "E:\\" not in test_text,
        "OS_FIRE_SHIELD_V2C_NO_FIXED_INSTALL_DRIVE",
    )
    require(
        len(command_text.splitlines()) <= 500,
        "OS_FIRE_SHIELD_V2C_MAX500_WORKFLOW_COMMAND_RUNNER",
    )
    require(
        len(test_text.splitlines()) <= 500,
        "OS_FIRE_SHIELD_V2C_MAX500_WORKFLOW_TEST_RUNNER",
    )
    require(
        all(ord(ch) < 128 for ch in command_text + test_text),
        "OS_FIRE_SHIELD_V2C_ASCII_TOUCHED_MODULES",
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    command_spec = manifest["helpers"]["workflow_command_runner.py"]
    test_spec = manifest["helpers"]["workflow_test_runner.py"]
    require(
        "run_tests" in (command_spec.get("exports") or []),
        "OS_FIRE_SHIELD_V2C_PUBLIC_RUN_TESTS_FACADE_PRESERVED",
    )
    require(
        not (test_spec.get("exports") or []),
        "OS_FIRE_SHIELD_V2C_TEST_HELPER_PRIVATE_OWNERSHIP",
    )
    require(
        "run_tests" in (manifest.get("exports") or [])
        and "run_tests" in (manifest.get("origin_all") or []),
        "OS_FIRE_SHIELD_V2C_AGGREGATE_EXPORT_PRESERVED",
    )
    print("OS_FIRE_SHIELD_V2C_STATIC_VALIDATION: PASS")


def _fixture_python(fixture_root: Path) -> Path:
    """Create one no-network Windows Project virtual environment."""
    venv.EnvBuilder(with_pip=False, clear=True).create(fixture_root / ".venv")
    python = fixture_root / ".venv" / "Scripts" / "python.exe"
    require(python.is_file(), "OS_FIRE_SHIELD_V2C_FIXTURE_PROJECT_PYTHON")
    return python


def _write_fake_pytest(fixture: Path) -> None:
    """Install a controlled pytest-compatible module inside fixture .venv."""
    package = fixture / ".venv" / "Lib" / "site-packages" / "pytest"
    package.mkdir(parents=True, exist_ok=True)
    (package / "__init__.py").write_text(
        "__version__ = 'v2c-fixture'\n",
        encoding="ascii",
    )
    main = """import json
import os
import sys
from pathlib import Path

project = Path.cwd()
tool_probe = Path(os.environ[\"KANDA_V2C_TOOL_PROBE\"])
payload = {
    \"python\": sys.executable,
    \"project_read\": False,
    \"project_write_denied\": False,
    \"tool_read_denied\": False,
    \"transient_write\": False,
    \"cache_provider_disabled\": False,
}
payload[\"project_read\"] = (project / \"allowed.txt\").read_text() == \"PROJECT_OK\"
try:
    (project / \"blocked_pytest.txt\").write_text(\"BAD\")
except OSError:
    payload[\"project_write_denied\"] = True
try:
    tool_probe.read_bytes()
except OSError:
    payload[\"tool_read_denied\"] = True
transient = Path(os.environ[\"TEMP\"])
(transient / \"pytest_v2c.txt\").write_text(\"OK\")
payload[\"transient_write\"] = (transient / \"pytest_v2c.txt\").read_text() == \"OK\"
args = sys.argv[1:]
payload[\"cache_provider_disabled\"] = \"-p\" in args and \"no:cacheprovider\" in args
print(\"KANDA_V2C_PYTEST_PAYLOAD=\" + json.dumps(payload, sort_keys=True))
ok = all(payload[key] for key in (
    \"project_read\",
    \"project_write_denied\",
    \"tool_read_denied\",
    \"transient_write\",
    \"cache_provider_disabled\",
))
raise SystemExit(0 if ok else 1)
"""
    (package / "__main__.py").write_text(main, encoding="ascii")


def _write_unittest_fixture(fixture: Path) -> None:
    """Create one unittest that proves the same external boundary."""
    tests = fixture / "tests"
    tests.mkdir()
    code = """import json
import os
import sys
import unittest
from pathlib import Path


class BoundaryTest(unittest.TestCase):
    def test_fire_shield_boundary(self):
        project = Path.cwd()
        tool_probe = Path(os.environ[\"KANDA_V2C_TOOL_PROBE\"])
        payload = {
            \"python\": sys.executable,
            \"project_read\": (project / \"allowed.txt\").read_text() == \"PROJECT_OK\",
            \"project_write_denied\": False,
            \"tool_read_denied\": False,
            \"transient_write\": False,
        }
        try:
            (project / \"blocked_unittest.txt\").write_text(\"BAD\")
        except OSError:
            payload[\"project_write_denied\"] = True
        try:
            tool_probe.read_bytes()
        except OSError:
            payload[\"tool_read_denied\"] = True
        transient = Path(os.environ[\"TEMP\"])
        (transient / \"unittest_v2c.txt\").write_text(\"OK\")
        payload[\"transient_write\"] = (
            transient / \"unittest_v2c.txt\"
        ).read_text() == \"OK\"
        print(\"KANDA_V2C_UNITTEST_PAYLOAD=\" + json.dumps(payload, sort_keys=True))
        self.assertTrue(all(payload[key] for key in (
            \"project_read\",
            \"project_write_denied\",
            \"tool_read_denied\",
            \"transient_write\",
        )))


if __name__ == \"__main__\":
    unittest.main()
"""
    (tests / "test_boundary.py").write_text(code, encoding="ascii")


def _payload(stdout: str, marker: str) -> dict[str, Any]:
    """Decode one marker-prefixed JSON line."""
    for line in stdout.splitlines():
        if line.startswith(marker):
            value = json.loads(line[len(marker) :])
            if isinstance(value, dict):
                return value
    raise RuntimeError("LIVE_PAYLOAD_MARKER_MISSING:" + marker)


def _source_snapshot(fixture: Path) -> dict[str, str]:
    """Hash fixture source while excluding the Project virtual environment."""
    result: dict[str, str] = {}
    for path in sorted(fixture.rglob("*")):
        if not path.is_file() or ".venv" in path.parts:
            continue
        result[path.relative_to(fixture).as_posix()] = _sha(path)
    return result


def _external_live(root: Path) -> None:
    """Exercise actual command_runner.run_tests on a disposable external Project."""
    if os.name != "nt":
        raise RuntimeError("OS_FIRE_SHIELD_V2C_WINDOWS_REQUIRED")

    from kanda_reasoner_app.manage_workflows.manage_workflows_help import (
        workflow_command_runner as command_runner,
    )
    from kanda_reasoner_app.manage_workflows.manage_workflows_help import (
        workflow_test_runner as test_runner,
    )
    from kanda_reasoner_app.manage_workflows.manage_workflows_help import (
        workflow_python_runtime as python_runtime,
    )
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from kanda_reasoner_app.project_support_boundary import (
        ProjectSelectionMode,
        canonical_project_support_root,
        canonical_transient_garbage_root,
    )

    tool_probe = root / "kanda_reasoner_app" / "project_fire_shield.py"
    tool_before = tool_probe.read_bytes()

    with tempfile.TemporaryDirectory(prefix="kanda_v2c_") as temp:
        temp_root = Path(temp)
        fixture = temp_root / "external_project"
        fixture.mkdir()
        (fixture / "allowed.txt").write_text("PROJECT_OK", encoding="ascii")
        project_python = _fixture_python(fixture)
        _write_fake_pytest(fixture)
        _write_unittest_fixture(fixture)

        registry_path = temp_root / "registry" / "projects.json"
        registry_path.parent.mkdir(parents=True)
        registry = ProjectSelectionRegistry(
            tool_source_root=root,
            registry_path=registry_path,
        )
        registry.register_explicit_selection(
            fixture,
            ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
        )

        def injected_probe(project_root, python_args, **kwargs):
            kwargs["tool_source_root"] = root
            kwargs["registry_path"] = registry_path
            return python_runtime.run_project_python_probe(
                project_root, python_args, **kwargs
            )

        def injected_has_module(project_root, module_name):
            probe = (
                "import importlib.util,sys;"
                "sys.exit(0 if importlib.util.find_spec(sys.argv[1]) else 1)"
            )
            completed = injected_probe(
                project_root,
                ["-I", "-c", probe, module_name],
                timeout=15,
            )
            return completed.returncode == 0

        test_runner.run_project_python_probe = injected_probe
        test_runner.project_python_has_module = injected_has_module
        os.environ["KANDA_V2C_TOOL_PROBE"] = str(tool_probe)
        before = _source_snapshot(fixture)
        discovered = {
            "pytest_files": [str(fixture / "tests/test_boundary.py")],
            "test_dirs": ["tests"],
        }

        pytest_result = command_runner.run_tests(
            fixture,
            discovered,
            {"enabled": True, "runner": "pytest", "pytest_args": ["-q"]},
        )[0]
        require(
            pytest_result.status == "pass",
            "OS_FIRE_SHIELD_V2C_PYTEST_EXIT_ZERO",
        )
        pytest_payload = _payload(
            str(pytest_result.details.get("stdout") or ""),
            "KANDA_V2C_PYTEST_PAYLOAD=",
        )
        require(
            pytest_payload.get("project_read") is True,
            "OS_FIRE_SHIELD_V2C_PYTEST_PROJECT_READ_ALLOWED",
        )
        require(
            pytest_payload.get("project_write_denied") is True,
            "OS_FIRE_SHIELD_V2C_PYTEST_PROJECT_WRITE_DENIED",
        )
        require(
            pytest_payload.get("tool_read_denied") is True,
            "OS_FIRE_SHIELD_V2C_PYTEST_TOOL_READ_DENIED",
        )
        require(
            pytest_payload.get("transient_write") is True,
            "OS_FIRE_SHIELD_V2C_PYTEST_TRANSIENT_WRITE_ALLOWED",
        )
        require(
            pytest_payload.get("cache_provider_disabled") is True,
            "OS_FIRE_SHIELD_V2C_PYTEST_CACHE_PROVIDER_DISABLED_LIVE",
        )
        require(
            Path(str(pytest_payload.get("python"))).resolve()
            == project_python.resolve(),
            "OS_FIRE_SHIELD_V2C_PYTEST_SELECTED_PROJECT_PYTHON_USED",
        )

        unittest_result = command_runner.run_tests(
            fixture,
            discovered,
            {
                "enabled": True,
                "runner": "unittest",
                "unittest_start_dir": "tests",
            },
        )[0]
        require(
            unittest_result.status == "pass",
            "OS_FIRE_SHIELD_V2C_UNITTEST_EXIT_ZERO",
        )
        unittest_payload = _payload(
            str(unittest_result.details.get("stdout") or ""),
            "KANDA_V2C_UNITTEST_PAYLOAD=",
        )
        require(
            unittest_payload.get("project_write_denied") is True,
            "OS_FIRE_SHIELD_V2C_UNITTEST_PROJECT_WRITE_DENIED",
        )
        require(
            unittest_payload.get("tool_read_denied") is True,
            "OS_FIRE_SHIELD_V2C_UNITTEST_TOOL_READ_DENIED",
        )
        require(
            unittest_payload.get("transient_write") is True,
            "OS_FIRE_SHIELD_V2C_UNITTEST_TRANSIENT_WRITE_ALLOWED",
        )
        require(
            Path(str(unittest_payload.get("python"))).resolve()
            == project_python.resolve(),
            "OS_FIRE_SHIELD_V2C_UNITTEST_SELECTED_PROJECT_PYTHON_USED",
        )

        after = _source_snapshot(fixture)
        require(
            before == after,
            "OS_FIRE_SHIELD_V2C_EXTERNAL_PROJECT_POST_STATE_UNCHANGED",
        )
        require(
            not (fixture / ".pytest_cache").exists(),
            "OS_FIRE_SHIELD_V2C_PYTEST_CACHE_NOT_CREATED",
        )
        require(
            not any(fixture.rglob("__pycache__")),
            "OS_FIRE_SHIELD_V2C_PROJECT_BYTECODE_CACHE_NOT_CREATED",
        )

        transient = canonical_transient_garbage_root(fixture)
        support = canonical_project_support_root(fixture)
        if transient.exists():
            shutil.rmtree(transient)
        if support.exists():
            shutil.rmtree(support)
        os.environ.pop("KANDA_V2C_TOOL_PROBE", None)

    require(
        tool_probe.read_bytes() == tool_before,
        "OS_FIRE_SHIELD_V2C_TOOL_POST_STATE_UNCHANGED",
    )
    print("OS_FIRE_SHIELD_V2C_EXTERNAL_TEST_EXECUTION_LIVE_VALIDATION: PASS")


def main() -> int:
    """Run focused static and optional live Windows validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    _anchor_validator_import_root(root)
    _static_validation(root)
    if not args.static_only:
        _external_live(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
