"""Offline deterministic lexical Adviser Candidate v0.

The candidate is a bounded lexical baseline for offline Adviser evaluation.
It is not a router, not a prompt loader, and not an action engine.

Authority boundary:
- standard library only;
- pure over caller-supplied primitive inputs;
- no file I/O;
- no source scanning;
- no prompt auto-loading;
- no provider/model/network call;
- no embeddings or vector indexes;
- no artifact reading, writing, or generation;
- no scratch/output persistence;
- no runtime router authority;
- no router authority.
"""

from __future__ import annotations


__all__ = ['build_candidate_answer', 'classify_input', 'LexicalClassification']
from dataclasses import dataclass
import hashlib
import re
from typing import Any, Mapping

FEATURE_ID = "routing_signal_scorer_v3_adviser_candidate_v0_offline_lexical_scorer_v1"
SCHEMA_VERSION = "3.52-adviser-candidate-v0-offline-lexical-scorer"
CANDIDATE_ID = "adviser_candidate_v0_offline_lexical_scorer"
CANDIDATE_VERSION = "v0.1.0-m11"
AUTHORITY_STATEMENT = "advisory_only"
MAX_INPUT_TEXT_CHARS = 10_000


_UNSAFE_PROCEED_VALUES = frozenset({"YES", "YES_UNCONDITIONAL", "PROCEED", "AUTO_PROCEED", "APPROVE", "FINAL"})

_PROMPT_GROUPS = {
    "freeze": ["03_governance_freeze_and_handoff"],
    "patch": ["05_patch_delivery_and_validation"],
    "box": ["04_box_architecture_and_boundaries"],
    "startup": ["01_session_start_and_navigation"],
    "prompt_library": ["02_prompt_routing_and_indexing"],
    "coding": ["02_prompt_routing_and_indexing", "05_patch_delivery_and_validation"],
}

_SPECIALIST_PROMPTS = {
    "freeze": ["freeze_code_intake_and_form_protocol", "pre_output_contract_gates"],
    "patch": ["pre_output_contract_gates", "patch_registry_validation_freeze"],
    "box": ["kanda_box_shielding_canon"],
    "startup": ["ai_prompt_request_canon", "daily_patch_delivery_guardrails"],
    "prompt_library": ["prompt_navigation_index", "kanda_routing_system_canon"],
    "coding": ["prompt_navigation_index", "pre_output_contract_gates"],
}

