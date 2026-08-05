# Error Memory

Keep practical lessons from real project failures so the same mistake is less likely to happen again.

Image note:

- Subject: Two people carefully reviewing and organizing a library of lessons.
- Asset path: `assets/drawings/architecture_review_issue_catalog_library.png`
- Alt text: Two people inspect and organize a library of carefully indexed project lessons.
- Caption: Error Memory is a reviewed lesson library, not an automatic log of every error.
- Artwork status: reused_existing_characterful_raster

## What This Tab Does

**In plain English:** Error Memory is a project-specific library of lessons learned from errors that actually happened. Each lesson records what went wrong, why it happened, how it was corrected, what must not be repeated, and how the correction should be checked in the future.

The tab does not automatically decide that every error deserves a permanent lesson. You review the evidence and choose whether to save, activate, deprecate, supersede, or delete a lesson.

## Before You Start

1. Confirm the correct **Project Root** at the top of the tab.
2. Make sure the error belongs to that project.
3. Gather the exact error message, relevant context, correction, and validation evidence.
4. Avoid including passwords, API keys, private credentials, or unnecessary personal information.
5. Use one lesson for one repeatable failure pattern.

> Important: Error Memory is prevention guidance. It does not replace inspection of the current source files.

## The Safest First-Time Workflow

1. Put the raw error and useful context in **AI-assisted error lesson intake**.
2. Click **Check Against Lessons** to see whether a similar lesson already exists.
3. Use **Copy and Open External AI** when you need AI help creating or correcting the lesson.
4. Paste the formatted result back with **Paste error formatted from AI**, or import an approved Error Lesson ZIP.
5. Review the complete lesson in **Error Editor**.
6. Use **Correct with AI** only when you want a preview correction. This does not save the lesson.
7. Use **Memorize Error** only after the lesson is complete and active-ready.
8. Confirm the lesson appears correctly in the **Lessons** table.

## Project and Folder Controls

### Project Root

This is the project whose Error Memory you are viewing. A wrong root can put a lesson in the wrong project library.

### Open EM Folder

Opens the current project's durable Error Memory folder. Use this when you need to inspect the stored lesson files directly.

### Open Second Prompt Files

Opens the handoff-output folder used for AI uploads. This is separate from the canonical Error Memory store.

### Get path buttons

These buttons copy folder paths. They do not copy lesson content.

### Get correct way to send me errors

Copies the canonical instructions for sending an error to AI. Use it when preparing a new error report outside the tab.

### Send Zip Errors

Copies the generalized current-Project prompt that instructs AI to create one self-contained Error Memory lesson intake ZIP. The resulting loader stages lessons for review only; Memorize Error remains human-controlled.

## AI-Assisted Error Lesson Intake

This left-side area is a temporary preparation area.

### Paste error formatted from AI

Loads a formatted Error Memory JSON block into the tab. It does not memorize the lesson automatically.

### Copy and Open External AI

Copies the current intake text together with the required Error Memory instructions and opens the selected external Python-coding assistant. Paste manually. The returned lesson remains untrusted until it is imported, checked against existing lessons, reviewed, and explicitly memorized.

### Clean

Clears the current intake and editor view. It does not automatically delete every disk-backed draft.

### Del Draft

Deletes the current matching draft and related pending intake records. Use this only when the draft should be removed completely.

### Memorize Error

Saves an active-ready lesson into the canonical Error Memory store.

Use it only when:

- the lesson describes a real repeatable failure;
- root cause and correction are supported;
- the do-not-repeat rule is clear;
- validation evidence is present;
- no secret or private data is included.

### Import Error Lesson ZIP

Loads an AI-created lesson package into the intake and editor. Importing is not the same as memorizing.

### Check Against Lessons

Searches for possible overlap with existing lessons. It is advisory and helps prevent duplicates.

### Copy Error Lesson Intake blueprint

Copies the active-ready template and instructions required for AI to format a lesson correctly.

## Error Editor

The Error Editor is the review area. A selected lesson, imported lesson, or formatted AI response appears here as JSON.

You may edit the lesson before saving it. Read the complete content instead of checking only the title.

### Save

Saves the JSON currently shown in the editor to the canonical lesson store. Use this carefully because it is a direct save action.

### Copy and Open External AI

Copies the current editor content with the required AI instructions and opens the selected external Python-coding assistant. The external answer cannot save, activate, supersede, or memorize a lesson.

### Clean

Clears the editor and intake views without approving a lesson.

### Undo

Restores the most recently deleted lesson when possible, or reloads the selected lesson.

### Delete

Deletes the selected canonical lesson. Use Undo immediately if deletion was accidental.

## Transfer Buttons

### Export Errors

Creates a portable folder containing valid lessons, including inactive lessons. Use it for controlled backup or transfer.

### Import Errors

Merges unique validated lessons from a KANDA Error Memory export. Existing lessons are not intentionally replaced or deleted.

### Lessons to Clipboard

Copies the complete Error Memory lesson library as JSON to the clipboard for manual AI transfer.

What happens next:

1. The complete JSON is copied to the clipboard.
2. A backup JSON file is written to the project support area.
3. The same JSON is shown in the Error Editor as a fallback copy source.

This button copies lessons, not the path to `second_prompt_files`.

## Lesson Status Controls

### Mark Draft

Keeps an incomplete lesson without presenting it as active prevention guidance.

### Mark Active

Promotes a complete lesson to active status. Required fields and validation evidence must be present.

### Deprecate

Keeps the lesson for history but excludes it from active guidance.

### Supersede

Marks the selected lesson as replaced by a newer lesson. Record the replacement lesson ID clearly.

### Correct with AI

Runs the selected correction engine in the background and loads the result as a preview. It does not save, activate, delete, supersede, or memorize anything by itself.

## The Lessons Table

The table shows saved lessons and pending intake rows.

Columns include:

- **Status** - draft, active, deprecated, or superseded.
- **Symptom** - what the user observed.
- **Do-not-repeat rule** - the prevention rule.
- **Updated** - when the lesson changed.
- **Lesson ID** - the stable machine-readable identifier.

Click a row to load it into the Error Editor. A pending row is not yet a permanent active lesson.

## Common Mistakes

### Memorizing too early

Do not memorize a lesson while root cause, correction, or evidence is still uncertain. Keep it as a draft.

### Creating duplicates

Run **Check Against Lessons** before creating a new lesson. Update or supersede an existing lesson when it already owns the same failure pattern.

### Treating Error Memory as source truth

A lesson helps prevent repetition, but current source files and current validation remain authoritative.

### Copying secrets

Remove API keys, passwords, tokens, private credentials, and unnecessary personal information before using clipboard or AI-transfer actions.

### Confusing export with memorization

Copying, exporting, importing, or AI-correcting does not automatically approve the lesson. Human review remains required.

## A Complete First-Time Example

Suppose a validation command used the wrong Python interpreter.

1. Paste the exact error and interpreter evidence into intake.
2. Check for an existing interpreter-resolution lesson.
3. If the existing lesson already covers the failure, use it instead of creating a duplicate.
4. If it is genuinely new, prepare one lesson describing the symptom, root cause, correct fix, do-not-repeat rule, and regression command.
5. Review the JSON in Error Editor.
6. Keep it as draft until the validation evidence passes.
7. Memorize or mark active only after the evidence is correct.

## Final Safety Reminder

Error Memory is valuable because it is selective, reviewed, project-specific, and evidence-based. More lessons are not always better. Clear ownership and accurate prevention rules matter more than volume.
