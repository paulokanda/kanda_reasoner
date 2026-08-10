#!/usr/bin/env python3
"""Reusable fixtures for portable Error Memory transfer validation."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
from pathlib import Path
import shutil
from typing import Any, Iterator
from uuid import uuid4


@contextmanager
def isolated_project_roots(
    base: Path,
    *labels: str,
) -> Iterator[tuple[Path, ...]]:
    """Create unique project fixtures and remove external support roots."""
    from kanda_reasoner_app.error_memory.paths import (
        resolve_show_project_to_ai_root,
    )

    token = uuid4().hex[:12]
    roots = tuple(base / (label + "_" + token) for label in labels)
    support_roots: list[Path] = []
    for root in roots:
        root.mkdir(parents=True, exist_ok=False)
        support_roots.append(resolve_show_project_to_ai_root(root))
    try:
        yield roots
    finally:
        for support_root in support_roots:
            support_name = support_root.name.lower()
            safe_name = (
                token in support_name
                and support_name.endswith("_show_project_to_ai")
            )
            if safe_name and support_root.is_dir():
                shutil.rmtree(support_root)


def expected_dynamic_lessons_dir(project_root: Path) -> Path:
    """Return the independently expected dynamic lesson folder."""
    support_name = project_root.name.lower() + "_show_project_to_AI"
    if project_root.drive:
        support_root = Path(project_root.anchor) / support_name
    else:
        support_root = project_root.parent / support_name
    return support_root / "project_error_memory" / "lessons"


def lesson_fixture(
    root: Path,
    *,
    lesson_id: str,
    raw_error: str,
    status: str = "draft",
    fingerprint_hash: str = "",
) -> dict[str, Any]:
    """Return one valid portable-transfer lesson fixture."""
    from kanda_reasoner_app.error_memory.models import build_lesson

    lesson = build_lesson(
        selected_project_root=root,
        raw_error_text=raw_error,
        operation_phase="validation",
        symptom="Portable transfer fixture symptom for " + lesson_id,
        root_cause="Portable transfer fixture root cause for " + lesson_id,
        wrong_assumption="Portable transfer fixture wrong assumption.",
        correct_fix="Portable transfer fixture correct fix.",
        long_term_prevention="Portable transfer fixture prevention.",
        do_not_repeat_rule="Portable transfer fixture rule for " + lesson_id,
        prevention_triggers=["portable transfer " + lesson_id],
        validation_evidence=["FIXTURE_VALIDATION: PASS"],
        status=status,
        lesson_id=lesson_id,
    )
    fingerprint = dict(lesson.get("fingerprint") or {})
    fingerprint["fingerprint_hash"] = (
        fingerprint_hash
        or hashlib.sha256(lesson_id.encode("utf-8")).hexdigest()
    )
    lesson["fingerprint"] = fingerprint
    if status == "active":
        lesson["validation_command_summary"] = "Run the fixture validator."
        lesson["exception"].update(
            {"type": "FixtureError", "message_normalized": raw_error}
        )
        lesson["redaction"]["rules"] = ["fixture redaction"]
        lesson["source_patch_zip"] = "fixture.zip"
        lesson["install_command_summary"] = "Install fixture."
        lesson["notes"] = "Active fixture lesson."
        lesson["regression_check"].update(
            {
                "type": "validation_command",
                "command": "python tools/fixture.py",
                "expected_marker": "FIXTURE: PASS",
                "required_before_freeze": True,
            }
        )
        lesson["status"] = "active"
    return lesson
