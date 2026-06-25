"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\ai_reasoner_main_window.py
# MANIFEST      : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\ai_reasoner_main_window_help.json
# HELP FOLDER   : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\main_window_help
# PURPOSE       : Execute one question-answer cycle and return a typed session result.
# EXPORTS       : SessionExecutionError, SessionExecutionResult, SessionService
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass

from kanda_reasoner_app.reasoner_engine.v10_models import RetrievalBundle
from kanda_reasoner_app.reasoner_engine.query_router import route_query_intent
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_session_capture import (
    capture_session_prompt_router_reasoner_review,
    summarize_session_capture_result,
)

__all__ = ["SessionExecutionError", "SessionExecutionResult", "SessionService"]


class SessionExecutionError(RuntimeError):
    pass


@dataclass
class SessionExecutionResult:
    route: str
    question: str
    selected_model: str
    bundle: RetrievalBundle
    prompt: str
    answer_text: str
    log_messages: list[str]
    prefer_code: bool


class SessionService:
    def execute(self, window, question: str, selected_model: str) -> SessionExecutionResult:
        if not window.project_index.index_data:
            raise SessionExecutionError("Please load a JSON file first.")
        if not question:
            raise SessionExecutionError("Please type a question.")
        if not selected_model:
            raise SessionExecutionError("Please select a model.")

        decision = route_query_intent(question)
        log_messages = [
            "Query route: "
            + decision.route
            + " | intent="
            + decision.intent_name
            + " | reason="
            + decision.reason
        ]

        if window.debug_checkbox.isChecked():
            log_messages.append(
                "Route debug: question="
                + question
                + " | route="
                + str(getattr(decision, "route", None))
                + " | intent="
                + str(getattr(decision, "intent_name", None))
                + " | reason="
                + str(getattr(decision, "reason", None))
            )

        window._rebuild_retriever_for_active_profile()

        bundle = window.retriever.retrieve(
            question,
            file_limit=10,
            symbol_limit=10,
            snippet_limit=6,
        )

        if not bundle.file_evidence and not bundle.symbol_evidence:
            raise SessionExecutionError("No relevant evidence was retrieved.")

        prefer_code = window.prefer_code_radio.isChecked()
        summary = dict(window.project_index.project_summary or {})
        summary["entry_files"] = summary.get("entry_files", [])
        prompt = window.prompt_builder.build(
            question=question,
            bundle=bundle,
            project_root=window.project_index.project_root,
            summary=summary,
            memory_turns=[],
            prefer_code=prefer_code,
            widget_registry=window.project_index.widget_registry,
            verbosity=window.verbosity_combo.currentText(),
            debug=window.debug_checkbox.isChecked(),
        )

        if decision.route == "ranked":
            lines: list[str] = ["Ranked retrieval result", ""]
            if bundle.file_evidence:
                lines.append("Top file evidence:")
                for item in bundle.file_evidence[:5]:
                    lines.append(f"[{item.evidence_id}] {item.path} | score={item.score}")
            else:
                lines.extend(["Top file evidence:", "None"])

            lines.append("")
            if bundle.symbol_evidence:
                lines.append("Top symbol evidence:")
                for item in bundle.symbol_evidence[:5]:
                    lines.append(
                        f"[{item.evidence_id}] {item.symbol_name} @ {item.path}:{item.line} | score={item.score}"
                    )
            else:
                lines.extend(["Top symbol evidence:", "None"])

            log_messages.append("Answered using ranked retrieval only.")
            result = SessionExecutionResult(
                route="ranked",
                question="",
                selected_model="",
                bundle=bundle,
                prompt="",
                answer_text="\n".join(lines),
                log_messages=log_messages,
                prefer_code=prefer_code,
            )
            self._capture_prompt_router_reasoner_review(window, question, selected_model, decision, bundle, prompt, prefer_code, result, log_messages)
            return result

        if decision.route == "deterministic":
            log_messages.append(
                "Answering with deterministic route via exact resolver / bridge fast path. "
                + "style="
                + ("prefer_code" if prefer_code else "prefer_prose")
            )
        else:
            log_messages.append(
                "Answering with generative route using local model. "
                + "style="
                + ("prefer_code" if prefer_code else "prefer_prose")
            )

        result = SessionExecutionResult(
            route=decision.route,
            question=question,
            selected_model=selected_model,
            bundle=bundle,
            prompt=prompt,
            answer_text="[Streaming...]\n\n",
            log_messages=log_messages,
            prefer_code=prefer_code,
        )
        self._capture_prompt_router_reasoner_review(window, question, selected_model, decision, bundle, prompt, prefer_code, result, log_messages)
        return result

    def _capture_prompt_router_reasoner_review(self, window, question, selected_model, decision, bundle, prompt, prefer_code, result, log_messages) -> None:
        """Record Prompt Router Reasoner runtime evidence without changing the result."""
        try:
            capture_result = capture_session_prompt_router_reasoner_review(
                project_root=window.project_index.project_root,
                question=question,
                decision=decision,
                bundle=bundle,
                prompt=prompt,
                final_session_result=result,
                selected_model=selected_model,
                prefer_code=prefer_code,
                verbosity=window.verbosity_combo.currentText(),
                enabled=True,
            )
            log_messages.append(summarize_session_capture_result(capture_result))
        except Exception as exc:
            log_messages.append("Prompt Router Reasoner capture: skipped | reason=runtime_capture_error | detail=" + str(exc))






