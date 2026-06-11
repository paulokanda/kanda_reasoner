"""Focused tests for JSONCTX013B bundle metadata correctness."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle import (  # noqa: E402
    build_active_snapshot_payload,
    build_file_manifest_payload,
    check_ai_context_bundle,
    generate_ai_context_bundle,
    resolve_project_context,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import (  # noqa: E402
    bundle_artifact_paths,
)


def _make_project() -> Path:
    root = Path(tempfile.mkdtemp(prefix="jsonctx013b_project_"))
    package = root / 'ask_' 'ai_project_reasoner'
    package.mkdir()
    (package / "module.py").write_text("VALUE = 1\r\n", encoding="utf-8", newline="")
    generated = root / "project_analysis_evidence" / "json_complete"
    generated.mkdir(parents=True)
    (generated / "old_generated.json").write_text("{}\n", encoding="utf-8")
    paths = bundle_artifact_paths(resolve_project_context(root))
    paths.complete_json.write_text(json.dumps({"complete": True}), encoding="utf-8")
    return root


def test_file_manifest_treats_generated_json_as_bundle_artifacts_not_active_source() -> None:
    root = _make_project()
    payload = build_file_manifest_payload(root)
    paths = {item["path"] for item in payload["files"]}
    generated_samples = payload["generated_artifact_path_samples"]

    assert 'ask_' 'ai_project_reasoner' '/module.py' in paths
    assert "project_analysis_evidence/json_complete/old_generated.json" not in paths
    assert generated_samples
    assert generated_samples[0]["rule_type"] == "generated_artifact"
    assert payload["counts"]["generated_artifact_path_samples"] == len(generated_samples)


def test_snapshot_preserves_original_newlines_and_declares_fidelity() -> None:
    root = _make_project()
    payload = build_active_snapshot_payload(root)
    files = {item["path"]: item for item in payload["files"]}

    assert files['ask_' 'ai_project_reasoner' '/module.py']["content"] == "VALUE = 1\r\n"
    assert files['ask_' 'ai_project_reasoner' '/module.py']["newline"] == "crlf"
    assert payload["snapshot_policy"]["content_fidelity"] == "text_content_preserves_original_newline_sequences"


def test_bundle_manifest_self_reference_is_not_reported_missing() -> None:
    root = _make_project()
    result = generate_ai_context_bundle(root)
    context = resolve_project_context(root)
    paths = bundle_artifact_paths(context)
    manifest = json.loads(paths.bundle_manifest_json.read_text(encoding="utf-8"))
    artifact_by_name = {item["name"]: item for item in manifest["artifacts"]}

    assert result["ok"], result
    assert manifest["counts"]["required_artifacts_missing"] == 0
    assert manifest["counts"]["artifacts_existing"] == 6
    assert artifact_by_name["bundle_manifest_json"]["exists"] is True
    assert artifact_by_name["bundle_manifest_json"]["self_reference"] is True
    assert artifact_by_name["bundle_manifest_json"]["hash_status"] == "self_hash_not_embedded"
    assert check_ai_context_bundle(root)["ok"] is True


if __name__ == "__main__":
    test_file_manifest_treats_generated_json_as_bundle_artifacts_not_active_source()
    test_snapshot_preserves_original_newlines_and_declares_fidelity()
    test_bundle_manifest_self_reference_is_not_reported_missing()
    print("JSONCTX013B bundle metadata correctness tests passed.")
