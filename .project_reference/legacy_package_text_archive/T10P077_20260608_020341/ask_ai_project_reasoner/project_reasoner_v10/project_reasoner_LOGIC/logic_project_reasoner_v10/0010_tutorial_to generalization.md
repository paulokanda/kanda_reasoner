# AI NEXT SESSION TUTORIAL
## Goal: Generalize Project Reasoner so it can work with any project, not only eeg_kernel_ai_neural_data_analysis

This tutorial is the canonical handoff for the next AI session.

Read it first.
Do not start changing code before understanding the rules and current locked state.

---

# 1. Main objective for next session

We are now moving from:

- a Project Reasoner that works well for `eeg_kernel_ai_neural_data_analysis`

to:

- a Project Reasoner that can be used with **any selected project**

while preserving:
- current working EEG behavior
- current grounding improvements
- current collector isolation rules
- current runtime contamination protections

The new session should focus on **generalizing the app safely**, not rewriting everything.

The main target is:

- `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_retriever.py`

But this must be done carefully and step by step.

---

# 2. What is already fixed and MUST NOT be undone

## 2.1 External project JSON must not contain internal reasoner runtime contamination

This is already fixed at the producer level.

For an external selected project like:

- `E:\eeg_kernel_ai_neural_data_analysis`

the generated main JSON must NOT contain:
- `developer_tools/kanda_reasoner_app/...`
- `runtime_runner.py`
- internal runtime metadata from the reasoner tool

This was fixed in:
- `collector_main.py`

Behavior now:
- external selected project root -> internal runtime metadata excluded
- internal `kanda_reasoner_app` root -> internal runtime metadata allowed

This is protected by regression tests.

Do not undo this.

---

## 2.2 `runtime_runner.py` is internal only

`runtime_runner.py` may be used:
- during collection
- to enrich JSON internally when collecting the reasoner tool itself

It must NOT:
- appear as answer evidence for EEG project questions
- be treated as a project file for external project reasoning
- influence external project reasoning in `v10_main_window.py`

This is canonical.

---

## 2.3 The canonical project file for use is the main JSON

Examples:
- `project_reasoner_v1_widget_text.json`

This is the canonical file for AI use.

It may be used:
- as one full JSON
- or split and reassembled later

The `_runtime_trace.json` file is only a helper/support file.
It is not the main canonical index.

---

## 2.4 `developer_tools` path layout does NOT need to be moved right now

We discussed moving:

- `E:\eeg_kernel_ai_neural_data_analysis\developer_tools`

to something like:
- `E:\developer_tools`

Conclusion:
- not needed now

Reason:
- the contamination problem was fixed correctly at the collector output level
- moving folders now would create unnecessary path/import churn
- regression tests are a better protection than path relocation

Do not start next session by moving folders.

---

## 2.5 Current AI grounding behavior improved and must be preserved

We improved:
- routing for code-evidence questions
- validator over-rejection for generative code-localized questions
- retrieval of call-site files
- retrieval of builder definitions
- retrieval for timeline/reset/top-navigation question families

Current behavior is healthier:
- fewer hallucinations
- more honest `INSUFFICIENT_EVIDENCE`
- better grounded answers

Do not undo those improvements while generalizing.

---

# 3. Current problem to solve next

The app still has many heuristics in `v10_retriever.py` that are too specific to the EEG project.

Examples of project-specific terms already observed:
- `NotebookBuilder`
- `NavBarBuilder`
- `build_top`
- `build_upper`
- `addtab`
- `attach_timeline_to_tab`
- `eeg_traces_tab`
- topomap/amplitude map terms
- timeline/reset/cleanup owner-path boosts tied to EEG project file names

This means:
- current behavior is strong for the EEG project
- but portability to arbitrary projects is weak

So the next session goal is:

## make the retriever generic without breaking the current EEG behavior

---

# 4. Correct architecture target

The retriever should become a 3-layer system:

## Layer 1 - Generic core retriever
Portable to any project.

This layer should keep only generic signals such as:
- exact path match
- exact filename match
- exact class match
- exact function match
- exact symbol match
- import/reference matching
- call-site matching
- entry-file boosts
- explain-chain boosts
- builder/launcher/main-window orchestration style boosts
- runtime-safe generic reasoning helpers
- collector-derived structural signals

## Layer 2 - Collector-derived project structure
Project-agnostic, but informed by the selected project’s JSON.

