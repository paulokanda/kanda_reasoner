"""Compatibility validator for the superseded separated-terminal routine."""

from __future__ import annotations

import argparse
from pathlib import Path

from _answer_validate_freeze_memorize_contract import validate_all

FEATURE_ID = "answer-validate-freeze-memorize-separated-terminal-phases-v1"
SUPERSEDED_BY = "answer-validate-freeze-memorize-chained-install-validate-v1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve(strict=True)

    validate_all(root)
    prompt = (
        root
        / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "05_patch_delivery_and_validation/"
        "patch_validate_freeze_error_memory_routine_blueprint.md"
    ).read_text(encoding="utf-8-sig")

    if "version: 4.2" not in prompt:
        raise AssertionError("CURRENT_ROUTINE_VERSION: FAIL")
    if "One terminal block never executes two lifecycle phases" in prompt:
        raise AssertionError("STALE_STRICT_PHASE_ISOLATION_PRESENT: FAIL")

    print("LEGACY_SEPARATED_TERMINAL_CONTRACT_SUPERSEDED: PASS")
    print("SUPERSEDED_BY: " + SUPERSEDED_BY)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
