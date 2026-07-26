# KANDA REASONER MINIMUM PROFESSIONAL VERSION HANDOFF

## 1. Purpose

Transform the existing KANDA Reasoner application into a dependable professional local Windows tool with the smallest reasonable implementation scope.

This is not a commercial release program.

This is not a SaaS conversion.

This is not a broad product redesign.

The target is:

> A stable local application that the owner can launch normally, validate with one command, reproduce on another Windows environment, and troubleshoot through clear logs and basic documentation.

## 2. Product level being targeted

This handoff targets:

> Professional internal tool / reusable local developer workbench.

It does not yet target:

* Public commercial distribution.
* Paying external customers.
* Enterprise support.
* Automatic updates.
* Team collaboration.
* Account management.
* Cloud infrastructure.
* Formal telemetry.
* Full customer-support diagnostics.

## 3. Governing decision

KANDA Reasoner already has enough functional depth.

Do not add:

* New AI engines.
* New project-intelligence engines.
* New scanners.
* New graphs.
* New prompt systems.
* New memory systems.
* New tabs.
* New workflow abstractions.
* New release-governance layers.

Professionalization must come from making existing functionality dependable.

The minimum professional milestone consists of five outcomes:

1. Reliable launch and shutdown.
2. One authoritative smoke validator.
3. Reproducible Python environment.
4. Portable Windows application package.
5. Basic versioning, logs, and documentation.

Anything beyond these five outcomes is deferred unless it is required to make one of them work.

## 4. Source and evidence gate

Before performing any baseline audit or implementation:

1. Load the KANDA startup pack.
2. Load the second project handoff pack.
3. Read compact Error Memory.
4. Confirm the collector completed successfully.
5. Inspect the exact current source archive.
6. Inspect the actual application registry and entry points.
7. Do not guess filenames, tabs, dependencies, or existing validators.

When source is unavailable, the AI may audit this specification only.

It must not produce a fictional project baseline containing phrases such as:

* “likely entry point”
* “possibly no pyproject”
* “typical tabs”
* “assume no tests”
* “common symptoms”
* “likely hardcoded paths”

Unknown facts must remain marked as unknown until exact source is inspected.

## 5. Minimum outcome 1: reliable launch

### Objective

KANDA Reasoner must start, display its complete visible interface, close, and reopen without a traceback.

### Required behavior

The application must:

* Start from its canonical launcher.
* Resolve the KANDA tool root correctly.
* Resolve the selected active project separately.
* Import the main window.
* Construct the real `QApplication`.
* Construct the real main window.
* Load or instantiate every visible tab.
* Display its application icon.
* Close without leaving active worker threads.
* Start successfully a second time.

### Required source inspection

Before modifying launch behavior, inspect at least:

* Root public launcher.
* GUI shell launcher.
* Main-window owner.
* Application constants.
* Tool/tab registry.
* Lazy-tab loader.
* Project-root resolver.
* Window-state owners.
* Every consumer of modified constants or compatibility symbols.

Do not delete, rename, or replace a public or private symbol before searching all current consumers.

### Acceptance markers

```text
APPLICATION_ENTRY_IMPORT: PASS
MAIN_WINDOW_CONSTRUCTION: PASS
VISIBLE_TAB_IMPORTS: PASS
VISIBLE_TAB_OPEN_SMOKE: PASS
APPLICATION_ICON_LOAD: PASS
CLEAN_SHUTDOWN: PASS
SECOND_LAUNCH: PASS
```

### Definition of success

A normal local launch produces no uncaught Python traceback.

The user can open every visible tab, close KANDA Reasoner, and immediately reopen it.

## 6. Minimum outcome 2: one smoke validator

### Objective

Provide one command that answers:

> Can the current KANDA Reasoner application start and operate at a basic level?

### Canonical scope

The smoke validator should have only these stages:

1. Source compilation.
2. Entry-point and visible-tab imports.
3. Real Qt main-window and tab-opening smoke.
4. Clean shutdown and final decision.

### Why source compilation remains

Importing the root launcher does not necessarily import every lazy-loaded source module.

