# Routing Signal Scorer v3 Shadow Mode / Assistant Transition Design v1

M17 starts the post-Adviser phase as a **design-only** milestone. It records the
minimum boundaries for a future shadow-mode / Assistant transition review after
M16 closed the Adviser phase.

This folder does not enable runtime behavior. It contains no shadow-mode runner,
no Assistant routing integration, no candidate promotion, no prompt auto-loading,
no source scanning, no provider calls, no embeddings, no persistence, and no
router authority.

Allowed output is only an in-memory design record that says future work must be
separately governed before any shadow-mode or Assistant behavior exists.


# M18 Shadow Mode Boundary Design v1

M18 adds an immutable design-only boundary for future shadow-mode work. It does
not activate shadow mode, Auxiliar/Assistant behavior, runtime authority, prompt
loading, persistence, report writing, gold or registry mutation, provider calls,
embeddings, or candidate promotion.

The next allowed milestone is M19: Shadow Mode Input Output Contract Design v1.

# M19 Shadow Mode Input Output Contract Design v1

M19 adds a static design-only input/output contract for future non-runtime
shadow observation evidence. It does not implement validation logic, observation
execution, report writing, persistence, runtime integration, prompt loading,
shadow-mode activation, Auxiliar/Assistant behavior, or candidate promotion.

The next allowed milestone is M20: Shadow Mode Contract Validator Design v1.

# M20 Shadow Mode Contract Validator Design v1

M20 adds static design-only rules for a future shadow-mode contract validator.
It does not implement live validation logic, input processing, output
generation, observation execution, report writing, persistence, runtime
integration, prompt loading, shadow-mode activation, Auxiliar/Assistant
behavior, or candidate promotion.

The next allowed milestone is M21: Shadow Mode Observation Skeleton Design v1.

# M21 Shadow Mode Observation Skeleton Design v1

M21 adds static design-only boundaries for a future non-runtime shadow
observation skeleton. It does not implement a callable observation builder,
live validation, input processing, output generation, route comparison, report
writing, persistence, runtime integration, prompt loading, shadow-mode
activation, Auxiliar/Assistant behavior, or candidate promotion.

The next allowed milestone is M22: Shadow Mode Implementation Gate Design v1.

# M22 Shadow Mode Implementation Gate Design v1

M22 adds static design-only boundaries for a future implementation gate. It
does not implement a live gate, read freeze memory, inspect source files,
process inputs, generate outputs, compare routes, build observations, write
reports, persist observations, activate shadow mode, integrate runtime routing,
start Auxiliar/Assistant behavior, or promote a candidate.

The next allowed milestone is M23: Non Runtime Shadow Observation Implementation v1.

# M23 Non Runtime Shadow Observation Implementation v1

M23 adds the first narrow implementation after the M18-M22 design-only chain.
It builds one in-memory non-runtime shadow observation dictionary from
caller-supplied JSON-safe primitive data and fails closed on unknown fields,
forbidden authority fields, missing required fields, and non-primitive values.

M23 does not activate shadow mode, start Auxiliar/Assistant behavior, integrate
with runtime routing, load prompts, read or write files, persist observations,
write reports, mutate gold or registry state, call providers, use embeddings,
promote candidates, or grant router authority.

The next allowed milestone is M24: Shadow Observation Review Evidence Design v1.

## M24 - Shadow Observation Review Evidence Design v1

`shadow_observation_review_evidence_design.py` defines the immutable design-only review-evidence envelope for future human review of M23 non-runtime observations. It has no live review evidence builder, no validation execution, no observation transformation, no persistence, no report writing, no review queue writer, no human decision recording, no route comparison, no runtime integration, no prompt loading, no shadow-mode activation, no Auxiliar/Assistant behavior, and no router authority.

The next allowed milestone after M24 freeze is M25: Shadow Mode Readiness Gate for Assistant Boundary Review v1.


## M25 - Shadow Mode Readiness Gate for Assistant Boundary Review v1

`shadow_mode_assistant_boundary_readiness_gate_design.py` defines immutable design-only prerequisites for a later M26 Auxiliar/Assistant boundary review. It has no live readiness gate, no readiness calculation, no review evidence building, no observation transformation, no file IO, no persistence, no report writing, no review queue writer, no human decision recording, no route comparison, no runtime integration, no prompt loading, no shadow-mode activation, no Auxiliar/Assistant behavior, and no router authority.

