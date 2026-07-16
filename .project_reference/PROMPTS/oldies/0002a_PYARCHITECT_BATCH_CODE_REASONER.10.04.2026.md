Project Reasoner V10 Prompt System 

MASTER_SYSTEM_PROMPT = """\
You are Project Reasoner V10, a strict evidence-grounded Python architecture analyst.

Grounding and honesty rules (never violate):
- Use ONLY the evidence pack provided in the user message: FILE EVIDENCE [F##], SYMBOL EVIDENCE [S##], and SOURCE SNIPPETS [SN##].
- Never invent or assume any file path, module, class, function, method, symbol, variable, line number, execution step, test, or evidence id.
- Do not infer missing code. If a relationship is not explicitly shown (e.g., a call edge), say it is not shown.
- If the evidence does not support an answer: output exactly:
  INSUFFICIENT_EVIDENCE
  Then 1-3 short lines stating what specific evidence is missing (e.g., a caller snippet, a signal map entry, a symbol definition snippet).

Citation contract (required):
- Every non-trivial technical claim MUST end with one or more evidence ids in square brackets.
  Examples: "The entry point is shell/kanda_main.py. [F01]" or "The call site appears in the snippet. [SN03]"
- Use [SN##] for any claim about concrete code behavior, control flow, or exact calls.
- Use [S##] for symbol ownership/location/kind claims.
- Use [F##] for file-level structure, packaging/docs intent, and section-level claims.
- Do not cite ids that are not present in the evidence pack.

Code quoting rules (required):
- Only include code blocks if the exact lines appear in SOURCE SNIPPETS.
- Copy code VERBATIM from SOURCE SNIPPETS only. Do not reconstruct or paraphrase code.
- When you show code, keep excerpts short and immediately explain what the excerpt proves, with citations.

Answer style (optimize for correctness and efficiency):
- Be concise. Prefer the smallest answer that fully resolves the question.
- Do not restate the full evidence pack.
- Calibrate certainty: use "the evidence shows" / "not shown in the provided evidence" when appropriate.
- If the user requests a one-line locator format, output exactly one line and nothing else.
"""

Executive summary

Project Reasoner V10 already implements a strong “strict grounding” posture via (a) a prompt-built evidence pack containing FILE EVIDENCE, SYMBOL EVIDENCE, and SOURCE SNIPPETS, (b) a system message repeating anti-hallucination rules, and (c) a post-generation validator that can emit INSUFFICIENT_EVIDENCE when the model violates grounding constraints. Local evidence: v10_prompt_builder.py (SYSTEM CONSTRAINTS; evidence pack sections), v10_ai_bridge.py (system message + validator/sanitizer), v10_main_window.py (route selection and prompt assembly), v10_qwen_ai_models.py (streaming chat completions), v10_help_index.py (validated tiers). External API contracts rely on Ollama’s OpenAI-compatibility layer and OpenAI-style Chat Completions streaming semantics.

The main prompt-system gaps are (1) duplicated and sometimes ambiguous guardrails (including literal “...” inside instructions), (2) missing a strict required citation policy (the current prompts forbid fake ids but do not force citations per claim), (3) uncontrolled prompt growth (memory + evidence + snippets) that increases token cost and latency, and (4) an OpenAI-compatibility risk in the request payload: v10_qwen_ai_models.py sends options: {"temperature": ...} to /v1/chat/completions, while OpenAI’s Chat Completions spec defines temperature as a top-level request parameter.

The upgrade recommended here refactors prompts into a stable master system prompt + small intent add-ons, enforces a citation-per-claim contract, introduces token-budgeted evidence selection, and preserves parseable section markers needed by the current deterministic/validator logic.
Current prompt system audit
PromptBuilder evidence-pack construction

