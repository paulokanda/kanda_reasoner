"""Detailed external AI handoff prompt for complete candidate-family review."""
from __future__ import annotations

from typing import Iterable

from .external_ai_candidate_exchange_contract import CandidateSetIdentity, ExchangeIdentity

__all__ = ["build_external_ai_candidate_review_task"]


def build_external_ai_candidate_review_task(
    *,
    candidate_identity: CandidateSetIdentity,
    exchange_identity: ExchangeIdentity,
    candidate_files: Iterable[str],
) -> str:
    """Build the complete governed task bundled inside every outbound exchange ZIP."""
    paths = tuple(sorted(str(item) for item in candidate_files))
    candidate_lines = "\n".join("- " + item for item in paths)
    text_entries = ",\n".join(
        "    {\"relative_path\": " + repr(path).replace("'", '"') + ", \"content_utf8\": \"<FULL UTF-8 FILE CONTENT>\"}"
        for path in paths
    )
    return "\n".join(
        [
            "# KANDA External AI Candidate Review Task",
            "",
            "Analyze, correct, and improve the complete candidate family in this ZIP.",
            "Review every candidate file, not only the main/facade file.",
            "Preserve behavior, public contracts, lineage, and package ownership boundaries.",
            "Use bounded context files as evidence only; generated evidence is not canonical source.",
            "",
            "## Required review method",
            "",
            "1. Reconstruct the candidate family in an isolated sandbox.",
            "2. Audit all candidate files together for behavior, API, imports, topology, typing, size, and formatting.",
            "3. Apply the smallest cumulative correction needed; preserve unchanged candidate-family files too.",
            "4. Validate the corrected family before packaging. Do not claim validation that was not run.",
            "5. Never directly write canonical Project source from this exchange.",
            "",
            "## Default and preferred return: governed KANDA patch ZIP",
            "",
            "Return one complete cumulative governed KANDA patch ZIP, not loose code fragments.",
            "The patch ZIP must preserve the complete candidate family, including unchanged files, and route files to the correct Project-owned destinations only when the human later runs INSTALL.ps1.",
            "Use the existing KANDA lifecycle: ZIP -> INSTALL -> VALIDATE -> Error Memory intake -> FREEZE evidence preparation -> Preview Freeze Entry -> human Confirm and Write.",
            "The patch must contain install, validate, and freeze-preparation scripts, a manifest with exact hashes, current feature identity metadata, and validation markers.",
            "Validation must check the candidate family, public API contract, imports/dependency topology, size policy, syntax/importability, and the exact defect being corrected.",
            "When an actual reusable failure lesson is found, include an active-ready Error Memory lesson and stage it only to pending AI-assisted Error Memory intake; do not write directly to canonical Lessons.",
            "Freeze preparation may merge validated evidence into the current hint intake, but it must not bypass Preview Freeze Entry or human Confirm and Write.",
            "Include beginner-safe install and validate commands in the response accompanying the ZIP.",
            "",
            "## Optional alternative return: structured text for Import AI Answer",
            "",
            "Only when useful, also provide one marker-wrapped JSON object that the human can paste into the Import AI Answer text window.",
            "This optional text route creates an append-only Project Support candidate generation only. It does not replace Preview, mutate canonical source, prepare a transaction, acknowledge warnings, or confirm human review.",
            "Return exactly this structure with full file contents and no extra or missing candidate paths:",
            "",
            "KANDA_AI_CANDIDATE_RETURN_BEGIN",
            "{",
            '  "schema_version": "1.0",',
            '  "return_kind": "candidate_generation_text",',
            '  "source_lineage": {',
            '    "exchange_id": "' + exchange_identity.exchange_id + '",',
            '    "project_card_identity": "' + exchange_identity.project_card_identity + '",',
            '    "target_relative_path": "' + exchange_identity.target_relative_path + '",',
            '    "source_preview_hash": "' + exchange_identity.source_preview_hash + '",',
            '    "source_candidate_set_hash": "' + exchange_identity.source_candidate_set_hash + '",',
            '    "source_exchange_identity_hash": "' + exchange_identity.identity_hash + '"',
            "  },",
            '  "candidate_family": [',
            text_entries,
            "  ]",
            "}",
            "KANDA_AI_CANDIDATE_RETURN_END",
            "",
            "The content_utf8 value for each candidate must contain the full exact corrected UTF-8 file content. Do not use patches, ellipses, placeholders, markdown fences, base64, or omitted unchanged files.",
            "",
            "## Source lineage",
            "",
            "exchange_id: " + exchange_identity.exchange_id,
            "project_card_identity: " + exchange_identity.project_card_identity,
            "target_relative_path: " + exchange_identity.target_relative_path,
            "source_preview_hash: " + exchange_identity.source_preview_hash,
            "source_candidate_set_hash: " + exchange_identity.source_candidate_set_hash,
            "candidate_identity_hash: " + candidate_identity.identity_hash,
            "exchange_identity_hash: " + exchange_identity.identity_hash,
            "",
            "## Required candidate paths",
            "",
            candidate_lines,
            "",
            "The default return route remains the governed patch ZIP. The structured text route is optional and uses the same lineage and candidate-family validation authority through transient Daily Work staging.",
            "",
        ]
    )
