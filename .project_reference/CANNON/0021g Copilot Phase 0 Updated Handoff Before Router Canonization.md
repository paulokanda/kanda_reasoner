# KANDA/PyArchitect Routing Signal Scorer v3

# Pilot/Copilot Phase 0 Updated Handoff Before Router Canonization

## 1. Purpose of this handoff

This document defines the updated complete logic for the next stage of the Routing Signal Scorer v3 roadmap after the Adviser-to-Pilot/Copilot bridge was closed.

It assimilates:

* the frozen M17-M35 bridge logic;
* specialist audit corrections;
* web research on secure AI lifecycle and risk management;
* book audit lessons from AI engineering, ML systems, reliable ML, human-in-the-loop ML, and secure software design.

This document is not code.

This document is not canon yet.

This document is the detailed handoff to be reviewed and then canonized into the router logic before P0 implementation begins.

## 2. Current canonical state

Long-term maturity path:

Adviser -> Auxiliar/Assistant -> Pilot -> Copilot

Current state:

* Adviser phase: closed and frozen through M16.
* M17-M35 bridge: complete and frozen.
* Bridge roadmap: 18 done, 0 to go.
* Auxiliar/Assistant: prepared through design and non-runtime bridge work, not active.
* Pilot: not started.
* Copilot: not started.
* Runtime shadow mode: not active.
* Runtime router authority: not granted.
* Candidate promotion: blocked.

Important:

M35 closed the bridge only.

M35 did not activate Pilot.

M35 did not activate Copilot.

M35 did not grant runtime authority.

M35 did not approve prompt loading.

M35 did not approve persistence.

M35 did not approve automatic maturity progression.

The next safe work is a new governed Pilot/Copilot Phase 0 scope.

The next safe milestone is:

P0 - Pilot/Copilot Scope Charter and Entry Gate Design v1

P0 must be design-only.

## 3. Safety boundary inherited from M35

The following remain forbidden unless a future governed scope explicitly changes them with validation, freeze, and human approval:

* no live Pilot behavior;
* no live Copilot behavior;
* no Assistant/Auxiliar activation;
* no Pilot activation;
* no Copilot activation;
* no shadow-mode activation;
* no automatic next milestone;
* no runtime route selection;
* no route override;
* no route execution;
* no prompt auto-loading;
* no prompt library scanning;
* no runtime integration;
* no router authority;
* no persistence;
* no caching of Pilot outputs;
* no review queue writing;
* no report writing;
* no human decision recording;
* no gold-set mutation;
* no registry mutation;
* no freeze-memory mutation by Pilot;
* no provider or model calls;
* no embeddings;
* no vector index use;
* no candidate promotion;
* no use of Pilot outputs as training data;
* no batch Pilot queries without separate governed approval.

## 4. Core doctrine

The doctrine remains:

ML recommends.
Canon and router governance decide.

For the Pilot stage, this must be tightened:

Pilot does not recommend.
Pilot does not decide.
Pilot does not route.
Pilot does not load prompts.
Pilot does not approve.
Pilot does not activate.
Pilot does not persist.
Pilot does not promote.

Pilot may later produce non-authoritative, opt-in, in-memory projection notes for human review only.

Evidence is not authority.

Projection is not recommendation.

Human review is not approval.

A readiness gate is not activation.

## 5. Main audit corrections assimilated

The audits identified several real improvements.

These are accepted.

### 5.1 Projection is not recommendation

Pilot must not be described as recommending a route.

Safe language:

Pilot produces a descriptive projection of how frozen canon constraints appear to classify a caller-supplied case summary.

Unsafe language:

Pilot recommends a route.
Pilot suggests a prompt.
Pilot proposes the best route.
Pilot selects required prompt groups.
Pilot decides what the router should do.

Required rule:

Every output must be framed as non-authoritative human-review support.

### 5.2 Disagreement taxonomy must come before implementation

Disagreement or divergence types must be defined before any callable Pilot projection exists.

