# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py
"""Second-prompt publication and generated-artifact cleanup helpers."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV,
    SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV,
    analysis_json_building_dir,
    project_analysis_evidence_root,
    project_name_from_root,
)
from kanda_reasoner_app.local_ai_json_contract import refresh_local_ai_copy
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_paths_private_impl import (
    _is_transient_daily_refactor_folder,
    _require_show_project_child_dir,
    cleanup_show_project_to_ai_root_after_success,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_state_private_impl import (
    STATUS_FILE_NAME,
)

__all__ = []


def second_prompt_files_building_dir(project_root: str | Path) -> Path:
    """Return the temporary second-prompt build directory for one project."""
    return analysis_json_building_dir(project_root).expanduser().resolve(strict=False)


def _clear_dir_contents(resolved_dir: Path) -> int:
    """Support clear dir contents behavior.
    
    Parameters
    ----------
    resolved_dir : Path
        The resolved dir value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    resolved_dir.mkdir(parents=True, exist_ok=True)
    removed = 0
    for child in resolved_dir.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
        removed += 1
    return removed


def write_second_prompt_status(output_dir: str | Path, *, status: str, step: str, project_root: str | Path | None=None, final_output_dir: str | Path | None=None, details: list[str] | None=None) -> Path:
    """Write a small visible status file for long Show Project to AI builds."""
    resolved_dir = Path(output_dir).expanduser().resolve(strict=False)
    resolved_dir.mkdir(parents=True, exist_ok=True)
    lines = ['Show Project to AI - Second Prompt Files', 'Status: ' + str(status), 'Step: ' + str(step), 'Output folder: ' + str(resolved_dir)]
    if project_root is not None:
        lines.append('Project root: ' + str(project_root))
    if final_output_dir is not None:
        lines.append('Final folder: ' + str(final_output_dir))
    if details:
        lines.append('')
        lines.extend((str(item) for item in details))
    lines.append('')
    status_path = resolved_dir / STATUS_FILE_NAME
    status_path.write_text('\n'.join(lines), encoding='utf-8')
    return status_path


def clear_second_prompt_files_building_dir(output_dir: str | Path) -> int:
    """Clear only the approved second_prompt_files_building output directory."""
    resolved_dir = _require_show_project_child_dir(output_dir, 'second_prompt_files_building')
    return _clear_dir_contents(resolved_dir)


def _rewrite_generated_text_paths(build_dir: Path, final_dir: Path) -> int:
    """Rewrite temporary build-folder references to final-folder references."""
    replacements = ((str(build_dir), str(final_dir)), (str(build_dir).replace('\\', '/'), str(final_dir).replace('\\', '/')), ('show_project_to_AI/second_prompt_files_building', 'show_project_to_AI/second_prompt_files'), ('show_project_to_AI\\second_prompt_files_building', 'show_project_to_AI\\second_prompt_files'), ('second_prompt_files_building', 'second_prompt_files'))
    changed = 0
    for path in build_dir.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {'.json', '.txt', '.md'}:
            continue
        try:
            text = path.read_text(encoding='utf-8-sig')
        except UnicodeDecodeError:
            continue
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding='utf-8')
            changed += 1
    return changed


def _refresh_bundle_manifest_after_publish_rewrite(build_dir: Path, final_dir: Path, *, project_root: str | Path | None) -> Path | None:
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
    from kanda_reasoner_app.reasoner_context_bundle.bundle_manifest_builder import write_bundle_manifest_json
    root_path = Path(project_root).expanduser().resolve(strict=False)
    evidence_root = project_analysis_evidence_root(root_path).expanduser().resolve(strict=False)
    try:
        build_dir.relative_to(evidence_root)
    except ValueError:
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
    _rewrite_generated_text_paths(build_dir, final_dir)
    return manifest_path


def _remove_forbidden_second_prompt_payloads(final_path: Path, project_root: str | Path | None=None) -> list[str]:
    """Remove stale heavy payloads that are not part of normal hybrid output."""
    removed: list[str] = []
    slug = ''
    if project_root is not None:
        try:
            slug = project_name_from_root(project_root)
        except Exception:
            slug = ''
    forbidden_suffixes = ('__complete.json', '__active_snapshot.json', '__reconstruction_payload.json')
    for child in list(final_path.iterdir()) if final_path.exists() and final_path.is_dir() else []:
        if not child.is_file():
            continue
        if child.name.endswith(forbidden_suffixes) or (slug and child.name in {slug + '__complete_runtime_trace.json'}):
            try:
                child.unlink()
                removed.append(str(child))
            except Exception:
                pass
    return removed


