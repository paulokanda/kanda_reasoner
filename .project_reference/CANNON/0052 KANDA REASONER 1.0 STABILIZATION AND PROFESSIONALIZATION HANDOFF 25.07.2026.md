# KANDA REASONER 1.0 STABILIZATION AND PROFESSIONALIZATION HANDOFF

## 1. Project context

KANDA Reasoner is a Windows desktop application for governed AI-assisted software development.

Its strongest differentiator is not simply access to AI models. Its differentiator is the governance layer surrounding project understanding and modification, including:

* Project/tool root separation.
* Box ownership and architectural boundaries.
* No-Leak rules.
* Architecture Review.
* Workflow Review.
* Error Memory.
* Freeze Memory.
* Project handoff generation.
* Source archive generation.
* Patch delivery and validation.
* Human-confirmed Preview and Confirm-and-Write workflows.
* Local AI and Web AI integrations.
* Project visualization and navigation tools.

The application already has substantial engineering depth. The current problem is not a shortage of features.

The current problem is that the system is more mature as an internal engineering laboratory than as a polished, reproducible, distributable professional product.

The next major project phase must therefore prioritize:

1. Runtime reliability.
2. Release reproducibility.
3. Installation simplicity.
4. End-to-end validation.
5. Product clarity.
6. New-user usability.
7. Documentation.
8. Operational security and support.
9. Simplification of duplicated or unclear ownership.
10. Regression prevention.

## 2. Governing strategic decision

Do not expand KANDA Reasoner with new major intelligence systems unless a demonstrated real-world limitation proves that the existing system cannot solve the problem adequately.

Do not create the following merely because they appear useful:

* A new project intelligence foundation.
* A duplicate symbol indexer.
* Another project graph engine.
* Another AI-context JSON format.
* Another risk-radar engine.
* Another Error Memory layer.
* Another prompt registry.
* Another architecture scanner.
* Another generalized reasoning engine.
* Additional GUI tabs without a verified product need.

The direction is now:

> Quality, reliability, simplification, and productization rather than expansion.

Any proposed new subsystem must first answer:

1. What verified problem exists?
2. Which current owner is unable to solve it?
3. Why can the existing owner not be improved?
4. What duplicated responsibility would the new subsystem introduce?
5. How will the new subsystem be validated and maintained?

## 3. Product positioning

The recommended product definition is:

> KANDA Reasoner is a safety and governance workspace for AI-assisted software development. It helps developers understand, modify, validate, and preserve software projects while preventing AI tools from silently damaging architecture, project boundaries, or governed project state.

The product should not present itself primarily as another generic AI coding chat.

Its primary user journeys should become:

1. Understand a project.
2. Plan a safe change.
3. Apply or review a change.
4. Validate the resulting project.
5. Preserve verified knowledge, errors, and frozen behavior.
6. Ask AI questions using governed project context.

The GUI may retain advanced tools, but the product should guide the user through these journeys rather than exposing an unstructured collection of capabilities.

## 4. Primary objective

Deliver a stable KANDA Reasoner 1.0 local Windows application that an independent developer can install, open, understand, validate, and use without relying on prior chat history or direct guidance from the original developer.

The professionalization milestone is reached only when:

* A clean Windows environment can install the application through one documented process.
* The user does not need to locate or invoke Python manually.
* The installed application reliably launches.
* All visible tabs can be opened in a real PySide6 runtime.
* One authoritative release validation command verifies the complete product.
* Product documentation is sufficient for an independent developer.
* Failures produce understandable diagnostics.
* Releases have versions, checksums, dependency identities, release notes, and rollback instructions.
* Visual and runtime behavior is verified through real application tests rather than static source inspection alone.
* No known critical architecture or workflow errors remain.

## 5. Critical lesson from recent regressions

Recent icon-related work demonstrated an important systemic weakness.

Several patches passed focused validation but still caused real application failures:

* The icon asset existed, but the application resolved a different path.
* A validator contained hidden control characters and failed before testing the feature.
* A patch removed `_PROJECT_ROOT`, although unchanged modules still imported it.
* Local feature validation did not sufficiently protect the complete application import surface.

These failures show that KANDA Reasoner has many strong focused validators but lacks one authoritative whole-product release gate.

The central professionalization requirement is:

