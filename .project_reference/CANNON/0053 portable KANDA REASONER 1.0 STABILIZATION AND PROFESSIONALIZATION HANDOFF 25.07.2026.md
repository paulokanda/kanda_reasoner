# KANDA REASONER PORTABLE WINDOWS BUILD HANDOFF

## 1. Objective

Create a portable Windows version of KANDA Reasoner that can be copied to another Windows computer and launched without:

* Installing Python manually.
* Selecting a Python interpreter.
* Configuring `PYTHONPATH`.
* Opening PyCharm.
* Running PowerShell installation commands.
* Modifying the Windows Registry.
* Using a traditional installer.

The user experience should be:

```text
Download or copy folder
-> extract folder
-> double-click KandaReasoner.exe
-> use application
```

## 2. Scope

This work is limited to producing and validating a portable Windows build.

Do not add:

* New application features.
* New GUI tabs.
* New AI systems.
* New memory systems.
* New architecture scanners.
* A traditional Windows installer.
* Automatic updates.
* A diagnostic ZIP system.
* A new home screen.
* A CI pipeline.
* A large documentation suite.
* A new release-management framework.

Only modify production code when required for the packaged application to start and operate correctly.

## 3. Recommended package format

Use a one-folder portable build.

Example structure:

```text
KANDA_Reasoner_Portable\
    KandaReasoner.exe
    KandaReasoner.ico
    README_PORTABLE.txt
    _internal\
        Python runtime
        PySide6 libraries
        Qt plugins
        QWebEngine resources
        KANDA application modules
        Application assets
```

Do not prioritize a single-file executable for the first version.

KANDA Reasoner uses PySide6 and may use QWebEngine. These components generally behave more predictably when their DLLs, plugins, subprocess executables, localization files, and resource folders remain visible in a packaged directory.

## 4. Packaging technology

Evaluate a Windows Python application bundler against the actual current KANDA source.

A likely first candidate is a one-folder PyInstaller build.

Do not assume it will work merely because the source application runs.

The selected packaging configuration must explicitly account for:

* PySide6 modules.
* Qt platform plugins.
* Qt image-format plugins.
* Qt styles where required.
* QtWebEngineProcess.
* QWebEngine resource files.
* QWebEngine localization files.
* Application icons.
* Help images and documentation assets.
* Prompt and configuration assets.
* Dynamically imported tab modules.
* Lazy-loaded modules.
* Application registries.
* Files located through `__file__`.
* Writable user data that must not remain inside the packaged program folder.

If another bundler handles the current source more reliably, it may be selected instead. The decision must be based on a tested prototype.

## 5. Required behavior

The portable build must:

1. Start by double-clicking `KandaReasoner.exe`.
2. Show the correct colorful brain application icon.
3. Show the same icon in the Windows taskbar.
4. Create the real KANDA Reasoner main window.
5. Load every visible registered tab.
6. Load PySide6 correctly.
7. Load QWebEngine correctly where used.
8. Resolve bundled read-only assets correctly.
9. Resolve the selected external project correctly.
10. Keep KANDA tool files separate from active project files.
11. Write logs and mutable state to an appropriate writable location.
12. Close without leaving background processes or QThreads running.
13. Reopen successfully.
14. Work when copied to a different folder.
15. Work when copied to a different Windows user profile.

## 6. Portable-path rules

The build must not depend on:

```text
E:\kanda_reasoner
C:\Users\paulo
PyCharm paths
A specific Downloads folder
A specific Desktop folder
The development Python installation
The current source-tree location
```

Bundled read-only application assets should be resolved through one canonical packaged-resource resolver.

External mutable data should be resolved separately.

Examples of mutable data:

* Logs.
* User preferences.
* Local AI configuration.
* Web AI configuration without secret values.
* Conversation history.
* Project selection.
* Temporary runtime files.
* Validation output.
* Error Memory or Freeze-related project state when applicable.

Do not write mutable state into the packaged `_internal` directory.

## 7. Project selection behavior

The portable application must not assume that the active project is the KANDA source folder.

At startup, it should either:

* Restore the previously selected project, when valid.
* Ask the user to select a project.
* Open without an active project and clearly show that no project is selected.

The packaged application root and selected project root must remain separate.

Moving the portable KANDA folder must not alter or relocate the selected project.

## 8. Required implementation audit