Otherwise, implementation will create an implicit taxonomy that becomes hard to change.

Required rule:

The disagreement taxonomy must be frozen before any non-runtime Pilot implementation.

### 5.3 Pilot must first match before it can disagree

Pilot cannot be trusted to identify meaningful divergence until it first proves it can reproduce frozen router or frozen canon outcomes.

Required rule:

Pilot must pass a frozen-router or frozen-canon reproduction comparison milestone before its divergence signals can be treated as useful evidence.

Default strict threshold:

* 100 percent agreement on critical governance cases;
* zero critical deviations;
* zero unsafe proceed cases;
* zero prompt-loading leakage;
* zero runtime-coupling findings.

Any relaxed threshold requires a separate governed decision.

### 5.4 Explicit implementation gate is required

The bridge used implementation gates before first implementation. Pilot must follow the same logic.

Required rule:

A Pilot Implementation Gate must exist after design milestones and before the first callable Pilot implementation.

The gate can only say:

* blocked;
* not blocked for separate human-approved non-runtime implementation review.

It must not say:

* approved;
* ready;
* enabled;
* activated;
* promoted;
* runtime permitted.

### 5.5 Remove Limited Shadow Runtime from initial P-series

The term "Limited Shadow Runtime" creates a dangerous conceptual jump.

Runtime shadow mode requires a separate future governed scope with its own threat model, kill-switch design, monitoring design, rollback design, and isolation verification.

Required rule:

No runtime shadow mode appears in P0-P12.

The initial P-series remains non-runtime.

### 5.6 Copilot must be deferred

Copilot must not be implemented inside Pilot scope.

Copilot may have a boundary charter after Pilot readiness gates, but no Copilot behavior may start during Pilot work.

Required rule:

Pilot readiness may only make the project "not blocked for Copilot Boundary Design Review."

It cannot activate Copilot.

### 5.7 Prompt-group naming must be removed

The name candidate_prompt_groups is unsafe.

It implies the Pilot knows about loadable prompt groups.

Required rule:

Avoid prompt group names in Pilot input/output fields.

Use safer names:

* task_classification_hints_summary;
* routing_context_public_summary;
* task_classification_projection_summary.

Do not use:

* candidate_prompt_groups;
* simulated_required_prompt_groups;
* suggested_prompt_groups;
* prompt_to_load.

### 5.8 Human review must be mandatory by invariant

Do not use a field that can become false.

Unsafe:

requires_human_review = true/false

Safe:

human_review_mandatory = True

Required rule:

human_review_mandatory must always be True.

No code path may set it to False.

Pilot may add a low-priority note, but it may not suppress review.

### 5.9 Effect fields must be constants

The following fields must be constants, not computed by logic:

ROUTING_EFFECT = "none"
PROMPT_LOADING_EFFECT = "none"
RUNTIME_EFFECT = "none"
ACTIVATION_EFFECT = "none"
STORAGE_STATUS = "in_memory_only"

Tests must assert exact equality.

No branch may compute alternate values.

### 5.10 Pilot must be opt-in, ephemeral, non-training, and non-batch by default

Required rules:

* Pilot must be opt-in per invocation.
* There must be no global enable Pilot flag.
* Pilot outputs are ephemeral.
* Pilot outputs must not be cached, logged, stored, serialized, or persisted.
* Pilot outputs must not be used as training data.
* Pilot must not be queried in batch mode unless a separate governed milestone approves it.

## 6. Research and book-audit assimilation

The external research and book audit added these implementation-logic improvements:

### 6.1 Capability is not readiness

Pilot output existence is not evidence of Pilot readiness.

A Pilot function can run and still be unsafe, unhelpful, poorly calibrated, or authority-leaking.

P0 must state:

* running is not readiness;
* deterministic output is not readiness;
* matching some cases is not readiness;
* human-readable output is not readiness;
* non-authoritative text labels are not sufficient protection;
* readiness requires frozen gates, regression evidence, zero critical failures, and explicit human approval.

