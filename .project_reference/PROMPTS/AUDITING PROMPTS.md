0010.d AI_Human_Engineering_Partnership_Master.md
File
0010.e Ai Human partinership.md
File
0010.f Final Ai Human partinership.md
File
0010.g Final Ai Human partinership how reason a demand.md
File
0011a How prompt on demand.md
File
0011b How prompt on demand.md
File
0011c How prompt on demand.md
File
0011d How prompt on demand first roadmap.md
File
you are a python senior prompt enginner and programmer with 25 years of experience in complex multilayer code implementation, you not only write code ,  you build  state of art app and systems  using as method AI plus prompts plus human  colaboration. Human do not code , he determine focus  , directions and app features, beside testing codes you create and suggests modifications  and modifications, audit uploads and list what more is missing to maximum performance of this partnership. I want a universal, project-agnostic framework — a master prompt/documents that define every determinant of professional AI-assisted app engineering, so any future session starts with comcatenated prompts called on demand. Now you are the maestro that will organize the discussion presented on engineering prompts.

first tell me if you understand these discussions and if you agree that  method 3 is the ideal to start with . Discussion goes in odre from 10d  to 11d 

I’ll read the uploaded sequence as a discussion chain, not as isolated documents, and judge whether Option/Method 3 is the right first operational step before anything more autonomous.

Yes, I understand the discussion chain.

You are building a universal AI-assisted engineering operating system, not just a prompt collection. The discussion evolves like this:

    0010.d defines the core AI + human engineering method: human as technical lead, AI as pair programmer, evidence-first work, surgical patches, validation, freeze discipline.

    0010.e / 0010.f strengthen that into a more mature v2.0 framework with extra determinants: performance, documentation sync, dependency freshness, rollback depth, hallucination detection, structured logs, and auditability.

    0010.g turns the framework into a reusable session-start master prompt, with role split, pre-code steps, scope declaration, owner-box identification, risk scoring, validation, freeze protocol, and handoff.

    0011a-c identify the next-level problem: once you have many specialist prompts, you need prompt orchestration, meaning the right prompt stack must be loaded on demand instead of manually remembered.

    0011d proposes the first buildable solution: Option/Method 3 — CLI Prompt Dispatcher, with prompt folders, metadata headers, prompt_index.json, dependency resolution, prompt composition, output to clipboard/file/API, and audit logs.

So yes: I agree that Method 3 is the ideal starting point.

But with one important precision:

Method 3 is not the final ideal system. It is the ideal first implementation.

The final direction is still:

3 → 5 → 6

Meaning:

Method 3: CLI Prompt Dispatcher
This is the first real automation layer. You type something like:

python dispatch.py new-patch
python dispatch.py architecture-check
python dispatch.py freeze-review

The dispatcher selects the correct prompt files, resolves dependencies, concatenates them in the right order, and sends them to clipboard/file/API. This gives immediate benefit without overbuilding.

Method 5: Desktop Prompt Orchestration App
Once Method 3 teaches us which prompts are used together, which triggers work, and which prompt combinations conflict, we can build a PySide6 visual app with prompt library, dependency graph, audit trail, versioning, and session state.

Method 6: Meta-AI Orchestrator
Only after the prompt graph is stable should an AI automatically decide which specialist prompts to inject. If we build Method 6 now, the orchestrator would route based on guesses, not evidence. The uploaded discussion correctly warns that an invisible autonomous router can confidently inject the wrong prompt at the wrong moment, which is dangerous because the failure is hidden.

My verdict:

Start with Method 3. Absolutely.

It is the correct bootstrap layer because it is:

    simple enough to build safely;

    useful immediately;

    auditable;

    compatible with any AI tool;

    manually triggered, so low risk;

    able to generate the real usage data needed for Method 5 and Method 6.

The next correct move is not to build the meta-AI yet. The next correct move is to build a clean Prompt Dispatcher v1 with:

prompts/
prompt_index.json
dispatcher_config.json
resolver.py
composer.py
matcher.py
dispatch.py
logs/dispatch_audit.jsonl
tests/

Then use it in real sessions until the prompt dependency graph becomes obvious from evidence, not theory.

Pasted text.txt
Document
wait  to make prompt stables lets first create some canonic rules:
audit all prompts,  use some large prompts , or smaller prompts, use prompts with I demmand commad , rule  or one prompt for each diferent task ,  create a initial set of prompts for  initial implementationsor just  one prompt . I belive that we must have a set of orientations like an index for human part of partnership ( to help choose prompt for task) , we must research which is confortable prompt tolken size for Ai ,  we can set  code communication between human and AI ,  example , human say at begining of day "I want create ..." , AI  answer to start creating I need  prompts  1 , 2 and 3,  then AI knows that  modules can have just 500 lines, and shes sees a file with 501 lines , then , she says ,  modules can have just  500 lines I need  prompt  23, etc.  So before coding I want audit all prompts  , remove repetition ,  redundancies,  improve language for AI understanding  and just after stabilize all prompts ,start using them .  I need more suggestions to improve these audit prompt ideas really architectural , coherent and otimized to add necessary features to this  audit , grouping prompt commands for use ,

 Before building the dispatcher, lests audit and canonize the prompt library itself to make it consistent . Think through this architecturally.
Create  a Prompt Engineering Canon — a set of rules that governs how prompts are written, sized, structured, and grouped before any automation is built. This is the foundation that makes everything else reliable.
build the complete audit framework adding more suggestions to comments bellow or improving them .

Layer 1 — Prompt size canon
S.1Define three prompt size tierssize rule
Nano (<300 tokens): single rule, single command, injected on demand. Micro (300–800 tokens): one focused topic, one phase. Standard (800–2000 tokens): full protocol for one workflow. Never exceed 2000 tokens per individual prompt file. The master session prompt is the only allowed exception and must be measured.
S.2Measure every prompt before adding itsize rule
Every prompt file must have its token count in its metadata header before it enters the library. Rule: token_count field is mandatory. A prompt with no token count is not allowed in the library. Use tiktoken or the Anthropic token counter to measure.
S.3Define the session token budgetsize rule
Total composed prompt stack must leave at least 60% of the context window free for evidence, conversation, and code. For Claude Sonnet (200k tokens): prompt stack budget = 80,000 tokens max. For a typical session with evidence uploads: keep composed stack under 20,000 tokens. Calculate headroom before every session start.

Layer 2 — Prompt structure canon
P.1Mandatory metadata header on every promptstructure rule
Every prompt file must declare: id, name, version, token_count, phase, type (rule/command/protocol/reference), trigger_keywords, depends_on, conflicts_with, last_validated, description (one sentence). No exceptions. A prompt without a complete header is rejected from the library.
P.2Four prompt types — never mix in one filestructure rule
RULE: a constraint the AI must always obey (e.g. never use Clear-Host). COMMAND: an action the AI performs on demand (e.g. generate handoff). PROTOCOL: a sequence of steps for a workflow (e.g. validation chain). REFERENCE: a lookup table the AI reads but does not execute (e.g. box type definitions). Each file contains exactly one type. Never mix types in one file.
P.3One responsibility per prompt — the Box rule applied to promptsstructure rule
A prompt file owns exactly one topic. If you cannot describe what the prompt does in one sentence without using "and", it must be split. Test: cover the prompt and ask "what does this file do?" If the answer has more than one verb, split it.
P.4Imperative language only — no suggestions, no maybesstructure rule
Every rule in a prompt must use imperative form: DO this, NEVER do that, ALWAYS confirm, STOP before proceeding. Never write "you should consider" or "it is recommended that". Weak language produces weak AI compliance. Every sentence must be a command or a fact, never a suggestion.