The next allowed milestone after M25 freeze is M26: Auxiliar/Assistant Boundary Design v1, only after separate human scope confirmation.

## M26 - Auxiliar/Assistant Boundary Design v1

M26 defines an immutable design-only boundary for a possible later Auxiliar/Assistant phase. It does not start Assistant behavior, activate shadow mode, compare routes, load prompts, write files, persist evidence, record human decisions, promote candidates, or grant runtime authority. Future Assistant roles remain non-authoritative human-review support only and require separate governed milestones.

## M27 - Auxiliar/Assistant Input Output Contract Design v1

M27 defines an immutable design-only input/output contract for a possible later Auxiliar/Assistant human-review support envelope. It does not process inputs, generate outputs, validate live payloads, start Assistant behavior, activate shadow mode, compare or select routes, load prompts, write files, persist evidence, record human decisions, promote candidates, or grant runtime authority. Future fields remain non-authoritative human-review support only.

The next allowed milestone after M27 freeze is M28: Auxiliar/Assistant Contract Validator Design v1.


## M28 - Auxiliar/Assistant Contract Validator Design v1

M28 defines immutable design-only fail-closed validation-rule boundaries for a
possible later Auxiliar/Assistant contract validator over the M27 input/output
contract. It does not implement live contract validation, input processing,
output generation, observation transformation, route comparison, route selection,
prompt loading, file IO, persistence, report writing, review queue writing,
human decision recording, gold or registry mutation, provider/model calls,
embeddings, candidate promotion, shadow-mode activation, or Auxiliar/Assistant
behavior.

The next allowed milestone after M28 freeze is M29: Auxiliar/Assistant Assistance
Skeleton Design v1.
## M29 - Auxiliar/Assistant Assistance Skeleton Design v1

M29 adds an immutable design-only assistance skeleton record for future non-authoritative Auxiliar/Assistant human-review support slots. It does not implement live assistance, a callable assistance builder, live contract validation, input processing, output generation, Assistant activation, shadow-mode activation, route comparison, route selection, prompt loading, runtime integration, persistence, human decision recording, or candidate promotion.

Next allowed milestone after M29 validation and freeze: M30 - Routing Signal Scorer v3 Auxiliar/Assistant Implementation Gate Design v1.

## M30 - Auxiliar/Assistant Implementation Gate Design v1

M30 adds an immutable design-only implementation gate record for a possible later non-runtime Auxiliar/Assistant assistance implementation. It does not implement a live gate, callable gate entrypoint, implementation permission grant, live assistance, live contract validation, input processing, output generation, Assistant activation, shadow-mode activation, route comparison, route selection, prompt loading, runtime integration, persistence, human decision recording, or candidate promotion.

Next allowed milestone after M30 validation and freeze: M31 - Routing Signal Scorer v3 Non Runtime Auxiliar/Assistant Assistance Implementation v1.

## M31 - Non Runtime Auxiliar/Assistant Assistance Implementation v1

M31 adds the first narrow non-runtime Auxiliar/Assistant assistance implementation. It builds one in-memory, non-authoritative human-review support record from caller-supplied JSON-safe primitive data and fails closed on unknown fields, forbidden authority fields, missing required fields, blank required fields, non-string values, and unsupported support labels.

M31 does not activate Assistant behavior, start Auxiliar behavior, activate shadow mode, compare or select routes, select or load prompts, integrate runtime routing, read or write files, persist records, write reports or queues, record human decisions, mutate gold or registry state, call providers, use embeddings, promote candidates, or grant runtime authority.

Next allowed milestone after M31 validation and freeze: M32 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Review Evidence Design v1.


## M32 - Auxiliar/Assistant Assistance Review Evidence Design v1

M32 defines an immutable design-only review-evidence envelope for possible later human review of M31 non-runtime Auxiliar/Assistant assistance records. It does not implement a live review-evidence builder, live validation, assistance transformation, Assistant activation, shadow-mode activation, route comparison, route selection, prompt selection, prompt loading, runtime integration, persistence, report writing, review queue writing, human decision recording, or candidate promotion.

Next allowed milestone after M32 validation and freeze: M33 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Readiness Gate for Pilot Boundary Review v1.

## M33 - Auxiliar/Assistant Assistance Readiness Gate for Pilot Boundary Review Design v1

