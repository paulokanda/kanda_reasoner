# project-path: kanda_reasoner_app/error_memory/exporter.py
"""Generate Error Memory files for Show Project to AI handoffs."""

from __future__ import annotations


__all__ = [
    'build_complete_error_memory_ai_clipboard_json',
    'write_complete_error_memory_ai_clipboard_export',
    'write_error_memory_ai_send_files',
]
import json
from pathlib import Path
from typing import Any
import zipfile

from kanda_reasoner_app.project_analysis_evidence_paths import project_name_from_root

from .models import compact_lesson
from .paths import (
    resolve_error_memory_exports_dir,
    resolve_error_memory_lessons_dir,
    resolve_project_error_memory_root,
)
from .scrubber import scrub_text
from .store import bootstrap_error_memory_store, list_lessons, rebuild_index

COMPACT_JSON_SUFFIX = "__error_lessons_compact.json"
PROMPT_MD_SUFFIX = "__error_memory_ai_prompt.md"
MANIFEST_SUFFIX = "__error_memory_manifest.json"
FULL_ZIP_SUFFIX = "__error_memory_full.zip"
EXPORTER_VERSION = "1.2"


def _safe_json_dump(payload: Any) -> str:
    """Support safe json dump behavior.
    
    Parameters
    ----------
    payload : Any
        The payload value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)


def _write_text(path: Path, text: str) -> Path:
    """Support write text behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    text : str
        The text value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _active_lessons_for_export(selected_project_root: str | Path, *, max_lessons: int = 10) -> list[dict[str, Any]]:
    """Support active lessons for export behavior.
    
    Parameters
    ----------
    selected_project_root : str | Path
        The selected project root value.
    max_lessons : int, optional
        The optional max lessons value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    active = [lesson for lesson in list_lessons(selected_project_root, include_inactive=False) if lesson.get("status") == "active"]
    active.sort(key=lambda item: str(item.get("updated_at_utc", "")), reverse=True)
    return active[:max_lessons]


def _prompt_text(project_slug: str, full_zip_name: str) -> str:
    """Support prompt text behavior.
    
    Parameters
    ----------
    project_slug : str
        The project slug value.
    full_zip_name : str
        The full zip name value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return "\n".join(
        [
            "# ERROR MEMORY AI PREFLIGHT",
            "",
            "Read the uploaded compact Error Memory files before proposing or editing code.",
            "",
            "Canon:",
            "- Compact Error Memory = always read.",
            "- Full Error Memory ZIP = opened only when needed.",
            "- Error Memory is prevention guidance, not source truth.",
            "- Exact source files must still be inspected before editing.",
            "",
            "Full Error Memory ZIP:",
            "- " + full_zip_name,
            "- Do not open by default.",
            "- Open only if the compact manifest says full context is needed, the task is repeated-error debugging, the user asks for Error Memory audit, compact lessons are insufficient, or a current plan conflicts with a prior lesson.",
            "",
            "Return this before coding:",
            "",
            "ERROR MEMORY CHECK",
            "",
            "Project slug: " + project_slug,
            "Compact export identity and freshness:",
            "Relevant lesson IDs:",
            "Confidence per match: exact / partial / weak / none",
            "Lesson freshness:",
            "Applicable avoidance rules:",
            "Regression obligations:",
            "ERROR MEMORY REGRESSION MATRIX",
            "Repeat one block for every Relevant lesson ID. The Lesson ID set must match exactly.",
            "Lesson ID:",
            "Match confidence: exact / partial / weak",
            "Freshness: current / stale / partial / unresolved",
            "Disposition: EXISTING_VALIDATOR / NEW_FOCUSED_TEST / NOT_APPLICABLE / CURRENT_SOURCE_REINTERPRETATION",
            "Protection owner:",
            "Validator or test path:",
            "Expected success marker:",
            "Expected rejection marker:",
            "Disposition reason:",
            "Status: COMPLETE / BLOCKED",
            "ERROR MEMORY LESSON FRESHNESS VERIFICATION",
            "Repeat one block for every Relevant lesson ID. The freshness lesson-key set must match exactly.",
            "Freshness lesson key:",
            "Lesson status: active / draft / deprecated / superseded",
            "Superseded by:",
            "Referenced file:",
            "File exists: YES / NO / N/A",
            "Referenced symbol:",
            "Symbol exists: YES / NO / N/A",
            "Current public facade:",
            "Current facade verified: YES / NO / N/A",
            "Current box:",
            "Current owner:",
            "Current source fingerprint:",
            "Lesson fingerprint comparison: EXACT / PARTIAL / MISMATCH / UNRESOLVED",
            "Invalidation conditions reviewed:",
            "Invalidation condition triggered: YES / NO / UNRESOLVED",
            "Freshness decision: CURRENT / STALE / PARTIAL / BLOCKED",
            "Freshness evidence:",
            "Freshness status: COMPLETE / BLOCKED",
            "Full Error Memory ZIP needed: YES / NO",
            "Full ZIP open reason:",
            "May proceed to exact-source inspection: YES / NO",
            "May begin coding: NO",
            "Reason:",
            "Next safe action:",
            "",
            "If no lesson applies, say: No prior error lesson applies.",
            "If full context is not needed, say: Full Error Memory ZIP not needed for this task.",
            "",
        ]
    )