Layer 3 — Prompt grouping canon
G.1Seven canonical prompt groupsgrouping rule
CORE: always-on rules loaded every session. PATCH: patch creation and delivery rules. ARCHITECTURE: ownership, layer, boundary rules. VALIDATION: testing, workflow, architecture validation chain. GOVERNANCE: freeze gate, freeze protocol, freeze authority. SESSION: session start, handoff, metrics. REFERENCE: lookup tables, taxonomies, box definitions. A prompt belongs to exactly one group.
G.2Always-on vs on-demand — two loading modesgrouping rule
ALWAYS-ON: loaded at every session start automatically. Maximum 3 prompts. Maximum 5,000 tokens total. Must be truly universal — no phase-specific rules. ON-DEMAND: loaded only when the phase requires them. Triggered by keyword or human command. This is the majority of the library. If you find yourself wanting more than 3 always-on prompts, you have a scoping problem.
G.3Named context stacks — pre-defined combinationsgrouping rule
A context stack is a named, ordered list of prompts that always travel together for a specific work phase. Examples: SESSION-START stack, NEW-PATCH stack, ARCHITECTURE-REVIEW stack, FREEZE-REVIEW stack. Stacks are defined in prompt_index.json, not assembled ad-hoc. If you find yourself combining prompts manually every session, that combination needs a named stack.

Layer 4 — Human-AI communication canon
C.1Human command vocabulary — standardized signal wordscomm rule
Define a small, stable vocabulary humans use to signal intent. START: begin a new session. PATCH: begin a new patch. ARCH: architecture review needed. VALIDATE: run validation chain. FREEZE: freeze gate review. HANDOFF: generate session handoff. NEED: I need prompt X loaded (explicit request). LOAD: force-load a specific prompt by id. This vocabulary is the routing table's input language.
C.2AI signals which prompts it needs — the NEED protocolcomm rule
When the AI detects it is missing a required prompt for the current task, it responds: "To proceed with [task] I need prompts: [id1], [id2]. Please load them." Human types: LOAD id1 id2. Dispatcher assembles and injects. AI confirms: "Prompts loaded. Proceeding." This is the explicit handshake that replaces guessing.
C.3AI self-check rule — detects violation, requests promptcomm rule
Every RULE-type prompt teaches the AI to self-monitor. When the AI detects it is about to violate a rule (e.g. a file has 501 lines, module limit is 500), it says: "RULE ALERT: [rule description]. Governing prompt: [id]. Load it or confirm override." It never silently violates a rule. It always signals before proceeding. This is coded into every RULE-type prompt as a standard closing instruction.
C.4Confidence interrupt — human kill switchcomm rule
Human types !/stop at any time. AI immediately stops, states current status, and waits. Human types !/resume to continue or !/redirect [new instruction] to change course. These commands bypass all routing and are hardcoded into the master session prompt as absolute overrides. No prompt can suppress them.

Layer 5 — Audit process
A.1Audit step 1 — inventory and classify every existing promptaudit
For each existing prompt file: (1) measure token count, (2) assign type: rule/command/protocol/reference, (3) assign group, (4) write one-sentence description, (5) flag: TOO-LARGE / MIXED-TYPE / NO-HEADER / DUPLICATE / WEAK-LANGUAGE / MISSING-TRIGGER. Do not edit yet. Inventory first, diagnose second, fix third.
A.2Audit step 2 — detect duplicates and redundanciesaudit
Read every prompt pair. Flag: DUPLICATE if two prompts state the same rule in different words. REDUNDANT if one prompt's content is fully covered by another. CONFLICTING if two prompts give contradictory instructions. For each flag: merge duplicates, remove redundants, resolve conflicts. One rule lives in exactly one prompt file.
A.3Audit step 3 — rewrite weak languageaudit
Replace every "should", "consider", "try to", "it is recommended", "where possible" with imperative commands. Replace every passive sentence with active. Replace every vague term ("clean", "good", "appropriate") with a specific measurable criterion. After rewriting: re-measure token count, update header, increment version number.
A.4Audit step 4 — split oversized and mixed-type promptsaudit
For every TOO-LARGE or MIXED-TYPE flag: identify the natural split points (different topics, different types, different phases). Create two or more new prompt files, each with a complete header. Add depends_on relationships between them if needed. Delete the original after the split is verified. Never split without first writing the new files.
A.5Audit step 5 — build the human indexaudit
After audit is complete: generate a human-readable PROMPT_INDEX.md listing every prompt by group, with: id, name, type, token count, one-sentence description, trigger keywords, and when to use it. This is the reference the human reads to choose prompts. It is not the machine-readable JSON — it is the human companion document. Update it every time a prompt changes.

You are correct to pause before coding. The dispatcher should not automate a messy library; first we need a canonical prompt architecture, then audit, then freeze, then automate.

Yes. This is exactly the right correction.

Before building the dispatcher, we need to stabilize the prompt library as an engineering asset. Otherwise the dispatcher will only automate disorder.

Your uploaded canon already has strong foundations: model-agnostic token measurement, size tiers, mandatory metadata, grouping, human commands, NEED protocol, audit process, prompt testing, lifecycle rules, and macro commands.

My architectural correction is this:

Do not start with 20-30 prompts. Start with one kernel prompt plus a controlled initial prompt set. Then audit, split, merge, freeze, and only then automate.

The dispatcher should be built after the prompt dependency graph becomes stable, because your previous discussion already identified that Option 3 is valuable exactly because it discovers real prompt combinations and dependency order through use.

Below is a complete upgraded framework you can use as the Prompt Engineering Canon v2.0.
Prompt Engineering Canon v2.0
Purpose

This canon defines how every prompt in the AI-assisted engineering partnership must be written, sized, grouped, audited, tested, loaded, and retired.

The goal is not to create many prompts.

The goal is to create a stable, minimal, non-redundant prompt library that can later be automated by a dispatcher, desktop orchestrator, or meta-AI router without creating confusion.

This canon must be applied before building any prompt dispatcher.
Part 1 - Core philosophy
Canon Principle 1 - The prompt library is source code

Treat every prompt as a source file.

Every prompt must have:

    one owner responsibility;

    version;

    metadata;

    trigger rules;

    dependency rules;

    conflict rules;

    token count;

    tests;

    lifecycle status;

    changelog.

A prompt that cannot be audited cannot be automated.
Canon Principle 2 - Fewer stable prompts are better than many unstable prompts

Do not create one prompt for every tiny idea.

Create a new prompt only when the rule, command, protocol, or reference table has a clear independent reason to exist.

Bad design:

    40 tiny prompts;

    unclear overlap;

    repeated commands;

    hidden conflicts;

    no dependency graph.

Good design:

    1 kernel prompt;

    8-15 stable specialist prompts;

    clear context stacks;

    no duplicated rules;

    deterministic loading order.

Canon Principle 3 - Every prompt must answer one question

Each prompt must answer exactly one of these:

    What must the AI always obey?

    What action must the AI perform now?

    What workflow steps must the AI follow?

    What reference information must the AI consult?

    What communication command must the human and AI use?

If one file answers more than one question, split it.
Canon Principle 4 - Automation must follow canonization

Do not build a dispatcher before the prompt library is canonical.

Correct order:

    Inventory prompts.

    Classify prompts.

    Remove duplicates.

    Resolve conflicts.

    Rewrite weak language.

    Split oversized prompts.

    Build human index.

    Build machine index.

    Test prompt stacks.

    Freeze prompt library.

    Build dispatcher.

Part 2 - Prompt size canon
S.1 - Prompt size tiers

Every prompt must belong to one size tier.

Nano prompt:

    less than 300 tokens;

    contains one atomic rule or one atomic command;

    used for high-priority on-demand injections;

    example: terminal log preservation rule.

Micro prompt:

    300 to 800 tokens;

    contains one focused topic;

    belongs to one phase;

    example: module size rule, file naming rule, failure classification rule.

Standard prompt:

    800 to 2000 tokens;

    contains one full workflow;

    example: patch creation protocol, validation protocol, freeze protocol.

Kernel prompt:

    maximum 4000 tokens;

    loaded at session start;

    contains only universal always-on rules;

    must not contain phase-specific details.

S.2 - Individual prompt limit

No normal prompt file may exceed 2000 tokens.

The only exception is the kernel prompt.

If a prompt exceeds 2000 tokens, it must be split unless there is a documented reason.
S.3 - Token measurement standard

Every prompt must be measured using one common tokenizer.