### 6.2 Pilot is a subsystem, not a helper function

Pilot must be treated as a governed subsystem with boundaries:

* lifecycle boundary;
* input boundary;
* output boundary;
* validation boundary;
* authority boundary;
* provenance boundary;
* human-review boundary;
* progression-gate boundary;
* runtime-exclusion boundary.

Do not describe Pilot as merely a helper function.

### 6.3 Critical boundary error budget is zero

Critical Pilot boundary error budget is zero.

Any critical boundary failure blocks progression.

Critical failures include:

* Pilot output affects routing;
* Pilot output implies approval;
* Pilot output implies prompt loading;
* Pilot imports runtime router;
* runtime router imports Pilot;
* Pilot reads project source files;
* Pilot writes files;
* Pilot persists output;
* Pilot logs output;
* Pilot mutates gold;
* Pilot mutates registry;
* Pilot mutates freeze memory;
* Pilot records human decisions;
* Pilot output is used as training data without separate approval;
* Pilot is queried in batch mode without separate approval;
* Pilot calls provider/model APIs;
* Pilot creates embeddings or vector indexes;
* Pilot activates Pilot/Copilot;
* Pilot grants runtime authority.

### 6.4 Human review must be designed

Human review must not be treated as a loose text label.

Pilot may support human review only when a governed milestone permits it.

Pilot must not record human decisions.

Pilot must not convert human review into approval.

Pilot must not create review queues or persistent review records in the initial P-series.

### 6.5 Threat modeling belongs in P0

P0 must include a threat model section.

The threat model must cover:

* authority leakage;
* prompt-loading leakage;
* runtime coupling;
* persistence leakage;
* batch evidence inflation;
* training-data leakage;
* cached-output authority drift;
* human overtrust;
* hidden import coupling;
* frozen canon drift;
* provenance tampering;
* scope creep from Pilot into Copilot or runtime shadow mode.

### 6.6 Lifecycle status must be explicit

P0 must define lifecycle status:

* govern: allowed;
* map: allowed;
* measure: design-only until contracts and taxonomy are frozen;
* manage: gate decisions only, no runtime action;
* deploy: forbidden;
* operate: forbidden.

Runtime shadow mode belongs to a separate future governed deployment/operation scope.

It must not appear as an initial P-series target.

### 6.7 Lightweight provenance is required

Every P-series freeze-ready patch must include lightweight provenance in KANDA_FREEZE_HINT.json.

Required provenance fields:

* patch_id;
* milestone_id;
* changed_files;
* validation_command;
* validation_markers;
* no_runtime_files_changed;
* no_startup_files_changed;
* no_prompt_files_changed;
* no_gold_files_changed;
* no_registry_files_changed;
* no_candidate_scorer_files_changed.

This is not full supply-chain tooling.

It is a lightweight tamper-resistance and review aid.

## 7. Revised P-series milestone ladder

The initial P-series should remain small and frozen milestone by milestone.

Do not compress everything into one large implementation.

Do not include runtime shadow mode.

Do not implement Copilot behavior.

### P0 - Pilot/Copilot Scope Charter and Entry Gate Design v1

Pattern protected:

scope-charter boundary pattern

Purpose:

Define the new governed Pilot/Copilot scope after M35.

Design-only.

P0 must define:

* current state;
* forbidden operations;
* lifecycle status;
* entry preconditions;
* evidence ladder;
* opt-in rule;
* ephemeral-output rule;
* no-training-data rule;
* no-batch rule;
* critical boundary error budget;
* surrounding process risks;
* future red-team seed cases;
* Copilot deferral;
* explicit non-goals.

No Pilot implementation.

No Copilot implementation.

No route analysis.

No input/output implementation.

No validator implementation.

### P1 - Pilot Boundary Design v1

Pattern protected:

Pilot boundary pattern

Purpose:

Define what Pilot is allowed to become and what remains forbidden.

Design-only.

Must state:

* Pilot is not active.
* Pilot is not runtime.
* Pilot is not Copilot.
* Pilot has no router authority.
* Pilot has no prompt-loading authority.
* Pilot has no persistence authority.
* Pilot outputs are non-authoritative human-review support only.
* Pilot is opt-in per invocation.
* Pilot outputs are ephemeral.
* Pilot cannot be used for training data without separate governed approval.
* Pilot cannot run in batch mode without separate governed approval.

### P2 - Pilot Input/Output Contract and Validator Design v1

Pattern protected:

contract and validator pattern

Purpose:

Define exact future input/output fields and fail-closed validation rules.

Design-only unless later intentionally split.

Must include:

* allowed input fields;
* allowed output fields;
* forbidden fields;
* primitive-only rule;
* unknown-key rejection rule;
* no live objects;
* no file handles;
* no callbacks;
* no provider/model instructions;
* no prompt-loading instructions;
* no route execution instructions;
* fixed authority notice;
* fixed effect constants;
* no prompt-group terminology.

Do not use candidate_prompt_groups.

Use task_classification_hints_summary.

### P3 - Pilot Disagreement Taxonomy Design v1

Pattern protected:

disagreement taxonomy before implementation pattern

Purpose:

Define all allowed divergence categories before any simulation logic exists.

Design-only.

The taxonomy must distinguish:

* no divergence;
* missing context;
* out-of-scope case;
* projection unavailable;
* non-critical projection divergence;
* safety boundary divergence;
* critical governance divergence.

The taxonomy must not imply that Pilot is correct when it differs from the router.

Preferred naming:

divergence_type

Avoid:

disagreement means Pilot is right

### P4 - Pilot Gold/Frozen Router Reproduction Harness Design v1

Pattern protected:

reproduction-before-disagreement pattern

Purpose:

Design how Pilot will later be compared against caller-supplied frozen router/canon outcomes.

Design-only.

This milestone establishes the rule:

Pilot must first demonstrate reproduction before divergence evidence is trusted.

Must forbid:

* gold mutation;
* file writes;
* persistence;
* source scanning;
* runtime router import;
* prompt loading.

### P5 - Pilot Simulation Skeleton Design v1

Pattern protected:

skeleton-before-implementation pattern

Purpose:

Define the future shape of a projection function without real logic.

Design-only.

No callable route analysis.

No live validation.

No projection execution.

No comparison execution.

No route suggestion.

No prompt selection.

### P6 - Pilot Implementation Gate Design v1

Pattern protected:

implementation gate pattern

Purpose:

Gate before first callable Pilot implementation.

Must require:

* P0-P5 frozen;
* all regressions passing;
* static import-boundary tests passing;
* no unsafe naming;
* no prompt-loading leakage;
* no runtime coupling;
* human approval for first non-runtime implementation.

Allowed outcomes:

* blocked;
* not blocked for separate human-approved non-runtime implementation review.

Forbidden outcomes:

* approved;
* ready;
* enabled;
* activated;
* promoted;
* runtime permitted.

### P7 - Non-Runtime Pilot Projection Implementation v1

Pattern protected:

non-runtime projection pattern

Purpose:

First callable Pilot function.

Allowed:

* pure function;
* caller-supplied primitive input only;
* fail-closed validation;
* in-memory output only;
* deterministic descriptive projection;
* fixed authority notice;
* fixed effect constants;
* human_review_mandatory = True.

Forbidden:

* recommendation;
* final route;
* prompt selection;
* prompt loading;
* runtime import;
* router call;
* file I/O;
* persistence;
* report writing;
* review queue writing;
* gold mutation;
* registry mutation;
* provider/model calls;
* embeddings;
* batch mode;
* training-data use;
* Copilot behavior.

### P8 - Non-Runtime Pilot Router Reproduction Comparison Implementation v1

Pattern protected:

router reproduction comparison pattern

