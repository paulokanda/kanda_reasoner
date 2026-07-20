---
prompt_id: project_folder_organization_canon
prompt_code: KPR-04-003
title: Project Folder Organization Canon
version: 4.0
status: active
load_type: routed
owner_box: 04_box_architecture_and_boundaries
source_stage: prompt-audit-wave4b-box-architecture-boundaries-v1
---

# Project Folder Organization Canon

## Purpose

Classify a file or artifact and select the current canonical owner or specialist
placement rule. Prevent source-tree contamination, wrong-root writes, duplicate
ownership, and generated evidence from being treated as source truth.

This prompt consumes root identities from `project_tool_boundary_canon`. It does
not invent an alternate root model or construct Project Support paths.

## Activate when

Use when placement, repository cleanliness, generated artifacts, folder
migration, or owner-zone conflicts are materially involved. Do not load at the
start of every implementation task.

## Artifact classes

Classify the item before selecting a path:

- canonical source or configuration;
- public interface or schema;
- tests and validation-only helpers;
- runtime resource;
- generated build or package output;
- durable project documentation or successful validation evidence;
- Project-local user data or state;
- logs and observability output;
- transient preview, scratch, cache, or daily-work artifact;
- external reference or historical evidence;
- secret or sensitive material governed by a dedicated owner.

Names such as `build`, `dist`, `deprecated`, `backup`, or `generated` are not
universal failures. Current policy, ownership, packaging, and explicit allowlists
control placement.

## Placement method

1. Resolve Tool, Active Project, Project Support, and transient roots through the
   Tool/Project owner when relevant.
2. Identify the responsibility owner and whether an existing specialist canon
   controls the artifact class.
3. Distinguish source truth from generated or durable evidence.
4. Check current consumers, imports, packaging, retention, redaction, and
   lifecycle.
5. Detect conflicting owners, duplicate copies, wrong-root writes, and hidden
   runtime dependencies.
6. Recommend the smallest current canonical path or return `PLACEMENT BLOCKED`.
7. Route source-changing migration to Brick Wall and the applicable delivery
   owner.

## Specialist dispatch

- durable project documents and validation evidence: durable artifact canon;
- Tool, Project, support, and transient roots: Tool/Project boundary canon;
- patch and installer artifacts: Class 05;
- freeze intake and frozen memory: current freeze owners;
- logs, secrets, security, packaging, and runtime data: their current owners.

## Placement assessment

```text
ARTIFACT PLACEMENT ASSESSMENT
Active Project:
Resolved root identities:
Artifact identity and class:
Canonical source authority: YES / NO
Current owner:
Current consumers:
Generated / durable / transient status:
Sensitivity and redaction:
Retention and cleanup:
Packaging or runtime dependency:
Proposed canonical path:
Existing specialized owner consulted:
Conflicting or duplicate locations:
Migration obligations:
Validation obligations:
Placement status: COMPLETE / BLOCKED / NOT_APPLICABLE
Brick Wall authorization still required for writes: YES
May write source from this assessment: NO
```

## Migration obligations

A placement migration may require public imports, configuration, packaging,
tests, documentation, compatibility paths, and cleanup. Do not move a file
without identifying these consumers. Preserve a compatibility redirect only
when a current owner requires it.

## Authority boundary

This canon does not define build systems, execute migration, implement secrets,
write freeze memory, prescribe a fixed patch roadmap, or authorize coding. It
returns a placement decision to the current owner and Brick Wall.
