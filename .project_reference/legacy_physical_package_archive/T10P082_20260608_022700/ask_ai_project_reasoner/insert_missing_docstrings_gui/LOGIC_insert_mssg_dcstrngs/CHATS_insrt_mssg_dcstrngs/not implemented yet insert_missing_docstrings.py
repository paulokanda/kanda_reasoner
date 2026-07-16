#!/usr/bin/env python3
"""Insert missing module/class/function docstrings without rewriting other code.

Phase 2 upgrade: AI-powered generation (local LLM via OpenAI-compatible API)
with parallel file processing via ThreadPoolExecutor.

New flags
---------
--ai [CONFIG]
    Enable AI docstring generation.  CONFIG is an optional path to an
    ai_config.json file.  Omit CONFIG to use built-in defaults (Ollama,
    codellama:13b, localhost:11434).

--workers N
    Number of parallel file-processing threads (default 4).
    Set to 1 to process sequentially (useful for debugging).

All existing flags are unchanged and the tool behaves identically when
--ai is not passed.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import json
import os
import re
import sys
import warnings
from pathlib import Path
from typing import Callable, Iterable

# ---------------------------------------------------------------------------
# Optional AI stack — imported lazily so the tool works without them.
# ---------------------------------------------------------------------------
try:
    from ai_config import AIConfig
    from context_builder import (
        build_class_context,
        build_function_context,
        build_module_context,
    )
    from ai_docstring_generator import AIDocstringGenerator
    from parallel_runner import FileProgress, RunSummary, run_parallel
    _AI_AVAILABLE = True
except ImportError:
    _AI_AVAILABLE = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".coverage",
    "htmlcov", "build", "dist", "node_modules", ".venv", "venv",
    "env", "tests", "test",
}

RELAXED_PATH_PREFIXES = (
    "temp/",
    "developer_tools/",
    "original_backups/",
    "_phase3_tmp_project/",
)

UTF8_BOM = b"\xef\xbb\xbf"


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def read_source_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    had_bom = raw.startswith(UTF8_BOM)
    return raw.decode("utf-8-sig"), had_bom


def write_source_text(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    path.write_text(text, encoding=encoding, newline="\n")


def normalize_rel_path(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/").lstrip("./")


# ---------------------------------------------------------------------------
# Path filters
# ---------------------------------------------------------------------------


def is_transitional_copy_filename(filename: str) -> bool:
    lowered = filename.lower()
    return " - copy" in lowered or lowered.startswith("copy of ")


def is_test_like_path(rel_path: str) -> bool:
    lowered = rel_path.lower()
    name = Path(lowered).name
    if lowered.startswith("step12_checks/"):
        return True
    if name == "conftest.py":
        return True
    if name.startswith("test_") and name.endswith(".py"):
        return True
    if name.endswith("_test.py"):
        return True
    return False


def is_relaxed_path(rel_path: str, filename: str) -> bool:
    lowered = rel_path.lower()
    if lowered.startswith(RELAXED_PATH_PREFIXES):
        return True
    if "/older/" in lowered:
        return True
    if "/backup/" in lowered or "/backups/" in lowered:
        return True
    if is_transitional_copy_filename(filename):
        return True
    if "to restore if needed" in filename.lower():
        return True
    return False


def should_exclude_path(
    rel_path: str,
    filename: str,
    *,
    include_relaxed_paths: bool,
    include_tests: bool,
) -> bool:
    if not include_relaxed_paths and is_relaxed_path(rel_path, filename):
        return True
    if not include_tests and is_test_like_path(rel_path):
        return True
    return False


def iter_python_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        path_obj = Path(dirpath)
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_EXCLUDE_DIRS]
        for filename in filenames:
            if filename.endswith(".py"):
                yield path_obj / filename


# ---------------------------------------------------------------------------
# AST utilities
# ---------------------------------------------------------------------------


def to_module_id(root: Path, path: Path) -> str:
    rel = path.relative_to(root)
    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def split_words(name: str) -> list[str]:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name.replace("_", " "))
    return [w for w in text.split() if w]


def prettify_name(name: str) -> str:
    return " ".join(split_words(name)).strip().lower()


def expr_to_text(expr: ast.expr | None) -> str:
    if expr is None:
        return "object"
    try:
        return ast.unparse(expr)
    except Exception:
        return "object"


def parse_source(text: str, path: Path) -> ast.Module:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return ast.parse(text, filename=str(path))


def extract_public_symbols(tree: ast.Module) -> list[str]:
    explicit_all: list[str] | None = None
    fallback_public: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                fallback_public.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    explicit = []
                    if isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
                        ok = True
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                explicit.append(elt.value)
                            else:
                                ok = False
                                break
                        if ok:
                            explicit_all = explicit
    return sorted(set(explicit_all if explicit_all is not None else fallback_public))


def extract_internal_import_modules(tree: ast.Module) -> list[str]:
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name.split(".")[-1] + ".py")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.append(node.module.split(".")[-1] + ".py")
    return sorted(set(modules))


# ---------------------------------------------------------------------------
# Heuristic docstring builders (used when --ai is absent or as fallback)
# ---------------------------------------------------------------------------


def function_summary(name: str) -> str:
    lower = name.lower()
    pretty = prettify_name(name)
    PREFIX_MAP = {
        "get_": "Get", "set_": "Set", "build_": "Build", "create_": "Create",
        "make_": "Make", "load_": "Load", "save_": "Save", "update_": "Update",
        "compute_": "Compute", "normalize_": "Normalize", "resolve_": "Resolve",
        "detect_": "Detect", "extract_": "Extract", "apply_": "Apply",
        "render_": "Render", "show_": "Show", "hide_": "Hide", "emit_": "Emit",
        "handle_": "Handle", "run_": "Run", "scan_": "Scan",
        "validate_": "Validate",
    }
    for prefix, verb in PREFIX_MAP.items():
        if lower.startswith(prefix):
            return f"{verb} {pretty[len(prefix) - 1:]}."
    if lower.startswith("is_"):
        return f"Return whether {pretty[3:]}."
    if lower.startswith("has_"):
        return f"Return whether {pretty[4:]}."
    return f"Handle {pretty or name}."


def class_summary(name: str) -> str:
    return f"Represent {prettify_name(name) or name}."


def module_summary(path: Path, module_id: str) -> str:
    if path.name == "__init__.py":
        package_name = module_id or path.parent.name
        package_words = prettify_name(package_name.split(".")[-1])
        return f"Package facade for {package_words or package_name}."
    stem_words = prettify_name(path.stem)
    return f"Utilities and definitions for {stem_words or path.stem}."


def iter_function_parameters(node: ast.FunctionDef | ast.AsyncFunctionDef):
    args = node.args
    posonly = list(args.posonlyargs)
    normal = list(args.args)
    kwonly = list(args.kwonlyargs)
    ordered = []
    defaults_offset = len(posonly) + len(normal) - len(args.defaults)
    all_regular = posonly + normal
    for idx, arg in enumerate(all_regular):
        if arg.arg in {"self", "cls"}:
            continue
        default = None
        if idx >= defaults_offset:
            default = args.defaults[idx - defaults_offset]
        ordered.append((arg.arg, expr_to_text(arg.annotation), default is not None))
    if args.vararg is not None:
        ordered.append((f"*{args.vararg.arg}", expr_to_text(args.vararg.annotation), False))
    for idx, arg in enumerate(kwonly):
        default = args.kw_defaults[idx]
        ordered.append((arg.arg, expr_to_text(arg.annotation), default is not None))
    if args.kwarg is not None:
        ordered.append((f"**{args.kwarg.arg}", expr_to_text(args.kwarg.annotation), False))
    return ordered


def build_module_docstring(
    path: Path, module_id: str, tree: ast.Module, root: Path, manifest: dict | None,
) -> str:
    del tree, root, manifest
    return f'"""{module_summary(path, module_id)}"""'


def build_class_docstring(node: ast.ClassDef) -> str:
    return f'"""{class_summary(node.name)}"""'


def build_function_docstring(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    lines: list[str] = ['"""' + function_summary(node.name), ""]
    params = list(iter_function_parameters(node))
    if params:
        lines += ["Parameters", "----------"]
        for name, annotation, has_default in params:
            suffix = ", optional" if has_default else ""
            lines.append(f"{name} : {annotation}{suffix}")
            lines.append(f"    TODO: describe {name}.")
        lines.append("")
    returns_text = expr_to_text(node.returns) if node.returns is not None else ""
    if returns_text and returns_text != "None":
        lines += ["Returns", "-------", returns_text, "    TODO: describe the return value.", ""]
    if lines[-1] == "":
        lines.pop()
    lines.append('"""')
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Indentation / insertion helpers
# ---------------------------------------------------------------------------


