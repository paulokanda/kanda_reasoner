# project-path: scripts/validate_prompt_router_reasoner_review_store_rebuild_json_repair_completion_guard_v1.py
"""Validate Prompt Router Reasoner review store rebuild JSON repair and completion guard.

This guard performs no additional source split. It freezes the post-Train-Car-1
state as complete under the v7.2 no-tiny-helper rule and verifies the repaired
append-only log rebuild path imports json correctly.
"""

from __future__ import annotations

import ast
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "prompt-router-reasoner-review-store-rebuild-json-repair-completion-guard-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PKG = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

REFACTOR_CORE_MODULES = {
    "prompt_router_reasoner_review_store.py": "thin public compatibility facade",
    "prompt_router_reasoner_review_models.py": "models/constants/PromptSnapshot/helper functions",
    "prompt_router_reasoner_review_core.py": "project-local store core, index/log lifecycle, review validation",
    "prompt_router_reasoner_review_advisory_files.py": "Ask AI and second-opinion advisory files",
    "prompt_router_reasoner_review_export.py": "read-only dataset export",
    "prompt_router_reasoner_review_import.py": "conservative dataset import",
}

SUBSTANTIVE_HELPERS = [
    "prompt_router_reasoner_review_models.py",
    "prompt_router_reasoner_review_core.py",
    "prompt_router_reasoner_review_advisory_files.py",
    "prompt_router_reasoner_review_export.py",
    "prompt_router_reasoner_review_import.py",
]

PUBLIC_API = [
    "compact_generator_text",
    "compute_ai_human_agreement",
    "detect_ai_second_opinion_label",
    "normalize_agreement_status",
    "normalize_human_label",
    "normalize_router_mode",
    "PromptRouterReasonerItemNotFoundError",
    "PromptRouterReasonerReviewStore",
    "PromptRouterReasonerStoreError",
    "PromptRouterReasonerValidationError",
    "PromptSnapshot",
]

PRIVATE_COMPAT = [
    "_atomic_write_text",
    "_ensure_prompt_snapshot",
    "_json_dumps",
    "_optional_float",
    "_read_json_object",
    "sha256_text",
    "utc_now_iso",
]

OWNERSHIP = {
    "prompt_router_reasoner_review_models.py": [
        "PromptSnapshot",
        "compact_generator_text",
        "detect_ai_second_opinion_label",
        "compute_ai_human_agreement",
    ],
    "prompt_router_reasoner_review_core.py": [
        "PromptRouterReasonerReviewStoreCoreMixin",
        "iter_events",
        "rebuild_index_from_log",
        "create_pending_review",
        "save_review",
        "undo_last_save",
        "_validate_review_item",
    ],
    "prompt_router_reasoner_review_advisory_files.py": [
        "PromptRouterReasonerReviewStoreAdvisoryFilesMixin",
        "save_ask_ai_request",
        "save_ai_second_opinion",
        "write_stats_cache",
        "expected_storage_paths",
    ],
    "prompt_router_reasoner_review_export.py": [
        "PromptRouterReasonerReviewStoreExportMixin",
        "export_review_dataset",
        "list_exported_review_datasets",
        "_review_item_to_export_row",
    ],
    "prompt_router_reasoner_review_import.py": [
        "PromptRouterReasonerReviewStoreImportMixin",
        "preview_import_review_dataset",
        "import_review_dataset",
        "_read_import_dataset_rows",
        "_review_export_row_to_import_item",
    ],
}

FORBIDDEN_STORAGE_MARKERS = [
    "project_freeze_after_update",
    "project_freeze_ledger",
    "frozen_features_memory",
    "freeze_hint_intake",
]


def _assert(condition: bool, message: str) -> None:
    """Support assert behavior.
    
    Parameters
    ----------
    condition : bool
        The condition value.
    message : str
        The message text.
    """
    
    if not condition:
        raise AssertionError(message)


def _text(path: Path) -> str:
    """Support text behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    """Support line count behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return len(_text(path).splitlines())


def _parse(path: Path) -> ast.Module:
    """Support parse behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    ast.Module
        The module result.
    """
    
    return ast.parse(_text(path), filename=str(path))


