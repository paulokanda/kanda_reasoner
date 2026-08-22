"""Validate canonical public surfaces for the remaining Portable modules."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

FEATURE_ID = 'architecture-portable-module-public-surfaces-wave2j-v1'
MANIFEST_REL = Path('portable/PORTABLE_BUILDER_MANIFEST.json')
EXPECTED_EXPORTS = {'portable/builder_members.py': ['BuilderMemberError', 'validate_exact_builder_members'], 'portable/constants.py': ['BUILDER_VERSION', 'PORTABLE_HARDENING_FEATURES', 'PORTABLE_HARDENING_STAGE', 'BUILDER_MEMBER_FEATURE_ID', 'EXTERNAL_CONTROL_FEATURE_ID', 'PRODUCTION_PORTABLE_ENABLED', 'PROJECT_FOLDER_NAME', 'SPEC_NAME', 'FINAL_ZIP_NAME', 'EXPECTED_PYTHON', 'EXPECTED_PYINSTALLER', 'MAX_ARCHIVE_PATH_BYTES', 'FIRST_SMOKE_CONFIRMATION', 'SMOKE_CONFIRMATION', 'NON_RUNTIME_LONG_PATH_DOCS', 'FORBIDDEN_GENERATED_FOLDER_NAMES', 'FORBIDDEN_GENERATED_PATH_SEQUENCES', 'RUNTIME_PACKAGE_PATH_SEQUENCES', 'FORBIDDEN_GENERATED_FILE_MARKERS', 'PORTABLE_ARCHIVE_SUFFIX', 'NON_RUNTIME_CACHE_FOLDER_NAMES', 'NON_RUNTIME_DEBRIS_FILE_NAMES', 'NON_RUNTIME_BACKUP_MARKERS', 'NON_RUNTIME_BACKUP_SUFFIXES', 'PROJECT_SNAPSHOT_IGNORES'], 'portable/external_controls.py': ['REQUIRED_EXTERNAL_CONTROLS', 'ExternalControlError', 'validate_external_build_controls'], 'portable/physical_runtime.py': ['RUNTIME_MANIFEST_RELATIVE', 'RUNTIME_ALLOWLIST_FEATURE_ID', 'REQUIRED_RUNTIME_ROLES', 'validate_runtime_allowlist_payload', 'load_runtime_allowlist', 'validate_runtime_allowlist_sources', 'hydrate_physical_runtime', 'validate_physical_runtime'], 'portable/registry_boundary.py': ['EXPLICIT_SELF_HOSTING', 'load_registry_boundary', 'assert_registry_unchanged', 'assert_outside_protected_roots', 'validate_publication_directory', 'validate_result_path'], 'portable/smoke_isolation.py': ['PreparedSmokeIsolation', 'verify_isolated_registry', 'prepared_smoke_isolation'], 'portable/validate_installed.py': ['main']}
MODULE_NAMES = {'portable/builder_members.py': 'portable.builder_members', 'portable/constants.py': 'portable.constants', 'portable/external_controls.py': 'portable.external_controls', 'portable/physical_runtime.py': 'portable.physical_runtime', 'portable/registry_boundary.py': 'portable.registry_boundary', 'portable/smoke_isolation.py': 'portable.smoke_isolation', 'portable/validate_installed.py': 'portable.validate_installed'}
BASELINE_HASHES = {'portable/builder_members.py': 'cb744eeb0d201234dfe6c1ec229e6b061f6b2f77043551dd7dcabeb10aec8596', 'portable/constants.py': 'bbd25636d6b540f799b5b794240663f928ff3fcc7060224881da79fcc915f1c4', 'portable/external_controls.py': 'b6136e45b1806e17ca6cb7eada59e070c1044209da0c20b9c1031e42ed9f7390', 'portable/physical_runtime.py': '04be54a006086136b8605243e87f14d674de917ab4ec7eeb7597ae34d426e66c', 'portable/registry_boundary.py': '5f4934212b4d876933bbbb467ce502178f1ea8106d05541b5cae161a03dbdd23', 'portable/smoke_isolation.py': 'b8c7f8f07afff0370955874666a7532affcd7b54831c838158d160c2c42714f1', 'portable/validate_installed.py': 'fc81d4a3e5c695efb50bfab18c27b88323e8a60aa58092a492b19e7dbbb526c0'}
INSTALLED_HASHES = {'portable/builder_members.py': '2059a59acdcbdd2a6d138bed42733cbe83fd4179e3e943d794d34c3358ac067a', 'portable/constants.py': 'c50c8b8b547763193a0d0ad0b2650ca5cbe7492ba5c71ba28344289f24c4aba7', 'portable/external_controls.py': '2b9f944027d92fc82d41cbb59518154a7ffd0ab8a3cb5b1c9c58a3041683d5d8', 'portable/physical_runtime.py': '8494451a184f09923c95ee6a318e1799f9334cce6f1e3f9bf9dab6b7049163ef', 'portable/registry_boundary.py': '984e3363841856535ff38812fd4cac8d9cf2496e19252344c8a6d0f3fca77df1', 'portable/smoke_isolation.py': '00a5cc4ec1da7312bf7315f4e33d079cbc6cdde15fe4fc9f824362c8f8e887a4', 'portable/validate_installed.py': 'a4fd943286131f6c020bc7dff78838305b31b71d1588f013e89e7c1d8d59f408'}
PUBLIC_BLOCKS = {'portable/builder_members.py': '__all__ = [\n    "BuilderMemberError",\n    "validate_exact_builder_members",\n]\n\n', 'portable/constants.py': '__all__ = [\n    "BUILDER_VERSION",\n    "PORTABLE_HARDENING_FEATURES",\n    "PORTABLE_HARDENING_STAGE",\n    "BUILDER_MEMBER_FEATURE_ID",\n    "EXTERNAL_CONTROL_FEATURE_ID",\n    "PRODUCTION_PORTABLE_ENABLED",\n    "PROJECT_FOLDER_NAME",\n    "SPEC_NAME",\n    "FINAL_ZIP_NAME",\n    "EXPECTED_PYTHON",\n    "EXPECTED_PYINSTALLER",\n    "MAX_ARCHIVE_PATH_BYTES",\n    "FIRST_SMOKE_CONFIRMATION",\n    "SMOKE_CONFIRMATION",\n    "NON_RUNTIME_LONG_PATH_DOCS",\n    "FORBIDDEN_GENERATED_FOLDER_NAMES",\n    "FORBIDDEN_GENERATED_PATH_SEQUENCES",\n    "RUNTIME_PACKAGE_PATH_SEQUENCES",\n    "FORBIDDEN_GENERATED_FILE_MARKERS",\n    "PORTABLE_ARCHIVE_SUFFIX",\n    "NON_RUNTIME_CACHE_FOLDER_NAMES",\n    "NON_RUNTIME_DEBRIS_FILE_NAMES",\n    "NON_RUNTIME_BACKUP_MARKERS",\n    "NON_RUNTIME_BACKUP_SUFFIXES",\n    "PROJECT_SNAPSHOT_IGNORES",\n]\n\n', 'portable/external_controls.py': '__all__ = [\n    "REQUIRED_EXTERNAL_CONTROLS",\n    "ExternalControlError",\n    "validate_external_build_controls",\n]\n\n', 'portable/physical_runtime.py': '__all__ = [\n    "RUNTIME_MANIFEST_RELATIVE",\n    "RUNTIME_ALLOWLIST_FEATURE_ID",\n    "REQUIRED_RUNTIME_ROLES",\n    "validate_runtime_allowlist_payload",\n    "load_runtime_allowlist",\n    "validate_runtime_allowlist_sources",\n    "hydrate_physical_runtime",\n    "validate_physical_runtime",\n]\n\n', 'portable/registry_boundary.py': '__all__ = [\n    "EXPLICIT_SELF_HOSTING",\n    "load_registry_boundary",\n    "assert_registry_unchanged",\n    "assert_outside_protected_roots",\n    "validate_publication_directory",\n    "validate_result_path",\n]\n\n', 'portable/smoke_isolation.py': '__all__ = [\n    "PreparedSmokeIsolation",\n    "verify_isolated_registry",\n    "prepared_smoke_isolation",\n]\n\n', 'portable/validate_installed.py': '__all__ = [\n    "main",\n]\n\n'}
BASELINE_MANIFEST_SHA256 = '7d8a5c42c7ede4cae71e4a3705f93ad54011489d877d89d7e2ff9bed80d2cb7d'
INSTALLED_MANIFEST_SHA256 = '6295875a5a97784a145b3a7b598f48933c8d99252b3a762880c868bb54453675'

REQUIRED_EXTERNAL_IMPORTS = {
    "portable.builder_members": {
        "BuilderMemberError",
        "validate_exact_builder_members",
    },
    "portable.constants": set(EXPECTED_EXPORTS["portable/constants.py"]),
    "portable.external_controls": {
        "REQUIRED_EXTERNAL_CONTROLS",
        "ExternalControlError",
        "validate_external_build_controls",
    },
    "portable.physical_runtime": {
        "RUNTIME_MANIFEST_RELATIVE",
        "RUNTIME_ALLOWLIST_FEATURE_ID",
        "REQUIRED_RUNTIME_ROLES",
        "validate_runtime_allowlist_payload",
        "load_runtime_allowlist",
        "validate_runtime_allowlist_sources",
        "hydrate_physical_runtime",
        "validate_physical_runtime",
    },
    "portable.registry_boundary": {
        "EXPLICIT_SELF_HOSTING",
        "load_registry_boundary",
        "assert_registry_unchanged",
        "assert_outside_protected_roots",
        "validate_publication_directory",
        "validate_result_path",
    },
    "portable.smoke_isolation": {
        "verify_isolated_registry",
        "prepared_smoke_isolation",
    },
    "portable.validate_installed": set(),
}

INTERNAL_CONSUMER_IMPORTS = {
    "portable.constants": {"FEATURE_ID"},
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


def imported_names(root: Path, module_name: str) -> set[str]:
    """Collect all direct imported symbols for one module."""
    names: set[str] = set()
    scan_roots = [root / "portable", root / "tools"]
    for scan_root in scan_roots:
        if not scan_root.is_dir():
            continue
        for path in scan_root.glob("*.py"):
            if path.as_posix().endswith(module_name.replace(".", "/") + ".py"):
                continue
            try:
                tree = ast.parse(
                    path.read_text(encoding="utf-8-sig"),
                    filename=str(path),
                )
            except (OSError, UnicodeError, SyntaxError):
                continue
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom) or node.module != module_name:
                    continue
                for alias in node.names:
                    require(
                        alias.name != "*",
                        "PORTABLE_PUBLIC_SURFACE_STAR_IMPORT:" + module_name,
                    )
                    names.add(alias.name)
    return names


def validate_sources(root: Path) -> None:
    """Validate exact public APIs and byte-identical source reconstruction."""
    for relative, expected_exports in EXPECTED_EXPORTS.items():
        path = root / relative
        require(path.is_file(), "PORTABLE_PUBLIC_SURFACE_TARGET_MISSING:" + relative)
        require(
            literal_all(path) == expected_exports,
            "PORTABLE_PUBLIC_SURFACE_DRIFT:" + relative,
        )
        names = top_level_names(path)
        for symbol in expected_exports:
            require(
                symbol in names,
                "PORTABLE_PUBLIC_SYMBOL_MISSING:" + relative + ":" + symbol,
            )
        if relative == "portable/constants.py":
            require(
                "FEATURE_ID" in names,
                "PORTABLE_INTERNAL_FEATURE_ID_DEFINITION_MISSING",
            )
            require(
                "FEATURE_ID" not in expected_exports,
                "PORTABLE_INTERNAL_FEATURE_ID_EXPORTED",
            )
        require(
            hashlib.sha256(path.read_bytes()).hexdigest()
            == INSTALLED_HASHES[relative],
            "PORTABLE_PUBLIC_SURFACE_INSTALLED_HASH_DRIFT:" + relative,
        )
        source = path.read_text(encoding="utf-8-sig")
        block = PUBLIC_BLOCKS[relative]
        require(
            source.count(block) == 1,
            "PORTABLE_PUBLIC_SURFACE_BLOCK_COUNT_INVALID:" + relative,
        )
        reconstructed = source.replace(block, "", 1)
        require(
            hashlib.sha256(reconstructed.encode("utf-8")).hexdigest()
            == BASELINE_HASHES[relative],
            "PORTABLE_PUBLIC_SURFACE_BASELINE_RECONSTRUCTION_DRIFT:" + relative,
        )
        require(
            len(source.splitlines()) <= 500,
            "PORTABLE_PUBLIC_SURFACE_SOURCE_EXCEEDS_500_LINES:" + relative,
        )

    print("PORTABLE SEVEN MODULE PUBLIC SURFACES: PASS")
    print("PORTABLE PUBLIC SYMBOLS DEFINED: PASS")
    print("PORTABLE INSTALLED SOURCE HASHES: PASS")
    print("PORTABLE BASELINE RECONSTRUCTION: PASS")
    print("PORTABLE PYTHON AND SIZE CONTRACT: PASS")


def validate_consumer_graph(root: Path) -> None:
    """Require all current direct consumers to use declared public symbols."""
    for relative, module_name in MODULE_NAMES.items():
        actual = imported_names(root, module_name)
        expected = set(EXPECTED_EXPORTS[relative])
        allowed_internal = INTERNAL_CONSUMER_IMPORTS.get(module_name, set())
        allowed = expected | allowed_internal
        require(
            actual.issubset(allowed),
            "PORTABLE_CONSUMER_IMPORTS_UNGOVERNED_SYMBOL:"
            + module_name
            + ":"
            + ",".join(sorted(actual - allowed)),
        )
        require(
            allowed_internal.issubset(actual),
            "PORTABLE_REQUIRED_INTERNAL_CONSUMER_IMPORT_MISSING:"
            + module_name
            + ":"
            + ",".join(sorted(allowed_internal - actual)),
        )
        require(
            REQUIRED_EXTERNAL_IMPORTS[module_name].issubset(actual),
            "PORTABLE_REQUIRED_CONSUMER_IMPORT_MISSING:"
            + module_name
            + ":"
            + ",".join(sorted(REQUIRED_EXTERNAL_IMPORTS[module_name] - actual)),
        )

    smoke_path = root / "portable/smoke_isolation.py"
    smoke_tree = ast.parse(
        smoke_path.read_text(encoding="utf-8-sig"),
        filename=str(smoke_path),
    )
    prepared = next(
        (
            node
            for node in smoke_tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "prepared_smoke_isolation"
        ),
        None,
    )
    require(prepared is not None, "PORTABLE_SMOKE_CONTEXT_MANAGER_MISSING")
    annotation = ast.unparse(prepared.returns) if prepared.returns is not None else ""
    require(
        "PreparedSmokeIsolation" in annotation,
        "PORTABLE_SMOKE_RETURN_TYPE_PUBLIC_CONTRACT_DRIFT",
    )

    print("PORTABLE CONSUMER IMPORTS GOVERNED: PASS")
    print("PORTABLE INTERNAL FEATURE ID REMAINS NONPUBLIC: PASS")
    print("PORTABLE REQUIRED CONSUMER GRAPH: PASS")
    print("PORTABLE SMOKE RETURN TYPE PUBLIC CONTRACT: PASS")
    print("PORTABLE STAR IMPORT ABSENT: PASS")


def validate_manifest(root: Path) -> None:
    """Require only the seven target member hashes to change."""
    manifest_path = root / MANIFEST_REL
    require(manifest_path.is_file(), "PORTABLE_BUILDER_MANIFEST_MISSING")
    require(
        hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        == INSTALLED_MANIFEST_SHA256,
        "PORTABLE_BUILDER_MANIFEST_INSTALLED_HASH_DRIFT",
    )
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = payload.get("files")
    require(isinstance(files, dict), "PORTABLE_BUILDER_MANIFEST_FILES_INVALID")

    for relative, installed_hash in INSTALLED_HASHES.items():
        require(
            files.get(Path(relative).name) == installed_hash,
            "PORTABLE_BUILDER_MANIFEST_TARGET_HASH_DRIFT:" + relative,
        )

    reconstructed = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative, baseline_hash in BASELINE_HASHES.items():
        reconstructed["files"][Path(relative).name] = baseline_hash
    reconstructed_bytes = (
        json.dumps(reconstructed, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    require(
        hashlib.sha256(reconstructed_bytes).hexdigest()
        == BASELINE_MANIFEST_SHA256,
        "PORTABLE_BUILDER_MANIFEST_BASELINE_RECONSTRUCTION_DRIFT",
    )

    print("PORTABLE BUILDER MANIFEST SEVEN HASHES: PASS")
    print("PORTABLE BUILDER MANIFEST UNRELATED CONTENT PRESERVED: PASS")


def run_command(
    root: Path,
    command: list[str],
    markers: tuple[str, ...],
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    """Run one command and require exit code and markers."""
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
    """Require the seven remaining public-surface warnings absent."""
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
        "Total issues: 4 | Errors: 0 | Warnings: 4 | Other: 0" in output,
        "WAVE2J_ARCHITECTURE_COUNT_UNEXPECTED",
    )
    require(
        "MISSING_PUBLIC_SURFACE_CONTROL" not in output,
        "WAVE2J_PUBLIC_SURFACE_WARNING_REMAINS",
    )

    print("WAVE2J PORTABLE PUBLIC SURFACE WARNINGS ABSENT: PASS")
    print("WAVE2J PORTABLE PUBLIC SURFACE FAMILY CLOSED: PASS")


def validate_inherited_contracts(root: Path) -> None:
    """Run exact-member governance and installed builder validation."""
    run_command(
        root,
        [
            sys.executable,
            str(
                root
                / "tools"
                / "validate_portable_exact_builder_member_governance_v1.py"
            ),
            "--project-root",
            str(root),
        ],
        (
            "PORTABLE BUILDER EXACT MEMBER CONTRACT: PASS",
            "VALIDATION OK: portable-exact-builder-member-governance-v1",
        ),
        "PORTABLE_EXACT_BUILDER_MEMBER_VALIDATION",
    )

    run_command(
        root,
        [
            sys.executable,
            str(root / "portable" / "validate_installed.py"),
            "--portable-root",
            str(root / "portable"),
        ],
        (
            "PORTABLE BUILDER PAYLOAD HASHES: PASS",
            "PORTABLE BUILDER EXACT MEMBER CONTRACT: PASS",
            "PORTABLE IDENTITY JSON RUNTIME: PASS",
            "PORTABLE PRODUCTION BUILD GATE CLOSED: PASS",
            "VALIDATION OK: kanda-reasoner-portable-timestamped-publication-name-v1r32",
        ),
        "PORTABLE_INSTALLED_BUILDER_VALIDATION",
    )

    print("PORTABLE SEVEN MODULE EXACT BUILDER CONTRACT: PASS")
    print("PORTABLE SEVEN MODULE INSTALLED BUILDER CONTRACT: PASS")
    print("PORTABLE BUILD EXECUTED BY WAVE2J VALIDATION: NO")


def main() -> int:
    """Run Wave 2J validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_sources(root)
    validate_consumer_graph(root)
    validate_manifest(root)

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