`shadow_mode_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design.py` defines an immutable design-only readiness-gate record for a possible later Pilot/Copilot boundary review. It does not execute a live readiness gate, calculate readiness, read evidence, transform assistance, persist records, record human decisions, activate Assistant/Pilot/Copilot behavior, activate shadow mode, load prompts, integrate runtime routing, or grant router authority. M34 requires separate governed scope confirmation, validation, and freeze.



## M34 - Pilot/Copilot Boundary Design v1

`shadow_mode_pilot_copilot_boundary_design.py` defines an immutable design-only boundary for a possible later Pilot/Copilot phase review. It does not activate Pilot or Copilot behavior, start Assistant or Auxiliar behavior, run a pilot, run a copilot, compare routes, select routes, execute routes, select or load prompts, integrate runtime routing, inspect runtime state, persist records, write reports or queues, record human decisions, mutate gold or registry state, call providers, use embeddings, promote candidates, activate shadow mode, or grant authority. M35 requires separate governed scope confirmation, validation, and freeze.


## M35 - Post-Adviser to Pilot/Copilot Handoff Closure Design v1

`shadow_mode_post_adviser_pilot_copilot_handoff_closure_design.py` defines an immutable design-only closure and handoff record for the post-Adviser bridge after M34. It does not activate Assistant, Auxiliar, Pilot, Copilot, or shadow mode; does not run a handoff; does not compare, select, override, or execute routes; does not select or load prompts; does not integrate runtime routing; does not persist records; does not record human decisions; and does not grant runtime authority. After M35 validation and freeze, this bridge sequence is closed. Any future Pilot/Copilot work requires a separate governed scope.

## P0 - Pilot/Copilot Scope Charter and Entry Gate Design v1

`pilot_copilot_scope_charter_entry_gate_design.py` defines the first governed P-series scope charter after the M35 bridge closure and RG-PILOT-000 router canon freeze. It is design-only and records current state, lifecycle limits, forbidden operations, evidence ladder, surrounding-process risks, red-team seed cases, and the revised P0-P12 ladder.

P0 does not implement Pilot, Copilot, route projection, route comparison, prompt loading, runtime integration, persistence, training-data use, batch mode, limited shadow runtime, or candidate promotion.

Next allowed milestone after P0 validation and freeze: P1 - Routing Signal Scorer v3 Pilot Boundary Design v1.

## P1 - Pilot Boundary Design v1

`pilot_boundary_design.py` defines the immutable design-only boundary for what a future Pilot may become after P0 freeze. It records that Pilot remains not active, not runtime, not Copilot, not router authority, not prompt loader, not state writer, not a training-data source, and not a batch engine.

P1 does not implement Pilot, Copilot, projection logic, route comparison, input/output contracts, live validators, prompt loading, runtime integration, persistence, human decision recording, training-data use, batch mode, limited shadow runtime, or candidate promotion.

Next allowed milestone after P1 validation and freeze: P2 - Routing Signal Scorer v3 Pilot Input Output Contract and Validator Design v1.

## P2 - Pilot Input Output Contract and Validator Design v1

`pilot_io_contract_validator_design.py` defines immutable design-only future Pilot input/output field contracts and fail-closed validator-rule plans after P1 freeze. It does not implement a live validator, process inputs, generate outputs, implement Pilot, implement Copilot, implement projection logic, execute route comparison, select or load prompts, integrate runtime routing, persist records, use outputs for training data, run batch mode, activate limited shadow runtime, or grant runtime authority.

The contract design replaces unsafe prompt-group terminology with `task_classification_hints_summary` and requires future output invariants including `human_review_mandatory = True`, effect fields fixed to `"none"`, and `storage_status = "in_memory_only"`.

Next allowed milestone after P2 validation and freeze: P3 - Routing Signal Scorer v3 Pilot Disagreement Taxonomy Design v1.

## P3 - Pilot Disagreement Taxonomy Design v1

`pilot_disagreement_taxonomy_design.py` defines immutable design-only future Pilot disagreement categories and evidence-language rules after P2 freeze. It does not detect disagreements, score disagreements, compare routes, project routes, recommend actions, select or load prompts, read freeze memory, read gold sets, mutate registries, persist records, train models, run batch mode, activate Limited Shadow Runtime, or grant runtime authority.

The taxonomy is descriptive vocabulary for later human review only. It preserves match-before-disagree: no future taxonomy label can be trusted as a real disagreement until a governed future reproduction harness proves frozen router/canon reproduction first.

Next allowed milestone after P3 validation, freeze, startup refresh, and `FREEZE_MEMORY_STATUS: OK`: P4 - Routing Signal Scorer v3 Pilot Gold/Frozen Router Reproduction Harness Design v1.

