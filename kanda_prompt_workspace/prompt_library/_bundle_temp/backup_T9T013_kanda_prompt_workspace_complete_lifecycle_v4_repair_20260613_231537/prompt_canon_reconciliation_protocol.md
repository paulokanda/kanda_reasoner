# Prompt Canon Reconciliation Protocol

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 1.0.0
Status: Reusable prompt-library maintenance protocol
Prompt ID: kanda_prompt_canon_reconciliation_protocol
Prompt type: prompt audit / canon reconciliation protocol
Scope: Use when the user uploads canon notes, handoffs, or roadmap documents and asks whether the ideas should update existing prompts or create new prompts.

## Purpose

Reconcile uploaded Kanda Reasoner canon material with the active prompt library.
The goal is to extract useful ideas without duplicating, over-updating, or
polluting unrelated prompts.

## Core rule

Do not paste every canon idea everywhere. Classify each idea and route it to the
smallest correct prompt asset.

## Decision classes

For each idea, classify it as one of:

```text
ALREADY_PRESENT
UPDATE_EXISTING_PROMPT
CREATE_NEW_PROMPT
REFERENCE_ONLY_NOT_ACTIVE
REQUIRES_GOVERNANCE_FREEZE
DEFER
REJECT
```

## Required workflow

1. Inventory uploaded canon files.
2. Extract unique ideas.
3. Compare against existing active prompts.
4. Identify the correct owning prompt or create a new prompt only when no owner exists.
5. Keep planning/handoff/prototype documents as reference-only when they are not reusable prompts.
6. Produce updated prompt files or new prompt files.
7. Produce an index update candidate for Tab 9 prompt routing.
8. Produce a reconciliation report explaining what changed and why.
9. Package one ZIP with the solved prompt assets.
10. Provide install/extract code and local text-check commands.

## Ownership map

Use this default mapping:

```text
validate-before-freeze / anti-vibe-coding -> KANDA_BUNDLE_GATED_DEVELOPMENT_WORKFLOW
prompt routing / marooned prompt prevention -> KANDA_PROMPT_ROUTER
reference/source/evidence placement -> AGNOSTIC APPLICATION FOLDER STRUCTURE CANON
closed-box ownership -> REASONER BOX ARCHITECTURE CANON
large-module split audit -> REASONER LARGE MODULE REFACTOR PROTOCOL
Tab 1 / Tab 2 detectors -> KANDA_TAB1_TAB2_AUDIT_TAXONOMY_ROADMAP
Tab 4 docstring quality -> KANDA_TAB4_DOCSTRING_QUALITY_ROADMAP
professional/commercial readiness -> KANDA_PRODUCTIZATION_READINESS_ROADMAP
prototype snippets -> REFERENCE_ONLY_NOT_ACTIVE
```

## Forbidden behavior

- Do not convert handoff notes into official governance.
- Do not update active governance unless the user explicitly requests a governance freeze bundle.
- Do not create a new prompt when an existing prompt clearly owns the idea.
- Do not update unrelated prompts just for visibility.
- Do not treat screenshots, prototype snippets, or one-off code examples as active implementation prompts by default.

## Output checklist

A complete reconciliation package includes:

```text
README
source evidence inventory
reconciliation matrix
updated prompt files
new prompt files
reference-only files if useful
index update candidates
post-generation self-check
install/extract commands
```

---

## Professional framework reconciliation update

### Handling professional engineering framework uploads

When the user uploads documents about professional AI-assisted engineering,
missing infrastructure, patch registries, freeze governance, or AI-human
partnership, treat them as reconciliation material.

Decision rules:

1. If the material is an updated final master framework, create or update an
   active reusable prompt.
2. If the material is a review of that framework, preserve it as reference or
   integrate accepted additions into the final framework.
3. If the material lists missing infrastructure modules, convert it into an
   implementation roadmap prompt and route it through the prompt router.
4. If the material is conversational encouragement or opinion, preserve the
   durable engineering principle but do not make the conversation itself active.
