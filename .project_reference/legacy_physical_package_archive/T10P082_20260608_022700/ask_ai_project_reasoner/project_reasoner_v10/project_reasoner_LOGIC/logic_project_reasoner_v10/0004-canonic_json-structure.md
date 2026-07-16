Below is the explanation you can give to another AI about the canonical JSON.

Canonical JSON: detailed structural contract

The canonical file is the main merged project artifact, for example:

project_reasoner_v20_widget_text.json

It is not just a report.
It is a consolidated project-knowledge container that combines:

static project analysis
derived structural indexes
derived architectural summaries
processed runtime projections
the full raw runtime trace payload

The canonical JSON must now be treated as the primary file for reasoning about the project.

Core idea

This JSON has three layers living together in one artifact.

Layer 1: static code intelligence
This comes from parsing the repository and building symbol maps, call maps, widget maps, boundaries, priorities, overlaps, risks, etc.

Layer 2: processed runtime intelligence
This is the normalized runtime material extracted into reasoning-friendly structures such as:
runtime_trace_summary
runtime_signal_connections
runtime_state_snapshots
runtime_call_stack_index

Layer 3: raw runtime truth
This is the full embedded runtime trace under:
runtime_trace_raw

That means the canonical JSON now contains both:
human/AI-friendly processed views
and the raw runtime evidence

Top-level purpose of the file

An AI should understand this file as:
a merged architectural index
a merged operational index
a merged UI/runtime index
a merged evidence artifact

It is suitable for answering:
what files exist
what they do
how symbols relate
where state is mutated
what widgets exist
what runtime actions actually happened in the executed scenario
what connections were recorded
what hotspots and risks exist

Top-level structure

The canonical JSON contains many top-level keys. The important mental grouping is this.

Group A: global metadata and health

collector_info
General metadata about the collector and run context.

project_summary
High-level counters and summary metrics for the project and all collected subsystems.
This is the best first place to inspect for scale and coverage.

collection_config
The collector configuration used to produce the artifact.

errors
Collector-level parse or processing failures that occurred during collection.

warning_index
Per-file warning mapping.

Group B: raw per-file project inventory

files
This is the main per-file payload list.
Each item is one parsed Python file and contains raw and enriched file-level analysis.

Each file record typically contains fields like:

{
    "path": "...",
    "module_name": "...",
    "imports": [...],
    "classes": [...],
    "functions": [...],
    "docstring": "...",
    "comments": [...],
    "strings": [...],
    "entry_markers": [...],
    "ui_keyword_hits": [...],
    "eeg_keyword_hits": [...],
    "semantic_hints": [...],
    "semantic_roles": [...],
    "primary_role": "...",
    "secondary_roles": [...],
    "role_confidence": ...,
    "summary": "...",
    "source": "...",
    "git_metadata": {...},
    "coverage_metadata": {...},
    "parse_warnings": [...],
    "module_responsibility_summary": {...},
    "localization": {...},
    "module_role": {...},
    "global_state": {...},
    "symbol_index": {...},
    "event_propagation": {...},
    "change_impact": {...}
}

Important interpretation:
files is the richest static raw layer.
If an AI needs per-module facts, this is the first detailed source.

Group C: core code-structure indexes

symbol_index
Global symbol-to-location map.

import_graph
Module import relationships.

call_edges
Cross-symbol or cross-file call relationships.

keyword_index
Currently empty placeholder in your present build.

semantic_roles
Per-file semantic role summary.

symbol_summaries
Human-readable semantic summaries for symbols.

snippet_index
Context snippets around functions, classes, methods.

duplicate_symbols
Detected duplicate symbol definitions.

test_links
Links between test artifacts and source artifacts.

Group D: UI and widget intelligence

qt_signal_map
Static Qt signal extraction map.

widget_registry
Registry of detected widgets.

widget_summary
Counts and aggregate widget metrics.

widget_hotspots
High-value widget concentration points.

widget_text_index
Index of widget display texts.

widget_text_hotspots
Most important duplicated or concentrated widget-text areas.

widget_layout_index
Widget layout mapping and layout summary.

widget_layout_hotspots
Layout concentration or layout anomaly hotspots.

widget_ui_action_bridge
Bridge between widgets and UI actions.

