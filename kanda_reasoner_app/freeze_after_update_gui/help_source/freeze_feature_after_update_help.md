# Freeze Feature After Update

A complete first-time guide for safely recording a validated feature as governed project memory.

## What this tab is for

After a feature has been implemented and validated, this tab records what the feature is, which files were checked, which paths are protected, what must not regress, and what evidence proves the result. This record helps future users and AI sessions understand what is already trusted.

Freezing does not make the source code physically impossible to edit. It creates governed memory so later changes are deliberate and informed.

## Safest first-time order

1. Select the correct Project Root.
2. Click Check Box Status.
3. Use Create / Repair Box only when the structure is missing or incomplete.
4. Validate the feature outside this tab and keep the real success markers.
5. Open Local Freeze Entry.
6. Refresh the current Freeze Hint.
7. Review the form fields and fix any stale information.
8. Click Preview Freeze Entry.
9. Read the complete preview.
10. Click Confirm and Write Freeze Entry only after human review.
11. Confirm that the startup freeze context was refreshed.

## Main tab controls

### Project Root
The active editable project. Every path and freeze record must belong to this project.

### Check Box Status
Inspects whether the project-specific freeze structure exists and is valid. It does not write a freeze entry.

### Create / Repair Box
Creates missing freeze folders and safe support files. It repairs structure only; it does not freeze a feature.

### Local Freeze Entry
Opens the normal local freeze workflow. This is the recommended path for most work.

### Get Last Freeze
Copies the newest frozen feature as an AI-ready reminder. Use it when an AI begins to forget the most recent protected feature.

### Get All Frozen
Copies all frozen entries as an AI-ready reminder. Use it when a new or long-running AI session needs the broader frozen project context.

### Get blueprint Freeze
Copies the strict KANDA freeze-form blueprint. This orange-labeled control is a recovery aid when an AI-generated freeze form is missing fields or has the wrong JSON structure.

### Open Box Folder
Opens the project-specific freeze support folder so you can inspect intake, memory, and support files.

### Help
Opens this guide.

## Validation evidence comes first

A freeze is trustworthy only when it contains real local validation evidence. Confirm and Write requires literal current-feature markers:

- VALIDATION OK: feature-id
- STATUS: IN_SYNC

Other hash, compile, runtime, or ZIP markers may support those lines but cannot replace them.
- Hash, compile, runtime, or focused-validator markers required by the feature

Do not invent evidence. Installation success alone is not validation.

## Local Freeze Entry dialog

### Refresh Current Freeze Hint
Loads the newest intake record for the current feature. Use this before filling or previewing the form so stale data is not reused.

### AI mode

- Heuristic: deterministic local starter that fills fields from current intake data.
- Local AI: local AI assistance when configured and ready.
- Web AI: external review or fallback. Human review remains mandatory.

Changing mode never bypasses Preview or confirmation.

### Fill Form Now
Populates the fields using the selected mode. Review every field afterward.

### Feature title
The exact human-readable name of the current validated feature.

### Primary box
The project-relative owner path for the feature.

### Box type
A simple category such as gui, module, tool, prompt, or documentation.

### Validated files
One project-relative validated file per line. These are files actually checked by the validation routine.

### Generated files
Generated artifacts produced by the feature, or n/a when none exist.

### Protected paths
Paths that future work should treat carefully.

### Do-not-regress rules
One clear rule per line describing behavior, layout, contracts, or safety boundaries that must remain intact.

### Validation evidence summary
Real success markers copied from local validation. Missing or unrecognizable evidence blocks the freeze.

### Known warnings
Real remaining cautions, or n/a.

### Planned next step
Usually Preview, then Confirm and Write after human review. After an entry is frozen, old planned-next-step text is historical rather than pending work.

### Notes
A brief explanation that helps future users and AI understand why the feature was frozen.

### Copy Entry to AI

Copies the strict draft-only Freeze formulary prompt to the clipboard. It does not open a browser or external assistant. Paste the prompt manually into the AI of your choice. The returned marker-wrapped form remains untrusted until **Receive Formulary from AI** parses it, the form is reviewed, and **Preview Freeze Entry** passes. This action never writes Freeze memory.

### Receive Formulary from AI

Imports a marker-wrapped external draft into the form. It does not write files, does not confirm the feature, and does not bypass Preview or Confirm and Write.

### Preview Freeze Entry
Read-only. It shows exactly what would be written, including identity, validated files, protected paths, rules, evidence, warnings, and notes. It never writes a file.

### Confirm and Write Freeze Entry
The only writing step. Use it only after the preview is correct. Explicit human confirmation is required.

### Ignore this Freeze
Deletes and forgets the currently displayed unfrozen Freeze candidate, removes its exact transient staged source when it is still safely inside `<project>_delete_after_daily_work`, clears the form and Preview, and keeps the New Local Freeze Entry window open. A minimal `ignored-by-human` consumption tombstone is retained so that the exact ignored source cannot be re-imported; genuinely different newer repair sources remain eligible. It never deletes or changes already frozen memory.

### Cancel
Closes the dialog without writing.

## Where information comes from and where it goes

Inputs include the selected Project Root, current Freeze Hint intake, validation evidence, current feature identity, and human-reviewed form fields.

Project-specific frozen memory is stored outside the editable project under:

`<project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory`

This separation reduces accidental edits and keeps governed memory distinct from normal source files. Project-specific memory must not be stored inside `project_freeze_ledger`; that box owns reusable blueprint logic only.

## When the AI starts to forget

Use the orange context and copy controls as reminders:

- Get Last Freeze for the newest protected feature.
- Get All Frozen for the complete frozen context.
- Get blueprint Freeze when the AI needs the exact form contract.

Paste the copied text into the AI conversation and tell the AI to treat it as read-only frozen feature memory. These reminders explain what the feature is, why it was frozen, what paths are protected, what is safe to change, and what must not regress.

## Common problems

### Current Freeze intake record is unavailable
Run the current package validation first. Confirm that evidence was merged into the current intake record. Do not reuse an older feature's intake.

### Missing validated_files or validation_evidence_summary
Return to the current feature evidence. Add only files actually validated and paste real markers.

### No recognizable validation evidence
Include the literal current-feature `VALIDATION OK: feature-id` line and `STATUS: IN_SYNC`. Narrative descriptions, installation-only messages, or planned validation do not authorize Freeze. A blocked Preview is shown as **FREEZE PREVIEW NOT READY** and is never rendered as a frozen entry.

### Preview contains the wrong feature
Stop. Refresh the Freeze Hint and correct the intake. Never confirm a stale preview.

### AI forgot frozen behavior
Use Get Last Freeze or Get All Frozen and paste the copied reminder into the AI conversation.

## Complete first-time example

A help-page update has been installed and validated. Validation shows its hash, layout, content, `VALIDATION OK`, `STATUS: IN_SYNC`, and `ZIP CONTRACT: PASS`. Open Local Freeze Entry, refresh the hint, verify that the feature title and files match that help update, preview the entry, and confirm only after every path and rule is correct. The entry is then written to external project-specific frozen memory and startup freeze context is refreshed.
