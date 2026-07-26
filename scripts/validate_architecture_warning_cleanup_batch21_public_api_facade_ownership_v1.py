# project-path: scripts/validate_architecture_warning_cleanup_batch21_public_api_facade_ownership_v1.py
"""Focused validator for Batch 21 public API facade ownership cleanup."""

from __future__ import annotations

import ast
import py_compile
import subprocess
import sys
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "architecture-warning-cleanup-batch21-public-api-facade-ownership-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE_VALIDATOR = PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture.py"

TOUCHED_FILES = (
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_models.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_paths.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_report.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_runner.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_sidecars.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_source_map.py",
    "kanda_reasoner_app/project_analysis_evidence_paths.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/file_retrieval.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_private_impl.py",
    "kanda_reasoner_app/routing_signal_scorer/advisory.py",
    "kanda_reasoner_app/routing_signal_scorer/contract.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_record_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_finalization_closure_shield.py",
    "kanda_reasoner_app/routing_signal_scorer/models.py",
    "kanda_reasoner_app/routing_signal_scorer/scoring.py",
    "kanda_reasoner_app/routing_signal_scorer/shield.py",
    "kanda_reasoner_app/routing_signal_scorer/similarity_preview.py",
    "scripts/validate_architecture_warning_cleanup_batch19_static_coverage_exports_v1.py",
    "scripts/validate_architecture_warning_cleanup_batch21_public_api_facade_ownership_v1.py",
)

PROVIDER_EMPTY_ALL_FILES = (
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_models.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_paths.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_report.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_runner.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_sidecars.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_source_map.py",
    "kanda_reasoner_app/routing_signal_scorer/advisory.py",
    "kanda_reasoner_app/routing_signal_scorer/models.py",
    "kanda_reasoner_app/routing_signal_scorer/scoring.py",
    "kanda_reasoner_app/routing_signal_scorer/shield.py",
    "kanda_reasoner_app/routing_signal_scorer/similarity_preview.py",
    "scripts/validate_architecture_warning_cleanup_batch19_static_coverage_exports_v1.py",
)

FACADE_PUBLIC_ALIAS_FILES = (
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py",
    "kanda_reasoner_app/project_analysis_evidence_paths.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/file_retrieval.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_private_impl.py",
    "kanda_reasoner_app/routing_signal_scorer/contract.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_record_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_finalization_closure_shield.py",
)

KNOWN_REMAINING_MISSING_PUBLIC_SURFACE_PATHS = (
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_state_private_impl.py",
)


def require(condition: bool, message: str) -> None:
    """Raise AssertionError when a validation condition fails."""
    if not condition:
        raise AssertionError(message)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _literal_dunder_all(path: Path) -> list[str] | None:
    tree = ast.parse(_read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = ast.literal_eval(node.value)
                    require(isinstance(value, (list, tuple)), f"{path}: __all__ is not a literal sequence")
                    require(all(isinstance(item, str) for item in value), f"{path}: __all__ contains non-string entries")
                    return list(value)
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__":
                value = ast.literal_eval(node.value)
                require(isinstance(value, (list, tuple)), f"{path}: __all__ is not a literal sequence")
                require(all(isinstance(item, str) for item in value), f"{path}: __all__ contains non-string entries")
                return list(value)
    return None


def validate_py_compile() -> None:
    """Compile all touched files without importing GUI-heavy modules."""
    for relative in TOUCHED_FILES:
        path = PROJECT_ROOT / relative
        require(path.is_file(), f"Missing touched file: {relative}")
        py_compile.compile(str(path), doraise=True)


def validate_line_counts() -> None:
    """Ensure the patch does not create any over-500-line touched module."""
    for relative in TOUCHED_FILES:
        path = PROJECT_ROOT / relative
        line_count = len(_read_text(path).splitlines())
        require(line_count <= 500, f"Touched file exceeds 500 lines: {relative} ({line_count})")


def validate_provider_empty_public_surface() -> None:
    """Ensure provider modules do not become duplicate public owners."""
    for relative in PROVIDER_EMPTY_ALL_FILES:
        exported = _literal_dunder_all(PROJECT_ROOT / relative)
        require(exported == [], f"{relative} must use __all__ = [] for facade-owned public surface")


def validate_facade_alias_pattern() -> None:
    """Ensure facades bind public names locally from private aliases."""
    for relative in FACADE_PUBLIC_ALIAS_FILES:
        text = _read_text(PROJECT_ROOT / relative)
        require("_public_" in text, f"Missing _public_ alias pattern in {relative}")
        require("__all__" in text, f"Missing facade __all__ in {relative}")


def validate_architecture_public_api_cleanup() -> None:
    """Run the architecture validator and require the target warning family to be gone."""
    result = subprocess.run(
        [sys.executable, str(ARCHITECTURE_VALIDATOR), "--root", str(PROJECT_ROOT), "--validate"],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    require(result.returncode == 0, output)
    require("Errors: 0" in output, output)
    require("PUBLIC_API_INSTABILITY" not in output, output)
    require("DUPLICATE_PUBLIC_SYMBOL" not in output, output)
    require("CROSS_BOX_PUBLIC_SYMBOL_COLLISION" not in output, output)

    for line in output.splitlines():
        if "MISSING_PUBLIC_SURFACE_CONTROL" not in line:
            continue
        stripped = line.strip()
        if stripped.startswith("MISSING_PUBLIC_SURFACE_CONTROL:"):
            continue
        if "Issue counts by code" in line:
            continue
        if any(path in line for path in KNOWN_REMAINING_MISSING_PUBLIC_SURFACE_PATHS):
            continue
        raise AssertionError("Unexpected missing public-surface warning: " + line)


def main() -> int:
    """Run the focused Batch 21 validation gates."""
    validate_py_compile()
    validate_line_counts()
    validate_provider_empty_public_surface()
    validate_facade_alias_pattern()
    validate_architecture_public_api_cleanup()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
