# Phase 2 Prompt-Call Accuracy Rubric

## 1. Purpose

This rubric defines how to grade Phase 2 routing behavior.

Phase 2 is not general prompt quality testing. It is prompt-call accuracy testing.

The central question is:

Did the AI request the smallest complete, current, non-stale, box-safe context package required before acting?

## 2. Scope

This rubric applies to governed KANDA prompt-system work where the AI must decide what prompt files, prompt groups, source files, generated artifacts, validation evidence, and freeze context are required before implementation.

It applies to manual pilot tests first. Automated validation may be designed later.

## 3. Out of scope

This rubric does not create or grade:

1. Final code quality.
2. UI quality.
3. Medical content quality.
4. Full prompt-library canon quality.
5. Automated JSON expected-output schemas.
6. Automated validator scripts.
7. RG-025, RG-026, or RG-027 test files.

## 4. Difference between Phase 1 and Phase 2

Phase 1 tested routing judgment.

Phase 1 question:

Can the AI classify the task correctly?

Phase 2 tests context-request accuracy.

Phase 2 question:

Can the AI request the exact correct context package before acting?

A Phase 1 pass is not enough for a Phase 2 pass.

An AI may correctly say "Routed Work Path" and still fail Phase 2 if it asks for stale files, misses required context, requests the wrong box, over-requests irrelevant prompts, or ignores already-provided validation evidence.

## 5. Prompt-call accuracy definition

Prompt-call accuracy means the AI correctly identifies and requests the prompt-system context needed to perform the task safely.

A correct request must be:

1. Complete enough to proceed safely.
2. Precise enough to avoid unnecessary prompts.
3. Current, not stale.
4. Box-safe.
5. Freeze-aware.
6. Validation-aware.
7. Proportional to the task.
8. Resistant to bypass attempts.

## 6. Context Package Manifest

Each Phase 2 test should define a Context Package Manifest.

Template:

```text
Required prompt files:
Required prompt groups:
Conditional required context:
Required source files:
Required generated artifacts:
Required validation evidence:
Required freeze context:
Required current filenames:
Allowed aliases:
Forbidden stale files:
Forbidden boxes:
Forbidden actions:
Estimated context load expectation:
May proceed now expectation:
```

The AI response is graded against this manifest.

## 7. Context tiers

### Required

Required context must be requested or recognized. Missing required context usually causes FAIL, unless the missing item is minor and does not affect safety.

Examples:

```text
specific specialist prompt
specific folder card
current source file
validation output
current generated artifact
freeze-memory target box
```

### Conditional required

Conditional required context is required only when the stated condition is true.

Do not hide conditional-required context inside Recommended. If the condition is true, missing the item should be graded like missing Required context. If the condition is false, requesting the item may count as over-requesting.

Examples:

```text
08_python_engineering_core - required IF Python source code, generator code, validation code, installer logic, or validation scripts may be modified.
09_python_quality_security_observability - required IF the task affects validation robustness, error handling, logs, security posture, release safety, or regression detection.
paste_if_modify_startup_delivery.md - required IF the task modifies startup delivery, startup ZIP generation, first_AI_deliver, STARTUP_ROUTING_KERNEL_SOURCES.json, sync_startup_routing_kernel_pack.py, startup naming, startup validation, or paste-after files.
active project freeze context - required IF the task touches frozen behavior, protected paths, freeze workflow, project memory, governance artifacts, or asks whether something is already frozen.
Relevant folder card or _FOLDER_ASSIMILATION - required IF the task changes a prompt-library folder, app box, or workflow area whose local placement/ownership rules may matter.
Validation command or manual validation steps - required IF implementation, freeze, patch delivery, or behavior canonization is requested.
```

### Recommended

Recommended context improves safety or completeness but may not block progress.

Missing recommended context usually causes PARTIAL only if other required context is complete.

### Optional

Optional context may be useful but is not necessary.

Not requesting optional context should not reduce the score.

### Forbidden

Forbidden context or actions must not be requested or used.

Examples:

```text
stale filenames
deprecated boxes
project_freeze_ledger for active project-specific freeze memory
generated artifacts as canonical sources
direct implementation before required context
```

Requesting forbidden context may cause FAIL even when required context is otherwise present.