def indentation_for_body(node: ast.AST, first_stmt: ast.stmt | None) -> str:
    if first_stmt is not None:
        return " " * first_stmt.col_offset
    col = getattr(node, "col_offset", 0)
    return " " * (col + 4)


def wrap_docstring_lines(docstring: str, indent: str) -> list[str]:
    raw_lines = docstring.splitlines()
    return [indent + line if line else indent for line in raw_lines]


def module_insert_index(lines: list[str]) -> int:
    idx = 0
    if idx < len(lines) and lines[idx].startswith("#!"):
        idx += 1
    if idx < len(lines) and "coding" in lines[idx]:
        idx += 1
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    return idx


def has_inline_body(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not node.body:
        return False
    return node.body[0].lineno == node.lineno


def load_manifest(root: Path) -> dict | None:
    manifest_path = root / "architecture_manifest.json"
    if not manifest_path.exists():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def apply_insertions_to_text(text: str, insertions: list[tuple[int, list[str]]]) -> str:
    if not insertions:
        return text
    lines = text.splitlines()
    trailing_newline = text.endswith("\n")
    for index, payload in insertions:
        lines[index:index] = payload
    result = "\n".join(lines)
    if trailing_newline or insertions:
        result += "\n"
    return result


def diff_text(current: str, desired: str, fromfile: str, tofile: str) -> str:
    return "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            desired.splitlines(keepends=True),
            fromfile=fromfile,
            tofile=tofile,
        )
    )


