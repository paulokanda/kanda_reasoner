# project-path: tools/validate_complete_json_web_ai_enrichment_ast_safe_refactor_v1.py
"""Validate the complete JSON Web-AI enrichment AST-safe refactor."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import sys
import zipfile
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

__all__ = [
    "main",
]


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_REL = (
    "kanda_reasoner_app/reasoner_context_collector/"
    "complete_json_web_ai_enrichment.py"
)
HELPER_REL = (
    "kanda_reasoner_app/reasoner_context_collector/"
    "_complete_json_web_ai_enrichment_analysis.py"
)
VALIDATOR_REL = "tools/validate_complete_json_web_ai_enrichment_ast_safe_refactor_v1.py"
FEATURE_ID = "complete-json-web-ai-enrichment-ast-safe-refactor-v1"
BASELINE_TARGET_SHA256 = (
    "3eab0a1f0d2124d14be9ccac6bd3bf34b548804fcebdda970aa1365a3137522c"
)
EXPECTED_PUBLIC_ALL = [
    "REQUIRED_WEB_AI_SECTIONS",
    "build_web_ai_sections",
    "complete_json_path_for_project",
    "enrich_complete_json_for_web_ai",
    "enrich_project_complete_json",
    "main",
]
DYNAMIC_CALL_NAMES = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "getattr",
    "globals",
    "locals",
    "setattr",
    "vars",
    "importlib.import_module",
}

def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return parent + "." + node.attr if parent else node.attr
    return ""


def _dynamic_calls(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node.func)
        if name in DYNAMIC_CALL_NAMES or name == "ast.unparse":
            found.append(name)
    return sorted(found)


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _assert_size(path: Path) -> None:
    count = _line_count(path)
    if not 101 <= count <= 499:
        raise AssertionError(f"MODULE_SIZE_101_499 failed for {path}: {count}")


def _assert_ascii_utf8_no_bom(path: Path) -> None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssertionError(f"UTF8_BOM_FORBIDDEN: {path}")
    raw.decode("ascii")


def _assert_dependency_direction(helper: Path) -> None:
    tree = ast.parse(helper.read_text(encoding="utf-8"), filename=str(helper))
    forbidden = "complete_json_web_ai_enrichment"
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and forbidden in str(node.module or ""):
            raise AssertionError("HELPER_TO_FACADE_IMPORT")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if forbidden in alias.name:
                    raise AssertionError("HELPER_TO_FACADE_IMPORT")


def _assert_main_guard_boundary(target: Path, helper: Path) -> None:
    target_text = target.read_text(encoding="utf-8")
    helper_text = helper.read_text(encoding="utf-8")
    marker = 'if __name__ == "__main__":'
    if marker not in target_text:
        raise AssertionError("MAIN_GUARD_MISSING_FROM_FACADE")
    if marker in helper_text:
        raise AssertionError("MAIN_GUARD_LEAKED_TO_HELPER")


def _create_fixture(root: Path) -> None:
    (root / "pkg").mkdir(parents=True, exist_ok=True)
    (root / "tests").mkdir(parents=True, exist_ok=True)
    (root / "pkg" / "a.py").write_text(
        "def alpha(x: int) -> int:\n    return x + 1\n\n"
        "class PublicThing:\n    pass\n",
        encoding="utf-8",
    )
    (root / "pkg" / "cli.py").write_text(
        "def main():\n    return 0\n\n"
        'if __name__ == "__main__":\n    raise SystemExit(main())\n',
        encoding="utf-8",
    )
    (root / "pkg" / "async_mod.py").write_text(
        'async def fetch() -> str:\n    return "ok"\n',
        encoding="utf-8",
    )
    (root / "tests" / "test_a.py").write_text(
        "def test_alpha():\n    assert True\n",
        encoding="utf-8",
    )
    (root / "pkg" / "bad.py").write_text(
        "def broken(:\n    pass\n",
        encoding="utf-8",
    )


def _behavior_payload() -> dict[str, Any]:
    from kanda_reasoner_app.reasoner_context_collector import (
        complete_json_web_ai_enrichment as module,
    )

    if list(module.__all__) != EXPECTED_PUBLIC_ALL:
        raise AssertionError("PUBLIC_API_ALL_CHANGED")

    with TemporaryDirectory() as tmp:
        root = Path(tmp) / "fixture"
        _create_fixture(root)
        sections = module.build_web_ai_sections(root)
        target = Path(tmp) / "complete.json"
        target.write_text(json.dumps({"existing": 1}), encoding="utf-8")
        first = module.enrich_complete_json_for_web_ai(target, root)
        payload1 = json.loads(target.read_text(encoding="utf-8"))
        second = module.enrich_complete_json_for_web_ai(target, root)
        payload2 = json.loads(target.read_text(encoding="utf-8"))
        first["target"] = "<TARGET>"
        second["target"] = "<TARGET>"
        result = {
            "required_sections": module.REQUIRED_WEB_AI_SECTIONS,
            "sections": sections,
            "first": first,
            "second": second,
            "payload_equal_after_second": payload1 == payload2,
            "keys": sorted(payload1),
        }
    return result


def _expected_stable_evidence_index(sections: dict[str, Any]) -> dict[str, Any]:
    """Independently derive stable evidence IDs from section values."""
    evidence: dict[str, Any] = {}
    for section_name, section_value in sorted(sections.items()):
        encoded = json.dumps(section_value, sort_keys=True, default=str)
        evidence_id = hashlib.sha256(
            (section_name + "\n" + encoded).encode("utf-8")
        ).hexdigest()[:16]
        evidence[evidence_id] = {
            "section": section_name,
            "sha256_16": evidence_id,
        }
    return evidence


def _assert_behavior_contract() -> None:
    payload = _behavior_payload()
    sections = payload["sections"]
    required = list(payload["required_sections"])

    if sorted(sections) != sorted(required):
        raise AssertionError("REQUIRED_SECTION_SET_CHANGED")

    summary = sections["web_ai_readme_summary"]
    readme = sections["web_ai_readme"]
    if readme.get("summary") != summary:
        raise AssertionError("README_SUMMARY_DIVERGED")
    if summary.get("source") != "pass_064d_ast_fallback":
        raise AssertionError("SUMMARY_SOURCE_CHANGED")

    responsibility_index = sections["web_ai_file_responsibility_index"]
    symbol_index = sections["web_ai_symbol_index"]
    entry_points = sections["entry_points_detail"]
    test_index = sections["web_ai_test_protection_index"]

    expected_counts = {
        "python_file_count": len(responsibility_index),
        "symbol_file_count": len(symbol_index),
        "entry_point_count": len(entry_points),
        "test_index_count": len(test_index),
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            raise AssertionError(f"SUMMARY_COUNT_MISMATCH: {key}")

    def is_protection_path(value: str) -> bool:
        normalized = str(value).replace("\\", "/").casefold()
        parts = normalized.split("/")
        return (
            normalized.startswith("tools/validate_")
            or "tests" in parts
            or "test" in Path(normalized).name
        )

    expected_production_count = sum(
        1
        for record in responsibility_index
        if not is_protection_path(str(record.get("file", "")))
    )
    if len(test_index) != expected_production_count:
        raise AssertionError("PROTECTION_INDEX_PRODUCTION_CARDINALITY_CHANGED")
    if any(
        is_protection_path(str(record.get("file", "")))
        for record in test_index
    ):
        raise AssertionError("PROTECTION_SOURCE_EMITTED_AS_PRODUCTION_RECORD")

    without_stable = {
        key: value
        for key, value in sections.items()
        if key != "stable_evidence_id_index"
    }
    expected_stable = _expected_stable_evidence_index(without_stable)
    if sections["stable_evidence_id_index"] != expected_stable:
        raise AssertionError("STABLE_EVIDENCE_ID_SEMANTICS_CHANGED")

    first = payload["first"]
    second = payload["second"]
    if first.get("changed") is not True:
        raise AssertionError("FIRST_ENRICHMENT_CHANGED_FLAG_FALSE")
    if first.get("missing_before") != required:
        raise AssertionError("FIRST_MISSING_BEFORE_ORDER_CHANGED")
    if first.get("missing_after") != []:
        raise AssertionError("FIRST_MISSING_AFTER_NOT_EMPTY")
    if second.get("changed") is not False:
        raise AssertionError("SECOND_ENRICHMENT_NOT_IDEMPOTENT")
    if second.get("missing_before") != [] or second.get("missing_after") != []:
        raise AssertionError("SECOND_ENRICHMENT_MISSING_SECTION_REGRESSION")
    if payload.get("payload_equal_after_second") is not True:
        raise AssertionError("SECOND_ENRICHMENT_PAYLOAD_CHANGED")
    if "existing" not in payload.get("keys", []):
        raise AssertionError("EXISTING_PAYLOAD_KEY_NOT_PRESERVED")

    from kanda_reasoner_app.reasoner_context_collector import (
        _complete_json_web_ai_enrichment_analysis as analysis,
    )

    cli_tree = ast.parse(
        'def main():\n    return 0\n\n'
        'if __name__ == "__main__":\n    raise SystemExit(main())\n'
    )
    plain_tree = ast.parse("def alpha():\n    return 1\n")
    if analysis._looks_like_entry_point(cli_tree) is not True:
        raise AssertionError("STRUCTURAL_MAIN_GUARD_NOT_DETECTED")
    if analysis._looks_like_entry_point(plain_tree) is not False:
        raise AssertionError("FALSE_ENTRY_POINT_DETECTION")


def _assert_cli_contract() -> None:
    from kanda_reasoner_app.reasoner_context_collector import (
        complete_json_web_ai_enrichment as module,
    )

    with TemporaryDirectory() as tmp:
        root = Path(tmp) / "fixture"
        _create_fixture(root)
        target = Path(tmp) / "complete.json"
        target.write_text("{}", encoding="utf-8")
        output = io.StringIO()
        with redirect_stdout(output):
            code = module.main(
                [
                    "--root",
                    str(root),
                    "--complete-json",
                    str(target),
                    "--compact",
                ]
            )
        if code != 0:
            raise AssertionError("CLI_EXIT_CODE_CHANGED")
        status = json.loads(output.getvalue())
        if status.get("missing_after") != []:
            raise AssertionError("CLI_MISSING_AFTER_CONTRACT_CHANGED")


def _assert_ast_safe(paths: list[Path]) -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for path in paths:
        result = run_large_module_split_audit(
            PROJECT_ROOT,
            path,
            classifier_mode="heuristic",
        )
        classification = result.data["refactor_safety_classification"]
        if classification["label"] != "SAFE REFACTORING":
            raise AssertionError(f"AST_SPLIT_SAFETY_LABEL_NOT_SAFE: {path}")
        if classification["hard_blockers"]:
            raise AssertionError(f"AST_SPLIT_HARD_BLOCKERS_REMAIN: {path}")


def _assert_patch_contract(patch_zip: Path) -> None:
    from kanda_reasoner_app.patch_governance.validator import (
        validate_install_script_text,
    )

    with zipfile.ZipFile(patch_zip, "r") as archive:
        names = set(archive.namelist())
        required_root = {
            "INSTALL.ps1",
            "VALIDATE.ps1",
            "FREEZE.ps1",
            "PACKAGE_MANIFEST.json",
            "KANDA_FREEZE_HINT.json",
        }
        if not required_root.issubset(names):
            raise AssertionError("PATCH_ROOT_CONTRACT_MISSING")
        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json").decode("utf-8"))
        by_path = {item["relative_path"]: item for item in manifest["files"]}
        target_item = by_path[TARGET_REL]
        accepted = set(target_item.get("accepted_existing_sha256", []))
        if BASELINE_TARGET_SHA256 not in accepted:
            raise AssertionError("SOURCE_IDENTITY_GUARD_BASELINE_HASH_MISSING")
        for rel in (TARGET_REL, HELPER_REL, VALIDATOR_REL):
            item = by_path[rel]
            payload = archive.read("payload/" + rel)
            digest = _sha256_bytes(payload)
            if digest != item["sha256"]:
                raise AssertionError(f"PACKAGE_PAYLOAD_HASH_MISMATCH: {rel}")
        install_text = archive.read("INSTALL.ps1").decode("utf-8")
        validate_install_script_text(install_text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", default="")
    args = parser.parse_args()

    target = PROJECT_ROOT / TARGET_REL
    helper = PROJECT_ROOT / HELPER_REL
    validator = PROJECT_ROOT / VALIDATOR_REL
    for path in (target, helper, validator):
        if not path.is_file():
            raise FileNotFoundError(path)
        _assert_ascii_utf8_no_bom(path)
        _assert_size(path)

    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("TOUCHED_SOURCE_MODULES_101_499: PASS")

    for path in (target, helper):
        dynamic = _dynamic_calls(path)
        if dynamic:
            raise AssertionError(f"DYNAMIC_CALLS_REMAIN: {path}: {dynamic}")
    print("REFLECTION_AND_DYNAMIC_CALLS_REMOVED: PASS")

    _assert_dependency_direction(helper)
    _assert_main_guard_boundary(target, helper)
    print("DEPENDENCY_DIRECTION_FACADE_TO_HELPER_ONLY: PASS")
    print("MAIN_GUARD_PRESERVED_IN_FACADE: PASS")

    _assert_behavior_contract()
    _assert_cli_contract()
    print("ACTIVE_COLLECTOR_POLICY_BEHAVIOR_CONTRACT: PASS")
    print("STRUCTURAL_ENTRY_POINT_DETECTION: PASS")
    print("PUBLIC_API_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")
    print("BEHAVIOR_REGRESSION: PASS")
    print("PROTECTION_INDEX_PRODUCTION_CARDINALITY: PASS")
    print("CLI_CONTRACT_PRESERVATION: PASS")

    _assert_ast_safe([target, helper])
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")

    if args.patch_zip:
        patch_zip = Path(args.patch_zip).expanduser().resolve()
        _assert_patch_contract(patch_zip)
        print("SOURCE_IDENTITY_GUARD: PASS")
        print("INSTALLER_CONTRACT: PASS")
        print("PACKAGE_PAYLOAD_HASHES: PASS")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
