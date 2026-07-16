# how deliver project to AI use

## 0. Roadmap purpose

This roadmap defines the final implementation plan to update the "deliver project to AI" logic in KANDA Reasoner.

The goal is to transform Project Structure Map from a large static project dump into a dynamic, project-agnostic, schema-valid, provenance-backed, freshness-aware, task-routed evidence system.

The system must work for any project selected in the Project Structure Map tab path. KANDA Reasoner is only one possible scanned project. No evidence path, filename, validation path, freeze path, or generated artifact path may be hardcoded to KANDA Reasoner.

Final target logic:

Dynamic selected project
-> dynamic evidence root
-> source inventory
-> static and runtime evidence
-> complete JSON
-> AI briefing
-> routing manifest
-> source anchors
-> patch safety routes
-> schemas
-> provenance
-> findings
-> validation state
-> task-specific handoff on demand
-> exact source inspection
-> validation
-> freeze only if validated

## 1. Core principles

### 1.1 Source-truth hierarchy

The implementation must preserve this authority order:

1. Exact source files are truth.
2. Generated JSON files are evidence maps, indexes, and routing aids.
3. Tests and validation prove that changes still work.
4. Freeze memory records only validated behavior.

Generated JSON may guide the AI, but it must never replace exact source inspection before editing.

### 1.2 Dynamic project rule

KANDA Reasoner is dynamic. The selected project changes frequently.

Evidence paths must always be derived from the selected project path.

Required dynamic pattern:

```text
<project_drive>:\<project_name>_architecture_audit\current\
```

Main complete JSON pattern:

```text
<project_drive>:\<project_name>_architecture_audit\current\json_complete\<project_name>__complete.json
```

Example:

```text
Selected project:
E:\kanda_reasoner

Evidence root:
E:\kanda_reasoner_architecture_audit\current\

Complete JSON:
E:\kanda_reasoner_architecture_audit\current\json_complete\kanda_reasoner__complete.json
```

Another example:

```text
Selected project:
D:\my_other_app

Evidence root:
D:\my_other_app_architecture_audit\current\

Complete JSON:
D:\my_other_app_architecture_audit\current\json_complete\my_other_app__complete.json
```

Hardcoded global path to avoid:

```text
E:\kanda_reasoner_architecture_audit\current\json_complete\kanda_reasoner__complete.json
```

That path is valid only when the selected project is KANDA Reasoner on drive E. It is not a universal path.

### 1.3 Evidence is derived data

Treat every generated artifact as derived data.

Primary data:

```text
selected project source files
```

Derived data:

```text
complete JSON
runtime trace
AI briefing
routing manifest
active snapshot
bundle manifest
patch safety routes
findings
task handoffs
```

Each derived artifact must declare what it was derived from.

### 1.4 Backward compatibility first

Do not break the current complete JSON contract in the first implementation phase.

The first changes must be additive:

1. Keep existing complete JSON generation.
2. Add new AI-first companion artifacts.
3. Add schema validation and provenance.
4. Add routing and safety layers.
5. Only later consider splitting or deprecating large complete JSON sections.

### 1.5 No noise inflation

The goal is not more JSON.

The goal is better signal:

1. Smaller first-read context.
2. Better task routing.
3. Better source grounding.
4. Better freshness checks.
5. Better validation honesty.
6. Less repeated text.
7. Runtime trace loaded only when useful.

## 2. Final target artifact structure

For any selected project:

```text
<project_drive>:\<project_name>_architecture_audit\current\
│
├── json_complete\
│   ├── <project_name>__complete.json
│   └── <project_name>__complete_runtime_trace.json
│
├── companions\
│   ├── <project_name>__ai_briefing.json
│   ├── <project_name>__routing_manifest.json
│   ├── <project_name>__bundle_manifest.json
│   ├── <project_name>__file_manifest.json
│   ├── <project_name>__exclusion_rules.json
│   ├── <project_name>__active_snapshot.json
│   ├── <project_name>__validation_state.json
│   ├── <project_name>__patch_safety_routes.json
│   └── <project_name>__dependency_inventory.json
│
├── schemas\
│   ├── ai_briefing.schema.json
│   ├── routing_manifest.schema.json
│   ├── bundle_manifest.schema.json
│   ├── file_manifest.schema.json
│   ├── active_snapshot.schema.json
│   ├── validation_state.schema.json
│   ├── patch_safety_routes.schema.json
│   └── findings_sarif_like.schema.json
│
├── findings\
│   └── <project_name>__findings.sarif.json
│
├── runtime\
│   ├── <project_name>__runtime_summary.json
│   └── <project_name>__runtime_raw.json
│
├── decisions\
│   └── <project_name>__evidence_architecture_decisions.json
│
└── task_handoffs\
    └── generated only on demand
```

Important notes:

1. `json_complete` preserves the old central complete JSON location.
2. `companions` contains AI-first additive artifacts.
3. `schemas` contains validation contracts.
4. `findings` contains structured warnings and risks.
5. `runtime` contains summarized and raw runtime evidence separately.
6. `decisions` records why evidence architecture choices exist.
7. `task_handoffs` is not filled by default. It is generated only for a specific requested task.

## 3. Phase 0 - Current behavior characterization before changes

Before changing the collector, write characterization tests that capture what the current system does.

### 3.1 Dynamic path characterization

Test selected project:

```text
D:\sample_app
```

Expected evidence root:

```text
D:\sample_app_architecture_audit\current\
```

Test selected project:

