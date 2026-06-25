"""Tab 4 JSON ZIP export helpers.

This module keeps ZIP-export GUI behavior outside the collector process helper
so the collector box remains focused on collection and bundle generation.
"""

from __future__ import annotations

import importlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV,
    SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV,
    analysis_json_building_dir,
    project_analysis_evidence_root,
    analysis_json_complete_dir,
    project_name_from_root,
)

__all__ = [
    "CONSERVATIVE_ZIP_SIZE_MB",
    "DEFAULT_ZIP_SIZE_MB",
    "EXTENDED_ZIP_SIZE_MB_OPTIONS",
    "ALLOWED_ZIP_SIZE_MB_OPTIONS",
    "auto_zip_json_complete",
    "cleanup_show_project_to_ai_root_after_success",
    "clear_second_prompt_files_dir",
    "clear_second_prompt_files_building_dir",
    "publish_second_prompt_files_building_dir",
    "second_prompt_files_building_dir",
    "write_second_prompt_status",
    "resolve_zip_dialog_start_folder",
    "run_zip_json_files",
    "selected_part_size_mb",
]

CONSERVATIVE_ZIP_SIZE_MB = 25
DEFAULT_ZIP_SIZE_MB = 40
EXTENDED_ZIP_SIZE_MB_OPTIONS = (100, 200, 300, 450)
ALLOWED_ZIP_SIZE_MB_OPTIONS = (
    CONSERVATIVE_ZIP_SIZE_MB,
    DEFAULT_ZIP_SIZE_MB,
    *EXTENDED_ZIP_SIZE_MB_OPTIONS,
)



STATUS_FILE_NAME = "_RUN_COLLECTOR_STATUS.txt"


def second_prompt_files_building_dir(project_root: str | Path) -> Path:
    """Return the temporary second-prompt build directory for one project."""
    return analysis_json_building_dir(project_root).expanduser().resolve(strict=False)


def _require_show_project_child_dir(output_dir: str | Path, expected_name: str) -> Path:
    resolved_dir = Path(output_dir).expanduser().resolve(strict=False)
    if resolved_dir.name != expected_name:
        raise ValueError(
            "Refusing output-folder operation because folder is not "
            + expected_name
            + ": "
            + str(resolved_dir)
        )
    parent = resolved_dir.parent
    if not parent.name.endswith("_show_project_to_AI"):
        raise ValueError(
            "Refusing output-folder operation because parent is not *_show_project_to_AI: "
            + str(resolved_dir)
        )
    return resolved_dir


def _clear_dir_contents(resolved_dir: Path) -> int:
    resolved_dir.mkdir(parents=True, exist_ok=True)
    removed = 0
    for child in resolved_dir.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
        removed += 1
    return removed




_ALLOWED_SHOW_PROJECT_CHILD_DIRS = {"first_prompt_files", "second_prompt_files"}
_STALE_SHOW_PROJECT_DIR_NAMES = {"second_prompt_files_building", "json_splitted"}
_STALE_SHOW_PROJECT_DIR_PREFIXES = (
    "json_handoff_zip_export_",
    ".json_handoff_zip_export_",
    ".json_handoff_zip_stage_",
    ".json_handoff_zip_work_",
    ".second_prompt_files_publish_",
    ".second_prompt_files_previous_",
)


def _is_known_show_project_root_file(path: Path, project_root: str | Path | None = None) -> bool:
    """Return True only for known generated files that leaked to the parent root."""
    if not path.is_file():
        return False
    name = path.name
    if name == STATUS_FILE_NAME:
        return True
    slug = ""
    if project_root is not None:
        try:
            slug = project_name_from_root(project_root)
        except Exception:
            slug = ""
    generated_suffixes = {".json", ".zip", ".txt", ".md"}
    if path.suffix.lower() not in generated_suffixes:
        return False
    if slug and (
        name.startswith(slug + "__")
        or name.startswith(slug + "_split_")
        or name.startswith(slug + "__complete")
    ):
        return True
    return (
        "__source_archive_" in name
        or "__ai_handoff" in name
        or "__complete" in name
        or name.endswith("_split_manifest.json")
        or name.endswith("_split_index.json")
        or name.endswith("__complete__web_ai_route_manifest.json")
    )


