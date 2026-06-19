---
freeze_id: freeze-20260613-freeze-after-update-bom-index-tolerance-v1
status: frozen
project: kanda_reasoner
box: project_freeze_ledger/freeze_tools + project_freeze_after_update/frozen_features_memory
date: 2026-06-13
validated: true
---

# Freeze: Freeze After Update BOM index tolerance v1

## Frozen behavior

Freeze Feature After Update must tolerate `freeze_index.json` files saved with a UTF-8 BOM.

The freeze generator must:

1. Read existing `freeze_index.json` using BOM-tolerant decoding.
2. Accept both UTF-8 and UTF-8-with-BOM JSON.
3. Rebuild/copy `files_to_send_ai` even when the active project freeze index previously contained a BOM.
4. Write regenerated `freeze_index.json` as normal UTF-8 without a BOM.
5. Keep project freeze memory inside `project_freeze_after_update/frozen_features_memory/`.
6. Keep project_freeze_ledger as the blueprint/generator box only, not as the active project freeze memory location.

Project rule: project_freeze_ledger is the blueprint/generator box only.

## Validation evidence

Validation evidence pasted by the human showed:

```text
VALIDATION OK - Freeze After Update BOM index patch v2 validation repair is installed and coherent.
```

The same validation included:

```text
BOM functional test passed
active freeze_index parses with utf-8-sig
```

The freeze send-pack was generated afterward and reported 12 existing freeze entries, confirming `files_to_send_ai` generation recovered.

## Protected paths

- `project_freeze_ledger/freeze_tools/freeze_after_update_generator.py`
- `project_freeze_after_update/frozen_features_memory/freeze_index.json`
- `project_freeze_after_update/frozen_features_memory/project_frozen_implemented_steps.md`
- `project_freeze_after_update/frozen_features_memory/entries/`
- `project_freeze_after_update/files_to_send_ai/`

## Do not touch summary

- Do not change BOM-tolerant JSON reads back to plain `utf-8` for existing freeze memory JSON.
- Do not allow BOM in regenerated `freeze_index.json`.
- Do not move active project freeze memory into `project_freeze_ledger`.
- Do not classify runtime/cache artifacts as persistent freeze architecture violations.
- Do not freeze future behavior unless validation evidence is pasted by the human.

## Regression symptoms

If this behavior regresses, the freeze send-pack may show:

```text
incomplete: freeze_index.json is invalid: Unexpected UTF-8 BOM
Freeze entries included: 0
```

That is a failure of freeze memory generation and must be repaired before freezing new behavior.
