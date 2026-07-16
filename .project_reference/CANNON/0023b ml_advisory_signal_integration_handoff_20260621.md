# ML Advisory Signal Integration Handoff

Date: 2026-06-21
Project: KANDA Reasoner / PyArchitect
Working area: Routing Signal Scorer / router prompt-selection logic
Prepared from: uploaded project ZIP, uploaded startup paste file, current freeze memory, and remembered prior ML integration discussion.
No new internet search was performed.

## 1. Current state

The project has already completed a large amount of non-runtime ML/router testing and governance work.

Verified current state from the uploaded project:

- The startup paste file is the active normal startup trigger for `first_prompts_to_ai.zip`.
- Normal startup requires loading `00_START_HERE_FOR_AI.md`, the manifest/readme, and numbered startup files 01 through 09 before project work.
- Startup and freeze hooks remain active.
- Project-specific freeze-intake state belongs under:
  - `project_freeze_after_update/freeze_hint_intake`
- Project-specific frozen memory belongs under:
  - `project_freeze_after_update/frozen_features_memory`
- Freeze entries must not be stored inside `project_freeze_ledger`.
- Preview remains read-only.
- Confirm and Write remains explicitly human-confirmed.
- Startup freeze context must be refreshed after local freeze write.

Verified current ML/router state from the uploaded project:

- Adviser phase was closed.
- Pilot/Copilot boundary work and non-runtime pilot planning were closed through the governed P-series path.
- LAB phase was created and closed through LAB-13.
- MLRT candidate reliability and prompt-selection testing proceeded through MLRT-112.
- The current MLRT expansion wave is closed and paused.
- Final closure preserved 1306/1306 validation-only cases across 24 real controlled offline prompt-selection suites and 24 paired review gates.
- MLRT tests are preserved as a reusable offline regression corpus.
- No cleanup patch is required by the final closure unless a later audit finds a concrete maintainability issue.
- ML is not integrated into router prompt logic yet.
- ML has no runtime route authority.
- ML cannot load prompts, modify router canon, write freeze memory, create training data, mutate gold registries, call providers, use embeddings/vector stores, persist reports, activate Pilot, or activate Copilot.

## 2. Confidence to continue

I understand where the project is now and I am safe to continue, with one important boundary:

I am secure to continue with the next governed ML advisory-signal integration design and patch sequence. I am not secure to jump directly into runtime ML routing, prompt auto-loading, autonomous prompt selection, provider calls, embeddings, training, calibration, persistence, activation, Pilot, or Copilot behavior.

The correct continuation is not more random MLRT expansion. The correct continuation is a separately governed ML Advisory Signal integration phase that uses the existing MLRT corpus and closure policy as safety evidence, while preserving router authority.

## 3. Synthesis from the prior external audit discussion

The previous discussion with the five AI specialists, internet review, and book audit was applied to the whole logic flow, not just one isolated part.

The accepted synthesis was:

- ML must remain an assistant/copilot-style advisory layer, not the router.
- The router/canon remains final authority.
- Use the internal term `ML Advisory Signal`.
- Split the integration into Phase 1a and Phase 1b.
- Phase 1a must be contract/stub/boundary only.
- Phase 1a must not expose advisory rankings.
- Phase 1a must not expose free-text explanations.
- Add a prompt-intake gate.
- Add a manual prompt-code resolver.
- A prompt code is a hint/reference, not authority.
- The router remains responsible for final required prompts/groups, missing context, May proceed, and next safe action.
- LAB and MLRT evidence is useful, but remains validation-only until a governed integration phase proves reliability under the frozen boundaries.

Book/audit-derived engineering additions to preserve:

- Formal evaluation loops before integration.
- System-level thinking: treat the ML advisory signal as one subsystem inside the router governance system, not a replacement for it.
- SRE-style critical error budget: critical boundary violations remain zero.
- Incident classes and failure taxonomy for all disagreements and unsafe outputs.
- Deterministic mocks and explicit fixtures for tests.
- Strong typing and strict schema validation for signal envelopes.
- Property-style and metamorphic tests for invariants.
- Only add ideas that materially improve safety, accuracy, or maintainability.

