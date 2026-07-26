# project-path: kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_router_mode_state.py
"""Router mode state for Prompt Router Reasoner.

This module is intentionally backend-only. It persists the global Prompt
Router Reasoner mode while preserving a readiness gate before ML can become
the effective mode. ML pilot mode is automatically allowed only when the
project-local review statistics satisfy the conservative pilot policy.
"""

from __future__ import annotations


__all__ = ['PromptRouterReasonerRouterModeState', 'RouterModeTransitionResult']
from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    REVIEW_FOLDER_NAME,
    ROUTER_WITH_HEURISTICS,
    ROUTER_WITH_HELP_OF_ML,
    ROUTER_WITH_ML,
    VALID_ROUTER_MODES,
    PromptRouterReasonerStoreError,
    normalize_router_mode,
    utc_now_iso,
)

ROUTER_MODE_STATE_SCHEMA_VERSION = "1.0"
ROUTER_MODE_STATE_FILENAME = "prompt_router_reasoner_router_mode_state.json"
ROUTER_MODE_STATE_KIND = "prompt_router_reasoner_router_mode_state"

MODE_CHANGE_STATUS_APPLIED = "applied"
MODE_CHANGE_STATUS_BLOCKED = "blocked"
MODE_CHANGE_STATUS_UNCHANGED = "unchanged"

BLOCK_REASON_ML_PILOT_LOCKED = "ml_pilot_activation_requires_validated_readiness"
BLOCK_REASON_ML_PILOT_NOT_READY = "ml_pilot_readiness_gate_not_met"
BLOCK_REASON_ML_PILOT_HAS_BLOCKERS = "ml_pilot_readiness_has_blocking_reasons"
BLOCK_REASON_UNSAFE_STORE_PATH = "router_mode_state_path_must_not_use_freeze_memory"

FORBIDDEN_ROUTER_MODE_STATE_PATH_FRAGMENTS = (
    "project_freeze_after_update",
    "project_freeze_ledger",
    "frozen_features_memory",
    "freeze_hint_intake",
)


