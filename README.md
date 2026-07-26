<div align="center">

# KANDA Reasoner

### A governed desktop workspace for understanding, auditing, and safely evolving complex software projects with AI assistance.

**Windows desktop · PySide6 · Project-aware · Evidence-first · Human-controlled**

[Download the latest release](https://github.com/paulokanda/kanda_reasoner/releases/latest) · [Report an issue](https://github.com/paulokanda/kanda_reasoner/issues)

</div>

---

## Overview

KANDA Reasoner is a Windows desktop application designed to help developers inspect, understand, document, audit, and improve complex software projects without surrendering control of the project to an automated agent.

It combines:

* project structure analysis;
* architecture auditing;
* AI-ready context generation;
* local and web AI workflows;
* interactive project visualization;
* validation and review tools;
* error-memory workflows;
* feature-freeze and regression-protection mechanisms.

KANDA Reasoner is built around one central principle:

> **The tool may analyze and operate on a project, but it must never become the owner of that project.**

The application keeps the reusable KANDA Reasoner tool, the active project, and project-specific support evidence logically separate—even when KANDA Reasoner is analyzing its own source code.

---

## Why KANDA Reasoner Exists

Large software projects become difficult to reason about long before they become impossible to edit.

Common problems include:

* architecture knowledge scattered across many files;
* AI assistants receiving incomplete or misleading context;
* large modules that are difficult to refactor safely;
* undocumented relationships between components;
* project-specific state leaking into reusable tooling;
* fixes that solve one problem while silently breaking another;
* repeated mistakes that are never converted into durable lessons;
* completed features being damaged by later changes.

KANDA Reasoner addresses these problems by turning project understanding into an explicit, reviewable workflow:

```text
SELECT PROJECT
      ↓
INSPECT STRUCTURE
      ↓
COLLECT EVIDENCE
      ↓
AUDIT AND REASON
      ↓
PREPARE AI CONTEXT
      ↓
REVIEW PROPOSED CHANGES
      ↓
VALIDATE
      ↓
AUTHORIZE
      ↓
APPLY
      ↓
VERIFY
      ↓
PRESERVE EVIDENCE
```

The goal is not autonomous code generation.

The goal is **better reasoning, clearer boundaries, safer changes, and durable project knowledge**.

---

## Core Capabilities

### Audit Project

Inspect a selected project for architecture, structure, dependency, maintainability, and implementation risks.

The audit workflow can help identify:

* oversized or overloaded modules;
* unclear ownership boundaries;
* architectural drift;
* suspicious dependencies;
* validation gaps;
* refactoring candidates;
* source hygiene problems;
* project-specific risks requiring human review.

---

### Show Project to AI

Create structured project context that can be shared with an AI assistant without manually copying hundreds of files.

The collector organizes project evidence so an AI can reason from:

* project structure;
* selected source files;
* module relationships;
* entry points;
* symbols;
* configuration;
* documentation;
* project-specific evidence;
* generated context artifacts.

This helps reduce incomplete-context answers and unsupported architectural assumptions.

---

### Project Structure 3D

Explore the selected project through an interactive graph-based visualization.

Depending on the available project evidence, the view can represent:

* modules;
* files;
* symbols;
* internal imports;
* external dependencies;
* validators;
* protected files;
* frozen features;
* semantic relationships.

Project Structure 3D uses Qt WebEngine and a local web-rendering bridge inside the desktop application.

---

### Architecture Review

Review the architecture of a project or selected module before making changes.

The intended lifecycle is:

```text
INSERT TARGET
    ↓
READ
    ↓
ANALYZE
    ↓
PLAN
    ↓
PREVIEW
    ↓
VALIDATE
    ↓
AUTHORIZE
    ↓
WRITE
    ↓
VERIFY
    ↓
RECORD RECEIPT
    ↓
EJECT TARGET-SPECIFIC TOOL STATE
```

The project keeps the result. The reusable tool does not become the owner of project-specific code, previews, receipts, or mutation state.

---

### Docstring Assistant

Inspect Python code for missing or incomplete documentation and prepare docstring improvements.

The workflow is designed to support review rather than blindly rewriting an entire project.

---

### Local AI

Connect KANDA Reasoner to supported local AI workflows.

Local AI can be useful when:

* project content should remain on the local machine;
* an external provider is not appropriate;
* offline or private reasoning is preferred;
* a local model is already installed and configured.

Always verify the active provider configuration before assuming that a workflow is fully local.

---

### Web AI

Use supported external AI providers for project-aware reasoning and review.

Web AI configuration is intentionally user-controlled:

* credentials are not bundled into the portable release;
* the environment API key is not automatically displayed;
* the environment key must be loaded explicitly;
* users choose when to invoke an external service.

> **Privacy notice:** Web AI workflows may transmit selected project content to an external provider. Review the selected content and provider settings before sending confidential, proprietary, regulated, or personally identifiable information.

---

### Error Memory

Convert recurring failures, incorrect assumptions, and user-detected problems into durable lessons.

Error Memory is intended to help prevent the same class of mistake from being repeated across future work.

A useful error-memory record can include:

* what happened;
* why it happened;
* the incorrect assumption;
* the correct behavior;
* affected files or workflows;
* evidence of the repair;
* future prevention rules.

---

### Freeze Feature After Update

Protect meaningful completed work from accidental regression.

A freeze record can preserve:

* the implemented feature;
* protected paths;
* validation evidence;
* expected behavior;
* known boundaries;
* replacement or supersession history.

Freeze protection does not make files permanently immutable. It makes later changes explicit, reviewable, and evidence-aware.

---

## Governing Design Principles

### 1. Tool and Project Are Different Owners

KANDA Reasoner is the reusable tool.

The selected repository is the active project.

The tool may inspect, analyze, plan, validate, and—with explicit authorization—modify the project. It must not silently absorb project-specific state into reusable tool ownership.

---

### 2. Evidence Before Mutation

A change should be based on current source, current contracts, current project state, and relevant validation evidence.

Generated reports and AI responses are supporting evidence—not automatic source truth.

---

### 3. Human Authorization

KANDA Reasoner is designed to support human-controlled engineering.

Potentially destructive or architecture-sensitive operations should pass through explicit review and authorization boundaries.

---

### 4. Clear Ownership Boundaries

Each responsibility should have one primary owner.

Private internals should not become informal cross-module APIs. Communication between major components should use explicit contracts, controllers, adapters, registries, signals, or bridges.

---

### 5. Durable Project Evidence Stays With the Project

Project-specific evidence should remain associated with the selected project or its external support root.

This includes items such as:

* validation results;
* architecture review evidence;
* workbench previews;
* error-memory records;
* freeze records;
* implementation receipts;
* project handoffs.

---

### 6. Portable Application Files Stay Separate

The packaged application folder contains reusable program files.

It should not become the permanent storage location for active-project source or durable project-specific evidence.

---

## Portable Windows Release

KANDA Reasoner is currently distributed as a **portable one-folder Windows application**.

No traditional installation process is required.

### Requirements

* Windows 10 or Windows 11;
* 64-bit Windows;
* enough storage for the extracted application;
* permission to extract and execute local files.

Python, PyCharm, and a separate Qt installation are not required for the portable release.

---

## Quick Start

### 1. Download

Open the repository’s [Releases page](https://github.com/paulokanda/kanda_reasoner/releases) and download:

```text
KandaReasoner-Windows-Portable.zip
```

### 2. Extract the ZIP

Right-click the ZIP and select:

```text
Extract All
```

Do not run the application directly from inside the compressed ZIP.

### 3. Keep the Folder Intact

The extracted folder contains:

```text
KandaReasoner.exe
_internal\
```

The `_internal` folder contains the bundled Python runtime, PySide6, Qt libraries, Qt WebEngine resources, application modules, and supporting assets.

Do not move only `KandaReasoner.exe` away from `_internal`.

### 4. Launch

Double-click:

```text
KandaReasoner.exe
```

### 5. Select a Project

Choose the software project that KANDA Reasoner should inspect.

The selected project does not need to be located inside the KANDA Reasoner application folder.

---

## Release Integrity

Portable release:

```text
KandaReasoner-Windows-Portable.zip
```

SHA-256:

```text
DD2EF4D3000FB993B4D6BE2F7130C11B6AFEE534A87DE7B5C322A88CA96BFD95
```

Verify it in PowerShell:

```powershell
Get-FileHash `
    .\KandaReasoner-Windows-Portable.zip `
    -Algorithm SHA256
```

The reported hash should match the value above exactly.

---

## Validated Portable Workflows

The current portable build has passed the following smoke tests:

| Validation                                                                | Status |
| ------------------------------------------------------------------------- | ------ |
| Main application window opens                                             | Pass   |
| Application runs without development Python                               | Pass   |
| Application runs without PyCharm                                          | Pass   |
| Extracted ZIP launches successfully                                       | Pass   |
| Portable folder works after relocation                                    | Pass   |
| Project Structure 3D loads                                                | Pass   |
| Project Structure 3D no longer freezes during protection matching         | Pass   |
| Show Project to AI loads                                                  | Pass   |
| Audit Project loads                                                       | Pass   |
| Qt WebEngine is packaged                                                  | Pass   |
| Qt WebChannel is packaged                                                 | Pass   |
| Config Web AI starts without automatically displaying the environment key | Pass   |
| Manual environment-key loading remains available                          | Pass   |

A fully independent clean-Windows virtual-machine validation is still recommended before treating the release as broadly production-ready.

---

## Windows SmartScreen

The current executable is not digitally signed.

Windows SmartScreen or antivirus software may therefore display a warning for an unfamiliar application.

This does not automatically mean the file is malicious. Confirm that:

1. the ZIP came from the official repository release;
2. the SHA-256 hash matches the published value;
3. the archive contents have not been modified.

Future releases may add code signing, but it is not part of the current portable baseline.

---

## Running From Source

### Current Validated Environment

The current Windows development baseline uses:

* Python 3.12;
* PySide6 6.9.2;
* shiboken6 6.9.2;
* requests 2.34.2;
* libcst 1.8.6;
* PyInstaller 6.21.0;
* Ruff 0.15.21.

### Create a Virtual Environment

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Upgrade packaging tools:

```powershell
python -m pip install --upgrade pip
```

Install the validated toolchain:

```powershell
python -m pip install `
    PySide6==6.9.2 `
    shiboken6==6.9.2 `
    requests==2.34.2 `
    libcst==1.8.6 `
    pyinstaller==6.21.0 `
    ruff==0.15.21
```

Optional or workflow-specific dependencies may still be required by specialized tools.

### Launch the Source Application

```powershell
python reasoner_tools_gui.py
```

Or explicitly:

```powershell
.\.venv\Scripts\python.exe reasoner_tools_gui.py
```

---

## Building the Portable Windows Version

The repository includes:

```text
KandaReasonerWindows.spec
```

Build with:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller `
    --noconfirm `
    --clean `
    .\KandaReasonerWindows.spec
```

The generated application will be placed at:

```text
dist\KandaReasoner\KandaReasoner.exe
```

The specification accounts for:

* dynamically imported KANDA modules;
* lazy-loaded tabs;
* PySide6;
* Qt WebEngine;
* Qt WebChannel;
* application data files;
* physical source fragments loaded through file paths;
* Audit Project support modules.

### Create the Distribution ZIP

```powershell
Compress-Archive `
    -Path .\dist\KandaReasoner\* `
    -DestinationPath .\KandaReasoner-Windows-Portable.zip `
    -CompressionLevel Optimal
```

---

## Source Validation

Run Ruff on a modified file:

```powershell
.\.venv\Scripts\python.exe -m ruff check `
    .\path\to\modified_file.py
```

Check repository status:

```powershell
git status --short
```

Launch the source application:

```powershell
.\.venv\Scripts\python.exe reasoner_tools_gui.py
```

Before creating a release, test the packaged folder outside the repository:

```powershell
Copy-Item `
    .\dist\KandaReasoner `
    E:\KandaReasonerPortableTest `
    -Recurse
```

Then launch the relocated copy.

---

## Repository Structure

A simplified project overview:

```text
kanda_reasoner/
├── reasoner_tools_gui.py
├── KandaReasonerWindows.spec
├── ruff.toml
├── WORKFLOWS.md
├── kanda_reasoner_app/
│   ├── manage_architecture/
│   ├── project_structure_visualizer/
│   ├── reasoner_context_collector/
│   ├── reasoner_engine/
│   ├── reasoner_tools_gui_shell/
│   ├── freeze_after_update/
│   ├── freeze_after_update_gui/
│   ├── error_memory/
│   ├── error_memory_gui/
│   ├── insert_missing_docstrings_gui/
│   ├── patch_governance/
│   └── ...
├── prompt_library/
├── kanda_prompt_workspace/
├── tests/
├── tools/
├── scripts/
└── validation/
```

The exact structure may evolve as responsibilities are moved into clearer ownership boundaries.

---

## Security and Privacy

### Credentials

Do not commit:

* API keys;
* access tokens;
* passwords;
* `.env` files containing secrets;
* private provider configuration;
* credential exports.

The portable release does not include the developer’s private Web AI key.

### External AI Providers

A Web AI request may send selected content outside the local computer.

Before sending:

* confirm the selected provider;
* review the files and context being shared;
* remove secrets;
* remove private customer data;
* remove patient or medical information;
* remove regulated or personally identifiable information;
* comply with the project owner’s data-handling rules.

### Local AI

A workflow labeled “Local AI” should not automatically be assumed private without checking the configured endpoint, model provider, and network behavior.

---

## Current Limitations

* The current distributed build targets 64-bit Windows.
* The portable package is large because it includes Python, PySide6, Qt, and Qt WebEngine.
* The application is distributed as a folder, not a single standalone executable.
* The `_internal` folder must remain beside the executable.
* There is no traditional installer.
* There is no automatic updater.
* There is no formal uninstaller.
* The executable is not digitally signed.
* Windows may display SmartScreen warnings.
* Updates require downloading and extracting a newer release.
* Existing shortcuts may stop working when the portable folder is moved.
* Some advanced workflows may require additional local tools or provider configuration.
* A clean Windows VM or separate clean user-profile validation remains recommended.
* The PyInstaller build may report a nonfatal warning involving an optional developer-tools collector module; validated runtime workflows still launch successfully.

---

## Uninstalling

Because this is a portable application, uninstalling normally means deleting the extracted KANDA Reasoner folder.

To remove optional saved settings, logs, or local state, also inspect:

```text
%LOCALAPPDATA%\KANDA Reasoner
```

Do not delete the selected active project or its project-support evidence unless that data is intentionally no longer needed.

---

## Reporting Problems

When opening an issue, include:

* KANDA Reasoner release version;
* Windows version;
* whether you used the source or portable build;
* the tab or workflow involved;
* the exact steps that triggered the problem;
* the complete error message or traceback;
* whether the issue persists after restarting;
* whether the portable folder was moved;
* whether the selected project is local, external, or self-hosting.

Do not include API keys, tokens, patient data, customer secrets, or proprietary source code unless the repository owner has explicitly approved it.

---

## Contributing

Changes should remain focused, reviewable, and evidence-backed.

Before submitting a pull request:

1. identify whether the change belongs to the reusable KANDA Reasoner tool or the selected active project;
2. identify the primary owning module or box;
3. avoid importing another component’s private internals;
4. preserve Tool-versus-Project separation;
5. run focused Ruff checks;
6. run relevant tests and validators;
7. launch the source application;
8. test affected visible tabs;
9. rebuild the portable application when packaging behavior changes;
10. document known risks and validation evidence.

A change that cannot clearly identify its owner or validation path should not be merged until those boundaries are resolved.

---

## Project Status

KANDA Reasoner is under active development.

The current `v0.1.0` portable release establishes a working Windows distribution baseline and proves that the application can run outside its original development environment.

The current focus is stability, boundary correctness, reliable workflows, and evidence-backed improvements—not uncontrolled feature expansion.

---

## License

License: KANDA Reasoner is free to use but proprietary. Modification, redistribution, reverse engineering, and reuse of its source code or assets are prohibited. See LICENSE.md.

---

<div align="center">

**KANDA Reasoner**

*Understand the project. Preserve its boundaries. Change it with evidence.*

</div>
