# KANDA REASONER WINDOWS PORTABLE
## Canonical Creation Logic and Next-Session Handoff

Date: 2026-07-30  
Validated baseline: Portable Creator v1r11  
Feature ID: `kanda-reasoner-portable-builder-install-v1r11`

---

## 1. Purpose of this handoff

This document tells the next AI exactly how KANDA Reasoner Windows Portable must
be created, validated, published, frozen, and connected to Error Memory without
repeating the long chain of failures that occurred during v1r8 through v1r11.

The goal is not to add another packaging system. The goal is to preserve and
reuse the already validated v1r11 architecture as the canonical baseline.

The next AI must treat this as a release workflow with strict ownership,
machine-readable phase contracts, fail-closed validation, human GUI checkpoints,
and durable diagnostic evidence.

Do not replace the working v1r11 logic with a new architecture merely because a
different design appears cleaner. Change the baseline only when a concrete,
reproducible defect is demonstrated.

---

## 2. Current validated release identity

```text
Portable builder version:
v1r11

Portable builder feature ID:
kanda-reasoner-portable-builder-install-v1r11

Validated final ZIP:
E:\KandaReasoner-Windows-Portable.zip

Validated final ZIP SHA-256:
1664bea434c2c7d98fe494e2a0c6061b73ffc52647e9845268f31c8b854b2a46

Validated final ZIP size:
475,891,224 bytes

Validated final ZIP member count:
4,356

Validated maximum member path:
204 bytes

Final status:
STATUS: PORTABLE READY AND VALIDATED
```

An older ZIP may still exist at:

```text
E:\kanda_reasoner\KandaReasoner-Windows-Portable.zip
```

That project-local ZIP is not the validated release authority. Do not delete,
replace, or trust it automatically. The release authority is the exact external
path and SHA-256 above.

---

## 3. Hard ownership boundaries

### 3.1 Selected project

```text
E:\kanda_reasoner
```

The selected project owns:

- its source code;
- `KandaReasonerWindows.spec`;
- the installed Portable creator under `portable`;
- source validation;
- the live Windows build;
- the final Portable artifact;
- project-specific Freeze evidence;
- project-specific Error Memory intake.

### 3.2 Project Support

```text
E:\kanda_reasoner_show_project_to_AI
```

Project Support owns:

- project-specific Freeze Memory;
- project-specific Error Memory;
- startup context and handoff evidence;
- Show Project artifacts.

Portable creation may read the resolved Project Support path for boundary and
immutability checks, but it must not invoke Show Project or write Show Project
outputs.

### 3.3 Transient root

```text
E:\kanda_reasoner_delete_after_daily_work
```

All temporary work belongs here:

- package extraction;
- installer tools;
- orchestration records;
- PyInstaller work;
- PyInstaller dist;
- release staging;
- clean extraction;
- smoke-test copies;
- receipts;
- transcripts;
- validation reports;
- failed-run diagnostics.

Nothing transient belongs inside the project source tree.

### 3.4 Final destination

The final destination must be selected by the user with a native folder picker.

It must be outside:

- the project root;
- Project Support;
- the transient root.

The Portable creator must derive and validate this boundary using resolved path
components, not raw string-prefix comparisons.

### 3.5 Independence from other workflows

Portable creation must not invoke:

- Show Project;
- Freeze writing;
- Error Memory staging;
- canonical Error Memory writes.

Portable creation, Freeze, and Error Memory are separate workflows. Their
evidence may be connected after successful validation, but their failure
surfaces must not be coupled.

---

## 4. Canonical toolchain

Use the governed interpreter:

```text
C:\Users\paulo\AppData\Local\Programs\Python\Python312\python.exe
```

Validated runtime:

```text
Python 3.12.10
64-bit
```

Validated PyInstaller:

```text
PyInstaller 6.21.0
```

Packaging authority:

```text
E:\kanda_reasoner\KandaReasonerWindows.spec
```

Rules:

1. Never default to plain `python`.
2. Validate the interpreter path, Python version, architecture, and exact
   PyInstaller version before building.
3. Keep `KandaReasonerWindows.spec` authoritative.
4. Do not rewrite the spec to solve a failure until exact evidence proves the
   spec is the owner.
5. Preserve the PyInstaller warning file for review.
6. A PyInstaller warning is not automatically fatal.
7. A successful COLLECT is not automatically a valid release.

---

## 5. Required five-phase release state machine

The public runner must execute five explicit phases.

