#!/usr/bin/env python3
"""Project architecture scanner, validator, diff generator, and writer.

This tool scans Python modules, builds an architecture manifest, validates
helper/refactor conventions, and optionally writes derived project artifacts.
"""
from __future__ import annotations

import argparse
import ast
import difflib
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".coverage", "htmlcov", "build", "dist", "node_modules",
    ".venv", "venv", "env",
    "tests", "test",
}

EXCLUDED_FILES = {
    "check_runtime_trace_schema.py",
    "migration_auditor_01.py",
    "migration_auditor_v2.py",
    "migration_auditor_v2_no_emoji.py",
    "migration_auditor_v2_no_emoji_placeholders.py",
    "migration_import_rewriter.py",
    "remaining_legacy_import_scanner.py",
}

EXCLUDED_DUPLICATE_DIR_PREFIXES = ()

EXCLUDED_DUPLICATE_SYMBOLS = {
    "main",
}

STRUCTURED_DOC_KEYS = (
    "PROJECT", "PACKAGE", "FILE", "PREFIX", "OWNS",
    "EXPOSES", "EXPORTS", "DEPENDS", "USED BY", "SEE ALSO",
)


@dataclass(slots=True)
class ValidationIssue:
    level: str
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "level": self.level,
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }


@dataclass(slots=True)
class ModuleInfo:
    module_id: str
    package: str
    path: str
    filename: str
    is_init: bool
    is_helper: bool
    helper_group: str | None
    line_count: int
    docstring: str
    doc_meta: dict[str, str]
    imports: list[str] = field(default_factory=list)
    public_symbols: list[str] = field(default_factory=list)
    has_explicit_all: bool = False
    all_symbols: list[str] = field(default_factory=list)
    direct_internal_imports: list[str] = field(default_factory=list)
    used_by: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "module_id": self.module_id,
            "package": self.package,
            "path": self.path,
            "filename": self.filename,
            "is_init": self.is_init,
            "is_helper": self.is_helper,
            "helper_group": self.helper_group,
            "line_count": self.line_count,
            "doc_meta": self.doc_meta,
            "imports": self.imports,
            "public_symbols": self.public_symbols,
            "has_explicit_all": self.has_explicit_all,
            "all_symbols": self.all_symbols,
            "direct_internal_imports": self.direct_internal_imports,
            "used_by": self.used_by,
        }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text_if_changed(path: Path, content: str) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def should_skip_dir(path: Path) -> bool:
    return path.name in DEFAULT_EXCLUDE_DIRS


def iter_python_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        path_obj = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not should_skip_dir(path_obj / d)]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            if filename in EXCLUDED_FILES:
                continue
            yield path_obj / filename


def to_module_id(root: Path, path: Path) -> str:
    rel = path.relative_to(root)
    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def package_for_module(module_id: str, is_init: bool) -> str:
    if is_init:
        return module_id
    return module_id.rsplit(".", 1)[0] if "." in module_id else ""


def package_for_relative_imports(module_id: str, is_init: bool) -> str:
    """Return the package context used to resolve relative imports."""
    if is_init:
        return module_id
    return module_id.rpartition(".")[0]


def resolve_imported_module(
    *,
    current_module_id: str,
    is_init: bool,
    level: int,
    imported_module: str | None,
) -> str | None:
    """Resolve an ImportFrom target to an absolute module id."""
    if level == 0:
        return imported_module

    base_package = package_for_relative_imports(current_module_id, is_init)
    if not base_package:
        return imported_module

    parts = base_package.split(".")
    up = level - 1
    if up:
        if up > len(parts):
            return None
        parts = parts[:-up]

    if imported_module:
        parts.extend(imported_module.split("."))

    return ".".join(part for part in parts if part)


