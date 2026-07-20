---
prompt_id: project_overlay_selector
prompt_code: KPR-02-003
title: Project Overlay Selector
version: 2.0
status: active
load_type: on_request
owner_box: 02_prompt_routing_and_indexing
source_stage: prompt-audit-wave2a-routing-owner-foundation-v1
---

# Project Overlay Selector

## Mission

Select an existing current Project overlay that matches the active Project identity. The selector never becomes the overlay and never writes Project or Prompt Library files.

## Required inputs

```text
active_project_id
active_project_slug
active_project_root
current overlay registrations or metadata
current Tool/Project identity record
requested task scope
```

## Selection algorithm

1. resolve current Project identity through KPR-12-001;
2. inspect registered overlay metadata, not generated summaries;
3. reject overlays for another Project or stale root identity;
4. reject generated overlay artifacts presented as source;
5. require exactly one current compatible overlay or return no match;
6. if several overlays match, return unresolved conflict and route to Class 07 reconciliation;
7. if no overlay matches, continue with global canon or route to the Project startup template when a new overlay is genuinely required.

## Output

```text
PROJECT OVERLAY SELECTION
Active Project ID:
Active Project root:
Selected overlay ID:
Selected overlay source path:
Overlay version and provenance:
Project identity match: YES / NO / UNRESOLVED
Stale or generated-as-source risk: YES / NO / UNRESOLVED
Selection decision: SELECTED / NO_MATCH / CONFLICT / BLOCKED
May write from this selector: NO
Next owner:
```

## Hard stops

Block selection when:

- Project identity is unresolved;
- more than one current overlay claims the same scope;
- the overlay targets another Project;
- the overlay source does not exist;
- only generated evidence exists;
- the overlay contains hardcoded legacy KANDA roots for a different Project;
- the selector is asked to authorize implementation, delivery, or freeze.

## Boundaries

- KPR-12-001 owns Tool/Project identity and roots.
- Project startup owners define new overlay templates.
- Class 07 owns overlay prompt creation, audit, identity, reconciliation, and insertion.
- Brick Wall owns implementation authorization.
- Freeze and delivery remain with their current owners.

## Trigger scope

Load for Project overlay selection, overlay conflicts, overlay freshness, or global-versus-Project route decisions. Do not load for ordinary current routing when the active overlay is already proven.

## Version history

- 2.0: replaced the hardcoded historical KANDA overlay with a true read-only selector.