Examples:
- `entry_files`
- `execution_chains`
- `qt_signal_map`
- ownership/responsibility info
- file summaries
- boundaries
- semantic roles
- runtime-safe project summaries when allowed

This layer is already strong and should remain a major source of intelligence.

## Layer 3 - Optional project profile
Project-specific heuristic boosts, separated from the core.

Examples for EEG profile:
- notebook/tab aliases
- navbar aliases
- timeline aliases
- topomap aliases
- reset/cleanup aliases
- special owner-path boosts for EEG project structure

This layer should be optional.

If a profile is absent:
- app still works with generic logic

If a profile is present:
- project-specific answers improve

---

# 5. What NOT to do

Do NOT do these things next session:

## 5.1 Do not delete all EEG-specific boosts at once
That would probably damage current working behavior.

## 5.2 Do not put more project-specific terms directly into the generic retriever core
The whole point is to reduce hardcoded EEG assumptions.

## 5.3 Do not reintroduce `developer_tools` references into external project JSON
That bug is fixed and must stay fixed.

## 5.4 Do not start from `v10_main_window.py`
The main generalization target is the retrieval architecture, not the window shell.

## 5.5 Do not weaken validators broadly
Validator changes should stay narrow and evidence-aware.

---

# 6. First concrete implementation goal next session

## Step 1 - Inventory the EEG-specific heuristics inside `v10_retriever.py`

Before refactoring anything, identify and label the heuristics that are clearly project-specific.

Create a categorized list of:
- generic heuristics
- collector-derived structural heuristics
- EEG-specific heuristics

Examples that likely belong to EEG-specific:
- `NotebookBuilder`
- `NavBarBuilder`
- `build_top`
- `build_upper`
- `attach_timeline_to_tab`
- `eeg_traces_tab`
- topomap-specific owner path terms
- timeline owner path terms
- reset/cleanup owner path terms tied to current project naming

Do this carefully.
This inventory step is important.

---

# 7. The recommended safe refactor path

## Step 2 - Introduce a project profile concept without changing behavior yet

Create a new concept such as:

- `project_profile`
- `retrieval_profile`
- `domain_profile`

Example shape:

```python
project_profile = {
    "domain_name": "...",
    "path_priority_terms": [...],
    "symbol_priority_terms": [...],
    "chain_aliases": {...},
    "owner_path_boosts": {...},
    "special_question_patterns": {...},
}

At this step:

do not move logic yet
just introduce the structure

The app should continue behaving exactly as before.

Step 3 - Move EEG-specific heuristics out of the retriever core into the profile

After the profile structure exists, gradually move the most obvious EEG-specific boosts into the profile.

Move only a few at a time.
Test after each group.

Suggested order:

builder-specific terms
timeline-specific terms
topomap-specific terms
reset/cleanup-specific terms
special owner-path boosts tied to current EEG folder/module names

Keep the generic retriever intact.

Step 4 - Keep generic logic in the core retriever

The generic core should still handle:

exact reference queries
call-site questions
where-is / who-calls / where-in-code
explanation / chain / flow questions
snippet-aware code-evidence routing
entry-file / orchestration logic
collector-derived execution chain usage

This is the portable part and should not depend on EEG naming.

Step 5 - Decide how the profile is selected

The profile should be selected from the loaded project JSON or project root context.

Possible strategies:

infer from project root path
infer from project summary/domain tags
infer from known entry files
infer from known subsystem names
or explicitly no profile if nothing matches

Default behavior must be:

No profile found -> generic retriever only

This is important for portability.

8. Testing strategy for next session
8.1 Keep current EEG behavior working

After each refactor step, retest these kinds of questions on the EEG project:

startup chain
superior/top navigation tab construction
topomap implementation
timeline chain
timeline attachment invocation
reset/cleanup chain

If these degrade badly, the refactor was too aggressive.

8.2 Add tests for generic behavior

After profile separation begins, add tests that prove:

the generic retriever still works without EEG-specific profile
profile-specific boosts are not required for basic reasoning
project-specific profile boosts can be turned on/off without breaking the core
8.3 Keep contamination tests passing

All previously added tests protecting external-project JSON isolation must continue passing.

Especially:

external selected project root excludes internal runtime metadata
internal reasoner-tool root can still include internal runtime metadata

Do not regress those tests.

9. Current known good results from this session

These are important because they define the baseline to preserve.

Good now:
top navigation / superior tab question works much better
reset / cleanup chain works much better
timeline chain is safer and more honest
attach_timeline_to_tab caller assumption is no longer hallucinated
internal runtime contamination from developer_tools is removed from external project JSON
regression tests are in place for that producer-side isolation
Still conceptually unfinished:
full generalization of retriever
separation of EEG-specific ranking logic into optional profile layer

That is the next session’s real mission.

10. How the next AI should work step by step

When the next session begins, the AI should follow this order:

Phase A - Read and understand
Read this tutorial fully
Do not patch anything yet
Inspect v10_retriever.py
Identify which logic is:
generic
project-structural
EEG-specific
Phase B - Plan the profile extraction
Propose a minimal project_profile structure
Keep behavior unchanged initially
Confirm insertion points before moving code
Phase C - Migrate gradually
Move one small group of EEG-specific heuristics into the profile
Compile
Test EEG questions
Repeat for the next small group
Phase D - Protect with tests
Add tests for generic-without-profile behavior
Add tests for EEG profile behavior
Re-run existing isolation tests
11. Strong rules for the next AI

The next AI must obey these rules:

Rule 1

Do not confuse:

reusable collector / reasoner tool domain
with
selected external project reasoning scope
Rule 2

Do not reintroduce developer_tools/kanda_reasoner_app/... into external project JSON.

Rule 3

Do not use runtime_runner.py as answer evidence for external project questions.

Rule 4

Do not generalize by deleting working logic blindly.
Generalize by separation, not destruction.

Rule 5

Do not assume missing links.
If evidence is missing, the answer should stay honest.

Rule 6

Prefer:

small patches
compile
retest
continue

not large rewrites.

12. Suggested first prompt for the next AI session

Use something like this:

We are continuing the Project Reasoner generalization work.

Read this tutorial first and follow it strictly.

Current goal:
generalize v10_retriever.py so the app can work with any project, not only eeg_kernel_ai_neural_data_analysis.

Important constraints:
- do not undo the external-project JSON isolation fix
- do not reintroduce developer_tools contamination
- do not break current EEG behavior
- proceed step by step
- first classify retriever heuristics into generic core vs project-specific profile candidates
- propose the minimal safe Step 1 refactor only
13. Final summary

The next session should NOT be about:

fixing contamination again
moving folders
rewriting the window
rewriting validators broadly

The next session SHOULD be about:

making retrieval architecture portable
separating project-specific boosts from generic retriever logic
preserving the now-working EEG behavior while enabling reuse for arbitrary projects

That is the canonical next objective.


# CANONICAL NEXT-SESSION ROADMAP
## Goal: Generalize Project Reasoner so it can harvest and answer questions for any selected project

This roadmap is for the next AI session.
It is not a brainstorming note.
It is a controlled implementation plan.

Follow it strictly.

---

# 0. Absolute rules

1. No hallucination.
   Do not guess.
   Do not assume.
   Do not invent missing files, call chains, symbols, classes, or flows.
   If a file is needed and not provided, ask for that file explicitly.

2. Keep the architecture canonical and parallel.
   There are 3 separate planes:

   A. Data collector plane
      Purpose: create and improve JSON only

   B. Runtime collector plane
      Purpose: generate internal runtime evidence only for the collector side

   C. V10 answer-reading plane
      Purpose: load JSON, retrieve evidence, build prompt, and answer questions

3. Never merge those planes.
   Data collector code must not be merged into V10 answer-reading logic.
   Runtime collector code must not be merged into V10 answer-reading logic.
   V10 must consume JSON only.

4. The selected external project is the reasoning target.
   `developer_tools/kanda_reasoner_app` is the tool.
   It is not the external project being analyzed.
   For external project reasoning, `developer_tools/...` must stay excluded from the final JSON and from answer evidence.

5. Keep current working behavior for `eeg_kernel_ai_neural_data_analysis`.
   Generalization must not destroy current EEG behavior.
   First separate.
   Then migrate.
   Then test.
   Then continue.

6. Every step must be:
   read files
   patch minimally
   compile
   run targeted tests
   validate behavior
   then continue

---

# 1. Canonical architecture to preserve

1. `reasoner_context_collector`
   creates the canonical project JSON.
   It may enrich that JSON.
   It must not be imported into V10 answer logic.

2. `reasoner_runtime_collector`
   is internal collector infrastructure.
   It may produce helper runtime evidence for collector-side enrichment.
   It must not be used directly by `v10_main_window.py` to answer project questions.

3. `project_reasoner_v10`
   is the answer-reading/UI plane.
   It loads the JSON, retrieves evidence, builds prompts, and asks the local model.
   The current window owns `JsonProjectIndex`, `ProjectRetriever`, `PromptBuilder`, and `LocalAIReasoner`. That separation must remain. :contentReference[oaicite:0]{index=0}

4. Main canonical file for AI use:
   `project_reasoner_v1_widget_text.json`
   This is the main project index.
   It may be used whole or split/reassembled later.

5. Helper file:
   `*_runtime_trace.json`
   This is helper/support evidence only.
   It is not the main canonical project index.

---

# 2. What is already fixed and must stay fixed

1. External selected project JSON must not contain:
   - `developer_tools/kanda_reasoner_app/...`
   - `runtime_runner.py`
   - internal runtime metadata from the reasoner tool

2. Internal runtime metadata is allowed only when collecting the internal reasoner root itself.

3. The producer-side isolation fix is already in place and protected by tests.
   Do not undo it.

4. Current AI grounding improvements are already in place:
   - better routing for code-evidence questions
   - narrower validator relaxation for generative code-localized questions
   - better retrieval for startup/top-navigation/reset/timeline question families
   Do not undo these changes while generalizing.

---

# 3. Main problem for next session

The current `v10_retriever.py` still contains many heuristics that are specific to `eeg_kernel_ai_neural_data_analysis`.

Examples of project-specific terms:
- `NotebookBuilder`
- `NavBarBuilder`
- `build_top`
- `build_upper`
- `addtab`
- `attach_timeline_to_tab`
- `eeg_traces_tab`
- timeline/topomap/reset owner-path boosts tied to current EEG project naming

This means:

- the app currently works well for the EEG project
- but portability to arbitrary projects is limited

The goal of next session is:

## Generalize retrieval architecture without breaking the current EEG behavior.

---

# 4. End-state architecture to reach

The retriever must become a 3-layer model.

## Layer 1. Generic core retriever
Portable to any project.

Must stay in `v10_retriever.py`.

Keep generic logic such as:
- exact path match
- exact filename match
- exact class/function/symbol match
- import/reference matching
- call-site matching
- entry-file boosts
- explanation / chain / flow boosts
- builder/launcher/main-window orchestration style boosts
- snippet-aware code-evidence routing
- collector-derived generic structural signals

## Layer 2. Collector-derived project structure
Still project-agnostic, but based on collected JSON.

Examples:
- `entry_files`
- `execution_chains`
- `qt_signal_map`
- ownership / responsibility
- subsystem summaries
- boundaries
- semantic roles
- other generic structural index outputs

This layer is already valuable and should remain.

## Layer 3. Optional project profile
Project-specific boosts, separated from the core.

Examples for the EEG project:
- notebook aliases
- navbar aliases
- timeline aliases
- topomap aliases
- reset / cleanup aliases
- owner-path boosts for EEG-specific folders

If no profile exists:
- generic retrieval must still work

If a profile exists:
- project-specific reasoning becomes sharper

---

# 5. Session protocol for the next AI

At the start of the next session, the AI must do this:

1. Read this roadmap fully.
2. Do not patch code yet.
3. Ask for the exact files needed for Step 1 only.
4. Read them.
5. Produce a classification of heuristics before changing anything.
6. Patch only one small step.
7. Compile and test.
8. Continue only after validation.

---

# 6. Step-by-step implementation roadmap

## Step 1. Inventory and classify retrieval heuristics

### Purpose
Separate:
- generic heuristics
- collector-derived structural heuristics
- EEG-project-specific heuristics

### Files the AI must ask for
1. `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_retriever.py`
2. `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_query_router.py`
3. `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_prompt_builder.py`
4. `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_main_window.py`
5. Any existing retriever tests, if present

### What to do
1. Read `v10_retriever.py` fully.
2. Mark every scoring rule as one of:
   - GENERIC
   - COLLECTOR-DERIVED
   - EEG-SPECIFIC
3. Output the list grouped by category.
4. Do not refactor yet.

### Expected output of Step 1
A written inventory such as:
- Generic core rules
- Collector-derived structural rules
- EEG profile candidates

### Validation
No code changes in this step.

### Stop condition
Do not continue until the classification is complete and explicit.

---

## Step 2. Introduce a project-profile structure without changing behavior

### Purpose
Create the architecture for profile-based specialization before moving any existing rules.

### Files the AI must ask for
1. `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_retriever.py`
2. `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_models.py`
3. `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_index_loader.py`

### New file to create
Recommended:
- `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_project_profile.py`

Optional supporting file:
- `developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_project_profile_registry.py`

### What to implement
Create a minimal profile container.
Example concept:

```python
from dataclasses import dataclass, field