```text
E:\kanda_reasoner
```

Expected evidence root:

```text
E:\kanda_reasoner_architecture_audit\current\
```

Test selected project:

```text
E:\
```

Expected behavior:

```text
reject unsafe broad root
```

### 3.2 Existing output contract characterization

Verify current required outputs still exist after a normal run:

```text
json_complete\<project_name>__complete.json
json_complete\<project_name>__complete_runtime_trace.json
```

### 3.3 Validation honesty characterization

Given no tests were run:

```text
validation_state must not claim tests passed
```

Given schema validation passed:

```text
validation_state must not claim application validation passed
```

Schema validation only proves artifact shape, not application correctness.

### 3.4 Source tree cleanliness characterization

Generated artifacts must not be written inside the selected source project.

Fail if evidence appears under:

```text
<selected_project_root>\...
```

unless the selected project root itself is explicitly the external audit root, which should normally be rejected as a scan target.

### 3.5 Runtime trace characterization

If runtime trace is enabled:

1. Runtime trace path must be paired with the selected project evidence root.
2. Raw runtime trace must not be loaded into the AI-first default bundle.
3. Runtime summary must be generated or marked unavailable.

## 4. Phase 1 - Dynamic project identity and evidence root resolver

### 4.1 Create one authoritative resolver

Implement a single project identity resolver used by all Project Structure Map outputs.

Required output fields:

```json
{
  "selected_project_root": "D:\\my_project",
  "project_drive": "D:\\",
  "project_name": "my_project",
  "project_slug": "my_project",
  "evidence_root": "D:\\my_project_architecture_audit\\current",
  "json_complete_dir": "D:\\my_project_architecture_audit\\current\\json_complete",
  "companions_dir": "D:\\my_project_architecture_audit\\current\\companions",
  "schemas_dir": "D:\\my_project_architecture_audit\\current\\schemas",
  "findings_dir": "D:\\my_project_architecture_audit\\current\\findings",
  "runtime_dir": "D:\\my_project_architecture_audit\\current\\runtime",
  "decisions_dir": "D:\\my_project_architecture_audit\\current\\decisions",
  "task_handoffs_dir": "D:\\my_project_architecture_audit\\current\\task_handoffs"
}
```

### 4.2 Project name normalization rules

Project name / slug should be safe for filenames.

Recommended rules:

1. Use selected folder name.
2. Lowercase if current project convention already lowercases.
3. Replace spaces with underscores.
4. Remove characters invalid for Windows filenames.
5. Preserve enough identity to avoid collisions.
6. Record both original folder name and normalized slug.

Example:

```json
{
  "project_folder_name": "My App",
  "project_slug": "my_app"
}
```

### 4.3 Unsafe root rejection

Reject:

```text
C:\
D:\
E:\
Desktop
Downloads
Documents
OneDrive root
user home root
system folders
```

unless explicitly allowed by a future advanced option.

### 4.4 Output location guard

Before writing anything, verify:

```text
evidence_root is outside selected_project_root
```

For selected project:

```text
D:\my_project
```

Valid:

```text
D:\my_project_architecture_audit\current
```

Invalid:

```text
D:\my_project\architecture_audit\current
```

### 4.5 Acceptance criteria

Phase 1 passes when:

1. Selected project root resolves dynamically.
2. Evidence root is derived from selected project drive and name.
3. No KANDA-specific evidence path is hardcoded.
4. Unsafe roots are rejected.
5. Existing complete JSON still writes to the dynamic evidence root.

## 5. Phase 2 - File manifest and exclusion policy

### 5.1 Generate file manifest

Create:

```text
companions\<project_name>__file_manifest.json
```

Required content:

```json
{
  "project_identity": {},
  "included_files": [],
  "excluded_files": [],
  "file_counts": {},
  "size_summary": {},
  "generated_at": "...",
  "source_tree_hash": "..."
}
```

Each included file should include:

```json
{
  "path": "relative\\path\\file.py",
  "absolute_path": "D:\\my_project\\relative\\path\\file.py",
  "size_bytes": 1234,
  "modified_at": "...",
  "sha256": "...",
  "category": "source",
  "parser_strategy": "python_ast",
  "parser_confidence": "high",
  "include_reason": "python source file under project root"
}
```

Each excluded file should include:

```json
{
  "path": "relative\\path\\.venv\\...",
  "exclude_reason": "virtual environment",
  "rule_id": "EXCLUDE.VENV"
}
```

### 5.2 Generate exclusion rules artifact

Create:

```text
companions\<project_name>__exclusion_rules.json
```

Required categories to exclude or mark carefully:

1. Virtual environments.
2. Caches.
3. Build directories.
4. Generated evidence folders.
5. Binary files.
6. Very large files.
7. Vendor directories.
8. Temporary files.
9. Logs unless explicitly requested.
10. Private credentials or secrets.
11. Old patch staging folders.
12. Architecture audit output folders.

### 5.3 Add generated-file detection

Mark generated files as evidence, not source truth.

Examples:

```text
*_architecture_audit\current\...
__pycache__
*.pyc
build\
dist\
*.egg-info
```

### 5.4 Acceptance criteria

Phase 2 passes when:

1. Every included file has a reason.
2. Every excluded file has a reason.
3. Evidence output folders are not recursively scanned as source.
4. File manifest includes hashes and modified timestamps.
5. Exclusion rules are visible to AI and future validators.

## 6. Phase 3 - Provenance and derived-data metadata

### 6.1 Add provenance block to every artifact

