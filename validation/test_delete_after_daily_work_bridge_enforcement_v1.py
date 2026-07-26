"""Validate daily-work bridge enforcement for patch delivery responses."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.validate_ai_response_patch_delivery import (  # noqa: E402
    ResponseValidationError,
    validate_response_text,
)

FEATURE_ID = "delete-after-daily-work-bridge-enforcement-v1"
BRIDGE_PATH = PROJECT_ROOT / (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/router_bridge_patch_delivery_contract.md"
)
VALIDATOR_PATH = PROJECT_ROOT / "scripts/validate_ai_response_patch_delivery.py"


def read_text(path: Path) -> str:
    """Read a UTF-8 text file with replacement for safety."""
    return path.read_text(encoding="utf-8", errors="replace")


def assert_contains(text: str, fragments: list[str], label: str) -> None:
    """Assert all expected fragments exist in text."""
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise AssertionError(label + " missing fragments: " + ", ".join(missing))


def good_patch_response() -> str:
    """Return a complete response that satisfies the tightened bridge contract."""
    return """
PATCH DELIVERY GATE
ZIP purpose: validate daily-work enforcement
ZIP placement path: <drive>:\\delete_after_daily_work_bridge_enforcement_v1_patch.zip then <drive>:\\kanda_reasoner_delete_after_daily_work\\delete_after_daily_work_bridge_enforcement_v1_patch.zip
What this ZIP is: updated bridge and validator files
What this ZIP is not: a full project copy
Install code present: YES
Validation code present: YES
Expected validation markers: VALIDATION OK: delete-after-daily-work-bridge-enforcement-v1 and STATUS: IN_SYNC
Changed files: router_bridge_patch_delivery_contract.md, validate_ai_response_patch_delivery.py, test_delete_after_daily_work_bridge_enforcement_v1.py
Allowed write paths: active project files only, plus <drive>:\\kanda_reasoner_delete_after_daily_work\\ for transient patch staging, extracted files, helper files, correction files, and validation helper files
Forbidden write paths: active project root for transient install, temp, correction, patch, validation-helper, one-use delivery, or staging files
Freeze/freeze-intake: root-level KANDA_FREEZE_HINT.json only
Error Memory payload: not applicable
Post-validation steps: freeze only after local validation
What not to do: do not unzip manually and do not put helper files in project root
Beginner-safe: YES
GATE STATUS: PASS

[Download patch](sandbox:/mnt/data/delete_after_daily_work_bridge_enforcement_v1_patch.zip)

```powershell
$PROJECT_ROOT = "E:\\kanda_reasoner"
$PATCH_NAME = "delete_after_daily_work_bridge_enforcement_v1_patch"
$PROJECT_NAME = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
$WORK_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
$ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT ($PATCH_NAME + ".zip")
$WORK_PATCH_ZIP = Join-Path $WORK_DIR ($PATCH_NAME + ".zip")
New-Item -ItemType Directory -Path $WORK_DIR -Force | Out-Null
Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force
Remove-Item -Path $ROOT_PATCH_ZIP -Force
$EXTRACT_DIR = Join-Path $WORK_DIR $PATCH_NAME
Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force
```

```powershell
$PROJECT_ROOT = "E:\\kanda_reasoner"
python "$PROJECT_ROOT\\validation\\test_delete_after_daily_work_bridge_enforcement_v1.py"
```

VALIDATION OK: delete-after-daily-work-bridge-enforcement-v1
STATUS: IN_SYNC
"""


def bad_patch_response_missing_gate_containment() -> str:
    """Return a response that tries to allow transient root writes."""
    return good_patch_response().replace(
        "Allowed write paths: active project files only, plus <drive>:\\kanda_reasoner_delete_after_daily_work\\ for transient patch staging, extracted files, helper files, correction files, and validation helper files",
        "Allowed write paths: active project root for project files",
    ).replace(
        "Forbidden write paths: active project root for transient install, temp, correction, patch, validation-helper, one-use delivery, or staging files",
        "Forbidden write paths: none",
    )


def test_bridge_contains_hard_gate() -> None:
    """Check the routed bridge carries the explicit daily-work hard gate."""
    text = read_text(BRIDGE_PATH)
    assert_contains(
        text,
        [
            "## First hard gate: dynamic daily-work containment",
            "<drive>:\\<project_name>_delete_after_daily_work\\",
            "All transient delivery artifacts must be created, staged, extracted, corrected, updated, or consumed only under",
            "The active project root may receive only real intended project files that belong in the project.",
            "Governed persistent freeze-intake and Error Memory intake files must use their canonical project-specific intake folders, not the active project root.",
            "Do not write transient install, temp, correction, patch, validation-helper, one-use delivery, or staging files into the active project root.",
        ],
        "bridge",
    )


def test_validator_contains_daily_work_gate() -> None:
    """Check the response validator enforces explicit daily-work gate values."""
    text = read_text(VALIDATOR_PATH)
    assert_contains(
        text,
        [
            "DAILY_WORK_TOKEN",
            "_validate_daily_work_gate_values",
            "Forbidden write paths must explicitly protect the active project root",
            "Install block is missing required dynamic daily-work staging fragments",
            "FORBIDDEN_INSTALL_BLOCK_TERMS",
        ],
        "validator",
    )


def test_validator_accepts_compliant_response() -> None:
    """Check a compliant response passes the strengthened validator."""
    messages = validate_response_text(good_patch_response())
    if "PATCH DELIVERY RESPONSE CONTRACT: PASS" not in messages:
        raise AssertionError("compliant response did not pass")


def test_validator_rejects_missing_daily_work_gate() -> None:
    """Check a response that omits daily-work containment is rejected."""
    try:
        validate_response_text(bad_patch_response_missing_gate_containment())
    except ResponseValidationError as exc:
        message = str(exc)
        if "_delete_after_daily_work" not in message and "active project root" not in message:
            raise AssertionError("unexpected rejection message: " + message) from exc
        return
    raise AssertionError("validator accepted response without daily-work containment")


def main() -> int:
    """Run validation tests without external dependencies."""
    tests = [
        test_bridge_contains_hard_gate,
        test_validator_contains_daily_work_gate,
        test_validator_accepts_compliant_response,
        test_validator_rejects_missing_daily_work_gate,
    ]
    for test in tests:
        print("RUN " + test.__name__)
        test()
        print("PASS " + test.__name__)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
