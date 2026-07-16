# Project Reasoner v10 - Help Guide

## What this system is for

Project Reasoner is a project-understanding assistant for Python applications.
It is designed to help you and an AI follow the build of an app without losing track of what already exists, what is active, what is legacy, and where a new change should go.

Its practical purpose is to give AI a structured evidence pack about a codebase so the AI can answer questions such as:

- Which module starts the app?
- Which code creates a given tab, window, or feature?
- Where is topomap, timeline, reset, splash, or state logic implemented?
- Which modules are active versus likely legacy?
- What changed, what is risky, and what should be edited next?

The underlying goal is not just code search. It is architectural control.
The system is meant to reduce drift, duplication, misplacement of new code, and confusion caused by large evolving projects.

## The four main folders

### 1. `developer_tools/project_reasoner/project_reasoner_v10`
This is the user-facing reasoning layer.
It is the part that loads collected evidence and helps the AI answer project questions.
It contains the main app, retrieval logic, prompt building, models, and the UI used to inspect project evidence.

Typical responsibilities:
- load static and runtime evidence
- retrieve relevant evidence for a question
- build grounded prompts for AI
- present answers with architectural context
- apply confidence rules when evidence is incomplete or conflicting

### 2. `developer_tools/project_reasoner/reasoner_context_collector`
This is the static collector.
It scans the codebase without running the app and builds a structural index.

Typical responsibilities:
- parse Python files
- collect modules, classes, functions, methods, imports, calls
- build subsystem and role summaries
- infer entry points and likely execution chains
- track state, ownership, duplicates, and architectural hotspots
- export JSON evidence for later AI retrieval

### 3. `developer_tools/project_reasoner/reasoner_runtime_collector`
This is the runtime evidence layer.
It captures what actually happened during a real or scripted app session.

Typical responsibilities:
- runtime trace events
- signal-slot wiring and firing evidence
- state snapshots
- object creation traces
- interaction flow traces
- errors, warnings, and exception context
- performance or timing evidence when implemented

### 4. `developer_tools/project_reasoner/runtime_scenarios`
This folder stores runtime scenario scripts or trace outputs that represent real sessions.
It is the bridge between the running app and the reasoning system.

Typical responsibilities:
- app startup scenarios
- controlled usage sessions
- saved runtime traces
- testable reproductions of important user flows

## Why this is useful with AI

Static indexing alone helps AI understand the code structure, but not full runtime truth.
The uploaded notes make this distinction very clear: the static collector gives a strong architectural map, while runtime traces are needed for actual execution truth, object behavior, and user-driven flows. Combining a static architecture index with a runtime evidence trace is explicitly recommended as the strongest next step. 

The system is meant to turn AI into a grounded implementation companion.
At the strongest cost-benefit level, the target is roughly:

- 97% to 98% structural map
- 92% to 95% functional reasoning
- 85% to 90% runtime-aware understanding

That is described in the notes as the best practical zone for controlling project creation without losing implementation awareness. 

In practice, this means AI becomes much better at:

- tracking what has already been implemented
- finding the correct active files
- separating likely canonical code from noise
- estimating where a new feature belongs
- warning when a change touches risky zones
- avoiding re-implementing something that already exists
- helping continue a project without losing context 

## What evidence the AI should use

Project Reasoner works best when the AI receives two complementary evidence files:

### File 1: Static architecture index
Use this as the source of truth for project structure.
It tells the AI:
- what exists
- where it exists
- which symbols are defined
- which modules import or call others
- which files look responsible for specific features

### File 2: Runtime evidence trace
Use this as the source of truth for observed behavior.
It tells the AI:
- what actually executed
- which objects were created
- which signals connected or fired
- which state changed during a session
- which path really happened in a real run

The notes explicitly recommend this two-file model and say it is much stronger than forcing one file to do everything. If static and runtime evidence disagree, the AI should say so explicitly rather than hide the disagreement. 

## How to use Project Reasoner during the build of another app

### Stage 1: Collect static evidence
Run the data collector against the target project.
This produces the structural JSON index.

Use it early in a project to answer:
- what files and symbols already exist
- where new code should probably go
- whether similar logic already exists somewhere else
- which modules appear to own a feature

### Stage 2: Collect runtime evidence
Run the app through one or more controlled scenarios.
Save the runtime trace.

Use it when you need to answer:
- what path really runs first
- which signal connection is actually effective
- what happened after a click, tab switch, load, reset, or toggle
- why a callback did not fire
- which object instance was involved in a bug

### Stage 3: Ask the AI grounded questions
Give the AI the static index and runtime trace.
Ask concrete questions such as:

- Which module starts the app?
- Which code creates the top tab?
- Show me which code implements topomap.
- Where is timeline wired?
- Which modules participate in reset and cleanup?
- Is this feature already implemented somewhere else?
- Which files should I edit for this new change?
- Which modules look active and which look legacy?

