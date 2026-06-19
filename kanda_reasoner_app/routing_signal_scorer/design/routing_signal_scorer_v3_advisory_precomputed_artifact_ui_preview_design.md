# Routing Signal Scorer v3 Advisory Precomputed Artifact UI Preview Design v1

Feature ID: `routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design_v1`

## Purpose

This patch adds an advisory UI preview design for future precomputed semantic
evidence artifact summaries. It is intentionally schema/design-only and adds
no UI implementation, no artifact reader, and no artifact loading behavior.

The semantic layer remains an untrusted evidence witness.

It may provide evidence. It may never provide authority.

## What this design allows

- Describing future preview sections for a redacted artifact summary.
- Declaring preconditions for any future UI preview implementation.
- Producing review-evidence-only denial and checklist reports.
- Keeping all artifact reading and semantic runtime behavior disabled.

## What this design does not authorize

This design does not authorize UI preview implementation.

This design does not authorize artifact reading for display.

This design does not authorize artifact loading at startup.

This design does not authorize artifact loading at runtime.

This design does not authorize raw text display.

This design does not authorize vector display.

This design does not authorize provider execution.

This design does not authorize semantic runtime enablement.

This design does not authorize threshold changes.

## Preview boundary rules

A future artifact UI preview must remain manually invoked, disabled by
default, schema-validated, redacted, review-evidence-only, and governed by a
separate patch and freeze. No startup loading. No runtime loading. No
background loading. No file-watcher loading. No automatic artifact discovery.
No automatic refresh.

The advisory precomputed artifact UI preview can only produce review
evidence. It may never enable semantic runtime behavior, may never mutate the
prompt router, may never auto-load prompts, may never decide final route, and
may never write freeze memory.

## Required future display sections

A future UI preview may show only redacted metadata summaries such as:

- artifact identity summary
- frozen manifest reference summary
- frozen gold-set reference summary
- schema validation status summary
- eligibility counts summary
- ambiguity policy summary
- stale/deprecated suppression summary
- no-authority banner
- review-evidence-only banner
- disabled-runtime banner

## Dependency and runtime position

This phase adds no external dependency. It adds no UI, no artifact reader,
no artifact loader, no provider, no model, no runner, no embedding
dependency, no vector database, no network call, no file watcher, and no
runtime loader.

## Do-not-regress summary

Preserve advisory only. Preserve standard library only. Preserve advisory
artifact UI preview design. Preserve no UI preview implementation. Preserve
no artifact reader. Preserve no artifact loading. Preserve no raw text
display. Preserve no vector display. Preserve no semantic runtime
enablement. Preserve no cross-box mutation.
