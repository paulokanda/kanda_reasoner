from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_manual_router_choice_capture import (
    CHOICE_END_MARKER,
    CHOICE_START_MARKER,
    ManualRouterChoiceCaptureError,
    capture_manual_router_choice,
    extract_manual_router_choice_payload,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import REVIEW_FOLDER_NAME


def _make_project_root() -> Path:
    root = Path(tempfile.mkdtemp(prefix="kanda_manual_choice_test_"))
    prompt_dir = root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "04_box_architecture_and_boundaries"
    metadata_dir = root / "kanda_prompt_workspace" / "prompt_library" / "METADATA"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    (prompt_dir / "box_architecture_and_boundaries.md").write_text(
        "# Box Architecture and Boundaries\n\nUse this prompt for box boundary logic.\n",
        encoding="utf-8",
    )
    (metadata_dir / "box_architecture_and_boundaries.meta.json").write_text(
        json.dumps(
            {
                "prompt_code": "KPR-04-001",
                "prompt_id": "box_architecture_and_boundaries",
                "title": "Box Architecture and Boundaries",
                "folder": "ACTIVE_PROMPTS/04_box_architecture_and_boundaries",
                "path": "ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_and_boundaries.md",
                "load_type": "routed",
                "status": "active",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return root


def _choice_block() -> str:
    payload = {
        "schema_version": "1.0",
        "event_type": "chatgpt_router_prompt_choice",
        "source": "chatgpt_browser_with_startup_router_context",
        "user_request": "gimme an example of box code",
        "router_classification": "box architecture / code demo",
        "selected_prompts": [
            {
                "prompt_code": "KPR-04-001",
                "prompt_id": "box_architecture_and_boundaries",
                "rank": 1,
                "reason": "The request is primarily about box logic.",
                "is_primary": True,
            }
        ],
        "advisory_only": True,
    }
    return CHOICE_START_MARKER + "\n" + json.dumps(payload, indent=2) + "\n" + CHOICE_END_MARKER


def test_extract_marked_routing_choice_json() -> None:
    payload = extract_manual_router_choice_payload(_choice_block())
    assert payload["event_type"] == "chatgpt_router_prompt_choice"
    assert payload["selected_prompts"][0]["prompt_code"] == "KPR-04-001"


def test_manual_router_choice_capture_loads_canonical_prompt_and_writes_separate_audit() -> None:
    root = _make_project_root()
    try:
        result = capture_manual_router_choice(root, _choice_block())
        assert result["ok"] is True
        assert result["metric_excluded"] is True
        assert result["ml_sleeping"] is True
        assert result["selected_prompt_codes"] == ("KPR-04-001",)
        assert "# Box Architecture and Boundaries" in result["assembled_prompt"]
        assert "gimme an example of box code" in result["assembled_prompt"]
        audit_file = Path(result["audit_file"])
        assert audit_file.is_file()
        assert REVIEW_FOLDER_NAME in audit_file.parts
        assert "manual_router_choice_captures" in audit_file.parts
        strict_log = root / REVIEW_FOLDER_NAME / "prompt_router_reasoner_reviews.jsonl"
        assert not strict_log.exists(), "manual capture must not append strict MLRT review rows"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_manual_router_choice_rejects_authority_and_mutation_fields() -> None:
    root = _make_project_root()
    payload = json.loads(_choice_block().split(CHOICE_START_MARKER, 1)[1].split(CHOICE_END_MARKER, 1)[0])
    payload["final_route_decision"] = "force_this_prompt"
    try:
        try:
            capture_manual_router_choice(root, json.dumps(payload))
            raise AssertionError("forbidden authority field was accepted")
        except ManualRouterChoiceCaptureError as exc:
            assert "forbidden" in str(exc).lower()
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_manual_router_choice_rejects_path_traversal() -> None:
    root = _make_project_root()
    payload = json.loads(_choice_block().split(CHOICE_START_MARKER, 1)[1].split(CHOICE_END_MARKER, 1)[0])
    payload["selected_prompts"][0]["prompt_code"] = ""
    payload["selected_prompts"][0]["prompt_path"] = "../project_freeze_after_update/secret.md"
    try:
        try:
            capture_manual_router_choice(root, json.dumps(payload))
            raise AssertionError("path traversal was accepted")
        except ManualRouterChoiceCaptureError as exc:
            assert "traversal" in str(exc).lower()
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    test_extract_marked_routing_choice_json()
    test_manual_router_choice_capture_loads_canonical_prompt_and_writes_separate_audit()
    test_manual_router_choice_rejects_authority_and_mutation_fields()
    test_manual_router_choice_rejects_path_traversal()
    print("VALIDATION OK: prompt router reasoner manual router choice capture")