def _refresh_project_qa_local_ai_json_before_cleanup(
    final_path: Path,
    project_root: str | Path | None = None,
) -> list[str]:
    """Refresh Project A&A local-AI JSON before loose JSON cleanup.

    Show Project to AI may remove loose web-AI JSON artifacts after ZIP export,
    but the local Project A&A tab needs an on-disk JSON evidence file for the
    selected project. This helper copies the freshly generated canonical
    ``<slug>__complete.json`` bytes to ``<slug>__complete_local_AI.json`` under
    the same dynamic ``<project>_show_project_to_AI/second_prompt_files`` root
    before the canonical loose JSON is removed.
    """
    if project_root is None:
        return []
    try:
        slug = project_name_from_root(project_root)
    except Exception:
        return []
    if not slug:
        return []

    canonical_path = final_path / (slug + "__complete.json")
    if not canonical_path.is_file():
        return []

    try:
        result = refresh_local_ai_copy(project_root)
    except Exception:
        return []

    local_ai_json = str(getattr(result, "local_ai_json", "") or "")
    if not local_ai_json:
        return []
    return [local_ai_json]


def cleanup_loose_json_files_after_success(final_path: str | Path) -> list[str]:
    """Remove loose JSON artifacts after their ZIP handoff package exists.

    The normal second-stage AI upload reads JSON artifacts from
    ``*_ai_handoff_upload.zip``.  Keeping loose JSON siblings in
    ``second_prompt_files`` is useful while building and auditing, but after a
    successful ZIP export they are duplicate delivery noise.  This helper only
    deletes root-level ``*.json`` files from the approved final folder; ZIP
    contents are never modified.
    """
    resolved_dir = _require_show_project_child_dir(final_path, 'second_prompt_files')
    removed: list[str] = []
    if not resolved_dir.exists() or not resolved_dir.is_dir():
        return removed
    upload_zips = [child for child in resolved_dir.iterdir() if child.is_file() and child.suffix.lower() == '.zip' and ('__ai_handoff_upload' in child.name)]
    if not upload_zips:
        return removed
    for child in sorted(resolved_dir.iterdir(), key=lambda item: item.name.lower()):
        if not child.is_file() or child.suffix.lower() != '.json':
            continue
        if '__error_' in child.name or '__error_memory' in child.name:
            continue
        name_lower = child.name.lower()
        if name_lower.endswith('__complete_local_ai.json') or name_lower.endswith('__complete_local_ai.meta.json'):
            continue
        if name_lower.endswith('__complete_json_manifest.json'):
            continue
        try:
            child.unlink()
            removed.append(str(child))
        except Exception:
            pass
    return removed


def cleanup_transient_daily_refactor_folders(project_root: str | Path | None, *, final_dir: str | Path | None=None) -> list[str]:
    """Remove transient daily-refactor output folders after successful handoff.

    Cleanup is deliberately scoped to the external Show Project to AI output
    tree and, optionally, its final ``second_prompt_files`` child.  It never
    deletes folders from the selected source project itself, so source modules
    such as ``kanda_reasoner_app/daily_rfctr_report`` are protected.
    """
    candidates: list[Path] = []
    if project_root is not None:
        try:
            candidates.append(project_analysis_evidence_root(project_root).expanduser().resolve(strict=False))
        except Exception:
            pass
    if final_dir is not None:
        try:
            candidates.append(Path(final_dir).expanduser().resolve(strict=False))
        except Exception:
            pass
    removed: list[str] = []
    seen: set[str] = set()
    for base in candidates:
        key = str(base)
        if key in seen or not base.exists() or (not base.is_dir()):
            continue
        seen.add(key)
        for child in sorted(base.iterdir(), key=lambda item: item.name.lower()):
            if not child.is_dir() or not _is_transient_daily_refactor_folder(child):
                continue
            try:
                shutil.rmtree(child)
                removed.append(str(child))
            except Exception:
                pass
    return removed


