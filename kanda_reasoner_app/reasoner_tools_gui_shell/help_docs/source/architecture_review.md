# Audit Project

Audience: a first-time KANDA Reasoner user who does not need to be a programmer.

Purpose: teach the user exactly what each part of Audit Project does, what to click, what result to expect, and which controls are advanced or potentially able to write files.

## The simple idea

Audit Project is the inspection area of KANDA Reasoner. It helps you check a project before asking a person or an AI to modify it. It can find architecture warnings, inspect large Python files, prepare safe refactor plans, review engineering risks, and examine workflows.

It does not mean that every warning must be fixed. It gives evidence so you can make a safer decision.

## Recommended first-time workflow

1. Open Audit Project.
2. Select Architecture Review.
3. Select Check Update Architecture.
4. Confirm Project root points to the project you intend to inspect.
5. Leave Mode on validate.
6. Keep Require confirm before write selected.
7. Click Validate Project.
8. Wait for the result and read Project Audit Results.
9. Save, copy, or use **Copy and Open External AI** before asking an AI to help. The external route is manual and advisory.
10. Use the advanced child tabs only when the audit identifies a specific large file or refactor need.

## Main Audit Project sections

Audit Project contains three main tabs:

- Architecture Review: checks architecture and contains the large-file planning tools.
- Engineering Safety: runs safety, quality, source-hygiene, and focused engineering checks.
- Workflow Review: checks whether a process or feature workflow is complete, connected, and safe.

Each section has its own purpose. Start with Architecture Review unless you already know you need a different review.

## Architecture Review child tabs

Architecture Review contains five child tabs:

1. Check Update Architecture.
2. Dismissed Findings.
3. Large Module AST Split Audit.
4. Large File Refactor Planner.
5. Large File Refactor WorkBench.

They are arranged as a progression. The first tab finds problems. The second studies one oversized Python file. The third creates a refactor plan. The fourth prepares and validates a real moved-code preview through controlled stages.

## Check Update Architecture

Validate output is shown first as grouped findings. Errors are listed before warnings, and findings are grouped by audit code such as `WARNING BOUNDARY_ERROR_CONTRACT`. Each group and finding has a checkbox. Use `Dismiss Selected` only after you have decided a finding is accepted, deferred, or a false positive for the selected Project.

`Raw Audit` is a Project-filtered projection of the canonical validator buffer. Clicking `Dismiss Selected` immediately removes those detail lines from both Grouped Findings and Raw Audit. `Restore Selected` immediately repopulates both views from Project-owned restored-pending evidence even when no current audit buffer is loaded. The next fresh Validate Project run merges that restored evidence with current scan data by stable finding identity, removes duplicates, and then retires the restored-pending copy. Permanent suppression keeps findings hidden on future scans. The original validator counts and exit status remain authoritative underneath, so Project dispositions never convert a failing validator into a pass. Copy/AI warning-review routes use the same Project-filtered evidence.

## Dismissed Findings

Dismissed Findings is Project-owned durable review state stored under `<drive>/<project>_show_project_to_AI/project_architecture_review/`. It is not Tool Error Memory, Freeze Memory, or Project source.

- `Restore Selected` moves the stored finding into Project-owned restored-pending state so Grouped Findings and Raw Audit repopulate immediately. The next fresh Validate Project run merges it with current audit data and removes the temporary restored-pending copy.
- `Delete Selected Permanently` removes the row from the visible bin but keeps a suppression tombstone so later scans do not resurrect the same finding.
- A stable finding identity ignores line-number-only movement but changes when the finding code, path, or material message changes.
- Dismissing an error hides it only from the review list; the validator exit status and raw audit remain unchanged.


This is the normal starting point.

### Validate Project

Runs the selected mode. In validate mode, it checks the project and reports architecture findings without intentionally changing project source files.

### Cancel

Requests cancellation of the current Architecture operation. Use it only when a run is taking too long or you selected the wrong project. A hard cancellation can stop work in the middle, so wait for normal completion when possible.

### Mode

- validate: recommended first choice. Checks the project and reports findings.
- diff: previews expected architecture-file changes.
- scan: prints collected project or manifest information.
- write: writes architecture artifacts. This is advanced and should be used only deliberately.

The green action button changes its name to match the selected mode.

### Require confirm before write

Keep this selected. It adds a human confirmation step before write mode can update architecture files.

### Heuristic, Local AI, and Web AI review

These controls choose how an additional read-only explanation is created after deterministic audit results exist.

