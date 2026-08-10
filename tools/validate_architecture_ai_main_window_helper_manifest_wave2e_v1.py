"""Validate complete AI main-window helper-manifest closure for wave 2E."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-ai-main-window-helper-manifest-wave2e-v1"
MANIFEST_REL = Path("kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help.json")
HELP_FOLDER_REL = Path("kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help")

EXPECTED_SOURCE_HASHES = {
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py": "a7deda2e9ad4e897d24e14356a1e94bcf04ff00b5b0bbae42db8c1654467c9de",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/local_ai_clipboard_actions.py": "a39992eca631a83f15e62a1d343bf063ec9db93420fc41c87842c1d688baed3b",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/signal_wiring.py": "936b39cb591bf82fb9d4625cb02a08008323ceddc0c031effe0cb21ac0117774",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_builder.py": "c1c0aff140dc730177998a89ffc8960e6159d05caad78d028c19877e16965036",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_theme.py": "c2cadfe2405c48e67675a43c715d2bcc22fb8136c24cd85654fe62dead6b2085"
}

REQUIRED_NEW_ENTRIES = {
    "ui_theme.py": {
        "stability": "stable",
        "exports": ["LOCAL_AI_THEME"],
        "depends_on": [],
        "consumed_by": ["ui_builder.py"],
    },
    "local_ai_clipboard_actions.py": {
        "stability": "stable",
        "exports": ["connect_local_ai_clipboard_actions"],
        "depends_on": [
            "kanda_reasoner_app.reasoner_engine.chat_clipboard_actions"
        ],
        "consumed_by": ["signal_wiring.py"],
    },
}


def require(condition: bool, code: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise RuntimeError(code)


def read_text(root: Path, relative: Path) -> str:
    """Read one governed UTF-8 file."""
    return (root / relative).read_text(encoding="utf-8-sig")


def literal_all(path: Path) -> list[str] | None:
    """Return one literal module __all__, or None when absent/nonliteral."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = (
            list(node.targets)
            if isinstance(node, ast.Assign)
            else [node.target]
        )
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in targets
        ):
            continue
        value = node.value
        if not isinstance(value, (ast.List, ast.Tuple)):
            return None
        result: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant):
                return None
            if not isinstance(item.value, str):
                return None
            result.append(item.value)
        return result
    return None


def validate_source_hashes(root: Path) -> None:
    """Prove the manifest-only patch did not change behavior sources."""
    for relative, expected in EXPECTED_SOURCE_HASHES.items():
        path = root / relative
        require(path.is_file(), "UNCHANGED_SOURCE_MISSING:" + relative)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(
            actual == expected,
            "UNCHANGED_SOURCE_HASH_DRIFT:" + relative,
        )
    print("AI MAIN WINDOW BEHAVIOR SOURCES UNCHANGED: PASS")


