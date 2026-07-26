---
prompt_id: durable_document_artifact_routing_canon
prompt_code: KPR-01-013
title: Durable Documentation Artifact Routing Canon
version: 2.0
status: active
load_type: always_startup
owner_box: 01_session_start_and_navigation
source_stage: prompt-audit-wave3b-specialist-startup-bridges-v1
---

# Durable Documentation Artifact Routing Canon

## Purpose

This prompt is the canonical routing owner for generated documentary artifacts
and durable validation evidence. It decides whether an artifact remains with
canonical source, belongs to a specialized Project Support owner, belongs to the
general durable project-documentation area, or is safely transient.

It does not own patch construction, terminal behavior, freeze forms, Error
Memory schemas, or handoff templates.

## Authority hierarchy

Use this order:

1. Canonical source owner.
2. Specialized Project Support owner.
3. General durable Project Support owner.
4. Transient daily-work owner.

A lower-priority destination must not replace a valid higher-priority owner.

## Classification sequence

Classify every generated documentary artifact through these questions:

```text
DURABLE ARTIFACT ROUTING RECORD
Artifact:
Active Project:
Source authority: CANONICAL_SOURCE / GENERATED_ARTIFACT
If generated, lifetime: DURABLE / TRANSIENT
Specialized owner exists: YES / NO
Selected owner:
Contains failed-validation or blocker evidence: YES / NO
Sensitivity or redaction required: YES / NO
Provenance label:
Write or copy destination:
May clean transient copy: YES / NO
Reason:
```

### Canonical source

Repository documentation, canonical prompts, source-controlled specifications,
and other files that are part of the Tool or Active Project source tree remain
with their source owner. Do not move source truth into Project Support merely
because the file is Markdown, text, JSON, or a report.

### Generated transient artifact

Temporary extraction files, disposable helpers, scratch reports, operational
copies, and reproducible intermediate output may live under the canonical
transient daily-work root. They must be safe to delete and must not be the only
copy of required evidence.

### Generated durable artifact

A generated artifact is durable when it must survive cleanup, support a future
AI or human review, explain a completed feature, support validation or freeze,
preserve a blocker, or continue work in another session.

When no specialized owner exists, use the selected Active Project's general
Project Support documentation area. Derive the root through
`project_tool_boundary_canon`; never hardcode the KANDA Reasoner path for another
project.

### Specialized Project Support owners

Specialized owners take precedence over the general documentation folder.
Examples include:

- Error Memory intake, lessons, and evidence;
- freeze hints, frozen-feature memory, and freeze evidence;
- project handoff and second-upload packages;
- architecture-review Preview and Shadow artifacts;
- collector exports and AI handoff packages;
- feature-specific validation evidence.

Use the current specialist contract. This canon routes to it but does not copy
its schema.

## Validation and blocker evidence

Successful validation evidence that supports release or freeze must be durable.
Failed-validation evidence, rollback evidence, unknown-hash diagnostics, and
unresolved blockers may also be durable when they are required to explain why
work stopped or to prevent unsafe repetition.

Do not label failed evidence as validation success. Preserve status explicitly:

```text
PASS / FAIL / BLOCKED / NOT_RUN / INDETERMINATE
```

An operational copy may remain in daily-work for compatibility, but the durable
owner must be identified before cleanup when the evidence has continuing value.

## Redaction and provenance

Before durable writing:

- remove secrets, credentials, patient data, and unnecessary user-home details;
- retain technical paths only when they are required evidence;
- label whether the artifact came from canonical source, local runtime,
  generated output, external AI, or human input;
- record the project and feature identity when applicable;
- do not present generated text as canonical source truth.

## Cross-owner routing

- Patch construction and delivery: current Class 05 delivery owner.
- Terminal behavior: `terminal_cleanup_contract`.
- Error Memory content and admission: `error_memory_ai_formulary_startup_canon`.
- Session closure: `handoff_at_end_of_work` plus the selected Class 03 template.
- Freeze intake and human confirmation: `freeze_code_intake_and_form_protocol`.
- Tool, Project, Project Support, and transient roots:
  `project_tool_boundary_canon`.

## Failure behavior

If ownership, project identity, sensitivity, or lifetime is unresolved, return:

```text
DURABLE DOCUMENT ROUTING BLOCKED
Artifact:
Unresolved classification:
Candidate owners:
Missing evidence:
Next safe action:
May write: NO
```

Do not guess a durable destination and do not leave important evidence only in a
transient directory.

## Scope exclusions

This prompt does not define:

- Error Memory schemas;
- freeze-form or freeze-hint schemas;
- patch ZIP structure;
- terminal commands;
- handoff templates;
- application storage internals;
- a new document database or registry.

## Do-not-regress rules

- Canonical source remains with its source owner.
- Daily-work remains disposable.
- Durable project artifacts remain attached to the selected project.
- Specialized owners take precedence over general fallback storage.
- Validation and blocker evidence keep honest status and provenance.
- Redaction occurs before durable export.
- Unknown ownership fails closed.