def publish_second_prompt_files_building_dir(building_dir: str | Path, final_dir: str | Path, *, project_root: str | Path | None=None) -> dict[str, object]:
    """Atomically publish a completed build folder into second_prompt_files.

    The final folder is not deleted or replaced until the build folder already
    contains the generated JSON artifacts and ZIP export artifacts. On failure,
    the previous final delivery is restored when possible. On success, temporary
    siblings such as second_prompt_files_building and json_splitted are removed
    so the show_project_to_AI root normally contains only first_prompt_files and
    second_prompt_files.
    """
    build_path = _require_show_project_child_dir(building_dir, 'second_prompt_files_building')
    final_path = _require_show_project_child_dir(final_dir, 'second_prompt_files')
    if build_path.parent != final_path.parent:
        raise ValueError('Refusing to publish because build and final folders are not siblings: ' + str(build_path) + ' -> ' + str(final_path))
    if not build_path.exists() or not build_path.is_dir():
        raise ValueError('Build folder does not exist: ' + str(build_path))
    rewritten_files = _rewrite_generated_text_paths(build_path, final_path)
    refreshed_manifest = _refresh_bundle_manifest_after_publish_rewrite(build_path, final_path, project_root=project_root)
    parent = final_path.parent
    token = str(os.getpid()) + '_' + str(abs(hash(str(build_path))))
    stage_path = parent / ('.second_prompt_files_publish_' + token)
    backup_path = parent / ('.second_prompt_files_previous_' + token)
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
        if final_path.exists() and backup_path.exists():
            try:
                if final_path.is_dir():
                    shutil.rmtree(final_path)
                else:
                    final_path.unlink()
            except Exception:
                pass
        if backup_path.exists() and (not final_path.exists()):
            try:
                shutil.move(str(backup_path), str(final_path))
            except Exception:
                pass
        if stage_path.exists() and (not build_path.exists()):
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
    refreshed_project_qa_local_ai_json = _refresh_project_qa_local_ai_json_before_cleanup(final_path, project_root)
    removed_forbidden_payloads = _remove_forbidden_second_prompt_payloads(final_path, project_root)
    removed_loose_json_files = cleanup_loose_json_files_after_success(final_path)
    removed_daily_refactor_folders = cleanup_transient_daily_refactor_folders(project_root, final_dir=final_path)
    cleanup_result = {'removed': [], 'skipped': []}
    if project_root is not None:
        cleanup_result = cleanup_show_project_to_ai_root_after_success(project_root, final_dir=final_path)
    write_second_prompt_status(final_path, status='complete', step='published generated files and ZIP export', project_root=project_root, final_output_dir=final_path, details=['Published from temporary folder: ' + str(build_path), 'Moved items: ' + str(moved_items), 'Removed old final-folder items: ' + str(removed_final_items), 'Rewritten generated text files: ' + str(rewritten_files), 'Cleaned stale root items: ' + str(len(cleanup_result.get('removed', []))), 'Removed stale heavy payloads from final folder: ' + str(len(removed_forbidden_payloads)), 'Removed loose JSON files after ZIP export: ' + str(len(removed_loose_json_files)), 'Removed transient daily_refactor folders: ' + str(len(removed_daily_refactor_folders))])
    return {'building_dir': str(build_path), 'final_dir': str(final_path), 'moved_items': moved_items, 'removed_final_items': removed_final_items, 'rewritten_files': rewritten_files, 'refreshed_bundle_manifest': str(refreshed_manifest) if refreshed_manifest is not None else '', 'cleanup_result': cleanup_result, 'refreshed_project_qa_local_ai_json': refreshed_project_qa_local_ai_json, 'removed_forbidden_payloads': removed_forbidden_payloads, 'removed_loose_json_files': removed_loose_json_files, 'removed_daily_refactor_folders': removed_daily_refactor_folders}


def clear_second_prompt_files_dir(output_dir: str | Path) -> int:
    """Clear only the approved second_prompt_files output directory contents."""
    resolved_dir = _require_show_project_child_dir(output_dir, 'second_prompt_files')
    return _clear_dir_contents(resolved_dir)

