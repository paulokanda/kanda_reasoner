# Routing Signal Scorer v3 Adviser Foundations Reference

Feature ID: routing_signal_scorer_v3_adviser_foundations_reference_and_box_boundary_design_v1
Schema version: 3.39-adviser-foundations-reference-and-box-boundary-design
Status: design-only foundations reference, no candidate scorer, no runtime behavior change.

## 1. Purpose

This reference defines the first safe implementation boundary for the KANDA/PyArchitect local ML-assisted prompt-router helper.

The immediate goal is Adviser foundations, not Adviser execution.

The long-term maturity path remains:

1. Adviser.
2. Assistant.
3. Copilot / Piloto.

The current milestone only defines the reference and box boundary needed before any local Adviser candidate is created.

## 2. Core doctrine

ML recommends. Canon/router governance decides.

Adviser output is evidence, not authority.

The local Adviser may eventually help the prompt router by producing structured, measurable, advisory-only recommendations about:

- likely governance domain;
- likely route family;
- likely required prompt groups;
- likely specialist prompts;
- missing context;
- risk flags;
- box-boundary concerns;
- freeze, patch, startup, and prompt-library governance concerns;
- ambiguous, abstain, and out-of-scope cases;
- human-confirmation requirements.

The Adviser must not decide final routing.

## 3. What this milestone permits

This milestone permits only:

- a foundations reference document;
- a box-boundary design document;
- manifest markers;
- tests proving no runtime authority was added.

## 4. What this milestone forbids

This milestone forbids:

- candidate scorer implementation;
- machine-learning execution;
- embeddings;
- vector indexes;
- provider calls;
- model calls;
- prompt auto-loading;
- router authority changes;
- runtime router integration;
- startup behavior changes;
- source scanning;
- artifact generation;
- artifact reading;
- artifact writing;
- autonomous freeze writes;
- autonomous decision recording;
- dependency installation;
- network calls;
- database access;
- writes outside future approved scratch/report paths;
- imports from runtime router modules;
- exports from routing_signal_scorer public contract.

## 5. Teacher is not ground truth

The teacher may be the current strong AI/canonical router reasoning, but it is not absolute ground truth.

Teacher answers must remain draft evidence until they are reviewed, versioned, validated, and frozen into a gold set.

A future Teacher-Student harness must not promote teacher answers into gold automatically.

The required path is:

1. Teacher answer.
2. Draft answer.
3. Human-reviewed answer.
4. Frozen gold answer.
5. Versioned and checksummed gold record.

## 6. ABSTAIN, AMBIGUOUS, and OUT_OF_SCOPE

Future Adviser schemas must support safe non-decision outputs.

ABSTAIN means the candidate does not have enough signal.

AMBIGUOUS means the request could belong to more than one route or depends on missing context.

OUT_OF_SCOPE means the request is outside Adviser routing competence.

Safety rule:

ABSTAIN, AMBIGUOUS, OUT_OF_SCOPE, and UNKNOWN must never permit action.

The deterministic router must treat them as not proceed.

## 7. Output guard requirement

A future Adviser output guard is mandatory before any candidate scorer is trusted for evaluation.

The output guard must hard-fail if:

- authority_statement is not advisory_only;
- a governed request receives an unsafe proceed recommendation;
- freeze bypass is not flagged;
- startup bypass is not flagged;
- prompt-library anti-audit bypass is not flagged;
- box invasion is not flagged;
- authority-promotion attempt is not flagged;
- output tries to load prompts;
- output tries to write memory;
- output claims final routing authority;
- output contains unexpected executable or action fields.

## 8. Severity as code

Disagreement severity must be implemented as code, not prose.

Critical severity includes:

- unsafe proceed on governed work;
- bypass accepted;
- freeze confirmation bypass;
- startup-delivery bypass;
- prompt-library anti-audit bypass;
- box invasion;
- router-authority promotion;
- prompt auto-loading;
- autonomous memory write;
- artifact generation or artifact I/O in a forbidden phase.

## 9. Gold set and review rules

Future gold sets must be:

- reviewed;
- versioned;
- append-only;
- checksummed;
- tied to teacher version;
- tied to schema version;
- tied to input hash;
- tied to review provenance;
- never automatically updated by candidate logic.

Candidate outputs must live only in scratch/report space and must never be treated as source-of-truth.

## 10. Resource limit rule

Even standard-library-only offline code must have limits before candidate implementation.

Future candidate code must define limits for:

- maximum input characters;
- maximum cases per run;
- maximum runtime per case;
- maximum report size;
- maximum flags per category;
- no threads;
- no network;
- no database;
- no environment mutation;
- scratch-only writes.

## 11. Implementation order

The safe patch order is:

1. Adviser Foundations Reference and Box Boundary Design.
2. Adviser System Card, Bug Bar, Threat Model, and Pattern Library.
3. Adviser Schema Family.
4. Adviser Contract Validator and Output Guard.
5. Adviser Severity Evaluator and Resource Limits.
6. Adviser Pure Comparison Harness.
7. Adviser Gold Manifest and Run Registry.
8. Adviser Seed Case Corpus.
9. Adviser Draft Teacher Answers and Review Records.
10. Adviser Seed Gold Set.
11. Adviser Candidate v0 Lexical Scorer Design.
12. Adviser Candidate v0 Offline Lexical Scorer.
13. Adviser Candidate v0 Evaluation Runner.
14. Adviser Active Review Queue.
15. Adviser Candidate Registry.
16. Adviser Gold Set Expansion Plan.
17. Adviser Promotion Criteria Gate.

Do not skip directly to candidate implementation.

## 12. Success definition for this milestone

This milestone succeeds if the project contains a clear Adviser foundations reference and a clear Adviser box boundary while adding no runtime authority, no candidate scorer, no prompt loading, no artifact I/O, no embeddings, no providers, no startup behavior, and no public runtime export.
