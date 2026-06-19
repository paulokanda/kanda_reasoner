---
prompt_id: kanda_patch_registry_validation_freeze
version: 1.0.0
status: active_roadmap_prompt
prompt_type: professional_infrastructure_roadmap
scope: patch registry, validation runner, freeze governance, GUI checklist, and failure triage
recommended_group: high_risk_engineering
---

# Patch Registry Validation and Freeze

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


## Purpose

Convert the AI-assisted patch workflow from personal discipline into auditable
project infrastructure.

## Principle

Do not confuse these states:

```text
created
installed
focused_validated
fully_validated
frozen
failed
restored
abandoned
```

A patch is not frozen just because it was created, installed, or partially
validated.

## Phase 1 - Patch Registry

Owner box:

```text
kanda_reasoner_app/patch_registry/
```

Evidence output:

```text
project_analysis_evidence/patch_registry/validated_patches.json
```

Required CLI:

```powershell
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --list
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --status PATCH_NAME
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --record-install install_manifest.json
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --record-validation validation_output.json
python kanda_reasoner_app\patch_registry\patch_registry_cli.py --root "$PROJECT_ROOT" --freeze PATCH_NAME
```

## Phase 2 - Unified Validation Runner

Owner box:

```text
kanda_reasoner_app/validation_runner/
```

Run order:

```text
py_compile
hallucination detector, when available
focused unit tests
focused integration tests
regression tests
performance benchmark, when required
workflow validation
architecture validation
manual GUI checklist, when visual
freeze gate
```

Outputs:

```text
project_analysis_evidence/validation_runs/<PATCH_NAME>_<timestamp>.log
project_analysis_evidence/validation_runs/<PATCH_NAME>_<timestamp>.results.json
```

The terminal output must remain visible. The runner may copy output into files,
but it must not clear, truncate, or hide terminal logs.

## Phase 3 - GUI Smoke Checklist System

Owner box:

```text
kanda_reasoner_app/gui_smoke_checklists/
```

For GUI patches, freeze requires a recorded human checklist result.

## Phase 4 - Freeze Governance Workflow

Owner box:

```text
kanda_reasoner_app/freeze_governance/
```

Freeze gates:

1. Patch registry status is installed.
2. Focused unit and integration tests passed.
3. Regression tests passed.
4. py_compile passed.
5. Workflow validation fail=0.
6. Architecture validation has no issues.
7. GUI checklist passed if GUI patch.
8. Generated evidence is fresh if relevant.
9. User explicitly issued freeze.

## Phase 5 - Failure Triage Classifier

Failure classes:

```text
patch-caused
existing-unrelated
generated-evidence-stale
environmental
missing-dependency
manual-GUI-needed
unknown
```

## Phase 6 - Supporting infrastructure

Add after the core workflow exists:

```text
Git Checkpoint Gate
Patch Install Manifest Indexer
State-Based Testing Sandbox
Human Override Log
End-of-Session Handoff Generator
```

## Out of scope

- Do not implement all phases in one bundle.
- Do not freeze official governance from this roadmap alone.
- Do not auto-commit Git changes.
- Do not create hidden patch state that is only stored in chat.
