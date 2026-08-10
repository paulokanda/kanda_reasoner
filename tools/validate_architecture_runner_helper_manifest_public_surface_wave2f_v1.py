"""Validate runner helper manifest/public-surface closure for wave 2F."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-runner-helper-manifest-public-surface-wave2f-v1"
MANIFEST_REL = Path("kanda_reasoner_app/reasoner_tools_shell/runner_help.json")
HELP_FOLDER_REL = Path("kanda_reasoner_app/reasoner_tools_shell/runner_help")
PNG_REL = HELP_FOLDER_REL / "png_reuse_cancel_controls_private_impl.py"

ADDED_HELPERS = {
    "answer_validate_freeze_memorize_button_private_impl.py",
    "bridge_metadata_classification.py",
    "png_reuse_cancel_controls_private_impl.py",
    "project_tool_boundary_prompt_button_private_impl.py",
}

EXPECTED_PNG_ALL = [
    "PNG_REUSE_PROMPT",
    "install_controls",
    "update_cancel_enabled",
    "cancel_run",
    "consume_cancel_on_finish",
]

EXPECTED_ADDED_RECORDS = {
    "answer_validate_freeze_memorize_button_private_impl.py": {
        "purpose": "Stable clipboard owner for the complete Answer, Validate, Freeze, and Error Memory routine.",
        "reason": "Public helper surface consumed by the Show Project window controls.",
        "stability": "stable",
        "exports": [
            "build_answer_validate_freeze_memorize_wrapper",
            "copy_answer_validate_freeze_memorize_to_clipboard",
        ],
        "depends_on": [],
        "consumed_by": ["window_methods_private_impl.py"],
    },
    "bridge_metadata_classification.py": {
        "purpose": "Stable bridge metadata classification helpers for complete bridge-list generation.",
        "reason": "Public helper surface consumed by the complete bridge-list owner.",
        "stability": "stable",
        "exports": [
            "bridge_display_name",
            "is_active_on_demand_bridge",
            "prompt_front_matter",
            "startup_source_records",
        ],
        "depends_on": [],
        "consumed_by": ["complete_bridge_list_private_impl.py"],
    },
    "png_reuse_cancel_controls_private_impl.py": {
        "purpose": "Stable PNG reuse prompt and cancellation controls for Show Project workflows.",
        "reason": "Public helper surface shared by UI construction and prompt-file process owners.",
        "stability": "stable",
        "exports": EXPECTED_PNG_ALL,
        "depends_on": [],
        "consumed_by": [
            "window_methods_private_impl.py",
            "window_process_private_impl.py",
            "zip_json_files_process_private_impl.py",
        ],
    },
    "project_tool_boundary_prompt_button_private_impl.py": {
        "purpose": "Stable Show Project clipboard control for the canonical Tool and Project boundary prompt.",
        "reason": "Public helper surface installed through the runner-help package initializer.",
        "stability": "stable",
        "exports": [
            "build_project_tool_boundary_wrapper",
            "copy_project_tool_boundary_to_clipboard",
            "install_control",
        ],
        "depends_on": [],
        "consumed_by": ["__init__.py"],
    },
}

BASELINE_EXISTING_HELPERS_SHA256 = (
    "4b8c8ed54662e35d9b63fdcf3408d9a691833657c38772802578e69d1b6ed571"
)
BASELINE_MANIFEST_METADATA_SHA256 = (
    "ebafa495d98b94adfbd5e883088181f148bbd37e01305e9e5eb2303113302c3f"
)
INSTALLED_PNG_SOURCE_SHA256 = "0f874cd2f091041f46cdb7335997eadbf3cd5ed881c6460b952e8f492641430a"
BASELINE_PNG_SOURCE_SHA256 = "9d8edab347f9985056a3b10306610c15637f4a00ad50f2b6b6a0e08c5b774595"
PNG_PUBLIC_SURFACE_BLOCK = """__all__ = [
    "PNG_REUSE_PROMPT",
    "install_controls",
    "update_cancel_enabled",
    "cancel_run",
    "consume_cancel_on_finish",
]

