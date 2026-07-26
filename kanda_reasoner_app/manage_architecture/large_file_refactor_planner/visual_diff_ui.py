# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/visual_diff_ui.py
"""Read-only visual diff evidence for Large File Refactor Workbench previews."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import difflib
import hashlib
import html
import json
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import preview_runs_root

__all__ = [
    "DEFAULT_CONTEXT_LINES",
    "DEFAULT_MAX_DIFF_ROWS",
    "VISUAL_DIFF_HTML_FILENAME",
    "VISUAL_DIFF_REPORT_FILENAME",
    "VISUAL_DIFF_TEXT_FILENAME",
    "VisualDiffReport",
    "VisualDiffRow",
    "build_multi_file_visual_diff_report",
    "build_visual_diff_report",
    "write_visual_diff_artifacts",
]


VISUAL_DIFF_REPORT_FILENAME = "VISUAL_DIFF_REPORT.json"
VISUAL_DIFF_TEXT_FILENAME = "VISUAL_DIFF_VIEW.txt"
VISUAL_DIFF_HTML_FILENAME = "VISUAL_DIFF_VIEW.html"
DEFAULT_CONTEXT_LINES = 3
DEFAULT_MAX_DIFF_ROWS = 2000


@dataclass(frozen=True)
class VisualDiffRow:
    """One display row in a side-by-side-friendly diff."""

    index: int
    kind: str
    old_lineno: int | None
    new_lineno: int | None
    text: str


@dataclass(frozen=True)
class VisualDiffReport:
    """Read-only visual diff report for preview/UI rendering."""

    status: str
    source_label: str
    target_label: str
    source_sha256: str
    target_sha256: str
    rows: list[VisualDiffRow]
    counts: dict[str, int]
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    visual_diff_enabled: bool = True
    source_mutation_enabled: bool = False
    apply_enabled: bool = False
    import_rewrite_apply_enabled: bool = False
    file_count: int = 1
    file_summaries: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-stable representation."""

        data = asdict(self)
        data["rows"] = [asdict(row) for row in self.rows]
        return data


def _sha256_text(text: str) -> str:
    """Return a stable sha256 for display inputs."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _is_under(child: Path, parent: Path) -> bool:
    """Return whether child is inside parent or equal to parent."""

    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _default_preview_root(project_root: Path) -> Path:
    """Return the selected project's persistent Workbench Preview support root."""
    return preview_runs_root(project_root)


def _allowed_preview_root(project_root: str | Path, preview_root: str | Path | None) -> Path:
    """Resolve and validate a project-support Preview root for visual artifacts."""

    root = Path(project_root).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Project root not found: {root}")
    expected = _default_preview_root(root).resolve()
    chosen = expected if preview_root is None else Path(preview_root).expanduser().resolve()
    if _is_under(chosen, root):
        raise ValueError("Visual diff preview root must not be inside project source.")
    if chosen == expected or _is_under(chosen, expected):
        return chosen
    raise ValueError("Visual diff artifacts must stay under selected project Preview support.")


def _parse_hunk_header(line: str) -> tuple[int, int]:
    """Parse the old/new starting line numbers from a unified diff hunk header."""

    old_start = 0
    new_start = 0
    parts = line.split()
    if len(parts) >= 3:
        old_text = parts[1].lstrip("-").split(",", 1)[0]
        new_text = parts[2].lstrip("+").split(",", 1)[0]
        old_start = int(old_text or "0")
        new_start = int(new_text or "0")
    return old_start, new_start