def parse_structured_doc_meta(docstring: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    if not docstring:
        return meta
    for raw_line in docstring.splitlines():
        line = raw_line.strip()
        for key in STRUCTURED_DOC_KEYS:
            for prefix in (f"{key}  :", f"{key}:"):
                if line.startswith(prefix):
                    meta[key] = line[len(prefix):].strip()
                    break
    return meta


def literal_str_list(node: ast.AST) -> list[str] | None:
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        values: list[str] = []
        for elt in node.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                values.append(elt.value)
            else:
                return None
        return values
    return None


def extract_explicit_all(tree: ast.Module) -> list[str] | None:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return literal_str_list(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "__all__":
                return literal_str_list(node.value)
    return None


def extract_assigned_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    if isinstance(node, ast.Name):
        names.add(node.id)
    elif isinstance(node, (ast.Tuple, ast.List)):
        for elt in node.elts:
            names.update(extract_assigned_names(elt))
    return names


def collect_top_level_names(tree: ast.Module) -> tuple[set[str], set[str]]:
    defined_names: set[str] = set()
    imported_names: set[str] = set()

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name.split(".")[0])

        elif isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            defined_names.add(node.name)

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                defined_names.update(extract_assigned_names(target))

        elif isinstance(node, ast.AnnAssign):
            defined_names.update(extract_assigned_names(node.target))

    return defined_names, imported_names


def extract_public_symbols(tree: ast.Module) -> tuple[list[str], list[str], bool]:
    explicit_all = extract_explicit_all(tree)
    defined_names, imported_names = collect_top_level_names(tree)

    if explicit_all is not None:
        public_symbols = sorted(dict.fromkeys(explicit_all))
        return public_symbols, sorted(defined_names), True

    public_symbols = sorted(
        name
        for name in defined_names
        if not name.startswith("_")
        and name not in imported_names
        and name != "__all__"
    )
    return public_symbols, sorted(defined_names), False


def determine_helper_group(path: Path) -> tuple[bool, str | None]:
    parent_name = path.parent.name
    if parent_name.endswith("_help"):
        return True, parent_name[:-5]
    return False, None


def project_top_level_names(root: Path) -> set[str]:
    return {p.name for p in root.iterdir() if p.is_dir()}


def scan_module(root: Path, path: Path, top_names: set[str]) -> ModuleInfo:
    text = read_text(path)
    tree = ast.parse(text, filename=str(path))
    module_id = to_module_id(root, path)
    is_init = path.name == "__init__.py"
    package = package_for_module(module_id, is_init)
    docstring = ast.get_docstring(tree) or ""
    doc_meta = parse_structured_doc_meta(docstring)
    is_helper, helper_group = determine_helper_group(path)

    imports: list[str] = []
    internal_imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
                if alias.name.split(".")[0] in top_names:
                    internal_imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            resolved = resolve_imported_module(
                current_module_id=module_id,
                is_init=is_init,
                level=node.level,
                imported_module=node.module,
            )
            if resolved:
                imports.append(resolved)
                if resolved.split(".")[0] in top_names:
                    internal_imports.append(resolved)

    public_symbols, all_symbols, has_explicit_all = extract_public_symbols(tree)

    return ModuleInfo(
        module_id=module_id,
        package=package,
        path=str(path.relative_to(root)).replace("\\", "/"),
        filename=path.name,
        is_init=is_init,
        is_helper=is_helper,
        helper_group=helper_group,
        line_count=len(text.splitlines()),
        docstring=docstring,
        doc_meta=doc_meta,
        imports=sorted(set(imports)),
        public_symbols=public_symbols,
        has_explicit_all=has_explicit_all,
        all_symbols=all_symbols,
        direct_internal_imports=sorted(set(internal_imports)),
    )


def build_reverse_dependencies(modules: dict[str, ModuleInfo]) -> None:
    for info in modules.values():
        info.used_by.clear()
    for mod in modules.values():
        for dep in mod.direct_internal_imports:
            if dep in modules:
                modules[dep].used_by.append(mod.module_id)
    for info in modules.values():
        info.used_by = sorted(set(info.used_by))


def helper_main_module_id(module: ModuleInfo) -> str | None:
    if not module.is_helper or not module.helper_group:
        return None
    helper_dir = Path(module.path).parent.parent
    main_path = helper_dir / f"{module.helper_group}.py"
    return ".".join(list(main_path.with_suffix("").parts)) if main_path.exists() else None



def is_test_path(path_text: str) -> bool:
    normalized = str(path_text).replace("\\", "/").lstrip("./")
    return normalized.startswith("tests/") or normalized.startswith("test/")


def declared_public_symbols(module: ModuleInfo) -> list[str]:
    raw = module.doc_meta.get("EXPOSES", "") or module.doc_meta.get("EXPORTS", "")
    return [s.strip() for s in raw.split(",") if s.strip()]


def is_generated_bundle_artifact(module: ModuleInfo) -> bool:
    normalized_path = module.path.replace("\\", "/")
    return any(part.endswith("_refactor_bundle") for part in normalized_path.split("/"))


def is_validator_script(module: ModuleInfo) -> bool:
    return module.filename.endswith("_validate_manifests.py")


def is_excluded_from_duplicate_checks(module: ModuleInfo) -> bool:
    normalized_path = module.path.replace("\\", "/")
    if is_validator_script(module):
        return True
    if is_generated_bundle_artifact(module):
        return True
    if not module.has_explicit_all:
        return True
    for prefix in EXCLUDED_DUPLICATE_DIR_PREFIXES:
        if normalized_path.startswith(prefix):
            return True
    return False


def validate_modules(root: Path, modules: dict[str, ModuleInfo]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for module in modules.values():
        path = module.path

        if not module.docstring and not is_test_path(path):
            issues.append(ValidationIssue("warning", "MISSING_DOCSTRING", path, "Missing module docstring."))

        declared_package = module.doc_meta.get("PACKAGE")
        if declared_package and declared_package != module.package:
            issues.append(ValidationIssue("error", "PACKAGE_MISMATCH", path, f"Docstring PACKAGE={declared_package!r} but actual package is {module.package!r}."))

        declared_file = module.doc_meta.get("FILE")
        if declared_file and declared_file != module.filename:
            issues.append(ValidationIssue("error", "FILE_MISMATCH", path, f"Docstring FILE={declared_file!r} but actual file is {module.filename!r}."))

        declared_symbols = declared_public_symbols(module)
        if declared_symbols:
            if not module.has_explicit_all:
                issues.append(
                    ValidationIssue(
                        "warning",
                        "MISSING___ALL___FOR_EXPOSES",
                        path,
                        "Module declares EXPOSES/EXPORTS but does not define __all__. "
                        "Use __all__ as the canonical public API.",
                    )
                )
            elif sorted(declared_symbols) != sorted(module.public_symbols):
                issues.append(
                    ValidationIssue(
                        "warning",
                        "EXPOSES_MISMATCH",
                        path,
                        f"Docstring EXPOSES/EXPORTS={declared_symbols} but __all__={module.public_symbols}.",
                    )
                )

        if module.line_count > 500 and not module.is_init:
            issues.append(ValidationIssue("warning", "MODULE_TOO_LARGE", path, f"Module has {module.line_count} lines; split threshold is 500."))

        if module.is_helper and module.helper_group:
            helper_dir = root / Path(module.path).parent.parent
            main_file = helper_dir / f"{module.helper_group}.py"
            if not main_file.exists():
                issues.append(ValidationIssue("error", "HELPER_WITHOUT_MAIN", path, f"Helper group expects main file {main_file.relative_to(root)}."))

    package_symbol_owners: dict[tuple[str, str], list[str]] = defaultdict(list)
    for module in modules.values():
        if module.is_init:
            continue
        if is_excluded_from_duplicate_checks(module):
            continue
        for sym in module.public_symbols:
            if sym in EXCLUDED_DUPLICATE_SYMBOLS:
                continue
            package_symbol_owners[(module.package, sym)].append(module.module_id)

    for (pkg, sym), owners in sorted(package_symbol_owners.items()):
        if len(owners) > 1:
            issues.append(ValidationIssue("error", "DUPLICATE_PUBLIC_SYMBOL", pkg or ".", f"Symbol {sym!r} owned by multiple modules: {owners}"))

    return issues


def build_manifest(root: Path, modules: dict[str, ModuleInfo], issues: list[ValidationIssue]) -> dict[str, Any]:
    packages: dict[str, dict[str, Any]] = defaultdict(lambda: {"modules": {}, "symbols": {}, "helper_groups": {}})
    package_symbol_owners: dict[tuple[str, str], list[str]] = defaultdict(list)

    for module_id, info in modules.items():
        packages[info.package]["modules"][module_id] = info.as_dict()

        if info.is_helper:
            main_id = helper_main_module_id(info)
            packages[info.package]["helper_groups"].setdefault(
                info.helper_group or "",
                {"main_module": main_id, "helpers": []},
            )
            packages[info.package]["helper_groups"][info.helper_group or ""]["helpers"].append(module_id)

        if not info.is_init:
            for sym in info.public_symbols:
                package_symbol_owners[(info.package, sym)].append(module_id)

    for (pkg, sym), owners in sorted(package_symbol_owners.items()):
        if len(owners) == 1:
            packages[pkg]["symbols"][sym] = owners[0]

    for pkg in packages:
        packages[pkg]["symbols"] = dict(sorted(packages[pkg]["symbols"].items()))
        packages[pkg]["modules"] = dict(sorted(packages[pkg]["modules"].items()))
        for helper_group in packages[pkg]["helper_groups"].values():
            helper_group["helpers"] = sorted(helper_group["helpers"])
        packages[pkg]["helper_groups"] = dict(sorted(packages[pkg]["helper_groups"].items()))

    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "packages": dict(sorted(packages.items())),
        "validation_issues": [issue.as_dict() for issue in issues],
    }


def generate_init_content(pkg: str, manifest: dict[str, Any]) -> str:
    pkg_info = manifest["packages"].get(pkg, {})
    symbol_map: dict[str, str] = pkg_info.get("symbols", {})
    rel_symbol_map: dict[str, str] = {}

    for symbol, owner in sorted(symbol_map.items()):
        if owner == pkg:
            continue
        rel_symbol_map[symbol] = owner[len(pkg) + 1:] if pkg and owner.startswith(pkg + ".") else owner

    all_list = ", ".join(json.dumps(sym) for sym in sorted(rel_symbol_map))
    module_map_entries = ",\n".join(
        f'    {json.dumps(sym)}: {json.dumps(mod)}'
        for sym, mod in sorted(rel_symbol_map.items())
    )

    return (
        '"""Minimal package facade."""\n\n'
        f"__all__ = [{all_list}]\n"
        "__module_map__ = {\n"
        f"{module_map_entries}\n"
        "}\n"
    )


def generate_architecture_md(manifest: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# ARCHITECTURE")
    lines.append("")
    lines.append("Generated from `architecture_manifest.json`. This file is a derived view.")
    lines.append("")
    lines.append("## Project Purpose")
    lines.append("")
    lines.append("Structural source of truth for packages, modules, public symbols, helper-group relationships, and dependency directions.")
    lines.append("")
    lines.append("## Package Map")
    lines.append("")

    for pkg, pkg_info in manifest["packages"].items():
        display = pkg or "<root>"
        lines.append(f"### {display}")
        lines.append("")
        lines.append("| Module | Owns | Exposes | Depends On | Used By | Helper Group |")
        lines.append("|---|---|---|---|---|---|")
        for module_id, info in pkg_info["modules"].items():
            owns = (info.get("doc_meta", {}) or {}).get("OWNS", "")
            exposes = ", ".join(info.get("public_symbols", []))
            depends = ", ".join(info.get("direct_internal_imports", []))
            used_by = ", ".join(info.get("used_by", []))
            helper_group = info.get("helper_group") or ""
            lines.append(f"| `{module_id}` | {owns} | {exposes} | {depends} | {used_by} | {helper_group} |")
        lines.append("")

        if pkg_info.get("helper_groups"):
            lines.append("**Helper Groups**")
            lines.append("")
            for group_name, group in pkg_info["helper_groups"].items():
                lines.append(f"- `{group_name}` → main `{group.get('main_module')}`")
                for helper in group.get("helpers", []):
                    lines.append(f"  - `{helper}`")
            lines.append("")

        if pkg_info.get("symbols"):
            lines.append("**Public Symbol Quick Reference**")
            lines.append("")
            for symbol, owner in pkg_info["symbols"].items():
                lines.append(f"- `{symbol}` → `{owner}`")
            lines.append("")

    lines.append("## Validation Issues")
    lines.append("")
    issues = manifest.get("validation_issues", [])
    if not issues:
        lines.append("No validation issues.")
    else:
        for issue in issues:
            lines.append(f"- **{issue['level'].upper()}** `{issue['code']}` in `{issue['path']}` — {issue['message']}")
    lines.append("")
    lines.append("## Need Professional Help in Developing Your Architecture?")
    lines.append("")
    lines.append("Please contact me at [sammuti.com](https://sammuti.com) :)")
    lines.append("")
    return "\n".join(lines)


def diff_text(current: str, desired: str, fromfile: str, tofile: str) -> str:
    return "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            desired.splitlines(keepends=True),
            fromfile=fromfile,
            tofile=tofile,
        )
    )


