"""GUI tab for local freeze after update, auto-filled local freezing, and optional external AI review export."""

from __future__ import annotations

import importlib
import json
import queue
import threading
from pathlib import Path
from typing import Any

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QDesktopServices, QFont, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.freeze_after_update.contract import (
    ensure_freeze_after_update_box,
    generate_freeze_after_update_ai_files,
    inspect_freeze_after_update_box,
    preview_freeze_entry,
    refresh_freeze_exposure,
    refresh_ai_compliance_context,
    validate_freeze_entry_preview,
    write_confirmed_freeze_entry,
)
from kanda_reasoner_app.freeze_hint_intake import (
    build_freeze_form_inputs_from_latest_hint,
    mark_latest_freeze_hint_used,
)
from kanda_reasoner_app.freeze_after_update.paths import build_paths
from kanda_reasoner_app.freeze_after_update.result import FreezeAfterUpdateResult
from kanda_reasoner_app.freeze_after_update_gui.local_freeze_preview_log import (
    build_local_freeze_preview_log_text,
)


AUTO_LOCAL_AI_MODEL_LABEL = "Auto (first available Ollama model)"
MODEL_REGISTRY_MODULE = "kanda_reasoner_app.reasoner_engine.v10_model_registry"
MODEL_REGISTRY_CLASS = "LocalModelRegistry"
LOCAL_AI_MODULE = "kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models"
LOCAL_AI_CLASS = "V9QwenAIModels"


def _load_local_ai_class(module_name: str, class_name: str) -> type[Any]:
    """Load local AI helper classes through a late-bound GUI-safe boundary."""
    module = importlib.import_module(module_name)
    loaded = getattr(module, class_name)
    if not isinstance(loaded, type):
        raise TypeError(module_name + "." + class_name + " is not a class")
    return loaded


def _list_local_ai_models() -> list[str]:
    """Return local Ollama models from the shared KANDA model registry."""
    registry_class = _load_local_ai_class(MODEL_REGISTRY_MODULE, MODEL_REGISTRY_CLASS)
    registry = registry_class()
    models = registry.list_models()
    return [str(model).strip() for model in models if str(model).strip()]


def _model_name_from_local_ai_combo_text(text: str) -> str:
    """Normalize the Local Freeze Entry model combo text."""
    selected = str(text or "").strip()
    if not selected or selected == AUTO_LOCAL_AI_MODEL_LABEL:
        return ""
    return selected


def _choose_local_ai_model(requested_model: str = "") -> str:
    """Choose a local AI model from a requested value or the first available model."""
    models = _list_local_ai_models()
    requested = str(requested_model or "").strip()
    if requested and requested in models:
        return requested
    if models:
        return models[0]
    return requested


def _build_local_ai_freeze_form_messages(inputs: dict, project_root: Path) -> list[dict[str, str]]:
    """Build a compact local-AI prompt that improves, but never weakens, the freeze form."""
    current_json = json.dumps(inputs, ensure_ascii=False, indent=2)
    keys = ", ".join([
        "feature_title",
        "primary_box",
        "box_type",
        "validated_files",
        "generated_files",
        "protected_paths",
        "do_not_regress_rules",
        "validation_evidence_summary",
        "known_warnings",
        "planned_next_step",
        "notes",
    ])
    return [
        {
            "role": "system",
            "content": (
                "You edit one JSON object. Return only valid JSON. "
                "Do not repeat the prompt. Do not explain. Do not use markdown. "
                "Never delete existing paths, rules, or validation lines."
            ),
        },
        {
            "role": "user",
            "content": (
                "Instruction: Improve the KANDA freeze form JSON only if needed.\n"
                "Required output: one JSON object only, starting with { and ending with }.\n"
                "NO prose. NO markdown. NO marker block. NO comments.\n"
                f"Allowed keys only: {keys}.\n"
                "Hard rules:\n"
                "- Preserve every existing validation line exactly.\n"
                "- Preserve every existing protected path exactly.\n"
                "- Preserve every existing do-not-regress rule; you may append clearer rules only.\n"
                "- Keep project-specific frozen memory under project_freeze_after_update/frozen_features_memory.\n"
                "- Do not store project-specific frozen memory inside project_freeze_ledger.\n"
                "- If unsure, return the input JSON unchanged.\n"
                "- Do not write the words Context:, Task:, Critical rules:, Return format, or Copy/paste-ready answer shape.\n"
                f"Active project root: {project_root}\n"
                "JSON TO REVIEW:\n"
                f"{current_json}\n"
            ),
        },
    ]


def _nonempty_lines(value: Any) -> list[str]:
    """Return non-empty normalized lines from a freeze-form multiline value."""
    return [line.strip() for line in str(value or "").splitlines() if line.strip()]


def _normalized_line_set(value: Any) -> set[str]:
    """Return case-insensitive normalized lines for quality-gate comparison."""
    return {" ".join(line.lower().split()) for line in _nonempty_lines(value)}


def _local_ai_response_looks_like_prompt_echo(response_text: str) -> bool:
    """Detect local model responses that echoed the task prompt instead of returning a form."""
    text = str(response_text or "")
    echo_markers = [
        "You are a specialist in KANDA Reasoner",
        "Context:\nI just implemented",
        "Task:\nReview and correct",
        "Critical rules:",
        "Return format - strict copy/paste contract",
        "Copy/paste-ready answer shape:",
        "Current auto-filled form JSON",
    ]
    return sum(1 for marker in echo_markers if marker in text) >= 2


def _validate_local_ai_form_against_heuristic(candidate: dict, heuristic: dict) -> tuple[bool, list[str]]:
    """Reject local AI output that weakens the deterministic heuristic baseline."""
    reasons: list[str] = []
    required_keys = set(heuristic.keys())
    missing_keys = sorted(key for key in required_keys if key not in candidate or str(candidate.get(key, "")).strip() == "")
    if missing_keys:
        reasons.append("missing required field(s): " + ", ".join(missing_keys))

    combined_candidate_text = "\n".join(str(candidate.get(key, "")) for key in required_keys)
    forbidden_echo_markers = [
        "You are a specialist in KANDA Reasoner",
        "Return format - strict copy/paste contract",
        "Copy/paste-ready answer shape",
        "Current auto-filled form JSON",
    ]
    if any(marker in combined_candidate_text for marker in forbidden_echo_markers):
        reasons.append("contains copied prompt/instruction text")

    typo_markers = ["freez_context", "freez context", "prqject_freeze", "KAN DA_F RE EZE"]
    if any(marker.lower() in combined_candidate_text.lower() for marker in typo_markers):
        reasons.append("contains known AI typo/damaged marker text")

    line_preserve_fields = [
        "validated_files",
        "generated_files",
        "protected_paths",
        "do_not_regress_rules",
        "validation_evidence_summary",
    ]
    for field in line_preserve_fields:
        heuristic_lines = _normalized_line_set(heuristic.get(field, ""))
        candidate_lines = _normalized_line_set(candidate.get(field, ""))
        missing_lines = sorted(heuristic_lines - candidate_lines)
        if missing_lines:
            preview = "; ".join(missing_lines[:3])
            if len(missing_lines) > 3:
                preview += "; ..."
            reasons.append(f"{field} lost baseline line(s): {preview}")

    if len(_nonempty_lines(candidate.get("do_not_regress_rules", ""))) < len(_nonempty_lines(heuristic.get("do_not_regress_rules", ""))):
        reasons.append("do_not_regress_rules became shorter than heuristic baseline")
    if len(_nonempty_lines(candidate.get("validation_evidence_summary", ""))) < len(_nonempty_lines(heuristic.get("validation_evidence_summary", ""))):
        reasons.append("validation_evidence_summary became shorter than heuristic baseline")
    if len(_nonempty_lines(candidate.get("protected_paths", ""))) < len(_nonempty_lines(heuristic.get("protected_paths", ""))):
        reasons.append("protected_paths became shorter than heuristic baseline")

    return (not reasons, reasons)


class LocalFreezeAIFormularyRunner:
    """Pure-Python runner that asks a local Ollama model to fill the freeze form.

    This intentionally avoids QThread/QObject signal wiring. The GUI starts it in a
    daemon Python thread and polls a queue from the Qt main thread, which is safer
    during shutdown and dialog close on Windows/PySide.
    """

    def __init__(self, *, inputs: dict, project_root: Path, model_name: str = "") -> None:
        self._inputs = dict(inputs)
        self._project_root = Path(project_root)
        self._requested_model = str(model_name or "").strip()

    def run(self) -> tuple[bool, str, str]:
        """Run the local AI fill request and return (ok, response_or_error, model)."""
        try:
            model_name = _choose_local_ai_model(self._requested_model)
            if not model_name:
                raise RuntimeError(
                    "No local Ollama model is available. Use Heuristics mode or refresh/install a local model."
                )
            ai_class = _load_local_ai_class(LOCAL_AI_MODULE, LOCAL_AI_CLASS)
            ai = ai_class()
            response_text = ai.chat(
                _build_local_ai_freeze_form_messages(self._inputs, self._project_root),
                model=model_name,
                temperature=0.05,
                max_tokens=2600,
                use_cache=False,
            )
            return True, str(response_text or ""), model_name
        except Exception as exc:
            return False, str(exc), ""


