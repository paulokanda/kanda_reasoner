# project-path: kanda_prompt_workspace/prompt_library/TOOLS/validate_context_routing_layer.py
"""Validate the staged KANDA Context Routing Layer package.

This validator is intentionally project-local and read-only. It checks the
prompt laboratory folder before any later live-app integration.

Compatible with Python 3.10+ on standard CPython and Windows/PyCharm.
"""

from __future__ import annotations


__all__ = [
    'iter_json_files',
    'validate',
    'validate_folder_cards',
    'validate_forbidden_paths',
    'validate_group_index',
    'validate_metadata_json',
    'validate_required_files',
    'validate_routing_tests',
    'ValidationState',
    'word_count',
]
import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


EXPECTED_GROUPS = [
    "01_session_start_and_navigation",
    "02_prompt_routing_and_indexing",
    "03_governance_freeze_and_handoff",
    "04_box_architecture_and_boundaries",
    "05_patch_delivery_and_validation",
    "06_refactor_and_architecture_hardening",
    "07_prompt_authoring_and_audit",
    "08_python_engineering_core",
    "09_python_quality_security_observability",
    "10_python_api_data_async_config",
    "11_productization_and_release_readiness",
    "12_generalized_project_canons",
]

REQUIRED_FILES = [
    "ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md",
    "ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md",
    "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
    "ROUTING/GROUP_ASSIMILATION_INDEX.md",
    "ROUTING/group_assimilation_index.json",
    "ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md",
    "ROUTING/folder_assimilation_cards_index.json",
    "ROUTING_TESTS/context_routing_test_cases.md",
    "ROUTING_TESTS/context_routing_expected_outputs.json",
]

FORBIDDEN_PATHS = [
    "kanda_reasoner_app",
    "prompt_library_gui",
]

CARD_SOFT_WORD_LIMIT = 300
CARD_HARD_WORD_LIMIT = 400


class ValidationState:
    """Collect validation failures and warnings while printing gates."""

    def __init__(self) -> None:
        """Support init behavior.
        """
        
        self.failures: int = 0
        self.warnings: int = 0

    def gate(self, name: str, passed: bool, detail: str = "") -> None:
        """Print a gate result and count failures."""
        exit_code = 0 if passed else 1
        if detail:
            print(f"GATE {name} {detail} EXIT_CODE {exit_code}")
        else:
            print(f"GATE {name} EXIT_CODE {exit_code}")
        if not passed:
            self.failures += 1

    def warn(self, name: str, message: str) -> None:
        """Print a warning that does not fail validation."""
        print(f"WARNING {name}: {message}")
        self.warnings += 1


def load_json(path: Path) -> Tuple[bool, Any, str]:
    """Load a JSON file and return success, data, and error message."""
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
        return True, data, ""
    except Exception as exc:  # noqa: BLE001 - validation should report all errors clearly.
        return False, None, str(exc)


def word_count(path: Path) -> int:
    """Count simple whitespace-separated words in a text file."""
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return len(text.split())


def normalize_path(relative_path: str) -> str:
    """Normalize a slash-style relative path for the current platform."""
    return relative_path.replace("/", "\\")


def iter_json_files(root: Path) -> Iterable[Path]:
    """Yield JSON files under the staged package."""
    for path in root.rglob("*.json"):
        if path.is_file():
            yield path


def validate_required_files(root: Path, state: ValidationState) -> None:
    """Validate that the known routing layer files exist."""
    for relative_path in REQUIRED_FILES:
        path = root / normalize_path(relative_path)
        state.gate("required_file_exists", path.exists(), relative_path)


def validate_forbidden_paths(root: Path, state: ValidationState) -> None:
    """Validate that forbidden live-app paths are not present in the staging box."""
    for relative_path in FORBIDDEN_PATHS:
        path = root / relative_path
        state.gate("forbidden_path_absent", not path.exists(), str(path))


def validate_group_index(root: Path, state: ValidationState) -> None:
    """Validate the global group assimilation index."""
    path = root / "ROUTING" / "group_assimilation_index.json"
    ok, data, error = load_json(path)
    state.gate("group_index_json_parse", ok, str(path))
    if not ok:
        print(error)
        return

    groups = data.get("groups") if isinstance(data, dict) else None
    state.gate("group_index_has_groups_list", isinstance(groups, list), "groups")
    if not isinstance(groups, list):
        return

    state.gate("group_index_count_12", len(groups) == 12, f"actual={len(groups)}")

    present = set()
    for item in groups:
        if isinstance(item, dict):
            group_id = item.get("group_id") or item.get("id") or item.get("folder_id")
            if isinstance(group_id, str):
                present.add(group_id)

    missing = [group for group in EXPECTED_GROUPS if group not in present]
    state.gate("group_index_expected_ids", not missing, ",".join(missing) if missing else "none")


