# Phase 2 Prompt-Call Accuracy Readiness

## Status

This folder is a Pre-Phase 2 readiness scaffold.

It is not a Phase 2 test suite yet.
It is not an automated validator.
It is not a JSON expected-output schema.
It does not contain RG-025, RG-026, or RG-027.

## Purpose

Phase 2 will test prompt-call accuracy.

Phase 1 asked whether the AI could classify a task correctly.

Phase 2 asks whether the AI can request the smallest complete, current, non-stale, box-safe context package before acting.

## Safe scope for this scaffold

This scaffold may define:

1. The rubric for prompt-call accuracy.
2. Human grading rules.
3. Future pilot-test rules.
4. Future validator requirements.

This scaffold must not define or execute:

1. RG-025, RG-026, or RG-027.
2. Automated validator code.
3. JSON expected-output schema.
4. Startup delivery changes.
5. Source-map changes.
6. Freeze-memory changes.
7. Changes to frozen tools.

## Folder contract

This folder is isolated from Phase 1 routing tests.

Canonical folder:

```text
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/
```

Expected files in this scaffold:

```text
README.md
phase2_prompt_call_rubric.md
```

## Relationship to future Phase 2 work

This scaffold must be reviewed by a human before any Phase 2 pilot tests are created.

Future sequence:

1. Review this rubric.
2. Repair the rubric if needed.
3. Approve the rubric as the Phase 2 contract.
4. Draft only three manual pilot tests:
   - RG-025: startup delivery modification and stale filename detection.
   - RG-026: freeze request where validation evidence is already stated.
   - RG-027: prompt-authoring anti-audit bypass request.
5. Run pilots manually.
6. Repair prompt logic only if pilots expose real weaknesses.
7. Freeze the approved behavior only after validation evidence.
8. Consider JSON schema and automated validator later.

## Hard boundaries

Do not modify these files or areas as part of the initial scaffold:

```text
kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py
kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py
kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json
kanda_prompt_workspace/first_prompt_files/
kanda_prompt_workspace/prompt_library/ROUTING_TESTS/context_routing_expected_outputs.json
project_freeze_after_update/frozen_features_memory/existing entries
project_freeze_ledger
```

## Review checklist

Before moving from Pre-Phase 2 into real Phase 2, confirm:

1. The rubric distinguishes Phase 1 from Phase 2.
2. The rubric can grade completeness and precision separately.
3. The rubric catches stale references.
4. The rubric enforces correct project boxes.
5. The rubric prevents over-requesting.
6. The rubric handles already-provided validation evidence correctly.
7. The rubric allows aliases only when they are safe and current.
8. The rubric forbids stale filenames and frozen/deprecated boxes.
9. The rubric is human-gradable before automation.
10. The rubric does not require a validator yet.

## Current next action after installing this scaffold

Human review.

Do not start RG-025 until the rubric is approved.
