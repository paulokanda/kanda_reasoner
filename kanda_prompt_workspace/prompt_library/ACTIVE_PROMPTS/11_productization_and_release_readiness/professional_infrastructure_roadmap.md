---
prompt_id: kanda_professional_infrastructure_roadmap
version: 1.0.0
status: active_roadmap_prompt
prompt_type: professional_infrastructure_roadmap
scope: Kanda Reasoner validation, patch, freeze, and handoff infrastructure
recommended_group: high_risk_engineering
---

# Professional Infrastructure Roadmap

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


**Project:** Kanda Reasoner / selected project root  
**Project root:** `E:\\selected_project`  
**Document purpose:** Complete analysis of missing infrastructure to make AI-assisted patch work tracked, validated, auditable, recoverable, and safely freezable.  
**Date:** 2026-06-05

---

## Current situation

The workflow discipline already in place is strong:

> inspect evidence → identify box → narrow patch → surgical ZIP → backup/install → focused tests → regressions → py_compile → workflow validation → architecture validation → freeze only after validation

What is missing is the **enforcement infrastructure** that makes that discipline automatic and auditable — not just personally practiced.

### Active blocker

Tab 7 patch (`tab7_ollama_startup_model_refresh_surgical`) is installed but not frozen. Workflow validation fails because `<project_slug>_split_manifest.json` source_sha256 does not match the current `<project_slug>__complete.json`. The source patch is clean — this is a stale generated artifact, not a code failure.

### Three patches with unresolved state

| Patch | Created | Installed | Validated | Frozen |
|---|---|---|---|---|
| tab4_zip_dialog_start_folder_fix_surgical | Yes | Unknown | Not confirmed | No |
| tab3_failed_load_import_repair_surgical | Yes | Unknown | Not confirmed | No |
| tab7_ollama_startup_model_refresh_surgical | Yes | Yes | Partial — workflow failed | No |

---

## The 10 missing modules

### Priority order (implement one at a time — never batch)

---

### Phase 1 — Evidence Freshness Gate  *(do first — unblocks current Tab 7 freeze)*

**Why first:** The current Tab 7 validation failure is not a code bug. It is a stale generated artifact. An evidence freshness gate would have caught it before full workflow validation ran, told the user exactly what to regenerate, and saved the entire debugging cycle.

**Scope:** Read-only checker. Compares sha256 of `json_complete/<PROJECT_SLUG>__complete.json` against `source_sha256` stored in `json_splitted/<PROJECT_SLUG>_split_manifest.json`. Reports OK or STALE per artifact with a recommended action.

**Owner box:** `kanda_reasoner_app/project_analysis_evidence_freshness/`

**CLI command:**
```powershell
python kanda_reasoner_app\project_analysis_evidence_freshness\evidence_freshness_cli.py --root "$PROJECT_ROOT" --check
```

**Expected output (stale case):**
```
Evidence freshness check
Complete JSON    : OK   <project_slug>__complete.json
Split manifest   : STALE <project_slug>_split_manifest.json
  Expected sha256: <current hash>
  Actual sha256  : <manifest hash>
Recommended action: Run Tab 4 Collector and regenerate split/export files.
```

**Hard constraints:**
- Read-only. No modification to Tab 4 GUI, Run Collector behaviour, architecture/workflow validation rules, or JSON schema.
- Dynamic project root — never hardcode `E:\\selected_project` inside implementation.

**Required tests:**
- `tests/test_evidence_freshness_complete_json.py`
- `tests/test_evidence_freshness_split_manifest_stale.py`
- `tests/test_evidence_freshness_project_slug_dynamic.py`

**Validation chain after implementation:**
```powershell
python tests\test_evidence_freshness_split_manifest.py
python -m py_compile kanda_reasoner_app\project_analysis_evidence_freshness\evidence_freshness_cli.py
python kanda_reasoner_app\manage_workflows\manage_workflows.py --root "$PROJECT_ROOT" --validate
python kanda_reasoner_app\manage_architecture\manage_architecture.py --root "$PROJECT_ROOT" --validate
```