def _build_compact_bundle(selected_project_root: str | Path, lessons: list[dict[str, Any]]) -> dict[str, Any]:
    """Support build compact bundle behavior.
    
    Parameters
    ----------
    selected_project_root : str | Path
        The selected project root value.
    lessons : list[dict[str, Any]]
        The lessons value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    project_slug = project_name_from_root(selected_project_root)
    return {
        "artifact_type": "error_memory_ai_export",
        "schema_version": "1.0",
        "derived_from": {
            "project_slug": project_slug,
            "canonical_store": str(resolve_project_error_memory_root(selected_project_root)),
            "lesson_ids": [str(lesson.get("lesson_id", "")) for lesson in lessons],
            "redaction_applied": True,
            "exporter_version": EXPORTER_VERSION,
        },
        "lessons": [compact_lesson(lesson) for lesson in lessons],
    }


def _build_manifest(selected_project_root: str | Path, lessons: list[dict[str, Any]], full_zip_name: str) -> dict[str, Any]:
    """Support build manifest behavior.
    
    Parameters
    ----------
    selected_project_root : str | Path
        The selected project root value.
    lessons : list[dict[str, Any]]
        The lessons value.
    full_zip_name : str
        The full zip name value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "artifact_type": "error_memory_manifest",
        "schema_version": "1.0",
        "project_slug": project_name_from_root(selected_project_root),
        "canonical_error_memory_root": str(resolve_project_error_memory_root(selected_project_root)),
        "compact_error_memory_always_read": True,
        "full_error_memory_zip": full_zip_name,
        "full_error_memory_zip_open_policy": "open_only_when_needed",
        "active_lesson_count_exported": len(lessons),
        "included_lesson_ids": [str(lesson.get("lesson_id", "")) for lesson in lessons],
        "open_full_zip_when": [
            "compact manifest says a relevant lesson requires full context",
            "current task is repeated-error debugging",
            "user explicitly asks to audit Error Memory",
            "compact lessons are insufficient to understand a prior failure",
            "current implementation plan conflicts with a previous lesson",
        ],
    }




def _all_saved_lesson_json_objects(selected_project_root: str | Path) -> list[dict[str, Any]]:
    """Return every saved Error Memory lesson JSON object from disk.

    Complete clipboard export must not depend on the compact/export helper or
    on any list/index helper that may filter by status. It should include
    active, draft, deprecated, and superseded lessons that are saved in the
    canonical lessons folder.
    """
    lessons_dir = resolve_error_memory_lessons_dir(selected_project_root)
    lessons_dir.mkdir(parents=True, exist_ok=True)
    lessons: list[dict[str, Any]] = []
    for path in sorted(lessons_dir.glob("lesson-*.json")):
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if isinstance(payload, dict):
            lessons.append(payload)
    return lessons

def build_complete_error_memory_ai_clipboard_json(
    selected_project_root: str | Path,
    *,
    include_inactive: bool = True,
) -> str:
    """Return complete Error Memory JSON text for manual AI transfer.

    This is the clipboard contract for the Error Memory tab export button.
    It intentionally includes full lesson objects, not the compact capped export.
    """
    bootstrap_error_memory_store(selected_project_root)
    rebuild_index(selected_project_root)
    project_slug = project_name_from_root(selected_project_root)
    lessons = _all_saved_lesson_json_objects(selected_project_root)
    if not include_inactive:
        lessons = [lesson for lesson in lessons if lesson.get("status") == "active"]
    lessons.sort(
        key=lambda item: (
            str(item.get("updated_at_utc", "")),
            str(item.get("lesson_id", "")),
        ),
        reverse=True,
    )
    payload = {
        "artifact_type": "error_memory_ai_clipboard_export",
        "schema_version": "1.0",
        "project_slug": project_slug,
        "canonical_error_memory_root": str(resolve_project_error_memory_root(selected_project_root)),
        "exporter_version": EXPORTER_VERSION,
        "include_inactive": bool(include_inactive),
        "lesson_count_exported": len(lessons),
        "clipboard_contract": (
            "Complete Error Memory JSON copied for manual AI transfer. "
            "This payload contains all saved full lesson objects, including draft and inactive statuses when requested, and is not capped to the compact export limit."
        ),
        "lessons": lessons,
    }
    return _safe_json_dump(payload)