Before creating the packaging configuration, inspect the exact current source for:

* Canonical root launcher.
* GUI shell launcher.
* Main-window owner.
* Application constants.
* Application icon owner.
* Tool and tab registry.
* Lazy import mechanisms.
* Dynamic imports.
* `sys.path` manipulation.
* Paths derived from `__file__`.
* Hardcoded absolute paths.
* Help assets.
* PNG, ICO, HTML, JavaScript, JSON, Markdown, and template assets.
* QWebEngine use.
* QWebChannel use.
* Subprocess calls.
* PowerShell calls.
* External helper scripts.
* Writable-state locations.
* Development-only imports.
* Optional dependencies.

Do not build the package before this inventory is complete.

## 9. Development changes allowed

The packaging work may change:

* Canonical resource-path resolution.
* Application-root resolution.
* Writable-state path resolution.
* Main launcher behavior.
* Icon loading.
* Bundled asset lookup.
* Dynamic import declarations needed by the packager.
* Logging initialization.
* Packaging configuration.
* Portable-build scripts.
* Portable-build validation scripts.

The work must preserve:

* Project/tool root boundaries.
* Box ownership.
* No-Leak behavior.
* Local AI behavior.
* Web AI behavior.
* Error Memory behavior.
* Freeze confirmation behavior.
* Existing application tabs and workflows.

## 10. Files expected to be added

Exact filenames must follow the current project architecture, but the minimum package will probably require equivalents of:

```text
packaging\
    kanda_reasoner.spec
    build_portable.ps1
    validate_portable_build.py
    validate_portable_build.ps1
    README_PORTABLE.txt
```

A root-level packaging configuration may be used when that is the current project convention.

Do not introduce multiple competing build systems.

## 11. Build command

Provide one canonical build command.

Example target:

```powershell
powershell -ExecutionPolicy Bypass -File E:\kanda_reasoner\packaging\build_portable.ps1
```

The command should:

1. Confirm the source root.
2. Confirm the governed Python interpreter.
3. Confirm required packaging dependencies.
4. Remove or isolate previous build output.
5. Build the one-folder portable package.
6. Confirm that required files exist.
7. Run the portable-build validator.
8. Produce the final portable folder.
9. Optionally create a ZIP of that folder.
10. Print the final output path.

The generated portable package must be built from the exact source that is being validated.

## 12. Validation

The source application passing validation is not enough.

The packaged application itself must be tested.

### 12.1 Static packaged-output checks

Confirm that the build contains:

* Main executable.
* Correct icon.
* Qt platform plugin.
* Required Qt DLLs.
* QWebEngine process and resources when applicable.
* Dynamically imported tab modules.
* Help and image assets.
* Required JSON and configuration assets.
* No developer-only secrets.
* No accidental source archives or patient information.

### 12.2 Packaged process launch

Launch the real packaged executable as a subprocess.

Confirm:

* Process starts.
* Main window appears.
* No immediate crash occurs.
* Startup log is created.
* Application version is reported.
* Application can close normally.

### 12.3 Visible-tab smoke

Open every visible registered tab in the packaged application.

Confirm that no tab fails because of:

* Missing hidden import.
* Missing asset.
* Missing Qt plugin.
* Missing QWebEngine resource.
* Incorrect bundled path.
* Development-only import assumptions.

### 12.4 Relocation test

Copy the entire portable folder to a different path.

Example:

```text
Original:
E:\KANDA_Reasoner_Portable

Relocated:
C:\Users\TestUser\Desktop\KANDA_Reasoner_Portable
```

Run the relocated copy.

It must not depend on its original build or extraction location.

### 12.5 Clean-profile test

Test under a Windows user profile that does not have:

* KANDA source installed.
* The development Python installation on `PATH`.
* PyCharm.
* Existing KANDA environment variables.
* Existing local KANDA configuration.

This may be a clean Windows virtual machine or a controlled test account.

### 12.6 Required final markers

```text
PORTABLE_BUILD_CONTENTS: PASS
PORTABLE_APPLICATION_LAUNCH: PASS
PORTABLE_APPLICATION_ICON: PASS
PORTABLE_VISIBLE_TABS: PASS
PORTABLE_QT_PLUGINS: PASS
PORTABLE_QWEBENGINE: PASS
PORTABLE_CLEAN_SHUTDOWN: PASS
PORTABLE_RELAUNCH: PASS
PORTABLE_RELOCATION: PASS
PORTABLE_CLEAN_PROFILE: PASS
PORTABLE WINDOWS BUILD: PASS
```

