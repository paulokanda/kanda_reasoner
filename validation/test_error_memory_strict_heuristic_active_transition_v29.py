"""Validate Error Memory strict heuristic active transition patch v29."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import py_compile
import sys
import types

FEATURE_ID = "error-memory-strict-heuristic-active-transition-v29"
EXPECTED_MARKER = "VALIDATION OK: " + FEATURE_ID

SAMPLE_DRAFT = {
    "correct_fix": "Update the method that produces the GUI readiness/state dictionary so it always includes ml_pilot_activation_state. Then rerun validation to confirm the key is present.",
    "created_at_utc": "2026-06-25T06:09:53Z",
    "do_not_repeat_rule": "Do not add a new validation-visible GUI key only to tests or validation logic. The method that produces the GUI state must return the key consistently.",
    "exception": {
        "function_or_test_name": "",
        "message_normalized": "'ml_pilot_activation_state'",
        "phase": "validation",
        "relative_file_path": "",
        "stacktrace_scrubbed": "Validation failed with KeyError for missing ml_pilot_activation_state.\n\nKeyError: 'ml_pilot_activation_state'",
        "type": "KeyError",
    },
    "fingerprint": {
        "components": ["KeyError", "", "", "validation", "'ml_pilot_activation_state'"],
        "fingerprint_hash": "91a62fadead964cde67219dde52e1642ded4b95718fbc0580eaebc2c79c27c14",
        "strategy": "v1_structural_conservative",
    },
    "install_command_summary": "",
    "lesson_id": "lesson-05cffd935c8b",
    "long_term_prevention": "When adding any validation-visible GUI key, update the producer method, the consumer/test logic, and the regression validation in the same patch.",
    "notes": "Draft lesson created from a failed validation message. This is not a validated correction yet. Keep as draft until a correction patch passes validation with VALIDATION OK and STATUS: IN_SYNC.",
    "operation_phase": "validation",
    "prevention_triggers": [
        "KeyError for missing GUI state key",
        "missing ml_pilot_activation_state",
        "validation-visible GUI key",
        "test expects key but producer does not return it",
        "producer and validation mismatch",
    ],
    "project_slug": "kanda_reasoner",
    "promotion_status": "not_candidate",
    "raw_error_snapshot_scrubbed": "Validation failed with KeyError for missing ml_pilot_activation_state.\n\nKeyError: 'ml_pilot_activation_state'",
    "raw_error_text": "Validation failed with KeyError for missing ml_pilot_activation_state.\n\nKeyError: 'ml_pilot_activation_state'",
    "redaction": {
        "applied": True,
        "export_safe": True,
        "rules": ["Draft preserved from incomplete Error Memory editor JSON; review redaction before active promotion."],
    },
    "regression_check": {
        "command": "",
        "expected_marker": "",
        "required_before_freeze": False,
        "type": "not_available",
    },
    "related_freeze_ids": [],
    "root_cause": "A validation-visible GUI state key was expected, but the method that produces the GUI state did not return ml_pilot_activation_state consistently.",
    "schema_version": "1.0",
    "source_patch_zip": "",
    "status": "draft",
    "superseded_by": "",
    "symptom": "Validation failed with KeyError for missing ml_pilot_activation_state.",
    "updated_at_utc": "2026-06-27T00:13:33Z",
    "validation_command_summary": "",
    "validation_evidence": ["Validation failed before correction with KeyError for missing ml_pilot_activation_state."],
    "wrong_assumption": "The implementation likely updated the validation or test expectation without updating the GUI state-producing method.",
}


def require(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear message when condition is false."""
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    """Read UTF-8 text with replacement for robust validation."""
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    sys.path.insert(0, str(project_root))

    source_files = [
        project_root / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py",
        project_root / "kanda_reasoner_app" / "error_memory" / "heuristic_normalizer.py",
        project_root / "kanda_reasoner_app" / "error_memory" / "models.py",
    ]
    for source_path in source_files:
        require(source_path.exists(), str(source_path) + " not found")
        py_compile.compile(str(source_path), doraise=True)

    tab_text = read_text(source_files[0])
    normalizer_text = read_text(source_files[1])
    models_text = read_text(source_files[2])

    require("from .models import active_ready_missing_reasons" in normalizer_text, "normalizer does not use central active-ready guard")
    require("Deterministic normalization would only produce a draft" in normalizer_text, "normalizer draft-only block missing")
    require("can_apply=False" in normalizer_text, "normalizer does not block draft-only heuristic apply")
    require("regression_check.type must be validation_command for active-ready lessons" in models_text, "active-ready validator allows not_available regression checks")
    require("regression_check.command must use forward slashes" in models_text, "active-ready validator lacks slash-only command guard")
    require("The formatted lesson parsed from " in tab_text, "Memorize Error draft warning path missing")
    require("will not re-save draft-only lessons as progress" in tab_text, "Memorize Error still permits draft loop wording")
    require("lesson[\"status\"] = \"active\"" in tab_text, "Memorize Error does not promote active-ready payloads to active before save")

    for old in (
        "Level 1 deterministic correction applied",
        "Saved draft Error Memory lesson from Error Editor",
        "The corrected lesson is still a draft. Click Memorize Error or Mark Draft",
    ):
        require(old not in tab_text, "old misleading GUI text remains: " + old)

    package = types.ModuleType("kanda_reasoner_app")
    package.__path__ = [str(project_root / "kanda_reasoner_app")]
    sys.modules["kanda_reasoner_app"] = package
    error_memory_package = types.ModuleType("kanda_reasoner_app.error_memory")
    error_memory_package.__path__ = [str(project_root / "kanda_reasoner_app" / "error_memory")]
    sys.modules["kanda_reasoner_app.error_memory"] = error_memory_package
    evidence_paths = types.ModuleType("kanda_reasoner_app.project_analysis_evidence_paths")
    evidence_paths.project_name_from_root = lambda value: Path(value).name
    sys.modules["kanda_reasoner_app.project_analysis_evidence_paths"] = evidence_paths
    fingerprint = types.ModuleType("kanda_reasoner_app.error_memory.fingerprint")
    fingerprint.build_fingerprint = lambda *args, **kwargs: {}
    fingerprint.extract_exception_info = lambda *args, **kwargs: {}
    sys.modules["kanda_reasoner_app.error_memory.fingerprint"] = fingerprint
    scrubber = types.ModuleType("kanda_reasoner_app.error_memory.scrubber")
    scrubber.scrub_text = lambda value: str(value or "")
    sys.modules["kanda_reasoner_app.error_memory.scrubber"] = scrubber

    models_spec = importlib.util.spec_from_file_location(
        "kanda_reasoner_app.error_memory.models",
        project_root / "kanda_reasoner_app" / "error_memory" / "models.py",
    )
    require(models_spec is not None and models_spec.loader is not None, "could not load models spec")
    models_module = importlib.util.module_from_spec(models_spec)
    sys.modules["kanda_reasoner_app.error_memory.models"] = models_module
    models_spec.loader.exec_module(models_module)

    heuristic_spec = importlib.util.spec_from_file_location(
        "kanda_reasoner_app.error_memory.heuristic_normalizer",
        project_root / "kanda_reasoner_app" / "error_memory" / "heuristic_normalizer.py",
    )
    require(heuristic_spec is not None and heuristic_spec.loader is not None, "could not load heuristic spec")
    heuristic_module = importlib.util.module_from_spec(heuristic_spec)
    sys.modules["kanda_reasoner_app.error_memory.heuristic_normalizer"] = heuristic_module
    heuristic_spec.loader.exec_module(heuristic_module)

    classify_and_normalize_error_lesson_text = heuristic_module.classify_and_normalize_error_lesson_text
    active_ready_missing_reasons = models_module.active_ready_missing_reasons

    result = classify_and_normalize_error_lesson_text(
        json.dumps(SAMPLE_DRAFT),
        project_slug="kanda_reasoner",
        now_factory=lambda: "2026-06-27T00:00:00Z",
        id_factory=lambda: "lesson-test-fixed",
    )
    require(result.label == "Need AI to Correct", "sample draft should route to Need AI to Correct")
    require(result.can_apply is False, "sample draft should not enable Heuristic Correction")
    require(result.lesson is not None, "blocked sample should preserve normalized draft for review")
    require(result.lesson.get("promotion_status") == "needs_ai_review", "blocked sample should be marked needs_ai_review")
    missing = active_ready_missing_reasons(dict(result.lesson))
    require("source_patch_zip is empty" in missing, "sample draft should report empty source_patch_zip")
    require("validation_command_summary is empty" in missing, "sample draft should report empty validation_command_summary")
    require("regression_check.type must be validation_command for active-ready lessons" in missing, "sample draft should reject not_available regression check")
    require("regression_check.command is empty for validation_command" in missing, "sample draft should require regression_check.command")
    require("regression_check.expected_marker is empty for validation_command" in missing, "sample draft should require regression_check.expected_marker")

    manifest_text = read_text(project_root / "bundle_manifest.json")
    require("python validation/test_error_memory_strict_heuristic_active_transition_v29.py" in manifest_text, "bundle manifest does not use forward-slash validation command")

    print(EXPECTED_MARKER)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
