"""Validate the exact Brick Wall Q06 release ZIP contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Sequence
import zipfile


FEATURE_ID = "brick-wall-q06-tool-project-identity-enforcement-v1"
PATCH_NAME = "kanda_brick_wall_q06_tool_project_identity_v1r2"
CONTROL_MEMBERS = {
    "FREEZE.ps1",
    "INSTALL.ps1",
    "INSTALL_MANIFEST.json",
    "KANDA_FREEZE_HINT.json",
    "PATCH_MANIFEST.json",
    "PATCH_README.txt",
    "VALIDATE.ps1",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _gate(name: str, passed: bool, detail: str = "") -> None:
    if not passed:
        suffix = f" - {detail}" if detail else ""
        raise AssertionError(f"{name}: FAIL{suffix}")
    suffix = f" - {detail}" if detail else ""
    print(f"{name}: PASS{suffix}")


def _safe_member(name: str) -> bool:
    if not name or "\x00" in name:
        return False
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts:
        return False
    if len(normalized) >= 2 and normalized[1] == ":":
        return False
    return True


def _load_json(archive: zipfile.ZipFile, name: str) -> dict[str, object]:
    return json.loads(archive.read(name).decode("utf-8-sig"))


def _validate_zip(patch_zip: Path) -> None:
    _gate("Q06_PATCH_ZIP_EXISTS", patch_zip.is_file(), str(patch_zip))
    with zipfile.ZipFile(patch_zip) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        _gate("Q06_ZIP_MEMBER_SAFETY", all(_safe_member(name) for name in names))
        folded = [name.casefold() for name in names]
        _gate("Q06_ZIP_CASE_COLLISION_GUARD", len(folded) == len(set(folded)))
        _gate(
            "Q06_NO_PYC_OR_CACHE",
            all("__pycache__" not in name and not name.endswith(".pyc") for name in names),
        )
        _gate(
            "Q06_FREEZE_HINT_ROOT_ONLY",
            [name for name in names if name.endswith("KANDA_FREEZE_HINT.json")]
            == ["KANDA_FREEZE_HINT.json"],
        )
        _gate("Q06_CONTROL_MEMBER_SET", CONTROL_MEMBERS.issubset(set(names)))

        patch_manifest = _load_json(archive, "PATCH_MANIFEST.json")
        install_manifest = _load_json(archive, "INSTALL_MANIFEST.json")
        freeze_hint = _load_json(archive, "KANDA_FREEZE_HINT.json")

        _gate(
            "Q06_PATCH_MANIFEST_IDENTITY",
            patch_manifest.get("feature_id") == FEATURE_ID
            and patch_manifest.get("patch_name") == PATCH_NAME,
        )
        expected_members = sorted(str(item) for item in patch_manifest.get("expected_members", []))
        _gate("Q06_EXACT_MEMBER_SET", expected_members == sorted(names))

        items = install_manifest.get("items")
        _gate("Q06_INSTALL_MANIFEST_ITEMS", isinstance(items, list) and bool(items))
        payload_paths = []
        for item in items:
            if not isinstance(item, dict):
                raise AssertionError("Q06_INSTALL_MANIFEST_ITEMS: FAIL - non-object item")
            relative = str(item.get("relative_path", ""))
            payload_paths.append(relative)
            _gate("Q06_MANIFEST_PATH_CONTAINMENT", _safe_member(relative), relative)
            _gate("Q06_PAYLOAD_MEMBER_PRESENT", relative in names, relative)
            _gate(
                "Q06_PAYLOAD_HASH",
                _sha256(archive.read(relative)) == str(item.get("payload_sha256", "")),
                relative,
            )
        _gate(
            "Q06_PAYLOAD_SET_ALIGNMENT",
            sorted(payload_paths)
            == sorted(str(item) for item in patch_manifest.get("payload_files", [])),
        )

        _gate(
            "Q06_FREEZE_PAYLOAD_IDENTITY",
            freeze_hint.get("feature_id") == FEATURE_ID
            and freeze_hint.get("source_patch_zip") == f"{PATCH_NAME}.zip",
        )
        control_text: dict[str, str] = {}
        for name in ("INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"):
            data = archive.read(name)
            _gate("Q06_CONTROL_BYTES", b"\x00" not in data, name)
            text = data.decode("utf-8-sig")
            control_text[name] = text
            _gate("Q06_TERMINAL_STAYS_OPEN", "Clear-Host" in text, name)
        validate_text = control_text["VALIDATE.ps1"]
        _gate(
            "Q06_EMPTY_EVIDENCE_LINE_CAPTURE",
            "[AllowEmptyString()]" in validate_text,
        )
        _gate(
            "Q06_STARTUP_BLANK_LINE_REGRESSION_BLOCKED",
            "Q06_STARTUP_BLANK_LINE_CAPTURE: PASS" in validate_text,
        )
        freeze_text = control_text["FREEZE.ps1"]
        _gate("Q06_FREEZE_NO_INLINE_PYTHON_C", "python -c" not in freeze_text.casefold())
        _gate(
            "Q06_CANONICAL_FREEZE_MERGE",
            "merge_validation_evidence_into_latest_hint" in freeze_text,
        )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--patch-zip", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    _validate_zip(args.patch_zip.resolve())
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
