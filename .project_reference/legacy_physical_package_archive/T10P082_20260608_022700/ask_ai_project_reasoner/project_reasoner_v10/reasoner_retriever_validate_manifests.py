"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

import ast
import json
from pathlib import Path

HEADER_FIELDS = [
    "MODULE ORIGIN",
    "MANIFEST",
    "HELP FOLDER",
    "PURPOSE",
    "EXPORTS",
    "DEPENDS ON",
    "REFACTOR DATE",
]

IGNORED_DIR_NAMES = {
    "__pycache__",
    ".git",
    ".idea",
    ".venv",
    "venv",
    "env",
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _load_json(path: Path) -> dict:
    return json.loads(_read_text(path))


def _extract_all(path: Path) -> list[str] | None:
    tree = ast.parse(_read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return list(ast.literal_eval(node.value))
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                return list(ast.literal_eval(node.value))
    return None


def _has_ai_context_docstring(path: Path) -> bool:
    text = _read_text(path)
    return "AI CONTEXT" in text and "REFACTORED MODULE" in text


def _has_header_fields(path: Path) -> list[str]:
    text = _read_text(path)
    return [field for field in HEADER_FIELDS if field not in text]


def _iter_manifest_paths(project_root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in project_root.rglob("*_help.json"):
        if any(part in IGNORED_DIR_NAMES for part in path.parts):
            continue
        paths.append(path)
    return sorted(paths)


def _helper_files(help_folder: Path) -> list[Path]:
    if not help_folder.exists():
        return []
    return sorted(
        path
        for path in help_folder.iterdir()
        if path.is_file() and path.suffix == ".py"
    )


def _validate_manifest(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    manifest = _load_json(manifest_path)

    origin = Path(manifest["origin"])
    help_folder = Path(manifest["help_folder"])
    helpers = manifest.get("helpers", {})
    dependency_graph = manifest.get("dependency_graph", {})

    if not origin.exists():
        errors.append(f"Missing origin file: {origin}")
    elif not _has_ai_context_docstring(origin):
        errors.append(f"Missing AI CONTEXT docstring in origin: {origin}")

    if not help_folder.exists():
        errors.append(f"Missing help folder: {help_folder}")
        return errors

    actual_files = {path.name for path in _helper_files(help_folder)}
    manifest_files = set(helpers.keys())

    for filename in sorted(manifest_files - actual_files):
        errors.append(f"Manifest lists missing helper file: {filename}")

    for filename in sorted(actual_files - manifest_files):
        errors.append(f"Helper file missing from manifest: {filename}")

    public_symbol_owners: dict[str, str] = {}

    for filename, meta in helpers.items():
        helper_path = help_folder / filename
        if not helper_path.exists():
            continue

        missing_fields = _has_header_fields(helper_path)
        if missing_fields:
            errors.append(
                f"Missing header fields in {filename}: {', '.join(missing_fields)}"
            )

        declared_depends = list(meta.get("depends_on", []))
        graph_depends = list(dependency_graph.get(filename, []))
        if declared_depends != graph_depends:
            errors.append(
                f"dependency_graph mismatch for {filename}: "
                f"helpers.depends_on={declared_depends} dependency_graph={graph_depends}"
            )

        for dep in declared_depends:
            if not (help_folder / dep).exists():
                errors.append(f"Missing depends_on target for {filename}: {dep}")

        file_all = _extract_all(helper_path)
        manifest_exports = list(meta.get("exports", []))

        if file_all is None:
            errors.append(f"Missing __all__ in {filename} despite manifest exports.")
            continue

        if file_all != manifest_exports:
            errors.append(
                f"Manifest exports mismatch in {filename}: "
                f"manifest={manifest_exports} file={file_all}"
            )

        for symbol in file_all:
            owner = public_symbol_owners.get(symbol)
            if owner and owner != filename:
                errors.append(
                    f"Duplicate public symbol '{symbol}' in {owner} and {filename}"
                )
            public_symbol_owners[symbol] = filename

    if origin.exists() and _extract_all(origin) is None:
        errors.append(f"Missing __all__ in origin: {origin}")

    return errors


def main() -> int:
    project_root = Path(__file__).resolve().parent
    manifests = _iter_manifest_paths(project_root)

    if not manifests:
        print("FAIL - no *_help.json manifests found")
        return 1

    any_fail = False
    for manifest_path in manifests:
        errors = _validate_manifest(manifest_path)
        if errors:
            any_fail = True
            print(f"FAIL - {manifest_path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS - {manifest_path}")

    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())






