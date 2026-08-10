# project-path: tools/validate_project_web_ai_smart_complete_json_context_v1.py
"""Validate Smart complete-JSON routing inside the canonical Project Web AI tab."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import py_compile
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "project-web-ai-smart-complete-json-context-v1"

CHANGED_CODE = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_complete_json_sections.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_complete_json_router.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_configuration_selector.py",
    "kanda_reasoner_app/web_ai_provider_contracts.py",
    "tools/validate_project_web_ai_smart_complete_json_context_v1.py",
)

PROTECTED_HASHES = {
    "kanda_reasoner_app/local_ai_configuration.py": (
        "9f66737307b4c59f018dcf0e9d02b1313478db1bb022abc06ac40cbcf7030d67"
    ),
    "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py": (
        "00f53d04ebfe4cafa4f291d89f79c906082cd5093311eb629e5ac1c140582c01"
    ),
    "kanda_reasoner_app/reasoner_engine/project_web_ai_session.py": (
        "87c7c9b85785f460448fff1829f943dcc8d283cb393f23f513cea344f516c571"
    ),
    "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py": (
        "e32125dfc3d5c4570df6e4abd193bfd2a899eb1d81c6275d072ef183bcaa68ec"
    ),
    "kanda_reasoner_app/project_selection_registry.py": (
        "98dbb376654e0608f9d6863829999ac5bcf0523715c859f3b067cde42b9d7fa1"
    ),
    "kanda_reasoner_app/project_operation_authority.py": (
        "76dc9df9f415c011a360056af9cf66a126aee7f052c67047f05e4358caed5434"
    ),
    # Approved after the session-key/free-access guard correction.
    "kanda_reasoner_app/web_ai_configuration.py": (
        "ca0b02a41c7f4a70edbdc7a9b89c7121dcbb67a93854d4ce652fa90e292dbe20"
    ),
    "kanda_reasoner_app/web_ai_model_catalog.py": (
        "43009e72d3d67ab4c4869934a142904245c852f6a9278ba2aa0217e2cd0533c4"
    ),
    "kanda_reasoner_app/web_ai_stream_runtime.py": (
        "2bdc5813c6cf16bb5dfa5904cb64a35c08acb0f07ddfcffab49e3f35e4cc9ddd"
    ),
    "kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py": (
        "882956d59d3cc6de1090c6447ba43c7c603ec07124d8ec26d22edec97fcd4843"
    ),
}


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    """Return one file SHA-256."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_source_contract(root: Path) -> None:
    """Validate syntax, module size, ownership, and read-only implementation."""
    with tempfile.TemporaryDirectory(
        prefix="kanda_smart_context_compile_"
    ) as compile_dir:
        compile_root = Path(compile_dir)
        for relative in CHANGED_CODE:
            path = root / relative
            require(path.is_file(), "changed source missing: " + relative)
            text = path.read_text(encoding="utf-8")
            require(text.isascii(), "non-ASCII changed source: " + relative)
            ast.parse(text, filename=str(path))
            py_compile.compile(
                str(path),
                cfile=str(compile_root / (path.name + ".pyc")),
                doraise=True,
            )
            require(
                0 < len(text.splitlines()) <= 500,
                relative + " exceeds 500 physical lines",
            )
    print("SMART_COMPLETE_JSON_PYTHON_SYNTAX: PASS")
    print("SMART_COMPLETE_JSON_MODULE_SIZE: PASS")

    router = (root / CHANGED_CODE[1]).read_text(encoding="utf-8")
    sections = (root / CHANGED_CODE[0]).read_text(encoding="utf-8")
    combined = router + "\n" + sections
    for forbidden in (
        "write_text(",
        "write_bytes(",
        ".unlink(",
        "os.replace(",
        "shutil.",
        "resolve_complete_json_evidence",
    ):
        require(forbidden not in combined, "write-capable token present: " + forbidden)
    for required in (
        "working_copy_json_path",
        "primary_evidence_json_path",
        "SMART COMPLETE JSON ROUTE",
        "generated routing evidence; exact source remains authoritative",
    ):
        require(required in router, "router contract missing: " + required)
    print("SMART_COMPLETE_JSON_READ_ONLY_RESOLUTION: PASS")
    print("SMART_COMPLETE_JSON_NO_WRITE_AUTHORITY: PASS")

    for relative, expected in PROTECTED_HASHES.items():
        require(
            sha256(root / relative) == expected,
            "protected source changed: " + relative,
        )
    print("LOCAL_AI_PROTECTED_HASHES: PASS")
    print("PROJECT_WEB_AI_CORE_PROTECTED_HASHES: PASS")
    print("DIRECT_PROVIDER_CONFIG_PROTECTED_HASHES: PASS")


