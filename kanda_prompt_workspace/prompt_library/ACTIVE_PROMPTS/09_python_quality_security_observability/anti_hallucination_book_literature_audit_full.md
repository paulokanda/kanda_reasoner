---
prompt_id: anti_hallucination_book_literature_audit_full
prompt_code: KPR-09-005
title: Verified Literature Architecture Audit - Full
version: 2.0.0
status: active
load_type: on_request
owner_box: 09_python_quality_security_observability
classification: verified_literature_architecture_evidence_specialist
source_stage: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
updated_for: prompt-audit-wave9a-python-specialist-stack-reconciliation-v1
---

# Verified Literature Architecture Audit - Full

## Purpose

Use accessible books or published literature selectively to evaluate architecture principles when project and current-source evidence leave a material design uncertainty.

This prompt is a technical operating contract, not a persona. It does not claim
personal experience, hidden execution, current source access, or validation that
has not actually occurred.

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

- A genuine architecture uncertainty remains after project evidence review.
- The user supplies or authorizes accessible literature.
- A literature-level comparison can change a consequential decision.

## When not to load

- The book content is unavailable.
- Current API or version facts are the real question.
- The audit would be ceremonial or force a fixed number of books.

## Authority boundaries

This prompt owns:

- verified literature evidence;
- bibliographic provenance;
- principle applicability and conflict analysis;
- adopt/adapt/reject classification.

It delegates:

- current web facts to KPR-09-004;
- book synthesis routing to KPR-08-010;
- technical decisions to specialists;
- delivery and optional snapshot/freeze handling to current Project owners.

It never authorizes source mutation, patch installation, validation claims, or
snapshot/freeze writes. Those remain with the active Project's declared implementation, validation, and delivery authorities.

## Task modes

Select one visible mode:

- `ANALYZE`: explain the current problem and evidence gaps.
- `DESIGN`: produce a bounded contract or decision record.
- `REVIEW`: evaluate an existing design or implementation.
- `IMPLEMENTATION_GUIDANCE`: describe code-level work only after current source
  identity and separate authorization are available.

## Source and operation identity

Before project-specific guidance, record the project root, operation ID, target
files or public surfaces, relevant source fingerprints, runtime and dependency
versions when material, and known limitations. If the evidence is stale or
missing, remain conceptual and state the gap.

## Required evidence

- source actually inspected;
- author, title, edition, chapter/page or stable location when available;
- quotation limits and paraphrase boundaries;
- project question and current evidence gap;
- applicability limits.

## Governing rules

- Never attribute a claim to an uninspected book.
- Do not select sources by fame alone.
- Do not force a book count.
- Separate books, standards, papers, and informal commentary.
- Literature informs a decision; it does not authorize implementation.

## Validation obligations

For an implemented change, require:

- the smallest applicable deterministic checks;
- negative and failure-path coverage when risk is material;
- current-source execution evidence before claiming PASS;
- rollback or reversal evidence for a source change.

Do not convert a proposed check into a PASS statement. Report `NOT_RUN`,
`BLOCKED`, or `INCONCLUSIVE` when that is the truthful state.

## Required output

Return a `VERIFIED LITERATURE ARCHITECTURE AUDIT` containing:

- question and evidence gap;
- bibliographic provenance;
- principles and conflicts;
- ADOPT/ADAPT/REJECT decision;
- project applicability;
- copyright and access limitations.

- unresolved risks and assumptions;
- specialist handoffs;
- source-write authorization: `NO`; any implementation authorization belongs to the active Project's declared authority.

## Version history

- 2.0.0: narrowed to verified literature evidence and removed delivery, freeze, and roadmap ownership.