Use cl100k_base as the common counting standard.

Every prompt header must contain:

token_count: 0
tokenizer: cl100k_base

The token count must be generated by script.

Manual token counts are not allowed.
S.4 - Session stack budget

The composed prompt stack must leave at least 60 percent of the model context window free for:

    project evidence;

    source code;

    logs;

    user conversation;

    AI reasoning output;

    validation results.

Default practical budget:

normal session prompt stack: <= 20000 tokens
heavy evidence session stack: <= 12000 tokens
minimal emergency stack: <= 5000 tokens

S.5 - Prompt budget classes

Each context stack must declare a budget class.

budget_class: minimal | normal | heavy | emergency

Definitions:

    minimal: less than 5000 tokens;

    normal: less than 12000 tokens;

    heavy: less than 20000 tokens;

    emergency: less than 3000 tokens.

Emergency stacks are used when the conversation is long or the context window is already crowded.
Part 3 - Prompt structure canon
P.1 - Mandatory metadata header

Every prompt file must start with a YAML metadata header.

Required fields:

---
id: prompt_id
name: Human Readable Prompt Name
version: 1.0
status: draft
token_count: 0
tokenizer: cl100k_base
lang: en-US
group: CORE
type: RULE
load_mode: always_on
trigger_keywords: []
human_commands: []
depends_on: []
conflicts_with: []
requires_evidence: false
last_validated: null
last_validated_with_library: null
description: One sentence description.
owner: prompt_library
---

A prompt without a complete header is rejected.
P.2 - Allowed prompt types

A prompt file must have exactly one type.

Allowed types:

RULE:
A constraint the AI must obey.

COMMAND:
An action the AI performs on demand.

PROTOCOL:
A sequence of steps for a workflow.

REFERENCE:
A lookup table the AI reads but does not execute.

TEMPLATE:
A reusable output structure.

CHECKLIST:
A verification list used before accepting something.

INDEX:
A human or machine navigation file.

Do not mix types in one file.
P.3 - One responsibility per prompt

A prompt owns one topic.

Split the prompt if its description requires:

    "and";

    "also";

    "plus";

    more than one main verb.

Examples:

Bad:

Patch creation and validation and freeze rules.

Good:

Defines how a surgical patch is created.

Defines how installed patches are validated.

Defines how freeze gates are reviewed.

P.4 - Imperative language only

Use strong operational language.

Allowed:

    MUST;

    NEVER;

    ALWAYS;

    STOP;

    DO;

    REPORT;

    CLASSIFY;

    CONFIRM.

Avoid:

    should;

    maybe;

    consider;

    try to;

    it is recommended;

    where possible;

    if convenient.

Weak language creates weak compliance.
P.5 - Measurable criteria

Replace vague words with measurable criteria.

Bad:

Keep files clean and not too large.

Good:

A normal Python module must stay at or below 500 lines. If a file exceeds 500 lines, stop and request the module size governance prompt.

Bad:

Use good tests.

Good:

Every patch must include at least one focused test that fails before the patch and passes after the patch.

P.6 - Standard closing self-check

Every RULE prompt must end with:

Before responding, verify whether this rule applies to the current task.
If the rule applies and is about to be violated, stop and respond:
RULE ALERT: [rule description]
Governing prompt: [prompt id]
Required action: load prompt, modify plan, or request explicit human override.

P.7 - No hardcoded project paths

Prompts must not contain fixed absolute paths.

Use placeholders:

[PROJECT_ROOT]
[PATCH_NAME]
[VALIDATION_CMD_1]
[BACKUP_ROOT]
[EVIDENCE_DIR]

The dispatcher or human fills placeholders.
P.8 - No hidden assumptions

Every prompt must declare its assumptions.

Example:

assumptions:
  - The project is Python-based.
  - The human performs GUI smoke testing.
  - The AI does not freeze patches.

If a prompt only works for a specific stack, it must declare that.
Part 4 - Prompt grouping canon
G.1 - Canonical groups

Every prompt belongs to exactly one main group.

CORE:
Universal always-on rules.

COMMUNICATION:
Human-AI command vocabulary and handshake rules.

PATCH:
Patch creation, delivery, backup, restore, and install rules.

CODE:
Coding standards and implementation rules.

ARCHITECTURE:
Ownership, layers, boundaries, module limits, dependency direction.

VALIDATION:
Tests, py_compile, regression, workflow validation, architecture validation.

GOVERNANCE:
Freeze, override, debt ledger, patch registry.

SESSION:
Session start, mid-session re-anchor, end-session handoff.

REFERENCE:
Tables, taxonomies, definitions, examples.

PROMPT_LIBRARY:
Rules for writing, auditing, testing, and freezing prompts themselves.
G.2 - Always-on prompts

Always-on prompts are loaded at every session start.

Limit:

maximum number: 3
maximum total size: 5000 tokens

Recommended always-on set:

    core_kernel

    human_ai_command_vocabulary

    safety_and_stop_controls

Everything else should be on-demand.
G.3 - On-demand prompts

Most prompts must be on-demand.

They are loaded only when:

    the human uses a command;

    the AI requests them with NEED;

    a context stack requires them;

    a rule alert is triggered.

G.4 - Context stacks

A context stack is a named ordered group of prompts.

Examples:

SESSION_START:
Loads the kernel and command vocabulary.

NEW_PATCH:
Loads patch protocol, code rules, owner box rules, and validation expectations.

ARCH_REVIEW:
Loads architecture rules, ownership rules, module size rules, dependency rules.

VALIDATE_FULL:
Loads validation chain, failure classification, structured logging.

FREEZE_REVIEW:
Loads freeze gate, override rules, debt ledger, regression requirements.

HANDOFF:
Loads handoff template, session summary rules, next-step format.

PROMPT_AUDIT:
Loads this canon, prompt audit checklist, prompt rewrite rules.
G.5 - Every stack has an entry condition and exit condition

Each stack must define:

entry_condition: when this stack is loaded
exit_condition: when this stack stops applying

Example:

stack: NEW_PATCH
entry_condition: Human says PATCH or NEW_PATCH.
exit_condition: Patch is frozen, abandoned, or superseded.

This prevents old prompts from contaminating the next phase.
Part 5 - Human-AI communication canon
C.1 - Human command vocabulary

The human uses a small stable command vocabulary.

Primary commands:

START:
Begin a session.

PATCH:
Begin a new patch.

ARCH:
Perform architecture review.

VALIDATE:
Run validation chain.

FREEZE:
Review freeze gates.

HANDOFF:
Generate session handoff.

AUDIT_PROMPTS:
Start prompt library audit.

LOAD:
Force-load specific prompt ids.

NEED:
AI requests missing prompts.

STATUS:
Report current active stack and task state.
C.2 - Meta-command prefix

All meta-commands use the prefix:

!/

Reserved meta-commands:

!/stop
!/resume
!/redirect
!/status
!/help
!/load
!/override
!/direct
!/end-patch
!/end-session

No normal prompt may use this prefix for another purpose.
C.3 - AI NEED protocol

When the AI detects that a required prompt is missing, it must not guess.

It must respond:

To proceed with [task], I need prompts:
- [prompt_id_1]&#58; [reason]
- [prompt_id_2]&#58; [reason]

Please LOAD these prompts or explicitly override.

The human responds:

LOAD prompt_id_1 prompt_id_2

The AI then confirms:

Prompts loaded. Proceeding with [task].

C.4 - AI rule alert protocol

When the AI detects a likely violation, it must stop.

Required format:

RULE ALERT: [specific rule]
Governing prompt: [prompt_id]
Current evidence: [what triggered the alert]
Required action: load governing prompt, change plan, or request human override.

Example:

RULE ALERT: The target module has 501 lines and exceeds the 500-line limit.
Governing prompt: architecture_module_size_rule
Current evidence: app/gui/tab7.py has 501 lines.
Required action: load architecture_module_size_rule before modifying this file.

C.5 - Confidence interrupt

The human can stop the system at any time.

!/stop

The AI must immediately stop and report:

Stopped.
Current task:
Active prompt stack:
Last completed step:
Next pending step:
Waiting for !/resume or !/redirect.

