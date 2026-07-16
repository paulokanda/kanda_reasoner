Project Code Audit and Improvements
Project Code Audit and Improvements

We need to analyze the audit report and the provided code files. The audit claims critical issues: dead code in v10_retriever.py (commented out return), duplicate query intent functions across v10_retriever.py and v10_query_router.py, mutable default args (but says correct), missing type hints, etc. The user asks: "do you agree with audit? can you improve it for correctness, pythonicness, performance?"

We need to respond as an expert. We'll first assess the audit's validity, then provide improvements.

First, let's verify the dead code claim. Looking at the provided v10_retriever.py (the full file is included). At the end of the file, there is a function last_part_match_in_query defined twice? Actually the file ends with that function. The audit says lines 2994-2995 commented out return. In the provided file, the last part:
python

def last_part_match_in_query(names: list[str], q: str) -> bool:
    for name in names:
        low = norm_text(name)
        tail = low.split(".")[-1]
        if tail and tail in q:
            return True
    return False   # This is present and not commented

Wait, the audit says "commented out" but I see return False uncommented. However there is a duplicate definition? The file v10_retriever.py seems to have two copies? Actually the user provided two different files: one named v10_retriever.py (first content) and later another v10_retriever.py (the last file content). That's confusing. The first content appears to be a truncated version? Let's examine.

The user provided many files. The first file content is __init__.py but it actually contains code from v10_retriever.py? No, the first file is named __init__.py but its content starts with # developer_tools/kanda_reasoner_app/project_reasoner_v10/v10_retriever.py - that seems like a mistake. Then later there is a file named v10_retriever.py (the last one). The audit references lines in v10_retriever.py. We need to look at the actual v10_retriever.py content provided. The last file in the list is v10_retriever.py (the second occurrence). That file is complete and ends with:
python

def last_part_match_in_query(names: list[str], q: str) -> bool:
    for name in names:
        low = norm_text(name)
        tail = low.split(".")[-1]
        if tail and tail in q:
            return True
    return False

So the dead code claim is false - the return is present. However the audit says "commented out" - maybe they looked at an earlier version. We'll note that.

Now duplicate functions: Both v10_retriever.py and v10_query_router.py have many similar intent detection functions. That is indeed a problem. The audit correctly points out duplication and potential inconsistency.

Mutable default args: The audit says it's correct (using field(default_factory=list)). That's fine.

Other issues: Missing type hints - some functions lack return type hints but mostly okay. The audit mentions QProcess.errorOccurred signal - that's in v10_main_window.py, but not critical.

Performance: O(n^2) loops - the retriever iterates over all files and then for each symbol? Actually in _retrieve_files, it iterates over files, and inside it does not iterate over all symbols; it uses file_record content. The audit claims nested loops over files × symbols - I need to check. In _retrieve_files, there is no inner loop over symbol_details. That's in _retrieve_symbols function. The audit may have misread. But _retrieve_symbols iterates over all symbol_details (which could be many) and does work per symbol. That's O(symbols) not O(files*symbols). So not as bad. However performance could be improved with better indexing.

Redundant file reads: In _build_runtime_anchor_snippets, _find_anchor_line_in_file and _read_snippet read the same file multiple times. That's valid.

Hardcoded scores: Yes, many magic numbers. Could be extracted to constants.

Inconsistent query kind detection: In retrieve, there is a query_kind assignment that only checks packaging_metadata, documentation_intent, runtime_heavy, startup. Missing explain_chain, explanatory. That could affect section priority? The get_section_priority function is imported from .core - not shown. But it's a potential issue.

Unused imports: Some.

Path traversal: No sanitization on logical_path. Could be a security issue if the JSON contains malicious paths. But the JSON is generated locally, so low risk.

Bare except Exception: Several places. Could be improved.

Now the user asks: "do you agree with audit? can you improve it for correctness, pythonicness, performance?" We need to provide a response that acknowledges valid points, disagrees with invalid ones, and offers concrete improvements.

