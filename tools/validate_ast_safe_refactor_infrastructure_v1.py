# project-path: tools/validate_ast_safe_refactor_infrastructure_v1.py
"""Focused validator for AST Safe Refactor Infrastructure v1.

The validator proves Box ownership, shielding, single-window preservation,
exact-source exchange identity, consumer/public-contract evidence, semantic
reflection detection, behavior comparison, fresh audits of new infrastructure
modules, and governed release-builder mechanics.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from kanda_reasoner_app.manage_architecture.ast_split_web_ai_gui import (
    build_ast_split_web_ai_risk_repair_wrapper,
)
from kanda_reasoner_app.manage_architecture.kanda_ast_safe_refactor_orchestrator import (
    build_preflight_evidence,
)
from kanda_reasoner_app.manage_architecture.kanda_ast_safe_refactor_routine import (
    build_exchange_preflight,
    run_project_ast_audit,
)
from kanda_reasoner_app.manage_architecture.kanda_refactor_probe_engine import (
    run_paired_probe_cases,
)
from kanda_reasoner_app.manage_architecture.kanda_refactor_project_index import (
    build_project_refactor_index,
)
from kanda_reasoner_app.manage_architecture.kanda_refactor_release_builder import (
    PayloadSpec,
    ReleaseDescriptor,
    build_governed_release_zip,
)
from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
    detect_semantic_dynamic_risks,
    evaluate_box_shielding,
)

__all__ = [
    "main",
]

FEATURE_ID = "ast-safe-refactor-infrastructure-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

INFRA_SOURCE_PATHS = [
    "kanda_reasoner_app/manage_architecture/kanda_ast_safe_refactor_orchestrator.py",
    "kanda_reasoner_app/manage_architecture/kanda_ast_safe_refactor_routine.py",
    "kanda_reasoner_app/manage_architecture/kanda_refactor_project_index.py",
    "kanda_reasoner_app/manage_architecture/kanda_refactor_semantic_safety.py",
    "kanda_reasoner_app/manage_architecture/kanda_refactor_probe_engine.py",
    "kanda_reasoner_app/manage_architecture/kanda_refactor_release_builder.py",
]

TOUCHED_PERMANENT_PATHS = [
    *INFRA_SOURCE_PATHS,
    "kanda_reasoner_app/manage_architecture/AST_SAFE_REFACTOR_ROUTINE.md",
    "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/web_ai_ast_split_risk_repair_protocol.md",
    "tools/validate_ast_safe_refactor_infrastructure_v1.py",
]

FORBIDDEN_PACKAGE_PATH_FRAGMENTS = (
    "large_file_refactor_planner/",
    "freeze_after_update/",
    "freeze_after_update_gui/",
    "architecture_review_subtabs.py",
    "large_module_split_audit_gui.py",
    "large_module_target_queue.py",
)


def _marker(name: str) -> None:
    """Print one stable validation marker."""
    print(name + ": PASS")


def _sha256(raw: bytes) -> str:
    """Return lowercase SHA-256 for exact package verification."""
    return hashlib.sha256(raw).hexdigest()


def _read(relative_path: str) -> str:
    """Read one permanent project text file as strict UTF-8."""
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8", errors="strict")


def _assert_line_law() -> None:
    """Require every touched permanent file to stay strictly within 101-499 lines."""
    violations: list[str] = []
    for relative_path in TOUCHED_PERMANENT_PATHS:
        path = PROJECT_ROOT / relative_path
        if not path.is_file():
            violations.append(relative_path + ":missing")
            continue
        line_count = len(path.read_text(encoding="utf-8", errors="strict").splitlines())
        if not 100 < line_count < 500:
            violations.append(relative_path + ":" + str(line_count))
    if violations:
        raise AssertionError("LINE_LAW_VIOLATIONS: " + ", ".join(violations))
    _marker("LINE_LAW_101_499_FITNESS")


def _assert_python_syntax_and_encoding() -> None:
    """Parse touched Python and reject BOM/non-ASCII corruption contracts."""
    for relative_path in [*INFRA_SOURCE_PATHS, "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py"]:
        path = PROJECT_ROOT / relative_path
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF8_BOM: " + relative_path)
        source = raw.decode("utf-8", errors="strict")
        ast.parse(source, filename=relative_path)
    _marker("PYTHON_SYNTAX")
    _marker("UTF8_NO_BOM")


def _assert_box_shielding() -> None:
    """Require new services to remain owned by Architecture Review without leaks."""
    source_map = {relative: _read(relative) for relative in INFRA_SOURCE_PATHS}
    result = evaluate_box_shielding(source_map)
    if not result["pass"]:
        raise AssertionError("BOX_SHIELDING: " + json.dumps(result["violations"], sort_keys=True))
    _marker("BOX_BOUNDARY_FITNESS")
    _marker("NO_LEAK_FITNESS")
    _marker("SHIELDING_LOGIC")


def _assert_single_window_and_wrapper_contract() -> None:
    """Protect the frozen one-window UI contract while proving enriched handoff."""
    wrapper_source = _read(
        "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py"
    )
    if "add_ast_split_web_ai_risk_repair_response_editor" in wrapper_source:
        raise AssertionError("SECOND_RESPONSE_EDITOR_REINTRODUCED")
    required_tokens = (
        "bind_ast_split_web_ai_single_output",
        "Send Web AI to make SAFE",
        "color: #FF8C00; font-weight: bold;",
        "AST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_BEGIN",
        "SOURCE_BYTE_LENGTH",
        "SOURCE_TEXT_ENDS_WITH_NEWLINE",
        "build_preflight_evidence_text",
    )
    for token in required_tokens:
        if token not in wrapper_source:
            raise AssertionError("WRAPPER_TOKEN_MISSING: " + token)
    _marker("SINGLE_AST_TEXT_WINDOW_PRESERVED")
    _marker("WEB_AI_PREFLIGHT_HANDOFF_INTEGRATION")


def _assert_exact_exchange_identity() -> None:
    """Round-trip exact source identity for newline and no-newline source variants."""
    audit_text = (
        "# Large Module AST Split Audit\n\n"
        "## Refactor safety classification\n\n"
        "Label: **RISK REFACTORING**\n\n"
        "Hard blockers:\n- Dynamic or reflection calls were detected.\n"
    )
    for source_text in ('print("hello")\n', 'print("hello")'):
        wrapper = build_ast_split_web_ai_risk_repair_wrapper(
            prompt_text="PROMPT",
            target_relative_path="pkg/target.py",
            source_text=source_text,
            audit_text=audit_text,
            safety_label="RISK REFACTORING",
            preflight_evidence_text='{"schema_version":"1.0"}',
        )
        preflight = build_exchange_preflight(wrapper)
        if not preflight["source_identity_match"]:
            raise AssertionError("SOURCE_IDENTITY_MISMATCH")
        if not preflight["source_byte_length_match"]:
            raise AssertionError("SOURCE_BYTE_LENGTH_MISMATCH")
        if not preflight["preflight_evidence_valid_json"]:
            raise AssertionError("PREFLIGHT_JSON_NOT_PARSED")
    _marker("SOURCE_IDENTITY_FITNESS")
    _marker("EXACT_SOURCE_BYTE_LENGTH_CONTRACT")


def _assert_semantic_detector() -> None:
    """Prove direct, imported-alias, and assignment-alias detection behavior."""
    source = (
        "from builtins import getattr as ga\n"
        "fn = ga\n"
        "def read_value(obj, name):\n"
        "    return fn(obj, name)\n"
    )
    findings = detect_semantic_dynamic_risks(source, "semantic_fixture.py")
    if not any(item["semantic_target"] == "builtins.getattr" for item in findings):
        raise AssertionError("ALIASED_GETATTR_NOT_DETECTED")
    safe_source = "def add(a, b):\n    return a + b\n"
    if detect_semantic_dynamic_risks(safe_source, "safe_fixture.py"):
        raise AssertionError("SEMANTIC_DETECTOR_FALSE_POSITIVE")
    _marker("SEMANTIC_REFLECTION_DETECTION")


def _build_project_fixture(root: Path) -> tuple[str, str]:
    """Create deterministic source and consumer files for project-index validation."""
    package = root / "sample_pkg"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("\n", encoding="utf-8")
    target_relative = "sample_pkg/target.py"
    source = (
        '__all__ = ["evaluate"]\n\n'
        "def evaluate(value: int = 1) -> int:\n"
        "    return value + 1\n"
    )
    (root / target_relative).write_text(source, encoding="utf-8", newline="\n")
    (package / "consumer.py").write_text(
        "from sample_pkg.target import evaluate\n"
        "RESULT = evaluate(2)\n",
        encoding="utf-8",
        newline="\n",
    )
    return target_relative, source


def _assert_project_index_and_orchestrator() -> None:
    """Prove consumer discovery, public contract capture, and bounded AI evidence."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        target_relative, source = _build_project_fixture(root)
        index = build_project_refactor_index(root, target_relative)
        if index["consumers"]["record_count"] != 1:
            raise AssertionError("CONSUMER_DISCOVERY_COUNT")
        all_state = index["public_contract"]["all_state"]
        if all_state != {"mode": "EXPLICIT_LITERAL", "symbols": ["evaluate"]}:
            raise AssertionError("PUBLIC_ALL_STATE")
        audit_text = (
            "# Large Module AST Split Audit\n\n"
            "## Refactor safety classification\n\n"
            "Label: **RISK REFACTORING**\n\n"
            "Hard blockers:\n- Dynamic or reflection calls were detected.\n"
        )
        evidence = build_preflight_evidence(
            root,
            target_relative_path=target_relative,
            source_text=source,
            audit_text=audit_text,
        )
        if evidence["ownership"]["subtab"] != "Large Module AST Split Audit":
            raise AssertionError("OWNERSHIP_SUBTAB")
        if evidence["architecture_review"]["architecture_authority"] != "web_ai_reasoning_plus_human_strategic_confirmation":
            raise AssertionError("ARCHITECTURE_AUTHORITY")
        if evidence["line_law"]["allowed_physical_lines"] != "101-499":
            raise AssertionError("LINE_LAW_EVIDENCE")
    _marker("CONSUMER_COMPATIBILITY_EVIDENCE")
    _marker("PUBLIC_CONTRACT_EVIDENCE")
    _marker("WEB_AI_PREFLIGHT_EVIDENCE")


