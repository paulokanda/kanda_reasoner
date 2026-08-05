"""Copy a compact dynamic bridge list for emergency AI handoff."""

from __future__ import annotations

import importlib
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_first_prompt_files_dir,
    analysis_project_freeze_after_update_dir,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.bridge_metadata_classification import (
    bridge_display_name as _bridge_display_name,
    is_active_on_demand_bridge as _is_active_on_demand_bridge,
    prompt_front_matter as _prompt_front_matter,
    startup_source_records as _startup_source_records,
)

__all__ = [
    'BRIDGE_LIST_BEGIN',
    'BRIDGE_LIST_END',
    'BridgeItem',
    'build_complete_bridge_list',
    'copy_complete_bridge_list_to_clipboard',
]


BRIDGE_LIST_BEGIN = "KANDA_COMPLETE_BRIDGE_LIST_BEGIN"
BRIDGE_LIST_END = "KANDA_COMPLETE_BRIDGE_LIST_END"

_STARTUP_ZIP_NAME = "first_prompts_to_ai.zip"
_PROMPT_LIBRARY_ZIP_NAME = "prompt_library.zip"
_TELL_AI_FILENAME = "tell_AI_read_before_all.md"

_ROUTER_BRIDGE_RE = re.compile(r"\brouter_bridge_[A-Za-z0-9_]+\b")
_FEATURE_TITLE_RE = re.compile(r"^feature_title:\s*[\\\"']?([^\\\"']+?)[\\\"']?\s*$", re.IGNORECASE)
_FREEZE_ID_RE = re.compile(r"^freeze_id:\s*[\\\"']?([^\\\"']+?)[\\\"']?\s*$", re.IGNORECASE)
_CODE_MODULE_SIZE_RE = re.compile(r"code module size bridge", re.IGNORECASE)
_LINE_LIMIT_RE = re.compile(r"(?:400|500)\s+(?:lines|code lines)", re.IGNORECASE)
_PROJECT_FEATURE_HANDLING_CHECKLIST = (
    "Confirm the selected Project ID, source root, Tool root, Project Support root, transient root, and self-hosting state.",
    "Classify the operation as PROJECT_OPERATION, TOOL_CHANGE, MIXED_GOVERNED, or BLOCKED before any mutation.",
    "Assign one feature ID and owner Box, then inspect exact current selected-Project source and fingerprints.",
    "Keep KANDA Reasoner Tool source read-only unless a separate Tool defect is proven and independently authorized.",
    "Build the patch payload for the selected Project only and stage ZIPs or extraction under its transient workspace.",
    "Install only into the selected Project target; never fall back to the KANDA Tool root or another Project.",
    "Validate the live selected Project with its governed interpreter and exact installed files; installation is not validation.",
    "Store Project-specific evidence, Error Memory, and Freeze Memory only under the selected Project Support root.",
    "Require human Memorize Error and human Freeze Confirm and Write; never convert staging or Preview into approval.",
    "Refresh the selected Project handoff and startup context after source, prompt, Error Memory, or Freeze changes.",
    "Continue from the last reliable marker and never make the user repeat phases already proven for the same feature and artifact.",
    "Never merge a selected Project feature into KANDA Tool source, another Project, generated handoff evidence, or transient staging.",
    "Keep Show Project to AI separate from portable distribution; portable builds require a separate explicit request.",
)


@dataclass(frozen=True)
class BridgeItem:
    """One compact bridge reminder item."""

    name: str
    source: str
    note: str = ""

    def key(self) -> str:
        return _normalize_name(self.name)


