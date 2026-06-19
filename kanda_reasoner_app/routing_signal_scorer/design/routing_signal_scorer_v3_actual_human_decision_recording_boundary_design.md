# Routing Signal Scorer v3 Actual Human Decision Recording Boundary Design v1

Feature ID: `routing_signal_scorer_v3_actual_human_decision_recording_boundary_design_v1`

Status: design only, schema only, review evidence only.

This milestone defines the boundary that a future actual human decision-recording
patch would have to pass before it could even be proposed. It does not record a real human decision and does not authorize a decision write.

## Purpose

The previous milestone defined an actual human decision record schema with the
current value `not_recorded`. This milestone adds a stricter recording boundary
around any future attempt to move from a schema-only record to an actual recorded
human decision.

The boundary exists to prevent a vague phrase such as `approve`, `go`, `continue`,
or `generate` from being interpreted as permission to create semantic artifacts or
to enable runtime semantic scoring.

## Allowed now

- Review the decision-recording boundary schema.
- Review the pre-recording evidence checklist.
- Review the allowed future decision values.
- Review the constraints that any future decision-recording patch must satisfy.

## Not allowed now

- Record a real human decision.
- Write a decision record.
- Store a decision record path.
- Authorize a generator candidate patch.
- Generate, write, read, load, discover, or overwrite semantic artifacts.
- Scan prompt libraries, freeze entries, project sources, or runtime user queries.
- Materialize raw prompt text, user query text, freeze entry text, source text,
  embedding values, vector values, or vector indexes.
- Add embeddings, TF-IDF dependencies, vector stores, providers, network access,
  credential loading, model loading, startup generation, runtime generation,
  background generation, or file-watcher generation.
- Modify deterministic router behavior, required prompt decisions, missing context
  decisions, missing behavior decisions, or May proceed now decisions.

## Required prior frozen milestones

- Routing Signal Scorer v3 Closure Shield v1.
- Routing Signal Scorer v3 Disabled Generation Boundary Design v1.
- Routing Signal Scorer v3 Dry-Run Artifact Generation Plan Design v1.
- Routing Signal Scorer v3 Local Generator Candidate Review Gate Design v1.
- Routing Signal Scorer v3 Human Architectural Review Record Design v1.
- Routing Signal Scorer v3 Human Decision Intake Design v1.
- Routing Signal Scorer v3 Actual Human Decision Record Design v1.
- V2 similarity runtime-lite advisory-only regressions.
- Freeze-hint state-machine regressions.

## Recording effect policy

The current state remains `not_recorded`. It has no effect on generator candidate
authorization, semantic artifact generation, runtime scoring, route selection,
required prompts, missing context, missing behavior, or May proceed now.

Even a future value named `permit_separate_generator_candidate_proposal_review_only`
would not authorize generation. It would only permit a separate governed candidate proposal review patch.

## Public contract boundary

This design module is intentionally not exported from `contract.py` or
`__init__.py`. It is directly testable as a design artifact, not a public runtime
scorer API.
