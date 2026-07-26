# project-path: tools/validate_safe_refactor_how_to_button_v1.py
"""Validate Safe Refactor How To prompt, routing, support bundle, and GUI button."""
from __future__ import annotations

import ast
import csv
import json
import py_compile
import sys
from pathlib import Path
from zipfile import ZipFile

__all__ = [
    "main",
]

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FEATURE_ID = "safe-refactor-how-to-button-v1"
PROMPT_CODE = "KPR-06-004"
PROMPT_ID = "safe_refactor_how_to"

PROMPT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/safe_refactor_how_to.md"
)
META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/safe_refactor_how_to.meta.json"
)
HELPER_REL = Path(
    "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py"
)
ROUTINE_GUIDE_REL = Path(
    "kanda_reasoner_app/manage_architecture/AST_SAFE_REFACTOR_ROUTINE.md"
)
ROUTINE_IMPL_REL = Path(
    "kanda_reasoner_app/manage_architecture/kanda_ast_safe_refactor_routine.py"
)
EXAMPLE_REL = Path(
    "kanda_reasoner_app/manage_architecture/"
    "runtime_activation_refactor_routine_report_example.json"
)
ROUTING_SYSTEM_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "02_prompt_routing_and_indexing/kanda_routing_system_canon.md"
)
NAV_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "02_prompt_routing_and_indexing/prompt_navigation_index.md"
)
FOLDER_CARD_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/_FOLDER_ASSIMILATION.md"
)
GROUP_MD_REL = Path(
    "kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md"
)
GROUP_JSON_REL = Path(
    "kanda_prompt_workspace/prompt_library/ROUTING/group_assimilation_index.json"
)
ROUTE_CSV_REL = Path(
    "kanda_prompt_workspace/prompt_library/ROUTING/prompt_route_coverage_table.csv"
)
CORE_PROTOCOL_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
)
BRIDGE_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
)


def _read(relative: Path) -> str:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit("VALIDATION ERROR: missing " + str(relative))
    return path.read_text(encoding="utf-8")


def _require(text: str, token: str, label: str) -> None:
    if token not in text:
        raise SystemExit("VALIDATION ERROR: " + label + " missing " + token)


def _validate_prompt_and_metadata() -> None:
    prompt = _read(PROMPT_REL)
    required = (
        "# Safe Refactor How To",
        PROMPT_CODE,
        "Version: 2.0.0",
        "user-facing KANDA safe-refactor refresher",
        "Specialist dispatch",
        "KPR-03-001",
        "KPR-06-003",
        "KPR-06-005",
        "KPR-06-007",
        "ideal at 400 physical lines or fewer",
        "hard maximum at 500 physical lines or fewer",
        "There is no universal 101-line minimum",
        "Post-refactor verification route",
        "Appended support-artifact roles",
        "non-authoritative historical evidence-shape example",
        "Preview remains read-only",
        "explicit human Confirm and Write",
    )
    for token in required:
        _require(prompt, token, "prompt")
    forbidden = (
        "strictly more than 100 physical lines",
        "101 through 499 physical lines inclusive",
        "Drive-root staging law",
        "Governed release construction",
        "Required delivery response",
        "LINE_LAW_101_499_FITNESS",
        "KANDA_ERROR_LESSON_JSON_BEGIN",
    )
    for token in forbidden:
        if token in prompt:
            raise SystemExit("VALIDATION ERROR: retired refresher doctrine remains: " + token)
    line_count = len(prompt.splitlines())
    if not 100 <= line_count <= 220:
        raise SystemExit(
            "VALIDATION ERROR: Safe Refactor dispatcher size drift: "
            + str(line_count)
        )

    meta = json.loads(_read(META_REL))
    if meta.get("prompt_code") != PROMPT_CODE:
        raise SystemExit("VALIDATION ERROR: prompt code mismatch")
    if meta.get("prompt_id") != PROMPT_ID:
        raise SystemExit("VALIDATION ERROR: prompt id mismatch")
    if meta.get("version") != "2.0.0":
        raise SystemExit("VALIDATION ERROR: prompt version mismatch")
    if meta.get("status") != "active" or meta.get("load_type") != "routed":
        raise SystemExit("VALIDATION ERROR: prompt lifecycle mismatch")
    if meta.get("source_stage") != "prompt-audit-wave6b-class06-consolidation-retirements-v1":
        raise SystemExit("VALIDATION ERROR: prompt provenance mismatch")
    support = meta.get("support_artifacts", [])
    expected = [
        ROUTINE_GUIDE_REL.as_posix(),
        ROUTINE_IMPL_REL.as_posix(),
        EXAMPLE_REL.as_posix(),
    ]
    if support != expected:
        raise SystemExit("VALIDATION ERROR: support artifact metadata mismatch")


