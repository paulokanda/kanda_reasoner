# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_shadow.py
"""Create and validate transient Shadow previews for Project Web AI proposals.

Shadow previews are written only below the selected Project daily-work root.
This module never changes active Project source or durable Project Support.
"""

from __future__ import annotations

import hashlib
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.reasoner_engine.project_web_ai_change_contracts import (
    ProjectWebAIChangeOperation,
    ProjectWebAIChangeProposal,
    ProjectWebAIChangeTarget,
)

__all__ = [
    "ProjectWebAIShadowError",
    "ProjectWebAIShadowPreview",
    "ShadowTargetPreview",
    "build_shadow_preview",
    "delete_shadow_preview",
]

_HUNK_HEADER = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? "
    r"\+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@(?: .*)?$"
)


class ProjectWebAIShadowError(RuntimeError):
    """Raised when a proposal cannot be safely materialized in Shadow."""


@dataclass(frozen=True)
class ShadowTargetPreview:
    """Describe one validated Shadow target."""

    relative_path: str
    original_sha256: str
    proposed_sha256: str
    shadow_path: str
    unified_diff: str
    python_syntax_status: str


@dataclass(frozen=True)
class ProjectWebAIShadowPreview:
    """Represent one transient, validated, source-unchanged Preview."""

    operation_id: str
    shadow_root: str
    summary: str
    targets: tuple[ShadowTargetPreview, ...]
    affected_public_contracts: tuple[str, ...]
    required_validators: tuple[str, ...]
    known_risks: tuple[str, ...]
    validation_markers: tuple[str, ...]


def build_shadow_preview(
    operation: ProjectWebAIChangeOperation,
    proposal: ProjectWebAIChangeProposal,
) -> ProjectWebAIShadowPreview:
    """Apply one current proposal only to a fresh transient Shadow tree."""
    if proposal.operation_id != operation.operation_id:
        raise ProjectWebAIShadowError("SHADOW_OPERATION_IDENTITY_MISMATCH")
    project_root = _canonical_directory(operation.project_root)
    daily_root = _canonical_or_create_daily_root(operation.daily_work_root)
    _require_distinct_transient_root(project_root, daily_root)
    shadow_root = (
        daily_root
        / "project_web_ai_prepare_changes"
        / operation.operation_id
        / "shadow"
    )
    operation_root = shadow_root.parent
    if operation_root.exists():
        shutil.rmtree(operation_root)
    shadow_root.mkdir(parents=True, exist_ok=False)

    source_map = operation.source_by_path()
    previews: list[ShadowTargetPreview] = []
    markers = [
        "PROPOSAL_IDENTITY: PASS",
        "TARGET_PATH_CONTAINMENT: PASS",
    ]
    try:
        for target in proposal.targets:
            source = source_map[target.relative_path]
            live_path = _contained_file(project_root, target.relative_path)
            raw = live_path.read_bytes()
            current_sha256 = hashlib.sha256(raw).hexdigest()
            if current_sha256 != source.sha256:
                raise ProjectWebAIShadowError(
                    "STALE_SOURCE_HASH:" + target.relative_path
                )
            proposed_text = apply_unified_diff(
                source.text,
                target,
                newline=source.newline,
            )
            syntax_status = _validate_python_syntax(
                target.relative_path,
                proposed_text,
            )
            proposed_raw = _encode_source(source, proposed_text)
            shadow_path = _contained_shadow_path(shadow_root, target.relative_path)
            shadow_path.parent.mkdir(parents=True, exist_ok=True)
            shadow_path.write_bytes(proposed_raw)
            if live_path.read_bytes() != raw:
                raise ProjectWebAIShadowError(
                    "PROJECT_SOURCE_CHANGED_DURING_SHADOW:" + target.relative_path
                )
            previews.append(
                ShadowTargetPreview(
                    relative_path=target.relative_path,
                    original_sha256=current_sha256,
                    proposed_sha256=hashlib.sha256(proposed_raw).hexdigest(),
                    shadow_path=str(shadow_path),
                    unified_diff=target.unified_diff,
                    python_syntax_status=syntax_status,
                )
            )
        markers.extend(
            (
                "SOURCE_HASH_FRESHNESS: PASS",
                "SHADOW_APPLY: PASS",
                "PROJECT_SOURCE_UNCHANGED: PASS",
            )
        )
        if any(item.python_syntax_status == "PASS" for item in previews):
            markers.append("PYTHON_SYNTAX: PASS")
        else:
            markers.append("PYTHON_SYNTAX: NOT_APPLICABLE")
        preview = ProjectWebAIShadowPreview(
            operation_id=operation.operation_id,
            shadow_root=str(shadow_root),
            summary=proposal.summary,
            targets=tuple(previews),
            affected_public_contracts=proposal.affected_public_contracts,
            required_validators=proposal.required_validators,
            known_risks=proposal.known_risks,
            validation_markers=tuple(markers),
        )
        return preview
    except Exception:
        if operation_root.exists():
            shutil.rmtree(operation_root, ignore_errors=True)
        raise


