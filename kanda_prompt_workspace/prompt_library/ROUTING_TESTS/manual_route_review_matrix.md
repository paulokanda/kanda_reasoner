# MANUAL ROUTE REVIEW MATRIX

Patch: kanda_context_routing_layer_phase5_human_review_v1
Purpose: human-readable route review examples

## How to use

Read each request and check whether the routing layer asks for the correct context.

The AI should not load all prompts.
The AI should route by task intent.

## Test matrix

| ID | Human request | Expected route behavior |
| --- | --- | --- |
| MR01 | Explain this prompt. | Fast path. No implementation stack required. |
| MR02 | Create a new folder with a databank. | Implementation path. Require delivery and Python engineering groups. |
| MR03 | Module X is too big. | Require refactor and architecture groups. |
| MR04 | Ok freeze. | Require governance, validation evidence, and handoff context. |
| MR05 | Create handoff for next AI. | Require session and handoff group. |
| MR06 | Audit this prompt batch. | Require prompt authoring and audit group plus routing/indexing group. |
| MR07 | Fix this import error. | Require Python engineering core and patch delivery validation. |
| MR08 | Change only the visual layout. | Require GUI-aware implementation path and delivery validation. |
| MR09 | Review security of this patch. | Require quality, security, and observability group. |
| MR10 | Productization roadmap. | Require productization and release readiness group. |

## Review rule

If a request is simple discussion, the router should not over-ask.

If a request changes files, architecture, governance, validation state, or prompt canon, the router must ask for the correct required context before implementation.
