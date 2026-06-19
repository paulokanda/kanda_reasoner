# Tab 1 and Tab 2 Audit Taxonomy

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.0.0
Status: Planning and detector-roadmap prompt
Prompt ID: kanda_tab1_tab2_audit_taxonomy
Prompt type: architecture/workflow detector roadmap
Scope: Improve "First step: check/correct architecture" and "Second step: check/correct workflow".

## Purpose

Guide the implementation of additive detector gates for Tab 1 architecture checks
and Tab 2 workflow checks. This prompt is not an implementation itself. It turns
the canon taxonomy into one narrow detector gate at a time.

## Frozen context rule

Do not reopen the complete JSON / split JSON web-AI readiness phase unless a new
validation failure proves a bug.

## Tab 1 architecture errors to expose

1. Duplicate public symbols.
2. Symbol shadowing.
3. Cross-box public symbol collisions.
4. Wrong owner box.
5. Cross-box boundary violations.
6. Circular imports.
7. Side effects on import.
8. Mixed responsibility files.
9. Stale or deprecated variants.
10. Misplaced tests.
11. Missing tests for critical owners.
12. Tests asserting implementation internals instead of public contracts.
13. Unsafe path and platform assumptions.
14. Canonical vs working-copy boundary errors.
15. Generated artifact contract errors.
16. Public API instability.
17. Missing `__all__` or uncontrolled public surface in public-facing modules.
18. Dead code and unreachable files.
19. Inconsistent source of truth.
20. Error-handling architecture problems.
21. Inconsistent error contracts across box boundaries.
22. Implicit coupling through shared mutable globals or module-level state.
23. Import heaviness and slow startup risks.
24. Bundle safety issues.
25. Project-wide AI confusion risks.

## Tab 2 workflow errors to expose

1. Workflow step points to a missing file.
2. Workflow step points to a deprecated file.
3. Button-to-action mismatch.
4. Wrong step order.
5. Input/output contract mismatch.
6. Output folder naming mismatch.
7. Stale generated artifacts.
8. Missing validation step in workflow.
9. Placeholder command misuse.
10. GUI state label mismatch.
11. Dual JSON track workflow mistakes.
12. Route manifest ignored by upload workflow.
13. `web_ai_readme` ignored by workflow.
14. Missing deterministic route for AI question types.
15. Broken local-AI Ask flow.
16. Workflow step does not expose enough logs.
17. Workflow step cannot be rerun idempotently.
18. Workflow references old validation logic.
19. Missing rollback or fail-safe workflow.
20. Workflow documentation drift.
21. Missing cross-project generalization.
22. Silent empty output despite apparent success.
23. Path-root drift between selected project, evidence output, and GUI labels.
24. Encoding or line-ending drift when files are generated or patched.
25. Dependency/version skew between documented command and real environment.

## Priority detector gates

Start with report-only gates.

### Tab 1 priority

1. duplicate_public_symbol_detector_gate.
2. cross_box_public_symbol_collision_gate.
3. shadowed_symbol_detector_gate.
4. box_owner_boundary_detector_gate.
5. deprecated_variant_source_of_truth_gate.
6. missing_public_surface_control_gate.
7. test_protection_gap_detector_gate.

### Tab 2 priority

1. workflow_silent_empty_output_detector_gate.
2. workflow_file_path_existence_gate.
3. workflow_step_io_contract_gate.
4. workflow_generated_artifact_freshness_gate.
5. workflow_dual_json_track_gate.
6. workflow_split_route_manifest_gate.
7. path_root_drift_detector_gate.

## Implementation rule

One detector gate per pass. Each pass must follow:

```text
Task 0 audit -> Task 1 roadmap -> Task 2 implementation -> dry run -> apply -> rollback on failure -> Tab 1 validation -> Tab 2 validation -> freeze only if clean
```

## Good detector report

A detector should report:

```text
finding code
severity
owner box
file/path
why it matters
human-readable explanation
machine-readable evidence
recommended repair gate
whether it is hard failure, transitional debt, or warning
```

## Do not do

- Do not patch all detector categories at once.
- Do not auto-correct in the first pass.
- Do not treat generated JSON as source truth for implementation.
- Do not weaken existing Tab 1 or Tab 2 validation gates.
