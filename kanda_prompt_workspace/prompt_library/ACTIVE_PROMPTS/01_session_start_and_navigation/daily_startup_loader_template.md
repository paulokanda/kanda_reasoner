---
prompt_id: daily_startup_loader_template
prompt_code: KPR-01-005
title: Daily Startup Loader Authoring Template
version: 2.0
status: active
load_type: on_request
owner_box: 01_session_start_and_navigation
source_stage: prompt-audit-wave3a-session-startup-kernel-v1
---

# Daily Startup Loader Authoring Template

## Mission

Produce a draft, project-agnostic startup-loader specification for review. Do not execute the startup workflow and do not register the draft automatically.

## Required inputs

- intended project or tool type;
- canonical source owner;
- minimum always-loaded context;
- on-demand context sources;
- readiness checkpoints;
- missing-context behavior;
- generated artifact owner;
- validation and regeneration commands;
- migration aliases, if any.

## Draft structure

1. identity and version;
2. one-sentence mission;
3. canonical source and generated-output boundary;
4. minimal startup inputs;
5. on-demand retrieval path;
6. readiness response;
7. hard blockers;
8. authority boundary;
9. validation obligations;
10. migration and rollback notes.

## Authoring rules

- Keep startup minimal.
- Reference specialist owners instead of copying their detailed rules.
- Treat generated startup files as outputs.
- Do not invent current source paths, hashes, validators, or load order.
- Do not add a context engine, registry, mega-prompt, or parallel startup owner.
- Do not write source, metadata, routing, or generated artifacts from this template.

## Required output

Return `DAILY STARTUP LOADER DRAFT` with unresolved placeholders clearly marked and `source_write_authorization: NO`.
