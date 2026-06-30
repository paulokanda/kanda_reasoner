first_prompts_to_ai.zip
Zip Archive
prompt_library.zip
Zip Archive
tell_AI_read_before_all.md
File
zz_read_only_if_modifying_startup_delivery.md
File

Vou verificar a ordem de leitura exigida, abrir o ZIP de startup e confirmar arquivo por arquivo antes de qualquer tarefa do projeto.

STARTUP PACK LOAD CHECK

Files recognized:
0. 00_START_HERE_FOR_AI.md - loaded - boot file with first-position routing overrides, startup rules, and required load-check contract

    01_ai_prompt_request_canon.md - loaded - canonical prompt request and routing intake rules

    02_prompt_navigation_index.md - loaded - navigation index for selecting prompt paths and routing assets

    03_GROUP_ASSIMILATION_INDEX.md - loaded - group-level assimilation index for governed prompt loading

    04_FOLDER_ASSIMILATION_CARDS_INDEX.md - loaded - folder card index for selecting relevant active prompt areas

    05_start_of_day_master_stack.md - loaded - start-of-day master stack and session initialization behavior

    06_session_start_upload_checklist.md - loaded - checklist for required startup and project upload files

    07_daily_patch_delivery_guardrails.md - loaded - daily patch delivery safeguards and validation expectations

    08_handoff_at_end_of_work.md - loaded - end-of-work handoff requirements

    09_patch_install_delivery_error_register.md - loaded - patch install and delivery error register

    10_prompt_router_reasoner_startup_check.md - loaded - startup check for prompt router behavior

    11_chatgpt_kanda_routing_choice_output_protocol.md - loaded - required routing-choice output protocol for ChatGPT

    12_error_memory_ai_formulary_startup_canon.md - loaded - startup canon for compact error-memory handling

    09_active_project_freeze_context.md - loaded - active project freeze-memory context and status

    README_STARTUP_PROMPT_REQUEST_KERNEL.md - loaded - startup pack purpose, source rules, and usage instructions

    STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json - loaded - generated startup pack manifest and metadata

Startup status:
COMPLETE

Routing behavior:
Startup routing is active. Governed project work must be routed through the startup indexes before implementation. prompt_library.zip is available as the canonical on-demand prompt source, but it should not be opened broadly at startup; only the specific selected prompt path should be retrieved when routing requires it. Bypass requests, direct implementation requests without required context, and startup-delivery modifications must follow the required guarded paths.

Next action:
Waiting for all files (Project Files) from second_prompt_files folder

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
What is kanda_reasoner for gime a brief summary of what each fo its tabs do.

KANDA_PY_TOOLS.5.11.25.7H.zip
Zip Archive
are inside the upload  any tool that could add  value to kanda_reasoner?

Yes. The upload contains several tools that could add value to KANDA Reasoner, but I would treat them as an idea/source incubator, not as code to copy directly.

I inspected the ZIP at a high level: it has about 1,420 files, including about 175 Python files. Some are useful, but some are old, EEG-specific, duplicated, contain encoding problems, or do not parse cleanly as Python. So the safe path is: extract concepts, then rewrite/adapt into KANDA Reasoner style.
Best candidates to add value
Upload tool	Could improve this KANDA tab	Value
AI Memory Map Builder / Brotherhood Analyzer	Brain Navigator, Refactor Report, Show Project to AI	Strongest candidate. It builds function/class/import/call-graph style maps and group reports. This could make Brain Navigator more “living project memory” instead of mostly navigation.
ProjectAnalyzer / On Every Push Tool	Architecture Review, Workflow Review, Engineering Safety	Generates repeatable reports: complexity, dependency hotspots, tech debt, architecture violations, quality gates. KANDA already has parts of this, but these could strengthen the “daily health scan” layer.
Function Indexer	Project Q&A, Brain Navigator, Symbol Atlas	Small and useful. It indexes functions across the project. Good candidate for a clean integration because it is simpler than the big analyzers.
GUI Specs Tool	Workflow Review, tab validation	Very relevant. It tries to infer GUI user flows from PySide/PyQt code. Could help KANDA detect when tab workflows, buttons, or expected UI sequences are incomplete.
Risk Change Radar	Engineering Safety, Patch Delivery gates	Useful concept: analyze staged diffs and identify risky change areas before patch delivery. KANDA already has risk logic, but this could enrich the risk report.
ADR Writer	Architecture Review, Freeze Feature After Update	Could generate small Architecture Decision Records after important validated changes. Good fit for traceability and freeze memory.
JSON In, Advice Out	Project Q&A, Error Memory, Show Project to AI	Useful pattern: take JSON evidence and produce human-readable advice. KANDA has lots of JSON handoff files, so this concept fits well.
Property Test Generator	Engineering Safety, Reliability Guidance	Valuable idea, but the uploaded file has syntax issues. Better to rewrite the concept cleanly than import it.
LLM SAST Assist	Engineering Safety	Could improve security review by combining Bandit/static analysis with local AI explanation. Useful, but should be optional and offline-safe.
File Path Copier	Show Project to AI, Prompt Library	Good UX idea for manually selecting relevant project files, but KANDA already has more advanced source archive/handoff logic. It could still improve manual file selection.
Already mostly covered by KANDA Reasoner

Some uploaded tools overlap with things KANDA Reasoner already appears to have:
Upload tool	Current overlap
Crash Triage	KANDA already has Engineering Safety / crash triage concepts.
Runtime Map	KANDA already has runtime collector and runtime trace evidence.
Release Notes Generator	KANDA already has governance/release notes logic.
Docstring Creator	KANDA already has the Docstring Assistant tab.
Formatter Pro	Potentially useful, but risky. KANDA should not add aggressive auto-formatting unless it is gated by diff/preview/validation.
Dependency Risk Briefs	Could enhance Engineering Safety, but likely not a new tab.
Lower priority or not directly useful

These are more EEG-app-specific or less aligned with KANDA Reasoner:
Tool	Reason
Synthetic EEG Cases	Useful for an EEG app, not for KANDA Reasoner itself.
Signal QA Assistant	EEG/signal-specific.
Labeling Copilot	EEG/signal-labeling-specific.
Preset Curator	More useful for an EEG visualization GUI than KANDA Reasoner.
Runtime GPU / LLM Guardrails	Useful only if KANDA deeply integrates local GPU models. Otherwise optional.
Contextual Tooltips	Could improve help UX, but not core project reasoning.
Important caution

I would not import the ZIP directly into KANDA Reasoner. I found signs of an older experimental toolbox: some Python files do not parse cleanly, there are cached files, logs, temporary files, EEG-specific material, and at least one filename suggests a token/password note. That should be scrubbed and never merged into the project root.

Best next move: create a small “candidate integration audit” inside KANDA Reasoner, starting with only 3 tools:

    Function Indexer

    GUI Specs

    AI Memory Map / Brotherhood Analyzer

These three give the best value-to-risk ratio.

each one will be a new tab?

No. Each uploaded tool should not become a new tab. That would make KANDA Reasoner too crowded and harder to maintain.

Better rule:

New tab only if the tool represents a complete workflow.
Subtool/button/card if it supports an existing workflow.
Internal service if it only produces data for other tabs.

Suggested placement:
Tool / idea	Best integration	New tab?
AI Memory Map / Brotherhood Analyzer	Strengthen Brain Navigator and Refactor Report	Maybe later, but not first
Function Indexer	Internal engine used by Brain Navigator, Project Q&A, Architecture Review	No
GUI Specs Tool	Add as a section inside Workflow Review	No
ProjectAnalyzer / On Every Push	Add as “Project Health Scan” inside Engineering Safety or Architecture Review	No
Risk Change Radar	Add to Engineering Safety / patch preflight	No
ADR Writer	Add to Architecture Review and Freeze Feature After Update	No
JSON In, Advice Out	Add to Project Q&A as a mode	No
Property Test Generator	Add to Engineering Safety as “Generate test ideas”	No
LLM SAST Assist	Add to Engineering Safety as optional security review	No
File Path Copier	Add to Show Project to AI as manual file selection helper	No
Contextual Tooltips	App-wide help/UX improvement	No
EEG-specific tools	Keep out of KANDA Reasoner unless building a separate EEG app/plugin	No

The only possible new tab I would consider is:
Possible new tab: Project Intelligence Lab

This would be an experimental/incubator tab where old tools can be tested before being promoted into real KANDA tabs.

It could contain:

    Function Indexer

    AI Memory Map

    GUI Specs preview

    Risk Radar preview

    JSON advice preview

But for production, I would avoid many new tabs. KANDA Reasoner already has good top-level tabs. The uploaded tools should mostly become features inside existing tabs, not new tabs.

these are the tools you think valuable:

Best candidates to add value
Upload tool	Could improve this KANDA tab	Value
AI Memory Map Builder / Brotherhood Analyzer	Brain Navigator, Refactor Report, Show Project to AI	Strongest candidate. It builds function/class/import/call-graph style maps and group reports. This could make Brain Navigator more “living project memory” instead of mostly navigation.
ProjectAnalyzer / On Every Push Tool	Architecture Review, Workflow Review, Engineering Safety	Generates repeatable reports: complexity, dependency hotspots, tech debt, architecture violations, quality gates. KANDA already has parts of this, but these could strengthen the “daily health scan” layer.
Function Indexer	Project Q&A, Brain Navigator, Symbol Atlas	Small and useful. It indexes functions across the project. Good candidate for a clean integration because it is simpler than the big analyzers.
GUI Specs Tool	Workflow Review, tab validation	Very relevant. It tries to infer GUI user flows from PySide/PyQt code. Could help KANDA detect when tab workflows, buttons, or expected UI sequences are incomplete.
Risk Change Radar	Engineering Safety, Patch Delivery gates	Useful concept: analyze staged diffs and identify risky change areas before patch delivery. KANDA already has risk logic, but this could enrich the risk report.
ADR Writer	Architecture Review, Freeze Feature After Update	Could generate small Architecture Decision Records after important validated changes. Good fit for traceability and freeze memory.
JSON In, Advice Out	Project Q&A, Error Memory, Show Project to AI	Useful pattern: take JSON evidence and produce human-readable advice. KANDA has lots of JSON handoff files, so this concept fits well.
Property Test Generator	Engineering Safety, Reliability Guidance	Valuable idea, but the uploaded file has syntax issues. Better to rewrite the concept cleanly than import it.
LLM SAST Assist	Engineering Safety	Could improve security review by combining Bandit/static analysis with local AI explanation. Useful, but should be optional and offline-safe.
File Path Copier	Show Project to AI, Prompt Library	Good UX idea for manually selecting relevant project files, but KANDA already has more advanced source archive/handoff logic. It could still improve manual file selection.

