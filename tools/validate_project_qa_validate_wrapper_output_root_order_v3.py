"""Validate Project QA VALIDATE.ps1 output-root initialization order."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-script", required=True)
    args = parser.parse_args()
    text = Path(args.validate_script).read_text(encoding="utf-8-sig")
    output_pos = text.find('$OutputRoot = Join-Path $DailyRoot')
    stdout_pos = text.find('$WrapperStdout = Join-Path $OutputRoot')
    stderr_pos = text.find('$WrapperStderr = Join-Path $OutputRoot')
    if min(output_pos, stdout_pos, stderr_pos) < 0:
        raise SystemExit("Required output-root wrapper lines are missing.")
    if not (output_pos < stdout_pos and output_pos < stderr_pos):
        raise SystemExit("OutputRoot must be initialized before wrapper output paths.")
    print("VALIDATE WRAPPER OUTPUT ROOT ORDER: PASS")
    print("VALIDATION OK: project-qa-validate-wrapper-output-root-order-v3")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