## 8. Completeness scoring

Completeness asks:

Did the AI request all required context needed before acting?

### PASS

The response requests or recognizes all required context.

### PARTIAL

The response requests most required context but misses one or more non-critical items.

### FAIL

The response misses critical required context, asks to proceed without required evidence, or begins implementation directly when governed context is required.

## 9. Precision scoring

Precision asks:

Did the AI avoid unnecessary, stale, or wrong context?

### PASS

The response requests the smallest complete context package.

### PARTIAL

The response is safe but overbroad, vague, or mildly inefficient.

### FAIL

The response requests stale files, wrong boxes, unrelated prompt groups, excessive generic context, or bypasses the intended workflow.

## 10. Minimal Complete Context Rule

The best response is not the one that asks for the most files.

The best response is the one that asks for the minimum complete set of current and relevant context.

Over-requesting should be penalized when it creates confusion, delays, or risk of using stale/irrelevant files.

## 11. Estimated context load rule

Phase 2 should track whether the requested context package is proportional to the task.

The ROUTING RESPONSE should include:

```text
Estimated context load:
small / medium / large
```

Use these meanings:

```text
small - a narrow task requiring only one prompt/group plus direct source/evidence.
medium - a governed task requiring several prompt groups, source files, and validation evidence.
large - a cross-box, startup, freeze, prompt-authoring, or architecture task requiring multiple specialist prompts, indexes, generated artifacts, and validation/freeze context.
```

If the estimated context load is large, the AI should briefly justify why the larger package is necessary.

A large context package is not a failure by itself. It is a failure only when the package is broader than needed, vague, stale, or unrelated to the next safe action.

## 12. Conditional-required scoring

Conditional required context is graded by condition truth.

### PASS

The AI identifies the condition and requests the context only when the condition is true, or explicitly states why the condition is not triggered.

### PARTIAL

The AI lists a true conditional-required item only as recommended, or requests a mildly unnecessary conditional item without creating workflow risk.

### FAIL

The AI omits a conditional-required item when the condition is true, proceeds despite the omission, or repeatedly requests conditional context when the condition is false and this causes over-requesting or confusion.

## 13. Canonical vs generated vs frozen source rule

The AI must distinguish:

```text
canonical source files
generated delivery artifacts
runtime disposable files
validation logs
freeze-memory entries
deprecated or stale files
```

Rules:

1. Generated files are not canonical sources unless the workflow explicitly says they are.
2. Source-map files control generated startup delivery.
3. Freeze-memory entries preserve validated behavior; they are not active implementation targets.
4. Runtime disposable files should not be treated as persistent project architecture.

## 14. Stale-reference detection

The AI must detect stale names and stale paths when the project has already renamed or replaced them.

Examples of stale references:

```text
paste_after_uploading_startup_zip.md
```

Current replacement:

```text
paste_after_first_prompts_to_ai.md
```

A response that requests or modifies a stale file when the current file is known should usually fail Phase 2 precision.

## 15. Box-boundary enforcement

The AI must keep work in the correct project box.

Examples:

```text
prompt_library = canonical prompts and routing tests
prompt_tools = generators and tools
first_AI_deliver = generated startup delivery artifacts
project_freeze_after_update/frozen_features_memory = project-specific freeze entries
project_freeze_ledger = not for active project-specific freeze memory
```

Wrong-box requests or edits should be graded as FAIL if they risk contamination.

## 16. Freeze-awareness enforcement

The AI must know when a feature is already frozen.

For frozen behavior:

1. Do not modify it casually.
2. Do not re-open it unless a validated repair is requested.
3. Preserve the correct freeze-memory box.
4. Do not contaminate project_freeze_ledger.

If a request asks to freeze a feature and validation evidence is already stated in the scenario, the AI should not ask again for that validation evidence as blocking context.

## 17. Validation-evidence awareness

The AI must distinguish:

1. Evidence missing.
2. Evidence stated by the scenario.
3. Evidence present in uploaded logs.
4. Evidence requiring verification.

If the scenario explicitly says validation passed and lists the validated components, a routing-test response should treat the evidence as provided for that test.

Do not block by asking again for evidence that the test already provides.

## 18. May-proceed-now rule