def is_minimal_generated_init_content(text: str) -> bool:
    stripped = text.lstrip()
    return stripped.startswith('"""Minimal package facade."""') and "__module_map__" in text


def should_generate_init(root: Path, pkg: str) -> bool:
    init_path = root / Path(*pkg.split(".")) / "__init__.py"
    if not init_path.exists():
        return True
    current = read_text(init_path)
    return is_minimal_generated_init_content(current)


def collect_generated_outputs(root: Path, manifest: dict[str, Any]) -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    outputs[root / "architecture_manifest.json"] = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    outputs[root / "ARCHITECTURE.md"] = generate_architecture_md(manifest)

    for pkg in manifest["packages"].keys():
        if not pkg:
            continue
        if not should_generate_init(root, pkg):
            continue
        init_path = root / Path(*pkg.split(".")) / "__init__.py"
        outputs[init_path] = generate_init_content(pkg, manifest)

    return outputs


def print_issues(issues: list[ValidationIssue]) -> None:
    if not issues:
        print("No validation issues.")
        return
    for issue in issues:
        print(f"{issue.level.upper():7} {issue.code:28} {issue.path} :: {issue.message}")


def normalize_generated_output_for_diff(path: Path, text: str) -> str:
    if path.name != "architecture_manifest.json":
        return text
    try:
        data = json.loads(text)
    except Exception:
        return text
    if isinstance(data, dict) and "generated_at_utc" in data:
        data["generated_at_utc"] = "<normalized>"
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def scan_project(root: Path) -> tuple[dict[str, ModuleInfo], list[ValidationIssue], dict[str, Any], dict[Path, str]]:
    top_names = project_top_level_names(root)
    modules: dict[str, ModuleInfo] = {}
    for path in iter_python_files(root):
        info = scan_module(root, path, top_names)
        modules[info.module_id] = info

    build_reverse_dependencies(modules)
    issues = validate_modules(root, modules)
    manifest = build_manifest(root, modules, issues)
    outputs = collect_generated_outputs(root, manifest)
    return modules, issues, manifest, outputs