> When final release validation passes, the installed application must start and its critical workflows must operate.

Focused validators remain valuable, but they must become components of a higher-level release decision.

## 6. Non-goals for this phase

The following are explicitly outside the initial stabilization scope:

* New AI providers unless required to repair an existing provider workflow.
* New project-analysis engines.
* New visualization engines.
* New memory systems.
* New prompt-library architectures.
* Cloud SaaS conversion.
* Team collaboration features.
* Enterprise account management.
* Marketplace or plugin ecosystem.
* Large UI redesign before runtime stabilization.
* Automatic removal of human confirmation gates.
* Automatic Freeze Memory writing without explicit confirmation.
* Replacing established Box, No-Leak, Error Memory, or Freeze governance.

## 7. Implementation principles

All implementation must follow these principles.

### 7.1 Exact-source inspection

Do not modify code based only on manifests, reports, handoff summaries, or assumptions.

Inspect the exact current source files and all known consumers before changing a public or private symbol.

### 7.2 Preserve existing contracts

Before renaming, deleting, moving, or replacing a symbol:

* Search all source consumers.
* Search tests and validators.
* Search dynamic imports and string references.
* Search help documentation.
* Search release and freeze metadata.
* Search Error Memory for relevant prior regressions.

Private symbols may still be active compatibility contracts.

### 7.3 Whole-application confidence

A focused validator cannot be treated as final release evidence.

Every feature patch must eventually feed into the complete application release validation.

### 7.4 Fail closed

Validation must fail when evidence is missing, stale, mismatched, incomplete, or generated from the wrong project root.

### 7.5 Human confirmation

Preserve explicit human confirmation for governed writes, including Freeze Memory and Error Memory operations.

### 7.6 Minimal ownership

Every capability must have one canonical owner.

Do not create a second owner because modifying the first owner appears inconvenient.

### 7.7 Professional Python quality

For new or touched source modules:

* Use Python 3.12-compatible code unless the project formally changes its supported runtime.
* Preserve PEP 8 formatting.
* Prefer cohesive modules.
* Keep code modules at or below 500 physical lines.
* Do not compress logic to remain under the line limit.
* Split responsibilities using clear public contracts.
* Avoid circular imports.
* Avoid hidden mutable state.
* Avoid private cross-box reach-in.

### 7.8 Windows-first behavior

The primary target is Windows.

All paths, launch behavior, taskbar identity, Qt runtime tests, packaging, dependency resolution, and installer behavior must be tested on Windows.

## 8. Workstream A: authoritative end-to-end release validation

### Objective

Create one canonical release-validation entry point that determines whether KANDA Reasoner is safe to release.

### Required capabilities

The release validator must:

1. Confirm the active project root and KANDA tool root.
2. Confirm the expected Python runtime identity.
3. Confirm dependency availability and versions.
4. Compile all Python source files.
5. Import the main application entry point.
6. Import every visible GUI tab and its immediate dependency surface.
7. Instantiate the real QApplication.
8. Instantiate the real main window.
9. Confirm the application icon path and icon loading.
10. Open every visible tab at least once.
11. Exercise one minimal safe operation in every critical workflow.
12. Capture stderr, stdout, Qt messages, Python exceptions, and thread failures.
13. Detect unresolved worker threads during shutdown.
14. Close the main window cleanly.
15. Restart the application in a second process or isolated runtime.
16. Confirm persistent settings can be loaded.
17. Run Architecture Review.
18. Run Workflow Review.
19. Run required focused validators.
20. Produce a structured release report.
21. Produce one final release status.

### Suggested command

A future canonical command should resemble:

```powershell
powershell -ExecutionPolicy Bypass -File E:\kanda_reasoner\RELEASE_VALIDATE.ps1
```

The exact command and location must be decided through current project ownership rules.

### Required final markers

The final runner should produce clear markers such as:

```text
PYTHON_RUNTIME_IDENTITY: PASS
DEPENDENCY_LOCK: PASS
SOURCE_COMPILE: PASS
APPLICATION_IMPORT: PASS
MAIN_WINDOW_CREATE: PASS
VISIBLE_TAB_IMPORTS: PASS
VISIBLE_TAB_OPEN_SEQUENCE: PASS
CRITICAL_WORKFLOW_SMOKE: PASS
THREAD_SHUTDOWN: PASS
APPLICATION_RESTART: PASS
ARCHITECTURE_ERRORS_ZERO: PASS
WORKFLOW_ERRORS_ZERO: PASS
FOCUSED_VALIDATORS: PASS
RELEASE VALIDATION: PASS
```