Every generated JSON must include:

```json
{
  "provenance": {
    "artifact_name": "<project_name>__ai_briefing.json",
    "artifact_type": "ai_briefing",
    "selected_project_root": "D:\\my_project",
    "evidence_root": "D:\\my_project_architecture_audit\\current",
    "generated_at": "...",
    "generator_name": "kanda_reasoner_project_structure_map",
    "generator_version": "...",
    "schema_version": "1.0",
    "source_manifest_hash": "...",
    "upstream_artifacts": [],
    "complete": true,
    "stale": false
  }
}
```

### 6.2 Add derived-from block

For derived summaries:

```json
{
  "derived_from": {
    "primary_source": "selected_project_source_tree",
    "upstream_artifacts": [
      "<project_name>__complete.json",
      "<project_name>__file_manifest.json"
    ],
    "derivation_mode": "deterministic_summary"
  }
}
```

### 6.3 Add artifact identity consistency

All artifacts generated in one run must share:

```text
same project_slug
same evidence_root
same generated_at or generation_run_id
same source_manifest_hash
same generation_run_id
```

### 6.4 Acceptance criteria

Phase 3 passes when:

1. Every JSON artifact has provenance.
2. Artifacts from one run share a generation_run_id.
3. Bundle manifest can prove all artifacts belong to the same selected project.
4. AI can identify stale or mismatched artifacts.

## 7. Phase 4 - Schema contracts

### 7.1 Create schemas

Create schema files:

```text
schemas\ai_briefing.schema.json
schemas\routing_manifest.schema.json
schemas\bundle_manifest.schema.json
schemas\file_manifest.schema.json
schemas\active_snapshot.schema.json
schemas\validation_state.schema.json
schemas\patch_safety_routes.schema.json
schemas\findings_sarif_like.schema.json
```

### 7.2 Validate after writing

After every artifact is written:

1. Load JSON.
2. Validate against schema.
3. Record validation result in bundle manifest.
4. If a required artifact fails schema validation, mark evidence package incomplete.

### 7.3 Schema validation is not app validation

Schema validation means:

```text
the JSON file has the expected shape
```

It does not mean:

```text
the scanned application works
the patch is safe
the tests passed
the freeze is approved
```

### 7.4 Acceptance criteria

Phase 4 passes when:

1. Required JSON artifacts pass schema validation.
2. Invalid JSON fails clearly.
3. Missing required fields fail clearly.
4. Schema results are recorded in bundle manifest.
5. Validation state remains honest and does not confuse schema validation with application validation.

## 8. Phase 5 - Keep complete JSON backward compatible

### 8.1 Preserve current complete JSON

Continue writing:

```text
json_complete\<project_name>__complete.json
```

This remains the canonical complete evidence graph.

Do not remove existing major sections in the first implementation.

### 8.2 Add metadata fields to complete JSON

Add, if not already present:

```json
{
  "schema_version": "1.0",
  "generation_run_id": "...",
  "project_identity": {},
  "evidence_freshness": {},
  "section_loading_policy": {},
  "provenance": {},
  "task_routing_pointer": "companions\\<project_name>__routing_manifest.json"
}
```

### 8.3 Add load tiers without moving sections yet

For each major section, add metadata in bundle manifest or complete JSON:

```json
{
  "section": "runtime_trace_raw",
  "load_policy": "read_only_on_request",
  "reason": "large raw runtime evidence"
}
```

Recommended tiers:

```text
always_read
read_for_routing
read_for_subsystem_edit
read_for_debugging
read_only_on_request
do_not_load_by_default
```

### 8.4 Acceptance criteria

Phase 5 passes when:

1. Existing consumers can still find complete JSON.
2. New metadata exists but does not break old consumers.
3. Large/noisy sections are tagged for loading policy.
4. Complete JSON points to AI-first artifacts.

## 9. Phase 6 - AI briefing

### 9.1 Create AI briefing artifact

Create:

```text
companions\<project_name>__ai_briefing.json
```

This is the first file an AI should read.

### 9.2 Required contents

```json
{
  "artifact_type": "ai_briefing",
  "project_identity": {},
  "freshness_status": {},
  "source_truth_policy": {},
  "evidence_files": {},
  "architecture_summary": {},
  "top_entry_points": [],
  "top_workflows": [],
  "protected_paths": [],
  "generated_files_policy": {},
  "first_read_policy": [],
  "do_not_do": [],
  "fallback_policy": {},
  "validation_policy": {}
}
```

### 9.3 Briefing content rules

The briefing must be:

1. Deterministic.
2. Small.
3. High-signal.
4. Explicit about freshness.
5. Explicit that source files are truth.
6. Explicit that generated JSON does not authorize edits.
7. Explicit about what to read next.

Recommended size:

```text
target: 2 KB to 5 KB
hard max: 10 KB
```

### 9.4 AI briefing must include dynamic root

Example:

```json
{
  "selected_project_root": "D:\\my_project",
  "evidence_root": "D:\\my_project_architecture_audit\\current"
}
```

### 9.5 Acceptance criteria

Phase 6 passes when:

1. AI can read the briefing and understand the project purpose.
2. AI can see whether evidence is fresh.
3. AI knows not to edit from JSON summaries alone.
4. AI knows where the routing manifest is.
5. AI knows which generated files must not be edited.

## 10. Phase 7 - Routing manifest

### 10.1 Create routing manifest artifact

Create:

```text
companions\<project_name>__routing_manifest.json
```

