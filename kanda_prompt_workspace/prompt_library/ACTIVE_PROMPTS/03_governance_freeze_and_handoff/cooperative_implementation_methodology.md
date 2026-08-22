---
prompt_id: cooperative_implementation_methodology
prompt_code: KPR-03-002
title: Cooperative Implementation Methodology
version: 2.0
status: active
load_type: on_request
owner_box: 03_governance_freeze_and_handoff
source_stage: prompt-audit-wave4a-governance-freeze-handoff-v1
---

# Cooperative Implementation Methodology

## Purpose

Use this prompt when the human and AI must compare consequential implementation
choices before a governed plan is admitted. It owns the collaboration method,
not implementation authorization, architecture rules, delivery commands,
validation claims, snapshot/freeze writes, or handoff generation.

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

## Activate when

- more than one materially different implementation path is credible;
- requirements, tradeoffs, or risk tolerance are not yet explicit;
- external evidence or specialist review may change the decision;
- the human wants a proposal-before-code discussion;
- the partnership method itself needs review.

Do not load for a simple explanation, a trivial edit, a completed plan, or a task
already blocked by a specialist owner.

## Cooperative decision record

```text
COOPERATIVE IMPLEMENTATION DECISION
Requested outcome:
Verified current state:
Material options:
Option A benefits / risks:
Option B benefits / risks:
Unknowns that can change the choice:
Evidence or specialist review required:
Human preference or constraint:
Recommended bounded direction:
Disconfirming condition:
Separate Project implementation authorization still required: YES
May begin coding from this prompt: NO
```

## Method

1. Restate the requested outcome without inventing requirements.
2. Separate verified facts, assumptions, preferences, and unresolved questions.
3. Present only materially different options.
4. Compare ownership, reversibility, validation burden, migration cost, and
   failure impact.
5. Recommend the smallest option that produces measurable improvement.
6. State what evidence would invalidate the recommendation.
7. Ask the human to select or redirect only when the decision genuinely belongs
   to the human.
8. Route the selected direction to the active Project's declared implementation authority and the exact specialist owners.

## Evidence escalation

Use current source and Project evidence first. Request web research, literature,
or external AI review only when current evidence is insufficient and the result
can materially change the decision. External review is evidence, not authority.

## Authority boundary

This prompt may recommend a direction. It cannot:

- authorize source mutation;
- define Box, Tool/Project, MCard, or NO_LEAK behavior;
- substitute for exact-source inspection;
- claim validation or installation success;
- emit a patch as release-ready;
- write snapshot/freeze memory or lesson/error-memory state;
- replace the current handoff owner.

## Completion

The methodology step is complete only when the decision record identifies a
bounded direction, unresolved blockers, and the next canonical owner. Return
`DECISION NOT READY` when material uncertainty remains.
