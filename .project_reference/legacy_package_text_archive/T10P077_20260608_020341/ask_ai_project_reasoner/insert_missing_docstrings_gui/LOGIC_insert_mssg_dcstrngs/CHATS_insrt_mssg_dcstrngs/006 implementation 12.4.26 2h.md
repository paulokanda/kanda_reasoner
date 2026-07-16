Pasted text.txt
Document

I’m looking through the pasted text to see what you shared and how best to help with it.

I see the pasted text. It is a system-prompt/spec for an evidence-grounded assistant focused on a Missing Docstrings Inserter tool, with strict rules for using only provided evidence packs, citation formatting like [F##], [S##], [SN##], and an INSUFFICIENT_EVIDENCE fallback. It also defines intent add-ons for usage, architecture, modification, and limitations.

The main issue is that this prompt is tuned for a very narrow QA workflow, not for general architecture/design work. It would constrain the assistant to only answer from explicit evidence snippets and could refuse often unless the caller always supplies a fully structured evidence pack.

A sensible next step is for me to either:

    adapt this into a cleaner production-ready system prompt for that docstring tool, or

    convert the same ideas into a prompt for your architecture-spec workflow.


you are pyarchitect

Yes — I’m PyArchitect.

I’ll stay focused on software architecture and help you shape the design step by step, without overwhelming you. I’ll suggest assumptions, ask at most two questions at a time, and turn the result into a concrete spec your team can build.

To start, tell me:

    What system or product are we designing?

    Who are the primary users and what is the main outcome they need?

A good starting assumption, if you want one: this is an MVP for a web-based internal or customer-facing application with API, database, auth, and basic observability.

insert_missing_docstrings.py
Python
insert_missing_docstrings_gui.py
Python
mode_options_hlp.py
Python
do you understand this project ? what it does? explain a summary or its logic.

Yes. I understand it.

This project is a developer tool for automatically inserting missing Python docstrings at the module, class, function, and method level, while trying not to change any other code. The core worker is insert_missing_docstrings.py, the desktop UI is insert_missing_docstrings_gui.py, and mode_options_hlp.py contains short human-readable help text about the modes and tool limitations.

At a high level, the worker walks a project tree, finds .py files, excludes common cache/build/vendor/test areas by default, parses each file with ast, detects which nodes have no docstring, generates placeholder docstrings from names/signatures/type annotations, and then either reports, previews, or writes those insertions depending on the selected mode.

The logic is roughly this:

    It scans Python files under a chosen root using os.walk, skipping directories like .git, __pycache__, node_modules, virtualenv folders, and test folders by default. It also has extra filtering for “relaxed” paths such as temp, backup, older, and copy-like files unless explicitly included.

    For each file, it reads the source while preserving whether the file had a UTF-8 BOM, then parses the code with ast.parse. If parsing fails, the file is skipped safely.

    If a module/class/function is missing a docstring, it builds one automatically. Module docstrings are generic one-line summaries like “Utilities and definitions for …”; class docstrings are “Represent …”; function docstrings are inferred from the function name, and may include Parameters and Returns sections based on the signature and annotations.

    It calculates insertion points from AST line numbers, preserves indentation, skips inline one-line bodies to avoid unsafe edits, applies the insertions in memory, and reparses the generated result to make sure the modified file is still valid Python before it is accepted as a change.

The three modes are:

    scan: prints a JSON summary of which files are missing docstrings and which files were skipped.

    diff: shows a unified diff of the exact docstrings that would be inserted, without changing files.

    write: writes the generated docstrings back to disk, preserving BOM behavior and normalizing line endings to \n.

The GUI is a thin wrapper around the worker. It lets the user choose the project root, select scan / diff / write, toggle whether to include module/class/function docstrings, and optionally require confirmation before write. It runs the worker in a QThread, captures stdout/stderr, streams the text into an output panel, and shows success or warning dialogs when the run finishes.

The intended safety model is conservative: the tool only inserts missing docstrings, does not refactor existing code, skips syntax-broken files, skips unsafe inline-body cases, and warns that the generated docstrings are structurally correct and signature-aware but not guaranteed to be semantically perfect.

One practical observation: mode_options_hlp.py defines reusable help text and a limitations summary, but the current GUI’s show_help() uses a hardcoded help string instead of importing that module, so the helper file looks more like a support/reference module than an active dependency in the current implementation.

In one sentence: it is a safe-ish AST-based batch docstring inserter with scan/diff/write modes and a simple PySide6 GUI for running it on a Python project.

I can also break this down into a component-by-component architecture summary next.

001 Roadmap AI-Powered Docstring Inserter.md
File
002 Roadmap AI-Powered Docstring Inserter.md
File
003 Roadmap AI-Powered Docstring Inserter continue.md
File
not implemented yet ai_config.py
Python
not implemented yet ai_docstring_generator.py
Python
not implemented yet context_builder.py
Python
not implemented yet insert_missing_docstrings.py
Python
not implemented yet insert_missing_docstrings_gui.py
Python
not implemented yet INTEGRATION_GUIDE.py
Python
not implemented yet parallel_runner.py
Python
I want you audit, analise the discussions uploaded files  now, improve those ideas in a full numered roadmap to  use local ai to update missing docstrings in module or project with many modules  , improving project 

I’m reviewing the roadmap notes alongside the current and “not implemented yet” modules, then I’ll consolidate them into one buildable numbered roadmap with gaps, risks, and improvements.

I’ve got the main shape. Now I’m checking the unfinished AI modules for where the roadmap is strong, where it overreaches, and what needs reordering to make it implementable on a large codebase.

Yes. I audited the current tool, the roadmap discussions, and the unfinished AI modules.

The direction is good: the existing worker already has the right safety skeleton for a large-codebase tool — AST parsing, exclusion filters, scan/diff/write modes, BOM preservation, and a parse-after-generation safety check before writing. That makes it a strong base for adding local AI rather than rebuilding the tool from scratch.

The main weakness is not architecture, it is consistency. The discussions and unfinished files drift in a few important places: the early AI generator contract returns a plain string body, while the later roadmap evolves it into a (docstring_body, confidence) tuple; meanwhile the integration guide and the Phase 2 worker still treat generator.generate(ctx) as a raw string. That mismatch would break the integration unless the interface is frozen first.

There is a second real gap in the GUI plan. The roadmap says the model selector should come from Ollama’s model-list endpoint, but the unfinished GUI uses a free-text model field and its connection test calls .../models; its in-panel build_ai_config() exists, yet the worker launch only passes ai_config_path and workers, so the panel’s base URL, model, timeout, and fallback settings are not actually wired into the backend path. Ollama’s documented local endpoints include GET /api/tags for model listing and GET /api/version for version checks, and Ollama exposes OpenAI-compatible APIs plus structured outputs guidance for deterministic integrations.

There is also a product-quality gap the roadmap only partly addresses: your earlier notes already point out that the current approach can be syntax-safe yet still fail repo-specific documentation conventions, including public-surface and EXPOSES-style mismatches. For a multi-module project, the missing piece is not just “better prompts,” but a repository policy layer that teaches the generator what your project considers a correct module/class/function docstring.

Here is the improved full numbered roadmap I would use.

    Freeze the contract of the existing tool before adding AI.
    Keep the current AST discovery, insertion points, exclusion rules, scan/diff/write behavior, BOM handling, and syntax re-parse exactly as the stable core. AI must be an additive generation backend, never a rewrite of the safe file-edit pipeline. That principle is already present in the roadmap and integration notes, and it is the right foundation.

    Add a repository policy layer before prompt tuning.
    Create a docstring_policy.py or docstring_policy.json that defines style (numpy), required sections, whether private symbols are included, how __init__ and @property should be documented, max line length, and any repo-specific module-header rules. Add project-specific rules for public exports, re-exports, and any manifest/EXPOSES convention your repo expects, because that is where the current approach was already shown to fall short.

    Replace the unstable generate() contract with a single typed result object.
    Do not let generate() sometimes mean str and sometimes mean tuple[str, str]. Freeze it as something like GenerationResult(body, confidence, used_ai, fallback_reason, warnings, cache_hit). That removes the current interface drift between the roadmap, integration guide, and worker.

    Introduce a provider abstraction, not a model-specific implementation.
    Create llm_client.py with one interface such as generate_structured(prompt, schema, config). Make the first provider Ollama because the discussions already target local OpenAI-compatible usage, but keep the worker unaware of the vendor. For Ollama, standardize health/model discovery on documented endpoints like /api/version and /api/tags, and keep generation on the OpenAI-compatible surface.

    Stop asking the model for raw free-form docstrings as the primary protocol.
    Use structured output instead: summary, parameters, returns, raises, notes, confidence, and uncertainty reasons in JSON, then render the final NumPy-style docstring in Python. This is a major improvement over the current “raw body + optional confidence comment” idea because it removes fragile parsing and keeps formatting deterministic. Ollama’s docs explicitly recommend structured outputs and low temperature for reliable deterministic completions.

    Keep context_builder.py, but scope it to the smallest useful context first.
    Start with symbol source, signature, decorators, imports, enclosing class, sibling docstrings, and module id. That is already the strongest part of the proposed design. Cap source length, sibling count, and import count so prompts stay bounded on very large modules. Add a prompt_version field so cache invalidation is intentional.

    Implement sequential AI mode first and treat it as the acceptance baseline.
    Wire --ai into the worker exactly once, but only for sequential processing at first. Preserve scan, diff, and write semantics unchanged. The roadmap already says correctness should come before parallelism, and that is the right order for a multi-module codebase.

    Add a strict validator that owns quality control, not the prompt.
    After the model returns structured content, validate: known parameter names only, no invented returns, no echoed code, max line length, no empty summary, no markdown fences, and syntax-valid insertion. Keep heuristic fallback on validation failure. The roadmap already moves in this direction; make the validator the gatekeeper.

    Add project-aware validation, not only symbol-aware validation.
    Beyond per-function correctness, validate repo conventions: public symbol coverage, module export rules, whether module docstrings reflect actual public API, and whether project-required sections are present. This is the step that actually improves the project rather than merely inserting text into files.

    Implement two-pass enrichment only after Step 8 is stable.
    Do module summary first, then class docstring, then methods. Keep __init__-derived Attributes, decorator-aware handling for @property, @staticmethod, @classmethod, and skip @overload stubs. These are solid second-wave improvements, but they should not come before the core contract and validator are stable.

    Change uncertainty handling from source-code comments to review metadata.
    The roadmap proposes appending # AI-UNCERTAIN into source. I would not do that in the MVP. Instead, expose confidence, fallback_used, and review_required in scan JSON, diff output, and GUI state. That keeps source files clean and avoids churn from machine-only comments. The existing notes already show confidence as optional, so this is an easy improvement in how it is surfaced.

    Add caching with stronger cache keys.
    Cache by symbol-source hash plus signature plus module id plus model name plus prompt version plus policy version. The roadmap already proposes source-hash caching; extend it so cache hits are invalidated when you change the renderer, validator, or policy rules, not just the symbol text.

    Add parallelism only for AI mode, and only by file.
    The Phase 2 plan is sound here: parallelize when AI is on, because local HTTP calls are the bottleneck; keep heuristic mode simple and sequential. Do per-file concurrency first. Keep per-symbol batching as a later, provider-dependent optimization rather than a foundation.

    Fix the GUI wiring before adding more GUI surface area.
    First make the AI panel real: either serialize the in-panel values to a temp config file or pass a fully materialized config object into the worker path. Change connection tests to documented Ollama endpoints, add model discovery from /api/tags, and only then add richer UI like previews. Right now the unfinished GUI exposes AI settings that are not fully connected to execution.

    Add a real review workflow before auto-write on large repos.
    For large projects, the safe rollout is: scan --ai → diff --ai → package-level approval → write --ai on a bounded subset. In the GUI, add a file/symbol review list before adding a free-form preview pane. In CLI mode, emit machine-readable JSON for “low confidence”, “fallback used”, and “validator warning” so CI or a human reviewer can gate writes. This follows the existing safe scan/diff/write model instead of replacing it.

    Add observability so you can improve quality with evidence.
    Write one JSONL audit file per run with file path, symbol, model, latency, cache hit, fallback reason, validation warnings, and whether the docstring was written. Ollama’s API exposes usage/performance metrics such as durations and token counts, which makes this straightforward if you choose to capture them.

    Build a benchmark suite before calling the AI path “done.”
    Create a small golden corpus of modules from your repo: simple utilities, dataclasses, service classes, decorators, async code, properties, overloaded APIs, and package __init__ files. Measure syntax validity, validator pass rate, fallback rate, human approval rate, and repo-policy pass rate. Without this, the roadmap remains a code-generation exercise instead of a product-quality improvement.

    Roll out in three releases, not one.
    Release 1: sequential AI, structured output, validator, fallback, cache.
    Release 2: two-pass enrichment and repo-policy validation.
    Release 3: parallelism, GUI model discovery, review workflow, and reporting.
    That ordering keeps risk low and matches the strongest parts of the notes: additive integration first, optimization later.

My recommended immediate next move is this: freeze Step 3 first — define GenerationResult, DocstringPolicy, and LLMClient before changing any more worker code. That single decision will remove most of the current roadmap drift and make the rest of the implementation much easier to land cleanly.

004 Roadmap AI-Powered Docstring Inserter continue.md
File
not implemented yet ai_config.py
Python
not implemented yet ai_docstring_generator.py
Python
not implemented yet context_builder.py
Python
not implemented yet docstring_validator.py
Python
not implemented yet insert_missing_docstrings.py
Python
not implemented yet insert_missing_docstrings_gui.py
Python
not implemented yet INTEGRATION_GUIDE.py
Python
not implemented yet module_summarizer.py
Python
not implemented yet parallel_runner.py
Python
PHASE3_PATCH.py
Python
PHASE4_PATCH.py
Python
wait I have some more ideas , what you think about them? files are updated check and see if they can help in roadmap

Yes — these updated files definitely help the roadmap.

They make the plan much more concrete and much closer to an implementable architecture, especially in three areas that were previously weak: module-level context, post-generation validation, and operational controls like confidence thresholds, private-symbol handling, and run statistics.

What got materially better:

    module_summarizer.py is a strong addition.
    This is one of the best new ideas. It adds a pre-pass that first does static AST profiling of classes and __init__ attributes, then makes one AI call per module to produce a compact module summary block that gets injected into later symbol prompts. That should improve coherence across large multi-module projects much more than isolated per-function prompting.

    docstring_validator.py makes the roadmap much safer.
    This is the biggest architectural improvement. The validator now has a dedicated ValidationConfig, structured ValidationResult, fatal vs warning checks, confidence scoring, invented-parameter and invented-raises guards, section-order checks, line-length checks, and source-echo detection. That changes the tool from “AI inserts text” into “AI proposes text, validator decides acceptance.” That is exactly what a large-project rollout needs.

    The generator is now observability-aware, not just prompt-aware.
    GenerationStats, on_low_confidence, cached/AI/fallback counters, and summary_line() are all useful additions. They will help you measure quality per run and make the GUI/CLI practical for reviewing results rather than blindly trusting them.

    The context model is much richer now.
    The upgraded context_builder.py adds useful fields such as module_summary_block, class_attributes, raises_types, overload siblings, decorator-aware flags, dataclass/init flags, and cached-property/property routing. That is a meaningful improvement over the earlier, simpler symbol context.

    The Phase 3 and Phase 4 wiring patches make the roadmap executable.
    The patches show how to connect the new pieces into the existing worker without replacing the safe AST/insertion pipeline. The Phase 3 patch adds the module-summary pre-pass and two-pass __init__ flow; the Phase 4 patch adds CLI/GUI controls for private symbols, minimum confidence, uncertainty annotation, and low-confidence logging.

So yes, these updates should change the roadmap.

I would now revise the roadmap order to this:

    Core AI integration — context_builder, ai_config, ai_docstring_generator, heuristic fallback. This is still the foundation.

    Validator before scale — add docstring_validator and confidence gating before parallelism or GUI richness. Your newer files now strongly support this sequencing.

    Module summarization and class/context propagation — add module_summarizer, two-pass __init__, attribute extraction, raises extraction, overload handling.

    Parallelism and run reporting — then scale with parallel_runner and generation stats once correctness is gated.

    GUI controls and review UX — confidence selector, include-private toggle, uncertainty toggle, progress, review-first flow.

    Policy layer for repo-specific docstring rules — this is still missing and should be added next, because your current updates improve technical safety but still do not fully encode project-specific documentation conventions. That gap was already visible in the earlier roadmap review.

What I would keep, but slightly change:

    I would keep the confidence system, but I would not default to writing # AI-UNCERTAIN into source files. It is useful for review, but better surfaced in scan/diff/GUI metadata first. The current validator and config support this behavior, but I would make it opt-in rather than the default production path.

    I would keep the module pre-pass, but treat it as Phase 3, not MVP. It is valuable, but the validator is more important than module summarization for the first safe release.

    I would keep the private-symbol controls because they are useful for real-world repos and are now consistently wired through config and patches.

My bottom line: the new files improve the roadmap a lot. They turn it from “good concept” into a more production-shaped design. The two strongest additions are docstring_validator.py and module_summarizer.py; together they give you both safety and better semantic context, which are the two hardest parts of using local AI on a large Python codebase.

The next best step is to rewrite the roadmap around these updated phases so it becomes one clean implementation plan instead of several evolving drafts.

do it , complete and numered , to be followed , step by step in next moment

I’m consolidating everything into one implementation-ready sequence now, using the updated roadmap notes and the newer AI modules so the steps line up cleanly.

Here is the clean, complete, numbered roadmap to follow step by step.

It is ordered so you build correctness first, then context quality, then scale, then UX. That order matches the strongest parts of the updated roadmap and code: the original plan makes the AI generator a drop-in replacement for the heuristic builders, the validator hardens acceptance, the module summarizer improves coherence, and the later patches add CLI/GUI controls and reporting.
Final Step-by-Step Roadmap
1. Freeze the architecture boundary

Do not redesign the existing safe worker pipeline. Keep the current AST parsing, missing-docstring detection, insertion-point calculation, BOM-safe I/O, scan/diff/write modes, and syntax re-parse after generation. AI should replace only the docstring-generation path, not the file-editing safety path.

Deliverable: a short architecture note defining the stable core vs AI extension points.
Done when: everyone agrees that insert_missing_docstrings.py remains the authoritative edit engine.
2. Establish the MVP target

The MVP is: local AI generates candidate docstrings, validator accepts or rejects them, heuristic fallback fills the gaps, and scan/diff/write still behave the same. This is already the intended shape in the roadmap and integration guide.

Deliverable: one-page MVP scope.
Done when: the team agrees that GUI polish, batching, and advanced review UX are not required for first release.
3. Create and finalize ai_config.py

Implement AIConfig first and treat it as the central runtime contract for the AI path. The updated version now needs connection settings, model selection, timeout, max tokens, cache controls, worker count, include-private behavior, confidence threshold, line-length and TODO-density limits, hallucination guard toggles, and uncertain-annotation behavior.

Deliverable: AIConfig with from_json(), to_json(), defaults, and validation_config() mapping.
Done when: the worker, generator, validator, and GUI can all read from one config object.
4. Build the first real SymbolContext in context_builder.py

Implement the context layer before touching prompts. The base roadmap already required source lines, signatures, imports, enclosing class, sibling docstrings, and decorators. The upgraded version should also carry module summary context, class attributes, raises types, overload siblings, decorator-routing flags, dataclass/init flags, and class/method mode flags.

Deliverable: SymbolContext, ParameterInfo, AttributeInfo, and build_module_context(), build_class_context(), build_function_context().
Done when: every missing symbol can be represented without extra parsing passes beyond the file AST.
5. Build ai_docstring_generator.py as the only AI entry point

Create a single generator responsible for prompt building, local model calls, sanitization, cache lookup, validation handoff, and heuristic fallback. The earlier roadmap already made this the core drop-in replacement for the three build_*_docstring() functions, and the updated version adds statistics, private-symbol routing, and low-confidence callbacks.

Deliverable: AIDocstringGenerator with generate(ctx) and flush_cache().
Done when: the worker can call one object regardless of whether the output came from AI, cache, or heuristic fallback.
6. Wire AI into the worker sequentially first

Before adding parallelism, integrate AI into insert_missing_docstrings.py in the simplest way: thread an optional generator through collect_changes() and collect_missing_docstring_insertions(), and replace the three direct builder calls with context-aware AI generation when enabled. This is explicitly described in the integration guide.

Deliverable: a sequential --ai path in the worker.
Done when: --scan --ai, --diff --ai, and --write --ai all work with the same safety behavior as heuristic mode.
7. Add a standalone validator before any scaling work

Implement docstring_validator.py next, before parallelism or GUI work. The updated validator is the strongest addition in the newer files: it separates fatal checks from warning checks, returns a ValidationResult, scores confidence, and cross-checks parameters and raised exceptions against AST ground truth.

Deliverable: ValidationConfig, ValidationResult, and validate().
Done when: invalid or hallucinated output is rejected automatically and routed to fallback.
8. Put confidence scoring under validator control

Confidence should not be a free-form model claim. It should be derived from validator results and configurable through min_confidence. The newer Phase 4 design already sets this direction and adds optional uncertainty annotation for low-confidence output.

Deliverable: confidence levels high|medium|low enforced by config.
Done when: accepted low-quality output is visible in logs/UI and rejected output falls back safely.
9. Add generation statistics and review hooks

Use the updated GenerationStats model and low-confidence callback. This gives you practical run visibility: total generated, cache hits, accepted AI outputs, fallbacks, low-confidence counts, and skipped-private counts.

Deliverable: stats summary at the end of each run plus low-confidence event callbacks.
Done when: you can answer “how well did AI do on this run?” without reading diffs manually.
10. Add cache support after validation is stable

Keep on-disk caching in the generator so unchanged symbols are not re-sent to the local model. The existing AI roadmap already identified source-hash caching as important for large projects, and the updated generator keeps cache-aware counters.

Deliverable: cache keyed by source-driven identity and flushed safely at end of run.
Done when: repeated --scan --ai runs on unchanged code avoid unnecessary model calls.
11. Add module_summarizer.py as the first semantic upgrade

Once the sequential AI + validator path is stable, add the module pre-pass. The updated Phase 3 files make this clear: one AI call per module produces a one-liner and paragraph, while AST profiling extracts class structure and __init__ attributes. That summary is then injected into all downstream symbol prompts.

Deliverable: ModuleSummary, ClassProfile, and build_module_summary().
Done when: symbol prompts in the same file share a coherent understanding of module purpose.
12. Implement two-pass __init__ and class attribute propagation

Next, use the Phase 3 pattern: generate or inspect __init__ first, then feed its results into class docstring generation. The roadmap evolution consistently points toward Attributes sections derived from __init__ and self.<attr> assignments rather than guesses.

Deliverable: two-pass class handling and attribute-aware class context.
Done when: class docstrings can describe real attributes with hints from code, not generic placeholders only.
13. Add decorator-aware routing and raises extraction

After class-context propagation, complete the semantic routing logic: suppress Parameters for @property and @cached_property, mark @staticmethod and @classmethod, capture explicit raises targets, collect overload siblings, and skip documenting @overload stubs themselves. These exact upgrades are called out in the updated context_builder.py and Phase 3 notes.

Deliverable: full decorator- and raises-aware context extraction.
Done when: prompts no longer need to guess which sections belong in the final docstring.
14. Upgrade the worker with the Phase 3 patch

Apply the targeted worker patch only after Steps 11–13 are ready. The Phase 3 patch specifically adds the module_summarizer import and replaces the body of collect_missing_docstring_insertions() so module-summary context and two-pass __init__ behavior are used during insertion generation.

Deliverable: patched worker function using module summary + two-pass generation.
Done when: AI generation uses module context everywhere but failures still degrade safely to heuristic behavior.
15. Add parallelism only after correctness is proven

Now add parallel_runner.py. The roadmap was right to place parallelism after correctness. The parallel engine is per-file and fits the local-LLM-over-HTTP model well.

Deliverable: run_parallel() plus per-file progress snapshots.
Done when: AI mode scales across many modules without changing output semantics.
16. Expand CLI flags after the backend is stable

Once the core path works, add operational flags: --ai, optional config path, --workers, --private/--no-private, --min-confidence, and uncertainty toggles. The updated Phase 4 patch defines these cleanly and forwards them into AIConfig and the worker.

Deliverable: complete CLI surface for AI mode.
Done when: operators can tune behavior without editing code.
17. Update the GUI only after CLI behavior is trustworthy

The roadmap already places the GUI after backend stabilization, and that is still the right order. The GUI should add an AI settings panel, progress reporting, confidence controls, private-symbol toggle, uncertainty toggle, and low-confidence highlighting. The newer patch notes also tie this to DocstringRunWorker.

Deliverable: backend-complete GUI, not a speculative GUI.
Done when: the GUI is only a frontend over already-correct worker behavior.
18. Add a human review workflow for large projects

Before broad write-mode rollout, standardize the operating sequence: scan --ai, then diff --ai, then selective or approved write --ai. The roadmap already emphasizes that diff mode remains structurally identical, which is useful because it lets AI output flow through an already safe review surface.

Deliverable: team runbook for human review.
Done when: AI-generated changes are reviewed like normal code changes, not silently committed.
19. Define acceptance metrics before calling it done

Measure at least: validator rejection rate, fallback rate, cache hit rate, low-confidence rate, files changed per run, syntax-safety rate, and manual approval rate. The updated generator stats and validator design make this measurable now.

Deliverable: a small benchmark folder and run report format.
Done when: you can compare models, prompts, and config changes with evidence.
20. Roll out in three releases

Release 1: sequential AI integration + validator + fallback + cache.
Release 2: module summarizer + two-pass class context + decorator/raises/overload handling.
Release 3: parallel runner + full CLI options + GUI progress/review controls. This sequence is the best fit for the updated files and the recommended implementation order already stated in the roadmap.
Recommended execution order for your next session

    Finalize ai_config.py.

    Finalize context_builder.py.

    Finalize ai_docstring_generator.py with heuristic fallback only.

    Integrate sequential --ai into insert_missing_docstrings.py.

    Add docstring_validator.py and confidence gating.

    Add stats and cache.

    Add module_summarizer.py.

    Apply the Phase 3 worker patch.

    Apply the Phase 4 CLI/GUI patch.

    Add parallel_runner.py.

    Do benchmark runs on a medium project before broad rollout.

Most important rule

Do not start with parallelism or GUI. Start with sequential AI + validator + fallback. That is the safest path and it is consistent with the roadmap’s own recommended implementation order.

I can turn this next into a contractor-ready SPEC document in your architecture format.

go

I’m turning the roadmap into a buildable architecture spec now, using the worker, validator, module summarizer, and wiring patches as the baseline so the plan is directly implementable.

I have enough to write the spec. I’m keeping it implementation-first: stable worker core, AI generator as an additive backend, validator-gated acceptance, then module summarization, then scale and GUI.
SPEC-1-AI-Powered-Local-Docstring-Inserter
Background

The current project already has the right safety-oriented base: it parses Python files with ast, preserves BOM and line endings, skips excluded paths, computes insertion points without rewriting unrelated code, and supports scan, diff, and write modes. Its main limitation is that docstring generation is still heuristic, driven by name-prefix rules rather than actual code understanding. The roadmap and patch files consistently aim to keep that safe worker core intact while replacing only the docstring-generation path with a local AI backend.

The newer design iterations materially improve that direction by adding a richer SymbolContext, a standalone validator with confidence scoring, a module-level summarizer, optional parallel execution, and CLI/GUI controls for confidence thresholds, private-symbol handling, and uncertainty reporting. Together, those changes move the project from “AI text insertion” toward “AI proposal + deterministic validation + safe codemod.”

This specification defines the MVP and the full implementation path for a contractor team to build the local-AI version cleanly, with one important improvement over the draft notes: the generator contract must be frozen to a single typed result, because the roadmap evolved from generate(...) -> str toward confidence-aware flows and low-confidence annotations, and that interface drift should be resolved before coding continues.
Requirements
Must have

    Preserve the current worker safety model: AST-based detection, BOM-safe I/O, syntax re-parse after insertion, and scan / diff / write compatibility.

    Add a local-AI generation path that is optional and additive; when AI is disabled, the tool must behave like the current heuristic tool.

    Build rich symbol context from existing AST data, including source lines, signature, decorators, imports, sibling docstrings, enclosing class, and module identity.

    Validate every AI-generated docstring before accepting it, with fatal checks, warning checks, and configurable minimum confidence.

    Fall back to heuristic generation on AI timeout, validation failure, or local model unavailability.

    Support local config via ai_config.json and CLI overrides for workers, confidence, private symbols, and uncertainty annotation.

    Support module-level pre-pass summarization and class-aware context propagation after the baseline AI path is stable.

    Expose per-run stats and low-confidence events for review.

Should have

    Per-file parallel execution for AI mode only.

    GUI AI settings panel, progress bar, and review-oriented controls.

    Cache AI results for unchanged symbols.

    Decorator-aware routing for @property, @cached_property, @staticmethod, @classmethod, and @overload.

    Explicit handling for __init__-derived class attributes and Raises extraction.

Could have

    Symbol-level preview/approval UI before write.

    Optional uncertainty annotation in generated source.

    Later support for non-NumPy docstring styles. The current config explicitly reserves style as "numpy" only.

Won’t have in MVP

    Remote hosted inference as a required dependency.

    Full semantic correctness guarantees for arbitrary business logic.

    Automatic refactoring beyond inserting missing docstrings.

    External database storage; MVP persists only JSON config and JSON cache/report artifacts.

Method
1. System boundary

The product is a safe codemod tool with local AI assistance, not a general coding assistant. The authoritative edit pipeline remains the worker script. AI participates only in producing candidate docstring bodies; the worker still owns detection, insertion placement, re-parse validation, diff generation, and file writes. This boundary is already the core architectural decision in the roadmap and integration guide, and it should remain fixed.
2. Runtime architecture

The system is composed of seven runtime parts:

    insert_missing_docstrings.py as the main worker and codemod engine.

    context_builder.py as the AST-to-context translation layer.

    ai_docstring_generator.py as the only AI-facing generation service.

    docstring_validator.py as the acceptance gate.

    module_summarizer.py as the optional pre-pass semantic augmenter.

    parallel_runner.py as the per-file executor for AI mode.

    insert_missing_docstrings_gui.py as the desktop frontend over the worker.

The MVP should first implement parts 1–4 in sequential mode. Parts 5–7 are layered on after the baseline path is correct. That sequencing is explicitly recommended in the roadmap.
3. Architectural correction: freeze the generator contract

The evolving drafts imply two incompatible generator contracts: an early generate(ctx) -> str design and a later confidence-aware path that expects uncertainty handling and low-confidence reporting. The implementation must resolve that by standardizing on a typed return object.

Use this contract:

from dataclasses import dataclass, field
from typing import Literal

@dataclass
class GenerationResult:
    body: str
    source: Literal["ai", "cache", "heuristic"]
    confidence: Literal["high", "medium", "low"]
    issues: list[str] = field(default_factory=list)
    cache_hit: bool = False
    used_fallback: bool = False
    uncertain: bool = False

And this interface:

class AIDocstringGenerator:
    def generate(self, ctx: SymbolContext) -> GenerationResult: ...
    def flush_cache(self) -> None: ...

This single decision removes ambiguity from worker integration, validator wiring, GUI review state, and reporting.
4. Persisted state

There is no external database in MVP. Persist only local JSON artifacts:

ai_config.json

{
  "base_url": "http://localhost:11434/v1",
  "model": "qwen2.5-coder:14b",
  "timeout_seconds": 25.0,
  "max_tokens": 512,
  "temperature": 0.05,
  "fallback_to_heuristic": true,
  "workers": 4,
  "cache_enabled": true,
  "cache_path": ".docstring_cache.json",
  "docstring_style": "numpy",
  "include_private": true,
  "min_confidence": "medium",
  "max_line_length": 88,
  "max_todo_ratio": 0.4,
  "allow_invented_params": false,
  "allow_invented_raises": false,
  "uncertain_annotation": true
}

This field set is already present in the updated Phase 4 config design.

.docstring_cache.json

{
  "<cache_key>": {
    "body": "Normalize the input path.",
    "confidence": "high",
    "issues": [],
    "model": "qwen2.5-coder:14b",
    "prompt_version": "v1",
    "policy_version": "v1"
  }
}

run_report.jsonl

{"path":"pkg/a.py","symbol":"parse_source","source":"ai","confidence":"high","cache_hit":false,"issues":[]}
{"path":"pkg/b.py","symbol":"_resolve","source":"heuristic","confidence":"low","cache_hit":false,"issues":["validator rejected AI output"]}

The cache and run report are local artifacts only. A future SQLite store is optional, but not part of MVP.
5. Component behavior
5.1 Worker

The worker remains responsible for file discovery, exclusion logic, AST parse, missing-docstring detection, insertion-point computation, diff rendering, and write safety. In AI mode it receives an optional generator and optional progress callbacks, but it still decides what to insert and where.
5.2 Context builder

context_builder.py builds SymbolContext from the already parsed AST. The upgraded design includes module summary block, class attributes, raised exception types, overload siblings, and decorator-specific flags such as is_property, is_cached_property, is_staticmethod, is_classmethod, is_overload, is_dataclass, and is_init. That is the right shape for accurate prompt assembly.
5.3 Generator

The generator builds prompts, calls the local model through the configured endpoint, normalizes the raw model output, calls the validator, consults the cache, and falls back to heuristics when needed. The updated design already includes GenerationStats, include_private routing, and low-confidence callbacks.
5.4 Validator

The validator is the hard gate. It performs fatal and warning checks, derives confidence, and decides acceptance via min_confidence. The updated design explicitly includes invented-parameter detection, invented-raises detection, line-length checks, section ordering, and source-echo detection.
5.5 Module summarizer

The module summarizer performs one AST-only structure pass and one optional AI summary pass per file. It creates ModuleSummary plus ClassProfile data, including __init__ params and self.<attr> assignments. Its output becomes shared context for all per-symbol generation in that module.
5.6 Parallel runner

Parallel execution is per file and activates only when AI mode is enabled and workers > 1. Heuristic mode stays sequential. That is the existing roadmap decision and should remain unchanged.
5.7 GUI

The GUI remains a wrapper over the worker. The upgraded design adds an AI settings panel, progress reporting, min-confidence selection, private-symbol toggle, and uncertainty toggle. Symbol preview is explicitly optional and should not block MVP.
6. Core algorithms
6.1 Per-file baseline algorithm

    Walk the project tree and filter excluded paths.

    Read source and preserve BOM state.

    Parse with ast; skip parse failures.

    Detect missing module/class/function docstrings.

    For each missing symbol, build SymbolContext.

    Generate a GenerationResult.

    If AI output fails validation or confidence threshold, use heuristic fallback.

    Wrap accepted body in triple quotes, preserve indentation, and queue insertion.

    Apply insertions in memory.

    Re-parse generated source; reject invalid modifications.

    Emit scan JSON, diff, or write updates depending on mode.

6.2 Module-aware algorithm

After baseline AI is stable, add the Phase 3 pre-pass:

    Parse module once.

    Build static ModuleSummary / ClassProfile structure.

    Attempt one AI summary call for module purpose.

    Store module_summary.context_block.

    Generate __init__ docstrings first per class.

    Generate class docstrings using __init__-derived attributes.

    Generate remaining functions/methods with shared module context, raises info, and overload siblings.

6.3 Confidence algorithm

Use validator-derived confidence, not raw model self-reporting:

    Start at high.

    Reduce to medium or low when warning checks fire.

    Reject when fatal checks fail.

    Reject when resulting confidence is below configured min_confidence.

6.4 Uncertainty policy

For MVP, store low-confidence state in logs, scan JSON, GUI labels, and run reports. Source-level # AI-UNCERTAIN annotation remains configurable but should default to off in production deployments even though the patch set supports it. This keeps source changes clean and review metadata separate. The files already support uncertainty annotation as a configurable behavior, so this spec narrows the default policy without discarding the feature.
7. PlantUML component diagram

This diagram reflects the component split already present in the roadmap and patch files, with the generator and validator placed between context creation and the worker’s final insertion pipeline.

@startuml
skinparam componentStyle rectangle

actor User
component GUI as "insert_missing_docstrings_gui.py"
component Worker as "insert_missing_docstrings.py"
component Context as "context_builder.py"
component Generator as "ai_docstring_generator.py"
component Validator as "docstring_validator.py"
component Summarizer as "module_summarizer.py"
component Parallel as "parallel_runner.py"
database Cache as ".docstring_cache.json"
file Config as "ai_config.json"
folder Project as "Python project files"

User --> GUI
User --> Worker
GUI --> Worker : run(mode, flags)
Worker --> Project : read / diff / write
Worker --> Context : build_*_context()
Worker --> Summarizer : build_module_summary()
Worker --> Generator : generate(ctx)
Generator --> Validator : validate(body, ctx, cfg)
Generator --> Cache : lookup / store
Worker --> Parallel : run_parallel()
Worker --> Config : load AIConfig
@enduml

8. PlantUML sequence diagram

The Phase 3 patch explicitly introduces module pre-pass and two-pass __init__ handling, so the runtime sequence must reflect that.

@startuml
actor User
participant Worker
participant Summarizer
participant Context
participant Generator
participant Validator

User -> Worker : run(--diff --ai)
Worker -> Worker : iter_python_files()
Worker -> Worker : parse_source()

opt AI enabled
  Worker -> Summarizer : build_module_summary()
  Summarizer --> Worker : ModuleSummary
end

opt Missing module docstring
  Worker -> Context : build_module_context()
  Context --> Worker : SymbolContext
  Worker -> Generator : generate(ctx)
  Generator -> Validator : validate(body, ctx, cfg)
  Validator --> Generator : ValidationResult
  Generator --> Worker : GenerationResult
end

loop __init__ methods first
  Worker -> Context : build_function_context(__init__)
  Worker -> Generator : generate(ctx)
  Generator -> Validator : validate(...)
  Generator --> Worker : GenerationResult
end

loop classes next
  Worker -> Context : build_class_context(class, init-derived attrs)
  Worker -> Generator : generate(ctx)
  Generator -> Validator : validate(...)
  Generator --> Worker : GenerationResult
end

loop remaining functions/methods
  Worker -> Context : build_function_context(node)
  Worker -> Generator : generate(ctx)
  Generator -> Validator : validate(...)
  Generator --> Worker : GenerationResult
end

Worker -> Worker : apply_insertions_to_text()
Worker -> Worker : parse_source(desired)
Worker --> User : diff / write / scan result
@enduml

9. Similar-product positioning

This product should be engineered like a deterministic code-quality tool with AI assistance, not like a free-form code assistant. In practical terms, that means the benchmark is predictable codemod behavior: AST-grounded context, strict validation, fallback on uncertainty, and review-friendly diff output. The roadmap itself already trends in this direction by keeping diff mode unchanged, keeping AI optional, and introducing a standalone validator and structured progress/reporting.
Implementation

    Stabilize contracts.
    Create GenerationResult, finalize AIConfig, and lock the SymbolContext schema. Do not begin worker rewiring until these three interfaces are fixed. This resolves the contract drift visible across roadmap phases.

    Implement baseline AI modules.
    Complete ai_config.py, context_builder.py, and ai_docstring_generator.py using sequential execution only. Use heuristic fallback and cache support, but do not yet add module summarization or parallelism.

    Wire AI into the worker.
    Follow the integration guide: pass an optional generator through collect_changes() and collect_missing_docstring_insertions(), and replace direct builder calls with context-aware generator calls. Maintain current behavior when AI is absent.

    Implement validator and confidence gates.
    Add docstring_validator.py, feed its ValidationConfig from AIConfig, and route failures to heuristic fallback. Add low-confidence callbacks and final run stats.

    Deliver CLI-complete backend.
    Add --ai, optional config path, --workers, --private/--no-private, --min-confidence, and uncertainty toggle handling. Print GenerationStats at end of AI runs.

    Add module summarization and two-pass class generation.
    Implement module_summarizer.py, apply the Phase 3 worker patch, and update context_builder.py to consume ModuleSummary and ClassProfile. Include Raises extraction and overload support.

    Add parallel execution.
    Integrate parallel_runner.py so AI mode can process files concurrently while heuristic mode remains sequential. Support on_file_complete and optional on_file_progress callbacks.

    Upgrade the GUI.
    Add AI settings, progress bar, min-confidence selector, private-symbol checkbox, and uncertainty toggle. Keep symbol preview optional until backend behavior is stable.

    Add run-report artifacts and benchmark corpus.
    Emit JSONL reports and create a test corpus containing utilities, dataclasses, async methods, overloaded APIs, properties, and __init__-heavy classes. This becomes the acceptance suite for model and prompt changes. The roadmap already emphasizes staged rollout and reviewable diff behavior; this formalizes it.

    Roll out in controlled stages.
    Use scan --ai, then diff --ai, then restricted write --ai on approved subsets of the repo. Do not enable broad write mode until validator rejection rate and manual approval rate are acceptable. This follows the existing operating model of the worker.

Milestones

    M1 — Baseline contracts finished
    AIConfig, SymbolContext, and GenerationResult are frozen and documented.

    M2 — Sequential AI path working
    --scan --ai and --diff --ai run successfully on a medium project with fallback enabled. This is the roadmap’s first recommended checkpoint.

    M3 — Validator-gated acceptance live
    All AI output passes through docstring_validator.py, and low-confidence events are visible in logs and stats.

    M4 — Phase 3 semantic enrichment live
    Module pre-pass, two-pass __init__, class attributes, raises extraction, and overload handling are integrated.

    M5 — Scalable execution live
    parallel_runner.py is integrated and stable under multi-worker runs.

    M6 — Reviewable product release
    CLI is complete, GUI is usable, benchmark corpus passes target thresholds, and staged write --ai rollout is approved.

Gathering Results

Success should be measured with operational metrics, not only code completion. Track at least:

    syntax-valid insertion rate after generation,

    validator rejection rate,

    heuristic fallback rate,

    low-confidence rate,

    cache hit rate,

    files changed per run,

    mean AI latency per symbol and per module,

    manual approval rate from diff review,

    false-positive rate for invented parameters or exceptions,

    user-reported usefulness of module and class docstrings.

These metrics are directly supported by the newer validator, generation stats, and patch-driven reporting model.

The acceptance gate for production rollout should be:

    zero invalid-Python writes,

    validator rejection rate low enough that AI materially reduces manual effort,

    manual approval rate high enough to justify write-mode use,

    low-confidence outputs clearly reviewable before commit,

    no regression in the original worker’s scan/diff/write safety guarantees.

Need Professional Help in Developing Your Architecture?

Please contact me at sammuti.com
:)

