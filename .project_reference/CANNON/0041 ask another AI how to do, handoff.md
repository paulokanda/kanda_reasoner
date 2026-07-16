Here's an improved, restructured version of your prompt. I tightened the ambiguous phrasing, made the role assignment and constraints explicit, added a clear output structure, and separated the "current task" as a fillable variable so it's reusable.

---

## Improved Prompt

```
ROLE ASSIGNMENT
You are about to consult another AI acting as an independent auditor.
Address that AI directly as follows:

"You are a Python specialist with 20 years of experience refactoring
large-scale, multi-layered, and architecturally complex codebases.
I want you to critically audit the implementation plan below before
any code is written."

CONTEXT TO PROVIDE
Share with the auditor AI:
1. A one-paragraph summary of the overall task/system we are building.
2. My current implementation plan, including:
   - Proposed module/file breakdown
   - Responsibilities of each layer/module
   - Key data flows and interfaces between modules
   - Any design patterns or architectural decisions already made

HARD CONSTRAINTS (must be stated explicitly to the auditor)
- Every code file, including helper/utility files, must be between
  100 and 500 lines (strictly: >100 and <500 lines).
- No "tiny" or trivial single-purpose modules are allowed — if a
  module would fall under 100 lines, it must be merged into a
  related module instead.
- No single file may exceed 500 lines — if it would, it must be split
  along logical/functional boundaries, not arbitrarily.
- Flag any part of the current plan that violates these constraints
  and propose a concrete restructuring.

REQUEST TO THE AUDITOR AI
Ask the auditor to respond with:
1. **Structural review** — Is the file/module breakdown sound? Are
   responsibilities well separated (single-responsibility, low
   coupling, high cohesion)?
2. **Risks** — Technical risks, edge cases, or failure modes in the
   proposed approach.
3. **Improvements** — Concrete suggestions to improve maintainability,
   testability, and performance.
4. **Corrections** — Any errors, inconsistencies, or anti-patterns in
   the current plan.
5. **Compliance check** — Explicit confirmation of whether the plan
   respects the 100–500 line constraint per file, with specific
   violations called out by filename/module.
6. **Final logic recommendation** — The auditor's best-practice
   recommendation for the final implementation logic, including
   naming, folder structure, and interface contracts.

OUTPUT FORMAT REQUESTED FROM AUDITOR
Ask the auditor to structure their reply under exactly these headers:
- Structural Review
- Risks
- Improvements
- Corrections
- Compliance Check (100–500 line rule)
- Final Recommended Logic

NEXT STEP (for me, after receiving the audit)
Once the auditor AI responds, return their full feedback to me
verbatim (or clearly summarized per section above) so I can review
it and decide which recommendations to incorporate before we proceed
to implementation.
```

---

### What I changed and why

| Issue in original | Fix |
|---|---|
| Run-on sentence mixing role assignment, task, and constraints | Split into clear sections: ROLE, CONTEXT, CONSTRAINTS, REQUEST, OUTPUT FORMAT, NEXT STEP |
| "Files and their help files must be less than 500 lines and above 100 lines" — grammatically ambiguous (less than 500 *and* above 100 could confuse a model into missing one bound) | Explicit strict range: `>100 and <500 lines`, stated as a **hard constraint**, applied to both main and helper files |
| "No tiny modules allowed" was vague — unclear threshold | Defined "tiny" concretely as anything under the 100-line floor, with an explicit remediation rule (merge, don't leave undersized) |
| No output structure requested from the auditor — response could ramble | Added a fixed 6-section header format so responses are consistent and easy to diff/compare across audit rounds |
| No explicit compliance check tied back to constraints | Added a dedicated "Compliance Check" section so the auditor must explicitly verify (not just implicitly consider) the line-count rule |
| Task itself ("the task we are working on") was left undefined inline | Added a CONTEXT section as a fill-in slot so this prompt is reusable across different projects |
| No instruction for what happens with the response | Added an explicit "NEXT STEP" so the loop (plan → audit → return to me) is unambiguous |