@dataclass
class ProjectProfile:
    name: str = "generic"
    path_priority_terms: list[str] = field(default_factory=list)
    symbol_priority_terms: list[str] = field(default_factory=list)
    owner_path_boosts: dict[str, int] = field(default_factory=dict)
    question_aliases: dict[str, list[str]] = field(default_factory=dict)

Then add a simple loader/selector that can return:

generic profile by default
EEG profile later
Important rule

At the end of Step 2, behavior must still be unchanged.

Validation

Compile:

v10_project_profile.py
any touched file
Stop condition

Do not move EEG-specific rules yet.

Step 3. Wire the retriever to accept a profile, but keep old behavior
Purpose

Allow the retriever to consume a profile object, while still preserving current EEG behavior exactly.

Files the AI must ask for
developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_retriever.py
developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_index_loader.py
developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_main_window.py
What to implement
Add a project_profile field to the retriever or retriever setup path.
If no profile is supplied, use a default generic profile.
For now, still keep current EEG behavior active by returning the EEG profile when the loaded JSON corresponds to the EEG project.
Important rule

Do not remove any old heuristic yet.
This step only adds the profile plumbing.

Validation
Compile touched files.
Run current working EEG questions and confirm no regression:
startup chain
top navigation / superior tab
topomap chain
timeline chain
reset / cleanup chain
Stop condition