def _owned_names(path: Path) -> set[str]:
    """Support owned names behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    names: set[str] = set()
    for node in _parse(path).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.add(child.name)
    return names


def _assert_line_policy() -> None:
    """Support assert line policy behavior.
    """
    
    counts = {name: _line_count(PKG / name) for name in REFACTOR_CORE_MODULES}
    _assert(counts["prompt_router_reasoner_review_store.py"] <= 140, "facade no longer thin")
    for name in REFACTOR_CORE_MODULES:
        _assert(counts[name] <= 500, f"refactor-created module exceeds v7.2 maximum: {name}={counts[name]}")
    for name in SUBSTANTIVE_HELPERS:
        _assert(counts[name] >= 100, f"substantive helper became suspiciously tiny under v7.2: {name}={counts[name]}")


def _assert_facade_contract() -> None:
    """Support assert facade contract behavior.
    """
    
    facade = _text(PKG / "prompt_router_reasoner_review_store.py")
    _assert("Thin compatibility facade" in facade, "facade docstring no longer declares thin compatibility facade")
    for marker in [
        "from .prompt_router_reasoner_review_models import",
        "from .prompt_router_reasoner_review_core import",
        "from .prompt_router_reasoner_review_advisory_files import",
        "from .prompt_router_reasoner_review_export import",
        "from .prompt_router_reasoner_review_import import",
    ]:
        _assert(marker in facade, f"facade missing re-export/import marker: {marker}")

    import kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store as contract

    for name in PUBLIC_API:
        _assert(hasattr(contract, name), f"missing public API from facade: {name}")
        _assert(name in contract.__all__, f"public API missing from __all__: {name}")
    for name in PRIVATE_COMPAT:
        _assert(hasattr(contract, name), f"missing private compatibility helper from facade: {name}")


def _assert_ownership() -> None:
    """Support assert ownership behavior.
    """
    
    for module_name, expected_names in OWNERSHIP.items():
        names = _owned_names(PKG / module_name)
        for expected_name in expected_names:
            _assert(expected_name in names, f"{module_name} no longer owns {expected_name}")


def _assert_rebuild_json_repair() -> None:
    """Support assert rebuild json repair behavior.
    """
    
    core_text = _text(PKG / "prompt_router_reasoner_review_core.py")
    _assert("import json" in core_text, "prompt_router_reasoner_review_core.py must import json for iter_events/rebuild_index_from_log")
    _assert("json.loads" in core_text, "iter_events should still parse JSONL events with json.loads")
    _assert("json.JSONDecodeError" in core_text, "iter_events should still catch JSON decode errors")


def _make_snapshot(contract, suffix: str):
    """Support make snapshot behavior.
    
    Parameters
    ----------
    contract : object
        The contract value.
    suffix : str
        The suffix value.
    """
    
    return contract.PromptSnapshot(
        prompt_id=f"prompt.{suffix}",
        prompt_name=f"Prompt {suffix}",
        prompt_path=f"prompts/{suffix}.md",
        prompt_hash=f"hash-{suffix}",
        prompt_summary=f"Summary {suffix}",
        score=0.8 if suffix == "heuristic" else None,
        confidence=0.7 if suffix == "ml" else None,
        keywords=("route", "prompt") if suffix == "heuristic" else (),
    )


def _assert_runtime_boundaries_and_rebuild() -> None:
    """Support assert runtime boundaries and rebuild behavior.
    """
    
    import kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store as contract

    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp) / "project"
        store = contract.PromptRouterReasonerReviewStore(project_root)
        review_id = store.create_pending_review(
            full_generator_text="Please route this request safely.",
            heuristic_prompt=_make_snapshot(contract, "heuristic"),
            ml_prompt=_make_snapshot(contract, "ml"),
            router_mode_at_capture=contract.ROUTER_WITH_HELP_OF_ML,
        )
        _assert(review_id.startswith("prr_"), "review id prefix changed")
        saved = store.save_review(review_id, contract.LABEL_HEURISTICS_CORRECT)
        _assert(saved["review_status"] == contract.STATUS_REVIEWED, "save_review did not mark reviewed")
        undone = store.undo_last_save(review_id)
        _assert(undone["review_status"] == contract.STATUS_PENDING, "undo did not restore pending")

        rebuilt = store.rebuild_index_from_log()
        _assert(review_id in rebuilt["items"], "rebuild_index_from_log lost the review item")
        _assert(rebuilt["items"][review_id]["review_status"] == contract.STATUS_PENDING, "rebuild did not preserve current pending status")

        request = store.save_ask_ai_request(review_id, "External advisory request only")
        _assert(Path(request["text_path"]).exists(), "Ask AI request file missing")
        answer = store.save_ai_second_opinion(review_id, "heuristics correct")
        _assert(answer["metadata"]["advisory_only"] is True, "AI second opinion must remain advisory-only")
        _assert(answer["metadata"]["ai_answer_label_detected"] == contract.LABEL_HEURISTICS_CORRECT, "AI label detection changed")

        store.write_stats_cache({"review_count": 1})
        export = store.export_review_dataset()
        _assert(Path(export["jsonl_path"]).exists(), "export JSONL missing")
        _assert(export["metadata"]["history_unchanged"] is True, "export must remain read-only to history")
        _assert(export["metadata"]["router_changed"] is False, "export must not change router")

        preview = store.preview_import_review_dataset(export["jsonl_path"])
        _assert(preview["dry_run"] is True, "preview import must be dry-run")
        _assert(preview["metadata"]["router_changed"] is False, "preview import must not change router")

        other_store = contract.PromptRouterReasonerReviewStore(Path(tmp) / "other_project")
        import_path = other_store.import_datasets_dir / Path(export["jsonl_path"]).name
        shutil.copy2(export["jsonl_path"], import_path)
        imported = other_store.import_review_dataset(import_path, dry_run=False)
        _assert(imported["imported_count"] == 1, "conservative import should import one missing row")
        _assert(imported["metadata"]["labels_overwritten"] is False, "import must not overwrite labels")
        _assert(imported["metadata"]["router_changed"] is False, "import must not change router")

        duplicate = other_store.import_review_dataset(import_path, dry_run=False)
        _assert(duplicate["imported_count"] == 0, "duplicate import should not create a second review item")
        _assert(duplicate["metadata"]["skipped_existing_count"] >= 1 or duplicate["metadata"]["skipped_duplicate_count"] >= 1, "duplicate import should report skipped rows")

        for path in store.expected_storage_paths():
            normalized = str(path).replace("\\", "/")
            _assert("prompt_router_reasoner_reviews" in normalized, "review path escaped review folder")
            for marker in FORBIDDEN_STORAGE_MARKERS:
                _assert(marker not in normalized, f"review storage path touches forbidden freeze path: {marker}")


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    for module_name in REFACTOR_CORE_MODULES:
        _assert((PKG / module_name).exists(), f"missing refactor-created module: {module_name}")
    _assert_line_policy()
    _assert_facade_contract()
    _assert_ownership()
    _assert_rebuild_json_repair()
    _assert_runtime_boundaries_and_rebuild()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
