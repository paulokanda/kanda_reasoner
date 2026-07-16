Here is the complete final execution order roadmap I would use for Project Reasoner V10.

This order respects your main operating prompt: do architecture-sensitive work sequentially, and use the large-module refactor prompt only after boundaries are defined. The main prompt sets a batch-first audit mindset, but explicitly forbids batching high-risk architectural surfaces; your refactor template is excellent for controlled module decomposition once those surfaces are stable.

Final order roadmap
1. Freeze the current baseline

Goal: preserve current behavior before refactoring anything.

Do this first:

Save one canonical sample JSON index.
Save 15-30 representative architecture questions.
Save current outputs for deterministic, ranked, and AI-assisted routes.
Save one UI smoke path: load JSON -> ask question -> inspect evidence -> inspect prompt preview.

Why first: this project is heavily behavior-driven. The app depends on the loaded canonical JSON, route selection, and evidence display, so you need a known baseline before moving logic around.

Mode: sequential.

2. Define the stable contracts before any large split

Goal: create the interfaces that all later refactors will target.

Create these first:

IntentAnalysis
RouteDecision
AnswerRequest
AnswerResult
ValidationResult
ReasonerSessionService
ModelProvider
IndexRepository or equivalent access layer interface

Why now: without these seams, splitting large modules will only spread mixed responsibilities into smaller files. The current system already has partial dataclass modeling, but many important flows are still implicit.

Mode: sequential.

3. Canonicalize intent analysis into one engine

Goal: eliminate duplicated query-shape logic across the system.

Refactor all intent/question-shape detection into one canonical component, then make every other layer consume it.

The duplication is currently visible across:

v10_retriever.py
v10_prompt_builder.py
v10_ai_bridge.py
v10_intent_detection.py

Why now: this is the highest-leverage cleanup after contract definition. It reduces drift between retrieval, prompting, and model behavior.

Mode: sequential.

4. Extract orchestration out of v10_main_window.py

Goal: turn the GUI into a thin presentation shell.

Move these responsibilities out of the main window:

query execution orchestration,
retrieval invocation,
prompt assembly coordination,
model-call workflow,
validation result handling,
reasoning session state transitions.

Leave the window responsible only for:

widgets,
user actions,
rendering results,
displaying logs and evidence.

Why now: this is the main coupling hub. Fixing it early makes all later refactors safer.

Mode: sequential, high risk.

5. Build the formal grounding and insufficient-evidence validator

Goal: make grounding enforcement a first-class engine, not a scattered behavior.

Create explicit validator rules for:

allowed paths,
allowed symbols,
allowed snippet ids,
required snippet presence,
no synthetic code,
unsupported-claim detection.

This aligns with the project’s core safety model: use only evidence, never invent files/symbols/flows, and report uncertainty explicitly.

Why now: prompt strictness alone is not enough. The validator should become the hard safety boundary before more decomposition.

Mode: sequential.

6. Refactor v10_retriever.py

Goal: split the largest reasoning core into cohesive parts.

This is the first large module where your refactor prompt should be used.

Target helper structure:

query_normalization.py
path_filters.py
intent_overrides.py
candidate_generation.py
file_scoring.py
symbol_scoring.py
snippet_scoring.py
retrieval_merge.py
retrieval_profiles.py

Use v10_scoring_config.py and v10_project_profile.py as proper collaborators, not side helpers.

Why here: once intent and validation are stabilized, the retriever becomes safe to decompose.

Mode: sequential roadmap, but internal helper extraction can be bundle-safe in controlled groups.

7. Refactor v10_prompt_builder.py

Goal: reduce prompt complexity and make prompt generation schema-driven.

Split it into:

system constraints,
route-specific prompt planners,
answer-style instructions,
evidence pack formatter,
output schema formatter.

The prompt builder is central to grounding, but it should consume stable retrieval and validation contracts rather than re-deciding behavior itself.

Why after retriever: prompt logic should reflect stable retrieval output shape, not define it.

Mode: sequential.

8. Refactor v10_ai_bridge.py and provider stack

Goal: separate model transport, deterministic fast paths, and response handling.