def validate_folder_cards(root: Path, state: ValidationState) -> None:
    """Validate folder assimilation cards and their index."""
    active_root = root / "ACTIVE_PROMPTS"
    cards = sorted(active_root.rglob("_FOLDER_ASSIMILATION.md")) if active_root.exists() else []
    state.gate("folder_assimilation_card_count_12", len(cards) == 12, f"actual={len(cards)}")

    for group in EXPECTED_GROUPS:
        path = active_root / group / "_FOLDER_ASSIMILATION.md"
        state.gate("folder_card_exists", path.exists(), group)
        if not path.exists():
            continue
        count = word_count(path)
        state.gate("folder_card_under_hard_word_limit", count <= CARD_HARD_WORD_LIMIT, f"{group} words={count}")
        if count > CARD_SOFT_WORD_LIMIT:
            state.warn("folder_card_soft_word_limit", f"{group} has {count} words; target is {CARD_SOFT_WORD_LIMIT}")

    index_path = root / "ROUTING" / "folder_assimilation_cards_index.json"
    ok, data, error = load_json(index_path)
    state.gate("folder_cards_index_json_parse", ok, str(index_path))
    if not ok:
        print(error)
        return

    folder_count = data.get("folder_count") if isinstance(data, dict) else None
    folders = data.get("folders") if isinstance(data, dict) else None
    state.gate("folder_cards_index_count_12", folder_count == 12 and isinstance(folders, list) and len(folders) == 12, f"folder_count={folder_count}")


def validate_routing_tests(root: Path, state: ValidationState) -> None:
    """Validate the routing test expectation file."""
    path = root / "ROUTING_TESTS" / "context_routing_expected_outputs.json"
    ok, data, error = load_json(path)
    state.gate("routing_tests_json_parse", ok, str(path))
    if not ok:
        print(error)
        return

    tests = data.get("tests") if isinstance(data, dict) else None
    test_count = data.get("test_count") if isinstance(data, dict) else None
    state.gate("routing_test_count_10", test_count == 10 and isinstance(tests, list) and len(tests) == 10, f"test_count={test_count}")

    required_fields = [
        "id",
        "input",
        "task_intent",
        "required_groups",
        "minimum_viable_context",
        "missing_behavior",
        "fast_path_allowed",
    ]

    missing_fields: List[str] = []
    if isinstance(tests, list):
        for item in tests:
            if not isinstance(item, dict):
                missing_fields.append("non_dict_test")
                continue
            test_id = str(item.get("id", "unknown"))
            for field in required_fields:
                if field not in item:
                    missing_fields.append(f"{test_id}:{field}")

    state.gate("routing_tests_required_fields", not missing_fields, ",".join(missing_fields) if missing_fields else "none")


def validate_metadata_json(root: Path, state: ValidationState) -> None:
    """Validate that JSON files in the staged package parse."""
    json_files = list(iter_json_files(root))
    state.gate("json_files_present", len(json_files) > 0, f"count={len(json_files)}")

    failed: List[str] = []
    for path in json_files:
        ok, _data, error = load_json(path)
        if not ok:
            failed.append(f"{path}: {error}")

    state.gate("all_json_files_parse", not failed, f"failed={len(failed)}")
    for item in failed:
        print(item)


def validate(root: Path) -> int:
    """Run all context routing layer validation gates."""
    state = ValidationState()
    print("CONTEXT ROUTING VALIDATOR START")
    print(f"Root: {root}")

    state.gate("root_exists", root.exists(), str(root))
    if not root.exists():
        print("VALIDATION SUMMARY")
        print(f"Failures: {state.failures}")
        print(f"Warnings: {state.warnings}")
        print("VALIDATION EXIT_CODE 1")
        return 1

    validate_required_files(root, state)
    validate_group_index(root, state)
    validate_folder_cards(root, state)
    validate_routing_tests(root, state)
    validate_metadata_json(root, state)
    validate_forbidden_paths(root, state)

    print("VALIDATION SUMMARY")
    print(f"Failures: {state.failures}")
    print(f"Warnings: {state.warnings}")

    if state.failures == 0:
        print("VALIDATION EXIT_CODE 0")
        return 0

    print("VALIDATION EXIT_CODE 1")
    return 1


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Validate the staged KANDA Context Routing Layer package."
    )
    parser.add_argument(
        "--root",
        required=True,
        help="Path to the prompt_library staging folder.",
    )
    return parser


def main() -> int:
    """Program entry point."""
    parser = build_parser()
    args = parser.parse_args()
    root = Path(args.root).resolve()
    return validate(root)


if __name__ == "__main__":
    raise SystemExit(main())
