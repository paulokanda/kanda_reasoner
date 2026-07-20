---
prompt_id: general_prompt_stack_load_order
title: General Prompt Stack Load Order Compatibility Record
version: 2.0
status: deprecated
load_type: compatibility_only
owner_box: 01_session_start_and_navigation
source_stage: prompt-audit-wave3a-session-startup-kernel-v1
---

# General Prompt Stack Load Order Compatibility Record

The former general stack and freeze router is retired.

Current order is owned by the startup source map, `KPR-01-001 start_of_day_master_stack`, `KPR-01-014 ai_prompt_request_canon`, `KPR-02-004 prompt_navigation_index`, and task-specific owners.

Historical identifiers resolve through `KPR-02-005 prompt_substitution_map`.

This record cannot define load order, route tasks, authorize implementation, package patches, validate, or freeze.