# ---------------------------------------------------------------------------
# Core per-file collector — now AI-aware
# ---------------------------------------------------------------------------


def collect_missing_docstring_insertions(
    root: Path,
    path: Path,
    include_module: bool,
    include_classes: bool,
    include_functions: bool,
    include_init: bool,
    manifest: dict | None,
    generator: object | None = None,  # AIDocstringGenerator | None
    on_symbol_done: Callable[[str, bool], None] | None = None,
) -> tuple[list[tuple[int, list[str]]], list[str], str, bool]:
    """Collect all missing-docstring insertions for a single Python file.

    Parameters
    ----------
    root : Path
        Project root directory.
    path : Path
        Python source file to analyse.
    include_module : bool
        Whether to insert a module-level docstring.
    include_classes : bool
        Whether to insert class docstrings.
    include_functions : bool
        Whether to insert function/method docstrings (including private ones).
    include_init : bool
        Whether to insert module docstrings in ``__init__.py`` files.
    manifest : dict, optional
        Optional architecture manifest loaded from ``architecture_manifest.json``.
    generator : AIDocstringGenerator, optional
        When provided, AI-generated docstrings replace heuristic ones.
    on_symbol_done : callable, optional
        Called with ``(symbol_name, used_ai: bool)`` after each docstring is
        generated.  Used by the parallel runner for progress reporting.

    Returns
    -------
    insertions : list[tuple[int, list[str]]]
        Sorted (descending by line) insertion payloads.
    skipped : list[str]
        Human-readable messages for skipped symbols.
    text : str
        Original file source text.
    had_bom : bool
        Whether the file had a UTF-8 BOM prefix.
    """
    text, had_bom = read_source_text(path)

    try:
        tree = parse_source(text, path)
    except SyntaxError as exc:
        return [], [f"{path}: source parse failed; skipped ({exc})"], text, had_bom

    module_id = to_module_id(root, path)
    source_lines = text.splitlines()
    insertions: list[tuple[int, list[str]]] = []
    skipped: list[str] = []

    # ------------------------------------------------------------------
    # Module docstring
    # ------------------------------------------------------------------
    if (
        include_module
        and ast.get_docstring(tree, clean=False) is None
        and (include_init or path.name != "__init__.py")
    ):
        idx = module_insert_index(source_lines)
        if generator is not None and _AI_AVAILABLE:
            ctx = build_module_context(path, module_id, tree, source_lines)
            body = generator.generate(ctx)
            module_doc = f'"""{body}"""'
            used_ai = True
        else:
            module_doc = build_module_docstring(path, module_id, tree, root, manifest)
            used_ai = False
        insertions.append((idx, [module_doc, ""]))
        if on_symbol_done:
            on_symbol_done(f"<module:{path.stem}>", used_ai)

    # ------------------------------------------------------------------
    # Class and function docstrings
    # ------------------------------------------------------------------
    for node in ast.walk(tree):

        if include_classes and isinstance(node, ast.ClassDef):
            if ast.get_docstring(node, clean=False) is None:
                if has_inline_body(node):
                    skipped.append(
                        f"{path}: class {node.name} on line {node.lineno} has inline body; skipped"
                    )
                    continue
                first_stmt = node.body[0] if node.body else None
                insert_at = (first_stmt.lineno - 1) if first_stmt is not None else node.lineno
                indent = indentation_for_body(node, first_stmt)

                if generator is not None and _AI_AVAILABLE:
                    module_ds = ast.get_docstring(tree) or ""
                    ctx = build_class_context(node, tree, module_id, source_lines, module_ds)
                    body = generator.generate(ctx)
                    raw_doc = f'"""{body}"""'
                    used_ai = True
                else:
                    raw_doc = build_class_docstring(node)
                    used_ai = False

                payload = wrap_docstring_lines(raw_doc, indent) + [indent]
                insertions.append((insert_at, payload))
                if on_symbol_done:
                    on_symbol_done(node.name, used_ai)

        if include_functions and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node, clean=False) is None:
                if has_inline_body(node):
                    skipped.append(
                        f"{path}: function {node.name} on line {node.lineno} has inline body; skipped"
                    )
                    continue
                first_stmt = node.body[0] if node.body else None
                insert_at = (first_stmt.lineno - 1) if first_stmt is not None else node.lineno
                indent = indentation_for_body(node, first_stmt)

                if generator is not None and _AI_AVAILABLE:
                    module_ds = ast.get_docstring(tree) or ""
                    # Resolve class docstring if this is a method.
                    class_ds = ""
                    for candidate in ast.walk(tree):
                        if isinstance(candidate, ast.ClassDef):
                            end = getattr(candidate, "end_lineno", candidate.lineno)
                            if candidate.lineno <= node.lineno <= end:
                                class_ds = ast.get_docstring(candidate) or ""
                                break
                    ctx = build_function_context(
                        node, tree, module_id, source_lines, module_ds, class_ds
                    )
                    body = generator.generate(ctx)
                    raw_doc = f'"""{body}"""'
                    used_ai = True
                else:
                    raw_doc = build_function_docstring(node)
                    used_ai = False

                payload = wrap_docstring_lines(raw_doc, indent) + [indent]
                insertions.append((insert_at, payload))
                if on_symbol_done:
                    on_symbol_done(node.name, used_ai)

    return sorted(insertions, key=lambda x: x[0], reverse=True), skipped, text, had_bom


