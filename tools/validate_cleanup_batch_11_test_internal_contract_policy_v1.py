# project-path: tools/validate_cleanup_batch_11_test_internal_contract_policy_v1.py
"""Validate Cleanup Batch 11 test-internal contract policy wiring."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Sequence

__all__ = [
    "main",
]

FEATURE_ID = "cleanup-batch-11-test-internal-contract-policy-v1"
MAX_MODULE_LINES = 500
SOURCE_LOADER_PATH = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "source_loader_private_impl.py"
)
WARNING_POLICY_PATH = Path(
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "source_loader_warning_policy_private_impl.py"
)


def fail(message: str) -> None:
    """Print a deterministic validation error and stop."""
    print("VALIDATION ERROR: " + message)
    raise SystemExit(1)


def _read_module(root: Path, relative_path: Path) -> str:
    """Read one required module and enforce its line limit."""
    path = root / relative_path
    if not path.is_file():
        fail("required module is missing: " + relative_path.as_posix())
    text = path.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    if line_count > MAX_MODULE_LINES:
        fail(
            relative_path.name
            + " exceeds 500 lines: "
            + str(line_count)
        )
    compile(text, str(path), "exec")
    return text


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        help="Project root. Defaults to the validator parent project.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the preserved Cleanup Batch 11 validation contract."""
    args = build_parser().parse_args(argv)
    root = (
        Path(args.project_root).expanduser().resolve()
        if args.project_root
        else Path(__file__).resolve().parents[1]
    )
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    loader_text = _read_module(root, SOURCE_LOADER_PATH)
    policy_text = _read_module(root, WARNING_POLICY_PATH)

    required_loader_markers = (
        "apply_manage_architecture_warning_policies",
        "source_loader_warning_policy_private_impl",
    )
    for marker in required_loader_markers:
        if marker not in loader_text:
            fail("missing source-loader delegation marker: " + marker)

    required_policy_markers = (
        "def _apply_test_protection_generated_private_policy",
        "def _apply_stale_variant_compatibility_shim_policy",
        "def _apply_generated_artifact_bundle_temp_manifest_policy",
        "def _apply_test_contract_cleanup_policy",
    )
    for marker in required_policy_markers:
        if marker not in policy_text:
            fail("missing warning-policy owner marker: " + marker)

    importlib.invalidate_caches()
    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture_help."
        "source_loader_private_impl"
    )
    decoded = module.load_manage_architecture_source()
    decoded_required = (
        "COMPATIBILITY_SHIM_STALE_VARIANT_PATHS",
        "TEST_COMPATIBILITY_SHIM_IMPORTS",
        "TEST_INTERNAL_DETAIL_ALLOWED_IMPORTS",
        "TEST_INTERNAL_DETAIL_ALLOWED_ATTRIBUTES",
        '"validation/"',
        "_is_documented_test_compatibility_shim_import(imported)",
        "_is_documented_test_internal_import(",
        "_is_documented_test_internal_attribute(",
        "kanda_reasoner_app.reasoner_context_bundle.source_archive_exporter",
        "kanda_reasoner_app.local_ai_json_working_copy",
        "_validate_error_memory_lesson_payload",
        "_similarity_level",
        "_prefs_path",
        "_refresh_bundle_manifest_after_publish_rewrite",
        "_check_bundle_if_requested",
        "_finalize_ai_context_artifacts_for_handoff",
        "_WindowProjectRootMixin",
    )
    for marker in decoded_required:
        if marker not in decoded:
            fail("decoded architecture source missing marker: " + marker)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