PromptBuilder.build(...) constructs a single user message string containing:

    A “SYSTEM CONSTRAINTS” block (still inside the user prompt) with strict grounding rules.
    The question duplicated as “PRIMARY TASK” and “USER QUESTION”.
    Optional “CALL-SITE EVIDENCE” for “which method calls” questions, prioritizing snippets that contain the literal invocation.
    “PROJECT SUMMARY” including project_root, indexed counts, and entry files.
    “EVIDENCE INTERPRETATION RULES” distinguishing packaging_metadata vs documentation_intent vs code/snippets.
    “CONVERSATION MEMORY” (last up to 3 turns; answers truncated).
    “FILE EVIDENCE” blocks printed as:
        Header line: [F##] score=<int>
        Then item.detail (which for normal files includes Path: ..., module name, role hints, runtime anchors, etc.).
    “SYMBOL EVIDENCE” blocks printed similarly as [S##] score=<int> + detail.
    “SOURCE SNIPPETS” printed with a strict regex-friendly header:
        [SN##] <path>:<line> anchor=<anchor>
        Then raw snippet text.
    “STRICT GROUNDING RULE” at the end that threatens INSUFFICIENT_EVIDENCE if the model mentions anything not present above.

Local evidence: v10_prompt_builder.py (PROJECT_SCOPE_GUARDRAIL; section labels; memory; snippet header format).
AI bridge system message and validator loop

LocalAIReasoner.ask(prompt, model_name) creates chat messages:

    role="system": a long anti-hallucination string, plus formatting constraints.
    Optional second role="system" “focus message” that is built by _build_generative_focus_message(...) to narrow attention to top snippets.
    role="user": the full PromptBuilder prompt string.

It calls a streaming Chat Completions endpoint and receives SSE-like chunks, extracting tokens via choices[0].delta.content. This matches OpenAI Chat Completions streaming chunk semantics.

After generation, _handle_done(...) performs repairs/sanitization for one-line answers and validates grounding (forbidden paths/symbols/ids and “ignored required snippets”), emitting INSUFFICIENT_EVIDENCE when needed. Local evidence: v10_ai_bridge.py.
Routing and “validated tiers”

Routing is driven by route_query_intent(question) returning a QueryRouteDecision(route, intent_name, reason) with routes: deterministic, ranked, or generative. Local evidence: v10_query_router.py, v10_main_window.py.

The help index contains “Validated Question Examples” across tiers:

    Tier 1: deterministic locators (fast exact answers).
    Tier 2: signal/action questions using qt_signal_map.
    Tier 3: flow/chain questions.
    Tier 4: responsibility/explanation questions.

Local evidence: v10_help_index.py.
Weaknesses and risk analysis
Hallucination and grounding risks

A citation-per-claim requirement is not enforced. The system prompt forbids inventing ids, but it does not force the model to cite evidence ids on each claim; this is a common failure mode where a model writes plausible prose without anchoring. Strengthening the citation contract reduces hallucination surface by forcing the model to “pay” evidence ids for every claim.

Several instructions include literal “...” inside sentences (not just UI truncation). This reduces clarity and can be misinterpreted as permission to omit details. Replace all “...” inside instruction text with explicit, complete sentences.

The user prompt redundantly contains “SYSTEM CONSTRAINTS” even though the system message already provides system-level constraints. Duplicated constraints inflate tokens and can create instruction conflicts if they drift.
Verbosity, token cost, and latency

The prompt includes: duplicated question lines, project summary, interpretation rules, memory turns, plus potentially large evidence lists and multi-snippet blobs. This increases input tokens and latency and may exceed context on smaller local models (context window is unspecified).

Conversation memory currently injects prior answers (up to ~900 chars each). This is expensive and often irrelevant, and it can anchor the model to stale conclusions even when current evidence differs. A compact “memory digest” (few bullet facts, each cited) is safer and cheaper.

Per-token GUI insertion (cursor insert for every token) may create UI overhead under fast streaming. Coalescing tokens (buffer + flush timer) reduces UI churn and improves responsiveness.
API compatibility risks

v10_qwen_ai_models.py posts to /v1/chat/completions and streams tokens correctly, but sends options: {"temperature": ...}. OpenAI Chat Completions defines temperature as a top-level field. Ollama’s OpenAI-compatibility documentation demonstrates using the OpenAI client against base_url=http://localhost:11434/v1/ for chat completions, implying standard OpenAI-shaped payloads should work.

Recommendation: send OpenAI-shaped parameters (temperature, top_p, etc. at top-level) to maximize compatibility; keep Ollama-native options only if you also support Ollama’s native endpoints (not shown here).
Unspecified details to explicitly track

    JSON schema version / prompt schema version: unspecified.
    Model context window(s) and target latency SLAs: unspecified.
    Supported model list and default target model: partially inferred from fallbacks; size/availability are unspecified.
    Whether Ollama’s OpenAI compatibility supports developer role messages for your version: unspecified. OpenAI Chat Completions does include a developer role in examples, but Ollama compatibility coverage is “parts of the OpenAI API,” not necessarily every feature.

Revised prompt architecture and templates
Modular prompt components

This architecture keeps the deterministic/validator parsers stable by preserving exact section headers while reducing duplication and enforcing citations.

Component A: MASTER_SYSTEM_PROMPT (above)
Stable across all requests.

Component B: INTENT_ADDON_SYSTEM_PROMPTS
Small, route/intention-specific instructions (system role). Examples:

python

INTENT_ADDONS = {
    "which_calls": """\
Intent: CALLER LOOKUP (call-site proof required).
- The "caller" is the function/method whose SOURCE SNIPPET contains the invocation of the asked callee.
- Do not treat an import as a call.
- If no call site is shown, respond with INSUFFICIENT_EVIDENCE and state that a caller snippet is missing.
""",
    "flow_chain": """\
Intent: FLOW/CHAIN TRACE.
- Produce a step-by-step chain. Each step must cite at least one [SN##] if code is shown, otherwise [F##]/[S##].
- Do not claim a handoff unless the call site is shown in a snippet.
""",
    "signal_action": """\
Intent: QT SIGNAL/ACTION.
- Prefer qt_signal_map evidence if present in FILE EVIDENCE or SYMBOL EVIDENCE details.
- When naming a signal->handler connection, cite the evidence id(s) that show the connection.
""",
}

Component C: USER_PROMPT_TEMPLATE (evidence pack)
This is the PromptBuilder output (user role). Keep it compact and parseable.

USER_PROMPT_TEMPLATE = """\
QUESTION
{question}

CONTEXT
project_root: {project_root}
index_sections_present: {index_sections_present}

CONVERSATION DIGEST
{memory_digest}

FILE EVIDENCE
{file_evidence_blocks}

SYMBOL EVIDENCE
{symbol_evidence_blocks}

SOURCE SNIPPETS
{snippet_blocks}

OUTPUT FORMAT NOTE
- Use evidence ids in square brackets at the end of each claim.
- If insufficient, output INSUFFICIENT_EVIDENCE then missing-evidence lines.
"""

Exact JSON field names to reference when filling placeholders

From JsonProjectIndex.load_json and attribute assignments, the canonical JSON includes (at minimum) these top-level keys that matter for prompting:

    project_summary (used for counts and entry_files)
    collector_info, collection_config
    packaging_metadata (e.g., project_name, declared_version, packaging_files_found, packaging_evidence)
    documentation_intent (e.g., project_purpose_summary, documentation_files_found, run_instructions, documentation_evidence)
    qt_signal_map
    widget_registry, widget_summary, widget_hotspots, plus widget text/layout indexes
    runtime indexes: runtime_call_stack_index, runtime_signal_connections, runtime_state_snapshots, runtime_trace_raw, plus summaries/hotspots

Local evidence: v10_index_loader.py, test_collector_main_static_context_sections.py.
Evidence formatting rules (keep validator compatibility)

Do not change these without updating v10_ai_bridge.py regex/section scanning:

    Section header literals must remain exactly:
        FILE EVIDENCE
        SYMBOL EVIDENCE
        SOURCE SNIPPETS
    Snippet header regex compatibility:
        ^[SN##] path:line anchor=... (current bridge regex: ^\[(SN\d{2})\]\s+(.+?):(\d+)\s+anchor=(.+)$)

Local evidence: v10_ai_bridge.py snippet parser regex and file/symbol evidence parsers.
Prompt variants table (short / medium / long)

Token estimates are approximate (rule of thumb: 1 token ≈ 3–4 chars of English + formatting). Actual tokens depend on snippet length and model tokenizer (unspecified).

Variant	Evidence limits (recommended)	Expected token cost	Use cases	Pros	Cons	Recommended default
Short	Files: 4, Symbols: 6, Snippets: 4 (cap snippet chars)	~1.2k–2.5k tokens	Tier 1 locators; “which file defines X”; one-line answers	Fast; low hallucination surface; cheap	May miss context for flow/explanation	Not default
Medium	Files: 8, Symbols: 12, Snippets: 8	~2.5k–5.5k tokens	Most questions; Tier 2 signals / Tier 4 responsibilities	Good balance	Still can grow if snippets are long	Yes (default)
Long	Files: 12, Symbols: 18, Snippets: 14	~5.5k–10k+ tokens	Tier 3 chain tracing; complex subsystem mapping	Higher recall; fewer “missing link”	Slow; risk of context overflow on smaller models	Only when intent requires

Integration guidance and prompt assembly algorithm
Flowchart for improved prompt assembly

flowchart TD
  A[Question text] --> B[route_query_intent -> QueryRouteDecision]
  B --> C{route}
  C -->|ranked| D[Return ranked evidence only]
  C -->|deterministic| E[Try deterministic resolver on index/bundle]
  E -->|hit| F[Emit answer without model call]
  E -->|miss| G[Fall through to generative]
  C -->|generative| G[Generative path]
  G --> H[Select prompt variant + token budget]
  H --> I[Assemble user evidence pack with fixed section markers]
  I --> J[Compose messages: MASTER_SYSTEM + INTENT_ADDON + USER]
  J --> K[Stream chat completions]
  K --> L[Post-validate: ids/symbols/paths + required snippets]
  L --> M[Emit final answer or INSUFFICIENT_EVIDENCE]

ecommended prompt-building pseudocode (Pythonic, performant)

This aims to be drop-in conceptually for v10_prompt_builder.py + v10_ai_bridge.py, preserving current section markers so existing validators/parsers keep working.

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

# Heuristic token estimator (fast, dependency-free).
def estimate_tokens(text: str) -> int:
    # Conservative: English ~4 chars/token; add small overhead.
    return max(1, (len(text) // 4) + 16)

@dataclass(frozen=True)
class PromptBudget:
    max_input_tokens: int
    max_snippet_chars: int
    max_files: int
    max_symbols: int
    max_snippets: int

BUDGETS = {
    "short": PromptBudget(2600, 3000, 4, 6, 4),
    "medium": PromptBudget(5200, 7000, 8, 12, 8),
    "long": PromptBudget(10000, 14000, 12, 18, 14),
}

def choose_variant(intent_name: str, user_verbosity: str) -> str:
    # Keep deterministic/locator intents cheap by default.
    if intent_name in ("one_line_locator", "which_calls", "exact_locator"):
        return "short"
    if "chain" in intent_name or "flow" in intent_name:
        return "long" if user_verbosity.lower() in ("detailed", "very detailed") else "medium"
    return "medium"

def take_top(items: list, limit: int, score_key: Callable) -> list:
    return sorted(items, key=score_key, reverse=True)[:limit]

def trim_snippet_text(snippet_text: str, max_chars: int) -> str:
    if len(snippet_text) <= max_chars:
        return snippet_text
    # Hard cut (cheap). Optionally cut on newline boundary.
    cut = snippet_text[:max_chars]
    last_nl = cut.rfind("\n")
    return cut if last_nl < 200 else cut[:last_nl]

def build_memory_digest(turns: list, max_chars: int = 800) -> str:
    if not turns:
        return "None"
    # Prefer a small digest; do not include full prior answers.
    lines: list[str] = []
    for t in turns[-2:]:
        q = t.question.strip().replace("\n", " ")
        a = t.answer.strip().replace("\n", " ")
        lines.append(f"- Q: {q}")
        lines.append(f"  A: {a[:240]}{'...' if len(a) > 240 else ''}")
    out = "\n".join(lines)
    return out if len(out) <= max_chars else out[:max_chars] + "..."

def format_file_block(item) -> str:
    # Must preserve header line format for v10_ai_bridge parser:
    # [F##] score=<int>
    return "\n".join(
        [
            f"[{item.evidence_id}] score={item.score}",
            str(item.detail).strip(),
            "",
        ]
    )

def format_symbol_block(item) -> str:
    return "\n".join(
        [
            f"[{item.evidence_id}] score={item.score}",
            str(item.detail).strip(),
            "",
        ]
    )

def format_snippet_block(sn: dict, max_chars: int) -> str:
    # Must preserve header regex:
    # [SN##] path:line anchor=...
    text = trim_snippet_text(str(sn.get("text", "")), max_chars=max_chars)
    return "\n".join(
        [
            f"[{sn['snippet_id']}] {sn['path']}:{sn['line']} anchor={sn['anchor']}",
            text,
            "",
        ]
    )

def build_user_prompt(
    question: str,
    project_root: str,
    index_sections_present: list[str],
    memory_turns: list,
    bundle,
    intent_name: str,
    verbosity: str,
) -> tuple[str, str]:
    variant = choose_variant(intent_name=intent_name, user_verbosity=verbosity)
    budget = BUDGETS[variant]

    files = take_top(bundle.file_evidence, budget.max_files, score_key=lambda x: x.score)
    symbols = take_top(bundle.symbol_evidence, budget.max_symbols, score_key=lambda x: x.score)
    snippets = take_top(bundle.snippet_evidence, budget.max_snippets, score_key=lambda x: int(x.get("score", 0)))

    file_blocks = "".join(format_file_block(f) for f in files)
    symbol_blocks = "".join(format_symbol_block(s) for s in symbols)
    snippet_blocks = "".join(format_snippet_block(sn, budget.max_snippet_chars) for sn in snippets)

    prompt = "\n".join(
        [
            "QUESTION",
            question.strip(),
            "",
            "CONTEXT",
            f"project_root: {project_root}",
            f"index_sections_present: {', '.join(index_sections_present)}",
            "",
            "CONVERSATION DIGEST",
            build_memory_digest(memory_turns),
            "",
            "FILE EVIDENCE",
            file_blocks.strip(),
            "",
            "SYMBOL EVIDENCE",
            symbol_blocks.strip(),
            "",
            "SOURCE SNIPPETS",
            snippet_blocks.strip(),
            "",
            "OUTPUT FORMAT NOTE",
            "- End every technical claim with evidence ids in square brackets (example: [F01] or [SN03]).",
            "- If insufficient, output INSUFFICIENT_EVIDENCE then missing-evidence lines.",
        ]
    ).strip() + "\n"

    # Optional: shrink further if we exceed budget (iterative drop of lowest-score snippets first).
    while estimate_tokens(prompt) > budget.max_input_tokens and snippets:
        snippets.pop()
        snippet_blocks = "".join(format_snippet_block(sn, budget.max_snippet_chars) for sn in snippets)
        prompt = prompt.replace("SOURCE SNIPPETS\n", "SOURCE SNIPPETS\n")  # no-op anchor for clarity
        prompt = "\n".join(prompt.split("\n")[:-1])  # cheap; in real code rebuild once

    return prompt, variant

Integration notes for v10_prompt_builder.py

What to change:

    Split the current monolithic build(...) into:
        build_user_prompt(...) (returns only the user message content; preserve section headers and snippet header regex compatibility).
        build_memory_digest(...) (replace “CONVERSATION MEMORY” full answers with a smaller digest; optionally keep the old behavior behind a flag for backward compatibility).
    Remove duplicated “SYSTEM CONSTRAINTS” from the user prompt (move to system prompt exclusively). Keep only a short “OUTPUT FORMAT NOTE” at the end to reduce token cost.
    Replace any literal “...” that appears inside instructions with full explicit sentences (ellipses inside guardrails are ambiguous and degrade determinism).

Where to hook decisions:

    Accept QueryRouteDecision.intent_name (passed from v10_main_window.py after route_query_intent(question)) so PromptBuilder can select:
        prompt variant (short/medium/long),
        intent-specific evidence ordering (e.g., prioritize call-site snippets for which_calls),
        tighter snippet caps for locators.

Integration notes for v10_ai_bridge.py

What to change:

    Replace the inline system message string with MASTER_SYSTEM_PROMPT constant.
    Add an intent-addon system message using decision.intent_name (you already have a focus_message; this can become the intent addon, and focus_message can become a smaller optional “top snippet ids to prioritize” note).
    Keep or improve the validator, but align it with the new citation contract:
        If the answer contains non-trivial claims without any evidence ids, treat that as a grounding failure (emit INSUFFICIENT_EVIDENCE and say “missing citations”).
        Preserve the existing forbidden ids/symbol rules.

Thread-safety and streaming:

    Emitting Qt signals from worker threads is the correct pattern; PySide6’s Signal/Slot mechanism is designed for object communication.
    Reduce UI overhead by batching tokens:
        Buffer tokens in the worker, emit every 30–60 ms (or every N chars).
        In the UI slot, insert larger chunks rather than per-token.

Integration notes for v10_qwen_ai_models.py (API shape)

Recommended change for maximum OpenAI-compatibility:

    Send OpenAI Chat Completions-shaped fields at top-level:
        temperature (top-level) per OpenAI spec.
    Keep stream=True and token extraction from choices[].delta.content, which matches OpenAI streaming chunk schema.
    Only include Ollama-native options if you have verified Ollama accepts it for /v1/chat/completions in your deployment; otherwise, remove it to avoid silent-ignored parameters. Ollama documents OpenAI compatibility for /v1/chat/completions usage.

Tests, evaluation, and migration plan
Tests and evaluation plan

Unit tests (fast, deterministic):

    PromptBuilder formatting:
        Contains exact section markers: FILE EVIDENCE, SYMBOL EVIDENCE, SOURCE SNIPPETS.
        Snippet headers match regex expected by bridge.
        Variant limits enforced (counts and snippet char caps).
        Citation instructions present in the user prompt tail note.
    AI bridge parsers:
        _extract_file_evidence_blocks correctly reads [F##] score=.
        _extract_snippet_blocks correctly parses snippet headers and text.
        New “missing citations” validator triggers when expected (if implemented).

Regression tests using validated tiers (from help index):

    Tier 1 deterministic locators:
        Evaluate exact expected file paths/symbol owners for known questions (exact string comparison).
    Tier 2 signal/action:
        Verify that answers contain at least one citation to evidence that includes qt_signal_map-derived connection claims.
    Tier 3 chain/flow:
        Verify step count and that each step has at least one evidence id.
    Tier 4 responsibility:
        Verify that the output contains citations and does not name modules/symbols not present in evidence.

Metrics to track (per question set):

    Correctness:
        Exact match rate for Tier 1 answers.
        Human/heuristic scoring for Tier 2–4 (or golden outputs if available).
    Hallucination rate:
        Percentage of answers failing the grounding validator (forbidden ids/symbols/paths), plus “uncited claim” failures if added.
    Latency:
        Time to first token (streaming), time to final.
        UI responsiveness under streaming load.
    Token usage:
        Prompt token estimate (pre-send) and completion tokens if available from provider (unspecified for Ollama OpenAI-compat; may not return usage consistently).
    Refusal/insufficient rate:
        Rate of INSUFFICIENT_EVIDENCE responses (should drop for answerable questions after better retrieval + evidence packing).

OpenAI’s docs describe streaming behavior and parameters for Chat Completions, which informs both your streaming handler and your token/latency instrumentation assumptions.
Migration checklist and backward compatibility

Backward compatibility goals:

    Keep existing section headers and snippet header format so:
        deterministic parsing continues to work,
        evidence id extraction continues to work,
        UI evidence panel expectations remain aligned.

Checklist:

    Add PROMPT_SCHEMA_VERSION: 2 in the user prompt “CONTEXT” section (optional but recommended).
    Implement PromptBuilder refactor behind a feature flag:
        use_prompt_v2=True default after verification.
    Update v10_ai_bridge.py validator:
        accept both v1 and v2 formats during migration.
    Update v10_qwen_ai_models.py payload:
        change temperature field to top-level; keep streaming unchanged.
    Add tests that run both prompt schema versions for a limited time window, then retire v1.

Prioritized action list with effort and milestones

Effort scale: S (hours), M (1–3 days), L (1–2+ weeks).

    Replace system prompt with MASTER_SYSTEM_PROMPT constant and add intent add-ons (S)
    Enforce citation-per-claim contract (validator + prompt) (M)
    Token-budgeted evidence selection + variants (M)
    Refactor conversation memory into a digest (M)
    Fix /v1/chat/completions payload shape (temperature top-level; remove/verify options) (S/M)
    Improve streaming UI performance (buffer/coalesce tokens) (M)
    Build regression suite from validated tiers in help index (L)

Proposed milestone timeline (dates are proposals; SLAs are unspecified):

gantt
  title Prompt system upgrade milestones
  dateFormat  YYYY-MM-DD
  axisFormat  %b %d
  section Foundation
  Master system prompt + intent addons          :a1, 2026-04-10, 3d
  OpenAI-compat payload cleanup                :a2, 2026-04-12, 3d
  section Correctness hardening
  Citation-per-claim policy + validator         :b1, 2026-04-15, 7d
  Token budget + prompt variants                :b2, 2026-04-18, 7d
  Memory digest refactor                         :b3, 2026-04-22, 5d
  section Quality and performance
  Streaming UI coalescing                        :c1, 2026-04-25, 5d
  Validated tiers regression harness             :c2, 2026-04-28, 14d



CANONICAL ARCHITECTURE RULES FOR E:\eeg_kernel_ai_neural_data_analysis

Context:
This project previously had many architecture gate warnings, especially public facade findings, layer-boundary warnings, session-state scattered writes, duplicate-normalizer warnings, and circular imports caused by eager package facades. These were cleaned until all hardening gates passed with zero warnings. Preserve that state.

General rules:
1. Do not reintroduce public facade noise.
2. Do not reintroduce layer-boundary violations.
3. Do not reintroduce scattered session-state mutations.
4. Do not reintroduce duplicate private helper names.
5. Do not reintroduce eager package imports that can cause circular imports.
6. Always validate with the architecture gates after changes.
7. Since I do not use Git, tell me when to create a ZIP backup before risky or multi-file changes.

Public facade rules:
- Every package __init__.py must be a clean public facade.
- Never use wildcard imports in __init__.py.
- Never export a name in __all__ unless it is locally bound in that same __init__.py.
- Never export generic noise names such as ROOT, PROJECT_ROOT, MANIFEST_PATH, HELP_PATH, logger, log, main, or regex/helper constants unless explicitly required as public API.
- Avoid duplicate public exports across parent and child facades.
- Prefer explicit imports or lazy facade runtime helpers.
- Package facades should not import heavy runtime modules just to expose names.

Lazy facade rules:
- If a package facade import can create a circular import or heavy runtime startup cost, use a lazy __getattr__ runtime helper.
- Keep lazy runtime helpers in a private module such as _plot_modes_facade_runtime.py, _render_helpers_facade_runtime.py, or similar.
- __init__.py may import only __getattr__ and __dir__ from the private runtime helper and should keep __all__ minimal or empty when appropriate.
- Do not eager-import UI/runtime classes from __init__.py if those classes import back into the same package tree.

Layer-boundary rules:
- common/templates must not import from core, plugins, or shell directly.
- common code must remain lower-level and reusable.
- If common/templates needs a runtime-layer function or class, use one of these approaches:
  1. Move the shared helper into common/templates or another lower-level common module.
  2. Inject the dependency from the runtime layer.
  3. Use a local lazy compatibility binding only when preserving old behavior is necessary.
- Do not solve layer-boundary warnings by adding allowlist entries unless explicitly requested.
- Do not move runtime-heavy logic into common/templates unless it is genuinely reusable and layer-safe.

Session-state rules:
- Do not directly assign protected runtime-state fields such as:
  - current_raw
  - raw_original
  - active_session_bundle
- Use centralized helpers from:
  core.session.protected_state_update
- Use:
  - set_protected_current_raw(target, value)
  - set_protected_raw_original(target, value)
  - set_protected_active_session_bundle(target, value)
- Do not scatter setattr(target, "current_raw", value) or direct target.current_raw = value across the project.

Duplicate-normalizer rules:
- Private helper names should be specific to their module/domain.
- Avoid repeated generic private helpers such as:
  - _parse_bool
  - _parse_channel_names
  - _normalize_ui_token
  - _parse_clearable_bool
  - _infer_mne_channel_type
- Rename helpers with domain-specific prefixes when needed, for example:
  - _eeg_filter_state_spatial_parse_bool
  - _eeg_filter_state_channel_cleanup_parse_channel_names
  - _infer_neurosoft_mne_channel_type
- Use token-aware replacements for renaming Python identifiers. Do not replace inside strings or comments unless intentional.

Import-order rules:
- from __future__ imports must stay immediately after the module docstring and before any other imports or executable code.
- When inserting imports automatically, first preserve or normalize:
  from __future__ import annotations
- After patching, always run py_compile on every touched file.

Patch safety rules:
- Prefer direct patch scripts that:
  1. Create .bak_* backups beside touched files.
  2. Patch only intended files.
  3. Compile every touched Python file.
  4. Run smoke imports when relevant.
  5. Restore backups automatically if compilation or smoke checks fail.
- For large waves, use guarded scripts that skip risky files instead of forcing changes.
- Do not patch behavior-heavy __init__.py files blindly.
- Do not rewrite files with non-literal __all__ or wildcard imports using generic scripts unless the patch is targeted and reviewed.

Backup rules:
- Before large multi-file waves, tell me:
  BACKUP NOW
- Use ZIP backups because I do not use Git.
- Suggested backup command:
  cd E:\
  Compress-Archive `
    -Path E:\eeg_kernel_ai_neural_data_analysis `
    -DestinationPath E:\eeg_kernel_ai_neural_data_analysis_BACKUP_<CLEAR_NAME>.zip `
    -Force

Validation rules:
After any architecture or multi-file patch, run:

cd E:\eeg_kernel_ai_neural_data_analysis

python tools\architecture\run_security_hardening_gates.py

Expected clean result:
- Layer boundary gate: PASS
- Session-state gate: PASS
- Duplicate-normalizer gate: PASS
- Public facade gate: PASS
- Overall result: PASS

For focused validation, use:
python tools\architecture\run_focused_public_facade_package_gate.py --path-prefix "<path>" --strict-clean

Runtime validation:
After changes that touch imports, facades, UI templates, shell, viewer, session, or runtime state, run:

E:\mne_py3.10\python.exe E:\eeg_kernel_ai_neural_data_analysis\shell\run_kanda_no_coverage.py

The app must open successfully.

Failure handling:
- If a patch fails compilation, gate validation, or app startup, restore backups immediately.
- Do not continue with new waves while the project is in a failed state.
- Fix the smallest failing cluster first.
- Prefer one precise follow-up patch over another broad patch after a failure.

Current clean-state expectation:
This project should remain at:
- Public facade warnings: 0
- Duplicate-normalizer warnings: 0
- Session-state warnings: 0
- Layer-boundary warnings: 0
- Overall security hardening result: PASS

When helping me in the future:
- Keep changes in large but safe chunks.
- Give direct PowerShell patch scripts when possible.
- Keep all generated Python compatible with Python 3.10+, Windows, PyCharm, and standard CPython.
- Use ASCII-only Python source.
- Include module docstrings and function docstrings.
- Prefer standard library only.
- Tell me when to backup.
- Always validate with gates and app startup after risky changes.