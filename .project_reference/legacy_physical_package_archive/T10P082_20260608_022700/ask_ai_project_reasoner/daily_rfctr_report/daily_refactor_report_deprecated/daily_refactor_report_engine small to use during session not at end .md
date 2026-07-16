{
  "state_vector_version": "2.0",
  "timestamp": "<ISO 8601 timestamp, e.g., 2025-01-01T00:00:00>",
  "incremental": true,
  "structural_change": {
    "magnitude": <number, e.g., 0-100>
  },
  "complexity_state": {
    // Add complexity metrics as needed; can be empty object {}
  },
  "governance_state": {
    "score": <number 0-100>,
    "rules": {
      "cortex_creator_boundary_contract": {
        "version": "1.0",
        "status": "canonical_constraint",
        "purpose": "Preserve architectural separation between Cortex advisory layer and Creator execution layer.",
        "boundary_rule": {
          "description": "Cortex must never directly mutate canonical project artifacts.",
          "enforced_flow": {
            "cortex_output": "DecisionPacket",
            "executor_layer": "Controlled execution component",
            "artifact_writer": "memory_builder via Creator runtime"
          },
          "forbidden_flow": [
            "Cortex calling memory_builder directly",
            "Cortex writing canonical artifacts",
            "Cortex bypassing execution layer"
          ],
          "principle": "Cortex can propose. Executor applies."
        }
      },
      "mandatory_future_implementation": {
        "explicit_degraded_confidence_classification": {
          "status": "not_yet_implemented",
          "priority": "high",
          "requirement": "Cortex must explicitly downgrade confidence when visibility is reduced.",
          "confidence_levels": [
            "high",
            "medium",
            "low",
            "degraded"
          ],
          "degradation_triggers": [
            "Governance unavailable",
            "Codex unavailable",
            "Semantic exports partially missing",
            "Symbol index missing",
            "Embedding layer unavailable",
            "Provider unavailable"
          ],
          "warning": "This must be implemented before full Cortex integration."
        }
      },
      "structural_change_triggers": {
        "status": "active_guard",
        "requires_architectural_review_if": [
          "A second path resolver appears",
          "A plugin writes directly to project bucket",
          "Awareness layer mutates structural artifacts",
          "Multiple public entrypoints are introduced",
          "Live runtime objects are treated as canonical truth instead of exported artifacts"
        ],
        "current_state": "none_detected",
        "layer_scope_note": "These constraints belong to Cortex governance layer and must not be enforced by Tab3 runtime directly."
      },
      "layer_responsibility_separation": {
        "creator_runtime": [
          "Build structural graph",
          "Export semantic layer",
          "Export symbol index",
          "Export embeddings",
          "Persist artifacts via JSONStore"
        ],
        "cortex_layer": [
          "Analyze exported artifacts",
          "Produce DecisionPacket",
          "Assess canonical pressure",
          "Classify confidence",
          "Advise but never mutate"
        ],
        "strict_separation": true
      }
    }
  },
  "refactor_pressure": {
    "debt_index": <number, e.g., 0-100>
  },
  "pattern_dynamics": {},
  "forward_projection": {},
  "architectural_snapshot": {}
}