# project-path: tools/engineering_diagnostics_wave2w_v1r2_public_boundary_gate.py
"""Boundary and implementation-shape gate for Wave 2W v1r2."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2w_v1r2_public_boundary"]

_TOUCHED = (
    "kanda_reasoner_app/safety_suite_cli/__main__.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/bom_provider.py",
    "kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py",
    "kanda_reasoner_app/source_hygiene/shadow_audit.py",
    "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py",
    "tests/test_engineering_diagnostics_wave2w_runtime_corrections.py",
    "tools/engineering_diagnostics_wave2w_v1r2_validation_runtime.py",
    "tools/engineering_diagnostics_wave2w_v1r2_architecture_gate.py",
    "tools/engineering_diagnostics_wave2w_v1r2_public_boundary_gate.py",
    "tools/validate_engineering_diagnostics_wave2w_v1r2.py",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_engineering_diagnostics_wave2w_v1r2_public_boundary(root: Path) -> None:
    root = root.expanduser().resolve(strict=True)
    for relative in _TOUCHED:
        path = root / relative
        _require(path.is_file(), "WAVE2W_V1R2_TOUCHED_FILE_MISSING:" + relative)
        raw = path.read_bytes()
        _require(all(byte < 128 for byte in raw), "WAVE2W_V1R2_NON_ASCII:" + relative)
        text = raw.decode("ascii")
        _require(len(text.splitlines()) <= 500, "WAVE2W_V1R2_MODULE_TOO_LARGE:" + relative)
        ast.parse(text, filename=relative)
    print("WAVE2W V1R2 MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2W V1R2 ASCII SOURCE CONTRACT: PASS")

    entry = (root / _TOUCHED[0]).read_text(encoding="utf-8")
    provider = (root / _TOUCHED[1]).read_text(encoding="utf-8")
    ruff = (root / _TOUCHED[2]).read_text(encoding="utf-8")
    shadow = (root / _TOUCHED[3]).read_text(encoding="utf-8")
    normalizer = (root / _TOUCHED[4]).read_text(encoding="utf-8")

    _require("from .commands import main" in entry, "BOM_CLI_PUBLIC_FACADE_ENTRYPOINT_MISSING")
    _require('"kanda_reasoner_app.safety_suite_cli"' in provider, "BOM_PACKAGE_ENTRYPOINT_NOT_USED")
    _require('"kanda_reasoner_app.safety_suite_cli.commands"' not in provider, "BOM_PRIVATE_MODULE_EXECUTION_RETAINED")
    print("BOM PUBLIC CLI EXECUTION SURFACE: PASS")

    _require("process.communicate(timeout=min(0.10, remaining))" in ruff, "RUFF_PIPE_DRAIN_MISSING")
    _require("sleep(" not in ruff, "RUFF_POLL_WITHOUT_DRAIN_REINTRODUCED")
    _require("RUFF_COLLECTION_TIMEOUT:" in ruff, "RUFF_TIMEOUT_FAIL_CLOSED_MISSING")
    print("RUFF PIPE BACKPRESSURE PREVENTION: PASS")

    for token in (
        "runtime_statement_fingerprint",
        "runtime_statement_ordinal",
        "runtime_statement_kind",
    ):
        _require(token in shadow, "SHADOW_RUNTIME_EVIDENCE_MISSING:" + token)
    _require("statement_key" in normalizer, "SHADOW_RUNTIME_STATEMENT_KEY_MISSING")
    _require("issue.line" not in normalizer.split("semantic_subject", 1)[0], "SHADOW_LINE_COUPLED_IDENTITY")
    print("SHADOW STRUCTURAL STATEMENT IDENTITY: PASS")

    forbidden = (
        "sqlite3.connect",
        "Memorize Error",
    )
    combined = "\n".join(
        (root / relative).read_text(encoding="utf-8") for relative in _TOUCHED[:5]
    )
    for token in forbidden:
        _require(token not in combined, "WAVE2W_V1R2_FORBIDDEN_SURFACE:" + token)
    print("WAVE2W V1R2 PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
