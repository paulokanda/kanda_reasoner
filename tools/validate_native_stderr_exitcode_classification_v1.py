"""Probe validation wrapper handling of benign native stderr output."""
from __future__ import annotations

import sys


def main() -> None:
    """Write one intentional stderr diagnostic and exit successfully."""
    print(
        "BENIGN_NATIVE_STDERR_PROBE: intentional diagnostic; exit code remains zero",
        file=sys.stderr,
    )
    print("NATIVE_STDERR_EXITCODE_CLASSIFICATION: PASS")


if __name__ == "__main__":
    main()
