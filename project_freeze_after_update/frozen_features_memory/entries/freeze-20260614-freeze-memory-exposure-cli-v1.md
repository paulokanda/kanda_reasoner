---
freeze_id: "freeze-20260614-freeze-memory-exposure-cli-v1"
box: "project_freeze_ledger/freeze_memory_dynamic_exposure_bridge"
status: "frozen"
date: "2026-06-14"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260614-freeze-memory-exposure-cli-v1.md"
protected_paths:
  - "project_freeze_ledger/freeze_tools/expose_freeze_memory.py"
  - "project_freeze_after_update/frozen_features_memory/freeze_index.json"
  - "project_freeze_after_update/frozen_features_memory/project_frozen_implemented_steps.md"
  - "project_freeze_after_update/frozen_features_memory/entries/freeze-20260614-freeze-memory-exposure-cli-v1.md"
do_not_touch_summary:
  - "Keep expose_freeze_memory.py as a CLI-only read-only freeze-memory exposure tool in v1."
  - "Require explicit --project-root; do not silently default to current working directory or KANDA root."
  - "Read active project freeze memory only from <project_root>/project_freeze_after_update/frozen_features_memory."
  - "Do not write, repair, regenerate, or mutate freeze_index.json, freeze entries, or files_to_send_ai in v1."
  - "Do not store active project-specific freeze memory in project_freeze_ledger."
  - "Detect stale AI-send exposure artifacts, index/file mismatch, corrupt index, missing freeze memory, and external project contamination risk."
  - "Keep GUI, startup integration, app contract integration, ZIP/context publishing, and automatic index repair out of v1."
superseded_by: null
---
# freeze-20260614-freeze-memory-exposure-cli-v1

## freeze identity

Freeze ID:

```text
freeze-20260614-freeze-memory-exposure-cli-v1
```

Date:

```text
2026-06-14
```

Project box:

```text
project_freeze_ledger/freeze_memory_dynamic_exposure_bridge
```

Freeze tier:

```text
tier 1: freeze-memory exposure / box-safety governance freeze
```

Status:

```text
frozen after install validation, sandbox validation, real-project smoke validation, and user acceptance
```

Human approval:

```text
accepted by user after freeze_memory_exposure_cli_v1 local validation output showed VALIDATION OK and expected STALE_EXPOSURE diagnostic
```

## frozen version

```text
freeze_memory_exposure_cli_v1
```

## summary

This freeze locks the validated v1 command-line freeze-memory exposure tool:

```text
project_freeze_ledger/freeze_tools/expose_freeze_memory.py
```

The tool solves the first part of the marooned-freeze-memory problem by allowing the user or AI workflow to expose the selected active project's frozen memory on demand, without moving project-specific state into the reusable freeze engine box.

It preserves the canonical project-specific freeze architecture:

```text
project_freeze_ledger
= reusable freeze engine / blueprint logic

<active_project_root>/project_freeze_after_update/frozen_features_memory
= active frozen memory for the selected project only
```

## what was implemented

```text
1. A new CLI tool under project_freeze_ledger/freeze_tools/expose_freeze_memory.py.
2. Explicit --project-root requirement.
3. Compact text output for AI-readable freeze memory exposure.
4. JSON output option for machine-readable status.
5. Read-only exposure behavior by default and in v1 overall.
6. Freeze-memory status detection.
7. Stale files_to_send_ai artifact detection.
8. Missing freeze memory detection.
9. Missing/corrupt freeze_index.json detection.
10. Index/file mismatch detection.
11. External project project_freeze_ledger contamination-risk detection.
12. KANDA-self exception warning when the selected project root is the KANDA Reasoner engine root.
13. Compact listing of freeze IDs, protected paths, do-not-regress rules, and AI operating instructions.
```

## validated behavior

The user-provided validation output confirmed:

```text
REAL PROJECT STATUS: FREEZE_MEMORY_STATUS: STALE_EXPOSURE
VALIDATION OK: freeze_memory_exposure_cli_v1
VALIDATION OK
```

The real project exposure output confirmed:

```text
FREEZE_MEMORY_STATUS: STALE_EXPOSURE
Index entries: 15
Entry files: 15
Active/non-superseded entries: 14
```

This status is expected and is not a tool failure. It means the active freeze memory source is newer than the old generated AI-send ZIP artifact.

The validation also confirmed the tool reports:

```text
CANONICAL RULE: project_freeze_ledger is reusable freeze engine logic; active freeze memory belongs only to the selected project's project_freeze_after_update/frozen_features_memory.
READ_ONLY_EXPOSURE: this report did not repair, regenerate, or mutate freeze_index.json, freeze entries, or files_to_send_ai.
```

## protected files

The primary protected implementation file is:

```text
project_freeze_ledger/freeze_tools/expose_freeze_memory.py
```

The freeze memory files updated by this freeze entry are:

```text
project_freeze_after_update/frozen_features_memory/freeze_index.json
project_freeze_after_update/frozen_features_memory/project_frozen_implemented_steps.md
project_freeze_after_update/frozen_features_memory/entries/freeze-20260614-freeze-memory-exposure-cli-v1.md
```

## do-not-regress rules

```text
1. Keep expose_freeze_memory.py CLI-only for v1.
2. Keep the tool read-only with respect to frozen_features_memory and files_to_send_ai.
3. Require explicit --project-root.
4. Do not add a default current-working-directory project root.
5. Do not write active project-specific memory to project_freeze_ledger.
6. Do not create project_freeze_ledger inside external projects.
7. Do not repair or regenerate freeze_index.json in this exposure tool.
8. Do not add GUI integration to v1.
9. Do not add startup prompt integration to v1.
10. Do not add app contract integration to v1.
11. Do not add ZIP or publish-output behavior to v1.
12. Keep stale AI-send artifacts reported as a diagnostic, not silently fixed.
13. Keep index/file mismatch reported as a diagnostic, not silently repaired.
14. Keep JSON output machine-readable and text output human/AI-readable.
```

## known expected status after freeze

After this freeze entry is installed, the exposure tool may still report:

```text
FREEZE_MEMORY_STATUS: STALE_EXPOSURE
```

This remains expected until a future explicitly approved v1.1 publish/context-refresh feature is implemented and validated.

## intentionally not frozen here

This freeze does not include and must not be treated as approval for:

```text
1. freeze_memory_context_publish_v1_1
2. writing current_freeze_memory_context.md
3. writing freeze_exposure_report.json
4. ZIP context pack generation
5. GUI refresh button
6. startup prompt integration
7. app contract integration
8. automatic freeze_index.json repair/regeneration
```

## future allowed step

The next allowed roadmap item may be:

```text
freeze_memory_context_publish_v1_1
```

That future patch may add explicit `--publish --yes` behavior only after a separate Box Boundary Audit, implementation, sandbox validation, local validation, and human approval.