A project-wide compile check is inexpensive and can detect syntax defects in modules that are not reached during the initial import.

It should remain one step inside the smoke validator, not become an independent feature or large subsystem.

### Proposed command

The final location must follow current ownership rules, but the user-facing command should resemble:

```powershell
powershell -ExecutionPolicy Bypass -File E:\kanda_reasoner\VALIDATE_APP.ps1
```

### Required behavior

The validator must:

* Report the Python executable.
* Report the Python version.
* Run `compileall` or an equivalent complete source compilation.
* Import the canonical launcher.
* Import every registered visible tab module.
* Create the real Qt application.
* Create the real main window.
* Open every visible tab.
* Process enough Qt events to expose immediate runtime failures.
* Close the window.
* Confirm worker-thread shutdown.
* Return a nonzero exit code on failure.
* Preserve the complete traceback.
* Print one final result.

### Minimum final markers

```text
SOURCE_COMPILE: PASS
APPLICATION_IMPORT: PASS
VISIBLE_TAB_IMPORTS: PASS
REAL_QT_SMOKE: PASS
CLEAN_SHUTDOWN: PASS
APPLICATION SMOKE VALIDATION: PASS
```

### Not required in this minimum validator

Do not initially require:

* Full Architecture Review.
* Full Workflow Review.
* Every feature-specific validator.
* Complete source-archive generation.
* Freeze preparation.
* Error Memory writing.
* Installer validation.
* Performance benchmarking.
* Large negative-fixture suites.

Those remain separate tools or later release checks.

### Initial regression fixtures

Test only failures already demonstrated in real work:

1. A required imported compatibility symbol is missing.
2. A script path contains an illegal hidden control character.
3. The application asset constant resolves to the wrong physical file.

Additional fixtures should be added only after a real failure demonstrates their value.

## 7. Minimum outcome 3: reproducible environment

### Objective

Make the Python environment explicit and reproducible without building an elaborate dependency-management program.

### Required artifacts

Use only:

```text
pyproject.toml
one dependency lock file
```

The lock may be implemented using the selected packaging workflow.

Do not initially create separate overlapping files for:

* Runtime requirements.
* Development requirements.
* Test requirements.
* Packaging requirements.
* Manual dependency inventories.

One canonical project configuration and one lock identity are enough for the minimum version.

### Required declarations

The environment must identify:

* Supported Python version.
* PySide6 version.
* Other runtime dependencies.
* Packaging dependencies where applicable.
* Application package name.
* Application version.
* Canonical launcher.

### Required runtime reporting

The smoke validator must print:

```text
Python executable:
Python version:
PySide6 version:
Qt version:
Application version:
```

### Acceptance criteria

* A fresh environment can install the declared dependencies.
* The application launches in that environment.
* The smoke validator passes.
* No undeclared local package is required.
* The runtime does not silently select an unrelated Python installation.

## 8. Minimum outcome 4: portable Windows package

### Objective

Allow KANDA Reasoner to start without the user manually invoking Python.

### Initial distribution target

Use a portable, self-contained one-folder Windows build as the first target.

A likely candidate may be a one-folder executable bundler, but the exact technology must be selected only after testing the current PySide6 and QWebEngine application.

Do not commit to a packaging technology from the handoff alone.

### Required behavior

The portable build must include:

* Application launcher.
* Python runtime or packaged runtime dependencies.
* Required Qt plugins.
* Required QWebEngine resources when applicable.
* Application icon.
* Application version.
* Required internal assets.
* Basic launch log.

### Minimum user experience

The user should be able to:

1. Extract or copy one application folder.
2. Double-click the KANDA Reasoner launcher.
3. Use the application.
4. Close and reopen it.

### Optional convenience

A simple script may create a desktop or Start Menu shortcut.

This is optional for the first minimum build.

### Explicitly deferred

Do not initially build:

* MSI package.
* Inno Setup installer.
* NSIS installer.
* Automatic upgrade system.
* Windows registry migration framework.
* Full uninstall workflow.
* Signed installer.
* Background updater.
* Differential patch updater.

