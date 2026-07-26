# LAB-6 Deterministic Runner Skeleton

Feature ID: `routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1`

This milestone creates the first non-runtime deterministic runner skeleton for the KANDA ML LAB.

LAB-6 is governed LAB infrastructure only.

LAB-6 does not create actual fixtures, hash manifest data files, corpus cases, candidate evaluation, scoring execution, metrics execution, provider calls, embeddings, prompt loading, route authority, persistence of ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

## Purpose

The LAB needs a future runner, but the runner must be introduced before candidate evaluation in the safest possible way.

LAB-6 therefore creates a skeleton that can only describe the runner contract and produce non-authoritative `NOT_EVALUATED` run-plan records from caller-supplied in-memory metadata.

The skeleton gives later milestones a stable shape without allowing any live routing authority or live project-state coupling.

## Allowed skeleton behavior

The LAB-6 skeleton may:

```text
declare immutable runner contract metadata
declare allowed input kinds
declare forbidden operation codes
declare hard stop conditions
compute SHA-256 for caller-supplied text
canonicalize caller-supplied JSON-like metadata deterministically
build an in-memory NOT_EVALUATED run plan
return frozen dataclass records
return read-only mapping views
```

The LAB-6 skeleton may not:

```text
load prompt files
load freeze memory
load router canon
load prompt library files
load runtime router modules
load fixtures from disk
discover fixture files
create fixture files
create hash manifest data files
create corpus files
execute candidate evaluation
score candidate outputs
compare routes
select routes
execute routes
approve readiness
record human approval
write reports
write freeze memory
write gold registry
write prompt library
write router canon
write persistent ML decisions
call providers
call embedding models
use network calls
use subprocesses
start async execution
start batch mode
activate Pilot
activate Copilot
enable field testing
```

## Public skeleton surface

The only LAB-6 source file is:

```text
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
```

The public surface is intentionally small:

```text
get_lab6_deterministic_runner_skeleton_record()
canonicalize_json_like_metadata(metadata)
compute_sha256_for_text(text)
build_not_evaluated_run_plan(...)
```

These functions are pure, deterministic, and in-memory.

They do not read from disk, write to disk, call network, call providers, call embeddings, import runtime router modules, or import prompt loader modules.

## Non-authoritative run-plan doctrine

A LAB-6 run plan is not a candidate evaluation result.

A LAB-6 run plan has outcome:

```text
NOT_EVALUATED
```

A LAB-6 run plan must not contain:

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

The run plan may only document that later LAB milestones are still required before candidate evaluation.


## Non-claims

LAB-6 does not create actual fixtures.

LAB-6 does not create hash manifest data files.

LAB-6 does not create a corpus.

LAB-6 does not execute candidate evaluation.

LAB-6 does not score candidates.

LAB-6 does not compare routes.

LAB-6 does not prove LAB self-validation.

LAB-6 does not prove ML router prompt logic reliability.

LAB-6 does not authorize continuing ML implementation.

## Relationship to LAB-5

LAB-5 defined future copied fixture and hash manifest doctrine.

LAB-6 does not create fixture files and does not read fixture files.

LAB-6 only accepts caller-supplied metadata such as fixture-set version and manifest hash as inert strings for a non-authoritative run plan.

Any future real fixture validation belongs to a later governed milestone.

## Relationship to LAB-7

LAB-7 is the next safe milestone after LAB-6 freeze.

LAB-7 must validate the LAB itself before candidate evaluation.

LAB-6 does not prove self-validation and does not evaluate candidates.

## Determinism doctrine

The skeleton must be deterministic:

```text
same caller-supplied metadata
same canonicalization rules
same run-plan output
same SHA-256 text hash output
```

No timestamp generation, random IDs, environment inspection, file-system discovery, provider calls, network calls, or runtime router state may affect the skeleton output.

## Boundary protection

The skeleton must remain inside the LAB box and must not be imported by production/runtime routing code.

The skeleton must not import runtime router modules, prompt loader modules, freeze writer modules, provider modules, embedding/vector modules, PySide/UI modules, activation modules, field-test modules, or Copilot modules.

## Roadmap lock

```text
LAB-5 frozen
→ LAB-6 Deterministic Runner Skeleton
→ LAB-6 freeze with FREEZE_MEMORY_STATUS OK
→ LAB-7 Lab Self-Validation Gate
→ candidate evaluation only after LAB self-validation gates pass
→ ML router prompt logic reliability only after LAB/test mission is fulfilled
→ ML implementation continuation only after reliability is validated
```

No generic `next`, `continue`, or `go` request may skip LAB self-validation, fixture integrity, human review, zero critical boundary doctrine, or freeze memory requirements.
