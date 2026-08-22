---
prompt_id: python_clean_architecture
prompt_code: KPR-08-001
title: Python Clean Architecture
version: 2.0.0
status: active
load_type: on_request
owner_box: 08_python_engineering_core
classification: python_dependency_direction_specialist
source_stage: prompt-audit-wave8b-python-architecture-design-boundaries-v1
---

# Python Clean Architecture

## Purpose

Use this prompt when a Python system needs explicit dependency direction,
framework isolation, ports and adapters, or a composition boundary.

The governing objective is to keep stable policy and domain behavior from
depending directly on volatile frameworks, persistence details, user-interface
mechanisms, or external services. This is an applicability and boundary-design
specialist, not a requirement to reproduce one named architecture diagram.

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

## Ownership boundary

This prompt owns:

- deciding whether dependency inversion is justified by current evidence;
- distinguishing stable policy from volatile implementation detail;
- defining ports, adapters, boundary data, and composition-root responsibility;
- identifying framework and infrastructure leakage into policy code;
- proposing incremental migration toward clearer dependency direction.

This prompt does not own:

- host-specific box paths, shielding implementation, public/private path ownership, or cross-box touch
  authorization; use the current Box Architecture owner;
- Ubiquitous Language, Bounded Contexts, aggregates, or tactical DDD;
- Repository, Unit of Work, service-layer, transaction, or session-state
  implementation; use the current enterprise/application-pattern owner;
- detailed testing, type-safety, security, resilience, package, terminal,
  validation-evidence, lesson/error memory, or snapshot/freeze mechanics;
- source mutation or implementation authorization.

## Applicability gate

Before recommending architectural separation, inspect current evidence and
classify the situation:

- `NOT_NEEDED` — a direct module, function, or small script is sufficient;
- `LOCAL_BOUNDARY` — one seam around a volatile dependency is sufficient;
- `PORTS_AND_ADAPTERS` — multiple interchangeable or volatile details justify
  an explicit inward-facing contract;
- `SYSTEM_ARCHITECTURE` — policy spans several entry points or infrastructure
  mechanisms and requires a composition boundary;
- `INSUFFICIENT_EVIDENCE` — ask for the minimum missing architecture context.

Do not infer architecture scale from file count alone. Consider change rate,
policy stability, dependency volatility, testability, deployment constraints,
team ownership, and current coupling.

## Evidence-first review

Record:

1. current entry points and externally visible contracts;
2. policy or domain behavior that must remain stable;
3. frameworks, storage, UI, devices, networks, clocks, queues, and other details;
4. current dependency direction;
5. concrete pain caused by the current coupling;
6. simpler alternatives already available;
7. migration and rollback constraints.

Separate observed facts from architectural inference. Do not invent missing
modules, interfaces, requirements, or framework behavior.

## Policy and detail classification

Treat a dependency as a detail when the business or application policy should
remain meaningful if that mechanism changes. Examples may include a database
library, web framework, GUI toolkit, filesystem, network client, or scheduler.

This classification is contextual. A framework-specific application may
legitimately keep framework concepts near its core when replacement is not a
real requirement and the abstraction would add cost without reducing risk.

## Ports and adapters

Introduce a port only when it expresses a stable need of the policy side. Keep
ports small, capability-oriented, and free of adapter-specific types where
practical. Do not create one interface per concrete class or mirror every
framework API behind a nominal abstraction.

Adapters translate between the external mechanism and the port. Boundary
translation must make ownership of validation, serialization, errors, identity,
time, and transaction scope explicit.

## Boundary data contracts

Choose boundary data according to the contract:

- domain objects when the boundary is inside one trusted domain model;
- immutable records or simple data structures for application boundaries;
- explicit DTOs or schemas for external or versioned contracts;
- framework types only when the dependency is deliberately accepted.

Do not require one representation universally. Prevent external mutable state
or framework lifecycle from leaking silently into stable policy.

## Composition root

Keep object graph construction and concrete adapter selection at an explicit
composition boundary appropriate to the application. This may be a function,
module, framework hook, command entry point, or dependency-injection container.

Dependency injection is a technique, not a mandatory framework. Prefer direct
construction and explicit parameters when sufficient. Do not require one class
and one public method per use case.

## Existing-system migration

For an existing system:

1. preserve public behavior and current owner boundaries;
2. identify one demonstrated dependency-direction problem;
3. create the smallest stable seam;
4. move translation or infrastructure logic behind that seam;
5. validate the touched behavior using the current test and evidence owners;
6. repeat only when another demonstrated problem remains.

Do not perform a ceremonial four-layer rewrite. Do not rename folders or move
files solely to resemble a reference architecture.

## Output profile

Return only the sections needed for the request. A useful review may include:

- applicability classification;
- current dependency map;
- policy/detail findings;
- proposed ports or simpler alternative;
- composition boundary;
- incremental migration steps;
- owner dispatch and unresolved evidence.

## Non-authorization statement

This prompt may analyze and recommend dependency boundaries. It does not
authorize source changes, cross-box edits, implementation, validation claims,
package delivery, lesson/error-memory insertion, or snapshot/freeze writes.