Split the current layer into:

provider adapter,
deterministic responders,
response parser,
streaming bridge,
cache coordinator,
governance-state reader.

This layer currently mixes transport, prompt parsing, route behavior, and runtime-heavy heuristics.

Why here: after retrieval and prompt contracts are stable, the model side can be simplified cleanly.

Mode: sequential.

9. Refactor v10_index_loader.py into loader + repositories

Goal: preserve the JSON contract while reducing loader sprawl.

Keep one canonical raw loader, but extract repository-style accessors for:

files,
symbols,
snippets,
static context,
runtime sections,
UI/action sections.

Do not change the canonical JSON shape. The project depends on broad section availability and backward-compatible access.

Why after earlier phases: the loader is contract-sensitive. It should be refactored once consumers are cleaner.

Mode: sequential.

10. Normalize the core models package

Goal: make all important flows typed and explicit.

Expand beyond the current dataclasses so the system has typed representations for:

retrieval plan,
evidence pack,
validator findings,
final answer shapes,
provider request/response envelopes.

Why now: after the major service boundaries exist, type normalization becomes much easier.

Mode: bundle-safe.

11. Clean static-context and profile subsystems

Goal: make packaging/docs/profile handling consistent and passive where appropriate.

Clean up:

v10_static_context_dialog.py
v10_static_context_evidence_formatter.py
v10_static_context_inspector_widget.py
v10_project_profile.py

These should remain support layers, not hidden routing engines.

Why here: this is lower blast radius after core reasoning flow is stabilized.

Mode: bundle-safe.

12. Add structured observability and debug artifacts

Goal: make every reasoning run diagnosable.

Add structured events for:

JSON load health,
route selection,
retrieval timing,
evidence counts,
validation failures,
model latency,
cache hits,
final answer type.

The UI already exposes evidence, prompt preview, and logs, so this phase makes that observability formal and exportable.

Mode: bundle-safe.

13. Add performance improvements

Goal: speed up retrieval and reduce repeated work.

Implement:

pre-tokenized indexes,
lazy section materialization,
retrieval result caching,
evidence-pack fingerprint caching,
repeated query deduplication,
targeted section search instead of broad rescans.

This is best done after the architecture is clean so you optimize the right seams, not temporary ones.

Mode: bundle-safe.

14. Expand tests into a real regression suite

Goal: make future refactors safe.

Add:

unit tests for intent analysis,
retrieval scoring tests,
grounding validator tests,
prompt planning tests,
provider mock tests,
golden-answer tests for validated question families,
loader contract tests.

The current project already shows test intent around collector output sections; now the reasoning engine needs the same rigor.

Mode: bundle-safe, except golden baselines should be reviewed carefully.

15. Update HELP_INDEX and operator-facing workflow documentation

Goal: keep the app self-explanatory after the refactor.

Refresh the help system to document:

new route behavior,
validation meaning,
insufficient-evidence diagnostics,
static-context interpretation,
cache/governance/provider behavior.

The help index is already a major operator guide, so it should stay aligned with architecture changes.

Mode: bundle-safe.

The exact large-module refactor order

Use your large-module refactor prompt in this exact order:

v10_retriever.py
v10_prompt_builder.py
v10_ai_bridge.py
v10_index_loader.py
selective cleanup of v10_main_window.py after the service layer is already extracted.
What not to do first

Do not start by blindly splitting every huge module just because it is large.

Do not refactor v10_main_window.py, v10_retriever.py, and v10_prompt_builder.py all at once.

Do not optimize performance before contracts, intent, and validation are stabilized.

Those moves would increase the chance of preserving the wrong architecture in smaller files.

Final condensed order
Freeze baseline.
Define contracts.
Canonicalize intent analysis.
Extract orchestration from GUI.
Build formal grounding validator.
Refactor retriever.
Refactor prompt builder.
Refactor AI bridge/provider stack.
Refactor index loader into loader + repositories.
Normalize models/contracts.
Clean static-context/profile layers.
Add structured observability.
Add performance improvements.
Expand tests and golden regressions.
Update help/documentation.

That is the final order I recommend.


