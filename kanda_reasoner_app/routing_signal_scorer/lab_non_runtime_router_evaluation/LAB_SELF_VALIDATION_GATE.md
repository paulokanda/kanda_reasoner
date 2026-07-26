# LAB-7 Lab Self-Validation Gate

Feature ID: `routing_signal_scorer_v3_ml_lab_self_validation_gate_v1`

LAB-7 creates the governed non-runtime self-validation gate for the ML LAB.

LAB-7 validates the LAB itself before any future candidate evaluation is permitted by later milestones.

LAB-7 does not evaluate candidates, compare routes, select routes, score candidates, load prompts, read live prompt library data, read live freeze memory, read live router canon, read fixtures from disk, create actual fixtures, create corpus cases, write reports, persist ML decisions, activate Pilot, field-test anything, or implement Copilot behavior.

## Purpose

The LAB cannot be trusted to evaluate candidate router logic until the LAB proves that its own control checks work.

LAB-7 introduces a deterministic in-memory gate that accepts caller-supplied self-validation control results and returns a non-authoritative self-validation status.

The gate does not discover or run controls by reading files. It only evaluates the facts supplied to it by the caller.

## Required self-validation controls

A future LAB self-validation pass must demonstrate all of the following controls:

```text
gold_vs_gold_control_passed
wrong_route_control_failed_as_expected
missing_prompt_control_failed_as_expected
forbidden_action_control_critical_failed_as_expected
fixture_hash_mismatch_control_lab_invalid_as_expected
skipped_match_before_disagree_control_critical_failed_as_expected
zero_critical_boundary_error_budget_enforced
lab6_runner_outputs_not_evaluated_only
no_live_project_reads_confirmed
no_authority_fields_confirmed
candidate_evaluation_blocked_until_self_validation_passed
```

All controls must be true for the self-validation gate to pass.

Any missing or false required control keeps the LAB in `LAB_INVALID` for candidate evaluation purposes.

## Gate outcomes

LAB-7 defines the following outcome vocabulary for the self-validation gate:

```text
LAB_SELF_VALIDATION_PASS
LAB_INVALID
NOT_EVALUATED
```

A pass means the self-validation gate itself is satisfied for this caller-supplied control set.

A pass does not evaluate a candidate and does not grant runtime authority.

A pass only permits the roadmap to continue to the next governed LAB milestone.

## Non-authority doctrine

A LAB-7 result must not contain or imply:

```text
route_decision
load_prompt
execute_route
approve_readiness
record_human_approval
write_freeze_memory
write_gold_registry
write_prompt_library
write_router_canon
activate_pilot
activate_copilot
enable_field_test
call_provider
call_embedding_model
start_batch_mode
persist_ml_decision
runtime_command
copilot_instruction
```

The gate may say that self-validation controls passed, but it may not approve production readiness, human approval, runtime readiness, candidate reliability, field-test readiness, Pilot activation, or Copilot activation.

## Relationship to LAB-6

LAB-6 created a deterministic runner skeleton that returns `NOT_EVALUATED` run-plan records.

LAB-7 checks that the LAB can prove the runner skeleton remains non-authoritative and that candidate evaluation is still blocked until the LAB is self-validated.

LAB-7 does not turn the LAB-6 skeleton into a candidate evaluator.

## Relationship to LAB-8

After LAB-7 is frozen with `FREEZE_MEMORY_STATUS: OK`, the next safe milestone is:

```text
LAB-8 — Alpha Corpus Seed
```

LAB-8 may introduce a governed static alpha corpus under a separate scope.

LAB-7 does not create corpus cases.

## Boundary protection

The gate must remain inside the LAB box and must not be imported by production/runtime routing code.

The gate must not import runtime router modules, prompt loader modules, freeze writer modules, provider modules, embedding/vector modules, PySide/UI modules, activation modules, field-test modules, or Copilot modules.

## Roadmap lock

```text
LAB-6 frozen
→ LAB-7 Lab Self-Validation Gate
→ LAB-7 freeze with FREEZE_MEMORY_STATUS OK
→ LAB-8 Alpha Corpus Seed
→ candidate evaluation only after later governed corpus, scoring, and harness milestones
→ ML router prompt logic reliability only after LAB/test mission is fulfilled
→ ML implementation continuation only after reliability is validated
```

No generic `next`, `continue`, or `go` request may skip self-validation, corpus governance, fixture integrity, human review, zero critical boundary doctrine, or freeze memory requirements.
