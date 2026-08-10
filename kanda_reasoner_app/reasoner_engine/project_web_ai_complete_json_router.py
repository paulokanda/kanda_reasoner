# project-path: kanda_reasoner_app/reasoner_engine/
# project_web_ai_complete_json_router.py
"""Build bounded question-specific context from verified complete-JSON evidence."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from kanda_reasoner_app.project_analysis_evidence_paths import (
    primary_evidence_json_path,
    working_copy_json_path,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_complete_json_sections import (
    APPROVED_COMPLETE_JSON_SECTIONS,
    SmartCompleteJsonReadError,
    complete_json_section_fingerprint,
    extract_complete_json_sections,
)

__all__ = [
    "RoutedProjectContext",
    "SmartProjectContextError",
    "build_remote_approval_text",
    "route_complete_json_context",
]

MAX_ROUTED_CONTEXT_BYTES = 64 * 1024
MAX_RECORD_TEXT = 12 * 1024
MAX_RECORDS = 28
_SECTION_LIMITS = {
    "web_ai_symbol_index": 7,
    "primary_definition_index": 5,
    "entry_points_detail": 4,
    "web_ai_file_responsibility_index": 6,
    "web_ai_test_protection_index": 6,
    "stable_evidence_id_index": 3,
}
_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do",
    "does", "for", "from", "how", "i", "in", "is", "it", "of", "on",
    "or", "project", "python", "the", "this", "to", "use", "what",
    "where", "which", "with",
}
_TOKEN_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,}")
_IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")


class SmartProjectContextError(RuntimeError):
    """Raised when present complete-JSON evidence is unsafe or malformed."""


@dataclass(frozen=True)
class RoutedProjectContext:
    """One bounded Project context prepared for a single approved question."""

    context_text: str
    context_bytes: int
    evidence_context_hash: str
    source_label: str
    source_status: str
    source_fingerprint: str
    record_count: int
    sections_used: tuple[str, ...]
    fallback_reason: str = ""

    @property
    def smart_context_used(self) -> bool:
        """Return whether complete-JSON evidence was included."""
        return self.record_count > 0

    def approval_summary(self) -> str:
        """Return a compact non-secret transmission summary."""
        if self.smart_context_used:
            return (
                "Smart complete-JSON context: enabled\n"
                "Complete-JSON source: " + self.source_label + "\n"
                "Routed evidence records: " + str(self.record_count) + "\n"
                "Routed sections: " + ", ".join(self.sections_used) + "\n"
                "Evidence context hash: " + self.evidence_context_hash[:16]
            )
        reason = self.fallback_reason or "no relevant complete-JSON evidence"
        return (
            "Smart complete-JSON context: compact fallback\n"
            "Fallback reason: " + reason + "\n"
            "Evidence context hash: " + self.evidence_context_hash[:16]
        )


def _tokens(text: str) -> tuple[str, ...]:
    """Return deterministic searchable tokens for one question or record."""
    found: list[str] = []
    seen: set[str] = set()
    for match in _TOKEN_PATTERN.findall(str(text or "")):
        token = match.casefold()
        parts = [part for part in token.split("_") if part]
        for candidate in (token, *parts):
            if len(candidate) < 2 or candidate in _STOPWORDS or candidate in seen:
                continue
            seen.add(candidate)
            found.append(candidate)
    return tuple(found[:40])



def _exact_identifiers(text: str) -> tuple[str, ...]:
    """Return exact code identifiers explicitly named in one question."""
    found: list[str] = []
    for raw in _IDENTIFIER_PATTERN.findall(str(text or "")):
        folded = raw.casefold()
        is_camel = (
            not raw.isupper()
            and any(character.isupper() for character in raw[1:])
        )
        if "_" not in folded and not is_camel:
            continue
        if folded.endswith("_") or folded.startswith(("validate_", "test_")):
            continue
        if folded not in found:
            found.append(folded)
    return tuple(found[:24])


def _is_protection_source_record(value: object) -> bool:
    """Return whether a protection record describes a validator or test file."""
    if not isinstance(value, Mapping):
        return False
    path = str(value.get("file", "")).replace("\\", "/").casefold()
    if path.startswith("tools/validate_") and path.endswith(".py"):
        return True
    parts = path.split("/")
    return "tests" in parts or "test" in Path(path).name


def _record_text(key: str, value: object) -> str:
    """Return bounded searchable text for one complete-JSON record."""
    try:
        payload = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError):
        payload = str(value)
    return (str(key) + " " + payload)[:MAX_RECORD_TEXT]


def _score_record(
    question_tokens: tuple[str, ...],
    exact_identifiers: tuple[str, ...],
    key: str,
    value: object,
) -> int:
    """Score one record against the current user question."""
    if not question_tokens:
        return 0
    key_folded = str(key).casefold()
    text_folded = _record_text(key, value).casefold()
    score = 0
    for token in question_tokens:
        if token == key_folded:
            score += 18
        elif token in key_folded:
            score += 10
        score += min(text_folded.count(token), 5) * 2
    for identifier in exact_identifiers:
        if identifier == key_folded:
            score += 240
        elif identifier in key_folded:
            score += 160
        if identifier in text_folded:
            score += 120
    return score


def _iter_records(value: object) -> Iterable[tuple[str, object]]:
    if isinstance(value, Mapping):
        for key in sorted(value, key=lambda item: str(item).casefold()):
            yield str(key), value[key]
    elif isinstance(value, list):
        for index, item in enumerate(value):
            key = "item_" + str(index)
            if isinstance(item, Mapping):
                for candidate in (
                    "qualified_name",
                    "name",
                    "path",
                    "file",
                    "source_file",
                    "entry_point",
                ):
                    if item.get(candidate):
                        key = str(item[candidate])
                        break
            yield key, item


def _select_records(
    sections: Mapping[str, object],
    question: str,
) -> dict[str, list[dict[str, object]]]:
    """Select the highest-signal records under deterministic section limits."""
    question_tokens = _tokens(question)
    exact_identifiers = _exact_identifiers(question)
    selected: dict[str, list[dict[str, object]]] = {}
    remaining = MAX_RECORDS
    for section in APPROVED_COMPLETE_JSON_SECTIONS:
        if remaining <= 0 or section not in sections:
            continue
        candidates: list[tuple[int, str, object]] = []
        for key, value in _iter_records(sections[section]):
            if (
                section == "web_ai_test_protection_index"
                and _is_protection_source_record(value)
            ):
                continue
            score = _score_record(
                question_tokens, exact_identifiers, key, value
            )
            if score > 0:
                candidates.append((score, key, value))
        candidates.sort(key=lambda item: (-item[0], item[1].casefold()))
        limit = min(_SECTION_LIMITS[section], remaining)
        records = [
            {"key": key, "score": score, "evidence": value}
            for score, key, value in candidates[:limit]
        ]
        if records:
            selected[section] = records
            remaining -= len(records)
    return selected


def _redact_root(text: str, project_root: str | Path) -> str:
    """Replace the active Project absolute path with its trust-boundary marker."""
    supplied_root = str(project_root)
    root = Path(project_root).expanduser().resolve(strict=False)
    redacted = str(text)
    raw_values = (
        supplied_root,
        supplied_root.replace("\\", "/"),
        str(root),
        root.as_posix(),
    )
    candidates: list[str] = []
    for raw in raw_values:
        if not raw:
            continue
        candidates.append(raw)
        candidates.append(json.dumps(raw, ensure_ascii=True)[1:-1])
    for raw in sorted(set(candidates), key=len, reverse=True):
        redacted = redacted.replace(raw, "<PROJECT_ROOT>")
    return redacted


def _bounded_route_text(payload: Mapping[str, object]) -> str:
    """Serialize and trim routed evidence without splitting UTF-8 code points."""
    prefix = "\n===== SMART COMPLETE JSON ROUTE =====\n"
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    encoded = (prefix + text + "\n").encode("utf-8")
    if len(encoded) <= MAX_ROUTED_CONTEXT_BYTES:
        return encoded.decode("utf-8")

    compact = dict(payload)
    evidence = compact.get("routed_evidence")
    if isinstance(evidence, dict):
        trimmed: dict[str, object] = {}
        for name in APPROVED_COMPLETE_JSON_SECTIONS:
            records = evidence.get(name)
            if isinstance(records, list):
                trimmed[name] = records[: max(1, len(records) // 2)]
        compact["routed_evidence"] = trimmed
        compact["truncated_to_budget"] = True
    encoded = (
        prefix
        + json.dumps(compact, ensure_ascii=False, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    if len(encoded) > MAX_ROUTED_CONTEXT_BYTES:
        raise SmartProjectContextError("SMART_CONTEXT_OUTPUT_BUDGET_EXCEEDED")
    return encoded.decode("utf-8")


def _fallback(compact_context: str, reason: str) -> RoutedProjectContext:
    digest = hashlib.sha256()
    digest.update(compact_context.encode("utf-8"))
    digest.update(reason.encode("utf-8"))
    return RoutedProjectContext(
        context_text=compact_context,
        context_bytes=len(compact_context.encode("utf-8")),
        evidence_context_hash=digest.hexdigest(),
        source_label="",
        source_status="compact_fallback",
        source_fingerprint="",
        record_count=0,
        sections_used=(),
        fallback_reason=reason,
    )


def _resolve_read_only_complete_json(
    project_root: str | Path,
) -> tuple[Path | None, str, str]:
    """Resolve existing complete-JSON evidence without creating cache files."""
    root = Path(project_root).expanduser().resolve(strict=False)
    candidates = (
        (
            working_copy_json_path(root).resolve(strict=False),
            "Show Project to AI local complete JSON",
            "show_project_local",
        ),
        (
            primary_evidence_json_path(root).resolve(strict=False),
            "loose canonical complete JSON",
            "loose",
        ),
    )
    for path, label, status in candidates:
        if path.is_file() and path.stat().st_size > 0:
            return path, label, status
    return None, "", "missing"


def route_complete_json_context(
    project_root: str | Path,
    question: str,
    compact_context: str,
) -> RoutedProjectContext:
    """Append bounded complete-JSON evidence relevant to one question."""
    try:
        path, source_label, source_status = _resolve_read_only_complete_json(
            project_root
        )
    except Exception as exc:
        raise SmartProjectContextError(
            "SMART_CONTEXT_SOURCE_RESOLUTION_FAILED:" + str(exc)
        ) from exc
    if path is None:
        return _fallback(compact_context, "verified complete JSON is unavailable")

    try:
        sections = extract_complete_json_sections(path)
    except SmartCompleteJsonReadError as exc:
        raise SmartProjectContextError(str(exc)) from exc
    if not sections:
        return _fallback(
            compact_context,
            "complete JSON has no approved Web-AI routing sections",
        )
    selected = _select_records(sections, question)
    if not selected:
        return _fallback(
            compact_context,
            "no complete-JSON records matched the current question",
        )

    source_fingerprint = complete_json_section_fingerprint(path, sections)
    record_count = sum(len(records) for records in selected.values())
    payload = {
        "authority": "generated routing evidence; exact source remains authoritative",
        "question_tokens": list(_tokens(question)),
        "source": {
            "label": source_label,
            "status": source_status,
            "fingerprint": source_fingerprint,
        },
        "routed_evidence": selected,
        "record_count": record_count,
        "instructions": [
            "Use these records to locate likely source and tests.",
            "Use bounded read-only Project tools for exact source before "
            "proposing edits.",
            "Do not treat generated evidence as source truth.",
        ],
    }
    route_text = _redact_root(_bounded_route_text(payload), project_root)
    combined = compact_context + route_text
    digest = hashlib.sha256()
    digest.update(source_fingerprint.encode("ascii"))
    digest.update(question.encode("utf-8"))
    digest.update(route_text.encode("utf-8"))
    return RoutedProjectContext(
        context_text=combined,
        context_bytes=len(combined.encode("utf-8")),
        evidence_context_hash=digest.hexdigest(),
        source_label=source_label,
        source_status=source_status,
        source_fingerprint=source_fingerprint,
        record_count=record_count,
        sections_used=tuple(selected),
    )


def build_remote_approval_text(
    profile: object,
    model: object,
    snapshot: object,
    routed_context: RoutedProjectContext,
    *,
    api_key_provided: bool,
    read_tools_enabled: bool,
) -> str:
    """Return the exact per-request cloud transmission summary."""
    key_state = "provided" if api_key_provided else "not provided"
    read_tools = "enabled" if read_tools_enabled else "disabled"
    price_label = getattr(model, "price_label")()
    return (
        "You are about to send project context to a remote AI provider.\n\n"
        "Provider: " + str(getattr(profile, "display_name")) + "\n"
        "Model: " + str(getattr(model, "model_id")) + "\n"
        "Model cost status: " + str(price_label) + "\n"
        "API key: " + key_state + "\n"
        "Project: " + str(getattr(snapshot, "project_slug")) + "\n"
        "Snapshot: " + str(getattr(snapshot, "short_hash")()) + "\n"
        "Context: " + f"{routed_context.context_bytes:,} bytes" + "\n"
        "Bounded read-only Project tools: " + read_tools + "\n"
        "Conversation persistence: memory only\n\n"
        + routed_context.approval_summary()
        + "\n\n"
        + str(getattr(profile, "privacy_summary"))
        + "\n\nApprove this request?"
    )