- Heuristic: local rule-based summary. Fast and does not need an AI model.
- Local AI: uses the configured local model.
- Web AI: uses the configured Web AI and requires approval before sending the audit context.

The AI review is advisory. The deterministic Project Audit result remains the authority.

### Clear Audit Results

Clears the visible result box only. It does not undo changes and does not delete saved files.

### Save Audit Results

Saves the current visible report to a file you choose. Use this when the result will be reviewed later or sent to another person or AI.

### Mode Help

Shows a short reminder explaining validate, diff, scan, and write.

### Include latest Refactor Report evidence

When selected, copied audit results can include compact evidence from the latest Refactor Report. Leave it selected when you want an AI to receive more complete context. Clear it when you need only the Architecture Review result.

### Copy Audit Results

Copies the current audit report to the clipboard. You can paste it into an AI conversation, document, or issue report.

### Copy and Open External AI

Copies the current audit evidence, including Refactor Report evidence when selected, and opens the configured external Python-coding assistant. The user pastes manually. The external answer is advisory only: it cannot change audit pass/fail, write Project source, authorize a patch, create Error Memory, or write Freeze memory.

### Warning Heuristic Resolver

Opens the warning-resolution workflow. It can classify or route warnings using the available heuristic, Local AI, or Web AI paths. Use it after a Project Audit has produced warnings, not before.

### Cancel Resolver

Stops a warning-resolution run. It is enabled only while the resolver is working.

### Large Module Creation/Refactor Protocol

Copies the governed large-module rules to the clipboard. Use this when an AI will create or refactor a Python module and must respect the KANDA size and architecture rules.

### Project Audit Results

This large read-only area shows progress, warnings, evidence paths, issue codes, and completion messages. It is the main result of the first audit step.

## Large Module AST Split Audit

Use this tab when the Project Audit identifies an oversized Python file or when you need to understand whether one file can be separated safely.

### Target .py

Shows the Python file being studied. Validate Project can populate the list of oversized modules automatically. You may also browse to a specific Python file inside the active project.

### Copy Path

Copies the selected target file path.

### Browse Target

Opens a file chooser for a Python file. Do not select a file outside the active project root.

### Large modules count

Shows how many oversized files were found in the latest Project Audit Results.

### Previous and next arrows

Move through the oversized-module list without retyping paths.

### Run AST Split Audit

Performs a read-only syntax-tree analysis of the selected file. It studies functions, classes, imports, responsibilities, dependencies, and possible helper groups. It does not refactor the source file.

### Copy Split Handoff for AI

Copies a structured report for an AI. Use it after the AST audit finishes and before asking an AI to propose a split.

### Safety classifier

The AST heuristic classifier explains whether a suggested split looks safer or more risky based on the source structure. It is guidance, not automatic permission to change the file.

### Web AI risk repair

When available, this prepares a controlled Web AI review of the AST split evidence. It still does not automatically apply a refactor.

## Large File Refactor Planner

Use the Planner only after choosing one specific large Python file. It turns audit evidence into a proposed plan while keeping separate deterministic, Local AI, and imported Web AI versions.

### Target and settings

The Planner shows the selected target file and settings such as Ideal, Max, and Min helper sizes. These are planning boundaries, not instructions to compress code unnaturally.

### Analysis evidence panel

Displays what the Planner learned about the file: symbols, responsibilities, dependencies, and possible groups.

### Proposed split plan panel

Displays a proposed facade-and-helper arrangement. It is a plan, not a source-code change.

### Analyze File

Reads the selected file and builds deterministic planning evidence.

### Generate Split Plan

Creates the deterministic split plan from the collected evidence.

### Generate Docstring Plan

Plans documentation updates that would be needed if functions or classes move.

### Review and Refine Plan with Local AI

Uses the configured Local AI to review the deterministic plan. The Local AI version remains separate so it cannot silently replace the deterministic version.

### AI Refactor Version How To

Explains how the different planning versions work and how to compare them.

### Copy Comprehensive Planning for Web AI

Copies a complete planning packet for a Web AI conversation. This is useful when the external AI needs the target, evidence, constraints, and current plan together.

### Review Imported Web AI Version

Checks a Web AI proposal that you pasted or imported. Review happens before the version can be adopted.

### Show Planning Summary

Shows the status of each stage and each available planning version.

## Large File Refactor WorkBench

The WorkBench is the advanced staged area. It starts from an accepted Planner plan. Follow the stages in order because later buttons remain disabled until earlier evidence exists.

### 1. Plan Intake from Large File Refactor Planner