### Failure behavior

A failure must report:

* Stage.
* Exception type.
* Exception message.
* Relevant source path.
* Relevant symbol.
* Captured traceback.
* Python executable.
* Project root.
* Application version.
* Suggested next diagnostic command.

Do not output only a generic `VALIDATION ERROR`.

### Acceptance criteria

* The validator detects a missing imported symbol such as `_PROJECT_ROOT`.
* The validator detects an invalid icon path.
* The validator detects a visible tab import failure.
* The validator detects a QThread lifecycle failure.
* The validator detects a failed QApplication or main-window construction.
* The validator detects hidden control characters in PowerShell files.
* The validator passes only when the real application can start and shut down successfully.

## 9. Workstream B: test architecture

### Objective

Establish a clear testing pyramid rather than relying mainly on feature-specific scripts.

### Required layers

#### Layer 1: static source checks

Examples:

* Syntax and compilation.
* Forbidden imports.
* Circular dependency detection.
* Box-boundary checks.
* Module-size checks.
* Control-character detection.
* Generated-file/source-owner checks.
* Absolute-path detection.
* Secret-pattern detection.

#### Layer 2: unit tests

Examples:

* Root-resolution functions.
* Path normalization.
* Manifest parsing.
* Error Memory normalization.
* Freeze Hint parsing.
* Source routing.
* Configuration resolution.
* Project/tool boundary functions.

#### Layer 3: integration tests

Examples:

* Tab controller and service interactions.
* Local AI request lifecycle.
* Web AI credential loading.
* Error Memory correction and reparse.
* Freeze intake and readiness.
* Project handoff creation.
* Source archive selection.
* Architecture Review orchestration.

#### Layer 4: real Qt tests

Examples:

* Main-window creation.
* Tab construction.
* Signal lifecycle.
* Widget destruction and reconstruction.
* Dropdown opacity.
* Taskbar and title-bar icon.
* Background action completion.
* QWebEngine readiness.
* Thread termination.

#### Layer 5: end-to-end release smoke

The full installed application must be launched from the same mechanism that a normal user will use.

### Acceptance criteria

* Every existing focused validator is categorized into one of these layers.
* Duplicate validators are consolidated.
* Each regression lesson has one canonical validator or test owner.
* Tests can run from a clean environment.
* Test failures are machine-readable and human-readable.

## 10. Workstream C: reproducible dependency management

### Objective

Make the Python runtime and dependency set explicit and reproducible.

### Required work

* Establish the canonical Python version.
* Create a canonical `pyproject.toml` or equivalent package configuration.
* Create a locked dependency set.
* Separate runtime dependencies from development dependencies.
* Record PySide6, QWebEngine, and other sensitive dependency versions.
* Define upgrade procedures.
* Add a dependency validation command.
* Ensure the application does not silently select an unrelated Miniconda or PATH Python.
* Confirm the exact interpreter used by installers, validators, and launchers.

### Acceptance criteria

* A fresh environment can reproduce the application.
* The exact dependency versions are identifiable.
* The selected Python executable is shown in diagnostics.
* Dependency drift is detected before release.
* No release depends on undeclared locally installed packages.

## 11. Workstream D: professional Windows packaging

### Objective

Allow normal users to install and launch KANDA Reasoner without invoking Python manually.

### Target options

Evaluate and choose one primary distribution method:

* Signed Windows installer.
* Portable Windows package.
* Self-contained executable bundle.
* Proper Python package plus managed launcher.

A developer installation may remain available separately.

### Required installer behavior

* Install to a predictable location.
* Create a Start Menu entry.
* Create an optional desktop shortcut.
* Register the correct application icon.
* Register a stable Windows AppUserModelID.
* Preserve user data during upgrades.
* Support clean uninstall.
* Show the installed application version.
* Avoid requiring administrator rights when possible.
* Avoid exposing staging folders and patch internals to normal users.

### Acceptance criteria