## 4. Non-negotiable integration doctrine

The doctrine for the rest of ML integration is:

`ML suggests signals. Router/canon decides.`

More precise rule:

`ML Advisory Signal may become one bounded input to router prompt logic, but it must never become the route decision, prompt loader, prompt selector, May proceed authority, freeze writer, startup modifier, training source, calibration authority, or Copilot instruction.`

Conflict rule:

- If ML Advisory Signal agrees with the router, it may increase confidence for human review.
- If ML Advisory Signal is incomplete, malformed, stale, unsafe, or contradictory, it is ignored or downgraded.
- If ML Advisory Signal conflicts with router canon, freeze memory, startup rules, prompt-library audit rules, or box boundaries, the router/canon wins.
- Any critical boundary violation blocks the signal and records the failure class in validation/review evidence.

## 5. Logic from current point to end of ML integration

### Stage A - Freeze-aware starting checkpoint

Goal:
Confirm current starting state before any new patch.

Inputs:
- Project ZIP.
- Startup paste file.
- Freeze memory index.
- Final MLRT closure entry.
- MLRT consolidation and coverage map.
- Active routing canons.

Required conclusion:
- MLRT expansion is closed and paused.
- Existing 1306/1306 cases are reusable offline regression coverage.
- The next work is a new ML Advisory Signal integration phase, not more MLRT growth and not runtime ML routing.

Allowed output:
- Handoff only.
- No code change.

### Stage B - RG-ML-ADV-000 integration canon

Goal:
Create the router canon that governs the new ML Advisory Signal integration phase.

Patch type:
- Prompt/canon documentation and metadata only.

Must define:
- Scope.
- Forbidden behaviors.
- Phase ladder.
- Required context package.
- May proceed rules.
- Freeze requirements.
- Critical boundary error budget = 0.
- Rule that router remains final authority.
- Rule that prompt code is hint/reference only.
- Rule that Phase 1a is contract/stub/boundary only.

Must not do:
- Python runtime integration.
- Prompt loading.
- Provider calls.
- Embeddings/vector stores.
- Persistence.
- Training/calibration.
- Actual ML output use.
- UI activation.
- Pilot/Copilot behavior.

Exit gate:
- Local validation.
- Freeze.
- Startup freeze context refreshed.
- FREEZE_MEMORY_STATUS OK.

### Stage C - Phase 1a: ML Advisory Signal contract and inert source surface

Goal:
Add the smallest safe source surface for the advisory signal.

Patch type:
- Standard-library-only Python contract/stub.
- Tests.
- Manifest entry.
- KANDA_FREEZE_HINT.

Allowed:
- Define `MLAdvisorySignalEnvelope`.
- Define strict schema/validator.
- Define boundary constants.
- Define status flags.
- Define no-op/inert stub function returning disabled/unavailable state.
- Define manual prompt-code resolver interface as a contract only.
- Define prompt-intake gate contract as a contract only.
- Validate that every forbidden capability is false.

Not allowed in Phase 1a:
- No rankings.
- No scores used for routing.
- No free-text explanations.
- No prompt group loading.
- No live prompt library reads.
- No freeze memory reads for ML.
- No provider calls.
- No embeddings.
- No persistence.
- No candidate execution.
- No model calls.
- No route comparison at runtime.
- No UI activation.
- No Pilot/Copilot behavior.

Suggested Phase 1a fields:
- `signal_schema_version`
- `signal_status`
- `advisory_only`
- `router_authority_effect`
- `prompt_loading_effect`
- `runtime_effect`
- `persistence_effect`
- `human_review_mandatory`
- `critical_boundary_error_budget`
- `prompt_code_hint`
- `prompt_code_resolver_status`
- `intake_gate_status`
- `blocked_reason_codes`

