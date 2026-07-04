first_prompts_to_ai.zip
Zip Archive
prompt_library.zip
Zip Archive
tell_AI_read_before_all.md
File
zz_read_only_if_modifying_startup_delivery.md
File

STARTUP PACK LOAD CHECK

Files recognized:
0. 00_START_HERE_FOR_AI.md - loaded - stable AI entrypoint, mandatory read order, and startup load-check instruction.

    01_ai_prompt_request_canon.md - loaded - defines how to request missing prompt groups, folder cards, specialist prompts, and behavior gates.

    02_prompt_navigation_index.md - loaded - maps task types to prompt groups and specialist prompt candidates.

    03_GROUP_ASSIMILATION_INDEX.md - loaded - summarizes the 12 prompt groups for first-pass routing.

    04_FOLDER_ASSIMILATION_CARDS_INDEX.md - loaded - indexes folder assimilation cards for folder-level boundaries and placement rules.

    05_start_of_day_master_stack.md - loaded - defines daily startup behavior, tiered routing, and startup bridges.

    06_session_start_upload_checklist.md - loaded - defines which context files should be present at session startup.

    07_daily_patch_delivery_guardrails.md - loaded - governs patch delivery staging, validation, terminal hygiene, and freeze-ready delivery rules.

    08_handoff_at_end_of_work.md - loaded - defines required end-of-work handoff behavior for governed sessions.

    09_patch_install_delivery_error_register.md - loaded - blocks repeated install, ZIP staging, and validation-wrapper regressions.

    10_prompt_router_reasoner_startup_check.md - loaded - defines Prompt Router Reasoner readiness and startup status behavior.

    11_chatgpt_kanda_routing_choice_output_protocol.md - loaded - defines safe advisory routing-choice output and prompt-library direct retrieval.

    12_error_memory_ai_formulary_startup_canon.md - loaded - defines Error Memory formulary intake behavior after errors, failures, and corrections.

    09_active_project_freeze_context.md - loaded - exposes active-project freeze memory and post-validation freeze-awareness rules.

    README_STARTUP_PROMPT_REQUEST_KERNEL.md - loaded - explains startup ZIP purpose, workflow, companion prompt-library ZIP, and integrity.

    STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json - loaded - provides manifest metadata, generation source, file roles, and integrity data.

Beginning-of-day active bridges:

    Code Module Size Bridge - loaded - hard gate: ideal <=400 code lines; maximum <=500 physical lines; every new or touched code/source module must be <=500 lines after create, update, modify, refactor, or split work; route above-limit code work to large_module_refactor_protocol on demand.

    Box Logic Startup Bridge - loaded - hard gate: mandatory beginning-of-chat box shield; identify active box, owner paths, allowed files, out-of-scope files, cross-box touches, public contracts, validation scope, and boundary risks before project work; keep code and responsibility inside the owning box; route boundary-risk work to box_architecture_canon on demand.

    Terminal Cleanup Bridge - loaded - install success waits about 2 seconds then Clear-Host; validation, freeze, errors, diagnostics, and other terminal blocks use Enter Enter then one final Clear-Host; keep terminal open; freeze-prep evidence merge must use a temp .py helper, not python -c, with PYTHONPATH/sys.path set to the project root.

Startup status:
COMPLETE

Routing behavior:
Startup routing is active. Fast Path is available only for safe explanation or non-governed tasks. Governed project, prompt-library, startup-delivery, patch, validation, freeze, GUI, architecture, or implementation work must route through the loaded indexes and request only the specific missing prompt, folder card, project file, or source archive needed. prompt_library.zip is recognized as the canonical on-demand prompt source and must not be opened wholesale at startup.

Next action:
Waiting for all files (Project Files) from second_prompt_files folder.

_RUN_COLLECTOR_STATUS.txt
Document
kanda_reasoner__ai_handoff_all_in_one.zip
Zip Archive
kanda_reasoner__ai_handoff_upload.zip
Zip Archive
kanda_reasoner__ai_handoff_upload_readme.txt
Document
kanda_reasoner__error_lessons_compact.json
File
kanda_reasoner__error_memory_ai_prompt.md
File
kanda_reasoner__error_memory_full.zip
Zip Archive
kanda_reasoner__error_memory_manifest.json
File
kanda_reasoner__png_assets_part01_of_01.zip
Zip Archive
kanda_reasoner__source_archive_part01_of_01.zip
Zip Archive

Vou carregar o segundo grupo na ordem indicada, verificar o ZIP de handoff principal e confirmar o estado do projeto antes de qualquer tarefa real.

PROJECT READY CHECK

Project slug:
kanda_reasoner

Active project root:
<PROJECT_ROOT> / inferred selected project: E:\kanda_reasoner

KANDA tool root:
<PROJECT_ROOT> / kanda_reasoner

Same physical root:
YES

Compact Error Memory loaded:
YES - 10 active compact lessons loaded; full Error Memory ZIP not opened because policy says open only when needed.

Second-upload handoff loaded:
YES - collector status is complete, ZIP export complete, and kanda_reasoner__ai_handoff_upload.zip was read as the primary JSON handoff package.

Tier-1 gates active:
YES - startup routing gates, compact Error Memory preflight, source-truth-before-editing, patch-safety routing, box boundary checks, module-size bridge, terminal cleanup bridge, and validation/freeze guardrails are active.

Next action:
WAIT_FOR_TASK

microfone is not working, any problem , or tolken proble?

Probably not a token problem. When the microphone does not work, it is usually one of these:

    Browser permission blocked

        In Firefox/Chrome, click the lock icon near the address bar.

        Check Microphone permission for ChatGPT.

        Set it to Allow, then refresh the page.

    Wrong microphone selected

        Check Windows sound settings and make sure the correct input device is selected.

        Also check the browser’s site permissions.

    Mic muted inside Voice Mode

        OpenAI’s Voice Mode FAQ says you may need to grant browser microphone access the first time, and during voice conversation you can mute/unmute the mic with the microphone icon.

    Browser/app glitch

        Refresh ChatGPT.

        Close and reopen the browser.

        Try another browser.

        Try the ChatGPT mobile app to see whether the issue is only on the computer.

    Windows privacy setting

        Windows Settings → Privacy & security → Microphone.

        Enable microphone access for apps and for the browser.

It is unlikely to be a token limit issue. Token problems affect message length/context, not microphone input. If typing works but audio does not, it is almost certainly permission, device selection, browser, or temporary voice-service instability.

0035 how refactor large files gui 30.06.2026.md
File
0035a how refactor large files 30.06.2026.md
File
0035b how refactor large files 30.06.2026.py
Python
0035c how refactor large files 30.06.2026.md
File
I want to implement a sub-tab on architecture review. Architecture review has already run selected mode, large module AST, split audit. I'd like to insert a tab exclusively for refactoring large files inside architecture review. What do you think about these ideas I uploaded? Can you improve it? Can you make it better? What do you think? And tell me what is your opinion.

I will treat this as a design review, not as an implementation patch yet. I will compare the uploaded idea files against the active architecture-review context and point out what should become the sub-tab contract.

I already see the main direction: the idea is strong, but it should be a guided refactor workflow, not an automatic "split this file now" button. The safest version is a proposal-first sub-tab that reuses Architecture Review evidence and only writes after validation plus explicit confirmation.

My opinion: yes, this is worth implementing, and it fits naturally inside Architecture Review. But I would not design it as an automatic refactor button. I would design it as a Large File Refactor Planner: it analyzes, proposes, previews, validates, and only then allows confirmed patch creation.

Your uploaded idea is strong because it already uses the right split of responsibility: deterministic AST/graph logic for most of the work, local LLM only for semantic boundary decisions, and LLM repair only for hard conflict cases. The skeleton also already defines the right target constraints: ideal 400 lines, maximum 500 lines, and minimum 100 lines to avoid tiny helper files.
My main improvement: do not make the base module “the largest bin”

In the skeleton, the largest bin becomes the base module. I would change that.

For KANDA Reasoner, the base module should usually be a facade/orchestrator, not the largest chunk. It should preserve public API, imports, compatibility, and entrypoints. The heavy implementation should move into private helper modules.

Better rule:

base module = public facade / orchestrator / compatibility surface
helper modules = extracted implementation groups

So the output should look more like:

architecture_review_large_file_refactor.py          # facade, public API, <=400 lines
_large_file_refactor_analysis.py                    # AST/CST analysis
_large_file_refactor_partition.py                   # bin planning
_large_file_refactor_imports.py                     # import mapping/rewrite
_large_file_refactor_validation.py                  # validation and cycle checks
_large_file_refactor_llm.py                         # optional local LLM arbitration

Not:

largest detected bin becomes the main module

That would risk preserving the monolith shape under a new filename.
Best sub-tab concept

I would name the sub-tab:

Large File Refactor Planner

Not “Large File Refactor” alone, because “Planner” communicates that it is proposal-first and not a destructive automatic writer.

Inside Architecture Review, it should sit beside the existing:

Run Selected Mode
Large Module AST
Split Audit
Large File Refactor Planner

The key idea: this new tab should consume evidence from the existing Architecture Review tools instead of duplicating them.
Suggested GUI layout

I would make the tab four zones:
1. Candidate files panel

Shows large files already detected by Architecture Review.

Columns:

File
Lines
Public symbols
Classes
Functions
Imports
Current architecture warnings
Suggested action

Suggested action examples:

Plan split
Needs source inspection
Blocked: public API risk
Blocked: global state
Already compliant

2. Refactor settings panel

Controls:

Ideal file size: 400
Maximum file size: 500
Minimum helper size: 100
Preserve public facade: ON
Use local LLM for ambiguous symbols: optional
Generate patch only, do not write directly: ON
Rewrite imports project-wide: optional but gated

I would keep Preserve public facade always on by default.
3. Proposed split panel

This is the heart of the tab.

Display each proposed output file:

architecture_review_x.py - 382 lines
  public facade
  exports: run_review, build_report

_architecture_review_ast.py - 427 lines
  symbols: parse_module, collect_symbols, collect_imports

_architecture_review_split_audit.py - 391 lines
  symbols: find_large_modules, build_split_candidates

Each proposed file should have status badges:

OK
Too large
Too small
Cycle risk
Import risk
Global state risk
Needs human decision

4. Validation and patch panel

Buttons should be staged:

Analyze only
Generate refactor plan
Preview generated files
Validate plan
Create patch ZIP
Confirm and Write

I would not allow “Apply directly” from this tab.
What your uploaded blueprint gets right

The best parts are:

    AST first, LLM second. The blueprint correctly avoids throwing a 3,500-line file into an LLM and hoping for a miracle. It parses symbols, builds a dependency graph, detects clusters, and only then asks the model about ambiguous boundaries.

    The 70/20/10 split is realistic. About 70% can be handled by deterministic structure, 20% by semantic grouping, and 10% by repair after subtle dependency/global-state problems.

    The risk list is correct. The uploaded review correctly identifies the dangerous parts: missing imports after moving symbols, circular imports between generated bins, decorator loss, and global-state ordering.

    LibCST is the right direction. Raw line slicing is fine for an early prototype, but production should use LibCST for comment/decorator/format preservation and import rewriting.

What I would add before implementing

I would add five hard gates.
Gate 1: “No source write from first pass”

The first pass should only generate:

refactor_plan.json
refactor_preview.md
proposed_file_map.json
risk_report.json

No code movement yet.
Gate 2: public API preservation

Before and after split, collect:

__all__
top-level public functions
top-level public classes
imported external references
known facade functions

Then validate:

old public API == new facade public API

This matters because Architecture Review already has public-surface rules, and previous Error Memory lessons show that public API ownership errors are a recurring source of problems.
Gate 3: import graph cycle validator

Your uploaded improvement already points to this. It is mandatory.

Before generating files, build:

symbol graph
bin graph
module import graph

If generated modules form:

A -> B -> A

then the plan is not ready. The tool should either merge bins or create a proposed shared helper.
Gate 4: global state quarantine

Global state should not be moved automatically.

Examples:

logging.basicConfig(...)
module-level cache = {}
environment reads
path initialization
Tkinter/UI initialization
plugin registration

These should stay in the base facade unless the user explicitly approves a move.
Gate 5: line-count validator after generation

The tab must validate the actual generated physical files, not just estimated symbol lines.

Required checks:

base module <= 500 physical lines
helper modules <= 500 physical lines
target ideal around 400 lines
no helper below 100 lines unless justified
no touched module above the active hard limit

My recommended implementation strategy

I would implement this in three versions.
Version 1: planner only

No code moving.

It should:

Read Architecture Review large-module findings
Let the user choose one large file
Analyze AST/CST symbols
Build dependency clusters
Suggest output files
Show line-count estimates
Flag ambiguous symbols
Show blockers

This version is safe and already useful.
Version 2: preview generator

Still no direct write.

It should generate proposed files into a temporary preview folder under the daily-work area, then run:

py_compile
line-count validation
import-cycle validation
public API preservation check
architecture validation if available

Version 3: patch creator

Only after the preview generator is solid.

It should create an installable patch ZIP with:

changed files only
validation script
KANDA_FREEZE_HINT.json if freezeable
clear install/validation commands
no direct root clutter

My verdict

I strongly support the feature, but I would narrow the first implementation.

Do not start by building a full automatic refactor engine.

Start with:

Architecture Review -> Large File Refactor Planner -> proposal-only

The first goal should be:

Given one large file, produce a safe split plan with line counts, symbol groups, dependency risks, and validation blockers.

Only after that should it generate preview files. Only after preview validation should it create patches.

The idea is excellent. The better version is not “AI refactors large files.” The better version is:

Architecture Review detects architectural debt.
Large File Refactor Planner converts that debt into a validated, reviewable split plan.
Human confirms.
Patch system applies.
Validation proves it.
Freeze system preserves it.


I want you remember some things. First, Canda Reasoner is a tool to improve, to help the building of apps, of code. But casually, we are working on itself. We are working in Canda Reasoner. So, Canda Reasoner here is a tool and also it is the project we are working on. It's important you make the difference between project and tool. Files related to project must be linked to project files. And files that are related to tools must be linked to the tool. For example, when you build a, when you refactor a module, code that refactor the module, that does the work, belongs to the tool. Besides the result, the splitted file, the file refactored, and its help files, they belong to the project. That must be very clear to you. For example, inside of Canda Reasoner in project files, in project path, we can have another completely different project. So, it's important to remember that we have Reasoner Canda as tool that builds where we are building the structure for refactor, for handle the code, whilst Canda Reasoner as a project is a separate thing. That's one point. The second point to remember is that it's very important to use box logic, shielding logic, and no leaking logic. Search in project for these implementations or these rules, okay? Tell me if you understand what I am talking about.

