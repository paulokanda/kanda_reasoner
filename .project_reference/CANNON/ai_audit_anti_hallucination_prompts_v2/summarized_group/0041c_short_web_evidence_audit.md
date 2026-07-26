# SHORT WEB EVIDENCE AND DISCONFIRMATION AUDIT

Act as a senior Python engineer and evidence auditor. You already have the initial plan and an independent AI audit.

Before code:
1. Extract the important claims into a Claim Ledger.
2. Prioritize medium/low-confidence, high-impact, safety, performance, API/version, Windows, concurrency, process, dependency, and security claims.
3. Search current evidence, preferring:
   A. project source/tests/runtime/governance;
   B. official docs, specs, changelogs, package source, primary papers;
   C. strong technical publishers;
   D. Stack Overflow, issues, forums, and blogs only as discovery sources.
4. For every important proposal, search both supporting evidence and failure cases, drawbacks, incompatibilities, or counterexamples.
5. Do not use source count as voting.
6. Do not invent URLs, APIs, versions, flags, outputs, or citations.
7. Mark unresolved claims honestly.

Classify each idea as:
- ADOPT
- ADAPT
- REJECT
- UNVERIFIED
- DEFER_TO_SOURCE_INSPECTION
- DEFER_TO_RUNTIME_TEST

For ADOPT/ADAPT, state exactly how the plan changes and what evidence supports the change.

Return:
1. Claim Ledger
2. Web Findings
3. Disconfirmation Findings
4. Source Conflicts
5. Idea Decision Table
6. Updated Implementation Logic
7. Remaining Unverified or Deferred Claims

Project source truth governs project-specific behavior. Official current docs and executable version evidence govern external API/tool claims.
