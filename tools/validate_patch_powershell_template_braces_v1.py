"""Reject unreplaced template braces in packaged PowerShell scripts."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_patch_powershell_template_braces_v1.py <patch.zip>")
    patch = Path(sys.argv[1]).resolve()
    if not patch.is_file():
        raise FileNotFoundError(patch)
    with zipfile.ZipFile(patch) as zf:
        for name in ("INSTALL.ps1", "VALIDATE.ps1"):
            text = zf.read(name).decode("utf-8-sig")
            if "{{" in text or "}}" in text:
                raise AssertionError(f"UNREPLACED_TEMPLATE_BRACES:{name}")
    print("POWERSHELL_TEMPLATE_BRACE_GUARD: PASS")


if __name__ == "__main__":
    main()
