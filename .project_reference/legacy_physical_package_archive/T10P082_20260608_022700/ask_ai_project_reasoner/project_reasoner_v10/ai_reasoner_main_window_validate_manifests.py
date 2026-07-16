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


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _find_manifests(project_root: Path) -> list[Path]:
    return sorted(project_root.rglob("*_help.json"))


def _parse_python_all(path: Path) -> tuple[list[str] | None, list[str]]:
    text = _read_text(path)
    errors: list[str] = []
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return None, [f"SyntaxError in {path}: {exc}"]

    found = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = node.targets
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    names = []
                    ok = True
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            names.append(elt.value)
                        else:
                            ok = False
                    if ok:
                        found = names
                    else:
                        errors.append(f"__all__ in {path} must contain only string literals.")
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    names = []
                    ok = True
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            names.append(elt.value)
                        else:
                            ok = False
                    if ok:
                        found = names
                    else:
                        errors.append(f"__all__ in {path} must contain only string literals.")
    return found, errors


def _header_errors(path: Path) -> list[str]:
    text = _read_text(path)
    return [f"Missing header field '{field}' in {path.name}." for field in HEADER_FIELDS if field not in text]


def _origin_docstring_errors(origin_path: Path) -> list[str]:
    text = _read_text(origin_path)
    if "AI CONTEXT" not in text or "REFACTORED MODULE" not in text:
        return [f"Origin file {origin_path.name} is missing AI CONTEXT docstring."]
    return []


def _iter_helper_files(help_folder: Path) -> list[Path]:
    return [path for path in sorted(help_folder.glob("*.py")) if path.is_file()]


def _check_manifest(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(_read_text(manifest_path))
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in {manifest_path}: {exc}"]

    origin = Path(manifest.get("origin", ""))
    help_folder = Path(manifest.get("help_folder", ""))
    helpers = manifest.get("helpers", {})
    dependency_graph = manifest.get("dependency_graph", {})

    if not origin.exists():
        errors.append(f"Origin file does not exist: {origin}")
    if not help_folder.exists():
        errors.append(f"Help folder does not exist: {help_folder}")
        return errors

    helper_files = [path.name for path in _iter_helper_files(help_folder)]
    manifest_helper_names = sorted(helpers.keys())

    for helper_name in manifest_helper_names:
        helper_path = help_folder / helper_name
        if not helper_path.exists():
            errors.append(f"Helper listed in manifest is missing: {helper_path}")

    for helper_name in helper_files:
        if helper_name not in helpers:
            errors.append(f"Helper file not listed in manifest: {helper_name}")

    for helper_name, meta in helpers.items():
        helper_path = help_folder / helper_name
        if not helper_path.exists():
            continue

        errors.extend(_header_errors(helper_path))
        all_names, all_errors = _parse_python_all(helper_path)
        errors.extend(all_errors)

        exports = meta.get("exports", [])
        if exports and all_names is None:
            errors.append(f"Missing __all__ in {helper_name} despite manifest exports.")
        if all_names is not None and list(exports) != list(all_names):
            errors.append(f"Manifest exports mismatch in {helper_name}: manifest={exports} file={all_names}")

        depends_on = meta.get("depends_on", [])
        for dep in depends_on:
            dep_path = help_folder / dep
            if not dep_path.exists():
                errors.append(f"Dependency listed in manifest for {helper_name} is missing: {dep}")

        graph_deps = dependency_graph.get(helper_name, [])
        if list(graph_deps) != list(depends_on):
            errors.append(f"dependency_graph mismatch for {helper_name}: graph={graph_deps} depends_on={depends_on}")

    if origin.exists():
        errors.extend(_origin_docstring_errors(origin))
        origin_all, origin_all_errors = _parse_python_all(origin)
        errors.extend(origin_all_errors)
        if origin_all is None:
            errors.append(f"Origin file {origin.name} is missing __all__.")

    return errors


def main() -> int:
    project_root = Path(__file__).resolve().parent
    manifests = _find_manifests(project_root)
    if not manifests:
        print("FAIL - no *_help.json manifests found")
        return 1

    any_fail = False
    for manifest_path in manifests:
        errors = _check_manifest(manifest_path)
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