is that all ?

Not quite.

What I gave you is the full architecture spec and roadmap, but there are still 4 important deliverables missing before a contractor can execute without guessing:

    File-by-file implementation plan
    Exact changes per file: ai_config.py, context_builder.py, ai_docstring_generator.py, docstring_validator.py, module_summarizer.py, insert_missing_docstrings.py, parallel_runner.py, and insert_missing_docstrings_gui.py. The uploaded patches and guides already point in that direction, but they are still spread across roadmap notes and patch documents.

    A missing policy layer
    The current updated files define config, context, generation, validation, and summarization, but they still do not define a repo-specific documentation policy module that says what your project considers a “good” module/class/function docstring beyond generic NumPy-style rules. That is still the biggest architectural gap.

    A test and benchmark plan
    The validator and generation stats now make quality measurable, but we still need an explicit benchmark corpus and pass/fail matrix for rollout. The current files support this operationally, but do not yet define the benchmark suite itself.

    Execution packaging
    The spec is readable, but not yet transformed into contractor work units like:

        Task 1: implement config

        Task 2: implement context builder

        Task 3: wire sequential AI

        Task 4: add validator

        and so on

So the answer is:

    Yes, the roadmap/spec is complete at the architecture level.

    No, it is not yet the final execution pack.

The next strongest artifact to create is a numbered implementation checklist by file, with exact coding order, dependencies, and definition of done for each task.