### 10.2 Required contents

```json
{
  "artifact_type": "routing_manifest",
  "project_identity": {},
  "task_routes": {},
  "first_files_to_read_by_task_type": {},
  "evidence_sections_by_task_type": {},
  "forbidden_paths_by_task_type": {},
  "validation_commands_by_task_type": {},
  "fallback_route": {},
  "loading_policy": {}
}
```

### 10.3 Initial task types

At minimum support these routes:

```text
general_project_understanding
gui_tab_change
runtime_bug_debugging
new_feature_patch
refactor_existing_feature
test_creation
validation_update
patch_delivery_update
freeze_workflow_update
startup_delivery_update
prompt_library_update
project_structure_map_update
documentation_help_update
```

### 10.4 Route entry format

Example:

```json
{
  "task_type": "gui_tab_change",
  "always_read": [
    "companions\\<project_name>__ai_briefing.json"
  ],
  "route_read": [
    "companions\\<project_name>__file_manifest.json",
    "json_complete\\<project_name>__complete.json:widget_registry",
    "json_complete\\<project_name>__complete.json:ui_action_index",
    "json_complete\\<project_name>__complete.json:widget_ui_action_bridge"
  ],
  "must_inspect_source_files": [],
  "forbidden_generated_paths": [
    "*_architecture_audit\\current\\*"
  ],
  "required_validation": [],
  "fallback": "search file_manifest and source_file_index by symbol name"
}
```

### 10.5 Routing is advisory

The routing manifest guides the first read. It must not create tunnel vision.

Every route must include a fallback:

```text
If the route does not match the task, consult file_manifest, source_file_index, and search exact source files.
```

### 10.6 Acceptance criteria

Phase 7 passes when:

1. AI can select an evidence route from a task type.
2. AI can identify must-read source files.
3. AI can identify forbidden generated paths.
4. AI has a fallback if no route matches.
5. AI does not need to load the full complete JSON first.

## 11. Phase 8 - Source-truth anchors

### 11.1 Add anchors to important symbols

For important symbols, add:

```json
{
  "symbol_id": "...",
  "name": "...",
  "kind": "function",
  "file_path": "relative\\path\\module.py",
  "absolute_path": "D:\\my_project\\relative\\path\\module.py",
  "start_line": 10,
  "end_line": 55,
  "signature": "def example(...)",
  "docstring_summary": "...",
  "span_hash": "sha256:...",
  "file_hash": "sha256:...",
  "last_modified": "...",
  "parser_strategy": "python_ast",
  "parser_confidence": "high",
  "stable_evidence_id": "..."
}
```

### 11.2 Scope first implementation

Do not anchor everything at first.

Start with:

1. Classes.
2. Functions.
3. Methods.
4. GUI callbacks.
5. Tab registrations.
6. Patch/freeze/startup critical functions.
7. Prompt-routing critical functions.
8. Test functions.
9. Public entry points.
10. File-level important constants only if relevant.

### 11.3 Hash behavior

If source span hash matches:

```text
JSON evidence is consistent for that symbol.
```

If source span hash does not match:

```text
JSON evidence for that symbol is stale.
AI must re-read exact source.
```

Even when hash matches:

```text
AI still must inspect exact source before editing.
```

### 11.4 Acceptance criteria

Phase 8 passes when:

1. Important symbols have line ranges.
2. Important symbols have span hashes.
3. Stale symbols can be detected.
4. AI can cite exact source locations.
5. Source anchors do not duplicate full source text.

## 12. Phase 9 - Parser strategy and confidence

### 12.1 Add parser strategy per file

Each file should declare how it was understood:

```json
{
  "file": "src\\main.py",
  "parser_strategy": "python_ast",
  "parser_confidence": "high"
}
```

Other possible values:

```text
python_ast
tree_sitter_optional_future
text_fallback
metadata_only
binary_skipped
excluded
```

### 12.2 Add confidence levels

```text
high
medium
low
not_parsed
excluded
```

### 12.3 Future-proof non-Python scanning

Do not add heavy multi-language parsing in the first patch.

Prepare adapter boundaries:

```text
Python files -> current Python AST collector
Supported future language -> parser adapter
Unsupported language -> text fallback with low confidence
Binary/generated/vendor -> exclude or metadata only
```

### 12.4 Acceptance criteria

Phase 9 passes when:

1. Every included file has parser strategy.
2. Every included file has parser confidence.
3. AI can tell which files were deeply parsed and which were only lightly indexed.
4. No false confidence is given for unsupported languages.

## 13. Phase 10 - Runtime evidence summarization

### 13.1 Separate runtime summary from runtime raw

Write:

```text
runtime\<project_name>__runtime_summary.json
runtime\<project_name>__runtime_raw.json
```

Keep existing compatibility output if needed:

```text
json_complete\<project_name>__complete_runtime_trace.json
```

### 13.2 Runtime summary contents

Include:

```json
{
  "runtime_available": true,
  "entry_points_observed": [],
  "callback_paths": [],
  "error_events": [],
  "warning_events": [],
  "hot_paths": [],
  "state_mutation_hotspots": [],
  "signal_connections": [],
  "runtime_counts": {},
  "raw_trace_pointer": "runtime\\<project_name>__runtime_raw.json"
}
```

### 13.3 Raw runtime loading policy

Raw trace must be:

```text
read_only_on_request
```

It must not be included in first-load AI context.

### 13.4 Acceptance criteria

Phase 10 passes when:

1. Runtime summary is compact.
2. Raw runtime trace is preserved but not default-loaded.
3. Errors and callback paths are easy for AI to find.
4. Runtime unavailable state is represented honestly.

## 14. Phase 11 - Contextual chunk metadata

### 14.1 Add metadata to AI-loadable chunks

Every AI-loadable section or chunk should include:

```json
{
  "chunk_id": "...",
  "parent_artifact": "...",
  "project_slug": "...",
  "subsystem": "...",
  "task_tags": [],
  "context_header": "...",
  "source_truth": {},
  "load_policy": "read_for_subsystem_edit"
}
```

### 14.2 Purpose

This prevents orphan chunks.

If an AI sees a chunk outside the full complete JSON, it still knows:

1. What project it belongs to.
2. What subsystem it describes.
3. What task it helps with.
4. Whether it points to source truth.
5. Whether it is safe to load by default.

### 14.3 Acceptance criteria

Phase 11 passes when:

1. Important chunks are self-describing.
2. Task handoffs can include selected chunks without losing context.
3. Chunk metadata does not duplicate large source text.
4. Load policy is visible per chunk.

## 15. Phase 12 - Bundle manifest as the evidence control plane

### 15.1 Create or extend bundle manifest

Create:

```text
companions\<project_name>__bundle_manifest.json
```

This is the control plane for generated evidence.

### 15.2 Required contents

```json
{
  "project_identity": {},
  "generation_run_id": "...",
  "artifact_inventory": [],
  "artifact_hashes": {},
  "schema_validation_results": {},
  "freshness": {},
  "compatibility_policy": {},
  "section_loading_policy": {},
  "source_truth_policy": {},
  "evidence_fitness_results": {},
  "package_status": "complete"
}
```

### 15.3 Compatibility policy

Include:

```json
{
  "compatibility_policy": {
    "complete_json_contract": "preserved",
    "new_artifacts_are_additive": true,
    "breaking_schema_changes_allowed": false,
    "deprecated_fields": [],
    "migration_mode": "additive_first"
  }
}
```

### 15.4 Acceptance criteria

Phase 12 passes when:

1. Bundle manifest lists all generated artifacts.
2. Bundle manifest includes hashes and sizes.
3. Bundle manifest records schema validation results.
4. Bundle manifest records freshness status.
5. Bundle manifest shows whether evidence package is complete or incomplete.

## 16. Phase 13 - Freshness and staleness detection

### 16.1 Required freshness fields

Add to bundle manifest, AI briefing, and complete JSON metadata:

```json
{
  "freshness": {
    "generated_at": "...",
    "source_tree_hash": "sha256:...",
    "git_commit": "...",
    "git_dirty": false,
    "source_files_newer_than_evidence": false,
    "stale": false,
    "stale_reasons": []
  }
}
```

### 16.2 Stale behavior

If stale:

```text
AI may use JSON for orientation only.
AI must inspect exact source files before reasoning about implementation.
AI should recommend rerunning Project Structure Map before major edits.
```

### 16.3 Staleness checks

Implement:

1. Source file modified after generated_at.
2. Source tree hash mismatch.
3. Artifact generation_run_id mismatch.
4. Missing upstream artifact.
5. File hash mismatch for source anchor.
6. Dirty git state if available.
7. Evidence root does not match selected project root.

### 16.4 Acceptance criteria

Phase 13 passes when:

1. Stale source changes are detected.
2. AI briefing surfaces stale evidence clearly.
3. Bundle manifest records stale reasons.
4. Stale evidence does not claim edit authority.

## 17. Phase 14 - Findings and warnings

### 17.1 Create findings artifact

Create:

```text
findings\<project_name>__findings.sarif.json
```

Use SARIF-like structure, even if not full SARIF initially.

### 17.2 Finding fields

```json
{
  "rule_id": "KANDA.STALE_EVIDENCE",
  "level": "warning",
  "message": "Source file is newer than evidence artifact.",
  "location": {
    "file": "relative\\path\\file.py",
    "start_line": 120
  },
  "required_action": "Inspect exact source before editing."
}
```

### 17.3 Initial finding types

Support:

```text
KANDA.STALE_EVIDENCE
KANDA.UNSAFE_OUTPUT_PATH
KANDA.SCHEMA_VALIDATION_FAILED
KANDA.MISSING_REQUIRED_ARTIFACT
KANDA.RUNTIME_TRACE_UNAVAILABLE
KANDA.RUNTIME_ERROR_OBSERVED
KANDA.MISSING_TEST_MAPPING
KANDA.HIGH_RISK_EDIT_HOTSPOT
KANDA.GENERATED_FILE_EDIT_RISK
KANDA.BOUNDARY_VIOLATION
KANDA.VALIDATION_NOT_RUN
```

### 17.4 Acceptance criteria

Phase 14 passes when:

1. Warnings are machine-readable.
2. Warnings include action guidance.
3. AI can load findings for safety review.
4. Findings do not replace validation.

## 18. Phase 15 - Patch safety routes

### 18.1 Create patch safety artifact

Create:

```text
companions\<project_name>__patch_safety_routes.json
```

### 18.2 Generate from existing evidence

Do not hand-maintain it manually.

Use:

```text
change_impact_index
boundary_index
boundary_violation_index
high_risk_edit_hotspots
untested_critical_hotspots
web_ai_test_protection_index
file responsibility index
validation_state
findings
```

### 18.3 Required structure