"""

UNCHANGED_SOURCE_HASHES = {
    "answer_validate_freeze_memorize_button_private_impl.py": "1fc436e1253d69b8c1f2668f9d85a15833d3c57006450199c04a1f30fa1799e1",
    "bridge_metadata_classification.py": "03da77a96f77ffa5006882cca22351f1179d1d0c8984c7e509ccf51c8ffaed06",
    "project_tool_boundary_prompt_button_private_impl.py": "f2b4d2e23d160d9ca82f6fe63c90b02ee7403335bbc564951a757eb36758b261",
    "__init__.py": "eeca77dc23b22a119c55a40f86c7c22899b23df4e1915c0d2506d8f44bb7d422",
    "window_methods_private_impl.py": "ca506993434e0fa1093ee6426db2c7832f9ea3e0bd142fa81adf685fcbcdb13f",
    "window_process_private_impl.py": "56102bc52aa41313d3319df277ebbc7ba6edeccefc2840bd3172599aa7af28c5",
    "zip_json_files_process_private_impl.py": "dabbdc67269d5e8e6de86f11caff265d9e48e39bcd78c6646dac838db9ca9a7e",
    "complete_bridge_list_private_impl.py": "37d289782f2374f19d259d47b23358007225f77a092f02411c01e0e9c0e86710",
    "show_project_backup_private_impl.py": "8384f55184f04aa4e6ade24017a20e993b89101a297d1ff36095e882a1935f8f",
    "show_project_backup_service.py": "2c14acbd327eda51a49f211af05133f320c5512fd3a89a9e39a448a49b9c33b1",
}

def require(condition: bool, code: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise RuntimeError(code)

def stable_json_sha256(value: object) -> str:
    """Hash one JSON-like value deterministically."""
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def assignment_targets(node: ast.Assign | ast.AnnAssign) -> list[ast.expr]:
    """Return assignment targets for Assign and AnnAssign."""
    if isinstance(node, ast.Assign):
        return list(node.targets)
    return [node.target]

def is_all_assignment(node: ast.stmt) -> bool:
    """Return whether one statement assigns __all__."""
    if not isinstance(node, (ast.Assign, ast.AnnAssign)):
        return False
    return any(
        isinstance(target, ast.Name) and target.id == "__all__"
        for target in assignment_targets(node)
    )

def literal_all(path: Path) -> list[str] | None:
    """Return a literal module __all__, or None when absent/nonliteral."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    for node in tree.body:
        if not is_all_assignment(node):
            continue
        value = node.value
        if not isinstance(value, (ast.List, ast.Tuple)):
            return None
        result: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                return None
            result.append(item.value)
        return result
    return None

