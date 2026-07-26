# SHORT BOOK AND LITERATURE ARCHITECTURE AUDIT

Perform a final literature audit only if the task has real architectural uncertainty, such as module boundaries, dependency direction, ownership, workflow sequencing, architecture governance, safe legacy-code change, complexity, persistence, testability, or failure containment.

Do not use books to verify current API signatures, versions, flags, deprecations, or runtime behavior; use official docs, source inspection, or execution for those.

When justified:
1. Select up to 5 highly regarded books directly relevant to the subject and up to 5 architecture/design books relevant to the core design.
2. Use cross-source convergence: established publishers, recognized authors, professional recurrence, and strong task relevance.
3. Extract only principles that materially affect this project.
4. For each idea classify:
   ADOPT / ADAPT / REJECT / NOT_APPLICABLE / ALREADY_SATISFIED / UNVERIFIED_APPLICATION.
5. Do not add ideas merely to show research was done.
6. Resolve conflicts in this priority:
   project source/governance -> executable evidence -> current official docs -> primary research -> applicable book principles -> senior judgment.
7. Update the plan only with ADOPT/ADAPT items.
8. Explain exactly what changed, why, and what validation consequence follows.
9. Produce a final objective proposal and a numbered roadmap titled "How Deliver Project to AI Use."

Module rule:
- every touched/new source module must stay below 500 physical lines;
- ideal target is 400 code lines or fewer where practical;
- choose boundaries by ownership, cohesion, information hiding, and reason to change;
- never pad files or create fake tiny wrappers for line-count compliance.

Return:
1. Book Audit Justification
2. Source Set
3. Relevant Findings
4. Decision Table
5. Source Conflicts
6. Final Integrated Logic
7. Final Objective Proposal
8. How Deliver Project to AI Use
9. Remaining Unverified Items
