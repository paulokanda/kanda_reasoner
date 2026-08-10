"""Validate the minimal public API for the shared answer routine contract."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-answer-routine-contract-public-surface-wave2g-v1"
CONTRACT_REL = Path("tools/_answer_validate_freeze_memorize_contract.py")
EXPECTED_EXPORTS = ['HELPER_REL', 'validate_all']
EXPECTED_CONSUMERS = {
    "tools/validate_answer_validate_freeze_memorize_cross_project_v3.py": [
        "validate_all"
    ],
    "tools/validate_answer_validate_freeze_memorize_daily_work_staging_v1.py": [
        "HELPER_REL",
        "validate_all"
    ],
    "tools/validate_answer_validate_freeze_memorize_separated_terminal_phases_v1.py": [
        "validate_all"
    ],
    "tools/validate_patch_validate_freeze_recovery_blueprint_v1.py": [
        "validate_all"
    ],
    "tools/validate_show_project_ai_answer_routine_blueprint_position_v1.py": [
        "validate_all"
    ],
    "tools/validate_show_project_answer_validate_freeze_memorize_button_v1.py": [
        "validate_all"
    ]
}
EXPECTED_CONSUMER_HASHES = {
    "tools/validate_answer_validate_freeze_memorize_cross_project_v3.py": "0de4b48d5a9b1e4b17aa6ba53b98c4dfc9ddcafdf3cc76c61ad0b1032942eb90",
    "tools/validate_answer_validate_freeze_memorize_daily_work_staging_v1.py": "3bbe1ead2615cc3a00e4d18d86d7c92d3cd91cbb9ee26588251fdff5c7e210cd",
    "tools/validate_answer_validate_freeze_memorize_separated_terminal_phases_v1.py": "fb70451060db88941499d697b23828b881137ec507edf4f66f615436c50db65b",
    "tools/validate_patch_validate_freeze_recovery_blueprint_v1.py": "af0ef578dc287b6b85b29e4bd6023a6de84ad9fdb529d8173bff1992ed4a2086",
    "tools/validate_show_project_ai_answer_routine_blueprint_position_v1.py": "48a8c379d5978aabaf314f22e3c8ca8b04b59228ae539c933f1388f5096d375d",
    "tools/validate_show_project_answer_validate_freeze_memorize_button_v1.py": "dbe1c133dc1173941faf6017eb67fd9602b9a485b51d9e2764b07aa45dec4837"
}
INSTALLED_CONTRACT_SHA256 = "4c3b6d261ed9b0198530c29d18d40bb74f38fa80b6be33c6b1090fa83ffec6e1"
BASELINE_CONTRACT_SHA256 = "35f9527a1d8c98a08a132f6c242e3bd2eaee609e73616c1bf4fbd76d9950c334"
PUBLIC_SURFACE_BLOCK = '__all__ = [\n    "HELPER_REL",\n    "validate_all",\n]\n\n'


def require(condition: bool, code: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise RuntimeError(code)


def literal_all(path: Path) -> list[str] | None:
    """Return one literal module __all__, or None when absent/nonliteral."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = list(node.targets) if isinstance(node, ast.Assign) else [node.target]
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in targets
        ):
            continue
        value = node.value
        if not isinstance(value, (ast.List, ast.Tuple)):
            return None
        exports: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                return None
            exports.append(item.value)
        return exports
    return None


def top_level_names(path: Path) -> set[str]:
    """Collect top-level assigned, function, and class names."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = list(node.targets) if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names


def imported_contract_names(path: Path) -> list[str] | None:
    """Return direct names imported from the shared contract, or None."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    imported: list[str] = []
    found = False
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module != "_answer_validate_freeze_memorize_contract":
            continue
        found = True
        for alias in node.names:
            require(alias.name != "*", "ANSWER_ROUTINE_STAR_IMPORT_PRESENT:" + str(path))
            imported.append(alias.name)
    return sorted(imported) if found else None


def validate_contract_source(root: Path) -> None:
    """Prove the source-only API declaration and exact baseline reconstruction."""
    path = root / CONTRACT_REL
    require(path.is_file(), "ANSWER_ROUTINE_CONTRACT_MISSING")
    require(
        literal_all(path) == EXPECTED_EXPORTS,
        "ANSWER_ROUTINE_PUBLIC_SURFACE_DRIFT",
    )
    names = top_level_names(path)
    for symbol in EXPECTED_EXPORTS:
        require(symbol in names, "ANSWER_ROUTINE_PUBLIC_SYMBOL_MISSING:" + symbol)

    installed = hashlib.sha256(path.read_bytes()).hexdigest()
    require(
        installed == INSTALLED_CONTRACT_SHA256,
        "ANSWER_ROUTINE_INSTALLED_SOURCE_HASH_DRIFT",
    )

    source = path.read_text(encoding="utf-8-sig")
    require(
        source.count(PUBLIC_SURFACE_BLOCK) == 1,
        "ANSWER_ROUTINE_PUBLIC_SURFACE_BLOCK_COUNT_INVALID",
    )
    baseline = source.replace(PUBLIC_SURFACE_BLOCK, "", 1)
    require(
        hashlib.sha256(baseline.encode("utf-8")).hexdigest()
        == BASELINE_CONTRACT_SHA256,
        "ANSWER_ROUTINE_BASELINE_RECONSTRUCTION_DRIFT",
    )

    py_compile.compile(str(path), doraise=True)
    require(
        len(source.splitlines()) <= 500,
        "ANSWER_ROUTINE_CONTRACT_EXCEEDS_500_LINES",
    )
    require(
        len(Path(__file__).read_text(encoding="utf-8-sig").splitlines()) <= 500,
        "WAVE2G_VALIDATOR_EXCEEDS_500_LINES",
    )

    print("ANSWER ROUTINE MINIMAL PUBLIC SURFACE: PASS")
    print("ANSWER ROUTINE PUBLIC SYMBOLS DEFINED: PASS")
    print("ANSWER ROUTINE INSTALLED SOURCE HASH: PASS")
    print("ANSWER ROUTINE BASELINE RECONSTRUCTION: PASS")
    print("ANSWER ROUTINE PYTHON AND SIZE CONTRACT: PASS")


