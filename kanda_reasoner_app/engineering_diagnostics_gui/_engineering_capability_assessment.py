# project-path: kanda_reasoner_app/engineering_diagnostics_gui/_engineering_capability_assessment.py
"""Assessment helpers for Full Diagnostics Engineering Safety coverage."""

from __future__ import annotations

import hashlib
import re

__all__ = [
    "bounded_evidence",
    "classify_output",
    "correction_guidance",
    "finding_count",
]

_MAX_EVIDENCE_CHARS = 12000


def bounded_evidence(text: str) -> str:
    """Bound verbose command evidence while retaining identity and tail context."""
    value = str(text or "").strip()
    if len(value) <= _MAX_EVIDENCE_CHARS:
        return value
    digest = hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()
    head = value[:8000].rstrip()
    tail = value[-3000:].lstrip()
    return "\n".join(
        (
            head,
            "",
            "[... evidence truncated for handoff ...]",
            "Full evidence SHA256: " + digest,
            "Full evidence characters: " + str(len(value)),
            "",
            tail,
        )
    )


def finding_count(text: str) -> int | None:
    """Return a best-effort finding/item count from public command evidence."""
    patterns = (
        r"(?im)^finding count:\s*(\d+)\s*$",
        r"(?i)(?:^|[;\s])findings=(\d+)(?:[.;\s]|$)",
        r"(?i)(?:^|[;\s])items=(\d+)(?:[.;\s]|$)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match is not None:
            return int(match.group(1))
    return None


def classify_output(
    command_name: str,
    status_code: int,
    stdout: str,
    stderr: str,
    scope_mode: str,
) -> tuple[str, str, str, int | None]:
    """Project command evidence into Diagnostics status without redefining truth."""
    combined = "\n".join((stdout, stderr)).strip()
    lowered = combined.casefold()
    findings = finding_count(combined)

    if status_code != 0:
        return (
            "FAILED",
            "ERROR",
            "Public capability returned non-zero status " + str(status_code) + ".",
            findings,
        )

    if "missing_evidence" in lowered or "missing evidence" in lowered:
        return (
            "MISSING_EVIDENCE",
            "WARNING",
            "Required canonical evidence is missing or unavailable.",
            findings,
        )

    if command_name == "crash-triage" and "no_crash_text" in lowered:
        return (
            "MISSING_EVIDENCE",
            "WARNING",
            "Crash triage needs traceback, log, or runtime trace evidence.",
            findings,
        )

    if (
        "status=needs_owner_review" in lowered
        or "human decision: pending" in lowered
        or "pre_patch_status=facade_patch_risk" in lowered
    ):
        return (
            "MANUAL_REVIEW_REQUIRED",
            "WARNING",
            "Capability output requires an owner or human governance decision.",
            findings,
        )

    if (
        "status=no_matches" in lowered
        or "confidence=low" in lowered
        or "merge status: live_only" in lowered
        or "merge_status: live_only" in lowered
    ):
        return (
            "DEGRADED",
            "WARNING",
            "Capability completed with low-confidence, live-only, or unresolved evidence.",
            findings,
        )

    if command_name == "push-plan" and (
        "overall status: unknown" in lowered
        or "no check results were supplied" in lowered
    ):
        return (
            "NOT_RUN",
            "INFO",
            "This surface provides a validation plan; it did not execute the checks.",
            findings,
        )

    if command_name in {"release-notes", "api-contract", "property-test"}:
        return (
            "DRAFT",
            "INFO",
            "This capability produces governed draft guidance, not project-wide defect truth.",
            findings,
        )

    if findings is not None and findings > 0:
        return (
            "FINDINGS",
            "WARNING",
            "Read-only capability completed with findings requiring review.",
            findings,
        )

    if scope_mode == "TARGETED_SMOKE":
        return (
            "TARGETED_SMOKE_COMPLETE",
            "INFO",
            (
                "Canonical smoke target completed. This is tool-health evidence, "
                "not exhaustive project coverage."
            ),
            findings,
        )

    return (
        "CLEAN",
        "INFO",
        "Capability completed without an explicit warning or failure marker.",
        findings,
    )


def correction_guidance(
    command_name: str,
    status: str,
    stderr: str,
) -> str:
    """Return bounded correction guidance based only on deterministic status."""
    if status == "FAILED":
        detail = str(stderr or "").strip()
        suffix = ""
        if detail:
            suffix = " Failure evidence begins: " + detail.splitlines()[0]
        return (
            "Inspect the public owner implementation for "
            + command_name
            + ", reproduce the exact failure, and correct the smallest canonical "
            "owner without bypassing Box boundaries."
            + suffix
        )

    if status == "MISSING_EVIDENCE":
        return (
            "Restore or regenerate required canonical evidence through its "
            "existing owner before treating downstream conclusions as authoritative."
        )

    if status in {"MANUAL_REVIEW_REQUIRED", "DEGRADED"}:
        return (
            "Use exact source plus owner evidence to resolve ambiguity before "
            "editing. Do not promote low-confidence output into source truth."
        )

    if status == "FINDINGS":
        return (
            "Use this capability evidence together with structured correction "
            "groups to identify exact affected files and focused validation."
        )

    return "No automatic correction is authorized by this capability assessment."
