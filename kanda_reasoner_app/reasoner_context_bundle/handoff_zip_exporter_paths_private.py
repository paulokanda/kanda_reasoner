"""Private path and publication helpers for handoff_zip_exporter."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .schema_models import ProjectContext

__all__: list[str] = []

def _cleanup_created_paths(created_paths: list[Path]) -> None:
    """Support cleanup created paths behavior.
    
    Parameters
    ----------
    created_paths : list[Path]
        The created paths value.
    """
    
    for created_path in created_paths:
        try:
            created_path.unlink()
        except Exception:
            pass


def _retarget_path_string(value: Any, stage: Path, destination: Path) -> Any:
    """Support retarget path string behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    stage : Path
        The stage value.
    destination : Path
        The destination path.
    
    Returns
    -------
    Any
        The any result.
    """
    
    if not isinstance(value, str):
        return value
    stage_text = str(stage)
    dest_text = str(destination)
    return value.replace(stage_text, dest_text).replace(
        stage_text.replace("\\", "/"), dest_text.replace("\\", "/")
    )


def _retarget_record_paths(value: Any, stage: Path, destination: Path) -> Any:
    """Support retarget record paths behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    stage : Path
        The stage value.
    destination : Path
        The destination path.
    
    Returns
    -------
    Any
        The any result.
    """
    
    if isinstance(value, dict):
        return {key: _retarget_record_paths(item, stage, destination) for key, item in value.items()}
    if isinstance(value, list):
        return [_retarget_record_paths(item, stage, destination) for item in value]
    return _retarget_path_string(value, stage, destination)


def _publish_stage_outputs(stage: Path, destination: Path) -> list[Path]:
    """Support publish stage outputs behavior.
    
    Parameters
    ----------
    stage : Path
        The stage value.
    destination : Path
        The destination path.
    
    Returns
    -------
    list[Path]
        The list of values.
    """
    
    published: list[Path] = []
    destination.mkdir(parents=True, exist_ok=True)
    for child in sorted(stage.iterdir(), key=lambda item: item.name.lower()):
        target = destination / child.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.move(str(child), str(target))
        published.append(target)
    return published


def _remove_obsolete_all_in_one_outputs(
    destination: Path,
    project_slug: str,
) -> list[Path]:
    """Remove deprecated all-in-one handoff ZIPs from one destination."""
    removed: list[Path] = []
    pattern = project_slug + "__ai_handoff_all_in_one*.zip"
    if not destination.exists():
        return removed
    for candidate in sorted(destination.glob(pattern), key=lambda item: item.name.lower()):
        if not candidate.is_file():
            continue
        candidate.unlink()
        removed.append(candidate)
    return removed


def _assert_no_forbidden_outputs(output_dir: Path) -> None:
    """Support assert no forbidden outputs behavior.
    
    Parameters
    ----------
    output_dir : Path
        The output dir value.
    """
    
    forbidden_names = {"CHUNK_MANIFEST.json", "json_splitted"}
    for child in output_dir.rglob("*"):
        if child.name in forbidden_names or child.name == "chunks":
            raise ValueError("Forbidden legacy split artifact generated: " + str(child))
        if child.name.endswith("__reconstruction_payload.json"):
            raise ValueError("Forbidden normal reconstruction payload generated: " + str(child))



def _delivery_folder_for_metadata(destination: Path) -> Path:
    """Return the final public folder to write inside artifact metadata."""
    if destination.name == "second_prompt_files_building":
        return destination.with_name("second_prompt_files")
    return destination


def _previous_second_prompt_files_for_reuse(destination: Path) -> Path:
    """Return the selected project's previous final second_prompt_files folder.

    Show Project to AI may build new artifacts in a temporary sibling named
    ``second_prompt_files_building``.  Reusable artifact families, such as
    PNG assets, must be read from the same selected project's previously
    published ``second_prompt_files`` folder, not from the tool installation
    and not from a hard-coded project name.
    """
    if destination.name == "second_prompt_files_building":
        return destination.with_name("second_prompt_files")
    return destination


def _rewrite_text_references(folder: Path, delivery_folder: Path) -> int:
    """Rewrite build/stage folder references to the public delivery folder."""
    replacements = (
        (str(folder), str(delivery_folder)),
        (str(folder).replace("\\", "/"), str(delivery_folder).replace("\\", "/")),
        ("show_project_to_AI/second_prompt_files_building", "show_project_to_AI/second_prompt_files"),
        ("show_project_to_AI\\second_prompt_files_building", "show_project_to_AI\\second_prompt_files"),
        ("second_prompt_files_building", "second_prompt_files"),
    )
    changed = 0
    if not folder.exists():
        return changed
    for path in folder.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".txt", ".md"}:
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


def _finalize_ai_context_artifacts_for_handoff(context: ProjectContext, destination: Path) -> None:
    """Refresh JSON artifacts before they are copied into upload ZIPs.

    The GUI builds in ``second_prompt_files_building`` and publishes later.
    Upload ZIPs are created before that publish step, so this function rewrites
    metadata to the final delivery folder and refreshes the mutually linked
    briefing/manifest pair before packaging.
    """
    from .ai_briefing_builder import write_ai_briefing_json
    from .bundle_manifest_builder import write_bundle_manifest_json

    delivery_folder = _delivery_folder_for_metadata(destination)
    _rewrite_text_references(destination, delivery_folder)
    write_ai_briefing_json(context)
    _rewrite_text_references(destination, delivery_folder)
    write_bundle_manifest_json(context)
    _rewrite_text_references(destination, delivery_folder)
    write_ai_briefing_json(context)
    _rewrite_text_references(destination, delivery_folder)
    write_bundle_manifest_json(context)
    _rewrite_text_references(destination, delivery_folder)
