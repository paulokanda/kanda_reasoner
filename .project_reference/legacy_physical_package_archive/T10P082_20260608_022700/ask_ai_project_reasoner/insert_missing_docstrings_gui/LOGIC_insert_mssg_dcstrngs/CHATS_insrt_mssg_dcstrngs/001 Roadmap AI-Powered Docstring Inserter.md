Roadmap: AI-Powered Docstring Inserter
Let me first read the core worker file to understand the current architecture before planning improvements.Viewed 2 filesViewed 2 filesGood, I have the full picture now. Here's the roadmap.

🗺️ Roadmap: AI-Powered Intelligent Docstring Inserter
Current State Analysis
The existing tool is solid structurally — AST parsing, BOM-safe I/O, syntax validation, scan/diff/write pipeline — but docstring generation is purely heuristic: function_summary() is a prefix-matching string template factory. The goal is to replace that with a local AI that reads and understands the actual code before writing.

Phase 1 — Local AI Integration Layer (Core Change)
What changes: Replace build_function_docstring, build_class_docstring, build_module_docstring with an AI-backed generator. Everything else (AST detection, insertion, BOM handling, scan/diff/write pipeline) stays intact.
1.1 — AI Context Builder (context_builder.py)
Before calling the AI, you need to give it real context, not just the function signature. Build a SymbolContext dataclass that packages:

The raw source lines of the target symbol (function/class/module)
Its enclosing class name if it's a method
The module-level imports (so AI knows what types come from)
__all__ if present
Any adjacent docstrings from sibling methods for stylistic consistency
The full function signature already unparsed via ast.unparse

This context is assembled once per symbol using information already extracted by collect_missing_docstring_insertions. No second parse needed.
1.2 — AI Docstring Generator (ai_docstring_generator.py)
Create a generator class with a clean interface:
pythonclass AIDocstringGenerator:
    def generate(self, symbol_context: SymbolContext) -> str: ...
Responsibilities:

Build a precise prompt from SymbolContext
Call the local LLM (Ollama via httpx or openai-compatible endpoint)
Parse and validate the response (strip triple-quotes if the model echoes them, check indentation)
Fall back to the existing heuristic if the AI call fails or times out

1.3 — Prompt Engineering
The prompt must instruct the AI to be a code reader, not a guesser. Key rules to embed in the system prompt:

"You are given the exact source of a Python symbol. Read it. Do not invent parameters or behavior."
"Only document what the code provably does."
"If a parameter's role is unclear from the source, write TODO: describe <name> — do not guess."
"Output only the raw docstring content between triple quotes. No prose, no explanation."
Format: NumPy-style (matching what the tool already uses)
Private methods (_name, __name__) get docstrings too — no special-casing

1.4 — Model Configuration (ai_config.py)
python@dataclass
class AIConfig:
    base_url: str = "http://localhost:11434/v1"  # Ollama default
    model: str = "codellama:13b"  # or deepseek-coder, qwen2.5-coder, etc.
    timeout_seconds: float = 30.0
    max_tokens: int = 512
    fallback_to_heuristic: bool = True
    temperature: float = 0.1   # low — docstrings need precision, not creativity
Expose this as a CLI flag --ai-config path/to/config.json and as a GUI panel.

Phase 2 — Performance: Parallel Processing
Currently collect_changes walks files sequentially. With AI calls (even local ones), that becomes a bottleneck fast.
2.1 — Per-file Parallelism
Wrap collect_missing_docstring_insertions + AI calls in a ThreadPoolExecutor (I/O-bound: LLM HTTP calls release the GIL fine). Add a --workers N CLI flag (default: 4).
pythonwith ThreadPoolExecutor(max_workers=config.workers) as pool:
    futures = {pool.submit(process_file, path, ...): path for path in python_files}
2.2 — Per-symbol Batching (Optional, Phase 2B)
For models that support it (OpenAI-compatible batch endpoints), collect all missing symbols from a file into a single prompt with numbered slots. This cuts HTTP round-trips from N (one per symbol) to 1 (one per file). Implement only after the sequential version is validated.
2.3 — Result Caching
Add a .docstring_cache.json at project root. Key: sha256(source_lines_of_symbol). If the symbol's source hasn't changed since the last run, reuse the cached docstring. This makes re-runs on large projects nearly instant.