If EEG behavior regresses, fix the profile wiring before continuing.

Step 4. Migrate the first EEG-specific group: builder/navigation heuristics
Purpose

Move the least controversial EEG-specific terms out of the retriever core.

Files the AI must ask for
developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_retriever.py
developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_project_profile.py
Any retriever tests already created or existing
Heuristics to move first

Examples:

NotebookBuilder
NavBarBuilder
build_top
build_upper
addtab
top/upper navigation builder owner-path hints
What to implement
Remove those literals from the core scoring logic.
Place them into the EEG profile as profile-driven boosts.
Have the retriever apply them through a generic profile mechanism.
Important rule

The core retriever must no longer know those names directly.

Validation
Compile touched files.
Re-test:
top navigation / superior tab question
notebook / builder-definition question
Confirm same or better answer quality for EEG.
Stop condition

If EEG answer quality drops sharply, refine the profile application, not the core.

Step 5. Migrate timeline-specific heuristics into the profile
Purpose

Remove hardcoded timeline-specific EEG assumptions from the core retriever.

Files the AI must ask for
v10_retriever.py
v10_project_profile.py
If needed for context:
v10_prompt_builder.py
v10_query_router.py
Heuristics to move

Examples:

attach_timeline_to_tab
eeg_traces_tab
time_clicked
window_moved
timeline-specific owner-path boosts
What to implement
Move timeline-specific literals and owner-path boosts into the EEG profile.
Keep only generic “where is X called / exact callsite / import+call” logic in the core.
Validation
Compile touched files.
Test timeline-specific questions again.
Confirm the AI still finds:
plugins/eeg_traces/eeg_traces_tab.py
shell/timeline/eeg_timeline_attachment.py
honest answers when the exact caller is missing from retrieved evidence
Stop condition

Do not continue until timeline behavior is preserved.

Step 6. Migrate topomap/amplitude-map heuristics into the profile
Purpose

Separate EEG topomap domain knowledge from generic retrieval.

Files the AI must ask for
v10_retriever.py
v10_project_profile.py
Heuristics to move

Examples:

topomap-specific path terms
amplitude-map-specific boosts
topomap renderer ownership hints
project-specific path families tied to topomap files
What to implement

Move those terms into the EEG profile.

Validation

Retest:

“Which code implements the topomap?”
“Explain the topomap chain...”
Stop condition

No generic-core hardcoded topomap literals should remain if they are clearly EEG-domain-specific.

Step 7. Migrate reset/cleanup heuristics into the profile
Purpose

Remove project-specific reset/cleanup naming assumptions from the core.

Files the AI must ask for
v10_retriever.py
v10_project_profile.py
Heuristics to move

Examples:

owner-path boosts tied to current EEG reset modules
cleanup module names
snapshot-specific project naming
Validation

Retest:

reset / cleanup chain question
Stop condition

The generic core should keep only generic reset/cleanup language, not EEG file-name assumptions.