```json
{
  "subsystems": {
    "project_structure_map": {
      "risk_level": "governed",
      "must_read_source_files": [],
      "allowed_edit_zones": [],
      "forbidden_generated_paths": [],
      "required_validation": [],
      "freeze_required": true,
      "notes": []
    }
  }
}
```

### 18.4 Safety rules

Patch safety routes guide AI but do not authorize edits.

Before editing:

1. AI reads briefing.
2. AI reads routing manifest.
3. AI reads patch safety route.
4. AI inspects exact source files.
5. AI creates small patch.
6. Validation runs.
7. Freeze only if validated.

### 18.5 Acceptance criteria

Phase 15 passes when:

1. Every major subsystem has safety guidance.
2. Generated files are clearly forbidden edit targets.
3. Required validations are listed.
4. Freeze-required workflows are marked.
5. Patch safety route is generated dynamically for selected project.

## 19. Phase 16 - Active snapshot redesign

### 19.1 Create active snapshot artifact

Create:

```text
companions\<project_name>__active_snapshot.json
```

### 19.2 Snapshot policy

Do not include full source text for everything.

Use tiers:

```text
hot_set_full_text
important_spans
summary_only
metadata_only
excluded
```

### 19.3 Hot set selection

Full text is allowed only for a small hot set:

1. Main entry points.
2. Current task files if task handoff is requested.
3. Core orchestrators.
4. GUI tab files for GUI tasks.
5. Validation/test harness files.
6. Patch/freeze/startup critical files when relevant.

### 19.4 Avoid duplication

If active_snapshot contains full text for a file, complete JSON should reference it instead of duplicating it.

### 19.5 Acceptance criteria

Phase 16 passes when:

1. Active snapshot is useful but not huge.
2. Source text is not duplicated across many JSONs.
3. Each included source text span has a reason.
4. Generated/cache/vendor files are excluded aggressively.

## 20. Phase 17 - Validation state honesty

### 20.1 Create validation state artifact

Create:

```text
companions\<project_name>__validation_state.json
```

### 20.2 Required fields

```json
{
  "validation_attempted": false,
  "commands_run": [],
  "results": [],
  "last_validation_at": null,
  "validation_summary": "No validation command was run by this evidence generation flow.",
  "schema_validation": {},
  "application_validation": {}
}
```

### 20.3 Separate schema validation from application validation

Schema validation:

```text
JSON artifact shape is valid.
```

Application validation:

```text
project tests, py_compile, startup checks, GUI checks, or other project validation commands actually ran.
```

Never mix them.

### 20.4 Acceptance criteria

Phase 17 passes when:

1. validation_state never claims success without command evidence.
2. Schema validation and application validation are separate.
3. Timestamps and command outputs are recorded when validation runs.
4. AI can see what was not validated.

## 21. Phase 18 - Evidence fitness functions

### 21.1 Add post-generation checks

Run fitness checks after evidence generation.

Required checks:

```text
dynamic_path_ok
outside_source_tree_ok
complete_json_present
required_companions_present
schema_valid
freshness_present
source_anchors_present
validation_honesty_ok
loading_policy_present
backward_compatibility_ok
generated_files_excluded_from_scan
artifact_project_identity_consistent
```

### 21.2 Fitness result format

Record in bundle manifest:

```json
{
  "evidence_fitness_results": {
    "dynamic_path_ok": {
      "passed": true,
      "message": "Evidence root is derived from selected project path."
    }
  }
}
```

### 21.3 Fail behavior

If a critical fitness function fails:

1. Mark evidence package incomplete.
2. Write finding.
3. Do not produce freeze-ready evidence.
4. Do not claim the package is safe for AI handoff.

### 21.4 Acceptance criteria

Phase 18 passes when:

1. Fitness checks run every time.
2. Failures are visible.
3. Bundle manifest records results.
4. Critical failures block safe-handoff status.

## 22. Phase 19 - Architecture decision ledger

### 22.1 Create decision artifact

Create:

```text
decisions\<project_name>__evidence_architecture_decisions.json
```

### 22.2 Purpose

The decision ledger tells future AI why the evidence architecture is shaped the way it is.

### 22.3 Entry format

```json
{
  "decision_id": "EVIDENCE-ADR-0001",
  "title": "Add AI briefing as first-load artifact",
  "status": "accepted",
  "context": "Complete JSON is too large for first-contact AI loading.",
  "decision": "Generate a small AI briefing file before routing.",
  "tradeoffs": {
    "gain": "Higher signal and lower context cost.",
    "cost": "One more generated artifact to validate.",
    "risk": "Briefing may become stale if not tied to freshness metadata."
  },
  "fitness_functions": [
    "ai_briefing_schema_valid",
    "ai_briefing_freshness_present"
  ]
}
```

### 22.4 Initial decisions to record

Record at least:

1. Dynamic evidence root based on selected project.
2. Complete JSON remains backward compatible.
3. AI briefing added.
4. Routing manifest added.
5. Schema validation added.
6. Source anchors added.
7. Raw runtime trace moved to on-demand policy.
8. Patch safety routes added.
9. Task handoffs generated on demand only.
10. Generated JSON remains evidence, not truth.

### 22.5 Acceptance criteria

Phase 19 passes when:

1. Decisions are machine-readable.
2. Decisions explain tradeoffs.
3. Future AI can understand why the system exists.
4. Decision ledger is generated dynamically for the selected project evidence run or maintained as part of KANDA's own evidence architecture.

## 23. Phase 20 - Task-specific handoff generation

### 23.1 Generate task handoffs only on demand