go

I’m turning the spec into contractor-ready work units now: file by file, dependency ordered, with definition of done and what to test after each step.

Yes — here is the contractor-ready execution pack: exact coding order, by file, with dependencies, definition of done, and what to test after each step.
0. Lock one interface before touching code

Files: ai_docstring_generator.py, insert_missing_docstrings.py, INTEGRATION_GUIDE.py
Depends on: none

Work
Standardize the generator contract first. The draft materials describe both a simple generate(ctx) -> body flow and a later confidence-aware flow with uncertainty handling and low-confidence reporting. Freeze this to one return type before implementation continues. Recommended shape: GenerationResult(body, source, confidence, issues, cache_hit, used_fallback, uncertain). This prevents rework in the worker, GUI, and validator wiring.

Definition of done
Every call site expects exactly one generator return contract, and no patch text still assumes both “raw string only” and “string + confidence” at the same time.

Test
No code test yet; review the interface and update all stubs and docs first.
1. Implement ai_config.py

Files: ai_config.py
Depends on: Step 0

Work
Implement AIConfig with JSON load/save, defaults, and validation mapping. Include the Phase 4 fields: include_private, min_confidence, max_line_length, max_todo_ratio, allow_invented_params, allow_invented_raises, and uncertain_annotation, in addition to connection, model, timeout, token, cache, and worker settings. Also add a helper that maps config into validator settings so the generator does not duplicate validation config construction.