def build_complete_bridge_list(project_root: str | Path) -> str:
    root = Path(project_root).expanduser().resolve(strict=False)
    first_prompt_dir = analysis_first_prompt_files_dir(root)
    startup_items = _collect_startup_bridge_items(root, first_prompt_dir)
    on_demand_items = _collect_on_demand_bridge_items(
        root, first_prompt_dir, {item.key() for item in startup_items}
    )
    frozen_items = _collect_frozen_bridge_memory_items(root)

    lines: list[str] = [
        BRIDGE_LIST_BEGIN,
        "Purpose: emergency AI memory reminder for KANDA bridges.",
        "Use this list only if context amnesia occurs or bridge awareness is uncertain.",
        "A bridge is a direction sign: it points the AI to the correct prompt, rule, or workflow surface.",
        "This list does not replace the startup pack, prompt_library.zip, source inspection, validation, or freeze rules.",
        "When a task matches a bridge below, load or apply the exact referenced prompt/source before acting.",
        "Project root: " + str(root),
        "First prompt files: " + str(first_prompt_dir),
        "Generated UTC: " + datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "",
        "ACTIVE STARTUP BRIDGES",
    ]
    _append_section(lines, startup_items)
    lines.append("")
    lines.append("ON-DEMAND BRIDGES")
    _append_section(lines, on_demand_items)
    lines.append("")
    lines.append("FROZEN BRIDGE MEMORIES")
    _append_section(lines, frozen_items)
    lines.append("")
    lines.append("SELECTED PROJECT FEATURE HANDLING CHECKLIST")
    for checklist_item in _PROJECT_FEATURE_HANDLING_CHECKLIST:
        lines.append("- [ ] " + checklist_item)
    lines.extend(
        [
            "",
            "DO NOT REGRESS",
            "- Keep the Code Module Size Bridge visible at beginning-of-day startup.",
            "- Keep ideal code modules at 400 lines or fewer and maximum code modules at 500 lines or fewer.",
            "- Keep full large_module_refactor_protocol on demand; do not auto-load it during normal startup.",
            "- Keep patch ZIP delivery behind the patch delivery bridge and ZIP contract validation.",
            "- Keep freeze Preview read-only and Confirm and Write human-confirmed.",
            "- Keep project-specific frozen memory under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.",
            BRIDGE_LIST_END,
        ]
    )
    return "\n".join(lines) + "\n"



def _load_qapplication():
    """Return QApplication using a lazy optional Qt import."""
    module = importlib.import_module("PySide6.QtWidgets")
    return module.QApplication


def copy_complete_bridge_list_to_clipboard(window: object) -> None:
    try:
        QApplication = _load_qapplication()

        raw_root = str(getattr(window, "project_root_edit").text()).strip()
        if not raw_root:
            raise ValueError("Project root field is empty.")
        project_root = Path(raw_root).expanduser().resolve(strict=False)
        text = build_complete_bridge_list(project_root)
        QApplication.clipboard().setText(text)
        active_count = _count_section_items(text, "ACTIVE STARTUP BRIDGES")
        on_demand_count = _count_section_items(text, "ON-DEMAND BRIDGES")
        frozen_count = _count_section_items(text, "FROZEN BRIDGE MEMORIES")
        message = (
            "Copied Complete Bridge List: "
            + str(active_count)
            + " active, "
            + str(on_demand_count)
            + " on-demand, "
            + str(frozen_count)
            + " frozen."
        )
        _set_status(window, message)
        _append_log(window, message)
    except Exception as exc:
        message = "[ERROR] Could not copy Complete Bridge List: " + str(exc)
        _set_status(window, message)
        _append_log(window, message)


def _collect_startup_bridge_items(project_root: Path, first_prompt_dir: Path) -> list[BridgeItem]:
    items: list[BridgeItem] = []
    tell_file = first_prompt_dir / _TELL_AI_FILENAME
    items.extend(_items_from_text_file(tell_file, "first_prompt_files/" + _TELL_AI_FILENAME))

    workspace = _workspace_root(project_root)
    source_records = _startup_source_records(workspace)
    generated_entries = tuple(
        str(record.get("generated_filename") or "").strip()
        for record in source_records
        if str(record.get("load_mode") or "").strip().lower() == "always_startup"
        and str(record.get("generated_filename") or "").strip()
    )
    if not generated_entries:
        generated_entries = (
            "00_START_HERE_FOR_AI.md",
            "02_prompt_navigation_index.md",
            "03_GROUP_ASSIMILATION_INDEX.md",
            "05_start_of_day_master_stack.md",
            "07_daily_patch_delivery_guardrails.md",
            "09_active_project_freeze_context.md",
            "14_project_tool_boundary_canon.md",
        )

    startup_zip = first_prompt_dir / _STARTUP_ZIP_NAME
    items.extend(_bridge_items_from_startup_records(source_records, startup_zip))
    items.extend(
        _items_from_zip_entries(
            startup_zip, generated_entries, "first_prompt_files/" + _STARTUP_ZIP_NAME
        )
    )

    if workspace is not None:
        active_stack = (
            workspace / "prompt_library" / "ACTIVE_PROMPTS"
            / "01_session_start_and_navigation" / "start_of_day_master_stack.md"
        )
        items.extend(
            _items_from_text_file(
                active_stack, _relative_to_root(active_stack, project_root)
            )
        )
    return _dedupe_items(items)


