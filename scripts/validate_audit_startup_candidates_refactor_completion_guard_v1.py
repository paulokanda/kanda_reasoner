"""Validate Audit Startup Candidates Refactor Completion Guard v1."""

from __future__ import annotations

import builtins
import importlib
import json
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "audit-startup-candidates-refactor-completion-guard-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"

EXPECTED_MODULES = {
    "audit_startup_candidates.py",
    "audit_startup_candidates_models.py",
    "audit_startup_candidates_paths.py",
    "audit_startup_candidates_source_map.py",
    "audit_startup_candidates_sidecars.py",
    "audit_startup_candidates_report.py",
    "audit_startup_candidates_runner.py",
}
MAX_LINES = 500
FACADE_MAX_LINES = 130
HELPER_MIN_LINES = 80
HELPER_MIN_EXCEPTIONS = {"audit_startup_candidates_paths.py"}

EXPECTED_PUBLIC = {
    "allowed_scan_roots",
    "append_items",
    "ask_yes_no",
    "atomic_write_text",
    "AuditResult",
    "compare_candidates_to_source_map",
    "create_report",
    "detect_stale_entries",
    "detect_workspace_root",
    "explain_missing_candidates",
    "find_sidecar_candidates",
    "handle_interactive_update",
    "is_hidden_or_cache_path",
    "is_relative_to_safe",
    "is_valid_workspace",
    "load_source_map_object",
    "normalize_rel_path",
    "parse_args",
    "parse_source_map",
    "proposed_entry_for_candidate",
    "read_json_file",
    "read_text_utf8_strict",
    "run_audit",
    "run_sync_generator",
    "sha256_file",
    "sidecar_to_candidate",
    "SourceMapEntry",
    "StartupCandidate",
    "suggested_next_filename_number",
    "suggested_next_load_order",
    "update_source_map_with_candidates",
    "validate_candidate_set",
    "write_text_utf8",
}

OWNERSHIP_MARKERS = {
    "audit_startup_candidates.py": [
        "Thin compatibility facade",
        "__package__",
        "audit_startup_candidates_runner",
        "if __name__ == \"__main__\"",
    ],
    "audit_startup_candidates_models.py": [
        "class SourceMapEntry",
        "class StartupCandidate",
        "class AuditResult",
        "def read_text_utf8_strict",
        "def write_text_utf8",
        "def sha256_file",
        "def utc_now_iso",
    ],
    "audit_startup_candidates_paths.py": [
        "def normalize_rel_path",
        "def is_hidden_or_cache_path",
        "def is_relative_to_safe",
        "def detect_workspace_root",
        "def is_valid_workspace",
    ],
    "audit_startup_candidates_source_map.py": [
        "def parse_source_map",
        "def detect_stale_entries",
        "def load_source_map_object",
        "def suggested_next_load_order",
        "def suggested_next_filename_number",
    ],
    "audit_startup_candidates_sidecars.py": [
        "def allowed_scan_roots",
        "ALLOWED_SCAN_DIRS",
        "def sidecar_to_candidate",
        "startup_kernel_include",
        "def find_sidecar_candidates",
        "def validate_candidate_set",
        "def compare_candidates_to_source_map",
    ],
    "audit_startup_candidates_report.py": [
        "def create_report",
        "Suggested JSON entry",
        "def explain_missing_candidates",
        "def ask_yes_no",
        "Type YES",
        "answer.strip() == \"YES\"",
    ],
    "audit_startup_candidates_runner.py": [
        "def run_audit",
        "def update_source_map_with_candidates",
        "def run_sync_generator",
        "--ensure-sync",
        "--yes",
        "def handle_interactive_update",
        "def parse_args",
        "def main",
    ],
}


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_completion_shape() -> None:
    actual = {path.name for path in PROMPT_TOOLS.glob("audit_startup_candidates*.py")}
    missing = EXPECTED_MODULES - actual
    unexpected = actual - EXPECTED_MODULES
    if missing:
        raise AssertionError(("missing audit-startup-candidates modules", sorted(missing)))
    if unexpected:
        raise AssertionError(("unexpected audit-startup-candidates helper sprawl", sorted(unexpected)))

    counts = {name: _line_count(PROMPT_TOOLS / name) for name in sorted(EXPECTED_MODULES)}
    if counts["audit_startup_candidates.py"] > FACADE_MAX_LINES:
        raise AssertionError(("facade too large", counts["audit_startup_candidates.py"], counts))
    for name, count in counts.items():
        if count > MAX_LINES:
            raise AssertionError(("module exceeds v7.2 500-line maximum", name, count))
    for name in sorted(EXPECTED_MODULES - {"audit_startup_candidates.py"} - HELPER_MIN_EXCEPTIONS):
        if counts[name] < HELPER_MIN_LINES:
            raise AssertionError(("substantive helper is suspiciously tiny", name, counts[name]))