Forbidden Phase 1a fields:
- `final_route`
- `selected_prompt`
- `prompt_to_load`
- `required_prompt_groups`
- `may_proceed_now`
- `approval_status`
- `human_approved`
- `confidence_ranking`
- `free_text_explanation`
- `write_memory`
- `training_label`

Exit gate:
- Contract tests prove no authority leakage.
- Freeze.
- Startup freeze context refreshed.
- FREEZE_MEMORY_STATUS OK.

### Stage D - Phase 1b: offline advisory signal preview, still non-runtime

Goal:
Allow a bounded offline advisory signal preview using explicit test-local inputs.

Patch type:
- Test-local simulation only.
- No runtime integration.

Allowed:
- Static input cases.
- Static candidate advisory envelopes.
- Manual prompt-code resolver mapping for known codes.
- Prompt-intake gate evaluation against fixed cases.
- Review-only advisory preview.
- Disagreement classification.
- No output persistence.

Not allowed:
- No live project prompt loading.
- No automatic prompt selection.
- No runtime router decision influence.
- No provider calls.
- No embeddings.
- No training or calibration.
- No saved report unless a separate report-persistence milestone is governed.

Exit gate:
- Validation proves the signal can be produced, resolved, and ignored safely when malformed.
- Freeze.
- Startup freeze context refreshed.
- FREEZE_MEMORY_STATUS OK.

### Stage E - Offline comparison against frozen router outcomes

Goal:
Use the existing MLRT corpus as regression coverage to test whether ML Advisory Signal can help prompt selection without authority.

Patch type:
- Validation-only offline comparison.

Use existing evidence:
- 1306/1306 validation-only cases.
- 24 real suites.
- 24 paired review gates.
- Risk families from MLRT-65 to MLRT-112.

Allowed:
- Compare advisory signal hint to expected prompt route in fixed cases.
- Count agreement, accepted alternate, forbidden route hit, malformed signal, missing signal, stale signal, and conflict categories.
- Hard gates before soft metrics.
- Critical boundary violations override any accuracy.

Not allowed:
- No reliability claim unless separately reviewed.
- No runtime use.
- No router prompt logic modification yet.
- No model improvement.
- No training/calibration.
- No persistent dataset mutation.
- No gold registry mutation.

Exit gate:
- Offline comparison passes strict gates.
- Human review accepts evidence as advisory-signal readiness evidence, not runtime authority.
- Freeze.
- Startup freeze context refreshed.
- FREEZE_MEMORY_STATUS OK.

### Stage F - Human review and promotion gate for advisory-signal integration

Goal:
Decide whether the advisory signal is ready to be connected to router prompt logic as a bounded input.

Patch type:
- Review gate documentation/test.

Required review questions:
- Does the signal ever claim final authority?
- Does it ever request prompt loading?
- Does it ever bypass freeze or startup rules?
- Does it ever bypass prompt-library audit?
- Does it ever produce unbounded free text?
- Does it ever create or mutate training/gold/persistence state?
- Does it remain safely ignorable?
- Does router/canon still win every conflict?
- Are there zero critical boundary violations?
- Is the performance enough to be useful, not just non-dangerous?

Exit options:
- `NOT_READY`
- `READY_FOR_NON_RUNTIME_ROUTER_LOGIC_ADVISORY_INPUT_ONLY`
- `BLOCKED_BY_CRITICAL_BOUNDARY_RISK`
- `BLOCKED_BY_LOW_USEFULNESS`
- `NEEDS_MORE_OFFLINE_CASES`

Only the second label may allow the next stage.

### Stage G - Router prompt logic integration as advisory input only

Goal:
Connect ML Advisory Signal to router prompt logic without making it authoritative.

Patch type:
- Minimal router prompt logic integration.
- Default-off or explicit path, depending on current router architecture.
- Strict guards.

