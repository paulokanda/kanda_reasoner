"""Validate the import-safe Portable facade entry point."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

FEATURE_ID = 'architecture-portable-facade-entrypoint-wave2i-v1'
FACADE_REL = Path('portable/create_kanda_reasoner_portable.py')
MANIFEST_REL = Path('portable/PORTABLE_BUILDER_MANIFEST.json')
EXPECTED_FACADE_SHA256 = 'e8d51230b3cd84c33d6a614aaf44938362068ded878058c0f3b53e07b3d9f6b6'
EXPECTED_MANIFEST_SHA256 = '7d8a5c42c7ede4cae71e4a3705f93ad54011489d877d89d7e2ff9bed80d2cb7d'
BASELINE_FACADE_SHA256 = '75d0f901e3fd302aaa4cdf23c3cd9ba09b4eb4b9a6cef7896a0346c1bbf1dace'
BASELINE_MANIFEST_SHA256 = 'c1c0013e9925039bb688e13532a6f279a2ee00053bb0d55047813b3a82022eaa'
EXPECTED_EXPORTS = ["main"]
EXPECTED_UNRELATED_MEMBER_HASHES = {'KANDA_REASONER_PORTABLE_WINDOWS_CURRENT_HANDOFF.md': '30a5527421e5f392ff0d6fbad84b20c5ba747c5a0a65b200587486760f4e88d2', 'PORTABLE_EXTERNAL_BUILD_CONTROLS.json': 'c76d490dc94cc3dd5af0b1b1c3e8014369ad8b849eb262311b86fabd7fd6536a', 'PORTABLE_RUNTIME_ALLOWLIST.json': '3edc2dc542d24b222384267a4d52f6e19b7cc959dc332bc36a259c7ce8a7a2a7', 'README.md': '30a5527421e5f392ff0d6fbad84b20c5ba747c5a0a65b200587486760f4e88d2', '__init__.py': '064b79009644d2047be5c87ab8e64a7cb567effffb2424d2bddac66db8445a46', 'archive.py': '4c7611f0a7f21f3d2752b873471d4810ee09f927bf56a4835296c911b8c97fba', 'build.py': 'ddf7cec25fad2841f76a28d84a8ea52217edd6cda5c6b4b7322dc380e86492fd', 'builder_members.py': 'cb744eeb0d201234dfe6c1ec229e6b061f6b2f77043551dd7dcabeb10aec8596', 'cli.py': '3243f22303b5c37a698a325db301e744f688dbe192dc32a991f7147d2ce8d5cf', 'constants.py': 'bbd25636d6b540f799b5b794240663f928ff3fcc7060224881da79fcc915f1c4', 'create_windows_zip.ps1': '12734ab36903620dab30212ac8e47fa9b542114e30aba96f82fee0dc412836b2', 'destination.py': '217dee093d0c63a7f179947f61f2843e972f84076b82cca91c07ad1009821b4d', 'environment.py': '7e3cb2814c286a44c51014d95ed80fa77f0c448df52669999dfbf3bc8e900ced', 'errors.py': 'febe2f4b0698060eff26f6606e1bfed66172f5dcdb36fad5879e5e5fd7edce2b', 'external_controls.py': 'b6136e45b1806e17ca6cb7eada59e070c1044209da0c20b9c1031e42ed9f7390', 'governed_root_rollback.py': 'd4d0466076bc3c5cc921b52499d4543681d2209674b6a930dbb17b01ae1375ee', 'models.py': '6ffd84b50c0ccb5ffd3b72fabb330291372c6bc594b435e7fe8f27f76e02537c', 'paths.py': '185399c0c9d07b34ec12d391419d0ecf3d91125971bef03d6cdf8d6f04e9eef5', 'physical_runtime.py': '04be54a006086136b8605243e87f14d674de917ab4ec7eeb7597ae34d426e66c', 'physical_runtime_validation.py': '9b3df528b2900473774665e88a85db753c9652197e5b9b6ca1848c3f527f5f5d', 'policy.py': '81dfa2ee91f9616811d70d7e4f2acb481a9c2557f24fac2482880a14461b72a7', 'publish.py': 'ce80be4428c75cf08eb61998717556c04c29247d9f048f9453cb7963eab481a7', 'registry_boundary.py': '5f4934212b4d876933bbbb467ce502178f1ea8106d05541b5cae161a03dbdd23', 'smoke_isolation.py': 'b8c7f8f07afff0370955874666a7532affcd7b54831c838158d160c2c42714f1', 'snapshots.py': 'fa9fce7b111832a1057f817b379522ba8be25882704e1577f7fa60dc6c1a6581', 'validate_installed.py': 'fc81d4a3e5c695efb50bfab18c27b88323e8a60aa58092a492b19e7dbbb526c0', 'workflow.py': 'dccf38002f4587a1b8c4daa9a140acc5294f8141229e1587bd60200168c763d0'}


def require(condition: bool, code: str) -> None:
    """Raise one deterministic validation error."""
    if not condition:
        raise RuntimeError(code)


def literal_all(tree: ast.Module) -> list[str] | None:
    """Return one literal module __all__ declaration."""
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


def function_node(tree: ast.Module, name: str) -> ast.FunctionDef | None:
    """Return one top-level function by name."""
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def top_level_side_effects(tree: ast.Module) -> list[str]:
    """Return forbidden import-time process mutations."""
    issues: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, ast.If):
            rendered = ast.unparse(node.test)
            if "__name__" in rendered and "__main__" in rendered:
                continue
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                call = ast.unparse(child.func)
                if call in {"sys.path.insert", "sys.path.append", "sys.path.extend"}:
                    issues.append(call)
            if isinstance(child, (ast.Assign, ast.AnnAssign)):
                targets = (
                    list(child.targets)
                    if isinstance(child, ast.Assign)
                    else [child.target]
                )
                for target in targets:
                    if ast.unparse(target) == "sys.dont_write_bytecode":
                        issues.append("sys.dont_write_bytecode")
    return sorted(set(issues))


def direct_portable_cli_imports(tree: ast.Module) -> list[str]:
    """Return top-level portable.cli imports."""
    imports: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "portable.cli":
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.Import):
            imports.extend(
                alias.name
                for alias in node.names
                if alias.name == "portable.cli"
            )
    return imports


def main_contract(main_node: ast.FunctionDef) -> None:
    """Require local bootstrap and lazy canonical CLI delegation."""
    source = ast.unparse(main_node)
    required = (
        "sys.dont_write_bytecode = True",
        "Path(__file__).resolve().parents[1]",
        "sys.path.insert(0, project_root_text)",
        "from portable.cli import main as cli_main",
        "return cli_main(project_root=project_root)",
    )
    for token in required:
        require(token in source, "PORTABLE_FACADE_MAIN_CONTRACT_DRIFT:" + token)


def main_guard_contract(tree: ast.Module) -> None:
    """Require one canonical executable main guard."""
    matching: list[ast.If] = []
    for node in tree.body:
        if not isinstance(node, ast.If):
            continue
        rendered = ast.unparse(node.test)
        if "__name__" in rendered and "__main__" in rendered:
            matching.append(node)
    require(len(matching) == 1, "PORTABLE_FACADE_MAIN_GUARD_COUNT_INVALID")
    body = ast.unparse(matching[0])
    require(
        "raise SystemExit(main())" in body,
        "PORTABLE_FACADE_MAIN_GUARD_DRIFT",
    )


def validate_source(root: Path) -> None:
    """Validate exact source, AST ownership, and import-time safety."""
    facade = root / FACADE_REL
    manifest = root / MANIFEST_REL
    require(facade.is_file(), "PORTABLE_FACADE_MISSING")
    require(manifest.is_file(), "PORTABLE_BUILDER_MANIFEST_MISSING")

    require(
        hashlib.sha256(facade.read_bytes()).hexdigest()
        == EXPECTED_FACADE_SHA256,
        "PORTABLE_FACADE_INSTALLED_HASH_DRIFT",
    )
    require(
        hashlib.sha256(manifest.read_bytes()).hexdigest()
        == EXPECTED_MANIFEST_SHA256,
        "PORTABLE_BUILDER_MANIFEST_INSTALLED_HASH_DRIFT",
    )

    tree = ast.parse(
        facade.read_text(encoding="utf-8-sig"),
        filename=str(facade),
    )
    require(
        literal_all(tree) == EXPECTED_EXPORTS,
        "PORTABLE_FACADE_PUBLIC_SURFACE_DRIFT",
    )
    main_node = function_node(tree, "main")
    require(main_node is not None, "PORTABLE_FACADE_MAIN_MISSING")
    require(
        top_level_side_effects(tree) == [],
        "PORTABLE_FACADE_IMPORT_SIDE_EFFECT_REMAINS",
    )
    require(
        direct_portable_cli_imports(tree) == [],
        "PORTABLE_FACADE_EAGER_CLI_IMPORT_REMAINS",
    )
    main_contract(main_node)
    main_guard_contract(tree)

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    files = payload.get("files")
    require(isinstance(files, dict), "PORTABLE_BUILDER_MANIFEST_FILES_INVALID")
    require(
        files.get("create_kanda_reasoner_portable.py")
        == EXPECTED_FACADE_SHA256,
        "PORTABLE_BUILDER_MANIFEST_FACADE_HASH_DRIFT",
    )
    unrelated = {
        member: digest
        for member, digest in files.items()
        if member != "create_kanda_reasoner_portable.py"
    }
    require(
        unrelated == EXPECTED_UNRELATED_MEMBER_HASHES,
        "PORTABLE_BUILDER_MANIFEST_UNRELATED_MEMBER_DRIFT",
    )

    require(
        len(facade.read_text(encoding="utf-8-sig").splitlines()) <= 100,
        "PORTABLE_FACADE_SIZE_CONTRACT_DRIFT",
    )
    require(
        len(Path(__file__).read_text(encoding="utf-8-sig").splitlines()) <= 500,
        "WAVE2I_VALIDATOR_SIZE_CONTRACT_DRIFT",
    )

    print("PORTABLE FACADE EXPLICIT PUBLIC ENTRYPOINT: PASS")
    print("PORTABLE FACADE IMPORT-TIME SIDE EFFECTS ABSENT: PASS")
    print("PORTABLE FACADE EAGER CLI IMPORT ABSENT: PASS")
    print("PORTABLE FACADE LAZY CLI DELEGATION: PASS")
    print("PORTABLE FACADE MAIN GUARD: PASS")
    print("PORTABLE BUILDER MANIFEST FACADE HASH: PASS")
    print("PORTABLE BUILDER MANIFEST UNRELATED HASHES PRESERVED: PASS")
    print("WAVE2I PYTHON JSON AND SIZE CONTRACT: PASS")


def run_command(
    root: Path,
    command: list[str],
    markers: tuple[str, ...],
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    """Run one command and require its exit code and markers."""
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


def validate_import_isolation(root: Path) -> None:
    """Prove importing the facade does not mutate bootstrap state."""
    script = r"""
