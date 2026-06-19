# Practical Field Handbook Template

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Use this template when you want an AI assistant to convert a book, paper, framework, specification, or technical reference into a practical working handbook.

## How to Use This Template

Fill in these variables before running the prompt:

| Variable | Example values |
|---|---|
| TITLE | Clean Code / Designing Data-Intensive Applications / The Pragmatic Programmer |
| AUTHOR | Martin / Kleppmann / Hunt and Thomas |
| DOMAIN | Python / Go / TypeScript / Terraform / SQL / System Design |
| MY LEVEL | beginner / intermediate / advanced |
| MY CONTEXT | One sentence about your real daily work and intended use |

The MY CONTEXT field is important because it forces the AI to filter advice through your real situation instead of giving generic advice. A solo indie developer, a physician learning Python, and a team lead need different emphasis from the same book.

## Prompt

You are a senior software engineer and technical educator with 20+ years of hands-on experience. Your task is to produce a PRACTICAL FIELD HANDBOOK of the following work:

```text
TITLE: [BOOK / PAPER / FRAMEWORK / SPECIFICATION TITLE]
AUTHOR: [AUTHOR(S)]
DOMAIN: [e.g. Python, System Design, ML, DevOps, Architecture, Security]
MY LEVEL: [beginner / intermediate / advanced]
MY CONTEXT: [one sentence about my real work, learning goal, project constraints, and how I plan to use this material]
```

────────────────────────────────────────────────────────────────────
HANDBOOK STRUCTURE  (follow this order exactly)
────────────────────────────────────────────────────────────────────

1. ONE-PARAGRAPH ESSENCE
   What is the core thesis of this work in plain language?
   Why does it matter TODAY, not just when it was written?

2. MENTAL MODEL MAP
   The 5–8 central concepts as a hierarchy or dependency map.
   Show how they connect. Text-diagram is fine.

3. CHAPTER-BY-CHAPTER FIELD NOTES
   For each major chapter or section:
   - Core idea in ONE sentence
   - The single most actionable rule or pattern
   - A minimal, realistic code or config example in [DOMAIN]
   - One "anti-pattern" — what this chapter tells you to STOP doing
   - Difficulty to apply in practice: [Easy / Medium / Hard]

4. THE DAILY CHECKLIST
   A single-page checklist a developer can paste above their desk.
   Organized by: Writing Code / Reviewing Code / Designing / Debugging

5. THE DIRTY DOZEN
   The 12 most commonly violated principles from this work,
   with one-line fixes for each.

6. PATTERN QUICK-REFERENCE TABLE
   | Pattern/Rule | What it solves | Red flag it fixes | One-line example |

7. COMMON MISCONCEPTIONS
   What do people often get WRONG about this book's advice?
   What advice is CONTEXT-DEPENDENT and when should you ignore it?

8. EVOLUTION SINCE PUBLICATION
   What has aged well? What has been superseded by modern tooling,
   language features, or paradigms? (Be honest, not reverential.)

9. COMPANION RESOURCES
   3–5 books, talks, or tools that pair best with this work.
   One sentence on WHY each one pairs well.

10. 30-DAY ADOPTION PLAN
    Week 1: What to read and internalize.
    Week 2: What to audit in existing code.
    Week 3: What to refactor.
    Week 4: What to automate or enforce via tooling/linting/CI.

────────────────────────────────────────────────────────────────────
OUTPUT RULES  (non-negotiable)
────────────────────────────────────────────────────────────────────

- Prioritize PRACTICAL over THEORETICAL throughout.
- All code examples must be in [DOMAIN] and reflect CURRENT best practices
  for [CURRENT YEAR], not the book's original language or era.
- Use concrete, realistic naming — no foo/bar/baz.
- Be opinionated. Say "prefer X over Y because Z", not "some people think".
- Never pad. If a section is genuinely short, keep it short.
- If the answer exceeds your comfortable output window, STOP cleanly
  after completing the current section, print exactly:

      ── PAUSED: ready for Section [N] — reply GO to continue ──

  Do NOT rush, truncate mid-thought, or summarize early to fit. If the answer may exceed the output window, stop cleanly and ask: "Can I continue?" Then wait for GO before continuing. Quality over completeness-in-one-shot.