def _assert_probe_engine() -> None:
    """Prove exact behavior equivalence and deliberate mismatch detection."""
    same = run_paired_probe_cases(
        {"value": lambda: {"accepted": True, "status": "safe"}},
        {"value": lambda: {"accepted": True, "status": "safe"}},
        profile_name="CONTRACT_MODULE",
    )
    if not same["pass"]:
        raise AssertionError("EQUIVALENT_PROBES_FAILED")
    different = run_paired_probe_cases(
        {"value": lambda: {"accepted": True}},
        {"value": lambda: {"accepted": False}},
        profile_name="CONTRACT_MODULE",
    )
    if different["pass"]:
        raise AssertionError("NON_EQUIVALENT_PROBES_PASSED")
    _marker("BEHAVIOR_EQUIVALENCE_FITNESS")


def _assert_release_builder() -> None:
    """Build a governed ZIP fixture and inspect required delivery contracts."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        payload_root = root / "payload_root"
        payload_file = payload_root / "pkg" / "new_module.py"
        payload_file.parent.mkdir(parents=True)
        payload_file.write_text(
            '"""Fixture payload."""\n' + "\n".join(
                "VALUE_{0} = {0}".format(index) for index in range(105)
            ) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        descriptor = ReleaseDescriptor(
            feature_id="fixture-release-v1",
            feature_title="Fixture Release",
            zip_name="fixture_release.zip",
            payloads=(PayloadSpec("pkg/new_module.py", new_file=True),),
            validator_relative_path="tools/fixture_validator.py",
            required_markers=("FIXTURE: PASS",),
            protected_paths=("pkg/new_module.py",),
            do_not_regress=("no cross-box leak",),
        )
        output = build_governed_release_zip(
            descriptor,
            payload_root=payload_root,
            output_path=root / descriptor.zip_name,
        )
        with zipfile.ZipFile(output) as archive:
            names = set(archive.namelist())
            required = {
                "PACKAGE_MANIFEST.json",
                "INSTALL.ps1",
                "VALIDATE.ps1",
                "FREEZE.ps1",
                "KANDA_FREEZE_HINT.json",
                "payload/pkg/new_module.py",
            }
            if not required.issubset(names):
                raise AssertionError("RELEASE_BUILDER_MISSING_FILES")
            install = archive.read("INSTALL.ps1").decode("utf-8")
            if "SOURCE FRESHNESS GUARD: PASS" not in install:
                raise AssertionError("RELEASE_BUILDER_FRESHNESS_GUARD")
            freeze = archive.read("FREEZE.ps1").decode("utf-8")
            if "Confirm and Write" not in freeze:
                raise AssertionError("RELEASE_BUILDER_FREEZE_BOUNDARY")
    _marker("DESCRIPTOR_DRIVEN_RELEASE_BUILDER")
    _marker("FREEZE_PREPARATION_ONLY_BOUNDARY")


def _assert_prompt_contract() -> None:
    """Require evidence-aware KPR protocol while preserving single-window return."""
    prompt = _read(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/web_ai_ast_split_risk_repair_protocol.md"
    )
    required = (
        "AST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_BEGIN",
        "Human/AI authority boundary",
        "101-499",
        "CONSUMER_COMPATIBILITY_FITNESS: PASS",
        "DEPENDENCY_DIRECTION_FITNESS: PASS",
        "BEHAVIOR_EQUIVALENCE_FITNESS: PASS",
        "Required single-window paste output",
        "one text window only",
    )
    for token in required:
        if token not in prompt:
            raise AssertionError("PROMPT_CONTRACT_MISSING: " + token)
    if "KANDA_AST_SPLIT_RISK_REPAIR_RESPONSE_BEGIN" in prompt:
        raise AssertionError("PARALLEL_JSON_RESPONSE_REINTRODUCED")
    _marker("KPR_06_003_EVIDENCE_AWARE_PROTOCOL")
    _marker("SINGLE_WINDOW_MARKDOWN_RETURN_CONTRACT")


def _assert_fresh_infrastructure_audits() -> None:
    """Run fresh authoritative AST audits on every new permanent Python service."""
    for relative_path in INFRA_SOURCE_PATHS:
        result = run_project_ast_audit(PROJECT_ROOT, relative_path)
        if result["label"] != "SAFE REFACTORING":
            raise AssertionError("INFRA_AST_NOT_SAFE: " + relative_path)
        if result["hard_blockers"]:
            raise AssertionError("INFRA_AST_HARD_BLOCKER: " + relative_path)
    _marker("FRESH_INFRASTRUCTURE_AST_FITNESS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")


def _assert_package_contract(patch_zip: Path | None) -> None:
    """Verify package manifest hashes and forbid cross-box payload mutation."""
    if patch_zip is None:
        return
    with zipfile.ZipFile(patch_zip) as archive:
        names = set(archive.namelist())
        if "PACKAGE_MANIFEST.json" not in names:
            raise AssertionError("PACKAGE_MANIFEST_MISSING")
        if "KANDA_FREEZE_HINT.json" not in names:
            raise AssertionError("ROOT_FREEZE_HINT_MISSING")
        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json"))
        for item in manifest.get("files", []):
            relative_path = str(item["relative_path"]).replace("\\", "/")
            for forbidden in FORBIDDEN_PACKAGE_PATH_FRAGMENTS:
                if forbidden in relative_path:
                    raise AssertionError("FORBIDDEN_PACKAGE_PATH: " + relative_path)
            payload_name = "payload/" + relative_path
            if payload_name not in names:
                raise AssertionError("PAYLOAD_MISSING: " + relative_path)
            digest = _sha256(archive.read(payload_name))
            if digest != str(item["sha256"]).lower():
                raise AssertionError("PAYLOAD_HASH_MISMATCH: " + relative_path)
    _marker("PACKAGE_PAYLOAD_HASHES")
    _marker("NO_QUEUE_PLANNER_WORKBENCH_AQR_FREEZE_MUTATION")


def main() -> int:
    """Run complete focused validation and print stable evidence markers."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", default="")
    args = parser.parse_args()
    patch_zip = Path(args.patch_zip).expanduser().resolve() if args.patch_zip else None

    _assert_package_contract(patch_zip)
    _assert_line_law()
    _assert_python_syntax_and_encoding()
    _assert_box_shielding()
    _assert_single_window_and_wrapper_contract()
    _assert_exact_exchange_identity()
    _assert_semantic_detector()
    _assert_project_index_and_orchestrator()
    _assert_probe_engine()
    _assert_release_builder()
    _assert_prompt_contract()
    _assert_fresh_infrastructure_audits()

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
