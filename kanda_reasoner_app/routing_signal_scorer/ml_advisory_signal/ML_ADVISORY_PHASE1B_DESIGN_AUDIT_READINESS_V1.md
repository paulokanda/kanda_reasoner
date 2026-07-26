# ML Advisory Signal Phase 1b Design Audit Readiness v1

This document records the safe entry criteria for the next phase after the
Phase 1a result-review gate is validated and frozen.

Next feature title:

Routing Signal Scorer ML Advisory-Signal Phase 1b Non-Runtime Design Audit Contract v1

## Purpose

Phase 1b is not runtime ML integration. It is a design audit and readiness
contract for later non-runtime advisory logic. Its job is to decide what
additional interfaces, examples, and tests are needed before any real advisory
adapter can be considered.

## Required limits

Phase 1b must preserve these limits:

- no real ML model execution;
- no provider calls;
- no embeddings or vector store;
- no persistence or report persistence;
- no prompt loading;
- no prompt registry mutation;
- no prompt library direct access;
- no freeze-memory direct access;
- no router-canon direct access;
- no runtime shadow mode;
- no router prompt logic modification;
- no router final selection modification;
- no route authority;
- no MLRT-113.

## Required audit questions

Phase 1b should answer these questions before implementation advances:

1. Which advisory input fields are sufficient for offline advisory tests?
2. Which output flags and reason codes remain safe without rankings or free
   text explanations?
3. How should NullAdvisor and MockAdvisor be compared without changing final
   routes?
4. What route-invariance tests are required before any optional advisory input
   is passed near router intake?
5. Which failure mode should cause advisory abstention rather than action?
6. What evidence is required before future offline real-adapter evaluation?

## Exit condition

Phase 1b may only end by freezing a design audit/readiness contract. It must
not end by enabling runtime ML. Phase 1b must not end by enabling runtime ML.