Phase 3 — Deeper Code Understanding
3.1 — Module-level Summarization
Before processing individual symbols in a module, make one AI call per module that reads the full file and returns a 2-3 sentence module summary. Use this as the module docstring and as a preamble injected into every subsequent per-symbol prompt in that module ("This function lives in a module that does X"). This dramatically improves coherence.
3.2 — Class-level Context Propagation
When generating docstrings for methods inside a class, include the class docstring (already written or just generated) in the prompt. Methods then document themselves in the context of their class's stated purpose.
3.3 — __init__ Parameter Inference
__init__ is special: its parameters define the class's public state. Generate the class docstring after __init__'s docstring is created, pulling the Attributes section from __init__'s parameter list. This is a two-pass operation per class.
3.4 — Decorator and Type Annotation Awareness
Extract @property, @staticmethod, @classmethod, @abstractmethod, @overload decorators from the AST and inject them into the prompt. A @property getter should not have a Parameters section. A @staticmethod should not mention self. The AI needs to know this upfront.

Phase 4 — Quality and Safety
4.1 — Post-generation Validator
After the AI returns a docstring, run these checks before accepting it:

No invented parameter names (cross-check against iter_function_parameters)
No invented return type (cross-check against node.returns)
Syntactically valid when inserted (already done by parse_source in collect_changes, keep it)
Does not exceed a configurable max line length (default 88, matching Black)
Does not contain the literal text of the source code (hallucination guard)

On failure → fall back to heuristic.
4.2 — Confidence Scoring (Optional)
Ask the model to output a confidence: high|medium|low tag alongside the docstring. Low-confidence docstrings get a # AI-UNCERTAIN comment appended. This lets developers prioritize review.
4.3 — Dry-run Diff for AI Output
The existing diff mode already shows what will be inserted. Make sure it works identically for AI-generated docstrings. No changes needed structurally — the AI generator is a drop-in replacement for the builder functions.

Phase 5 — GUI Updates (insert_missing_docstrings_gui.py)
5.1 — AI Settings Panel
Add a collapsible "AI Settings" section to the form:

Model selector (combo box, populated by querying GET /api/tags from Ollama)
Base URL field
Timeout spinner
"Test connection" button that pings the model and shows latency
Fallback checkbox

5.2 — Per-file Progress
DocstringRunWorker currently emits output_ready as a single blob. Refactor to emit progress per-file (filename + count of symbols processed). Show a QProgressBar in the status bar.
5.3 — Symbol Preview Panel
Add a second QPlainTextEdit (splitter layout) that shows the AI-generated docstring for the currently selected file/symbol before write. Lets users approve or skip individual docstrings.

Phase 6 — New CLI Flags
FlagPurpose--aiEnable AI mode (off by default, heuristic is default)--ai-model MODELOverride model name--ai-url URLOverride base URL--workers NParallel file workers--cache / --no-cacheEnable/disable result cache--privateExplicitly include _ and __ prefixed symbols (already included in AST walk, but make it explicit)

Recommended Implementation Order
Phase 1.1 → 1.2 → 1.3 → 1.4   (get AI working sequentially, validate quality)
Phase 4.1                        (validate output before touching Phase 2)
Phase 2.1                        (parallelize once correctness is confirmed)
Phase 3.1 → 3.2 → 3.3 → 3.4   (layer in deeper context incrementally)
Phase 5.1 → 5.2 → 5.3           (GUI last, after backend is stable)
Phase 2.2 + 4.2 + 6             (optional enhancements)

That covers Phases 1–6 of the full roadmap. The most impactful change by far is Phase 1 (AI generator as a drop-in for the three build_* functions) — everything else builds on that foundation.
Want me to continue into implementation details for Phase 1 — concrete code for SymbolContext, the prompt template, and the generator class?

Let me read the frontend design skill first, then build the implementation.Reading frontend design skillReading frontend design skillNow let me build the Phase 1 implementation — concrete code for SymbolContext, the prompt template, and the AI generator class.Now I have everything I need. Here is the Phase 1 implementation — full concrete code.

Phase 1 Implementation: AI-Powered Docstring Generator
Three new files to create alongside your existing ones.
File 1 — context_builder.pySymbolContext dataclass and context builder for AI docstring generationSymbolContext dataclass and context builder for AI docstring generationFile 2 — ai_config.pyAI configuration dataclass with JSON load/save supportAI configuration dataclass with JSON load/save supportFile 3 — ai_docstring_generator.pyAI docstring generator: prompt builder, LLM caller, validator, heuristic fallbackAI docstring generator: prompt builder, LLM caller, validator, heuristic fallbackNow let's show the integration patch — the exact diff to apply to insert_missing_docstrings.py to wire these in.Created a file, read a fileCreated a file, read a fileHere's a summary of what was delivered and how the pieces connect.

