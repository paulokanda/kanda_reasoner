"""Validate the explicit nonfreezeable Workbench recovery package contract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import zipfile


REQUIRED_ROOT_FILES = {
    "INSTALL.ps1",
    "VALIDATE.ps1",
    "PACKAGE_MANIFEST.json",
    "NONFREEZEABLE_REASON.txt",
    "README.txt",
}
FORBIDDEN_SCRIPT_SNIPPETS = (
    "Downloads",
    "Desktop",
    "python -c",
    "python.exe -c",
)


def _sha256_bytes(data: bytes) -> str:
    """Return SHA-256 for bytes."""
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    """Validate one recovery ZIP path."""
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: validate_nonfreezeable_workbench_recovery_package_contract_v1.py <zip>"
        )

    zip_path = Path(sys.argv[1]).resolve()
    assert zip_path.is_file(), "PATCH_ZIP_MISSING"

    with zipfile.ZipFile(zip_path, "r") as archive:
        infos = archive.infolist()
        names = [item.filename for item in infos]
        assert len(names) == len(set(names)), "DUPLICATE_ZIP_MEMBER"
        assert REQUIRED_ROOT_FILES.issubset(set(names)), "REQUIRED_ROOT_FILE_MISSING"
        assert "KANDA_FREEZE_HINT.json" not in names, (
            "NONFREEZEABLE_PACKAGE_MUST_NOT_CLAIM_FREEZE_HINT"
        )
        assert not any(
            name.endswith(".pyc") or "__pycache__/" in name
            for name in names
        ), "BYTECODE_ARTIFACT_FORBIDDEN"
        assert all(
            not name.startswith("/")
            and ".." not in Path(name).parts
            and "\\" not in name
            for name in names
        ), "UNSAFE_ZIP_MEMBER_PATH"

        manifest = json.loads(
            archive.read("PACKAGE_MANIFEST.json").decode("utf-8")
        )
        assert manifest.get("freezeable") is False, (
            "PACKAGE_MUST_BE_EXPLICITLY_NONFREEZEABLE"
        )
        assert str(manifest.get("nonfreezeable_reason", "")).strip(), (
            "NONFREEZEABLE_REASON_REQUIRED"
        )

        reason = archive.read("NONFREEZEABLE_REASON.txt").decode("utf-8").strip()
        assert reason == str(manifest["nonfreezeable_reason"]).strip(), (
            "NONFREEZEABLE_REASON_MISMATCH"
        )

        for item in manifest.get("files", []):
            operation = str(item.get("operation", ""))
            relative = str(item.get("relative_path", ""))
            assert operation in {"replace", "delete"}, "UNKNOWN_OPERATION"
            assert relative and not relative.startswith("/"), (
                "RELATIVE_PATH_REQUIRED"
            )
            assert ".." not in Path(relative).parts, "RELATIVE_PATH_TRAVERSAL"
            if operation == "replace":
                member = "payload/" + relative
                assert member in names, "PAYLOAD_MEMBER_MISSING:" + relative
                digest = _sha256_bytes(archive.read(member))
                assert digest == str(item.get("sha256", "")), (
                    "PAYLOAD_HASH_MISMATCH:" + relative
                )
            else:
                assert "payload/" + relative not in names, (
                    "DELETE_TARGET_MUST_NOT_HAVE_PAYLOAD:" + relative
                )
                assert item.get("accepted_existing_sha256"), (
                    "DELETE_HASH_GUARD_REQUIRED:" + relative
                )

        install_text = archive.read("INSTALL.ps1").decode("utf-8")
        validate_text = archive.read("VALIDATE.ps1").decode("utf-8")
        combined = install_text + "\n" + validate_text
        for snippet in FORBIDDEN_SCRIPT_SNIPPETS:
            assert snippet not in combined, (
                "FORBIDDEN_SCRIPT_SNIPPET:" + snippet
            )
        assert "SOURCE FRESHNESS GUARD: PASS" in install_text
        assert "PATCH CLASSIFICATION: NONFREEZEABLE TRANSITIONAL RECOVERY" in validate_text

    print("NONFREEZEABLE_MANIFEST_CONTRACT: PASS")
    print("NONFREEZEABLE_REASON_CONTRACT: PASS")
    print("PAYLOAD_HASH_CONTRACT: PASS")
    print("DELETE_HASH_GUARD_CONTRACT: PASS")
    print("NO_FREEZE_HINT_CLAIM: PASS")
    print("NO_DOWNLOADS_DESKTOP_FALLBACK: PASS")
    print("NO_INLINE_PYTHON_C: PASS")
    print("ZIP_REOPEN_AND_CONTENT_SCOPE: PASS")
    print("NONFREEZEABLE ZIP CONTRACT: PASS")


if __name__ == "__main__":
    main()
