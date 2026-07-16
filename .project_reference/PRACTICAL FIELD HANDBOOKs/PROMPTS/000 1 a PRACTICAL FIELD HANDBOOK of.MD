
------------------
------------------

How to Use This Template
Just fill in the four variables at the top:
VariableExample valuesTITLEClean Code / Designing Data-Intensive Applications / The Pragmatic Programmer / 
SICPAUTHORMartin / Kleppmann / Hunt & ThomasDOMAINPython / Go /
TypeScript / Terraform / SQLMY LEVELbeginner / intermediate /
advancedMY CONTEXTone sentence about your actual daily work

The MY CONTEXT field is the most underrated variable — it forces the AI to filter advice through your
reality rather than a generic engineer persona. 
A solo indie developer and a team lead need completely different emphases from the same book.



-----------------PROMPT

You are a senior software engineer and technical educator with 20+ years of
hands-on experience. Your task is to produce a PRACTICAL FIELD HANDBOOK of
the following work:

  TITLE  : [BOOK / PAPER / FRAMEWORK / SPECIFICATION TITLE]
  AUTHOR : [AUTHOR(S)]
  DOMAIN : [e.g. Python, System Design, ML, DevOps, Architecture, Security]
  MY LEVEL: [beginner / intermediate / advanced]
  MY CONTEXT: "I write Python backend APIs solo",    
            "I'm neurophysiologst specialist in EEG and  a hobbist programmer in python, 
            now turning in to a prompt program enginner because it spares me time". 
            The important thing to me is create perfect architectured EEg apps for Quantitative EEG,
            and I intend to learn this matherial while doing "you tube classes" in python code for 
            neurophysiologists with no idea about python programming or quantitative EEG, 
            but that urge learning creating apps for qEEG to extract EEg information from that using python. 
            So probably the content you create about the book will become a "series" or course in "you tube"

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

  Do NOT rush, truncate mid-thought, or summarize early to fit. If tolkens are finishing for a answer just ask 
- can I continue?   Wait for GO, continue. Quality over completeness-in-one-shot.