def write_complete_error_memory_ai_clipboard_export(
    selected_project_root: str | Path,
    *,
    include_inactive: bool = True,
) -> dict[str, Any]:
    """Write and return the complete Error Memory JSON clipboard payload.

    This function is the contract for the Error Memory tab export button.
    It does not use ``second_prompt_files`` and must not return a folder path
    as the clipboard payload.
    """
    clipboard_json = build_complete_error_memory_ai_clipboard_json(
        selected_project_root,
        include_inactive=include_inactive,
    )
    export_dir = resolve_error_memory_exports_dir(selected_project_root)
    export_dir.mkdir(parents=True, exist_ok=True)
    complete_json_path = _write_text(
        export_dir / "latest_error_memory_complete_for_ai.json",
        clipboard_json,
    )
    payload = json.loads(clipboard_json)
    return {
        "ok": True,
        "project_slug": payload.get("project_slug", project_name_from_root(selected_project_root)),
        "canonical_error_memory_root": str(resolve_project_error_memory_root(selected_project_root)),
        "complete_json": str(complete_json_path),
        "complete_json_lesson_count": int(payload.get("lesson_count_exported", 0)),
        "complete_clipboard_json": clipboard_json,
        "clipboard_contract": "complete_json_only",
    }

def _write_full_error_memory_zip(selected_project_root: str | Path, destination_folder: Path) -> Path:
    """Support write full error memory zip behavior.
    
    Parameters
    ----------
    selected_project_root : str | Path
        The selected project root value.
    destination_folder : Path
        The destination folder value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    project_slug = project_name_from_root(selected_project_root)
    full_zip = destination_folder / (project_slug + FULL_ZIP_SUFFIX)
    canonical_root = resolve_project_error_memory_root(selected_project_root)
    canonical_root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(full_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(canonical_root.rglob("*")):
            if not path.is_file():
                continue
            try:
                relative = path.relative_to(canonical_root)
            except ValueError:
                continue
            archive.write(path, "project_error_memory/" + str(relative).replace("\\", "/"))
    return full_zip


def write_error_memory_ai_send_files(
    selected_project_root: str | Path,
    destination_folder: str | Path,
    *,
    max_lessons: int = 10,
) -> dict[str, Any]:
    """Write compact Error Memory files and full ZIP into a second-prompt folder.

    ``destination_folder`` may be ``second_prompt_files_building`` during a GUI
    rebuild or ``second_prompt_files`` during direct/manual export.
    """
    bootstrap_error_memory_store(selected_project_root)
    rebuild_index(selected_project_root)
    destination = Path(destination_folder).expanduser().resolve(strict=False)
    destination.mkdir(parents=True, exist_ok=True)
    project_slug = project_name_from_root(selected_project_root)
    lessons = _active_lessons_for_export(selected_project_root, max_lessons=max_lessons)
    full_zip_name = project_slug + FULL_ZIP_SUFFIX

    compact_bundle = _build_compact_bundle(selected_project_root, lessons)
    manifest = _build_manifest(selected_project_root, lessons, full_zip_name)
    prompt_text = _prompt_text(project_slug, full_zip_name)

    compact_path = _write_text(destination / (project_slug + COMPACT_JSON_SUFFIX), _safe_json_dump(compact_bundle))
    manifest_path = _write_text(destination / (project_slug + MANIFEST_SUFFIX), _safe_json_dump(manifest))
    prompt_path = _write_text(destination / (project_slug + PROMPT_MD_SUFFIX), scrub_text(prompt_text).text)
    full_zip = _write_full_error_memory_zip(selected_project_root, destination)

    # Keep an export copy under the canonical Error Memory tree as generated/disposable output.
    export_dir = resolve_error_memory_exports_dir(selected_project_root)
    export_dir.mkdir(parents=True, exist_ok=True)
    _write_text(export_dir / "latest_error_lessons_compact.json", compact_path.read_text(encoding="utf-8"))
    _write_text(export_dir / "latest_error_memory_manifest.json", manifest_path.read_text(encoding="utf-8"))
    _write_text(export_dir / "latest_ai_send_prompt.md", prompt_path.read_text(encoding="utf-8"))

    complete_clipboard_json = build_complete_error_memory_ai_clipboard_json(
        selected_project_root,
        include_inactive=True,
    )
    complete_json_path = _write_text(
        export_dir / "latest_error_memory_complete_for_ai.json",
        complete_clipboard_json,
    )

    return {
        "ok": True,
        "project_slug": project_slug,
        "canonical_error_memory_root": str(resolve_project_error_memory_root(selected_project_root)),
        "destination_folder": str(destination),
        "compact_json": str(compact_path),
        "prompt_md": str(prompt_path),
        "manifest_json": str(manifest_path),
        "full_zip": str(full_zip),
        "complete_json": str(complete_json_path),
        "complete_json_lesson_count": len(list_lessons(selected_project_root, include_inactive=True)),
        "complete_clipboard_json": complete_clipboard_json,
        "active_lesson_count_exported": len(lessons),
    }