def _assert_facade_contract() -> None:
    facade = _read(PROMPT_TOOLS / "audit_startup_candidates.py")
    forbidden_defs = [
        "def run_audit",
        "def update_source_map_with_candidates",
        "def run_sync_generator",
        "def sidecar_to_candidate",
        "def find_sidecar_candidates",
        "def create_report",
        "def parse_source_map",
    ]
    for marker in forbidden_defs:
        if marker in facade:
            raise AssertionError(("facade owns runtime logic", marker))
    for marker in ["main", "__all__", "audit_startup_candidates_runner"]:
        if marker not in facade:
            raise AssertionError(("facade missing compatibility marker", marker))


def _assert_ownership_markers() -> None:
    for filename, markers in OWNERSHIP_MARKERS.items():
        text = _read(PROMPT_TOOLS / filename)
        for marker in markers:
            if marker not in text:
                raise AssertionError(("missing ownership marker", filename, marker))


def _assert_no_freeze_memory_writes() -> None:
    forbidden = [
        "project_freeze_ledger",
        "frozen_features_memory",
        "freeze_hint_intake",
        "project_freeze_after_update",
    ]
    for path in (PROMPT_TOOLS / name for name in EXPECTED_MODULES):
        text = _read(path)
        for token in forbidden:
            if token in text:
                raise AssertionError(("startup candidate auditor must not touch freeze memory", path.name, token))