Yes — those are the tools I think are valuable from the upload.

But I would not convert each one into a separate tab. I would integrate them like this:
Tool	Best destination in KANDA Reasoner	Form
AI Memory Map Builder / Brotherhood Analyzer	Brain Navigator + Refactor Report + Show Project to AI	Internal engine + visual/report section
ProjectAnalyzer / On Every Push Tool	Architecture Review + Engineering Safety	“Project Health Scan” button/section
Function Indexer	Brain Navigator + Project Q&A	Internal symbol index engine
GUI Specs Tool	Workflow Review	“GUI Flow / Tab Spec Audit” section
Risk Change Radar	Engineering Safety + Patch Delivery	Pre-patch risk report
ADR Writer	Architecture Review + Freeze Feature After Update	“Create ADR” button after validated changes
JSON In, Advice Out	Project Q&A + Error Memory + Show Project to AI	AI explanation mode for JSON evidence
Property Test Generator	Engineering Safety	Test-idea generator, not direct auto-test writer at first
LLM SAST Assist	Engineering Safety	Optional security review mode
File Path Copier	Show Project to AI	Manual file-selection helper

The most important principle:

KANDA Reasoner should gain smarter engines, not more tabs.

I would prioritize them in this order:

    Function Indexer
    Smallest, safest, high value. Helps Project Q&A, Brain Navigator, Architecture Review.

    GUI Specs Tool
    Very useful because KANDA is tab-heavy. It can detect incomplete GUI flows, missing buttons, weak tab contracts, and workflow drift.

    Risk Change Radar
    Directly improves patch safety, which is central to KANDA.

    AI Memory Map / Brotherhood Analyzer
    Potentially very powerful, but bigger. I would integrate after the smaller engines are clean.

    ADR Writer
    Good governance feature after the architecture/risk tools are stable.

    JSON In, Advice Out
    Useful, but more of a convenience layer than a core analyzer.

    Property Test Generator / LLM SAST Assist
    Valuable, but should stay optional and gated because they can produce noisy or low-confidence output.

    File Path Copier
    Helpful UX, but lower priority because Show Project to AI already handles structured handoff.

My recommendation: create one new internal layer called something like:

Project Intelligence Engines

Not a user-facing tab at first. It would contain reusable engines:

symbol_index_engine.py
gui_spec_audit_engine.py
risk_change_radar_engine.py
memory_map_engine.py
adr_writer_engine.py
json_advice_engine.py

Then each existing tab can call those engines where useful. This keeps KANDA Reasoner clean, modular, and easier to validate.

great . now  create a handoff to oTher AI , say to AI "
You are a senior Python engineer, prompt architect, and AI-human collaboration 
specialist. You build production-grade applications using a cooperative model 
where the human owns direction and confirmation, and you own implementation, 
quality assurance, and proactive research."

then show the context, what kanda_reasoner is supposed to do , what it has , what is already implemented
then show the tools you intend to implement , ask if AI agree, and explain why or why not ,  ask for suggestions on implementation, improvement , risks , order of implementation , ways to make kanda_reasoner more helpfull to human user, and ways to maximaze performance and suggestions of tools to add 

Vou transformar isso em um texto de handoff pronto para copiar para outro AI, incluindo contexto, arquitetura atual, proposta de integração e perguntas objetivas para revisão.

Below is a copy-paste handoff you can send to another AI. I grounded the project context in the uploaded KANDA Reasoner second-upload package and its source-truth policy: the handoff package says the AI-readable JSON handoff should be read first, and exact source files must still be inspected before editing. The compact Error Memory should also be read before code changes, while the full Error Memory ZIP is only for repeated/debugging/audit cases.

You are a senior Python engineer, prompt architect, and AI-human collaboration specialist. You build production-grade applications using a cooperative model where the human owns direction and confirmation, and you own implementation, quality assurance, and proactive research.

I want your review before implementation. Do not patch yet. First, analyze the plan, agree or disagree, explain why, and suggest improvements.

PROJECT CONTEXT

The project is KANDA Reasoner.

KANDA Reasoner is a desktop Python application intended to help a human user and an AI collaborate safely on a software project. It is not just a code helper. It is a project-understanding, routing, governance, validation, handoff, and memory system.

Its core purpose is to help the human:

    show the project to an AI in a structured way;

    route tasks through the correct project prompts and safeguards;

    understand the architecture and workflows;

    identify risky changes before patching;

    validate patches;

    preserve validated behavior through freeze memory;

    preserve past mistakes through Error Memory so future AI sessions do not repeat them;

    keep the project useful for a non-programmer human who is directing AI-assisted development.

CURRENT IMPLEMENTED AREAS / TABS

KANDA Reasoner already has these main areas:

    Brain Navigator
    Purpose: main navigation and project-brain entry point. It should eventually become a living map of the project, not only a tab launcher.

    Architecture Review
    Purpose: review project architecture, boundaries, ownership, symbol structure, imports, stale design, and architecture violations.

    Workflow Review
    Purpose: review project workflows, step order, validation references, IO contracts, documentation drift, artifact routes, and workflow consistency.

    Engineering Safety
    Purpose: safety tools before patching, including diagnostics, risk analysis, crash triage, release hygiene, and pre-patch checks.

    Docstring Assistant
    Purpose: inspect Python files for missing or weak docstrings and help generate/review docstrings safely.

    Show Project to AI
    Purpose: generate the AI handoff package, including project briefing, routing manifest, file manifest, source archive manifest, validation state, compact Error Memory, and source archive parts.

    Error Memory
    Purpose: store active project-specific lessons from prior mistakes. Compact Error Memory must be read before editing. Full Error Memory is opened only when compact lessons are insufficient, repeated-error debugging is needed, or the user asks for an audit.

    Refactor Report
    Purpose: generate a state-vector/refactor report of the project, including complexity, refactor pressure, source structure, and AI-ready evidence.

    Project Q&A
    Purpose: allow the user to ask questions about project JSON and project evidence through an AI-facing reasoning interface.

    Freeze Feature After Update
    Purpose: after a validated feature or patch, prepare and write local freeze memory only after explicit human confirmation. The Confirm and Write gate must not be bypassed.

    Exclusion Rules
    Purpose: manage files, folders, and extensions that should be excluded from project scanning, handoff, validation, or archives.

    Prompt Library
    Purpose: browse or retrieve project prompt-library content. It should not load everything at startup. It should route to specific prompts when needed.

IMPORTANT GOVERNANCE AND SAFETY CONTEXT

Before editing code:

    inspect exact source files;

    do not rely only on JSON summaries;

    read compact Error Memory;

    do not open full Error Memory unless needed;

    do not place temporary, installer, correction, patch, or validation-helper files in the active project root;

    transient work should go under the dynamic folder:
    <drive>:<project>_delete_after_daily_work

    do not deliver isolated ZIP patches without install code, validation code, expected markers, freeze handling, and Error Memory handling when applicable;

    do not bypass Freeze Feature confirmation gates;

    do not treat generated handoff files as canonical source.

PROPOSED INTEGRATION CONCEPT

I uploaded an older toolbox archive named KANDA_PY_TOOLS.5.11.25.7H.zip. It contains several useful tool ideas, but they should not be copied blindly into KANDA Reasoner.

The goal is not to add many new tabs. KANDA Reasoner already has enough top-level tabs. The better architecture is to extract or rewrite useful tools as internal "Project Intelligence Engines" and expose them inside existing tabs.

Proposed internal layer:

Project Intelligence Engines

Possible engine files or packages:

    symbol_index_engine.py

    gui_spec_audit_engine.py

    risk_change_radar_engine.py

    memory_map_engine.py

    adr_writer_engine.py

    json_advice_engine.py

    property_test_idea_engine.py

    sast_assist_engine.py

    file_selection_helper.py

These should be clean Python 3.10+ modules, Windows-compatible, ASCII-only, with minimal dependencies, explicit exceptions, validation scripts, and safe UI integration.

TOOLS PROPOSED FOR IMPLEMENTATION

    Function Indexer

Proposed destination:

    internal engine used by Brain Navigator, Project Q&A, Architecture Review, and possibly Refactor Report.

Purpose:

    index functions, classes, methods, imports, call relationships if available, docstrings, file ownership, and symbol location.

    produce a stable project symbol map that other tabs can use.

Why it may add value:

    improves Project Q&A accuracy;

    helps Brain Navigator become a true project map;

    helps Architecture Review identify misplaced symbols and duplicated responsibilities;

    easier and safer to implement first because it is smaller than the larger analyzers.

Implementation idea:

    build with ast from the standard library first;

    no AI required for the first version;

    output JSON and a readable report;

    add validation using a small fixture project.

    GUI Specs Tool

Proposed destination:

    Workflow Review as "GUI Flow / Tab Spec Audit";

    possibly Engineering Safety for pre-patch GUI risk.

Purpose:

    inspect PySide/PyQt tab code and infer:

        buttons;

        callbacks;

        required user flow;

        missing callback wiring;

        tab contract inconsistencies;

        duplicated or stale GUI controls;

        mismatch between visible UI and workflow docs.

Why it may add value:

    KANDA Reasoner is tab-heavy;

    many failures can happen when a tab exists but its workflow is incomplete or stale;

    this helps a human understand whether a GUI tab is actually usable.

Implementation idea:

    start with static scan of source files;

    detect common Qt patterns;

    produce "detected controls", "detected callbacks", "unresolved callbacks", "workflow risks";

    do not auto-edit GUI code in v1.

    Risk Change Radar

Proposed destination:

    Engineering Safety;

    patch delivery preflight.

Purpose:

    analyze a proposed patch or changed files and classify risk:

        GUI risk;

        import risk;

        validation risk;

        freeze-memory risk;

        prompt-routing risk;

        file-placement risk;

        root-cleanliness risk;

        startup-delivery risk;

        generated-file-vs-canonical-source risk.