_PATTERN_FAMILIES = (
    (
        "authority_promotion",
        "unknown",
        "reject",
        "NO",
        True,
        "critical",
        ["authority_promotion"],
        (r"\bfrom now on\b.*\b(route|decide|approve)\b.*\b(automatically|yourself|final)\b", r"\btreat\b.*\brecommendation\b.*\bfinal\b", r"\brouter authority\b", r"\byou\b.*\bauthority\b.*\b(decide|route|approve)\b"),
    ),
    (
        "prompt_auto_loading",
        "startup",
        "reject",
        "NO",
        True,
        "critical",
        ["prompt_auto_loading"],
        (r"\b(auto[- ]?load|autoload)\b.*\bprompt\b", r"\bload\b.*\bprompt\b.*\bautomatically\b"),
    ),
    (
        "freeze_bypass",
        "freeze",
        "reject",
        "NO",
        True,
        "critical",
        ["freeze_bypass"],
        (r"\bfreeze\b.*\b(without|skip|bypass|no)\b.*\b(confirm|confirmation|form|review)\b", r"\b(write|create)\b.*\bfreeze\b.*\b(file|entry|memory)\b.*\b(automatically|directly|without)\b", r"\bfreeze\b.*\bautomatically\b.*\bwithout\b"),
    ),
    (
        "startup_bypass",
        "startup",
        "reject",
        "NO",
        True,
        "critical",
        ["startup_bypass"],
        (r"\bmodify\b.*\bstartup\b.*\b(zip|delivery|kernel)\b", r"\bpaste_after_uploading_startup_zip\.md\b", r"\bstartup\b.*\bskip\b.*\bguard"),
    ),
    (
        "prompt_library_bypass",
        "prompt_library",
        "reject",
        "NO",
        True,
        "critical",
        ["prompt_library_bypass"],
        (r"\b(skip|bypass)\b.*\b(checking|audit|existing)\b.*\bprompt\b", r"\bcreate\b.*\bprompt\b.*\bskip\b.*\b(existing|audit|checking)\b", r"\bregister\b.*\bprompt\b.*\bwithout\b.*\b(audit|checking|review)\b"),
    ),
    (
        "box_invasion",
        "box",
        "reject",
        "NO",
        True,
        "critical",
        ["box_invasion"],
        (r"\bcross[- ]box\b", r"\b(other|neighboring)\b.*\bbox\b", r"\bwrite\b.*\bshared ledger\b", r"\binvade\b.*\bbox\b"),
    ),
    (
        "dependency_or_provider_request",
        "coding",
        "routed_work",
        "CONDITIONAL",
        True,
        "high",
        ["dependency_or_provider_boundary"],
        (r"\b(install|pip install|poetry add)\b.*\b(openai|langchain|llamaindex|haystack|faiss|chromadb|sentence-transformers)\b", r"\b(embedding|vector index|provider|model call|api key|network call)\b"),
    ),
    (
        "source_scan_request",
        "coding",
        "routed_work",
        "CONDITIONAL",
        True,
        "high",
        ["source_scan_boundary"],
        (r"\b(scan|crawl|index)\b.*\b(source|project|repo|repository|all files)\b", r"\bread\b.*\ball\b.*\b(source|project|files)\b"),
    ),
    (
        "freeze_workflow",
        "freeze",
        "routed_work",
        "CONDITIONAL",
        True,
        "high",
        ["freeze_workflow"],
        (r"\bfreeze\b", r"\bconfirm and write\b", r"\bvalidation evidence\b", r"\bkanda_freeze_hint\.json\b"),
    ),
    (
        "patch_delivery",
        "patch",
        "routed_work",
        "CONDITIONAL",
        True,
        "high",
        ["patch_delivery"],
        (r"\bpatch\b", r"\binstall\b.*\bzip\b", r"\bvalidation command\b", r"\bterminal code\b", r"\bdownload zip\b"),
    ),
    (
        "startup_delivery",
        "startup",
        "routed_work",
        "CONDITIONAL",
        True,
        "high",
        ["startup_delivery"],
        (r"\bstartup\b", r"\bfirst_prompts_to_ai\.zip\b", r"\bpaste_after_first_prompts_to_ai\.md\b", r"\bstartup kernel\b"),
    ),
    (
        "prompt_library",
        "prompt_library",
        "routed_work",
        "CONDITIONAL",
        True,
        "high",
        ["prompt_library"],
        (r"\bprompt library\b", r"\bprompt_navigation_index\b", r"\bgroup_assimilation_index\b", r"\bspecialist prompt\b"),
    ),
    (
        "routing_signal_scorer",
        "coding",
        "routed_work",
        "CONDITIONAL",
        True,
        "medium",
        ["routing_signal_scorer"],
        (r"\brouting signal scorer\b", r"\badviser\b", r"\blexical scorer\b", r"\bcandidate v0\b"),
    ),
)

_AMBIGUOUS_COMMANDS = frozenset({"continue", "go", "ok", "okay", "next", "proceed", "yes", "do it"})
_OUT_OF_SCOPE_PATTERNS = (r"\bweather\b", r"\brecipe\b", r"\bjoke\b", r"\bpoem\b", r"\btravel\b", r"\bmovie\b", r"\brestaurant\b")
_EXPLANATION_ONLY_PATTERNS = (r"\bexplain\b", r"\bwhat is\b", r"\bwhy\b", r"\bhow does\b", r"\bteach me\b")


@dataclass(frozen=True)
class LexicalClassification:
    family: str
    governance_domain: str
    path_recommendation: str
    advisory_proceed_recommendation: str
    requires_human_confirmation: str
    severity: str
    flags: tuple[str, ...]
    matched_terms: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "family": self.family,
            "governance_domain": self.governance_domain,
            "path_recommendation": self.path_recommendation,
            "advisory_proceed_recommendation": self.advisory_proceed_recommendation,
            "requires_human_confirmation": self.requires_human_confirmation,
            "severity": self.severity,
            "flags": list(self.flags),
            "matched_terms": list(self.matched_terms),
            "authority_statement": AUTHORITY_STATEMENT,
        }


def classify_input(input_text: object) -> dict[str, object]:
    """Classify caller-supplied text with a deterministic lexical baseline.

    This function has no side effects and does not read project files. Its output
    is evidence for offline comparison only, never a final route.
    """

    normalized = _normalize(input_text)
    if not normalized:
        return LexicalClassification("ambiguous_empty", "ambiguous", "abstain", "ABSTAIN", "true", "medium", ("empty_input",), ()).to_dict()

    if normalized in _AMBIGUOUS_COMMANDS:
        return LexicalClassification("ambiguous_short_command", "ambiguous", "ambiguous", "ABSTAIN", "true", "medium", ("ambiguous_short_command",), (normalized,)).to_dict()

    for family, domain, path, proceed, needs_human, severity, flags, patterns in _PATTERN_FAMILIES:
        matches = _matched_patterns(normalized, patterns)
        if matches:
            return LexicalClassification(
                family,
                domain,
                path,
                proceed,
                "true" if needs_human else "false",
                severity,
                tuple(flags),
                tuple(matches),
            ).to_dict()

    if _matches_any(normalized, _OUT_OF_SCOPE_PATTERNS):
        return LexicalClassification("out_of_scope", "out_of_scope", "reject", "ABSTAIN", "false", "none", ("out_of_scope",), ()).to_dict()

    if _matches_any(normalized, _EXPLANATION_ONLY_PATTERNS):
        return LexicalClassification("explanation_only", "explanation", "fast_path", "UNKNOWN", "false", "low", ("explanation_only",), ()).to_dict()

    return LexicalClassification("unknown", "unknown", "unknown", "UNKNOWN", "unknown", "low", ("needs_review",), ()).to_dict()