Do not pre-generate many handoffs every run.

Create task handoff only when needed:

```text
task_handoffs\<project_name>__<task_type>_handoff.json
```

### 23.2 Handoff required structure

Every handoff begins with:

```json
{
  "task_type": "...",
  "project_identity": {},
  "freshness_status": {},
  "source_truth_rule": "JSON is evidence. Exact source files are truth.",
  "selected_route": {},
  "must_read_source_files": [],
  "forbidden_generated_files": [],
  "required_validation": [],
  "patch_safety": {},
  "evidence_chunks": [],
  "fallback_policy": {}
}
```

### 23.3 Initial task handoffs

Support on demand:

```text
gui_tab_change
project_structure_map_update
patch_delivery_update
freeze_workflow_update
startup_delivery_update
prompt_library_update
validation_update
runtime_bug_debugging
test_creation
general_project_review
```

### 23.4 Acceptance criteria

Phase 20 passes when:

1. Task handoffs include only relevant evidence.
2. Handoffs repeat source-truth policy.
3. Handoffs include freshness.
4. Handoffs include must-read exact source files.
5. Handoffs include validation requirements.
6. Handoffs are not generated unless requested.

## 24. Phase 21 - Dependency inventory

### 24.1 Create optional dependency inventory

Create:

```text
companions\<project_name>__dependency_inventory.json
```

### 24.2 Python first

For Python projects, collect:

```text
pyproject.toml
requirements.txt
setup.py
setup.cfg
Pipfile
poetry.lock
uv.lock
imported third-party packages
stdlib imports
local imports
```

### 24.3 Purpose

AI should know:

1. Which dependencies are available.
2. Which imports are local.
3. Which imports are standard library.
4. Which imports are third-party.
5. Whether suggesting a new dependency would be risky.

### 24.4 Acceptance criteria

Phase 21 passes when:

1. Dependency file presence is detected.
2. Imports are classified where possible.
3. Missing dependency information is marked honestly.
4. AI is warned before suggesting new dependencies.

## 25. Phase 22 - UI integration

### 25.1 Keep UI simple

The Project Structure Map tab should expose the improved output without overwhelming the user.

Recommended UI additions:

```text
Evidence Root:
<computed dynamic evidence root>

Generation Mode:
- Standard
- Full
- Briefing + Routing Only

Post-generation Status:
- Complete
- Incomplete
- Stale
- Schema failed
- Validation not run

Buttons:
- Run Project Structure Map
- Open Evidence Folder
- Export AI Handoff ZIP
- Generate Task Handoff
- View Findings
```

### 25.2 Do not expose too many files as primary UI

The user does not need to manage every artifact manually.

Show:

1. AI briefing.
2. Routing manifest.
3. Complete JSON.
4. Findings.
5. Bundle manifest.
6. Handoff ZIP.

### 25.3 Acceptance criteria

Phase 22 passes when:

1. User can see dynamic evidence root.
2. User can see evidence package status.
3. User can export handoff.
4. User can generate task-specific handoff.
5. UI does not encourage editing generated files manually.

## 26. Phase 23 - Handoff ZIP contract

### 26.1 ZIP contents

Default AI handoff ZIP should include:

```text
companions\<project_name>__ai_briefing.json
companions\<project_name>__routing_manifest.json
companions\<project_name>__bundle_manifest.json
companions\<project_name>__file_manifest.json
companions\<project_name>__exclusion_rules.json
companions\<project_name>__validation_state.json
companions\<project_name>__patch_safety_routes.json
findings\<project_name>__findings.sarif.json
json_complete\<project_name>__complete.json
runtime\<project_name>__runtime_summary.json
```

Optional:

```text
runtime raw trace
full snippets
task-specific handoff
active snapshot
```

### 26.2 ZIP manifest

The ZIP must include a manifest with:

1. Project identity.
2. Evidence root.
3. Generation run id.
4. Artifact hashes.
5. Schema validation status.
6. Freshness status.
7. Loading instructions.
8. Source-truth policy.

### 26.3 Acceptance criteria

Phase 23 passes when:

1. ZIP contains AI briefing and routing manifest.
2. ZIP does not include unwanted raw runtime by default.
3. ZIP manifest matches contained file hashes.
4. ZIP does not include generated artifacts from another project.
5. ZIP can be understood by another AI without source tree access, but still tells AI source files are final truth before editing.

## 27. Phase 24 - Validation tests for the new architecture

### 27.1 Unit tests

Required tests:

1. Dynamic path resolver.
2. Project slug generation.
3. Unsafe root rejection.
4. Evidence root outside source tree.
5. File manifest inclusion/exclusion.
6. Provenance block generation.
7. Schema validation success/failure.
8. AI briefing generation.
9. Routing manifest generation.
10. Source anchor generation.
11. Staleness detection.
12. Patch safety route generation.
13. Findings generation.
14. Bundle manifest artifact hashing.
15. Validation state honesty.

### 27.2 Integration tests

Required integration scenarios:

1. Scan small Python project.
2. Scan KANDA Reasoner itself.
3. Scan project with no tests.
4. Scan project with runtime trace unavailable.
5. Scan project with generated evidence folder nearby.
6. Scan project with stale source after evidence generation.
7. Generate task handoff for GUI task.
8. Export AI handoff ZIP.

### 27.3 AI retrieval tests

Simulate these tasks:

1. Add a GUI tab.
2. Fix runtime crash.
3. Update patch delivery logic.
4. Update freeze workflow.
5. Write a test for a core function.