Step 8. Add profile selection logic that works for arbitrary projects
Purpose

Choose the right profile for the loaded JSON without coupling V10 to collector/runtime code.

Files the AI must ask for
v10_index_loader.py
v10_main_window.py
v10_project_profile.py
v10_project_profile_registry.py if created
What to implement

Profile selection should use only loaded JSON information or project-root context.
Examples:

project root path
project summary hints
entry file names
subsystem names
known domain markers
Important rule

Do not import collector code into V10.
Do not call runtime collector code.
Profile selection must use already-loaded JSON only.

Validation
Compile touched files.
Confirm:
EEG project loads EEG profile
unknown project falls back to generic profile
Stop condition

No direct dependency from v10_main_window.py to data collector or runtime collector logic.

Step 9. Add generic collector-side profile hints, if needed
Purpose

Optionally enrich the JSON with generic project identity hints that help profile selection, without merging planes.

Files the AI must ask for
developer_tools/kanda_reasoner_app/reasoner_context_collector/collector_main.py
developer_tools/kanda_reasoner_app/reasoner_context_collector/collector_output.py
relevant collector tests
What to implement

If needed, add generic top-level or summary fields such as:

project type hints
entry-point families
UI framework hints
dominant subsystem families
path-family summaries

These hints must be:

generic
collector-produced
passive data only
Absolute rule

Do not put V10 answer logic inside collector code.
Collector produces data only.

Validation
Compile collector files.
Rebuild JSON.
Confirm external-project contamination protections still pass.
Confirm hints are generic and free of internal reasoner contamination.
Stop condition

No developer_tools/... leakage in external project JSON.

Step 10. Add tests for generic mode and profile mode
Purpose

Protect the new architecture from regression.

Files the AI must ask for
existing tests in:
reasoner_context_collector/tests/
any V10 tests if present
touched files from Steps 2–9
Tests to add
Generic mode:
no profile found
generic retriever still works
EEG profile mode:
profile boosts apply
current EEG answers still work
External-project JSON isolation:
must continue passing
Internal reasoner root:
may still include internal runtime metadata where allowed
Important rule

Each test must target one contract only.

Validation

Run targeted pytest commands after each added test file.

Step 11. Update help/documentation only after behavior is stable
Purpose

Document the generalized architecture without racing ahead of implementation.

Files the AI must ask for
v10_help_index.py
current README or contract docs if relevant
What to document
V10 reads JSON only
Data collector creates JSON only
Runtime collector enriches collector-side information only
Project profiles are optional and project-specific
Generic mode works without a project profile
Important rule

Do not write docs for behavior that is not yet implemented and validated.

7. Concrete validation checkpoints after each phase

After every phase, the AI must run all relevant validations.

Minimum compile rule

Always compile every touched file.

Minimum regression rule

Always rerun the smallest targeted tests related to the step.

Minimum live behavior rule

For EEG project, retest at least one known-good question from:

startup
top navigation
timeline
reset/cleanup
8. Canonical file requests by phase
Phase 1 files to request
v10_retriever.py
v10_query_router.py
v10_prompt_builder.py
v10_main_window.py
existing retriever tests, if any
Phase 2 files to request
v10_retriever.py
v10_models.py
v10_index_loader.py
Phase 3 files to request
v10_retriever.py
v10_index_loader.py
v10_main_window.py
Phase 4–7 files to request
v10_retriever.py
v10_project_profile.py
relevant tests
Phase 8 files to request
v10_index_loader.py
v10_main_window.py
v10_project_profile.py
registry/helper file if present
Phase 9 files to request
collector_main.py
collector_output.py
related collector tests
Phase 10 files to request
all touched tests and touched production files
Phase 11 files to request
v10_help_index.py
README / contract doc if needed
9. Hard stop conditions

The next AI must stop and report if any of these occur:

External project JSON starts containing developer_tools/kanda_reasoner_app/... again.
runtime_runner.py reappears as answer evidence for external project questions.
V10 starts importing collector or runtime collector logic directly.
EEG answer quality collapses after moving a profile group.
The AI cannot verify a needed file and would otherwise have to guess.
10. Final directive for the next AI

Start with Step 1 only.

Do not jump to Step 4 or Step 8.
Do not do a large rewrite.
Do not generalize by deleting working code blindly.

The correct sequence is:

classify
introduce profile structure
wire profile support with no behavior change
migrate one heuristic group at a time
test each step
preserve collector/runtime/V10 separation
keep the app canonical

That is the required implementation path.