---

### Phase 2 — Patch Registry

**Why second:** Three patches currently exist with unclear installed/validated/frozen state. The registry prevents future AI sessions from mistaking "created" for "frozen" and provides a full, auditable lifecycle trail for every patch.

**Lifecycle states:** `created → installed → focused_validated → fully_validated → frozen`  
Also tracks: `created → installed → failed → restored` and `abandoned`.

**Owner box:** `kanda_reasoner_app/patch_registry/`

**Evidence output:** `<PROJECT_ROOT>\project_analysis_evidence\patch_registry\validated_patches.json`

**Implementation files:**
- `patch_registry.py`
- `patch_registry_models.py`
- `patch_registry_io.py`
- `patch_registry_cli.py`

**CLI commands:**
```powershell
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --list
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --status PATCH_NAME
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --record-install install_manifest.json
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --record-validation validation_output.json
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --freeze PATCH_NAME
```

**Required behaviour:**
- Use dynamic project root.
- Store project-relative paths where possible; external backup paths only as install evidence.
- Never mark a patch frozen unless validation is fully clean.
- Preserve failed patch attempts for audit — never delete them.
- Never clear terminal logs.

**Required tests:**
- `tests/test_patch_registry_create_update.py`
- `tests/test_patch_registry_status_transitions.py`
- `tests/test_patch_registry_project_agnostic_paths.py`

---

### Phase 3 — Unified Validation Runner

**Why third:** The current validation chain is run manually, step-by-step, and is not reproducible as a single command. One command should run the full chain in declared order, stop on failure (architecture is skipped if workflow fails), write a machine-readable JSON result, update the patch registry, and never clear terminal logs.

**Owner box:** `kanda_reasoner_app/validation_runner/`

**CLI command:**
```powershell
python kanda_reasoner_app\validation_runner\validate_patch.py --root "$PROJECT_ROOT" --patch PATCH_NAME
```

**Chain order:** focused tests → regressions → py_compile → workflow validation → architecture validation → optional GUI checklist

**Evidence output:** `<PROJECT_ROOT>\project_analysis_evidence\validation_runs\<PATCH_NAME>_<timestamp>.json`

**Critical terminal log rule:** The runner writes a copy of validation output to the evidence file. It must never erase or truncate terminal output. No `Clear-Host`, `cls`, `clear`, `Reset-Host`, or terminal reset commands.

**Required tests:**
- `tests/test_validation_runner_order.py`
- `tests/test_validation_runner_failure_stops_freeze.py`
- `tests/test_validation_runner_records_json.py`
- `tests/test_validation_runner_preserves_logs_contract.py`

---

### Phase 4 — GUI Smoke Checklist System

**Why fourth:** Unit tests cannot prove that the Tab 7 model dropdown actually shows both Ollama models in the live application. A formal checklist system forces explicit human confirmation before freeze is allowed for any GUI patch.

**Owner box:** `kanda_reasoner_app/gui_smoke_checklists/`

