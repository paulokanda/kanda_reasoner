# KANDA Reasoner Architecture Review
## Beginner Handoff: Run Selected Mode, Validate, Diff, Scan, and Write

Document purpose: Help a first-time user understand what the Architecture Review tool does, what each mode means, when to use it, and what can safely change the project.

Audience: A new user who is not a programmer and has never used KANDA Reasoner.

Current status: All four modes are active. None of them is deprecated.

---

## 1. What is this project for?

KANDA Reasoner is a project-inspection and project-governance application. It helps a person or an AI understand a software project before making changes.

Think of a software project as a large building:

- Files are rooms.
- Folders are departments or floors.
- Public functions and classes are doors used by other parts of the building.
- Imports are hallways connecting rooms.
- Tests are safety inspections.
- Architecture files are the official building map.

The Architecture Review tool checks whether this building is organized safely. It can find problems, show what documentation would change, print a detailed map, or update the official architecture records.

It is mainly used to reduce mistakes such as:

- editing the wrong file;
- creating two owners for the same function;
- using an old or copied file as the source of truth;
- creating circular dependencies;
- placing code in the wrong architectural box;
- leaving a very large file without a refactoring plan;
- writing generated architecture files before important errors are resolved.

The tool does not repair all problems automatically. Its first responsibility is to inspect, report, and protect the project.

---

## 2. What does "Run Selected Mode" mean?

`Run Selected Mode` is the main Start button.

It does not represent a fifth mode. It runs whichever option is currently selected in the `Mode` list:

1. `validate`
2. `diff`
3. `scan`
4. `write`

Example:

- Mode shows `validate`.
- You click `Run Selected Mode`.
- The application runs Validate.

If you change Mode to `diff` and click the same button, the application runs Diff.

Before any mode starts, the application checks that:

- the worker script exists;
- the selected project root exists;
- no other Architecture Review operation is already running.

For Write mode, the application can also ask for explicit confirmation before changing files.

---

## 3. Recommended order for a new user

Use the modes in this order:

1. **Validate** - find architecture problems.
2. **Diff** - preview architecture-file changes.
3. **Scan** - use only when you need the full technical project map.
4. **Write** - update architecture records only after reviewing Validate and Diff.

The safest everyday sequence is:

```text
Validate -> fix or review important errors -> Diff -> Write -> Validate again
```

For a new user, Validate should be the default starting point.

---

# 4. Validate mode

## What Validate is for

Validate is the project safety inspection.

It examines the project and reports architecture problems without writing the generated architecture files.

Validate is the best mode for answering questions such as:

- Is this project structurally safe enough to work on?
- Are there files that appear to have the wrong owner?
- Are there duplicate public names?
- Are there circular dependencies?
- Are files placed in the wrong architectural box?
- Are there stale, copied, legacy, or backup variants that may confuse a person or AI?
- Are modules too large?
- Are helper folders missing their expected main owner?
- Are generated artifacts or bundles violating project rules?
- Are important tests missing or placed incorrectly?

## What Validate actually does

Validate first scans the project tree. It reads Python files, builds a structural model, evaluates architecture rules, and groups findings by severity.

The result can contain:

- **ERROR** - a blocking architecture problem.
- **WARNING** - a risk that needs review but does not automatically block Write.

Important behavior:

- Validate does not write `architecture_manifest.json`.
- Validate does not write `ARCHITECTURE.md`.
- Validate does not create or replace generated `__init__.py` facades.
- Validate returns a failure status when at least one ERROR exists.
- Warnings alone do not make Validate fail.

This means:

```text
0 errors + 20 warnings = Validate may finish successfully, but the warnings still matter.
1 error + 0 warnings = Validate finishes with issues and Write will be blocked.
```

## When to use Validate

Use Validate:

- at the start of a work session;
- before asking an AI to modify architecture-sensitive code;
- before using Write;
- after installing a patch;
- after moving, renaming, splitting, or deleting Python files;
- after changing imports or public functions;
- when the project reports architecture warnings;
- when you are unsure whether the project root is correct;
- after Write, to confirm the resulting project remains valid.

