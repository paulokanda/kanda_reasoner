---
audit_id: A030
audit_decision: UPDATE
audit_classification: ACTIVE_UNIVERSAL_DELIVERY_PROTOCOL
audit_batch: prompt_audit_chunk_003
review_status: sandbox_checked
---

> Audit note: This file was reviewed in batch mode. The content below is the real updated file for this audit decision.

# Universal Delivery Protocol

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.3
Status: Universal PyArchitect delivery protocol
Use: Applies to KANDA, Project Reasoner, and any Python project unless a project-specific governance file explicitly narrows a rule.

Core delivery flow:
audit -> request current files if needed -> classify complexity -> warn if complex -> roadmap for complex updates -> focused patch in sandbox -> helper split if needed -> compile/check/test -> package ZIP with project-relative folders -> user extracts at project base -> user validates locally -> only then freeze/canonize

Source truth:
- Current source files are the source of truth.
- Runtime logs and real validation output outrank memories and old prompts.
- Do not guess unseen code.
- If required files are missing, request a ZIP with a Windows/PyCharm command.

Prompt request rule:
Before implementation, state which prompts are needed.

Required wording:
"For this task, I need these prompt files before implementation:
1. <prompt>
2. <prompt>
Please upload them or confirm they are already loaded."

Testing honesty:
- Do not claim exhaustive runtime testing unless the complete project, dependencies,
  runnable entry points, and required sample data were provided and actually run.
- If only targeted files were provided, say:
  "Regular targeted testing was performed on the provided files only."
- GUI validation must be marked as manual/user-run unless the GUI was actually run.

Complex update rule:
If the correction affects GUI lifecycle, runtime behavior, schema, persistence,
threading, public APIs, large modules, or multiple boxes, warn:
"This is a complex update. I will create a roadmap first, validate the logic, and implement one focused gate at a time."

Large file rule:
- Ideal file size: <= 400 lines.
- Maximum: <= 500 lines.
- If a relevant Python file is above 500 lines, ask whether to split it into a
  main file plus helper files unless the active project canon already requires
  a split protocol.

Windows/PyCharm source request:
When files are needed, provide a PowerShell collector that:
- runs from the project root;
- copies exact project-relative paths into a staging folder;
- preserves folder structure;
- includes a large-file report;
- creates one ZIP in the project root;
- does not modify source files.

Delivery package rule:
- Create files in the sandbox.
- Validate the generated files where possible.
- Deliver one ZIP with final project-relative paths.
- The ZIP is extracted directly into the project root.
- The ZIP must not require an install script.
- The ZIP must not require a script under a separate backup-script folder.
- The ZIP must not require the user to unzip to a temporary folder first.

Manifest rule:
- Runtime/source bundles include _bundle_temp\BUNDLE_MANIFEST_<task_slug>.txt.
- Governance-only bundles may use their own project-specific governance folder.
- Do not use a generic BUNDLE_MANIFEST.txt.
- Do not put runtime/source manifests at ZIP root.

Bundle manifest must state:
- bundle name;
- changed box;
- task class;
- risk level;
- files changed;
- what changed;
- what did not change;
- safety boundaries preserved;
- validation performed;
- user validation commands;
- next recommended step.

Backup rule:
Before risky extraction, tell the user to use version control or make a project
checkpoint. Do not make normal updates depend on a custom install script.

Windows install command template:
$root = "<PROJECT_ROOT>"
$zipPath = "E:\<bundle_name>.zip"
Expand-Archive -Path $zipPath -DestinationPath $root -Force
Write-Host "Bundle installed."

Final delivery checklist:
- Project-relative paths preserved.
- _bundle_temp manifest included for source/runtime bundles.
- No extra top-level wrapper folder.
- No install script required.
- UTF-8 without BOM.
- Python files ASCII-safe unless existing source requires Unicode.
- Touched Python files compile where possible.
- Validation commands provided.
- Manual GUI checklist provided when relevant.


Prompt-audit package note:
- Prompt-audit ZIPs may include a terminal extraction command for user convenience.
- That command is not a required install script and must not mutate source beyond normal ZIP extraction.
- The ZIP itself remains the deliverable; terminal code is only a transparent install/extract helper.
