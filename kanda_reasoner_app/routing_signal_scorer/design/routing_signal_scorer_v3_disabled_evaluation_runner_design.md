# Routing Signal Scorer v3 Disabled Evaluation Runner Design v1

Feature ID: `routing_signal_scorer_v3_disabled_evaluation_runner_design_v1`

## Purpose

This design freezes the disabled-by-default contract for any future offline evaluation runner. The semantic layer remains an untrusted evidence witness. It may provide evidence. It may never provide authority.

This phase is deliberately **design/contract only**. It does not implement an evaluation runner, execute evaluation, generate embeddings, create vector indexes, tune thresholds, enable semantic runtime behavior, call providers, mutate prompt routing, or write freeze memory.

## Scope

This patch belongs only to `kanda_reasoner_app/routing_signal_scorer`.

It adds:

- a standard-library-only disabled runner contract module;
- a design document;
- manifest registration;
- permanent regression tests.

It does not touch `contract.py`, `__init__.py`, prompt-router files, startup delivery, freeze boxes, provider code, vector indexes, corpus generators, or runtime scorer behavior.

## Master rule

A future evaluation runner may only produce review evidence. It may never enable semantic runtime behavior, change thresholds, promote candidates, load prompts, produce a final route, produce required prompts, produce May-proceed signals, write freeze memory, mutate the prompt router, or become startup/runtime/background automation.

## Disabled-by-default status

The runner design requires all of the following to remain false in this phase:

- evaluation execution;
- semantic runtime enablement;
- threshold auto-tuning;
- embedding generation;
- vector index generation;
- corpus generation;
- external API calls;
- startup execution;
- runtime execution;
- background execution;
- file-watcher execution;
- freeze-memory writes;
- prompt-router mutation;
- prompt auto-loading;
- May-proceed generation.

## Required preconditions before any future runner

A future runner implementation requires a separate governed patch after all relevant design/schema artifacts are frozen. Before any implementation, the following must be true:

- frozen gold-set artifact exists;
- frozen Metadata Vector Manifest artifact exists;
- offline corpus governance is frozen;
- human review is complete;
- explicit manual invocation is required;
- metrics are declared before the run;
- thresholds are declared before the run;
- lexical fallback remains primary;
- semantic evidence remains advisory-only;
- runtime enablement is not allowed from runner results.

## Required future inputs

A future manual runner may not read raw prompt files, freeze entries, chat logs, or project-private text directly. It must operate on frozen, schema-validated artifacts only:

- frozen gold-set schema-validated artifact;
- frozen Metadata Vector Manifest schema-validated artifact;
- predeclared metric and threshold contract;
- human-approved evaluation plan;
- dependency review if a future optional provider exists.

## Forbidden actions

The disabled runner design explicitly forbids:

- run evaluation now;
- run at startup;
- run at runtime;
- run in background;
- run from file watcher;
- rebuild corpus;
- generate embeddings;
- create vector index;
- call external embedding API;
- persist user queries;
- auto-adjust thresholds after results;
- enable semantic runtime;
- promote semantic candidates;
- modify prompt router;
- auto-load prompts;
- write freeze memory;
- produce final route;
- produce required prompts;
- produce May-proceed signals.

## Permitted future outputs

Even in a later implementation, output must be limited to review evidence only:

- metrics report draft only;
- candidate failure report only;
- disagreement report only;
- human review queue only;
- no runtime enablement;
- no threshold changes;
- no prompt loading;
- no May-proceed signal;
- no final route signal.

## Review gates

The future runner boundary requires these gates:

- manual invocation gate;
- gold-set freeze gate;
- manifest freeze gate;
- privacy gate;
- authority leakage gate;
- stale candidate gate;
- threshold-change separate patch gate;
- runtime-enablement separate patch gate;
- dependency-adoption separate patch gate;
- freeze required before any runner implementation.

## No-authority assertions

Runner results are evidence only. Runner results cannot change router decisions, required prompts, May-proceed decisions, semantic runtime state, thresholds, freeze memory, startup delivery, or prompt-router canon.

## Forbidden fields

The disabled runner contract rejects authority fields such as `final_route`, `required_prompts`, `may_proceed_now`, `route_override`, `auto_load_prompts`, `write_freeze_memory`, `modify_prompt_router`, `enable_semantic_runtime`, and `adjust_thresholds`.

It also rejects raw/private text fields such as `raw_user_query`, `user_query_text`, `chat_history`, `private_project_text`, `freeze_entry_text`, `prompt_file_text`, `prompt_body_text`, and `terminal_log_text`.

It also rejects vector/provider fields such as `embedding`, `embeddings`, `vector`, `vectors`, `vector_index`, `provider`, `provider_name`, `external_api_key`, `model_name`, and `model_path`.

## Validation expectation

Permanent tests must prove that:

- the contract is standard-library-only;
- every execution/runtime/provider flag is disabled;
- activation requests never authorize execution;
- forbidden authority, raw-text, vector, and provider fields are rejected;
- manifest registration preserves the frozen v3 chain;
- previous v3 schema/design tests still pass with the new manifest version;
- no runner, embeddings, vector values, vector indexes, provider implementation, runtime behavior, threshold tuning, startup execution, background execution, or cross-box mutation is introduced.

## Final canon

This design does not authorize evaluation execution. This design does not authorize semantic runtime enablement. This design does not authorize threshold changes. This design does not authorize embeddings, vectors, providers, vector indexes, corpus generators, prompt-router changes, or freeze-memory writes.