Why it may add value:

    directly supports KANDA Reasoner's most important goal: safe AI-assisted patching.

    can prevent repeated mistakes before patch delivery.

Implementation idea:

    first version can compare changed file paths against known risky subsystems;

    later versions can inspect AST/import deltas;

    output a concise risk report with required validation commands.

    AI Memory Map Builder / Brotherhood Analyzer

Proposed destination:

    Brain Navigator;

    Refactor Report;

    Show Project to AI.

Purpose:

    create a higher-level living memory map of modules, groups, responsibilities, imports, and related components.

    identify "brotherhoods" or families of related files/functions/classes.

Why it may add value:

    can turn Brain Navigator from a static launcher into a real project cognition layer.

    can help AI sessions understand project structure faster.

Implementation concern:

    bigger and more complex than Function Indexer.

    should likely depend on the Function Indexer instead of duplicating scanning logic.

Implementation idea:

    implement after the Function Indexer is stable;

    use symbol index output as input;

    produce grouped maps and summaries;

    avoid using AI in the first version unless optional.

    ADR Writer

Proposed destination:

    Architecture Review;

    Freeze Feature After Update.

Purpose:

    generate small Architecture Decision Records after validated changes:

        decision;

        context;

        alternatives;

        consequences;

        validation evidence;

        linked freeze memory;

        linked patch or feature id.

Why it may add value:

    improves traceability;

    helps future AI sessions understand why a design decision exists;

    complements freeze memory.

Implementation idea:

    v1 should be template-based, not AI-dependent;

    allow user review before writing;

    never write automatically without explicit confirmation.

    JSON In, Advice Out

Proposed destination:

    Project Q&A;

    Error Memory;

        Show Project to AI.

Purpose:

    take structured JSON evidence from KANDA Reasoner and produce human-readable advice:

        what matters;

        what is risky;

        what to inspect next;

        what the human should decide;

        what an AI should not assume.

Why it may add value:

    KANDA Reasoner generates many JSON artifacts;

    the human user benefits when JSON becomes clear, useful guidance.

Implementation idea:

    start as a deterministic formatter/summarizer;

    optional AI explanation later;

    preserve source-truth warning: JSON summaries do not authorize patches.

    ProjectAnalyzer / On Every Push Tool

Proposed destination:

    Architecture Review;

    Workflow Review;

    Engineering Safety.

Purpose:

    daily or per-change project health scan:

        complexity;

        dependency hotspots;

        circular imports;

        risk hotspots;

        stale files;

        architectural drift;

        validation gaps;

        tech debt.

Why it may add value:

    KANDA already has partial versions of this;

    it could unify scattered safety checks into one "Project Health Scan."

Implementation concern:

    overlap with existing Architecture Review and Workflow Review.

    should be implemented as a coordinator over existing tools, not a competing analyzer.

Implementation idea:

    do not create a new tab;

    add a "Project Health Scan" section or button;

    reuse outputs from Architecture Review, Workflow Review, Function Indexer, and Risk Change Radar.

    Property Test Generator

Proposed destination:

    Engineering Safety.

Purpose:

    suggest property-based test ideas for pure functions, parsers, validators, and transformation logic.

Why it may add value:

    helps make validation stronger;

    useful for patch validators.

Implementation concern:

    should not auto-generate noisy tests into the project.

    should propose test ideas first.

Implementation idea:

    v1: "Generate test ideas" report only;

    v2: optional test skeleton after human confirmation.

    LLM SAST Assist

Proposed destination:

    Engineering Safety.

Purpose:

    security/static-analysis support:

        dangerous file operations;

        unsafe eval/exec;

        shell command risks;

        path traversal risks;

        secret leakage;

        unsafe archive extraction;

        unsafe subprocess usage.

Why it may add value:

    KANDA Reasoner manages files, ZIPs, patch install, source archives, and user project roots.

    Security review is important.

Implementation concern:

    should be optional and offline-safe.

    avoid mandatory external dependencies.

    AI advice must not replace deterministic checks.

Implementation idea:

    v1 deterministic source scanner;

    optional Bandit integration only if available;

    optional AI explanation only after deterministic findings.

    File Path Copier / Manual Selection Helper

Proposed destination:

    Show Project to AI;

    Prompt Library.

Purpose:

    improve manual selection of files for AI handoff, copying paths, selecting important files, and preparing targeted file bundles.

Why it may add value:

    useful for human control;

    complements automated source archive generation.

Implementation concern:

    lower priority because Show Project to AI already creates structured handoff packages.

Implementation idea:

    add only as a small UX helper, not a major feature.

PROPOSED PRIORITY ORDER

Suggested implementation order:

Phase 1 - Foundation, low risk, high value

    Function Indexer

    GUI Specs Tool

    Risk Change Radar

Phase 2 - Project intelligence
4. AI Memory Map / Brotherhood Analyzer
5. JSON In, Advice Out
6. Project Health Scan coordinator

Phase 3 - Governance and advanced safety
7. ADR Writer
8. Property Test Idea Generator
9. LLM SAST Assist
10. File Path Copier / Manual Selection Helper

DESIGN QUESTION

Do you agree with the principle that these tools should mostly become internal engines or sections inside existing tabs, rather than new top-level tabs?

Please answer:

    Which proposed tools do you agree are worth implementing?

    Which tools should be rejected, delayed, or merged into existing KANDA features?

    Do you agree with the proposed order? If not, propose a better order.

    What is the safest architecture for the new "Project Intelligence Engines" layer?

    What exact package/module structure would you recommend?

    What validation scripts should be created for each phase?

    What are the main risks of integrating these tools?

    How can we avoid duplicating existing KANDA logic?

    How can we make KANDA Reasoner more helpful for a non-programmer human user?

    How can we maximize performance on large projects?

    What additional tools or engines should be added beyond this list?

    Which parts should be deterministic only, and which parts can optionally use AI?

    What should be the first smallest patch that gives real value without increasing risk?

IMPORTANT RESPONSE REQUIREMENT

Before proposing implementation, please provide an assessment only.

Use this structure:

ASSESSMENT

Agreement:

    Agree / partially agree / disagree

    Why

Recommended implementation order:
1.
2.
3.

Architecture recommendation:

    Proposed package structure

    Shared engine contracts

    Output formats

    Validation strategy

Risks:

    Risk

    Mitigation

Performance recommendations:

    Caching

    incremental scan

    AST reuse

    file filters

    large project strategy

Human-helpfulness recommendations:

    UI wording

    reports

    buttons

    previews

    confirmation gates

    explainability

Suggested additional tools:

    Tool

    Why it helps

First patch recommendation:

    Smallest useful patch

    Files likely affected

    Validation expected

    Why it is safe


Understood. I’ll treat this as the First Ideas / conservative implementation direction and won’t comment or modify it yet.

I’ll wait for your next prompt.

Pasted text.txt
Document
Pasted text (2).txt
Document

ASSESSMENT
Agreement

Position: Strongly Agree with the principle of embedding these tools as internal engines rather than adding top-level tabs.
Why

KANDA Reasoner has reached UI layout saturation. Adding ten new tabs would cause severe navigation fatigue, fragment the user's mental model, and violate the Box Logic Canon. Transforming these tools into background Project Intelligence Engines that feed existing views respects the current UI architecture while drastically increasing its analytical depth.

Furthermore, making the core engines 100% deterministic (AST/Static Analysis) in V1 guarantees that the tool remains fast, localized, offline-safe, and free from the hallucination risks common to pure AI analysis tools.
Recommended Implementation Order

The proposed phase structure is sound, but the sequencing within Phase 1 requires structural adjustment to achieve a data-dependency pipeline where each step naturally builds upon the output of the last.

[Phase 1: Foundations]
Function Indexer ──► GUI Specs Tool ──► Risk Change Radar

[Phase 2: Aggregation & Synthesis]
Project Health Scan Coordinator ──► Memory Map Analyzer ──► JSON In, Advice Out

[Phase 3: Deep Governance]
LLM SAST Assist ──► ADR Writer ──► Property Test Generator ──► File Selection Helper

    Function Indexer (Phase 1): Unchanged priority. This is the structural foundation. It populates the symbol map that subsequent analysis engines require.

    GUI Specs Tool (Phase 1): High priority for KANDA because KANDA is inherently tab-driven. It exposes hidden wiring issues before they manifest as runtime crashes.

    Risk Change Radar (Phase 1): Promoted to close Phase 1. It consumes data from the Function Indexer to map incoming patch files to systemic dependency risk profiles.

    Project Health Scan Coordinator (Phase 2): Promoted ahead of the Memory Map. This consolidates existing architectural metrics with the new Function Indexer outputs into a unified database.

    AI Memory Map / Brotherhood Analyzer (Phase 2): Uses the consolidated health and symbol indexes to calculate systemic component relationships.

    JSON In, Advice Out (Phase 2): Translates the resulting structural data into clear, human-readable summaries.

    LLM SAST Assist (Phase 3): Moved to the top of Phase 3. Security vulnerabilities in patch ingestion represent a critical operational safety risk.

    ADR Writer (Phase 3): Essential for change governance, linked directly to the existing Freeze workflow.

    Property Test Idea Generator (Phase 3): Purely advisory validation enhancement.

    File Path Copier / Manual Selection Helper (Phase 3): Low complexity, simple UX utility enhancement.

Architecture Recommendation
Proposed Package Structure

To enforce strict boundaries and prevent tool logic from contaminating project workspaces, all engines must live inside a dedicated, isolated namespace beneath the app core:

kanda_reasoner_app/
└── project_intelligence/
    ├── __init__.py
    ├── base_engine.py          # Abstract base contract class
    ├── symbol_indexer.py       # Pure AST scanner
    ├── gui_spec_audit.py       # PySide string/AST investigator
    ├── risk_radar.py           # Patch validation & path metrics
    └── models.py               # Immutable dataclasses for engine communication

Shared Engine Contracts

Every intelligence engine must inherit from a unified abstract class. This architecture guarantees predictable exception states and standardized serialization structures.
Python

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseIntelligenceEngine(ABC):
    @abstractmethod
    def run_scan(self, project_root: str, context_filter: Any = None) -> Dict[str, Any]:
        """Executes deterministic scan. Must raise localized EngineExecutionError on failure."""
        pass

