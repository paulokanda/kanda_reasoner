# project-path: tests/test_architecture_warning_cleanup_batch20_public_api_instability_followup.py
"""Static smoke coverage for Batch 20 public API instability follow-up."""

from __future__ import annotations

import importlib

import scripts.validate_architecture_warning_cleanup_batch20_public_api_instability_followup_v1 as validate_module

repair_module = importlib.import_module(
    "scripts.repair_architecture_warning_cleanup_batch20_public_api_instability_followup_v1"
)


def test_batch20_followup_modules_expose_narrow_public_entrypoints() -> None:
    assert repair_module.__all__ == ["main"]
    assert validate_module.__all__ == ["main"]


def test_batch20_followup_repair_script_static_markers() -> None:
    text = repair_module.Path(repair_module.__file__).read_text(encoding="utf-8-sig")
    assert "exec(compile" not in text
    assert "_remove_empty_dunder_all" in text
    assert "refusing to remove non-empty __all__" in text
    assert "warnings.simplefilter(\"ignore\", SyntaxWarning)" in text


def test_batch20_followup_target_modules_are_named() -> None:
    assert repair_module.FACADE_OWNER_MODULE.endswith("zip_json_files_private_impl.py")
    assert any("zip_json_files_state_private_impl.py" in item for item in repair_module.TARGET_HELPERS)
    assert any("zip_json_files_process_private_impl.py" in item for item in repair_module.TARGET_HELPERS)
    assert any("zip_json_files_publish_private_impl.py" in item for item in repair_module.TARGET_HELPERS)
    assert any("zip_json_files_paths_private_impl.py" in item for item in repair_module.TARGET_HELPERS)


def test_batch20_followup_validator_imports() -> None:
    imported = importlib.import_module(
        "scripts.validate_architecture_warning_cleanup_batch20_public_api_instability_followup_v1"
    )
    assert imported.FEATURE_ID == "architecture-warning-cleanup-batch20-public-api-instability-followup-v1"
