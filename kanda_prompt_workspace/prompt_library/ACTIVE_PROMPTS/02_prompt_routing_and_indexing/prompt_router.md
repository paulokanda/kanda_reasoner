---
prompt_id: prompt_router
title: Prompt Router Compatibility Redirect
version: 2.0
status: deprecated
load_type: compatibility_only
owner_box: 02_prompt_routing_and_indexing
source_stage: prompt-audit-wave2b-legacy-routing-retirement-v1
---

# Prompt Router Compatibility Redirect

## Lifecycle state

`prompt_router` and the historical alias `kanda_prompt_router` no longer own task routing.

This file remains only to preserve address continuity for old links, audits, and saved references. It must not be selected for new work and must not accumulate specialist rules.

## Current destinations

- Request admission and missing context: `KPR-01-014 ai_prompt_request_canon`.
- Human-readable prompt lookup: `KPR-02-004 prompt_navigation_index`.
- Routing architecture and machine-route contracts: `KPR-02-002 kanda_routing_system_canon`.
- Historical identity lookup: `KPR-02-005 prompt_substitution_map`.
- Governed implementation authorization: `KPR-03-001 brick_wall_comprehensive_quality_gate`.

## Compatibility behavior

When an old artifact requests `prompt_router` or `kanda_prompt_router`:

1. classify the reference as deprecated;
2. resolve the required current owner through KPR-02-005;
3. load only the smallest current owner set;
4. do not execute instructions from historical router bodies;
5. do not restore broad aliases, route tables, patch rules, freeze rules, or specialist implementation logic here.

## Authority boundary

This compatibility record cannot route, authorize coding, select prompts, mutate source, validate, deliver patches, write freeze memory, activate ML, or replace current machine route data.