### Acceptance criteria

The exact packaged folder must be tested, not only the source environment.

Required test:

```text
Clean environment
-> copy portable build
-> launch
-> open visible tabs
-> close
-> relaunch
-> PASS
```

## 9. Minimum outcome 5: version, logs, and documentation

### 9.1 Version

Add one canonical application version owner.

The version should be visible in one of:

* Window title.
* About dialog.
* Help panel.
* Main status area.

Use a simple version such as:

```text
0.9.0
```

during stabilization.

Use `1.0.0` only after all minimum acceptance criteria pass.

A git tag is sufficient initial release identity.

Formal release provenance is deferred.

### 9.2 Logs

Add or standardize one persistent application log.

The log must record:

* Application startup.
* Application version.
* Python executable.
* Active project root.
* Main-window construction.
* Tab-load failures.
* Uncaught exceptions.
* Worker-thread failures.
* Application shutdown.

Provide one visible action:

```text
Open Log Folder
```

or:

```text
Open Current Log
```

### Secret rule

API keys, tokens, and full credential values must never be written to the log.

This is required because KANDA Reasoner includes Web AI behavior.

### Diagnostics ZIP

A diagnostic ZIP exporter is deferred.

Do not create:

* Redaction pipelines.
* Fingerprint bundles.
* Thread-state export schemas.
* Error Memory diagnostic summaries.
* Support upload packages.

The log file and complete traceback are sufficient for the minimum professional version.

### 9.3 Documentation

Create one primary document:

```text
README.md
```

The README must contain:

1. What KANDA Reasoner is.
2. Supported Windows and Python environment.
3. Development launch instructions.
4. Portable build launch instructions.
5. Five-minute quick start.
6. How to select a project.
7. How to run the smoke validator.
8. Where logs are stored.
9. Five common troubleshooting cases.
10. A short Web AI privacy warning.
11. Current known limitations.

Separate documents may be added later only when the README becomes genuinely difficult to navigate.

### Minimum troubleshooting cases

Document:

* Application does not start.
* Wrong Python interpreter.
* Missing dependency.
* A visible tab fails to load.
* QWebEngine or Qt resource failure.
* Application icon is cached or missing.
* Where to find the complete traceback.

## 10. Features explicitly removed from the minimum scope

The following were present in the earlier handoff but are no longer minimum requirements.

### Deferred product features

* New home screen.
* Workflow-oriented navigation redesign.
* Complete visual redesign.
* New settings center.
* First-run wizard.
* Example project.
* Guided tutorial.
* Help buttons for every tab.

### Deferred release engineering

* CI pipeline.
* Clean hosted Windows runner.
* Signed installer.
* Artifact provenance framework.
* Software bill of materials.
* Formal checksums for every local build.
* Formal rollback documentation.
* Automatic updater.
* Migration framework.

### Deferred diagnostics

* Diagnostic ZIP export.
* Automated redaction pipeline.
* Support bundle.
* Telemetry.
* Crash-report upload.
* Thread-state export.
* Applied Error Memory lesson report.

### Deferred documentation

* Separate installation guide.
* Separate quick-start guide.
* Separate troubleshooting guide.
* Separate privacy guide.
* Separate changelog.
* Documentation website.

### Deferred validation

* Full Architecture Review on every launch validation.
* Full Workflow Review on every launch validation.
* Every focused validator in one release command.
* Seven or more synthetic failure fixtures.
* Performance benchmarking.
* Long-running workflow tests.
* Automated Freeze verification.

These may be added after the minimum professional version has been used successfully and a real deficiency is demonstrated.

## 11. Minimal implementation sequence

### Package 1: baseline and startup stability

Purpose:

* Inspect exact launch and tab-loading source.
* Record the current visible registry.
* Reproduce current startup.
* Fix startup regressions.
* Add no new product functionality.

Deliverables:

* Verified entry-point map.
* Verified visible-tab map.
* Verified consumer map for launch constants.
* Application starts.
* Every visible tab opens.
* Application closes and reopens.

Required result:

```text
APPLICATION STARTUP BASELINE: PASS
```

