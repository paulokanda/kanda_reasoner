"""Validate the minimal Tool Portable builder/smoke public surfaces."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = 'architecture-tool-portable-public-surface-wave2h-v1'
BUILDER_REL = Path('tools/build_kanda_reasoner_tool_portable.py')
SMOKE_REL = Path('tools/tool_portable_functional_smoke.py')
DIRECT_VALIDATOR_REL = Path('tools/validate_kanda_reasoner_tool_portable_direct_build_v1r1.py')
OWNER_VALIDATOR_REL = Path('tools/validate_tool_portable_functional_smoke_owner_reuse_v1.py')
AUTHORITY_VALIDATOR_REL = Path('tools/validate_tool_portable_local_ai_project_authority_v1r1.py')

EXPECTED_EXPORTS = {
    BUILDER_REL.as_posix(): ['assert_no_project_capture', 'stage_application', 'create_deterministic_zip', 'main'],
    SMOKE_REL.as_posix(): ['validate_runtime_report', 'seed_external_smoke_registry', 'smoke_no_project', 'smoke_external_project'],
}
INSTALLED_HASHES = {'tools/build_kanda_reasoner_tool_portable.py': 'b132cf72cbcc053981ced4abfd18fa49423fa4ee20d0c7ac79960547cb07b14d', 'tools/tool_portable_functional_smoke.py': '61d7cd515c32dcb324c43c2a10bf58ec30427d6063886b88919e5ef501af9f91'}
BASELINE_HASHES = {'tools/build_kanda_reasoner_tool_portable.py': '17d5a6e3df3a70ce71bd441304b6385715357c4cbff583e8c227a828c732be10', 'tools/tool_portable_functional_smoke.py': '9a8993989ba801a3e3704d0f289aece1edfc7d114b0419315099a120ea0e694c'}
PUBLIC_SURFACE_BLOCKS = {
    BUILDER_REL.as_posix(): '__all__ = [\n    "assert_no_project_capture",\n    "stage_application",\n    "create_deterministic_zip",\n    "main",\n]\n\n',
    SMOKE_REL.as_posix(): '__all__ = [\n    "validate_runtime_report",\n    "seed_external_smoke_registry",\n    "smoke_no_project",\n    "smoke_external_project",\n]\n\n',
}

def require(condition: bool, code: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise RuntimeError(code)


def literal_all(path: Path) -> list[str] | None:
    """Return one literal module __all__ declaration."""
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
        result: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                return None
            result.append(item.value)
        return result
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


def imported_names(path: Path, module_name: str) -> list[str]:
    """Return direct imported names for one exact module."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or node.module != module_name:
            continue
        for alias in node.names:
            require(alias.name != "*", "TOOL_PORTABLE_STAR_IMPORT_PRESENT")
            names.append(alias.name)
    return sorted(names)


def attribute_names(path: Path, owner_name: str) -> set[str]:
    """Collect attribute names read through one loaded-module variable."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == owner_name
    }


def parser_flags(path: Path) -> set[str]:
    """Collect literal argparse option names declared by one validator."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    flags: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if not (
            isinstance(function, ast.Attribute)
            and function.attr == "add_argument"
            and node.args
        ):
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            flags.add(first.value)
    return flags