@dataclass(frozen=True)
class RouterModeTransitionResult:
    """Result of attempting to change Prompt Router Reasoner router mode."""

    schema_version: str
    status: str
    requested_mode: str
    effective_mode: str
    previous_mode: str
    ml_pilot_locked: bool
    blocking_reasons: tuple[str, ...]
    state_path: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable transition result."""
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "requested_mode": self.requested_mode,
            "effective_mode": self.effective_mode,
            "previous_mode": self.previous_mode,
            "ml_pilot_locked": self.ml_pilot_locked,
            "blocking_reasons": list(self.blocking_reasons),
            "state_path": self.state_path,
        }


class PromptRouterReasonerRouterModeState:
    """Persist and guard the global Prompt Router Reasoner mode.

    The stored mode is for the Prompt Router Reasoner GUI workflow. In v1,
    router_with_heuristics and router_with_help_of_ml are allowed. The
    router_with_ml is present but blocked until project-local readiness stats
    satisfy the conservative pilot policy. Once the stats pass, this state
    class may make router_with_ml the effective mode without a separate manual
    unlock flag.
    """

    def __init__(self, project_root: str | Path) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        project_root : str | Path
            The project root path.
        """
        
        self.project_root = Path(project_root).expanduser().resolve()
        self.review_dir = self.project_root / REVIEW_FOLDER_NAME
        self.state_file = self.review_dir / ROUTER_MODE_STATE_FILENAME
        self._validate_state_path()
        self.review_dir.mkdir(parents=True, exist_ok=True)
        if not self.state_file.exists():
            self._write_state(self._default_state())

    def load_state(self) -> dict[str, Any]:
        """Load router mode state, repairing missing optional fields safely."""
        try:
            loaded = json.loads(self.state_file.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            raise PromptRouterReasonerStoreError("Invalid router mode state JSON") from exc
        if not isinstance(loaded, dict):
            raise PromptRouterReasonerStoreError("Router mode state must be a JSON object")
        return self._normalize_state(loaded)

    def get_effective_mode(self) -> str:
        """Return the current effective mode for the GUI workflow."""
        return str(self.load_state()["effective_mode"])

    def is_ml_pilot_locked(self) -> bool:
        """Return True while router_with_ml is unavailable for activation."""
        return bool(self.load_state()["ml_pilot_locked"])

    def activate_ml_pilot_if_ready(
        self,
        readiness_stats: Mapping[str, Any] | None,
    ) -> RouterModeTransitionResult:
        """Set router_with_ml automatically when readiness stats pass."""
        return self.set_mode(ROUTER_WITH_ML, readiness_stats=readiness_stats)

    def set_mode(
        self,
        requested_mode: str,
        *,
        readiness_stats: Mapping[str, Any] | None = None,
        governed_pilot_unlock: bool = False,
    ) -> RouterModeTransitionResult:
        """Attempt to set the Prompt Router Reasoner mode.

        router_with_ml is allowed only when the supplied readiness snapshot has
        pilot_threshold_met true and no blocking reasons. The legacy
        governed_pilot_unlock argument is accepted for compatibility but no
        longer required by this auto-activation policy.
        """
        normalized_requested = normalize_router_mode(requested_mode)
        state = self.load_state()
        previous_mode = str(state["effective_mode"])

        if normalized_requested == ROUTER_WITH_ML:
            blocking_reasons = self._ml_mode_blocking_reasons(
                readiness_stats=readiness_stats,
                governed_pilot_unlock=governed_pilot_unlock,
            )
            if blocking_reasons:
                state.update(
                    {
                        "requested_mode": normalized_requested,
                        "effective_mode": previous_mode,
                        "ml_pilot_locked": True,
                        "last_blocking_reasons": list(blocking_reasons),
                        "updated_at": utc_now_iso(),
                    }
                )
                self._write_state(state)
                return RouterModeTransitionResult(
                    schema_version=ROUTER_MODE_STATE_SCHEMA_VERSION,
                    status=MODE_CHANGE_STATUS_BLOCKED,
                    requested_mode=normalized_requested,
                    effective_mode=previous_mode,
                    previous_mode=previous_mode,
                    ml_pilot_locked=True,
                    blocking_reasons=tuple(blocking_reasons),
                    state_path=str(self.state_file),
                )

        effective_mode = normalized_requested
        status = MODE_CHANGE_STATUS_UNCHANGED if effective_mode == previous_mode else MODE_CHANGE_STATUS_APPLIED
        state.update(
            {
                "requested_mode": normalized_requested,
                "effective_mode": effective_mode,
                "ml_pilot_locked": normalized_requested != ROUTER_WITH_ML,
                "last_blocking_reasons": [],
                "updated_at": utc_now_iso(),
            }
        )
        self._write_state(state)
        return RouterModeTransitionResult(
            schema_version=ROUTER_MODE_STATE_SCHEMA_VERSION,
            status=status,
            requested_mode=normalized_requested,
            effective_mode=effective_mode,
            previous_mode=previous_mode,
            ml_pilot_locked=bool(state["ml_pilot_locked"]),
            blocking_reasons=(),
            state_path=str(self.state_file),
        )

    def reset_to_heuristics(self) -> RouterModeTransitionResult:
        """Reset mode to the safe default."""
        return self.set_mode(ROUTER_WITH_HEURISTICS)

    def _ml_mode_blocking_reasons(
        self,
        *,
        readiness_stats: Mapping[str, Any] | None,
        governed_pilot_unlock: bool,
    ) -> list[str]:
        """Support ml mode blocking reasons behavior.
        
        Parameters
        ----------
        readiness_stats : Mapping[str, Any] | None
            The readiness stats value.
        governed_pilot_unlock : bool
            The governed pilot unlock value.
        
        Returns
        -------
        list[str]
            The list of values.
        """
        
        reasons: list[str] = []
        del governed_pilot_unlock
        stats = dict(readiness_stats or {})
        if stats.get("pilot_threshold_met") is not True:
            reasons.append(BLOCK_REASON_ML_PILOT_NOT_READY)
        blockers = stats.get("pilot_blocking_reasons", [])
        if blockers:
            reasons.append(BLOCK_REASON_ML_PILOT_HAS_BLOCKERS)
        return reasons

    def _default_state(self) -> dict[str, Any]:
        """Support default state behavior.
        
        Returns
        -------
        dict[str, Any]
            The mapped values.
        """
        
        now = utc_now_iso()
        return {
            "schema_version": ROUTER_MODE_STATE_SCHEMA_VERSION,
            "kind": ROUTER_MODE_STATE_KIND,
            "created_at": now,
            "updated_at": now,
            "requested_mode": ROUTER_WITH_HEURISTICS,
            "effective_mode": ROUTER_WITH_HEURISTICS,
            "allowed_display_modes": [
                ROUTER_WITH_HEURISTICS,
                ROUTER_WITH_HELP_OF_ML,
                ROUTER_WITH_ML,
            ],
            "backend_allowed_modes": [
                ROUTER_WITH_HEURISTICS,
                ROUTER_WITH_HELP_OF_ML,
            ],
            "ml_pilot_locked": True,
            "ml_pilot_lock_reason": BLOCK_REASON_ML_PILOT_LOCKED,
            "auto_ml_pilot_activation_policy": "conservative_wilson_lcb_auto_ml_pilot_v1",
            "last_blocking_reasons": [],
            "router_authority": "heuristics_authoritative_until_validated_ml_pilot",
            "ml_authority": "validated_pilot_only_after_readiness_gate",
        }

    def _normalize_state(self, state: Mapping[str, Any]) -> dict[str, Any]:
        """Support normalize state behavior.
        
        Parameters
        ----------
        state : Mapping[str, Any]
            The state value.
        
        Returns
        -------
        dict[str, Any]
            The mapped values.
        """
        
        data = self._default_state()
        data.update(dict(state))
        data["schema_version"] = ROUTER_MODE_STATE_SCHEMA_VERSION
        data["kind"] = ROUTER_MODE_STATE_KIND
        data["requested_mode"] = normalize_router_mode(str(data.get("requested_mode", ROUTER_WITH_HEURISTICS)))
        effective_mode = normalize_router_mode(str(data.get("effective_mode", ROUTER_WITH_HEURISTICS)))
        if effective_mode == ROUTER_WITH_ML and data.get("ml_pilot_locked", True):
            effective_mode = ROUTER_WITH_HEURISTICS
        data["effective_mode"] = effective_mode
        data["allowed_display_modes"] = [
            mode for mode in data.get("allowed_display_modes", []) if mode in VALID_ROUTER_MODES
        ] or [ROUTER_WITH_HEURISTICS, ROUTER_WITH_HELP_OF_ML, ROUTER_WITH_ML]
        ml_pilot_locked = bool(data.get("ml_pilot_locked", True))
        backend_modes = [mode for mode in data.get("backend_allowed_modes", []) if mode in VALID_ROUTER_MODES]
        if ml_pilot_locked:
            backend_modes = [mode for mode in backend_modes if mode != ROUTER_WITH_ML]
        elif ROUTER_WITH_ML not in backend_modes:
            backend_modes.append(ROUTER_WITH_ML)
        data["backend_allowed_modes"] = backend_modes or [ROUTER_WITH_HEURISTICS, ROUTER_WITH_HELP_OF_ML]
        data["ml_pilot_locked"] = ml_pilot_locked
        return data

    def _write_state(self, state: Mapping[str, Any]) -> None:
        """Support write state behavior.
        
        Parameters
        ----------
        state : Mapping[str, Any]
            The state value.
        """
        
        normalized = self._normalize_state(state)
        text = json.dumps(normalized, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        temp_path = self.state_file.with_name(self.state_file.name + ".tmp")
        temp_path.write_text(text, encoding="utf-8", newline="\n")
        os.replace(temp_path, self.state_file)

    def _validate_state_path(self) -> None:
        """Support validate state path behavior.
        """
        
        review_dir_text = str(self.review_dir).replace("\\", "/").lower()
        relative_text = str(self.review_dir.relative_to(self.project_root)).replace("\\", "/").lower()
        for fragment in FORBIDDEN_ROUTER_MODE_STATE_PATH_FRAGMENTS:
            lowered = fragment.lower()
            if lowered in relative_text or lowered in review_dir_text.split("/"):
                raise PromptRouterReasonerStoreError(BLOCK_REASON_UNSAFE_STORE_PATH)
