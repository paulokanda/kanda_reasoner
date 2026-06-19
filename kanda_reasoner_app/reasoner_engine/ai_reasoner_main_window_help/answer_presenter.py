"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\ai_reasoner_main_window.py
# MANIFEST      : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\ai_reasoner_main_window_help.json
# HELP FOLDER   : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\main_window_help
# PURPOSE       : Present evidence, history, final answers, and AI errors in the GUI.
# EXPORTS       : ConfidenceStatus, AnswerPresenter
# DEPENDS ON    : ui_components.py
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

from kanda_reasoner_app.reasoner_engine.main_window_help.ui_components import (
    shorten_path,
)
from kanda_reasoner_app.reasoner_engine.v10_models import ConversationTurn, RetrievalBundle

__all__ = ["ConfidenceStatus", "AnswerPresenter"]


@dataclass(frozen=True)
class ConfidenceStatus:
    label: str
    evidence_count: int


class AnswerPresenter:
    def populate_evidence_lists(self, window, bundle: RetrievalBundle) -> None:
        window.file_evidence_list.clear()
        window.symbol_evidence_list.clear()
        window.detail_box.clear()

        for item in bundle.file_evidence:
            label = "[" + item.evidence_id + "] " + shorten_path(item.path) + " | score=" + str(item.score)
            list_item = QListWidgetItem(label)
            list_item.setData(Qt.UserRole, item.evidence_id)
            window.file_evidence_list.addItem(list_item)

        for item in bundle.symbol_evidence:
            label = (
                "[" + item.evidence_id + "] "
                + item.symbol_name
                + " @ "
                + shorten_path(item.path, 70)
                + ":"
                + str(item.line)
            )
            list_item = QListWidgetItem(label)
            list_item.setData(Qt.UserRole, item.evidence_id)
            window.symbol_evidence_list.addItem(list_item)

        if bundle.file_evidence:
            window.file_evidence_list.setCurrentRow(0)
        elif bundle.symbol_evidence:
            window.symbol_evidence_list.setCurrentRow(0)

    def show_selected_file_detail(self, window, current) -> None:
        if not current:
            return
        evidence_id = current.data(Qt.UserRole)
        for item in window._last_bundle.file_evidence:
            if item.evidence_id == evidence_id:
                window.detail_box.setPlainText(item.detail)
                return

    def show_selected_symbol_detail(self, window, current) -> None:
        if not current:
            return
        evidence_id = current.data(Qt.UserRole)
        for item in window._last_bundle.symbol_evidence:
            if item.evidence_id == evidence_id:
                window.detail_box.setPlainText(item.detail)
                return

    def show_selected_history_turn(self, window, current) -> None:
        if not current:
            return
        row = window.history_list.row(current)
        turns = window.memory.turns()
        if row < 0 or row >= len(turns):
            return
        turn = turns[row]
        window.answer_box.setPlainText(turn.answer)
        window.prompt_preview.setPlainText(turn.prompt)

    def refresh_history_list(self, window) -> None:
        window.history_list.clear()
        for idx, turn in enumerate(window.memory.turns(), start=1):
            label = str(idx) + ". " + turn.question
            item = QListWidgetItem(label)
            window.history_list.addItem(item)

    def _build_confidence_status(self, bundle: RetrievalBundle) -> ConfidenceStatus:
        evidence_count = len(bundle.file_evidence) + len(bundle.symbol_evidence)
        if evidence_count < 3:
            label = "low"
        elif evidence_count < 7:
            label = "medium"
        else:
            label = "high"
        return ConfidenceStatus(label=label, evidence_count=evidence_count)

    def handle_ai_answer_ready(self, window, text: str) -> None:
        window.answer_box.setPlainText(text)
        window._append_log("Local AI answer received.")

        turn = ConversationTurn(
            question=window._pending_question,
            answer=text,
            prompt=window._last_prompt,
            retrieval=window._last_bundle,
            selected_model=window._last_selected_model,
        )

        confidence = self._build_confidence_status(window._last_bundle)
        window.statusBar().showMessage(
            "Answer confidence: "
            + confidence.label
            + " (based on "
            + str(confidence.evidence_count)
            + " evidence items)"
        )

        window.memory.add_turn(turn)
        self.refresh_history_list(window)

    def handle_ai_error_ready(self, window, error_text: str) -> None:
        window.answer_box.setPlainText("AI error:\n" + error_text)
        window._append_log("AI error: " + error_text)






