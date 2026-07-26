# project-path: tools/validate_project_qa_freeze_merge_quote_fix_v2.py
"""Validate safe native argument quoting in Project QA FREEZE.ps1."""

from __future__ import annotations

import argparse
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze-script", required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    path = Path(args.freeze_script).resolve()
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    required = [
        "function Quote-NativeArgument",
        "(Quote-NativeArgument $FeatureTitle)",
        "(Quote-NativeArgument $ProjectRoot)",
        "(Quote-NativeArgument $ZipPath)",
        "(Quote-NativeArgument $EvidenceFile)",
        '"--feature-title"',
        '"--project-root"',
        '"--feature-id"',
        '"--patch-zip"',
        '"--evidence-file"',
    ]
    missing = [item for item in required if item not in text]
    if missing:
        print("FREEZE MERGE ARGUMENT QUOTING: FAIL")
        for item in missing:
            print("MISSING: " + item)
        return 1
    stale = [
        '"--feature-title",\n        $FeatureTitle,',
    ]
    for item in stale:
        if item in text:
            print("FREEZE MERGE ARGUMENT QUOTING: FAIL")
            print("STALE UNQUOTED FEATURE TITLE ARGUMENT: PRESENT")
            return 1
    print("FREEZE MERGE ARGUMENT QUOTING: PASS")
    print("VALIDATION OK: project-qa-freeze-merge-quote-fix-v2")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