def _make_workspace(base: Path) -> Path:
    workspace = base / "kanda_prompt_workspace"
    tools = workspace / "prompt_tools"
    active = workspace / "prompt_library" / "ACTIVE_PROMPTS" / "demo"
    routing = workspace / "prompt_library" / "ROUTING" / "ignored"
    hidden = workspace / "prompt_library" / "ACTIVE_PROMPTS" / "__pycache__"
    tools.mkdir(parents=True)
    active.mkdir(parents=True)
    routing.mkdir(parents=True)
    hidden.mkdir(parents=True)

    (tools / "STARTUP_ROUTING_KERNEL_SOURCES.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "startup_sources": [
                    {
                        "load_order": 1,
                        "canonical_source": "prompt_library/ACTIVE_PROMPTS/existing.md",
                        "generated_filename": "01_existing.md",
                        "prompt_id": "existing",
                        "load_mode": "always_startup",
                        "role": "Existing startup prompt",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (tools / "sync_startup_routing_kernel_pack.py").write_text(
        "from pathlib import Path\nPath('SYNC_WAS_RUN.txt').write_text('sync ok', encoding='utf-8')\nraise SystemExit(0)\n",
        encoding="utf-8",
    )

    (active / "new_prompt.md").write_text("# New prompt\n", encoding="utf-8")
    (active / "new_prompt.meta.json").write_text(
        json.dumps(
            {
                "startup_kernel_include": True,
                "startup_load_mode": "always_startup",
                "startup_generated_filename": "02_new_prompt.md",
                "prompt_id": "new_prompt",
                "startup_role": "New startup prompt",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (routing / "not_included.md").write_text("# ignored\n", encoding="utf-8")
    (routing / "not_included.meta.json").write_text(
        json.dumps({"startup_kernel_include": False}, indent=2) + "\n",
        encoding="utf-8",
    )
    (hidden / "hidden.md").write_text("# hidden\n", encoding="utf-8")
    (hidden / "hidden.meta.json").write_text(
        json.dumps({"startup_kernel_include": True}, indent=2) + "\n",
        encoding="utf-8",
    )
    return workspace


def _source_map_text(workspace: Path) -> str:
    return (workspace / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json").read_text(encoding="utf-8")


def _assert_public_api() -> object:
    sys.path.insert(0, str(PROJECT_ROOT))
    module = importlib.import_module("kanda_prompt_workspace.prompt_tools.audit_startup_candidates")
    missing = sorted(name for name in EXPECTED_PUBLIC if not hasattr(module, name))
    if missing:
        raise AssertionError(("facade missing public compatibility names", missing))
    return module


def _assert_report_only_and_interactive_gates(module: object) -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_audit_startup_completion_guard_") as tmp_text:
        workspace = _make_workspace(Path(tmp_text))
        before = _source_map_text(workspace)

        code, status, report_path, entries, result = module.run_audit(workspace, "REPORT.md")
        if code != 1 or status != "UPDATE_CANDIDATE_FOUND":
            raise AssertionError(("unexpected synthetic audit status", code, status))
        if len(result.missing_candidates) != 1:
            raise AssertionError(("expected exactly one missing candidate", len(result.missing_candidates)))
        report_text = report_path.read_text(encoding="utf-8")
        for marker in [
            "Source-map errors",
            "Candidate errors",
            "Warnings",
            "Stale source-map entries",
            "Existing marked candidates",
            "Missing startup candidates",
            "Ignored sidecars",
            "Suggested JSON entry",
        ]:
            if marker not in report_text:
                raise AssertionError(("report missing required section/marker", marker))
        if _source_map_text(workspace) != before:
            raise AssertionError("run_audit/report write mutated the source map")

        report_code = module.main(["--workspace", str(workspace), "--report", "--report-filename", "REPORT_ONLY.md"])
        if report_code != 1:
            raise AssertionError(("report-only mode should return update-candidate status without updating", report_code))
        if _source_map_text(workspace) != before:
            raise AssertionError("--report mode mutated STARTUP_ROUTING_KERNEL_SOURCES.json")

        no_interactive_code = module.main([
            "--workspace",
            str(workspace),
            "--no-interactive",
            "--report-filename",
            "NO_INTERACTIVE.md",
        ])
        if no_interactive_code != 1:
            raise AssertionError(("no-interactive mode should return update-candidate status without updating", no_interactive_code))
        if _source_map_text(workspace) != before:
            raise AssertionError("--no-interactive mode mutated STARTUP_ROUTING_KERNEL_SOURCES.json")

        original_input = builtins.input
        try:
            builtins.input = lambda _prompt="": "yes"
            lower_yes_code = module.handle_interactive_update(workspace, entries, result)
            if lower_yes_code != 1:
                raise AssertionError(("lowercase yes must not pass exact YES gate", lower_yes_code))
            if _source_map_text(workspace) != before:
                raise AssertionError("lowercase yes bypassed exact YES gate")

            builtins.input = lambda _prompt="": "YES"
            yes_code = module.handle_interactive_update(workspace, entries, result)
            if yes_code != 0:
                raise AssertionError(("exact YES interactive update failed", yes_code))
        finally:
            builtins.input = original_input

        updated = json.loads(_source_map_text(workspace))
        if len(updated.get("startup_sources", [])) != 2:
            raise AssertionError("exact YES did not append exactly one candidate")
        if not (workspace / "SYNC_WAS_RUN.txt").exists():
            raise AssertionError("sync_startup_routing_kernel_pack.py was not invoked after exact YES update")


def _assert_atomic_rollback(module: object) -> None:
    runner = importlib.import_module("kanda_prompt_workspace.prompt_tools.audit_startup_candidates_runner")
    with tempfile.TemporaryDirectory(prefix="kanda_audit_startup_rollback_guard_") as tmp_text:
        workspace = _make_workspace(Path(tmp_text))
        before = _source_map_text(workspace)
        _code, _status, _report_path, entries, result = module.run_audit(workspace, "ROLLBACK_REPORT.md")
        real_parse = runner.parse_source_map
        try:
            runner.parse_source_map = lambda _path: ([], ["forced post-write validation failure"], [])
            try:
                module.update_source_map_with_candidates(workspace, entries, result.missing_candidates)
            except ValueError:
                pass
            else:
                raise AssertionError("forced post-write validation failure did not raise")
        finally:
            runner.parse_source_map = real_parse
        if _source_map_text(workspace) != before:
            raise AssertionError("source-map update rollback failed after validation failure")


def main() -> int:
    _assert_completion_shape()
    _assert_facade_contract()
    _assert_ownership_markers()
    _assert_no_freeze_memory_writes()
    module = _assert_public_api()
    _assert_report_only_and_interactive_gates(module)
    _assert_atomic_rollback(module)
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
