# Routing Signal Scorer — ML Advisory Signal, Governed Prompt Intake, and Manual Prompt Code Hint Canon v1

Generated: 2026-06-21  
Project: KANDA / PyArchitect / `kanda_reasoner`  
Component: Routing Signal Scorer  
Status: Canon for next-phase design, not yet implementation  
Primary purpose: Preserve the agreed architecture and boundaries before creating the next governed patch.

---

## 1. Canonical Current State

The controlled offline ML prompt-selection MLRT wave is complete.

### Frozen MLRT status

- MLRT expansion is closed and paused.
- MLRT-113 must not be created as a continuation of the completed wave.
- Final MLRT coverage: `1306/1306`.
- Real MLRT suites: `24`.
- Paired review gates: `24`.
- Existing MLRT tests are preserved as a reusable offline regression corpus.
- MLRT tests must not be deleted, collapsed, or rewritten into vague aggregate tests.
- Future MLRT expansion is allowed only if:
  - a new governed risk appears, or
  - a separate ML advisory-signal integration phase introduces new risks that require new tests.

### Frozen final closure feature

Frozen feature:

```text
Routing Signal Scorer MLRT Final Closure Audit and Reuse Policy v1
```

Confirmed:

- Organization/readability audit: done.
- Coverage map by risk family and suite number: done.
- Duplicate/redundant suite-language review: done.
- Runtime/router authority leakage check: done.
- Cleanup patch: not required unless a later concrete issue appears.
- ML is not integrated into route prompt logic.
- ML has no runtime route authority.
- ML remains validation-only / advisory-design preparatory context.

---

## 2. Core Principle

The next phase must not make ML the router.

The next phase may define a safe future path for ML as a non-authoritative advisory signal, but:

```text
ML may suggest.
ML may warn.
ML may abstain.
ML may help identify a prompt gap.
ML may never decide the final route.
ML may never override governed router logic.
ML may never write prompts, freeze entries, registries, route decisions, or prompt-library state.
```

The governed router remains the final authority.

---

## 3. Correct Next Phase Name

Use this internal phase name:

```text
Routing Signal Scorer ML Advisory-Signal and Governed Prompt Intake Boundary Contract v1
```

Avoid using `router copilot` as the formal internal name because “copilot” implies shared agency.

Allowed conversational explanation:

```text
This is a copilot-like advisory layer.
```

Canonical internal language:

```text
ML Advisory Signal
Non-authoritative advisory telemetry
Boundary contract
Phase 1a
```

---

## 4. Phase Split

The next work must be split into Phase 1a and Phase 1b.

### Phase 1a — allowed now

Phase 1a is contract, isolated subbox, deterministic stub/mock, prompt-intake boundary, and tests.

Allowed:

- Documentation/canon.
- Threat model.
- Standards crosswalk.
- Isolated `ml_advisory_signal` subbox skeleton.
- Frozen typed dataclass contracts.
- Advisor protocol/interface.
- Null advisor.
- Deterministic mock advisor.
- Boundary guard helpers.
- Output/egress firewall.
- AST import-boundary tests.
- Capability-denial tests.
- No-I/O/no-network/no-subprocess tests.
- No-authority tests.
- Route-invariance tests.
- Prompt-intake boundary documentation.
- Manual Prompt Code Hint Gate documentation/tests.
- Closure doc.

### Phase 1a — forbidden

Forbidden:

- Real ML inference.
- Provider calls.
- Embeddings.
- Vector stores.
- Model training.
- Model calibration.
- Model improvement.
- Persistent logs/datasets.
- Runtime shadow mode.
- Runtime Pilot/Copilot behavior.
- Advisory rankings as route precedence.
- Free-text advisory explanation parsed by code.
- Router prompt logic modification that gives ML influence.
- Prompt library reads from ML.
- Freeze memory reads from ML.
- Router canon reads from ML.
- Gold registry writes.
- Registry mutation.
- Prompt insertion into router logic.

### Phase 1b — future, separate review only