Purpose:

Test whether Pilot projections reproduce caller-supplied frozen router/canon outcomes.

Allowed:

* caller-supplied case list;
* in-memory aggregate result;
* deterministic comparison;
* no gold mutation.

Required for progression:

* 100 percent agreement on critical governance cases;
* zero critical deviations;
* no unsafe proceed;
* no prompt-loading leakage;
* no runtime coupling.

If non-critical thresholds are needed later, they require a separate governed decision.

### P9 - Pilot Passive Simulation Evidence Record Design v1

Pattern protected:

passive evidence record pattern

Purpose:

Define passive in-memory evidence notes for human review.

Design-only.

Use:

Simulation Evidence Record

Avoid:

Review approval record
Human decision record
Promotion evidence
Readiness evidence

No persistence.

No queue writer.

No report writer.

No human decision recording.

### P10 - Pilot Readiness Gate for Copilot Boundary Review v1

Pattern protected:

readiness gate pattern

Purpose:

Determine whether the project is not blocked from designing a Copilot boundary.

This does not start Copilot.

Allowed outcomes:

* blocked;
* not blocked for separate Copilot boundary design review.

Forbidden outcomes:

* Copilot active;
* Copilot approved;
* runtime enabled;
* Pilot promoted;
* router authority granted.

Must require:

* P0-P9 frozen;
* 100 percent agreement on critical frozen cases;
* zero critical deviations;
* no prompt-loading leakage;
* no runtime imports;
* no persistence;
* no gold mutation;
* human sign-off artifact.

### P11 - Copilot Boundary Charter Design v1

Pattern protected:

Copilot boundary charter pattern

Purpose:

After P10 only, define what Copilot is allowed to become.

Design-only.

No Copilot implementation.

No Copilot runtime.

No route execution.

No prompt loading.

This milestone prevents Copilot from being treated as an implicit consequence of Pilot readiness.

### P12 - Copilot Scope Gate Design v1

Pattern protected:

future Copilot scope gate pattern

Purpose:

Create a gate for any future Copilot implementation scope.

Design-only.

No Copilot activation.

This becomes the entry point for a separate future governed Copilot scope.

## 8. P0 required record contents

P0 should expose one immutable, design-only record.

Required fields:

* milestone_id = "P0";
* title = "Pilot/Copilot Scope Charter and Entry Gate Design v1";
* design_status = "design_only";
* adviser_phase = "closed";
* bridge_phase = "closed";
* auxiliar_assistant_phase = "design_complete_not_activated";
* pilot_phase = "scope_charter_only";
* copilot_phase = "not_started";
* shadow_mode_active = False;
* pilot_active = False;
* copilot_active = False;
* runtime_authority_granted = False;
* prompt_loading_authority_granted = False;
* persistence_authority_granted = False;
* candidate_promotion_status = "blocked";
* implementation_blocked_by_default = True;
* pilot_outputs_ephemeral = True;
* pilot_opt_in_per_invocation = True;
* pilot_training_data_use_allowed = False;
* pilot_batch_mode_allowed = False;
* critical_boundary_error_budget = "zero";
* lifecycle_status;
* authority_statement;
* forbidden_operations;
* required_preconditions;
* evidence_ladder;
* surrounding_process_risks;
* red_team_seed_cases;
* revised_pilot_ladder;
* explicit_non_goals.

The authority statement must say:

Pilot/Copilot Phase 0 is a non-authoritative scope charter only. It does not start Pilot, does not start Copilot, does not route, does not load prompts, does not persist output, does not mutate gold or registry data, does not promote candidates, and does not grant runtime authority. Human governance and the real router remain authoritative.

## 9. Future Pilot input contract

Allowed future input fields should be primitive strings or tuple of strings only:

* case_id;
* schema_version;
* user_request_summary;
* routing_context_public_summary;
* task_classification_hints_summary;
* current_router_outcome_summary;
* frozen_canon_constraints_summary;
* known_boundary_flags;
* caller_generated_timestamp_utc.