**Evidence folder:** `<PROJECT_ROOT>\project_analysis_evidence\gui_smoke_checks\`

**CLI commands:**
```powershell
python kanda_reasoner_app\gui_smoke_checklists\gui_smoke_cli.py --root "$PROJECT_ROOT" --list
python kanda_reasoner_app\gui_smoke_checklists\gui_smoke_cli.py --root "$PROJECT_ROOT" --show tab7_ollama_model_refresh
python kanda_reasoner_app\gui_smoke_checklists\gui_smoke_cli.py --root "$PROJECT_ROOT" --record tab7_ollama_model_refresh --status passed
```

**Tab 7 checklist (already fully specified — implement this first):**

| Step | Instruction | Expected outcome |
|---|---|---|
| open_app | Open Kanda Reasoner | App opens without traceback |
| open_tab7 | Open Tab 7 | Tab 7 loads without error |
| startup_models | Inspect model dropdown after startup | Both qwen3-coder:30b and qwen2.5-coder:7b are available |
| refresh_models | Click Refresh Models | Dropdown still shows both models |
| log_line | Check Tab 7 log output | Log says: Ollama model refresh found 2 model(s) |

**Freeze gate rule:** For GUI patches, `freeze_allowed` requires automated validation clean AND manual GUI checklist status = passed.

---

### Phase 5 — Freeze Governance Workflow

**Why fifth:** No current mechanism prevents premature freeze. All 9 gates must pass before `freeze_patch.py` writes the frozen status. The command never auto-governs — explicit user approval is always required.

**Owner box:** `kanda_reasoner_app/freeze_governance/`

**CLI command:**
```powershell
python kanda_reasoner_app\freeze_governance\freeze_patch.py --root "$PROJECT_ROOT" --patch PATCH_NAME
```

**The 9 freeze gates:**

1. Patch registry status is `installed`
2. Focused tests passed
3. Regressions passed
4. py_compile passed
5. Workflow validation passed
6. Architecture validation passed
7. GUI checklist passed (if GUI patch)
8. Generated evidence is fresh (if patch touches Tab 4 or evidence)
9. User explicitly issued the freeze command

**Required output:**
```
Freeze allowed: yes/no
Blocking reasons:
  - <reason 1>
  - <reason 2>