Only emit a final success marker for tests that were actually executed.

## 13. Logs

The portable application should create a persistent startup and error log.

Suggested location:

```text
%LOCALAPPDATA%\KANDA Reasoner\logs
```

A portable-local data folder may be used only when deliberately selected and documented.

The log should include:

* Application version.
* Executable path.
* Application resource root.
* Selected project root.
* Windows version.
* Qt and PySide6 versions.
* Main-window startup.
* Tab-loading failures.
* Complete uncaught tracebacks.
* Shutdown status.

The log must not include:

* API keys.
* Tokens.
* Passwords.
* Full credential values.
* Unredacted private environment variables.

## 14. Minimum documentation

Include one file in the portable package:

```text
README_PORTABLE.txt
```

It should explain:

1. How to launch KANDA Reasoner.
2. That no Python installation is required.
3. How to select a project.
4. Where logs are stored.
5. How to report a startup failure.
6. That Web AI may transmit selected content externally.
7. Known limitations.
8. How to move the portable folder.
9. Which folders must remain together.
10. How to remove the application.

Removing the portable application should normally require deleting:

* The portable application folder.
* The optional user-data folder, when the user wants to remove saved settings and logs.

## 15. Explicitly deferred

The portable build does not require:

* MSI.
* Inno Setup.
* NSIS.
* Windows Store packaging.
* Administrator installation.
* Automatic updates.
* Background updater.
* Registry-based installation.
* Formal uninstall program.
* File associations.
* Shell extensions.
* Windows service.
* Digital code signing.
* CI/CD.
* Public download website.
* Diagnostic ZIP.
* Telemetry.
* Crash uploads.
* New GUI home screen.
* New documentation suite.
* New application features.

## 16. Pros of the portable approach

### 16.1 Minimal user friction

The user does not need to install Python or configure an environment.

### 16.2 Low implementation complexity

A portable one-folder build is usually simpler than creating and maintaining a complete installer.

### 16.3 Easy rollback

Different versions can remain in separate folders:

```text
KANDA_Reasoner_0.9.0
KANDA_Reasoner_0.9.1
KANDA_Reasoner_1.0.0
```

Returning to a previous version only requires opening the previous folder.

### 16.4 Low system impact

The portable application can avoid:

* Registry installation.
* Administrator rights.
* System-level PATH changes.
* Global Python modifications.

### 16.5 Easy testing

The exact folder can be copied to another machine or VM and tested directly.

### 16.6 Development and release separation

The user runs a packaged application rather than the live source tree.

This reduces accidental source modifications and environment drift.

### 16.7 Useful intermediate milestone

A successful portable package proves that:

* Dependencies are understood.
* Dynamic imports are mapped.
* Resource paths are controlled.
* The application can run outside the development environment.

This is valuable even if a traditional installer is created later.

## 17. Cons of the portable approach

### 17.1 Large folder size

PySide6, Qt, and QWebEngine can make the package large.

A portable KANDA Reasoner folder may contain many DLLs and resource files.

### 17.2 Many visible internal files

A one-folder build is not visually elegant.

The user must keep the executable together with its `_internal` or support folder.

### 17.3 Slower build process

Qt and QWebEngine packaging can take significant build time and produce large outputs.

### 17.4 Hidden-import risk

Dynamic tabs and lazy imports may not be detected automatically by the bundler.

They must be explicitly collected and validated.

### 17.5 QWebEngine complexity

QWebEngine requires subprocesses, resources, localization files, and correct runtime paths.

It is one of the highest-risk parts of the portable build.

### 17.6 Antivirus false positives

Unsigned Python executable bundles may occasionally be flagged or treated cautiously by antivirus products.

### 17.7 No automatic updating

The user must replace the portable folder manually when installing a new version.

### 17.8 User-data decisions remain necessary

Even a portable application needs a clear policy for:

* Preferences.
* Logs.
* Conversations.
* Project configuration.
* Temporary files.

Keeping all state inside the portable folder improves portability but can create permission and data-loss problems.

Using `%LOCALAPPDATA%` is safer but makes the application less completely portable.

### 17.9 Shortcut maintenance