import importlib.util
import json
import sys
from pathlib import Path

path = Path(sys.argv[1]).resolve()
before_path = list(sys.path)
before_bytecode = sys.dont_write_bytecode
spec = importlib.util.spec_from_file_location("wave2i_facade_import_probe", path)
if spec is None or spec.loader is None:
    raise RuntimeError("FACADE_SPEC_FAILED")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(json.dumps({
    "path_unchanged": sys.path == before_path,
    "bytecode_unchanged": sys.dont_write_bytecode == before_bytecode,
    "exports": list(module.__all__),
    "main_callable": callable(module.main),
}, sort_keys=True))
"""
    output = run_command(
        root,
        [sys.executable, "-c", script, str(root / FACADE_REL)],
        (),
        "PORTABLE_FACADE_IMPORT_PROBE",
        timeout=120,
    )
    lines = [line for line in output.splitlines() if line.strip().startswith("{")]
    require(len(lines) == 1, "PORTABLE_FACADE_IMPORT_PROBE_JSON_COUNT")
    payload = json.loads(lines[0])
    require(payload.get("path_unchanged") is True, "PORTABLE_FACADE_IMPORT_MUTATED_PATH")
    require(
        payload.get("bytecode_unchanged") is True,
        "PORTABLE_FACADE_IMPORT_MUTATED_BYTECODE_POLICY",
    )
    require(payload.get("exports") == EXPECTED_EXPORTS, "PORTABLE_FACADE_RUNTIME_EXPORT_DRIFT")
    require(payload.get("main_callable") is True, "PORTABLE_FACADE_RUNTIME_MAIN_NOT_CALLABLE")
    print("PORTABLE FACADE IMPORT PROCESS STATE UNCHANGED: PASS")


def validate_identity(root: Path) -> None:
    """Run the facade's no-build identity command."""
    output = run_command(
        root,
        [
            sys.executable,
            str(root / FACADE_REL),
            "--identity-json",
        ],
        (),
        "PORTABLE_FACADE_IDENTITY_COMMAND",
        timeout=120,
    )
    lines = [line for line in output.splitlines() if line.strip().startswith("{")]
    require(len(lines) == 1, "PORTABLE_FACADE_IDENTITY_JSON_COUNT")
    payload = json.loads(lines[0])
    require(payload.get("schema_version") == "1.0", "PORTABLE_FACADE_IDENTITY_SCHEMA_DRIFT")
    require(
        payload.get("feature_id")
        == "kanda-reasoner-portable-builder-install-v1r12",
        "PORTABLE_FACADE_IDENTITY_FEATURE_DRIFT",
    )
    require(
        payload.get("production_portable_enabled") is False,
        "PORTABLE_FACADE_IDENTITY_PRODUCTION_GATE_DRIFT",
    )
    print("PORTABLE FACADE IDENTITY COMMAND: PASS")
    print("PORTABLE BUILD EXECUTED BY WAVE2I VALIDATION: NO")


