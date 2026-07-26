# project-path: tools/validate_error_memory_local_ai_corrector_retry_v4.py
"""Focused validation for Error Memory local AI evidence recovery v4."""

from __future__ import annotations

import ast
import importlib
import json
import py_compile
import sys
import tempfile
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

TOUCHED_FILES = [
    "kanda_reasoner_app/error_memory_gui/_ai_evidence_recovery.py",
    "kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py",
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "kanda_reasoner_app/error_memory_gui/_ai_corrector_service.py",
    "tools/validate_error_memory_local_ai_corrector_retry_v4.py",
]


def _assert(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear message when condition is false."""
    if not condition:
        raise AssertionError(message)


def _line_count(path: Path) -> int:
    """Return physical line count for a source file."""
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def _sample_lesson() -> dict[str, Any]:
    """Return a representative lesson for parser and corrector tests."""
    return {
        "schema_version": "1.0",
        "project_slug": "kanda_reasoner",
        "lesson_id": "lesson-batch17-freeze-hint-repair-target-mismatch-v2",
        "status": "draft",
        "superseded_by": "",
        "operation_phase": "freeze_hint_preparation",
        "created_at_utc": "2026-07-01T02:40:00Z",
        "updated_at_utc": "2026-07-01T02:40:00Z",
        "source_patch_zip": "kanda_architecture_warning_cleanup_batch17_line_count_smoke_v1_patch.zip",
        "raw_error_text": "FREEZE BLOCKED - no recognizable validation evidence found.",
        "raw_error_snapshot_scrubbed": "Preview still read old paraphrased evidence.",
        "symptom": "Preview Freeze Entry continued to block.",
        "root_cause": "The repair targeted one guessed freeze-hint file.",
        "wrong_assumption": "Assumed one exact freeze hint filename was active.",
        "correct_fix": "Search all Batch 17 freeze-intake JSON files.",
        "do_not_repeat_rule": "Do not repair freeze evidence by guessing one filename.",
        "long_term_prevention": "Update every matching freeze-hint JSON for the feature.",
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets included."],
        },
        "exception": {
            "type": "FreezeEvidenceRecognitionError",
            "phase": "freeze_hint_preparation",
            "relative_file_path": "project_freeze_after_update/freeze_hint_intake",
            "function_or_test_name": "Preview Freeze Entry",
            "message_normalized": "FREEZE BLOCKED - no recognizable validation evidence found.",
            "stacktrace_scrubbed": "No traceback; GUI preview blocked the freeze.",
        },
        "fingerprint": {
            "strategy": "freeze_hint_target_mismatch",
            "components": ["validation_evidence_summary", "batch17", "ZIP CONTRACT: PASS"],
            "fingerprint_hash": "batch17-freeze-hint-repair-target-mismatch-v2",
        },
        "prevention_triggers": ["freeze hint repair"],
        "regression_check": {
            "type": "validation_command",
            "command": "python scripts/validate_architecture_warning_cleanup_batch17_line_count_smoke_v1.py",
            "expected_marker": "VALIDATION OK: architecture-warning-cleanup-batch17-line-count-smoke-v1; Errors: 0; ZIP CONTRACT: PASS",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run focused validation and ZIP contract validation.",
        "validation_evidence": [],
        "install_command_summary": "Installer stages pending lesson only.",
        "notes": "Human review remains required.",
    }


def _write_project_evidence_fixture(base: Path) -> Path:
    """Create a project/show_project fixture with observed validation markers."""
    project_root = base / "kanda_reasoner"
    evidence_dir = base / "kanda_reasoner_show_project_to_AI" / "project_freeze_after_update" / "freeze_hint_intake"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    project_root.mkdir(parents=True, exist_ok=True)
    evidence_file = evidence_dir / "batch17_freeze_hint.json"
    evidence_file.write_text(
        json.dumps(
            {
                "source_patch_zip": "kanda_architecture_warning_cleanup_batch17_line_count_smoke_v1_patch.zip",
                "feature_id": "architecture-warning-cleanup-batch17-line-count-smoke-v1",
                "validation_evidence_summary": [
                    "VALIDATION OK: architecture-warning-cleanup-batch17-line-count-smoke-v1",
                    "Errors: 0",
                    "ZIP CONTRACT: PASS",
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return project_root


def _validate_module_hygiene() -> None:
    """Validate touched files compile and remain under the line-count gate."""
    for relative in TOUCHED_FILES:
        path = PROJECT_ROOT / relative
        _assert(path.exists(), "missing touched file: " + relative)
        _assert(_line_count(path) <= 500, relative + " exceeds 500 lines")
        py_compile.compile(str(path), doraise=True)
        ast.parse(path.read_text(encoding="utf-8", errors="replace"))


def _validate_prompt_builder_hints() -> None:
    """Validate recovered evidence hints are included in local AI prompts."""
    builder = importlib.import_module("kanda_reasoner_app.error_memory_gui._ai_prompt_builder")
    messages = builder.build_error_memory_correction_messages(
        intake_text="FREEZE BLOCKED",
        editor_text="{}",
        project_root="E:/kanda_reasoner",
        evidence_hints=["Recovered from project file x.json: ZIP CONTRACT: PASS"],
    )
    text = "\n".join(message["content"] for message in messages)
    _assert("PROJECT EVIDENCE HINTS RECOVERED BY THE APP" in text, "hints header missing")
    _assert("Recovered from project file x.json" in text, "hints not injected")
    _assert("do not invent validation evidence" in text.lower(), "anti-hallucination rule missing")


def _validate_evidence_recovery(base: Path) -> tuple[Path, list[str]]:
    """Validate the project scanner finds observed markers but ignores expected text."""
    recovery = importlib.import_module("kanda_reasoner_app.error_memory_gui._ai_evidence_recovery")
    project_root = _write_project_evidence_fixture(base)
    expected_only = project_root.with_name("kanda_reasoner_show_project_to_AI") / "project_error_memory"
    expected_only.mkdir(parents=True, exist_ok=True)
    (expected_only / "template.md").write_text(
        "expected_marker: VALIDATION OK: should-not-count\n",
        encoding="utf-8",
    )
    evidence = recovery.recover_validation_evidence(
        project_root=project_root,
        lesson=_sample_lesson(),
        context_text=json.dumps(_sample_lesson()),
    )
    joined = "\n".join(evidence)
    _assert("VALIDATION OK: architecture-warning-cleanup-batch17-line-count-smoke-v1" in joined, "VALIDATION OK not recovered")
    _assert("ZIP CONTRACT: PASS" in joined, "ZIP contract marker not recovered")
    _assert("should-not-count" not in joined, "expected marker was falsely counted")
    return project_root, evidence


def _validate_parser_empty_evidence() -> None:
    """Validate empty evidence remains a truthful draft-only placeholder."""
    validator = importlib.import_module("kanda_reasoner_app.error_memory_gui._ai_response_validator")
    lesson = _sample_lesson()
    parsed = validator.parse_one_lesson_block(validator.format_lesson_block(lesson))
    _assert(parsed.lesson["status"] == "draft", "empty evidence did not keep draft")
    _assert(parsed.lesson["validation_evidence"], "empty evidence not repaired")
    _assert("No successful validation evidence" in parsed.lesson["validation_evidence"][0], "wrong default evidence")


def _validate_service_merges_recovered_evidence(project_root: Path) -> None:
    """Validate the corrector replaces placeholder evidence with recovered markers."""
    corrector = importlib.import_module("kanda_reasoner_app.error_memory_gui._ai_corrector_service")
    validator = importlib.import_module("kanda_reasoner_app.error_memory_gui._ai_response_validator")
    lesson = _sample_lesson()
    calls: list[list[dict[str, str]]] = []

    def fake_candidates(selection: str) -> list[str]:
        return ["qwen2.5-coder:7b"]

    def fake_chat(messages: list[dict[str, str]], **kwargs: Any) -> tuple[str, str]:
        calls.append(messages)
        return validator.format_lesson_block(lesson), "qwen2.5-coder:7b"

    old_chat = corrector.chat_with_local_model
    old_candidates = corrector.get_local_ai_model_candidates
    corrector.chat_with_local_model = fake_chat
    corrector.get_local_ai_model_candidates = fake_candidates
    try:
        result = corrector.correct_error_memory_lesson_with_local_ai(
            intake_text=validator.format_lesson_block(lesson),
            editor_text="",
            project_root=project_root,
            model_selection="qwen2.5-coder:7b",
        )
    finally:
        corrector.chat_with_local_model = old_chat
        corrector.get_local_ai_model_candidates = old_candidates
    _assert(result.ok, "corrector did not succeed")
    evidence = result.lesson_block.lesson["validation_evidence"] if result.lesson_block else []
    joined = "\n".join(evidence)
    _assert("Recovered from project file" in joined, "recovered evidence was not merged")
    _assert("ZIP CONTRACT: PASS" in joined, "recovered ZIP marker missing")
    first_prompt = "\n".join(message["content"] for message in calls[0])
    _assert("PROJECT EVIDENCE HINTS RECOVERED BY THE APP" in first_prompt, "prompt did not receive hints")


def main() -> int:
    """Run focused validation for v4 project evidence recovery."""
    _validate_module_hygiene()
    _validate_prompt_builder_hints()
    with tempfile.TemporaryDirectory(prefix="kanda_error_memory_v4_fixture_") as temp_root:
        project_root, _evidence = _validate_evidence_recovery(Path(temp_root))
        _validate_parser_empty_evidence()
        _validate_service_merges_recovered_evidence(project_root)
    print("VALIDATION OK: error-memory-local-ai-corrector-retry-v4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