## Example for a non-programmer

Suppose Validate reports:

```text
ERROR DUPLICATE_PUBLIC_SYMBOL
Symbol 'build_report' is owned by two modules.
```

Plain-English meaning:

Two rooms are claiming to be the official location of the same public service. Other parts of the project may not know which one is correct.

What to do:

- Do not use Write yet.
- Save or copy the audit output.
- Ask a developer or AI to identify the true owner.
- Correct the ownership conflict.
- Run Validate again.

Another example:

```text
WARNING MODULE_TOO_LARGE
Module has 620 lines; split threshold is 500.
```

Plain-English meaning:

The file is larger than the project allows. It may still work today, but it is harder to understand and safer refactoring should be planned.

What to do:

- You may continue reviewing the project.
- Do not assume the warning means the file is broken.
- Use the Large File Refactor Planner when appropriate.

## What a successful Validate does not prove

A successful Validate does not prove that:

- every business feature works;
- every medical or domain rule is correct;
- every possible runtime error has been tested;
- the selected project root was the one you intended, unless you checked it;
- warnings can be ignored.

Validate is an architecture inspection, not a complete replacement for all tests.

---

# 5. Diff mode

## What Diff is for

Diff is the preview mode.

It shows how generated architecture files would look if Write were used now.

Diff can preview changes to:

- `architecture_manifest.json`;
- `ARCHITECTURE.md`;
- eligible minimal generated `__init__.py` facade files.

Diff does not apply those changes.

## What the Diff display means

A Diff normally uses symbols similar to:

```text
- old line
+ new line
```

- A line beginning with `-` exists in the current file but would be removed or replaced.
- A line beginning with `+` would be added.
- Lines without those signs provide surrounding context.

## Important behavior that can confuse new users

When Diff finds changes, it returns a non-zero result. The GUI may therefore say that Diff "finished with issues."

For Diff mode, this does not necessarily mean that the project is broken.

It often means:

```text
The current generated files are different from the files the tool would generate now.
```

If Diff prints:

```text
No diffs.
```

then the generated architecture files are already synchronized with the current project model.

## When to use Diff

Use Diff:

- after Validate;
- before Write;
- after adding, moving, or renaming modules;
- when you want to know exactly what Write would change;
- when reviewing a patch that affects project structure;
- when you want evidence without changing files.

## Example

Suppose you added a new public class named `PatientReportBuilder`.

Diff may show that:

- the class will appear in `architecture_manifest.json`;
- the package map in `ARCHITECTURE.md` will include it;
- a minimal package facade may expose it through `__init__.py`.

Diff allows you to review this before any generated file is changed.

## What Diff does not do

Diff does not:

- write files;
- approve the proposed changes;
- fix validation errors;
- prove that the new architecture is correct;
- replace human review before Write.

---

# 6. Scan mode

## What Scan is for

Scan prints the complete architecture manifest as JSON.

JSON is a structured technical data format. It is designed mainly for software tools, developers, and AI systems rather than casual reading.

The Scan output can include:

- packages;
- modules;
- public symbols;
- dependencies;
- reverse dependencies;
- helper groups;
- file metadata;
- validation issues;
- project-root information.

## When to use Scan

Use Scan when:

- a developer or AI asks for the full architecture manifest;
- you need detailed project evidence for a handoff;
- you are debugging why a module or symbol was classified a certain way;
- you need to save a machine-readable project map;
- a specialized workflow explicitly requires manifest JSON.

For ordinary use, start with Validate instead.

## Important safety detail

Scan builds the same project model and includes validation issues in the manifest, but Scan returns success after printing the JSON.

Therefore:

```text
Scan completed successfully
```

does not mean:

```text
The project has no validation errors.
```

Scan means the map was printed successfully. Use Validate to make a pass/fail architecture decision.

## Example

A support specialist may ask:

> Run Scan and save the output so I can see which module owns `run_selected_mode`.