def _validate_support_artifacts() -> None:
    guide = _read(ROUTINE_GUIDE_REL)
    implementation = _read(ROUTINE_IMPL_REL)
    example = json.loads(_read(EXAMPLE_REL))
    if len(guide.splitlines()) < 101 or len(guide.splitlines()) > 499:
        raise SystemExit("VALIDATION ERROR: canonical routine guide line law")
    if len(implementation.splitlines()) < 101 or len(implementation.splitlines()) > 499:
        raise SystemExit("VALIDATION ERROR: canonical routine implementation line law")
    example_lines = len(_read(EXAMPLE_REL).splitlines())
    if not 101 <= example_lines <= 499:
        raise SystemExit("VALIDATION ERROR: worked example line law")
    if example.get("example_status") != "NON_AUTHORITATIVE_HISTORICAL_WORKED_EXAMPLE":
        raise SystemExit("VALIDATION ERROR: worked example authority label missing")
    if "report" not in example or not isinstance(example["report"], dict):
        raise SystemExit("VALIDATION ERROR: worked example report payload missing")
    for deprecated_name in (
        "0044a AST_SAFE_REFACTOR_ROUTINE.md",
        "0044b kanda_ast_safe_refactor_routine.py",
        "0044c runtime_activation_refactor_routine_report.json",
    ):
        if (ROOT / deprecated_name).exists():
            raise SystemExit("VALIDATION ERROR: deprecated upload copied into project: " + deprecated_name)


def _validate_routing() -> None:
    routing_system = _read(ROUTING_SYSTEM_REL)
    _require(routing_system, "KPR-02-002", str(ROUTING_SYSTEM_REL))
    _require(routing_system, "machine-readable route data", str(ROUTING_SYSTEM_REL))

    for relative in (
        NAV_REL,
        FOLDER_CARD_REL,
        CORE_PROTOCOL_REL,
        BRIDGE_REL,
    ):
        text = _read(relative)
        _require(text, PROMPT_ID, str(relative))
        _require(text, PROMPT_CODE, str(relative))

    group_md = _read(GROUP_MD_REL)
    _require(
        group_md,
        "| 06_refactor_and_architecture_hardening | 8 |",
        "group assimilation markdown",
    )
    group = json.loads(_read(GROUP_JSON_REL))
    item = next(
        entry
        for entry in group["groups"]
        if entry["group_id"] == "06_refactor_and_architecture_hardening"
    )
    if item.get("prompt_count") != len(item.get("main_prompts", [])) or item.get("prompt_count") != 8:
        raise SystemExit("VALIDATION ERROR: group 06 prompt count must be 8")
    if "safe_refactor_how_to.md" not in item.get("main_prompts", []):
        raise SystemExit("VALIDATION ERROR: Safe Refactor prompt missing from group index")

    rows = list(csv.reader((ROOT / ROUTE_CSV_REL).open(encoding="utf-8", newline="")))
    row = next((entry for entry in rows if entry and entry[0] == PROMPT_ID), None)
    if row is None:
        raise SystemExit("VALIDATION ERROR: route coverage row missing")
    if "Safe Refactor How To" not in row[4]:
        raise SystemExit("VALIDATION ERROR: route coverage trigger missing")


