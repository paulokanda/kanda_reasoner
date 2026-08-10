# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_models.py
"""Own workflow validation result data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "CheckResult",
]

@dataclass(slots=True)
class CheckResult:
    """Represent check result."""
    
    category: str
    name: str
    status: str
    message: str
    duration_seconds: float = 0.0
    command: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Support as dict behavior.
        
        Returns
        -------
        dict[str, Any]
            The mapped values.
        """
        
        return {
            "category": self.category,
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "duration_seconds": self.duration_seconds,
            "command": self.command,
            "details": self.details,
        }
