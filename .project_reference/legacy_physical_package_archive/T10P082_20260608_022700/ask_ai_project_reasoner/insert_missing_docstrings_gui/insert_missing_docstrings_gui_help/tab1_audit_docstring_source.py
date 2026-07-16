
"""Read missing-docstring targets from the Tab 1 architecture audit."""

from __future__ import annotations


__all__ = [
    "MISSING_DOCSTRING_CODE",
    "TAB1_AUDIT_SOURCE_LABEL",
    "Tab1AuditDocstringSourceResult",
    "Tab1MissingDocstringFinding",
    "extract_missing_docstring_findings",
    "read_missing_docstrings_from_tab1_audit",
    "refresh_tab1_audit_docstring_source",
    "tab1_audit_source_is_enabled",
]

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


MISSING_DOCSTRING_CODE = "MISSING_DOCSTRING"
TAB1_AUDIT_SOURCE_LABEL = "get missing docstring from Tab1 audit."
MISSING_DOCSTRING_RE = re.compile(
    r"^(?:ERROR|WARNING)\s+MISSING_DOCSTRING\s+(.+?)\s+::\s+(.+)$"
)


@dataclass(frozen=True)
class Tab1MissingDocstringFinding:
    """Represent one missing-docstring issue reported by Tab 1."""

    path: str
    message: str
    raw_line: str
    target_kind: str = ""


@dataclass(frozen=True)
class Tab1AuditDocstringSourceResult:
    """Represent the result of reading missing docstrings from Tab 1."""

    findings: tuple[Tab1MissingDocstringFinding, ...]
    command: tuple[str, ...]
    exit_code: int
    output: str
    error: str = ""


def extract_missing_docstring_findings(output: str) -> tuple[Tab1MissingDocstringFinding, ...]:
    """Extract MISSING_DOCSTRING findings from Tab 1 validation output."""
    findings: list[Tab1MissingDocstringFinding] = []
    seen: set[tuple[str, str]] = set()

    for raw_line in output.splitlines():
        line = raw_line.strip()
        match = MISSING_DOCSTRING_RE.search(line)
        if not match:
            continue

        path = match.group(1).strip()
        message = match.group(2).strip()
        key = (path, message)
        if key in seen:
            continue

        findings.append(
            Tab1MissingDocstringFinding(
                path=path,
                message=message,
                raw_line=raw_line,
                target_kind=_target_kind_from_message(message),
            )
        )
        seen.add(key)

    return tuple(findings)


def read_missing_docstrings_from_tab1_audit(
    project_root: Path,
    command_runner=None,
) -> Tab1AuditDocstringSourceResult:
    """Run Tab 1 validation and return missing-docstring findings."""
    tool_root = Path(__file__).resolve().parents[3]
    tool_dir = "manage" + "_architecture"
    tool_name = tool_dir + ".py"
    tool_path = tool_root / "kanda_reasoner_app" / tool_dir / tool_name

    command = (
        sys.executable,
        str(tool_path),
        "--root",
        str(project_root),
        "--validate",
    )

    if command_runner is None:
        completed = subprocess.run(
            list(command),
            cwd=str(tool_root),
            capture_output=True,
            text=True,
            errors="replace",
        )
        exit_code = int(completed.returncode)
        output = (completed.stdout or "") + (completed.stderr or "")
    else:
        exit_code, output = command_runner(command, tool_root)

    findings = extract_missing_docstring_findings(output)
    return Tab1AuditDocstringSourceResult(
        findings=findings,
        command=command,
        exit_code=exit_code,
        output=output,
    )


def refresh_tab1_audit_docstring_source(
    window: object,
    checked: bool | None = None,
    command_runner=None,
) -> Tab1AuditDocstringSourceResult | None:
    """Refresh Tab 1 audit findings for a MissingDocstringsWindow."""
    if checked is False:
        return None

    root_text = ""
    root_edit = getattr(window, "_root_path_edit", None)
    if root_edit is not None and callable(getattr(root_edit, "text", None)):
        root_text = str(root_edit.text()).strip()

    project_root = Path(root_text or Path.cwd()).resolve()
    result = read_missing_docstrings_from_tab1_audit(
        project_root=project_root,
        command_runner=command_runner,
    )

    setattr(window, "_tab1_audit_missing_docstring_findings", result.findings)
    setattr(window, "_tab1_audit_docstring_source_result", result)

    _append_window_text(
        window,
        "[tab1 audit] MISSING_DOCSTRING findings: "
        + str(len(result.findings))
        + "\n",
    )
    if result.findings:
        for finding in result.findings[:20]:
            _append_window_text(window, "  - " + finding.path + " :: " + finding.message + "\n")
        if len(result.findings) > 20:
            _append_window_text(
                window,
                "  ... "
                + str(len(result.findings) - 20)
                + " additional findings not shown.\n",
            )

    return result


def tab1_audit_source_is_enabled(window: object) -> bool:
    """Return whether the Tab 1 audit docstring source radio is enabled."""
    radio = getattr(window, "_tab1_audit_docstring_radio", None)
    if radio is None:
        return False

    is_checked = getattr(radio, "isChecked", None)
    if callable(is_checked):
        try:
            return bool(is_checked())
        except Exception:
            return False

    checked = getattr(radio, "checked", None)
    return bool(checked)


def _target_kind_from_message(message: str) -> str:
    lowered = message.lower()
    if "module" in lowered:
        return "module"
    if "class" in lowered:
        return "class"
    if "method" in lowered:
        return "method"
    if "function" in lowered:
        return "function"
    return ""


def _append_window_text(window: object, text: str) -> None:
    append_text = getattr(window, "_append_text", None)
    if callable(append_text):
        append_text(text)
        return

    output = getattr(window, "_output", None)
    append_plain_text = getattr(output, "appendPlainText", None)
    if callable(append_plain_text):
        append_plain_text(text.rstrip("\n"))
