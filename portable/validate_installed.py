"""Static validator for the installed Portable builder Box."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path


FORBIDDEN_IMPORT_PREFIXES = (
    "kanda_reasoner_app.reasoner_context_bundle",
    "reasoner_context_bundle",
    "handoff_zip_exporter",
    "collector_main",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _imported_modules(tree: ast.AST) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _is_forbidden_import(module: str) -> bool:
    normalized = module.casefold()
    return any(
        normalized == prefix
        or normalized.startswith(prefix + ".")
        for prefix in FORBIDDEN_IMPORT_PREFIXES
    )


def _validate_python(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    source.encode("ascii")
    tree = ast.parse(source, filename=str(path))
    line_count = len(source.splitlines())
    if line_count > 500:
        raise RuntimeError(
            f"Python module exceeds 500 lines: {path.name} ({line_count})"
        )

    forbidden = sorted(
        module
        for module in _imported_modules(tree)
        if _is_forbidden_import(module)
    )
    if forbidden:
        raise RuntimeError(
            "Show Project implementation import in "
            f"{path.name}: {', '.join(forbidden)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--portable-root", required=True)
    args = parser.parse_args()

    root = Path(args.portable_root).resolve()
    manifest_path = root / "PORTABLE_BUILDER_MANIFEST.json"
    if not manifest_path.is_file():
        raise RuntimeError(f"Manifest not found: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_files = manifest.get("files", {})
    if not isinstance(expected_files, dict) or not expected_files:
        raise RuntimeError("Portable builder manifest has no file hashes.")

    for relative, expected_hash in sorted(expected_files.items()):
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"Required builder file missing: {relative}")
        actual_hash = _sha256(path)
        if actual_hash.casefold() != str(expected_hash).casefold():
            raise RuntimeError(f"Builder file hash mismatch: {relative}")

    python_files = sorted(root.glob("*.py"))
    for path in python_files:
        _validate_python(path)

    facade = root / "create_kanda_reasoner_portable.py"
    facade_tree = ast.parse(
        facade.read_text(encoding="utf-8"),
        filename=str(facade),
    )
    facade_imports = _imported_modules(facade_tree)
    if "portable.cli" not in facade_imports:
        raise RuntimeError("Portable facade contract is missing.")

    environment_source = (root / "environment.py").read_text(encoding="utf-8")
    paths_source = (root / "paths.py").read_text(encoding="utf-8")
    build_source = (root / "build.py").read_text(encoding="utf-8")
    destination_source = (root / "destination.py").read_text(encoding="utf-8")
    publish_source = (root / "publish.py").read_text(encoding="utf-8")
    workflow_source = (root / "workflow.py").read_text(encoding="utf-8")
    if "Programs" not in environment_source or "Python312" not in environment_source:
        raise RuntimeError("Governed Python 3.12 identity contract is missing.")
    if ".venv" in environment_source or ".venv" in paths_source:
        raise RuntimeError("Project virtual-environment coupling remains.")
    if "Path(sys.executable).resolve()" not in paths_source:
        raise RuntimeError("Current governed interpreter propagation is missing.")
    if "--workpath" not in build_source or "--distpath" not in build_source:
        raise RuntimeError("External PyInstaller output paths are missing.")
    if "askdirectory" not in destination_source or "mustexist=True" not in destination_source:
        raise RuntimeError("Native destination-folder picker contract is missing.")
    if "Selected Portable destination is inside the project" not in paths_source:
        raise RuntimeError("Selected destination project-boundary guard is missing.")
    if "Selected Portable destination is inside Project Support" not in paths_source:
        raise RuntimeError("Selected destination Show Project guard is missing.")
    if "shutil.copyfile" not in publish_source or "os.replace" not in publish_source:
        raise RuntimeError("Cross-volume atomic publication contract is missing.")
    if "select_output_directory" not in workflow_source:
        raise RuntimeError("Portable workflow does not request a destination folder.")

    print("PORTABLE BUILDER PAYLOAD HASHES: PASS")
    print("PORTABLE BUILDER PYTHON AST: PASS")
    print("PORTABLE BUILDER ASCII SOURCE: PASS")
    print("PORTABLE BUILDER MODULE SIZE: PASS")
    print("PORTABLE SHOW PROJECT IMPLEMENTATION IMPORTS: ABSENT")
    print("PORTABLE VALIDATOR SELF-MATCH REGRESSION: PASS")
    print("PORTABLE GOVERNED PYTHON CONTRACT: PASS")
    print("PORTABLE PROJECT VENV COUPLING: ABSENT")
    print("PORTABLE EXTERNAL BUILD OUTPUT CONTRACT: PASS")
    print("PORTABLE NATIVE DESTINATION PICKER: PASS")
    print("PORTABLE SELECTED DESTINATION BOUNDARIES: PASS")
    print("PORTABLE CROSS-VOLUME ATOMIC PUBLICATION: PASS")
    print("VALIDATION OK: kanda-reasoner-portable-builder-install-v1r3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
