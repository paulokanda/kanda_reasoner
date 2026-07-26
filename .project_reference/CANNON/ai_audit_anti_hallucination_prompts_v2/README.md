# AI Audit and Anti-Hallucination Prompt Pack v2

This pack is divided into two groups.

## large_group

Use for architectural, multi-file, dependency-changing, concurrency-sensitive, security-sensitive, high-risk, or unfamiliar work.

Files:
- 0041_large_independent_ai_audit.md
- 0041b_large_web_evidence_audit.md
- 0041d_large_book_literature_audit.md
- 0043_large_anti_hallucination_protocol.md

Recommended order:
1. Build the provisional implementation plan.
2. Run the independent adversarial AI audit.
3. Build the Claim Ledger.
4. Run the web evidence and disconfirmation audit.
5. Use the book/literature audit only when the task has genuine architecture uncertainty.
6. Integrate only ADOPT and ADAPT findings.
7. Implement only after source inspection and the applicable human approval gate.
8. Validate through deterministic evidence and a final adversarial verification pass.

## summarized_group

Use for routine or lower-risk work when the same safety logic is needed with less context overhead.

Files:
- 0041a_short_independent_ai_audit.md
- 0041c_short_web_evidence_audit.md
- 0041e_short_book_literature_audit.md
- 0043_short_anti_hallucination_protocol.md

The short prompts preserve the same core model:
- independent criticism;
- claim ledger;
- evidence hierarchy;
- disconfirmation search;
- ADOPT/ADAPT/REJECT/UNVERIFIED decisions;
- source inspection and runtime-test deferrals;
- human approval and validation gates.

## Important design change

The prior workflow risked sequential confirmation bias:
Plan -> AI agrees -> web finds support -> books provide supporting principles.

The v2 workflow is:
Source truth -> provisional plan -> independent adversarial review -> claim ledger -> support and disconfirmation search -> targeted literature audit -> evidence-based synthesis -> implementation -> validation -> adversarial verification -> human approval.

The anti-hallucination protocol is provided in both full and short form.