```

**Hard constraint:** Does not modify governance/canon automatically. Only updates after explicit user approval.

---

### Phase 6 — Git Checkpoint Gate

**Why sixth:** Surgical backups are the primary recovery layer. Git checkpoints are a second layer that gives the user a clean rollback point before any patch install, at no cost.

**Owner box:** `kanda_reasoner_app/development_safety/`

**Behaviour:** Before patch install, inspect `git status --short`, `git branch --show-current`, `git rev-parse --is-inside-work-tree`. Print recommended checkpoint commands — never auto-commit. Graceful no-op if no Git repo is found.

**Required tests:**
- `tests/test_git_checkpoint_no_repo.py`
- `tests/test_git_checkpoint_dirty_repo.py`
- `tests/test_git_checkpoint_clean_repo.py`

---

### Phase 7 — Patch Install Manifest Indexer

**Why seventh:** Install manifests are written to `E:\\_kanda_patch_backups\\<PATCH_NAME>_<timestamp>\\install_manifest.json` — outside the project root. Without an index, future sessions cannot discover them. The indexer scans the backup root and writes a discoverable index inside project evidence.

**Owner box:** `kanda_reasoner_app/patch_registry/manifest_indexer.py`

**Index output:** `<PROJECT_ROOT>\project_analysis_evidence\patch_registry\install_manifest_index.json`

**Hard constraints:** Read-only by default. Never deletes or moves backup folders. Never clears logs.

---

### Phase 8 — Failure Triage Classifier

**Why eighth:** When validation fails, the user needs to know immediately whether the failure is caused by their patch or by something unrelated. The Tab 7 case is the canonical example: source tests passed, workflow failed because a generated split manifest was stale. A classifier would have output: "Classification: generated-evidence-stale. Action: rerun Tab 4 evidence generation, then validate again."

**Owner box:** `kanda_reasoner_app/validation_runner/failure_triage.py`

**Seven failure classes:**

| Class | Meaning |
|---|---|
| patch-caused | The changed files directly introduced the failure |
| existing-unrelated | Failure existed before this patch |
| generated-evidence-stale | Stale artifact hash mismatch — regenerate evidence |
| environmental | Dependency, path, or environment issue |
| missing-dependency | Required module or tool not installed |
| manual-GUI-needed | Automated tests cannot prove this — human checklist required |
| unknown | Cannot classify — needs manual investigation |

**Required tests:**
- `tests/test_failure_triage_generated_artifact_contract.py`
- `tests/test_failure_triage_py_compile_patch_failure.py`
- `tests/test_failure_triage_missing_dependency.py`

---

### Phase 9 — Prompt and Protocol Enforcement

**Why ninth:** AI workflow rules are currently undocumented inside the app. Every new AI session risks prompt drift. Adding the rules to Tab 9 prompt library ensures every session starts with the correct context, constraints, and workflow.

**Owner box:** Tab 9 prompt library / governance prompts

**Six missing prompt assets:**

1. AI-assisted engineering professional workflow prompt
2. Terminal log preservation canonical overlay
3. Patch registry workflow prompt
4. Freeze governance workflow prompt
5. Validation runner workflow prompt
6. GUI smoke checklist workflow prompt

**Hard constraint:** Every new prompt must be routable through Tab 9 prompt groups. No marooned prompts.

**Canonical terminal log preservation rule (must appear in overlay):**
- Do not use `Clear-Host`, `cls`, `clear`, `Reset-Host`, terminal reset commands, or log cleanup commands.
- Do not provide scripts that close the visible PowerShell session unless explicitly requested.
- Leave install, audit, validation, traceback, and diagnostic output visible.

---

### Phase 10 — End-of-Session Handoff Generator

**Why last:** The handoff document that triggered this analysis was written manually. This module auto-generates it at session end, ensuring nothing is missed and every future AI session receives the same quality of context.

**Owner box:** `kanda_reasoner_app/session_handoff/`

**CLI command:**
```powershell
python kanda_reasoner_app\session_handoff\session_handoff_cli.py --root "$PROJECT_ROOT" --patch PATCH_NAME
```

**Output path:** `<PROJECT_ROOT>\project_analysis_evidence\session_handoffs\<timestamp>__handoff.md`

**Handoff must include:** current task · files changed · patch ZIP name · install manifest path · validation commands run · validation results · failures · freeze status · next steps · do-not-forget rules · relevant evidence freshness status.

---

## Immediate next session — resolve Tab 7 before implementing any phase

Before opening any implementation ticket, resolve the current Tab 7 validation state.

**Step 1 — Refresh generated evidence**

Open Kanda Reasoner → Tab 4 → Run Collector → regenerate split/export JSON evidence.

**Step 2 — Rerun Tab 7 validation**

Run the no-log-clearing validation script. Expected clean result:

```
Tab 7 Ollama startup model refresh tests passed.
PATCH focused direct test exit code: 0
Tab 7 Ollama model registry merge regression tests passed.
Regression direct test exit code: 0
Tab 7 Ollama model refresh registry tests passed.
Regression direct test exit code: 0
py_compile exit code: 0
workflow validation: Summary: pass=8 fail=0 warn=0 skip=3
workflow validation exit code: 0
architecture validation: No validation issues.
architecture validation exit code: 0
Validation failed flag: False
PowerShell session left open. No terminal logs were cleared.
```

**Step 3 — Manual GUI smoke check**

Open Kanda Reasoner → Tab 7 → confirm both models appear in the dropdown:

- `qwen3-coder:30b`
- `qwen2.5-coder:7b`

Click Refresh Models → confirm both remain visible → confirm Tab 7 log reports "2 model(s)".

**Step 4 — Freeze only after clean validation**

Only after clean automated validation AND manual GUI confirmation:

```
Freeze: tab7_ollama_startup_model_refresh_surgical
```

Once Tab 7 is frozen, open a new narrow ticket for Phase 1 — Evidence Freshness Gate.

---

## Implementation rules (apply to every phase)

- Each phase is a separate narrow surgical ticket. Do not batch phases.
- Each phase must pass its own focused tests + regressions + py_compile + workflow validation + architecture validation before being frozen.
- Never hardcode `E:\\selected_project` inside any implementation. Always use dynamic project root.
- Never clear terminal logs. Never use `Clear-Host`, `cls`, `clear`, or `Reset-Host`.
- Never mark a patch frozen unless all applicable gates are clean.
- Do not confuse "patch created" with "patch frozen."
- The next AI must read the latest uploaded evidence before implementing any code.

---

*This document was generated from session analysis on 2026-06-05. No code was changed by this document. Do not freeze anything based on this document alone.*