def _fixture_payload(project_root: Path) -> dict[str, object]:
    """Return one complete-JSON fixture with nested duplicate section names."""
    return {
        "web_ai_readme": {
            "sections": {"web_ai_symbol_index": {"note": "nested and smaller"}}
        },
        "primary_definition_index": {
            "ProviderRouter": {
                "file": "kanda_reasoner_app/provider_router.py",
                "line_start": 10,
            }
        },
        "web_ai_symbol_index": {
            "ProviderRouter": {
                "file": "kanda_reasoner_app/provider_router.py",
                "qualified_name": "provider.ProviderRouter",
                "docstring_first_line": "Select gateway and direct API providers",
                "project_root": str(project_root),
            },
            "UnrelatedWidget": {
                "file": "kanda_reasoner_app/unrelated_widget.py",
                "qualified_name": "widgets.UnrelatedWidget",
            },
        },
        "entry_points_detail": [
            {
                "name": "main",
                "file": "kanda_reasoner_app/__main__.py",
                "reason": "provider configuration entry point",
            }
        ],
        "web_ai_file_responsibility_index": {
            "kanda_reasoner_app/provider_router.py": {
                "responsibility": "Web AI provider selection and API routing"
            }
        },
        "web_ai_test_protection_index": {
            "kanda_reasoner_app/provider_router.py": {
                "linked_tests": [{"test_file": "tools/test_provider_router.py"}]
            }
        },
        "stable_evidence_id_index": {
            "provider-router": {
                "file": "kanda_reasoner_app/provider_router.py",
                "symbol": "ProviderRouter",
            }
        },
    }


def validate_router_runtime(root: Path) -> None:
    """Validate extraction, routing, redaction, and fail-closed behavior."""
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.reasoner_engine import (
        project_web_ai_complete_json_router as router,
    )
    from kanda_reasoner_app.reasoner_engine import (
        project_web_ai_complete_json_sections as section_reader,
    )
    SmartCompleteJsonReadError = section_reader.SmartCompleteJsonReadError
    extract_complete_json_sections = section_reader.extract_complete_json_sections

    with tempfile.TemporaryDirectory() as temporary:
        project_root = Path(temporary) / "fixture_project"
        project_root.mkdir()
        complete_json = Path(temporary) / "fixture__complete_local_AI.json"
        complete_json.write_text(
            json.dumps(_fixture_payload(project_root), separators=(",", ":")),
            encoding="utf-8",
        )
        sections = extract_complete_json_sections(complete_json)
        require(
            len(sections["web_ai_symbol_index"]) == 2,
            "largest top-level symbol section was not selected",
        )
        print("SMART_COMPLETE_JSON_LARGEST_SECTION_SELECTION: PASS")

        original_resolver = router._resolve_read_only_complete_json
        router._resolve_read_only_complete_json = lambda _root: (
            complete_json,
            "fixture complete JSON",
            "fixture",
        )
        try:
            routed = router.route_complete_json_context(
                project_root,
                "How does Web AI select a direct API provider?",
                "compact-context",
            )
        finally:
            router._resolve_read_only_complete_json = original_resolver

        require(routed.smart_context_used, "smart route unexpectedly fell back")
        require(routed.record_count >= 4, "too few relevant records routed")
        require(
            "ProviderRouter" in routed.context_text,
            "relevant provider evidence missing",
        )
        require(
            "UnrelatedWidget" not in routed.context_text,
            "unrelated evidence was included",
        )
        require(str(project_root) not in routed.context_text, "absolute root leaked")
        windows_root = r"E:\\kanda_reasoner"
        serialized_root = json.dumps({"root": windows_root})
        redacted_root = router._redact_root(serialized_root, windows_root)
        escaped_windows_root = json.dumps(windows_root)[1:-1]
        require(windows_root not in redacted_root, "Windows root leaked")
        require(
            escaped_windows_root not in redacted_root,
            "escaped Windows root leaked",
        )
        require("<PROJECT_ROOT>" in redacted_root, "Windows root marker missing")
        require("<PROJECT_ROOT>" in routed.context_text, "root marker missing")
        require(
            routed.context_bytes <= len(b"compact-context") + 64 * 1024,
            "budget exceeded",
        )
        require(len(routed.evidence_context_hash) == 64, "route hash missing")
        print("SMART_COMPLETE_JSON_QUERY_ROUTING: PASS")
        print("SMART_COMPLETE_JSON_CONTEXT_BUDGET: PASS")
        print("SMART_COMPLETE_JSON_ROOT_REDACTION: PASS")

        profile = SimpleNamespace(display_name="Gemini", privacy_summary="privacy")
        model = SimpleNamespace(model_id="gemini-test", price_label=lambda: "free")
        snapshot = SimpleNamespace(project_slug="fixture", short_hash=lambda: "abc123")
        approval = router.build_remote_approval_text(
            profile,
            model,
            snapshot,
            routed,
            api_key_provided=True,
            read_tools_enabled=True,
        )
        for token in (
            "Smart complete-JSON context: enabled",
            "Routed evidence records:",
            "Evidence context hash:",
            f"Context: {routed.context_bytes:,} bytes",
        ):
            require(token in approval, "approval summary missing: " + token)
        require(str(project_root) not in approval, "approval leaked absolute root")
        print("SMART_COMPLETE_JSON_APPROVAL_SUMMARY: PASS")

        missing_resolver = router._resolve_read_only_complete_json
        router._resolve_read_only_complete_json = lambda _root: (None, "", "missing")
        try:
            fallback = router.route_complete_json_context(
                project_root,
                "provider",
                "compact-context",
            )
        finally:
            router._resolve_read_only_complete_json = missing_resolver
        require(not fallback.smart_context_used, "missing evidence did not fall back")
        require(
            fallback.context_text == "compact-context",
            "fallback changed compact context",
        )
        print("SMART_COMPLETE_JSON_MISSING_EVIDENCE_FALLBACK: PASS")

        malformed = Path(temporary) / "malformed.json"
        malformed.write_text('{"web_ai_symbol_index":{]}', encoding="utf-8")
        try:
            extract_complete_json_sections(malformed)
        except SmartCompleteJsonReadError:
            pass
        else:
            raise AssertionError("malformed present evidence did not fail closed")
        print("SMART_COMPLETE_JSON_MALFORMED_EVIDENCE_REJECTED: PASS")


