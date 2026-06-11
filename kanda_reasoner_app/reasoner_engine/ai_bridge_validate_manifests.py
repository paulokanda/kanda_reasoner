"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

import logging

import ast
import json
import sys
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


def find_manifests(root: Path) -> list[Path]:
    return sorted(root.rglob("*_help.json"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_header_fields(path: Path) -> set[str]:
    fields: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:20]:
        stripped = line.strip()
        if stripped.startswith("#"):
            for field in HEADER_FIELDS:
                if field in stripped:
                    fields.add(field)
    return fields


def parse_module_exports(path: Path) -> tuple[list[str], set[str]]:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))

    all_exports: list[str] = []
    public_defs: set[str] = set()

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = str(node.name)
            if not name.startswith("_"):
                public_defs.add(name)

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    try:
                        value = ast.literal_eval(node.value)
                    except Exception:
                        logging.exception("Boundary failure in parse_module_exports")
                        value = None

                    if isinstance(value, (list, tuple)):
                        all_exports = [
                            str(item)
                            for item in value
                            if isinstance(item, str)
                        ]

    return all_exports, public_defs


def helper_files(help_folder: Path) -> list[Path]:
    return sorted(
        p for p in help_folder.glob("*.py")
        if p.name != "__pycache__"
    )


def has_ai_context_docstring(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    return "AI CONTEXT - REFACTORED MODULE" in text


def validate_manifest(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(manifest_path)

    origin = Path(data["origin"])
    help_folder = Path(data["help_folder"])
    helpers = data.get("helpers", {})
    dependency_graph = data.get("dependency_graph", {})

    if not origin.exists():
        errors.append(f"origin file does not exist: {origin}")

    if not help_folder.exists():
        errors.append(f"help folder does not exist: {help_folder}")
        return errors

    if not has_ai_context_docstring(origin):
        errors.append(f"origin file missing AI CONTEXT docstring: {origin}")

    existing_helper_names = {p.name for p in helper_files(help_folder)}
    declared_helper_names = set(helpers.keys())

    for helper_name in sorted(declared_helper_names):
        helper_path = help_folder / helper_name
        if not helper_path.exists():
            errors.append(f"declared helper missing on disk: {helper_name}")

    for helper_name in sorted(existing_helper_names):
        if helper_name not in declared_helper_names:
            errors.append(f"helper exists on disk but missing from manifest: {helper_name}")

    public_symbol_owner: dict[str, str] = {}

    for helper_name, helper_info in helpers.items():
        helper_path = help_folder / helper_name
        if not helper_path.exists():
            continue

        depends_on = helper_info.get("depends_on", [])
        for dep in depends_on:
            if not (help_folder / dep).exists():
                errors.append(f"depends_on target missing for {helper_name}: {dep}")

        header_fields = parse_header_fields(helper_path)
        missing_headers = [field for field in HEADER_FIELDS if field not in header_fields]
        if missing_headers:
            errors.append(
                f"helper missing header fields {helper_name}: " + ", ".join(missing_headers)
            )

        all_exports, public_defs = parse_module_exports(helper_path)
        declared_exports = helper_info.get("exports", [])

        if declared_exports and all_exports is None:
            errors.append(f"helper declares exports but is missing __all__: {helper_name}")
            continue

        if all_exports is not None and list(all_exports) != list(declared_exports):
            errors.append(
                f"manifest exports do not match __all__ for {helper_name}: "
                f"manifest={declared_exports} __all__={all_exports}"
            )

        if all_exports is not None:
            for symbol in all_exports:
                if helper_name != "__init__.py":
                    owner = public_symbol_owner.get(symbol)
                    if owner is not None:
                        errors.append(
                            f"duplicate public symbol ownership: {symbol} in {owner} and {helper_name}"
                        )
                    else:
                        public_symbol_owner[symbol] = helper_name

        graph_deps = dependency_graph.get(helper_name, [])
        if list(graph_deps) != list(depends_on):
            errors.append(
                f"dependency_graph mismatch for {helper_name}: graph={graph_deps} depends_on={depends_on}"
            )

    return errors


def main() -> int:
    root = Path(__file__).resolve().parent
    manifests = find_manifests(root)

    if not manifests:
        print("---  FAIL - no manifests found")
        return 1

    any_fail = False
    for manifest_path in manifests:
        errors = validate_manifest(manifest_path)
        if errors:
            any_fail = True
            print(f"---  FAIL - {manifest_path}")
            for error in errors:
                print(f"     --- {error}")
        else:
            print(f"--...  PASS - {manifest_path}")

    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