Phase 1b may later consider real advisory logic or controlled offline replay, but only after Phase 1a is validated and frozen.

Phase 1b requires a separate audit and freeze.

No implementation from Phase 1b should be smuggled into Phase 1a.

---

## 5. Four Canonical Boxes

The architecture now has four conceptual boxes.

### 5.1 Governed Router

Role:

- Final route authority.
- Applies governed routing rules.
- Validates candidate prompts.
- Rejects unsafe or out-of-scope hints.
- Never treats ML as final authority.

Hard rule:

```text
The governed router can consider advisory or manual hint information only through validation.
The governed router never delegates final route selection to ML or to a user-entered code.
```

### 5.2 ML Advisory Signal

Role:

- Non-authoritative telemetry.
- May flag ambiguity.
- May flag conflicts.
- May flag possible prompt gaps.
- May abstain.
- May produce controlled reason codes.

Forbidden:

- Authoring prompts.
- Registering prompts.
- Editing prompt library.
- Reading full prompt library.
- Reading freeze memory.
- Reading router canon.
- Deciding the final route.
- Producing final prompt selection.
- Outputting executable commands.
- Persisting data.
- Calling providers.
- Calling embeddings.
- Performing training/calibration.

### 5.3 Governed Prompt Intake Gate

Role:

- The only safe door for new prompts.
- Creates, edits, classifies, tests, codes, and registers prompts.
- Supports global, box-specific, and project-specific prompts.
- Runs test batteries before router binding.
- Freezes validated prompt additions.

Important distinction:

```text
ML may detect that a prompt gap exists.
ML may not write or register the new prompt.
```

### 5.4 Interactive Manual Prompt Code Resolver

Role:

- Human-in-the-loop disambiguation for difficult classifications.
- Converts user clarification into a validated prompt-code hint.
- Allows adding, removing, replacing, or clearing the code.
- Helps classification but does not override final routing authority.

Example:

```text
User: use box logic here
Router: ambiguous
App presents choices
User selects Routing Signal Scorer logic
App attaches RSS-0005 as a manual classification hint
Router validates RSS-0005
Router considers the linked prompt card
Final routing remains governed
```

---

## 6. ML Advisory Signal Contract

### 6.1 Allowed input concept

Use a frozen typed input object, not raw prompts or generic metadata.

Recommended input shape:

```text
AdvisoryInput:
- scenario_id: str
- sanitized_context_hash: str
- candidate_prompt_group_ids: tuple[str, ...]
- ambiguity_score: float
- conflict_score: float
- risk_family_id: str | None
```

### 6.2 Forbidden inputs

The ML advisory box must not receive:

- Raw user prompt text.
- Full prompt text.
- Prompt library entries.
- Freeze memory.
- Router canon.
- Workflow metadata.
- User PII.
- Execution stack traces.
- File-system paths.
- Mutable router objects.
- Database handles.
- Provider handles.
- Registry handles.
- Arbitrary metadata dictionaries.
- Direct references to project files.
- Direct references to prompt-library/freeze-memory objects.

### 6.3 Allowed output concept

Use frozen typed output.

Recommended output shape:

```text
AdvisoryOutput:
- advisory_flags: tuple[AdvisoryFlag, ...]
- advisory_group_observations: tuple[AdvisoryGroupObservation, ...]
- advisory_reason_codes: tuple[AdvisoryReasonCode, ...]
- advisory_should_abstain: bool
- non_authoritative_confidence: float
- boundary_status: BoundaryStatus
- is_mock: bool
```

### 6.4 Important naming correction

Do not use:

```text
must_not_route
```

Use:

```text
advisory_should_abstain
```

Reason:

- `must_not_route` sounds like ML has veto power.
- `advisory_should_abstain` correctly means ML has no useful advisory signal.
- Governed routing continues normally.

### 6.5 No advisory rankings in Phase 1a

Do not use:

```text
advisory_rankings
```

Reason:

- Ranking implies precedence.
- Precedence can become hidden tie-breaking authority.
- Hidden tie-breaking authority is authority creep.