def delete_shadow_preview(preview: ProjectWebAIShadowPreview | None) -> None:
    """Delete one abandoned transient Preview without touching Project source."""
    if preview is None:
        return
    shadow_root = Path(preview.shadow_root)
    operation_root = shadow_root.parent
    if operation_root.name == "":
        return
    shutil.rmtree(operation_root, ignore_errors=True)


def apply_unified_diff(
    original_text: str,
    target: ProjectWebAIChangeTarget,
    *,
    newline: str,
) -> str:
    """Apply one strict same-file unified diff to source text in memory."""
    diff_lines = target.unified_diff.replace("\r\n", "\n").split("\n")
    while diff_lines and diff_lines[-1] == "":
        diff_lines.pop()
    if len(diff_lines) < 3:
        raise ProjectWebAIShadowError(
            "UNIFIED_DIFF_TOO_SHORT:" + target.relative_path
        )
    old_path = _diff_header_path(diff_lines[0], "--- ")
    new_path = _diff_header_path(diff_lines[1], "+++ ")
    if old_path != target.relative_path or new_path != target.relative_path:
        raise ProjectWebAIShadowError(
            "UNIFIED_DIFF_PATH_MISMATCH:" + target.relative_path
        )

    original_lines = original_text.replace("\r\n", "\n").split("\n")
    original_had_newline = original_text.endswith(("\n", "\r"))
    if original_had_newline and original_lines and original_lines[-1] == "":
        original_lines.pop()
    result: list[str] = []
    source_index = 0
    line_index = 2
    saw_hunk = False
    output_no_newline = not original_had_newline

    while line_index < len(diff_lines):
        header = diff_lines[line_index]
        match = _HUNK_HEADER.match(header)
        if match is None:
            raise ProjectWebAIShadowError(
                "INVALID_UNIFIED_DIFF_HUNK_HEADER:" + header[:120]
            )
        saw_hunk = True
        old_start = int(match.group("old_start"))
        old_count = int(match.group("old_count") or "1")
        new_count = int(match.group("new_count") or "1")
        expected_index = max(0, old_start - 1)
        if expected_index < source_index or expected_index > len(original_lines):
            raise ProjectWebAIShadowError(
                "UNIFIED_DIFF_HUNK_RANGE_INVALID:" + target.relative_path
            )
        result.extend(original_lines[source_index:expected_index])
        source_index = expected_index
        line_index += 1
        consumed_old = 0
        produced_new = 0
        while (
            line_index < len(diff_lines)
            and not diff_lines[line_index].startswith("@@ ")
        ):
            line = diff_lines[line_index]
            line_index += 1
            if line == "\\ No newline at end of file":
                output_no_newline = True
                continue
            if not line:
                raise ProjectWebAIShadowError(
                    "UNIFIED_DIFF_LINE_PREFIX_MISSING:" + target.relative_path
                )
            prefix = line[0]
            payload = line[1:]
            if prefix == " ":
                _require_source_line(original_lines, source_index, payload, target)
                result.append(payload)
                source_index += 1
                consumed_old += 1
                produced_new += 1
            elif prefix == "-":
                _require_source_line(original_lines, source_index, payload, target)
                source_index += 1
                consumed_old += 1
            elif prefix == "+":
                result.append(payload)
                produced_new += 1
            else:
                raise ProjectWebAIShadowError(
                    "UNIFIED_DIFF_LINE_PREFIX_INVALID:" + target.relative_path
                )
        if consumed_old != old_count or produced_new != new_count:
            raise ProjectWebAIShadowError(
                "UNIFIED_DIFF_HUNK_COUNT_MISMATCH:" + target.relative_path
            )

    if not saw_hunk:
        raise ProjectWebAIShadowError("UNIFIED_DIFF_HAS_NO_HUNKS")
    result.extend(original_lines[source_index:])
    text = newline.join(result)
    if not output_no_newline:
        text += newline
    return text