Measure:

1. Did AI start with briefing?
2. Did AI use routing manifest?
3. Did AI avoid loading full complete JSON unnecessarily?
4. Did AI identify exact source files?
5. Did AI avoid generated files?
6. Did AI state required validation?

### 27.4 Noise budget tests

Track:

1. Size of AI briefing.
2. Size of routing manifest.
3. Size of default handoff ZIP.
4. Size of complete JSON.
5. Runtime raw size.
6. Token estimate for default AI first load.

Set regression limits:

```text
AI briefing hard max: 10 KB
routing manifest hard max: project-dependent, but should remain compact
runtime raw: not included by default
full complete JSON: not first-loaded by policy
```

### 27.5 Acceptance criteria

Phase 24 passes when:

1. All tests pass.
2. Dynamic root works across different drives.
3. Evidence package is schema-valid.
4. Staleness is detected.
5. Validation honesty is preserved.
6. AI routing improves without source-truth bypass.

## 28. Phase 25 - Migration plan

### 28.1 Migration stage A - Additive only

Add:

```text
ai_briefing
routing_manifest
bundle_manifest extensions
schema validation
provenance
freshness metadata
source anchors
findings
patch safety routes
```

Do not remove complete JSON sections.

### 28.2 Migration stage B - Default loading changes

Update AI handoff instructions:

1. Read AI briefing first.
2. Read routing manifest second.
3. Load selected evidence only.
4. Inspect exact source before editing.
5. Use patch safety and validation state.

### 28.3 Migration stage C - Companion extraction

Move very large raw data to companions or runtime folder, but keep pointers in complete JSON.

Candidates:

```text
runtime_trace_raw
full call_edges
full import_graph
full snippet_index
large widget layout details
```

### 28.4 Migration stage D - Compatibility mode

Offer modes:

```text
Briefing + Routing Only
Standard
Full
Compatibility Full
```

### 28.5 Migration stage E - Deprecation

Only after validation:

1. Mark redundant sections as deprecated.
2. Keep deprecated sections for one release cycle.
3. Remove only after all consumers are updated.

### 28.6 Acceptance criteria

Migration is acceptable only if:

1. Existing complete JSON consumers still work.
2. New AI-first workflow works.
3. No generated evidence path is hardcoded.
4. No freeze/patch/startup gates are weakened.
5. Validation proves behavior.

## 29. Phase 26 - Safety rules that must never regress

### 29.1 Never edit from JSON alone

AI must inspect exact source files before editing.

### 29.2 Never treat generated files as source truth

Generated evidence is evidence, not authority.

### 29.3 Never write generated evidence inside source tree

Evidence goes to:

```text
<project_drive>:\<project_name>_architecture_audit\current\
```

### 29.4 Never hardcode KANDA Reasoner as universal target

KANDA Reasoner is only the selected project when the tab path points to it.

### 29.5 Never claim validation that did not run

Schema validation is not application validation.

### 29.6 Never bypass freeze or confirmation gates

Freeze requires validated behavior and explicit human confirmation where governed.

### 29.7 Never default-load raw trace

Raw runtime is on-demand only.

### 29.8 Never duplicate full source text across many artifacts

Use one authoritative source-text location and references elsewhere.

### 29.9 Never make routing restrictive without fallback

Routing guides the first read. It does not replace source search.

## 30. Final implementation order summary

Recommended implementation order:

1. Characterization tests for current behavior.
2. Dynamic project identity and evidence root resolver.
3. File manifest and exclusion rules.
4. Provenance and derived-data metadata.
5. Schema contracts and schema validation.
6. Backward-compatible complete JSON metadata.
7. AI briefing generation.
8. Routing manifest generation.
9. Source-truth anchors for important symbols.
10. Parser strategy and confidence per file.
11. Runtime summary vs raw separation.
12. Contextual chunk metadata.
13. Bundle manifest as control plane.
14. Freshness and staleness detection.
15. Findings and warnings.
16. Patch safety routes.
17. Active snapshot redesign.
18. Validation state honesty improvements.
19. Evidence fitness functions.
20. Architecture decision ledger.
21. On-demand task handoff generation.
22. Optional dependency inventory.
23. UI integration.
24. Handoff ZIP contract.
25. Full validation test suite.
26. Migration to companion extraction only after compatibility is proven.

## 31. Final target behavior

After this roadmap is implemented, KANDA Reasoner should behave like this:

1. User selects any project folder in the Project Structure Map tab.
2. KANDA derives the project drive, project name, and dynamic evidence root.
3. KANDA scans source files while excluding generated/noisy folders.
4. KANDA builds complete project evidence.
5. KANDA generates AI-first companions.
6. KANDA validates schemas.
7. KANDA records provenance and freshness.
8. KANDA creates source anchors and patch safety routes.
9. KANDA writes findings and validation honesty state.
10. KANDA optionally exports a handoff ZIP.
11. Another AI reads briefing first, routing second, then only the evidence needed.
12. Another AI inspects exact source before edits.
13. Validation proves changes.
14. Freeze records only validated behavior.

## 32. Final principle

KANDA Reasoner must dynamically scan any selected project and produce a schema-valid, provenance-backed, freshness-aware, fitness-tested, task-routed evidence package that helps AI know what to read, what not to read, what exact source files to verify, what generated files to avoid, what validation is required, and why the evidence architecture exists.

The system must maximize useful AI knowledge while minimizing noise and preserving safe programming behavior.
