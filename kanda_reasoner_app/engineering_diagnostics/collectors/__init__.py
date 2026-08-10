# project-path: kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py
"""Public collector contracts for Engineering Diagnostics."""

from .architecture_collector import (
    ARCHITECTURE_COLLECTOR_CONTRACT_VERSION,
    ARCHITECTURE_PRODUCER_ID,
    ArchitectureCollectionCancelled,
    ArchitectureCollectionError,
    ArchitectureCollectionResult,
    ArchitectureIssueEvidence,
    collect_architecture_findings,
)
from .architecture_normalizer import build_architecture_diagnostic_run
from .ruff_collector import (
    RUFF_COLLECTOR_CONTRACT_VERSION,
    RUFF_PRODUCER_ID,
    RuffCollectionCancelled,
    RuffCollectionError,
    RuffCollectionResult,
    collect_ruff_json,
)
from .ruff_normalizer import build_ruff_diagnostic_run
from .shadow_collector import (
    SHADOW_COLLECTOR_CONTRACT_VERSION,
    SHADOW_PRODUCER_ID,
    ShadowCollectionCancelled,
    ShadowCollectionError,
    ShadowCollectionResult,
    ShadowIssueEvidence,
    collect_shadow_findings,
)
from .shadow_normalizer import build_shadow_diagnostic_run

__all__ = [
    "ARCHITECTURE_COLLECTOR_CONTRACT_VERSION",
    "ARCHITECTURE_PRODUCER_ID",
    "ArchitectureCollectionCancelled",
    "ArchitectureCollectionError",
    "ArchitectureCollectionResult",
    "ArchitectureIssueEvidence",
    "RUFF_COLLECTOR_CONTRACT_VERSION",
    "RUFF_PRODUCER_ID",
    "RuffCollectionCancelled",
    "RuffCollectionError",
    "RuffCollectionResult",
    "SHADOW_COLLECTOR_CONTRACT_VERSION",
    "SHADOW_PRODUCER_ID",
    "ShadowCollectionCancelled",
    "ShadowCollectionError",
    "ShadowCollectionResult",
    "ShadowIssueEvidence",
    "build_shadow_diagnostic_run",
    "collect_shadow_findings",
    "build_architecture_diagnostic_run",
    "build_ruff_diagnostic_run",
    "collect_architecture_findings",
    "collect_ruff_json",
]