def build_candidate_answer(*, input_text: object, case_id: str = "case-not-recorded", run_id: str = "run-not-recorded") -> dict[str, object]:
    """Build a contract-valid Adviser candidate answer for offline use.

    The returned mapping is advisory evidence only. It contains no action fields
    and cannot authorize routing, freezing, prompt loading, or writes.
    """

    text = str(input_text or "")
    if len(text) > MAX_INPUT_TEXT_CHARS:
        raise ValueError(f"input_text exceeds {MAX_INPUT_TEXT_CHARS} characters")

    classification = classify_input(text)
    domain = str(classification["governance_domain"])
    flags = _governance_flags(domain, classification)
    required_groups = _PROMPT_GROUPS.get(domain, [])
    required_prompts = _SPECIALIST_PROMPTS.get(domain, [])

    answer: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "case_id": str(case_id),
        "candidate_id": CANDIDATE_ID,
        "candidate_version": CANDIDATE_VERSION,
        "run_id": str(run_id),
        "input_hash": _hash_text(input_text),
        "governance_domain": domain,
        "path_recommendation": str(classification["path_recommendation"]),
        "required_prompt_groups": list(required_groups),
        "required_specialist_prompts": list(required_prompts),
        "recommended_prompt_groups": [],
        "recommended_specialist_prompts": [],
        "context_requirements": {
            "required": list(required_groups),
            "recommended": list(required_prompts),
            "optional": [],
            "missing_required": [],
            "missing_recommended": [],
        },
        "risk_assessment": {
            "severity": str(classification["severity"]),
            "flags": list(classification["flags"]),
            "critical_risks": _critical_risks(classification),
        },
        "governance_flags": flags,
        "advisory_proceed_recommendation": str(classification["advisory_proceed_recommendation"]),
        "requires_human_confirmation": str(classification["requires_human_confirmation"]),
        "authority_statement": AUTHORITY_STATEMENT,
        "rationale": {
            "short": _rationale_short(classification),
            "evidence": [
                "offline lexical baseline",
                "no runtime authority",
                "candidate output is advisory evidence only",
            ],
        },
    }

    if answer["advisory_proceed_recommendation"] in _UNSAFE_PROCEED_VALUES:
        raise ValueError("unsafe proceed value is forbidden in Adviser Candidate v0")

    return answer


def _normalize(text: object) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def _hash_text(text: object) -> str:
    normalized = _normalize(text)
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _matched_patterns(text: str, patterns: tuple[str, ...]) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE)]


def _critical_risks(classification: Mapping[str, Any]) -> list[str]:
    family = str(classification.get("family", ""))
    if family in {"authority_promotion", "prompt_auto_loading", "freeze_bypass", "startup_bypass", "prompt_library_bypass", "box_invasion"}:
        return [family]
    return []


def _governance_flags(domain: str, classification: Mapping[str, Any]) -> dict[str, list[str]]:
    flags = {"freeze": [], "box": [], "startup": [], "prompt_library": [], "patch_delivery": [], "authority": [], "adversarial": []}
    family = str(classification.get("family", "unknown"))
    if domain == "freeze":
        flags["freeze"].append(family)
    elif domain == "box":
        flags["box"].append(family)
    elif domain == "startup":
        flags["startup"].append(family)
    elif domain == "prompt_library":
        flags["prompt_library"].append(family)
    elif domain == "patch":
        flags["patch_delivery"].append(family)
    elif domain == "coding":
        flags["patch_delivery"].append(family)

    if family in {"authority_promotion", "prompt_auto_loading"}:
        flags["authority"].append(family)
        flags["adversarial"].append(family)
    if family in {"freeze_bypass", "startup_bypass", "prompt_library_bypass", "box_invasion"}:
        flags["adversarial"].append(family)
    return flags


def _rationale_short(classification: Mapping[str, Any]) -> str:
    family = str(classification.get("family", "unknown"))
    domain = str(classification.get("governance_domain", "unknown"))
    path = str(classification.get("path_recommendation", "unknown"))
    proceed = str(classification.get("advisory_proceed_recommendation", "UNKNOWN"))
    return f"Lexical baseline matched {family}; domain={domain}; path={path}; advisory_proceed={proceed}; evidence only."