def build_visual_diff_report(
    source_text: str,
    target_text: str,
    *,
    source_label: str = "source",
    target_label: str = "preview",
    context_lines: int = DEFAULT_CONTEXT_LINES,
    max_rows: int = DEFAULT_MAX_DIFF_ROWS,
) -> VisualDiffReport:
    """Build a read-only visual diff report from two text snapshots."""

    warnings: list[str] = []
    blockers: list[str] = []
    if context_lines < 0:
        blockers.append("NEGATIVE_CONTEXT_LINES")
    if max_rows < 1:
        blockers.append("MAX_ROWS_MUST_BE_POSITIVE")
    if blockers:
        return VisualDiffReport(
            status="blocked",
            source_label=source_label,
            target_label=target_label,
            source_sha256=_sha256_text(source_text),
            target_sha256=_sha256_text(target_text),
            rows=[],
            counts={},
            warnings=warnings,
            blockers=blockers,
        )

    diff_lines = list(
        difflib.unified_diff(
            source_text.splitlines(),
            target_text.splitlines(),
            fromfile=source_label,
            tofile=target_label,
            lineterm="",
            n=context_lines,
        )
    )
    rows: list[VisualDiffRow] = []
    counts = {"equal": 0, "add": 0, "remove": 0, "hunk": 0, "header": 0}
    old_lineno: int | None = None
    new_lineno: int | None = None

    for raw in diff_lines:
        if len(rows) >= max_rows:
            warnings.append("VISUAL_DIFF_TRUNCATED_TO_MAX_ROWS")
            break
        kind = "equal"
        shown_old: int | None = None
        shown_new: int | None = None
        text = raw
        if raw.startswith("--- ") or raw.startswith("+++ "):
            kind = "header"
        elif raw.startswith("@@"):
            kind = "hunk"
            old_start, new_start = _parse_hunk_header(raw)
            old_lineno = old_start
            new_lineno = new_start
        elif raw.startswith("-"):
            kind = "remove"
            shown_old = old_lineno
            old_lineno = None if old_lineno is None else old_lineno + 1
            text = raw[1:]
        elif raw.startswith("+"):
            kind = "add"
            shown_new = new_lineno
            new_lineno = None if new_lineno is None else new_lineno + 1
            text = raw[1:]
        elif raw.startswith(" "):
            kind = "equal"
            shown_old = old_lineno
            shown_new = new_lineno
            old_lineno = None if old_lineno is None else old_lineno + 1
            new_lineno = None if new_lineno is None else new_lineno + 1
            text = raw[1:]
        counts[kind] = counts.get(kind, 0) + 1
        rows.append(VisualDiffRow(len(rows), kind, shown_old, shown_new, text))

    status = "no_changes" if source_text == target_text else "visual_diff_ready"
    return VisualDiffReport(
        status=status,
        source_label=source_label,
        target_label=target_label,
        source_sha256=_sha256_text(source_text),
        target_sha256=_sha256_text(target_text),
        rows=rows,
        counts=counts,
        warnings=warnings,
        blockers=blockers,
    )



def build_multi_file_visual_diff_report(
    comparisons: list[tuple[str, str, str, str]],
    *,
    context_lines: int = DEFAULT_CONTEXT_LINES,
    max_rows: int = DEFAULT_MAX_DIFF_ROWS,
) -> VisualDiffReport:
    """Build one payload-wide visual diff covering replaced and created files."""

    if not comparisons:
        return build_visual_diff_report(
            "",
            "",
            source_label="sealed-payload-empty",
            target_label="sealed-payload-empty",
            max_rows=1,
        )

    rows: list[VisualDiffRow] = []
    counts = {"equal": 0, "add": 0, "remove": 0, "hunk": 0, "header": 0}
    warnings: set[str] = set()
    blockers: set[str] = set()
    summaries: list[dict[str, Any]] = []
    source_fingerprint: list[str] = []
    target_fingerprint: list[str] = []

    for source_text, target_text, source_label, target_label in comparisons:
        remaining = max_rows - len(rows)
        if remaining < 1:
            warnings.add("VISUAL_DIFF_TRUNCATED_TO_MAX_ROWS")
            break
        report = build_visual_diff_report(
            source_text,
            target_text,
            source_label=source_label,
            target_label=target_label,
            context_lines=context_lines,
            max_rows=remaining,
        )
        source_fingerprint.append(source_label + ":" + report.source_sha256)
        target_fingerprint.append(target_label + ":" + report.target_sha256)
        summaries.append(
            {
                "source_label": source_label,
                "target_label": target_label,
                "status": report.status,
                "source_sha256": report.source_sha256,
                "target_sha256": report.target_sha256,
                "counts": dict(report.counts),
                "created_file": source_text == "" and target_text != "",
            }
        )
        for key, value in report.counts.items():
            counts[key] = counts.get(key, 0) + int(value)
        warnings.update(report.warnings)
        blockers.update(report.blockers)
        for row in report.rows:
            rows.append(
                VisualDiffRow(
                    index=len(rows),
                    kind=row.kind,
                    old_lineno=row.old_lineno,
                    new_lineno=row.new_lineno,
                    text=row.text,
                )
            )

    all_unchanged = all(item[0] == item[1] for item in comparisons)
    return VisualDiffReport(
        status="no_changes" if all_unchanged else "visual_diff_ready",
        source_label="MULTI_FILE_SOURCE_SET",
        target_label="SEALED_PAYLOAD_FILE_SET",
        source_sha256=_sha256_text("\n".join(source_fingerprint)),
        target_sha256=_sha256_text("\n".join(target_fingerprint)),
        rows=rows,
        counts=counts,
        warnings=sorted(warnings),
        blockers=sorted(blockers),
        file_count=len(summaries),
        file_summaries=summaries,
    )