def validate_manifest_closure(root: Path) -> None:
    """Require exact closure across files, __all__, summary, and graph."""
    manifest_path = root / MANIFEST_REL
    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8-sig")
    )
    helpers = manifest.get("helpers")
    dependency_graph = manifest.get("dependency_graph")
    summary = manifest.get("summary")

    require(isinstance(helpers, dict), "HELPERS_SECTION_INVALID")
    require(
        isinstance(dependency_graph, dict),
        "DEPENDENCY_GRAPH_INVALID",
    )
    require(isinstance(summary, dict), "SUMMARY_SECTION_INVALID")

    help_folder = root / HELP_FOLDER_REL
    actual_files = sorted(
        path.name
        for path in help_folder.glob("*.py")
        if path.is_file()
    )
    declared_files = sorted(str(name) for name in helpers)

    require(
        declared_files == actual_files,
        "HELPER_FILE_MANIFEST_CLOSURE_MISMATCH",
    )
    require(
        sorted(str(name) for name in dependency_graph) == actual_files,
        "HELPER_DEPENDENCY_GRAPH_CLOSURE_MISMATCH",
    )

    public_count = 0
    internal_count = 0
    for helper_name in actual_files:
        source_all = literal_all(help_folder / helper_name)
        require(
            source_all is not None,
            "HELPER_LITERAL_ALL_MISSING:" + helper_name,
        )
        declared_exports = helpers[helper_name].get("exports")
        require(
            declared_exports == source_all,
            "HELPER_EXPORT_DRIFT:" + helper_name,
        )
        if source_all:
            public_count += 1
        else:
            internal_count += 1

    require(
        summary.get("total_helpers") == len(actual_files),
        "SUMMARY_TOTAL_HELPERS_DRIFT",
    )
    require(
        summary.get("public_helpers") == public_count,
        "SUMMARY_PUBLIC_HELPERS_DRIFT",
    )
    require(
        summary.get("internal_helpers") == internal_count,
        "SUMMARY_INTERNAL_HELPERS_DRIFT",
    )

    require(
        len(actual_files) == 19,
        "AI_MAIN_WINDOW_HELPER_COUNT_UNEXPECTED",
    )
    require(public_count == 17, "AI_MAIN_WINDOW_PUBLIC_COUNT_UNEXPECTED")
    require(internal_count == 2, "AI_MAIN_WINDOW_INTERNAL_COUNT_UNEXPECTED")

    for helper_name, expected in REQUIRED_NEW_ENTRIES.items():
        record = helpers.get(helper_name)
        require(
            isinstance(record, dict),
            "REQUIRED_HELPER_ENTRY_MISSING:" + helper_name,
        )
        for key, value in expected.items():
            require(
                record.get(key) == value,
                "REQUIRED_HELPER_ENTRY_DRIFT:"
                + helper_name
                + ":"
                + key,
            )
        require(
            dependency_graph.get(helper_name)
            == {
                "depends_on": expected["depends_on"],
                "consumed_by": expected["consumed_by"],
            },
            "REQUIRED_DEPENDENCY_GRAPH_DRIFT:" + helper_name,
        )

    require(
        "LOCAL_AI_THEME"
        in helpers["ui_theme.py"]["exports"],
        "LOCAL_AI_THEME_MANIFEST_EXPORT_MISSING",
    )
    require(
        "connect_local_ai_clipboard_actions"
        in helpers["local_ai_clipboard_actions.py"]["exports"],
        "LOCAL_AI_CLIPBOARD_MANIFEST_EXPORT_MISSING",
    )

    require(
        len(manifest_path.read_text(encoding="utf-8-sig").splitlines())
        <= 500,
        "AI_MAIN_WINDOW_MANIFEST_EXCEEDS_500_LINES",
    )
    require(
        len(Path(__file__).read_text(encoding="utf-8-sig").splitlines())
        <= 500,
        "WAVE2E_VALIDATOR_EXCEEDS_500_LINES",
    )

    print("AI MAIN WINDOW HELPER FILE CLOSURE: PASS")
    print("AI MAIN WINDOW HELPER EXPORT CLOSURE: PASS")
    print("AI MAIN WINDOW DEPENDENCY GRAPH CLOSURE: PASS")
    print("AI MAIN WINDOW HELPER SUMMARY COUNTS: PASS")
    print("UI THEME MANIFEST REGISTRATION: PASS")
    print("LOCAL AI CLIPBOARD MANIFEST REGISTRATION: PASS")
    print("WAVE2E JSON AND SIZE CONTRACT: PASS")


