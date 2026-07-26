"""Validate No Isolated ZIP Gate v1 prompt and response-validator wiring."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "kanda-router-bridge-no-isolated-zip-gate-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_patch_delivery_contract.md",
    "kanda_prompt_workspace/prompt_library/METADATA/router_bridge_patch_delivery_contract.meta.json",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md",
    "kanda_reasoner_app/patch_governance/KANDA_PATCH_DELIVERY_MANIFEST.schema.json",
    "kanda_reasoner_app/patch_governance/KANDA_PATCH_TRACE.schema.json",
    "scripts/validate_ai_response_patch_delivery.py",
)

REQUIRED_NEEDLES = {
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_patch_delivery_contract.md": (
        "PATCH DELIVERY GATE",
        "No ZIP link may appear unless GATE STATUS is PASS.",
        "Do not deliver a patch ZIP as an isolated artifact.",
    ),
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md": (
        "router_bridge_patch_delivery_contract",
        "NO_ISOLATED_ZIP_ROUTER_BRIDGE_V1_START",
    ),
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md": (
        "router_bridge_patch_delivery_contract",
        "NO_ISOLATED_ZIP_NAVIGATION_GATE_V1_START",
    ),
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md": (
        "NO_ISOLATED_ZIP_RESPONSE_CONTRACT",
        "CONTRACT NOT MET - PATCH DELIVERY BLOCKED",
    ),
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md": (
        "NO_ISOLATED_ZIP_DELIVERY_FORMAT_V1_START",
        "PATCH DELIVERY GATE",
    ),
}

GOOD_RESPONSE = r'''
PATCH DELIVERY GATE
ZIP purpose: test patch delivery response
ZIP placement path: E:\kanda_reasoner
What this ZIP is: a test patch ZIP
What this ZIP is not: a startup ZIP
Install code present: YES
Validation code present: YES
Expected validation markers: VALIDATION OK: kanda-router-bridge-no-isolated-zip-gate-v1
Changed files: scripts/validate_ai_response_patch_delivery.py
Allowed write paths: scripts/
Forbidden write paths: project_freeze_after_update/frozen_features_memory/
Freeze/freeze-intake: KANDA_FREEZE_HINT.json is included for later human-confirmed freeze.
Error Memory payload: included for the user-detected isolated ZIP failure.
Post-validation steps: run startup sync if needed.
What not to do: do not manually unzip into the project.
Beginner-safe: YES
GATE STATUS: PASS

Download: sandbox:/mnt/data/kanda_router_bridge_no_isolated_zip_gate_v1_patch.zip

```powershell
$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "kanda_router_bridge_no_isolated_zip_gate_v1_patch"
$DriveRoot = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
$WorkDir = Join-Path $DriveRoot "kanda_reasoner_delete_after_daily_work"
$RootPatchZip = Join-Path $DriveRoot ($PATCH_NAME + ".zip")
$WorkPatchZip = Join-Path $WorkDir ($PATCH_NAME + ".zip")
New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null
Copy-Item -Force $RootPatchZip $WorkPatchZip
Expand-Archive -Force -Path $WorkPatchZip -DestinationPath (Join-Path $WorkDir "extract")
```

```powershell
$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
python validation\test_no_isolated_zip_gate_v1.py
```
'''

BAD_RESPONSE = "Download this patch: sandbox:/mnt/data/isolated_patch.zip\n"


def _read(relative: str) -> str:
    return (PROJECT_ROOT / relative).read_text(encoding="utf-8", errors="replace")


def _require_files() -> None:
    missing = [relative for relative in REQUIRED_FILES if not (PROJECT_ROOT / relative).is_file()]
    if missing:
        raise AssertionError("Missing required files: " + ", ".join(missing))


def _require_needles() -> None:
    for relative, needles in REQUIRED_NEEDLES.items():
        text = _read(relative)
        absent = [needle for needle in needles if needle not in text]
        if absent:
            raise AssertionError(relative + " missing: " + ", ".join(absent))


def _run_validator(response_text: str, *, expect_success: bool) -> None:
    validator = PROJECT_ROOT / "scripts" / "validate_ai_response_patch_delivery.py"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        handle.write(response_text)
        temp_path = Path(handle.name)
    try:
        completed = subprocess.run(
            [sys.executable, str(validator), str(temp_path), "--user-detected-correction"],
            cwd=str(PROJECT_ROOT),
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if expect_success and completed.returncode != 0:
            raise AssertionError("Expected validator success, got failure:\n" + completed.stdout)
        if not expect_success and completed.returncode == 0:
            raise AssertionError("Expected validator failure, got success:\n" + completed.stdout)
    finally:
        try:
            temp_path.unlink()
        except OSError:
            pass


def main() -> int:
    _require_files()
    _require_needles()
    _run_validator(BAD_RESPONSE, expect_success=False)
    _run_validator(GOOD_RESPONSE, expect_success=True)
    print("VALIDATION OK: " + FEATURE_ID)
    print("PATCH DELIVERY RESPONSE CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