Output Formats

    Storage: Every engine must serialize its output as raw, structured JSON stored within the transient work directory: :<project>_delete_after_daily_work/intelligence/engine_name.json.

    Exposures: Engines must expose a standard to_markdown() method. The GUI components can capture this markdown directly to display rich, scannable summaries within existing text panels without parsing complex raw data objects in the UI layer.

Validation Strategy

Each engine module must be accompanied by an isolated validation fixture layout under the tests/ tree:

    Use standard library mock trees (unittest.mock) to evaluate how engines handle missing file systems or corrupt source code targets.

    Ensure tests run verification asserts checking that engine scan operations do not write temporary artifacts into the targeted active project root.

Risks & Mitigations

    Risk: AST Performance Degradation on Large Source Trees.

        Description: Walking massive project structures with standard library ast.parse routines can block the main GUI thread, making the application appear frozen.

        Mitigation: Run all engine execution pipelines inside a background thread worker pool (QRunnable or QThread). Ensure the scanner skips files matching patterns registered in the existing Exclusion Rules registry.

    Risk: Token Exhaustion from AI-Advice Transforms.

        Description: Passing full engine JSON payloads out to an LLM for advice generation creates bloated prompt sequences and increases processing latency.

        Mitigation: Feed the AI only the filtered anomalies or warnings flagged by the deterministic code layer rather than the entire raw index footprint.

Performance Recommendations

    Caching: Maintain a centralized .kanda_intelligence_cache.json within the daily delete folder. Map file system paths to their st_mtime timestamps.

    Incremental Scans: The Function Indexer must inspect only those files whose modification timestamps have shifted since the last run.

    AST Reuse: The Project Health Scan Coordinator must act as the primary file scraper. It reads a file once, generates the base AST object, and shares that node reference across the GUI Spec and SAST sub-engines to eliminate redundant file read operations.

Human-Helpfulness Recommendations

    UI Integration Style: Inside tabs like Architecture Review or Engineering Safety, replace large text areas with split display grids. Place a primary action trigger button (e.g., < Run Risk Analysis Radar >) directly beside an interactive report panel.

    Explanation Layering: Use a structured tiered warning display format within the UI text readouts:

        [CRITICAL SYSTEM VIOLATION]: Requires human override or patch adjustment before the tool permits a patch generation pass.

        [ADVISORY DESIGN NOTE]: Highlighting architecture drift or missing context clues that the user can safely pass downstream to an AI prompt block.

Suggested Additional Tools

    Import Dependency Cycle Sentinel:

        Why: Circular dependencies regularly cause unexpected runtime failures during AI-driven refactoring passes. Catching cyclical import patterns early protects system runtime stability.

    Validation Command Auto-Discovery Engine:

        Why: Automatically extracts local testing runners (e.g., pytest, tox) from tox.ini or pyproject.toml configurations. This passes reliable validation commands to the Patch Delivery template without forcing the human to look them up manually.

First Patch Recommendation
Smallest Useful Patch

The safest initial step is delivering the core BaseIntelligenceEngine architecture along with a minimal, deterministic Function Indexer AST Engine devoid of any GUI visual attachments.
Files Likely Affected

kanda_reasoner_app/project_intelligence/__init__.py
kanda_reasoner_app/project_intelligence/base_engine.py
kanda_reasoner_app/project_intelligence/symbol_indexer.py
tests/test_project_intelligence_symbol_indexer.py

Validation Expected

    Unit tests must demonstrate successful AST parsing of nested functions and top-level definitions on mock target fixtures.

    Verification that run_scan handles syntax errors gracefully without raising unhandled parent thread exceptions.

    Absolute guarantee that no files are written to the target project root during scan execution.

Why it is Safe

This patch introduces no new GUI widgets, alters no active application logic paths, consumes zero LLM prompt tokens, and functions as an isolated, testable utility module.

I am ready to formulate the architectural files for this initial foundation stage. Would you like to proceed with inspecting the base engine interface models, or should we verify the cache strategy parameters first?


these are the other ideas audit comment , and get ideas the really add values, do not implement tools already in app , and lets start implementing from the more valuble for the less, in fact lets equilibrate safety with importance

I’ll consolidate the two external assessments into one safer roadmap: keep only additions that create new value, merge overlaps into existing tabs, and rank by impact versus risk.

I agree with the more conservative direction. The best strategy is not “add all tools,” but:

Add only engines that create new project intelligence, do not duplicate existing tabs, and improve safety or human understanding.

The external assessments converge on the same core principle: internal engines, deterministic first, no new top-level tabs, and no blind copying from the old toolbox. One assessment explicitly warns that the biggest risk is creating “9 different half-finished JSON dialects,” so the shared engine contract must come first. The second also agrees that KANDA’s current tab structure is already broad and that engines should feed existing tabs instead of creating new navigation burden.
My audited decision
Definitely valuable

These add real value and should be implemented:
Priority	Tool / idea	Why it really adds value
1	Function Indexer / Symbol Indexer	Foundation for everything else. It lets KANDA understand functions, classes, imports, methods, docstrings, and file structure deterministically.
2	Risk Change Radar v1	Directly improves patch safety, which is central to KANDA. Start path-based, not complex AST-based.
3	GUI Specs / Tab Audit	KANDA is tab-heavy. This can catch unwired buttons, missing callbacks, and stale GUI workflow contracts.
4	JSON In, Advice Out	Very high human value. It makes KANDA’s JSON/report outputs understandable to a non-programmer.
5	Error Memory Correlator	This may be more valuable than several original tools. It checks whether a new risk resembles a mistake already recorded in Error Memory.
6	Validation Command Auto-Discovery	Useful for patch delivery. It can detect pytest, validation scripts, tox, pyproject, or project-specific validation commands.
7	Import Dependency Cycle Sentinel	Good safety engine. Circular imports are a frequent AI-refactor failure mode.
8	Deterministic SAST / Unsafe Operation Scanner	Valuable because KANDA handles ZIPs, paths, file writes, subprocesses, and patch installers. Keep deterministic and optional first.
Useful, but later
Tool	Decision
Project Health Scan Coordinator	Later. It should aggregate existing reports, not create another scanner.
AI Memory Map / Brotherhood Analyzer	Later. Potentially powerful, but too ambitious until Symbol Indexer is stable.
ADR Writer	Later. Good governance feature, but should come after freeze/report contracts are stable.
Property Test Idea Generator	Later. Useful but niche. Advisory only.
File Path Copier	Lowest priority. Show Project to AI already does structured handoff, so this is only UX polish.
Do not reimplement if already present

Avoid rebuilding these unless source inspection proves there is a gap:
Existing area	Do not duplicate
Architecture Review	Do not create another architecture scanner. New engines should feed it.
Workflow Review	Do not create a second workflow checker. GUI Specs should become a workflow audit feature.
Engineering Safety	Do not duplicate crash triage, release notes, or existing diagnostics.
Docstring Assistant	Do not add another docstring tool. Symbol Indexer can expose docstring metadata only.
Show Project to AI	Do not duplicate source archive or handoff packaging.
Freeze Feature	ADR Writer must not bypass Confirm and Write.
Error Memory	Correlator should read/compare lessons, not replace Error Memory.
Final implementation order I recommend

This balances importance + safety + low duplication.
Phase 0 — Mandatory anti-duplication audit

Before adding tools, inspect current source for existing scanners, report models, exclusion rules, and validation command logic.

Goal: avoid rebuilding what KANDA already has.

Output: short map:

Existing scanner/report utilities:
Existing exclusion-rule API:
Existing validation command logic:
Existing UI report panels:
Safe integration points:
Do not touch:

Phase 1 — Foundation

Patch 1: Project Intelligence base + Symbol Indexer, no GUI yet.

Files likely:

kanda_reasoner_app/project_intelligence/__init__.py
kanda_reasoner_app/project_intelligence/base_engine.py
kanda_reasoner_app/project_intelligence/models.py
kanda_reasoner_app/project_intelligence/symbol_indexer.py
tests/test_project_intelligence_symbol_indexer.py

Why no GUI in first patch: it keeps the first patch isolated, read-only, deterministic, and easy to validate.
Phase 2 — Human-readable outputs

Add a small deterministic Engine Report Formatter before more engines.

This is basically the safe core of “JSON In, Advice Out,” but not an AI tool yet.

It standardizes every engine report into:

What this found
Why it matters
What to inspect next
What an AI must not assume

This is important because KANDA is for a non-programmer human user, not just developers.
Phase 3 — Patch safety

Add Risk Change Radar v1.

Start with path/rule based risk:

startup delivery files -> high governance risk
freeze memory files -> high freeze risk
prompt library files -> high routing/canon risk
GUI files -> GUI workflow risk
validation files -> validation contract risk
installer/ZIP/path files -> patch delivery risk
Error Memory files -> memory/canon risk

Also enforce the existing root-cleanliness lesson: transient install, temp, correction, patch, validation helper, and staging files must not go into the active project root. The compact Error Memory specifically records this as an active prevention rule.
Phase 4 — GUI/tab safety

Add GUI Specs / Tab Audit into Workflow Review.

This should detect:

buttons
callbacks
unresolved callback names
tabs without clear run/preview/export flow
UI labels that imply a feature exists but no handler is wired
dangerous direct write buttons without confirmation

Phase 5 — Error-aware intelligence

Add Error Memory Correlator.

This is not in your original list, but it may be one of the highest-value additions.

Purpose:

New patch touches project root installer logic
-> correlate with prior delete_after_daily_work lesson

New patch touches Project Q&A imports
-> correlate with prior import-path regression lesson

New validation output lacks STATUS: IN_SYNC
-> correlate with prior validation marker lesson

This directly supports KANDA’s mission: prevent repeated AI mistakes.
Phase 6 — Validation helper

Add Validation Command Auto-Discovery.

This helps the user and future AIs avoid guessing validation commands.

It should inspect:

validation/
tests/
pyproject.toml
tox.ini
pytest.ini
README validation sections
known KANDA validation markers

Output should be advisory, not automatic.
Phase 7 — Dependency cycle sentinel

Add import graph and circular import detection.

This can build on Symbol Indexer.
Phase 8 — Deterministic security scanner

Add minimal offline SAST.

