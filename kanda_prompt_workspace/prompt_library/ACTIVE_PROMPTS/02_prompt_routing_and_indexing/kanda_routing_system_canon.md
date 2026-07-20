---
prompt_id: kanda_routing_system_canon
prompt_code: KPR-02-002
title: KANDA Routing System Canon
version: 3.0
status: active
load_type: on_request
owner_box: 02_prompt_routing_and_indexing
source_stage: prompt-audit-wave2a-routing-owner-foundation-v1
---

# KANDA Routing System Canon

## Mission

Define the architecture and authority boundaries of the KANDA prompt-routing system.

This canon does not perform task implementation, prompt authoring, startup generation, patch delivery, freeze writing, or automatic prompt loading.

## Routing architecture

The routing system has distinct owners:

- request admission: `KPR-01-014 ai_prompt_request_canon`;
- human-readable navigation: `KPR-02-004 prompt_navigation_index`;
- machine-readable route data: `ROUTING/prompt_navigation_index.json`;
- advisory route-choice exchange: `KPR-02-001`;
- Project overlay selection: `KPR-02-003`;
- historical identity resolution: `KPR-02-005`;
- prompt lifecycle and insertion: Class 07;
- governed implementation authorization: Brick Wall.

One owner must not reproduce another owner's full protocol.

## Core invariants

1. Deterministic current metadata and explicit routes are authoritative.
2. Similarity, semantic, ML, and adviser outputs are evidence only unless a separately governed authority change is implemented and validated.
3. Prompts are registered and selected, not globally injected.
4. Route selection requests the smallest complete context.
5. Human-readable and machine-readable route representations must agree.
6. Historical aliases never become active destinations without current lifecycle evidence.
7. Generated startup and prompt-library ZIPs are outputs, not source authority.
8. Routing cannot authorize coding, source writes, patch delivery, validation claims, or freeze.
9. Tool/Project, Box, No-Leak, and MCard owners remain separate.
10. Project-specific routes belong in Project overlays, not the global routing canon.

## Canonical route record

A routable current prompt record should identify, when applicable:

```text
prompt_id
prompt_code
canonical path
category/folder
status
load type
priority
narrow trigger phrases
when to load
when not to load
required companions
optional companions
historical aliases
owner box
version and provenance
```

The route-data owner must fail closed when the target is missing, duplicated, deprecated without a replacement, or inconsistent with metadata.

## Routing sequence

1. classify Fast Path or Routed Work Path;
2. identify current Project and task scope;
3. consult current group/folder indexes;
4. select the smallest exact route from machine data;
5. resolve historical identities through the substitution owner when needed;
6. select a Project overlay only when current Project identity requires it;
7. retrieve only the addressed prompts;
8. activate Brick Wall for governed work;
9. keep specialist implementation with the specialist owner.

## Conflict rules

- Exact current canonical metadata outranks historical prose.
- Active route data outranks deprecated compatibility text.
- A direct current prompt address outranks broad alias matching.
- Multiple equally valid routes require focused clarification or a read-only route review.
- No route may silently downgrade required context to recommended.

## Advisory systems

Similarity and semantic systems may rank or explain candidates. They must not:

- override deterministic route eligibility;
- load prompts automatically;
- decide May proceed now;
- mutate routing metadata;
- persist private queries without a governed owner;
- activate runtime ML or provider behavior.

## Registration boundary

Class 07 owns prompt audit, reconciliation, identity allocation, generalization, and authorized insertion. This canon defines what a complete route record means but does not edit the Prompt Library.

## Startup boundary

Startup owners decide which compact bridges are always loaded. This canon may state required routing invariants but must not reproduce the startup boot sequence.

## Freeze boundary

Routing selects the current freeze owners. It does not authorize Preview, Confirm and Write, frozen-memory writes, or startup freeze-context refresh.

## Validation

Validate:

- one active semantic owner per route responsibility;
- unique prompt codes;
- exact ID/path resolution;
- human/machine route agreement;
- narrow aliases;
- no domain-specific leakage in global routes;
- no historical phase prompt selected for current expansion;
- no duplicate active source;
- no automatic loading or authority escalation.

## Version history

- 3.0: reduced to routing architecture, owner boundaries, route records, and conflict rules.