```text
PHASE 01 — delivery package validation
PHASE 02 — transactional creator installation
PHASE 03 — live installed creator validation
PHASE 04 — real Portable creation and GUI smoke testing
PHASE 05 — independent final Portable validation
```

Each phase must have:

- an exact identity;
- a machine-readable result;
- visible PASS or FAIL markers;
- a retained diagnostic root;
- no dependence on human-readable text wrapping;
- no false success continuation after failure.

The next AI must resume from the last reliable marker. Do not rerun already
proven earlier phases unless the relevant artifact, source fingerprint, version,
feature ID, interpreter, spec, or installed creator changed.

---

## 6. Phase 01 — validate the delivery package

The delivery ZIP must be validated before installation.

Required checks:

- exact expected ZIP SHA-256;
- exact member set;
- exact file hashes;
- Python AST parse;
- ASCII source contract when the package requires ASCII-safe Python;
- PowerShell 5.1 parse safety;
- package manifest identity;
- builder version;
- feature ID;
- no stale creator revision;
- no Show Project implementation imports;
- final-validator fixture;
- runtime-package positive fixture;
- generated-state negative fixture;
- physical-runtime manifest fixture;
- Error Memory lesson draft contract when a lesson is included;
- explicit marker that live Windows building is not yet claimed.

Required phase marker:

```text
PHASE 01 PACKAGE VALIDATION: PASS
```

Important evidence distinction:

```text
PACKAGE LIVE WINDOWS BUILD: NOT CLAIMED
```

Synthetic fixture output must never be presented as proof that the actual
Windows Portable was built.

---

## 7. Phase 02 — install the creator transactionally

Install the creator under:

```text
E:\kanda_reasoner\portable
```

Installation must:

1. extract to a transient staging folder;
2. validate the staged package;
3. snapshot the current installed creator if present;
4. write through a transactional replacement;
5. verify the exact installed member set;
6. verify exact installed file hashes;
7. verify the installed validator executes;
8. verify the installed identity JSON;
9. reject stale creator revisions;
10. preserve rollback evidence.

Required markers:

```text
PHASE 02 CREATOR INSTALLATION: PASS
PHASE 02 EXACT LIVE HASHES: PASS
PHASE 02 MACHINE IDENTITY JSON: PASS
```

Installation is not live Portable validation.

---

## 8. Phase 03 — validate the installed creator

Machine identity must use compact one-line JSON, for example:

```json
{"builder_version":"v1r11","feature_id":"kanda-reasoner-portable-builder-install-v1r11","schema_version":"1.0"}
```

PowerShell must:

1. capture native output directly;
2. parse it with `ConvertFrom-Json`;
3. compare `builder_version` with exact equality;
4. compare `feature_id` with exact equality;
5. reject additional or stale identities when the contract requires exact
   fields.

Never use:

- `Out-String`;
- host-formatted output;
- line wrapping;
- whitespace collapse;
- regex matching of the human `--version` output.

Required markers:

```text
IDENTITY JSON LIVE ONE-LINE CAPTURE: PASS
IDENTITY JSON CONVERTFROM-JSON: PASS
IDENTITY JSON EXACT VERSION EQUALITY: PASS
IDENTITY JSON EXACT FEATURE EQUALITY: PASS
OUT-STRING MACHINE IDENTITY PARSING: NOT USED
PHASE 03 LIVE CREATOR VALIDATION: PASS
```

---

## 9. Phase 04 — real Portable creation

Phase 04 is the core build state machine.

### 9.1 Explicit user request

Require the exact confirmation phrase:

```text
BUILD KANDA PORTABLE
```

Do not build or publish a Portable from an implicit request.

### 9.2 Native destination picker

Use a native folder picker.

Record:

- selected project;
- Project Support;
- transient root;
- selected destination;
- final output path;
- governed Python;
- spec path;
- feature ID;
- builder version;
- unique run ID.

### 9.3 Unique run root

Create a unique run root under:

```text
E:\kanda_reasoner_delete_after_daily_work\portable_build\<unique-run-id>
```

The run root owns:

```text
pyinstaller_work
pyinstaller_dist
release_stage
clean_extract
candidate ZIP
temporary publication evidence
```

Never merge build products into the project.

### 9.4 Pre-build immutable snapshots

Before PyInstaller, capture deterministic content-hash snapshots of:

```text
E:\kanda_reasoner
E:\kanda_reasoner_show_project_to_AI
```

Ignore only explicitly governed transient or irrelevant metadata according to
the current snapshot owner.

The same snapshot algorithm must be used after smoke tests and after
publication.

### 9.5 Validate the spec and environment

Require:

```text
PORTABLE CANONICAL SPECIFICATION: PASS
PORTABLE SPEC MACHINE-SPECIFIC PATHS: ABSENT
PORTABLE QT WEBENGINE SPEC CONTRACT: PASS
PORTABLE PHYSICAL HELP DATA CONTRACT: PASS
PORTABLE GOVERNED PYTHON IDENTITY: PASS
```

### 9.6 Execute PyInstaller

Canonical command shape:

```text
<governed-python> -m PyInstaller
    --noconfirm
    --clean
    --workpath <transient-run>\pyinstaller_work
    --distpath <transient-run>\pyinstaller_dist
    E:\kanda_reasoner\KandaReasonerWindows.spec
```

Required PyInstaller outputs:

- direct application executable;
- `_internal`;
- `QtWebEngineProcess.exe`;
- Qt Windows platform plugin `qwindows.dll`.

Preserve:

```text
warn-KandaReasonerWindows.txt
xref-KandaReasonerWindows.html
```

Do not suppress or patch warnings blindly.

### 9.7 Build output validation

Require:

```text
PORTABLE QT WEBENGINE PROCESS: PASS
PORTABLE QT WINDOWS PLATFORM PLUGIN: PASS
PORTABLE PYINSTALLER BUILD: PASS
PORTABLE BUILD PRODUCTS OUTSIDE PROJECT: PASS
```

---

## 10. Physical runtime dependency hydration

This was the decisive correction in v1r11.

PyInstaller normally embeds imported Python modules inside its Python archive.
Several active KANDA features do not use normal imports. They require real
filesystem files because they use:

- `Path.exists()`;
- `spec_from_file_location()`;
- `exec_module()`;
- subprocess commands pointing to `.py` files;
- package-relative external workspace paths.

Therefore the creator must hydrate audited physical runtime files after
PyInstaller and before ZIP creation.

### 10.1 Required runtime roles

The physical-runtime manifest must contain all roles:

```text
architecture_worker
workflows_worker
docstrings_worker
architecture_grimp_probe
collector_source_parts
prompt_tools
prompt_library
freeze_blueprint_tools
```

### 10.2 Exact critical workers

Copy physically into `_internal`:

```text
kanda_reasoner_app/manage_architecture/manage_architecture.py

kanda_reasoner_app/manage_workflows/manage_workflows.py

kanda_reasoner_app/insert_missing_docstrings_gui/
insert_missing_docstrings.py
```

The destination must mirror the path expected by each GUI.

### 10.3 Collector fragments

Copy the active physical source fragments required by:

```text
kanda_reasoner_app/reasoner_context_collector/collector_main.py
```

The current collector reconstructs source from physical helper parts under:

```text
kanda_reasoner_app/reasoner_context_collector/collector_main_help/
```

Do not assume `collect_submodules()` satisfies this loader.

### 10.4 Architecture probe

Copy:

```text
kanda_reasoner_app/manage_architecture/
large_file_refactor_planner/grimp_graph_probe.py
```

### 10.5 Freeze blueprint runtime

Copy only active runtime blueprint tools from:

```text
project_freeze_ledger/freeze_tools/
```

Do not copy project-specific frozen memory.

Do not copy deprecated one-time apply, repair, cleanup, or validator scripts
unless the current runtime contract proves they are required.

### 10.6 Prompt workspace

Copy required runtime files from:

```text
kanda_prompt_workspace/prompt_tools/
kanda_prompt_workspace/prompt_library/
```

Exclude:

- generated first-prompt deliveries;
- generated second-prompt deliveries;
- first-AI delivery folders;
- `_bundle_temp`;
- backups;
- caches;
- archives;
- credentials;
- `.env` files.

### 10.7 Full-path classification

Classify by normalized owner path sequence, not basename.

Required distinction:

```text
PRESERVE:
kanda_reasoner_app/freeze_hint_intake

EXCLUDE:
project_freeze_after_update/freeze_hint_intake
```

A generic basename blacklist previously rejected the legitimate runtime
package.

### 10.8 Physical runtime manifest

Write:

```text
_internal/kanda_portable_runtime/physical_runtime_manifest.json
```

For every copied file record:

- role;
- project-relative source path;
- Portable archive-relative path;
- SHA-256;
- size.

Validate the manifest:

1. immediately after hydration;
2. after cleanup;
3. before ZIP creation;
4. from the final ZIP;
5. during final independent validation.

Required markers:

```text
PORTABLE ARCHITECTURE WORKER PHYSICAL FILE: PASS
PORTABLE WORKFLOWS WORKER PHYSICAL FILE: PASS
PORTABLE DOCSTRINGS WORKER PHYSICAL FILE: PASS
PORTABLE COLLECTOR SOURCE PARTS PHYSICAL FILES: PASS
PORTABLE GRIMP PROBE PHYSICAL FILE: PASS
PORTABLE FREEZE BLUEPRINT TOOLS PHYSICAL FILES: PASS
PORTABLE PROMPT WORKSPACE PHYSICAL FILES: PASS
PORTABLE PHYSICAL RUNTIME MANIFEST: PASS
PORTABLE PHYSICAL RUNTIME EXACT HASHES: PASS
PORTABLE PHYSICAL RUNTIME REQUIRED ROLES: PASS
```

The successful v1r11 live build recorded:

```text
PORTABLE PHYSICAL RUNTIME FILE COUNT: 354
```

Do not hard-code `354` as a universal future count. The exact count may change
when governed runtime files change. The manifest and role/hash contract are
authoritative.

---

## 11. Release staging cleanup

Before ZIP creation:

- remove cache folders;
- remove bytecode;
- remove backups;
- remove temporary bundle folders;
- remove generated deliveries;
- remove archives;
- remove source debris not required at runtime;
- remove environment files;
- remove deprecated or nonimplemented trees according to the current policy;
- preserve required physical runtime files.

Cleanup must be idempotent.

Do not rewrite copied source files merely to normalize line endings. Exact
byte-preserving hashes matter for manifests and intake artifacts.

Required markers:

```text
PORTABLE NON-RUNTIME BACKUP/CACHE DEBRIS REMOVED: <count>
PORTABLE NON-RUNTIME DEBRIS ABSENT: PASS
PORTABLE GENERATED ARTIFACT PATH CLASSIFIER: PASS
PORTABLE STAGE CONTENTS: PASS
```

---

## 12. Candidate ZIP contract

Create a candidate ZIP under the transient run root.

Required ZIP structure:

1. exactly one top-level folder;
2. exactly one direct application executable in that folder;
3. all runtime files inside that folder;
4. no unsafe paths;
5. no path traversal;
6. no absolute members;
7. no case-colliding member names;
8. no environment credential files;
9. no Show Project generated outputs;
10. no backup/cache debris;
11. required Qt runtime;
12. required physical-runtime manifest and files;
13. current path-length contract;
14. valid CRC for every member.

Required markers:

```text
WINDOWS_EXPLORER_ZIP_CHECK=PASS
TOP_LEVEL_ENTRIES=1
PORTABLE WINDOWS EXPLORER ZIP CHECK: PASS
PORTABLE ZIP INTEGRITY: PASS
PORTABLE ZIP PATH SAFETY: PASS
PORTABLE ZIP NON-RUNTIME DEBRIS ABSENT: PASS
PORTABLE SHOW PROJECT OUTPUT EXCLUSION: PASS
```

---

## 13. Clean extraction and functional smoke testing

Archive validation is not enough.

Extract the exact candidate ZIP into a fresh empty transient directory.

Launch the executable from that clean extraction.

### 13.1 First launch checklist

Test at least:

```text
main window responsiveness
Validate Project
Manage Workflows
Insert Missing Docstrings
Project Structure 3D
Show Project to AI
Audit Project
Freeze Feature After Update
Config Web AI
important changed tabs
collector-related actions
local help/resources
```

For write-capable features, use read-only modes:

- Validate;
- Scan;
- Diff;
- Preview;
- Help.

Do not authorize source mutation merely for smoke testing.

### 13.2 First natural close

The required sequence is:

1. test the GUI;
2. close it normally;
3. wait until the actual process exits;
4. require exit code zero;
5. only then accept:

```text
FIRST PASS CLOSED
```

The human phrase is not proof of process termination. The creator must verify
the process itself.

Required markers:

```text
PORTABLE APPLICATION FIRST LAUNCH: PASS
PORTABLE APPLICATION FIRST NATURAL CLOSE: PASS
```

### 13.3 Second launch

Relaunch the exact same clean extraction, not a rebuilt copy.

Repeat the important checks.

Close naturally and only then accept:

```text
PORTABLE TESTS PASS CLOSED
```

Required markers:

```text
PORTABLE APPLICATION RELAUNCH: PASS
PORTABLE APPLICATION RELAUNCH NATURAL CLOSE: PASS
PORTABLE CLEAN SHUTDOWN: PASS
PORTABLE HUMAN GUI SMOKE TEST: PASS
```