* Application launches from the Start Menu.
* Application launches without a manually selected Python path.
* Top-left window icon is correct.
* Windows taskbar icon is correct.
* Uninstall removes application files but preserves or clearly handles user data.
* Reinstall and upgrade paths are tested.
* The installed package passes the authoritative release validation.

## 12. Workstream E: product versioning and release lifecycle

### Objective

Create a recognizable and auditable product release process.

### Required artifacts

* Application semantic version.
* Build identifier.
* Release date.
* Changelog.
* Release notes.
* Dependency lock identity.
* ZIP or installer checksum.
* Validation report.
* Known issues.
* Upgrade instructions.
* Rollback instructions.
* Freeze metadata.
* Source commit or source fingerprint.

### Suggested version model

```text
MAJOR.MINOR.PATCH
```

Examples:

* `1.0.0` for the first professional stable release.
* `1.0.1` for a backward-compatible defect correction.
* `1.1.0` for a backward-compatible feature release.
* `2.0.0` for a breaking architecture or data-model change.

Patch ZIP revision names may remain internal but should map clearly to the application version.

### Acceptance criteria

* The GUI shows the application version.
* Diagnostic bundles include the version.
* Validation reports include the version.
* Every distributable artifact has a checksum.
* Every release can be traced to exact source and validation evidence.

## 13. Workstream F: CI and clean-environment validation

### Objective

Prevent local-machine success from being mistaken for release readiness.

### Required pipeline

At minimum, the CI or controlled release environment should:

1. Create a clean Windows environment.
2. Install the governed Python runtime.
3. Install locked dependencies.
4. Install KANDA Reasoner.
5. Run static validation.
6. Run unit tests.
7. Run integration tests.
8. Run real Qt smoke tests.
9. Run the complete release validator.
10. Build the distributable artifact.
11. Validate the built artifact.
12. Generate checksums and reports.

### Required protections

* No developer-specific absolute paths.
* No dependency on `E:\kanda_reasoner`.
* No hidden requirement for PyCharm.
* No dependence on a previously running parent process.
* No use of untracked local configuration.
* No use of generated artifacts as canonical source.
* No silent network dependency during offline validation.

### Acceptance criteria

* The pipeline can reproduce a passing release from a clean checkout or canonical source package.
* Failures prevent artifact publication.
* Published artifacts are the exact artifacts that passed validation.
* The release report is retained as durable evidence.

## 14. Workstream G: user experience and information architecture

### Objective

Make KANDA Reasoner understandable without requiring the user to know the internal architecture in advance.

### Recommended primary navigation

The user-facing structure should emphasize workflows:

#### Understand

* Project overview.
* Brain Navigator.
* Architecture Review.
* Workflow Review.
* Project Structure visualization.

#### Change

* Change planning.
* AI-assisted analysis.
* Local AI.
* Web AI.
* Prompt Library.

#### Validate

* Validation center.
* Architecture errors.
* Workflow errors.
* Release readiness.
* Diagnostics.

#### Preserve

* Error Memory.
* Freeze Feature After Update.
* Project handoff.
* Durable evidence.

#### Configure

* AI providers.
* Project selection.
* Exclusion rules.
* Application settings.

This is a conceptual recommendation. Do not reorganize tabs before confirming current ownership and dependencies.

### Required UX improvements

* Clear home/dashboard screen.
* Current project identity always visible.
* Current tool root and project root visible when relevant.
* Application version visible.
* Last validation status visible.
* Last successful validation time visible.
* Clear distinction between Preview and Write actions.
* Clear distinction between local and web AI.
* Clear warnings before external data transmission.
* Unified status and notification behavior.
* Consistent button labels.
* Consistent busy-state handling.
* Searchable help.
* Direct access to diagnostics.

### Acceptance criteria

A new user can answer these questions within the interface:

* Which project is active?
* What can KANDA Reasoner do?
* What should I do first?
* Is the project currently valid?
* What did the last operation change?
* Was anything written to the project?
* Was any content sent to an external AI?
* How can I undo or diagnose a failure?

## 15. Workstream H: onboarding

### Objective

Allow an independent developer to complete a useful workflow without prior chat context.

### Required onboarding flow

The first-run experience should:

1. Explain what KANDA Reasoner is.
2. Ask the user to select or create a project configuration.
3. Explain project root versus KANDA tool root.
4. Run a safe project scan.
5. Show the project overview.
6. Guide the user through one read-only AI or architecture task.
7. Show how validation works.
8. Explain Preview versus Confirm-and-Write.
9. Explain Error Memory and Freeze Memory.
10. Offer an example project or tutorial mode.

### Required documentation

* README.
* Installation guide.
* Five-minute quick start.
* First-project tutorial.
* Architecture overview.
* Validation guide.
* Troubleshooting guide.
* Privacy and security guide.
* AI-provider configuration guide.
* Error Memory guide.
* Freeze workflow guide.
* Glossary.
* Release notes.
* Known limitations.

### Acceptance criteria

An independent developer can:

* Install the product.
* Open it.
* Select a project.
* Run a safe read-only analysis.
* Interpret the result.
* Run validation.
* Locate diagnostics.
* Exit without assistance.

## 16. Workstream I: diagnostics and supportability

### Objective

Make failures understandable and supportable without exposing sensitive data.

### Required diagnostic bundle

Add a controlled diagnostic export containing:

* Application version.
* Python version and executable.
* Operating system version.
* Dependency versions.
* Active project slug.
* Redacted project root information when appropriate.
* Recent application logs.
* Recent validation report.
* Recent exception tracebacks.
* Active tab or workflow.
* Thread-state summary.
* Configuration identities without secrets.
* Relevant source fingerprints.
* Error Memory lesson IDs that were applied.
* Freeze state summary.

### Redaction requirements

The diagnostic bundle must not include:

* API keys.
* Authentication tokens.
* Full private prompts unless explicitly approved.
* Full source files unless explicitly selected.
* Patient or medical information.
* User credentials.
* Raw environment-variable secrets.

### Acceptance criteria

* A user can generate one diagnostic ZIP from the GUI.
* The bundle clearly states what it contains.
* Secret scanning passes before export.
* Support can identify the failed stage from the bundle.

## 17. Workstream J: security and privacy

### Objective

Make local-versus-external data handling explicit and testable.

### Required work

* Document what remains local.
* Document what may be sent to Web AI.
* Show a preflight summary before external transmission.
* Allow the user to inspect the outgoing request.
* Preserve session-only credential behavior where intended.
* Avoid logging secrets.
* Define retention for local conversation history.
* Define deletion behavior.
* Define project exclusion behavior.
* Validate that excluded paths are not transmitted.
* Validate that project/tool boundaries are preserved.
* Add secret-pattern scanning to release and diagnostic flows.

### Acceptance criteria

* External transmission requires an explicit user action.
* The user can inspect the data boundary.
* API keys are never shown in logs.
* Exclusion rules are enforced by tests.
* Local AI remains clearly distinguishable from Web AI.
* Privacy behavior is documented.

## 18. Workstream K: state and migration management

### Objective

Prevent application upgrades from corrupting or silently invalidating saved state.

### State types to inventory

* Application preferences.
* Project configuration.
* Prompt-library metadata.
* Error Memory.
* Freeze Memory.
* AI conversation history.
* Validation history.
* Handoff configuration.
* Exclusion rules.
* Provider configuration.
* User interface state.

### Required work

* Identify canonical owner and schema version for each state type.
* Add schema-version fields where missing.
* Add migration functions.
* Add backup-before-migration behavior.
* Add rollback or recovery behavior.
* Test upgrade from at least one prior supported version.
* Detect unsupported future schema versions.
* Avoid silently discarding unknown fields.

### Acceptance criteria

* An upgrade preserves supported state.
* Failed migration restores the backup.
* Migration logs are available.
* Old and new schema tests exist.
* Project-specific state is never written under the wrong project.

## 19. Workstream L: architecture and ownership simplification

### Objective

Reduce fragility caused by duplicated responsibilities, compatibility ambiguity, and indirect ownership.

### Required audit

For every major capability, document:

* Canonical owner module.
* Public facade.
* Private implementation modules.
* Known consumers.
* Persistent state owner.
* Validator owner.
* Help/documentation owner.
* Release contract owner.
* Error Memory lessons.
* Freeze Memory entry.
* Deprecated predecessors.

### Priority audit targets

