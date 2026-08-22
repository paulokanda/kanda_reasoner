---
prompt_id: project_startup_canon_template
prompt_code: KPR-01-006
title: Project Startup Profile Authoring Template
version: 2.0
status: active
load_type: on_request
owner_box: 01_session_start_and_navigation
source_stage: prompt-audit-wave3a-session-startup-kernel-v1
---

# Project Startup Profile Authoring Template

## Mission

Draft a stable Project-specific startup profile or overlay without executing startup, changing global canons, or writing Project state.

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

## Include only stable Project facts

- Project identity and source root;
- external Project-support root;
- canonical architecture and workflow documents;
- primary boxes and public contracts;
- durable evidence and memory locations;
- required local environment facts;
- Project-specific restrictions;
- approved overlay routes;
- freshness and invalidation conditions.

## Exclude session-specific facts

Do not embed the current task, current patch, current operation ID, temporary target, daily-work paths, transient validation output, mutable runtime state, or one-session decisions.

## Global versus Project boundary

- Global canons remain global owners.
- The Project profile may narrow or specialize behavior but must not silently weaken global safety contracts.
- Project source, support artifacts, optional lesson/error memory, optional snapshot/freeze memory, and generated evidence remain owned by their declared Project or host owners.
- Tool and Project identity remain logically separate during self-hosting.

## Required output

Return `PROJECT STARTUP PROFILE DRAFT` containing:

- proposed identity;
- stable fields;
- excluded transient fields;
- canonical owner references;
- unresolved conflicts;
- validation obligations;
- registration owner;
- `source_write_authorization: NO`.

## Authority boundary

This template does not register an overlay, modify startup delivery, write Project files, select a Project, authorize coding, or write snapshot/freeze state.