What was built
context_builder.py — the intelligence layer. SymbolContext is a rich dataclass capturing everything the AI needs: actual source lines, the full signature, decorators (@property, @abstractmethod, etc.), enclosing class name, sibling docstrings for style mirroring, and module-level imports for type resolution. The three build_*_context() functions populate it from the existing AST nodes your tool already parses — zero extra parsing passes.
ai_config.py — clean config with from_json() / to_json() and a validate() method. Drop an ai_config.json next to your scripts to tune model, timeout, temperature, worker count, and cache behavior without touching code.
ai_docstring_generator.py — the generator itself. The key design decisions:

The system prompt explicitly forbids the model from inventing parameters or behavior not visible in the source, and tells it to write TODO: describe <n> when uncertain — so AI failures are honest rather than confident lies.
The validator cross-checks every parameter name the model emits against the AST ground truth. If the model hallucinates a parameter name, the docstring is rejected and the heuristic fallback fires instead.
The cache is keyed by a SHA-256 hash of the source lines + signature, so unchanged symbols are never re-sent on subsequent runs.
Uses only urllib.request from stdlib — no requests, no httpx dependency.

INTEGRATION_GUIDE.py — step-by-step patch instructions for wiring all three files into your existing insert_missing_docstrings.py. The change is purely additive: generator=None preserves current behavior when --ai is not passed.
Ready to continue to Phase 2 (parallel ThreadPoolExecutor processing + per-file progress signals)?

Good. Now I have everything I need to write Phase 2 precisely.

Phase 2: Parallel Processing + Progress Signals
Three deliverables this iteration:

parallel_runner.py — the ThreadPoolExecutor engine with per-file progress callbacks
insert_missing_docstrings.py replacement — the full patched worker (all phases wired in cleanly)
insert_missing_docstrings_gui.py patch — progress bar + AI settings panel

File 1 — parallel_runner.pyParallel file processor with progress callbacks and thread-safe result collectionParallel file processor with progress callbacks and thread-safe result collectionFile 2 — Fully patched insert_missing_docstrings.pyViewed a file, created a fileViewed a file, created a fileFile 3 — Patched insert_missing_docstrings_gui.pyCreated a file, read a fileCreated a file, read a fileHere's a precise summary of every decision made in Phase 2.

What was built
parallel_runner.py — the executor engine. run_parallel() is a direct drop-in for the sequential for path in eligible loop. Each file gets its own FileProgress object owned exclusively by its thread — no shared mutable state except two single-element lists (mutable int counters) protected by a single threading.Lock. The function uses as_completed() so results stream in as they finish rather than waiting for the slowest file. It accepts two callbacks: on_file_progress (per-symbol, hot path) and on_file_complete (per-file, used by the GUI). The parallel path only activates when workers > 1 AND generator is not None — pure heuristic mode always runs sequentially since it's CPU-fast with no I/O wait.
insert_missing_docstrings.py (full replacement, not a patch) — the key architectural decision here was making the AI stack an optional import. The try/except ImportError block at the top means the worker runs identically to the original when the four new files aren't present. The collect_missing_docstring_insertions function grew two new optional parameters: generator (the AI instance) and on_symbol_done (the progress callback). The collect_changes function now routes to either run_parallel() or the original sequential loop based on workers > 1. The new --ai flag accepts an optional config path, defaulting to "default" which uses AIConfig.default().
insert_missing_docstrings_gui.py (full replacement) — three concrete GUI additions: the AISettingsPanel is a QCheckBox-gated QGroupBox (collapsed by default, zero visual noise when AI is off). The QProgressBar lives in the permanent section of QStatusBar and switches between indeterminate (spinner) until the first progress_tick signal arrives, then drives setValue / setMaximum normally. The file_complete signal carries a _ProgressPayload — a plain __slots__ object, not the FileProgress dataclass directly, because Qt signal crossing requires picklable types and avoids importing parallel_runner in the GUI process.
Deployment checklist — all six files in the same directory:
insert_missing_docstrings.py      ← replaced
insert_missing_docstrings_gui.py  ← replaced
ai_config.py                      ← Phase 1
context_builder.py                ← Phase 1
ai_docstring_generator.py         ← Phase 1
parallel_runner.py                ← Phase 2 (new)
Ready to continue to Phase 3 (module-level summarization, class-context propagation, __init__ attribute inference, and decorator-aware prompt routing)?