Rules only, no AI required:

eval / exec
subprocess with shell=True
unsafe ZIP extraction
path traversal risk
hardcoded absolute roots
writes to project root
secret-looking tokens
dangerous delete operations

Phase 9+ — Bigger synthesis

Only after the above are stable:

Project Health Scan Coordinator
Memory Map / Brotherhood Analyzer
ADR Writer
Property Test Idea Generator
File Path Helper

Refined first patch

I would not start with a Brain Navigator button yet.

Better first patch:

Project Intelligence Foundation v1
- base engine contract
- immutable dataclasses / JSON-safe report model
- Symbol Indexer v1
- fixture tests
- no GUI changes
- no writes to active project root

Expected validation:

python tests/test_project_intelligence_symbol_indexer.py

Expected markers:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Why this is the safest first implementation:

    read-only;

    no GUI risk;

    no LLM usage;

    no freeze interaction;

    no Error Memory write;

    standard library only;

    creates the contract every future engine must follow.

Final recommendation

Use this final priority:

    Anti-duplication source audit

    Base engine contract + Symbol Indexer

    Engine report formatter

    Risk Change Radar v1

    GUI Specs / Tab Audit

    Error Memory Correlator

    Validation Command Auto-Discovery

    Import Cycle Sentinel

    Deterministic SAST

    Project Health Coordinator

    Memory Map

    ADR Writer

    Property Test Ideas

    File Path Helper

This gives KANDA more intelligence without making it bloated.

great! now transform decision in a detailed  canonic  documment for AI and mine reference while implementing . This document will be the guide for actual implementation of selected features. create canonic docuiment

I’ll write this as a canon-style implementation reference, not as a patch. It will define scope, priorities, non-goals, architecture contracts, validation gates, and phase order so future AI sessions do not reinterpret the plan.

I created the canon document below. It preserves the core constraints from the project handoff: exact source must still be inspected before editing, compact Error Memory is always read before code changes, and full Error Memory is opened only when needed. It also incorporates the active prevention rule that transient install, temp, patch, correction, validation-helper, and staging files must stay out of the active project root and use the dynamic daily-work folder.
KANDA Reasoner Project Intelligence Engines Canon v1

Status: canonical implementation guide
Scope: selected future intelligence features for KANDA Reasoner
Audience: human project owner and AI implementation agents
Mode: reference before implementation, patch planning, validation, and future audits
1. Purpose

This document defines the canonical implementation direction for adding selected Project Intelligence features to KANDA Reasoner.

The goal is to increase KANDA Reasoner's ability to understand, explain, audit, and protect a Python project without bloating the user interface, duplicating existing tabs, or introducing unsafe AI-dependent behavior.

The selected features must be implemented as internal engines or contextual sections inside existing tabs, not as new top-level tabs.

KANDA Reasoner should become more intelligent, not more crowded.
2. Project role

KANDA Reasoner is a desktop Python application for AI-human software collaboration.

It helps the human user:

    show a project to an AI in a structured way;

    route tasks through the correct prompt and project governance context;

    understand architecture and workflows;

    identify risky changes before patching;

    validate patches;

    preserve validated behavior through freeze memory;

    preserve past mistakes through Error Memory;

    help non-programmer humans direct AI-assisted development safely.

KANDA Reasoner is not just a code scanner. It is a reasoning, governance, validation, handoff, and memory system.
3. Current major areas

The new intelligence engines must support the existing app, not replace it.

Existing areas include:

    Brain Navigator

        Main project-brain entry point.

        Should eventually display living project knowledge.

    Architecture Review

        Reviews architecture, boundaries, ownership, imports, stale design, and architecture risks.

    Workflow Review

        Reviews workflow order, IO contracts, documentation drift, validation references, and GUI/workflow consistency.

    Engineering Safety

        Runs diagnostics, risk checks, crash triage, release hygiene, and pre-patch safety tools.

    Docstring Assistant

        Reviews and helps generate docstrings.

    Show Project to AI

        Builds structured AI handoff packages and source archives.

    Error Memory

        Stores active project-specific lessons from previous mistakes.

    Refactor Report

        Produces project state/refactor evidence.

    Project Q&A

        Lets the user ask questions about project evidence and JSON artifacts.

    Freeze Feature After Update

    Writes validated feature memory only after explicit human confirmation.

    Exclusion Rules

    Manages project-specific ignored files, folders, and extensions.

    Prompt Library

    Browses and routes prompt-library content.

4. Core decision

The selected tools from the uploaded toolbox must not become one tab each.

Canonical rule:

    New tab only if there is a complete, independent, recurring workflow that cannot fit inside an existing tab.

    Internal engine if the tool produces reusable project intelligence.

    Existing-tab section if the tool supports a current workflow.

    Utility module if the tool is only a helper.

The current decision is:

    Do not add new top-level tabs for these tools.

    Build a Project Intelligence internal layer.

    Expose engine output inside existing tabs only after the engine contract is stable.

    Keep V1 deterministic, offline-safe, and read-only.

    Treat AI explanations as optional second-pass summaries, never as source-of-truth findings.

5. Non-goals

The following are explicitly out of scope for the first implementation wave:

    no new top-level tabs;

    no direct copying of old toolbox code without audit;

    no AI-dependent findings in V1;

    no automatic file modification by engines;

    no automatic freeze writing;

    no automatic ADR writing;

    no mandatory external tools such as Bandit, pytest plugins, graph libraries, or LLM APIs;

    no duplicated architecture scanner if Architecture Review already has equivalent logic;

    no duplicated workflow checker if Workflow Review already has equivalent logic;

    no duplicated docstring tool if Docstring Assistant already covers it;

    no replacement of Show Project to AI handoff packaging;

    no generated report treated as canonical source.

6. Implementation principles

Every new engine must follow these principles:

    Deterministic first

        V1 findings must come from code, paths, AST, config files, project metadata, or existing KANDA evidence.

        AI may explain findings later but must not create primary findings.

    Read-only by default

        Engines must not edit target project files.

        Engines must not write temporary files into the active project root.

        Engine report output must go only to the dynamic daily-work folder unless a later explicit write feature is approved.

    No source-truth confusion

        Engine outputs are generated evidence.

        Engine outputs help reasoning but never replace exact source inspection before patching.

    Reuse existing KANDA logic

        Respect Exclusion Rules.

        Reuse existing scanners when available.

        Feed Architecture Review, Workflow Review, Engineering Safety, Show Project to AI, Project Q&A, and Brain Navigator rather than competing with them.

    Small patches

        Each patch must introduce one coherent capability.

        First patch must not include GUI changes unless source audit proves a tiny safe UI hook is better.

    Validation before expansion

        No second engine should be implemented until the shared engine contract and Symbol Indexer are validated.

    Human-readable output

        Every engine must produce clear, plain-language summaries.

        Every report must include what was found, why it matters, what to inspect next, and what an AI must not assume.

7. Required pre-implementation audit

Before implementing Project Intelligence code, run a source audit.

Purpose:

    avoid duplicating existing KANDA features;

    identify safe integration points;

    identify current project naming conventions;

    identify current exclusion-rule APIs;

    identify current report panel patterns;

    identify existing validation command patterns.

Audit output must include:

PROJECT INTELLIGENCE SOURCE AUDIT

Existing scanner/report utilities:
Existing AST or file-walk utilities:
Existing exclusion-rule API:
Existing validation command logic:
Existing UI report panels:
Existing JSON/report schemas:
Safe integration points:
Potential duplication risks:
Do not touch:
Recommended first patch:

No implementation patch should be created before this audit is completed.
8. Selected feature list
8.1 Selected for implementation

The following features are approved for staged implementation:

    Project Intelligence base contract

    Symbol Indexer / Function Indexer

    Engine Report Formatter

    Risk Change Radar v1

    GUI Specs / Tab Audit

    Error Memory Correlator

    Validation Command Auto-Discovery

    Import Dependency Cycle Sentinel

    Deterministic SAST / Unsafe Operation Scanner

    Project Health Scan Coordinator

    Memory Map / Brotherhood Analyzer

    ADR Writer

    Property Test Idea Generator

    File Path Helper

8.2 Delayed or lower priority

Delayed until core engines are stable:

    Project Health Scan Coordinator

    Memory Map / Brotherhood Analyzer

    ADR Writer

    Property Test Idea Generator

    File Path Helper

8.3 Not to duplicate

Do not reimplement these as separate systems:

    Architecture Review scanner logic

    Workflow Review scanner logic

    Engineering Safety diagnostics

    Docstring Assistant

    Show Project to AI archive/handoff logic

    Freeze Feature write workflow

    Error Memory storage and promotion workflow

9. Final implementation order

The canonical implementation order is:

    Anti-duplication source audit

    Base engine contract plus Symbol Indexer

    Engine Report Formatter

    Risk Change Radar v1

    GUI Specs / Tab Audit

    Error Memory Correlator

    Validation Command Auto-Discovery

    Import Dependency Cycle Sentinel

    Deterministic SAST / Unsafe Operation Scanner

    Project Health Scan Coordinator

    Memory Map / Brotherhood Analyzer

    ADR Writer

    Property Test Idea Generator

    File Path Helper

This order balances value, safety, dependency structure, and implementation risk.
10. Package architecture

Preferred namespace:

kanda_reasoner_app/
    project_intelligence/
        __init__.py
        base_engine.py
        models.py
        scanner.py
        report_formatter.py
        symbol_indexer.py
        risk_radar.py
        gui_spec_audit.py
        error_memory_correlator.py
        validation_command_discovery.py
        import_cycle_sentinel.py
        unsafe_operation_scanner.py
        health_coordinator.py
        memory_map.py
        adr_writer.py
        property_test_ideas.py
        file_path_helper.py

Alternative names are allowed only if current source audit shows existing naming conventions that should be followed.

The preferred namespace is kanda_reasoner_app/project_intelligence/ because it is explicit, isolated, and avoids blending new engine code into existing tabs.
11. Shared engine contract

Every Project Intelligence engine must follow a shared contract.

Recommended public interface:

class BaseIntelligenceEngine:
    engine_id: str
    engine_name: str
    engine_version: str

    def run_scan(self, project_root, context_filter=None, options=None):
        raise NotImplementedError

    def to_markdown(self, report):
        raise NotImplementedError

