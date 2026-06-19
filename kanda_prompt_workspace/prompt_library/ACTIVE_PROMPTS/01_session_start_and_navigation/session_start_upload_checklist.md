# Session Start Upload Checklist

Version: 1.1
Status: Human-facing operational checklist / prompt-library support asset
Source generalized from: PyKANDA daily upload checklist v1.2
Project: KANDA Reasoner / project-agnostic PyArchitect workflow

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.

## Purpose

Use this checklist at the start of a KANDA Reasoner or PyArchitect engineering session so the AI receives the correct operating context before proposing code, patch bundles, prompt updates, or governance changes.

This is not itself an implementation prompt. It is a human upload checklist that tells the user which context files, evidence, logs, and task materials should be sent before work begins.

## Core rule

Do not let the AI work from memory alone. The session should begin from current evidence, current governance, current task context, and latest validation state.

## Startup kernel staleness check

The startup kernel can become stale relative to active project freeze memory.
At session start, compare the startup delivery generation time, when available from `STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json`, with the newest active project freeze entry summarized in `09_active_project_freeze_context.md`.

If active project freeze memory contains entries newer than the startup kernel generation time, flag:

```text
STARTUP_KERNEL_STALENESS_REVIEW
```

This warning does not automatically fail startup and does not authorize automatic repair.
It means the AI should avoid relying on stale startup assumptions and should request startup regeneration, active freeze context refresh, or `paste_if_modify_startup_delivery.md` before modifying startup delivery, source maps, freeze-context generation, or governed routing behavior.

Do not inject full freeze memory into the normal startup. Keep compact startup freeze context plus on-demand full freeze review.

## Send every start of chat

1. Current prompt stack load order or prompt navigation index.
2. Current universal delivery protocol.
3. Current project startup canon.
4. Current daily startup loader.
5. Current active governance files or active governance ZIP.
6. Latest active workflow handoff or session handoff.
7. Current task description.
8. Relevant source ZIP, prompt ZIP, logs, validation output, screenshots, traceback, or observed behavior.
9. Current project root and active product root, if they matter for the task.
10. Current validation baseline, including architecture validation and workflow validation if available.

## Send only when needed

### High-risk engineering work

Send the professional engineering governance layer when the task involves:

- runtime behavior
- GUI lifecycle
- local model / AI routing
- schema changes
- persistence
- multi-box behavior
- public API changes
- generated evidence changes
- validator changes
- workflow gates

### Governance freeze

Send the end-of-chat or active governance update protocol only after validation is clean and the user explicitly wants a freeze/canon update.

### Large module or helper split

Send the large-module refactor protocol when the user says things like:

- module is too big
- split this file
- extract helper
- reduce mixed responsibility
- preserve public API while refactoring

### Handoff or break in work

Send the current workflow handoff template when the user says things like:

- create a handoff
- next AI should know
- continue next time
- summarize where we are

### Many warnings/errors

Send the problem-set roadmap solver when the task is to order many failures, warnings, or validation issues.

### Architecture hardening

Send the architecture hardening triage protocol when the task involves ownership, boundary violations, stale variants, import heaviness, public API instability, or mixed responsibility.

### Uploaded reports, chunks, or merged evidence

Send the canonical reader / merger protocol when the task involves reading many uploaded chunks, evidence reports, split JSON exports, or generated project analysis files.

### Cross-box or multi-tab work

Send the tab/box boundary protocol when the task touches more than one tab, package, workflow, or responsibility box.

## Required AI behavior after upload

After the files are uploaded, the AI should confirm:

1. Which evidence files were received.
2. Which files are source truth, governance truth, generated evidence, or reference-only.
3. What the active box is.
4. What is explicitly out of scope.
5. Whether the task is audit-only, roadmap-only, implementation, freeze, or handoff.
6. Which validation gates would be required before freeze.

## Main reminder for the user

If the AI starts proposing code before declaring the active box, stop it and say:

> Declare the active KANDA box before patching.

If the AI proposes a large patch touching unrelated systems, stop it and say:

> One problem, one patch, one owner box.

If the AI claims success without local validation, stop it and say:

> Local validation is the source of truth. Do not freeze yet.

## What was generalized from the source file

The source PyKANDA checklist was project-specific, with PyKANDA names, root paths, and file names. This generalized version preserves the workflow logic but removes project-specific root assumptions and makes the checklist reusable for KANDA Reasoner and future PyArchitect projects.
## AI Prompt Request Canon Requirement

At the start of the session and before any non-trivial project action, load or enforce i_prompt_request_canon.

The AI must classify the user's request and, when the needed prompt stack or project evidence is missing, ask the human for the correct prompts/files before implementation, refactor, prompt-library modification, architecture change, database/storage work, validation, freeze, or handoff.

For example, if the human says "we will start creating a new folder with a databank," the AI must recognize a new architecture/data-storage task and request the relevant prompt stack: session start, AI prompt request canon, Box Logic, folder organization, database design, validation/type safety, security, implementation roadmap, and bundle-gated workflow.