If any visible function fails, the candidate is not release-ready even if the
ZIP and executable are structurally valid.

---

## 14. Post-smoke immutability checks

After both launches, recompute the project and Project Support snapshots.

Require:

```text
PORTABLE PROJECT SOURCE UNCHANGED: PASS
SHOW PROJECT SUPPORT UNCHANGED: PASS
```

If a GUI read-only smoke test changed governed source or Project Support, fail
the release.

---

## 15. Atomic publication

Never publish directly over the final path while copying.

Publication algorithm:

1. create a partial file in the selected destination folder;
2. copy the exact validated candidate bytes into the partial file;
3. verify the partial SHA-256 and size;
4. atomically replace or rename the partial file to:

```text
KandaReasoner-Windows-Portable.zip
```

5. verify final SHA-256 and size;
6. retain the transient candidate and evidence until final validation succeeds.

The partial file must be created in the destination folder so the final rename
is same-volume and atomic.

Required markers:

```text
PORTABLE SELECTED-FOLDER ATOMIC PUBLICATION: PASS
PORTABLE ATOMIC PUBLICATION: PASS
PORTABLE OWNER SEPARATION: PASS
PORTABLE OUTPUT USER-SELECTED FOLDER: PASS
PORTABLE OUTPUT OUTSIDE PROJECT ROOT: PASS
PORTABLE OUTPUT OUTSIDE PROJECT SUPPORT: PASS
PORTABLE BUILD RESULTS NOT MERGED INTO PROJECT: PASS
SHOW PROJECT WORKFLOW NOT INVOKED: PASS
```

After publication, recompute source snapshots again:

```text
PORTABLE PROJECT SOURCE UNCHANGED AFTER PUBLICATION: PASS
SHOW PROJECT SUPPORT UNCHANGED AFTER PUBLICATION: PASS
```

---

## 16. Phase 04 result JSON

Every success or failure must write a structured result JSON under the
orchestration root.

Current pattern:

```text
E:\kanda_reasoner_delete_after_daily_work\
portable_creator_orchestration_v1r11\
<run-id>\
portable_result.json
```

On success include at least:

- schema version;
- status `portable_ready`;
- builder version;
- feature ID;
- selected project;
- Project Support;
- transient run root;
- final ZIP path;
- final ZIP SHA-256;
- final ZIP size;
- member count;
- smoke evidence;
- before/after source hashes;
- final report path.

On failure include at least:

- status `failed`;
- error type;
- exact error message;
- failed phase;
- project root;
- diagnostic root;
- paths to transcript and partial evidence;
- pre-run snapshots;
- candidate ZIP path if one exists.

Do not surface only:

```text
Portable creator failed with exit code 1
```

The outer wrapper may show that summary, but it must also show the exact result
JSON and transcript paths.

Required phase marker:

```text
PHASE 04 PORTABLE CREATOR: PASS
```

---

## 17. Phase 05 — independent final validation

Phase 05 must validate the published final ZIP independently of the build
function.

It must consume:

- Phase 04 result JSON;
- final published ZIP;
- final validation evidence;
- project/source snapshots;
- Project Support snapshots;
- smoke-test evidence.

Required checks:

```text
FINAL PORTABLE RECEIPT: PASS
FINAL PORTABLE BUILDER VERSION: PASS
FINAL PORTABLE FEATURE ID: PASS
FINAL PORTABLE ZIP EXISTS: PASS
FINAL PORTABLE ZIP SHA256: PASS
FINAL PORTABLE ZIP SIZE: PASS
FINAL PORTABLE ZIP CRC: PASS
FINAL PORTABLE ZIP CASE-UNIQUE MEMBERS: PASS
FINAL PORTABLE ZIP PATH SAFETY: PASS
FINAL PORTABLE ZIP STRUCTURE: PASS
FINAL PORTABLE PHYSICAL RUNTIME MANIFEST: PASS
FINAL PORTABLE PHYSICAL RUNTIME HASHES: PASS
FINAL PORTABLE PHYSICAL WORKER ROLES: PASS
FINAL PORTABLE DIRECT EXECUTABLE: PASS
FINAL PORTABLE QT WEBENGINE PROCESS: PASS
FINAL PORTABLE QT WINDOWS PLUGIN: PASS
FINAL PORTABLE NON-RUNTIME DEBRIS ABSENT: PASS
FINAL PORTABLE GENERATED OUTPUT EXCLUSION: PASS
FINAL PORTABLE RUNTIME FREEZE HINT PACKAGE: PASS
FINAL PORTABLE ENVIRONMENT FILE EXCLUSION: PASS
FINAL PORTABLE MEMBER PATH LENGTH: PASS
FINAL PORTABLE MEMBER COUNT: PASS
FINAL PORTABLE SMOKE EVIDENCE: PASS
FINAL PROJECT CONTENT HASH UNCHANGED: PASS
FINAL PROJECT SUPPORT CONTENT HASH UNCHANGED: PASS
FINAL PORTABLE DESTINATION BOUNDARIES: PASS
FINAL PORTABLE QT RUNTIME: PASS
```