C.6 - AI must acknowledge commands

Every human command must receive a short acknowledgment before action.

Example:

Command received: PATCH.
I will load the NEW_PATCH stack and ask for scope.

Part 6 - Prompt loading canon
Ld.1 - Load modes

Every prompt has one load mode.

always_on:
Loaded at every session start.

stack:
Loaded as part of a named context stack.

need:
Loaded when AI requests it.

manual:
Loaded only by explicit human command.

reference_only:
Not injected unless specifically needed; usually summarized or queried.

deprecated:
Not used unless restoring old behavior.
Ld.2 - Load priority

Every prompt has priority.

priority: critical | high | normal | low

Critical:
Safety, terminal preservation, freeze authority, human stop command.

High:
Patch protocol, validation protocol, architecture ownership.

Normal:
Style, formatting, documentation, handoff.

Low:
Examples, optional heuristics, teaching notes.
Ld.3 - Conflict behavior

If two prompts conflict, the AI must stop.

It must report:

PROMPT CONFLICT:
Prompt A:
Prompt B:
Conflict:
Resolution needed:

No prompt conflict may be silently resolved by the AI.
Ld.4 - Dependency behavior

If prompt A depends on prompt B, prompt B must load first.

Dependency order is deterministic.

The dispatcher must reject circular dependencies.
Ld.5 - Active stack visibility

The AI must be able to report the current active stack.

Human command:

!/status

AI response:

Active stack:
Loaded prompts:
Current phase:
Missing prompts:
Potential conflicts:

Part 7 - Prompt audit canon
A.1 - Audit step 1: inventory

Inventory every prompt file.

For each file, record:

    filename;

    id;

    group;

    type;

    version;

    status;

    token count;

    description;

    triggers;

    dependencies;

    conflicts;

    missing metadata fields;

    weak language count;

    duplicate candidate score;

    oversized flag;

    mixed-type flag.

Output:

audit_report_v1.csv

Do not edit during inventory.

Inventory first, diagnose second, rewrite third.
A.2 - Audit step 2: classify

Assign each prompt one type and one group.

If a prompt cannot be classified cleanly, mark:

MIXED_TYPE

If a prompt appears to belong to multiple groups, choose the real owner group and move the other content elsewhere.
A.3 - Audit step 3: detect duplicates

Detect duplicates at three levels.

Exact duplicate:
Same rule, same meaning.

Semantic duplicate:
Same instruction in different words.

Scope duplicate:
Two prompts claim ownership of the same behavior.

Actions:

    merge exact duplicates;

    rewrite semantic duplicates into one canonical rule;

    resolve scope duplicates by assigning one owner prompt.

One rule must live in one prompt.
A.4 - Audit step 4: detect conflicts

Flag conflict when two prompts give incompatible instructions.

Examples:

    one prompt says always deliver ZIP;

    another prompt says paste full code in chat;

    one prompt says maximum 500 lines;

    another prompt says file length does not matter.

Every conflict must be resolved before freeze.

No conflict can be deferred into automation.
A.5 - Audit step 5: remove weak language

Replace weak phrasing.

Examples:

should -> MUST
consider -> EVALUATE and REPORT
try to -> DO
where possible -> IF NOT POSSIBLE, REPORT WHY
recommended -> REQUIRED

Replace vague quality words.

clean -> passes lint and has no unused imports
small -> below the defined token or line threshold
safe -> has backup, restore, and validation path
good -> meets listed acceptance criteria

A.6 - Audit step 6: split oversized prompts

Split prompts when:

    token count exceeds limit;

    multiple types are mixed;

    multiple groups are mixed;

    multiple workflows are mixed;

    one prompt has too many triggers.

Never split blindly.

For every split:

    create new prompt files;

    assign headers;

    assign dependencies;

    update index;

    test stacks;

    deprecate old prompt;

    remove old prompt only after freeze.

A.7 - Audit step 7: build human index

Generate:

PROMPT_INDEX.md

It must include:

    prompt id;

    name;

    group;

    type;

    token count;

    description;

    when to use;

    when not to use;

    trigger words;

    dependencies;

    conflicts;

    common stacks;

    example human commands.

The human index is for decision support.

It is not the machine routing file.
A.8 - Audit step 8: build machine index

Generate:

prompt_index.json

It must include:

    prompts;

    stacks;

    dependencies;

    conflicts;

    triggers;

    token budgets;

    macros;

    deprecated prompts;

    aliases.

This file is the future dispatcher contract.
A.9 - Audit step 9: freeze the prompt library

After audit, issue:

freeze prompt_library_v1.0

Freeze means:

    prompt files are accepted;

    prompt index is accepted;

    stack definitions are accepted;

    tests pass;

    future changes require a new version.

Part 8 - Prompt testing canon
T.1 - Header validation test

Every prompt must pass metadata validation.

Fail if:

    header missing;

    required field missing;

    invalid group;

    invalid type;

    invalid load mode;

    invalid status;

    missing token count;

    token count stale.

T.2 - Token budget test

Every context stack must be measured.

Fail if:

    stack exceeds configured token budget;

    always-on stack exceeds 5000 tokens;

    emergency stack exceeds 3000 tokens.

T.3 - Dependency test

Every stack must resolve in deterministic order.

Fail if:

    dependency missing;

    circular dependency;

    prompt references unknown prompt id;

    deprecated prompt is used without explicit permission.

T.4 - Conflict test

If two prompts conflict, loading both must trigger an alert.

Fail if the conflict is silently ignored.
T.5 - Rule compliance test

Every RULE prompt must have at least one compliance test.

Test pattern:

    load rule prompt;

    give AI a scenario where violation is tempting;

    verify AI stops or alerts instead of violating.

T.6 - Command behavior test

Every COMMAND prompt must have at least one behavior test.

Test pattern:

    load command prompt;

    issue command;

    verify output format and action match expected behavior.

T.7 - Protocol sequence test

Every PROTOCOL prompt must have at least one sequence test.

Test pattern:

    load protocol;

    ask AI to perform workflow;

    verify steps occur in correct order;

    verify stop conditions are respected.

T.8 - Stack smoke test

Every context stack must be tested as a composed unit.

Required stacks:

    SESSION_START;

    NEW_PATCH;

    ARCH_REVIEW;

    VALIDATE_FULL;

    FREEZE_REVIEW;

    HANDOFF;

    PROMPT_AUDIT.

Part 9 - Prompt lifecycle canon
V.1 - Versioning

Use:

major.minor

Major version changes:

    new behavior;

    removed rule;

    changed dependency;

    incompatible command vocabulary;

    changed stack behavior.

Minor version changes:

    clearer wording;

    token optimization;

    examples improved;

    typo fixes;

    formatting.

V.2 - Status values

Allowed statuses:

draft
audit
validated
frozen
deprecated
retired

Meaning:

draft:
Prompt is being written.

audit:
Prompt exists but has not passed audit.

validated:
Prompt passed tests but is not frozen.

frozen:
Prompt is accepted as part of the library.

deprecated:
Prompt is replaced but kept for compatibility.

retired:
Prompt is no longer used.
V.3 - Deprecation rule

Do not delete replaced prompts immediately.

When replacing a prompt:

status: deprecated
replaced_by: new_prompt_id
deprecation_date: YYYY-MM-DD

Keep deprecated prompts for at least 30 days or until the next stable library freeze.
V.4 - Changelog

Every prompt must have a changelog.

Either external:

prompt_id.changelog.md

Or embedded:

changelog:
  - date: YYYY-MM-DD
    version: 1.1
    change: Clarified module size alert.
    reason: AI failed to stop when module exceeded 500 lines.

V.5 - Prompt library release

Each stable prompt library version must produce:

prompt_library_release_vX.Y/
  prompts/
  PROMPT_INDEX.md
  prompt_index.json
  audit_report.csv
  stack_budget_report.csv
  prompt_tests_report.json
  changelog.md

Part 10 - Initial canonical prompt set

Start with this set before creating more prompts.
Always-on prompts
core_kernel

