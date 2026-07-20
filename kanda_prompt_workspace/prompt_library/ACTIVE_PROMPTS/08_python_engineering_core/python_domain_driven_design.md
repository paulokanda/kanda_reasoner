---
prompt_id: python_domain_driven_design
prompt_code: KPR-08-004
title: Python Domain-Driven Design
version: 2.0.0
status: active
load_type: on_request
owner_box: 08_python_engineering_core
classification: strategic_tactical_domain_modeling_specialist
source_stage: prompt-audit-wave8b-python-architecture-design-boundaries-v1
historical_aliases:
  - A023
---

# Python Domain-Driven Design

## Purpose

Use this prompt when domain language, business invariants, subdomain boundaries,
or Bounded Contexts materially drive the design.

The governing objective is to model the domain accurately enough that important
rules and language remain explicit, while avoiding DDD ceremony for simple CRUD,
small utilities, or low-complexity workflows.

## Ownership boundary

This prompt owns:

- DDD applicability;
- Ubiquitous Language and domain terminology;
- subdomain and core-domain analysis;
- Bounded Contexts and Context Maps;
- entities, value objects, aggregates, domain services, domain events, and
  Anti-Corruption Layer semantics;
- domain invariants and consistency-boundary reasoning.

This prompt does not own:

- generic dependency direction, ports, framework isolation, or composition-root
  design; use KPR-08-001;
- KANDA box paths or shielding; use the current Box Architecture owner;
- Repository, Unit of Work, transaction, session, persistence, or application
  service implementation; use the current enterprise/application owner;
- API, messaging, async/distributed delivery, testing, source mutation, package,
  validation evidence, Error Memory, or freeze authority.

## Applicability gate

Classify the request:

- `SIMPLE_DOMAIN` — direct data and service logic is sufficient;
- `DOMAIN_MODEL` — meaningful invariants justify explicit domain objects;
- `MULTIPLE_CONTEXTS` — language or model meaning changes across bounded areas;
- `STRATEGIC_DDD` — subdomain investment and context relationships drive
  architecture or organizational ownership;
- `INSUFFICIENT_EVIDENCE` — ask for the minimum missing domain context.

Do not use arbitrary counts of rules, entities, tables, or modules as the gate.
Consider language ambiguity, invariant complexity, rate of business change,
integration boundaries, ownership, and cost of model mistakes.

## Existing-domain evidence

Collect domain terms, decisions, invariants, examples, exceptions, workflows,
external systems, regulatory constraints, and disagreements among stakeholders.
Distinguish user-provided facts from inference. Do not invent terminology,
policies, event semantics, or business rules.

## Ubiquitous Language

Create or refine a glossary only from current evidence. Each important term
should have one meaning inside one Bounded Context. Record synonyms, overloaded
terms, prohibited ambiguous terms, and unresolved questions.

Code, tests, documentation, UI language, and discussions should converge on the
context-appropriate terminology when implementation is separately authorized.

## Subdomains and core domain

Identify core, supporting, and generic capabilities only when this distinction
changes investment or ownership. Do not label every module a subdomain or force
an organizational structure from a conceptual model.

## Bounded Contexts and Context Maps

A Bounded Context defines where a model and language are internally consistent.
Do not equate a context automatically with a package, service, database, team,
or KANDA box.

For each relationship, record the actual dependency, translation, ownership,
and change risk. Use Context Map patterns only when they clarify a real
relationship; do not label integrations ceremonially.

## Tactical-pattern selection

Use tactical patterns only when they protect demonstrated domain meaning or
invariants:

- Entity: continuity defined by a stable identity contract;
- Value Object: identity-free value semantics and validity rules;
- Aggregate: a transactional consistency boundary with one entry point for its
  protected invariants;
- Domain Service: domain behavior that does not belong naturally to one entity
  or value object;
- Domain Event: a domain-significant fact that has occurred;
- Repository port: a domain-facing collection-like capability when aggregate
  retrieval or persistence independence is justified;
- Specification or Policy: an explicit business rule when named composition
  improves the model.

Do not require every tactical pattern.

## Entity identity contract

Define identity source, scope, stability, equality, hashing, and lifecycle.
Unsaved or provisional entities require explicit semantics; do not compare all
instances with missing identifiers as equal. Avoid dataclass-generated equality
when it conflicts with the intended identity model.

## Value Object semantics

A value object is defined by its values and invariants, not by absence of a
database key alone. Prefer immutability when it supports valid value semantics,
but follow project constraints and avoid pretending nested mutable state is
immutable.

## Aggregate and consistency boundaries

An aggregate protects invariants that must be consistent together. Keep the
boundary as small as the invariant permits. References across aggregates should
respect independent lifecycle and consistency; do not navigate and mutate an
entire object graph implicitly.

Cross-aggregate workflows may require application coordination, eventual
consistency, or process management. Dispatch transaction and delivery mechanics
to their current owners.

## Domain services and application policy

A domain service expresses domain logic that does not fit naturally on one
entity or value object. It may use domain concepts and need not be stateless by
universal rule, though hidden mutable state should be justified.

Application services coordinate use cases, authorization, transactions,
external calls, and domain objects. They may contain application policy while
keeping core domain invariants in the domain model.

## Domain events and integration events

A domain event records a meaningful fact inside a domain model. An integration
event is an external contract for another context or system. They may differ in
schema, timing, reliability, privacy, and compatibility.

Do not claim that publishing after commit guarantees delivery. Reliable
cross-boundary delivery requires the current transaction, persistence,
messaging, and async/distributed owners to define atomicity, outbox/inbox,
idempotency, retries, ordering, and failure handling where applicable.

## Repository and persistence boundary

Repositories are optional. Use a domain-facing repository port when aggregate
retrieval and persistence separation justify it. Do not create a generic CRUD
repository for every table or require one repository per entity.

Repository placement and Unit of Work implementation depend on the selected
application architecture and current enterprise owner.

## Anti-Corruption Layer

Use an Anti-Corruption Layer when an external or neighboring model would distort
important local domain meaning. Define translation direction, ownership,
versioning, failure behavior, and information loss. A simple adapter or mapping
function may be sufficient.

## Output profile

Return the smallest useful domain-design artifact, such as:

- applicability classification;
- evidence-grounded glossary;
- subdomain or Bounded Context proposal;
- Context Map relationship;
- invariant and aggregate record;
- entity/value-object identity contract;
- domain-versus-integration event distinction;
- simpler alternative and owner dispatch.

Do not always generate a complete domain model or runnable implementation.

## Non-authorization statement

This prompt may analyze and model domain concepts. It does not authorize source
changes, architecture-path changes, persistence or messaging implementation,
validation claims, package delivery, Error Memory insertion, or freeze.