# ---------------------------------------------------------------------------
# collect_changes  —  sequential (default) or parallel (--workers N + --ai)
# ---------------------------------------------------------------------------


def collect_changes(
    root: Path,
    *,
    include_module: bool,
    include_classes: bool,
    include_functions: bool,
    include_init: bool,
    include_relaxed_paths: bool,
    include_tests: bool,
    generator: object | None = None,       # AIDocstringGenerator | None
    workers: int = 1,
    on_file_progress: Callable | None = None,
    on_file_complete: Callable | None = None,
) -> tuple[dict[Path, tuple[str, bool]], list[str]]:
    """Collect all changes across the project, optionally in parallel.

    Parameters
    ----------
    root : Path
        Project root directory.
    include_module : bool
        Insert missing module docstrings.
    include_classes : bool
        Insert missing class docstrings.
    include_functions : bool
        Insert missing function/method docstrings.
    include_init : bool
        Process ``__init__.py`` module docstrings.
    include_relaxed_paths : bool
        Include temp/backup/older paths normally skipped.
    include_tests : bool
        Include test files normally skipped.
    generator : AIDocstringGenerator, optional
        AI generator instance; ``None`` uses heuristics.
    workers : int, optional
        Parallel worker threads.  1 = sequential (default without --ai).
    on_file_progress : callable, optional
        Progress callback forwarded to the parallel runner.
    on_file_complete : callable, optional
        Completion callback forwarded to the parallel runner.

    Returns
    -------
    changes : dict[Path, tuple[str, bool]]
        Files with pending insertions mapped to (new_text, had_bom).
    skipped_messages : list[str]
        Human-readable skip/error messages.
    """
    manifest = load_manifest(root)

    # Collect eligible paths first (always sequential — os.walk is fast).
    eligible: list[Path] = []
    for path in iter_python_files(root):
        rel_path = normalize_rel_path(root, path)
        if should_exclude_path(
            rel_path, path.name,
            include_relaxed_paths=include_relaxed_paths,
            include_tests=include_tests,
        ):
            continue
        eligible.append(path)

    # ------------------------------------------------------------------
    # Parallel path  — used when workers > 1 and AI stack is available.
    # ------------------------------------------------------------------
    if workers > 1 and _AI_AVAILABLE and generator is not None:
        def _processor(
            path: Path,
            *,
            on_symbol_done: Callable[[str, bool], None] | None = None,
        ) -> tuple:
            return collect_missing_docstring_insertions(
                root, path,
                include_module=include_module,
                include_classes=include_classes,
                include_functions=include_functions,
                include_init=include_init,
                manifest=manifest,
                generator=generator,
                on_symbol_done=on_symbol_done,
            )

        summary: RunSummary = run_parallel(
            eligible,
            _processor,
            parse_source,
            apply_insertions_to_text,
            workers=workers,
            on_file_progress=on_file_progress,
            on_file_complete=on_file_complete,
        )
        return summary.changes, summary.skipped_messages

    # ------------------------------------------------------------------
    # Sequential path  — heuristic mode, or workers=1.
    # ------------------------------------------------------------------
    changes: dict[Path, tuple[str, bool]] = {}
    skipped_messages: list[str] = []

    for path in eligible:
        insertions, skipped, current, had_bom = collect_missing_docstring_insertions(
            root, path,
            include_module=include_module,
            include_classes=include_classes,
            include_functions=include_functions,
            include_init=include_init,
            manifest=manifest,
            generator=generator,
        )
        skipped_messages.extend(skipped)
        if not insertions:
            continue
        desired = apply_insertions_to_text(current, insertions)
        if desired != current:
            try:
                parse_source(desired, path)
            except SyntaxError as exc:
                skipped_messages.append(
                    f"{path}: generated insertion would create invalid syntax; skipped ({exc})"
                )
                continue
            changes[path] = (desired, had_bom)

    return changes, skipped_messages


