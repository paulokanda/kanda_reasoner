"""Validate internal naming consistency for a governed patch ZIP."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "patch-internal-name-consistency-v1"
STALE_NAMES = (
    "kanda_aqr_correction_session_until_fresh_pass_v1r3",
    "kanda_aqr_correction_session_until_fresh_pass_v1r4",
)


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(f"{marker}: PASS")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_patch_internal_name_consistency_v1.py <patch-zip>")
    zip_path = Path(sys.argv[1]).resolve()
    with zipfile.ZipFile(zip_path) as archive:
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8"))
        install = archive.read("INSTALL.ps1").decode("utf-8")
        freeze = archive.read("FREEZE.ps1").decode("utf-8")

    patch_name = str(hint.get("patch_name", "")).strip()
    require(zip_path.stem == patch_name, "PATCH_ZIP_NAME_MATCHES_HINT_PATCH_NAME")
    require(
        '$FreezeHintPath = Join-Path $PSScriptRoot "KANDA_FREEZE_HINT.json"' in install
        and '$PATCH_NAME = [string]$FreezeHint.patch_name' in install,
        "INSTALL_DERIVES_PATCH_NAME_FROM_HINT",
    )
    require(
        '$FreezeHintPath = Join-Path $PSScriptRoot "KANDA_FREEZE_HINT.json"' in freeze
        and '$PATCH_NAME = [string]$FreezeHint.patch_name' in freeze,
        "FREEZE_DERIVES_PATCH_NAME_FROM_HINT",
    )
    joined = install + "\n" + freeze
    require(
        all(name not in joined for name in STALE_NAMES),
        "NO_STALE_PACKAGE_PATCH_NAME_LITERAL",
    )
    require(
        str(hint.get("source_patch_zip", "")) == zip_path.name,
        "HINT_SOURCE_PATCH_ZIP_MATCHES_ARCHIVE",
    )
    print("PATCH_INTERNAL_NAME_CONSISTENCY: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
