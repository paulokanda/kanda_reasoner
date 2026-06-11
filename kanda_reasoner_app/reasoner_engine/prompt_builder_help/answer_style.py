"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from .prompt_classification import (
    is_chain_or_flow_question,
    is_code_localized_explanation_question,
    is_explain_implementation_question,
    is_which_method_calls_question,
    norm_text,
)

__all__ = ["build_answer_style_instructions"]


def build_answer_style_instructions(question: str, prefer_code: bool) -> str:
    q = norm_text(question)

    calibration = (
        "Use evidence-calibrated wording such as 'the retrieved snippets show', "
        "'appears to be orchestrated by', 'is delegated to', 'is supported by', "
        "or 'seems to' when the relationship is inferred.\n"
        "Use stronger wording only when the link is directly shown by evidence.\n"
        "Do not present inferred transitions as certain facts unless explicitly shown.\n"
        "Do not claim that something does not happen unless the evidence explicitly shows its absence; "
        "otherwise say that it is 'not shown in the provided evidence'.\n"
    )

    code_excerpt_rules = (
        "You must include real code excerpts when relevant SOURCE SNIPPETS exist.\n"
        "When code is shown, copy it only from SOURCE SNIPPETS.\n"
        "Never quote prompt instructions, answer-style instructions, or validator guidance as if they were source code.\n"
        "Only use text as a code excerpt when it comes from a real SOURCE SNIPPET tied to a file path and symbol or anchor.\n"
        "If the retrieved text is instructional or meta text rather than source code, describe it in prose and do not place it in a code block.\n"
        "Do not invent code, reconstruct missing code, or synthesize pseudo-code.\n"
        "Never output a code block for a function unless that exact function body is present in SOURCE SNIPPETS.\n"
        "If a helper is supported only by file-level evidence, describe it in prose only.\n"
        "Do not synthesize placeholder code, representative code, or reconstructed code.\n"
        "Show at least 2 short real code excerpts when the evidence pack contains them.\n"
    )

    chain_evidence_rules = (
        "Every reported step in the flow must include at least one concrete evidence anchor.\n"
        "If a step has no SOURCE SNIPPET, mark it explicitly as 'file-level evidence only' "
        "and do not present it as equally strong as snippet-backed steps.\n"
        "Do not reuse the previous step's anchor for a different symbol.\n"
        "For each handoff step, prefer one short snippet showing either the call site or the callee body.\n"
        "Do not treat an import statement as proof that the imported function is called.\n"
        "If a snippet only shows an import, label the relationship as 'imported helper' "
        "or 'handoff candidate', not a direct call.\n"
        "Do not use verbs like 'calls', 'invokes', 'delegates to', or 'hands off to' "
        "unless the call site or callee body proves that relationship.\n"
        "Do not merge different symbols into the same step. The caller step and callee step "
        "must keep separate file paths, symbols, and anchors.\n"
        "Do not continue into an imported helper as the next flow step unless the current step "
        "shows a direct call site or another snippet proves the invocation relationship.\n"
        "Do not add side-branch helpers from other modules unless the traced chain shows their direct call edge "
        "or the callee is directly invoked by a snippet-backed step.\n"
        "Do not add contextual or 'similar pattern' modules to the traced flow unless the evidence shows they "
        "participate in the same execution path.\n"
        "Do not claim that a helper performs a specific signal disconnect, reconnect, or handler removal "
        "in the traced flow unless that exact action is shown in the helper's own SOURCE SNIPPET or in a direct "
        "call-site snippet.\n"
        "Do not describe helper internals from the caller's invocation line alone. If the caller only shows "
        "`_helper(...)`, describe only that invocation unless the helper's own SOURCE SNIPPET is also shown.\n"
        "In a traced flow, do not combine a caller snippet with separate file-level evidence to claim a helper's "
        "internal operation. Only describe that internal operation if the helper's own SOURCE SNIPPET is also shown; "
        "otherwise say the helper is invoked and its internals are not shown in the provided evidence.\n"
        "If a step shows a direct call to a named method or function, and the evidence pack also contains the callee "
        "definition or snippet elsewhere, continue the flow into that callee instead of stopping at the call site.\n"
        "If the middle handoff method is named but its body is not shown, say: "
        "'The call is evidenced, but the callee body is not present in SOURCE SNIPPETS.'\n"
        "Do not claim that downstream helpers do not perform additional disconnects, reconnects, timer stops, "
        "or timer restarts unless the snippet explicitly shows that absence; otherwise say those actions are "
        "'not shown in the provided evidence'.\n"
        "Copy file paths, symbol names, and function names exactly as they appear in the evidence. "
        "Do not respell, normalize, or rename identifiers.\n"
        "For runtime/reset questions, if disconnect or stop actions are shown but reconnect or restart actions are not shown, "
        "say that reconnect/restart behavior is 'not shown in the provided evidence' rather than claiming it does not occur.\n"
        "If a downstream function is shown after a runtime/reset step, describe only the disconnect/stop operations "
        "explicitly present in that downstream function's snippet; otherwise say those operations are "
        "'not shown in the provided snippet' rather than saying the function does not perform them.\n"
        "If a shown function body contains helper calls or cleanup steps but does not explicitly show additional "
        "disconnect/reconnect operations, say those operations are 'not shown in the provided snippet' rather than "
        "claiming they are not performed there.\n"
        "Do not say that generic cleanup code 'implies' specific signal cleanup, disconnection, reconnection, "
        "or handler removal unless that specific operation is explicitly shown in the snippet.\n"
        "If one transition is not directly shown, say exactly which link is missing.\n"
    )

    if is_which_method_calls_question(q):
        wants_callsite_code = (
            prefer_code
            or "snippet" in q
            or "snippets" in q
            or "call site" in q
            or "exact snippet" in q
            or "what exact snippet shows" in q
            or "show code" in q
            or "with code" in q
        )

        base = (
            "ANSWER STYLE\n"
            "For this question, answer strictly as a caller lookup with call-site proof.\n"
            "Lead with the caller method or function, never with the callee definition.\n"
            "The caller is the method or function whose snippet contains the invocation of the asked callee.\n"
            "Do not answer with the callee's definition as if it were the caller.\n"
            "Do not use the callee definition snippet as caller evidence.\n"
            "Prefer snippets that literally contain the callee invocation, such as `callee_name(...)`.\n"
            "If multiple caller snippets are present, name the most direct caller first and then mention that additional callers are also evidenced.\n"
            "If a caller snippet is shown, begin with: `The caller shown by the evidence is ...`\n"
            "If the call site is shown but the surrounding method body is partial, say the call site is shown and the full caller body is partial.\n"
            "Do not answer with phrases like `The best evidence-backed caller is <callee>`.\n"
            + calibration
        )

        if wants_callsite_code:
            return (
                base
                + "You must include one short verbatim code excerpt showing the actual call site.\n"
                + "The code excerpt must contain the callee invocation itself.\n"
                + "Immediately below the excerpt, state:\n"
                + "- the caller file path,\n"
                + "- the caller symbol,\n"
                + "- why this snippet proves the caller relationship.\n"
                + "If more than one caller snippet exists, prefer the most direct and self-contained caller snippet first.\n"
                + "Do not use an import statement as the call-site proof when a direct invocation snippet is available.\n"
                + "Do not use the callee definition snippet unless the user separately asks where the callee is defined.\n"
            )

        return (
            base
            + "Do not output code blocks unless the user explicitly asks for code.\n"
            + "Still identify the exact caller and describe the exact call-site proof in prose.\n"
        )

    if is_code_localized_explanation_question(question):
        base = (
            "ANSWER STYLE\n"
            "For this question, explain the flow or implementation as a code-localized technical walkthrough.\n"
            "Use this order when supported by evidence:\n"
            "1) brief purpose of the flow,\n"
            "2) entry file and entry symbol,\n"
            "3) step-by-step handoff across files or symbols,\n"
        )

        if prefer_code:
            return (
                base
                + "4) real code excerpts from SOURCE SNIPPETS,\n"
                + "5) short note about the missing link if evidence is partial.\n"
                + "Prefer exact evidence-backed file paths, symbol names, snippet anchors, and line numbers when present.\n"
                + code_excerpt_rules
                + "For each excerpt, immediately explain:\n"
                + "- what file it comes from,\n"
                + "- what symbol or anchor it belongs to,\n"
                + "- why it matters in the flow.\n"
                + "Prefer prose plus code localization over prose-only explanation.\n"
                + "When supported by evidence, mention concrete file paths and approximate line anchors from the snippet headers.\n"
                + calibration
            )

        return (
            base
            + "4) code-localization notes using file paths, symbols, and snippet anchors,\n"
            + "5) short note about the missing link if evidence is partial.\n"
            + "Prefer exact evidence-backed file paths, symbol names, snippet anchors, and line numbers when present.\n"
            + "Do not output code blocks unless the user explicitly asks for code.\n"
            + "Focus on precise code localization in prose.\n"
            + calibration
        )

    if is_explain_implementation_question(question):
        base = (
            "ANSWER STYLE\n"
            "For this question, explain the implementation as a technical walkthrough in plain prose.\n"
            "Use this order when supported by evidence:\n"
            "1) implementation entry point,\n"
            "2) main orchestration class or method,\n"
            "3) rendering or execution class or method,\n"
            "4) update, interaction, or refresh flow,\n"
            "5) one missing link sentence at the end if evidence is partial.\n"
            "Prefer exact evidence-backed symbol names when they are present in the evidence pack.\n"
        )

        if prefer_code:
            return (
                base
                + "If retrieved snippets contain real implementation code, you must include real code excerpts in the answer.\n"
                + "When code is shown, it must be copied only from the provided SOURCE SNIPPETS.\n"
                + "Do not invent code, do not reconstruct missing code, and do not synthesize pseudo-source from description alone.\n"
                + "Show at least 2 short real code excerpts when the evidence pack contains relevant snippets.\n"
                + "For each code excerpt, add a short prose explanation immediately below it.\n"
                + "Prefer code-backed explanation over prose-only explanation in this mode.\n"
                + calibration
            )

        return (
            base
            + "Prefer architectural prose over code excerpts.\n"
            + "Do not output code blocks unless the user explicitly asks for code.\n"
            + "Summarize the implementation mainly in prose, using concrete evidence-backed symbols and relationships.\n"
            + calibration
        )

    if is_chain_or_flow_question(question):
        base = (
            "ANSWER STYLE\n"
            "For this question, explain the flow step by step in execution order.\n"
            "For reset/cleanup questions, prefer this order when supported by evidence:\n"
            "1) entry/orchestrator symbol,\n"
            "2) direct handoff calls,\n"
            "3) leaf cleanup/reset methods,\n"
            "4) one explicit missing-link note if the invocation path is not shown.\n"
            "Do not lead with leaf cleanup methods if an orchestrator or reset-flow controller is present in evidence.\n"
            "Name the concrete file paths, symbols, and handoff points when supported by evidence.\n"
        )

        if prefer_code:
            return (
                base
                + "If SOURCE SNIPPETS are present, include at least 2 short verbatim code excerpts copied exactly from those snippets to anchor the key handoff points.\n"
                + "Never output a code block for a function unless that exact function body is present in SOURCE SNIPPETS.\n"
                + "If a helper is supported only by file-level evidence, describe it in prose only.\n"
                + "Do not synthesize placeholder code, representative code, or reconstructed code.\n"
                + "For each code excerpt, immediately state the file, symbol, and why it matters in the flow.\n"
                + "Never quote prompt instructions, answer-style instructions, or validator guidance as if they were source code.\n"
                + "Only use a code block when the excerpt comes from a real SOURCE SNIPPET tied to the reported file path and symbol.\n"
                + "If the retrieved text is instructional or meta text rather than source code, describe it in prose and do not place it in a code block.\n"
                + chain_evidence_rules
                + "Calibrate certainty carefully:\n"
                + "- Use 'the evidence shows' for directly supported transitions.\n"
                + "- Use 'appears to connect to' or 'is likely followed by' only when inferred.\n"
            )

        return (
            base
            + "Do not output code blocks unless the user explicitly asks for code.\n"
            + "Explain the same flow in prose, but still name the concrete file paths, symbols, and handoff points when supported by evidence.\n"
            + chain_evidence_rules
            + "Calibrate certainty carefully:\n"
            + "- Use 'the evidence shows' for directly supported transitions.\n"
            + "- Use 'appears to connect to' or 'is likely followed by' only when inferred.\n"
        )

    if prefer_code:
        return (
            "ANSWER STYLE\n"
            "Answer with a mix of concise prose and short verbatim code excerpts from SOURCE SNIPPETS.\n"
            "Lead with the most evidence-backed file and symbol.\n"
            "Include at least one code excerpt copied verbatim from SOURCE SNIPPETS when available.\n"
            "Do not invent code. If no snippet covers a detail, describe it in prose.\n"
            "If evidence is partial, state the missing link in one sentence at the end.\n"
            "Calibrate certainty carefully and avoid overstating inferred links.\n"
        )

    return (
        "ANSWER STYLE\n"
        "Answer entirely in plain prose. Do NOT output any code blocks.\n"
        "Prefer concrete evidence-backed files, symbols, and relationships over general summary language.\n"
        "Describe what methods do, what they call, and how they connect in English sentences only.\n"
        "If evidence is partial, state the missing link in one sentence at the end.\n"
        "Calibrate certainty carefully and avoid overstating inferred links.\n"
    )