Allowed Phase 1a substitute:

```text
advisory_group_observations
```

Observation must not create order semantics.

### 6.6 No natural-language explanation in Phase 1a

Do not use:

```text
advisory_explanation: str
```

Use:

```text
advisory_reason_codes: tuple[AdvisoryReasonCode, ...]
```

Reason:

- Natural language output can become a prompt-injection channel.
- Natural language can be accidentally parsed as logic.
- Reason codes are bounded, testable, and safe.

---

## 7. ML Advisory Forbidden Field Names

The advisory output contract must reject these names:

```text
route
selected_route
final_route
selected_prompt
final_prompt
decision
override
must_route
must_not_route
ranking
rankings
winner
best_candidate
execute
command
write
mutate
register
freeze
insert_prompt
```

If any future advisor returns fields with these semantics, the output firewall must reject it.

---

## 8. Output / Egress Firewall

The ML advisory subbox must include an output validator.

Purpose:

- Validate shape.
- Validate allowed keys.
- Reject unknown keys.
- Reject executable semantics.
- Reject authority semantics.
- Reject mutation semantics.

The output firewall must reject:

- Unknown fields.
- Callable objects.
- Commands.
- Executable strings.
- `exec`.
- `eval`.
- `subprocess`.
- `os.system`.
- `importlib`.
- Shell commands.
- Registry write semantics.
- Freeze write semantics.
- Router override semantics.
- Ranking/selection/winner semantics in Phase 1a.
- Free-form explanation fields in Phase 1a.

---

## 9. Capability-Denial Contract

The ML advisory box must have zero capabilities in Phase 1a.

Denied capabilities:

- No file writes.
- No file reads except its own static contract/test fixtures if explicitly allowed.
- No network.
- No subprocess.
- No provider SDK.
- No embeddings.
- No vector stores.
- No prompt loading.
- No freeze-memory read.
- No router-canon read.
- No registry write.
- No gold registry write.
- No prompt-library mutation.
- No callbacks into router internals.
- No background threads.
- No persistence.
- No report persistence.
- No dataset creation.
- No training-data collection.

---

## 10. Import Boundary Contract

### 10.1 Allowed imports inside `ml_advisory_signal`

Allowed:

- Python standard library.
- `typing`.
- `dataclasses`.
- `enum`.
- Local contract/interface modules inside the advisory subbox.

### 10.2 Forbidden imports inside `ml_advisory_signal`

Forbidden:

- Router internals.
- Router canon.
- Prompt library.
- Freeze memory.
- Workflow engine.
- Registry logic.
- Gold registry.
- Persistence layer.
- Provider SDKs.
- Embedding libraries.
- Network libraries.
- Subprocess helpers.
- Prompt-loading logic.
- Other high-authority boxes.

### 10.3 Directional dependency

Allowed direction:

```text
Governed router / test harness -> public advisory interface
```

Forbidden direction:

```text
ML advisory subbox -> governed router internals
ML advisory subbox -> freeze memory
ML advisory subbox -> prompt library
ML advisory subbox -> router canon
```

---

## 11. Prompt Intake Gate

### 11.1 Purpose

The Governed Prompt Intake Gate is the only safe path for adding future prompts.

It exists because:

- Future projects may need project-specific prompts.
- Automatic classification may be difficult.
- Prompts must be treated as software artifacts.
- New prompts must be classified, tested, validated, and frozen before router binding.

### 11.2 Prompt as first-class artifact

Every governed prompt should have:

```text
Prompt ID
Prompt code
Prompt title
Box ownership
Project/global scope
Allowed use cases
Forbidden use cases
Input contract
Output contract
Boundary rules
Test battery status
Freeze status
Version
Supersession status
Lifecycle state
```

### 11.3 Prompt lifecycle states

Canonical lifecycle:

```text
PROPOSED
CLASSIFIED
DRAFTED
TESTED
VALIDATED
ROUTER_BOUND
FROZEN
SUPERSEDED
RETIRED
REJECTED
```

