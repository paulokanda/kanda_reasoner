# Routing Signal Scorer v3 Generator Candidate Human Decision Gate Design v1

This document defines a **design only** and **schema only** human decision gate after the generator-candidate preparation closure shield inside `kanda_reasoner_app/routing_signal_scorer`.

Feature ID: `routing_signal_scorer_v3_generator_candidate_human_decision_gate_design_v1`

Schema version: `3.29-generator-candidate-human-decision-gate-design`

## Purpose

This milestone makes one boundary explicit: after the preparation chain is closed, a real human decision is still required before any future candidate patch phase.

It does not record a human decision. It does not infer approval from prior schemas, validation, freeze output, or preparation closure. It does not create or authorize a generator candidate patch. It does not authorize generation, dependencies, side effects, artifact IO, source scanning, raw text materialization, embeddings, vectors, providers, runtime scoring, router authority, public runtime export, prompt loading, or freeze-memory writing.

## Current state

`human_decision_not_recorded`

The current effect is:

`no_effect_schema_only_human_decision_not_recorded`

## Required future human decision inputs

A future governed decision-record patch would need, at minimum:

- explicit human decision text
- decision actor or source
- decision timestamp or session reference
- decision scope
- referenced preparation closure freeze ID
- referenced review bundle freeze ID
- touched paths allowed for any future candidate patch
- acknowledgement of candidate patch non-goals
- acknowledgement of artifact IO, source scanning, runtime, and router non-goals
- rollback or stop-condition acknowledgement

## Non-goals

This gate is not approval. It is a schema-only missing-decision checkpoint.

A future real decision record must be another separately governed patch before any candidate patch can be proposed or implemented.

## Stop conditions

Stop if the request asks this milestone to record approval, infer approval, create a candidate patch, authorize a generator, install dependencies, authorize side effects, write/read artifacts, scan sources, materialize raw text, create embeddings or vectors, run providers, enable runtime/router behavior, write freeze memory, or touch another box.