I understand the distinction you are making. I will save the durable rule, then I will search the uploaded project context for “box logic”, “shielding”, and “no leaking” so I can align future patches with the actual implementation instead of relying only on memory.

Yes, I understand.

I saved the rule: KANDA Reasoner must be treated as two separate identities:

    KANDA Reasoner as the tool
    Owns reusable engines, GUI tabs, validators, refactor planners, source analyzers, patch tooling, prompt routing, freeze tooling, and other machinery that can operate on any project.

    KANDA Reasoner as the active project
    Owns the actual project source being changed, plus project-specific outputs such as split/refactored files, project helper files, freeze memory, handoff output, and validation evidence.

So for the large-file refactor feature:

Refactor engine / planner / analyzer / GUI sub-tab = tool-side logic
Specific generated split files for a selected module = project-side output

I also searched the uploaded project archive. The rule already exists in project context as Project Tool Boundary Canon, with exactly this separation: the reusable KANDA Reasoner runtime must not be collapsed into the selected active project, even when the selected project is KANDA Reasoner itself. It also says project-specific support state belongs under the active project support/daily-work roots, while reusable tool writes stay in the KANDA Reasoner tool source.

I also found the relevant box/shielding rules:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md
scripts/validate_project_tool_boundary_canon_v1.py
kanda_reasoner_app/reasoner_context_collector/collector_boundary_violations.py
kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/boundary_guard.py

This aligns with the startup bridge, which requires identifying the active box, owner paths, allowed files, out-of-scope files, cross-box touches, public contracts, validation scope, and boundary risks before project work.

For future patches, I will apply this distinction before touching files:

BOX CHECK
- Is this reusable KANDA Reasoner tool logic?
- Is this selected-project source/output?
- Is this project-specific support state?
- Are we accidentally writing tool logic into project files?
- Are we accidentally writing project-specific memory into tool/global paths?
- Are we crossing into another box?

And I will treat box logic, shielding logic, and no-leaking logic as mandatory for the architecture-review refactor tab. The compact Error Memory also supports this cautious approach: exact source files still need inspection before editing, and compact lessons are prevention guidance, not source truth.

is this already implemented in code?

Yes, partially implemented, but not completely in the way you are describing.

The current state looks like this:
1. Tool/project boundary logic: already exists, partially implemented

This is already present at three levels:

Prompt/canon level: yes. There is a project_tool_boundary_canon.md in the prompt library. It explicitly defines the separation between KANDA Reasoner as reusable tool/runtime and the active selected project.

Validation level: yes. There is a validator:

scripts/validate_project_tool_boundary_canon_v1.py

It checks that the canon, routing text, and path helpers preserve the distinction between tool root, active project root, external *_show_project_to_AI, and *_delete_after_daily_work.

Code/path level: yes, partially. I found actual source code that supports dynamic project resolution and avoids hardcoding KANDA Reasoner as the only project:

kanda_reasoner_app/project_root_resolver.py
kanda_reasoner_app/_project_analysis_evidence_path_resolution.py
kanda_reasoner_app/project_analysis_evidence_paths.py

Those files implement dynamic active-project support paths such as:

<project_drive>/<active_project_slug>_show_project_to_AI
<project_drive>/<active_project_slug>_delete_after_daily_work

So the project/tool distinction is not only a prompt idea. It is partly enforced in code.
2. Box logic / shielding / no-leaking: partially implemented

Also yes, but spread across several layers.

I found:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md
kanda_reasoner_app/reasoner_context_collector/collector_boundary_violations.py
kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/boundary_guard.py

The startup system also has a Box Logic Startup Bridge, which says every project task must identify active box, owner paths, allowed files, out-of-scope files, cross-box touches, public contracts, validation scope, and boundary risks before project work.

So: box/shielding logic exists, but I would not yet call it a single universal enforcement system. It is implemented as a combination of:

prompt canons
startup bridge
path helpers
boundary violation collector
routing boundary guard
validation scripts

3. Large-file refactor sub-tab: not implemented yet

The specific thing you want now — an Architecture Review sub-tab dedicated to large-file refactor planning — does not appear to be implemented yet.

The current Architecture Review GUI source I inspected has these two local subtabs:

Run Selected Mode
Large Module AST Split Audit

I did not find a third sub-tab like:

Large File Refactor Planner
Large File Refactor
Refactor Large Module

So this part still needs a patch.
4. Heuristic refactor engine: not implemented yet, only skeleton/design

The uploaded 0035b how refactor large files 30.06.2026.py is a good skeleton, but it is clearly not production implementation yet. It still has TODOs for the most important pieces: circular-import detection, dangling reference detection, cross-bin imports, LibCST writing, project-wide import rewriting, and physically moving LLM-reassigned symbols between bins.

The orchestrator also still treats several stages as placeholders, including conflict repair and project-wide import rewriting.

So my answer is:

Tool/project boundary: YES, partially implemented in code.
Box/shielding/no-leaking: YES, partially implemented in code and prompts.
Large-file refactor planner sub-tab: NO, not yet implemented.
Automatic/refactor proposal engine: NO, only blueprint/skeleton exists.

My recommendation: before creating the new sub-tab, we should make its first internal gate explicitly ask:

Is this refactor engine/tool code?
Or is this generated project refactor output?

That gate should be built directly into the new Large File Refactor Planner workflow, because the uploaded blueprint correctly says this should be a proposal tool, not an auto-applier.

First tell me, is box logic, shielding logic, and no-leak logic already well described in prompts? Is it all right in Bridge? And it's easy to you to find next time we open a chat. First this.

Yes — mostly yes.
1. Box logic is well described in prompts

It is clearly described in the prompt library under:

04_box_architecture_and_boundaries
box_architecture_canon.md

It defines the key rule: before implementation/refactor/architecture work, I must identify:

active box
owner paths
allowed files
out-of-scope files
cross-box touches
public contracts
validation scope
boundary risks

That is exactly the behavior you want.
2. Shielding logic is also well described

It is separately described under:

04_box_architecture_and_boundaries
kanda_box_shielding_canon.md

That canon treats shielding as a box-protection layer, not as a feature expansion. It protects boundaries, contracts, side effects, dependency direction, and prevents invading neighboring boxes.

So yes: shielding is not only implied; it has its own canon.
3. No-leak logic exists, but I would improve its naming

The concept is there. It appears as:

no private reach-in
no leaking registry behavior
no hidden mutable cross-box state
anti-contamination
do-not-invade-other-box boundary
tool/project boundary separation

So the logic exists, but the exact phrase “no-leak logic” is not as visible as “box logic” and “box shielding”.

My opinion: it would be safer to eventually add a small explicit named bridge phrase like:

No-Leak Logic Bridge - prevent tool/project leakage, cross-box leakage, private reach-in, hidden mutable state, and wrong-root writes.

Not urgent, but it would make the concept easier to retrieve and harder to miss.
4. The bridge is all right

The startup bridge already says the important thing:

Box Logic Startup Bridge - hard gate: mandatory beginning-of-chat box shield; identify active box, owner paths, allowed files, out-of-scope files, cross-box touches, public contracts, validation scope, and boundary risks before project work; keep code and responsibility inside the owning box; route boundary-risk work to box_architecture_canon on demand.

That is good. It is compact, findable, and loaded at startup.
5. Will it be easy to find next chat?

Yes, if the normal startup files are loaded, it is easy to find next time because:

tell_AI_read_before_all.md loads the startup bridge
first_prompts_to_ai.zip contains routing/index logic
prompt_library.zip contains the full box/shielding canons
04_box_architecture_and_boundaries is the obvious route

The startup instructions also tell me not to open the full prompt library at startup, but to retrieve the exact prompt only when routing selects it. That means next time I should first see the bridge, then request/load the specific box/shielding canon if the task touches architecture or boundaries.
My verdict

Box logic: YES, well described.
Shielding logic: YES, well described.
No-leak logic: YES, concept exists, but naming could be made more explicit.
Bridge: YES, good and active.
Easy to find next chat: YES, through the startup bridge and 04_box_architecture_and_boundaries.

The only improvement I would make later is to give no-leak logic a more explicit named bridge or checklist, because the concept is present but distributed across boundary, shielding, anti-contamination, and project/tool separation language.

give no-leak logic a more explicit named bridge or checklist, because the concept is present but distributed across boundary, shielding, anti-contamination, and project/tool separation language.Specify no leak logic as an unique specific object inside that logic.

This is governed prompt/startup-boundary work because it changes how the routing logic names and retrieves a boundary concept. I will keep it small: add “No-Leak Logic” as a named object, not rewrite the whole box system.

Yes. I would define it as a first-class named object inside Box Logic/Shielding, not as scattered wording.

The current startup bridge already has the right foundation: it says the Box Logic bridge must identify active box, owner paths, allowed files, out-of-scope files, cross-box touches, public contracts, validation scope, and boundary risks before project work.

But I agree with you: “No-Leak Logic” should become its own explicit object.

Here is the exact object I would add.
No-Leak Logic Bridge

NO_LEAK_LOGIC_V1: No-Leak Logic is a named boundary-protection object inside Box Logic and Box Shielding.

It prevents ownership, path, state, contract, evidence, and responsibility from leaking across boxes.

No-Leak Logic is not a separate architecture system. It is a specific enforcement object inside the existing Box Logic and Shielding discipline.
Core rule

Before implementation, refactor, prompt update, validation, freeze, patch delivery, GUI work, or artifact generation, classify every touched item as one of:

    tool-owned logic;

    active-project source;

    project-specific support state;

    generated evidence or handoff artifact;

    temporary daily-work artifact;

    external box dependency;

    out-of-scope file.

If classification is unclear, stop before writing and inspect the source, manifest, prompt, or validation context.
No-Leak checklist

The AI must block or flag all of the following:

    Tool/project leakage
    Reusable KANDA Reasoner tool logic must not be written into active-project output paths. Active-project generated/refactored files must not be written into reusable tool-source paths.

    Wrong-root leakage
    Project-specific support files must use the selected active project root and its external support folders, not a hardcoded KANDA Reasoner root.

    Cross-box logic leakage
    Code, imports, mutable state, UI logic, domain logic, prompt logic, validation logic, governance logic, freeze logic, or delivery logic must not move from one box into another without an explicit governed cross-box touch.

    Private reach-in leakage
    A box must not import, call, edit, or depend on another box's private internals. Use public contracts only.

    Public API ownership leakage
    Helper modules must not accidentally become public owners of facade symbols. Facades own public compatibility surfaces unless a separate architecture change approves another owner.

    Mutable-state leakage
    Hidden mutable globals, registries, caches, singletons, or shared runtime state must not become silent communication channels between boxes.

    Generated-artifact leakage
    Generated handoff files, startup ZIP contents, reports, manifests, validation output, and preview artifacts are not source truth unless explicitly promoted through the governed source path.

    Validation/freeze leakage
    Validation evidence, freeze hints, freeze memory, and error-memory intake must stay in their governed locations and must not be mixed into unrelated tool, project, or generated-output paths.

    Prompt/canon leakage
    Prompt-library canon updates must be made in canonical prompt files, not only in generated startup artifacts or copied ZIP contents.

    Refactor-output leakage
    Refactor engines, analyzers, planners, and validators are tool-owned. The concrete split/refactored files produced for a selected project are project-owned.

Required output when risk exists

When a task has no-leak risk, output this before implementation:

NO-LEAK CHECK

Active box:
Tool-owned files:
Project-owned files:
Project-specific support files:
Generated/evidence files:
Temporary daily-work files:
External boxes touched:
Out-of-scope files:
Leak risks:
Blocked writes:
Safe next action:
Routing rule

If any no-leak answer is uncertain, route to:

    box_architecture_canon.md;

    kanda_box_shielding_canon.md;

    project_tool_boundary_canon.md when tool/project ownership is involved;

    startup delivery maintenance rules when generated startup delivery is involved.

Do not proceed from memory when ownership, root, box, public contract, generated/source status, or freeze/validation location is unclear.

I would place this in three places:

1. box_architecture_canon.md
   As a new section: "No-Leak Logic Object"

2. kanda_box_shielding_canon.md
   As a shield-specific checklist: "No-Leak Shield Checklist"

3. start_of_day_master_stack.md
   As a compact startup bridge: "No-Leak Logic Bridge"

And I would update the startup load check so next chat shows:

Beginning-of-day active bridges:
1. Code Module Size Bridge
2. Box Logic Startup Bridge
3. No-Leak Logic Bridge
4. Terminal Cleanup Bridge

That would make it easy to find next time. The startup instructions already make prompt_library.zip the on-demand source and say the AI should retrieve exact prompts only when routing selects them, so naming the object NO_LEAK_LOGIC_V1 makes it much easier to locate later.

do it

I will implement this as a small governed startup/prompt-library patch: add NO_LEAK_LOGIC_V1 to the canonical box/shielding prompts and add a compact No-Leak bridge to startup delivery sources. I will inspect exact source paths first, then package only changed files.

I found the exact places that need the small patch: the canonical Box Architecture canon, Box Shielding canon, Project Tool Boundary canon, start-of-day master stack, and the startup generator files that print the bridge list.

Done. I created the patch ZIP:

What it changes:

- Adds NO_LEAK_LOGIC_V1 as a named object inside Box Architecture.
- Adds a No-Leak Shield Checklist inside Box Shielding.
- Adds a No-Leak tool/project rule inside Project Tool Boundary Canon.
- Adds a startup-visible No-Leak Logic Bridge to start_of_day_master_stack.md.
- Updates startup generator bridge reporting so future startup load checks show:
  1. Code Module Size Bridge
  2. Box Logic Startup Bridge
  3. No-Leak Logic Bridge
  4. Terminal Cleanup Bridge
- Adds validation/test_no_leak_logic_bridge_v1.py.

Validation completed in sandbox:

VALIDATION OK: no-leak-logic-bridge-v1
STATUS: SOURCE_CHECKED
ZIP CONTRACT: PASS

One honest note: I did focused source validation and patch ZIP contract validation. I did not use full startup generator sync as release evidence in the sandbox because the uploaded source archive did not include prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md, which the generator expects. The patch is structured so you can run the full sync locally after install if your full workspace has that source file. Startup-delivery maintenance requires generated delivery files to remain outputs, not canonical sources.
Install

Save the ZIP as:

E:\kanda_no_leak_logic_bridge_v1_patch.zip