widget_ui_action_hotspots
High-value widget-to-action hotspots.

ui_action_index
Normalized UI action map.

ui_action_summary
Aggregate UI action counts.

ui_action_hotspots
Most important UI action hotspots.

Important interpretation:
This group is the canonical UI reasoning layer.
If an AI is trying to answer:
what widget triggers what
where are buttons or line edits concentrated
what textual UI exists
what layouts exist
this group is the primary source.

Group E: state, ownership, execution, buckets

attribute_state_map
Attributes and state-related mapping.

object_ownership
Ownership map for objects/components.

execution_chains
Entry-driven execution chains.

subsystems
Subsystem summaries.

bucket_index
Bucket classification per file.

bucket_summary
Aggregate bucket summaries.

bucket_insights
Bucket-level hotspot reasoning.

entry_bucket_flows
Entry-to-bucket flow mapping.

entry_bucket_flow_summary
Summary of entry-bucket traversal.

Important interpretation:
This group answers:
what owns what
how execution begins
how files cluster by purpose
how entry points propagate through the project

Group F: architecture and risk layers

boundary_index
Architectural boundaries inferred across files.

boundary_summary
Counts of controllers, services, domains, etc.

boundary_handoffs
Cross-boundary handoff records.

boundary_violation_index
Potential boundary breaches.

boundary_violation_summary
Aggregate boundary violation info.

boundary_violation_hotspots
Most important violations.

orchestration_index
Orchestration candidates and orchestration structure.

orchestration_summary
Orchestration-level aggregates.

orchestration_hotspots
High orchestration concentration or risk.

state_mutation_index
State mutation candidates.

state_mutation_summary
Aggregate mutation insights.

state_mutation_hotspots
High-risk or central state mutation areas.

persistence_io_index
Persistence and file/database IO structures.

persistence_io_summary
Aggregate persistence info.

persistence_io_hotspots
Important persistence risk points.

event_propagation_index
Event propagation inference.

event_propagation_summary
Aggregate event routing info.

event_propagation_hotspots
Most important event hubs.

canonical_conflict_index
Potential canonical-vs-legacy conflicts.

canonical_conflict_summary
Aggregate conflict summary.

legacy_shadow_hotspots
Legacy shadowing hotspots.

responsibility_overlap_index
Files or modules with overlapping responsibilities.

responsibility_overlap_summary
Aggregate overlap summary.

overlap_hotspots
Most significant overlap zones.

feature_registry
Feature-to-file map.

feature_summary
Feature-level aggregate counts.

feature_hotspots
Feature concentration zones.

implementation_chronology_index
Implementation/migration chronology map.

implementation_chronology_summary
Chronology-level summary.

migration_transition_hotspots
Migration hotspots.

config_schema_registry
Configuration keys and schema registry.

config_schema_summary
Config summary counts.

schema_risk_hotspots
Schema risk points.

state_lifecycle_index
Reset/rehydration/state lifecycle reasoning.

state_lifecycle_summary
Lifecycle-level aggregate metrics.

state_lifecycle_hotspots
Lifecycle risk points.

change_impact_index
Predicted impact of edits.

change_impact_summary
Impact summary.

high_risk_edit_hotspots
Files or zones with high edit risk.

active_code_index
Active/relevant code map.

active_code_summary
Active-code summary.

untested_critical_hotspots
High-risk untested active zones.

Important interpretation:
This is the canonical architecture-governance layer.
If an AI must reason about risk, ownership, boundaries, refactors, canonical paths, migration, or edit safety, this group is the main source.

Group G: runtime-derived processed intelligence

runtime_scenario_index
Scenario-level runtime aggregation.

runtime_scenario_summary
Runtime scenario counts.

runtime_scenario_hotspots
Scenario hotspots.

runtime_feature_attribution_index
Runtime-to-feature attribution mapping.

runtime_feature_attribution_summary
Aggregate feature runtime hits.

runtime_feature_attribution_hotspots
Runtime feature hotspots.

runtime_trace_summary
Processed summary extracted from raw runtime trace.

runtime_signal_connections
Processed signal connection records extracted from runtime trace.

runtime_state_snapshots
Processed runtime state snapshots extracted from runtime trace.

runtime_call_stack_index
Processed call-stack grouping/index derived from runtime trace.