def cleanup_show_project_to_ai_root_after_success(project_root: str | Path, *, final_dir: str | Path | None = None) -> dict[str, object]:
    """Remove stale generated siblings so the root keeps only first/second folders.

    This cleanup is deliberately limited to known Show Project to AI generated
    folders/files. It preserves the two canonical child folders and does not
    touch arbitrary user folders unless they match known temporary/export names.
    """
    root = project_analysis_evidence_root(project_root).expanduser().resolve(strict=False)
    removed: list[str] = []
    skipped: list[str] = []
    if not root.exists():
        return {"root": str(root), "removed": removed, "skipped": skipped}
    final_path = Path(final_dir).expanduser().resolve(strict=False) if final_dir is not None else None
    for child in list(root.iterdir()):
        name = child.name
        if name in _ALLOWED_SHOW_PROJECT_CHILD_DIRS:
            skipped.append(str(child))
            continue
        if final_path is not None:
            try:
                if child.resolve(strict=False) == final_path:
                    skipped.append(str(child))
                    continue
            except Exception:
                pass
        remove_child = False
        if child.is_dir():
            remove_child = name in _STALE_SHOW_PROJECT_DIR_NAMES or name.startswith(_STALE_SHOW_PROJECT_DIR_PREFIXES)
        elif child.is_file():
            remove_child = _is_known_show_project_root_file(child, project_root)
        if not remove_child:
            skipped.append(str(child))
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
        removed.append(str(child))
    return {"root": str(root), "removed": removed, "skipped": skipped}


def write_second_prompt_status(
    output_dir: str | Path,
    *,
    status: str,
    step: str,
    project_root: str | Path | None = None,
    final_output_dir: str | Path | None = None,
    details: list[str] | None = None,
) -> Path:
    """Write a small visible status file for long Show Project to AI builds."""
    resolved_dir = Path(output_dir).expanduser().resolve(strict=False)
    resolved_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "Show Project to AI - Second Prompt Files",
        "Status: " + str(status),
        "Step: " + str(step),
        "Output folder: " + str(resolved_dir),
    ]
    if project_root is not None:
        lines.append("Project root: " + str(project_root))
    if final_output_dir is not None:
        lines.append("Final folder: " + str(final_output_dir))
    if details:
        lines.append("")
        lines.extend(str(item) for item in details)
    lines.append("")
    status_path = resolved_dir / STATUS_FILE_NAME
    status_path.write_text("\n".join(lines), encoding="utf-8")
    return status_path


def clear_second_prompt_files_building_dir(output_dir: str | Path) -> int:
    """Clear only the approved second_prompt_files_building output directory."""
    resolved_dir = _require_show_project_child_dir(output_dir, "second_prompt_files_building")
    return _clear_dir_contents(resolved_dir)


def _rewrite_generated_text_paths(build_dir: Path, final_dir: Path) -> int:
    """Rewrite temporary build-folder references to final-folder references."""
    replacements = (
        (str(build_dir), str(final_dir)),
        (str(build_dir).replace("\\", "/"), str(final_dir).replace("\\", "/")),
        ("show_project_to_AI/second_prompt_files_building", "show_project_to_AI/second_prompt_files"),
        ("show_project_to_AI\\second_prompt_files_building", "show_project_to_AI\\second_prompt_files"),
        ("second_prompt_files_building", "second_prompt_files"),
    )
    changed = 0
    for path in build_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".json", ".txt", ".md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def _refresh_bundle_manifest_after_publish_rewrite(
    build_dir: Path,
    final_dir: Path,
    *,
    project_root: str | Path | None,
) -> Path | None:
    """Refresh bundle-manifest hashes after build-folder text rewrites.

    Companion bundle generation occurs inside ``second_prompt_files_building``.
    Before publication, generated text artifacts are rewritten so the final
    delivery mentions ``second_prompt_files`` rather than the temporary build
    folder.  That rewrite changes bytes for several JSON artifacts, so the
    bundle manifest must be regenerated after the rewrite and then have its own
    logical path references rewritten to the final folder.
    """
    if project_root is None:
        return None

    from kanda_reasoner_app.reasoner_context_bundle.bundle_manifest_builder import (
        write_bundle_manifest_json,
    )

    root_path = Path(project_root).expanduser().resolve(strict=False)
    evidence_root = project_analysis_evidence_root(root_path).expanduser().resolve(strict=False)
    try:
        build_dir.relative_to(evidence_root)
    except ValueError:
        # Older tests and manual helper calls may use an arbitrary temporary
        # sibling pair that is not the selected project's real dynamic output
        # folder. Those synthetic folders have no selected-project manifest
        # contract to refresh.
        return None

    previous_output_override = os.environ.get(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV)
    previous_project_root = os.environ.get(SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV)
    try:
        os.environ[SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV] = str(root_path)
        os.environ[SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV] = str(build_dir)
        manifest_path = write_bundle_manifest_json(root_path)
    finally:
        if previous_output_override is None:
            os.environ.pop(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV, None)
        else:
            os.environ[SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV] = previous_output_override
        if previous_project_root is None:
            os.environ.pop(SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV, None)
        else:
            os.environ[SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV] = previous_project_root

    # The refreshed manifest is the only freshly written file that can still
    # contain build-folder logical paths. Rewrite it to the final delivery
    # contract without changing the already-recorded hashes for other files.
    _rewrite_generated_text_paths(build_dir, final_dir)
    return manifest_path