V1 should use standard library dataclasses rather than Pydantic unless the current project already depends on Pydantic.

Required output object:

@dataclass(frozen=True)
class EngineFinding:
    finding_id: str
    severity: str
    category: str
    title: str
    message: str
    file_path: str
    line_number: int
    evidence: str
    recommendation: str


@dataclass(frozen=True)
class EngineReport:
    engine_id: str
    engine_version: str
    status: str
    generated_at: str
    project_root_label: str
    summary: str
    findings: list[EngineFinding]
    warnings: list[str]
    errors: list[str]
    next_steps: list[str]
    ai_must_not_assume: list[str]

Severity vocabulary:

info
advisory
warning
high
critical

Status vocabulary:

ok
completed_with_findings
completed_with_warnings
failed_gracefully
blocked

Every engine report must include:

This generated report is advisory evidence. It is not canonical source. Exact source files must be inspected before editing.

12. Report format

Every engine must support both:

    JSON-safe output

    Human-readable Markdown or plain text output

Standard human report sections:

What this found
Why it matters
What to inspect next
What an AI must not assume
Findings
Warnings
Errors
Suggested validation

The human report must be written for a non-programmer user first, then provide technical details below.

Avoid jargon in the top summary.

Preferred UI wording:

    "Build project map" instead of "Run Symbol Indexer"

    "Check patch safety" instead of "Run Risk Radar"

    "Audit GUI tabs" instead of "Run Qt Spec Audit"

    "Explain this report" instead of "JSON In, Advice Out"

    "Find repeated mistake risks" instead of "Error Memory Correlator"

13. Storage and file placement

Project Intelligence engines are read-only against the active project root.

Default generated report location:

<drive>:\<project>_delete_after_daily_work\intelligence\

Examples:

<drive>:\<project>_delete_after_daily_work\intelligence\symbol_indexer.json
<drive>:\<project>_delete_after_daily_work\intelligence\symbol_indexer.md
<drive>:\<project>_delete_after_daily_work\intelligence\risk_radar.json
<drive>:\<project>_delete_after_daily_work\intelligence\risk_radar.md

Forbidden locations for transient engine outputs:

<project_root>\
<project_root>\validation\
<project_root>\tests\
<project_root>\kanda_reasoner_app\

Exception:

    Source code patches may add real implementation files to the project only through a validated patch.

    Runtime report outputs and temporary artifacts must not be placed in the active project root.

14. Exclusion rules

Every engine must respect the existing Exclusion Rules system.

No engine may independently decide to scan:

.git
__pycache__
.venv
venv
env
build
dist
node_modules
*.pyc
generated archives
daily-work folders
excluded project paths

File filtering must happen before file reading.

The shared scanner should apply exclusion rules once and pass the filtered file list to engines.
15. Performance rules

Project Intelligence must remain fast enough for large projects.

Required performance rules:

    Shared file walk

        The project tree should be walked once.

        Filtered Python file lists should be reused.

    AST reuse

        Parse each Python file once per scan run.

        Reuse parsed ASTs for Symbol Indexer, GUI Specs, Import Cycle Sentinel, and SAST.

    Incremental cache

        Cache per-file metadata using path plus mtime or hash.

        Rescan changed files only when safe.

    Quick versus deep scan

        Default should be Quick Scan for UI use.

        Deep Scan should be explicit.

    GUI thread safety

        Heavy scans should not block the main GUI thread once integrated into UI.

        V1 command/test execution may be synchronous.

        GUI integration should use the current app's worker/thread pattern if one exists.

    Large output control

        Reports should summarize top findings first.

        Full detail should be expandable or written to report files.

16. Validation rules

Every engine patch must include validation.

Minimum validation per engine:

1. Unit or script validation against fixture project.
2. Syntax-error handling test.
3. Exclusion rule handling test when applicable.
4. No-write-to-target-root test.
5. JSON serialization test.
6. Markdown/plain report generation test.
7. Expected validation marker.
8. STATUS: IN_SYNC marker when project contract requires it.

Expected marker pattern:

VALIDATION OK: project-intelligence-<engine-id>-v1
STATUS: IN_SYNC

Patch ZIP delivery must also include:

ZIP CONTRACT: PASS

17. First patch canon

The first implementation patch must be:

Project Intelligence Foundation v1

It must include:

kanda_reasoner_app/project_intelligence/__init__.py
kanda_reasoner_app/project_intelligence/base_engine.py
kanda_reasoner_app/project_intelligence/models.py
kanda_reasoner_app/project_intelligence/symbol_indexer.py
tests/test_project_intelligence_symbol_indexer.py

It must not include:

new GUI widgets
new top-level tabs
AI calls
Freeze Feature writes
Error Memory writes
patch delivery changes
startup delivery changes
prompt-library changes

The first patch must be read-only and standard-library only.

Expected validation command:

python tests/test_project_intelligence_symbol_indexer.py

Expected validation output:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

18. Feature specifications
18.1 Symbol Indexer / Function Indexer

Priority: 1
Risk: low
Value: foundational
Mode: deterministic only

Purpose:

    inspect Python files;

    detect functions, async functions, classes, methods, imports, docstrings, line numbers, and simple ownership metadata;

    produce a reusable symbol map for later engines.

Must detect:

    top-level functions;

    nested functions when feasible;

    classes;

    methods;

    async functions;

    import statements;

    from-import statements;

    docstring present or missing;

    file path;

    line number.

Must not:

    modify files;

    infer behavior beyond available source;

    perform AI summarization;

    scan excluded paths;

    create GUI dependencies.

Initial output:

    JSON report;

    Markdown/plain report;

    summary counts.

Example human summary:

Project map completed. Found 312 functions, 58 classes, and 421 import statements across 96 Python files. This report is advisory and does not replace source inspection before editing.

18.2 Engine Report Formatter

Priority: 2
Risk: low
Value: high for human usability
Mode: deterministic first

Purpose:

    standardize human-readable explanations for all engine outputs.

Required sections:

    What this found

    Why it matters

    What to inspect next

    What an AI must not assume

Must not:

    invent findings;

    turn advisory reports into authorization to patch;

    hide technical detail entirely.

This may be implemented as report_formatter.py or as a method in base_engine.py if source audit shows a simpler pattern.
18.3 Risk Change Radar v1

Priority: 3
Risk: medium-low
Value: very high
Mode: deterministic only

Purpose:

    identify risk in changed files, proposed patch paths, or selected file paths.

V1 should be path/rule based.

Risk categories:

    GUI risk;

    import risk;

    validation risk;

    freeze-memory risk;

    prompt-routing risk;

    startup-delivery risk;

    patch-delivery risk;

    root-cleanliness risk;

    Error Memory risk;

    generated-file-versus-canonical-source risk.

Examples:

    files under startup delivery paths -> startup-delivery risk;

    files under freeze memory paths -> freeze-memory risk;

    files under prompt_library -> prompt-routing/canon risk;

    files under GUI modules -> GUI workflow risk;

    validation scripts -> validation contract risk;

    installer, ZIP, archive, subprocess, path files -> patch delivery or unsafe operation risk.

Must include:

    risk level;

    reason;

    required source inspection;

    suggested validation commands when discoverable;

    related Error Memory lesson candidates when correlator exists.

V1 must not:

    block patches by itself;

    invent validation success;

    inspect full AST unless Symbol Indexer is already stable.

18.4 GUI Specs / Tab Audit

Priority: 4
Risk: medium
Value: high
Mode: deterministic only

Purpose:

    inspect PySide/PyQt GUI code and identify tab workflow risks.

Should detect:

    visible buttons;

    button labels;

    connected callbacks;

    missing callback targets;

    likely run/preview/export/write flows;

    tabs with write actions but no apparent confirmation;

    tab names and tool specs when available;

    UI labels that imply a feature exists without obvious logic.

Destination:

    Workflow Review as "Audit GUI tabs"

    Engineering Safety as a future optional pre-patch GUI risk input

Must not:

    auto-edit GUI files;

    assume a missing callback is definitely broken without evidence;

    block patching without human review.

18.5 Error Memory Correlator

Priority: 5
Risk: medium
Value: very high
Mode: deterministic first

Purpose:

    compare current risks or touched files against compact Error Memory lessons.

Examples:

    patch touches installer/root staging logic -> correlate with delete-after-daily-work lesson;

    patch touches Project Q&A imports -> correlate with import-path regression lesson;

    validation output lacks STATUS: IN_SYNC -> correlate with validation marker lesson;

    response includes isolated ZIP -> correlate with no-isolated-ZIP lesson.

Must read:

    compact Error Memory export;

    lesson IDs;

    triggers;

    do-not-repeat rules;

    regression checks.

Must not:

    edit Error Memory;

    promote lessons;

    open full Error Memory by default;

    treat compact lesson text as source code truth.

Output:

    related lesson IDs;

    match strength: exact, partial, weak, none;

    avoidance rule;

    next safe action.

18.6 Validation Command Auto-Discovery

Priority: 6
Risk: medium-low
Value: high
Mode: deterministic only

Purpose:

    find likely validation commands for the project or patch.

Should inspect:

    validation/ directory;

    tests/ directory;

    pyproject.toml;

    pytest.ini;

    tox.ini;

    README validation sections;

    existing KANDA validation scripts;

    known expected markers.

Must output:

    candidate command;

    confidence;

    why it was selected;

    expected marker if discoverable;

    warning if command is inferred.

Must not:

    run commands automatically without user action;

    claim validation passed;

    replace patch-specific validation instructions.

18.7 Import Dependency Cycle Sentinel

Priority: 7
Risk: medium
Value: high
Mode: deterministic only

Purpose:

    detect circular imports and high-risk dependency relationships.

Should build on:

    Symbol Indexer import data;

    shared scanner.

Must output:

    cycle path;

    files involved;

    import lines where available;

    likely risk;

    suggested inspection.

Must not:

    rewrite imports;

    auto-resolve cycles;

    treat optional imports as definitely wrong without context.

18.8 Deterministic SAST / Unsafe Operation Scanner

Priority: 8
Risk: medium
Value: high
Mode: deterministic only in V1

Purpose:

    detect unsafe operations relevant to KANDA's responsibilities.