### Stage 4: Use the AI to plan safe edits
Once the AI identifies the likely files and flows, use it to:
- map the blast radius of a change
- find duplicates before adding new code
- identify the best insertion point for new features
- locate ownership and dependency boundaries
- keep new logic aligned with existing architecture

### Stage 5: Re-collect after major changes
After implementing a feature, run the collectors again.
This refreshes the project memory so the next change starts from the new ground truth.

## What kinds of questions it should answer well

The uploaded notes say the system should already be helpful for questions like:

- Which module starts the app?
- Which code creates tabs?
- Where is timeline wired?
- Where is splash created?
- Where is reset logic?
- Which modules are involved in topomap?
- What are the major subsystems?
- Which class owns a given responsibility? 

This is because the collector already provides strong structural evidence such as AST structure, imports, calls, symbols, execution chains, Qt signal hints, state and ownership hints, module summaries, hotspots, warnings, and subsystem buckets. 

## What kinds of questions still need runtime evidence

The same notes also warn that static collection alone is weaker for questions like:

- Which exact path runs first at runtime in all cases?
- Which of two similar modules is truly active?
- Which signal connection is actually effective at runtime?
- Why a GUI callback did not fire?
- What state changed after a specific user action?
- Why an element flashes, disappears, or fails after a real sequence of interactions? 

That is why the runtime collector is not optional if you want strong debugging support.

## Best way to keep app building on the correct track

The strongest practical strategy from the notes is:

1. Do not chase perfect runtime understanding first.
2. First remove ambiguity in what is active, canonical, duplicated, and authoritative.
3. Then add execution-truth layers.
4. Use confidence-aware evidence so the AI distinguishes known facts from inference.  

In practical terms, this means:

- mark active versus deprecated code
- detect duplicate and alias symbols
- keep a feature-to-file registry
- maintain subsystem summaries
- link tests where possible
- add runtime traces for important user flows
- compare static possibility with runtime reality

## High-value upgrades already identified in the notes

The uploaded notes propose several specific improvements that make the system better for long-lived app construction.
These include:

- control-flow analysis per function
- data-flow and dependency graphs
- Qt signal-slot runtime resolution
- runtime call-stack context
- git history metadata
- unit test coverage linkage
- structured docstring and comment summaries
- AI-generated module responsibility summaries
- ADR parsing
- queryable SQLite interface
- object instance tracking
- performance profiling
- user interaction flow logging
- structured exception traces
- confidence-based answering  

These upgrades are not random.
They are aimed at improving three layers:

- structural certainty
- functional reasoning
- runtime truth

## Recommended workflow for a new or evolving project

### Lightweight workflow
Use this when you only need architectural navigation:

1. Run the static collector.
2. Load the JSON into the reasoner.
3. Ask architecture and ownership questions.
4. Use the answer to choose where to edit.

### Strong workflow
Use this when the project is medium or large, or when you want to avoid drift:

1. Run the static collector.
2. Run one or more runtime scenarios.
3. Load both evidence files into the reasoner.
4. Ask the AI grounded questions.
5. Make the change.
6. Re-run collectors.
7. Ask the AI to compare before and after.

### Best workflow for long-lived apps
Use this when you want Project Reasoner to become a durable project memory:

1. Keep the static index current.
2. Keep runtime traces for major workflows.
3. Label active, legacy, backup, experimental, and deprecated modules.
4. Refresh subsystem summaries after major refactors.
5. Store traces for startup, tab switching, timeline actions, reset, splash, load, and feature toggles.
6. Use confidence-aware prompts so AI states when something is inferred rather than proven.

## How to ask the AI good questions

Good questions are specific, architectural, and evidence-seeking.
Examples:

- Which module most likely owns EEG reset logic?
- Show the startup chain from entry point to main window creation.
- Which files are involved in topomap rendering and toggle behavior?
- What user action chain leads from a timeline click to plot redraw?
- Which modules are risky to edit for this feature?
- Is there duplicate responsibility for this behavior?
- Which path looks active and which path looks legacy?
- Which tests appear to cover this module?

Avoid asking only vague questions like "explain the whole app" when the evidence pack is large.
Project Reasoner works best when the question is targeted.

## Limits you should understand

Project Reasoner is powerful, but it does not magically replace a maintainer.
The notes are explicit that static understanding has a ceiling because of:

- dynamic imports
- reflection
- monkey patching
- environment-dependent paths
- user-driven UI sequences
- thread and async timing
- plugin activation
- config-dependent behavior
- dead code versus actually used code
- legacy files that may still be invoked indirectly 

So the right goal is not perfect certainty.
The right goal is strong, grounded, confidence-aware assistance.

## Bottom line

Project Reasoner is best understood as a project brain for AI-assisted software building.
It helps keep app construction aligned with real architecture by combining:

- static structure
- runtime evidence
- retrieval
- confidence-aware reasoning

Used correctly, it helps you build faster without losing track of what already exists, where new code belongs, what is risky, and what actually happened at runtime. The notes explicitly frame its strongest value as helping continue a project without losing context while reducing duplication and architectural drift. 
