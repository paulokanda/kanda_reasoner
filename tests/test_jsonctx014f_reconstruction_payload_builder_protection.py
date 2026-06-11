from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle.reconstruction_payload_builder import (  # noqa: E402
    build_reconstruction_payload,
    write_reconstruction_payload_json,
)


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def test_reconstruction_payload_builder_public_api_is_directly_protected(tmp_path: Path) -> None:
    project_root = tmp_path / "developer_tools"
    source_dir = project_root / "src"
    source_dir.mkdir(parents=True)

    text_path = source_dir / "main.py"
    binary_path = source_dir / "asset.bin"
    text_path.write_bytes(b'print("hello")\r\n')
    binary_path.write_bytes(b"\x00\x01\x02binary-data")

    payload = build_reconstruction_payload(project_root)

    assert payload["bundle_kind"] == "reconstruction_payload"
    assert payload["reconstruction_policy"]["exact_file_bytes"] is True
    assert payload["reconstruction_policy"]["exact_binary_reconstruction"] is True
    assert payload["reconstruction_policy"]["internet_or_ai_contact"] is False

    files = {
        str(item["path"]): item
        for item in payload["files"]
    }

    assert set(files) == {"src/asset.bin", "src/main.py"}
    assert base64.b64decode(str(files["src/main.py"]["content_base64"])) == b'print("hello")\r\n'
    assert base64.b64decode(str(files["src/asset.bin"]["content_base64"])) == b"\x00\x01\x02binary-data"

    output_path = write_reconstruction_payload_json(project_root)
    assert output_path.exists()

    written = _read_json(output_path)
    assert written["bundle_kind"] == "reconstruction_payload"
    assert written["counts"]["files"] == 2
    assert written["counts"]["embedded_files"] == 2


def main() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        test_reconstruction_payload_builder_public_api_is_directly_protected(
            Path(temp_dir)
        )
    print("JSONCTX014F reconstruction payload builder protection tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
