# project-path: kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/manual_code_hint_contract.py
"""Manual prompt code hint contract.

Manual hints help classification. They are not route authority, not router
overrides, and not prompt execution commands.
"""

from __future__ import annotations


__all__ = [
    'add_manual_hint',
    'clear_manual_hint',
    'ManualClassificationHint',
    'ManualHintScope',
    'ManualHintSource',
    'ManualHintStatus',
    'remove_manual_hint',
    'replace_manual_hint',
]
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .prompt_code_contract import PromptCode


class ManualHintSource(str, Enum):
    """Source for a manual classification hint."""

    USER_DISAMBIGUATION = "user_disambiguation"
    USER_CORRECTION = "user_correction"
    REVIEWER_SELECTION = "reviewer_selection"


class ManualHintScope(str, Enum):
    """Scope for a manual classification hint."""

    CURRENT_REQUEST = "current_request"
    CURRENT_THREAD = "current_thread"
    CURRENT_PROJECT = "current_project"


class ManualHintStatus(str, Enum):
    """Status for a manual classification hint."""

    ACTIVE = "active"
    REMOVED = "removed"
    CLEARED = "cleared"
    REPLACED = "replaced"
    REJECTED = "rejected"


@dataclass(frozen=True)
class ManualClassificationHint:
    """Removable namespaced prompt-code classification hint."""

    code: PromptCode
    source: ManualHintSource
    scope: ManualHintScope
    status: ManualHintStatus
    removable: bool = True
    superseded_by: Optional[PromptCode] = None

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        if not isinstance(self.code, PromptCode):
            raise TypeError("code must be PromptCode")
        if not isinstance(self.source, ManualHintSource):
            raise TypeError("source must be ManualHintSource")
        if not isinstance(self.scope, ManualHintScope):
            raise TypeError("scope must be ManualHintScope")
        if not isinstance(self.status, ManualHintStatus):
            raise TypeError("status must be ManualHintStatus")
        if not isinstance(self.removable, bool):
            raise TypeError("removable must be bool")
        if self.superseded_by is not None and not isinstance(self.superseded_by, PromptCode):
            raise TypeError("superseded_by must be PromptCode or None")

    def is_classification_hint_only(self) -> bool:
        """Return the permanent safety invariant for hints."""

        return True


def add_manual_hint(
    code: str,
    *,
    source: ManualHintSource = ManualHintSource.USER_DISAMBIGUATION,
    scope: ManualHintScope = ManualHintScope.CURRENT_REQUEST,
) -> ManualClassificationHint:
    """Create an active manual classification hint."""

    return ManualClassificationHint(
        code=PromptCode(code.strip().upper()),
        source=source,
        scope=scope,
        status=ManualHintStatus.ACTIVE,
        removable=True,
    )


def remove_manual_hint(hint: ManualClassificationHint) -> ManualClassificationHint:
    """Return a removed copy of an existing hint."""

    if not hint.removable:
        raise ValueError("Manual hint is not removable")
    return ManualClassificationHint(
        code=hint.code,
        source=hint.source,
        scope=hint.scope,
        status=ManualHintStatus.REMOVED,
        removable=hint.removable,
        superseded_by=hint.superseded_by,
    )


def clear_manual_hint(hint: ManualClassificationHint) -> ManualClassificationHint:
    """Return a cleared copy of an existing hint."""

    if not hint.removable:
        raise ValueError("Manual hint is not removable")
    return ManualClassificationHint(
        code=hint.code,
        source=hint.source,
        scope=hint.scope,
        status=ManualHintStatus.CLEARED,
        removable=hint.removable,
        superseded_by=hint.superseded_by,
    )


def replace_manual_hint(hint: ManualClassificationHint, new_code: str) -> ManualClassificationHint:
    """Return a replaced copy that points to a new code."""

    if not hint.removable:
        raise ValueError("Manual hint is not removable")
    return ManualClassificationHint(
        code=hint.code,
        source=hint.source,
        scope=hint.scope,
        status=ManualHintStatus.REPLACED,
        removable=hint.removable,
        superseded_by=PromptCode(new_code.strip().upper()),
    )
