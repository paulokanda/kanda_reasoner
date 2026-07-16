# ASK_AI_PROJECT_REASONER Reusable Domain Contract

Status
- Canonical
- Reusable
- Project-agnostic

Purpose
This document defines how `developer_tools/kanda_reasoner_app` must be treated in future work.
Its purpose is to keep the project-reasoner stack generic, reusable across any selected repository, and isolated from project-specific runtime traces or code paths.

## 1. Core rule: reusable domain only

`developer_tools/kanda_reasoner_app` is a reusable tooling domain.
It is not part of any specific target project.
It may analyze a selected project root, but it must not become coupled to that project's runtime architecture.

Allowed
- Generic collector logic
- Generic runtime scenario logic
- Generic runtime feature attribution
- Generic retention and cleanup logic
- Generic reusable tests
- Generic metadata about reusable scope

Not allowed
- Hard dependencies on `shell/*`
- Hard dependencies on EEG-specific modules
- Project-specific hooks or traces leaking into reusable analytics
- Any assumption that the selected repository is `E:\eeg_kernel_ai_neural_data_analysis`

Practical rule
The selected repository is input.
`kanda_reasoner_app` is the reusable engine.
Never merge those two concerns.

## 2. line_level_source_truth

`project_reasoner` now includes `line_level_source_truth` as a canonical evidence layer.
This means future AI work should prefer grounded evidence tied to exact lines or tightly-scoped source anchors instead of vague file-level claims whenever that evidence exists.

Implications
- Prefer precise source-backed attribution over broad guesses.
- Treat line-level evidence as stronger than generic static summaries.
- Do not redesign this layer casually.
- Build on top of it; do not bypass it.

Intent
This layer exists to improve reasoning fidelity, auditability, and deterministic evidence selection.

## 3. Reusable runtime domain contract

Runtime scenario collection and runtime feature attribution are allowed only when they remain generic and reusable.

Canonical domain scope
- `kanda_reasoner_app`

Canonical runtime scope
- `generic_reusable`

Canonical project-summary metadata
- `collector_domain_scope = "kanda_reasoner_app"`
- `collector_runtime_scope = "generic_reusable"`
- `collector_is_project_agnostic = true`
- `collector_runtime_scenario_filter_mode = "canonical_domain_only"`

Canonical top-level metadata
- `collector_scope.domain_scope = "kanda_reasoner_app"`
- `collector_scope.runtime_scope = "generic_reusable"`
- `collector_scope.is_project_agnostic = true`
- `collector_scope.runtime_scenario_filter_mode = "canonical_domain_only"`

If future work changes these values, it must be intentional and tested.

## 4. Scenario admission and filtering rule

Runtime scenario ingestion is intentionally fenced.
Not every trace file found under the runtime-scenarios folder should be treated as valid reusable-domain evidence.

Canonical admission logic
A scenario may be admitted when it is clearly owned by `kanda_reasoner_app`, for example through one or more of the following:
- canonical scenario name ownership
- canonical app entry ownership
- canonical source-file ownership

Canonical pruning logic
Even when a scenario is admitted, only canonical-domain events should remain in the reusable analytics payload.
Foreign events should be pruned.

Interpretation rule
- Admit scenario by canonical ownership.
- Prune events by canonical source-file domain.
- Summarize only the pruned canonical event set.

This prevents mixed or contaminated traces from polluting the reusable output while preserving valid reusable-domain sessions.

## 5. Explicit exclusions

The following are intentionally excluded from reusable-domain runtime analytics unless a future design explicitly changes the contract:
- `shell/*`
- `plugins/*`
- `core/*`
- legacy `developer_tools/project_reasoner/*`
- other project-specific traces outside the canonical reusable domain

Why
These paths represent project-specific runtime behavior, not reusable collector-domain behavior.
Allowing them into the reusable analytics layer would contaminate scenario hotspots, feature attribution, and future AI reasoning.

Important
This is not a statement that those traces are useless.
It is a statement that they do not belong inside the reusable `kanda_reasoner_app` analytics contract.

## 6. Generic hotspot hook rule

`runtime_hotspot_hooks.py` must remain generic.
It may patch reusable-domain functions inside `developer_tools.kanda_reasoner_app`, such as:
- collector orchestration
- runtime scenario indexing
- runtime scenario summary building
- runtime scenario hotspot building
- runtime feature attribution building

It must not reintroduce:
- `shell.*`
- EEG-specific targets
- project-specific launcher or UI hooks

If future hooks target project-specific modules, they must live in a project-specific layer, not in the reusable domain.

## 7. Runtime trace retention

Runtime scenario traces are stored as individual `*_trace.json` files.
Retention exists to keep the shared reusable trace folder healthy over time.

Current retention behavior
- trace retention is wired into scenario finalization
- pruning is count-based by default
- pruning happens after finalize succeeds
- runtime analytics are not responsible for file cleanup

Canonical environment variable
- `ASK_AI_PROJECT_REASONER_KEEP_LATEST_RUNTIME_TRACES`

Meaning
Controls how many of the most recent runtime trace files are retained.

Resolver behavior
- missing env var -> use default
- invalid value -> use default
- too small -> clamp to minimum
- too large -> clamp to maximum

Interpretation rule for future AI work
If retention behavior must change, change the dedicated retention config/helper layer first.
Do not spread retention constants across unrelated modules.

## 8. What future AI should do

When modifying `kanda_reasoner_app`, future AI should:
- preserve project-agnostic behavior
- preserve line-level source truth as a first-class evidence layer
- preserve the canonical reusable-domain metadata in output JSON
- preserve the scenario admission and event pruning fence
- preserve the exclusion of `shell/*` and other project-specific paths from reusable analytics
- preserve generic hotspot hook scope
- preserve retention configurability through the dedicated env var
- prefer small additive changes with tests

Future AI should not:
- couple reusable analytics to the currently selected project's architecture
- use EEG-specific or shell-specific traces as reusable-domain evidence
- bypass the admission/filtering rule to "get more data"
- hardcode project roots into reusable logic
- scatter retention policy across multiple modules

## 9. Validation expectations

Any future modification to this contract should be protected by tests covering at least:
- scenario isolation
- hotspot hook generic scope
- retention helper behavior
- retention integration after finalize
- retention config resolution
- reusable collector scope integration

## 10. Summary

`kanda_reasoner_app` is a reusable analysis engine.
It may inspect many projects, but it must remain isolated from any one project's runtime identity.

The canonical guardrails are:
- line-level source truth stays authoritative
- runtime analytics stay inside the reusable domain
- non-canonical traces are excluded or pruned
- hotspot hooks stay generic
- retention stays configurable and centralized

That contract should remain stable unless intentionally redesigned with matching tests.