If the folder is moved, an existing desktop or Start Menu shortcut may stop working.

### 17.10 No polished uninstall experience

The user deletes folders manually rather than using Windows Apps and Features.

## 18. Recommended state model

Use a hybrid model.

### Packaged program files

Keep read-only files inside the portable application folder:

* Executable.
* Python runtime.
* Qt libraries.
* Application code.
* Icons.
* Help assets.
* Built-in prompts and templates.

### User state

Store mutable user data under:

```text
%LOCALAPPDATA%\KANDA Reasoner
```

This is recommended for:

* Logs.
* Preferences.
* Recent project selection.
* Local conversation metadata.
* Temporary files.
* Non-secret application state.

### Project-specific state

Continue storing project-specific governed data under the selected project support root according to existing KANDA rules.

Do not store project-specific Error Memory, Freeze Memory, or handoff state inside the portable application folder.

## 19. Recommended implementation sequence

### Step 1: package-readiness audit

Inspect:

* Entry points.
* Dynamic imports.
* Registered tabs.
* Assets.
* QWebEngine.
* Root resolution.
* Writable-state paths.
* Subprocesses.
* External scripts.

Deliverable:

```text
PORTABLE BUILD READINESS AUDIT
```

### Step 2: minimal packaging prototype

Build the smallest one-folder executable that opens the main window.

Do not attempt to perfect every workflow yet.

Deliverable:

```text
PORTABLE MAIN WINDOW PROTOTYPE: PASS
```

### Step 3: visible-tab completion

Add required hidden imports and assets until every visible tab opens.

Deliverable:

```text
PORTABLE VISIBLE TAB SMOKE: PASS
```

### Step 4: QWebEngine and advanced runtime support

Validate all web-based tabs and bridge resources.

Deliverable:

```text
PORTABLE QWEBENGINE RUNTIME: PASS
```

### Step 5: writable-state separation

Move or confirm mutable state outside bundled read-only resources.

Deliverable:

```text
PORTABLE MUTABLE STATE: PASS
```

### Step 6: relocation and clean-profile test

Test the exact portable folder outside the development machine assumptions.

Deliverable:

```text
PORTABLE WINDOWS BUILD: PASS
```

## 20. Definition of done

The portable Windows build is complete when:

* `KandaReasoner.exe` launches by double-click.
* Python is not required on the target machine.
* The correct brain icon appears.
* Every visible tab opens.
* QWebEngine functionality operates where required.
* The application closes cleanly.
* The application reopens.
* The folder works after relocation.
* The folder works under a clean Windows profile.
* The application does not depend on `E:\kanda_reasoner`.
* Mutable user state is stored in a writable location.
* Project-specific governed state remains outside the application package.
* A startup log is available.
* `README_PORTABLE.txt` is included.
* The exact portable folder passes packaged-runtime validation.

Final required result:

```text
PORTABLE WINDOWS BUILD: PASS
```

## 21. Immediate next task

Perform a read-only portable-build readiness audit against the actual KANDA Reasoner source.

The audit must identify:

1. Canonical executable entry point.
2. Main-window import path.
3. Registered visible tabs.
4. Dynamic and lazy imports.
5. QWebEngine dependencies.
6. Required non-Python assets.
7. Current icon assets.
8. Current application-root assumptions.
9. Current project-root assumptions.
10. Writable-state locations.
11. Subprocess and PowerShell dependencies.
12. Existing packaging files.
13. Existing version owner.
14. Existing logging owner.
15. Likely bundler exclusions and hidden imports.

The audit must end with:

```text
PORTABLE BUILD BASELINE

Recommended packaging technology:
Recommended packaging mode: ONE-FOLDER
Canonical launcher:
QWebEngine required: YES / NO
Dynamic import risk: LOW / MEDIUM / HIGH
Writable-state repair required: YES / NO
Absolute-path repair required: YES / NO

FIRST IMPLEMENTATION PACKAGE:
kanda-reasoner-portable-windows-prototype-v1

SUCCESS CONDITION:
The packaged executable creates the real main window on a Windows environment without using the development Python installation.
```
My recommendation for KANDA Reasoner

Use a one-folder portable build first.

It offers roughly 80% of the practical professionalism benefit with much less complexity than a traditional installer. A full installer only becomes worthwhile when you need distribution to multiple external users, automatic upgrades, code signing, or a polished uninstall experience.