Important interpretation:
This is the runtime reasoning layer optimized for queries.
If an AI wants a normalized runtime answer, use these fields first.

Group H: raw runtime preserved inside canonical JSON

runtime_trace_raw_path
Absolute path of the runtime trace file used as source.

runtime_trace_raw_counts
Quick raw counts:
event count
signal connection count
state snapshot count
error count
warning count

runtime_trace_raw
The full raw runtime trace JSON embedded directly into the canonical file.

This raw structure itself contains:

{
    "trace_info": {...},
    "session_info": {...},
    "events": [...],
    "signal_connections": [...],
    "state_snapshots": [...],
    "errors": [...],
    "warnings": [...]
}

This means the canonical JSON now preserves all runtime-trace information, not only projections.

Runtime raw event structure

Each raw event is typically shaped like:

{
    "id": ...,
    "time": "...",
    "timestamp": "...",
    "type": "...",
    "event_type": "...",
    "source_file": "...",
    "source_symbol": "...",
    "message": "...",
    "object_name": "...",
    "object_type": "...",
    "tags": [...],
    "extra": {...}
}

Runtime raw signal connection structure

Each raw signal connection is typically shaped like:

{
    "id": ...,
    "time": "...",
    "timestamp": "...",
    "sender_type": "...",
    "sender_name": "...",
    "signal_name": "...",
    "receiver_type": "...",
    "receiver_name": "...",
    "slot_name": "...",
    "source_file": "...",
    "caller_file": "...",
    "source_line": ...,
    "caller_line": ...,
    "extra": {...},

    # compatibility aliases
    "widget": "...",
    "widget_name": "...",
    "widget_type": "...",
    "signal": "...",
    "handler": "...",
    "target": "...",
    "target_kind": "...",
    "line": ...
}

Runtime raw state snapshot structure

Each raw state snapshot is typically shaped like:

{
    "id": ...,
    "time": "...",
    "timestamp": "...",
    "label": "...",
    "context": "...",
    "state": {...}
}

Trust model for an AI using this JSON

An AI should reason with the following trust order.

Most authoritative for “what happened at runtime”:
runtime_trace_raw

Best normalized runtime layer for fast reasoning:
runtime_trace_summary
runtime_signal_connections
runtime_state_snapshots
runtime_call_stack_index

Best static per-file truth:
files

Best fast project overview:
project_summary

Best architecture/risk reasoning layer:
all boundary, orchestration, state, persistence, overlap, impact, active-code sections

Canonical interpretation rule

If there is any tension between:
a processed runtime field
and
the raw runtime trace

the raw runtime trace should be considered the source of truth for runtime facts.

If there is any tension between:
a summary count
and
the deeper indexed structure

the deeper indexed structure should be trusted over the summary count.

What this canonical file can answer well now

An AI can now answer, from one file alone:

what files exist and what they appear to do
what the project’s main symbols and import/call relations are
what widgets, texts, layouts, and UI actions exist
which files are controllers/services/domains/orchestrators
where state is mutated
where persistence occurs
where edit risk is high
what runtime scenario actually ran
which runtime events occurred
which signal-slot connections were recorded
what runtime state snapshots were captured
and it can inspect the full original runtime evidence without opening a second file

What this canonical file is now

The best description is:

a merged static-plus-runtime project intelligence artifact
with both indexed reasoning views and embedded raw runtime evidence

Short version for another AI

If you want a short copy-paste description for another AI, use this:

The canonical JSON is the main project artifact. It contains:
1) static project analysis across the repo,
2) processed runtime projections,
3) the full raw runtime trace embedded under runtime_trace_raw.

Use project_summary for overview.
Use files for detailed per-module facts.
Use symbol_index/import_graph/call_edges for code structure.
Use widget_registry/ui_action_index/widget_layout_index for UI reasoning.
Use boundary/orchestration/state/persistence/change_impact sections for architecture and risk reasoning.
Use runtime_trace_summary/runtime_signal_connections/runtime_state_snapshots/runtime_call_stack_index for normalized runtime reasoning.
Use runtime_trace_raw as the source of truth for exact runtime facts.

The canonical JSON is now self-contained for both static and runtime project reasoning.

If you want, I can next turn this into a strict schema-style document with section-by-section field definitions and intended AI usage rules.