You would:

1. Select `scan`.
2. Click `Run Selected Mode`.
3. Wait for the JSON output.
4. Click `Save Audit Results`.
5. Send the saved text file as evidence.

## What Scan does not do

Scan does not:

- write generated architecture files;
- fix problems;
- block because architecture errors exist;
- provide the easiest report for a beginner.

---

# 7. Write mode

## What Write is for

Write updates the generated architecture records so they match the current project structure.

It can write:

- `architecture_manifest.json`;
- `ARCHITECTURE.md`;
- eligible minimal generated `__init__.py` facade files.

Write is the only one of the four modes that intentionally changes these project files.

## Safety checks before Write

Before Write begins, the GUI checks the project root and worker script.

When `Require confirm before write` is checked, the application displays a confirmation message. The default answer is No.

The worker then performs validation before writing.

If any ERROR-level validation issue exists, Write refuses to continue and reports:

```text
Refusing to write because validation has errors.
```

Warnings do not automatically block Write. They must still be reviewed.

## What happens during Write

The sequence is:

1. Scan the current project.
2. Run architecture validation.
3. Stop if ERROR-level issues exist.
4. Generate the expected architecture outputs.
5. Write files whose content has changed.
6. Scan the project again after writing.
7. Validate the post-write state.
8. Stop and report if post-write ERROR-level issues exist.
9. Update generated outputs again if the second scan requires it.
10. Report how many files were updated.

## When to use Write

Use Write only when:

- the selected project root has been personally checked;
- Validate has been reviewed;
- blocking errors have been corrected;
- Diff has been reviewed;
- you intentionally want to update generated architecture records;
- the confirmation checkbox remains enabled unless a governed workflow explicitly says otherwise.

## Example

You added a new correctly placed module and Validate reports no errors. Diff shows only expected additions to the manifest and architecture map.

Safe sequence:

1. Confirm the Project Root.
2. Run Validate.
3. Review warnings.
4. Run Diff.
5. Confirm the preview is expected.
6. Select Write.
7. Keep `Require confirm before write` checked.
8. Click `Run Selected Mode`.
9. Read the confirmation dialog carefully.
10. Click Yes only when you intend to write.
11. Run Validate again afterward.

## Important post-write warning

Write performs a second validation after files are written. If that second validation finds an ERROR, Write reports failure.

Some files may already have been updated before the post-write error was discovered. Therefore, save the output and request review rather than repeatedly pressing Write.

## What Write does not do

Write does not:

- repair all reported architecture problems;
- modify every Python source file;
- automatically approve warnings;
- freeze a feature;
- replace patch validation;
- replace backups or version control;
- guarantee that application behavior is correct.

---

# 8. Are any modes deprecated?

No. In the current Architecture Review implementation:

- Validate is active.
- Diff is active.
- Scan is active.
- Write is active.
- Run Selected Mode is the active launcher for the chosen mode.

None of these options is marked as deprecated.

Their recommended use is different:

| Option | Status | Risk level | Recommended for beginners |
|---|---|---:|---|
| Validate | Active | Low, read-only | Yes, use first |
| Diff | Active | Low, read-only | Yes, use after Validate |
| Scan | Active | Low, read-only but technical | Only when detailed JSON is needed |
| Write | Active | High because it changes files | Use carefully after Validate and Diff |
| Run Selected Mode | Active launcher | Depends on selected mode | Yes, after checking the selected mode |

---

# 9. Quick decision guide

## I only want to know whether there are architecture problems

Use **Validate**.

## I want to see what would change, but I do not want to change files

Use **Diff**.

## A developer or AI asked for the full technical architecture map

Use **Scan**, then save the output.

## I reviewed the project and intentionally want to update generated architecture files

Use **Write**, with confirmation enabled.

## I do not know which one to choose

Use **Validate**.

---

# 10. Beginner walkthrough

## First inspection of a project