Type: PROTOCOL
Group: CORE
Purpose: Defines role split, evidence-first rule, no auto-freeze, no terminal clearing, and command awareness.
human_ai_command_vocabulary

Type: REFERENCE
Group: COMMUNICATION
Purpose: Defines START, PATCH, ARCH, VALIDATE, FREEZE, HANDOFF, LOAD, NEED, and meta-commands.
safety_and_stop_controls

Type: RULE
Group: COMMUNICATION
Purpose: Defines !/stop, !/resume, !/redirect, !/override, and AI stop behavior.
On-demand prompts
evidence_first_protocol

Type: PROTOCOL
Group: CORE
Purpose: Defines what evidence must be read before coding or auditing.
patch_creation_protocol

Type: PROTOCOL
Group: PATCH
Purpose: Defines surgical patch creation, scope declaration, and changed-file limits.
code_implementation_rules

Type: RULE
Group: CODE
Purpose: Defines coding standards, file limits, formatting, and dependency constraints.
architecture_owner_box_rules

Type: RULE
Group: ARCHITECTURE
Purpose: Defines ownership, duplicate owner detection, layer boundaries, and module responsibility.
module_size_governance

Type: RULE
Group: ARCHITECTURE
Purpose: Defines maximum line counts and what to do when a file exceeds the limit.
validation_chain_protocol

Type: PROTOCOL
Group: VALIDATION
Purpose: Defines py_compile, focused tests, regression tests, workflow validation, architecture validation, and GUI smoke checklist.
failure_classification_reference

Type: REFERENCE
Group: VALIDATION
Purpose: Defines patch-caused, existing-unrelated, stale evidence, environmental, missing dependency, manual GUI needed, and unknown.
freeze_gate_protocol

Type: PROTOCOL
Group: GOVERNANCE
Purpose: Defines the freeze gates and confirms only the human can freeze.
handoff_generation_command

Type: COMMAND
Group: SESSION
Purpose: Generates the session handoff document.
prompt_audit_protocol

Type: PROTOCOL
Group: PROMPT_LIBRARY
Purpose: Runs the audit process defined in this canon.
prompt_rewrite_rules

Type: RULE
Group: PROMPT_LIBRARY
Purpose: Defines how to rewrite weak prompts into imperative, measurable language.
Part 11 - Standard context stacks
SESSION_START stack

Purpose:
Start a normal engineering session.

Prompts:

    core_kernel

    human_ai_command_vocabulary

    safety_and_stop_controls

Entry condition:
Human says START.

Exit condition:
Session ends.
NEW_PATCH stack

Purpose:
Begin a new surgical patch.

Prompts:

    core_kernel

    patch_creation_protocol

    code_implementation_rules

    architecture_owner_box_rules

    validation_chain_protocol

Entry condition:
Human says PATCH or NEW_PATCH.

Exit condition:
Patch is frozen, abandoned, or explicitly ended.
ARCH_REVIEW stack

Purpose:
Review ownership, layers, file size, and dependency direction.

Prompts:

    core_kernel

    architecture_owner_box_rules

    module_size_governance

    failure_classification_reference

Entry condition:
Human says ARCH or AI detects ownership risk.

Exit condition:
Architecture review is completed or converted into a patch.
VALIDATE_FULL stack

Purpose:
Run full validation.

Prompts:

    core_kernel

    validation_chain_protocol

    failure_classification_reference

Entry condition:
Human says VALIDATE.

Exit condition:
Validation passes, fails with classification, or human stops.
FREEZE_REVIEW stack

Purpose:
Review whether a patch can be frozen.

Prompts:

    core_kernel

    validation_chain_protocol

    freeze_gate_protocol

    failure_classification_reference

Entry condition:
Human says FREEZE.

Exit condition:
Human freezes, rejects freeze, or requests further validation.
HANDOFF stack

Purpose:
Generate session handoff.

Prompts:

    core_kernel

    handoff_generation_command

Entry condition:
Human says HANDOFF.

Exit condition:
Handoff is generated and reviewed.
PROMPT_AUDIT stack

Purpose:
Audit and canonicalize the prompt library.

Prompts:

    core_kernel

    prompt_audit_protocol

    prompt_rewrite_rules

    human_ai_command_vocabulary

Entry condition:
Human says AUDIT_PROMPTS.

Exit condition:
Prompt library is frozen or audit is paused.
Part 12 - Macro command canon
K.1 - Macro commands

Macro commands combine stack loading and AI action.

Required macros:

START_DAY
NEW_PATCH <name>
ARCH_REVIEW <target>
VALIDATE_FULL <patch_name>
FREEZE_REVIEW <patch_name>
HANDOFF_SESSION
AUDIT_PROMPTS
STATUS

K.2 - Macro command examples

START_DAY

Loads SESSION_START and asks the AI to confirm readiness.

NEW_PATCH tab7_output_layout

Loads NEW_PATCH and asks the AI to declare scope.

ARCH_REVIEW app/gui/tab7.py

Loads ARCH_REVIEW and asks the AI to identify owner boxes and risks.

VALIDATE_FULL tab7_output_layout

Loads VALIDATE_FULL and asks the AI to run or plan validation.

FREEZE_REVIEW tab7_output_layout

Loads FREEZE_REVIEW and asks the AI to report gate status.

AUDIT_PROMPTS

Loads PROMPT_AUDIT and starts prompt inventory.
K.3 - Command chaining

The dispatcher may later support chaining:

NEW_PATCH tab7_output_layout && VALIDATE_FULL tab7_output_layout

Until the dispatcher exists, chaining is manual.
Part 13 - Human index canon

The human index must be easy to read.

It must answer:

    Which prompt do I use now?

    Which command do I type?

    Which stack is loaded?

    What does the AI do next?

    When should I stop or redirect?

The human index must include these tables:

    Prompt list by group.

    Prompt list by command.

    Context stack list.

    Macro command list.

    AI NEED examples.

    RULE ALERT examples.

    Deprecated prompts.

    Common workflow recipes.

Example workflow recipe:

Goal: Start a new coding patch.

Human command:
NEW_PATCH patch_name

Loaded stack:
NEW_PATCH

AI must respond with:
- current evidence needed;
- scope;
- owner box;
- risk score;
- proposed changed files;
- files not touched;
- request for human acknowledgment.

Part 14 - Machine index canon

The machine index must be deterministic.

It must not rely on vague descriptions.

Required structure:

{
  "library_version": "1.0",
  "tokenizer": "cl100k_base",
  "prompts": {},
  "stacks": {},
  "macros": {},
  "aliases": {},
  "deprecated": {},
  "budgets": {}
}

Each prompt entry must include:

{
  "file": "prompts/core/core_kernel.md",
  "group": "CORE",
  "type": "PROTOCOL",
  "status": "frozen",
  "token_count": 0,
  "load_mode": "always_on",
  "triggers": ["START"],
  "depends_on": [],
  "conflicts_with": [],
  "description": "Defines universal session behavior."
}

Part 15 - Build order after canonization

Do not build the dispatcher until these artifacts exist:

prompts/
PROMPT_INDEX.md
prompt_index.json
audit_report_v1.csv
stack_budget_report.csv
prompt_tests_report.json
prompt_library_changelog.md

Correct build order:

    Create prompt folder.

    Add all existing prompts as raw imports.

    Run inventory.

    Classify each prompt.

    Rewrite weak language.

    Split oversized prompts.

    Merge duplicates.

    Resolve conflicts.

    Assign context stacks.

    Build human index.

    Build machine index.

    Run prompt tests.

    Freeze prompt library.

    Build CLI dispatcher.

Part 16 - Freeze gates for prompt library

The prompt library can be frozen only if all gates are green.

    Every prompt has complete metadata.

    Every prompt has valid token count.

    No normal prompt exceeds 2000 tokens.

    Always-on stack is at or below 5000 tokens.

    No duplicate rules remain.

    No unresolved conflicts remain.

    Every context stack resolves dependencies.

    Every stack is under budget.

    Human index exists and is readable.

    Machine index exists and is valid JSON.

    Prompt tests pass or missing tests are documented.

    Human explicitly issues freeze command.

