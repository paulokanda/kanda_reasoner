# project-path: kanda_reasoner_app/safety_suite_cli/commands_output_private.py
"""Private report-output helpers for safety-suite CLI commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, TextIO

__all__: list[str] = []

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

def _read_text_or_literal(value: str) -> str:
    """Support read text or literal behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = str(value or "")
    if not text:
        return ""
    path = Path(text)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return text

def _source_report_markdown(data: dict[str, Any]) -> str:
    """Support source report markdown behavior.
    
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
        "# Source Hygiene Report",
        "",
        "Report type: " + str(data.get("report_type", "unknown")),
        "Summary: " + str(data.get("summary", "")),
        "Finding count: " + str(data.get("finding_count", 0)),
        "",
        "## Findings",
    ]
    findings = data.get("findings", [])
    if isinstance(findings, list) and findings:
        for finding in findings:
            if isinstance(finding, dict):
                path = str(finding.get("path", ""))
                code = str(finding.get("code", ""))
                message = str(finding.get("message", ""))
                lines.append("- " + code + " :: " + path + " :: " + message)
    else:
        lines.append("- No findings.")
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