1. Open Architecture Review.
2. Confirm the `Project Root` field points to the intended project.
3. Confirm Mode is `validate`.
4. Click `Run Selected Mode`.
5. Wait until the activity finishes.
6. Read the first ERROR and WARNING summaries.
7. Use `Save Audit Results` before asking for help.
8. Do not use Write when ERROR-level findings remain.

## Previewing architecture records

1. Run Validate first.
2. Select `diff`.
3. Click `Run Selected Mode`.
4. Review lines beginning with `-` and `+`.
5. Remember that "finished with issues" may simply mean differences were found.
6. Save the output when another person or AI needs to review it.

## Updating architecture records

1. Confirm the Project Root again.
2. Run Validate.
3. Review all errors and important warnings.
4. Run Diff.
5. Confirm the proposed changes are expected.
6. Select `write`.
7. Keep `Require confirm before write` enabled.
8. Click `Run Selected Mode`.
9. Read the confirmation dialog.
10. Confirm only when you deliberately want the changes.
11. Run Validate again.

---

# 11. Common mistakes

## Mistake: Treating Scan success as validation success

Correction: Scan proves that the map was printed. Validate determines whether blocking architecture errors exist.

## Mistake: Thinking Diff already changed files

Correction: Diff is only a preview.

## Mistake: Treating every warning as a broken application

Correction: Warnings identify risks. Errors are the findings that automatically block Write.

## Mistake: Ignoring warnings because Validate returned success

Correction: Validate returns failure only for errors. Warnings still require review.

## Mistake: Using Write without checking the Project Root

Correction: Always verify the root immediately before Write.

## Mistake: Repeatedly running Write after a post-write error

Correction: Save the output and investigate which files changed and why post-write validation failed.

## Mistake: Turning off confirmation because it feels inconvenient

Correction: Keep confirmation enabled. It is a deliberate safety barrier.

---

# 12. How to read the final status

Typical successful Validate:

```text
[finished] mode=validate exit_code=0
```

Meaning: No ERROR-level architecture findings remained after the active warning baseline was applied. Warnings may still exist.

Validate with blocking errors:

```text
[finished] mode=validate exit_code=1
```

Meaning: At least one ERROR-level issue exists, or the worker encountered a failure.

Diff with changes:

```text
[finished] mode=diff exit_code=1
```

Meaning: Usually, differences were found. Review the Diff output. This does not automatically mean the project is broken.

Diff with no changes:

```text
No diffs.
[finished] mode=diff exit_code=0
```

Meaning: Generated architecture records match the current generated view.

Successful Write:

```text
Done. Updated N file(s).
[finished] mode=write exit_code=0
```

Meaning: Pre-write validation allowed writing, files were updated as needed, and post-write validation had no blocking errors.

Blocked Write:

```text
Refusing to write because validation has errors.
[finished] mode=write exit_code=1
```

Meaning: No architecture write should proceed until the blocking errors are corrected.

---

# 13. Safety summary

Remember these four sentences:

1. **Validate tells you what is wrong.**
2. **Diff shows what would change.**
3. **Scan prints the full technical map.**
4. **Write changes generated architecture records.**

And remember:

```text
When unsure, select Validate.
```

---

# 14. Implementation handoff for maintainers

This user guide was checked against the current source behavior in:

- `kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py`
- `kanda_reasoner_app/manage_architecture/manage_architecture_gui.py`
- the runtime implementation loaded by `kanda_reasoner_app/manage_architecture/manage_architecture.py`

Current mode selector:

```text
validate, diff, scan, write
```

Current default mode:

```text
validate
```

Current runtime behavior:

- Every mode builds the project scan and validation model first.
- Validate prints issues and fails only when ERROR-level findings exist.
- Diff prints generated-output differences and returns a non-zero status when differences exist.
- Scan prints manifest JSON and returns success after printing it.
- Write blocks on pre-write ERROR findings, writes generated outputs, rescans, and performs post-write ERROR validation.

Do not create a second independent Validate engine. Maintain one validation source of truth and improve user-facing explanation or tests around that existing engine.