def _collect_on_demand_bridge_items(
    project_root: Path,
    first_prompt_dir: Path,
    startup_keys: set[str] | None = None,
) -> list[BridgeItem]:
    excluded = set(startup_keys or set())
    items: list[BridgeItem] = []
    workspace = _workspace_root(project_root)
    if workspace is not None:
        active_root = workspace / "prompt_library" / "ACTIVE_PROMPTS"
        if active_root.is_dir():
            for path in sorted(active_root.rglob("*")):
                if not path.is_file() or _is_noise_path(path):
                    continue
                if "bridge" not in path.name.lower():
                    continue
                text = _read_text(path)
                metadata = _prompt_front_matter(text)
                if not _is_active_on_demand_bridge(metadata):
                    continue
                item = BridgeItem(
                    name=_bridge_display_name(path, metadata),
                    source=_relative_to_root(path, project_root),
                    note="active on-demand prompt/library bridge",
                )
                if item.key() not in excluded:
                    items.append(item)

    prompt_library_zip = first_prompt_dir / _PROMPT_LIBRARY_ZIP_NAME
    items.extend(_items_from_prompt_library_zip(prompt_library_zip, excluded))
    return _dedupe_items(items)


def _bridge_items_from_startup_records(
    records: list[dict[str, object]], startup_zip: Path
) -> list[BridgeItem]:
    available_entries: set[str] = set()
    try:
        with zipfile.ZipFile(startup_zip, "r") as archive:
            available_entries = set(archive.namelist())
    except Exception:
        pass
    items: list[BridgeItem] = []
    for record in records:
        if str(record.get("load_mode") or "").strip().lower() != "always_startup":
            continue
        prompt_id = str(record.get("prompt_id") or "").strip()
        source = str(record.get("canonical_source") or "").strip()
        generated = str(record.get("generated_filename") or "").strip()
        if "bridge" not in (prompt_id + " " + source + " " + generated).lower():
            continue
        zip_source = "first_prompt_files/" + _STARTUP_ZIP_NAME
        if generated and generated in available_entries:
            zip_source += "/" + generated
        note = "always-startup bridge"
        if source:
            note += "; canonical source: " + source
        items.append(BridgeItem(prompt_id or _name_from_path(PurePosixPath(source)), zip_source, note))
    return items


def _collect_frozen_bridge_memory_items(project_root: Path) -> list[BridgeItem]:
    items: list[BridgeItem] = []
    freeze_root = analysis_project_freeze_after_update_dir(project_root) / "frozen_features_memory"
    entries_dir = freeze_root / "entries"
    if not entries_dir.is_dir():
        return items
    for path in sorted(entries_dir.glob("*.md")):
        text = _read_text(path)
        if "bridge" not in text.lower():
            continue
        feature_title = _first_regex_group(_FEATURE_TITLE_RE, text) or _title_from_markdown(text) or path.stem
        freeze_id = _first_regex_group(_FREEZE_ID_RE, text) or path.stem
        items.append(
            BridgeItem(
                name=feature_title.strip(),
                source="project_freeze_after_update/frozen_features_memory/entries/" + path.name,
                note="frozen memory: " + freeze_id.strip(),
            )
        )
    return _dedupe_items(items)


def _items_from_prompt_library_zip(
    zip_path: Path, excluded_keys: set[str] | None = None
) -> list[BridgeItem]:
    excluded = set(excluded_keys or set())
    items: list[BridgeItem] = []
    if not zip_path.is_file():
        return items
    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            for name in sorted(archive.namelist()):
                normalized = name.replace("\\", "/")
                if normalized.endswith("/") or "/ACTIVE_PROMPTS/" not in "/" + normalized:
                    continue
                base = PurePosixPath(normalized).name
                if "bridge" not in base.lower():
                    continue
                text = archive.read(name).decode("utf-8-sig", errors="replace")
                metadata = _prompt_front_matter(text)
                if not _is_active_on_demand_bridge(metadata):
                    continue
                item = BridgeItem(
                    name=_bridge_display_name(PurePosixPath(base), metadata),
                    source="prompt_library.zip/" + normalized,
                    note="active on-demand prompt-library ZIP entry",
                )
                if item.key() not in excluded:
                    items.append(item)
    except Exception:
        return items
    return items