def validate_integration(root: Path) -> None:
    """Validate canonical Web AI integration and request identity binding."""
    contracts = (root / "kanda_reasoner_app/web_ai_provider_contracts.py").read_text(
        encoding="utf-8"
    )
    tab = (root / "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py").read_text(
        encoding="utf-8"
    )
    require("evidence_context_hash: str = \"\"" in contracts, "identity field missing")
    for token in (
        "route_complete_json_context(",
        "build_remote_approval_text(",
        "evidence_context_hash=routed_context.evidence_context_hash",
        "routed_context.context_text",
        "bool(identity.evidence_context_hash)",
    ):
        require(token in tab, "Project Web AI integration missing: " + token)
    require("FreePythonAITab" not in tab, "duplicate chat owner returned")
    print("SMART_COMPLETE_JSON_REQUEST_IDENTITY: PASS")
    print("ONE_PROJECT_WEB_AI_CONVERSATION_OWNER: PASS")


def validate_real_qt(root: Path, *, allow_missing_qt: bool = False) -> None:
    """Instantiate the canonical Web AI tab under real PySide6."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    sys.path.insert(0, str(root))
    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication
        from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import (
            ProjectWebAITab,
        )
    except ModuleNotFoundError:
        if allow_missing_qt:
            print("SMART_COMPLETE_JSON_REAL_QT: NOT_RUN_LOCAL_ENV")
            return
        raise

    app = QApplication.instance() or QApplication([])
    widget = ProjectWebAITab()
    require(widget.objectName() == "projectWebAITab", "wrong canonical Web AI widget")
    require(
        "Smart complete-JSON" in (root / CHANGED_CODE[2]).read_text(encoding="utf-8"),
        "smart context status not visible",
    )
    widget.close()
    widget.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    app.processEvents()
    print("SMART_COMPLETE_JSON_REAL_QT: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--allow-missing-qt", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source_contract(root)
    validate_router_runtime(root)
    validate_integration(root)
    validate_real_qt(root, allow_missing_qt=args.allow_missing_qt)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
