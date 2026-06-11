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


The next strongest artifact to create is a numbered implementation checklist by file, with exact coding order, dependencies, and definition of done for each task.

go

I’m turning the spec into contractor-ready work units now: file by file, dependency ordered, with definition of done and what to test after each step.

Thought for 20s

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