Definition of done
A JSON config file can be loaded, saved, and used without code edits, and Phase 4 CLI overrides have matching fields in config.

Test
Create a sample ai_config.json, load it, save it back, and verify the Phase 4 example fields survive round-trip.
2. Implement context_builder.py

Files: context_builder.py
Depends on: Step 0

Work
Build the context layer first. Start with the Phase 1 core fields: source lines, signature, decorators, enclosing class, sibling docstrings, imports, parameters, and return annotation. Then include the Phase 3 upgrades: module_summary_block, class_attributes, raises_types, overload_siblings, is_staticmethod, is_classmethod, is_cached_property, is_overload, is_dataclass, and is_init. Ensure @property and @cached_property suppress parameter lists, overload siblings are collected as hints, and raised exception types are extracted from ast.Raise.

Definition of done
build_module_context(), build_class_context(), and build_function_context() all return complete, deterministic SymbolContext objects from one parsed module tree.

Test
Unit-test with small modules containing: a plain function, a property, a staticmethod, a classmethod, an overloaded function, a nested class, and a function that raises exceptions. Validate produced flags and extracted fields.
3. Implement baseline ai_docstring_generator.py

Files: ai_docstring_generator.py
Depends on: Steps 1–2

Work
Implement the generator as the only AI-facing module. It should build prompts from SymbolContext, call the local endpoint with stdlib urllib.request, sanitize the response, optionally read/write cache, and fall back to the heuristic generator when AI fails. Keep this first version sequential and do not yet depend on module summaries or parallelism. The roadmap explicitly positions this as the most impactful change and the drop-in replacement for the existing build_* functions.

Definition of done
Given a SymbolContext, the generator can return an accepted docstring candidate or a heuristic fallback without changing the worker yet.

Test
Mock the local endpoint and verify: normal AI response, timeout, malformed response, and fallback behavior. Confirm cache keying is based on source/signature identity as described in the roadmap.
4. Wire sequential AI into insert_missing_docstrings.py

Files: insert_missing_docstrings.py, INTEGRATION_GUIDE.py
Depends on: Steps 1–3

