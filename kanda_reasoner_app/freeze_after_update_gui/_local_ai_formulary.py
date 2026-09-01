# project-path: kanda_reasoner_app/freeze_after_update_gui/_local_ai_formulary.py
"""Local-AI formulary helpers for the Freeze Feature After Update tab."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_response_parser import (
    canonical_formulary_payload,
)
from kanda_reasoner_app.reasoner_engine.local_ai_chat_service import (
    chat_with_local_model,
    list_local_ai_models as _shared_list_local_ai_models,
    resolve_local_ai_model,
)

__all__ = [
    "AUTO_LOCAL_AI_MODEL_LABEL",
    "LocalFreezeAIFormularyRunner",
    "list_local_ai_models",
    "local_ai_response_looks_like_prompt_echo",
    "model_name_from_local_ai_combo_text",
    "validate_local_ai_form_against_heuristic",
]

AUTO_LOCAL_AI_MODEL_LABEL = "Auto (global Config Local AI model)"
MODEL_REGISTRY_MODULE = "kanda_reasoner_app.reasoner_engine.v10_model_registry"
MODEL_REGISTRY_CLASS = "LocalModelRegistry"
LOCAL_AI_MODULE = "kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models"
LOCAL_AI_CLASS = "V9QwenAIModels"


def _load_local_ai_class(module_name: str, class_name: str) -> type[Any]:
    """Load local AI helper classes through a late-bound GUI-safe boundary."""
    module = importlib.import_module(module_name)
    loaded = getattr(module, class_name)
    if not isinstance(loaded, type):
        raise TypeError(module_name + "." + class_name + " is not a class")
    return loaded


def list_local_ai_models() -> list[str]:
    """Return models from the globally configured Local AI endpoint."""
    return _shared_list_local_ai_models()


def model_name_from_local_ai_combo_text(text: str) -> str:
    """Normalize the Local Freeze Entry model combo text."""
    selected = str(text or "").strip()
    if not selected or selected == AUTO_LOCAL_AI_MODEL_LABEL:
        return ""
    return selected


def _choose_local_ai_model(requested_model: str = "") -> str:
    """Resolve legacy requests through the global Config Local AI owner."""
    return resolve_local_ai_model(requested_model)


def _build_local_ai_freeze_form_messages(inputs: dict, project_root: Path) -> list[dict[str, str]]:
    """Build a compact local-AI prompt that improves, but never weakens, the freeze form."""
    current_json = json.dumps(
        canonical_formulary_payload(inputs),
        ensure_ascii=False,
        indent=2,
    )
    keys = ", ".join(
        [
            "feature_title",
            "primary_box",
            "box_type",
            "validated_files",
            "generated_files",
            "protected_paths",
            "do_not_regress_rules",
            "validation_evidence_summary",
            "known_warnings",
            "planned_next_step",
            "notes",
        ]
    )
    return [
        {
            "role": "system",
            "content": (
                "You edit one JSON object. Return only valid JSON. Do not repeat the prompt. "
                "Do not explain. Do not use markdown. Never delete existing paths, rules, or validation lines."
            ),
        },
        {
            "role": "user",
            "content": (
                "Instruction: Improve the KANDA freeze form JSON only if needed.\n"
                "Required output: one canonical JSON object only, starting with { and ending with }.\n"
                "NO prose. NO markdown. NO marker block. NO comments.\n"
                "Keep validated_files, generated_files, protected_paths, do_not_regress_rules, "
                "and validation_evidence_summary as JSON arrays of strings.\n"
                f"Allowed keys only: {keys}.\n"
                "Hard rules:\n"
                "- Preserve every existing validation line exactly.\n"
                "- Preserve every existing protected path exactly.\n"
                "- Preserve every existing do-not-regress rule; you may append clearer rules only.\n"
                "- Keep project-specific frozen memory under <project>_show_project_to_AI/"
                "project_freeze_after_update/frozen_features_memory.\n"
                "- Do not store project-specific frozen memory inside project_freeze_ledger.\n"
                "- If unsure, return the input JSON unchanged.\n"
                "- Do not write the words Context:, Task:, Critical rules:, Return format, "
                "or Copy/paste-ready answer shape.\n"
                f"Active project root: {project_root}\n"
                "JSON TO REVIEW:\n"
                f"{current_json}\n"
            ),
        },
    ]


def _nonempty_lines(value: Any) -> list[str]:
    """Return non-empty normalized lines from a freeze-form multiline value."""
    return [line.strip() for line in str(value or "").splitlines() if line.strip()]


def _normalized_line_set(value: Any) -> set[str]:
    """Return case-insensitive normalized lines for quality-gate comparison."""
    return {" ".join(line.lower().split()) for line in _nonempty_lines(value)}


def local_ai_response_looks_like_prompt_echo(response_text: str) -> bool:
    """Detect local model responses that echoed the task prompt instead of returning a form."""
    text = str(response_text or "")
    echo_markers = [
        "You are a specialist in KANDA Reasoner",
        "Context:\nI just implemented",
        "Task:\nReview and correct",
        "Critical rules:",
        "Return format - strict copy/paste contract",
        "Copy/paste-ready answer shape:",
        "Current auto-filled form JSON",
    ]
    return sum((1 for marker in echo_markers if marker in text)) >= 2


def validate_local_ai_form_against_heuristic(candidate: dict, heuristic: dict) -> tuple[bool, list[str]]:
    """Reject local AI output that weakens the deterministic heuristic baseline."""
    reasons: list[str] = []
    required_keys = set(heuristic.keys())
    missing_keys = sorted(
        (key for key in required_keys if key not in candidate or str(candidate.get(key, "")).strip() == "")
    )
    if missing_keys:
        reasons.append("missing required field(s): " + ", ".join(missing_keys))
    combined_candidate_text = "\n".join((str(candidate.get(key, "")) for key in required_keys))
    forbidden_echo_markers = [
        "You are a specialist in KANDA Reasoner",
        "Return format - strict copy/paste contract",
        "Copy/paste-ready answer shape",
        "Current auto-filled form JSON",
    ]
    if any((marker in combined_candidate_text for marker in forbidden_echo_markers)):
        reasons.append("contains copied prompt/instruction text")
    typo_markers = ["freez_context", "freez context", "prqject_freeze", "KAN DA_F RE EZE"]
    if any((marker.lower() in combined_candidate_text.lower() for marker in typo_markers)):
        reasons.append("contains known AI typo/damaged marker text")
    line_preserve_fields = [
        "validated_files",
        "generated_files",
        "protected_paths",
        "do_not_regress_rules",
        "validation_evidence_summary",
    ]
    for field in line_preserve_fields:
        heuristic_lines = _normalized_line_set(heuristic.get(field, ""))
        candidate_lines = _normalized_line_set(candidate.get(field, ""))
        missing_lines = sorted(heuristic_lines - candidate_lines)
        if missing_lines:
            preview = "; ".join(missing_lines[:3])
            if len(missing_lines) > 3:
                preview += "; ..."
            reasons.append(f"{field} lost baseline line(s): {preview}")
    if len(_nonempty_lines(candidate.get("do_not_regress_rules", ""))) < len(
        _nonempty_lines(heuristic.get("do_not_regress_rules", ""))
    ):
        reasons.append("do_not_regress_rules became shorter than heuristic baseline")
    if len(_nonempty_lines(candidate.get("validation_evidence_summary", ""))) < len(
        _nonempty_lines(heuristic.get("validation_evidence_summary", ""))
    ):
        reasons.append("validation_evidence_summary became shorter than heuristic baseline")
    if len(_nonempty_lines(candidate.get("protected_paths", ""))) < len(
        _nonempty_lines(heuristic.get("protected_paths", ""))
    ):
        reasons.append("protected_paths became shorter than heuristic baseline")
    return (not reasons, reasons)


# Backward-compatible private aliases for existing internal consumers.
_list_local_ai_models = list_local_ai_models
_model_name_from_local_ai_combo_text = model_name_from_local_ai_combo_text
_local_ai_response_looks_like_prompt_echo = local_ai_response_looks_like_prompt_echo
_validate_local_ai_form_against_heuristic = validate_local_ai_form_against_heuristic


class LocalFreezeAIFormularyRunner:
    """Pure-Python runner that asks a local Ollama model to fill the freeze form.

    This intentionally avoids QThread/QObject signal wiring. The GUI starts it in a
    daemon Python thread and polls a queue from the Qt main thread, which is safer
    during shutdown and dialog close on Windows/PySide.
    """

    def __init__(self, *, inputs: dict, project_root: Path, model_name: str = "") -> None:
        """Support init behavior.
        
        Parameters
        ----------
        inputs : dict
            The inputs value.
        project_root : Path
            The project root path.
        model_name : str, optional
            The optional model name value.
        """
        
        self._inputs = dict(inputs)
        self._project_root = Path(project_root)
        self._requested_model = str(model_name or "").strip()

    def run(self) -> tuple[bool, str, str]:
        """Run the local AI fill request and return (ok, response_or_error, model)."""
        try:
            model_name = _choose_local_ai_model(self._requested_model)
            if not model_name:
                raise RuntimeError(
                    "No global Local AI model is configured. Open Config AI > Config Local AI."
                )
            response_text, used_model = chat_with_local_model(
                _build_local_ai_freeze_form_messages(self._inputs, self._project_root),
                model_selection=model_name,
                temperature=0.05,
                max_tokens=2600,
            )
            return (True, str(response_text or ""), used_model)
        except Exception as exc:
            return (False, str(exc), "")
