"""Validate audit startup candidates refactor train car 1."""

from __future__ import annotations

import importlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "audit-startup-candidates-refactor-train-car-1-v1"
ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = ROOT / "kanda_prompt_workspace" / "prompt_tools"

FILES = [
    PROMPT_TOOLS / "audit_startup_candidates.py",
    PROMPT_TOOLS / "audit_startup_candidates_models.py",
    PROMPT_TOOLS / "audit_startup_candidates_paths.py",
    PROMPT_TOOLS / "audit_startup_candidates_source_map.py",
    PROMPT_TOOLS / "audit_startup_candidates_sidecars.py",
    PROMPT_TOOLS / "audit_startup_candidates_report.py",
    PROMPT_TOOLS / "audit_startup_candidates_runner.py",
]

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
    "audit_startup_candidates.py": ["Thin compatibility facade", "__package__"],
    "audit_startup_candidates_models.py": ["class SourceMapEntry", "class StartupCandidate", "def sha256_file"],
    "audit_startup_candidates_paths.py": ["def detect_workspace_root", "def is_relative_to_safe"],
    "audit_startup_candidates_source_map.py": ["def parse_source_map", "def detect_stale_entries"],
    "audit_startup_candidates_sidecars.py": ["def sidecar_to_candidate", "def validate_candidate_set"],
    "audit_startup_candidates_report.py": ["def create_report", "def ask_yes_no", "Type YES"],
    "audit_startup_candidates_runner.py": ["def run_audit", "def run_sync_generator", "--ensure-sync"],
}


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _make_workspace(base: Path) -> Path:
    workspace = base / "kanda_prompt_workspace"
    prompt_tools = workspace / "prompt_tools"
    prompt_dir = workspace / "prompt_library" / "ACTIVE_PROMPTS" / "demo"
    prompt_tools.mkdir(parents=True)
    prompt_dir.mkdir(parents=True)
    shutil.copytree(PROMPT_TOOLS, prompt_tools, dirs_exist_ok=True)
    (prompt_tools / "STARTUP_ROUTING_KERNEL_SOURCES.json").write_text(
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
    (prompt_dir / "new_prompt.md").write_text("# New prompt\n", encoding="utf-8")
    (prompt_dir / "new_prompt.meta.json").write_text(
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
    (prompt_tools / "sync_startup_routing_kernel_pack.py").write_text(
        "import sys\nraise SystemExit(0)\n",
        encoding="utf-8",
    )
    return workspace


def main() -> int:
    missing = [str(path) for path in FILES if not path.exists()]
    if missing:
        raise SystemExit("Missing expected files: " + ", ".join(missing))

    for path in FILES:
        lines = _line_count(path)
        if lines > 500:
            raise SystemExit(f"{path.relative_to(ROOT)} exceeds v7.2 500-line maximum: {lines}")

    facade_text = (PROMPT_TOOLS / "audit_startup_candidates.py").read_text(encoding="utf-8")
    if "def run_audit" in facade_text or "def sidecar_to_candidate" in facade_text:
        raise SystemExit("audit_startup_candidates.py must remain a thin facade, not own runtime logic.")

    for filename, markers in OWNERSHIP_MARKERS.items():
        text = (PROMPT_TOOLS / filename).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                raise SystemExit(f"Missing ownership marker {marker!r} in {filename}")

    sys.path.insert(0, str(ROOT))
    module = importlib.import_module("kanda_prompt_workspace.prompt_tools.audit_startup_candidates")
    missing_public = sorted(name for name in EXPECTED_PUBLIC if not hasattr(module, name))
    if missing_public:
        raise SystemExit("Facade missing public compatibility names: " + ", ".join(missing_public))

    with tempfile.TemporaryDirectory() as tmp:
        workspace = _make_workspace(Path(tmp))
        sys.path.insert(0, str(workspace.parent))
        code, status, report_path, entries, result = module.run_audit(workspace, "REPORT.md")
        if code != 1 or status != "UPDATE_CANDIDATE_FOUND":
            raise SystemExit(f"Unexpected audit status: code={code}, status={status}")
        if len(entries) != 1 or len(result.missing_candidates) != 1:
            raise SystemExit("Synthetic audit did not preserve missing-candidate detection.")
        if not report_path.exists() or "Suggested JSON entry" not in report_path.read_text(encoding="utf-8"):
            raise SystemExit("Synthetic audit did not write the expected report.")
        updated_path = module.update_source_map_with_candidates(workspace, entries, result.missing_candidates)
        updated = json.loads(updated_path.read_text(encoding="utf-8"))
        if len(updated["startup_sources"]) != 2:
            raise SystemExit("Source-map update did not append exactly one candidate.")
        if module.run_sync_generator(workspace) != 0:
            raise SystemExit("Sync generator invocation did not preserve successful return code.")

    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