Freeze command:

freeze prompt_library_v1.0

Part 17 - Final rule

The dispatcher does not decide prompt architecture.

The prompt library decides prompt architecture.

The dispatcher only executes the already frozen architecture.

If the prompt library is messy, the dispatcher will amplify the mess.

If the prompt library is canonical, the dispatcher becomes powerful, safe, and scalable.

The most important additions I made are:

    One kernel prompt only as the true always-on base. This prevents the “giant book” problem.

    Load modes: always-on, stack, need, manual, reference-only, deprecated.

    Prompt lifecycle: draft → audit → validated → frozen → deprecated → retired.

    Prompt freeze gates, separate from code freeze gates.

    Human index and machine index separation. The human needs decision help; the dispatcher needs deterministic JSON.

    Initial canonical prompt set, so you do not start from a blank page or from 30 chaotic prompts.

    RULE ALERT and NEED as formal protocols, so the AI does not silently proceed when a governing prompt is missing.

My recommendation for the next step is: create Prompt Library Audit Session 1, where the only goal is inventory and classification. No rewriting yet. Just list every prompt, token count, type, group, duplicate risk, conflict risk, and whether it should survive.

0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
File
0000 0.1.1 PYARCHITECT REASONER delivery style mandatory v1.1.md
File
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3.md
File
0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4.md
File
0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2.md
File
0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md
File
0000 4.2 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v3.0.md
File
0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md
File
0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md
File
0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.1.md
File
0000 8.0 REASONER ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md
File
0000 9.1 T9T013_teach_ai_prompt_authoring_complete_lifecycle_roadmap.md
File
0000 9.2 T9T013_other_ai_review_handoff.md
File
0000 10.2 how implement code and send do user.md
File
0000 11 roadmap of implementation prompt.md
File
0000 12 github tutorial.md
File
0000 13 end of day handoff.md
File
0000 14 how organize folder at begining of a project.md
File
0000 15 Box Architecture Canon v1.0 prompt.md
File
0000 PROMPT SUBSTITUTION MAP REASONER v1.1.md
File
the  problem is that instead of (Canon Principle 2) -many unstable prompts  I have many useful prompts for instance if I use One prompt  instead all of the uploaded (and I have many ) , we will miss many important architectural cannonic choices , see some examples. so we must work diferently , with many important prompts called manually by the human partner to help freeze them.

I agree with your correction. These uploads are not “many unstable prompts”; they are many useful specialized governance assets, so the audit method must preserve specialization instead of compressing everything into one master prompt.

You are right. I would revise my previous principle.

The problem is not “many prompts.”
The problem is many prompts without canonical ownership, load rules, substitution rules, and freeze status.

Your uploaded examples prove that many prompts are genuinely useful because they encode different architectural decisions:

    The load-order prompt already defines daily minimum prompts, special prompts used only when needed, precedence, and the rule that AI must request missing prompts before implementation.

    The universal delivery prompt defines the direct-ZIP delivery model, source truth hierarchy, testing honesty, and no-install-script delivery behavior.

    The Teach AI Prompt Authoring roadmap already recognizes the need to inspect existing prompts, decide create vs update vs link, update groups, stacks, indexes, and avoid duplication.

    The Box Architecture canon is too important to compress into a tiny summary because it defines ownership, contracts, private internals, communication routes, tests, and freeze gates.

So the new answer is:

Do not reduce many useful prompts into one prompt. Build a federated prompt canon.

That means:

one small kernel prompt
+ many specialized canonical prompts
+ manual human-controlled loading
+ prompt-by-prompt audit
+ stack-by-stack freeze
+ substitution map
+ conflict ledger
+ human index
+ later dispatcher

The human partner should manually call important prompts while they are being stabilized. The dispatcher comes later, after the manual calls reveal which prompts are truly canonical.
Revised Canon Principle 2

Replace the old principle with this:
Revised Canon Principle 2 - Many Useful Prompts, Controlled Loading

The prompt library may contain many important prompts.

The goal is not to minimize prompt count.

The goal is to eliminate unstable, duplicate, conflicting, outdated, or ownerless prompts.

A large prompt library is acceptable when every prompt has:

    a clear owner responsibility;

    a known loading condition;

    a known dependency list;

    a known conflict list;

    a known substitution history;

    a freeze status;

    a reason to exist separately.

Do not merge important specialist prompts into one master prompt if merging would erase architectural detail.

Use one small always-on kernel plus many manually callable specialist prompts.

The human partner may manually call prompts during the stabilization phase.

Manual prompt calling is not a weakness. It is the audit phase that teaches the future dispatcher what to automate.

A prompt becomes dispatcher-ready only after it survives manual use, audit, conflict review, and freeze.
The better architecture: federated prompt canon

Think of your prompt library as a modular monolith, not as a book.

Each prompt is like a box.
Prompt role	Meaning	Example from your uploads
Kernel prompt	Always-on minimal operating rules	Startup / load order
Delivery protocol	How files are delivered	Universal delivery protocol
Architecture canon	How code ownership works	Box Architecture Canon
Special protocol	Loaded only under special trigger	Large module refactor, hardening triage
Governance protocol	Only after validated freeze	End-of-chat governance update
Handoff template	Transfers state to next chat	Current active workflow handoff
Substitution map	Tells which prompt replaces older prompts	Prompt substitution map
Authoring protocol	Teaches AI how to create/update prompts	T9T013 prompt authoring lifecycle

This is not “too many prompts.”
This is a specialized engineering operating system.
What changes in the audit strategy

The audit should no longer ask:

How do we reduce this to fewer prompts?

It should ask:

Which prompts deserve to remain separate?
Which prompts are obsolete?
Which prompts conflict?
Which prompts are parents?
Which prompts are overlays?
Which prompts are task-specific specialists?
Which prompts should be manually loaded before they are automated?

So the audit needs a stronger classification system.
New classification: prompt survival decision

Each prompt gets one of these outcomes:
Decision	Meaning
KEEP_AS_CANONICAL	Prompt is important and should remain separate
KEEP_AS_SPECIALIST	Prompt is useful only under specific conditions
KEEP_AS_OVERLAY	Prompt modifies another prompt but does not stand alone
MERGE_INTO_PARENT	Prompt repeats another prompt and should be absorbed
SPLIT	Prompt contains multiple responsibilities
DEPRECATE	Prompt was replaced by a newer one
RETIRE	Prompt is no longer used
CONFLICT_REVIEW	Prompt contains rules that contradict another prompt
HUMAN_TEST_REQUIRED	Prompt seems useful but must be manually tried before freeze

This solves your concern: useful prompts are preserved, not compressed.
Critical audit idea: prompt-by-prompt freeze

Do not freeze the entire library at once.

Freeze one prompt at a time, then one stack at a time.
Level 1 - Individual prompt freeze

A prompt can be frozen when:

1. Its purpose is clear.
2. It has no internal contradictions.
3. It has no unresolved conflict with higher-precedence prompts.
4. Its load condition is clear.
5. Its dependencies are known.
6. Its substitutions are known.
7. The human has manually used it successfully at least once.

Level 2 - Stack freeze

A stack can be frozen when:

1. Every prompt in the stack is individually frozen.
2. Prompt order is known.
3. No prompt in the stack conflicts with another.
4. The stack has a clear entry condition.
5. The stack has a clear exit condition.
6. The human has used the full stack successfully.

Level 3 - Library freeze

The prompt library can be frozen when:

1. Core stack is frozen.
2. Daily startup stack is frozen.
3. New patch stack is frozen.
4. Architecture stack is frozen.
5. Validation stack is frozen.
6. Handoff stack is frozen.
7. Substitution map is current.
8. Deprecated prompts are marked.
9. Human index exists.
10. Machine index exists.

This gives you a practical path from many prompts to a stable system.
Very important audit finding from your examples

Your current prompt set already shows why the audit is necessary.

For example, your load-order prompt says normal prompt/source updates should not require an install script, and should be delivered as a direct ZIP with project-relative paths.
The universal delivery protocol says the same: create files in sandbox, validate, deliver one ZIP, and do not require an install script or separate backup-script folder.