## P4 - Pilot Gold/Frozen Router Reproduction Harness Design v1

`pilot_gold_router_reproduction_harness_design.py` defines immutable design-only future reproduction harness boundaries after P3 freeze. It preserves match-before-disagree: no Pilot disagreement evidence can be trusted until a later governed harness proves frozen router/canon reproduction first.

P4 does not implement a harness, load gold sets, read freeze memory, inspect runtime router state, compare routes, calculate scores, rank candidates, certify readiness, select or load prompts, persist records, train models, run batch mode, activate Limited Shadow Runtime, or grant Pilot/Copilot authority. It adds no Pilot implementation, no Copilot implementation, and no runtime authority.

Next allowed milestone after P4 validation, freeze, startup refresh, and `FREEZE_MEMORY_STATUS: OK`: P5 - Routing Signal Scorer v3 Pilot Simulation Skeleton Design v1.

## P5 - Pilot Simulation Skeleton Design v1

`pilot_simulation_skeleton_design.py` defines an immutable design-only skeleton for a future non-authoritative, opt-in, ephemeral Pilot simulation review envelope after P4 freeze. It names placeholder slots and stage ordering only.

P5 does not implement a simulator, callable builder, live validator, input processor, output generator, reproduction harness, no input processing, no output generation, gold loader, freeze-memory reader, prompt-library reader, route comparison executor, score calculator, disagreement detector, route projection, recommendation engine, prompt selection or loading, report writer, queue writer, persistence, human decision recording, training-data use, batch mode, Limited Shadow Runtime, Pilot behavior, Copilot behavior, or runtime authority.

Next allowed milestone after P5 validation, freeze, startup refresh, and `FREEZE_MEMORY_STATUS: OK`: P6 - Routing Signal Scorer v3 Pilot Review Evidence Design v1.

## P6 - Pilot Review Evidence Design v1

`pilot_review_evidence_design.py` defines immutable design-only vocabulary for a future non-authoritative, opt-in, ephemeral Pilot review evidence packet after P5 freeze. It names evidence fields and section ordering only.

P6 does not implement evidence collection, evidence packet generation, live validation, input processing, output generation, simulation execution, reproduction harness execution, gold loading, freeze-memory reading, prompt-library reading, runtime router inspection, route comparison execution, metric calculation, disagreement detection or trust, route projection, recommendation, prompt selection or loading, report writing, queue writing, persistence, human decision recording, approval recording, training-data use, batch mode, Limited Shadow Runtime, Pilot behavior, Copilot behavior, or runtime authority.

Next allowed milestone after P6 validation, freeze, startup refresh, and `FREEZE_MEMORY_STATUS: OK`: P7 - Routing Signal Scorer v3 Pilot Implementation Gate Design v1.

## P7 - Pilot Implementation Gate Design v1

`pilot_implementation_gate_design.py` defines immutable design-only gate conditions for a future non-runtime Pilot candidate implementation after P6 freeze. It names gate conditions and stage ordering only.

P7 does not implement gate evaluation, implementation approval, Pilot candidate creation, callable Pilot behavior, live validation, input processing, output generation, evidence collection, evidence packet generation, simulation execution, reproduction harness execution, gold loading, freeze-memory reading, prompt-library reading, runtime router inspection, route comparison execution, metric calculation, disagreement detection or trust, route projection, recommendation, prompt selection or loading, persistence, human decision recording, approval recording, training-data use, batch mode, Limited Shadow Runtime, Pilot runtime behavior, Copilot behavior, or runtime authority.

Next allowed milestone after P7 validation, freeze, startup refresh, and `FREEZE_MEMORY_STATUS: OK`: P8 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Implementation v1.

## P8 - Non-Runtime Pilot Candidate Implementation v1

`non_runtime_pilot_candidate.py` defines the first immutable non-runtime Pilot
candidate record after P7 freeze. It creates static metadata only: candidate
identity, boundary state, allowed/forbidden capability declarations, predecessor
precondition declarations, and fixed no-effect constants.

P8 does not implement a live Pilot, Copilot behavior, a callable simulator, live
validation, input processing, output generation, route projection, route
comparison execution, prompt selection or loading, prompt-library reading,
freeze-memory reading, gold loading, persistence, report writing, review queue
writing, human decision recording, approval recording, provider calls,
embeddings, training-data use, batch mode, Limited Shadow Runtime, field-test
activation, definitive enablement, or runtime authority.

