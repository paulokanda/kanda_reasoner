# project-path: kanda_reasoner_app/safety_suite_cli/project_symbol_atlas_commands.py
"""CLI integration for Project Symbol Atlas commands.

This module owns parser wiring and presentation for atlas commands only. All
analysis and decision logic remains in the reasoner_symbol_atlas backend box.
"""

from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path
from contextlib import contextmanager
from typing import Any, TextIO

__all__ = [
    "add_reasoner_symbol_atlas_parsers",
    "reasoner_symbol_atlas_cli_commands",
]

_QUERY_COMMANDS: tuple[tuple[str, str, str], ...] = (
    ("find-symbol", "symbol", "Find an existing symbol and its owner."),
    ("find-owner", "owner", "Find the likely owner path for a symbol."),
    ("facade-owner", "facade_owner", "Resolve facade versus real owner."),
    ("main-helpers", "main_helpers", "Map main file and helper files."),
    ("related-files", "related_files", "Find related help and support files."),
    ("logic-placement", "logic_placement", "Advise where logic should go."),
    ("pre-patch-gate", "pre_patch_gate", "Run the pre-patch ownership gate."),
)


def reasoner_symbol_atlas_cli_commands() -> tuple[str, ...]:
    """Return Project Symbol Atlas command names exposed by the CLI."""

    return (
        "atlas-report",
        "evidence-freshness",
        "facade-owner",
        "find-owner",
        "find-symbol",
        "logic-placement",
        "main-helpers",
        "pre-patch-gate",
        "related-files",
        "symbol-atlas",
    )


def add_reasoner_symbol_atlas_parsers(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add Project Symbol Atlas parsers to the safety-suite CLI."""

    _add_atlas_report_parser(subparsers)
    _add_evidence_freshness_parser(subparsers)
    _add_symbol_atlas_parser(subparsers)
    for command_name, query_type, help_text in _QUERY_COMMANDS:
        _add_existing_code_query_parser(subparsers, command_name, query_type, help_text)


def _add_common_output_arguments(parser: argparse.ArgumentParser) -> None:
    """Support add common output arguments behavior.
    
    Parameters
    ----------
    parser : argparse.ArgumentParser
        The parser value.
    """
    
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Default: markdown.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional file path. If omitted, output is printed to stdout.",
    )


def _add_common_atlas_arguments(parser: argparse.ArgumentParser) -> None:
    """Support add common atlas arguments behavior.
    
    Parameters
    ----------
    parser : argparse.ArgumentParser
        The parser value.
    """
    
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--query", default="", help="Free-text atlas query.")
    parser.add_argument("--symbol", default="", help="Symbol name to search.")
    parser.add_argument("--target", default="", help="Target file path.")
    parser.add_argument("--task", default="", help="Task description.")
    parser.add_argument("--json-path", default="", help="Optional complete JSON path.")
    parser.add_argument("--exact", action="store_true", help="Use exact symbol matching.")
    parser.add_argument("--include-private", action="store_true", help="Include private symbols.")
    parser.add_argument("--include-workbench", action="store_true", help="Include workbench files.")
    parser.add_argument(
        "--max-matches",
        type=int,
        default=25,
        help="Maximum matching symbols or report items. Default: 25.",
    )


def _add_atlas_report_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Support add atlas report parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser(
        "atlas-report",
        help="Build and write Project Symbol Atlas reports.",
    )
    _add_common_atlas_arguments(parser)
    parser.add_argument("--output-dir", default="", help="Report output directory.")
    parser.add_argument("--no-existing-code", action="store_true", help="Skip existing-code report.")
    parser.add_argument("--no-freshness", action="store_true", help="Skip freshness report.")
    parser.add_argument("--no-merge", action="store_true", help="Skip live-plus-JSON merge report.")
    parser.add_argument(
        "--no-json-quality",
        action="store_true",
        help="Skip complete-JSON active-scope quality report.",
    )
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_atlas_report)


def _add_symbol_atlas_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Support add symbol atlas parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser(
        "symbol-atlas",
        help="Build a Project Symbol Atlas existing-code report without writing files.",
    )
    _add_common_atlas_arguments(parser)
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_symbol_atlas)


def _add_evidence_freshness_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Support add evidence freshness parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    """
    
    parser = subparsers.add_parser(
        "evidence-freshness",
        help="Check Project Analysis Evidence freshness.",
    )
    parser.add_argument("--root", required=True, help="Project root.")
    parser.add_argument("--json-path", default="", help="Optional complete JSON path.")
    parser.add_argument("--max-items", type=int, default=25, help="Maximum mismatch items.")
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_evidence_freshness)


def _add_existing_code_query_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    command_name: str,
    query_type: str,
    help_text: str,
) -> None:
    """Support add existing code query parser behavior.
    
    Parameters
    ----------
    subparsers : argparse._SubParsersAction[argparse.ArgumentParser]
        The subparsers value.
    command_name : str
        The command name value.
    query_type : str
        The query type value.
    help_text : str
        The help text value.
    """
    
    parser = subparsers.add_parser(command_name, help=help_text)
    _add_common_atlas_arguments(parser)
    _add_common_output_arguments(parser)
    parser.set_defaults(func=_cmd_existing_code_query, atlas_query_type=query_type)


