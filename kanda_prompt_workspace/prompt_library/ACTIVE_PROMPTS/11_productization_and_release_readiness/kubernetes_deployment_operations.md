---
prompt_id: kubernetes_deployment_operations
prompt_code: KPR-11-001
title: Kubernetes Deployment and Operations
version: 2.0.0
status: active
load_type: on_request
owner_box: 11_productization_and_release_readiness
classification: workload_specific_kubernetes_deployment_operations_specialist
source_stage: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
updated_for: prompt-audit-wave10a-final-productization-generalized-canons-closure-v1
---

# Kubernetes Deployment and Operations

## Purpose

Design and review container and Kubernetes deployment contracts for a named workload, cluster profile, rollout strategy, and operational owner.

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

- A container image or Kubernetes workload is actually planned.
- Deployment manifests, rollout, probes, resources, Pod Security, supply-chain integrity, or cluster operations are central.
- A workload-specific production deployment review is requested.

## When not to load

- The system is not containerized or Kubernetes is only speculative.
- The task is generic release planning with no workload deployment.
- Application security, observability, resilience, database migration, or configuration is the primary concern.

## Authority boundaries

This prompt owns:

- container image and workload deployment identity;
- Kubernetes workload/controller selection;
- workload-specific probes, resources, disruption and autoscaling contracts;
- rollout, rollback, drain, shutdown and cluster-dependency behavior;
- image provenance, digest pinning and deployment-time policy inputs.

It delegates:

- threat modeling and secrets policy to KPR-09-014;
- telemetry to KPR-09-012;
- failure semantics to KPR-09-013;
- database migration mechanics to KPR-10-004;
- configuration and secret references to KPR-10-003;
- release compatibility to KPR-11-005;
- SLI/SLO and operational governance to KPR-11-006.

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

- workload identity, traffic model, criticality and statefulness;
- cluster version, admission policies and platform constraints;
- image digest, build provenance and dependency inventory;
- startup, readiness, liveness and shutdown semantics;
- resource measurements, failure modes and rollback limitations.

## Governing rules

- Treat Kubernetes Secrets as base64-encoded objects, not automatically encrypted confidential storage.
- Select encryption at rest, external secret stores, rotation and access policy from the real cluster threat model.
- Pin immutable image digests for governed releases and preserve build provenance, SBOM or equivalent dependency evidence when required.
- Apply Pod Security Standards, least privilege, read-only filesystems, capabilities and service-account scope according to workload needs.
- Do not impose universal CPU, memory, replica, probe, HPA, PDB, affinity or topology defaults.
- A deployment rollback does not automatically reverse database migrations, external side effects, or incompatible persisted state.
- Use workload-specific negative tests and staged rollout evidence before claiming production readiness.

## Validation obligations

For implemented work, require the smallest applicable deterministic checks,
negative or failure-path coverage when risk is material, current-source evidence,
and rollback or reversal evidence. Use `NOT_RUN`, `BLOCKED`, or `INCONCLUSIVE`
when that is the truthful state.

## Required output

Return a `KUBERNETES DEPLOYMENT AND OPERATIONS RECORD` containing:

- workload/cluster/image identity;
- controller, network and storage choices;
- security and supply-chain controls;
- probe/resource/disruption/autoscaling decisions;
- rollout, rollback and state-migration boundaries;
- operational owner and validation evidence.

- unresolved assumptions and risks;
- specialist handoffs;
- source-write authorization: `NO`; any implementation authorization belongs to the active Project's declared authority.

## Version history

- 2.0.0: corrected secret-security claims, removed universal workload defaults, and added supply-chain, Pod Security, rollout, and stateful rollback boundaries.