Rules should include:

    eval;

    exec;

    subprocess with shell=True;

    unsafe ZIP extraction patterns;

    path traversal risk;

    hardcoded absolute project roots;

    writes directly to project root;

    broad delete operations;

    secret-looking tokens;

    shell command construction from unchecked input.

Must be optional at first.

Must not:

    require Bandit;

    require internet;

    produce AI-only security findings;

    block all patching automatically.

18.9 Project Health Scan Coordinator

Priority: 9
Risk: medium
Value: high after prior engines exist
Mode: aggregation only

Purpose:

    aggregate existing Architecture Review, Workflow Review, Refactor Report, Symbol Indexer, Risk Radar, GUI Audit, and SAST findings.

Must not:

    duplicate scanner logic;

    become a parallel Architecture Review;

    run heavy deep scans without user awareness.

Output:

    health summary;

    biggest risk;

    top next actions;

    report links.

18.10 Memory Map / Brotherhood Analyzer

Priority: 10
Risk: high
Value: potentially high
Mode: delayed

Purpose:

    group related files, functions, classes, and modules into project families.

Depends on:

    stable Symbol Indexer;

    stable Import Cycle Sentinel;

    stable Health Coordinator or shared evidence format.

Must not:

    be implemented early;

    use vague AI grouping as primary logic;

    replace exact source inspection.

18.11 ADR Writer

Priority: 11
Risk: medium
Value: governance value
Mode: template first

Purpose:

    draft Architecture Decision Records after validated changes.

Must require:

    preview;

    explicit human confirmation before writing;

    validation evidence;

    linked feature ID or patch ID;

    optional freeze reference.

Must not:

    write automatically;

    bypass Freeze Feature confirmation;

    invent validation evidence.

18.12 Property Test Idea Generator

Priority: 12
Risk: low-medium
Value: niche
Mode: advisory only

Purpose:

    suggest property-based test ideas for pure functions, parsers, validators, and transformation logic.

Must not:

    auto-add tests in V1;

    create noisy or speculative test files;

    require Hypothesis unless separately approved.

18.13 File Path Helper

Priority: 13
Risk: low
Value: small UX improvement
Mode: utility only

Purpose:

    help user copy/select important paths for AI handoff or manual review.

Must not:

    duplicate Show Project to AI source archive logic;

    create a new tab;

    become a second handoff generator.

19. UI integration canon

No engine should get a new top-level tab by default.

Preferred destinations:

Symbol Indexer -> Brain Navigator, Project Q&A, Architecture Review
Risk Change Radar -> Engineering Safety, patch preflight
GUI Specs / Tab Audit -> Workflow Review
Error Memory Correlator -> Engineering Safety, Error Memory, patch preflight
Validation Command Auto-Discovery -> Engineering Safety, patch delivery
Import Cycle Sentinel -> Architecture Review, Engineering Safety
SAST Scanner -> Engineering Safety
Health Coordinator -> Brain Navigator, Architecture Review, Engineering Safety
Memory Map -> Brain Navigator, Refactor Report
ADR Writer -> Architecture Review, Freeze Feature
Property Test Ideas -> Engineering Safety
File Path Helper -> Show Project to AI

UI wording must avoid developer-only jargon.

Use plain labels:

    Build project map

    Check patch safety

    Audit GUI tabs

    Find repeated mistake risks

    Suggest validation command

    Check import cycles

    Scan unsafe operations

    Create health summary

20. Patch delivery requirements

Any patch implementing this canon must follow normal KANDA patch delivery rules.

Patch delivery must include:

    patch ZIP;

    install instructions;

    validation instructions;

    expected validation markers;

    freeze handling when applicable;

    Error Memory handling when applicable.

No isolated ZIP delivery is allowed.

Install and temporary files must be staged under:

<drive>:\<project>_delete_after_daily_work\

Patch ZIPs that are freezeable must include root-level:

KANDA_FREEZE_HINT.json

unless explicitly declared non-freezeable with reason.
21. Freeze policy

Project Intelligence engine implementation patches may become freezeable after validation.

However:

    engine report outputs do not automatically become freeze memory;

    ADR Writer must not write ADRs without confirmation;

    Freeze Feature Confirm and Write must remain explicitly human-confirmed;

    validation evidence must include expected markers before freeze.

22. Error Memory policy

Before code editing:

    read compact Error Memory;

    apply relevant avoidance rules;

    do not open full Error Memory unless needed.

Project Intelligence features must not write active Error Memory automatically.

Error Memory Correlator may:

    read compact lessons;

    report related lesson IDs;

    warn about repeated risk patterns.

Error Memory Correlator must not:

    create lessons;

    promote lessons;

    alter active memory;

    open full memory by default.

23. AI usage policy

V1 engines must be deterministic.

Allowed AI usage later:

    explain deterministic findings;

    rewrite a human-readable summary;

    suggest next questions;

    draft ADR text from validated evidence;

    suggest test ideas from already-detected pure functions.

Forbidden AI usage:

    creating primary findings without deterministic evidence;

    claiming validation passed;

    deciding freeze eligibility without validation evidence;

    replacing source inspection;

    silently editing project files.

Canonical rule:

AI explains and helps prioritize. Deterministic engines detect.

24. Acceptance checklist for first patch

First patch is accepted only if all are true:

[ ] Source audit completed.
[ ] No duplicate existing scanner was created.
[ ] project_intelligence package added in isolated namespace.
[ ] Base engine contract exists.
[ ] Shared report models exist.
[ ] Symbol Indexer detects functions, classes, methods, imports, line numbers, and docstring presence.
[ ] Syntax errors are handled gracefully.
[ ] Excluded paths are not scanned.
[ ] No files are written to active project root during scan.
[ ] JSON report can serialize.
[ ] Human-readable report can render.
[ ] Validation script passes.
[ ] Validation output includes expected marker.
[ ] STATUS: IN_SYNC is present if required by current contract.
[ ] Patch ZIP contract passes.

25. Required first validation script behavior

The first validation script must:

    create or use a small fixture project;

    include at least one top-level function;

    include at least one async function;

    include at least one class;

    include at least one method;

    include at least one nested function if supported;

    include at least one import and one from-import;

    include at least one syntax-error file to test graceful failure;

    assert no output is written to the target fixture root;

    assert JSON output is valid;

    assert report text contains advisory source-truth warning.

Required final print markers:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC

If patch ZIP validation is included:

ZIP CONTRACT: PASS

26. Future implementation rule

After each implemented feature, update this canon only if:

    the implementation revealed a better safe architecture;

    a feature was rejected;

    an engine was merged into existing logic;

    a validation rule changed;

    a new high-value engine was discovered.

Do not update this canon to justify scope creep.

Every future update must preserve:

    internal engines over new tabs;

    deterministic V1;

    no source-truth confusion;

    no root transient files;

    explicit human confirmation for writes;

    compact Error Memory before editing;

    exact source inspection before patching.

27. Canon summary

KANDA Reasoner's Project Intelligence layer should be implemented as a small, deterministic, shared, read-only engine system that feeds existing tabs.

Implementation must start with:

Anti-duplication audit
Base engine contract
Symbol Indexer

Only after that should KANDA add:

report formatting
risk radar
GUI audit
Error Memory correlation
validation discovery
import cycle detection
unsafe operation scanning

Large synthesis tools such as Memory Map, Health Coordinator, ADR Writer, and Property Test Ideas must wait until the foundation is stable.

The final design objective is:

Make KANDA Reasoner safer, clearer, and more useful for a human directing AI-assisted development, without adding unnecessary tabs or duplicating existing app logic.


now gimme a complete numered roadmap for first implementation 

Below is a complete numbered roadmap for the first implementation: Project Intelligence Foundation v1.

This roadmap is for the first safe patch only: anti-duplication audit + internal engine foundation + Symbol Indexer v1, with no GUI changes yet.
Roadmap: Project Intelligence Foundation v1
1. Confirm implementation scope

Implement only:

    project_intelligence internal package.

    Base engine contract.

    Shared report/data models.

    Symbol Indexer / Function Indexer v1.

    Validation script for Symbol Indexer.

    Patch delivery with install and validation instructions.

Do not implement yet:

    Brain Navigator button.

    GUI Specs Tool.

    Risk Change Radar.

    JSON Advice.

    Error Memory Correlator.

    Health Scan.

    ADR Writer.

    SAST.

    Memory Map.

    Any new top-level tab.

Reason: first patch should prove the engine architecture safely before touching UI.
2. Load required safety context before coding

Before any source edit, the implementing AI must confirm:

    Startup routing is loaded.

    Project handoff is loaded.

    Compact Error Memory is loaded.

    Full Error Memory is not opened unless compact lessons are insufficient or repeated-error debugging is needed. The uploaded Error Memory preflight explicitly says compact memory is always read and full memory is only opened when needed.

    Exact source files are inspected before editing; JSON handoff is helpful but not source truth.

Required pre-coding response:

ERROR MEMORY CHECK

Project slug: kanda_reasoner
Relevant lesson IDs:
Confidence per match:
Applicable avoidance rules:
Full Error Memory ZIP needed: YES / NO
May proceed:
Reason:
Next safe action:

For this first patch, likely relevant lessons:

    lesson-delete-after-daily-work-bridge-enforcement-v1

    lesson-no-isolated-zip-delivery-contract-v1

    lesson-validation-output-status-in-sync-required-v1

3. Run anti-duplication source audit

Before creating files, inspect the current source tree for existing equivalents.

Audit must answer:

PROJECT INTELLIGENCE SOURCE AUDIT

Existing scanner/report utilities:
Existing AST or file-walk utilities:
Existing exclusion-rule API:
Existing validation command logic:
Existing UI report panels:
Existing JSON/report schemas:
Safe integration points:
Potential duplication risks:
Do not touch:
Recommended first patch:

The audit must specifically search for:

    Existing AST scanners.

    Existing project file walkers.

    Existing exclusion-rule loaders.

    Existing report/dataclass models.

    Existing validation script conventions.

    Existing STATUS: IN_SYNC patterns.

    Existing source archive / handoff scanners.

    Existing Architecture Review scan logic.

    Existing Workflow Review scan logic.

    Existing Engineering Safety scan logic.

Stop gate:

If existing reusable scanner/report utilities exist, reuse or wrap them.
Do not create duplicate scanner logic unless the audit proves there is no safe reusable interface.

