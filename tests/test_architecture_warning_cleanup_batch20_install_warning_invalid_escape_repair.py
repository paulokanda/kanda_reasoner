# project-path: tests/test_architecture_warning_cleanup_batch20_install_warning_invalid_escape_repair.py
"""Static smoke coverage for Batch 20 invalid-escape warning repair."""

from __future__ import annotations

from scripts import repair_architecture_warning_cleanup_batch20_runner_help_public_ownership_v1 as repair
from scripts import validate_architecture_warning_cleanup_batch20_install_warning_invalid_escape_repair_v1 as validator


def test_batch20_invalid_escape_repair_entrypoints_are_available() -> None:
    assert repair.__all__ == ["main"]
    assert validator.__all__ == ["main"]
    assert validator.FEATURE_ID == "architecture-warning-cleanup-batch20-install-warning-invalid-escape-repair-v1"


def test_batch20_invalid_escape_repair_static_contract_mentions_warning_controls() -> None:
    text = validator.REPAIR_SCRIPT.read_text(encoding="utf-8-sig")
    assert "import warnings" in text
    assert "warnings.simplefilter" in text
    assert "SyntaxWarning" in text
    assert '"snippets"' in text
    assert "exec(compile" not in text