But the same load-order file still has old trailing lines saying:

Install script:
- prints install result
- prints manifest and backup path
- then automatically clears screen

Validation script:
- prints all validation output
- waits for Enter twice
- then clears screen

That is a conflict artifact.

It does not mean the prompt is bad. It means the prompt is valuable but needs audit cleanup. The correct audit decision would be:

KEEP_AS_CANONICAL
but flag:
- INTERNAL_CONFLICT
- LEGACY_TAIL
- TERMINAL_LOG_RULE_CONFLICT

Then remove or supersede the obsolete script-clearing lines.

This is exactly why we should not blindly merge or delete prompts. We need a prompt conflict ledger.
Add this to the audit framework: Prompt Conflict Ledger

Every audit should produce:

PROMPT_CONFLICT_LEDGER.md

Each entry:

Conflict ID:
Prompt A:
Prompt B:
Conflict type:
- delivery_model
- terminal_log
- freeze_authority
- source_truth
- governance_path
- module_size
- install_method
- validation_order
- prompt_loading_order

Higher authority:
Decision:
Action:
Status:

Example:

Conflict ID: C001
Prompt A: 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1
Prompt B: 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3
Conflict type: terminal_log / install_method
Issue: 0.1 contains old lines requiring scripts that clear screen, while the active delivery model forbids install-script dependency and preserves output.
Higher authority: Universal delivery protocol + terminal log preservation rule
Decision: remove old script-clearing tail from 0.1 or mark as deprecated text
Status: pending human approval

This is the kind of audit that will make the library professional.
Manual prompt loading should become part of the method

During stabilization, the human should manually call prompts using simple commands.

Example:

AUDIT_PROMPT 0000 15 Box Architecture Canon

AI responds:

Prompt audit started.
Prompt type: ARCHITECTURE_CANON
Recommended status: KEEP_AS_CANONICAL
Conflicts found: none / list
Dependencies: startup canon, delivery protocol
Should remain separate: YES
Freeze recommendation: not frozen yet / freezeable

Example:

TEST_STACK NEW_PATCH

AI responds:

For NEW_PATCH I need:
1. Load order
2. Universal delivery protocol
3. Startup canon
4. Daily loader
5. Box architecture canon
6. Code implementation rules
7. Validation protocol

Missing:
- validation protocol

Please LOAD validation protocol or confirm override.

This is better than immediately automating because the human learns which prompts actually matter.
New prompt audit commands

I suggest these manual commands:

AUDIT_PROMPT <prompt_id>

Audit one prompt.

COMPARE_PROMPTS <prompt_a> <prompt_b>

Check duplicate, overlap, conflict, substitution.

FREEZE_PROMPT <prompt_id>

Freeze one prompt after audit.

DEPRECATE_PROMPT <prompt_id> -> <replacement_id>

Mark old prompt as replaced.

TEST_STACK <stack_id>

Load a candidate stack and check order, dependencies, conflicts, token size.

FREEZE_STACK <stack_id>

Freeze one context stack.

BUILD_HUMAN_INDEX

Create the human-facing prompt index.

BUILD_MACHINE_INDEX

Create the future dispatcher JSON.

PROMPT_CONFLICT_REVIEW

List all unresolved conflicts.

PROMPT_SUBSTITUTION_REVIEW

Update the substitution map.

These commands are the bridge between manual human control and future automation.
The new build order

The right order now becomes:

1. Preserve all uploaded prompts as raw candidates.
2. Create a prompt inventory.
3. Classify each prompt.
4. Compare prompts against the substitution map.
5. Manually audit high-value prompts one by one.
6. Freeze individual prompts.
7. Build candidate stacks manually.
8. Test candidate stacks manually.
9. Freeze stacks.
10. Build human index.
11. Build machine index.
12. Only then build dispatcher.

This respects your point: the human partner helps choose and freeze prompts before automation.
Practical first stack to stabilize

I would start with this stack:

REASONER_DAILY_STARTUP_STACK_CANDIDATE
1. 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3
3. 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4
4. 0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2
5. 0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1
6. 0000 PROMPT SUBSTITUTION MAP REASONER v1.1

Then test special prompts separately:

SPECIAL_PROMPT_ARCHITECTURE
- 0000 15 Box Architecture Canon v1.0

SPECIAL_PROMPT_LARGE_MODULE
- 0000 5.7 Reasoner Large Module Refactor Protocol

SPECIAL_PROMPT_HARDENING
- 0000 8.0 Architecture Hardening Triage Protocol

SPECIAL_PROMPT_PROMPT_AUTHORING
- 0000 9.1 / 9.2 Teach AI Prompt Authoring Lifecycle

SPECIAL_PROMPT_GOVERNANCE_UPDATE
- 0000 4.2 / 4.11 governance update prompt

Do not merge these into the daily startup stack yet. They are too important and too specialized.
Final corrected principle

Your prompt system should not be:

one huge master prompt

and should not be:

30 random prompts loaded by memory

It should be:

manual prompt council first
dispatcher later

The human partner manually calls the important prompts, the AI audits them, the human freezes them, then the dispatcher learns from the frozen stack map.

That is the right architecture.

in cases like this
"
Conflict ID: C001
Prompt A: 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1
Prompt B: 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3
Conflict type: terminal_log / install_method
Issue: 0.1 contains old lines requiring scripts that clear screen, while the active delivery model forbids install-script dependency and preserves output.
Higher authority: Universal delivery protocol + terminal log preservation rule
Decision: remove old script-clearing tail from 0.1 or mark as deprecated text
Status: pending human approval"

it is important to ask user which option will be cannon.

I believe also that  whe must load at beginnig of working day a  prompt exclusively  with the summary of features of each specialized engineering operating prompt , so when ai needs to update or create a code she asks for prompt number 3 or 4 or whatever separatede from other prompts . So I suggest insert all files in a folder  and renumber then, them we audity one by one  and we decide if it is useful , deprecad , if must merge with other or be edited, ate same time create the sumary prompt to ask human  the prompt Ai needs. Agree or have better idea ?  

Yes, I agree with your direction — with one refinement.

You should not renumber the original files immediately. First, place them in a folder and give each one a stable audit ID. Only after audit/freeze should we rename or renumber canonical versions. This avoids breaking references too early.

Your idea is correct:

1. Put all prompts in one prompt-library folder.
2. Create a daily summary/router prompt.
3. Audit prompts one by one.
4. For each conflict, ask the human which rule becomes canon.
5. Decide: useful / edit / merge / deprecated / retired.
6. Build the human index at the same time.
7. Only after that, automate with dispatcher.

The uploaded load-order prompt already supports this direction because it says the AI must request needed prompts before implementation and not proceed if a dependent prompt is missing. It also already separates daily minimum prompts from special prompts such as governance, large-module refactor, and roadmap prompts.
The better name for your summary prompt

I would not call it just “summary prompt.” I would call it:

0000 PROMPT NAVIGATION INDEX v1.0

or:

0000 ENGINEERING PROMPT ROUTER SUMMARY v1.0

Its job is not to contain all rules.

Its job is to answer:

For this task, which specialized prompt files do I need?

So it should contain short descriptions like:

Prompt 03 - Universal Delivery Protocol
Use when: creating, editing, packaging, or sending files.
Purpose: direct ZIP delivery, project-relative paths, no install script.

Prompt 07 - Large Module Refactor Protocol
Use when: a Python file is above 500 lines or the task is a module split.
Purpose: audit first, roadmap second, implementation third.

Prompt 15 - Box Architecture Canon
Use when: changing architecture, ownership, module boundaries, GUI/domain separation.
Purpose: identify owner box and prevent responsibility contamination.

This prompt should be loaded at the beginning of the working day together with the kernel prompts. Then, when the human says:

I want to create a new feature in Tab 7

the AI responds:

For this task, I need:
1. Universal Delivery Protocol
2. Startup Canon
3. Box Architecture Canon
4. Validation Protocol
5. Latest handoff
6. Relevant source files/logs