def _cmd_atlas_report(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd atlas report behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del stderr
    from kanda_reasoner_app.reasoner_symbol_atlas.atlas_report_builder import (
        ProjectSymbolAtlasReportBuilderOptions,
        write_reasoner_symbol_atlas_reports,
    )

    options = ProjectSymbolAtlasReportBuilderOptions(
        project_root=args.root,
        output_dir=args.output_dir,
        query_text=args.query,
        query_type="auto",
        symbol_name=args.symbol,
        target_path=args.target,
        task_description=args.task,
        json_path=args.json_path,
        exact=bool(args.exact),
        include_private=bool(args.include_private),
        include_workbench=bool(args.include_workbench),
        max_matches=int(args.max_matches),
        include_existing_code_report=not bool(args.no_existing_code),
        include_freshness_report=not bool(args.no_freshness),
        include_merge_report=not bool(args.no_merge),
        include_json_quality_report=not bool(args.no_json_quality),
    )
    with _suppress_noisy_project_warnings():
        result = write_reasoner_symbol_atlas_reports(options)
    return _emit_report(result.to_dict(), _format_builder_result_markdown(result.to_dict()), args, stdout)


def _cmd_symbol_atlas(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd symbol atlas behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del stderr
    from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (
        build_reasoner_symbol_atlas_existing_code_report,
    )
    from kanda_reasoner_app.reasoner_symbol_atlas.report_writer import (
        format_reasoner_symbol_atlas_markdown,
    )

    with _suppress_noisy_project_warnings():
        report = build_reasoner_symbol_atlas_existing_code_report(_existing_options(args, "auto"))
    return _emit_report(report.to_dict(), format_reasoner_symbol_atlas_markdown(report), args, stdout)


def _cmd_existing_code_query(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd existing code query behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del stderr
    from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (
        build_reasoner_symbol_atlas_existing_code_report,
    )
    from kanda_reasoner_app.reasoner_symbol_atlas.report_writer import (
        format_reasoner_symbol_atlas_markdown,
    )

    query_type = str(getattr(args, "atlas_query_type", "auto") or "auto")
    with _suppress_noisy_project_warnings():
        report = build_reasoner_symbol_atlas_existing_code_report(_existing_options(args, query_type))
    return _emit_report(report.to_dict(), format_reasoner_symbol_atlas_markdown(report), args, stdout)


def _cmd_evidence_freshness(args: argparse.Namespace, stdout: TextIO, stderr: TextIO) -> int:
    """Support cmd evidence freshness behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    stderr : TextIO
        The stderr value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    del stderr
    from kanda_reasoner_app.reasoner_symbol_atlas.evidence_freshness import (
        ProjectSymbolAtlasEvidenceFreshnessOptions,
        build_reasoner_symbol_atlas_evidence_freshness_report,
    )
    from kanda_reasoner_app.reasoner_symbol_atlas.report_writer import (
        format_reasoner_symbol_atlas_markdown,
    )

    with _suppress_noisy_project_warnings():
        report = build_reasoner_symbol_atlas_evidence_freshness_report(
            ProjectSymbolAtlasEvidenceFreshnessOptions(
                project_root=args.root,
                json_path=args.json_path,
                max_items=int(args.max_items),
            )
        )
    return _emit_report(report.to_dict(), format_reasoner_symbol_atlas_markdown(report), args, stdout)




@contextmanager
def _suppress_noisy_project_warnings():
    """Support suppress noisy project warnings behavior.
    """
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        warnings.simplefilter("ignore", DeprecationWarning)
        yield

def _existing_options(args: argparse.Namespace, query_type: str) -> Any:
    """Support existing options behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    query_type : str
        The query type value.
    
    Returns
    -------
    Any
        The any result.
    """
    
    from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (
        ProjectSymbolAtlasExistingCodeFinderOptions,
    )

    return ProjectSymbolAtlasExistingCodeFinderOptions(
        project_root=args.root,
        query_text=args.query,
        query_type=query_type,
        symbol_name=args.symbol,
        target_path=args.target,
        task_description=args.task,
        json_path=args.json_path,
        exact=bool(args.exact),
        include_private=bool(args.include_private),
        include_workbench=bool(args.include_workbench),
        max_matches=int(args.max_matches),
    )


def _emit_report(data: dict[str, Any], markdown: str, args: argparse.Namespace, stdout: TextIO) -> int:
    """Support emit report behavior.
    
    Parameters
    ----------
    data : dict[str, Any]
        The input data.
    markdown : str
        The markdown value.
    args : argparse.Namespace
        The positional arguments.
    stdout : TextIO
        The stdout value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    text = json.dumps(_json_ready(data), indent=2, sort_keys=True) + "\n"
    if getattr(args, "format", "markdown") == "markdown":
        text = markdown
    output_path = str(getattr(args, "output", "") or "").strip()
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(text, encoding="utf-8")
    else:
        stdout.write(text)
    return 0


def _format_builder_result_markdown(data: dict[str, Any]) -> str:
    """Support format builder result markdown behavior.
    
    Parameters
    ----------
    data : dict[str, Any]
        The input data.
    
    Returns
    -------
    str
        The string result.
    """
    
    lines = [
        "# Project Symbol Atlas Reports",
        "",
        "Status: " + str(data.get("status", "")),
        "Project root: " + str(data.get("project_root", "")),
        "Output dir: " + str(data.get("output_dir", "")),
        "Report count: " + str(data.get("report_count", 0)),
        "Written report count: " + str(data.get("written_report_count", 0)),
        "",
        "## Written reports",
    ]
    written = data.get("written_reports", [])
    if isinstance(written, list) and written:
        for item in written:
            if isinstance(item, dict):
                lines.append("- " + str(item.get("markdown_path", "")))
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Notes")
    notes = data.get("notes", [])
    if isinstance(notes, list) and notes:
        lines.extend("- " + str(note) for note in notes)
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def _json_ready(value: Any) -> Any:
    """Support json ready behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    Any
        The any result.
    """
    
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value