* Application root resolution.
* Project root resolution.
* Application icon ownership.
* Main-window launch.
* Tab registration.
* Local AI controllers.
* Web AI controllers.
* Error Memory parsing.
* Freeze readiness.
* Project handoff generation.
* Source archive generation.
* Validation orchestration.
* Prompt-library routing.
* Architecture Review integration.
* Workflow Review integration.

### Acceptance criteria

* Every major capability has one canonical owner.
* Deprecated owners are removed or explicitly shimmed.
* Compatibility shims are tested.
* No generated file acts as canonical source.
* No duplicated scanner or registry remains without justification.
* Ownership documentation matches the current source.

## 20. Workstream M: product documentation versus internal governance documentation

### Objective

Separate normal-user documentation from developer and governance internals.

### Documentation layers

#### User documentation

Focused on:

* Installation.
* Starting the application.
* Selecting a project.
* Core workflows.
* Safety and privacy.
* Troubleshooting.

#### Developer documentation

Focused on:

* Architecture.
* Boxes.
* Public contracts.
* Testing.
* Building.
* Releasing.
* State migrations.

#### Governance documentation

Focused on:

* Error Memory.
* Freeze Memory.
* Patch delivery.
* No-Leak logic.
* Source ownership.
* Startup routing.
* AI handoff rules.

The normal user should not be required to understand all governance mechanics before obtaining value.

### Acceptance criteria

* Each document has a clear audience.
* User documentation avoids unnecessary internal terminology.
* Governance rules remain complete and authoritative.
* Duplicate explanations are consolidated.

## 21. Recommended implementation order

Do not attempt all workstreams simultaneously.

### Phase 0: establish baseline

Deliverables:

* Current version identifier.
* Exact source baseline.
* Current dependency inventory.
* Current architecture and workflow validation.
* Current tab inventory.
* Current validator inventory.
* Current known-issues list.
* Current Error Memory applicability map.
* Current state-schema inventory.

No product behavior should change in this phase unless required to restore a broken baseline.

### Phase 1: runtime stabilization

Priorities:

1. Restore reliable application launch.
2. Build application import smoke tests.
3. Build main-window construction tests.
4. Build visible-tab import and opening tests.
5. Fix known startup and lifecycle failures.
6. Establish clean shutdown testing.
7. Add complete traceback capture.

Exit criteria:

* Application launches and closes reliably.
* All visible tabs load.
* No critical runtime traceback remains.

### Phase 2: authoritative release validator

Priorities:

1. Create release runner.
2. Integrate focused validators.
3. Add real Qt smoke.
4. Add restart test.
5. Add structured report.
6. Add final release status.

Exit criteria:

* One command provides credible whole-product release confidence.

### Phase 3: dependency and packaging

Priorities:

1. Canonical dependency declaration.
2. Dependency lock.
3. Governed runtime identity.
4. Windows packaging prototype.
5. Start Menu and icon behavior.
6. Install, upgrade, uninstall, and rollback tests.

Exit criteria:

* A clean Windows environment can install and launch the product without manual Python invocation.

### Phase 4: product UX and onboarding

Priorities:

1. Product home/dashboard.
2. Workflow-oriented navigation.
3. First-run experience.
4. Help system.
5. Five-minute quick start.
6. Example project.

Exit criteria:

* An independent developer can complete one useful workflow without assistance.

### Phase 5: CI and release automation

Priorities:

1. Clean Windows build environment.
2. Automated test layers.
3. Artifact generation.
4. Artifact validation.
5. Checksum and report publication.
6. Release blocking on failure.

Exit criteria:

* Published artifacts are reproducible and are exactly the artifacts that passed validation.

### Phase 6: operational hardening

Priorities:

1. Diagnostic bundle.
2. Security and privacy documentation.
3. State migrations.
4. Update mechanism.
5. Support workflow.
6. Retention and deletion rules.

Exit criteria:

* The application can be safely maintained and supported after release.

### Phase 7: independent usability review

Recruit at least one developer who has not participated in the project.

Ask that person to:

1. Install the application.
2. Open a sample project.
3. Run an analysis.
4. Interpret the output.
5. Run validation.
6. Export diagnostics.
7. Upgrade or reinstall.
8. Report confusion and failures.

Do not explain the product during the test unless the documentation instructs the user to ask for support.

Exit criteria:

* The independent user can complete the workflow using only the product and documentation.

## 22. Definition of done for KANDA Reasoner 1.0

