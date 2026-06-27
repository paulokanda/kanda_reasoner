# handoff_at_end_of_work.md

Version: 1.0
Status: always-startup session-closure guardrail
Role: force a complete contextualized handoff when project work is paused or ended
Scope: end-of-work handoff behavior for long governed KANDA sessions
Do not use as: implementation prompt, patch prompt, freeze entry, or replacement for validation evidence

## Purpose

This prompt prevents loss of project context when a long governed work session pauses or ends.

When the user indicates that the work session is ending, pausing, or taking a break, the AI must not answer with only a short farewell.

Instead, it must create a complete contextualized handoff so the next AI chat can resume safely without guessing what was done, what was validated, what was frozen, and what remains next.

## Trigger phrases

Treat these user phrases, and close variants, as end-of-work handoff triggers when project work is active:

```text
lets take a break
let's take a break
lets stop now
let's stop now
pause here
pause this work
stop for today
finish this section
end of day
wrap this up
create handoff
handoff for next time
we continue later
we will continue later
chat is huge
```

A trigger can be written with different capitalization or minor punctuation.

If the user clearly asks only a casual non-project goodbye and no project work is active, a short response is acceptable.

If project work is active, treat the trigger as a session-closure workflow.

## Mandatory behavior

When an end-of-work handoff trigger is detected during active project work, the AI must:

```text
1. Stop normal implementation flow.
2. Do not create new code, patches, tests, or freezes unless the user explicitly asks before the break.
3. Produce a complete contextualized handoff for the next AI.
4. Include what was completed, validated, frozen, discussed, and not started.
5. Include exact next safe action.
6. Include warnings about what must not be modified or assumed.
7. Make the handoff self-contained enough that a new AI can continue without reading the whole chat.
```

## Required handoff content

The handoff must include these sections when known:

```text
1. Project name.
2. Project root.
3. Active workspace paths and boxes.
4. Current task family or workflow.
5. Completed work in this session.
6. Installed patches and patch names.
7. Validation evidence already provided.
8. Freeze entries installed or planned.
9. Current generated artifact names.
10. Stale or forbidden names that must not be revived.
11. Files changed.
12. Files that must not be modified next.
13. Current decision state.
14. Work discussed but not implemented.
15. Next safe action.
16. Explicit do-not-do list for the next AI.
17. Any open questions or risks.
```

Use only facts available in the current conversation, uploaded files, validation logs, or frozen memory.

Do not invent validation evidence.

If validation status is unknown, say that it is unknown.

If a patch was prepared but not installed or not validated, say that clearly.

## Required style

The handoff should be direct, concrete, and operational.

Prefer exact paths and filenames.

Use Windows paths when the project uses Windows paths.

Use project terminology already established by the user.

Do not use vague summaries such as:

```text
We worked on the project and should continue next time.
```

Instead, write concrete continuation instructions.

## Handoff template

Use this structure unless a better project-specific structure is required:

```text
KANDA PROJECT HANDOFF - END OF WORK SESSION

Session status:
[paused / stopped / end of day]

Project:
[project name]

Project root:
[path]

Important boxes:
1. [box] - [role]
2. [box] - [role]

Completed in this session:
- ...

Installed patches:
- [patch name] - [status]

Validation evidence:
- ...

Frozen behavior / freeze entries:
- ...

Current active names:
- ...

Stale or forbidden names:
- ...

Files changed:
- ...

Files not to modify next:
- ...

Discussed but not implemented:
- ...

Next safe action:
[one concrete next step]

Do not do next:
- ...

Risks / open questions:
- ...

End of handoff.
```

## Interaction with freeze workflow

If a validated feature was completed but not frozen, say:

```text
Feature appears validation-ready but is not frozen yet.
Next safe action: prepare Freeze Feature After Update entry under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory after confirming validation evidence.
```

If a feature was frozen and validation passed, say:

```text
Feature is frozen and validation evidence was accepted.
Do not refreeze unless the user explicitly requests a new freeze for new behavior.
```

## Interaction with startup delivery workflow

If the session changed startup delivery, include current startup delivery names and stale names.

Current normal startup delivery names must be reported exactly when relevant:

```text
tell_AI_read_before_all.md
first_prompts_to_ai.zip
prompt_library.zip
```

The maintenance file must be reported when relevant:

```text
zz_read_only_if_modifying_startup_delivery.md
```

Do not treat old startup paste filenames as active current files.

## Final rule

When project work is active and the user says to take a break, stop, pause, or continue later, a complete contextualized handoff is mandatory.

A short goodbye alone is a failure of this prompt.

## Freeze-intake metadata in handoffs

When ending or pausing governed implementation work that produced an installed or validated patch, include a short freeze-intake metadata block in the handoff.

This block helps the next AI chat and the KANDA Reasoner app avoid guessing the wrong feature during New Local Freeze Entry.

Required fields in the handoff block:

- latest_patch_name
- feature_title
- feature_id, if available
- primary_box
- box_type
- installed_payload_files
- generated_files
- protected_paths
- validation_evidence_available
- validation_evidence_summary
- freeze_status: not_frozen / freeze_ready / frozen
- next_freeze_action

Do not invent validation. If validation has not yet passed, mark `validation_evidence_available` as false and state what validation is still missing.

Do not reuse the validation list of an older feature merely because the local freeze form heuristic selected it. The handoff must identify the feature that was actually implemented in the current work segment.

If a patch ZIP was delivered, state whether it contains `KANDA_FREEZE_HINT.json` and whether the sidecar is only delivery metadata or also an installed file.