def _diff_header_path(line: str, prefix: str) -> str:
    """Return one normalized same-file path from a unified diff header."""
    if not line.startswith(prefix):
        raise ProjectWebAIShadowError("UNIFIED_DIFF_HEADER_MISSING:" + prefix.strip())
    value = line[len(prefix):].split("\t", 1)[0].strip().replace("\\", "/")
    if value.startswith("a/") or value.startswith("b/"):
        value = value[2:]
    unsafe = (
        not value
        or value == "/dev/null"
        or value.startswith("/")
        or ".." in value.split("/")
    )
    if unsafe:
        raise ProjectWebAIShadowError("UNSAFE_UNIFIED_DIFF_PATH:" + value)
    return value


def _require_source_line(
    original_lines: list[str],
    source_index: int,
    payload: str,
    target: ProjectWebAIChangeTarget,
) -> None:
    """Require exact hunk context against current selected source."""
    if source_index >= len(original_lines) or original_lines[source_index] != payload:
        raise ProjectWebAIShadowError(
            "UNIFIED_DIFF_CONTEXT_MISMATCH:" + target.relative_path
        )


def _validate_python_syntax(relative_path: str, text: str) -> str:
    """Compile Python source in memory without importing or executing it."""
    if not relative_path.lower().endswith(".py"):
        return "NOT_APPLICABLE"
    try:
        compile(text, relative_path, "exec")
    except SyntaxError as exc:
        raise ProjectWebAIShadowError(
            "PYTHON_SYNTAX_ERROR:"
            + relative_path
            + ":"
            + str(exc.lineno or 0)
            + ":"
            + str(exc.msg)
        ) from exc
    return "PASS"


def _encode_source(source: object, text: str) -> bytes:
    """Encode Shadow source using the selected file UTF-8 BOM contract."""
    raw = text.encode("utf-8")
    if bool(getattr(source, "had_utf8_bom", False)):
        return b"\xef\xbb\xbf" + raw
    return raw


def _canonical_directory(path_value: str | Path) -> Path:
    """Return one existing canonical directory."""
    path = Path(path_value).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ProjectWebAIShadowError("PROJECT_ROOT_IS_NOT_A_DIRECTORY")
    return path


def _canonical_or_create_daily_root(path_value: str | Path) -> Path:
    """Return the selected Project transient root, creating it when absent."""
    path = Path(path_value).expanduser().resolve(strict=False)
    path.mkdir(parents=True, exist_ok=True)
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise ProjectWebAIShadowError("DAILY_WORK_ROOT_IS_NOT_A_DIRECTORY")
    return resolved



def _require_distinct_transient_root(project_root: Path, daily_root: Path) -> None:
    """Reject transient storage that overlaps active Project source."""
    if project_root == daily_root:
        raise ProjectWebAIShadowError("DAILY_WORK_ROOT_EQUALS_PROJECT_ROOT")
    try:
        daily_root.relative_to(project_root)
    except ValueError:
        pass
    else:
        raise ProjectWebAIShadowError("DAILY_WORK_ROOT_INSIDE_PROJECT_ROOT")
    try:
        project_root.relative_to(daily_root)
    except ValueError:
        pass
    else:
        raise ProjectWebAIShadowError("PROJECT_ROOT_INSIDE_DAILY_WORK_ROOT")

def _contained_file(root: Path, relative_path: str) -> Path:
    """Return one existing regular file contained in Project root."""
    candidate = (root / Path(relative_path)).resolve(strict=True)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ProjectWebAIShadowError(
            "PROJECT_SOURCE_PATH_ESCAPE:" + relative_path
        ) from exc
    if not candidate.is_file():
        raise ProjectWebAIShadowError("PROJECT_SOURCE_FILE_MISSING:" + relative_path)
    return candidate


def _contained_shadow_path(shadow_root: Path, relative_path: str) -> Path:
    """Return one not-yet-required Shadow path contained in its operation root."""
    candidate = (shadow_root / Path(relative_path)).resolve(strict=False)
    try:
        candidate.relative_to(shadow_root)
    except ValueError as exc:
        raise ProjectWebAIShadowError("SHADOW_PATH_ESCAPE:" + relative_path) from exc
    return candidate