5. Do not update official active governance unless the user explicitly requests a
   governance-only freeze package.

Preferred outputs:

```text
professional_ai_assisted_engineering_framework.md
professional_infrastructure_roadmap.md
evidence_freshness_gate.md
patch_registry_validation_freeze.md
```

Every new prompt must answer:

```text
Is it active, optional overlay, roadmap, or reference-only?
Which parent prompt or router knows it exists?
Which Tab 9 group should contain it?
Does it change app source? Usually no.
Does it change official governance? Only after explicit governance task.
```


## Domain-Specific Canon Import Addendum

When importing material from a different project, the prompt update process must ask:

1. Is this a reusable engineering rule or a domain fact?
2. Does it contain source-project-only paths, labels, coordinates, clinical/domain assumptions, or frozen state?
3. Can it be expressed as a project-agnostic KANDA Reasoner prompt?
4. Should it become an active prompt, optional special prompt, route/index candidate, or reference-only record?
5. Which existing prompt should receive the update, if any?

The rule is: import the pattern, not the foreign domain.

<!-- T9T013_KANDA_COMPLETE_LIFECYCLE_START -->

## T9T013 Complete Prompt Asset Lifecycle for Create/Update Prompt Requests

When the user asks to create, update, revise, generalize, reconcile, or register a prompt in this KANDA prompt workspace, treat the task as prompt-library lifecycle work, not as a loose text edit.

Active prompt assets live under:

```text
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/
```

Metadata lives under:

```text
kanda_prompt_workspace/prompt_library/METADATA/
```

Use only the active KANDA prompt workspace path for install, validation, manifest, and handoff instructions. If an unrelated project root appears as the active target, treat it as a regression and stop before implementation.

### Mandatory pre-action checklist

Before creating or updating any prompt asset, the AI must:

1. inspect the relevant existing prompt-library assets first;
2. search for duplicate, older, overlapping, or stronger existing prompts;
3. decide one of `CREATE_NEW_PROMPT`, `UPDATE_EXISTING_PROMPT`, or `LINK_OR_REGISTER_EXISTING_PROMPT`;
4. update the smallest correct owner prompt rather than spreading the same rule everywhere;
5. create or update the `.md` prompt file only in the active prompt library when implementation is approved;
6. create or update the matching metadata record under `prompt_library/METADATA/`;
7. update routing/group/index files only when dashboard or routing visibility is explicitly required;
8. use `bundle_gated_development_workflow` as a required companion when an installable bundle is requested;
9. provide install and validation commands that target `E:\kanda_reasoner` / `kanda_prompt_workspace`;
10. avoid governance, runtime, GUI, source architecture, and unrelated prompt changes unless the user explicitly opens that separate gate.

### Create vs update vs link decision

Use this decision rule:

```text
CREATE_NEW_PROMPT
- No existing active prompt owns the behavior.
- The behavior is reusable, stable, and not merely project-specific conversation.
- A metadata record and routing/visibility plan can be stated.

UPDATE_EXISTING_PROMPT
- An active prompt already owns the behavior.
- The user is improving or clarifying that owner prompt.
- The update can be made without changing unrelated prompts.

LINK_OR_REGISTER_EXISTING_PROMPT
- The prompt already exists, but another index/group/metadata record should know about it.
- Only perform registration if the user explicitly requests dashboard/routing visibility or the current task requires it.
```

### Full bundle output contract

A complete prompt-library implementation bundle must include:

```text
1. changed prompt files or an idempotent installer that edits them;
2. changed metadata files or an idempotent installer that updates them;
3. a bundle manifest listing every intended change;
4. backups or a clear backup location;
5. PowerShell install command;
6. PowerShell validation command;
7. validation that no unrelated project root is used as the active target;
8. validation that no unrelated prompt, GUI, runtime, or governance file was modified.
```

<!-- T9T013_KANDA_COMPLETE_LIFECYCLE_END -->