Allowed:
- Router can read a prevalidated in-memory advisory signal envelope.
- Router can use it as a secondary check after canonical route determination.
- Router can display or record internally that advisory signal agrees/disagrees, only if no persistence is introduced.
- Router can downgrade/ignore unsafe signals.
- Router can require human review when signal conflicts with canon.

Not allowed:
- ML cannot choose final required prompts/groups.
- ML cannot set May proceed.
- ML cannot load prompts.
- ML cannot suppress missing context.
- ML cannot override stale-file rules.
- ML cannot bypass freeze confirmation.
- ML cannot bypass startup maintenance rules.
- ML cannot update prompt library or metadata.
- ML cannot change freeze memory.
- ML cannot create training labels.
- ML cannot become Pilot/Copilot.

Conflict behavior:
- Canon route wins.
- Freeze memory wins.
- Startup rules win.
- Box boundaries win.
- Prompt-library audit rules win.
- Missing context rules win.
- Pre-output gates win.
- ML signal is ignored when malformed, stale, unsafe, ambiguous, or contradictory.

Exit gate:
- Full regression against MLRT corpus and routing canons.
- Boundary tests pass.
- Freeze.
- Startup freeze context refreshed.
- FREEZE_MEMORY_STATUS OK.

### Stage H - Shadow observation, still non-authoritative

Goal:
Observe advisory-signal usefulness under controlled tasks without changing final routing.

Patch type:
- Shadow/manual observation only.

Allowed:
- Human-visible note or review packet if separately approved.
- Agreement/disagreement classification.
- No automatic decisions.
- No persistence unless separately governed.

Not allowed:
- No training loop.
- No provider call.
- No prompt auto-loading.
- No autonomous patching.
- No automatic freeze writing.
- No Copilot.

Exit gate:
- Human review decides whether advisory signal is useful enough to remain.
- Critical boundary error budget remains zero.

### Stage I - Final advisory integration freeze

Goal:
Freeze the integrated ML Advisory Signal as a stable advisory-only subsystem.

End state:
- ML Advisory Signal exists.
- Router prompt logic may consider it as a bounded advisory input.
- Router/canon keeps final authority.
- All critical boundary protections remain.
- MLRT corpus remains reusable for future regression.
- No runtime route authority is granted.
- No autonomous prompt loading.
- No training/calibration unless a separate future phase is governed.
- No Pilot/Copilot activation unless a separate future phase is governed.

## 6. What "end of ML integration" should mean for this project

The safe end of this ML integration should not be "ML routes automatically."

The safe end should be:

`ML Advisory Signal is integrated as a guarded, non-authoritative helper for prompt-selection reasoning, while the governed router remains the only authority that selects required context, decides missing behavior, applies May proceed rules, and enforces freeze/startup/patch gates.`

That is the best balance between the positive test results and the project's safety/governance architecture.

## 7. Next safe action

The next safe action is to create a governed patch for:

`RG-ML-ADV-000 - ML Advisory Signal Integration Phase Router Canon v1`

That patch should be documentation/metadata only. It should not touch runtime routing code yet.

## 8. Patch discipline for next work

For the next patch:

- Use a compact Windows-safe ZIP basename.
- Include only updated files.
- Include root-level `KANDA_FREEZE_HINT.json` unless intentionally non-freezeable.
- Use feature-specific freeze data.
- Do not hardcode one project root as every project root.
- Use project-specific freeze paths under `project_freeze_after_update`.
- Preserve explicit Confirm and Write.
- Refresh startup freeze context after freeze.
- Do not use old Downloads/Desktop-first installer search template.
- Do not create runtime ML behavior before the canon and Phase 1a freeze.

## 9. My continuation readiness

I am safe to continue from here if the next requested work stays on this governed path:

1. RG-ML-ADV-000 canon.
2. Phase 1a inert contract/stub/boundary.
3. Phase 1b offline advisory preview.
4. Offline comparison and review gates.
5. Only then minimal advisory-only router prompt logic integration.

I should not continue by directly implementing ML route selection or modifying router prompt logic to trust ML output.