def literal_string_assignment(path: Path, name: str) -> str | None:
    """Return one top-level literal string assignment."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = list(node.targets) if isinstance(node, ast.Assign) else [node.target]
        if not any(
            isinstance(target, ast.Name) and target.id == name
            for target in targets
        ):
            continue
        value = node.value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            return value.value
    return None


def require_tokens(path: Path, tokens: tuple[str, ...], code: str) -> None:
    """Require semantic markers without freezing the complete file hash."""
    source = path.read_text(encoding="utf-8-sig")
    for token in tokens:
        require(token in source, code + ":" + token)


def validate_sources(root: Path) -> None:
    """Validate explicit APIs and exact behavior-preserving reconstruction."""
    for relative in (BUILDER_REL, SMOKE_REL):
        path = root / relative
        key = relative.as_posix()
        require(path.is_file(), "TOOL_PORTABLE_PUBLIC_SURFACE_TARGET_MISSING:" + key)
        require(
            literal_all(path) == EXPECTED_EXPORTS[key],
            "TOOL_PORTABLE_PUBLIC_SURFACE_DRIFT:" + key,
        )
        names = top_level_names(path)
        for symbol in EXPECTED_EXPORTS[key]:
            require(
                symbol in names,
                "TOOL_PORTABLE_EXPORTED_SYMBOL_MISSING:" + key + ":" + symbol,
            )

        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == INSTALLED_HASHES[key],
            "TOOL_PORTABLE_INSTALLED_SOURCE_HASH_DRIFT:" + key,
        )
        source = path.read_text(encoding="utf-8-sig")
        block = PUBLIC_SURFACE_BLOCKS[key]
        require(
            source.count(block) == 1,
            "TOOL_PORTABLE_PUBLIC_SURFACE_BLOCK_COUNT_INVALID:" + key,
        )
        reconstructed = source.replace(block, "", 1)
        require(
            hashlib.sha256(reconstructed.encode("utf-8")).hexdigest()
            == BASELINE_HASHES[key],
            "TOOL_PORTABLE_BASELINE_RECONSTRUCTION_DRIFT:" + key,
        )
        py_compile.compile(str(path), doraise=True)
        require(
            len(source.splitlines()) <= 500,
            "TOOL_PORTABLE_SOURCE_EXCEEDS_500_LINES:" + key,
        )

    print("TOOL PORTABLE BUILDER MINIMAL PUBLIC SURFACE: PASS")
    print("TOOL PORTABLE SMOKE MINIMAL PUBLIC SURFACE: PASS")
    print("TOOL PORTABLE EXPORTED SYMBOLS DEFINED: PASS")
    print("TOOL PORTABLE INSTALLED SOURCE HASHES: PASS")
    print("TOOL PORTABLE BASELINE RECONSTRUCTION: PASS")
    print("TOOL PORTABLE PYTHON AND SIZE CONTRACT: PASS")


def validate_consumer_graph(root: Path) -> None:
    """Validate runtime imports and source-loaded validator consumers."""
    builder = root / BUILDER_REL
    direct = root / DIRECT_VALIDATOR_REL
    owner = root / OWNER_VALIDATOR_REL
    authority = root / AUTHORITY_VALIDATOR_REL

    require(
        imported_names(builder, "tool_portable_functional_smoke")
        == ["smoke_external_project", "smoke_no_project"],
        "TOOL_PORTABLE_BUILDER_SMOKE_IMPORT_GRAPH_DRIFT",
    )

    builder_refs = attribute_names(direct, "build_module")
    require(
        {
            "assert_no_project_capture",
            "stage_application",
            "create_deterministic_zip",
        }.issubset(builder_refs),
        "TOOL_PORTABLE_DYNAMIC_BUILDER_CONSUMER_DRIFT",
    )
    require(
        builder_refs.intersection(set(EXPECTED_EXPORTS[BUILDER_REL.as_posix()]))
        == {
            "assert_no_project_capture",
            "stage_application",
            "create_deterministic_zip",
        },
        "TOOL_PORTABLE_DYNAMIC_BUILDER_PUBLIC_REF_DRIFT",
    )

    smoke_refs = attribute_names(direct, "smoke_module")
    require(
        {
            "validate_runtime_report",
            "seed_external_smoke_registry",
            "_sha256_text",
        }.issubset(smoke_refs),
        "TOOL_PORTABLE_DYNAMIC_SMOKE_CONSUMER_DRIFT",
    )
    require(
        "_sha256_text" not in EXPECTED_EXPORTS[SMOKE_REL.as_posix()],
        "TOOL_PORTABLE_PRIVATE_TEST_HOOK_EXPORTED",
    )

    for path in (direct, owner, authority):
        require(path.is_file(), "TOOL_PORTABLE_CONSUMER_MISSING:" + str(path))
        source = path.read_text(encoding="utf-8-sig")
        ast.parse(source, filename=str(path))
        require(
            len(source.splitlines()) <= 500,
            "TOOL_PORTABLE_CONSUMER_EXCEEDS_500_LINES:" + str(path),
        )

    require(
        "--tool-root" in parser_flags(direct),
        "TOOL_PORTABLE_DIRECT_VALIDATOR_CLI_DRIFT",
    )
    require(
        literal_string_assignment(direct, "FEATURE_ID")
        == "kanda-reasoner-tool-portable-direct-pyinstaller-v1r2",
        "TOOL_PORTABLE_DIRECT_VALIDATOR_ID_DRIFT",
    )

    owner_text = owner.read_text(encoding="utf-8-sig")
    require(
        BUILDER_REL.as_posix() in owner_text and SMOKE_REL.as_posix() in owner_text,
        "TOOL_PORTABLE_OWNER_VALIDATOR_TARGET_GRAPH_DRIFT",
    )
    require(
        "--tool-root" in parser_flags(owner),
        "TOOL_PORTABLE_OWNER_VALIDATOR_CLI_DRIFT",
    )
    require_tokens(
        owner,
        (
            "PORTABLE BUILD EXECUTED BY VALIDATION: NO",
            "kanda-reasoner-tool-portable-functional-smoke-owner-reuse-v1",
        ),
        "TOOL_PORTABLE_OWNER_VALIDATOR_CONTRACT_DRIFT",
    )

    require(
        literal_string_assignment(authority, "FEATURE_ID")
        == "kanda-reasoner-tool-portable-local-ai-project-authority-v1r1",
        "TOOL_PORTABLE_AUTHORITY_VALIDATOR_ID_DRIFT",
    )
    require(
        literal_string_assignment(authority, "BUILDER_RELATIVE")
        == BUILDER_REL.as_posix(),
        "TOOL_PORTABLE_AUTHORITY_BUILDER_TARGET_DRIFT",
    )
    authority_flags = parser_flags(authority)
    require(
        {"--tool-root", "--skip-existing-validators"}.issubset(authority_flags),
        "TOOL_PORTABLE_AUTHORITY_VALIDATOR_CLI_DRIFT",
    )
    require_tokens(
        authority,
        (
            "validate_tool_portable_local_ai_project_authority_v1r1.py",
            "--skip-existing-validators",
            "LOCAL AI PROJECT AUTHORITY PRE-BUILD GATE: PASS",
            "PORTABLE BUILD EXECUTED BY VALIDATION: NO",
        ),
        "TOOL_PORTABLE_AUTHORITY_VALIDATOR_CONTRACT_DRIFT",
    )

    print("TOOL PORTABLE BUILDER TO SMOKE IMPORT GRAPH: PASS")
    print("TOOL PORTABLE DYNAMIC CONSUMER GRAPH: PASS")
    print("TOOL PORTABLE CONSUMER STRUCTURAL CONTRACTS: PASS")
    print("TOOL PORTABLE CONSUMER EVOLUTION TOLERANCE: PASS")
    print("TOOL PORTABLE PRIVATE TEST HOOK REMAINS PRIVATE: PASS")
    print("TOOL PORTABLE STAR IMPORT ABSENT: PASS")


def run_command(
    root: Path,
    command: list[str],
    markers: tuple[str, ...],
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    """Run one inherited validator and require exact markers."""
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
    for marker in markers:
        require(marker in output, code + "_MARKER_MISSING:" + marker)
    return output


def validate_architecture(root: Path) -> None:
    """Require both owned warnings absent and the expected live count."""
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
        ("ARCHITECTURE VALIDATION SUMMARY",),
        "ARCHITECTURE_VALIDATION",
    )
    require("Errors: 0" in output, "ARCHITECTURE_ERRORS_REMAIN")
    require(
        "Total issues: 14 | Errors: 0 | Warnings: 14 | Other: 0" in output,
        "WAVE2H_ARCHITECTURE_COUNT_UNEXPECTED",
    )
    for relative in (BUILDER_REL, SMOKE_REL):
        warning = "MISSING_PUBLIC_SURFACE_CONTROL " + relative.as_posix()
        require(warning not in output, "WAVE2H_PUBLIC_SURFACE_WARNING_REMAINS:" + warning)

    print("WAVE2H BUILDER PUBLIC SURFACE WARNING ABSENT: PASS")
    print("WAVE2H SMOKE PUBLIC SURFACE WARNING ABSENT: PASS")
    print("WAVE2H TOOL PUBLIC SURFACE FAMILY CLOSED: PASS")


def validate_inherited_contracts(root: Path) -> None:
    """Run the current Tool Portable owner and authority validators."""
    owner_output = run_command(
        root,
        [
            sys.executable,
            str(root / OWNER_VALIDATOR_REL),
            "--tool-root",
            str(root),
        ],
        (
            "VALIDATION OK: kanda-reasoner-tool-portable-direct-pyinstaller-v1r2",
            "VALIDATION OK: kanda-reasoner-tool-portable-functional-smoke-owner-reuse-v1",
        ),
        "TOOL_PORTABLE_OWNER_REUSE_VALIDATION",
    )
    require(
        "PORTABLE BUILD EXECUTED BY VALIDATION: NO" in owner_output,
        "TOOL_PORTABLE_BUILD_EXECUTION_BOUNDARY_MISSING",
    )

    run_command(
        root,
        [
            sys.executable,
            str(root / AUTHORITY_VALIDATOR_REL),
            "--tool-root",
            str(root),
            "--skip-existing-validators",
        ],
        (
            "VALIDATION OK: kanda-reasoner-tool-portable-local-ai-project-authority-v1r1",
        ),
        "TOOL_PORTABLE_AUTHORITY_VALIDATION",
    )

    print("TOOL PORTABLE DIRECT BUILD CONTRACT: PASS")
    print("TOOL PORTABLE FUNCTIONAL SMOKE OWNER CONTRACT: PASS")
    print("TOOL PORTABLE LOCAL AI PROJECT AUTHORITY CONTRACT: PASS")
    print("TOOL PORTABLE BUILD EXECUTED BY WAVE2H VALIDATION: NO")


def main() -> int:
    """Run the Wave 2H public-surface validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_sources(root)
    validate_consumer_graph(root)

    if not args.static_only:
        validate_architecture(root)
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