Please load these prompts or confirm they are already loaded.

That is exactly the human-AI partnership model.
Critical rule: conflicts require human canon decision

You are also right about conflicts.

The AI must not decide canon alone.

For every conflict, the AI should present options:

CONFLICT DECISION REQUIRED

Conflict ID: C001

Prompt A:
0000 0.1 Load Order

Prompt B:
0000 0.8 Universal Delivery Protocol

Conflict:
Prompt A contains old lines saying scripts clear the screen.
Prompt B says normal delivery uses direct ZIP and no install script.

Possible canon choices:

Option A - Universal Delivery wins.
Remove old script-clearing lines from Prompt A.

Option B - Prompt A wins.
Restore install/validation script behavior.

Option C - Split by context.
Direct ZIP is canon for normal prompt/source updates.
Install scripts are allowed only for high-risk special cases.

AI recommendation:
Option A or C.

Human decision required:
Which option becomes canon?

The conflict you gave is a perfect example because your load-order prompt says direct ZIP delivery and no install script, but it also contains an old tail saying install/validation scripts clear the screen. The universal delivery protocol clearly says the ZIP must not require an install script or separate backup-script folder. That is not an AI decision; it is a human canon decision gate.
My refined plan

I would do it in this order:
Phase 1 - Raw prompt archive

Put every prompt into:

prompt_library_raw/

Do not edit yet.

Keep original filenames.
Phase 2 - Assign audit IDs

Create:

PROMPT_AUDIT_REGISTER.md

Example:

P001 - 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1
P002 - 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3
P003 - 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4
P004 - 0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2

Use these audit IDs during discussion. Rename files only later.
Phase 3 - Create the daily prompt navigation index

This is the first canonical prompt to create.

It should contain:

1. Prompt ID
2. Filename
3. Purpose
4. When to load
5. When not to load
6. Depends on
7. Conflicts with
8. Replaces older prompts
9. Human command to request it

This prompt is loaded daily.
Phase 4 - Audit one prompt at a time

For each prompt:

AUDIT_PROMPT P001

AI outputs:

Status: useful / edit / merge / deprecate / retire
Role: kernel / specialist / overlay / reference / governance
Conflicts:
Dependencies:
Suggested canonical edits:
Human decision required:

Phase 5 - Conflict decision sessions

For conflicts, no automatic resolution.

The AI gives:

Option A
Option B
Option C
Recommendation
Consequences
Human canon decision required

Then you decide.
Phase 6 - Freeze individual prompts

After editing and resolving conflicts:

FREEZE_PROMPT P001

Only then is it stable.
Phase 7 - Freeze stacks

After individual prompts are frozen:

FREEZE_STACK DAILY_STARTUP
FREEZE_STACK NEW_PATCH
FREEZE_STACK LARGE_MODULE_REFACTOR
FREEZE_STACK GOVERNANCE_UPDATE

Phase 8 - Build dispatcher

Only after frozen stacks exist.
Important improvement to your renumbering idea

Do not use only numbers as the permanent identity.

Use both:

P001 - audit number
reasoner_load_order - canonical id
original filename - preserved evidence

Why?

Because numbers change when prompts are inserted. Semantic IDs survive.

Best metadata:

audit_id: P001
canonical_id: reasoner_load_order
original_filename: 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
status: audit
decision: pending

Final answer

Yes, I agree.

Your better architecture is:

Manual prompt council first.
Prompt navigation index loaded daily.
Human chooses canon in conflicts.
Audit and freeze prompts one by one.
Freeze stacks after prompts.
Build dispatcher only after the library is stable.

This is stronger than trying to compress everything into one prompt, and safer than automating before the prompt library is canonical.

and prompts must be projects agnostic to be used with any project , what is first step

The first step is not editing the prompts. It is separating universal rules from project-specific facts, because the current files still mix both in several places.

The first step is:
Create a Project-Agnostic Conversion Register

Do not edit the prompts yet.

First, make a register that separates each prompt into:

1. Universal engineering rule
2. Project-specific fact
3. Placeholder needed
4. Candidate generic version
5. Project overlay needed
6. Human canon decision needed

Why this is first: your current prompts contain excellent universal rules, but many are still tied to Project Reasoner, E:\developer_tools, kanda_reasoner_app, specific governance paths, and specific box names. For example, the startup canon says PROJECT_ROOT is dynamic, but also contains Reasoner-specific root paths and box names. The agnostic folder canon already gives the correct model: declare project-specific paths at Step 0 instead of hardcoding them into the rule itself.

So the first artifact should be:

PROMPT_AGNOSTIC_CONVERSION_REGISTER.md

With one row per prompt:

Audit ID:
Original filename:
Current status:
Universal value:
Project-specific content found:
Must become placeholder:
Should become project overlay:
Conflicts:
Human decision required:
Recommended action:

Example:

Audit ID: P003
Original filename: 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4

Universal value:
- Evidence first.
- Source truth over memory.
- Identify owner box before editing.
- Dynamic PROJECT_ROOT.
- One box per responsibility.
- Direct ZIP delivery.
- User validation before freeze.

Project-specific content found:
- Project Reasoner identity.
- E:\developer_tools.
- kanda_reasoner_app.
- Static Data Collector / Runtime Collector / V10 Reader names.
- ACTIVE_PROJECT_ GOVERNANCE path.

Must become placeholder:
- [PROJECT_NAME]
- [WORKSPACE_ROOT]
- [PRODUCT_PACKAGE]
- [PROJECT_ROOT]
- [GOVERNANCE_FOLDER]
- [BOX_REGISTRY]

Should become project overlay:
- Reasoner-specific box registry.
- Reasoner-specific governance folder.
- Reasoner-specific daily source request.

Recommended action:
Split into:
1. project_agnostic_startup_kernel
2. reasoner_project_overlay

The key rule

Every prompt must become either:

PROJECT-AGNOSTIC CANON

or:

PROJECT OVERLAY

Never both.
The structure I recommend

prompt_library/
  00_router/
    engineering_prompt_router_summary.md

  01_agnostic_core/
    agnostic_startup_kernel.md
    universal_delivery_protocol.md
    evidence_first_protocol.md
    human_ai_command_vocabulary.md

  02_agnostic_architecture/
    box_architecture_canon.md
    module_size_governance.md
    architecture_hardening_protocol.md

  03_agnostic_patch/
    surgical_patch_protocol.md
    validation_chain_protocol.md
    freeze_protocol.md

  04_agnostic_session/
    handoff_template.md
    governance_update_template.md

  05_project_overlays/
    reasoner_overlay.md
    eeg_overlay.md
    future_project_overlay.md

  90_raw_imports/
    original_uploaded_prompts/

  99_audit/
    PROMPT_AGNOSTIC_CONVERSION_REGISTER.md
    PROMPT_CONFLICT_LEDGER.md
    PROMPT_SUBSTITUTION_MAP.md

Most important design decision

The daily loaded router prompt must be project-agnostic.

It should not say:

Use E:\developer_tools
Use kanda_reasoner_app
Use Reasoner governance files

It should say:

First load the project overlay for the active project.
Then use the overlay to resolve:
- project name
- project root
- package path
- governance folder
- validation commands
- box registry
- delivery exceptions

That way the same system works for:

Project Reasoner
EEG app
future PySide app
CLI tool
medical paper automation app
any Python project

First actual work session

Start with this exact task:

AUDIT SESSION 1 - Project-Agnostic Separation

Goal:
Create PROMPT_AGNOSTIC_CONVERSION_REGISTER.md.

Do not rewrite prompts.
Do not rename prompts.
Do not merge prompts.
Do not deprecate prompts yet.

For each uploaded prompt:
1. assign audit ID;
2. identify universal rules;
3. identify project-specific facts;
4. list placeholders needed;
5. decide if it should become agnostic canon, project overlay, or both after split;
6. flag conflicts requiring human decision.

My answer in one sentence

The first step is to inventory all prompts and create a Project-Agnostic Conversion Register, separating universal engineering rules from project-specific overlays before editing, renaming, merging, or automating anything.