def public_top_level_names(path: Path) -> set[str]:
    """Return public definitions and assignments, excluding imports."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.add(node.name)
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            for target in assignment_targets(node):
                if isinstance(target, ast.Name):
                    name = target.id
                    if name != "__all__" and not name.startswith("_"):
                        names.add(name)
    return names

def reconstructed_png_baseline_sha256(path: Path) -> str:
    """Hash pre-patch source after removing only the canonical __all__."""
    source = path.read_text(encoding="utf-8-sig")
    require(source.count(PNG_PUBLIC_SURFACE_BLOCK) == 1, "PNG_PUBLIC_SURFACE_BLOCK_COUNT_INVALID")
    return hashlib.sha256(source.replace(PNG_PUBLIC_SURFACE_BLOCK, "", 1).encode("utf-8")).hexdigest()

def validate_manifest(root: Path) -> None:
    """Validate complete helper-file and public-export closure."""
    manifest_path = root / MANIFEST_REL
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    helpers = manifest.get("helpers")
    require(isinstance(helpers, dict), "RUNNER_HELPERS_SECTION_INVALID")

    metadata = {key: value for key, value in manifest.items() if key != "helpers"}
    require(
        stable_json_sha256(metadata) == BASELINE_MANIFEST_METADATA_SHA256,
        "RUNNER_MANIFEST_METADATA_DRIFT",
    )

    existing = {
        key: value
        for key, value in helpers.items()
        if key not in ADDED_HELPERS
    }
    require(
        stable_json_sha256(existing) == BASELINE_EXISTING_HELPERS_SHA256,
        "RUNNER_PREEXISTING_HELPER_RECORD_DRIFT",
    )

    folder = root / HELP_FOLDER_REL
    physical_files = sorted(path.name for path in folder.glob("*.py") if path.is_file())
    require(
        sorted(str(name) for name in helpers) == physical_files,
        "RUNNER_HELPER_FILE_MANIFEST_CLOSURE_MISMATCH",
    )

    for name in physical_files:
        path = folder / name
        exports = helpers[name].get("exports")
        require(isinstance(exports, list), "RUNNER_EXPORT_LIST_INVALID:" + name)
        module_all = literal_all(path)
        public_names = public_top_level_names(path)
        if module_all is None:
            require(not public_names, "RUNNER_PUBLIC_NAMES_WITHOUT_ALL:" + name)
            require(exports == [], "RUNNER_MANIFEST_EXPORTS_WITHOUT_ALL:" + name)
        else:
            require(exports == module_all, "RUNNER_HELPER_EXPORT_DRIFT:" + name)

    for name, expected in EXPECTED_ADDED_RECORDS.items():
        require(helpers.get(name) == expected, "RUNNER_ADDED_RECORD_DRIFT:" + name)

    require(
        literal_all(folder / "png_reuse_cancel_controls_private_impl.py")
        == EXPECTED_PNG_ALL,
        "PNG_CONTROL_PUBLIC_SURFACE_DRIFT",
    )

    require(len(physical_files) == 19, "RUNNER_HELPER_COUNT_UNEXPECTED")
    require(len(helpers) == 19, "RUNNER_MANIFEST_HELPER_COUNT_UNEXPECTED")
    require(
        len(manifest_path.read_text(encoding="utf-8-sig").splitlines()) <= 500,
        "RUNNER_HELP_MANIFEST_EXCEEDS_500_LINES",
    )

    print("RUNNER HELPER FILE MANIFEST CLOSURE: PASS")
    print("RUNNER HELPER EXPORT MANIFEST CLOSURE: PASS")
    print("RUNNER FOUR OMITTED HELPERS REGISTERED: PASS")
    print("PNG CONTROLS EXPLICIT PUBLIC SURFACE: PASS")
    print("RUNNER PREEXISTING MANIFEST RECORDS PRESERVED: PASS")

def validate_source_behavior(root: Path) -> None:
    """Prove the source patch changes no executable PNG-control behavior."""
    folder = root / HELP_FOLDER_REL
    png_path = root / PNG_REL
    require(hashlib.sha256(png_path.read_bytes()).hexdigest() == INSTALLED_PNG_SOURCE_SHA256, "PNG_CONTROL_INSTALLED_SOURCE_HASH_DRIFT")
    require(reconstructed_png_baseline_sha256(png_path) == BASELINE_PNG_SOURCE_SHA256, "PNG_CONTROL_BASELINE_RECONSTRUCTION_DRIFT")
    for name, expected in UNCHANGED_SOURCE_HASHES.items():
        actual = hashlib.sha256((folder / name).read_bytes()).hexdigest()
        require(actual == expected, "RUNNER_UNCHANGED_SOURCE_HASH_DRIFT:" + name)

    markers = {
        "window_methods_private_impl.py": [
            "png_reuse_cancel_controls_private_impl as _png_controls",
            "_png_controls.install_controls(self, project_root_row)",
            "answer_validate_freeze_memorize_button_private_impl as _answer_routine",
        ],
        "window_process_private_impl.py": [
            "png_reuse_cancel_controls_private_impl as _png_controls",
            "_png_controls.consume_cancel_on_finish",
        ],
        "zip_json_files_process_private_impl.py": [
            "png_reuse_cancel_controls_private_impl as _png_controls",
            "_png_controls.consume_cancel_on_finish",
        ],
        "complete_bridge_list_private_impl.py": [
            "bridge_metadata_classification import",
            "bridge_display_name",
            "is_active_on_demand_bridge",
            "prompt_front_matter",
            "startup_source_records",
        ],
        "__init__.py": [
            "project_tool_boundary_prompt_button_private_impl as _button",
            "_button.install_control(window)",
        ],
    }
    for name, required_markers in markers.items():
        text = (folder / name).read_text(encoding="utf-8-sig")
        for marker in required_markers:
            require(marker in text, "RUNNER_CONSUMER_MARKER_MISSING:" + name + ":" + marker)

    for path in root.rglob("*.py"):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except (UnicodeDecodeError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.module is None or not node.module.endswith(
                "png_reuse_cancel_controls_private_impl"
            ):
                continue
            require(
                all(alias.name != "*" for alias in node.names),
                "PNG_CONTROL_STAR_IMPORT_DETECTED:" + str(path),
            )

    for relative in (PNG_REL, Path(__file__).resolve()):
        path = relative if relative.is_absolute() else root / relative
        require(
            len(path.read_text(encoding="utf-8-sig").splitlines()) <= 500,
            "WAVE2F_TOUCHED_MODULE_EXCEEDS_500_LINES:" + str(path),
        )

    print("PNG CONTROL INSTALLED SOURCE HASH: PASS")
    print("PNG CONTROL BASELINE RECONSTRUCTION: PASS")
    print("PNG CONTROLS EXECUTABLE AST UNCHANGED: PASS")
    print("PYTHON VERSION INDEPENDENT BEHAVIOR PROOF: PASS")
    print("RUNNER RELATED SOURCE HASHES UNCHANGED: PASS")
    print("RUNNER MANIFEST CONSUMER GRAPH VERIFIED: PASS")
    print("PNG CONTROLS STAR IMPORT ABSENT: PASS")
    print("WAVE2F PYTHON JSON AND SIZE CONTRACT: PASS")

def run_command(
    root: Path,
    command: list[str],
    marker: str,
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    """Run one governed command and require an exact success marker."""
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

def validate_owned_png_contracts(root: Path) -> None:
    """Run only the PNG/cancel contracts owned by this wave."""
    validator_path = root / "tools/validate_show_project_png_reuse_cancel_controls_v1.py"
    spec = importlib.util.spec_from_file_location("_wave2f_png_contract_validator", validator_path)
    require(spec is not None and spec.loader is not None, "PNG_OWNED_VALIDATOR_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    root_text = str(root)
    inserted = False
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
        inserted = True
    try:
        spec.loader.exec_module(module)
        module.validate_reuse_signature()
        module.validate_full_reuse_contract()
        module.validate_cancel_contract()
        module.validate_ui_source(root)
        module.validate_optional_save_prefs(root)
        module.validate_optional_runtime_event(root)
        module.validate_sys_import_for_child_launch(root)
        module.validate_safe_child_mode_arg(root)
    finally:
        if inserted and sys.path and sys.path[0] == root_text:
            sys.path.pop(0)
    print("PNG REUSE CANCEL OWNED CONTRACTS: PASS")
    print("UNRELATED COMPLETE JSON ASSERTION EXCLUDED: PASS")

def validate_live_architecture(root: Path) -> None:
    """Require both owned architecture warnings to be absent."""
    output = run_command(
        root,
        [
            sys.executable,
            str(root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
            "--root",
            str(root),
            "--validate",
        ],
        "ARCHITECTURE VALIDATION SUMMARY",
        "ARCHITECTURE_VALIDATION",
    )
    require("Errors: 0" in output, "ARCHITECTURE_ERRORS_REMAIN")
    require(
        "HELPER_MANIFEST_CONTRACT     kanda_reasoner_app/reasoner_tools_shell/runner_help ::"
        not in output,
        "RUNNER_HELP_FOLDER_WARNING_REMAINS",
    )
    require(
        "HELPER_MANIFEST_CONTRACT     kanda_reasoner_app/reasoner_tools_shell/runner_help.json ::"
        not in output,
        "RUNNER_HELP_MANIFEST_WARNING_REMAINS",
    )
    require(
        "  HELPER_MANIFEST_CONTRACT:" not in output,
        "HELPER_MANIFEST_CONTRACT_FAMILY_REMAINS",
    )
    print("WAVE2F RUNNER HELPER PUBLIC SURFACE WARNING ABSENT: PASS")
    print("WAVE2F RUNNER HELPER MANIFEST WARNING ABSENT: PASS")
    print("WAVE2F HELPER MANIFEST FAMILY CLOSED: PASS")

def validate_inherited_contracts(root: Path) -> None:
    """Run all directly affected functional and ownership validators."""
    validate_owned_png_contracts(root)
    run_command(
        root,
        [
            sys.executable,
            str(root / "tools/validate_show_project_toolbar_surgical_ui_v1.py"),
            "--root",
            str(root),
        ],
        "VALIDATION OK: show-project-toolbar-surgical-ui-v1",
        "SHOW_PROJECT_TOOLBAR_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(root / "tools/validate_answer_validate_freeze_memorize_separated_terminal_phases_v1.py"),
            "--root",
            str(root),
        ],
        "VALIDATION OK: answer-validate-freeze-memorize-separated-terminal-phases-v1",
        "ANSWER_VALIDATE_FREEZE_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(root / "tools/validate_show_project_tool_project_prompt_button_v1r3.py"),
            str(root),
        ],
        "VALIDATION OK: show-project-tool-project-prompt-copy-button-v1r3",
        "TOOL_PROJECT_BUTTON_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(root / "scripts/validate_complete_bridge_list_button_v1.py"),
        ],
        "VALIDATION OK: complete-bridge-classification-and-selected-project-feature-checklist-v1",
        "COMPLETE_BRIDGE_LIST_VALIDATOR",
    )
    run_command(
        root,
        [
            sys.executable,
            str(root / "tools/validate_show_project_backup_button_v1.py"),
        ],
        "VALIDATION OK: show-project-backup-button-v1r2",
        "SHOW_PROJECT_BACKUP_VALIDATOR",
    )

def main() -> int:
    """Run Wave 2F validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve(strict=True)
    validate_manifest(root)
    validate_source_behavior(root)

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