Then run this in Windows PowerShell / PyCharm terminal:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "kanda_no_leak_logic_bridge_v1_patch"
$PAYLOAD_FOLDER = "kanda_no_leak_logic_bridge_v1_patch_payload"

$ErrorActionPreference = "Stop"

try {
    $ProjectPath = (Resolve-Path $PROJECT_ROOT).Path
    $ProjectName = Split-Path $ProjectPath -Leaf
    $DriveRoot = [System.IO.Path]::GetPathRoot($ProjectPath)
    $WorkDir = Join-Path $DriveRoot ($ProjectName + "_delete_after_daily_work")
    $RootPatchZip = Join-Path $DriveRoot ($PATCH_NAME + ".zip")
    $WorkPatchZip = Join-Path $WorkDir ($PATCH_NAME + ".zip")
    $ExtractDir = Join-Path $WorkDir ($PATCH_NAME + "_extract")

    if (-not (Test-Path $WorkDir)) {
        New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null
    }

    if (Test-Path $RootPatchZip) {
        Copy-Item -Path $RootPatchZip -Destination $WorkPatchZip -Force
        if (Test-Path $WorkPatchZip) {
            Remove-Item -Path $RootPatchZip -Force
        }
    } elseif (-not (Test-Path $WorkPatchZip)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ExtractDir) {
        Remove-Item -Path $ExtractDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $ExtractDir -Force | Out-Null
    Expand-Archive -Path $WorkPatchZip -DestinationPath $ExtractDir -Force

    $PayloadDir = Join-Path $ExtractDir $PAYLOAD_FOLDER
    if (-not (Test-Path $PayloadDir)) {
        throw "Patch payload folder was not found inside the staged ZIP."
    }

    Copy-Item -Path (Join-Path $PayloadDir "*") -Destination $ProjectPath -Recurse -Force

    Write-Host ""
    Write-Host "INSTALL OK. Terminal will clear in 2 seconds..."
    Start-Sleep -Seconds 2
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL ERROR. Review the error below before clearing the terminal."
    Write-Host $_.Exception.Message
    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
    $global:LASTEXITCODE = 1
    return
}

Validate

$PROJECT_ROOT = "E:\kanda_reasoner"
$ErrorActionPreference = "Stop"

try {
    $ProjectPath = (Resolve-Path $PROJECT_ROOT).Path
    $env:PYTHONPATH = $ProjectPath
    python (Join-Path $ProjectPath "validation\test_no_leak_logic_bridge_v1.py")
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION ERROR. Review the error below before clearing the terminal."
    Write-Host $_.Exception.Message
    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
    $global:LASTEXITCODE = 1
    return
}

Expected result:

VALIDATION OK: no-leak-logic-bridge-v1
STATUS: SOURCE_CHECKED


Let's go back to the discussion about creating a tab for refactoring large files. Before you continue implementing this idea, go to the web, search in specific sites on Python and sites like Stack Overflow and Hugging Face for ideas to better implementation of this logic. How implement adequately a tab, a sub-tab, where we can refactor large files with the best performance and best logic. Bring those ideas that are really good for our project.

I will pause implementation and do this as a research/design pass. I will prioritize primary Python tooling sources, then Stack Overflow-style practical failure cases, then Hugging Face/local-model ideas that could fit your tool/project boundary.

I searched current Python tooling, Stack Overflow discussions, and Hugging Face/local-model material. My conclusion: your idea is good, but the best version is not an automatic refactor tab. It should be a Large File Refactor Planner inside Architecture Review: fast deterministic analysis first, preview-only generation second, validation third, patch creation last.
Core design I recommend

The tab should have this pipeline:

1. Select large file from Architecture Review findings
2. Analyze with AST for speed
3. Build symbol/dependency/import/global-state maps
4. Propose split plan
5. Validate import graph and public API preservation
6. Use local LLM only for ambiguous semantic grouping
7. Generate preview files in daily-work area
8. Compile and architecture-validate preview
9. Create patch ZIP only after validation

That matches the strongest evidence I found. LibCST is the best core transformation layer because it is designed for automated codemods/refactors while preserving comments, whitespace, parentheses, and formatting; AST is still good for fast analysis, but not enough for safe rewriting.
Best ideas to bring into our project
1. Use AST for scanning, LibCST for writing

The tab should use AST as the fast scanner and LibCST as the safe writer.

AST should collect:

functions
classes
constants
imports
decorators
top-level side effects
symbol references
line counts

LibCST should handle:

moving nodes
preserving comments
preserving decorators
rewriting imports
generating preview files

This avoids the weakness in the current skeleton where raw line slicing may lose decorators or import context. LibCST is explicitly positioned for codemods over large codebases, while Python’s own ast documentation frames AST as an abstract grammar tree, not a formatting-preserving rewrite engine.
2. Use graphlib.TopologicalSorter for cycle detection

Instead of writing a custom DFS cycle detector first, I would use Python’s standard graphlib.TopologicalSorter for the inter-bin dependency graph. It is built for topological ordering of dependency graphs, which is exactly what we need for “can these proposed helper modules import each other safely?”

The tab should show:

Import graph: OK
or
Cycle detected:
  helper_a -> helper_b -> helper_a
Suggested repair:
  merge helpers
  or extract shared symbols into _shared.py

This should be visible in the GUI before any patch is created.
3. Treat import rewriting as a first-class preview, not a hidden step

Stack Overflow discussions show that moving Python functions/modules and updating imports is a common pain point; PyCharm-style refactoring is valued because it shows and updates references, while other tooling often leaves gaps around automatic import-path updates.

So the tab should have a dedicated Import Migration Preview section:

Old:
from architecture_review import run_selected_mode

New:
from architecture_review_run import run_selected_mode

It should also flag risky cases:

from module import *
dynamic getattr/importlib usage
module alias used across file
relative import from script context

Python’s import docs matter here because import both searches for a module and binds names, and relative imports depend on package context. Generated refactor files must respect that, or they will compile but fail at runtime.
4. Keep imports PEP 8-compliant

Generated files should place imports after the module docstring and before globals/constants, grouped as standard library, third-party, and local application imports. This should be automatic in the generated preview.

This means the preview generator should have an import-rendering phase:

module docstring
standard library imports
third-party imports
local imports
constants
public facade
private helpers

5. Use Rope only as an optional backend, not the main engine

Rope is useful because it supports moving global classes, functions, and variables to another module. That can help for focused, well-defined moves.

But I would not make Rope the core engine. For our tab, the core should remain:

AST analysis
LibCST transformation
KANDA validation
KANDA patch workflow

Rope can be an optional “try safer IDE-like move” backend later.
6. Do not build the core on Bowler

Bowler is interesting because it was designed for safe large-scale syntax-tree refactoring and preserving formatting/comments.

But I would not choose it as the main dependency now because Bowler’s docs describe it as built on lib2to3, and Python’s own docs state lib2to3 was deprecated and removed in Python 3.13, with LibCST suggested as an alternative.

So for KANDA Reasoner: LibCST wins.
7. Local LLM should return structured JSON only

For qwen/local models, the LLM should not generate code directly in the main path. It should answer small semantic decisions:

{
  "symbol": "build_split_plan",
  "assigned_module": "_large_file_refactor_partition.py",
  "confidence": "high",
  "reason": "partitioning responsibility"
}

Hugging Face’s structured-output guidance emphasizes JSON-schema-shaped outputs for predictable, parsable AI responses, and Qwen3-Coder-30B-A3B-Instruct is available with local app / vLLM-style usage paths.

For our app, this means the LLM layer should be boxed as:

Input: symbol group + candidate modules + constraints
Output: JSON decision only
Never: direct whole-file rewrite

8. Validation must be stronger than “it compiles”

Python’s py_compile and compileall are useful baseline checks because they compile Python source files and catch syntax/import-time bytecode issues.

But the tab should validate more:

py_compile generated files
line count <= 500
no helper < 100 unless justified
public API preserved
no circular import graph
no lost decorators
no lost __all__
no lost constants
no wrong-root writes
architecture validation still passes

The LLM/refactoring literature also supports this: LLM-based refactoring remains validation-intensive and developer-guided, so the GUI should assume validation is the product, not an afterthought.
Best GUI structure for the sub-tab

I would build the tab with five panels:

1. Candidate file selector
2. Analysis evidence
3. Proposed split plan
4. Risk and validation panel
5. Patch/preview actions

The key buttons should be staged:

Analyze File
Generate Split Plan
Ask Local LLM for Ambiguous Symbols
Preview Generated Files
Validate Preview
Create Patch ZIP

I would not include an “Apply Now” button in v1.
Most important implementation rule for our project

Because of your tool/project distinction:

The refactor planner engine belongs to the KANDA Reasoner tool.
The generated split files belong to the active selected project.

So the tab must begin with a no-leak gate:

NO-LEAK CHECK

Tool-owned:
- analyzer
- planner
- LibCST writer
- LLM arbitration
- validation runner
- Architecture Review GUI tab

Project-owned:
- selected source file
- proposed split files
- generated preview
- patch payload for that selected project

Blocked:
- writing generated project split files into reusable tool source
- writing tool refactor engine code into project output
- hardcoding E:\kanda_reasoner as the target for every project

Final recommendation

The best implementation is:

Architecture Review
  -> Large File Refactor Planner
      -> proposal-first
      -> LibCST-backed
      -> graph-validated
      -> public-API preserving
      -> local-LLM-assisted only for ambiguous semantic grouping
      -> preview and validation before patch creation

The main upgrade from your original blueprint is this:

Do not make the largest bin the base module.
Make the base module a public facade/orchestrator.
Move implementation into private helper modules.

That is the most important architecture correction for KANDA Reasoner. It protects public API ownership, avoids facade/helper duplicate ownership errors, and fits your Box Logic / No-Leak Logic model.

I like very much your recommendations. Before implement, let's also insert a feature in this implementation that's the following. If any docstring is missing, also create the adequate docstring for the class or function or module. Another thing before implementing this project, subproject, go again to the web, search for the five top of the list books on this subject, Python, refactoring, improving logic, and bring to us the best suggestions of how implement this logic from these books.

I agree with adding this before implementation. The new tab should not only split large files; it should also pay documentation debt while refactoring.

The feature should be a separate stage:

Large File Refactor Planner
  -> Analyze large file
  -> Propose split
  -> Detect missing docstrings
  -> Generate docstring preview
  -> Validate generated code
  -> Create patch only after confirmation

I saved that as part of the future Large File Refactor Planner direction.
Docstring feature: how I would implement it

Docstring generation should be bounded and reviewable, not free-form.

The tab should detect missing docstrings for:

module docstring
public classes
public functions
public methods
important private helpers when complex

PEP 257 says modules should normally have docstrings and exported functions/classes should have docstrings; PEP 8 also says docstrings should be written for all public modules, functions, classes, and methods.

I would use this policy:

Public API: require docstring.
Private helper: require docstring only if complex, long, cross-box, or non-obvious.
Generated helper module: require module docstring explaining ownership and generated/refactor role.
Facade module: require docstring explaining public compatibility surface.

For style, I would choose Google-style docstrings by default because they are readable in source and supported by Sphinx Napoleon. The Google Python Style Guide says docstrings are the first statement in a package, module, class, or function and recommends triple double quotes; Sphinx Napoleon parses Google and NumPy style docstrings.

The GUI should show docstrings in the preview like this:

Missing docstring:
  run_large_file_refactor_plan

Generated proposal:
  """Build a preview-only refactor plan for a selected Python module.

  Args:
      request: User-selected refactor settings and target file metadata.

  Returns:
      A validated refactor plan with proposed module boundaries and risks.
  """

Then the user can approve, edit, or reject.
The five books I would use as design input

I would not blindly follow one book. I would combine five sources, each for a different part of the tab.
1. Refactoring, Martin Fowler

This is still the core book for the philosophy of refactoring. Fowler defines refactoring as a controlled technique for improving an existing codebase through small behavior-preserving changes.

What we should bring into KANDA:

Never treat the tab as "rewrite this file."
Treat it as "small behavior-preserving transformations."

Implementation consequence:

Every generated split must have:
- before/after public API check
- compile validation
- import graph validation
- line-count validation
- explicit preview
- explicit patch generation

The tab should show the transformation as a sequence of small moves, not one giant diff.
2. Architecture Patterns with Python, Harry Percival and Bob Gregory

This is the most relevant Python architecture book for your project. It focuses on managing application complexity with architecture patterns and using tests to get value from the architecture.

The book’s public online version says its aim is to introduce architectural patterns supporting TDD, DDD, and event-driven services, and it highlights layered architecture, abstractions, repositories, service layers, and dependency inversion.

What we should bring into KANDA:

Split by responsibility, not only by line count.

Implementation consequence:

The planner should classify symbols into responsibility layers:
- GUI/view
- orchestration/use case
- domain logic
- adapters/infrastructure
- validation
- file/path IO
- prompt/governance
- freeze/evidence

This is very important for KANDA because of tool/project boundaries. The refactor engine should not group code only by function name prefixes; it should also detect architecture responsibility.
3. Clean Code in Python, Mariano Anaya

This is directly relevant because it is Python-specific and explicitly about refactoring legacy code. The Packt/GitHub description emphasizes clean code, development tools, Python magic methods, object-oriented design, removing duplication with decorators/descriptors, refactoring with unit tests, and SOLID principles.

What we should bring into KANDA:

The tab should detect "refactor smell reasons," not just file size.

Implementation consequence:

For each large file, show why it should be refactored:
- too many public symbols
- mixed responsibilities
- duplicated helper patterns
- excessive imports
- long classes
- long functions
- hidden global state
- missing docstrings
- weak test/validation surface

This makes the tab more than a mechanical splitter. It becomes an architecture repair assistant.
4. Robust Python, Patrick Viafore

This book is useful for the validation and type-safety side. O’Reilly describes it as a book about using Python’s type system, user-defined types, type hints, extensibility, and comprehensive testing strategies to write clearer and more maintainable code.

What we should bring into KANDA:

The planner should preserve and improve type clarity.

Implementation consequence:

The refactor preview should detect:
- missing annotations
- Any-heavy public APIs
- dataclass/pydantic-like structures
- protocol/interface candidates
- functions whose docstring conflicts with type hints

I would not make type annotation generation mandatory in v1, but the tab should at least not damage type hints, and the docstring generator should use existing type hints when generating Args/Returns sections.
5. Effective Python, Brett Slatkin

The current third edition is described as 125 specific ways to write better Python and avoid hidden pitfalls; the second edition has 90 best practices with realistic code examples.

What we should bring into KANDA:

Generated helpers must stay idiomatic Python.

Implementation consequence:

The tab should avoid generating:
- over-engineered class wrappers
- unnecessary inheritance
- Java-style architecture in Python
- clever but hard-to-maintain code
- implicit side effects hidden behind imports

This supports the earlier recommendation: the base module should be a small facade, but helpers should remain simple Python modules, not a maze of abstractions.
Additional book worth borrowing from: Fluent Python

Even if we limit the “top five” to the books above, I would still borrow from Fluent Python when implementing the analyzer. O’Reilly’s page shows it covers the Python data model, sequences, dictionaries/sets, Unicode/text/bytes, and data class builders.

Practical consequence:

The analyzer must understand Pythonic constructs before judging complexity.

For example, a file may look short but contain dense dynamic behavior through decorators, descriptors, dataclasses, __getattr__, dynamic imports, or registration patterns. Those should be marked as refactor risk, not blindly moved.
Final design update from the books

I would update our implementation plan like this:

Large File Refactor Planner v1

1. Candidate discovery
   Uses Architecture Review large-module findings.

2. Responsibility analysis
   Detects GUI, orchestration, domain, adapter, validation, path/file IO, governance, freeze, and prompt logic.

3. Split proposal
   Targets facade <=400 lines, helpers <=500 lines, helpers >=100 lines.

4. Public API preservation
   Keeps facade exports stable.

5. Docstring completion
   Detects missing module/class/function/method docstrings.
   Generates reviewable Google-style docstrings.
   Uses type hints and AST signatures.
   Never silently overwrites existing docstrings.

6. Import and dependency validation
   Uses LibCST for rewrite preview.
   Uses graph validation for cycles.

7. Risk report
   Flags global state, decorators, dynamic imports, registries, hidden mutable state, tool/project leakage, and private reach-in.

8. Preview-only generation
   Writes preview to daily-work area first.

9. Validation
   py_compile, line count, public API, import graph, architecture validation, docstring check.

10. Patch creation
   Only after preview passes.

My strongest recommendation from the book review is this:

Do not let "line count" be the main architecture principle.
Use line count as a hard safety limit, but use responsibility, public API stability, dependency direction, and tests/validation as the real split logic.

And with the new docstring feature:

Every refactor should leave the code not only smaller, but more understandable.


Okay, before continuing, give me a complete, detailed handoff for Kanda Reasoner tool versus Kanda Reasoner project, so that next time I need to show you, to explain to you in another chat what is it, you can totally explain to the other AI what we are talking about, and that when we are implementing code, we are creating files, we must always remember this division. Files that are related to the project stay in the project. Files that are related to Kanda Reasoner tool remain in its own space.

Here is a complete handoff you can paste into another chat before implementation work.
HANDOFF: KANDA Reasoner Tool vs KANDA Reasoner Project Boundary
Purpose of this handoff

This handoff explains a critical boundary rule for all KANDA Reasoner work.

KANDA Reasoner has two identities that must never be confused:

    KANDA Reasoner as the tool

    KANDA Reasoner as the active project currently being edited

Sometimes we are working on KANDA Reasoner itself. In that situation, the same repository may appear to be both the tool and the project. Even then, the AI must preserve the distinction between tool-owned logic and project-owned source/output.

This distinction is mandatory before editing code, creating files, generating patches, writing validation scripts, refactoring modules, or producing freeze/handoff artifacts.
1. KANDA Reasoner as the tool

KANDA Reasoner as the tool is the reusable system that helps build, inspect, refactor, validate, patch, document, and maintain code projects.

Tool-owned files are reusable application logic. They belong to the KANDA Reasoner tool/runtime, not to the selected project output.

Examples of tool-owned logic:

    Architecture Review GUI tabs

    Large File Refactor Planner GUI

    large-module analyzers

    AST or LibCST refactor engines

    code analyzers

    import rewriters

    docstring insertion engines

    prompt routers

    validation generators

    patch creation tools

    freeze-prep tools

    handoff generators

    Error Memory tools

    startup delivery generators

    project collectors

    path resolvers

    no-leak validators

    box/shielding validators

In short:

If the code performs reusable work on projects, it belongs to the KANDA Reasoner tool.

Example:

A module that analyzes a selected Python file and proposes a safe split into helper modules is tool-owned.

A module that inserts missing docstrings into selected source files is tool-owned.

A GUI tab that lets the user preview a refactor plan is tool-owned.

A validator that checks whether the proposed split preserves public API and avoids circular imports is tool-owned.
2. KANDA Reasoner as the project

KANDA Reasoner as the project is the active selected codebase being edited. In many sessions, the selected project is KANDA Reasoner itself, but it must still be treated as a project target when the task is modifying its project source.

Project-owned files are the actual source files, generated output files, helper files, reports, previews, freeze records, or validation artifacts that belong to the active project being worked on.

Examples of project-owned files:

    selected source file being refactored

    split/refactored modules produced for that selected project

    project-specific helper modules generated as the result of a refactor

    project-specific validation evidence

    project-specific freeze hints

    project-specific handoff output

    project-specific Error Memory intake

    project-specific preview files

    project-specific generated documentation

    project-specific temporary work output

In short:

If the file is the result or target of work on a selected project, it belongs to the active project.

Example:

If the tool refactors large_module.py from the active project into:

    large_module.py

    _large_module_analysis.py

    _large_module_validation.py

    _large_module_io.py

those output files belong to the active project, not to the reusable tool layer.
3. The key distinction

The same repository can contain tool logic and project source, especially when the active project is KANDA Reasoner itself.

Therefore, the AI must not decide ownership only by repository path or project name.

The AI must classify by responsibility.
Tool-owned

A file is tool-owned when it implements reusable machinery that can operate on any project.

Examples:

    refactor planner engine

    refactor planner GUI

    docstring generator engine

    import migration engine

    AST/CST symbol analyzer

    architecture validator

    patch builder

    startup delivery generator

Project-owned

A file is project-owned when it is the selected project source or a generated result for that selected project.

Examples:

    the actual module being split

    the generated split helper files

    project-specific preview output

    project-specific patch payload

    project-specific validation evidence

    project-specific freeze hint

4. Concrete example: Large File Refactor Planner

We are planning a new Architecture Review sub-tab for refactoring large Python files.

This feature must follow the tool/project boundary.
Tool side

These belong to KANDA Reasoner as the reusable tool:

    the Architecture Review sub-tab UI

    the Large File Refactor Planner controller

    AST analysis code

    LibCST transformation code

    import rewrite engine

    dependency graph builder

    circular import validator

    docstring detection/generation engine

    local LLM arbitration wrapper

    preview generator

    validation runner

    patch ZIP builder

    no-leak gate

Project side

These belong to the active selected project:

    the selected large source file

    generated split/refactored source files

    generated project helper files

    generated docstrings inserted into project code

    refactor preview files

    patch payload files for that project

    validation evidence for that project

    freeze hint for that project

Critical rule

The refactor engine belongs to the tool.

The refactored output belongs to the project.

Do not put reusable refactor-engine code inside project output.

Do not put project-specific split files inside reusable tool source unless the selected project source itself is being intentionally patched.
5. Box Logic, Shielding Logic, and No-Leak Logic

The AI must use three related safety concepts before implementation.
Box Logic

Box Logic asks:

    What box owns this file?

    What is the active box?

    What are the owner paths?

    Which files are allowed?

    Which files are out of scope?

    Are there cross-box touches?

    What public contracts are involved?

    What validation scope is needed?

    What boundary risks exist?

Shielding Logic

Shielding Logic protects each box from accidental invasion.

It prevents:

    editing neighboring boxes without routing

    importing private internals from another box

    mixing UI logic with domain logic

    mixing validation logic with runtime logic

    changing generated artifacts instead of source truth

    bypassing public contracts

    bypassing confirmation gates

No-Leak Logic

No-Leak Logic is a named first-class object inside Box Logic and Shielding Logic.

Use the name:

NO_LEAK_LOGIC_V1

No-Leak Logic prevents ownership, path, state, contract, evidence, and responsibility from leaking across boxes.

It specifically blocks:

    tool/project leakage

    wrong-root writes

    cross-box leakage

    private reach-in

    public API ownership leakage

    hidden mutable state leakage

    generated-artifact-as-source leakage

    validation/freeze evidence leakage

    prompt/canon leakage

    refactor-output leakage

6. Required NO-LEAK CHECK before coding

Before any implementation, refactor, patch, validation script, generated file, startup update, or freeze-ready work, the AI should output or internally complete this check:

NO-LEAK CHECK

Active box:
Tool-owned files:
Project-owned files:
Project-specific support files:
Generated/evidence files:
Temporary daily-work files:
External boxes touched:
Out-of-scope files:
Leak risks:
Blocked writes:
Safe next action:

If any answer is uncertain, do not patch from memory. Inspect the actual source, routing manifest, prompt, path resolver, or validation context.
7. Required BOX CHECK before implementation

Before implementation, the AI should also complete:

BOX CHECK

Task type:
Active box:
Owner path:
Allowed files:
Out-of-scope files:
Cross-box touches:
Public contracts:
Validation scope:
Boundary risks:
Tool/project ownership risk:
No-leak risk:
May proceed:
Next safe action:

If the task changes architecture, startup delivery, prompt-library canons, freeze behavior, patch delivery, validation behavior, GUI behavior, or project/tool path ownership, treat it as governed work.
8. Wrong patterns to avoid
Wrong pattern 1: Treating KANDA Reasoner as always the project

Bad:

All generated files go under E:\kanda_reasoner because the tool is KANDA Reasoner.

Correct:

Generated project files go under the selected active project root.
Reusable tool logic goes under the KANDA Reasoner tool source.

Wrong pattern 2: Treating generated output as source truth

Bad:

Modify generated startup ZIP contents directly as if they are canonical source.

Correct:

Modify canonical prompt/source files and regenerate generated delivery artifacts.

Wrong pattern 3: Putting reusable refactor logic into project output

Bad:

Generated split project helper files include the reusable refactor planner engine.

Correct:

The refactor planner remains tool-owned. The project receives only the selected project's refactored source output.

Wrong pattern 4: Hardcoding KANDA Reasoner as every target project

Bad:

Write support files to E:\kanda_reasoner_show_project_to_AI for every project.

Correct:

Use the selected active project root and derive:
<project_drive>\<active_project_slug>_show_project_to_AI
<project_drive>\<active_project_slug>_delete_after_daily_work

Wrong pattern 5: Letting helper modules accidentally own facade API

Bad:

A private helper module exports the same public symbol as the facade.

Correct:

The facade owns public compatibility. Helpers stay private unless a governed architecture change says otherwise.

9. File ownership rules for refactoring work

When implementing a refactor feature, classify every file.
Reusable refactor system files

These are tool-owned:

large_file_refactor_planner.py
_large_file_refactor_analysis.py
_large_file_refactor_partition.py
_large_file_refactor_imports.py
_large_file_refactor_validation.py
_large_file_refactor_docstrings.py
_large_file_refactor_llm.py
architecture_review_large_file_refactor_tab.py
validation/test_large_file_refactor_planner_v1.py

Refactored project output files

These are project-owned:

selected_module.py
_selected_module_analysis.py
_selected_module_imports.py
_selected_module_validation.py
_selected_module_docstrings.py

Only generate these under the active selected project path or its preview/daily-work area.
10. Special rule when KANDA Reasoner is both tool and project

When the active selected project is KANDA Reasoner itself, the AI must be extra careful.

The same physical repository may contain:

    tool code being enhanced

    project code being refactored

    generated support files

    temporary daily-work files

    freeze/handoff evidence

Do not assume everything in the repository has the same ownership.

Classify by responsibility:

Is this reusable system machinery?
Then it is tool-owned.

Is this the selected source being changed or generated output for that source?
Then it is project-owned.

Is this freeze, validation, handoff, or preview state?
Then it is project-specific support/evidence.

Is this temporary installation or patch staging material?
Then it belongs in _delete_after_daily_work.

11. Startup and retrieval guidance for future chats

At the beginning of future chats, after loading startup files, the AI should look for or request these concepts if needed:

    Box Logic Startup Bridge

    No-Leak Logic Bridge

    box_architecture_canon.md

    kanda_box_shielding_canon.md

    project_tool_boundary_canon.md

    patch delivery guardrails

    active project freeze context

    compact Error Memory

    project handoff routing manifest

    source archive only when exact source inspection is needed

If the user asks to implement or patch code, the AI must not rely only on this handoff. It must inspect the actual source files first.

This handoff defines the rule. Source files define the implementation truth.
12. How this applies to the planned Large File Refactor Planner

The planned feature is:

Architecture Review
  -> Large File Refactor Planner

The safest design is:

1. proposal-first
2. preview-only before write
3. LibCST-backed for formatting-preserving edits
4. AST-backed for fast analysis
5. dependency-graph validated
6. public API preserving
7. docstring completion included
8. local LLM only for bounded semantic decisions
9. no direct auto-apply in v1
10. patch ZIP only after validation

The planner should include a Docstring Completion stage.

It should detect missing docstrings for:

    modules

    public classes

    public functions

    public methods

    complex private helpers when needed

It should propose docstrings in preview and never silently overwrite existing docstrings.

The generated docstrings belong to the selected project source because they are inserted into project code.

The docstring generation engine belongs to the KANDA Reasoner tool.
13. Final compact rule

Use this sentence as the shortest version:

KANDA Reasoner as a tool owns reusable machinery; the active project owns selected source files and generated project outputs. Even when the active project is KANDA Reasoner itself, every file must be classified by responsibility before writing. Apply Box Logic, Shielding Logic, and NO_LEAK_LOGIC_V1 to prevent tool/project leakage, wrong-root writes, cross-box leakage, private reach-in, public API leakage, generated-artifact leakage, and validation/freeze evidence leakage.

I would paste this in the next chat right after the startup/project-ready checks and before asking for implementation.

Okay, now give me the complete implementation of subtab refactoring large modules. This sub-tab will be in architecture review tab. I need a complete explanation for AI understand what we are about to do and how to do it with the best performance.

I will make this as an implementation handoff/specification, not a patch yet: clear enough for a future AI to implement after source inspection, with box/no-leak boundaries, GUI behavior, engine modules, validation, and performance rules.

I grounded this implementation spec in official/current sources for the core technical choices: Python ast for syntax-tree analysis, LibCST codemods for large-scale refactoring, graphlib.TopologicalSorter for dependency ordering/cycle validation, PEP 257 for docstring policy, and py_compile for compile validation.

Here is the complete handoff/specification for the implementation.
IMPLEMENTATION HANDOFF: Architecture Review Sub-Tab for Large File Refactoring
Feature name

Architecture Review -> Large File Refactor Planner

Internal feature id suggestion:

architecture-review-large-file-refactor-planner-v1

Purpose

Create a new sub-tab inside the existing Architecture Review tab.

The sub-tab helps refactor large Python modules into smaller, maintainable modules while preserving behavior, public API, imports, docstrings, validation evidence, and KANDA Reasoner box boundaries.

This must not be an automatic destructive refactor button.

It must be a proposal-first, preview-first, validation-first workflow.

The user should be able to:

    select a large Python file detected by Architecture Review;

    analyze its symbols, dependencies, imports, globals, and docstrings;

    generate a split plan targeting ideal 400 lines and maximum 500 lines per module;

    avoid tiny helper files below 100 lines unless justified;

    preserve the original public facade;

    generate missing docstrings during preview;

    detect circular imports and public API risks;

    preview all generated files before writing;

    validate the preview;

    create an installable patch only after validation and confirmation.

Core design principle

Do not split only by line count.

Line count is a safety limit.

The real split logic must be based on:

    responsibility;

    public API preservation;

    import direction;

    dependency graph;

    global-state safety;

    docstring/documentation quality;

    box/no-leak ownership;

    validation evidence.

Mandatory tool/project boundary

KANDA Reasoner has two identities:

    KANDA Reasoner as the reusable tool;

    KANDA Reasoner as the active project currently being edited.

The Large File Refactor Planner itself is tool-owned.

The concrete refactored files produced for a selected project are project-owned.
Tool-owned files

The following belong to the KANDA Reasoner tool/runtime:

Architecture Review GUI sub-tab
large file refactor planner controller
AST analyzer
LibCST writer
dependency graph builder
import rewriter
docstring detector/generator
local LLM arbitration wrapper
preview generator
validation runner
patch creator
No-Leak gate

Project-owned files

The following belong to the active selected project:

selected source file being refactored
generated split files
project-specific helper files
generated docstrings inserted into project code
preview output for that project
patch payload for that project
validation evidence for that project
freeze hint for that project

Critical no-leak rule

Refactor engine code belongs to the tool.

Refactor output belongs to the project.

Do not write reusable refactor engine code into project output.

Do not write project-specific split files into reusable tool source unless the selected project source itself is being intentionally patched.
Required beginning-of-task checks

Before implementation, the AI must perform:

BOX CHECK

Task type:
Active box:
Owner path:
Allowed files:
Out-of-scope files:
Cross-box touches:
Public contracts:
Validation scope:
Boundary risks:
Tool/project ownership risk:
No-leak risk:
May proceed:
Next safe action:

And:

NO-LEAK CHECK

Active box:
Tool-owned files:
Project-owned files:
Project-specific support files:
Generated/evidence files:
Temporary daily-work files:
External boxes touched:
Out-of-scope files:
Leak risks:
Blocked writes:
Safe next action:

If uncertain, inspect source files and prompt canons before patching.

Do not implement from memory.
Required prompt/canon context before implementation

Before coding, load or apply the specific relevant prompt/library context:

04_box_architecture_and_boundaries
box_architecture_canon.md
kanda_box_shielding_canon.md
project_tool_boundary_canon.md
NO_LEAK_LOGIC_V1 / No-Leak Logic Bridge
05_patch_delivery_and_validation
07_daily_patch_delivery_guardrails
08_python_engineering_core
09_python_quality_security_observability
09_active_project_freeze_context
large_module_refactor_protocol, if present
pre_output_contract_gates before patch/PowerShell output
freeze_code_intake_and_form_protocol if feature is freeze-ready

Also load compact Error Memory before code changes.

Open full Error Memory only if compact lessons indicate a relevant repeated error or the task conflicts with a prior lesson.
New sub-tab placement

Add this as a new sub-tab inside Architecture Review.

Existing local sub-tabs include:

Run Selected Mode
Large Module AST Split Audit

Add:

Large File Refactor Planner

Recommended UI order:

Run Selected Mode
Large Module AST Split Audit
Large File Refactor Planner

The sub-tab should reuse existing Architecture Review results where possible.

It should not duplicate the whole Architecture Review scanner.
GUI layout

The sub-tab should have five sections.
Section 1: Candidate file selector

Purpose: choose the file to analyze.

Inputs:

candidate file dropdown/list
manual file path input, if existing app pattern supports it
refresh candidates button
line limit settings

Candidate source:

Architecture Review large-module findings
Large Module AST Split Audit output
manual selected file fallback

Candidate table columns:

File
Current lines
Public functions
Public classes
Total symbols
Imports
Global-state risks
Docstring missing count
Architecture warnings
Suggested action

Suggested actions:

Analyze
Already compliant
Needs source inspection
Blocked: global state
Blocked: generated artifact
Blocked: wrong box
Blocked: not Python source

Section 2: Refactor settings

Default values:

Ideal file size: 400 lines
Maximum file size: 500 physical lines
Minimum helper size: 100 physical lines
Preserve public facade: ON
Generate missing docstrings: ON
Rewrite project imports: OFF in v1, preview only
Use local LLM: OFF by default or ON if configured
Preview only: ON
Create patch only after validation: ON

Do not provide an "Apply now" button in v1.

Allowed buttons:

Analyze File
Generate Split Plan
Ask Local LLM for Ambiguous Symbols
Generate Preview
Validate Preview
Create Patch ZIP
Open Preview Folder
Copy Summary

Section 3: Analysis evidence

After analysis, show:

module docstring present/missing
public API symbols
top-level functions
top-level classes
constants
imports
relative imports
decorators
global state
module-level side effects
dynamic imports
__all__
if __name__ == "__main__"
symbol dependency graph summary
line count per symbol
docstring missing count

Risk badges:

GLOBAL_STATE
DYNAMIC_IMPORT
STAR_IMPORT
PUBLIC_API_RISK
DECORATOR_RISK
CIRCULAR_IMPORT_RISK
PRIVATE_REACH_IN_RISK
NO_LEAK_RISK
MISSING_DOCSTRING
TOO_LARGE
TOO_SMALL

Section 4: Proposed split plan

Show proposed output modules.

Each proposed module row:

Output filename
Role
Estimated lines
Physical preview lines, after generation
Symbols included
Imports needed
Docstrings generated
Risks
Status

Roles:

public_facade
analysis_helper
partition_helper
import_helper
docstring_helper
validation_helper
io_helper
gui_helper
llm_helper
shared_helper
domain_helper
adapter_helper

The base module must usually be the public facade/orchestrator, not the largest bin.

Wrong:

largest bin becomes the base module

Correct:

base module preserves public API and orchestration
implementation moves to private helper modules

Section 5: Preview, validation, and patch

This section should show the stage status:

Analysis: not run / ok / warning / blocked
Plan: not generated / ok / warning / blocked
Docstrings: not generated / ok / warning / blocked
Preview: not generated / ok / warning / blocked
Validation: not run / passed / failed
Patch: not created / ready / blocked

Validation output should be visible and copyable.

Patch creation is blocked unless validation passes.
Workflow
Stage 1: Candidate discovery

Input:

active project root
Architecture Review findings
optional manual file selection

Output:

LargeFileCandidate list

Candidate eligibility:

file is .py
file is active project source
file is not generated preview/evidence
file is not under _delete_after_daily_work unless explicitly preview
file is not startup delivery artifact unless task is startup maintenance
file is not prompt generated ZIP content
file has physical line count > threshold

Default threshold:

> 500 physical lines

Stage 2: Fast AST analysis

Use Python ast for fast structural analysis. The official ast module is designed to process Python abstract syntax grammar trees, which makes it appropriate for symbol and dependency extraction.

Collect:

module docstring
top-level classes
top-level functions
async functions
constants
assignments
imports
ImportFrom
__all__
decorators
type annotations
global statements
nonlocal statements
module-level expressions
module-level calls
if __name__ == "__main__" blocks
line spans
end line spans
symbol references

Do not use AST for final rewriting, because AST does not preserve comments and formatting.
Stage 3: CST parse for rewrite readiness

Use LibCST for formatting-preserving preview generation and future codemods. LibCST codemods are designed for automated refactors across codebases, and LibCST is the correct layer for preserving comments, whitespace, and concrete syntax during source transformations.

CST parse should be lazy:

Run AST first.
Only parse with LibCST when generating preview or validating exact node movement.
Cache parsed CST by file path + content hash.

Stage 4: Symbol model

Create an internal data model similar to:

SymbolInfo
  name
  kind
  visibility
  start_line
  end_line
  physical_lines
  decorators
  args_signature
  returns_annotation
  has_docstring
  docstring_text
  references
  imported_names_used
  global_names_used
  assigns_global_state
  class_methods
  parent_class
  risk_flags

Visibility rules:

public if not starting with "_"
private if starting with "_"
dunder if __name__
public if exported by __all__
facade-critical if imported elsewhere or in public contract

Stage 5: Import model

Create:

ImportInfo
  original_node
  module
  imported_name
  alias
  is_relative
  is_star
  line_span
  used_by_symbols
  risk_flags

Import risks:

star import
dynamic import
relative import ambiguity
try/except import fallback
conditional import
platform-specific import
import side effect risk

Stage 6: Global state and side-effect analysis

Flag but do not automatically move:

logging.basicConfig
environment reads
path setup
registry setup
global mutable containers
cache initialization
Tkinter or GUI initialization
thread/process startup
network/file/database side effects
plugin registration
monkeypatching
import-time execution

Global state policy:

Default: keep in public facade or original module.
Move only if clearly pure or explicitly approved.

Stage 7: Dependency graph

Build a symbol dependency graph:

node = symbol
edge A -> B when A references/calls/uses B

Then build a proposed module graph:

node = proposed output module
edge module A -> module B when symbols in A require symbols in B

Use graph validation before writing files.

Python graphlib.TopologicalSorter is appropriate for checking whether proposed module dependencies can be ordered as a DAG; it provides topological sorting for graph-like structures.

If cycle exists:

helper_a -> helper_b -> helper_a

Then block preview or repair plan:

Option 1: merge bins
Option 2: extract shared symbols into _shared.py
Option 3: keep problematic symbols in facade
Option 4: ask local LLM for semantic regrouping

Stage 8: Responsibility classification

Classify each symbol into likely responsibility:

gui
controller
orchestration
domain
validation
path_io
file_io
serialization
import_handling
docstring_handling
prompt_handling
freeze_handling
patch_delivery
architecture_review
error_memory
startup_delivery
llm_integration
test_validation
unknown

Heuristics:

name prefixes
imports used
called functions
class names
module-level comments/docstrings
Architecture Review owner box
folder path
existing neighboring modules

Do not use only name prefixes.
Stage 9: Split planning

Targets:

ideal: around 400 physical lines
maximum: 500 physical lines
minimum helper: 100 physical lines

Planning rules:

    Keep public facade stable.

    Keep global side effects in facade unless safe to move.

    Group by responsibility first.

    Preserve strongly connected symbol groups.

    Do not split class methods into separate files.

    Do not separate decorators from decorated functions/classes.

    Do not create helpers below 100 lines unless clearly justified.

    Do not exceed 500 physical lines after preview generation.

    Prefer private helper modules for implementation details.

    Generate a shared helper only when it reduces circular dependency risk.

Facade policy:

The original module should usually remain as a public facade.
It should import/re-export moved symbols when needed.
It should preserve __all__ when present.
It should preserve public compatibility.

Stage 10: Local LLM arbitration

Use local LLM only for bounded decisions.

Do not ask the LLM to rewrite a whole file.

Allowed LLM tasks:

assign ambiguous symbol to one proposed module
suggest semantic filename for helper module
draft missing docstring from signature/body summary
explain a dependency cycle
suggest merge vs shared-helper decision

Forbidden LLM tasks in v1:

rewrite entire module
move code without deterministic validation
create patch directly
decide tool/project ownership without source inspection
bypass no-leak checks

LLM output must be JSON only.

Example schema for ambiguous symbol:

{
  "symbol": "build_split_plan",
  "recommended_module": "_large_file_refactor_partition.py",
  "confidence": "high",
  "reason": "The symbol groups partitioning rules and size constraints."
}

Example schema for docstring proposal:

{
  "symbol": "build_split_plan",
  "docstring_style": "google",
  "docstring": "Build a preview-only split plan for a Python module.\n\nArgs:\n    request: Refactor settings and target module metadata.\n\nReturns:\n    A split plan with proposed modules, symbol ownership, and risk flags."
}

Cache LLM decisions by:

file content hash
symbol name
symbol line span
symbol body hash
candidate module list hash

Stage 11: Docstring completion

The tab must include a docstring completion stage.

Policy should follow Python docstring conventions. PEP 257 says module docstrings should list exported classes, exceptions, functions, and other objects with summaries, and it defines conventions for docstrings.

Detect missing docstrings for:

module
public classes
public functions
public methods
complex private helpers
generated helper modules
facade modules

Do not overwrite existing docstrings by default.

Docstring style:

Google-style docstrings
Triple double quotes
Summary first
Blank line before Args/Returns/Raises when present
Use existing type hints
Use signature information
Keep concise
No speculation
No fake behavior claims

Docstring generator priority:

1. deterministic template from name/signature/return annotation
2. local LLM proposal for complex bodies
3. user review in preview

Example deterministic class docstring:

"""Coordinate large-file refactor planning for one selected module."""

Example deterministic function docstring:

"""Build a split plan from analyzed symbols and dependency edges.

Args:
    symbols: Analyzed symbol records from the selected module.
    settings: User-selected file-size and safety settings.

Returns:
    A refactor plan containing proposed modules, risks, and validation blockers.
"""

Docstring validation:

module docstring exists in generated modules
public class/function/method docstrings exist or justified
existing docstrings preserved
no generated docstring changes runtime behavior
line count after docstrings still <= 500

Docstring insertion must use LibCST or equivalent formatting-preserving transformation.
Stage 12: Preview generation

Preview output must not write directly into the active source tree.

Preview location should be under the active project's daily-work area:

<project_drive>\<active_project_slug>_delete_after_daily_work\large_file_refactor_preview\<feature_id>\

Preview should include:

proposed generated modules
refactor_plan.json
symbol_map.json
import_migration_preview.json
docstring_proposals.json
risk_report.json
validation_report.json
README_PREVIEW.txt

Preview generated files must be clearly marked as preview, not source truth.

Generated preview files should preserve:

license/header if present
module docstring or proposed module docstring
imports
comments
decorators
type annotations
__all__
public API facade
function/class bodies

Stage 13: Import rewriting preview

Do not silently rewrite project-wide imports in v1.

Instead produce an import migration preview.

Detect:

from old_module import symbol
import old_module
old_module.symbol
from old_module import *
relative import references
aliases

Risk cases:

star import
dynamic importlib
getattr(module, name)
string-based imports
plugin discovery
conditional imports

In v1, the patch may update imports only if the migration is deterministic and validated.

Otherwise, show a warning and require manual approval.
Stage 14: Validation

Validation is mandatory before patch creation.

Use at least:

py_compile generated preview files
line count validation
minimum helper line validation
public API preservation validation
symbol preservation validation
docstring validation
import graph cycle validation
no lost decorators validation
__all__ preservation validation
no wrong-root writes validation
no generated-artifact-as-source validation
Architecture Review validation, if available

Python py_compile provides source compilation behavior and is suitable as a baseline syntax validation step.

Validation must check actual physical files after preview generation, not only estimated symbol lines.

Expected success marker:

VALIDATION OK: architecture-review-large-file-refactor-planner-v1
STATUS: IN_SYNC

If ZIP patch is created:

ZIP CONTRACT: PASS

Stage 15: Patch creation

Patch creation is allowed only after validation passes.

Patch contents:

changed tool files
validation script
metadata/manifest
KANDA_FREEZE_HINT.json if freezeable
no project preview outputs unless intentionally part of source patch

If the patch implements the tool feature, patch files belong to the KANDA Reasoner tool source.

If the patch applies a generated split to a selected project, patch files belong to that selected project's source tree.

Do not mix the two without clear feature separation.
Recommended implementation modules

Exact paths must be determined by source inspection.

Suggested tool-owned module grouping:

kanda_reasoner_app/<architecture_review_package>/large_file_refactor/
    __init__.py
    controller.py
    models.py
    candidate_discovery.py
    ast_analyzer.py
    cst_rewriter.py
    dependency_graph.py
    split_planner.py
    docstring_planner.py
    import_migration.py
    validation.py
    preview_writer.py
    llm_arbitration.py
    no_leak_gate.py
    gui_tab.py

If the existing Architecture Review package uses a different structure, adapt to it.

Do not create a new unrelated architecture island.

Prefer small modules under 400 lines and never above 500 physical lines.
Data contracts
LargeFileRefactorSettings

ideal_lines: int
max_lines: int
min_helper_lines: int
preserve_public_facade: bool
generate_docstrings: bool
use_local_llm: bool
preview_only: bool
rewrite_imports: bool
active_project_root: Path
tool_root: Path
target_file: Path

LargeFileCandidate

path
relative_path
line_count
public_symbol_count
class_count
function_count
missing_docstring_count
risk_flags
source_box
is_eligible
blocked_reason

RefactorSymbol

name
kind
visibility
start_line
end_line
physical_lines
decorators
signature
return_annotation
has_docstring
docstring
references
imports_used
globals_used
risk_flags
assigned_module

ProposedModule

filename
role
symbols
estimated_lines
preview_lines
imports
exports
docstrings_generated
risk_flags
status

RefactorPlan

feature_id
target_file
settings
public_api_before
public_api_after
symbols
proposed_modules
import_migration
docstring_proposals
risks
validation_blockers
status

ValidationReport

feature_id
line_count_ok
compile_ok
docstrings_ok
public_api_ok
symbol_preservation_ok
import_graph_ok
no_leak_ok
architecture_ok
errors
warnings
success_markers

GUI state machine

Use explicit state transitions:

IDLE
CANDIDATE_SELECTED
ANALYZED
PLAN_READY
LLM_REVIEW_READY
PREVIEW_READY
VALIDATION_PASSED
VALIDATION_FAILED
PATCH_READY
BLOCKED

Blocked states must show why.

Do not allow patch creation from:

IDLE
CANDIDATE_SELECTED
ANALYZED
PLAN_READY
PREVIEW_READY without validation
VALIDATION_FAILED
BLOCKED

Performance strategy

Use a staged performance model.
Fast path

Run these quickly:

line counting
AST parse
symbol extraction
docstring detection
basic import extraction
basic risk detection

Lazy heavy path

Run only when needed:

LibCST parse
project-wide import scan
LLM arbitration
preview file generation
full validation
architecture validation

Caching

Cache by:

file path
file size
mtime
content hash
AST hash
CST hash
symbol body hash
settings hash

Avoid expensive operations

Do not parse the whole project unless import migration preview is requested.

For project-wide import search:

first use text search for old module name
only parse matching files with LibCST
skip generated/evidence/daily-work folders unless explicitly selected

LLM performance

Keep LLM calls small.

Batch only related ambiguous symbols.

Never send full 3500-line files to the LLM.

Send:

symbol name
signature
docstring if any
short body summary
references
candidate module summaries
risk flags

Use JSON output only.
GUI responsiveness

Follow the existing GUI worker pattern.

Do not freeze the UI during analysis or validation.

Show progress by stage:

Analyzing AST...
Building dependency graph...
Planning split...
Checking docstrings...
Generating preview...
Validating...

Safety and error handling

Every stage must return a structured result.

No stage should crash the whole GUI.

Error types:

SourceReadError
AstParseError
CstParseError
UnsupportedPythonSyntaxError
NoLeakViolation
PublicApiMismatch
CircularImportRisk
DocstringGenerationError
PreviewWriteError
ValidationError
PatchCreationBlocked

For each error, show:

what failed
why it matters
safe next action
whether user can continue

Validation script requirements

Add a focused validation script for the tool feature.

Suggested name:

validation/test_architecture_review_large_file_refactor_planner_v1.py

It should validate:

new sub-tab is registered
tool/project boundary text exists
NO_LEAK gate exists
settings defaults are correct
planner targets 400/500/100 line rules
facade preservation rule exists
docstring stage exists
LibCST/CST writer module exists or is explicitly optional
dependency graph validation exists
preview-only default exists
patch creation is validation-gated
all new/touched modules <= 500 physical lines
py_compile passes for changed Python files

Expected output:

VALIDATION OK: architecture-review-large-file-refactor-planner-v1
STATUS: IN_SYNC

Implementation phases
Phase 1: GUI shell and data model

Goal:

Add the sub-tab, settings, state machine, and empty result panels.

No refactor generation yet.

Validation:

sub-tab appears
settings defaults correct
no-leak text present
no write actions enabled

Phase 2: Analyzer

Goal:

Analyze one selected file with AST and show symbols, line counts, imports, docstrings, global state, and risks.

Validation:

AST parse works
candidate file analysis works
missing docstrings detected
global-state risks flagged
no writes performed

Phase 3: Split planner

Goal:

Generate a proposed split plan with facade preservation and line constraints.

Validation:

no helper below 100 unless justified
no proposed module above 500 estimated lines
facade role exists
symbol map complete

Phase 4: Docstring planner

Goal:

Generate reviewable docstring proposals for missing module/class/function/method docstrings.

Validation:

existing docstrings preserved
missing docstrings proposed
docstrings use signatures/type hints
line counts recalculated

Phase 5: Preview generator

Goal:

Generate preview files under active project daily-work preview folder.

Validation:

preview path uses active project root
no tool/project leakage
generated files compile
source tree not modified

Phase 6: Import graph and public API validation

Goal:

Validate import graph, public API preservation, __all__, decorators, and symbol preservation.

Validation:

cycle detection works
public API mismatch blocks patch
lost decorator blocks patch

Phase 7: Patch creator

Goal:

Create patch ZIP after preview validation passes.

Validation:

ZIP contract passes
changed files only
KANDA_FREEZE_HINT.json included if freezeable
install and validation commands follow patch delivery guardrails

Acceptance criteria

The feature is accepted when:

1. Architecture Review contains Large File Refactor Planner sub-tab.
2. The sub-tab can analyze a selected large Python file.
3. It shows symbols, imports, dependencies, globals, and missing docstrings.
4. It proposes split modules with ideal 400, maximum 500, minimum 100 line policy.
5. It preserves the original module as public facade when appropriate.
6. It proposes missing docstrings without overwriting existing docstrings.
7. It generates preview files only in the active project's daily-work preview area.
8. It validates preview files before patch creation.
9. It blocks circular import plans.
10. It blocks public API mismatches.
11. It blocks wrong-root writes and tool/project leakage.
12. It creates patch ZIP only after validation.
13. All new/touched source modules remain <=500 physical lines.
14. Focused validation prints:
    VALIDATION OK: architecture-review-large-file-refactor-planner-v1
    STATUS: IN_SYNC
15. Patch ZIP contract prints:
    ZIP CONTRACT: PASS

Explicit non-goals for v1

Do not implement these in v1:

fully automatic apply without preview
whole-project automatic refactor
LLM rewriting entire modules
unvalidated project-wide import rewrites
automatic moving of global side effects
automatic split of class methods across files
automatic rewrite of generated startup artifacts

Best final implementation summary

Build the feature as a planner, not a magic refactor button.

The tab should answer:

What file is too large?
Why is it too large?
What responsibilities are mixed?
What safe split is proposed?
What docstrings are missing?
What imports/public API might break?
What validation proves the preview is safe?
What patch should be created only after confirmation?

The feature succeeds when it makes large-file refactoring safer, more understandable, and more reviewable while respecting KANDA Reasoner tool/project boundaries, Box Logic, Shielding Logic, and NO_LEAK_LOGIC_V1.

This is the specification I would give to the next AI before code implementation. It is intentionally strict because this feature touches GUI, source transformation, validation, patch delivery, docstrings, local LLM behavior, and tool/project ownership at the same time.

Pasted text.txt
Document
auditi these modification suggestions to give fina handoff.  Overall this is a strong, disciplined spec — the preview-first/validation-gated posture and the explicit tool/project ownership split are the right instincts for something this destructive-by-nature. Here's where I'd push back or tighten it.
What's solid, don't touch

AST for fast analysis, LibCST for rewrite — correct division of labor, and you called out why (AST loses formatting) instead of just asserting it.
Patch gated strictly behind validation, with explicit blocked-state list for the GUI — good, no ambiguity about when "Create Patch ZIP" is allowed.
Non-goals section. Most specs skip this and it's exactly what prevents scope creep mid-implementation.
LLM confined to bounded, JSON-only, cacheable micro-decisions rather than "rewrite this file" — correct way to keep a local model in the loop without letting it own correctness.

Real gaps / risks I'd fix before Phase 1
1. The core principle contradicts the hard limits.
"Do not split only by line count" is stated, then every planning rule is a line-count number (400/500/100). That's fine as a constraint, but there's no tie-break rule for when responsibility-based grouping produces a cohesive block that's, say, 650 lines. Right now the planner has no defined behavior for that case. Add an explicit rule: if a responsibility group exceeds max_lines, sub-partition by secondary responsibility (not by raw line cut), and if it still can't fit, flag TOO_LARGE_COHESIVE_GROUP and block auto-planning for that group rather than silently violating the cap.
2. No policy for an oversized single class.
"Do not split class methods into separate files" is right, but what happens when one class alone is 700 lines? Silence here means the planner will either violate the 500-line cap or crash on an edge case you didn't design for. Needs an explicit TOO_LARGE_CLASS risk flag that routes to manual review, not automatic handling.
3. Facade re-export risk isn't addressed.
The public-facade-as-re-exporter pattern (from ._helper import symbol) can reintroduce the exact circular-import risk you're trying to detect, because it forces eager imports of every helper at facade import time — even ones the caller never uses. Worth adding a lazy-export option (__getattr__-based lazy facade, PEP 562 style) as a fallback when eager re-export would create a cycle, rather than only offering "merge bins / shared helper / keep in facade."
4. Docstring generator has no confidence signal.
"No speculation, no fake behavior claims" is the right instinct, but a signature-only deterministic docstring for a function with non-obvious side effects is a soft speculation risk even without literally inventing behavior. I'd tag every generated docstring with its provenance (deterministic / llm-drafted / low-confidence-needs-review) so the human reviewer in preview knows which ones to actually read carefully instead of treating them all as equally trustworthy.
5. LLM output isn't validated, only cached.
You cache by content hash — good — but nothing checks that recommended_module in the JSON actually exists in the candidate module list, or that confidence is a real enum value, before the planner trusts it. Add a schema/sanity check on every LLM response with a deterministic fallback (put symbol in facade or flag ambiguous) if the response fails validation. Also worth stating explicitly: what happens if Ollama is unreachable mid-session? Right now nothing degrades gracefully — it should fall back to deterministic-only planning with a warning badge, not block the tab.
6. Validation proves structure, not behavior.
py_compile + symbol/API/import-graph checks prove the split is structurally sound, but nothing proves the reassembled code is byte-for-byte equivalent to the original (minus intentional docstring insertions), and nothing runs the project's own tests against the preview if a test suite exists. I'd add two things to Stage 14: (a) a normalized source-content diff — concatenated body of all generated modules should match the original body content aside from added docstrings/imports — and (b) an optional "run existing test suite against preview" soft gate when a test suite is detected, surfaced as a warning rather than a hard block if none exists.
7. Staleness between analysis and patch isn't handled.
If the target file changes on disk between ANALYZED and PATCH_READY (user edits it, another process touches it, a git pull happens), the plan is now built against content that no longer exists, and the patch would apply blind. Add a content-hash recheck immediately before patch creation — mismatch forces re-analysis rather than allowing a stale patch through.
8. No-Leak enforcement is described conceptually, not mechanically.
The spec says the gate exists but doesn't say how writes are actually stopped. If each stage independently "checks" no-leak, one stage will eventually forget. I'd centralize this into a single assert_within_allowed_roots(path, allowed_roots) that every file-write call — preview writer, patch creator, docstring inserter — is required to funnel through, so there's exactly one place that can leak, not N places that each need to remember not to.
Smaller things worth adding

Rollback story: patch metadata should include a copy/hash of the original file(s) being replaced, so a bad apply can be reverted without relying on the user's own backups.
Filename collision check: before preview write, check proposed helper filenames (e.g. _shared.py) against files that already exist in the project — two refactor runs on different large files could independently propose the same helper name.
Schema versioning: RefactorPlan/ValidationReport JSON gets written to disk and potentially reloaded later — add a schema_version field now, it's nearly free and saves pain on v2.
Diff view in Section 5: currently preview only lists generated files. A unified before/after diff of the facade module specifically would make review dramatically faster than reading N new files cold.
Path handling: the preview path example uses Windows backslashes (<project_drive>\...) — make sure the actual implementation notes say pathlib.Path, not string concatenation, so this isn't accidentally Windows-only.
Validation script size: you're asking one script to check ~13 distinct concerns and also enforce ≤500 lines on itself — worth splitting it into per-concern check functions in one file, or a small validation/checks/ package, so it doesn't become the very thing it's validating against.

Priority if you're implementing in order
Fix #7 (staleness) and #8 (centralized no-leak gate) before Phase 1 — both are cheap now and expensive to retrofit once multiple stages exist. Fix #1/#2 (oversized-group and oversized-class policy) before Phase 3 (split planner), since the planner literally can't be tested against real-world files without them. #4–#6 can land incrementally through Phases 4–6 as you build those stages.
Want me to turn any of these into concrete data-contract additions (e.g. the TOO_LARGE_CLASS flag, schema_version field, docstring provenance tag) or sketch the assert_within_allowed_roots gate function?
Claude is AI and can make mistakes. Please double-check responses.

I audited the suggestions and agree with almost all of them. The only point I would modify is the suggestion to generate sed/find commands for import migration: for KANDA/Windows/PyCharm compatibility, that should be a plain Python helper preview instead of Unix-style commands.

The attached audit also supports the main direction: staged workflow, tool/project separation, validation gates, AST + LibCST division, bounded LLM use, preview location, and no-leak checks are strong, but integration with existing Architecture Review data, shared AI model selection, relative imports, public API detection, cycle resolution, docstring line-count impact, worker threads, and validation design need to be tightened before implementation.

Below is the final handoff I would use.
FINAL HANDOFF: Architecture Review - Large File Refactor Planner
Feature name

Architecture Review -> Large File Refactor Planner

Feature id:

architecture-review-large-file-refactor-planner-v1

Purpose

Implement a new sub-tab inside the existing Architecture Review tab.

The sub-tab must help refactor large Python modules safely by producing a reviewable, validated split plan before any source write.

This is not an automatic refactor button.

It is a planner, previewer, validator, and patch-preparation workflow.

The feature must:

    identify large Python files;

    analyze symbols, imports, dependencies, globals, public API, docstrings, and risks;

    propose a split plan;

    preserve the original public facade when appropriate;

    keep files near 400 lines when possible and always <=500 physical lines unless blocked;

    avoid tiny helpers below 100 lines unless justified;

    detect missing docstrings and propose adequate docstrings;

    validate circular imports, public API preservation, lost symbols, lost decorators, stale source, and no-leak boundaries;

    generate preview files only in the active project's daily-work preview area;

    create a patch only after validation passes.

Mandatory ownership rule: KANDA Reasoner tool vs KANDA Reasoner project

KANDA Reasoner has two identities:

    KANDA Reasoner as the reusable tool.

    KANDA Reasoner as the active project currently being edited.

The Large File Refactor Planner itself is tool-owned.

Concrete split/refactored files produced for a selected target module are project-owned.
Tool-owned

Tool-owned files include:

Architecture Review GUI sub-tab
large file refactor planner controller
AST analyzer
LibCST preview writer
dependency graph builder
cycle resolver
import migration planner
docstring planner
local LLM arbitration wrapper
preview writer
validation runner
no-leak gate
patch creator

Project-owned

Project-owned files include:

selected source file being refactored
generated split source files
project-specific helper files
generated project docstrings
project-specific preview files
project-specific validation evidence
project-specific refactor plan JSON
project-specific patch payload
project-specific freeze hint, if applicable

Core no-leak rule

The refactor engine belongs to the KANDA Reasoner tool.

The refactored output belongs to the active project.

Do not write reusable tool logic into project output.

Do not write project-specific split files into reusable tool source unless the selected project source itself is intentionally being patched.
Required pre-implementation checks

Before coding, complete:

BOX CHECK

Task type:
Active box:
Owner path:
Allowed files:
Out-of-scope files:
Cross-box touches:
Public contracts:
Validation scope:
Boundary risks:
Tool/project ownership risk:
No-leak risk:
May proceed:
Next safe action:

And:

NO-LEAK CHECK

Active box:
Tool-owned files:
Project-owned files:
Project-specific support files:
Generated/evidence files:
Temporary daily-work files:
External boxes touched:
Out-of-scope files:
Leak risks:
Blocked writes:
Safe next action:

If ownership is unclear, inspect source and routing manifests before writing.
Required prompt/canon context before implementation

Load or apply:

04_box_architecture_and_boundaries
box_architecture_canon.md
kanda_box_shielding_canon.md
project_tool_boundary_canon.md
NO_LEAK_LOGIC_V1 / No-Leak Logic Bridge
05_patch_delivery_and_validation
07_daily_patch_delivery_guardrails
08_python_engineering_core
09_python_quality_security_observability
09_active_project_freeze_context
compact Error Memory
large_module_refactor_protocol, if present
pre_output_contract_gates before patch/PowerShell output
freeze_code_intake_and_form_protocol if freeze-ready

Do not implement from memory alone.
Sub-tab placement

Add a new local sub-tab inside Architecture Review:

Run Selected Mode
Large Module AST Split Audit
Large File Refactor Planner

The new sub-tab must reuse existing Architecture Review results when possible.

It must not duplicate the whole Architecture Review scanner unless needed as fallback.
Required integration with existing Architecture Review

The new sub-tab must discover candidate files in this order:

    Use the last Large Module AST Split Audit result, if available.

    Use parent Architecture Review controller state, if it exposes large-file findings.

    Fall back to a limited active-project-root scan.

Create a tool-owned module such as:

candidate_discovery.py

Its behavior:

1. Try parent Architecture Review state.
2. Try last AST Split Audit result.
3. If none exists, scan active project root for Python files above threshold.
4. Exclude generated, evidence, preview, freeze, handoff, ZIP, and daily-work artifacts unless explicitly selected.

Required integration with existing AI/model infrastructure

The tab must reuse the existing AI model selector/header pattern.

Do not create a separate independent Ollama model selector if one already exists.

The LLM arbitration module should reuse the same shared client or service used elsewhere in KANDA Reasoner, if present.

Suggested rule:

llm_arbitration.py must receive:
- selected model name
- model settings
- timeout
- whether local LLM use is enabled

LLM support must be optional.

If Ollama/local model is unavailable, the tab must degrade gracefully to deterministic-only planning and show a warning badge.
GUI layout

The sub-tab should have five sections.
1. Candidate file selector

Fields:

candidate file list
manual file selector, if existing UI supports it
refresh candidates
line-count threshold
active project root display
source ownership status

Candidate columns:

File
Lines
Public functions
Public classes
Total symbols
Imports
Global-state risks
Missing docstrings
External importers
Architecture warnings
Suggested action

Suggested actions:

Analyze
Already compliant
Needs source inspection
Blocked: generated artifact
Blocked: wrong box
Blocked: global state
Blocked: not Python source

2. Settings panel

Defaults:

Ideal physical lines: 400
Maximum physical lines: 500
Minimum helper physical lines: 100
Preserve public facade: ON
Generate missing docstrings: ON
Rewrite project imports: OFF in v1
Import migration preview: ON
Use local LLM: OFF by default or ON if configured
Preview only: ON
Create patch only after validation: ON

No "Apply now" button in v1.

Buttons:

Analyze File
Generate Split Plan
Ask Local LLM for Ambiguous Symbols
Generate Preview
Validate Preview
Create Patch ZIP
Open Preview Folder
Copy Summary
Cancel

3. Analysis evidence panel

Show:

module docstring present/missing
__all__ detected
public API symbols
external importers
top-level functions
top-level classes
constants
imports
relative imports
star imports
decorators
nested functions/classes
global state
module-level side effects
if __name__ == "__main__" block
dynamic imports
symbol references
line count per symbol
missing docstring count

Risk badges:

GLOBAL_STATE
DYNAMIC_IMPORT
STAR_IMPORT
RELATIVE_IMPORT_RISK
PUBLIC_API_RISK
FACADE_REEXPORT_RISK
LAZY_EXPORT_REQUIRED
DECORATOR_RISK
NESTED_SYMBOL_CLUSTER
CIRCULAR_IMPORT_RISK
PRIVATE_REACH_IN_RISK
NO_LEAK_RISK
MISSING_DOCSTRING
TOO_LARGE_COHESIVE_GROUP
TOO_LARGE_CLASS
TOO_SMALL_HELPER
STALE_SOURCE
FILENAME_COLLISION

4. Proposed split plan panel

For each proposed output module, show:

Output filename
Role
Estimated lines
Preview physical lines
Symbols included
Imports needed
Exports/re-exports
Docstrings generated
Docstring provenance
External importer impact
Risks
Status

Roles:

public_facade
analysis_helper
partition_helper
import_helper
docstring_helper
validation_helper
io_helper
gui_helper
llm_helper
shared_helper
domain_helper
adapter_helper
manual_review_required

The base module must usually be a public facade/orchestrator, not the largest bin.

Wrong:

largest bin becomes base module

Correct:

base module preserves public API, __all__, external imports, and orchestration
implementation moves into private helper modules

5. Preview, validation, and patch panel

Stage statuses:

Analysis: not run / ok / warning / blocked
Plan: not generated / ok / warning / blocked
LLM: disabled / ok / warning / unavailable
Docstrings: not generated / ok / warning / blocked
Preview: not generated / ok / warning / blocked
Validation: not run / passed / failed
Patch: not created / ready / blocked

Patch creation is blocked unless validation passes and source hash is fresh.
Core workflow
Stage 1: Candidate discovery

Input:

active project root
Architecture Review findings
Large Module AST Split Audit results
manual selected file, if provided

Output:

LargeFileCandidate[]

Candidate eligibility:

file is .py
file belongs to active project source
file is not generated/evidence/freeze/handoff/preview output
file is not under _delete_after_daily_work unless explicitly preview
file is not a startup delivery artifact unless task is startup maintenance
file exceeds threshold, default >500 physical lines

Physical lines mean total file lines, including comments and blank lines.

Use Python/pathlib for line counting. Do not use shell-specific commands.
Stage 2: AST analysis

Use Python AST for fast analysis.

Collect:

module docstring
top-level classes
top-level functions
async functions
constants
assignments
imports
ImportFrom
__all__
decorators
type annotations
global statements
nonlocal statements
module-level expressions
module-level calls
if __name__ == "__main__" blocks
line spans
end line spans
symbol references
nested symbols

Do not use AST for final rewriting because AST does not preserve comments and formatting.
Stage 3: LibCST readiness

Use LibCST for formatting-preserving preview writing and import/docstring transformation.

Parse with LibCST lazily:

Run AST first.
Parse with LibCST only for preview generation, exact node movement, import rewrite preview, or docstring insertion.
Cache CST by file path + content hash.

Stage 4: Symbol and cluster model

Use symbol records.

Required fields:

schema_version
name
kind
visibility
start_line
end_line
physical_lines
decorators
signature
return_annotation
has_docstring
docstring_text
docstring_provenance
references
imports_used
globals_used
external_importers
risk_flags
assigned_module
content_hash

Nested functions/classes must remain with the parent.

Class methods must remain with the class.

Decorators must remain with the decorated function/class.

Atomic clusters:

class + methods
decorator + decorated symbol
nested function/class + parent
strongly connected symbol group
module-level side-effect group
__all__ + facade exports
if __name__ == "__main__" block + facade/original module

Stage 5: Import model

Create import records:

schema_version
original_module
imported_name
alias
is_relative
relative_level
is_star
line_span
used_by_symbols
risk_flags

High-risk imports:

star import
relative import
conditional import
try/except fallback import
dynamic importlib
getattr-based module access
string-based imports
plugin discovery
import side-effect dependency

For v1, project-wide import rewriting is preview-only unless deterministic and explicitly approved.
Stage 6: Public API and external usage detection

Public API is determined by:

__all__
top-level symbols not starting with "_"
symbols imported by other project files
symbols documented as public in module docstring
known facade entrypoints
existing package exports

Perform a project-wide text search for the old module name first.

Only parse likely importer files with AST/LibCST.

Mark symbols imported elsewhere as:

public_contract = true
facade_critical = true

Validation must prove those symbols remain accessible through the original facade unless the user explicitly approves a breaking change.
Stage 7: Global state and side-effect policy

Flag but do not automatically move:

logging.basicConfig
environment reads
path setup
registry setup
global mutable containers
cache initialization
Tkinter or GUI initialization
thread/process startup
network/file/database side effects
plugin registration
monkeypatching
import-time execution

Default:

Keep in original module/facade.
Move only when clearly pure or explicitly approved.

Stage 8: Split planning

Targets:

ideal: around 400 physical lines
maximum: 500 physical lines
minimum helper: 100 physical lines

Planning priority:

1. Preserve behavior and public API.
2. Preserve box/no-leak ownership.
3. Preserve global-state ordering.
4. Group by responsibility.
5. Respect dependency graph.
6. Avoid cycles.
7. Respect line-count constraints.
8. Avoid tiny helper files.

Line count is a constraint, not the architecture principle.
Oversized cohesive group policy

If a responsibility group exceeds max_lines:

1. Try sub-partition by secondary responsibility.
2. Try sub-partition by dependency direction.
3. Try sub-partition by import/resource family.
4. Try shared helper extraction only if it reduces coupling.
5. If still oversized, flag TOO_LARGE_COHESIVE_GROUP.
6. Block automatic planning for that group.

Do not silently split by raw line cut.
Oversized single class policy

If one class alone exceeds 500 physical lines:

flag TOO_LARGE_CLASS
do not split methods into separate files automatically
route to manual class refactor workflow
allow docstring/comment-only improvements only if safe

The planner may suggest future manual refactors such as:

extract collaborator class
extract dataclass/config object
extract strategy object
extract pure utility functions
split UI from logic

But v1 must not automatically split class methods across modules.
Minimum helper justification

A helper below 100 physical lines is allowed only if at least one is true:

required to break circular dependency
contains one cohesive class with at least 3 methods
contains at least 2 pure utilities used by multiple modules
is a public facade compatibility shim
isolates import side effects
isolates optional dependency integration
contains generated import migration adapter approved by validation

Otherwise merge it into the nearest related module.
Filename collision check

Before preview writing:

check proposed filenames against existing project files
check proposed filenames against other preview files
check repeated refactor runs do not collide

If collision exists:

flag FILENAME_COLLISION
suggest target-specific prefix/suffix
block preview unless resolved

Cycle detection and cycle resolution

Build a module dependency graph.

Use topological sorting or a deterministic fallback.

If cycle is detected, apply deterministic resolution in order:

1. Merge involved modules if final line count <=500.
2. Keep one or more cycle-causing symbols in facade if facade remains <=500.
3. Extract shared pure symbols into a shared helper if it breaks the cycle and helper size is justified.
4. Use lazy facade export if cycle is only created by eager facade re-export.
5. Ask local LLM for semantic grouping only as advisory JSON.
6. If unresolved, flag CIRCULAR_IMPORT_RISK and block patch.

Facade re-export policy

The original module should usually become the public facade.

Facade responsibilities:

preserve public imports
preserve __all__
preserve external import compatibility
preserve if __name__ == "__main__" block when present
delegate implementation to private helpers
avoid duplicate public ownership

Default eager re-export:

from ._helper import public_symbol

But eager re-export can create cycles.

If eager re-export causes a cycle, consider lazy export using module-level __getattr__ as fallback.

Lazy export policy:

Use lazy facade export only when:
- public API preservation requires facade access;
- eager re-export creates a cycle;
- symbol can be lazily imported safely;
- validation confirms no duplicate public ownership;
- the behavior is documented in the refactor plan.

Do not use lazy export as default.
LLM arbitration policy

LLM use must be optional and bounded.

Allowed:

assign ambiguous symbol to proposed module
suggest semantic helper filename
draft missing docstring
explain cycle cause
suggest merge vs shared-helper decision

Forbidden:

rewrite whole module
create patch directly
decide ownership without source inspection
bypass validation
bypass no-leak

LLM output must be JSON-only.

Every LLM response must be schema-validated.

Invalid LLM response behavior:

discard response
show warning badge
fall back to deterministic assignment
put symbol in facade if safest
or flag AMBIGUOUS_SYMBOL_NEEDS_REVIEW

LLM unavailable behavior:

continue deterministic-only planning
show LLM_UNAVAILABLE warning
do not block analysis or deterministic plan
block only LLM-dependent optional actions

LLM cache key must include:

schema_version
file_content_hash
symbol_name
symbol_line_span
symbol_body_hash
candidate_module_list_hash
model_name
temperature
llm_settings_hash
prompt_version

Docstring completion stage

The planner must detect and propose missing docstrings.

Targets:

module docstring
public classes
public functions
public methods
complex private helpers
generated helper modules
facade modules

Do not overwrite existing docstrings by default.

Docstring style:

Google-style
triple double quotes
short summary first
Args when parameters exist
Returns when return value exists
Raises only when explicit raises are detected
use existing type hints
do not invent behavior
do not claim side effects unless statically evident

Docstring provenance must be recorded.

Allowed provenance values:

existing
deterministic_template
llm_drafted
low_confidence_needs_review
manual_required

Docstring confidence rule:

If function has non-obvious side effects, dynamic behavior, global writes, network/file/database calls, or unclear return semantics, mark low_confidence_needs_review.

Line count must be revalidated after docstring insertion.

If docstrings push a module above 500 physical lines:

1. shorten docstrings using concise template;
2. re-plan if possible;
3. if not possible, flag DOCSTRING_LINE_LIMIT_RISK and block patch.

Preview generation

Preview must not write directly to active source tree.

Preview location:

active_project_daily_work_root / "large_file_refactor_preview" / feature_id_or_timestamp

Use project path resolver and pathlib.

Do not concatenate Windows strings manually.

Preview output must include:

refactor_plan.json
symbol_map.json
import_migration_plan.json
docstring_proposals.json
risk_report.json
validation_report.json
README_PREVIEW.txt
README_IMPORTS.txt
facade_diff.patch or facade_diff.txt
generated preview modules

No Unix-only commands.

If import migration helper is generated, make it a plain Python helper preview, not sed/find commands.
Centralized no-leak write gate

No write function may write paths directly.

All writes must pass through one centralized gate:

assert_within_allowed_roots(path, allowed_roots, purpose)

This gate must be used by:

preview writer
patch creator
docstring inserter
import migration preview writer
validation evidence writer
cache writer

The gate must reject:

wrong active project root
tool/project ownership mismatch
writes into generated startup ZIP contents
writes into freeze memory from preview
writes outside allowed daily-work or patch payload roots
path traversal
ambiguous root

Every file-write function must call a shared safe_write_text, safe_write_bytes, or equivalent wrapper that invokes this gate.
Staleness protection

Every plan must store:

source_path
source_size
source_mtime
source_content_hash
analysis_timestamp
settings_hash

Before preview generation and before patch creation:

re-read source file
recompute content hash
compare with plan hash

If mismatch:

flag STALE_SOURCE
block patch creation
force re-analysis

This is a hard gate.
Rollback metadata

Patch metadata should include:

original file path
original file content hash
original file size
original mtime
preview source hash
generated file hashes
patch feature id
schema_version

If feasible, include a backup copy in the patch staging metadata or record enough hash/path data to support safe manual rollback.
Validation

Validation must prove more than compile success.

Required validations:

py_compile generated preview files
AST parse generated files
line count <=500 physical lines
helper >=100 physical lines or justified
public API preservation
external importers still resolved through facade
symbol preservation
decorator preservation
nested symbol preservation
__all__ preservation
if __name__ == "__main__" preservation
module dependency graph acyclic or justified lazy facade export
docstring validation
docstring provenance recorded
filename collision check
source hash fresh
no-leak write gate used
preview wrote only allowed roots
patch creation validation-gated

Behavior validation:

If project tests are detected, offer "Run existing test suite against preview/patch" as a soft gate.
If no tests are found, show warning: TEST_SUITE_NOT_DETECTED.

Do not claim behavior equivalence from py_compile alone.

Also generate a normalized source-content comparison:

Compare original movable symbol bodies with generated symbol bodies.
Allow expected differences:
- imports
- module docstrings
- inserted docstrings
- facade re-exports
- formatting preserved/normalized by LibCST

Flag unexpected body changes.
Import migration preview

V1 default:

Rewrite project imports: OFF
Import migration preview: ON

Generate:

import_migration_plan.json
README_IMPORTS.txt
optional Python helper preview

Do not generate sed/find commands.

Relative imports:

detect and flag high risk
only auto-preview rewrite if package path remains valid
otherwise require manual review

Star imports:

flag high risk
do not auto-rewrite in v1

GUI responsiveness

All long-running work must run in the existing GUI worker pattern.

If an existing worker exists, reuse it.

If not, create a small refactor-specific worker consistent with the app.

Long-running operations:

AST scan over large project
LibCST parse
LLM call
preview generation
validation
import migration scan
project test detection

Worker requirements:

progress messages
safe cancellation
structured result
structured error
no UI freeze
no direct UI mutation from worker thread

Add Cancel button.
State machine

Use explicit states:

IDLE
CANDIDATE_SELECTED
ANALYZING
ANALYZED
PLAN_READY
LLM_REVIEW_READY
DOCSTRING_READY
PREVIEW_GENERATING
PREVIEW_READY
VALIDATING
VALIDATION_PASSED
VALIDATION_FAILED
PATCH_READY
BLOCKED
STALE_SOURCE
CANCELLED

Patch creation allowed only from:

VALIDATION_PASSED

Patch creation blocked from all other states.
Data contracts

All persisted JSON must include:

schema_version
feature_id
created_at
tool_version_or_patch_id
active_project_root
target_file
source_content_hash
settings_hash

LargeFileCandidate

schema_version
path
relative_path
line_count_physical
public_symbol_count
class_count
function_count
missing_docstring_count
external_importer_count
risk_flags
source_box
is_eligible
blocked_reason

RefactorSymbol

schema_version
name
kind
visibility
start_line
end_line
physical_lines
decorators
signature
return_annotation
has_docstring
docstring_text
docstring_provenance
references
imports_used
globals_used
external_importers
atomic_cluster_id
risk_flags
assigned_module
content_hash

ProposedModule

schema_version
filename
role
symbols
estimated_lines
preview_physical_lines
imports
exports
docstrings_generated
risk_flags
status
line_limit_justification

RefactorPlan

schema_version
feature_id
target_file
source_content_hash
settings
public_api_before
public_api_after_expected
symbols
atomic_clusters
proposed_modules
import_migration
docstring_proposals
risks
validation_blockers
status

ValidationReport

schema_version
feature_id
source_content_hash
line_count_ok
compile_ok
ast_cross_check_ok
docstrings_ok
public_api_ok
symbol_preservation_ok
decorator_preservation_ok
nested_symbol_ok
import_graph_ok
no_leak_ok
staleness_ok
filename_collision_ok
architecture_ok
test_suite_status
errors
warnings
success_markers

Patch creation policy

Differentiate patch types:

is_tool_patch
is_project_patch
is_mixed_patch

For v1 implementation of the tab itself:

is_tool_patch = true

It should include only tool-owned modules, GUI registration changes, and validation scripts.

For future application of a split to a selected project:

is_project_patch = true

It should include project-owned refactored source files and project-specific validation evidence.

Do not mix tool feature implementation and project refactor output in the same patch unless explicitly governed and validated.

Freeze hint:

Tool-only patch: include freeze hint only if local freeze workflow expects it for validated tool features.
Project split patch: include project-specific freeze hint if freezeable.
Mixed patch: avoid unless explicitly approved.

Validation script design

Focused validation script:

validation/test_architecture_review_large_file_refactor_planner_v1.py

It must be self-contained and avoid broad project-wide imports.

Use synthetic sample modules and mock GUI/controller state where possible.

Checks:

new sub-tab registration exists
candidate discovery fallback exists
shared AI model selection hook exists or is intentionally deferred
settings defaults 400/500/100 exist
facade preservation rule exists
oversized cohesive group rule exists
TOO_LARGE_CLASS rule exists
central no-leak write gate exists
source hash staleness gate exists
docstring provenance exists
LLM schema validation exists
LLM unavailable fallback exists
filename collision check exists
preview path uses pathlib/path resolver
import migration preview is ON and auto-rewrite OFF by default
relative import risk flag exists
nested symbols are atomic with parent
validation-gated patch creation exists
all new/touched Python modules <=500 physical lines
py_compile passes changed Python files

Expected markers:

VALIDATION OK: architecture-review-large-file-refactor-planner-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Keep the validation script itself under 500 physical lines.

If too large, split validation helpers into small validation modules under an appropriate validation helper folder, preserving module-size rules.
Implementation phases
Phase 1: Shell and contracts

Implement:

sub-tab shell
settings panel
state machine
data models
candidate discovery stub
central no-leak write gate
staleness contract
validation skeleton

No preview generation yet.

Highest priority gates to implement now:

central no-leak write gate
source hash staleness gate

Phase 2: Analyzer

Implement:

AST analyzer
symbol extraction
docstring detection
import detection
public API detection
global-state risk flags
nested symbol/atomic cluster detection
candidate discovery from parent Architecture Review state or fallback scan

Phase 3: Split planner

Implement:

responsibility classification
dependency graph
line constraints
oversized cohesive group policy
oversized single class policy
minimum helper justification
cycle resolver
filename collision check
facade preservation plan

Phase 4: Docstring planner

Implement:

missing docstring proposals
docstring provenance
low-confidence flag
line recount after docstrings
docstring validation

Phase 5: LLM arbitration

Implement:

shared model selection integration
JSON-only responses
schema validation
cache with model/settings hash
unavailable fallback
invalid response fallback

Phase 6: Preview writer

Implement:

LibCST-based preview generation
safe write through no-leak gate
preview folder creation via pathlib/path resolver
facade diff generation
import migration plan
README_PREVIEW
README_IMPORTS

Phase 7: Validation and patch creation

Implement:

py_compile
AST cross-check
symbol preservation
public API preservation
dependency graph validation
docstring validation
staleness recheck
no-leak validation
test-suite detection soft gate
patch ZIP creation after validation only

Explicit non-goals for v1

Do not implement:

automatic apply without preview
whole-project automatic refactor
LLM rewriting entire files
automatic class-method splitting
automatic moving of import-time side effects
automatic project-wide import rewrite
Unix sed/find command output
type stub rewriting
test generation
mixed tool/project patch unless explicitly approved

Acceptance criteria

The feature is accepted when:

1. Architecture Review contains Large File Refactor Planner sub-tab.
2. The tab reuses existing Architecture Review large-file evidence or falls back to active-project scan.
3. The tab uses shared AI model selection where available.
4. The tab can analyze a selected large Python file.
5. It shows symbols, imports, dependencies, globals, public API, external importers, and missing docstrings.
6. It proposes split modules using responsibility first and line count as constraint.
7. It enforces ideal 400, maximum 500, and minimum 100 physical line policy.
8. It blocks or flags oversized cohesive groups.
9. It blocks or flags oversized single classes.
10. It preserves facade/public API.
11. It detects facade re-export cycle risk and supports lazy facade fallback only when validated.
12. It proposes docstrings with provenance and confidence.
13. It validates LLM JSON responses and degrades gracefully if LLM is unavailable.
14. It checks source hash before preview and before patch creation.
15. It routes all writes through a centralized no-leak write gate.
16. It writes preview only to active project daily-work preview root.
17. It generates import migration preview without applying project-wide rewrites by default.
18. It validates generated preview files before patch creation.
19. It blocks patch creation on stale source, circular imports, public API mismatch, filename collision, no-leak violation, or validation failure.
20. It creates patch ZIP only after validation.
21. All new/touched source modules remain <=500 physical lines.
22. Focused validation prints:
    VALIDATION OK: architecture-review-large-file-refactor-planner-v1
    STATUS: IN_SYNC
23. Patch contract validation prints:
    ZIP CONTRACT: PASS

Final implementation priority

Before Phase 1:

1. Centralized no-leak write gate.
2. Source hash staleness gate.

Before Phase 3:

1. Oversized cohesive group policy.
2. Oversized single class policy.
3. Minimum helper justification.
4. Filename collision check.

Before Phase 4 and 5:

1. Docstring provenance.
2. LLM schema validation.
3. LLM unavailable fallback.

Before Phase 6 and 7:

1. Public API/external importer preservation.
2. Facade re-export cycle handling.
3. Preview-only import migration.
4. Behavior-aware validation warning via optional test-suite detection.

Final compact summary

Build the Large File Refactor Planner as a safe Architecture Review sub-tab that converts large-file architecture debt into a validated, reviewable plan.

It must not be a magic refactor button.

It must use:

AST for fast analysis
LibCST for formatting-preserving preview generation
dependency graphs for cycle detection
public facade preservation
docstring completion with provenance
bounded JSON-only local LLM decisions
central no-leak write gate
source hash staleness gate
preview-only output
validation-gated patch creation

Most important rule:

The refactor planner engine is KANDA Reasoner tool-owned.
The concrete split/refactored source files are active-project-owned.
Every write must prove its ownership and allowed root before it happens.

My final verdict: approved with amendments. The amended version above is now stronger than the prior spec because it closes the two most dangerous gaps before implementation: stale-source patching and distributed no-leak enforcement.


