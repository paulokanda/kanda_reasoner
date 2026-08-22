---
prompt_id: plugin_package_import_canon
prompt_code: KPR-12-012
title: Plugin Package Import and Trust Canon
version: 2.0.0
status: active
load_type: on_request
owner_box: 12_generalized_project_canons
classification: portable_package_plugin_trust_transaction_lifecycle_canon
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# Plugin Package Import and Trust Canon

## Purpose

Define safe inspection, trust assessment, import planning, transactional installation, enablement, update, rollback, disablement, and removal for user-importable packages or plugins.

This prompt is a bounded technical contract. It is not a persona, a source-write
authority, a release gate, or proof that implementation or validation occurred.

## Project-agnostic operating rule

This prompt defines standalone Project engineering logic. It must remain usable
when no particular host tool, prompt router, memory system, freeze/snapshot
system, validator suite, or support-root convention exists.

- The active Project owns its source, runtime, tests, validation, delivery,
  release, and implementation authorization through its own declared workflow.
- Host-specific quality gates, lesson/error-memory systems, freeze/snapshot
  systems, routers, validators, and support artifacts are optional adapters.
  Their absence must not block this prompt's technical reasoning.
- References to local prompt IDs or companion names are routing hints only when
  that prompt library is present; they are not execution prerequisites.
- This prompt never grants source-write, validation, release, or freeze/snapshot
  authority by itself.

## When to load

- A user-importable package, extension, plugin, theme, template, workflow, or code bundle is planned.
- Archive trust, permissions, installation destination, update or uninstall is central.
- A portable application-owned container format is being reviewed.

## When not to load

- The artifact is an ordinary governed patch ZIP.
- No import or activation lifecycle exists.
- The task is to create a universal plugin engine without verified product need.

## Authority boundaries

This prompt owns:

- portable package structure and manifest contract;
- archive inspection and containment;
- publisher/authenticity/trust state;
- declared capabilities and permissions;
- import plan, transactional install and lifecycle states;
- update, rollback, disable and uninstall records.

It delegates:

- project/tool destination identity to KPR-12-001;
- code security and sandboxing to KPR-09-014;
- application-specific activation mechanics to the product owner;
- patch delivery to Class 05.

This specialist does not own implementation or release authority. Those remain
with the active Project's declared implementation, validation, and delivery owners.

## Task modes

Choose one visible mode:

- `ANALYZE`: identify the current state, evidence, and gaps.
- `DESIGN`: produce a bounded contract or decision record.
- `REVIEW`: evaluate an existing artifact or implementation.
- `IMPLEMENTATION_GUIDANCE`: describe source work only after exact source and
  separate authorization are available.

## Required evidence

- package bytes/hash, archive format and manifest version;
- publisher/signature or explicit unsigned trust state;
- payload inventory, capabilities, permissions and dependencies;
- target application/version and destination root;
- install/update/uninstall/rollback strategy and negative tests.

## Governing rules

- Reject absolute paths, traversal, drive-qualified members, links or extraction targets outside the staging root.
- Validate archive limits, duplicate members, case collisions, compression ratios and declared payload hashes before install.
- Separate inspection, installation, enablement and execution states.
- Unsigned or unknown-publisher packages require an explicit trust decision and must not be described as verified.
- Executable code is high risk: require least privilege, capability allowlists, isolation where available, and explicit activation.
- Install transactionally with preview, backup, rollback verification and durable receipt.
- Define dependency resolution, compatibility, update, disable, uninstall and orphan-data policy.
- Do not create a generic plugin runtime unless an actual application requirement and owner exist.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `PLUGIN PACKAGE TRUST AND LIFECYCLE RECORD` containing:

- package/manifest/hash identity;
- archive-safety and trust result;
- capabilities/permissions/dependencies;
- destination and import plan;
- install/enable/update/rollback/uninstall lifecycle;
- negative-test and receipt evidence.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO`; any implementation authorization belongs to the active Project's declared authority.

## Version history

- 2.0.0: added archive containment, authenticity, permissions, transactional lifecycle, destination ownership, and code-isolation boundaries.