Only prompts with all of the following may be considered by router logic:

```text
VALIDATED
ROUTER_BOUND
FROZEN
ACTIVE
NOT SUPERSEDED
SCOPE ALLOWED
TESTS PASSED
```

### 11.4 Prompt-intake pipeline

Canonical pipeline:

```text
1. Proposal
2. Classification
3. Duplicate/overlap audit
4. Prompt clarity edit
5. Security/boundary review
6. Test battery
7. Code binding
8. Router binding
9. Freeze
```

### 11.5 Prompt-intake firewall

Prompt Intake must reject prompts that instruct the system to:

- Ignore previous rules.
- Override router.
- Bypass freeze.
- Write directly to registry.
- Modify prompt library without tests.
- Always select this prompt.
- Treat this prompt as final route.
- Import from other box internals.
- Call provider/network/persistence.
- Leak freeze memory or router canon.
- Create training data without governance.
- Mutate gold registry.
- Mutate freeze index.
- Modify unrelated boxes.

---

## 12. Prompt Code Registry

### 12.1 User-friendly code vs internal code

User may type:

```text
use box logic
use code 0005
```

Internally, codes must be namespaced.

Examples:

```text
BOX-0005
RSS-0005
PLIB-0005
FRZ-0005
TEST-0005
PROJECT-KANDA-0005
PROJECT-KANDA-RSS-0005
GLOBAL-BOX-0005
```

### 12.2 Code is reference, not command

Canonical rule:

```text
User code = candidate prompt reference.
User code ≠ final authority.
User code ≠ router override.
User code ≠ direct prompt execution command.
```

### 12.3 Code resolution checks

When a code is present, the system must check:

```text
Does the code exist?
Is it active?
Is it scoped to this project?
Is it allowed for this box?
Did it pass prompt test batteries?
Is it frozen/validated?
Does the current task match allowed use cases?
Is it superseded?
Does a higher-priority safety rule block it?
Does it conflict with another active code?
```

### 12.4 Code binding after validation

A prompt receives a stable code only after passing:

- Classification test.
- Duplicate/overlap test.
- Boundary test.
- Clarity test.
- Injection-resistance test.
- Project-scope test.
- Code-binding test.
- Regression test.
- Router non-authority test.
- Freeze-readiness test.

---

## 13. Interactive Manual Prompt Code Resolver

### 13.1 Purpose

This gate supports cases where automatic classification is hard and the user/manual workflow knows the intended logic.

Example ambiguity:

```text
User says: "Use box logic here."

Automatic router may not know whether this means:
- Routing Signal Scorer box
- Prompt Library box
- Freeze workflow box
- Project-specific box
- Test-generation box
```

### 13.2 Correct interactive behavior

When uncertain, the app may ask:

```text
Which box logic do you mean?

1. Routing Signal Scorer logic — RSS-0005
2. Prompt Library logic — PLIB-0005
3. Freeze workflow logic — FRZ-0005
4. Project-specific KANDA logic — PROJECT-KANDA-0005
5. Test-generation logic — TEST-0005
```

When user answers, the app attaches the selected code to the current routing context.

Important:

```text
Attach the code to the request envelope/routing context.
Do not blindly insert it into prompt text.
```

### 13.3 Manual code hint object

Recommended object:

```text
ManualClassificationHint:
- code: str
- resolved_internal_code: str
- source: user_disambiguation | explicit_user_code | app_suggested_clarification
- scope: current_request | current_thread | current_project
- status: active | removed | replaced | rejected
- removable: bool
- created_at: str
- superseded_by: str | None
- validation_status: pending | valid | invalid
```

### 13.4 Add/remove/replace commands

Supported user-friendly commands:

```text
add code RSS-0005
use code RSS-0005
remove code RSS-0005
clear code
undo code
show active code
replace code RSS-0005 with FRZ-0005
wrong code, use freeze logic
clear manual hint
```

### 13.5 Manual hint safety rule

Manual code can:

- Correct classification ambiguity.
- Reference a validated prompt card.
- Improve routing clarity.
- Reduce fuzzy classification reliance.
- Support project-specific prompts.

Manual code cannot:

- Override final route logic.
- Bypass validation.
- Bypass safety.
- Insert prompt text directly.
- Mutate router logic.
- Mutate prompt registry.
- Bypass freeze.
- Force a prompt when task fit fails.

---

## 14. Manual Code and Prompt Insertion

The user may enter a phrase such as:

```text
use box logic
```

The system may internally resolve it to:

```text
BOX-0005
```

The code may be inserted into the routing envelope in the current session/context.

This is useful because classification can be manually corrected when automatic routing is uncertain.

However:

```text
The code is a validated classification hint.
The code is not a final route command.
The code must be removable if incorrect.
The code must be auditable.
The code must be validated before use.
```

The system must support removal/replacement commands to correct mistakes.

---

## 15. Router Treatment of Manual Codes

The router should treat manual codes as:

```text
High-priority candidate hints
```

Not as:

```text
Final authority
```

Router flow:

```text
1. User request arrives.
2. Router attempts classification.
3. Router detects ambiguity or user provides a code/phrase.
4. Manual Prompt Code Resolver resolves candidate code.
5. Code validation runs.
6. Router considers linked prompt/card.
7. Governed routing rules select final route.
8. If code is wrong, inactive, superseded, or out of scope, reject/warn.
9. User can remove, replace, or clear code.
```

---

## 16. Prompt Test Battery

Before a new prompt is inserted into router logic, it must pass a test battery.

Canonical battery:

```text
1. Classification test
2. Duplicate/overlap test
3. Boundary test
4. Clarity/readability test
5. Injection-resistance test
6. Project-scope test
7. Code-binding test
8. Regression test
9. Router non-authority test
10. Freeze-readiness test
```

### 16.1 Classification test

Checks whether prompt belongs to intended box/project.

### 16.2 Duplicate/overlap test

Checks whether prompt duplicates or conflicts with existing prompts.

### 16.3 Boundary test

Checks whether prompt attempts to override router, freeze, prompt canon, or other boxes.

### 16.4 Clarity/readability test

Checks whether prompt is clear, specific, non-ambiguous, and maintainable.

### 16.5 Injection-resistance test

Checks whether user text can trick prompt into ignoring governance.

### 16.6 Project-scope test

Checks whether prompt is global, project-specific, temporary, or experimental.

### 16.7 Code-binding test

Checks whether code resolves only to this prompt and does not collide.

### 16.8 Regression test

Checks whether adding the prompt changes unrelated routing behavior.

### 16.9 Router non-authority test

Checks whether user can force routing by code alone.

Expected answer:

```text
No. Code must still validate task fit and safety.
```

### 16.10 Freeze-readiness test

Checks whether the prompt has:

- Title.
- ID.
- Scope.
- Tests.
- Protected paths.
- Validation evidence.
- Boundary summary.
- Freeze-ready summary.

---

## 17. Standards and Book-Derived Improvements Adopted

The following ideas were adopted as real gains.

### 17.1 From external AI/security standards review

Adopted:

- Threat-model document.
- Standards crosswalk.
- No free-text advisory explanation in Phase 1a.
- No rankings in Phase 1a.
- Egress/output firewall.
- Capability-denial tests.
- Route-invariance delta test.
- Explicit Phase 1a/Phase 1b gate.

### 17.2 From external architectural audits

Adopted:

- Phase 1a and Phase 1b split.
- Interface/stub first.
- Advisory-signal naming.
- No generic metadata dictionary.
- `advisory_should_abstain` instead of `must_not_route`.
- AST import-boundary tests.
- No runtime shadow mode yet.
- Prompt library/freeze memory/router canon never visible directly to ML.
- Immutable/frozen dataclasses.
- NullAdvisor and deterministic MockAdvisor.
- Route invariance with ML absent vs mock present.
- Treat ML output as telemetry only.

### 17.3 From book-based design pass

Adopted:

- Prompts are first-class software artifacts.
- Prompt Intake Pipeline before router binding.
- Prompt code is a reference, not a command.
- Prompt-output validation, not only ML-output validation.
- Strategy/Registry/Adapter/Null Object pattern.
- Project-specific prompt namespace.
- Prompt lifecycle states.
- Prompt battery regression before insertion.

---

## 18. Recommended Folder Concepts

The final implementation must inspect the real project before choosing exact paths, but the conceptual structure is:

```text
routing_signal_scorer/
    ml_advisory_signal/
        __init__.py
        contract.py
        advisor_interface.py
        null_advisor.py
        mock_advisor.py
        boundary_guard.py
        output_firewall.py
        phase1a_threat_model.md
        phase1a_boundary_contract.md
        phase1a_closure_audit.md

    governed_prompt_intake/
        prompt_intake_contract.md
        prompt_lifecycle.md
        prompt_registry_contract.md
        prompt_test_battery.md
        prompt_output_firewall.md

    manual_prompt_code_resolver/
        manual_code_hint_contract.md
        code_resolution_rules.md
        code_add_remove_replace_commands.md
```

Tests should live in the project’s existing test structure unless the project convention requires local tests.

---

## 19. Tests Required for Phase 1a

### 19.1 ML advisory tests

Required:

- AST import-boundary test.
- No forbidden import test.
- Contract schema test.
- Output firewall test.
- Forbidden field-name rejection test.
- Capability-denial test.
- No I/O test.
- No network test.
- No subprocess test.
- No mutation test.
- NullAdvisor test.
- MockAdvisor test.
- Advisory abstention test.
- Advisory non-authority test.
- Route-invariance test if a safe non-runtime route harness exists.

### 19.2 Prompt intake tests

Required:

- Prompt artifact schema test.
- Prompt lifecycle state test.
- Prompt code namespace test.
- Duplicate code rejection test.
- Invalid code rejection test.
- Prompt-output firewall test.
- Forbidden prompt instruction rejection test.
- Prompt test battery manifest test.
- Prompt freeze-readiness manifest test.

### 19.3 Manual code resolver tests

Required:

- User phrase to code candidate test.
- Ambiguous phrase requires clarification test.
- Add code test.
- Remove code test.
- Replace code test.
- Clear code test.
- Active code display test.
- Code validation test.
- Inactive/superseded code rejection test.
- Out-of-scope code rejection test.
- Wrong-code correction test.
- Code is not final authority test.

---

## 20. Performance and Reliability Rules

Phase 1a must be low overhead.

Rules:

- No heavy ML dependency.
- No provider SDK.
- No runtime model loading.
- No network.
- No vector store.
- No background worker.
- No asynchronous state.
- No persistence.
- No disk writes.
- Mock/Null advisor must be deterministic.
- Failure must degrade to no advisory signal.
- Advisory failure must not block routing.
- Prompt code resolver failure must degrade to normal governed classification.

---

## 21. Security Rules

### 21.1 Least privilege

Every new box must receive only the minimum data needed.

### 21.2 Defense in depth

Do not rely only on docs.

Every key boundary must be enforced by tests.

### 21.3 No hidden authority

No field, function, file, or code path should imply that ML or manual code selects final route.

### 21.4 No raw prompt transfer to ML

The ML advisory box must not receive raw prompt text or full prompt library data.

### 21.5 No prompt injection channel

Avoid free-text advisory explanations and generic metadata in Phase 1a.

### 21.6 No accidental dataset creation

Do not persist advisory inputs/outputs in Phase 1a.

---

## 22. Red Flags That Block Implementation

Block the patch if any of these appear:

- ML advisory imports router internals.
- ML advisory imports prompt library.
- ML advisory imports freeze memory.
- ML advisory imports provider SDKs.
- ML advisory imports embedding/vector libraries.
- ML advisory writes files.
- ML advisory persists logs/datasets.
- ML advisory returns `final_route`.
- ML advisory returns `selected_prompt`.
- ML advisory returns rankings in Phase 1a.
- Prompt Intake inserts prompt into router without full test battery.
- Manual code bypasses validation.
- Manual code cannot be removed.
- Manual code is inserted into prompt text instead of routing envelope.
- User-entered code is treated as final command.
- Any router branch says “if ML confidence > threshold, use ML choice.”
- Any router branch uses ML as tie-breaker.
- Any prompt says “always select this prompt.”
- Any prompt says “ignore governance.”
- Any future AI is asked to implement Phase 1b inside Phase 1a.

---

## 23. Canonical Do / Don’t

### Do

- Do keep ML advisory non-authoritative.
- Do keep Phase 1a contract/stub/test only.
- Do use frozen dataclasses.
- Do use reason-code enums.
- Do create output firewalls.
- Do create import-boundary tests.
- Do create capability-denial tests.
- Do preserve MLRT corpus.
- Do create Prompt Intake Gate for future prompts.
- Do support project-specific prompt namespaces.
- Do allow manual prompt-code hints for hard classifications.
- Do allow code add/remove/replace/clear commands.
- Do validate codes before use.
- Do freeze prompt additions after validation.

### Don’t

- Don’t call it router copilot in filenames.
- Don’t give ML route authority.
- Don’t use ML as tie-breaker.
- Don’t use advisory rankings in Phase 1a.
- Don’t use free-text ML explanations in Phase 1a.
- Don’t pass raw prompts to ML advisory.
- Don’t use generic metadata dictionaries.
- Don’t let ML write prompts.
- Don’t let ML register prompts.
- Don’t let a manual code bypass router.
- Don’t insert manual code directly into prompt text.
- Don’t mutate prompt library without Prompt Intake Gate.
- Don’t add provider calls, embeddings, vector stores, or persistence in Phase 1a.
- Don’t create MLRT-113 as continuation of the closed MLRT wave.

---

## 24. Final Updated Logic Flux

```text
A. User request enters system.

B. Governed router attempts normal classification.

C. If ambiguity exists or user asks "use box logic":
   - Interactive Manual Prompt Code Resolver may ask clarification.
   - User selection becomes a manual classification hint.
   - App attaches validated code to routing envelope, not prompt text.

D. If ML Advisory Signal exists:
   - It may produce non-authoritative flags/reason codes.
   - It may abstain.
   - It may flag possible prompt gap.
   - It cannot create prompts.
   - It cannot select route.

E. If prompt gap is detected:
   - New prompt must enter Governed Prompt Intake Gate.
   - Prompt is classified, edited, tested, coded, validated, and frozen.
   - Only then can router consider it.

F. Router validates all inputs:
   - user request
   - manual code hint
   - prompt registry entry
   - task fit
   - scope
   - active/frozen status
   - boundary rules

G. Governed router selects final route.

H. No ML advisory signal or manual code is final authority.

I. If code was wrong:
   - user can remove, replace, clear, or undo code.
   - router returns to normal classification.

J. Phase 1a ends only after boundary contract, tests, and closure doc are validated and frozen.
```

---

## 25. Phase 1a Stopping Criteria

Phase 1a is complete only when:

- Boundary canon is written.
- Threat model is written.
- Standards/book-derived gains are recorded.
- ML advisory subbox skeleton exists.
- Contracts are typed/frozen.
- NullAdvisor exists.
- Deterministic MockAdvisor exists.
- Output firewall exists.
- Prompt Intake Gate boundary is documented.
- Manual Prompt Code Hint Gate is documented.
- Add/remove/replace/clear semantics are documented/tested.
- All boundary tests pass.
- No real ML exists.
- No runtime shadow mode exists.
- No prompt insertion occurs.
- No router authority is delegated.
- Freeze entry records Phase 1a as contract-only / stub-only / non-authoritative.

---

## 26. One-Sentence Canon

```text
ML Advisory Signal may help notice ambiguity or prompt gaps, Governed Prompt Intake may safely create and test future prompts, and Manual Prompt Code Hints may guide difficult classification, but only the Governed Router may make the final route decision after validation.
```
