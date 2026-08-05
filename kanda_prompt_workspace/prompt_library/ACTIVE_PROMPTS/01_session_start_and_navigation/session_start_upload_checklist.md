---
prompt_id: session_start_upload_checklist
prompt_code: KPR-01-002
title: Session Start Upload Checklist
version: 2.1
status: active
load_type: always_startup
owner_box: 01_session_start_and_navigation
source_stage: project-ready-check-active-project-display-v1
---

# Session Start Upload Checklist

## Mission

Own the human-facing two-stage upload sequence for a KANDA session.

This checklist determines whether the startup and Project handoff inputs are present. It does not authorize coding, reconstruct missing source, validate local execution, or replace Brick Wall.

## Stage 1 - startup delivery

Required normal startup inputs:

1. `tell_AI_read_before_all.md` - read first.
2. `first_prompts_to_ai.zip` - open `00_START_HERE_FOR_AI.md` first, then the numbered members in source-map order.
3. `prompt_library.zip` - keep available; open only exact selected prompt paths.

Conditional input:

- `zz_read_only_if_modifying_startup_delivery.md` - read only when the task changes startup delivery, its source map, generator, names, content, or validation.

Do not require retired prompts, loose generated numbered files, old paste filenames, deprecated startup canons, or the whole Prompt Library.

After Stage 1, return only the governed `STARTUP PACK LOAD CHECK`, confirm the required members loaded, and wait for the second upload group.

## Stage 2 - selected Project handoff

Read in this order:

1. `_RUN_COLLECTOR_STATUS.txt`, when present.
2. `<project_slug>__ai_handoff_upload_readme.txt`.
3. Compact Error Memory files:
   - `<project_slug>__error_memory_ai_prompt.md`;
   - `<project_slug>__error_lessons_compact.json`;
   - `<project_slug>__error_memory_manifest.json`.
4. `<project_slug>__ai_handoff_upload*.zip` in numeric order.
5. Inside the handoff ZIP: `UPLOAD_README.txt`, AI briefing, routing manifest, bundle manifest, patch-safety routes, file manifest, source-archive manifest, validation state, and compact Error Memory.
6. Full Error Memory ZIP only when the compact memory, repeated-error debugging, an audit request, insufficiency, or a conflict requires it.
7. Source archive parts only when exact source inspection or reconstruction is required.
8. PNG asset parts only when exact reconstruction requires those assets.
9. All-in-one handoff only as fallback when the primary handoff ZIP is unavailable.

Generated source archives and handoffs are evidence, not canonical source authority.

## Stage 2 readiness response

After the required second-upload files are loaded, return:

`PROJECT READY CHECK`

Include:

- Project slug;
- Active Project root;
- KANDA Tool root;
- whether they are the same physical root;
- compact Error Memory status;
- second-upload handoff status;
- Tier-1 gate status;
- next action;
- active Project display name immediately before the ready token.

Use this exact tail:

```text
Next action:
PROJECT IN USE: <ACTIVE PROJECT DISPLAY NAME>
WAIT_FOR_TASK
```

Derive `<ACTIVE PROJECT DISPLAY NAME>` from the selected active Project name or
slug, not from the KANDA Tool name. Replace underscores with spaces and convert
the result to uppercase. For example, `my_project` becomes `MY PROJECT`.
`KANDA REASONER` is valid only when KANDA Reasoner itself is the selected active
Project.

End with `WAIT_FOR_TASK` only when the required handoff is complete, and only
after the `PROJECT IN USE:` line.

## Hard blockers

Do not accept the real Project task before Stage 2 readiness.
Do not claim local validation from generated handoff evidence.
Do not infer missing source, hashes, freeze entries, Error Memory, or validation markers.
Do not ask for a prompt that already exists at a selected exact path in `prompt_library.zip`.
Do not open the entire Prompt Library when one addressed prompt is sufficient.

## Authority boundary

This checklist may classify files as required, conditional, missing, stale, or not applicable. It cannot mutate source, install a patch, validate locally, write Error Memory, write Freeze Memory, or grant implementation authority.
