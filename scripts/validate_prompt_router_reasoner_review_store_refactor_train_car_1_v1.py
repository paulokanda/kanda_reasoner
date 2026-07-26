"""Validate prompt router reasoner review store refactor train car 1."""

from __future__ import annotations

import importlib
import shutil
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "prompt-router-reasoner-review-store-refactor-train-car-1-v1"
ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

PKG = ROOT / "kanda_reasoner_app" / "reasoner_engine"

MODULES = {
    "prompt_router_reasoner_review_store.py": (50, 140),
    "prompt_router_reasoner_review_models.py": (250, 420),
    "prompt_router_reasoner_review_core.py": (300, 500),
    "prompt_router_reasoner_review_advisory_files.py": (180, 320),
    "prompt_router_reasoner_review_export.py": (240, 380),
    "prompt_router_reasoner_review_import.py": (300, 500),
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_text(path).splitlines())


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_static_shape() -> None:
    for name, (minimum, maximum) in MODULES.items():
        path = PKG / name
        _assert(path.exists(), f"missing module: {name}")
        lines = _line_count(path)
        _assert(minimum <= lines <= maximum, f"unexpected line count for {name}: {lines}")

    contract = _text(PKG / "prompt_router_reasoner_review_store.py")
    _assert("class PromptRouterReasonerReviewStore(" in contract, "facade class missing")
    _assert("PromptRouterReasonerReviewStoreCoreMixin" in contract, "core mixin missing")
    _assert("PromptRouterReasonerReviewStoreAdvisoryFilesMixin" in contract, "advisory mixin missing")
    _assert("PromptRouterReasonerReviewStoreExportMixin" in contract, "export mixin missing")
    _assert("PromptRouterReasonerReviewStoreImportMixin" in contract, "import mixin missing")
    _assert("project_freeze_ledger" not in contract, "facade should not route storage to freeze ledger")

    models = _text(PKG / "prompt_router_reasoner_review_models.py")
    _assert("class PromptSnapshot" in models, "PromptSnapshot not owned by models")
    _assert("FORBIDDEN_REVIEW_STORE_PATH_FRAGMENTS" in models, "storage boundary constants missing")
    _assert("project_freeze_after_update" in models, "freeze memory boundary guard missing")
    _assert("project_freeze_ledger" in models, "freeze ledger boundary guard missing")

    core = _text(PKG / "prompt_router_reasoner_review_core.py")
    for needle in (
        "def create_pending_review(",
        "def save_review(",
        "def undo_last_save(",
        "def rebuild_index_from_log(",
        "def _validate_review_item(",
    ):
        _assert(needle in core, f"core ownership missing: {needle}")

    advisory = _text(PKG / "prompt_router_reasoner_review_advisory_files.py")
    for needle in (
        "def save_ask_ai_request(",
        "def save_ai_second_opinion(",
        "advisory_only",
    ):
        _assert(needle in advisory, f"advisory ownership missing: {needle}")

    export = _text(PKG / "prompt_router_reasoner_review_export.py")
    for needle in (
        "def export_review_dataset(",
        "def list_exported_review_datasets(",
        "history_unchanged",
        "router_changed",
    ):
        _assert(needle in export, f"export ownership missing: {needle}")

    importer = _text(PKG / "prompt_router_reasoner_review_import.py")
    for needle in (
        "def import_review_dataset(",
        "dry_run: bool = True",
        "missing_rows_only_skip_conflicts_never_overwrite",
        "labels_overwritten",
        "router_changed",
    ):
        _assert(needle in importer, f"import ownership missing: {needle}")


def validate_runtime_behavior() -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store"
    )
    Store = module.PromptRouterReasonerReviewStore
    Snapshot = module.PromptSnapshot

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        store = Store(root)
        heuristic = Snapshot(
            prompt_id="heuristic.prompt",
            prompt_name="Heuristic Prompt",
            prompt_path="prompts/heuristic.md",
            prompt_hash="hash-heuristic",
            prompt_summary="Heuristic summary",
            score=0.8,
            keywords=("route", "prompt"),
        )
        ml = Snapshot(
            prompt_id="ml.prompt",
            prompt_name="ML Prompt",
            prompt_path="prompts/ml.md",
            prompt_hash="hash-ml",
            prompt_summary="ML summary",
            confidence=0.7,
        )
        review_id = store.create_pending_review(
            full_generator_text="Please route this request safely.",
            heuristic_prompt=heuristic,
            ml_prompt=ml,
            router_mode_at_capture=module.ROUTER_WITH_HELP_OF_ML,
        )
        _assert(review_id.startswith("prr_"), "review id prefix changed")
        _assert(store.get_review_item(review_id)["review_status"] == module.STATUS_PENDING, "pending status changed")

        saved = store.save_review(review_id, module.LABEL_HEURISTICS_CORRECT)
        _assert(saved["review_status"] == module.STATUS_REVIEWED, "save_review did not review")
        undone = store.undo_last_save(review_id)
        _assert(undone["review_status"] == module.STATUS_PENDING, "undo did not restore pending")

        request = store.save_ask_ai_request(review_id, "External advisory request")
        _assert(Path(request["text_path"]).exists(), "ask-ai request text file missing")
        answer = store.save_ai_second_opinion(review_id, "heuristics correct")
        _assert(
            answer["metadata"]["ai_answer_label_detected"] == module.LABEL_HEURISTICS_CORRECT,
            "AI second opinion label detection changed",
        )
        _assert(answer["metadata"]["advisory_only"] is True, "AI second opinion must remain advisory-only")

        store.write_stats_cache({"review_count": 1})
        export = store.export_review_dataset()
        _assert(Path(export["jsonl_path"]).exists(), "export jsonl missing")
        _assert(export["metadata"]["history_unchanged"] is True, "export must not mutate history")
        _assert(export["metadata"]["router_changed"] is False, "export must not change router")
        _assert(store.list_exported_review_datasets(), "export listing failed")

        preview = store.preview_import_review_dataset(export["jsonl_path"])
        _assert(preview["dry_run"] is True, "preview import must be dry run")
        _assert(preview["rows_seen"] == 1, "preview did not read one row")
        _assert(preview["metadata"]["router_changed"] is False, "preview must not change router")

        other = Store(root / "other_project")
        import_target = other.import_datasets_dir / Path(export["jsonl_path"]).name
        shutil.copy2(export["jsonl_path"], import_target)
        imported = other.import_review_dataset(import_target, dry_run=False)
        _assert(imported["imported_count"] == 1, "dataset import failed")
        _assert(imported["metadata"]["labels_overwritten"] is False, "import must not overwrite labels")
        _assert(imported["metadata"]["router_changed"] is False, "import must not change router")

        for path in store.expected_storage_paths():
            normalized = str(path).replace("\\", "/")
            _assert("project_freeze_ledger" not in normalized, "store path touches project_freeze_ledger")
            _assert("project_freeze_after_update" not in normalized, "store path touches project freeze memory")


if __name__ == "__main__":
    _ensure_project_root_on_path()
    validate_static_shape()
    validate_runtime_behavior()
    print(f"VALIDATION OK: {FEATURE_ID}")