def validate_consumers(root: Path) -> None:
    """Require exact consumers, imports, hashes, and absence of star imports."""
    discovered: dict[str, list[str]] = {}
    for path in sorted((root / "tools").glob("*.py")):
        imported = imported_contract_names(path)
        if imported is None:
            continue
        discovered[path.relative_to(root).as_posix()] = imported

    require(
        discovered == EXPECTED_CONSUMERS,
        "ANSWER_ROUTINE_CONSUMER_IMPORT_GRAPH_DRIFT",
    )

    for relative, expected_hash in EXPECTED_CONSUMER_HASHES.items():
        path = root / relative
        require(path.is_file(), "ANSWER_ROUTINE_CONSUMER_MISSING:" + relative)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(
            actual == expected_hash,
            "ANSWER_ROUTINE_CONSUMER_SOURCE_HASH_DRIFT:" + relative,
        )
        for imported in discovered[relative]:
            require(
                imported in EXPECTED_EXPORTS,
                "ANSWER_ROUTINE_CONSUMER_IMPORTS_INTERNAL_SYMBOL:"
                + relative
                + ":"
                + imported,
            )

    print("ANSWER ROUTINE CONSUMER GRAPH: PASS")
    print("ANSWER ROUTINE CONSUMER IMPORTS PUBLIC ONLY: PASS")
    print("ANSWER ROUTINE CONSUMER SOURCES UNCHANGED: PASS")
    print("ANSWER ROUTINE STAR IMPORT ABSENT: PASS")


def run_command(
    root: Path,
    command: list[str],
    marker: str,
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    """Run one inherited command and require exact success."""
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


def validate_architecture(root: Path) -> None:
    """Require the owned warning absent and the expected live issue count."""
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
    require(
        "Total issues: 16 | Errors: 0 | Warnings: 16 | Other: 0" in output,
        "WAVE2G_ARCHITECTURE_COUNT_UNEXPECTED",
    )
    target = (
        "MISSING_PUBLIC_SURFACE_CONTROL "
        "tools/_answer_validate_freeze_memorize_contract.py"
    )
    require(target not in output, "ANSWER_ROUTINE_PUBLIC_SURFACE_WARNING_REMAINS")
    print("WAVE2G ANSWER ROUTINE PUBLIC SURFACE WARNING ABSENT: PASS")


def validate_inherited_consumers(root: Path) -> None:
    """Run all six real consumers of the shared contract."""
    commands = [
        (
            [
                sys.executable,
                str(root / "tools/validate_answer_validate_freeze_memorize_cross_project_v3.py"),
                str(root),
            ],
            "VALIDATION OK: answer-validate-freeze-cross-project-routine-v3",
            "CROSS_PROJECT_ROUTINE",
        ),
        (
            [
                sys.executable,
                str(root / "tools/validate_show_project_answer_validate_freeze_memorize_button_v1.py"),
                str(root),
            ],
            "VALIDATION OK: show-project-answer-validate-freeze-memorize-button-v1",
            "SHOW_PROJECT_BUTTON",
        ),
        (
            [
                sys.executable,
                str(root / "tools/validate_answer_validate_freeze_memorize_daily_work_staging_v1.py"),
                "--root",
                str(root),
            ],
            "VALIDATION OK: answer-validate-freeze-memorize-daily-work-staging-v1",
            "DAILY_WORK_STAGING",
        ),
        (
            [
                sys.executable,
                str(root / "tools/validate_show_project_ai_answer_routine_blueprint_position_v1.py"),
                str(root),
            ],
            "VALIDATION OK: show-project-ai-answer-routine-blueprint-position-v1",
            "BLUEPRINT_POSITION",
        ),
        (
            [
                sys.executable,
                str(root / "tools/validate_patch_validate_freeze_recovery_blueprint_v1.py"),
                str(root),
            ],
            "VALIDATION OK: patch-validate-freeze-recovery-blueprint-v1",
            "RECOVERY_BLUEPRINT",
        ),
        (
            [
                sys.executable,
                str(root / "tools/validate_answer_validate_freeze_memorize_separated_terminal_phases_v1.py"),
                "--root",
                str(root),
            ],
            "VALIDATION OK: answer-validate-freeze-memorize-separated-terminal-phases-v1",
            "SEPARATED_TERMINAL_PHASES",
        ),
    ]
    for command, marker, code in commands:
        run_command(root, command, marker, code)
    print("ANSWER ROUTINE SIX CONSUMER VALIDATORS: PASS")


def main() -> int:
    """Run the Wave 2G public-surface validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_contract_source(root)
    validate_consumers(root)

    if not args.static_only:
        validate_architecture(root)
        validate_inherited_consumers(root)

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
