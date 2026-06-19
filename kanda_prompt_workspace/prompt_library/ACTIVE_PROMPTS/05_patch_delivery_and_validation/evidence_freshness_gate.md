---
prompt_id: kanda_evidence_freshness_gate
version: 1.0.0
status: active_first_implementation_ticket
prompt_type: implementation_roadmap
scope: read-only generated evidence freshness checking
recommended_group: high_risk_engineering
---

# Evidence Freshness Gate

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

Build a read-only checker that detects stale generated evidence before full
workflow validation fails. This should be the first professional infrastructure
module because stale generated evidence blocked the Tab 7 freeze.

## Owner box

```text
kanda_reasoner_app/project_analysis_evidence_freshness/
```

## Required behavior

- Resolve project root dynamically from `--root`.
- Derive project slug dynamically.
- Locate canonical complete JSON under:

```text
project_analysis_evidence/json_complete/<PROJECT_SLUG>__complete.json
```

- Locate split manifest under:

```text
project_analysis_evidence/json_splitted/<PROJECT_SLUG>_split_manifest.json
```

- Compare current complete JSON sha256 with `source_sha256` recorded in the split manifest.
- Also warn if complete JSON is older than the configured threshold, default 7 days.
- Print clear OK or STALE results.
- Never modify source files, generated JSON, manifests, or logs.

## CLI

```powershell
python kanda_reasoner_app\project_analysis_evidence_freshness\evidence_freshness_cli.py --root "$PROJECT_ROOT" --check
```

## Stale output example

```text
Evidence freshness check
Complete JSON  : OK    developer_tools__complete.json
Split manifest : STALE developer_tools_split_manifest.json
Expected sha256: <current complete json hash>
Actual sha256  : <manifest source_sha256>
Recommended action: Run collector and regenerate split/export files.
```

## Tests

```text
tests/test_evidence_freshness_complete_json.py
tests/test_evidence_freshness_split_manifest_stale.py
tests/test_evidence_freshness_project_slug_dynamic.py
tests/test_evidence_freshness_timestamp_staleness.py
```

## Validation

```powershell
python tests\test_evidence_freshness_split_manifest.py
python -m py_compile kanda_reasoner_app\project_analysis_evidence_freshness\evidence_freshness_cli.py
python kanda_reasoner_app\manage_workflows\manage_workflows.py --root "$PROJECT_ROOT" --validate
python kanda_reasoner_app\manage_architecture\manage_architecture.py --root "$PROJECT_ROOT" --validate
```

## Out of scope

- Do not change Tab 4 GUI.
- Do not change collector behavior.
- Do not change splitter schema.
- Do not change workflow validation rules in this first pass.
- Do not auto-regenerate evidence.