4. Define first patch name and feature ID

Recommended feature ID:

project-intelligence-symbol-indexer-v1

Recommended patch ZIP name:

kanda_project_intelligence_symbol_indexer_v1_patch.zip

Recommended validation marker:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

5. Create isolated package namespace

Add the internal namespace:

kanda_reasoner_app/project_intelligence/

Initial files:

kanda_reasoner_app/project_intelligence/__init__.py
kanda_reasoner_app/project_intelligence/base_engine.py
kanda_reasoner_app/project_intelligence/models.py
kanda_reasoner_app/project_intelligence/symbol_indexer.py

Important: no GUI imports inside this package.

This package must be:

    Standard-library only.

    ASCII-only.

    Windows-compatible.

    Read-only against the target project.

    Independent from PySide/PyQt.

    Safe to test in isolation.

6. Define shared models first

File:

kanda_reasoner_app/project_intelligence/models.py

Required dataclasses:

    EngineFinding

    EngineReport

    SymbolRecord

    ImportRecord

    FileSymbolSummary

Minimum model fields:

EngineFinding:
- finding_id
- severity
- category
- title
- message
- file_path
- line_number
- evidence
- recommendation

EngineReport:
- engine_id
- engine_version
- status
- generated_at
- project_root_label
- summary
- findings
- warnings
- errors
- next_steps
- ai_must_not_assume

SymbolRecord:
- name
- symbol_type
- file_path
- line_number
- end_line_number
- parent_name
- has_docstring
- is_async

ImportRecord:
- module
- imported_name
- import_type
- file_path
- line_number

FileSymbolSummary:
- file_path
- function_count
- class_count
- method_count
- import_count
- syntax_error

No Pydantic unless already used by the project and audit approves it.
7. Define base engine contract

File:

kanda_reasoner_app/project_intelligence/base_engine.py

Required objects:

    EngineExecutionError

    BaseIntelligenceEngine

Minimum methods:

run_scan(project_root, context_filter=None, options=None)
to_markdown(report)

Required behavior:

    Engine errors must be localized.

    A syntax error in one file must not crash the whole scan.

    Engine output must include the advisory warning:

This generated report is advisory evidence. It is not canonical source. Exact source files must be inspected before editing.

8. Implement Symbol Indexer v1

File:

kanda_reasoner_app/project_intelligence/symbol_indexer.py

Use only:

ast
dataclasses
datetime
json
pathlib
typing

Symbol Indexer must detect:

    Top-level functions.

    Async functions.

    Classes.

    Methods.

    Nested functions if feasible.

    import x.

    import x as y.

    from x import y.

    Docstring presence.

    File path.

    Line number.

    Syntax-error files as graceful warnings.

V1 does not need:

    Full call graph.

    Type inference.

    Runtime import execution.

    AI summarization.

    GUI integration.

    Writing reports to disk.

9. Enforce read-only behavior

The indexer must not write files into the target project root.

During tests, assert that no new file appears in the fixture project after scan.

Runtime report writing, if included at all, must go only under:

<drive>:\<project>_delete_after_daily_work\intelligence\

This matters because the active compact Error Memory records that install, temp, correction, patch, validation-helper, and staging files must not be placed in the active project root.

For first patch, safest option:

Do not implement report writing yet.
Return reports in memory only.

10. Respect exclusion rules carefully

First patch has two acceptable options:

Option A — safer if exclusion API is not clear:

Implement a small default exclusion list inside Symbol Indexer v1.
Mark existing Exclusion Rules integration as TODO after audit.

Default skip list:

.git
__pycache__
.venv
venv
env
build
dist
node_modules
*.pyc

Option B — better if audit finds a clean existing exclusion API:

Use the existing Exclusion Rules API.
Do not duplicate exclusion logic.

Stop gate:

Do not guess the Exclusion Rules API.
Inspect exact source first.

11. Create validation fixture inside test script or tests fixture

Preferred first validation: self-contained test script that creates a temporary fixture using Python tempfile.

This avoids adding many fixture files.

Validation fixture should contain:

    sample_module.py with:

        import

        from-import

        top-level function with docstring

        top-level function without docstring

        async function

        class

        method

        nested function

    bad_syntax.py with invalid Python syntax.

    Excluded folder:

        __pycache__/ignored.py

        .venv/ignored.py

12. Add validation script

File:

tests/test_project_intelligence_symbol_indexer.py

The script must be runnable directly:

python tests/test_project_intelligence_symbol_indexer.py

Required validation checks:

    Imports package successfully.

    Builds temporary fixture project.

    Runs Symbol Indexer.

    Detects expected top-level functions.

    Detects expected async function.

    Detects expected class.

    Detects expected method.

    Detects expected imports.

    Detects docstring presence and absence.

    Handles syntax error gracefully.

    Skips excluded folders.

    Does not write files to fixture root.

    Produces JSON-serializable report.

    Produces Markdown/plain report.

    Contains advisory non-canonical-source warning.

    Prints expected validation markers.

Final prints:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC

13. Run syntax validation

Before packaging:

python -m py_compile kanda_reasoner_app/project_intelligence/__init__.py
python -m py_compile kanda_reasoner_app/project_intelligence/base_engine.py
python -m py_compile kanda_reasoner_app/project_intelligence/models.py
python -m py_compile kanda_reasoner_app/project_intelligence/symbol_indexer.py
python -m py_compile tests/test_project_intelligence_symbol_indexer.py

All Python must be standard Python 3.10+ and ASCII-only.
14. Run functional validation

Command:

python tests/test_project_intelligence_symbol_indexer.py

Expected output must include:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC

If output lacks STATUS: IN_SYNC, do not freeze. The compact Error Memory includes a prior lesson specifically requiring this marker when the project contract requires sync evidence.
15. Prepare patch ZIP with only updated files

Patch ZIP must include only files changed/added by the patch.

Expected ZIP contents:

kanda_reasoner_app/project_intelligence/__init__.py
kanda_reasoner_app/project_intelligence/base_engine.py
kanda_reasoner_app/project_intelligence/models.py
kanda_reasoner_app/project_intelligence/symbol_indexer.py
tests/test_project_intelligence_symbol_indexer.py
KANDA_FREEZE_HINT.json

Include KANDA_FREEZE_HINT.json because this patch is freezeable after validation.

Do not include:

temporary files
logs
cache files
full source tree
old toolbox archive files
daily-work folder contents

16. Validate ZIP contract

Patch delivery must pass the KANDA ZIP contract.

Expected marker:

ZIP CONTRACT: PASS

Do not deliver the ZIP if the contract cannot be validated.

The active Error Memory includes a prevention lesson against isolated ZIP delivery: a ZIP must not be sent without install code, validation code, expected markers, and freeze/Error Memory handling when applicable.
17. Prepare install instructions

Install instructions must:

    Detect project drive from $PROJECT_ROOT.

    Stage ZIP under:

<drive>:\<project>_delete_after_daily_work\

    Delete any root-drive ZIP copy after staging.

    Extract only from the staged ZIP.

    Copy only updated files into the active project.

    Never place installer/temp/helper files in project root.

    Use correct terminal cleanup behavior from the patch delivery contract.

This directly follows the root-cleanliness and dynamic daily-work containment lesson.
18. Prepare user-facing validation instructions

Validation block must include:

python -m py_compile kanda_reasoner_app/project_intelligence/__init__.py
python -m py_compile kanda_reasoner_app/project_intelligence/base_engine.py
python -m py_compile kanda_reasoner_app/project_intelligence/models.py
python -m py_compile kanda_reasoner_app/project_intelligence/symbol_indexer.py
python -m py_compile tests/test_project_intelligence_symbol_indexer.py
python tests/test_project_intelligence_symbol_indexer.py

Expected markers:

VALIDATION OK: project-intelligence-symbol-indexer-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

19. Prepare freeze hint

KANDA_FREEZE_HINT.json should summarize:

feature_id: project-intelligence-symbol-indexer-v1
feature_name: Project Intelligence Symbol Indexer v1
status: freezeable_after_local_validation
validated_files:
- kanda_reasoner_app/project_intelligence/__init__.py
- kanda_reasoner_app/project_intelligence/base_engine.py
- kanda_reasoner_app/project_intelligence/models.py
- kanda_reasoner_app/project_intelligence/symbol_indexer.py
- tests/test_project_intelligence_symbol_indexer.py
validation_command:
- python tests/test_project_intelligence_symbol_indexer.py
expected_markers:
- VALIDATION OK: project-intelligence-symbol-indexer-v1
- STATUS: IN_SYNC

Freeze must still require human confirmation through Freeze Feature After Update.
20. Do not update canon unless needed

The first patch should not update the canon document unless source audit reveals that:

    package path must change;

    model contract must change;

    exclusion API requires a different architecture;

    current KANDA already has a reusable scanner;

    validation conventions differ from expected.

Otherwise, keep the canon stable.
21. First implementation success criteria

The first implementation is successful only if:

    Source audit is completed.

    No duplicated existing scanner is introduced.

    project_intelligence package exists.

    Base engine contract exists.

    Shared dataclasses exist.

    Symbol Indexer detects functions/classes/imports/docstrings.

    Syntax errors are handled gracefully.

    Excluded folders are skipped.

    No files are written to active target project root during scan.

    Report is JSON-serializable.

    Report can render as Markdown/plain text.

    Validation passes.

    Output includes VALIDATION OK: project-intelligence-symbol-indexer-v1.

    Output includes STATUS: IN_SYNC.

    ZIP contract passes.

    Patch delivery includes install and validation instructions.

    Freeze hint is included.

    No GUI behavior is changed.

Final numbered implementation order

    Load startup/project/compact Error Memory context.

    Return ERROR MEMORY CHECK.

    Inspect exact source files.

    Run anti-duplication source audit.

    Confirm first patch scope.

    Create project_intelligence package.

    Add models.py.

    Add base_engine.py.

    Add symbol_indexer.py.

    Add direct validation script.

    Run py_compile.

    Run functional validation.

    Confirm no target-root writes.

    Prepare freeze hint.

    Build patch ZIP with only changed files.

    Validate ZIP contract.

    Deliver patch with install block.

    Deliver validation block.

    Include expected markers.

    Explain freeze handling.

    Stop and wait for local validation result before any freeze-memory action.