Final success requires:

```text
PHASE 05 FINAL PORTABLE VALIDATION: PASS
STATUS: PORTABLE READY AND VALIDATED
```

No earlier marker is sufficient to claim a validated release.

---

## 18. Canonical evidence files

Retain:

```text
portable_result.json
portable_creator_transcript.txt
FINAL_VALIDATION.txt
warn-KandaReasonerWindows.txt
xref-KandaReasonerWindows.html
delivery package manifest
installed creator manifest
physical_runtime_manifest.json
```

These files are the basis for:

- exact failure diagnosis;
- future regression comparison;
- Freeze evidence;
- Error Memory lessons;
- next-session continuation.

Never diagnose from the final generic PowerShell exception alone when the
structured evidence exists.

---

## 19. Warning policy

Current nonblocking warning:

```text
Failed to collect submodules for
kanda_reasoner_app.reasoner_context_collector.developer_tools

ModuleNotFoundError for collector_packaging_metadata
```

The validated v1r11 build still completed:

- Analysis;
- PYZ;
- PKG;
- EXE;
- COLLECT;
- two clean-extraction GUI launches;
- atomic publication;
- independent final validation.

Therefore:

1. keep the warning visible;
2. do not silently suppress it;
3. do not patch the spec blindly;
4. investigate only if an intended `developer_tools` workflow fails or the
   warning is separately selected as a quality repair;
5. validate any correction as its own feature.

---

## 20. Failure-recovery state machine

The creator must fail closed.

### 20.1 Before build

If package, installation, identity, environment, path, or spec validation
fails:

- do not run PyInstaller;
- do not create a candidate;
- do not publish;
- retain diagnostics;
- report the failed phase and next exact action.

### 20.2 During PyInstaller

If PyInstaller returns nonzero:

- retain work, dist, warning, xref, and transcript;
- do not stage or publish;
- report the exact command and exit code.

### 20.3 During staging

If a required physical runtime role or hash fails:

- retain the dist and stage;
- identify the exact role and path;
- do not create or publish the ZIP.

### 20.4 During ZIP validation

If CRC, path safety, structure, Qt runtime, or manifest validation fails:

- retain the candidate;
- do not launch;
- do not publish.

### 20.5 During GUI smoke testing

If the application exits early, remains running, exits nonzero, or a required
feature fails:

- retain candidate ZIP and clean extraction;
- write the exact failure to result JSON;
- do not publish;
- do not freeze;
- do not claim release readiness.

### 20.6 During publication

If partial copy, hash verification, or atomic replace fails:

- leave the validated candidate under transient storage;
- clean incomplete partial files when safe;
- do not report a final release.

### 20.7 During final validation

If Phase 05 fails:

- keep the published artifact but mark it unvalidated;
- do not freeze it as a successful release;
- report the exact failed final check;
- repair only the owning layer.

---

## 21. Common errors and permanent prevention

### Error 1 — PowerShell variable followed by colon

Cause:

```text
$Variable:
```

can be parsed as an invalid variable reference.

Prevention:

```text
${Variable}:
```

or use formatting/concatenation.

### Error 2 — `Out-String` machine identity corruption

Cause: host wrapping modified a long feature ID.

Prevention: compact one-line JSON plus exact field equality.

### Error 3 — raw path-prefix boundary checks

Cause: sibling paths with a shared textual prefix were treated as child paths.

Prevention: resolved component-aware ancestry checks.

### Error 4 — non-JSON-native receipt values

Cause: a Python set reached `json.dumps`.

Prevention: recursively normalize to deterministic JSON-native values.

### Error 5 — coupled Portable, Freeze, and Error Memory workflow

Cause: an unrelated later failure obscured Portable build status.

Prevention: independent workflows and receipts.

### Error 6 — generic exit code masking the inner error

Cause: wrapper showed only exit code 1.

Prevention: structured result JSON, transcript, diagnostic root, exact message.

### Error 7 — synthetic fixture mistaken for live success

Cause: live-looking PASS markers appeared during package validation.

Prevention: explicit scope and mandatory later Phase 04/05 markers.