# ---------------------------------------------------------------------------
# run()  — main entry point called by GUI and CLI
# ---------------------------------------------------------------------------


def run(
    root: Path,
    mode: str,
    *,
    include_module: bool = True,
    include_classes: bool = True,
    include_functions: bool = True,
    include_init: bool = False,
    include_relaxed_paths: bool = False,
    include_tests: bool = False,
    ai_config_path: str | None = None,
    workers: int = 1,
    on_file_progress: Callable | None = None,
    on_file_complete: Callable | None = None,
) -> int:
    """Run the docstring inserter in the given *mode*.

    Parameters
    ----------
    root : Path
        Project root directory.
    mode : str
        One of ``"scan"``, ``"diff"``, or ``"write"``.
    include_module : bool, optional
        Insert missing module docstrings.
    include_classes : bool, optional
        Insert missing class docstrings.
    include_functions : bool, optional
        Insert missing function/method docstrings (including ``_private``).
    include_init : bool, optional
        Process ``__init__.py`` module docstrings.
    include_relaxed_paths : bool, optional
        Include temp/backup zones.
    include_tests : bool, optional
        Include test files.
    ai_config_path : str, optional
        Path to an ``ai_config.json`` file, or ``"default"`` for built-in
        defaults.  ``None`` disables AI (pure heuristic mode).
    workers : int, optional
        Parallel worker threads for AI mode.  Ignored in heuristic mode.
    on_file_progress : callable, optional
        Per-symbol progress callback — signature: ``(FileProgress) -> None``.
    on_file_complete : callable, optional
        Per-file completion callback — signature: ``(FileProgress) -> None``.

    Returns
    -------
    int
        Exit code: 0 on success, 2 on bad arguments.
    """
    # ------------------------------------------------------------------
    # Optionally build an AI generator.
    # ------------------------------------------------------------------
    generator = None
    if ai_config_path is not None and _AI_AVAILABLE:
        try:
            cfg = (
                AIConfig.from_json(ai_config_path)
                if ai_config_path != "default"
                else AIConfig.default()
            )
            errors = cfg.validate()
            if errors:
                for e in errors:
                    print(f"AI config error: {e}", file=sys.stderr)
                return 2

            def _on_fallback(symbol_name: str, reason: str) -> None:
                print(f"AI FALLBACK {symbol_name}: {reason}")

            generator = AIDocstringGenerator(
                config=cfg,
                project_root=root,
                on_fallback=_on_fallback,
            )
            effective_workers = cfg.workers if workers == 1 else workers
            print(
                f"AI mode: model={cfg.model}  workers={effective_workers}"
                f"  cache={'on' if cfg.cache_enabled else 'off'}"
            )
        except Exception as exc:
            print(f"Failed to initialise AI generator: {exc}", file=sys.stderr)
            return 2
    elif ai_config_path is not None and not _AI_AVAILABLE:
        print(
            "ERROR: --ai requested but AI stack (ai_config, context_builder, "
            "ai_docstring_generator, parallel_runner) is not installed.",
            file=sys.stderr,
        )
        return 2
    else:
        effective_workers = 1

    effective_workers = (
        (AIConfig.default().workers if ai_config_path == "default" else workers)
        if generator is not None
        else 1
    )

    changes, skipped_messages = collect_changes(
        root,
        include_module=include_module,
        include_classes=include_classes,
        include_functions=include_functions,
        include_init=include_init,
        include_relaxed_paths=include_relaxed_paths,
        include_tests=include_tests,
        generator=generator,
        workers=effective_workers,
        on_file_progress=on_file_progress,
        on_file_complete=on_file_complete,
    )

    if generator is not None and _AI_AVAILABLE:
        generator.flush_cache()

    # ------------------------------------------------------------------
    # Mode output
    # ------------------------------------------------------------------
    if mode == "scan":
        summary = {
            "project_root": str(root),
            "include_module": include_module,
            "include_classes": include_classes,
            "include_functions": include_functions,
            "include_init": include_init,
            "include_relaxed_paths": include_relaxed_paths,
            "include_tests": include_tests,
            "ai_enabled": generator is not None,
            "files_with_missing_docstrings": len(changes),
            "files": [
                str(p.relative_to(root)).replace("\\", "/") for p in sorted(changes)
            ],
            "skipped": skipped_messages,
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    if mode == "diff":
        if not changes and not skipped_messages:
            print("No missing docstrings found.")
            return 0
        for msg in skipped_messages:
            print(f"SKIPPED {msg}")
        for path, (desired, _had_bom) in sorted(changes.items()):
            current, _ = read_source_text(path)
            print(diff_text(current, desired, f"{path} (current)", f"{path} (generated)"))
        return 0

    if mode == "write":
        if not changes and not skipped_messages:
            print("No missing docstrings found.")
            return 0
        for msg in skipped_messages:
            print(f"SKIPPED {msg}")
        if not changes:
            print("No safe docstring insertions to write.")
            return 0
        changed = 0
        for path, (desired, had_bom) in sorted(changes.items()):
            write_source_text(path, desired, had_bom)
            print(f"WROTE {path}")
            changed += 1
        print(f"\nDone. Updated {changed} file(s).")
        return 0

    raise ValueError(f"Unsupported mode: {mode}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Insert missing module/class/function docstrings without changing other code."
        )
    )
    parser.add_argument("--root", required=True, help="Project root path.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true")
    group.add_argument("--diff", action="store_true")
    group.add_argument("--write", action="store_true")

    parser.add_argument("--no-module", action="store_true")
    parser.add_argument("--no-classes", action="store_true")
    parser.add_argument("--no-functions", action="store_true")
    parser.add_argument("--include-init", action="store_true")
    parser.add_argument("--include-relaxed-paths", action="store_true")
    parser.add_argument("--include-tests", action="store_true")

    # Phase 2 additions
    parser.add_argument(
        "--ai",
        metavar="CONFIG",
        nargs="?",
        const="default",
        help=(
            "Enable AI docstring generation using a local LLM.  "
            "Optionally pass a path to an ai_config.json.  "
            "Defaults to Ollama + codellama:13b on localhost:11434."
        ),
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Number of parallel file-processing threads (default: value from "
            "ai_config.json, or 4 when --ai default is used).  "
            "Ignored without --ai."
        ),
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    mode = "scan" if args.scan else "diff" if args.diff else "write"
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Project root does not exist: {root}", file=sys.stderr)
        return 2

    return run(
        root,
        mode,
        include_module=not args.no_module,
        include_classes=not args.no_classes,
        include_functions=not args.no_functions,
        include_init=args.include_init,
        include_relaxed_paths=args.include_relaxed_paths,
        include_tests=args.include_tests,
        ai_config_path=args.ai,
        workers=args.workers or 1,
    )


if __name__ == "__main__":
    raise SystemExit(main())
