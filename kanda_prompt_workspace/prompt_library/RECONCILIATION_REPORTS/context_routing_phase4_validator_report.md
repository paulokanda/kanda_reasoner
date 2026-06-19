# Context Routing Layer Phase 4 Validator Report

Patch: kanda_context_routing_layer_phase4_validator_v1
Owner box: Context Routing Validator Box
Status: draft until local validation output is reviewed

## Purpose

This phase adds a read-only Python validator for the staged KANDA Context Routing Layer package.

The validator checks the prompt laboratory folder only. It does not edit prompts, metadata, routing files, or live app code.

## Files added

- TOOLS/validate_context_routing_layer.py
- METADATA/validate_context_routing_layer.meta.json
- RECONCILIATION_REPORTS/context_routing_phase4_validator_report.md
- _bundle_temp/BUNDLE_MANIFEST_kanda_context_routing_layer_phase4_validator_v1.json

## Validation scope

The validator checks:

- required routing kernel files exist;
- global group index exists and contains 12 groups;
- 12 folder assimilation cards exist;
- folder card index exists and contains 12 folders;
- routing test expectation file parses and contains 10 tests;
- required routing test fields are present;
- JSON files parse;
- forbidden live-app folders are absent from prompt_library.

## Safety boundaries

The validator is read-only.

It must not touch:

- kanda_reasoner_app/
- prompt_library_gui/
- live app files
- runtime source files outside prompt_library

## Known limitation

The validator checks structural consistency. It does not prove that future AI behavior will always route correctly. Human review and manual routing trials are still required before live app integration.