def _items_from_zip_entries(zip_path: Path, entry_names: list[str] | tuple[str, ...], source_prefix: str) -> list[BridgeItem]:
    items: list[BridgeItem] = []
    if not zip_path.is_file():
        return items
    wanted = set(entry_names)
    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            for entry_name in wanted:
                if entry_name not in archive.namelist():
                    continue
                text = archive.read(entry_name).decode("utf-8-sig", errors="replace")
                items.extend(_items_from_text(text, source_prefix + "/" + entry_name))
    except Exception:
        return items
    return items


def _items_from_text_file(path: Path, source: str, token_only: bool = False) -> list[BridgeItem]:
    if not path.is_file():
        return []
    return _items_from_text(_read_text(path), source, token_only=token_only)


def _items_from_text(text: str, source: str, token_only: bool = False) -> list[BridgeItem]:
    items: list[BridgeItem] = []
    if not text:
        return items
    lines = text.splitlines()
    for line in lines:
        stripped = line.strip()
        lowered = stripped.lower()
        if not stripped or "bridge" not in lowered:
            continue
        if _CODE_MODULE_SIZE_RE.search(stripped):
            note = "startup-visible rule"
            if _LINE_LIMIT_RE.search(text):
                note = "startup-visible rule; ideal <=400 lines, maximum <=500 lines"
            items.append(BridgeItem("Code Module Size Bridge", source, note))
        for token in _ROUTER_BRIDGE_RE.findall(stripped):
            items.append(BridgeItem(token, source, "router bridge pointer"))
        if token_only:
            continue
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip(" -")
            if title and "bridge" in title.lower():
                items.append(BridgeItem(title, source, "startup heading"))
        elif lowered.startswith("mandatory") and "bridge" in lowered:
            items.append(BridgeItem(_simple_sentence(stripped), source, "mandatory startup bridge"))
    return items


def _append_section(lines: list[str], items: list[BridgeItem]) -> None:
    if not items:
        lines.append("- No bridge items found in current files.")
        return
    for item in items:
        line = "- " + item.name + " -- " + item.source
        if item.note:
            line += " -- " + item.note
        lines.append(line)


def _dedupe_items(items: list[BridgeItem]) -> list[BridgeItem]:
    seen: set[str] = set()
    unique: list[BridgeItem] = []
    for item in items:
        if not item.name.strip():
            continue
        key = item.key()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return sorted(unique, key=lambda item: (_normalize_name(item.name), item.source.lower()))


def _workspace_root(project_root: Path) -> Path | None:
    direct = project_root / "kanda_prompt_workspace"
    if direct.is_dir():
        return direct
    app_root = Path(__file__).resolve().parents[3]
    fallback = app_root / "kanda_prompt_workspace"
    if fallback.is_dir():
        return fallback
    return None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""


def _first_regex_group(pattern: re.Pattern[str], text: str) -> str:
    for line in text.splitlines():
        match = pattern.match(line.strip())
        if match:
            return match.group(1)
    return ""


def _title_from_markdown(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return ""


def _name_from_path(path: object) -> str:
    name = getattr(path, "name", str(path))
    for suffix in (".meta.json", ".md", ".json", ".txt"):
        if name.lower().endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name


def _relative_to_root(path: Path, project_root: Path) -> str:
    try:
        return str(path.resolve(strict=False).relative_to(project_root.resolve(strict=False))).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def _normalize_name(name: str) -> str:
    normalized = re.sub(r"[_-]+", " ", str(name).strip().lower())
    return re.sub(r"\s+", " ", normalized)


def _simple_sentence(text: str) -> str:
    clean = re.sub(r"\s+", " ", text).strip(" -")
    return clean[:120]


def _is_noise_path(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    return any(part.endswith(".bak") for part in parts) or "__pycache__" in parts


def _count_section_items(text: str, heading: str) -> int:
    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return 0
    count = 0
    for line in lines[start:]:
        if line and line.upper() == line and not line.startswith("-"):
            break
        if line.startswith("- ") and "No bridge items found" not in line:
            count += 1
    return count


def _set_status(window: object, text: str) -> None:
    for attr in ("first_prompt_status_label", "status_label"):
        try:
            target = getattr(window, attr, None)
            if target is not None:
                target.setText(str(text))
                return
        except Exception:
            pass


def _append_log(window: object, text: str) -> None:
    try:
        target = getattr(window, "first_prompt_log_box", None)
        if target is not None:
            target.appendPlainText(str(text))
            return
    except Exception:
        pass
    try:
        window._append_log(str(text))
    except Exception:
        pass