- Load Latest Planner Plan: transfers the latest plan into WorkBench ownership.
- Recheck Source Hash: confirms that the source file has not changed since the plan was created.

If the hash changed, return to the Planner and create a fresh plan.

### 2. Dependency and Scope Readiness

Analyze Dependency Readiness checks whether the proposed moved groups and their dependencies are sufficiently understood. This stage is read-only.

### 3. Real Moved-Code Preview Generation

Generate Real Preview creates real facade and helper preview files under governed project-support storage. It does not write active project source.

### 4. Structural Validation

Validate Real Preview checks structure, imports, symbol placement, and migration evidence. A structural pass does not automatically prove full behavior equivalence.

### Advanced Quality Review

After structural validation, the advanced review checks the candidate more deeply. Follow the visible status and correction controls. Do not skip forward because later stages depend on this evidence.

### 6. Preflight Backup and Source Payload

- Prepare Preflight Backup Readiness: prepares recovery evidence and proves that a safe backup path is available.
- Build Source Apply Payload: builds the exact source-ready payload but still does not apply it.

The current workflow continues to a separate completion review and authorization step. Do not treat source-payload creation as permission to modify the project.

### Stage correction controls

Each WorkBench stage may offer correction actions. They operate on that stage's evidence. Read the result and rerun the stage before moving forward.

## Engineering Safety

Engineering Safety is the second main tab inside Audit Project. It contains broader quality and safety checks, including full audits and focused audits. Use it when you need to inspect issues such as source hygiene, unsafe commands, architecture safety, test protection, public interfaces, or project-wide engineering risks.

For a first run:

1. Confirm the shared Project root.
2. Choose the broad or focused audit that matches your need.
3. Run the audit.
4. Read the findings and evidence before applying any repair.
5. Use the dedicated Engineering Safety Help page for every control in that section.

## Workflow Review

Workflow Review is the third main tab. It checks whether a project workflow has complete steps, correct connections, expected artifacts, and validation coverage.

For a first run:

1. Confirm the shared Project root.
2. Select or load the workflow to review.
3. Run the deterministic review.
4. Read missing-step, contract, and evidence findings.
5. Use the dedicated Workflow Review Help page for its detailed controls.

## Understanding paths

Project root is the folder of the project being audited. Audit Project uses it to prevent the tools from studying or writing into the wrong project.

Evidence and preview artifacts may be created in project-support or daily-work folders outside active project source. This separation protects the project: reports, previews, temporary files, and AI exchanges should not be mistaken for canonical source code.

## What is safe for a first-time user

Recommended:

- validate mode.
- Save Audit Results.
- Copy Audit Results.
- AST Split Audit on one selected file.
- Planner analysis and plan generation.
- Read-only WorkBench stages in order.

Advanced or higher risk:

- write mode.
- warning resolver actions that propose file changes.
- imported AI refactor versions.
- source payload and later authorization stages.

When unsure, stop after copying or saving the evidence and ask for review.

## Success checkpoints

A normal Architecture Review should show a completion message and an audit report. A large-file workflow should show a current target, current source hash, completed stage evidence, and enabled next-stage button.

Do not continue when you see:

- wrong Project root.
- missing target file.
- stale source hash.
- cancelled or incomplete operation.
- output from an older project.
- a disabled next-stage button.
- a warning that current validation evidence is missing.

## Common mistakes

- Starting in write mode instead of validate.
- Clearing results before copying or saving them.
- Asking AI to fix warnings without providing the audit output.
- Selecting a target outside the active project.
- Skipping the Planner and trying to start in WorkBench.
- Treating a structural pass as proof that behavior is unchanged.
- Assuming an AI review is more authoritative than deterministic audit evidence.

## Complete beginner example

1. Open Audit Project.
2. Open Architecture Review and Check Update Architecture.
3. Confirm Project root.
4. Select validate.
5. Click Validate Project.
6. Copy and save the results.
7. If the report names a large Python module, open Large Module AST Split Audit.
8. Select that module and run the AST audit.
9. Copy the AI handoff if expert help is needed.
10. Open Large File Refactor Planner only when you deliberately want a plan for that file.
11. Generate and review the plan.
12. Use WorkBench only after the plan is current and accepted.
13. Stop before any source-writing or authorization stage unless validation, backup, and human approval are complete.

## Authority boundary

Audit Project diagnoses, explains, plans, and prepares evidence. It does not make every warning mandatory, does not make AI authoritative, and does not automatically grant permission to change or freeze the project.
