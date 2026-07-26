# project-path: tools/validate_large_module_split_audit_safety_classifier_v1.py
"""Run focused safety classifier validation."""
from __future__ import annotations

from importlib import import_module
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
_TEST_MODULE = "validation.test_large_module_split_audit_safety_classifier_v1"


def main() -> int:
    """Run the focused validation with the project root on sys.path."""
    module = import_module(_TEST_MODULE)
    validation_main = getattr(module, "main")
    return int(validation_main())


if __name__ == "__main__":
    raise SystemExit(main())
