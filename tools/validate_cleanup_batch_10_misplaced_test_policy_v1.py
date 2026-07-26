# project-path: tools/validate_cleanup_batch_10_misplaced_test_policy_v1.py
"""Validate Cleanup Batch 10 misplaced-test policy wiring."""
from __future__ import annotations
import importlib.util, sys
from pathlib import Path
FEATURE_ID = "cleanup-batch-10-misplaced-test-policy-v1"

def fail(message: str) -> None:
    """Support fail behavior.
    
    Parameters
    ----------
    message : str
        The message text.
    """
    
    print("VALIDATION ERROR: " + message)
    raise SystemExit(1)

def load_module(root: Path):
    """Load the module.
    
    Parameters
    ----------
    root : Path
        The root path.
    """
    
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    import importlib
    return importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture_help.source_loader_private_impl"
    )

def main() -> None:
    """Support main behavior.
    """
    
    root = Path(__file__).resolve().parents[1]
    source_file = root / "kanda_reasoner_app/manage_architecture/manage_architecture_help/source_loader_private_impl.py"
    text = source_file.read_text(encoding="utf-8")
    if "def _apply_misplaced_test_policy" not in text:
        fail("missing misplaced-test policy patch function")
    if "TEST_COMPATIBILITY_SHIM_IMPORTS" not in text:
        fail("missing documented test compatibility shim import allowlist")
    module = load_module(root)
    decoded = module.load_manage_architecture_source()
    if '"validation/"' not in decoded:
        fail("decoded validator source does not include validation/ as canonical")
    for shim in [
        "kanda_reasoner_app.local_ai_json_working_copy",
        "kanda_reasoner_app.reasoner_context_bundle.source_archive_exporter",
    ]:
        if shim not in decoded:
            fail("decoded validator source missing shim allowlist entry: " + shim)
    if "if _is_documented_test_compatibility_shim_import(imported):" not in decoded:
        fail("decoded MISPLACED_TEST detector does not skip documented shim imports")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")

if __name__ == "__main__":
    main()