Forbidden input concepts:

* raw prompt text;
* prompt file paths;
* prompt group objects;
* prompt library handles;
* live router objects;
* runtime state objects;
* provider/model configuration;
* file paths intended for execution;
* registry objects;
* gold-set mutation handles;
* callbacks;
* callables;
* training-data request;
* batch-mode request;
* activation request.

## 10. Future Pilot output contract

Use non-authoritative fields only:

* pilot_record_kind = "PILOT_PROJECTION_NON_AUTHORITATIVE";
* case_id;
* schema_version;
* authority_notice;
* projection_analysis_summary;
* task_classification_projection_summary;
* reasoning_summary_for_human_review;
* boundary_flags_for_human_review;
* divergence_summary_for_human_review;
* divergence_type;
* missing_information_summary;
* human_review_mandatory = True;
* advisory_review_priority;
* routing_effect = "none";
* prompt_loading_effect = "none";
* runtime_effect = "none";
* activation_effect = "none";
* storage_status = "in_memory_only".

Forbidden output fields:

* approved_route;
* final_route;
* execute_route;
* load_prompt;
* activate_pilot;
* activate_copilot;
* promote_candidate;
* write_gold;
* write_registry;
* record_human_decision;
* persist_report;
* runtime_authority;
* confidence;
* score;
* probability;
* recommendation;
* suggested_route;
* suggested_prompts;
* human_review_completed;
* promotion_ready;
* route_override;
* prompt_to_load;
* copilot_ready;
* runtime_enabled.

## 11. Validator requirements for later implementation

When validators are implemented, they must fail closed.

Input validator must reject:

* unknown keys;
* missing required keys;
* non-string values where strings are required;
* non-tuple values where tuple strings are required;
* nested objects;
* callables;
* file handles;
* runtime objects;
* prompt objects;
* registry objects;
* provider/model configuration;
* path execution markers;
* URL or network instruction markers;
* prompt-loading instructions;
* route execution instructions;
* gold mutation instructions;
* registry mutation instructions;
* persistence instructions;
* training-data-use instructions;
* batch-mode instructions;
* activation instructions.

Output validator must assert:

* authority_notice exact equality;
* human_review_mandatory is True;
* routing_effect == "none";
* prompt_loading_effect == "none";
* runtime_effect == "none";
* activation_effect == "none";
* storage_status == "in_memory_only";
* divergence_type belongs to frozen taxonomy;
* no forbidden output field appears.

## 12. Mandatory test doctrine

From P0 onward:

* immutable output test;
* exact phase assertion test;
* exact authority notice test;
* forbidden naming test;
* AST import-boundary test;
* no runtime router import;
* no prompt loader import;
* no freeze writer import;
* no gold writer import;
* no registry writer import;
* no provider/model import;
* no embedding/vector import;
* no open/eval/exec/compile/dynamic import;
* no stdout/stderr/logging;
* no side-effect snapshot test;
* no file or directory creation;
* no startup file mutation;
* no gold mutation;
* no registry mutation;
* no candidate scorer mutation;
* M17-M35 regression tests;
* Adviser closure regression tests;
* freeze hint test.

From P7 onward:

* deterministic output test;
* fail-closed invalid input tests;
* human_review_mandatory always True;
* effect constants exactly equal "none";
* storage_status exactly equals "in_memory_only";
* no batch mode without approval;
* no training-data use behavior;
* no runtime coupling;
* no prompt-loading leakage.

From P8 onward:

* frozen router/canon reproduction comparison tests;
* no gold-set mutation;
* caller-supplied cases only;
* critical governance cases must match exactly;
* zero critical deviations required for progression.

## 13. Required provenance in each patch

Every freeze-ready P-series patch must include root-level KANDA_FREEZE_HINT.json.

The freeze hint should include:

* patch_id;
* milestone_id;
* feature_id;
* changed_files;
* validation_command;
* validation_markers;
* expected_freeze_title;
* no_runtime_files_changed;
* no_startup_files_changed;
* no_prompt_files_changed;
* no_gold_files_changed;
* no_registry_files_changed;
* no_candidate_scorer_files_changed;
* no_persistence_added;
* no_prompt_loading_added;
* no_runtime_authority_added.

KANDA_FREEZE_HINT.json is delivery metadata only.

It must not be installed into project root.

## 14. What is rejected from audits

Some audit suggestions are not assimilated literally.

### 14.1 Do not compress everything into six large milestones

The idea of reducing planning debt is good.

But this project relies on small frozen increments.

So we do not collapse P0-P12 into six broad implementation milestones.

Instead, we keep small milestones but remove runtime scope creep and improve ordering.

### 14.2 Do not add external tools yet

Do not add:

* Import Linter dependency;
* SLSA tooling;
* Docker;
* external red-team tooling;
* provider SDKs;
* embeddings;
* vector databases;
* runtime audit hooks;
* monitoring stacks.

Use standard-library AST checks and deterministic tests for now.

### 14.3 Do not add runtime shadow steps

Runtime shadow mode is not part of P0-P12.

Any runtime shadow work requires a separate future governed scope after Pilot evidence, Copilot boundary, threat model, kill-switch design, monitoring design, rollback design, and human approval.

### 14.4 Do not define detailed Copilot behavior too early

Copilot gets a boundary charter after P10.

No Copilot implementation exists in this P-series.

## 15. Progress counter for future implementation

Current state before P0:

Bridge roadmap:
18 done, 0 to go.

Pilot/Copilot P-series:
0 done, 13 to go.

P-series milestones:

P0 - Scope Charter and Entry Gate Design
P1 - Pilot Boundary Design
P2 - Pilot Input/Output Contract and Validator Design
P3 - Pilot Disagreement Taxonomy Design
P4 - Pilot Gold/Frozen Router Reproduction Harness Design
P5 - Pilot Simulation Skeleton Design
P6 - Pilot Implementation Gate Design
P7 - Non-Runtime Pilot Projection Implementation
P8 - Non-Runtime Pilot Router Reproduction Comparison Implementation
P9 - Pilot Passive Simulation Evidence Record Design
P10 - Pilot Readiness Gate for Copilot Boundary Review
P11 - Copilot Boundary Charter Design
P12 - Copilot Scope Gate Design

When delivering code, state:

Progress:

* Bridge roadmap: 18 done, 0 to go.
* Pilot/Copilot P-series before current milestone: X done, Y to go.
* Current stage: Pn - milestone name.
* Current milestone delivery stage: 1 done, 4 to go.
* After local validation and freeze: X+1 done, Y-1 to go.
* Next local action: install patch, then run validation.
* Do not proceed until validation passes, freeze is written, startup freeze context is refreshed, and FREEZE_MEMORY_STATUS is OK.

## 16. Immediate next action

Do not implement Pilot yet.

Do not implement Copilot yet.

Do not implement P1-P12 yet.

Immediate next action:

Implement P0 only.

P0 must be a design-only scope charter and entry gate.

P0 should update the project with an immutable static record, notes, validation tests, box manifest update if required, regression whitelist updates if required, and a root-level KANDA_FREEZE_HINT.json in the patch ZIP only.

P0 must not add any callable Pilot projection logic.

P0 must not add runtime behavior.

P0 must not add prompt loading.

P0 must not add persistence.

P0 must not add Copilot behavior.

## 17. One-sentence canon candidate

Pilot/Copilot Phase 0 begins only as a design-only, non-authoritative, opt-in, ephemeral, zero-critical-error scope charter that preserves M35 bridge closure, forbids runtime authority and prompt loading, requires Pilot to reproduce frozen router/canon outcomes before disagreement evidence is trusted, and defers Copilot and any runtime shadow mode to separately governed future scopes.
