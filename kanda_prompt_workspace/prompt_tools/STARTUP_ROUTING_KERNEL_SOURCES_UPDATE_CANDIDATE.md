# STARTUP_ROUTING_KERNEL_SOURCES Update Candidate Report

Generated: 2026-06-14T19:04:44.752139Z
Workspace root: E:\kanda_reasoner\kanda_prompt_workspace
Source map: E:\kanda_reasoner\kanda_prompt_workspace\prompt_tools\STARTUP_ROUTING_KERNEL_SOURCES.json
Source map SHA-256: 3800b73f121fd2534810c452f76556fc241f7a21df47eac165db758011af1c5d

## Summary

- Current source-map entries: 8
- Existing marked candidates already mapped: 1
- Missing marked candidates: 0
- Stale source-map entries: 0
- Source-map errors: 0
- Candidate errors: 0
- Warnings: 2
- Suggested next load_order: 9
- Suggested next filename number: 09

## Status meaning

- NO_UPDATE_NEEDED means no marked candidate is missing from the source map.
- UPDATE_CANDIDATE_FOUND means one or more marked candidates need human review.
- AUDIT_ERRORS means source-map or candidate errors must be fixed before changes.

## Source-map errors

- None

## Candidate errors

- None

## Source-map warnings

- startup_sources[3]: prompt_id should be lowercase alphanumeric plus underscores: GROUP_ASSIMILATION_INDEX
- startup_sources[4]: prompt_id should be lowercase alphanumeric plus underscores: FOLDER_ASSIMILATION_CARDS_INDEX

## Sidecar warnings

- None

## Candidate warnings

- None

## Stale source-map entries

- None

## Existing marked candidates already in source map

- handoff_at_end_of_work: prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/handoff_at_end_of_work.md

## Missing startup candidates

- None

## Ignored sidecars

- None

## Required human workflow

1. Review this report.
2. If a missing candidate should be startup-loaded, manually edit STARTUP_ROUTING_KERNEL_SOURCES.json.
3. Re-run this auditor until no unexpected missing candidates remain.
4. Then run sync_startup_routing_kernel_pack.py --ensure-sync --yes.

