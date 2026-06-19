---
freeze_id: "freeze-20260612-project-freeze-ledger-v20-freeze-index"
box: "project_freeze_ledger/freeze_index"
status: "frozen"
date: "2026-06-12"
entry: "project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v20-freeze-index.md"
protected_paths:
  - "project_freeze_ledger/freeze_tools/build_freeze_index.py"
  - "project_freeze_ledger/freeze_index.json"
  - "project_freeze_ledger/entries/"
  - "project_freeze_ledger/project_frozen_implemented_steps.md"
do_not_touch_summary:
  - "Keep Markdown entries as canonical source."
  - "Keep freeze_index.json generated from structured freeze entries."
  - "Do not edit freeze_index.json manually."
  - "Do not create protected path checker in this frozen box."
superseded_by: null
---

# freeze-20260612-project-freeze-ledger-v20-freeze-index

## freeze identity

```text
freeze id: freeze-20260612-project-freeze-ledger-v20-freeze-index
date: 2026-06-12
project box: project_freeze_ledger/freeze_index
freeze tier: tier 1 governance / baseline freeze
status: frozen after validation and user acceptance
```

## frozen version

```text
project_freeze_ledger v20 freeze_index.json generator
```

## summary

The `project_freeze_ledger` now has a generated machine-readable freeze index.

The canonical source remains the Markdown structured freeze entries:

```text
project_freeze_ledger/entries/*.md
```

The generated index is:

```text
project_freeze_ledger/freeze_index.json
```

The index is derived from structured frontmatter and should not be edited manually.

## what was implemented

The v20 implementation added:

```text
project_freeze_ledger/freeze_tools/build_freeze_index.py
```

The tool supports:

```text
--sync
--check
--print
```

The user ran:

```text
py -3 .\project_freeze_ledger\freeze_tools\build_freeze_index.py --sync
```

which generated:

```text
project_freeze_ledger/freeze_index.json
```

The user then ran:

```text
py -3 .\project_freeze_ledger\freeze_tools\build_freeze_index.py --check
```

which confirmed that the generated index is in sync with structured freeze entries.

## files and folders affected

Frozen files/folders for this v20 index layer:

```text
project_freeze_ledger/freeze_tools/build_freeze_index.py
project_freeze_ledger/freeze_index.json
project_freeze_ledger/entries/
project_freeze_ledger/project_frozen_implemented_steps.md
```

This freeze entry:

```text
project_freeze_ledger/entries/freeze-20260612-project-freeze-ledger-v20-freeze-index.md
```

## validation evidence summary

User ran sync:

```text
SYNC OK
schema_version=1.0
entries_count=4
- freeze-20260612-phase7a-v24 [frozen] paths=3
- freeze-20260612-project-freeze-ledger-v1 [superseded] paths=3
- freeze-20260612-project-freeze-ledger-v18 [frozen] paths=5
- freeze-20260612-project-freeze-ledger-v19-structured-entries [frozen] paths=4
freeze_index.json is generated from Markdown entries. Do not edit it manually.
```

User ran check:

```text
CHECK OK
freeze_index.json is in sync with structured freeze entries.
schema_version=1.0
entries_count=4
- freeze-20260612-phase7a-v24 [frozen] paths=3
- freeze-20260612-project-freeze-ledger-v1 [superseded] paths=3
- freeze-20260612-project-freeze-ledger-v18 [frozen] paths=5
- freeze-20260612-project-freeze-ledger-v19-structured-entries [frozen] paths=4
No protected path checker was created.
```

## behavioral tests

Not applicable as application runtime behavior.

This is a governance/tooling freeze. The relevant behavior is:

```text
--sync creates freeze_index.json from structured Markdown entries
--check confirms freeze_index.json is in sync
the index includes frozen and superseded entries
the index does not replace Markdown as canonical source
no protected path checker is created in this box
```

## what is explicitly not included

This freeze does not include:

```text
check_protected_paths.py
AI-send ZIP filtering by protected paths
automatic preflight blocker
manual JSON editing
runtime app logic changes
startup delivery logic changes
compiled build output
```

Those are later boxes.

## do-not-touch boundaries

Do not casually change:

```text
project_freeze_ledger/freeze_tools/build_freeze_index.py
project_freeze_ledger/freeze_index.json generation contract
project_freeze_ledger/entries/*.md structured frontmatter fields
```

Do not reintroduce:

```text
manual freeze_index.json maintenance
hardcoded local absolute paths
external YAML dependency
protected path checker in this v20 box
```

Keep the rule:

```text
Markdown entries are canonical.
freeze_index.json is generated.
If freeze_index.json is out of sync, regenerate with build_freeze_index.py --sync.
```

## downstream dependencies

Later boxes depend on this baseline:

```text
v21 protected path checker
v22 AI-send pack upgraded with index/checker awareness
v23 superseded lifecycle formalization
```

Future tools should use:

```text
project_freeze_ledger/freeze_index.json
```

as a fast detection/index layer, but detailed Markdown entries remain the authority.

## exposure classification

```text
safe_for_targeted_ai_upload
```

Rationale:

```text
This entry contains governance metadata, file names, and validation evidence.
It does not contain credentials, secrets, patient data, or full project source code.
```

## external AI sharing rule

Safe to share with an external AI for targeted review or implementation involving:

```text
freeze index generation
freeze ledger validation
protected path checker planning
AI-send package upgrade planning
```

Do not share unrelated project source code or full project ZIPs unless separately reviewed.

## rollback / break-glass protocol

To change this frozen baseline:

```text
1. read this freeze entry first
2. state why the generated index contract must change
3. preserve Markdown entries as canonical source
4. preserve dynamic project-root compatibility
5. avoid hardcoded local absolute paths
6. implement the smallest possible patch inside project_freeze_ledger
7. rerun build_freeze_index.py --sync
8. rerun build_freeze_index.py --check
9. create a new freeze entry if accepted
```

If the index becomes stale or corrupted:

```text
project_freeze_ledger/freeze_tools/build_freeze_index.py --sync
project_freeze_ledger/freeze_tools/build_freeze_index.py --check
```

## next allowed step

The next allowed implementation box is:

```text
v21 protected path checker
```

Only after explicit user approval.

The v21 checker must use `freeze_index.json` as the fast index and must require reading the detailed Markdown entry before modifying protected paths.