def validate_architecture(root: Path) -> None:
    """Require all three facade architecture warnings absent."""
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
        "Total issues: 11 | Errors: 0 | Warnings: 11 | Other: 0" in output,
        "WAVE2I_ARCHITECTURE_COUNT_UNEXPECTED",
    )
    path = FACADE_REL.as_posix()
    for code in (
        "DEAD_CODE_UNREACHABLE_FILE",
        "PROJECT_WIDE_AI_CONFUSION",
        "SIDE_EFFECT_ON_IMPORT",
    ):
        require(
            code + " " + path not in output,
            "WAVE2I_FACADE_WARNING_REMAINS:" + code,
        )
    print("WAVE2I PORTABLE FACADE DEAD CODE WARNING ABSENT: PASS")
    print("WAVE2I PORTABLE FACADE SIDE EFFECT WARNING ABSENT: PASS")
    print("WAVE2I PORTABLE FACADE AI CONFUSION WARNING ABSENT: PASS")
    print("WAVE2I PORTABLE FACADE WARNING FAMILY CLOSED: PASS")


def validate_inherited_contracts(root: Path) -> None:
    """Run exact builder-member and installed-builder validators."""
    run_command(
        root,
        [
            sys.executable,
            str(root / "tools/validate_portable_exact_builder_member_governance_v1.py"),
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
            str(root / "portable/validate_installed.py"),
            "--portable-root",
            str(root / "portable"),
        ],
        (
            "PORTABLE IDENTITY JSON RUNTIME: PASS",
            "PORTABLE BUILDER EXACT MEMBER CONTRACT: PASS",
            "VALIDATION OK: kanda-reasoner-portable-timestamped-publication-name-v1r32",
        ),
        "PORTABLE_INSTALLED_BUILDER_VALIDATION",
    )

    print("PORTABLE FACADE EXACT BUILDER MEMBER CONTRACT: PASS")
    print("PORTABLE FACADE INSTALLED BUILDER CONTRACT: PASS")


def main() -> int:
    """Run Wave 2I validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_source(root)
    validate_import_isolation(root)
    validate_identity(root)

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
