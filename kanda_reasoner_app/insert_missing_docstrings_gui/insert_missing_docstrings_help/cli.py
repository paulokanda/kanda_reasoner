# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/cli.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Command-line parser and entry point for the docstring inserter
# EXPORTS       : build_parser, main
# DEPENDS ON    : run_orchestrator.py
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Command-line parser and entry point for the docstring inserter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .run_orchestrator import run

__all__ = [
    "build_parser",
    "main",
]


def build_parser() -> argparse.ArgumentParser:
    """Build  parser.
    
    Returns
    -------
    argparse.ArgumentParser
        TODO: describe the return value.
    """
    
    parser = argparse.ArgumentParser(
        description="Insert missing module/class/function docstrings without changing other code."
    )
    parser.add_argument("--root", required=True, help="Project root path.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true", help="Scan and summarize missing docstrings.")
    group.add_argument("--diff", action="store_true", help="Show diffs for inserted missing docstrings.")
    group.add_argument("--write", action="store_true", help="Write missing docstrings into source files.")
    parser.add_argument("--no-module", action="store_true", help="Do not insert module docstrings.")
    parser.add_argument("--no-classes", action="store_true", help="Do not insert class docstrings.")
    parser.add_argument("--no-functions", action="store_true", help="Do not insert function/method docstrings.")
    parser.add_argument(
        "--insert-file-address",
        action="store_true",
        help="Insert a top file-address comment such as '# package/module.py' when missing.",
    )
    parser.add_argument("--include-init", action="store_true", help="Allow module docstrings in __init__.py files.")
    parser.add_argument(
        "--include-relaxed-paths",
        action="store_true",
        help="Include temp, developer-tools, backup, older, and copy-path zones.",
    )
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include test-style files such as conftest.py, step12_checks, test_*.py, and *_test.py.",
    )
    parser.add_argument(
        "--module",
        dest="target_module",
        help="Restrict processing to one Python module/file. Accepts relative .py path, absolute path under the root, or dotted module name.",
    )
    parser.add_argument(
        "--package",
        dest="target_package",
        help="Restrict processing to one package/folder. Accepts relative folder path, absolute folder path under the root, or dotted package name.",
    )
    parser.add_argument(
        "--ai",
        metavar="CONFIG",
        nargs="?",
        const="default",
        help="Enable AI docstring generation. Optionally pass path to ai_config.json.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of workers reserved for AI mode. Sequential mode ignores this.",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        default=True,
        help="Document private (_name, __name) symbols. Default: on.",
    )
    parser.add_argument(
        "--no-private",
        dest="private",
        action="store_false",
        help="Skip private (_name, __name) symbols in AI mode.",
    )
    parser.add_argument(
        "--min-confidence",
        choices=["high", "medium", "low"],
        default="low",
        help="Minimum confidence required to accept an AI docstring before fallback.",
    )
    parser.add_argument(
        "--no-uncertain",
        action="store_true",
        help="Suppress # AI-UNCERTAIN comments for low-confidence AI docstrings.",
    )
    parser.add_argument(
        "--require-ai-success",
        action="store_true",
        help="Disable heuristic fallback. Any AI failure or rejected AI output becomes a hard error.",
    )
    parser.add_argument(
        "--report",
        dest="report_path",
        help="Optional JSONL report path for inserted, existing, skipped, and failed targets.",
    )
    return parser

def main() -> int:
    """Handle main.
    
    Returns
    -------
    int
        TODO: describe the return value.
    """
    
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
        insert_file_address_at_top=args.insert_file_address,
        include_init=args.include_init,
        include_relaxed_paths=args.include_relaxed_paths,
        include_tests=args.include_tests,
        ai_config_path=args.ai,
        workers=max(1, args.workers),
        include_private=args.private,
        min_confidence=args.min_confidence,
        no_uncertain=args.no_uncertain,
        require_ai_success=args.require_ai_success,
        target_module=args.target_module,
        target_package=args.target_package,
        report_path=args.report_path,
    )