Work
Apply the additive worker integration described in the guide. Add optional AI imports, thread generator through collect_changes() and collect_missing_docstring_insertions(), expose --ai [CONFIG], load AIConfig, create AIDocstringGenerator, and replace direct build_module_docstring, build_class_docstring, and build_function_docstring calls with context-aware generation when AI is enabled. Keep generator=None behavior identical to the original worker.

Definition of done
These commands work end to end without GUI: --scan --ai, --diff --ai, and --write --ai. Heuristic mode still works unchanged when --ai is absent.

Test
Run:

python insert_missing_docstrings.py --root /path/to/project --scan --ai
python insert_missing_docstrings.py --root /path/to/project --diff --ai

Then verify write mode on a small test project only.
5. Implement docstring_validator.py

Files: docstring_validator.py
Depends on: Steps 1–4

Work
Add the standalone validator before any scaling or deeper context work. Use the Phase 4 design: fatal checks plus warning checks, confidence scoring, structured ValidationResult, invented-parameter detection scoped to the Parameters section, invented-raises detection, section ordering, line-length enforcement, TODO-density checks, markdown/code-echo rejection, and source-verbatim detection.

Definition of done
Every AI output passes through validate(), receives ok/cleaned/confidence/issues, and can be rejected before insertion.

Test
Unit-test at least these cases: empty output, code fence output, echoed source, invented param, invented raises, wrong section order, overlong lines, and TODO-heavy but still nonfatal output.
6. Upgrade ai_docstring_generator.py to validator-gated generation

Files: ai_docstring_generator.py, ai_config.py
Depends on: Steps 1, 3, 5

Work
Replace any inline validator logic with the standalone validator. Add GenerationStats, on_low_confidence, include_private routing, and optional uncertain annotation support. The newer generator design already describes these counters and behaviors, and the Phase 4 patch expects stats printing and low-confidence callbacks from the worker.

Definition of done
The generator can report accepted AI outputs, low-confidence accepted outputs, fallbacks, cache hits, and skipped-private counts.

Test
Run the generator on a mix of public/private symbols and intentionally bad model responses. Confirm fallback, stats accumulation, and min-confidence behavior work.
7. Patch insert_missing_docstrings.py for Phase 4 controls

Files: insert_missing_docstrings.py
Depends on: Steps 1, 4, 5, 6

Work
Add CLI and runtime controls from Phase 4: --private/--no-private, --min-confidence, and --no-uncertain. Override the loaded config with explicit CLI values, pass on_low_confidence to the generator, and print GenerationStats after the run.

Definition of done
Operators can choose whether to include private symbols, require medium/high confidence, and suppress uncertainty annotation from CLI alone.

Test
Run:

python insert_missing_docstrings.py --root . --diff --ai --no-private --min-confidence medium --no-uncertain
python insert_missing_docstrings.py --root . --diff --ai my_config.json --min-confidence high --workers 6

Verify output includes low-confidence notices and final AI generation stats.
8. Add the missing docstring_policy.py layer

Files: docstring_policy.py (new), optionally ai_config.py, docstring_validator.py
Depends on: Steps 1, 5

Work
This file is not present in the uploaded implementation set, but it should be added. The current files define generic NumPy-style behavior and validation knobs, yet they do not encode repo-specific documentation policy. Add a policy module or JSON policy file that defines project conventions such as required sections, whether module docstrings are mandatory in __init__.py, whether private symbols should be documented by default, allowed TODO density by symbol kind, and any house rules for module/class/function summaries. This is the main architectural gap still missing from the roadmap artifacts.

Definition of done
Project-level documentation rules are centralized instead of scattered across prompts, config defaults, and validator heuristics.

Test
Create a sample policy and verify the validator/generator honor it for at least one module, one class, and one function.
9. Implement module_summarizer.py

Files: module_summarizer.py
Depends on: Steps 1–3

Work
Add the module pre-pass. Implement AST-only structural profiling first, producing ClassProfile and InitAttribute data. Then add the optional single AI call per module to generate one_liner and purpose_paragraph, falling back silently to heuristic summaries on any failure. This module is explicitly designed to be stateless and non-blocking to downstream symbol generation.

Definition of done
A module can produce a shared ModuleSummary with class inventory, public functions, constants, and a prompt-ready context_block.

Test
Use a file with multiple classes, constants, public functions, and __init__ attributes. Confirm the AST profile works without AI and the AI summary path fails safely.
10. Apply the Phase 3 worker patch

Files: insert_missing_docstrings.py
Depends on: Steps 2, 6, 9

Work
Apply the targeted Phase 3 patch: import build_module_summary, replace collect_missing_docstring_insertions() with the module-aware version, run one pre-pass summary call per file, forward module_summary into all build_*_context() calls, and change the symbol processing order to __init__ first, then classes, then remaining functions. This is the two-pass __init__ strategy. Also add is_overload_function() and skip overload stubs as direct documentation targets.

Definition of done
Per-symbol prompts in a module share module context, class docstrings can use __init__-derived information, and overload stubs are not documented independently.

Test
Run --diff --ai on a test module containing __init__, properties, overloads, and explicit raises. Confirm ordering and output shape match expectations.
11. Implement parallel_runner.py

Files: parallel_runner.py, insert_missing_docstrings.py
Depends on: Steps 4–7

Work
Add the per-file ThreadPoolExecutor engine with FileProgress, RunSummary, on_file_progress, and on_file_complete. Keep heuristic mode sequential; only activate parallel mode when AI is on and workers > 1. The roadmap is explicit that parallelism comes only after correctness is validated.

Definition of done
collect_changes() can route to either the original sequential loop or run_parallel() with equivalent results.

Test
Run the same project twice: once with --workers 1, once with --workers 4, and confirm identical diffs with better elapsed time under AI mode.
12. Upgrade insert_missing_docstrings_gui.py

Files: insert_missing_docstrings_gui.py
Depends on: Steps 7, 11

Work
Implement the AI settings panel and progress reporting after the backend is already stable. Add AI enablement, config path, workers, min-confidence selector, include-private checkbox, uncertainty checkbox, and progress bar wiring. Forward these values into DocstringRunWorker and then into module.run(...). The patches also call for status-bar messaging and output panel visibility for AI stats.

Definition of done
The GUI becomes a thin, accurate frontend over the already working CLI path and shows file progress plus AI settings that actually affect the backend.

Test
Run scan/diff from GUI with AI on and off, toggle min confidence and private symbol options, and verify the worker receives them and the output panel shows stats.
13. Add benchmark and rollout assets

Files: tests/ or benchmark/, run_report.jsonl generator, sample projects
Depends on: Steps 5–12

Work
Create a benchmark corpus with utilities, dataclasses, async functions, properties, overloads, explicit raises, __init__-heavy classes, and package __init__.py files. Use validator results, generation stats, and diff review to decide rollout readiness. The roadmap and patches already make these operational metrics observable; this step formalizes them.

Definition of done
You can measure rejection rate, fallback rate, cache hit rate, low-confidence rate, and manual approval rate for a controlled corpus before broad write-mode usage.

Test
Run the benchmark corpus in scan --ai, then diff --ai, and record the metrics for at least two models/configs.
14. Rollout sequence

Files: all
Depends on: Steps 1–13

Work
Roll out in this order, which matches the roadmap’s own recommended sequence: sequential AI integration first, validator before parallelism, deeper module/class context after baseline correctness, GUI last, and optional extras after the core is stable.

Definition of done
The team uses: scan --ai first, then diff --ai, then controlled write --ai only after validator and review metrics are acceptable.
Final coding order to hand to contractors

    Freeze generator contract.

    Implement ai_config.py.

    Implement context_builder.py.

    Implement baseline ai_docstring_generator.py.

    Wire sequential AI into insert_missing_docstrings.py.

    Implement docstring_validator.py.

    Upgrade generator to validator-gated mode with stats.

    Patch worker CLI/runtime controls for confidence/private/uncertainty.

    Add docstring_policy.py.

    Implement module_summarizer.py.

    Apply Phase 3 worker patch.

    Implement parallel_runner.py.

    Upgrade insert_missing_docstrings_gui.py.

    Build benchmark corpus and rollout checklist.

The strongest next move is to turn this into Task Cards 1–14 with assignee-ready acceptance criteria and estimated complexity.

continue

Here are the Task Cards 1–14 so a contractor team can execute without guessing.
Task Card 1 — Freeze the generator contract

Goal
Define one stable interface for AI generation and remove the current ambiguity between “return raw string” and “return confidence-aware result.” The roadmap, worker wiring, and Phase 4 logic already imply richer outcomes than a plain string, so this must be resolved first.

Files
ai_docstring_generator.py, insert_missing_docstrings.py, INTEGRATION_GUIDE.py

Depends on
None.

Acceptance criteria
Every documented and coded call path expects one return type only. The worker, validator, and GUI notes no longer describe conflicting contracts.

Complexity
M

Main risk
Contract drift continues and causes repeated rewiring in later steps.
Task Card 2 — Implement configuration as the runtime control plane

Goal
Finish AIConfig so all AI behavior is driven by config plus CLI overrides: endpoint, model, timeout, caching, workers, private-symbol behavior, confidence threshold, validator limits, and uncertainty annotation. The newer config draft already defines these fields.

Files
ai_config.py

Depends on
Task 1.

Acceptance criteria
from_json() and to_json() work, unknown keys fail fast, defaults are sane, and validator-related fields are exposed cleanly to downstream code.

Complexity
S

Main risk
Validation knobs end up duplicated between config and validator code.
Task Card 3 — Build the AST-to-context translation layer

Goal
Complete context_builder.py so the model receives grounded symbol context rather than only names and signatures. The updated design already includes parameters, decorators, sibling docstrings, raises types, overload siblings, class attributes, module summary blocks, and routing flags like property/static/class method.

Files
context_builder.py

Depends on
Task 1.

Acceptance criteria
build_module_context(), build_class_context(), and build_function_context() return deterministic contexts from one parsed module tree and correctly handle properties, overloads, explicit raises, and init-aware class data.

Complexity
M

Main risk
Too much context is included and prompts become noisy or slow.
Task Card 4 — Implement the baseline AI generator

Goal
Finish the first working AIDocstringGenerator that builds prompts, calls the local model, sanitizes output, uses cache if enabled, and falls back to the heuristic builder on failure. This is the core replacement for the current heuristic-only builders.

Files
ai_docstring_generator.py

Depends on
Tasks 1–3.

Acceptance criteria
Given a valid SymbolContext, the generator returns a usable generation result for success, timeout, malformed response, and fallback cases.

Complexity
M

Main risk
Prompt parsing and response cleaning stay too fragile.
Task Card 5 — Wire sequential AI into the worker

Goal
Integrate AI into the existing worker without changing its safety behavior. The integration guide already describes threading an optional generator through collect_changes() and collect_missing_docstring_insertions() and replacing direct builder calls only when AI is enabled.

Files
insert_missing_docstrings.py, INTEGRATION_GUIDE.py

Depends on
Tasks 1–4.

Acceptance criteria
scan, diff, and write all work in AI mode, and non-AI behavior remains identical to the current worker.

Complexity
M

Main risk
AI mode accidentally changes insertion semantics or bypasses re-parse safety.
Task Card 6 — Build the standalone validator

Goal
Implement docstring_validator.py as the acceptance gate. The updated validator design is a major improvement and should be treated as mandatory before scale work: fatal checks, warning checks, confidence scoring, invented-name guards, line-length checks, TODO-density checks, and cleaned output generation.

Files
docstring_validator.py

Depends on
Tasks 1–3.

Acceptance criteria
Every AI output can be classified into accepted or rejected with ok, cleaned, confidence, issues, and fatal reason fields.

Complexity
M

Main risk
The validator is either too strict and kills usefulness or too weak and lets hallucinations through.
Task Card 7 — Upgrade the generator to validator-gated mode

Goal
Replace any inline validation in the generator with the standalone validator and add operational reporting: GenerationStats, low-confidence callbacks, private-symbol routing, and optional uncertainty annotation. The updated generator draft already expects these features.