The future activation key or maturity on/off behavior belongs to a separate
Activation Gate Box after lab testing and maturity evidence. P8 only records
that such activation is blocked in this milestone.

Next allowed milestone after P8 validation, freeze, startup refresh, and
`FREEZE_MEMORY_STATUS: OK`: P9 - Routing Signal Scorer v3 Non-Runtime Pilot
Candidate Contract Conformance v1.

## P9 - Non-Runtime Pilot Candidate Contract Conformance v1

P9 adds an immutable static contract-conformance declaration for the P8
non-runtime Pilot candidate. P9 is a static conformance declaration only. It maps future allowed input fields, future allowed
non-authoritative output fields, forbidden fields, and fixed invariants without
creating a live validator.

P9 does not process inputs, generate outputs, transform payloads, run a Pilot,
run a Copilot, compare routes, load prompts, read prompt libraries, read gold,
read freeze memory, persist records, write queues, write reports, call providers,
use embeddings, train from output, run batch mode, activate field testing,
activate Pilot/Copilot behavior, or grant runtime authority.

Field-test activation and definitive enablement remain deferred to a later
Activation Gate Box after lab testing and maturity evidence.
## P10 - Non-Runtime Pilot Candidate Readiness Gate v1

P10 adds an immutable static readiness gate declaration for the non-runtime
Pilot candidate after P9 freeze. It names readiness prerequisites, blocker
classes, allowed static outcome names, forbidden outcome names, and fixed
no-effect constants without creating a live gate evaluator.

P10 does not evaluate readiness, approve readiness, mark the candidate ready,
create a review packet, start lab testing, start field testing, activate Pilot,
start Copilot, compare routes, load prompts, read prompt libraries, read
gold, read freeze memory, persist records, write queues, write reports, call
providers, use embeddings, train from output, run batch mode, or grant runtime
authority.

Before any test-lab coding begins, the AI must warn the user and wait for
explicit confirmation. Field-test activation and definitive enablement remain
deferred to a later Activation Gate Box after lab testing and maturity evidence.

## P8/P9 regression phrase preservation note

Non-Runtime Pilot Candidate Implementation v1 remains an inert, static candidate record.
It is not a Pilot runtime. Human governance and the real router remain authoritative.
The field-test and definitive enablement are not allowed in this milestone.
The Activation Gate Box after lab testing and maturity evidence remains deferred.
P9 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Contract Conformance v1 remains the P8 successor.

Non-Runtime Pilot Candidate Contract Conformance v1 remains a static conformance declaration only.
It is not a live validator. Field-test activation and definitive enablement remain deferred.
P10 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Readiness Gate v1 remains the P9 successor.
## P11 - Non-Runtime Pilot Candidate Review Evidence Packet v1

P11 adds an immutable static review-evidence packet shape declaration for the
non-runtime Pilot candidate after P10 freeze. It names the future evidence
sections that a later governed human-review artifact must contain, but it does
not collect evidence, build a packet, populate a packet, write reports, persist
records, write review queues, record human decisions, approve readiness, or
activate any Pilot/Copilot behavior.

P11 does not start lab testing or field testing. Before any test-lab coding
begins, the AI must warn the user and wait for explicit confirmation. Field-test
activation and definitive enablement remain deferred to a later Activation Gate
Box after lab testing and maturity evidence.

P11 preserves no route comparison execution, no prompt loading, no prompt
library reading, no gold loading, no freeze-memory reading, no providers, no
embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, and
no runtime authority.
## P12 - Non-Runtime Pilot Phase Closure / Copilot Boundary Entry Gate v1

P12 adds an immutable static closure and entry-gate declaration for the current
non-runtime Pilot candidate foundation series after P11 freeze. It records that
P0 through P12 may be considered closed only after P12 validation, local freeze
write, startup freeze-context refresh, and `FREEZE_MEMORY_STATUS: OK`.

P12 does not implement Copilot, define Copilot scope, approve Copilot boundary,
start Pilot runtime, mark the ML mature, start lab testing, start field testing,
create an activation key, load prompts, persist records, compare routes, mutate
gold or registry data, train from output, run batch mode, or grant route
authority.

After P12 is frozen, the next safe behavior is STOP. Before any test-lab design
or coding begins, the AI must warn the user explicitly and wait for
confirmation. Any Copilot boundary design also requires a separate governed
scope.
