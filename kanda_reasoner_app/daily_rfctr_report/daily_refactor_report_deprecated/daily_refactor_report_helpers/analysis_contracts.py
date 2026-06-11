from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


JsonDict = Dict[str, Any]


@dataclass(frozen=True)
class AnalysisInputs:
    """
    #### - Immutable inputs bundle for all analyzers (read-only) - ####
    snapshot: project snapshot dict (from project_snapshot_extractor)
    symbol_index: symbol index dict (from symbol_index_extractor)
    symbol_churn: churn dict (from symbol_churn_analyzer)
    dependency_graph: optional graph dict (from dependency_graph_extractor)
    governance_rules: optional rules dict (from governance_rules.json)
    """
    snapshot: JsonDict
    symbol_index: JsonDict
    symbol_churn: JsonDict
    dependency_graph: Optional[JsonDict] = None
    governance_rules: Optional[JsonDict] = None


@dataclass(frozen=True)
class AnalyzerResult:
    """
    #### - Standard analyzer return (always JSON-serializable) - ####
    name: analyzer name string
    version: analyzer version string
    result: dict payload
    """
    name: str
    version: str
    result: JsonDict


class AnalyzerProtocol:
    """
    #### - Informal protocol: implement analyze(inputs) -> AnalyzerResult - ####
    """
    def analyze(self, inputs: AnalysisInputs) -> AnalyzerResult:
        raise NotImplementedError