Files
ai_docstring_generator.py, ai_config.py

Depends on
Tasks 2, 4, 6.

Acceptance criteria
The generator reports counts for AI success, fallback, low confidence, medium confidence, cache hits, and skipped private symbols, and it routes rejected outputs to heuristics.

Complexity
M

Main risk
Stats and review signals become inconsistent with actual inserted output.
Task Card 8 — Patch worker runtime controls for Phase 4

Goal
Add and wire --private/--no-private, --min-confidence, and --no-uncertain, plus stats printing and low-confidence notices. The Phase 4 patch already describes these exact changes.

Files
insert_missing_docstrings.py

Depends on
Tasks 2, 5, 6, 7.

Acceptance criteria
CLI flags override config correctly, low-confidence messages are emitted, and end-of-run AI stats are printed.

Complexity
S

Main risk
Config values and CLI overrides conflict in unclear ways.
Task Card 9 — Add the missing policy layer

Goal
Create docstring_policy.py to encode repo-specific documentation rules. This is not in the uploaded implementation set, but it is still the biggest architectural gap: the current design is technically safe, yet still generic. Add policy for required sections, private-symbol defaults, module docstring behavior, style limits by symbol kind, and project-specific rules. The existing config and validator support this direction, but no policy module exists yet.

Files
docstring_policy.py (new), optionally ai_config.py, docstring_validator.py

Depends on
Tasks 2 and 6.

Acceptance criteria
Repo-specific docstring rules are centralized and consumable by both generator and validator.

Complexity
M

Main risk
Without this layer, the tool remains high-quality but generic rather than project-improving.
Task Card 10 — Implement module summarization

Goal
Add module_summarizer.py as the first semantic upgrade after the baseline AI path is stable. The updated design is strong here: one AI call per module, backed by AST-only class and init-attribute profiling, creates a shared module context block that improves coherence across all symbol prompts in the same file.

Files
module_summarizer.py

Depends on
Tasks 2–4.

Acceptance criteria
A file can produce a ModuleSummary with one-liner, purpose paragraph, class inventory, public functions, constants, and init-derived structural hints, while failures stay non-fatal.

Complexity
M

Main risk
The pre-pass adds cost without enough quality gain if prompts are not carefully bounded.
Task Card 11 — Apply the Phase 3 worker patch

Goal
Patch the worker to use module summaries and two-pass class generation. The patch text already specifies the changes: import the summarizer, build one module summary per file, pass it into all context builders, and generate __init__ before class bodies so class docstrings can use attribute data. It also adds overload-skipping behavior.

Files
insert_missing_docstrings.py

Depends on
Tasks 3, 7, 10.

Acceptance criteria
Module-aware prompts are used consistently, class generation can see init-derived attributes, and overload stubs are not documented as independent implementations.

Complexity
L

Main risk
Ordering bugs in the symbol loop cause inconsistent or duplicated insertions.
Task Card 12 — Add per-file parallelism

Goal
Implement parallel_runner.py and wire it into the worker for AI mode only. The roadmap and draft runner are already aligned on per-file ThreadPoolExecutor execution with FileProgress and RunSummary.

Files
parallel_runner.py, insert_missing_docstrings.py

Depends on
Tasks 5–8.

Acceptance criteria
Runs with workers > 1 produce the same output as sequential mode while improving AI throughput and exposing file-complete progress snapshots.

Complexity
M

Main risk
Shared state such as stats, cache writes, or callbacks becomes race-prone.
Task Card 13 — Upgrade the GUI last

Goal
Update the GUI only after the CLI path is stable. Add AI settings, workers, min-confidence, private-symbol toggle, uncertainty toggle, and progress bar support. The newer GUI and Phase 4 patch already point in this direction, and they should remain a thin frontend over the working backend.

Files
insert_missing_docstrings_gui.py

Depends on
Tasks 8 and 12.

Acceptance criteria
The GUI launches the same worker behavior as CLI AI mode, shows progress, and exposes the new runtime controls accurately.

Complexity
M

Main risk
GUI options drift from actual backend semantics.
Task Card 14 — Build benchmarks and rollout gates

Goal
Create a benchmark corpus and operational rollout checklist. The newer validator and generator stats make this practical now, but the benchmark suite itself still needs to be defined. Include modules with utilities, dataclasses, async code, properties, overloads, explicit raises, and init-heavy classes.

Files
benchmark/ or tests/, sample projects, run report scripts

Depends on
Tasks 6–13.

Acceptance criteria
You can measure validator rejection rate, fallback rate, cache hit rate, low-confidence rate, diff approval rate, and write-safety rate before enabling broad write-mode use.

Complexity
M

Main risk
The team ships based on impressions instead of evidence.
Delivery sequence by release

Release 1
Tasks 1–8. This gives you sequential AI, validator gating, fallback, config, stats, and operator controls. That is the minimum safe product.

Release 2
Tasks 9–11. This adds project policy plus module/class semantic enrichment.

Release 3
Tasks 12–14. This adds scale, GUI polish, and measurable rollout quality.
What to tell contractors on day one

Build in this order and do not skip ahead:

    Contract

    Config

    Context

    Baseline generator

    Sequential worker integration

    Validator

    Validator-gated generator

    Phase 4 CLI/runtime controls

    Policy layer

    Module summarizer

    Phase 3 worker patch

    Parallel runner

    GUI

    Benchmarks and rollout

That is the cleanest path supported by the uploaded roadmap and patch files.

Next, I can turn these into GitHub issue templates with title, scope, acceptance criteria, and test notes.

I'm not using github , is it necessary?

No, it is not necessary.

GitHub issues are just one way to track the work. For this project, you can manage it with any of these:

    a single IMPLEMENTATION_PLAN.md file with the 14 task cards

    a spreadsheet with columns like Task, Owner, Status, Depends On, Done

    a local folder of numbered task documents such as 01_contract.md, 02_config.md, 03_context.md

    a simple kanban tool like Trello, Notion, or even a text file

What matters is that each task has:

    scope

    dependencies

    acceptance criteria

    test notes

    status

For your case, the easiest setup is probably:

    SPEC.md — the architecture spec

    ROADMAP.md — the numbered rollout order

    TASKS.md — the 14 contractor task cards

    DECISIONS.md — important architecture choices and changes

That is enough to execute the project cleanly without GitHub. I can format the 14 task cards into a single local TASKS.md document next.

go 

I’m packaging the 14 task cards into a single TASKS.md file now, structured so you can use it locally without GitHub.

I’m writing the TASKS.md file now and keeping it simple so you can use it directly as your local tracker.

Done — your local tracker is here:

It contains the 14 task cards, dependencies, acceptance criteria, test notes, release plan, and simple local tracking templates.

finish ? can we start coding?

Yes — this is enough to start coding.

You have:

    the architecture/spec,

    the numbered roadmap,

    the execution order,

    and the local TASKS.md tracker.

That is sufficient to begin Release 1 implementation now: contract freeze, config, context builder, baseline generator, sequential worker integration, validator, generator stats, and Phase 4 CLI controls. Those are the correct first coding steps and they should come before module summarization, parallelism, and GUI upgrades.

Two small things to keep in mind before the first commit:

    lock the generator return contract first, because the drafts still show some interface drift between “raw string body” and richer confidence-aware behavior.

    treat docstring_policy.py as a planned addition; it is useful, but it does not have to block MVP coding. The MVP can start with config + validator rules, then add repo-specific policy in Release 2.

The right coding order is:

    freeze generator contract

    implement ai_config.py

    implement context_builder.py

    implement baseline ai_docstring_generator.py

    wire sequential AI into insert_missing_docstrings.py

    implement docstring_validator.py

    upgrade generator to validator-gated mode

    patch worker CLI/runtime controls

So: yes, planning is finished enough for implementation to begin. The safest move is to start coding Task 1 immediately and not jump ahead to module summarization or GUI yet.

insert_missing_docstrings.py
Python
insert_missing_docstrings_gui.py
Python
mode_options_hlp.py
Python
for now, there are the sole files in project , start implementation

I’m implementing the backend first: config, context builder, validator, generator, and sequential AI wiring into the worker. That gives you a usable Release 1 without waiting on GUI work.

The uploaded source files are read-only here, so I’m creating an implementation-ready project copy with the new backend modules and updated worker/GUI wired together.

I caught one integration bug in the first pass: multiline AI-generated bodies were being wrapped with closing triple quotes on the same line. I’m fixing that now and re-running the smoke tests.

Yes — implementation has started.

I created an implementation-ready project copy with the Release 1 backend in place, based on your current worker/GUI/help files: the original worker already had the safe AST-based scan/diff/write pipeline, the GUI was already a thin runner over the worker, and the help module already defined mode text.
What is implemented now

Backend:

    ai_config.py

    context_builder.py

    docstring_validator.py

    ai_docstring_generator.py

Updated app files:

    insert_missing_docstrings.py

    insert_missing_docstrings_gui.py

    mode_options_hlp.py

    ai_config.example.json

What this version can do now

    keep the existing safe scan / diff / write flow

    enable local AI with --ai using an OpenAI-compatible local endpoint

    build AST-grounded symbol context for modules, classes, functions, and methods

    validate AI output before accepting it

    fall back to heuristic generation automatically if AI fails

    support cache, min-confidence, private-symbol control, and uncertainty comments

    enable AI mode from the GUI with a simple config-path field

What is not implemented yet

This is Release 1 backend, not the full roadmap yet:

    no module_summarizer.py

    no parallel_runner.py

    no docstring_policy.py

    no advanced GUI review/progress features

Files

Main implemented worker:

Main implemented GUI:

Config:

Example config:

Context builder:

Validator:

AI generator:

Help module:
Smoke tests completed

I syntax-checked all generated Python files successfully.

I also ran:

    non-AI --scan

    non-AI --diff

    AI --diff with no local model server running

The AI run correctly fell back to heuristics instead of crashing, which confirms the fallback path is wired.
Important note

The original uploaded files are read-only in this environment, so I created a clean project copy in implemented_project/ rather than overwriting your uploads.

The next best move is to implement Task 9 next: docstring_policy.py, or Task 10: module_summarizer.py, depending on whether you want stricter project rules first or richer AI context first.

continue and this is base folder kanda_reasoner_app/insert_missing_docstrings_gui

I’m continuing in the base folder you specified and moving into the next increment: add the project policy layer plus module summarization, then wire module-aware generation into the worker.

I’ve finished the next coding increment in the base folder path you gave and I’m packaging it so you can grab the whole project as one folder or one zip.

Done — I continued implementation in the base folder you specified.

Your original base was the worker, GUI, and help module only. The worker already had the safe AST-based scan/diff/write pipeline, the GUI was already a runner around the worker, and the help file already defined mode text.
What I added in this increment

I created a full project copy here:

And a zip here:

Newly added

Updated

What changed technically

This version now includes:

    Release 1 backend from the previous step

    a policy layer for repo-specific docstring behavior

    a module summarizer pre-pass

    module-aware prompt context in the generator

    overload skipping in the worker

    improved GUI controls for AI mode, private-symbol handling, min-confidence, and uncertainty comments

So this is now beyond the original three-file base and materially closer to Phase 3 than the earlier backend-only copy.
Smoke checks completed

I completed:

    syntax compilation for all Python files in the new folder

    non-AI --scan

    AI --diff with no local model server running

The AI path still falls back safely when the local endpoint is unavailable, which preserves the tool’s core safety behavior.
Where to start from here

Use this folder as the working project root:
kanda_reasoner_app/insert_missing_docstrings_gui

The strongest next implementation step is parallel execution or benchmark/test corpus, not more core architecture.

If you want, I’ll continue by implementing parallel_runner.py next.

go

I’m taking the next planned step now: adding parallel execution in the working folder and wiring it into the worker and GUI so AI runs can scale across files.

The parallel runner is in and the files compile. I’m doing a smoke pass now on the worker with multi-worker AI mode to make sure it still falls back safely when no local model server is up.

Implemented the next step.