def run_command(
    root: Path,
    command: list[str],
    marker: str,
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    """Run one owned command and require one exact success marker."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        cwd=str(root),
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )
    output = completed.stdout or ""
    print(output, end="" if output.endswith("\n") else "\n")
    require(completed.returncode == 0, code + "_NONZERO_EXIT")
    require(marker in output, code + "_MARKER_MISSING")
    return output


def required_cli_flags(path: Path) -> set[str]:
    """Return required long-form argparse flags from one validator."""
    tree = ast.parse(
        path.read_text(encoding="utf-8-sig"),
        filename=str(path),
    )
    required: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "add_argument" or not node.args:
            continue
        first = node.args[0]
        if not isinstance(first, ast.Constant):
            continue
        if not isinstance(first.value, str):
            continue
        if not first.value.startswith("--"):
            continue
        is_required = any(
            keyword.arg == "required"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is True
            for keyword in node.keywords
        )
        if is_required:
            required.add(first.value)
    return required


def validate_inherited_cli_contracts(root: Path) -> None:
    """Require the packaged command flags to match inherited parsers."""
    paste_flags = required_cli_flags(root / Path(
        "tools/validate_local_web_ai_paste_send_state_repair_v1.py"
    ))
    layout_flags = required_cli_flags(root / Path(
        "tools/validate_local_ai_project_web_ai_layout_v1.py"
    ))

    require(
        paste_flags == {"--root"},
        "PASTE_SEND_VALIDATOR_CLI_CONTRACT_DRIFT",
    )
    require(
        layout_flags == {"--project-root"},
        "LAYOUT_VALIDATOR_CLI_CONTRACT_DRIFT",
    )

    source = Path(__file__).read_text(encoding="utf-8-sig")
    require(
        '"--root",\n            str(root),\n        ],\n'
        '        "VALIDATION OK: local-web-ai-paste-send-state-repair-v1"'
        in source,
        "PASTE_SEND_PACKAGED_FLAG_MISMATCH",
    )
    require(
        '"--project-root",\n            str(root),\n        ],\n'
        '        "VALIDATION OK: local-ai-project-web-ai-layout-v1"'
        in source,
        "LAYOUT_PACKAGED_FLAG_MISMATCH",
    )

    print("PASTE SEND VALIDATOR CLI CONTRACT: PASS")
    print("LOCAL AI LAYOUT VALIDATOR CLI CONTRACT: PASS")
    print("INHERITED VALIDATOR CLI CONTRACTS: PASS")


def validate_live_architecture(root: Path) -> None:
    """Require zero errors and absence of the owned manifest warning."""
    output = run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "kanda_reasoner_app"
                / "manage_architecture"
                / "manage_architecture.py"
            ),
            "--root",
            str(root),
            "--validate",
        ],
        "ARCHITECTURE VALIDATION SUMMARY",
        "ARCHITECTURE_VALIDATION",
    )
    require("Errors: 0" in output, "ARCHITECTURE_ERRORS_REMAIN")
    target = (
        "HELPER_MANIFEST_CONTRACT     "
        "kanda_reasoner_app/reasoner_engine/"
        "ai_reasoner_main_window_help.json"
    )
    require(
        target not in output,
        "AI_MAIN_WINDOW_HELPER_MANIFEST_WARNING_REMAINS",
    )
    print("WAVE2E AI MAIN WINDOW HELPER WARNING ABSENT: PASS")


def validate_inherited_contracts(root: Path) -> None:
    """Run manifest and unchanged behavior validators."""
    run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "kanda_reasoner_app"
                / "reasoner_engine"
                / "ai_reasoner_main_window_validate_manifests.py"
            ),
        ],
        "PASS - ",
        "AI_MAIN_WINDOW_MANIFEST_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "tools"
                / "validate_local_web_ai_paste_send_state_repair_v1.py"
            ),
            "--root",
            str(root),
        ],
        "VALIDATION OK: local-web-ai-paste-send-state-repair-v1",
        "LOCAL_WEB_AI_PASTE_SEND_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "tools"
                / "validate_local_ai_project_web_ai_layout_v1.py"
            ),
            "--project-root",
            str(root),
        ],
        "VALIDATION OK: local-ai-project-web-ai-layout-v1",
        "LOCAL_AI_LAYOUT_VALIDATOR",
    )


def main() -> int:
    """Run Wave 2E validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_source_hashes(root)
    validate_manifest_closure(root)
    validate_inherited_cli_contracts(root)

    if not args.static_only:
        validate_live_architecture(root)
        validate_inherited_contracts(root)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(exc.__class__.__name__ + ": " + str(exc))
        raise SystemExit(1)