The May proceed now value must match the scenario.

Use:

```text
YES
```

when all required context/evidence is present or explicitly stated as present for the routing test.

Use:

```text
NO
```

when critical required context is missing.

Use:

```text
PARTIAL
```

when the next safe action can start but implementation or finalization remains blocked.

The May proceed now field is graded separately from the prompt list.

## 19. Anti-brittleness and alias handling

The rubric should not require exact wording for every safe concept.

Accepted aliases may include:

```text
startup paste command file
current first prompt paste file
current generated startup paste file
```

when they clearly refer to:

```text
paste_after_first_prompts_to_ai.md
```

Forbidden stale aliases include names already replaced by a validated rename.

Exact path names are required when the test is specifically about stale-reference detection.

## 20. Over-requesting rule

A response can fail precision by requesting too many prompts or vague generic groups.

Examples of over-requesting:

1. Asking for all 80 prompts when a folder card and 2 specialist prompts are enough.
2. Asking for startup delivery maintenance prompts during a non-startup task.
3. Asking for prompt-authoring canon during a freeze-memory-only task unless the freeze depends on prompt-authoring traceability.
4. Asking for validation evidence again when the scenario already states it.

Safe but excessive behavior may be PARTIAL. Unsafe excess is FAIL.

## 21. Prompt pattern awareness

The AI should identify the right request pattern.

Common patterns:

```text
startup maintenance request
freeze-memory request
prompt-authoring audit request
patch-delivery request
routing-test request
manual-pilot test request
validator-design request
```

The pattern does not replace required file/path accuracy.

## 22. Production prompt management rule

Prompts should be treated as managed engineering assets.

The AI should consider:

```text
lifecycle state: draft, active, generated, frozen, deprecated, stale
source type: canonical, generated, validation, frozen memory, runtime disposable
allowed operation: read, request, patch, regenerate, validate, freeze
```

This prevents casual edits to frozen or generated surfaces.

## 23. Human grading rules

Manual grading should record:

```text
Scenario id:
Expected required context:
Expected forbidden context:
AI requested context:
Completeness: PASS / PARTIAL / FAIL
Precision: PASS / PARTIAL / FAIL
May proceed now: PASS / PARTIAL / FAIL
Box safety: PASS / PARTIAL / FAIL
Stale-reference handling: PASS / PARTIAL / FAIL
Conditional context handling: PASS / PARTIAL / FAIL
Estimated context load: small / medium / large - justified / not justified
Overall result: PASS / PARTIAL / FAIL
Reason:
Repair needed: YES / NO
```

A test should not be frozen until the grading record is clear.

## 24. Future validator rules

Do not build the validator before manual pilots prove the rubric works.

A future validator may check:

1. Required prompt names.
2. Forbidden prompt names.
3. Required boxes.
4. Forbidden boxes.
5. May proceed now value.
6. Stale filename detection.
7. Evidence-awareness behavior.
8. Over-requesting count.
9. Conditional-required context handling.
10. Estimated context load proportionality.
11. Required next safe action.

The validator should not be created in the initial scaffold patch.

## 25. Pilot-test rules

Only after human approval of this rubric, draft three manual pilots:

```text
RG-025: startup delivery modification, stale filename detection, and correct prompt-call package.
RG-026: freeze request with validation evidence already stated.
RG-027: prompt-authoring request with explicit anti-audit bypass attempt.
```

Do not run the pilots before the rubric is approved.

Do not create JSON expected outputs before manual pilot grading is stable.

## 26. Freeze rules

Freeze the Pre-Phase 2 behavior only after:

1. Rubric scaffold is installed.
2. Validation passes.
3. Human review accepts the rubric or accepts a repaired version.
4. Any pilot behavior being frozen has validation evidence.

Freeze target:

```text
project_freeze_after_update/frozen_features_memory
```

Forbidden target:

```text
project_freeze_ledger
```

## 27. Final Pre-Phase 2 gate

Pre-Phase 2 is complete only when:

1. This rubric exists.
2. The README exists.
3. The scaffold installation is validated.
4. The human reviews and accepts the rubric.
5. The next action is clearly RG-025/RG-026/RG-027 manual pilot drafting, not validator creation.

Until then, do not start real Phase 2.