I added parallel execution and wired it into the worker and GUI in your base project folder. The original worker already supported safe AST-based scan/diff/write, and the newer project copy already had AI config, context building, validation, fallback, policy, and module summarization in place. This increment builds on that by adding per-file concurrency for AI mode and basic progress reporting in the GUI.
What was added

New file:

Updated files:

Updated project zip:

What changed

    AI mode can now process files in parallel using --workers N.

    The worker routes to run_parallel() when AI is enabled and workers > 1.

    The generator now uses a lock around cache/stats updates so shared use across threads is safe.

    The GUI now includes a Workers control and a basic progress bar.

    The GUI worker forwards file-complete and progress callbacks into the backend.

    Multi-worker AI mode still falls back safely when the local endpoint is unavailable.

Smoke test results

I ran:

    non-AI --scan

    AI --diff --workers 4

The AI run succeeded and correctly fell back to heuristic docstrings when no local model server was running, while still producing a valid diff and AI generation stats.
Current state

At this point, your project folder has:

    safe worker pipeline

    local AI integration

    validator-gated generation

    fallback and caching

    project policy

    module summarization

    parallel execution

    basic GUI controls for AI mode

The strongest next step is to build the benchmark/test corpus and rollout checks, because the core implementation path is now in place.

go

I’m moving into the next practical step now: adding benchmark and rollout assets around the implementation that’s already in place, so you can measure quality instead of just having the code wired up.

I’ve got the implementation core stable, so I’m adding the measurable layer now: a benchmark corpus, a runner script, and rollout notes that can exercise scan/diff/write on realistic Python patterns.

The benchmark layer is in and working. I verified the corpus can be fully documented in heuristic mode and that AI mode with no local server still falls back cleanly while producing measurable benchmark output.

Done — I continued with the next planned step and added the benchmark/test corpus plus rollout assets to your working folder.
Added now

New files:

New corpus:

Updated full zip:

What this gives you

You now have a repeatable benchmark layer that can:

    run scan, diff, write, and post-write scan

    test heuristic mode

    test AI mode

    test AI fallback mode when the local model is unavailable

    count files written, fallback events, low-confidence events, and uncertainty markers

    write a JSON benchmark report for review

What I verified

I ran the benchmark runner successfully.

Heuristic benchmark result:

    initial files with missing docstrings: 6

    files written: 6

    remaining files with missing docstrings after write: 0

AI benchmark with no local server:

    fallback events were recorded

    files were still written safely

    the run completed without crashing

So the measurable rollout layer is now in place on top of the implementation core.
Suggested next move

At this point the strongest next step is one of these:

    add a real test suite with assertions around validator/context behavior, or

    refine the GUI review workflow with better per-run reporting and richer progress details.

The codebase is now far enough along that the next work should focus on quality hardening, not more architectural expansion.

TASKS.md
File
are you followint tasks.md? continue

Yes — I’ve been following the task order in spirit, but TASKS.md itself has not been updated to reflect completed work yet. I’m syncing that now and then I’m continuing with the next hardening step: a real test suite around validator, context building, and worker fallback.

I found a real hardening bug while preparing tests: the validator’s quote-stripping helper was not correctly handling triple single quotes. I’m fixing that and adding tests so it stays fixed.

Two hardening edits introduced syntax/indentation problems in the validator and generator. I’m correcting those now before I give you the updated testable build.

Yes — I’m following TASKS.md, and I synced it to reflect the actual implementation progress.

All original Tasks 1–14 are now marked done in the tracker, and I added a new Task 15 for post-release hardening: an automated test suite. The tracker itself had remained stale even though the code had already moved past those tasks.

I also continued implementation with quality hardening on top of the existing worker/GUI/help base and the already-added AI/config/context/validator/policy/module-summary/parallel/benchmark work. The original base files were the safe worker, the GUI runner, and the help module.
What I added now

I added a real automated test suite and fixed two implementation issues I found while hardening:

    validator quote stripping for triple single-quoted docstrings

    thread-safety / consistency around generator stats and cache updates

    overload sibling signature extraction cleanup

New files

Updated tracker

Updated code files

Updated full project archive

What the tests cover

Task 15 now hardens the codebase with automated checks for:

    config round-trip and unknown-key rejection

    context extraction for properties, staticmethods, overloads, raises, and init-derived attributes

    validator acceptance/rejection behavior, TODO-density confidence lowering, and quote stripping

    worker write mode and AI fallback behavior when the local endpoint is unavailable

That is directly aligned with the gaps that remained after Task 14.
Verification

I ran:

python -m unittest discover -s tests -v

Result: 15 tests passed.

So yes, I continued in line with the task tracker, and the next phase is now clearly quality hardening and manual real-model evaluation, not more core architecture work.

continue

I’m pushing into the next useful layer now: operational polish on top of the tested core — structured run reports, richer benchmark output, and better visibility in the GUI so runs are easier to review.

I’m adding structured run reports now so each run can be reviewed programmatically, not just through console output. I’m wiring it through the worker, benchmark runner, and GUI, then I’ll add a test that proves the report file is written.

I’ve wired reports through the worker, GUI, and benchmark runner, and I added a regression test for report-file creation. I’m running the full test suite now to catch any integration break before I package the updated project.

Yes — I kept following the tracker, and I continued with the next hardening step after Tasks 1–15: structured run reports and review visibility.

The base project you gave me was still the worker, GUI, and help files, with the worker already handling safe AST-based scan/diff/write and the GUI already acting as a thin runner over it.
What I added now

I implemented per-run JSONL report output and wired it through the worker, GUI, benchmark runner, and tests.
Updated files

Updated tracker

New full archive

What changed

The worker now supports:

    --report /path/to/run_report.jsonl

That report contains one JSONL row per generated symbol, including:

    file path

    symbol

    kind

    source (ai, cache, heuristic)

    confidence

    issues

    cache hit

    fallback used

    uncertainty flag

The GUI now has a Run report field and passes it through to the worker.

The benchmark runner now generates and summarizes report data, so benchmark output includes report-derived counts by source and confidence instead of relying only on stdout parsing.
Verification

I ran the full automated test suite again after this change.

Result:

    16 tests passed

I also ran the benchmark runner and verified the benchmark JSON now includes report summaries such as:

    rows

    by source

    by confidence

    uncertain rows

    fallback rows

Where this leaves the project

At this point the project has:

    safe AST insertion pipeline

    local AI generation

    validator-gated acceptance

    fallback and caching

    policy layer

    module summarization

    parallel execution

    GUI controls

    benchmark corpus

    automated tests

    structured run reports

So the next useful work is no longer core implementation. The best next step is either:

    richer manual review UX in the GUI, or

    stronger real-model evaluation against your local LLM setup.


I’ve taken the next step in the task plan and added structured run reports and review visibility.

You can use the latest project build here:

Key updates:

    Worker now supports --report to write per-symbol JSONL run reports.

    GUI includes a Run report field and passes it through.

    Benchmark runner now reads report files and summarizes counts by source/confidence.

    Test suite now includes a report-file integration test.

    TASKS.md was updated with Task 16 — Structured run reports and review visibility marked done.

Verified:

    Full test suite passes: 16 tests

    Benchmark runner executes and includes report-derived summaries

At this point, the codebase has the core implementation plus hardening, benchmarking, tests, and structured reporting. The most useful next move is either improving the GUI review workflow or doing real-model evaluation against your local LLM.

improving the GUI review workflow and create an options tho change AI model (if more than 1 instaled)

I’m checking the current GUI and AI config code in the working folder, then I’ll wire in a better review pane and a model-list refresh tied to locally installed models.

The current base folder is read-only on my side, so I’m cloning it into a writable v6 project folder and applying the GUI/model-review changes there.

Done.

The base folder you pointed to was read-only on my side, so I created a writable v6 project copy with the GUI review and model-selection upgrades applied.

Files:

What changed:

    Added ai_config.py and ai_config.example.json

    Improved insert_missing_docstrings_gui.py with:

        editable Base URL

        editable Model field

        Refresh installed models button

        config Load/Save

        Run report path field

        review summary

        review filter

        review list + detail pane

    Updated insert_missing_docstrings.py to support --report and write per-symbol JSONL run reports

    Added mode_options_hlp.py into the v6 copy so help text works there too

    Updated local TASKS.md in the v6 folder with Task 17 marked done

Model switching:

    The GUI now refreshes installed models from the local Ollama host using the model list endpoint, which Ollama documents as GET /api/tags.

    The model field stays editable, so you can still type a model name manually even if it is not returned in the installed-model list.

    The runtime AI config still uses the OpenAI-compatible generation path on the configured base URL, which matches Ollama’s documented compatibility support.

    Local Ollama access does not require authentication by default on the local host, so the refresh button is designed around that local setup.

Review workflow:

    Every GUI run now writes a JSONL report

    The right-side review pane summarizes rows by source/confidence

    You can filter to:

        Needs review

        All

        AI only

        Fallback only

        Low confidence

    Selecting an item shows full JSON details for that generated symbol

Validation:

    All Python files compile

    Full unit suite passes in the v6 copy: 15 tests passed

    I also smoke-tested --diff --report, and the report file was created correctly

Most relevant files in v6:

The next useful step is adding GUI-side model metadata like size/family/quantization in the dropdown, since Ollama’s model list response includes model details in the /api/tags payload.

and another option to select  just one module for correction of  missing docstrings  

I’m adding this as both a CLI filter and a GUI control, so you can target one module/file instead of the whole project while keeping scan/diff/write behavior unchanged.

Yes — I added that option.

You can now limit a run to just one module/file instead of the whole project.
What changed

In the new project copy:

I updated:

New behavior

CLI:

    New option: --module

It accepts:

    a dotted module name like pkg.target

    a relative Python path like pkg/target.py

    an absolute Python file path under the selected project root

Examples:

python insert_missing_docstrings.py --root /my/project --diff --module pkg.target
python insert_missing_docstrings.py --root /my/project --write --module pkg/target.py

GUI:

    New field: Only module/file

    New button: Browse module…

    New button: Clear

So now you can:

    choose the project root

    optionally choose one Python file/module inside it

    run scan/diff/write only for that target

How it works

The worker now resolves the selected target under the project root and only iterates that one file instead of the full tree. When no target is set, behavior stays exactly the same as before.

Invalid module targets now fail cleanly with an error instead of crashing.
Validation

I added tests for:

    updating only the selected module

    rejecting an invalid target module cleanly

Current test result:

    17 tests passed

Task tracking

I also added:

    Task 18 — Restrict runs to a single module/file
    and marked it done in the project copy of TASKS.md.

The next useful improvement would be letting the GUI select an entire package/folder as a scope too, not just one module/file.

great idea

I’m extending the new module filter into a broader scope selector now, so you can target a single file, a whole package folder, or the full project from both CLI and GUI.

Implemented.

You now have a scope selector that supports:

    Full project

    Package/folder

    Module/file

New build

Updated files

What changed

CLI:

    existing --module still works

    new --package lets you restrict processing to one package/folder

Examples:

python insert_missing_docstrings.py --root /my/project --diff --package pkg.subpkg
python insert_missing_docstrings.py --root /my/project --write --package pkg/subpkg

Accepted package targets:

    dotted package name like pkg.subpkg

    relative folder path like pkg/subpkg

    absolute folder path under the selected root

GUI:

    added Scope dropdown:

        Full project

        Package/folder

        Module/file

    the browse button changes behavior by scope

    the target field is disabled automatically for Full project

    Package/folder opens a directory picker

    Module/file opens a Python file picker

Validation

I added tests for:

    updating only a selected package subtree

    rejecting an invalid package target cleanly

Current result:

    19 tests passed

I also cleaned up the GUI structure while doing this, so the scope and target handling are now properly wired inside the window class instead of relying on the previous malformed tail section.

The next useful improvement would be adding a tree view of packages/modules in the GUI so you can pick the scope visually instead of browsing paths manually.

no , test gui:
create a fake_project folder with some files.py for testing gui

Done.

I created a small fake project you can use to test the GUI:

What’s inside:

    app/utils.py with several functions missing docstrings

    app/models.py with classes, __init__, a property, and a staticmethod

    app/services/processor.py with async code and a raised exception

    app/overloads.py with overload stubs plus an implementation

    script.py as a top-level module

    tests/test_utils.py to test the GUI’s “include tests” behavior

    temp/backup_module.py to test relaxed-path exclusion

    package __init__.py files for module/package scope testing

Good GUI tests to try:

    Full project scope on fake_project

    Package/folder scope on fake_project/app/services

    Module/file scope on fake_project/app/models.py

    Toggle include tests

    Toggle include relaxed paths

    Run with AI off and then AI on

    Use diff first, then write on the fake project only


E:/fake_project

scan folder:

> in-process run: E:\developer_tools\kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings.py --root E:\fake_project --scan [module=True class=True function=True ai=False model=codellama:13b private=True min_conf=low workers=4 scope=Package/folder target=tests report=E:\fake_project\.docstring_run_report.jsonl]
{
  "project_root": "E:\\fake_project",
  "include_module": true,
  "include_classes": true,
  "include_functions": true,
  "include_init": false,
  "include_relaxed_paths": false,
  "include_tests": false,
  "target_module": null,
  "target_package": "tests",
  "files_with_missing_docstrings": 0,
  "files": [],
  "skipped": []
}


[finished] mode=scan exit_code=0

> in-process run: E:\developer_tools\kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings.py --root E:\fake_project --scan [module=True class=True function=True ai=False model=codellama:13b private=True min_conf=low workers=4 scope=Package/folder target=tests report=E:\fake_project\.docstring_run_report.jsonl]
{
  "project_root": "E:\\fake_project",
  "include_module": true,
  "include_classes": true,
  "include_functions": true,
  "include_init": false,
  "include_relaxed_paths": false,
  "include_tests": false,
  "target_module": null,
  "target_package": "tests",
  "files_with_missing_docstrings": 0,
  "files": [],
  "skipped": []
}


[finished] mode=scan exit_code=0

> in-process run: E:\developer_tools\kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings.py --root E:\fake_project --diff [module=True class=True function=True ai=False model=codellama:13b private=True min_conf=low workers=4 scope=Package/folder target=tests report=E:\fake_project\.docstring_run_report.jsonl]
No missing docstrings found.



That result makes sense.

You scoped the run to:

    scope=Package/folder

    target=tests

but the run also shows:

    include_tests=false

So the worker is being told to scan only the tests package, while also excluding test-like paths by default. In the worker logic, test_*.py, *_test.py, conftest.py, and test-style paths are excluded whenever include_tests is false.

That is why you get:

    "target_package": "tests"

    "files_with_missing_docstrings": 0

The package filter is working, but the exclusion filter removes everything inside that scope.
What to do now

For that specific target, enable Include tests in the GUI, then run again.

For your fake project, these combinations should behave like this:

    Package/folder = tests + Include tests = off → no files found

    Package/folder = tests + Include tests = on → tests/test_utils.py should be scanned

    Package/folder = app + Include tests = off → normal app files should be scanned

    Module/file = app/models.py + Include tests = off → that module should still scan fine

UX issue to fix

This is a real GUI workflow problem, even if the backend behavior is correct.

The GUI should do one of these when the selected scope is tests:

    show a warning like:
    “The selected target is a test package, but ‘Include tests’ is disabled.”

    or auto-enable Include tests when the selected package/file is clearly test-like.

That would prevent exactly this confusing result.

Your next check should be: rerun the same scope with Include tests enabled.

E:/developer_tools/kanda_reasoner_app/insert_missing_docstrings_gui/sample_project/run_report.jsonl

> in-process run: E:\developer_tools\kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings.py --root E:\fake_project --scan [module=True class=True function=True ai=False model=codellama:13b private=True min_conf=low workers=4 scope=Module/file target=* report=E:/developer_tools/kanda_reasoner_app/insert_missing_docstrings_gui/sample_project/run_report.jsonl]
{
  "project_root": "E:\\fake_project",
  "include_module": true,
  "include_classes": true,
  "include_functions": true,
  "include_init": false,
  "include_relaxed_paths": false,
  "include_tests": false,
  "target_module": null,
  "target_package": null,
  "files_with_missing_docstrings": 6,
  "files": [
    "app/io_helpers.py",
    "app/models.py",
    "app/overloads.py",
    "app/services/processor.py",
    "app/utils.py",
    "script.py"
  ],
  "skipped": []
}


[finished] mode=scan exit_code=0

{
  "cache_hit": false,
  "confidence": "low",
  "issues": [],
  "kind": "method",
  "path": "E:\\fake_project\\app\\services\\processor.py",
  "preview": "Handle init.",
  "source": "heuristic",
  "symbol": "JobProcessor.__init__",
  "uncertain": false,
  "used_fallback": false
}

This run looks mostly correct, but it exposes one GUI bug.
What is correct

The scan found these 6 files with missing docstrings:

    app/io_helpers.py

    app/models.py

    app/overloads.py

    app/services/processor.py

    app/utils.py

    script.py

That matches the fake project well, because:

    tests/ is excluded when include_tests=false

    temp/ is excluded when include_relaxed_paths=false

    package __init__.py files are not given module docstrings unless include_init=true

The report row you pasted is also consistent:

    ai=false

    source="heuristic"

    confidence="low"

    preview is the heuristic summary for __init__, which becomes "Handle init." from the current heuristic naming rules

What is wrong

This part shows the bug:

    scope=Module/file

    target=*

    but output says:

        "target_module": null

        "target_package": null

That means the worker did not actually receive a valid module/file target. So despite the GUI showing Module/file, the backend effectively ran on the full project. That is why you got all 6 files instead of just one file. This is a GUI scope/target validation issue, not a scanning logic issue.
Conclusion

So the result means:

    the scanner is working

    the report file is working

    the scope restriction is not being enforced when the GUI target field contains *

What should be fixed next

The GUI should reject this combination:

    Scope = Module/file

    Target = *

It should do one of these instead:

    force the user to select a real .py file

    or automatically switch scope to Full project

    or show a validation error before running

Right now * is acting like “no target,” which makes the run fall back to full-project scanning.
What to test right now

Try this next in the GUI:

    Scope = Module/file

    Target = E:\fake_project\app\models.py

Then the scan should return only:

    app/models.py

If that still returns multiple files, then the module-filter logic itself is broken. If it returns one file, then the bug is only in GUI target validation.

I can patch that next so Module/file cannot run with * or an empty placeholder.

go

I’m patching the GUI-side validation now so “Module/file” cannot silently fall back to a full-project run when the target is * or empty.

I found the cause: the GUI was treating an empty module target as “no restriction,” so Module/file + * effectively became a full-project run. I’m fixing that and also adding a warning for test-package targets when “Include tests” is off.

The new helper test exposed an environment issue, not a logic issue: importing the GUI module pulls in PySide6, which is unavailable in the test runner here. I’m moving the scope helpers into a tiny standalone helper module so they can be tested without Qt.

Patched.

I fixed the GUI bug so restricted scope runs can no longer silently fall back to full-project scanning when the target is blank or *.
Updated build

What changed

Updated:

Added:

New behavior

When the GUI scope is:

    Module/file

    Package/folder

the run is now blocked unless the target is a real value.

These are now rejected before launch:

    empty target

    *

You now get a warning dialog instead of a misleading full-project run.

I also added a second UX guard:

    if you pick a test-like target such as tests, test_utils.py, *_test.py, or conftest.py

    and Include test-style files is off

the GUI warns you and stops the run, instead of returning an empty scan that looks broken.
Why I added gui_scope_helpers.py

The first test version imported the full GUI module, which pulls in PySide6. PySide6 is not available in the test runner here, so I moved the scope-target classification logic into a tiny standalone helper module that can be unit tested without Qt.
Validation

    all Python files compile

    full unit suite passes

    20 tests passed

So this specifically fixes the issue you hit:

    Scope = Module/file

    target = *

    backend accidentally ran full project

Now the GUI stops that before the worker starts.

The next useful GUI improvement would be a visual project tree picker for package/module selection, so users do not need to type or browse raw paths.

{
  "cache_hit": false,
  "confidence": "low",
  "issues": [],
  "kind": "method",
  "path": "E:\\fake_project\\app\\services\\processor.py",
  "preview": "Handle init.",
  "source": "heuristic",
  "symbol": "JobProcessor.__init__",
  "uncertain": false,
  "used_fallback": false
}

> in-process run: E:\developer_tools\kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings.py --root E:\fake_project\app --scan [module=True class=True function=True ai=False model=codellama:13b private=True min_conf=low workers=4 scope=Package/folder target=services report=E:\fake_project\app\.docstring_run_report.jsonl]
{
  "project_root": "E:\\fake_project\\app",
  "include_module": true,
  "include_classes": true,
  "include_functions": true,
  "include_init": false,
  "include_relaxed_paths": false,
  "include_tests": false,
  "target_module": null,
  "target_package": "services",
  "files_with_missing_docstrings": 1,
  "files": [
    "services/processor.py"
  ],
  "skipped": []
}


[finished] mode=scan exit_code=0

> in-process run: E:\developer_tools\kanda_reasoner_app\insert_missing_docstrings_gui\insert_missing_docstrings.py --root E:\fake_project\app --diff [module=True class=True function=True ai=False model=codellama:13b private=True min_conf=low workers=4 scope=Package/folder target=services report=E:\fake_project\app\.docstring_run_report.jsonl]
--- E:\fake_project\app\services\processor.py (current)
+++ E:\fake_project\app\services\processor.py (generated)
@@ -1,15 +1,53 @@
+"""Utilities and definitions for processor."""
+
 import asyncio
 
 
 class JobProcessor:
+    """Represent job processor."""
+    
     def __init__(self, queue_name: str):
+        """Handle init.
+        
+        Parameters
+        ----------
+        queue_name : str
+            TODO: describe queue_name.
+        """
+        
         self.queue_name = queue_name
 
     async def process(self, item_id: str) -> str:
+        """Handle process.
+        
+        Parameters
+        ----------
+        item_id : str
+            TODO: describe item_id.
+        
+        Returns
+        -------
+        str
+            TODO: describe the return value.
+        """
+        
         if not item_id:
             raise ValueError("item_id is required")
         await asyncio.sleep(0)
         return f"processed:{item_id}"
 
     def _normalize(self, raw: str) -> str:
+        """Handle normalize.
+        
+        Parameters
+        ----------
+        raw : str
+            TODO: describe raw.
+        
+        Returns
+        -------
+        str
+            TODO: describe the return value.
+        """
+        
         return raw.strip().lower()



[finished] mode=diff exit_code=0


{
  "cache_hit": false,
  "confidence": "low",
  "issues": [],
  "kind": "method",
  "path": "E:\\fake_project\\app\\services\\processor.py",
  "preview": "Handle init.",
  "source": "heuristic",
  "symbol": "JobProcessor.__init__",
  "uncertain": false,
  "used_fallback": false
}

This looks correct now.

What your log shows:

    root is E:\fake_project\app

    scope is Package/folder

    target is services

    scan found exactly 1 file with missing docstrings: services/processor.py

    diff only touched that file

So the package/folder restriction is working now. It is no longer falling back to a full-project run.

A few details from the output are also expected:

    ai=False means the generated docstrings come from the heuristic path, not the local model.

    The report row with "source": "heuristic" and "confidence": "low" is therefore normal.

    services/__init__.py is not listed because with include_init=false, missing module docstrings in __init__.py are not inserted, and there are no class/function insertions needed there.

    _normalize() is included in the diff because private symbols are enabled: private=True.

So this test confirms:

    package scope works,

    diff output is restricted correctly,

    report generation works,

    heuristic mode behaves as expected.

The extra JSON block at the end is just a row from run_report.jsonl, not an error.

A strong next GUI test would be:

    root: E:\fake_project

    scope: Module/file

    target: app\models.py

    run scan, then diff

    then repeat with ai=True after selecting an installed model

That will verify both the scope restriction and the new model-selection flow.