def _remove_forbidden_second_prompt_payloads(final_path: Path, project_root: str | Path | None = None) -> list[str]:
    """Remove stale heavy payloads that are not part of normal hybrid output."""
    removed: list[str] = []
    slug = ""
    if project_root is not None:
        try:
            slug = project_name_from_root(project_root)
        except Exception:
            slug = ""
    forbidden_suffixes = ("__complete.json", "__active_snapshot.json", "__reconstruction_payload.json")
    for child in list(final_path.iterdir()) if final_path.exists() and final_path.is_dir() else []:
        if not child.is_file():
            continue
        if child.name.endswith(forbidden_suffixes) or (slug and child.name in {slug + "__complete_runtime_trace.json"}):
            try:
                child.unlink()
                removed.append(str(child))
            except Exception:
                pass
    return removed

def publish_second_prompt_files_building_dir(
    building_dir: str | Path,
    final_dir: str | Path,
    *,
    project_root: str | Path | None = None,
) -> dict[str, object]:
    """Atomically publish a completed build folder into second_prompt_files.

    The final folder is not deleted or replaced until the build folder already
    contains the generated JSON artifacts and ZIP export artifacts. On failure,
    the previous final delivery is restored when possible. On success, temporary
    siblings such as second_prompt_files_building and json_splitted are removed
    so the show_project_to_AI root normally contains only first_prompt_files and
    second_prompt_files.
    """
    build_path = _require_show_project_child_dir(building_dir, "second_prompt_files_building")
    final_path = _require_show_project_child_dir(final_dir, "second_prompt_files")
    if build_path.parent != final_path.parent:
        raise ValueError(
            "Refusing to publish because build and final folders are not siblings: "
            + str(build_path)
            + " -> "
            + str(final_path)
        )
    if not build_path.exists() or not build_path.is_dir():
        raise ValueError("Build folder does not exist: " + str(build_path))

    rewritten_files = _rewrite_generated_text_paths(build_path, final_path)
    refreshed_manifest = _refresh_bundle_manifest_after_publish_rewrite(
        build_path,
        final_path,
        project_root=project_root,
    )

    parent = final_path.parent
    token = str(os.getpid()) + "_" + str(abs(hash(str(build_path))))
    stage_path = parent / (".second_prompt_files_publish_" + token)
    backup_path = parent / (".second_prompt_files_previous_" + token)
    for transient in (stage_path, backup_path):
        if transient.exists():
            shutil.rmtree(transient)

    moved_items = len(list(build_path.iterdir()))
    removed_final_items = len(list(final_path.iterdir())) if final_path.exists() and final_path.is_dir() else 0
    try:
        shutil.move(str(build_path), str(stage_path))
        if final_path.exists():
            shutil.move(str(final_path), str(backup_path))
        shutil.move(str(stage_path), str(final_path))
    except Exception:
        # Best-effort rollback: preserve the previous final delivery and restore
        # the build folder for debugging when publication fails.
        if final_path.exists() and backup_path.exists():
            try:
                if final_path.is_dir():
                    shutil.rmtree(final_path)
                else:
                    final_path.unlink()
            except Exception:
                pass
        if backup_path.exists() and not final_path.exists():
            try:
                shutil.move(str(backup_path), str(final_path))
            except Exception:
                pass
        if stage_path.exists() and not build_path.exists():
            try:
                shutil.move(str(stage_path), str(build_path))
            except Exception:
                pass
        raise
    finally:
        if stage_path.exists():
            shutil.rmtree(stage_path, ignore_errors=True)

    if backup_path.exists():
        shutil.rmtree(backup_path, ignore_errors=True)

    removed_forbidden_payloads = _remove_forbidden_second_prompt_payloads(final_path, project_root)

    cleanup_result = {"removed": [], "skipped": []}
    if project_root is not None:
        cleanup_result = cleanup_show_project_to_ai_root_after_success(project_root, final_dir=final_path)

    write_second_prompt_status(
        final_path,
        status="complete",
        step="published generated files and ZIP export",
        project_root=project_root,
        final_output_dir=final_path,
        details=[
            "Published from temporary folder: " + str(build_path),
            "Moved items: " + str(moved_items),
            "Removed old final-folder items: " + str(removed_final_items),
            "Rewritten generated text files: " + str(rewritten_files),
            "Cleaned stale root items: " + str(len(cleanup_result.get("removed", []))),
            "Removed stale heavy payloads from final folder: " + str(len(removed_forbidden_payloads)),
        ],
    )
    return {
        "building_dir": str(build_path),
        "final_dir": str(final_path),
        "moved_items": moved_items,
        "removed_final_items": removed_final_items,
        "rewritten_files": rewritten_files,
        "refreshed_bundle_manifest": str(refreshed_manifest) if refreshed_manifest is not None else "",
        "cleanup_result": cleanup_result,
        "removed_forbidden_payloads": removed_forbidden_payloads,
    }