KANDA Reasoner 1.0 is ready only when all statements below are true.

### Installation

* One supported installation path is documented.
* Installation works on a clean Windows environment.
* The application launches without manual Python commands.
* Application icon and taskbar identity are correct.
* Uninstall and reinstall work.

### Runtime

* Main application starts without traceback.
* All visible tabs open.
* Critical workflows complete minimal smoke operations.
* Application closes without hanging worker threads.
* Application restarts successfully.

### Validation

* One authoritative release command exists.
* Focused validators are integrated.
* Architecture errors are zero.
* Workflow errors are zero.
* Real Qt validation passes.
* The built artifact itself is validated.

### Documentation

* README exists.
* Installation guide exists.
* Quick start exists.
* Architecture guide exists.
* Validation guide exists.
* Troubleshooting guide exists.
* Privacy and security guide exists.
* Release notes exist.

### Product usability

* Active project identity is clear.
* Current validation state is clear.
* Preview and write operations are distinguishable.
* Local and Web AI are distinguishable.
* The first useful workflow is guided.
* Errors provide actionable information.

### Release management

* Version is visible.
* Dependencies are locked.
* Artifact checksums are available.
* Validation evidence is retained.
* Upgrade and rollback are documented.
* Known issues are documented.

### Security

* Secrets are not logged.
* External transmissions are explicit.
* Exclusion rules are tested.
* Diagnostic bundles are redacted.
* State retention and deletion are defined.

### Independence

* A developer unfamiliar with the project can install and operate it using documentation alone.

## 23. Required behavior for the implementing AI

Before proposing code:

1. Complete the normal startup pack load.
2. Complete the project-ready handoff load.
3. Read compact Error Memory.
4. Open full Error Memory only when required.
5. Classify the requested subtask.
6. Select the smallest relevant prompt and Box owner set.
7. Inspect exact source.
8. Identify all affected consumers.
9. Identify current validators.
10. Produce an Error Memory regression matrix when lessons apply.

Before changing code:

* State the active Box.
* State canonical owner paths.
* State allowed files.
* State out-of-scope files.
* State cross-box touches.
* State public and private compatibility contracts.
* State validation scope.
* State rollback plan.

Before delivering a patch:

* Run package-side validation.
* Run static source checks.
* Run focused tests.
* Run the whole-application import smoke.
* Run real Qt validation when GUI behavior is affected.
* Run ZIP contract validation.
* Include root-level `KANDA_FREEZE_HINT.json` for freezeable patches.
* Generate Freeze Hint and freeze-form data from the same payload source.
* Do not claim local Windows visual confirmation unless it was actually performed.

After installation:

* Require local validation.
* Require application launch testing.
* Require visual confirmation for visual changes.
* Require explicit human Preview and Confirm-and-Write for Freeze.
* Refresh startup freeze context after a successful local freeze write.

## 24. Immediate next task

The first implementation task should be:

> Build a read-only KANDA Reasoner 1.0 stabilization baseline and release-readiness audit.

It must not modify production behavior.

The audit should produce:

1. Current application version state.
2. Current launch entry points.
3. Full visible-tab inventory.
4. Full tab import dependency map.
5. Current dependency inventory.
6. Current test and validator inventory.
7. Current release and installer inventory.
8. Current documentation inventory.
9. Current state-schema inventory.
10. Current critical-workflow inventory.
11. Current known runtime failures.
12. Current duplicated ownership findings.
13. Current absolute-path and developer-machine assumptions.
14. Current CI readiness.
15. Proposed authoritative release-validator architecture.
16. Prioritized stabilization backlog.
17. Risk-ranked implementation sequence.

The audit must clearly separate:

* Verified source facts.
* Runtime evidence.
* Inferences.
* Missing evidence.
* Recommended changes.

Do not begin product restructuring, packaging, or broad refactoring until this baseline audit is complete and reviewed.

## 25. Final project direction

KANDA Reasoner already contains enough conceptual and technical depth to become a distinctive professional developer product.

Its next stage is not to become larger.

Its next stage is to become:

* Predictable.
* Reproducible.
* Installable.
* Understandable.
* Testable.
* Supportable.
* Secure.
* Independently usable.

The guiding standard is:

> Reduce the distance between “the validator says it works” and “the user opens the application and it simply works.”