def _validate_gui_source() -> None:
    helper = _read(HELPER_REL)
    ast.parse(helper)
    py_compile.compile(str(ROOT / HELPER_REL), doraise=True)
    line_count = len(helper.splitlines())
    if not 101 <= line_count <= 499:
        raise SystemExit("VALIDATION ERROR: GUI helper line law violation")

    send_token = 'QtWidgets.QPushButton("Send Web AI to make SAFE")'
    howto_token = 'QtWidgets.QPushButton("Safe Refactor How To")'
    send_add = "action_row.addWidget(button)"
    howto_add = "action_row.addWidget(how_to_button)"
    if not (
        helper.index(send_token)
        < helper.index(send_add)
        < helper.index(howto_token)
        < helper.index(howto_add)
    ):
        raise SystemExit("VALIDATION ERROR: Safe Refactor button is not after Send Web AI")

    howto_pos = helper.index(howto_token)
    howto_block = helper[howto_pos : howto_pos + 1200]
    _require(
        howto_block,
        'how_to_button.setStyleSheet("color: #FF8C00; font-weight: bold;")',
        "Safe Refactor button style",
    )
    if "background-color" in howto_block:
        raise SystemExit("VALIDATION ERROR: Safe Refactor button must inherit background")

    for token in (
        "copy_safe_refactor_how_to_bundle",
        "build_safe_refactor_how_to_bundle",
        "SAFE_REFACTOR_HOW_TO_SUPPORT_BUNDLE_BEGIN",
        "CURRENT_CANONICAL_ROUTINE_GUIDE",
        "CURRENT_CANONICAL_ROUTINE_IMPLEMENTATION",
        "NON_AUTHORITATIVE_WORKED_REPORT_EXAMPLE",
    ):
        _require(helper, token, "GUI helper")

    forbidden = (
        "large_file_refactor_planner",
        "large_file_refactor_workbench",
        "advanced_quality_review",
        "freeze_after_update",
    )
    import_nodes = [
        node
        for node in ast.walk(ast.parse(helper))
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    import_text = "\n".join(ast.unparse(node) for node in import_nodes)
    for token in forbidden:
        if token in import_text:
            raise SystemExit("VALIDATION ERROR: cross-box import leak: " + token)

    if "QPlainTextEdit(" in howto_block or "QTextEdit(" in howto_block:
        raise SystemExit("VALIDATION ERROR: Safe Refactor button created a second editor")
    if "window._large_module_targets" in howto_block:
        raise SystemExit("VALIDATION ERROR: Safe Refactor button mutates target queue")


def _validate_bundle_builder() -> None:
    from kanda_reasoner_app.manage_architecture.ast_split_web_ai_gui import (
        build_safe_refactor_how_to_bundle,
    )

    prompt = _read(PROMPT_REL)
    support = [
        (
            "CURRENT_CANONICAL_ROUTINE_GUIDE",
            "Current canonical process guide; use as active support context.",
            ROUTINE_GUIDE_REL.as_posix(),
            _read(ROUTINE_GUIDE_REL),
        ),
        (
            "CURRENT_CANONICAL_ROUTINE_IMPLEMENTATION",
            "Current canonical read-only helper implementation; do not treat as a source writer.",
            ROUTINE_IMPL_REL.as_posix(),
            _read(ROUTINE_IMPL_REL),
        ),
        (
            "NON_AUTHORITATIVE_WORKED_REPORT_EXAMPLE",
            "Historical evidence-shape example only; never reuse its paths, hashes, or audit truth.",
            EXAMPLE_REL.as_posix(),
            _read(EXAMPLE_REL),
        ),
    ]
    bundle = build_safe_refactor_how_to_bundle(
        prompt_text=prompt,
        support_artifacts=support,
    )
    if not bundle.startswith(prompt.rstrip()):
        raise SystemExit("VALIDATION ERROR: clipboard bundle does not start with canonical prompt")
    if bundle.count("SAFE_REFACTOR_SUPPORT_ARTIFACT_BEGIN") != 3:
        raise SystemExit("VALIDATION ERROR: clipboard bundle must contain three support artifacts")
    if bundle.count("SAFE_REFACTOR_SUPPORT_ARTIFACT_END") != 3:
        raise SystemExit("VALIDATION ERROR: clipboard bundle support end-marker count mismatch")
    for name, _role, path, content in support:
        _require(bundle, "NAME: " + name, "clipboard bundle")
        _require(bundle, "RELATIVE_PATH: " + path, "clipboard bundle")
        _require(bundle, content[:180], "clipboard bundle content")
    _require(bundle, "SAFE_REFACTOR_HOW_TO_SUPPORT_BUNDLE_END", "clipboard bundle")


def _validate_patch_zip(patch_zip: Path | None) -> None:
    if patch_zip is None:
        return
    if not patch_zip.is_file():
        raise SystemExit("VALIDATION ERROR: patch ZIP missing: " + str(patch_zip))
    with ZipFile(patch_zip) as archive:
        names = set(archive.namelist())
        required = {
            "PACKAGE_MANIFEST.json",
            "KANDA_FREEZE_HINT.json",
            "INSTALL.ps1",
            "VALIDATE.ps1",
            "FREEZE.ps1",
            "payload/" + PROMPT_REL.as_posix(),
            "payload/" + META_REL.as_posix(),
            "payload/" + HELPER_REL.as_posix(),
            "payload/" + EXAMPLE_REL.as_posix(),
        }
        missing = sorted(required - names)
        if missing:
            raise SystemExit("VALIDATION ERROR: patch ZIP missing: " + ", ".join(missing))
        for forbidden in (
            "0044a AST_SAFE_REFACTOR_ROUTINE.md",
            "0044b kanda_ast_safe_refactor_routine.py",
            "0044c runtime_activation_refactor_routine_report.json",
        ):
            if any(name.endswith(forbidden) for name in names):
                raise SystemExit("VALIDATION ERROR: deprecated upload packaged: " + forbidden)


def main() -> int:
    patch_zip = None
    if "--patch-zip" in sys.argv:
        index = sys.argv.index("--patch-zip")
        try:
            patch_zip = Path(sys.argv[index + 1]).resolve()
        except IndexError as exc:
            raise SystemExit("VALIDATION ERROR: --patch-zip requires a value") from exc

    _validate_prompt_and_metadata()
    _validate_support_artifacts()
    _validate_routing()
    _validate_gui_source()
    _validate_bundle_builder()
    _validate_patch_zip(patch_zip)

    print("SAFE_REFACTOR_HOW_TO_PROMPT: PASS")
    print("SAFE_REFACTOR_HOW_TO_ROUTER_REGISTRATION: PASS")
    print("SAFE_REFACTOR_HOW_TO_BUTTON_POSITION: PASS")
    print("SAFE_REFACTOR_HOW_TO_BUTTON_ORANGE_BOLD_TEXT_ONLY: PASS")
    print("SAFE_REFACTOR_HOW_TO_CURRENT_CANONICAL_SUPPORT: PASS")
    print("SAFE_REFACTOR_HOW_TO_EXAMPLE_NON_AUTHORITATIVE: PASS")
    print("SAFE_REFACTOR_HOW_TO_THREE_ARTIFACT_BUNDLE: PASS")
    print("SAFE_REFACTOR_HOW_TO_NO_CROSS_BOX_IMPORT_LEAK: PASS")
    print("SAFE_REFACTOR_HOW_TO_SINGLE_WINDOW_PRESERVED: PASS")
    print("SAFE_REFACTOR_HOW_TO_QUEUE_UNCHANGED: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