def clear_second_prompt_files_dir(output_dir: str | Path) -> int:
    """Clear only the approved second_prompt_files output directory contents."""
    resolved_dir = _require_show_project_child_dir(output_dir, "second_prompt_files")
    return _clear_dir_contents(resolved_dir)

def _qt_widgets():
    return importlib.import_module("PySide6" + ".QtWidgets")


def _process_helpers():
    from kanda_reasoner_app.reasoner_tools_shell.runner_help import (
        window_process_private_impl as helpers,
    )
    return helpers


def _prefs_path() -> Path:
    return Path(__file__).resolve().parent / ".zip_json_export_prefs.json"


def _load_destination() -> str:
    try:
        prefs_path = _prefs_path()
        if prefs_path.exists():
            payload = json.loads(prefs_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                destination = str(payload.get("destination_folder", "")).strip()
                if destination:
                    return destination
    except Exception:
        pass
    return ""


def _save_destination(destination_folder: str) -> None:
    try:
        _prefs_path().write_text(
            json.dumps({"destination_folder": destination_folder}, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def _destination_inside_project_root(project_root: Path, destination: Path) -> bool:
    try:
        resolved_root = project_root.expanduser().resolve()
        resolved_destination = destination.expanduser().resolve()
        resolved_destination.relative_to(resolved_root)
        return True
    except ValueError:
        return False
    except Exception:
        return False


def selected_part_size_mb(window: Any) -> int:
    """Return the selected ZIP size option for the collector tab."""
    radio_by_size = (
        (CONSERVATIVE_ZIP_SIZE_MB, "zip_size_conservative_radio"),
        (DEFAULT_ZIP_SIZE_MB, "zip_size_default_radio"),
        (100, "zip_size_100_radio"),
        (200, "zip_size_200_radio"),
        (300, "zip_size_300_radio"),
        (450, "zip_size_450_radio"),
    )
    for size_mb, attribute in radio_by_size:
        try:
            if bool(getattr(window, attribute).isChecked()):
                return size_mb
        except Exception:
            pass
    return DEFAULT_ZIP_SIZE_MB


def _selected_part_size_mb(window: Any) -> int:
    return selected_part_size_mb(window)


def _set_controls_enabled(window: Any, enabled: bool) -> None:
    for attribute in (
        "run_button",
        "browse_project_button",
        "browse_output_button",
        "zip_json_files_button",
        "zip_size_conservative_radio",
        "zip_size_default_radio",
        "zip_size_100_radio",
        "zip_size_200_radio",
        "zip_size_300_radio",
        "zip_size_450_radio",
    ):
        try:
            getattr(window, attribute).setEnabled(enabled)
        except Exception:
            pass


def _append_log(window: Any, text: str) -> None:
    try:
        window._append_log(text)
    except Exception:
        pass


def _start_zip_status(window: Any) -> None:
    try:
        window._start_busy_animation("Zipping JSON files")
    except Exception:
        try:
            window.status_label.setText("Zipping JSON files...")
        except Exception:
            pass
    _set_controls_enabled(window, False)


def _finish_zip_status(window: Any, status_text: str) -> None:
    try:
        window._stop_busy_animation(status_text)
    except Exception:
        try:
            window.status_label.setText(status_text)
        except Exception:
            pass
    _set_controls_enabled(window, True)


def _decode_process_output(process: Any) -> tuple[str, str]:
    stdout_text = bytes(process.readAllStandardOutput()).decode("utf-8", errors="replace").strip()
    stderr_text = bytes(process.readAllStandardError()).decode("utf-8", errors="replace").strip()
    return stdout_text, stderr_text


def _on_zip_process_finished(window: Any, exit_code: int, _exit_status: Any) -> None:
    process = getattr(window, "_process", None)
    stdout_text = ""
    stderr_text = ""
    if process is not None:
        stdout_text, stderr_text = _decode_process_output(process)

    if exit_code != 0:
        try:
            final_dir = getattr(window, "_pending_second_prompt_final_dir", "")
            if final_dir:
                write_second_prompt_status(final_dir, status="failed", step="ZIP export failed")
        except Exception:
            pass
        _finish_zip_status(window, "Failed")
        _append_log(window, "[ERROR] JSON ZIP export failed:")
        _append_log(window, stderr_text or stdout_text or "Unknown child-process error")
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.critical(
            window,
            "JSON ZIP export error",
            stderr_text or stdout_text or "Unknown child-process error",
        )
        window._process = None
        return

    try:
        result = json.loads(stdout_text) if stdout_text else {}
    except Exception:
        result = {}

    zip_parts = result.get("zip_parts", [])
    zip_count = len(zip_parts) if isinstance(zip_parts, list) else 0
    warnings = result.get("warnings", [])

    destination = str(result.get("destination_folder", "") or "").strip()
    published_after_zip: dict[str, object] | None = None
    try:
        pending_build = Path(str(getattr(window, "_pending_second_prompt_build_dir", "") or "")).expanduser().resolve(strict=False)
        pending_final = Path(str(getattr(window, "_pending_second_prompt_final_dir", "") or "")).expanduser().resolve(strict=False)
        destination_path = Path(destination).expanduser().resolve(strict=False) if destination else None
        if destination_path is not None and pending_build and destination_path == pending_build and str(pending_final):
            project_root_for_publish = getattr(window, "_pending_project_root", None)
            published_after_zip = publish_second_prompt_files_building_dir(
                pending_build,
                pending_final,
                project_root=project_root_for_publish,
            )
            destination = str(pending_final)
            final_output_json = pending_final / Path(str(getattr(window, "_pending_output_json", "") or "")).name
            final_runtime_trace = pending_final / Path(str(getattr(window, "_pending_runtime_trace_json", "") or "")).name
            window._pending_output_json = str(final_output_json)
            window._pending_runtime_trace_json = str(final_runtime_trace)
            window._current_output_json = str(final_output_json)
            try:
                window.output_json_edit.setText(str(final_output_json))
                window.runtime_trace_json_edit.setText(str(final_runtime_trace))
            except Exception:
                pass
            _append_log(window, "[OK] Published second_prompt_files delivery folder after ZIP export.")
            _append_log(window, "  final folder: " + str(pending_final))
            _append_log(window, "  moved_items: " + str(published_after_zip.get("moved_items", "")))
    except Exception as exc:
        _finish_zip_status(window, "Failed")
        _append_log(window, "[ERROR] Publishing second_prompt_files after ZIP export failed:")
        _append_log(window, str(exc))
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.critical(window, "Collector publish error", str(exc))
        window._process = None
        return

    try:
        if destination:
            write_second_prompt_status(
                destination,
                status="complete",
                step="ZIP export complete",
                details=[
                    "ZIP parts created: " + str(zip_count),
                    "Selected part size MB: " + str(result.get("part_size_mb", "")),
                    "Published after ZIP: " + str(published_after_zip is not None),
                ],
            )
            try:
                cleanup_root = getattr(window, "_pending_project_root", None)
                if cleanup_root:
                    cleanup_show_project_to_ai_root_after_success(cleanup_root, final_dir=destination)
            except Exception:
                pass
    except Exception:
        pass

    _finish_zip_status(window, "Finished")
    _append_log(window, "[OK] JSON ZIP export completed.")
    _append_log(window, "  zip_count: " + str(zip_count))
    _append_log(window, "  part_size_mb: " + str(result.get("part_size_mb", "")))
    if isinstance(zip_parts, list):
        for item in zip_parts:
            if isinstance(item, dict):
                _append_log(
                    window,
                    "  zip: "
                    + str(item.get("filename", ""))
                    + " ("
                    + str(item.get("size_bytes", ""))
                    + " bytes)",
                )
    if isinstance(warnings, list):
        for item in warnings:
            _append_log(window, "  warning: " + str(item))

    window._process = None


def _on_zip_process_error(window: Any, _process_error: Any) -> None:
    _finish_zip_status(window, "Failed")
    _append_log(window, "[ERROR] JSON ZIP export process could not start.")
    QMessageBox = _qt_widgets().QMessageBox
    QMessageBox.critical(window, "JSON ZIP export error", "JSON ZIP export process could not start.")
    window._process = None


def _start_zip_process(
    window: Any,
    project_root: Path,
    destination_folder: Path,
    part_size_mb: int,
) -> None:
    helpers = _process_helpers()
    process = helpers.QProcess(window)
    window._process = process
    process.finished.connect(lambda exit_code, status: _on_zip_process_finished(window, exit_code, status))
    process.errorOccurred.connect(lambda error: _on_zip_process_error(window, error))

    env = helpers._tab4_build_child_env(project_root)
    # Automatic Create Second Prompt Files writes the lightweight bundle into
    # second_prompt_files_building first.  The ZIP child process must inherit
    # the same build-folder override; otherwise it resolves bundle artifacts
    # from the final second_prompt_files folder and reports
    # "bundle_manifest artifact is missing" before publish.
    try:
        helpers._tab4_apply_second_prompt_build_env(window, env)
    except Exception:
        pass
    helpers._tab4_apply_qprocess_env(process, env, helpers._tab4_tool_root())

    process_args = [
        "-m",
        "kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter",
        "--root",
        str(project_root),
        "--destination",
        str(destination_folder),
        "--part-size-mb",
        str(part_size_mb),
        "--compact",
    ]

    _start_zip_status(window)
    process.start(sys.executable, process_args)


def _existing_dialog_start_folder(path_text: str) -> Path | None:
    """Return an existing folder suitable for QFileDialog, if available."""
    try:
        candidate = Path(path_text).expanduser()
        if candidate.exists():
            if candidate.is_dir():
                return candidate.resolve()
            parent = candidate.parent
            if parent.exists() and parent.is_dir():
                return parent.resolve()
        parent = candidate.parent
        if parent != candidate and parent.exists() and parent.is_dir():
            return parent.resolve()
    except Exception:
        return None
    return None


def _fallback_dialog_start_folder(project_root: Path) -> str:
    """Return a stable existing start folder for the ZIP destination dialog."""
    anchor = project_root.anchor
    if anchor:
        try:
            anchor_path = Path(anchor).resolve()
            if anchor_path.exists() and anchor_path.is_dir():
                return str(anchor_path)
        except Exception:
            pass
    parent = project_root.parent
    try:
        if parent.exists() and parent.is_dir():
            return str(parent.resolve())
    except Exception:
        pass
    return str(project_root)


def resolve_zip_dialog_start_folder(
    project_root: str | Path,
    last_destination: str | Path | None = None,
) -> str:
    """Return an existing start folder for the ZIP destination dialog."""
    root_path = Path(project_root).expanduser()
    if last_destination is None:
        destination_text = _load_destination()
    else:
        destination_text = str(last_destination).strip()
    if destination_text:
        existing_start = _existing_dialog_start_folder(destination_text)
        if existing_start is not None:
            return str(existing_start)
    return _fallback_dialog_start_folder(root_path)


def _start_folder_for_dialog(project_root: Path) -> str:
    return resolve_zip_dialog_start_folder(project_root)


def auto_zip_json_complete(window: Any, project_root: str | Path | None = None) -> None:
    """Automatically export handoff ZIP parts into the dynamic second_prompt_files folder.

    This is the Run Collector follow-up path. It intentionally bypasses the
    manual ``Zip JSON files`` destination button: the selected project root owns
    the destination contract, and ZIPs are written next to the generated
    complete/companion JSON artifacts under
    ``<project_drive>:/<project_name>_show_project_to_AI/second_prompt_files``.
    """
    if getattr(window, "_process", None) is not None:
        _append_log(window, "[WARN] Automatic JSON ZIP export skipped because another process is active.")
        return

    raw_root = project_root
    if raw_root is None:
        raw_root = window.project_root_edit.text().strip()
    try:
        resolved_project_root = _process_helpers()._tab4_resolve_project_root(raw_root)
    except Exception as exc:
        _append_log(window, "[ERROR] Automatic JSON ZIP export could not resolve project root: " + str(exc))
        return

    final_destination = analysis_json_complete_dir(resolved_project_root).expanduser().resolve()
    pending_build_raw = str(getattr(window, "_pending_second_prompt_build_dir", "") or "").strip()
    pending_final_raw = str(getattr(window, "_pending_second_prompt_final_dir", "") or "").strip()
    destination_path = final_destination
    if pending_build_raw and pending_final_raw:
        pending_build = Path(pending_build_raw).expanduser().resolve(strict=False)
        pending_final = Path(pending_final_raw).expanduser().resolve(strict=False)
        if pending_final == final_destination and pending_build.exists():
            destination_path = pending_build
    destination_path.mkdir(parents=True, exist_ok=True)
    part_size_mb = selected_part_size_mb(window)

    _append_log(window, "Starting automatic JSON ZIP export after Run Collector...")
    _append_log(window, "  manual Zip JSON files button: bypassed")
    _append_log(window, "  root       : " + str(resolved_project_root))
    _append_log(window, "  build/final: " + ("build folder first" if destination_path != final_destination else "final folder"))
    _append_log(window, "  destination: " + str(destination_path))
    _append_log(window, "  final      : " + str(final_destination))
    _append_log(window, "  part size  : " + str(part_size_mb) + " MB")
    _start_zip_process(window, resolved_project_root, destination_path, part_size_mb)


def run_zip_json_files(window: Any) -> None:
    """Prompt for an outside destination and export JSON handoff ZIP parts."""
    if getattr(window, "_process", None) is not None:
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, "Busy", "Wait for the current Tab 4 process to finish.")
        return

    project_root_raw = window.project_root_edit.text().strip()
    try:
        project_root = _process_helpers()._tab4_resolve_project_root(project_root_raw)
    except Exception as exc:
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(
            window,
            "Invalid path",
            "Project root must be a project folder, not a broad drive root.\n" + str(exc),
        )
        return

    if not project_root.is_dir():
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, "Invalid path", "Project root does not exist:\n" + str(project_root))
        return

    QFileDialog = _qt_widgets().QFileDialog
    destination = QFileDialog.getExistingDirectory(
        window,
        "Select ZIP destination outside the project folder",
        _start_folder_for_dialog(project_root),
    )
    if not destination:
        return

    destination_path = Path(destination).expanduser()
    if not destination_path.exists() or not destination_path.is_dir():
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(
            window,
            "Invalid ZIP destination",
            "Selected ZIP destination folder does not exist:\n" + str(destination_path),
        )
        return

    if _destination_inside_project_root(project_root, destination_path):
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(
            window,
            "Invalid ZIP destination",
            "ZIP files cannot be saved inside the active project folder.\n\n"
            "Project root:\n" + str(project_root) + "\n\n"
            "Choose a folder outside the project.",
        )
        return

    _save_destination(str(destination_path))
    part_size_mb = _selected_part_size_mb(window)
    _append_log(window, "Starting JSON ZIP export...")
    _append_log(window, "  root       : " + str(project_root))
    _append_log(window, "  destination: " + str(destination_path))
    _append_log(window, "  part size  : " + str(part_size_mb) + " MB")
    _start_zip_process(window, project_root, destination_path, part_size_mb)