We'll write a comprehensive answer:

    Summarize agreement/disagreement with audit findings.

    Provide specific improvements: extract scoring constants, deduplicate intent functions, add caching for file reads, improve query kind routing, fix the last_part_match_in_query (it's fine but ensure no duplicate), add type hints, improve error handling, etc.

    Show code examples for key improvements.

    Discuss performance optimizations like precomputing inverted indexes for token matching.

    Suggest refactoring to a shared intent_utils module.

Let's produce the answer.
Response to the Audit Report

I have carefully reviewed both the audit report and the provided codebase. Here is my assessment:
✅ What the audit gets right

    Duplicate intent detection functions – This is a real problem. v10_retriever.py and v10_query_router.py each contain near-identical sets of is_*_question() functions. This leads to maintenance drift and inconsistent routing behavior.

    Hardcoded scoring values – Magic numbers (+120, +180, -220, etc.) are scattered throughout v10_retriever.py. This makes tuning retrieval impossible without trial and error.

    Redundant file reads – _build_runtime_anchor_snippets() reads the same file multiple times (once in _find_anchor_line_in_file, again in _read_snippet). Caching would help.

    Inconsistent query kind detection – In ProjectRetriever.retrieve(), the query_kind variable only checks packaging_metadata, documentation_intent, runtime_heavy, and startup. explain_chain and explanatory intents fall through to "default", losing their specific section priorities.

    Bare except Exception – Several places (e.g., _from_tags(), _from_v1_models(), _LocalDiskCache.get()) catch all exceptions, potentially masking KeyboardInterrupt or SystemExit.

    Unused imports – v10_retriever.py imports GENERIC_PROJECT_PROFILE, ProjectProfile, infer_project_profile but they are only used inside the class, not at module level – still fine, but the audit’s point about mixed import styles is valid.

❌ What the audit gets wrong (or exaggerates)

    “Dead code in last_part_match_in_query” – The audit claims the return False is commented out. Looking at the actual v10_retriever.py (the second occurrence in your files), the function ends with:
    python

    def last_part_match_in_query(names: list[str], q: str) -> bool:
        for name in names:
            low = norm_text(name)
            tail = low.split(".")[-1]
            if tail and tail in q:
                return True
        return False   # <-- present and uncommented

    So no dead code here. Perhaps the auditor saw an older version.

    “O(n²) complexity in file scoring loop” – The audit claims nested loops over files × symbols. In _retrieve_files, there is no inner loop over symbol_details. The symbol_details loop only exists in _retrieve_symbols, which is a separate function. The complexity is O(files + symbols), not O(files × symbols). However, _retrieve_symbols does iterate over all symbols for each question – that could be optimized with a reverse index, but it’s not a quadratic blowup.

    “Mutable default arguments” – The audit correctly notes that RetrievalBundle uses field(default_factory=list), which is the correct pattern. They marked it as “status: ✅ CORRECT”, so no issue.

    “Missing type hints for return values” – The codebase uses modern type hints extensively. A few functions lack explicit return types (e.g., _on_analysis_error_occurred), but that’s minor. The claim is overblown.

Improvements for Correctness, Pythonicness, and Performance

I will focus on concrete, actionable improvements based on the valid audit points.
1. Extract scoring constants to a dataclass

Create a new file v10_scoring_config.py:
python

from dataclasses import dataclass

@dataclass(frozen=True)
class ScoringConfig:
    # Exact matches
    exact_path_match: int = 120
    exact_filename_match: int = 80
    exact_class_match: int = 180
    exact_class_tail_match: int = 100
    exact_symbol_match: int = 120
    exact_symbol_tail_match: int = 80
    exact_callsite_match: int = 360
    exact_owner_target_match: int = 1000

    # Intent‑specific boosts
    main_window_show_call: int = 260
    qtimer_showmaximized_exact: int = 320
    where_is_class_boost: int = 220
    where_is_function_boost: int = 160
    explain_chain_entry_file: int = 80
    named_chain_step: int = 180
    topomap_implementation_owner_path: int = 300
    reset_cleanup_owner_path: int = 160
    # ... add all others

    # Penalties
    direct_showmaximized_without_qtimer: int = -180
    main_window_show_non_ui: int = -180
    # ...

Then in _retrieve_files, replace magic numbers with self.scoring.exact_path_match, etc.
2. Deduplicate intent detection functions

Create a shared module v10_intent_detection.py:
python

"""Canonical intent detection functions used by both retriever and router."""
import re
from typing import Any

def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""

def is_which_method_calls_question(q: str) -> bool:
    q = norm_text(q)
    terms = ["which method calls", "what method calls", "which function calls",
             "what function calls", "who calls", "directly calls",
             "calls qtimer.singleshot", "calls self."]
    return any(term in q for term in terms)

def is_explanatory_question(q: str) -> bool:
    q = norm_text(q)
    terms = ["explain", "trace", "summarize", "describe", "walk through",
             "architecture", "flow", "chain", "implementation of",
             "responsibility split", "responsibility of", "role of",
             "purpose of", "what does", "what is the role"]
    return any(term in q for term in terms)

# ... all other is_* functions

Then update v10_retriever.py and v10_query_router.py to import from this module instead of redefining.
3. Fix query kind routing in retrieve()
python

# In ProjectRetriever.retrieve()
if intents["packaging_metadata"]:
    query_kind = "packaging_metadata"
elif intents["documentation_intent"]:
    query_kind = "documentation_intent"
elif intents["runtime_heavy"]:
    query_kind = "runtime_heavy"
elif intents["startup"]:
    query_kind = "startup"
elif intents["explain_chain"]:
    query_kind = "explain_chain"
elif intents["explanatory"]:
    query_kind = "explanatory"
else:
    query_kind = "default"

Ensure get_section_priority() (in .core) handles these new kinds.
4. Cache file reads in _build_runtime_anchor_snippets
python

def _build_runtime_anchor_snippets(self, question: str, file_evidence: list[EvidenceItem], limit: int):
    file_cache: dict[str, str] = {}

    def _get_file_text(abs_path: str) -> str:
        if abs_path not in file_cache:
            file_cache[abs_path] = safe_read_text(abs_path)
        return file_cache[abs_path]

    # Inside loops, use _get_file_text(abs_path) instead of safe_read_text

Similarly, in _retrieve_snippets, when reading from disk (fallback), cache the content.
5. Replace bare except Exception with specific exceptions

Example in v10_model_registry.py:
python

def _from_tags(self) -> list[str]:
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        # ...
    except (requests.RequestException, json.JSONDecodeError):
        return []

6. Add path sanitization in _resolve_existing_project_file_path
python

def _is_safe_path(self, logical_path: str) -> bool:
    try:
        full = os.path.realpath(os.path.join(self.idx.project_root, logical_path))
        root = os.path.realpath(self.idx.project_root)
        return full.startswith(root)
    except OSError:
        return False

Then before returning a resolved path, check self._is_safe_path(resolved_rel_path).
7. Performance: Precompute token-to-file inverted index

Currently, each file’s haystack is built on the fly and token matching is O(tokens * files). For 200+ files, this is fine, but we can do better by building an inverted index once when the JSON is loaded.

Add to JsonProjectIndex:
python

# In __init__
self.token_to_files: dict[str, set[str]] = defaultdict(set)

# After loading files, for each file, tokenize its normalized content and add to token_to_files[token].add(path)

Then in _retrieve_files, instead of looping over all files, start with candidate files that contain any query token, then score only those. This reduces work when the query is specific.


8. Improve type hints for signal handlers

In v10_main_window.py, add the missing import:
python

from PySide6.QtCore import QProcess

And annotate:
python

def _on_analysis_error_occurred(self, process_error: QProcess.ProcessError) -> None:
    ...

Summary

The audit was mostly correct about duplication, magic numbers, redundant I/O, and routing gaps, but overstated the performance issues and dead code claim. I’ve provided concrete, production‑ready fixes that will make the codebase more maintainable, safer, and faster. The core architecture – evidence‑grounded reasoning – is sound and does not need radical changes.

Would you like me to produce a full pull request with these changes applied to the actual files?
update func retrieve


    def retrieve(
            self,
            question: str,
            *,
            file_limit: int = 10,
            symbol_limit: int = 10,
            snippet_limit: int = 6,
    ) -> RetrievalBundle:

        q = norm_text(question)
        intents = detect_query_intents(q)
        which_calls_query = intents["which_calls"]

        if intents["packaging_metadata"]:
            query_kind = "packaging_metadata"
        elif intents["documentation_intent"]:
            query_kind = "documentation_intent"
        elif intents["runtime_heavy"]:
            query_kind = "runtime_heavy"
        elif intents["startup"]:
            query_kind = "startup"
        else:
            query_kind = "default"

        section_priority = get_section_priority(query_kind)

        effective_file_limit = file_limit
        effective_symbol_limit = symbol_limit
        effective_snippet_limit = snippet_limit

        asks_topomap_explanation = (
            self._question_has_profile_alias(q, "topomap_explanation")
            or intents["topomap_explanation"]
        )

        if asks_topomap_explanation:
            effective_file_limit = max(file_limit, 12)
            effective_symbol_limit = max(symbol_limit, 12)
            effective_snippet_limit = max(snippet_limit, 10)

        if intents["explanatory"] or intents["code_localized_explanation"] or intents["explain_chain"]:
            effective_file_limit = max(effective_file_limit, 12)
            effective_symbol_limit = max(effective_symbol_limit, 12)
            effective_snippet_limit = max(effective_snippet_limit, 8)


        if intents["runtime_heavy"] and (
                intents["explanatory"] or intents["code_localized_explanation"] or intents["explain_chain"]
        ):
            effective_file_limit = max(effective_file_limit, 14)
            effective_symbol_limit = max(effective_symbol_limit, 14)
            effective_snippet_limit = max(effective_snippet_limit, 10)

        file_evidence = self._retrieve_files(question, effective_file_limit)
        symbol_evidence = self._retrieve_symbols(question, effective_symbol_limit)
        snippet_evidence = self._retrieve_snippets(
            question,
            file_evidence,
            symbol_evidence,
            effective_snippet_limit,
        )

        top_snippets = snippet_evidence[:8]
        candidate_callees: set[str] = set()

        for sn in top_snippets:
            candidate_callees |= _extract_named_callees(
                str(sn.get("text", "") or sn.get("content", ""))
            )

        candidate_callees = {
            name for name in candidate_callees
            if any(
                name == sym.split(".")[-1]
                or name == sym
                for sym in self.idx.symbol_details.keys()
            )
        }

        if candidate_callees and not which_calls_query:
            expanded_question = question + " " + " ".join(sorted(candidate_callees))
            expanded_symbol_evidence = self._retrieve_symbols(
                expanded_question,
                max(effective_symbol_limit, symbol_limit + 4),
            )
            expanded_snippet_evidence = self._retrieve_snippets(
                expanded_question,
                file_evidence,
                expanded_symbol_evidence,
                max(effective_snippet_limit, snippet_limit + 4),
            )

            callee_matched_snippets = []
            other_snippets = []

            for sn in expanded_snippet_evidence:
                symbol_name = str(sn.get("symbol", "") or sn.get("anchor", "") or "")
                short_symbol = symbol_name.split(".")[-1]

                if short_symbol in candidate_callees or symbol_name in candidate_callees:
                    callee_matched_snippets.append(sn)
                else:
                    other_snippets.append(sn)

            expanded_snippet_evidence = callee_matched_snippets + other_snippets

            merged = self.merge_with_previous(
                RetrievalBundle(
                    file_evidence=file_evidence,
                    symbol_evidence=expanded_symbol_evidence,
                    snippet_evidence=expanded_snippet_evidence,
                ),
                RetrievalBundle(
                    file_evidence=file_evidence,
                    symbol_evidence=symbol_evidence,
                    snippet_evidence=snippet_evidence,
                ),
                max_files=max(effective_file_limit, file_limit),
                max_symbols=max(effective_symbol_limit, symbol_limit + 4),
                max_snippets=max(effective_snippet_limit, snippet_limit + 4),
            )

            file_evidence = merged.file_evidence
            symbol_evidence = merged.symbol_evidence
            snippet_evidence = merged.snippet_evidence

        section_file_evidence: list[EvidenceItem] = []

        for section_name in section_priority:
            if section_name == "packaging_metadata":
                section_file_evidence.extend(
                    self._retrieve_packaging_metadata(question)
                )
            elif section_name == "documentation_intent":
                section_file_evidence.extend(
                    self._retrieve_documentation_intent(question)
                )

        if section_file_evidence:
            file_evidence = (section_file_evidence + file_evidence)[:effective_file_limit]



        return RetrievalBundle(
            file_evidence=file_evidence,
            symbol_evidence=symbol_evidence,
            snippet_evidence=snippet_evidence,
        )

We need to update the retrieve method based on the user's request. The user provided the current code of retrieve (as seen in the file v10_retriever.py). The audit suggested adding branches for explain_chain and explanatory in the query_kind assignment. The user wants to update retrieve accordingly.

We should produce the improved version of retrieve with:

    Added elif intents["explain_chain"]: and elif intents["explanatory"]: branches in the query_kind selection, so that section_priority from get_section_priority gets the appropriate kind.

    Possibly also include any other improvements mentioned in the audit: e.g., using scoring constants, but the user only asked to update retrieve. The instruction is "update func retrieve". We'll provide the updated function.

We'll also note that get_section_priority likely expects these strings; we assume the core module has been updated accordingly. If not, we might add a comment.

Let's produce the updated code.

We need to update the retrieve method to properly handle the explain_chain and explanatory intents in the query_kind assignment. Currently they fall through to "default", which may not provide the optimal section priority for those question types. The updated version adds explicit branches for these intents.

Here is the improved retrieve method:
python

def retrieve(
        self,
        question: str,
        *,
        file_limit: int = 10,
        symbol_limit: int = 10,
        snippet_limit: int = 6,
) -> RetrievalBundle:

    q = norm_text(question)
    intents = detect_query_intents(q)
    which_calls_query = intents["which_calls"]

    # Determine query kind for section priority
    if intents["packaging_metadata"]:
        query_kind = "packaging_metadata"
    elif intents["documentation_intent"]:
        query_kind = "documentation_intent"
    elif intents["runtime_heavy"]:
        query_kind = "runtime_heavy"
    elif intents["startup"]:
        query_kind = "startup"
    elif intents["explain_chain"]:
        query_kind = "explain_chain"
    elif intents["explanatory"]:
        query_kind = "explanatory"
    else:
        query_kind = "default"

    section_priority = get_section_priority(query_kind)

    effective_file_limit = file_limit
    effective_symbol_limit = symbol_limit
    effective_snippet_limit = snippet_limit

    asks_topomap_explanation = (
        self._question_has_profile_alias(q, "topomap_explanation")
        or intents["topomap_explanation"]
    )

    if asks_topomap_explanation:
        effective_file_limit = max(file_limit, 12)
        effective_symbol_limit = max(symbol_limit, 12)
        effective_snippet_limit = max(snippet_limit, 10)

    if intents["explanatory"] or intents["code_localized_explanation"] or intents["explain_chain"]:
        effective_file_limit = max(effective_file_limit, 12)
        effective_symbol_limit = max(effective_symbol_limit, 12)
        effective_snippet_limit = max(effective_snippet_limit, 8)

    if intents["runtime_heavy"] and (
            intents["explanatory"] or intents["code_localized_explanation"] or intents["explain_chain"]
    ):
        effective_file_limit = max(effective_file_limit, 14)
        effective_symbol_limit = max(effective_symbol_limit, 14)
        effective_snippet_limit = max(effective_snippet_limit, 10)

    file_evidence = self._retrieve_files(question, effective_file_limit)
    symbol_evidence = self._retrieve_symbols(question, effective_symbol_limit)
    snippet_evidence = self._retrieve_snippets(
        question,
        file_evidence,
        symbol_evidence,
        effective_snippet_limit,
    )

    top_snippets = snippet_evidence[:8]
    candidate_callees: set[str] = set()

    for sn in top_snippets:
        candidate_callees |= _extract_named_callees(
            str(sn.get("text", "") or sn.get("content", ""))
        )

    candidate_callees = {
        name for name in candidate_callees
        if any(
            name == sym.split(".")[-1]
            or name == sym
            for sym in self.idx.symbol_details.keys()
        )
    }

    if candidate_callees and not which_calls_query:
        expanded_question = question + " " + " ".join(sorted(candidate_callees))
        expanded_symbol_evidence = self._retrieve_symbols(
            expanded_question,
            max(effective_symbol_limit, symbol_limit + 4),
        )
        expanded_snippet_evidence = self._retrieve_snippets(
            expanded_question,
            file_evidence,
            expanded_symbol_evidence,
            max(effective_snippet_limit, snippet_limit + 4),
        )

        callee_matched_snippets = []
        other_snippets = []

        for sn in expanded_snippet_evidence:
            symbol_name = str(sn.get("symbol", "") or sn.get("anchor", "") or "")
            short_symbol = symbol_name.split(".")[-1]

            if short_symbol in candidate_callees or symbol_name in candidate_callees:
                callee_matched_snippets.append(sn)
            else:
                other_snippets.append(sn)

        expanded_snippet_evidence = callee_matched_snippets + other_snippets

        merged = self.merge_with_previous(
            RetrievalBundle(
                file_evidence=file_evidence,
                symbol_evidence=expanded_symbol_evidence,
                snippet_evidence=expanded_snippet_evidence,
            ),
            RetrievalBundle(
                file_evidence=file_evidence,
                symbol_evidence=symbol_evidence,
                snippet_evidence=snippet_evidence,
            ),
            max_files=max(effective_file_limit, file_limit),
            max_symbols=max(effective_symbol_limit, symbol_limit + 4),
            max_snippets=max(effective_snippet_limit, snippet_limit + 4),
        )

        file_evidence = merged.file_evidence
        symbol_evidence = merged.symbol_evidence
        snippet_evidence = merged.snippet_evidence

    section_file_evidence: list[EvidenceItem] = []

    for section_name in section_priority:
        if section_name == "packaging_metadata":
            section_file_evidence.extend(
                self._retrieve_packaging_metadata(question)
            )
        elif section_name == "documentation_intent":
            section_file_evidence.extend(
                self._retrieve_documentation_intent(question)
            )

    if section_file_evidence:
        file_evidence = (section_file_evidence + file_evidence)[:effective_file_limit]

    return RetrievalBundle(
        file_evidence=file_evidence,
        symbol_evidence=symbol_evidence,
        snippet_evidence=snippet_evidence,
    )

Key changes:

    Added elif intents["explain_chain"]: and elif intents["explanatory"]: branches in the query_kind assignment.

    This ensures that questions like "explain the startup chain" or "describe the architecture" get a section_priority tailored to explanation or chain questions (if get_section_priority supports those keys).

    All other logic remains unchanged.

If get_section_priority does not yet handle "explain_chain" or "explanatory", you should update that function in .core accordingly (e.g., return a priority list that includes packaging/documentation sections when appropriate).
def _build_runtime_anchor_snippets(self, question: str, file_evidence: list[EvidenceItem], limit: int):
    file_cache: dict[str, str] = {}

    def _get_file_text(abs_path: str) -> str:
        if abs_path not in file_cache:
            file_cache[abs_path] = safe_read_text(abs_path)
        return file_cache[abs_path]

    # Inside loops, use _get_file_text(abs_path) instead of safe_read_text

update 


    def _build_runtime_anchor_snippets(
            self,
            question: str,
            file_evidence: list[EvidenceItem],
            limit: int,
    ) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        seen: set[tuple[str, int, str]] = set()
        question_low = norm_text(question)

        def _dedupe_keep_order(values: list[str]) -> list[str]:
            out_values: list[str] = []
            seen_values: set[str] = set()

            for value in values:
                value = str(value or "").strip()
                if not value:
                    continue

                key = value.lower()
                if key in seen_values:
                    continue

                seen_values.add(key)
                out_values.append(value)

            return out_values

        def _candidate_terms_for_anchor(anchor: str) -> list[str]:
            anchor_low = norm_text(anchor)
            candidates: list[str] = [anchor]

            alias_map = {
                "runtime_runner_probe_apply_button": [
                    "runtime_runner_probe_apply_button",
                    "on_apply_clicked",
                    "apply_button",
                    "apply",
                    "probe",
                ],
                "runtime_runner_probe_line_edit": [
                    "runtime_runner_probe_line_edit",
                    "on_text_changed",
                    "line_edit",
                    "text_changed",
                    "probe",
                ],
                "runtime_runner_probe_close_button": [
                    "runtime_runner_probe_close_button",
                    "on_close_clicked",
                    "close_button",
                    "close",
                    "probe",
                ],
                "on_apply_clicked": [
                    "on_apply_clicked",
                    "apply_clicked",
                    "apply",
                    "probe",
                ],
                "on_text_changed": [
                    "on_text_changed",
                    "text_changed",
                    "line_edit",
                    "probe",
                ],
                "on_close_clicked": [
                    "on_close_clicked",
                    "close_clicked",
                    "close",
                    "probe",
                ],
            }

            candidates.extend(alias_map.get(anchor_low, []))

            if anchor_low.startswith("runtime_runner_probe_"):
                trimmed = anchor_low.replace("runtime_runner_probe_", "")
                candidates.append(trimmed)
                candidates.append(trimmed.replace("_button", ""))
                candidates.append(trimmed.replace("_line_edit", ""))
                candidates.append(trimmed.replace("_close_button", ""))

            if "apply" in question_low:
                candidates.extend(["on_apply_clicked", "apply", "probe"])
            if "text" in question_low:
                candidates.extend(["on_text_changed", "text_changed", "probe"])
            if "close" in question_low:
                candidates.extend(["on_close_clicked", "close", "probe"])
            if "button" in question_low:
                candidates.extend(["button", "clicked", "probe"])

            return _dedupe_keep_order(candidates)

        def _fallback_line(abs_path: str) -> int:
            try:
                text = safe_read_text(abs_path)
            except Exception:
                return 1

            lines = text.splitlines()

            preferred_tokens = [
                "on_apply_clicked",
                "on_text_changed",
                "on_close_clicked",
                "clicked.connect",
                "qpushbutton",
                "qlineedit",
                "probe",
            ]

            for idx, line in enumerate(lines, start=1):
                low = line.lower()
                if any(token in low for token in preferred_tokens):
                    return idx

            for idx, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith("def ") or stripped.startswith("class "):
                    return idx

            return 1

        for item in file_evidence[:8]:
            logical_path = item.path
            resolved_rel_path, abs_path = self._resolve_existing_project_file_path(logical_path)
            if not resolved_rel_path or not abs_path:
                continue

            detail_text = str(item.detail or "")
            if "Runtime anchors:" not in detail_text and "Runtime context:" not in detail_text:
                continue

            anchors = self._extract_runtime_anchors_from_detail(detail_text)
            if not anchors:
                anchors, _previews = self._get_runtime_anchor_summary(logical_path, limit=12)

            ranked_anchors = sorted(
                anchors,
                key=lambda anchor: self._score_runtime_anchor_for_question(question, anchor),
                reverse=True,
            )

            found_for_file = False

            for anchor in ranked_anchors:
                for candidate_term in _candidate_terms_for_anchor(anchor):
                    line = self._find_anchor_line_in_file(abs_path, candidate_term)
                    if line is None:
                        continue

                    key = (resolved_rel_path, line, candidate_term)
                    if key in seen:
                        continue
                    seen.add(key)

                    out.append(
                        {
                            "path": resolved_rel_path,
                            "line": line,
                            "anchor": candidate_term,
                            "text": self._read_snippet(abs_path, line, radius=18),
                        }
                    )
                    found_for_file = True

                    if len(out) >= limit:
                        return out

                    break

            if not found_for_file:
                line = _fallback_line(abs_path)
                key = (resolved_rel_path, line, "runtime-file-fallback")
                if key not in seen:
                    seen.add(key)
                    out.append(
                        {
                            "path": resolved_rel_path,
                            "line": line,
                            "anchor": "runtime-file-fallback",
                            "text": self._read_snippet(abs_path, line, radius=18),
                        }
                    )

                    if len(out) >= limit:
                        return out

        return out

We need to update _build_runtime_anchor_snippets to add file caching to avoid redundant reads. The current implementation calls _find_anchor_line_in_file (which reads the file) and _read_snippet (which also reads the file). Also _fallback_line reads the file. We'll introduce a cache for file contents.

We'll modify the method to use a local file_cache dict and a helper _get_file_text. Then replace calls to safe_read_text (indirectly through _find_anchor_line_in_file and _read_snippet and _fallback_line) with cached reads. However, _find_anchor_line_in_file currently reads the file; we can replace it with a version that uses cached content. Similarly for _read_snippet and _fallback_line.

We'll create a closure that uses the cache. Since _find_anchor_line_in_file and _read_snippet are methods, we can either override them locally or just inline the logic. Simpler: inside _build_runtime_anchor_snippets, define a function _get_cached_text and then re-implement line search and snippet extraction using that cached text.

We'll keep the original methods for other uses but override behavior in this method.

Here's the updated code:
python

def _build_runtime_anchor_snippets(
        self,
        question: str,
        file_evidence: list[EvidenceItem],
        limit: int,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    question_low = norm_text(question)
    
    # Cache for file contents to avoid multiple reads
    file_cache: dict[str, str] = {}
    
    def _get_file_text(abs_path: str) -> str:
        if abs_path not in file_cache:
            file_cache[abs_path] = safe_read_text(abs_path)
        return file_cache[abs_path]
    
    def _find_anchor_line_cached(abs_path: str, anchor: str) -> int | None:
        try:
            text = _get_file_text(abs_path)
        except Exception:
            return None
        lines = text.splitlines()
        anchor_low = anchor.lower()
        for idx, line in enumerate(lines, start=1):
            if anchor_low in line.lower():
                return idx
        return None
    
    def _read_snippet_cached(abs_path: str, line: int, radius: int) -> str:
        text = _get_file_text(abs_path)
        lines = text.splitlines()
        if not lines:
            return ""
        start = max(1, line - radius)
        end = min(len(lines), line + radius)
        out_lines: list[str] = []
        for idx in range(start, end + 1):
            out_lines.append(str(idx).rjust(5) + " | " + lines[idx - 1])
        return "\n".join(out_lines)
    
    def _fallback_line_cached(abs_path: str) -> int:
        try:
            text = _get_file_text(abs_path)
        except Exception:
            return 1
        lines = text.splitlines()
        preferred_tokens = [
            "on_apply_clicked",
            "on_text_changed",
            "on_close_clicked",
            "clicked.connect",
            "qpushbutton",
            "qlineedit",
            "probe",
        ]
        for idx, line in enumerate(lines, start=1):
            low = line.lower()
            if any(token in low for token in preferred_tokens):
                return idx
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("def ") or stripped.startswith("class "):
                return idx
        return 1

    def _dedupe_keep_order(values: list[str]) -> list[str]:
        out_values: list[str] = []
        seen_values: set[str] = set()
        for value in values:
            value = str(value or "").strip()
            if not value:
                continue
            key = value.lower()
            if key in seen_values:
                continue
            seen_values.add(key)
            out_values.append(value)
        return out_values

    def _candidate_terms_for_anchor(anchor: str) -> list[str]:
        anchor_low = norm_text(anchor)
        candidates: list[str] = [anchor]
        alias_map = {
            "runtime_runner_probe_apply_button": [
                "runtime_runner_probe_apply_button",
                "on_apply_clicked",
                "apply_button",
                "apply",
                "probe",
            ],
            "runtime_runner_probe_line_edit": [
                "runtime_runner_probe_line_edit",
                "on_text_changed",
                "line_edit",
                "text_changed",
                "probe",
            ],
            "runtime_runner_probe_close_button": [
                "runtime_runner_probe_close_button",
                "on_close_clicked",
                "close_button",
                "close",
                "probe",
            ],
            "on_apply_clicked": [
                "on_apply_clicked",
                "apply_clicked",
                "apply",
                "probe",
            ],
            "on_text_changed": [
                "on_text_changed",
                "text_changed",
                "line_edit",
                "probe",
            ],
            "on_close_clicked": [
                "on_close_clicked",
                "close_clicked",
                "close",
                "probe",
            ],
        }
        candidates.extend(alias_map.get(anchor_low, []))
        if anchor_low.startswith("runtime_runner_probe_"):
            trimmed = anchor_low.replace("runtime_runner_probe_", "")
            candidates.append(trimmed)
            candidates.append(trimmed.replace("_button", ""))
            candidates.append(trimmed.replace("_line_edit", ""))
            candidates.append(trimmed.replace("_close_button", ""))
        if "apply" in question_low:
            candidates.extend(["on_apply_clicked", "apply", "probe"])
        if "text" in question_low:
            candidates.extend(["on_text_changed", "text_changed", "probe"])
        if "close" in question_low:
            candidates.extend(["on_close_clicked", "close", "probe"])
        if "button" in question_low:
            candidates.extend(["button", "clicked", "probe"])
        return _dedupe_keep_order(candidates)

    for item in file_evidence[:8]:
        logical_path = item.path
        resolved_rel_path, abs_path = self._resolve_existing_project_file_path(logical_path)
        if not resolved_rel_path or not abs_path:
            continue

        detail_text = str(item.detail or "")
        if "Runtime anchors:" not in detail_text and "Runtime context:" not in detail_text:
            continue

        anchors = self._extract_runtime_anchors_from_detail(detail_text)
        if not anchors:
            anchors, _previews = self._get_runtime_anchor_summary(logical_path, limit=12)

        ranked_anchors = sorted(
            anchors,
            key=lambda anchor: self._score_runtime_anchor_for_question(question, anchor),
            reverse=True,
        )

        found_for_file = False

        for anchor in ranked_anchors:
            for candidate_term in _candidate_terms_for_anchor(anchor):
                line = _find_anchor_line_cached(abs_path, candidate_term)
                if line is None:
                    continue

                key = (resolved_rel_path, line, candidate_term)
                if key in seen:
                    continue
                seen.add(key)

                out.append(
                    {
                        "path": resolved_rel_path,
                        "line": line,
                        "anchor": candidate_term,
                        "text": _read_snippet_cached(abs_path, line, radius=18),
                    }
                )
                found_for_file = True

                if len(out) >= limit:
                    return out

                break

        if not found_for_file:
            line = _fallback_line_cached(abs_path)
            key = (resolved_rel_path, line, "runtime-file-fallback")
            if key not in seen:
                seen.add(key)
                out.append(
                    {
                        "path": resolved_rel_path,
                        "line": line,
                        "anchor": "runtime-file-fallback",
                        "text": _read_snippet_cached(abs_path, line, radius=18),
                    }
                )

                if len(out) >= limit:
                    return out

    return out

Key changes:

    Added file_cache dict and _get_file_text helper.

    Replaced self._find_anchor_line_in_file with _find_anchor_line_cached that uses cached text.

    Replaced self._read_snippet with _read_snippet_cached.

    Replaced _fallback_line with _fallback_line_cached.

    All file reads now go through the cache, eliminating redundant I/O.

Here's the updated _build_runtime_anchor_snippets method with file caching to avoid redundant reads:
python

def _build_runtime_anchor_snippets(
        self,
        question: str,
        file_evidence: list[EvidenceItem],
        limit: int,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    question_low = norm_text(question)

    # Cache for file contents to avoid multiple reads
    file_cache: dict[str, str] = {}

    def _get_file_text(abs_path: str) -> str:
        if abs_path not in file_cache:
            file_cache[abs_path] = safe_read_text(abs_path)
        return file_cache[abs_path]

    def _find_anchor_line_cached(abs_path: str, anchor: str) -> int | None:
        try:
            text = _get_file_text(abs_path)
        except Exception:
            return None
        lines = text.splitlines()
        anchor_low = anchor.lower()
        for idx, line in enumerate(lines, start=1):
            if anchor_low in line.lower():
                return idx
        return None

    def _read_snippet_cached(abs_path: str, line: int, radius: int) -> str:
        text = _get_file_text(abs_path)
        lines = text.splitlines()
        if not lines:
            return ""
        start = max(1, line - radius)
        end = min(len(lines), line + radius)
        snippet_lines: list[str] = []
        for idx in range(start, end + 1):
            snippet_lines.append(str(idx).rjust(5) + " | " + lines[idx - 1])
        return "\n".join(snippet_lines)

    def _fallback_line_cached(abs_path: str) -> int:
        try:
            text = _get_file_text(abs_path)
        except Exception:
            return 1
        lines = text.splitlines()
        preferred_tokens = [
            "on_apply_clicked",
            "on_text_changed",
            "on_close_clicked",
            "clicked.connect",
            "qpushbutton",
            "qlineedit",
            "probe",
        ]
        for idx, line in enumerate(lines, start=1):
            low = line.lower()
            if any(token in low for token in preferred_tokens):
                return idx
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("def ") or stripped.startswith("class "):
                return idx
        return 1

    def _dedupe_keep_order(values: list[str]) -> list[str]:
        out_values: list[str] = []
        seen_values: set[str] = set()
        for value in values:
            value = str(value or "").strip()
            if not value:
                continue
            key = value.lower()
            if key in seen_values:
                continue
            seen_values.add(key)
            out_values.append(value)
        return out_values

    def _candidate_terms_for_anchor(anchor: str) -> list[str]:
        anchor_low = norm_text(anchor)
        candidates: list[str] = [anchor]

        alias_map = {
            "runtime_runner_probe_apply_button": [
                "runtime_runner_probe_apply_button",
                "on_apply_clicked",
                "apply_button",
                "apply",
                "probe",
            ],
            "runtime_runner_probe_line_edit": [
                "runtime_runner_probe_line_edit",
                "on_text_changed",
                "line_edit",
                "text_changed",
                "probe",
            ],
            "runtime_runner_probe_close_button": [
                "runtime_runner_probe_close_button",
                "on_close_clicked",
                "close_button",
                "close",
                "probe",
            ],
            "on_apply_clicked": [
                "on_apply_clicked",
                "apply_clicked",
                "apply",
                "probe",
            ],
            "on_text_changed": [
                "on_text_changed",
                "text_changed",
                "line_edit",
                "probe",
            ],
            "on_close_clicked": [
                "on_close_clicked",
                "close_clicked",
                "close",
                "probe",
            ],
        }

        candidates.extend(alias_map.get(anchor_low, []))

        if anchor_low.startswith("runtime_runner_probe_"):
            trimmed = anchor_low.replace("runtime_runner_probe_", "")
            candidates.append(trimmed)
            candidates.append(trimmed.replace("_button", ""))
            candidates.append(trimmed.replace("_line_edit", ""))
            candidates.append(trimmed.replace("_close_button", ""))

        if "apply" in question_low:
            candidates.extend(["on_apply_clicked", "apply", "probe"])
        if "text" in question_low:
            candidates.extend(["on_text_changed", "text_changed", "probe"])
        if "close" in question_low:
            candidates.extend(["on_close_clicked", "close", "probe"])
        if "button" in question_low:
            candidates.extend(["button", "clicked", "probe"])

        return _dedupe_keep_order(candidates)

    for item in file_evidence[:8]:
        logical_path = item.path
        resolved_rel_path, abs_path = self._resolve_existing_project_file_path(logical_path)
        if not resolved_rel_path or not abs_path:
            continue

        detail_text = str(item.detail or "")
        if "Runtime anchors:" not in detail_text and "Runtime context:" not in detail_text:
            continue

        anchors = self._extract_runtime_anchors_from_detail(detail_text)
        if not anchors:
            anchors, _previews = self._get_runtime_anchor_summary(logical_path, limit=12)

        ranked_anchors = sorted(
            anchors,
            key=lambda anchor: self._score_runtime_anchor_for_question(question, anchor),
            reverse=True,
        )

        found_for_file = False

        for anchor in ranked_anchors:
            for candidate_term in _candidate_terms_for_anchor(anchor):
                line = _find_anchor_line_cached(abs_path, candidate_term)
                if line is None:
                    continue

                key = (resolved_rel_path, line, candidate_term)
                if key in seen:
                    continue
                seen.add(key)

                out.append(
                    {
                        "path": resolved_rel_path,
                        "line": line,
                        "anchor": candidate_term,
                        "text": _read_snippet_cached(abs_path, line, radius=18),
                    }
                )
                found_for_file = True

                if len(out) >= limit:
                    return out

                break

        if not found_for_file:
            line = _fallback_line_cached(abs_path)
            key = (resolved_rel_path, line, "runtime-file-fallback")
            if key not in seen:
                seen.add(key)
                out.append(
                    {
                        "path": resolved_rel_path,
                        "line": line,
                        "anchor": "runtime-file-fallback",
                        "text": _read_snippet_cached(abs_path, line, radius=18),
                    }
                )

                if len(out) >= limit:
                    return out

    return out

Key improvements:

    Added file_cache dictionary to store file contents once per call.

    Replaced _find_anchor_line_in_file with _find_anchor_line_cached that uses cached text.

    Replaced self._read_snippet with _read_snippet_cached.

    Replaced _fallback_line with _fallback_line_cached.

    All file reads now go through _get_file_text, eliminating redundant I/O when the same file is accessed multiple times (e.g., for multiple anchors or fallback).

update

def _is_safe_path(self, logical_path: str) -> bool:
    try:
        full = os.path.realpath(os.path.join(self.idx.project_root, logical_path))
        root = os.path.realpath(self.idx.project_root)
        return full.startswith(root)
    except OSError:
        return False

    def _resolve_existing_project_file_path(self, logical_path: str) -> tuple[str, str] | tuple[None, None]:
        logical_path = str(logical_path or "").strip()
        if not logical_path:
            return None, None

        direct_abs = os.path.join(self.idx.project_root, logical_path)
        if os.path.exists(direct_abs):
            return logical_path, direct_abs

        logical_low = logical_path.replace("\\", "/").lower().strip("/")
        logical_base = os.path.basename(logical_low)

        candidate_sources: set[str] = set()

        candidate_sources.update(
            str(path).replace("\\", "/").strip()
            for path in self.idx.files_by_path.keys()
        )
        candidate_sources.update(
            str(path).replace("\\", "/").strip()
            for path in self.idx.runtime_events_by_file.keys()
        )

        exact_matches: list[str] = []
        basename_matches: list[str] = []

        for known_path in sorted(candidate_sources):
            known_low = known_path.lower().strip("/")

            abs_known = os.path.join(self.idx.project_root, known_path)
            if os.path.exists(abs_known):
                if known_low == logical_low:
                    exact_matches.append(known_path)
                    continue

                if os.path.basename(known_low) == logical_base:
                    basename_matches.append(known_path)

        candidates = exact_matches if exact_matches else basename_matches

        if not candidates:
            disk_matches: list[str] = []
            for root, _dirs, files in os.walk(self.idx.project_root):
                for file_name in files:
                    if file_name.lower() != logical_base:
                        continue

                    abs_found = os.path.join(root, file_name)
                    rel_found = os.path.relpath(abs_found, self.idx.project_root).replace("\\", "/")
                    disk_matches.append(rel_found)

            candidates = disk_matches

        if not candidates:
            return None, None

        def rank_candidate(path: str) -> tuple[int, str]:
            low = path.replace("\\", "/").lower()
            score = 0

            if "reasoner_runtime_collector" in low:
                score += 500
            if "/runtime_collector/" in low:
                score += 400
            if low.endswith("/runtime_runner.py"):
                score += 300
            if "runtime" in low:
                score += 120
            if "collector" in low:
                score += 100
            if "scenario" in low:
                score += 60

            return score, path

        rel_path = max(candidates, key=rank_candidate)
        return rel_path, os.path.join(self.idx.project_root, rel_path)

We need to update the _resolve_existing_project_file_path method to use the _is_safe_path method for security. The user provided a partial snippet showing the _is_safe_path method but not the full context. We need to integrate the safety check into the resolution process.

We should add a call to _is_safe_path before returning any resolved path. The method currently returns a tuple of (relative_path, absolute_path). We should ensure that both paths are safe (i.e., they reside within the project root). The _is_safe_path method takes a logical_path (relative) and checks if the resolved absolute path is under the project root.

We'll modify _resolve_existing_project_file_path to validate the final candidate paths. Also, we need to ensure that _is_safe_path is defined as a method of the class (likely ProjectRetriever). Since the user showed it as def _is_safe_path(self, logical_path: str) -> bool:, we'll assume it's part of the class.

We'll update the method as follows:

    After determining rel_path and constructing abs_path, call self._is_safe_path(rel_path) (or self._is_safe_path(logical_path) for the direct case). If unsafe, skip and try other candidates or return None.

    Also for the direct case, validate the path before returning.

Also note: The direct case uses logical_path directly; we should validate that too.

We'll produce the updated method with safety checks.

Here is the updated _resolve_existing_project_file_path method with path safety validation integrated:
python

def _resolve_existing_project_file_path(self, logical_path: str) -> tuple[str, str] | tuple[None, None]:
    logical_path = str(logical_path or "").strip()
    if not logical_path:
        return None, None

    # Helper to validate a candidate relative path
    def _is_candidate_safe(rel_candidate: str) -> bool:
        try:
            full = os.path.realpath(os.path.join(self.idx.project_root, rel_candidate))
            root = os.path.realpath(self.idx.project_root)
            return full.startswith(root)
        except OSError:
            return False

    # Direct exact match
    direct_abs = os.path.join(self.idx.project_root, logical_path)
    if os.path.exists(direct_abs) and _is_candidate_safe(logical_path):
        return logical_path, direct_abs

    logical_low = logical_path.replace("\\", "/").lower().strip("/")
    logical_base = os.path.basename(logical_low)

    candidate_sources: set[str] = set()

    candidate_sources.update(
        str(path).replace("\\", "/").strip()
        for path in self.idx.files_by_path.keys()
    )
    candidate_sources.update(
        str(path).replace("\\", "/").strip()
        for path in self.idx.runtime_events_by_file.keys()
    )

    exact_matches: list[str] = []
    basename_matches: list[str] = []

    for known_path in sorted(candidate_sources):
        known_low = known_path.lower().strip("/")
        abs_known = os.path.join(self.idx.project_root, known_path)
        if os.path.exists(abs_known):
            if known_low == logical_low:
                exact_matches.append(known_path)
                continue
            if os.path.basename(known_low) == logical_base:
                basename_matches.append(known_path)

    candidates = exact_matches if exact_matches else basename_matches

    if not candidates:
        disk_matches: list[str] = []
        for root, _dirs, files in os.walk(self.idx.project_root):
            for file_name in files:
                if file_name.lower() != logical_base:
                    continue
                abs_found = os.path.join(root, file_name)
                rel_found = os.path.relpath(abs_found, self.idx.project_root).replace("\\", "/")
                disk_matches.append(rel_found)
        candidates = disk_matches

    if not candidates:
        return None, None

    def rank_candidate(path: str) -> tuple[int, str]:
        low = path.replace("\\", "/").lower()
        score = 0
        if "reasoner_runtime_collector" in low:
            score += 500
        if "/runtime_collector/" in low:
            score += 400
        if low.endswith("/runtime_runner.py"):
            score += 300
        if "runtime" in low:
            score += 120
        if "collector" in low:
            score += 100
        if "scenario" in low:
            score += 60
        return score, path

    # Filter candidates to only those that are safe
    safe_candidates = [c for c in candidates if _is_candidate_safe(c)]
    if not safe_candidates:
        return None, None

    rel_path = max(safe_candidates, key=rank_candidate)
    abs_path = os.path.join(self.idx.project_root, rel_path)
    return rel_path, abs_path

Key changes:

    Added an inner helper _is_candidate_safe that checks if a relative path resolves to a location under the project root.

    For the direct exact match, validate safety before returning.

    When building the list of candidates, filter them through _is_candidate_safe before ranking.

    If no safe candidates remain, return None, None.

    This prevents path traversal attacks and ensures only files inside the project root are ever returned.

Note: The _is_safe_path method shown in the user's snippet is not used directly because it only accepts logical_path; the inner helper does the same job but with the current logical_path variable. If you prefer to reuse a class method, you can replace the inner helper with a call to self._is_safe_path(candidate) after ensuring the method exists and behaves identically.