class FreezeAfterUpdateTab(QWidget):
    """Human-facing controller for the project-local freeze-after-update box."""

    def __init__(self) -> None:
        super().__init__()
        self._last_output_folder: Path | None = None
        self._pending_staged_project_root: Path | None = None
        self._pending_staged_action: str | None = None
        self._local_freeze_preview: dict | None = None
        self._local_freeze_dialog: QDialog | None = None
        self._what_to_say_dialog: QDialog | None = None
        self._what_to_say_text_edit: QTextEdit | None = None
        self._local_freeze_ai_thread: threading.Thread | None = None
        self._local_freeze_ai_result_queue: queue.Queue | None = None
        self._local_freeze_ai_request_id: object | None = None
        self._local_freeze_ai_poll_timer: QTimer | None = None
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        title = QLabel("Freeze Feature After Update")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title.setFont(title_font)
        header_layout.addWidget(title, 1)

        self.help_button = QPushButton("Help")
        self.help_button.setToolTip("Open practical help for the Freeze Feature After Update tab")
        header_layout.addWidget(self.help_button, 0)

        root_layout.addLayout(header_layout)

        intro = QLabel(
            "Prepare or execute the project-local freeze / AI-compliance flow after "
            "a validated update. Normal freezing happens locally through preview and "
            "human confirmation. External AI review export remains available as an "
            "advanced fallback. Frozen memory stays inside the actual project."
        )
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(12)
        root_layout.addLayout(columns_layout, 1)

        left_column_widget = QWidget()
        left_column = QVBoxLayout(left_column_widget)
        left_column.setContentsMargins(0, 0, 0, 0)
        left_column.setSpacing(10)

        right_column_widget = QWidget()
        right_column = QVBoxLayout(right_column_widget)
        right_column.setContentsMargins(0, 0, 0, 0)
        right_column.setSpacing(10)

        columns_layout.addWidget(left_column_widget, 1)
        columns_layout.addWidget(right_column_widget, 1)

        project_group = QGroupBox("Active project")
        project_layout = QGridLayout(project_group)
        project_layout.setColumnStretch(1, 1)

        project_layout.addWidget(QLabel("Project root:"), 0, 0)
        self.project_root_edit = QLineEdit()
        self.project_root_edit.setPlaceholderText("Select or receive the current project root")
        project_layout.addWidget(self.project_root_edit, 0, 1)

        self.choose_project_button = QPushButton("Choose Project Folder")
        project_layout.addWidget(self.choose_project_button, 0, 2)

        project_layout.addWidget(QLabel("Box folder:"), 1, 0)
        self.box_folder_edit = QLineEdit()
        self.box_folder_edit.setReadOnly(True)
        project_layout.addWidget(self.box_folder_edit, 1, 1, 1, 2)

        project_layout.addWidget(QLabel("External AI review folder:"), 2, 0)
        self.files_to_send_path_edit = QLineEdit()
        self.files_to_send_path_edit.setReadOnly(True)
        project_layout.addWidget(self.files_to_send_path_edit, 2, 1, 1, 2)

        left_column.addWidget(project_group)

        status_group = QGroupBox("Status, local workflow, and advanced export")
        status_layout = QGridLayout(status_group)
        status_layout.setColumnStretch(1, 1)

        status_layout.addWidget(QLabel("Status:"), 0, 0)
        self.status_label = QLabel("Not checked yet")
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label, 0, 1, 1, 3)

        self.check_button = QPushButton("Check Box Status")
        self.create_button = QPushButton("Create / Repair Box")
        self.generate_button = QPushButton("Export for External AI Review")
        self.open_box_button = QPushButton("Open project_freeze_after_update")
        self.open_output_button = QPushButton("Open External AI Review Folder")
        self.copy_output_path_button = QPushButton("Copy External AI Review Folder Path")
        self.show_instruction_button = QPushButton("Show what_to_say_to_ai")

        status_layout.addWidget(self.check_button, 1, 0)
        status_layout.addWidget(self.create_button, 1, 1)
        status_layout.addWidget(self.generate_button, 1, 2)
        status_layout.addWidget(self.open_box_button, 2, 0)
        status_layout.addWidget(self.open_output_button, 2, 1)
        status_layout.addWidget(self.copy_output_path_button, 2, 2)
        status_layout.addWidget(self.show_instruction_button, 3, 0, 1, 3)

        left_column.addWidget(status_group)

        staged_group = QGroupBox("Staged freeze / AI compliance action")
        staged_layout = QGridLayout(staged_group)
        staged_layout.setColumnStretch(1, 1)

        self.prepare_staged_action_button = QPushButton("Prepare Freeze / AI Compliance Update")
        self.do_staged_action_button = QPushButton("Do it")
        self.undo_staged_action_button = QPushButton("Undo / Cancel")
        self.do_staged_action_button.setEnabled(False)
        self.undo_staged_action_button.setEnabled(False)

        staged_help = QLabel(
            "Click Prepare first. The log will show exactly what will be read, "
            "written, refreshed, and not touched. Nothing changes until Do it."
        )
        staged_help.setWordWrap(True)

        staged_layout.addWidget(staged_help, 0, 0, 1, 3)
        staged_layout.addWidget(self.prepare_staged_action_button, 1, 0)
        staged_layout.addWidget(self.do_staged_action_button, 1, 1)
        staged_layout.addWidget(self.undo_staged_action_button, 1, 2)

        left_column.addWidget(staged_group)

        local_freeze_group = QGroupBox("Local freeze entry")
        local_freeze_layout = QGridLayout(local_freeze_group)
        local_freeze_layout.setColumnStretch(1, 1)

        local_freeze_help = QLabel(
            "Create a local freeze entry from this tab. The form now defaults to Local AI auto-fill "
            "when a local model is available, with a safe heuristic fallback. It immediately builds "
            "a preview and then waits for human confirmation before writing."
        )
        local_freeze_help.setWordWrap(True)
        self.new_local_freeze_entry_button = QPushButton("New Local Freeze Entry")
        self.new_local_freeze_entry_button.setToolTip("Open an auto-filled local freeze draft; review, preview, then confirm/write")

        local_freeze_layout.addWidget(local_freeze_help, 0, 0, 1, 2)
        local_freeze_layout.addWidget(self.new_local_freeze_entry_button, 1, 0)

        left_column.addWidget(local_freeze_group)

        outputs_group = QGroupBox("Advanced external AI review export")
        outputs_layout = QGridLayout(outputs_group)
        outputs_layout.setColumnStretch(1, 1)

        outputs_layout.addWidget(QLabel("ZIP:"), 0, 0)
        self.zip_edit = QLineEdit()
        self.zip_edit.setReadOnly(True)
        outputs_layout.addWidget(self.zip_edit, 0, 1)

        outputs_layout.addWidget(QLabel("Instruction MD:"), 1, 0)
        self.instruction_edit = QLineEdit()
        self.instruction_edit.setReadOnly(True)
        outputs_layout.addWidget(self.instruction_edit, 1, 1)

        left_column.addWidget(outputs_group)
        left_column.addStretch(1)

        log_group = QGroupBox("Log window")
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(8, 8, 8, 8)
        log_layout.setSpacing(6)

        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setPlaceholderText("Output log")
        log_layout.addWidget(self.output_log, 1)

        right_column.addWidget(log_group, 1)

        self._refresh_derived_paths()

    def _connect_signals(self) -> None:
        self.project_root_edit.textChanged.connect(self._refresh_derived_paths)
        self.choose_project_button.clicked.connect(self._choose_project_folder)
        self.check_button.clicked.connect(self._check_box_status)
        self.create_button.clicked.connect(self._create_or_repair_box)
        self.generate_button.clicked.connect(self._generate_files)
        self.prepare_staged_action_button.clicked.connect(self._prepare_staged_freeze_action)
        self.do_staged_action_button.clicked.connect(self._do_staged_freeze_action)
        self.undo_staged_action_button.clicked.connect(self._undo_staged_freeze_action)
        self.new_local_freeze_entry_button.clicked.connect(self._open_local_freeze_entry_dialog)
        self.open_box_button.clicked.connect(self._open_box_folder)
        self.open_output_button.clicked.connect(self._open_output_folder)
        self.copy_output_path_button.clicked.connect(self._copy_output_folder_path)
        self.show_instruction_button.clicked.connect(self._show_what_to_say_window)
        self.help_button.clicked.connect(self._show_help_window)

    def _project_root(self) -> Path | None:
        text = self.project_root_edit.text().strip()
        if not text:
            return None
        return Path(text).expanduser()

    def _paths(self):
        project_root = self._project_root()
        if project_root is None:
            return None
        return build_paths(project_root)

    def _refresh_derived_paths(self) -> None:
        paths = self._paths()
        if paths is None:
            self.box_folder_edit.clear()
            self.files_to_send_path_edit.clear()
            return
        self.box_folder_edit.setText(str(paths.box_root))
        self.files_to_send_path_edit.setText(str(paths.send_root))

    def _choose_project_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose Project Folder")
        if folder:
            self.project_root_edit.setText(folder)

    def _append_log(self, message: str) -> None:
        self.output_log.append(message)

    def _append_log_block(self, text: str) -> None:
        """Append a plain-text block to the visible log without HTML rendering."""
        block = str(text or "").rstrip()
        if not block:
            return
        current = self.output_log.toPlainText().rstrip()
        combined = (current + "\n" if current else "") + block + "\n"
        self.output_log.setPlainText(combined)
        self.output_log.moveCursor(QTextCursor.MoveOperation.End)

    def _show_result(self, result: FreezeAfterUpdateResult) -> None:
        status_text = f"{result.status.value}: {result.message}"
        self.status_label.setText(status_text)
        self._append_log(status_text)

        if result.box_root is not None:
            self.box_folder_edit.setText(str(result.box_root))
            self.files_to_send_path_edit.setText(str(result.box_root / "files_to_send_ai"))

        if result.missing_paths:
            self._append_log("Missing paths:")
            for path in result.missing_paths:
                self._append_log(f"- {path}")

        if result.created_paths:
            self._append_log("Created paths:")
            for path in result.created_paths:
                self._append_log(f"- {path}")

        if result.output_zip is not None:
            self.zip_edit.setText(str(result.output_zip))
            self._last_output_folder = result.output_zip.parent
            self.files_to_send_path_edit.setText(str(result.output_zip.parent))
            self._append_log(f"ZIP created: {result.output_zip}")

        if result.output_instruction is not None:
            self.instruction_edit.setText(str(result.output_instruction))
            self._last_output_folder = result.output_instruction.parent
            self.files_to_send_path_edit.setText(str(result.output_instruction.parent))
            self._append_log(f"Instruction file created: {result.output_instruction}")

        if result.freeze_count:
            self._append_log(f"Freeze entries included: {result.freeze_count}")
        else:
            self._append_log("Freeze entries included: 0")

    def _require_project_root(self) -> Path | None:
        project_root = self._project_root()
        if project_root is None:
            QMessageBox.warning(self, "Project missing", "Select a project folder first.")
            return None
        return project_root

    def _check_box_status(self) -> None:
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(inspect_freeze_after_update_box(project_root))

    def _create_or_repair_box(self) -> None:
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(ensure_freeze_after_update_box(project_root))

    def _generate_files(self) -> None:
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(generate_freeze_after_update_ai_files(project_root))

    def _set_pending_staged_action(self, project_root: Path | None, action: str | None) -> None:
        self._pending_staged_project_root = project_root
        self._pending_staged_action = action
        has_pending = project_root is not None and action is not None
        self.do_staged_action_button.setEnabled(has_pending)
        self.undo_staged_action_button.setEnabled(has_pending)

    def _prepare_staged_freeze_action(self) -> None:
        project_root = self._require_project_root()
        if project_root is None:
            return

        paths = build_paths(project_root)
        exposure = refresh_freeze_exposure(project_root)
        exposure_status = exposure.get("status") or "UNKNOWN"
        exposure_warnings = exposure.get("warnings") or []
        exposure_errors = exposure.get("errors") or []

        self.output_log.clear()
        self.status_label.setText("Prepared staged freeze / AI compliance action. Review log, then choose Do it or Undo / Cancel.")
        self._append_log("STAGED ACTION PREVIEW")
        self._append_log("")
        self._append_log("Action: refresh Freeze Feature After Update AI compliance package")
        self._append_log(f"Active project: {paths.project_root}")
        self._append_log(f"Current freeze exposure status: {exposure_status}")

        if exposure_warnings:
            self._append_log("Warnings from current freeze exposure:")
            for warning in exposure_warnings:
                self._append_log(f"- {warning}")

        if exposure_errors:
            self._append_log("Current freeze exposure errors:")
            for error in exposure_errors:
                self._append_log(f"- {error}")

        self._append_log("")
        self._append_log("WILL READ:")
        self._append_log(f"- {paths.memory_root}")
        self._append_log(f"- {paths.freeze_index}")
        self._append_log(f"- {paths.frozen_steps}")
        self._append_log(f"- {paths.entries_root}")

        self._append_log("")
        self._append_log("WILL WRITE / REFRESH:")
        self._append_log(f"- {paths.send_root}")
        self._append_log("- fresh freeze_feature_ai_send_pack_*.zip")
        self._append_log(f"- {paths.what_to_say}")
        self._append_log("- AI startup-readable freeze/compliance instructions generated from active project memory")

        self._append_log("")
        self._append_log("WILL NOT WRITE:")
        self._append_log("- project_freeze_ledger as project-specific memory")
        self._append_log("- other project roots")
        self._append_log("- temporary files in the project root")
        self._append_log("- frozen_features_memory entries, freeze_index.json, or project_frozen_implemented_steps.md")

        self._append_log("")
        self._append_log("No files have been changed yet.")
        self._append_log("Choose Do it to perform this action once, or Undo / Cancel to discard it.")

        self._set_pending_staged_action(project_root, "refresh_ai_compliance_package")

    def _do_staged_freeze_action(self) -> None:
        if self._pending_staged_project_root is None or self._pending_staged_action is None:
            QMessageBox.warning(self, "No staged action", "Prepare a staged action first.")
            return

        project_root = self._pending_staged_project_root
        action = self._pending_staged_action
        self._set_pending_staged_action(None, None)

        if action != "refresh_ai_compliance_package":
            QMessageBox.critical(self, "Unknown staged action", f"Unknown staged action: {action}")
            return

        self._append_log("")
        self._append_log("DO IT selected. Executing staged freeze / AI compliance action...")
        result = generate_freeze_after_update_ai_files(project_root)
        self._show_result(result)
        if result.ok:
            self._append_log("AI compliance package is ready for this project.")
            self._append_log("Use it in the next AI interaction, or continue with local freeze writing when that workflow is available in the tab.")

    def _undo_staged_freeze_action(self) -> None:
        if self._pending_staged_project_root is None:
            self._append_log("No staged action to cancel.")
            self.do_staged_action_button.setEnabled(False)
            self.undo_staged_action_button.setEnabled(False)
            return

        cancelled_root = self._pending_staged_project_root
        self._set_pending_staged_action(None, None)
        self.status_label.setText("Staged action cancelled. No files were changed.")
        self._append_log("")
        self._append_log("UNDO / CANCEL selected.")
        self._append_log(f"Cancelled staged action for: {cancelled_root}")
        self._append_log("No files were changed.")

    def _build_heuristic_local_freeze_inputs(self, project_root: Path) -> dict:
        """Build the local freeze form from project-local intake, then fallback.

        The normal local-freeze path is: patch ZIP carries root-level
        KANDA_FREEZE_HINT.json, the intake box saves that sidecar under the
        selected project's project_freeze_after_update/freeze_hint_intake, and
        the Freeze Feature After Update tab fills this form from that saved
        project-local JSON.

        If no current hint exists, return a safe starter draft. The starter is
        intentionally not writable until the human/AI supplies current feature
        validation evidence.
        """
        fallback_inputs = {
            "feature_title": "Current validated feature - replace with exact feature title",
            "primary_box": "Replace with the primary box for the current feature",
            "box_type": "Replace with the current box type",
            "validated_files": "",
            "generated_files": "",
            "protected_paths": "project_freeze_after_update/frozen_features_memory/",
            "do_not_regress_rules": "\n".join([
                "Do not freeze without current feature validation evidence.",
                "Preserve the current feature behavior validated by the user.",
                "Keep project-specific frozen memory under project_freeze_after_update/frozen_features_memory.",
                "Do not store project-specific frozen memory inside project_freeze_ledger.",
                "Do not replace current feature data with stale legacy workflow data.",
            ]),
            "validation_evidence_summary": "",
            "known_warnings": (
                "Starter draft only. Replace placeholders with the current validated feature data. "
                "No validation evidence has been inferred or invented."
            ),
            "planned_next_step": "Replace placeholders with current feature evidence, then Preview Freeze Entry before Confirm and Write.",
            "notes": (
                "Auto-filled by the Freeze Feature After Update tab as a safe current-feature starter. "
                "This draft intentionally avoids stale legacy freeze-workflow titles, paths, and validation markers."
            ),
        }
        try:
            return build_freeze_form_inputs_from_latest_hint(project_root, fallback_inputs)
        except Exception as exc:
            recovered = dict(fallback_inputs)
            recovered["known_warnings"] = (
                str(recovered.get("known_warnings", "")).strip()
                + " Freeze hint intake was unavailable, so the safe starter draft was kept. Error: "
                + str(exc)
            ).strip()
            return recovered

    def _open_local_freeze_entry_dialog(self) -> None:
        project_root = self._require_project_root()
        if project_root is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("New Local Freeze Entry")
        dialog.resize(980, 820)

        layout = QVBoxLayout(dialog)

        intro = QLabel(
            "Local freeze entry workflow: choose Heuristics or Local AI. Heuristics is the default "
            "because it is deterministic and validated. Local AI remains optional for testing and can "
            "improve the heuristic draft only when it passes quality gates. Preview is read-only; "
            "Confirm and Write still requires human confirmation."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        mode_group = QGroupBox("Auto-fill mode")
        mode_layout = QGridLayout(mode_group)
        mode_layout.setColumnStretch(3, 1)
        local_ai_radio = QRadioButton("Local AI")
        heuristic_radio = QRadioButton("Heuristics (default)")
        heuristic_radio.setChecked(True)
        local_ai_model_combo = QComboBox()
        local_ai_model_combo.setMinimumWidth(240)
        local_ai_model_combo.setToolTip("Select the local Ollama model used to fill this freeze form.")
        refresh_local_ai_models_button = QPushButton("Refresh AI Models")
        mode_status_label = QLabel("Heuristics selected by default. Local AI is optional and must pass quality gates before replacing the heuristic draft.")
        mode_status_label.setWordWrap(True)
        mode_layout.addWidget(local_ai_radio, 0, 0)
        mode_layout.addWidget(heuristic_radio, 0, 1)
        mode_layout.addWidget(QLabel("AI model:"), 0, 2)
        mode_layout.addWidget(local_ai_model_combo, 0, 3)
        mode_layout.addWidget(refresh_local_ai_models_button, 0, 4)
        mode_layout.addWidget(mode_status_label, 1, 0, 1, 5)
        layout.addWidget(mode_group, 0)

        form_group = QGroupBox("Freeze entry fields")
        form_layout = QGridLayout(form_group)
        form_layout.setColumnStretch(1, 1)

        feature_title_edit = QLineEdit()
        feature_title_edit.setPlaceholderText("Example: Local Freeze Writer Contract v1.1")
        primary_box_edit = QLineEdit()
        primary_box_edit.setPlaceholderText("Example: kanda_reasoner_app/freeze_after_update/contract.py")
        box_type_edit = QLineEdit("Module Box")

        validated_files_edit = QTextEdit()
        validated_files_edit.setPlaceholderText("One project-relative validated file per line")
        generated_files_edit = QTextEdit()
        generated_files_edit.setPlaceholderText("Optional: one generated file per line")
        protected_paths_edit = QTextEdit()
        protected_paths_edit.setPlaceholderText("One protected project-relative path per line")
        do_not_regress_edit = QTextEdit()
        do_not_regress_edit.setPlaceholderText("One do-not-regress rule per line")
        validation_evidence_edit = QTextEdit()
        validation_evidence_edit.setPlaceholderText(
            "Paste validation output. Must include a marker such as VALIDATION OK, INSTALL OK, py_compile passed, validator passed, or STATUS: IN_SYNC."
        )
        known_warnings_edit = QTextEdit()
        known_warnings_edit.setPlaceholderText("Optional warnings")
        planned_next_step_edit = QTextEdit()
        planned_next_step_edit.setPlaceholderText("Optional planned next step")
        notes_edit = QTextEdit()
        notes_edit.setPlaceholderText("Optional summary/notes")

        for editor in [
            validated_files_edit,
            generated_files_edit,
            protected_paths_edit,
            do_not_regress_edit,
            validation_evidence_edit,
            known_warnings_edit,
            planned_next_step_edit,
            notes_edit,
        ]:
            editor.setMaximumHeight(86)

        row = 0
        form_layout.addWidget(QLabel("Feature title:"), row, 0)
        form_layout.addWidget(feature_title_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Primary box:"), row, 0)
        form_layout.addWidget(primary_box_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Box type:"), row, 0)
        form_layout.addWidget(box_type_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Validated files:"), row, 0)
        form_layout.addWidget(validated_files_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Generated files:"), row, 0)
        form_layout.addWidget(generated_files_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Protected paths:"), row, 0)
        form_layout.addWidget(protected_paths_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Do-not-regress rules:"), row, 0)
        form_layout.addWidget(do_not_regress_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Validation evidence:"), row, 0)
        form_layout.addWidget(validation_evidence_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Known warnings:"), row, 0)
        form_layout.addWidget(known_warnings_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Planned next step:"), row, 0)
        form_layout.addWidget(planned_next_step_edit, row, 1)
        row += 1
        form_layout.addWidget(QLabel("Notes:"), row, 0)
        form_layout.addWidget(notes_edit, row, 1)

        layout.addWidget(form_group, 0)

        preview_group = QGroupBox("Preview and validation")
        preview_layout = QVBoxLayout(preview_group)
        preview_text_edit = QTextEdit()
        preview_text_edit.setReadOnly(True)
        preview_text_edit.setPlaceholderText("Click Preview Freeze Entry to generate a read-only local freeze preview.")
        preview_layout.addWidget(preview_text_edit, 1)
        layout.addWidget(preview_group, 1)

        button_row = QHBoxLayout()
        autofill_button = QPushButton("Fill Form Now")
        copy_to_ai_button = QPushButton("Copy Formulary to AI")
        receive_from_ai_button = QPushButton("Receive Formulary from AI")
        preview_button = QPushButton("Preview Freeze Entry")
        confirm_write_button = QPushButton("Confirm and Write Freeze Entry")
        cancel_button = QPushButton("Cancel")
        confirm_write_button.setEnabled(False)
        copy_to_ai_button.setToolTip("Copy a strict review prompt with the current auto-filled freeze form for an AI specialist")
        receive_from_ai_button.setToolTip("Paste the strict AI JSON answer and apply it back into this form")
        autofill_button.setToolTip("Fill using the selected mode: Heuristics by default, or optional Local AI.")
        button_row.addWidget(autofill_button)
        button_row.addWidget(copy_to_ai_button)
        button_row.addWidget(receive_from_ai_button)
        button_row.addWidget(preview_button)
        button_row.addWidget(confirm_write_button)
        button_row.addStretch(1)
        button_row.addWidget(cancel_button)
        layout.addLayout(button_row)

        self._local_freeze_preview = None

        def collect_inputs() -> dict:
            return {
                "feature_title": feature_title_edit.text().strip(),
                "primary_box": primary_box_edit.text().strip(),
                "box_type": box_type_edit.text().strip() or "Module Box",
                "validated_files": validated_files_edit.toPlainText(),
                "generated_files": generated_files_edit.toPlainText(),
                "protected_paths": protected_paths_edit.toPlainText(),
                "do_not_regress_rules": do_not_regress_edit.toPlainText(),
                "validation_evidence_summary": validation_evidence_edit.toPlainText(),
                "known_warnings": known_warnings_edit.toPlainText().strip(),
                "planned_next_step": planned_next_step_edit.toPlainText().strip(),
                "notes": notes_edit.toPlainText().strip(),
            }

        def apply_inputs(inputs: dict) -> None:
            feature_title_edit.setText(str(inputs.get("feature_title", "")))
            primary_box_edit.setText(str(inputs.get("primary_box", "")))
            box_type_edit.setText(str(inputs.get("box_type", "Module Box") or "Module Box"))
            validated_files_edit.setPlainText(str(inputs.get("validated_files", "")))
            generated_files_edit.setPlainText(str(inputs.get("generated_files", "")))
            protected_paths_edit.setPlainText(str(inputs.get("protected_paths", "")))
            do_not_regress_edit.setPlainText(str(inputs.get("do_not_regress_rules", "")))
            validation_evidence_edit.setPlainText(str(inputs.get("validation_evidence_summary", "")))
            known_warnings_edit.setPlainText(str(inputs.get("known_warnings", "")))
            planned_next_step_edit.setPlainText(str(inputs.get("planned_next_step", "")))
            notes_edit.setPlainText(str(inputs.get("notes", "")))

        def selected_local_ai_model_name() -> str:
            return _model_name_from_local_ai_combo_text(str(local_ai_model_combo.currentText() or ""))

        def set_ai_fill_busy(is_busy: bool) -> None:
            autofill_button.setEnabled(not is_busy)
            preview_button.setEnabled(not is_busy)
            copy_to_ai_button.setEnabled(not is_busy)
            receive_from_ai_button.setEnabled(not is_busy)
            refresh_local_ai_models_button.setEnabled(not is_busy)
            local_ai_radio.setEnabled(not is_busy)
            heuristic_radio.setEnabled(not is_busy)
            local_ai_model_combo.setEnabled(not is_busy)
            if is_busy:
                confirm_write_button.setEnabled(False)

        def populate_local_ai_model_combo() -> list[str]:
            previous = selected_local_ai_model_name()
            local_ai_model_combo.blockSignals(True)
            try:
                local_ai_model_combo.clear()
                local_ai_model_combo.addItem(AUTO_LOCAL_AI_MODEL_LABEL)
                try:
                    models = _list_local_ai_models()
                except Exception as exc:
                    models = []
                    mode_status_label.setText("Local AI model refresh failed; Heuristics remains available. Error: " + str(exc))
                for model_name in models:
                    local_ai_model_combo.addItem(model_name)
                if previous:
                    index = local_ai_model_combo.findText(previous)
                    if index >= 0:
                        local_ai_model_combo.setCurrentIndex(index)
                if models:
                    mode_status_label.setText("Local AI ready: " + str(len(models)) + " model(s) found. Default fill mode is Local AI.")
                else:
                    mode_status_label.setText("No local AI model found yet. Local AI mode will fall back to Heuristics.")
                return models
            finally:
                local_ai_model_combo.blockSignals(False)

        def fill_with_heuristics_only(reason: str = "") -> None:
            confirm_write_button.setEnabled(False)
            self._local_freeze_preview = None
            apply_inputs(self._build_heuristic_local_freeze_inputs(project_root))
            if reason:
                self._append_log(reason)
            self._append_log("Local freeze entry fields filled from project-local freeze hint intake when available; otherwise a safe starter was used. No files were written.")
            preview_local_freeze()

        def handle_local_ai_fill_result(response_text: str, model_name: str) -> None:
            set_ai_fill_busy(False)
            heuristic_inputs = self._build_heuristic_local_freeze_inputs(project_root)
            if _local_ai_response_looks_like_prompt_echo(response_text):
                self._append_log("Local AI output rejected by quality gates: prompt echo detected. Heuristic draft kept.")
                mode_status_label.setText("Local AI echoed the prompt; heuristic draft kept.")
                QMessageBox.warning(
                    dialog,
                    "Local AI fill rejected",
                    "Local AI echoed the prompt/instructions instead of returning a clean form. The heuristic draft was kept and previewed."
                )
                return
            try:
                updated_inputs = parse_ai_formulary_response(response_text)
            except Exception as exc:
                self._append_log("Local AI returned an answer that could not be parsed. Keeping heuristic draft.")
                self._append_log("Local AI parse error: " + str(exc))
                mode_status_label.setText("Local AI answer could not be parsed; heuristic draft kept.")
                QMessageBox.warning(
                    dialog,
                    "Local AI fill fallback",
                    "Local AI ran, but its answer could not be parsed. The heuristic draft was kept and previewed."
                )
                return
            ok_to_apply, quality_reasons = _validate_local_ai_form_against_heuristic(updated_inputs, heuristic_inputs)
            if not ok_to_apply:
                self._append_log("Local AI output rejected by quality gates. Heuristic draft kept.")
                for reason in quality_reasons:
                    self._append_log("- " + reason)
                mode_status_label.setText("Local AI degraded the heuristic baseline; heuristic draft kept.")
                QMessageBox.warning(
                    dialog,
                    "Local AI fill rejected",
                    "Local AI returned a parseable form, but it weakened the heuristic baseline. The heuristic draft was kept.\n\n"
                    + "\n".join("- " + reason for reason in quality_reasons[:8])
                )
                return
            confirm_write_button.setEnabled(False)
            self._local_freeze_preview = None
            apply_inputs(updated_inputs)
            self._append_log("Local AI filled the freeze formulary using model: " + str(model_name) + ". Quality gates passed. No files were written.")
            mode_status_label.setText("Local AI fill applied with model: " + str(model_name) + " after quality gates.")
            preview_local_freeze()

        def handle_local_ai_fill_error(error_message: str) -> None:
            set_ai_fill_busy(False)
            mode_status_label.setText("Local AI unavailable; heuristic draft was kept.")
            self._append_log("Local AI fill unavailable. Falling back to heuristics. Error: " + str(error_message))
            # The heuristic draft is already present and previewed before the local AI request.

        def stop_local_ai_polling() -> None:
            self._local_freeze_ai_request_id = None
            if self._local_freeze_ai_poll_timer is not None:
                self._local_freeze_ai_poll_timer.stop()
                self._local_freeze_ai_poll_timer.deleteLater()
                self._local_freeze_ai_poll_timer = None
            self._local_freeze_ai_result_queue = None

        def poll_local_ai_fill_queue() -> None:
            request_id = self._local_freeze_ai_request_id
            result_queue = self._local_freeze_ai_result_queue
            if request_id is None or result_queue is None:
                return
            try:
                returned_request_id, ok, payload, model_name = result_queue.get_nowait()
            except queue.Empty:
                return
            stop_local_ai_polling()
            self._local_freeze_ai_thread = None
            if returned_request_id is not request_id:
                return
            if not dialog.isVisible():
                return
            if ok:
                handle_local_ai_fill_result(str(payload), str(model_name))
            else:
                handle_local_ai_fill_error(str(payload))

        def fill_with_local_ai() -> None:
            fill_with_heuristics_only("Local AI mode starts from the deterministic heuristic draft, then asks the selected local model to improve it.")
            selected_model = selected_local_ai_model_name()
            if local_ai_model_combo.count() <= 1 and not selected_model:
                mode_status_label.setText("No local AI model found; heuristic draft kept.")
                self._append_log("Local AI mode selected, but no model was found. Heuristic draft kept.")
                return
            stop_local_ai_polling()
            set_ai_fill_busy(True)
            request_id = object()
            result_queue: queue.Queue = queue.Queue(maxsize=1)
            self._local_freeze_ai_request_id = request_id
            self._local_freeze_ai_result_queue = result_queue
            mode_status_label.setText("Local AI is filling the freeze form. The form remains usable after the result returns.")
            self._append_log("Local AI formulary fill requested through a shutdown-safe Python daemon thread. No files will be written.")

            runner = LocalFreezeAIFormularyRunner(
                inputs=collect_inputs(),
                project_root=project_root,
                model_name=selected_model,
            )

            def run_local_ai_request() -> None:
                ok, payload, model_name = runner.run()
                try:
                    result_queue.put_nowait((request_id, ok, payload, model_name))
                except Exception:
                    pass

            self._local_freeze_ai_thread = threading.Thread(
                target=run_local_ai_request,
                name="kanda-local-freeze-ai-fill",
                daemon=True,
            )
            self._local_freeze_ai_thread.start()

            self._local_freeze_ai_poll_timer = QTimer(dialog)
            self._local_freeze_ai_poll_timer.setInterval(200)
            self._local_freeze_ai_poll_timer.timeout.connect(poll_local_ai_fill_queue)
            dialog.destroyed.connect(stop_local_ai_polling)
            self._local_freeze_ai_poll_timer.start()

        def auto_fill_local_freeze() -> None:
            if local_ai_radio.isChecked():
                fill_with_local_ai()
            else:
                fill_with_heuristics_only()

        def render_findings(result: dict) -> str:
            lines = []
            errors = result.get("errors") or []
            warnings = result.get("warnings") or []
            if errors:
                lines.append("ERRORS:")
                lines.extend(f"- {item}" for item in errors)
                lines.append("")
            if warnings:
                lines.append("WARNINGS:")
                lines.extend(f"- {item}" for item in warnings)
                lines.append("")
            return "\n".join(lines)

        def preview_local_freeze() -> None:
            self._local_freeze_preview = None
            confirm_write_button.setEnabled(False)
            inputs = collect_inputs()
            result = preview_freeze_entry(project_root, inputs)
            self._local_freeze_preview = result if result.get("ok") else None
            markdown = result.get("markdown") or ""
            preview_text_edit.setPlainText(render_findings(result) + markdown)
            validation_result = None

            if result.get("ok") and result.get("is_writable"):
                validation_result = validate_freeze_entry_preview(project_root, result)
                if validation_result.get("ok"):
                    self._local_freeze_preview = result
                    confirm_write_button.setEnabled(True)
                    self.status_label.setText("Local freeze preview ready. Review it, then confirm if correct.")
                    self._append_log("Local freeze entry preview is ready and writable. No files were written.")
                else:
                    preview_text_edit.setPlainText(render_findings(validation_result) + markdown)
                    self._append_log("Local freeze preview was generated but validation blocked writing.")
            else:
                self._append_log("Local freeze preview is not writable. Fix the required fields or validation evidence.")

            self._append_log_block(build_local_freeze_preview_log_text(result, validation_result))

        def build_ai_review_prompt() -> str:
            current_inputs = collect_inputs()
            current_json = json.dumps(current_inputs, ensure_ascii=False, indent=2)
            return (
                "You are a specialist in KANDA Reasoner, Box Architecture, local-first freeze memory, "
                "AI-assisted programming workflows, human-confirmed freeze entries, and safe project-memory governance.\n\n"
                "Context:\n"
                "I just implemented and validated a feature. I am about to freeze it using the KANDA Reasoner "
                "Freeze Feature After Update tab. The form below was auto-filled heuristically by KANDA Reasoner.\n\n"
                "Task:\n"
                "Review and correct the freeze form for the current validated feature only. Improve clarity, protected paths, "
                "do-not-regress rules, validation summary, warnings, and notes. If the current form contains placeholders "
                "or stale legacy data from another feature, replace it using only evidence already present in this chat. "
                "Do not invent validation that is not present. Do not ask me to upload files. Do not write a patch. "
                "Do not include explanations outside the required return format.\n\n"
                "Critical rules:\n"
                "- Keep project-specific frozen memory under project_freeze_after_update/frozen_features_memory.\n"
                "- Do not store project-specific frozen memory inside project_freeze_ledger.\n"
                "- Preserve the local freeze workflow: preview is read-only; Confirm and Write requires human confirmation.\n"
                "- Preserve AI startup compliance: after local freeze write, the startup freeze context must be refreshed.\n"
                "- External AI review remains advanced/fallback, not the normal freeze path.\n\n"
                "Return format - strict copy/paste contract for KANDA Reasoner:\n"
                "Your entire answer must be exactly the receive-ready block.\n"
                "The first visible characters of your answer must be KANDA_FREEZE_FORM_JSON_BEGIN.\n"
                "The last visible characters of your answer must be KANDA_FREEZE_FORM_JSON_END.\n"
                "Do not use markdown. Do not use code fences. Do not use bullets. Do not add comments.\n"
                "Do not write explanations before or after the block.\n"
                "Between the markers, return one valid JSON object only.\n"
                "Use double quotes for every key and string value.\n"
                "Do not use trailing commas.\n"
                "For multiline text fields, keep each field as one JSON string and escape line breaks as \\n.\n"
                "Do not place real unescaped line breaks inside string values.\n"
                "Do not change the marker names.\n\n"
                "Copy/paste-ready answer shape:\n"
                "KANDA_FREEZE_FORM_JSON_BEGIN\n"
                "{\n"
                "  \"feature_title\": \"...\",\n"
                "  \"primary_box\": \"...\",\n"
                "  \"box_type\": \"...\",\n"
                "  \"validated_files\": \"one project-relative path per line, encoded with \\\\n between lines\",\n"
                "  \"generated_files\": \"one project-relative path per line, encoded with \\\\n between lines\",\n"
                "  \"protected_paths\": \"one project-relative path per line, encoded with \\\\n between lines\",\n"
                "  \"do_not_regress_rules\": \"one rule per line, encoded with \\\\n between lines\",\n"
                "  \"validation_evidence_summary\": \"validation evidence only; do not invent validation; encode line breaks with \\\\n\",\n"
                "  \"known_warnings\": \"...\",\n"
                "  \"planned_next_step\": \"...\",\n"
                "  \"notes\": \"...\"\n"
                "}\n"
                "KANDA_FREEZE_FORM_JSON_END\n\n"
                "Current form JSON to review and correct for the current feature only:\n"
                "If a field is a placeholder or belongs to an older unrelated freeze workflow, replace it from the current chat evidence.\n"
                f"{current_json}\n"
            )

        def copy_formulary_to_ai() -> None:
            QApplication.clipboard().setText(build_ai_review_prompt())
            self._append_log("Copied AI specialist review prompt for the current local freeze formulary. No files were written.")
            QMessageBox.information(
                dialog,
                "Copied formulary prompt",
                "The strict AI review prompt was copied to the clipboard. Paste it into AI. Its answer should start with KANDA_FREEZE_FORM_JSON_BEGIN and end with KANDA_FREEZE_FORM_JSON_END, with no markdown or explanation. Then paste that exact answer into Receive Formulary from AI.",
            )

        def parse_ai_formulary_response(text: str) -> dict:
            """Parse AI formulary answers with a forgiving multi-candidate extractor.

            Receive Formulary from AI must accept the real world: some AIs add prose,
            markdown fences, template examples, damaged markers, or raw newlines inside
            JSON strings. This parser extracts every JSON-like object it can find,
            repairs common formatting damage, and selects the best freeze-form object.
            """

            start = "KANDA_FREEZE_FORM_JSON_BEGIN"
            end = "KANDA_FREEZE_FORM_JSON_END"
            allowed = {
                "feature_title",
                "primary_box",
                "box_type",
                "validated_files",
                "generated_files",
                "protected_paths",
                "do_not_regress_rules",
                "validation_evidence_summary",
                "known_warnings",
                "planned_next_step",
                "notes",
            }

            def normalize_ai_text(raw_text: str) -> str:
                return (
                    (raw_text or "")
                    .replace("\ufeff", "")
                    .replace("\u200b", "")
                    .replace("\u200c", "")
                    .replace("\u200d", "")
                    .replace("\u00a0", " ")
                    .strip()
                )

            def strip_markdown_fences(raw_text: str) -> str:
                stripped = normalize_ai_text(raw_text)
                if not stripped.startswith("```"):
                    return stripped
                lines = stripped.splitlines()
                if lines and lines[0].strip().startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                return "\n".join(lines).strip()

            def remove_trailing_commas(raw_text: str) -> str:
                text_work = raw_text
                previous = None
                while previous != text_work:
                    previous = text_work
                    text_work = text_work.replace(",\n}", "\n}").replace(",\r\n}", "\r\n}")
                    text_work = text_work.replace(", }", " }").replace(",}", "}")
                    text_work = text_work.replace(",\n]", "\n]").replace(",\r\n]", "\r\n]")
                    text_work = text_work.replace(", ]", " ]").replace(",]", "]")
                return text_work

            def escape_raw_control_chars_inside_strings(raw_text: str) -> str:
                """Repair real newlines/tabs pasted inside JSON string values."""

                repaired: list[str] = []
                in_string = False
                escaped = False
                for char in raw_text:
                    if in_string:
                        if escaped:
                            repaired.append(char)
                            escaped = False
                            continue
                        if char == "\\":
                            repaired.append(char)
                            escaped = True
                            continue
                        if char == '"':
                            repaired.append(char)
                            in_string = False
                            continue
                        if char == "\n":
                            repaired.append("\\n")
                            continue
                        if char == "\r":
                            continue
                        if char == "\t":
                            repaired.append("\\t")
                            continue
                        repaired.append(char)
                        continue

                    repaired.append(char)
                    if char == '"':
                        in_string = True

                return "".join(repaired)

            def normalize_common_ai_markdown_damage(value: str) -> str:
                # Some AIs convert __init__.py to **init**.py when not using a code block.
                return value.replace("**init**.py", "__init__.py")

            def extract_balanced_json_objects(raw_text: str) -> list[str]:
                """Return every balanced JSON object from arbitrary pasted AI text."""

                candidate = normalize_ai_text(raw_text)
                objects: list[str] = []
                length = len(candidate)
                index = 0
                while index < length:
                    if candidate[index] != "{":
                        index += 1
                        continue

                    in_string = False
                    escaped = False
                    depth = 0
                    end_index: int | None = None
                    cursor = index
                    while cursor < length:
                        char = candidate[cursor]
                        if in_string:
                            if escaped:
                                escaped = False
                            elif char == "\\":
                                escaped = True
                            elif char == '"':
                                in_string = False
                            cursor += 1
                            continue

                        if char == '"':
                            in_string = True
                        elif char == "{":
                            depth += 1
                        elif char == "}":
                            depth -= 1
                            if depth == 0:
                                end_index = cursor + 1
                                break
                        cursor += 1

                    if end_index is not None:
                        objects.append(candidate[index:end_index].strip())
                        index = end_index
                    else:
                        index += 1
                return objects

            def collect_candidate_blocks(raw_text: str) -> list[str]:
                """Collect marker payloads, fenced JSON, full objects, and form-object fallbacks."""

                normalized = normalize_ai_text(raw_text)
                blocks: list[str] = []

                if start in normalized and end in normalized:
                    marker_payload = normalized.split(start, 1)[1].split(end, 1)[0].strip()
                    blocks.append(marker_payload)

                # Also tolerate damaged or missing markers by scanning the whole paste.
                for fence_part in normalized.split("```"):
                    block = strip_markdown_fences(fence_part)
                    if block.lower().startswith("json"):
                        block = block[4:].strip()
                    if "{" in block and "}" in block:
                        blocks.append(block)

                blocks.extend(extract_balanced_json_objects(normalized))

                # If the user accidentally pasted the whole AI prompt, choose the object
                # around the last visible freeze-form key rather than the template example.
                for key in ['"feature_title"', "'feature_title'"]:
                    key_index = normalized.rfind(key)
                    if key_index >= 0:
                        left = normalized.rfind("{", 0, key_index)
                        right = normalized.find("}", key_index)
                        if left >= 0 and right > left:
                            blocks.append(normalized[left : right + 1])

                # Last-resort broad slice from first { to last }, useful when markers are
                # damaged but the paste contains one object surrounded by prose.
                first_brace = normalized.find("{")
                last_brace = normalized.rfind("}")
                if first_brace >= 0 and last_brace > first_brace:
                    blocks.append(normalized[first_brace : last_brace + 1])

                unique: list[str] = []
                seen: set[str] = set()
                for block in blocks:
                    cleaned_block = strip_markdown_fences(block).strip()
                    if not cleaned_block or cleaned_block in seen:
                        continue
                    seen.add(cleaned_block)
                    unique.append(cleaned_block)
                return unique

            def json_load_attempts(raw_block: str) -> dict | None:
                """Try strict and repaired JSON parsing for one candidate block."""

                variants: list[str] = []
                base = strip_markdown_fences(raw_block)
                variants.append(base)
                variants.append(remove_trailing_commas(base))
                variants.append(remove_trailing_commas(escape_raw_control_chars_inside_strings(base)))

                # If the candidate is a large text slice, try all balanced objects inside it too.
                for obj in extract_balanced_json_objects(base):
                    variants.append(obj)
                    variants.append(remove_trailing_commas(obj))
                    variants.append(remove_trailing_commas(escape_raw_control_chars_inside_strings(obj)))

                attempted: set[str] = set()
                for variant in variants:
                    candidate = variant.strip()
                    if not candidate or candidate in attempted:
                        continue
                    attempted.add(candidate)
                    try:
                        payload = json.loads(candidate)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(payload, dict):
                        return payload
                return None

            def payload_score(payload: dict) -> tuple[int, int, int]:
                present_keys = sum(1 for key in allowed if key in payload)
                meaningful_chars = 0
                placeholder_penalty = 0
                for key in allowed:
                    value = payload.get(key)
                    if value is None:
                        continue
                    text_value = str(value)
                    meaningful_chars += len(text_value.strip())
                    if "..." in text_value or "one project-relative path" in text_value:
                        placeholder_penalty += 1
                return (present_keys, meaningful_chars, -placeholder_penalty)

            parsed_payloads: list[dict] = []
            for block in collect_candidate_blocks(text):
                payload = json_load_attempts(block)
                if payload is not None:
                    parsed_payloads.append(payload)

            if not parsed_payloads:
                raise ValueError(
                    "Could not find a usable freeze-form JSON object in the AI answer. "
                    "The receiver searched marker payloads, fenced JSON, balanced JSON objects, and broad fallback slices."
                )

            payload = max(parsed_payloads, key=payload_score)
            if not isinstance(payload, dict):
                raise ValueError("AI response JSON must be an object.")

            cleaned = collect_inputs()
            ignored = sorted(str(key) for key in payload.keys() if key not in allowed)
            for key in allowed:
                if key not in payload:
                    continue
                value = payload[key]
                if isinstance(value, list):
                    cleaned[key] = "\n".join(
                        normalize_common_ai_markdown_damage(str(item).strip())
                        for item in value
                        if str(item).strip()
                    )
                elif isinstance(value, dict):
                    cleaned[key] = json.dumps(value, ensure_ascii=False, indent=2)
                elif value is None:
                    cleaned[key] = ""
                else:
                    cleaned[key] = normalize_common_ai_markdown_damage(str(value))
            if ignored:
                self._append_log("Ignored unknown AI formulary field(s): " + ", ".join(ignored))
            return cleaned

        def receive_formulary_from_ai() -> None:
            receive_dialog = QDialog(dialog)
            receive_dialog.setWindowTitle("Receive Formulary from AI")
            receive_dialog.resize(820, 620)
            receive_layout = QVBoxLayout(receive_dialog)
            receive_help = QLabel(
                "Paste the AI answer here. It must contain JSON between "
                "KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END. "
                "Applying it updates this form and regenerates a read-only preview; it does not write files."
            )
            receive_help.setWordWrap(True)
            receive_layout.addWidget(receive_help)
            response_edit = QTextEdit()
            response_edit.setPlaceholderText(
                "Paste AI response here, including KANDA_FREEZE_FORM_JSON_BEGIN / END markers."
            )
            receive_layout.addWidget(response_edit, 1)
            receive_button_row = QHBoxLayout()
            apply_button = QPushButton("Apply AI Formulary to Form")
            close_receive_button = QPushButton("Cancel")
            receive_button_row.addStretch(1)
            receive_button_row.addWidget(apply_button)
            receive_button_row.addWidget(close_receive_button)
            receive_layout.addLayout(receive_button_row)

            def apply_ai_formulary() -> None:
                try:
                    updated_inputs = parse_ai_formulary_response(response_edit.toPlainText())
                except Exception as exc:
                    QMessageBox.critical(
                        receive_dialog,
                        "Could not parse AI formulary",
                        "The AI answer could not be parsed even after the tolerant extractor tried to select and repair the JSON block. "
                        "Ask AI to do it again. Tell AI to return exactly one valid JSON object between "
                        "KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END, with no markdown, no prose, and no extra text. "
                        "You can also paste the JSON object only.\n\n"
                        f"Error: {exc}",
                    )
                    return
                confirm_write_button.setEnabled(False)
                self._local_freeze_preview = None
                apply_inputs(updated_inputs)
                self._append_log("Received AI formulary and applied it to the local freeze form. No files were written.")
                preview_local_freeze()
                receive_dialog.close()

            apply_button.clicked.connect(apply_ai_formulary)
            close_receive_button.clicked.connect(receive_dialog.close)
            receive_dialog.show()
            receive_dialog.raise_()
            receive_dialog.activateWindow()

        def confirm_and_write_local_freeze() -> None:
            preview = self._local_freeze_preview
            if not preview:
                QMessageBox.warning(self, "Preview missing", "Generate a valid preview first.")
                return

            targets = preview.get("write_targets") or []
            target_text = "\n".join(f"- {path}" for path in targets)
            reply = QMessageBox.question(
                self,
                "Confirm local freeze write",
                "You are about to write a local freeze entry for this active project.\n\n"
                "WILL WRITE:\n"
                f"{target_text}\n\n"
                "WILL NOT WRITE:\n"
                "- project_freeze_ledger as project-specific memory\n"
                "- other project roots\n"
                "- temporary files in the project root\n\n"
                "Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                self._append_log("Local freeze write cancelled by human confirmation gate.")
                return

            result = write_confirmed_freeze_entry(project_root, preview, confirmation=True)
            if not result.get("ok"):
                errors = "\n".join(result.get("errors") or ["Unknown error"])
                QMessageBox.critical(self, "Local freeze write failed", errors)
                self._append_log("LOCAL FREEZE WRITE FAILED")
                self._append_log(errors)
                return

            self.status_label.setText("Local freeze entry written successfully.")
            self._append_log("LOCAL FREEZE WRITE OK")
            self._append_log(f"Freeze ID: {result.get('freeze_id')}")
            self._append_log("Written paths:")
            for path in result.get("written_paths") or []:
                self._append_log(f"- {path}")

            intake_used = mark_latest_freeze_hint_used(project_root, freeze_id=str(result.get("freeze_id") or ""))
            if intake_used.get("ok"):
                self._append_log("Freeze hint intake record marked as used for this freeze.")
            elif intake_used.get("warnings"):
                self._append_log("Freeze hint intake was not marked used:")
                for warning in intake_used.get("warnings") or []:
                    self._append_log(f"- {warning}")
            elif intake_used.get("errors"):
                self._append_log("Freeze hint intake mark-used warning:")
                for error in intake_used.get("errors") or []:
                    self._append_log(f"- {error}")

            compliance = refresh_ai_compliance_context(project_root)
            self._append_log("")
            self._append_log("AI COMPLIANCE REFRESH AFTER LOCAL WRITE")
            if compliance.get("ai_send_refreshed"):
                self._append_log("AI-send exposure refreshed for current freeze memory.")
                if compliance.get("ai_send_zip"):
                    self._append_log(f"- AI-send ZIP: {compliance.get('ai_send_zip')}")
                if compliance.get("ai_send_instruction"):
                    self._append_log(f"- AI-send instruction: {compliance.get('ai_send_instruction')}")
            else:
                self._append_log("AI-send exposure refresh failed or was unavailable.")

            if compliance.get("startup_context_refreshed"):
                self._append_log("Startup freeze context refreshed for next AI programming session.")
                self._append_log(f"- Startup ZIP: {compliance.get('startup_zip')}")
                self._append_log(f"- Paste-after file: {compliance.get('paste_after_uploading')}")
                self._append_log(f"- Context file inside startup ZIP: {compliance.get('generated_context_filename')}")
            else:
                self._append_log("Startup freeze context refresh failed or was unavailable.")

            if compliance.get("errors"):
                self._append_log("AI compliance refresh errors:")
                for error in compliance.get("errors") or []:
                    self._append_log(f"- {error}")

            if compliance.get("report"):
                self._append_log("")
                self._append_log("Current freeze exposure after write:")
                self._append_log(str(compliance.get("report")))

            if not compliance.get("ok"):
                QMessageBox.warning(
                    self,
                    "Local freeze written; AI compliance refresh warning",
                    "The local freeze entry was written, but the AI-visible startup context refresh reported a warning or error. Check the log.",
                )
            else:
                QMessageBox.information(
                    self,
                    "Local freeze written",
                    "Freeze entry written successfully and AI startup freeze context was refreshed.",
                )
            dialog.close()

        refresh_local_ai_models_button.clicked.connect(populate_local_ai_model_combo)
        local_ai_radio.toggled.connect(lambda checked: mode_status_label.setText("Local AI selected. The form will use the selected local model only if it passes quality gates; otherwise heuristic draft is kept." if checked else "Heuristics selected. The form will use deterministic local rules only."))
        autofill_button.clicked.connect(auto_fill_local_freeze)
        copy_to_ai_button.clicked.connect(copy_formulary_to_ai)
        receive_from_ai_button.clicked.connect(receive_formulary_from_ai)
        preview_button.clicked.connect(preview_local_freeze)
        confirm_write_button.clicked.connect(confirm_and_write_local_freeze)
        cancel_button.clicked.connect(dialog.close)
        dialog.finished.connect(lambda _result=0: stop_local_ai_polling())

        self._local_freeze_dialog = dialog
        populate_local_ai_model_combo()
        auto_fill_local_freeze()
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def _open_path(self, path: Path | None, label: str) -> None:
        if path is None:
            QMessageBox.warning(self, "Path missing", f"No {label} path is available yet.")
            return
        if not path.exists():
            QMessageBox.warning(self, "Path missing", f"The {label} path does not exist:\n{path}")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def _open_box_folder(self) -> None:
        paths = self._paths()
        self._open_path(paths.box_root if paths is not None else None, "box folder")

    def _send_root_path(self) -> Path | None:
        paths = self._paths()
        output_path = self._last_output_folder
        if output_path is None and paths is not None:
            output_path = paths.send_root
        return output_path

    def _what_to_say_path(self) -> Path | None:
        paths = self._paths()
        if paths is None:
            return None
        return paths.what_to_say

    def _open_output_folder(self) -> None:
        self._open_path(self._send_root_path(), "External AI review folder")

    def _copy_output_folder_path(self) -> None:
        output_path = self._send_root_path()
        if output_path is None:
            QMessageBox.warning(self, "Path missing", "No external AI review folder path is available yet.")
            return
        QApplication.clipboard().setText(str(output_path))
        self.files_to_send_path_edit.setText(str(output_path))
        self._append_log(f"Copied external AI review folder path: {output_path}")

    def _show_what_to_say_window(self) -> None:
        what_to_say_path = self._what_to_say_path()
        if what_to_say_path is None:
            QMessageBox.warning(self, "Project missing", "Select a project folder first.")
            return
        if not what_to_say_path.exists():
            QMessageBox.warning(
                self,
                "Instruction file missing",
                "The instruction file does not exist yet.\n\n"
                "Export for External AI Review first, then open this window.\n\n"
                f"Expected path:\n{what_to_say_path}",
            )
            return

        try:
            text = what_to_say_path.read_text(encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(self, "Could not read instruction file", str(exc))
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("what_to_say_to_ai_freeze_feature.md")
        dialog.resize(900, 700)

        layout = QVBoxLayout(dialog)

        warning = QLabel(
            'Warning: file "what_to_say_to_ai_freeze_feature.md" should not be edited manually here or anywhere else.'
        )
        warning.setWordWrap(True)
        warning_font = QFont()
        warning_font.setBold(True)
        warning.setFont(warning_font)
        layout.addWidget(warning)

        path_label = QLabel(str(what_to_say_path))
        path_label.setWordWrap(True)
        layout.addWidget(path_label)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(text)
        layout.addWidget(text_edit, 1)

        button_row = QHBoxLayout()
        copy_button = QPushButton("Copy Complete Text")
        close_button = QPushButton("Close")
        button_row.addStretch(1)
        button_row.addWidget(copy_button)
        button_row.addWidget(close_button)
        layout.addLayout(button_row)

        def copy_complete_text() -> None:
            QApplication.clipboard().setText(text_edit.toPlainText())
            self._append_log("Copied complete what_to_say_to_ai_freeze_feature.md text.")

        copy_button.clicked.connect(copy_complete_text)
        close_button.clicked.connect(dialog.close)

        self._what_to_say_dialog = dialog
        self._what_to_say_text_edit = text_edit
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def _render_help_html(self) -> str:
        """Return the rich practical help shown by the Help button."""
        return r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
body {
    font-family: "Segoe UI", "Aptos", "Calibri", sans-serif;
    font-size: 14px;
    line-height: 1.55;
    color: #243043;
    background: #fffaf2;
    margin: 0;
    padding: 0;
}
.page {
    padding: 18px 22px 26px 22px;
}
h1 {
    color: #16213e;
    font-size: 26px;
    margin: 0 0 8px 0;
}
h2 {
    color: #0f766e;
    font-size: 20px;
    margin-top: 26px;
    border-bottom: 2px solid #99f6e4;
    padding-bottom: 4px;
}
h3 {
    color: #7c3aed;
    font-size: 16px;
    margin-top: 18px;
}
.hero {
    background: #fff3c4;
    border: 1px solid #facc15;
    border-radius: 12px;
    padding: 12px 14px;
    margin: 10px 0 18px 0;
}
.card {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-left: 6px solid #3b82f6;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 12px 0;
}
.good {
    border-left-color: #10b981;
}
.warn {
    border-left-color: #f59e0b;
    background: #fffbeb;
}
.danger {
    border-left-color: #ef4444;
    background: #fff1f2;
}
.step {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 8px 10px;
    margin: 8px 0;
}
code {
    background: #e0f2fe;
    color: #075985;
    border-radius: 5px;
    padding: 2px 5px;
    font-family: "Cascadia Mono", "Consolas", monospace;
}
ul { margin-top: 6px; }
strong { color: #111827; }
.small { color: #64748b; font-size: 13px; }
</style>
</head>
<body>
<div class="page">
<h1>Freeze Feature After Update — Practical Help</h1>
<div class="hero">
<strong>Start here:</strong> after changing a project and validating the change, use this tab to freeze locally first. External AI review export is available as an advanced fallback.
</div>

<h2>1. Create / Repair Box</h2>
<div class="card good">
<p><strong>Use this first when a project does not have its freeze folder yet, or when some required files are missing.</strong></p>
<p>This button creates or repairs:</p>
<ul>
<li><code>&lt;project&gt;\project_freeze_after_update\</code></li>
<li><code>frozen_features_memory\</code> — the project-specific long-term freeze memory</li>
<li><code>files_to_send_ai\</code> — optional external AI review/export artifacts, not the local source of truth</li>
</ul>
<p>It is safe because it creates missing structure without overwriting accepted freeze memory.</p>
</div>

<h2>2. In plain English: what is Freeze Feature After Update?</h2>
<div class="card">
<p><strong>Freeze Feature After Update</strong> is the project safety memory system.</p>
<p>When you finish a feature, validate it, and decide it should not be accidentally broken later, this tab now supports auto-filled local freeze writing with human confirmation. The optional external AI review export can still generate a small AI-send package when you want a second AI to review or help.</p>
<p>Think of it like a project passport: every validated feature receives a stamp, and future work must check the passport before touching protected behavior.</p>
</div>

<h2>3. Why is this important?</h2>
<div class="card good">
<ul>
<li><strong>Prevents regressions:</strong> future patches can see what is already validated.</li>
<li><strong>Keeps memory local:</strong> each project owns its own freeze history.</li>
<li><strong>Avoids contamination:</strong> KANDA Reasoner does not store another project’s freeze memory centrally.</li>
<li><strong>Improves AI handoff:</strong> the startup freeze context and optional review export tell AI what is already frozen.</li>
<li><strong>Protects your workflow:</strong> AI must provide ZIP + install code + validation code before a feature is accepted.</li>
</ul>
</div>

<h2>4. How it works</h2>
<div class="step"><strong>Step 1:</strong> Select the active project root.</div>
<div class="step"><strong>Step 2:</strong> Click <strong>Create / Repair Box</strong> if the project-local box does not exist.</div>
<div class="step"><strong>Step 3:</strong> Prefer <strong>Prepare Freeze / AI Compliance Update</strong>. Review the log, then click <strong>Do it</strong> or <strong>Undo / Cancel</strong>.</div>
<div class="step"><strong>Step 4:</strong> Prefer <strong>New Local Freeze Entry</strong> for normal freezing, then preview and confirm locally.</div>
<div class="step"><strong>Step 5:</strong> Use <strong>Export for External AI Review</strong> only when you want optional AI review outside the app.</div>
<div class="step"><strong>Step 6:</strong> After local freeze write succeeds, the AI startup context is refreshed for the next programming session.</div>

<h2>5. Active project group</h2>
<div class="card">
<h3>Project root</h3>
<p>The folder of the project you are updating. Example: <code>E:\kanda_reasoner</code>.</p>
<h3>Choose Project Folder</h3>
<p>Opens a folder picker so you can choose the target project.</p>
<h3>Box folder</h3>
<p>Shows the dynamic project-local freeze box path:</p>
<p><code>&lt;project&gt;\project_freeze_after_update</code></p>
<h3>External AI review folder</h3>
<p>Shows the exact dynamic folder used for optional external AI review artifacts:</p>
<p><code>&lt;project&gt;\project_freeze_after_update\files_to_send_ai</code></p>
</div>

<h2>6. Status and actions group</h2>
<div class="card">
<h3>Check Box Status</h3>
<p>Inspects the project-local freeze box and reports whether it is valid, incomplete, or missing.</p>
<h3>Create / Repair Box</h3>
<p>Creates missing folder/files for the freeze-after-update box. Use it before generating files in a new project.</p>
<h3>Export for External AI Review</h3>
<p>Advanced fallback. Generates the old AI review ZIP and instruction Markdown only when you want an external AI to inspect or help. This is no longer the normal freeze path.</p>
<h3>Prepare Freeze / AI Compliance Update</h3>
<p>Stages the action and writes a preview in the log window. It shows what will be read, what will be refreshed, and what will not be touched. No files change yet.</p>
<h3>Do it</h3>
<p>Executes the staged action once and refreshes the AI-compliance package for this active project.</p>
<h3>Undo / Cancel</h3>
<p>Cancels the staged action before writing. In this version, undo means cancel before execution, not rollback after writing.</p>
<h3>Open project_freeze_after_update</h3>
<p>Opens the root freeze box in Windows Explorer.</p>
<h3>Open External AI Review Folder</h3>
<p>Opens the optional external AI review/export folder in Windows Explorer.</p>
<h3>Copy External AI Review Folder Path</h3>
<p>Copies the optional external AI review folder path to the clipboard.</p>
<h3>Show what_to_say_to_ai</h3>
<p>Opens a floating, read-only window with the generated instruction Markdown.</p>
</div>

<h2>7. Advanced external AI review export group</h2>
<div class="card">
<h3>ZIP</h3>
<p>The latest optional external AI review ZIP. Use this only when you want AI review/export instead of the normal local freeze workflow.</p>
<h3>Instruction MD</h3>
<p>The latest generated instruction file for optional external AI review. It is not required for normal local freezing.</p>
</div>

<h2>8. Log window</h2>
<div class="card">
<p>The log window shows what the tab just did: status checks, created paths, generated files, output ZIP, instruction file, and freeze entry count.</p>
<p>Use it as a quick audit trail after each button press.</p>
</div>

<h2>9. Important warning</h2>
<div class="card danger">
<p><strong>Do not manually edit</strong> <code>what_to_say_to_ai_freeze_feature.md</code>.</p>
<p>This file is generated by the blueprint generator. If the text needs to change, update the generator, not the generated file.</p>
</div>

<h2>10. Best practical workflow</h2>
<div class="card good">
<ol>
<li>Select project root.</li>
<li>Click <strong>Check Box Status</strong>.</li>
<li>If incomplete, click <strong>Create / Repair Box</strong>.</li>
<li>After a feature is validated, click <strong>Prepare Freeze / AI Compliance Update</strong>.</li>
<li>Read the log preview.</li>
<li>Click <strong>Do it</strong> if correct, or <strong>Undo / Cancel</strong> if not.</li>
<li>Optional only: click <strong>Export for External AI Review</strong> if you want a review pack for another AI.</li>
<li>Optional only: upload the external review ZIP.</li>
<li>Optional only: click <strong>Show what_to_say_to_ai</strong>, then copy and paste the full instruction text.</li>
<li>Normal path: use <strong>New Local Freeze Entry</strong>, preview, confirm, and write locally.</li>
<li>Only trust the freeze after validation reports clean success.</li>
</ol>
</div>

<p class="small">Box rule: <code>project_freeze_ledger</code> is KANDA Reasoner’s blueprint generator box. <code>project_freeze_after_update</code> is the project-specific freeze memory/output box.</p>
</div>
</body>
</html>
"""

    def _show_help_window(self) -> None:
        """Open the practical Freeze Feature After Update help window."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Freeze Feature After Update - Help")
        dialog.resize(980, 760)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        help_view = QTextEdit()
        help_view.setReadOnly(True)
        help_view.setHtml(self._render_help_html())
        layout.addWidget(help_view, 1)

        button_row = QHBoxLayout()
        copy_button = QPushButton("Copy Complete Help Text")
        close_button = QPushButton("Close")
        button_row.addStretch(1)
        button_row.addWidget(copy_button)
        button_row.addWidget(close_button)
        layout.addLayout(button_row)

        def copy_complete_help_text() -> None:
            QApplication.clipboard().setText(help_view.toPlainText())
            self._append_log("Copied complete Freeze Feature After Update help text.")

        copy_button.clicked.connect(copy_complete_help_text)
        close_button.clicked.connect(dialog.close)

        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