### Package 2: application smoke validator

Purpose:

* Add one minimal authoritative validation command.

Deliverables:

* PowerShell or equivalent entry point.
* Python smoke-test owner.
* Source compile.
* Import checks.
* Real Qt smoke.
* Clean shutdown.
* Complete traceback reporting.

Required result:

```text
APPLICATION SMOKE VALIDATION: PASS
```

### Package 3: environment declaration

Purpose:

* Make the development/runtime environment reproducible.

Deliverables:

* `pyproject.toml`
* One lock file.
* Canonical Python-version declaration.
* Dependency installation instructions.
* Runtime identity reporting.

Required result:

```text
FRESH ENVIRONMENT APPLICATION SMOKE: PASS
```

### Package 4: portable Windows build

Purpose:

* Launch KANDA Reasoner without a manual Python command.

Deliverables:

* Portable one-folder build.
* Executable launcher.
* Required Qt assets.
* Application icon.
* Build instructions.
* Packaged-runtime smoke validation.

Required result:

```text
PORTABLE WINDOWS BUILD SMOKE: PASS
```

### Package 5: logs, version, and README

Purpose:

* Make the stabilized application understandable and supportable.

Deliverables:

* Canonical version.
* Persistent log.
* Open-log action.
* Root README.
* Known limitations.

Required result:

```text
MINIMUM PROFESSIONAL USABILITY: PASS
```

## 12. Definition of done

The minimum professional version is complete when:

### Startup

* The application starts without an uncaught traceback.
* Every visible tab opens.
* The application closes cleanly.
* The application starts a second time.

### Validation

* One application smoke command exists.
* It compiles the source.
* It imports the canonical launcher.
* It imports all visible tabs.
* It runs a real Qt smoke.
* It fails with a nonzero exit code and complete traceback when broken.

### Environment

* `pyproject.toml` exists.
* One lock file exists.
* The expected Python runtime is explicit.
* A fresh environment reproduces a passing smoke test.

### Packaging

* A portable Windows build exists.
* It launches without a manual Python command.
* It has the correct icon.
* The packaged application passes the same essential smoke behavior.

### Supportability

* The application has a visible version.
* The application writes a persistent log.
* The user can open the log location.
* Secrets are not logged.
* A root README explains installation, launch, validation, logs, and common failures.

### Independence

A developer who did not build KANDA Reasoner can:

1. Obtain the portable folder.
2. Launch the application.
3. Select a project.
4. Open the main visible tools.
5. Run the smoke validator.
6. Find the log when something fails.

No additional professionalization feature is required before this milestone is declared complete.

## 13. Immediate next task

Perform a read-only minimum-professional baseline audit using the actual uploaded source.

The audit must verify rather than infer:

1. Canonical launcher.
2. GUI shell launcher.
3. Main-window owner.
4. Visible tool registry.
5. Lazy-tab loading behavior.
6. Current application-root resolution.
7. Current project-root resolution.
8. Current icon ownership.
9. Current shutdown behavior.
10. Existing logging behavior.
11. Existing version owner.
12. Existing dependency declaration files.
13. Existing packaging configuration.
14. Existing startup-focused validators.
15. Existing real Qt validators.

The audit must end with:

```text
MINIMUM PROFESSIONAL BASELINE

Canonical launcher:
Visible tab count:
Current startup status:
Current shutdown status:
Current version owner:
Current logging owner:
Dependency declaration:
Lock file:
Portable packaging:
Existing smoke validator:

FIRST PACKAGE:
startup-stability-and-application-smoke-v1

FILES ALLOWED TO CHANGE:
[to be determined from exact source]

FILES OUT OF SCOPE:
all feature engines and unrelated GUI redesign

SUCCESS CONDITION:
The real application starts, opens every visible tab, closes, and starts again.
```

## 14. Final direction

KANDA Reasoner does not need a full professional software organization built around it.

It needs a small dependable core:

```text
Launch
Validate
Reproduce
Package
Troubleshoot
```

The correct standard is:

> Double-click it, use it, close it, reopen it, and understand the failure when something breaks.