### Error 8 — human close-confirmation race

Cause: confirmation was typed before process exit was proven.

Prevention: process-aware natural-close validation.

### Error 9 — basename-only path classification

Cause: legitimate runtime `freeze_hint_intake` was confused with generated
external intake.

Prevention: full normalized owner path sequence.

### Error 10 — structural validation without feature testing

Cause: ZIP and main window passed while Validate Project failed.

Prevention: clean-extraction functional smoke checklist.

### Error 11 — physical Python workers omitted

Cause: PyInstaller embedded modules, but GUIs required loose `.py` files.

Prevention: audited physical-runtime hydration and manifest.

### Error 12 — collector fragments omitted

Cause: `collector_main.py` loads helper parts by physical path.

Prevention: explicit `collector_source_parts` role.

### Error 13 — non-worker physical assets omitted

Cause: probe, blueprint, and prompt-workspace paths were not covered.

Prevention: audit subprocess targets and external workspaces, not only GUI
worker loaders.

### Error 14 — PyInstaller warning treated without evidence

Cause: warning was either considered automatically fatal or safe.

Prevention: preserve warning, correlate with functional behavior.

### Error 15 — ambiguous release authority

Cause: multiple ZIPs shared the same basename.

Prevention: exact final path plus SHA-256.

### Error 16 — Freeze form envelope not recognized

Cause: GUI fell back to a placeholder starter form.

Prevention: verify exact populated feature title, validated files, and evidence
before Preview.

### Error 17 — placeholder Freeze preview looked authoritative

Cause: generated freeze-style text appeared despite blocking errors.

Prevention: blocking errors and placeholders always override rendered status
language.

### Error 18 — mandatory Freeze evidence missing

Cause: `validated_files` and `validation_evidence_summary` were blank.

Prevention: preserve exact current validation lines.

### Error 19 — absolute path in project-relative Freeze field

Cause: external `E:/...` release path was placed in `generated_files` or
`protected_paths`.

Prevention: external paths belong in evidence or notes; governed path fields
must be project-relative.

### Error 20 — Error Memory line-ending hash mismatch

Cause: LF lesson files were rewritten as CRLF before hash comparison.

Prevention: copy intake artifacts byte-for-byte and never normalize before
checking exact hashes.

---

## 22. Freeze after successful Portable validation

Freeze is not part of Portable creation.

Freeze eligibility begins only after:

```text
PHASE 05 FINAL PORTABLE VALIDATION: PASS
STATUS: PORTABLE READY AND VALIDATED
```

Freeze form rules:

- `validated_files`: project-relative only;
- `generated_files`: project-relative only;
- `protected_paths`: project-relative only;
- external final ZIP path and SHA-256 belong in validation evidence or notes;
- preserve literal recognizable evidence lines;
- Preview is read-only;
- Confirm and Write remains human;
- project-specific memory stays under:

```text
<project>_show_project_to_AI/
project_freeze_after_update/
frozen_features_memory
```

Do not store project-specific frozen memory in:

```text
project_freeze_ledger
```

After a confirmed write, refresh startup Freeze context.

---

## 23. Error Memory after successful diagnosis

Error Memory is not part of Portable creation.

Correct routine:

1. create one current-schema lesson candidate per durable, nonduplicate failure;
2. wrap each lesson with:

```text
KANDA_ERROR_LESSON_JSON_BEGIN
{ one JSON object }
KANDA_ERROR_LESSON_JSON_END
```

3. stage byte-for-byte under:

```text
E:\kanda_reasoner_show_project_to_AI\
project_error_memory\
pending_ai_assisted_error_lesson_intake
```

4. do not write directly into canonical Lessons;
5. open Error Memory;
6. review duplicate/overlap/supersession status;
7. human clicks Memorize Error;
8. only successfully memorized lessons participate in canonical Error Memory
   logic.

Do not change line endings before hash verification.

---

## 24. Recommended module ownership

Preserve or converge toward these owners without performing an unnecessary
rewrite:

```text
portable/constants.py
    version, feature ID, required identities

portable/paths.py
    project, Project Support, transient, run-root resolution

portable/destination.py
    native destination selection and boundary validation

portable/environment.py
    governed Python and PyInstaller identity

portable/policy.py
    exclusions, runtime/generated ownership classification

portable/physical_runtime.py
    audited physical-file hydration and manifest

portable/build.py
    PyInstaller execution, Qt checks, stage construction, cleanup

portable/archive.py
    ZIP creation, ZIP validation, clean extraction, GUI smoke, publication

portable/workflow.py
    phase order, snapshots, result state, failure handling

portable/validate_installed.py
    creator payload and installation validation

KandaReasonerWindows.spec
    committed PyInstaller packaging authority

RUN_PORTABLE_CREATION.ps1
    public five-phase Windows PowerShell orchestration

VALIDATE_PACKAGE.py
    delivery-package validation

VALIDATE_FINAL_PORTABLE.py
    independent final published-ZIP validation
```

