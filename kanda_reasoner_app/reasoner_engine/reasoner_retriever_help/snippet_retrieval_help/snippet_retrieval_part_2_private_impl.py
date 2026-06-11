"""Private snippet retrieval helper implementation part 2."""

from __future__ import annotations

__all__ = []


def _bind_root_globals(root_globals):
    skipped = {
        '__name__',
        '__package__',
        '__loader__',
        '__spec__',
        '__file__',
        '__cached__',
        '__builtins__',
    }
    for name, value in root_globals.items():
        if name not in skipped and name not in globals():
            globals()[name] = value


def _sr_retrieve_snippets_impl(
    retriever,
    question: str,
    file_evidence: list[EvidenceItem],
    symbol_evidence: list[SymbolEvidenceItem],
    limit: int,
) -> list[dict[str, Any]]:
    q = norm_text(question)

    reset_runtime_query = is_runtime_heavy_question(q) and (
        "reset" in q
        or "close" in q
        or "disconnect" in q
        or "timer" in q
        or "signal" in q
    )

    which_calls_query = detect_query_intents(norm_text(question))["which_calls"]

    exact_call_targets = []
    if which_calls_query:
        for token in tokenize_query(q):
            if ("_" in token or "." in token) and len(token) >= 6:
                for sym in retriever.idx.symbol_details.keys():
                    sym_tail = sym.split(".")[-1].lower()
                    if token == sym.lower() or token == sym_tail:
                        exact_call_targets.append(token)
                        break

    if which_calls_query:
        print(
            "[SNIPPET CALLSITE DEBUG]",
            {
                "question": question,
                "which_calls_query": which_calls_query,
                "exact_call_targets": exact_call_targets,
            },
        )

    snippets: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()

    snippets_by_file = getattr(retriever.idx, "snippets_by_file", {})

    if snippets_by_file:
        if which_calls_query and exact_call_targets:
            preferred_paths = {
                item.path
                for item in file_evidence
                if is_allowed_project_path(item.path)
            }

            for path in sorted(preferred_paths or snippets_by_file.keys()):
                if not is_allowed_project_path(path):
                    continue

                candidates = snippets_by_file.get(path, [])
                if not candidates:
                    continue

                for rec in candidates:
                    line = int(rec.get("line", 1) or 1)
                    symbol_name = str(rec.get("symbol_name", "") or "").strip()
                    symbol_tail = symbol_name.split(".")[-1].strip().lower()
                    text = str(rec.get("snippet", "") or "").rstrip()
                    if not text:
                        continue

                    text_norm = text.lower()

                    matched_target = None
                    for target in exact_call_targets:
                        target_tail = target.split(".")[-1].lower()

                        is_definition = f"def {target_tail}(" in text_norm
                        has_direct_call = f"{target_tail}(" in text_norm

                        has_symbol_reference = re.search(
                            rf"\b{re.escape(target_tail)}\b",
                            text_norm,
                        ) is not None

                        has_callback_reference = has_symbol_reference and any(
                            marker in text_norm
                            for marker in [
                                f".{target_tail}",
                                f" {target_tail},",
                                f" {target_tail})",
                                ".connect",
                                "set_close_action",
                                "signal",
                                "slot",
                                "handler",
                                "callback",
                            ]
                        )

                        if (
                                (has_direct_call or has_callback_reference)
                                and not is_definition
                                and symbol_tail != target_tail
                        ):
                            matched_target = target_tail
                            break



                    if matched_target:
                        print(
                            "[SNIPPET CALLSITE MATCH]",
                            {
                                "path": path,
                                "line": line,
                                "symbol_name": symbol_name,
                                "matched_target": matched_target,
                            },
                        )

                    if not matched_target:
                        continue

                    key = (path, line, symbol_name or matched_target)
                    if key in seen:
                        continue

                    seen.add(key)
                    snippets.append(
                        {
                            "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                            "path": path,
                            "line": line,
                            "anchor": symbol_name or matched_target,
                            "text": text,
                        }
                    )

                    if len(snippets) >= limit:
                        return snippets

        if which_calls_query and snippets:
            return snippets

        signal_connection_query = (
            "signal connection" in q
            or "signal connections" in q
            or "signal-slot" in q
            or "slot" in q
            or "connect" in q
            or "handler" in q
            or "callback" in q
        )

        if signal_connection_query:
            preferred_paths = [
                item.path
                for item in file_evidence[:5]
                if is_allowed_project_path(item.path)
            ]

            exact_signal_targets: list[str] = []
            for token in tokenize_query(q):
                if ("_" in token or "." in token) and len(token) >= 6:
                    exact_signal_targets.append(token.lower())

            wiring_markers = [
                ".connect(",
                ".clicked.connect",
                ".triggered.connect",
                "set_close_action(",
                "set_open_action(",
                "set_apply_action(",
                "_wire_",
            ]

            for path in preferred_paths:
                candidates = snippets_by_file.get(path, [])
                if not candidates:
                    continue

                for rec in candidates:
                    line = int(rec.get("line", 1) or 1)
                    symbol_name = str(rec.get("symbol_name", "") or "").strip()
                    text = str(rec.get("snippet", "") or "").rstrip()
                    if not text:
                        continue

                    text_norm = text.lower()
                    symbol_norm = symbol_name.lower()

                    if not any(marker in text_norm or marker in symbol_norm for marker in wiring_markers):
                        continue

                    if exact_signal_targets:
                        target_hit = False
                        for target in exact_signal_targets:
                            target_tail = target.split(".")[-1]
                            if (
                                target_tail in text_norm
                                or f".{target_tail}" in text_norm
                                or target_tail in symbol_norm
                            ):
                                target_hit = True
                                break
                        if not target_hit:
                            continue

                    key = (path, line, symbol_name or "signal-connection")
                    if key in seen:
                        continue

                    seen.add(key)
                    snippets.append(
                        {
                            "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                            "path": path,
                            "line": line,
                            "anchor": symbol_name or "signal-connection",
                            "text": text,
                        }
                    )

                    if len(snippets) >= limit:
                        return snippets

            if snippets:
                return snippets


        for item in symbol_evidence:
            if not is_allowed_project_path(item.path):
                continue

            candidates = snippets_by_file.get(item.path, [])
            if not candidates:
                continue

            symbol_full = str(item.symbol_name or "").strip()
            symbol_tail = symbol_full.split(".")[-1].strip().lower()

            path_norm = norm_text(item.path)
            symbol_norm = norm_text(symbol_full)

            if reset_runtime_query:
                generic_startup_signal_symbol = (
                    "init_signals" in symbol_norm or "signalmanager" in symbol_norm
                )
                generic_startup_signal_path = path_norm.endswith(
                    "shell/viewer/eeg_signal_manager.py"
                )
                explicit_reset_runtime_symbol = (
                    "on_close_clicked" in symbol_norm
                    or "eeg_visu_reset_snpsht" in symbol_norm
                    or "reset_to_initial_eeg_state" in symbol_norm
                    or "disconnect" in symbol_norm
                    or "stop" in symbol_norm
                )

                if (
                    generic_startup_signal_symbol or generic_startup_signal_path
                ) and not explicit_reset_runtime_symbol:
                    continue

            preferred = [
                rec
                for rec in candidates
                if str(rec.get("symbol_name", "")).strip().lower()
                == symbol_full.lower()
                or str(rec.get("symbol_name", "")).split(".")[-1].strip().lower()
                == symbol_tail
            ]

            selected_candidates = preferred if preferred else candidates

            for rec in selected_candidates:
                line = int(rec.get("line", 1) or 1)
                key = (item.path, line, symbol_full)
                if key in seen:
                    continue

                text = str(rec.get("snippet", "") or "").rstrip()
                if not text:
                    continue

                seen.add(key)
                snippets.append(
                    {
                        "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                        "path": item.path,
                        "line": line,
                        "anchor": symbol_full or str(rec.get("symbol_name", "")),
                        "text": text,
                    }
                )

                if len(snippets) >= limit:
                    return snippets

    intents = detect_query_intents(q)

    runtime_first = (
        intents["runtime_heavy"]
        and ("runtime" in q or "probe" in q or "signal" in q or "slot" in q)
    )

    if runtime_first:
        runtime_snippets = retriever._build_runtime_anchor_snippets(
            question,
            file_evidence,
            limit=limit,
        )

        for item in runtime_snippets:
            key = (
                str(item.get("path", "")),
                int(item.get("line", 0)),
                str(item.get("anchor", "")),
            )
            if key in seen:
                continue
            seen.add(key)

            snippets.append(
                {
                    "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                    "path": item["path"],
                    "line": item["line"],
                    "anchor": item["anchor"],
                    "text": item["text"],
                }
            )

            if len(snippets) >= limit:
                return snippets

    for item in symbol_evidence:
        if not is_allowed_project_path(item.path):
            continue

        resolved_rel_path, abs_path = retriever._resolve_existing_project_file_path(
            item.path
        )
        if not resolved_rel_path or not abs_path:
            continue

        key = (resolved_rel_path, item.line, item.symbol_name)
        if key in seen:
            continue
        seen.add(key)

        radius = 20
        anchor_low = str(item.symbol_name).lower()
        if any(
            term in anchor_low
            for term in ["topomap", "draw", "render", "plot", "topography"]
        ):
            radius = 28

        snippet_text = retriever._read_snippet(abs_path, item.line, radius=radius)

        snippets.append(
            {
                "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                "path": resolved_rel_path,
                "line": item.line,
                "anchor": item.symbol_name,
                "text": snippet_text,
            }
        )

        if len(snippets) >= limit:
            return snippets

    for item in file_evidence:
        if not is_allowed_project_path(item.path):
            continue

        resolved_rel_path, abs_path = retriever._resolve_existing_project_file_path(
            item.path
        )
        if not resolved_rel_path or not abs_path:
            continue

        key = (resolved_rel_path, 1, "file-start")
        if key in seen:
            continue
        seen.add(key)

        snippet_text = retriever._read_snippet(abs_path, 1, radius=40)

        snippets.append(
            {
                "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                "path": resolved_rel_path,
                "line": 1,
                "anchor": "file-start",
                "text": snippet_text,
            }
        )

        if len(snippets) >= limit:
            return snippets

    return snippets
