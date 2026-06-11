from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle.bundle_manifest_builder import (  # noqa: E402
    BUNDLE_ARTIFACT_ORDER,
)
from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import (  # noqa: E402
    generate_ai_context_bundle,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import (  # noqa: E402
    bundle_artifact_paths,
)


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def test_json_handoff_bundle_has_validation_and_exact_active_file_reconstruction(tmp_path: Path) -> None:
    project_root = tmp_path / "developer_tools"
    source_dir = project_root / "src"
    source_dir.mkdir(parents=True)
    paths = bundle_artifact_paths(project_root)
    paths.complete_json.parent.mkdir(parents=True)

    paths.complete_json.write_text(
        '{"bundle_kind":"complete_graph"}',
        encoding="utf-8",
    )
    (source_dir / "main.py").write_bytes(b'print("hello")\r\n')
    (source_dir / "asset.bin").write_bytes(b"\x00\x01\x02binary-data")

    command_results = {
        "architecture_validate": {
            "ran": True,
            "exit_code": 0,
            "status": "pass",
            "summary": "Architecture validation passed.",
        },
        "workflow_validate": {
            "ran": True,
            "exit_code": 0,
            "status": "pass",
            "summary": "Workflow validation passed.",
        },
    }

    result = generate_ai_context_bundle(
        project_root,
        command_results=command_results,
        commands_run_by_bundle=True,
    )

    assert result["ok"] is True
    paths = bundle_artifact_paths(project_root)
    assert paths.reconstruction_payload_json.exists()

    manifest = _read_json(paths.file_manifest_json)
    snapshot = _read_json(paths.active_snapshot_json)
    validation = _read_json(paths.validation_state_json)
    reconstruction = _read_json(paths.reconstruction_payload_json)
    bundle_manifest = _read_json(paths.bundle_manifest_json)

    manifest_paths = {
        str(item["path"]): str(item["sha256_raw"])
        for item in manifest["files"]  # type: ignore[index]
    }
    snapshot_paths = {
        str(item["path"])
        for item in snapshot["files"]  # type: ignore[index]
    }
    manifest_snapshot_paths = {
        str(item["path"])
        for item in manifest["files"]  # type: ignore[index]
        if item.get("included_in_active_snapshot") is True
    }
    reconstruction_files = {
        str(item["path"]): item
        for item in reconstruction["files"]  # type: ignore[index]
    }

    assert manifest_snapshot_paths == snapshot_paths
    assert set(reconstruction_files) == set(manifest_paths)
    assert validation["overall"]["status"] == "pass"  # type: ignore[index]
    assert validation["overall"]["freeze_ready_required_commands"] is True  # type: ignore[index]

    binary_record = reconstruction_files["src/asset.bin"]
    assert binary_record["content_encoding"] == "base64_raw_bytes"
    assert base64.b64decode(str(binary_record["content_base64"])) == b"\x00\x01\x02binary-data"

    text_record = reconstruction_files["src/main.py"]
    assert base64.b64decode(str(text_record["content_base64"])) == b'print("hello")\r\n'

    artifact_names = [item["name"] for item in bundle_manifest["artifacts"]]  # type: ignore[index]
    assert "reconstruction_payload_json" in artifact_names
    assert "reconstruction_payload_json" in BUNDLE_ARTIFACT_ORDER


def main() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        test_json_handoff_bundle_has_validation_and_exact_active_file_reconstruction(
            Path(temp_dir)
        )
    print("JSONCTX014E JSON better-than-project-files handoff tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