Do not create duplicate owners for the same responsibility.

---

## 25. Canonical high-level pseudocode

```text
resolve exact project identity
resolve governed Python
resolve Project Support
resolve transient root
validate package ZIP and manifest
install creator transactionally
validate installed creator with compact JSON
require BUILD KANDA PORTABLE
select final destination
validate ownership boundaries
create unique transient run root
snapshot project and Project Support
validate spec and environment
run PyInstaller
validate executable and Qt runtime
hydrate audited physical runtime dependencies
write and verify physical runtime manifest
remove non-runtime debris
validate stage
create candidate ZIP
validate CRC, structure, paths, runtime, exclusions
extract candidate into a clean folder
launch and test first time
require natural clean close
launch the exact extraction a second time
require natural clean close
verify project and Project Support unchanged
publish candidate atomically to selected folder
verify final path, size, and SHA-256
verify project and Project Support unchanged again
write portable_result.json
independently validate the published ZIP
write FINAL_VALIDATION.txt
print STATUS: PORTABLE READY AND VALIDATED
only afterward prepare Freeze and Error Memory intake
```

---

## 26. Required next-AI behavior

At the start of a future Portable task, the next AI must:

1. identify the current validated Portable builder revision;
2. read the current installed creator manifest;
3. read the latest successful result JSON and final validation report;
4. compare current source/spec/runtime dependencies with the v1r11 baseline;
5. determine whether a rebuild is requested or a defect is being repaired;
6. preserve passed phases and resume from the last reliable marker;
7. avoid speculative changes;
8. issue one paste-safe PowerShell unit at a time;
9. prefer packaged scripts instead of giant inline PowerShell;
10. never emit detached `else`, `elseif`, `catch`, or `finally`;
11. never claim live validation from sandbox/package fixtures;
12. never freeze or memorize errors automatically;
13. preserve exact hashes and byte identity;
14. keep the final user-facing release identity explicit.

---

## 27. Definition of done

The Portable task is complete only when all are true:

```text
PHASE 01 PACKAGE VALIDATION: PASS
PHASE 02 CREATOR INSTALLATION: PASS
PHASE 02 EXACT LIVE HASHES: PASS
PHASE 02 MACHINE IDENTITY JSON: PASS
PHASE 03 LIVE CREATOR VALIDATION: PASS
PORTABLE PYINSTALLER BUILD: PASS
PORTABLE PHYSICAL RUNTIME REQUIRED ROLES: PASS
PORTABLE HUMAN GUI SMOKE TEST: PASS
PORTABLE PROJECT SOURCE UNCHANGED: PASS
SHOW PROJECT SUPPORT UNCHANGED: PASS
PORTABLE ATOMIC PUBLICATION: PASS
PHASE 04 PORTABLE CREATOR: PASS
FINAL PORTABLE PHYSICAL RUNTIME HASHES: PASS
FINAL PORTABLE SMOKE EVIDENCE: PASS
FINAL PROJECT CONTENT HASH UNCHANGED: PASS
FINAL PROJECT SUPPORT CONTENT HASH UNCHANGED: PASS
FINAL PORTABLE DESTINATION BOUNDARIES: PASS
PHASE 05 FINAL PORTABLE VALIDATION: PASS
STATUS: PORTABLE READY AND VALIDATED
```

Anything less is a candidate, partial build, package fixture, or failed release,
not a validated Portable.

---

## 28. Final instruction to the next AI

Use v1r11 as the canonical working baseline.

Do not restart the design from zero.

Do not treat a single error as proof that the entire architecture must be
replaced.

Read the retained evidence, identify the exact owner, repair the smallest
layer, preserve all previously passed contracts, rerun only affected phases,
and require the complete final acceptance markers before declaring success.

The main lesson is:

```text
A reliable Portable is not “a PyInstaller build that opens.”

It is a governed release produced by:
exact identity
+ isolated build roots
+ audited physical runtime dependencies
+ clean ZIP validation
+ two real functional GUI tests
+ immutable source boundaries
+ atomic publication
+ independent final validation
+ human Freeze and Error Memory completion.
```