def run(root: Path, mode: str) -> int:
    _modules, issues, manifest, outputs = scan_project(root)

    if mode == "scan":
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0

    if mode == "validate":
        print_issues(issues)
        return 1 if any(i.level == "error" for i in issues) else 0

    if mode == "diff":
        exit_code = 0
        for path, desired in outputs.items():
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            current_norm = normalize_generated_output_for_diff(path, current)
            desired_norm = normalize_generated_output_for_diff(path, desired)
            diff = diff_text(current_norm, desired_norm, f"{path} (current)", f"{path} (generated)")
            if diff:
                print(diff)
                exit_code = 1
        if exit_code == 0:
            print("No diffs.")
        return exit_code

    if mode == "write":
        if any(i.level == "error" for i in issues):
            print_issues(issues)
            print("\nRefusing to write because validation has errors.")
            return 1

        changed = 0
        for path, content in outputs.items():
            if write_text_if_changed(path, content):
                print(f"WROTE {path}")
                changed += 1

        # Re-scan after writing generated __init__.py facades so the manifest and
        # ARCHITECTURE.md reflect the post-write tree instead of the pre-write tree.
        _modules2, issues2, manifest2, outputs2 = scan_project(root)

        if any(i.level == "error" for i in issues2):
            print_issues(issues2)
            print("\nPost-write validation has errors.")
            return 1

        for path, content in outputs2.items():
            if write_text_if_changed(path, content):
                print(f"WROTE {path}")
                changed += 1

        print(f"\nDone. Updated {changed} file(s).")
        return 0

    raise ValueError(f"Unsupported mode: {mode}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage architecture manifest, minimal __init__ facades, and ARCHITECTURE.md.")
    parser.add_argument("--root", default=r"E:\eeg_kernel_ai_neural_data_analysis", help="Project root path.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true", help="Print manifest JSON.")
    group.add_argument("--validate", action="store_true", help="Validate the source tree.")
    group.add_argument("--diff", action="store_true", help="Show diffs for generated outputs.")
    group.add_argument("--write", action="store_true", help="Write manifest, __init__.py, and ARCHITECTURE.md.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    mode = "scan" if args.scan else "validate" if args.validate else "diff" if args.diff else "write"
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Project root does not exist: {root}", file=sys.stderr)
        return 2
    return run(root, mode)


if __name__ == "__main__":
    raise SystemExit(main())