def _format_text(report: VisualDiffReport) -> str:
    """Return a compact text rendering of a visual diff report."""

    lines = ["Visual Diff", "===========", "", f"status: {report.status}"]
    lines.append(f"source: {report.source_label} {report.source_sha256}")
    lines.append(f"target: {report.target_label} {report.target_sha256}")
    lines.append("source_mutation_enabled: false")
    lines.append("apply_enabled: false")
    lines.append(f"file_count: {report.file_count}")
    if report.file_summaries:
        lines.append("files:")
        for item in report.file_summaries:
            lines.append(
                "- "
                + str(item.get("target_label", ""))
                + " status="
                + str(item.get("status", ""))
                + " created="
                + str(bool(item.get("created_file", False))).lower()
            )
    lines.append("")
    for row in report.rows:
        old = "" if row.old_lineno is None else str(row.old_lineno)
        new = "" if row.new_lineno is None else str(row.new_lineno)
        marker = {"add": "+", "remove": "-", "hunk": "@", "header": "#"}.get(row.kind, " ")
        lines.append(f"{marker} {old:>5} {new:>5} | {row.text}")
    return "\n".join(lines) + "\n"


def _format_html(report: VisualDiffReport) -> str:
    """Return a minimal standalone HTML diff rendering without scripts."""

    body = [
        "<!doctype html>",
        "<meta charset=\"utf-8\">",
        "<title>Large File Refactor Visual Diff</title>",
        "<style>body{font-family:system-ui, sans-serif;} table{border-collapse:collapse;width:100%;}",
        "td,th{border:1px solid #ddd;padding:4px 6px;font-family:ui-monospace,monospace;}",
        ".add{background:#eaffea}.remove{background:#ffecec}.hunk{background:#eef}.header{background:#f6f6f6}</style>",
        "<h1>Large File Refactor Visual Diff</h1>",
        f"<p>Status: {html.escape(report.status)}</p>",
        "<p>Read-only view. Source mutation and apply are disabled by this artifact.</p>",
        "<table><thead><tr><th>kind</th><th>old</th><th>new</th><th>text</th></tr></thead><tbody>",
    ]
    for row in report.rows:
        cls = html.escape(row.kind)
        old = "" if row.old_lineno is None else str(row.old_lineno)
        new = "" if row.new_lineno is None else str(row.new_lineno)
        body.append(
            f"<tr class=\"{cls}\"><td>{cls}</td><td>{old}</td><td>{new}</td><td>{html.escape(row.text)}</td></tr>"
        )
    body.append("</tbody></table>")
    return "\n".join(body) + "\n"


def write_visual_diff_artifacts(
    project_root: str | Path,
    source_text: str,
    target_text: str,
    *,
    preview_root: str | Path | None = None,
    source_label: str = "source",
    target_label: str = "preview",
    context_lines: int = DEFAULT_CONTEXT_LINES,
    max_rows: int = DEFAULT_MAX_DIFF_ROWS,
) -> VisualDiffReport:
    """Write read-only visual diff artifacts under the project-support Preview root."""

    preview = _allowed_preview_root(project_root, preview_root)
    report = build_visual_diff_report(
        source_text,
        target_text,
        source_label=source_label,
        target_label=target_label,
        context_lines=context_lines,
        max_rows=max_rows,
    )
    preview.mkdir(parents=True, exist_ok=True)
    (preview / VISUAL_DIFF_REPORT_FILENAME).write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (preview / VISUAL_DIFF_TEXT_FILENAME).write_text(_format_text(report), encoding="utf-8")
    (preview / VISUAL_DIFF_HTML_FILENAME).write_text(_format_html(report), encoding="utf-8")
    return report

