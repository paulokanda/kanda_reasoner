from __future__ import annotations

from pathlib import Path
import tempfile

from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.session_service import (
    SessionExecutionResult,
    SessionService,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    PromptRouterReasonerReviewStore,
    STATUS_PENDING,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_session_capture import (
    build_heuristic_prompt_snapshot,
    build_ml_advisory_prompt_context_snapshot,
    capture_session_prompt_router_reasoner_review,
    summarize_session_capture_result,
)
from kanda_reasoner_app.reasoner_engine.query_router import route_query_intent
from kanda_reasoner_app.reasoner_engine.v10_models import EvidenceItem, RetrievalBundle


class _BoolControl:
    def __init__(self, value: bool) -> None:
        self._value = value

    def isChecked(self) -> bool:
        return self._value


class _TextControl:
    def __init__(self, value: str) -> None:
        self._value = value

    def currentText(self) -> str:
        return self._value


class _FakeProjectIndex:
    def __init__(self, project_root: Path) -> None:
        self.project_root = str(project_root)
        self.index_data = {"loaded": True}
        self.project_summary = {"entry_files": ["main.py"]}
        self.widget_registry = {}


class _FakeRetriever:
    def retrieve(self, question: str, *, file_limit: int, symbol_limit: int, snippet_limit: int) -> RetrievalBundle:
        return RetrievalBundle(
            file_evidence=[
                EvidenceItem(
                    evidence_id="F1",
                    score=10,
                    path="kanda_reasoner_app/example.py",
                    module_name="example",
                    reason="test evidence",
                    detail="test detail",
                )
            ],
            symbol_evidence=[],
            snippet_evidence=[{"path": "kanda_reasoner_app/example.py", "text": "class Example: pass"}],
        )


class _FakePromptBuilder:
    def build(self, **kwargs) -> str:
        return "FINAL PROMPT FOR: " + str(kwargs.get("question", ""))


class _FakeWindow:
    def __init__(self, project_root: Path) -> None:
        self.project_index = _FakeProjectIndex(project_root)
        self.debug_checkbox = _BoolControl(False)
        self.prefer_code_radio = _BoolControl(True)
        self.verbosity_combo = _TextControl("Normal")
        self.retriever = _FakeRetriever()
        self.prompt_builder = _FakePromptBuilder()
        self.rebuild_count = 0

    def _rebuild_retriever_for_active_profile(self) -> None:
        self.rebuild_count += 1


def test_session_capture_helper_builds_two_valid_snapshots_and_keeps_output_identity() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        decision = route_query_intent("create a patch and validation zip")
        bundle = _FakeRetriever().retrieve("create a patch", file_limit=10, symbol_limit=10, snippet_limit=6)
        final_output = object()
        result = capture_session_prompt_router_reasoner_review(
            project_root=root,
            question="create a patch and validation zip",
            decision=decision,
            bundle=bundle,
            prompt="assembled heuristic prompt",
            final_session_result=final_output,
            selected_model="local-model",
            prefer_code=True,
            verbosity="Normal",
        )
        assert result.final_router_output is final_output
        assert result.final_router_output_unchanged is True
        store = PromptRouterReasonerReviewStore(root)
        items = store.list_review_items()
        assert len(items) == 1
        assert items[0]["review_status"] == STATUS_PENDING
        assert items[0]["heuristic_prompt"]["prompt_id"].startswith("heuristic_session_prompt_")
        assert items[0]["ml_prompt"]["prompt_id"].startswith("ml_shadow_context_")
        assert items[0]["ml_prompt"]["safety_status"] == "advisory_only_no_router_authority"
        assert "no router authority" in items[0]["ml_prompt"]["disagreement_reason"].lower()


def test_snapshot_builders_are_pure_and_do_not_create_review_storage() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        decision = route_query_intent("where is the main entry file")
        bundle = _FakeRetriever().retrieve("where is the main entry file", file_limit=10, symbol_limit=10, snippet_limit=6)
        heuristic = build_heuristic_prompt_snapshot(
            question="where is the main entry file",
            decision=decision,
            bundle=bundle,
            prompt="prompt text",
            selected_model="local-model",
            prefer_code=False,
            verbosity="Concise",
        )
        ml = build_ml_advisory_prompt_context_snapshot(question="where is the main entry file")
        assert heuristic.prompt_id.startswith("heuristic_session_prompt_")
        assert heuristic.safety_status == "authoritative_heuristic_baseline"
        assert ml.prompt_id.startswith("ml_shadow_context_")
        assert ml.safety_status == "advisory_only_no_router_authority"
        assert not (root / "prompt_router_reasoner_reviews").exists()


def test_session_service_runtime_capture_creates_pending_review_without_changing_result() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        window = _FakeWindow(root)
        service = SessionService()
        result = service.execute(window, "explain the architecture of the main window", "local-model")

        assert isinstance(result, SessionExecutionResult)
        assert result.answer_text == "[Streaming...]\n\n"
        assert result.selected_model == "local-model"
        assert window.rebuild_count == 1
        assert any(message.startswith("Prompt Router Reasoner capture: captured") for message in result.log_messages)

        store = PromptRouterReasonerReviewStore(root)
        items = store.list_review_items()
        assert len(items) == 1
        item = items[0]
        assert item["review_status"] == STATUS_PENDING
        assert item["full_generator_text"] == "explain the architecture of the main window"
        assert item["heuristic_prompt"]["safety_status"] == "authoritative_heuristic_baseline"
        assert item["ml_prompt"]["safety_status"] == "advisory_only_no_router_authority"
        assert not (root / "project_freeze_after_update").exists()
        assert not (root / "project_freeze_ledger").exists()


def test_session_capture_log_summary_is_compact() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        decision = route_query_intent("freeze this validated feature")
        bundle = _FakeRetriever().retrieve("freeze this validated feature", file_limit=10, symbol_limit=10, snippet_limit=6)
        result = capture_session_prompt_router_reasoner_review(
            project_root=root,
            question="freeze this validated feature",
            decision=decision,
            bundle=bundle,
            prompt="prompt text",
            final_session_result={"route": "unchanged"},
        )
        summary = summarize_session_capture_result(result)
        assert "Prompt Router Reasoner capture: captured" in summary
        assert "authoritative_output_unchanged=True" in summary
        assert "review_item_id=" in summary


if __name__ == "__main__":
    test_session_capture_helper_builds_two_valid_snapshots_and_keeps_output_identity()
    test_snapshot_builders_are_pure_and_do_not_create_review_storage()
    test_session_service_runtime_capture_creates_pending_review_without_changing_result()
    test_session_capture_log_summary_is_compact()
    print("VALIDATION OK: prompt router reasoner session service runtime capture wiring")
