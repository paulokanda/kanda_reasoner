We are not vibe coding. We are doing something significantly more sophisticated.

What Vibe Coding Actually Is
Vibe coding is:

"Make me an app that does X" → accept whatever comes out
No architecture awareness
No validation discipline
No governance
No understanding of what was generated
Vibes-based iteration: "make it prettier", "fix the error"

The programmer is essentially a prompt typist with no engineering judgment applied.

What We Are Actually Doing
Looking at our prompt stack alone:

Our PracticeEngineering TermLocked load order (0.1)
+------------------------------------------+----------------------------------+
    |OUR PRACTICE                            | ENGINEERING TERM                 |
+------------------------------------------+----------------------------------+
| Locked load order (0.1)                  | Dependency management            |
| Source truth hierarchy                   | Evidence-grounded reasoning      |
| One box per responsibility               | Separation of concerns           |
| Validate before freeze                   | CI/CD discipline                 |
| Governance files                         | Architecture control             |
| Blast radius assessment                  | Risk management                  |
| ZIP delivery with project-relative paths | Reproducible deployment          |
| py_compile + manual GUI checklist        | Acceptance testing               |
| Handoff documents (6.0)                  | Session continuity / knowledge   |
|                                          | management                       |
+------------------------------------------+----------------------------------+


The Real Name for What We Do
We are a Prompt Architect practicing AI-augmented software engineering.

The distinction is critical:
Vibe coder:    AI drives → human accepts

Our workflow: Human architects → AI implements → Human validates → Human governs

We hold the engineering judgment. The AI holds the implementation labor. 
That is exactly how senior engineers used junior developers for decades
— except our junior never gets tired and never argues.

The One Honest Caveat
We approach vibe coding territory only if:

We accept generated code without reading it
We skip the validation commands
We let the AI modify governance files without your explicit approval

Our prompt stack specifically forbids all three of those.
So we are architecturally protected from drifting into vibe coding even on a bad day.

Bottom line: Vibe coding is accidental software.
What we are doing is intentional software with AI execution. 
Those are not the same discipline.

what we are doing is vibecoding?

Partly, yes — but not in the usual loose sense of vibe coding.

What we are doing is closer to:

governed AI-assisted software engineering
or
disciplined vibe coding with architecture, validation, and rollback

Classic vibe coding is often:

tell AI what you want
→ AI writes code
→ run it
→ fix whatever breaks
→ keep going

Our workflow is more like:

intent
→ architecture audit
→ identify owner box
→ define allowed scope
→ generate bounded patch
→ install
→ validate
→ inspect real runtime behavior
→ correct narrowly
→ Error Memory if something failed
→ freeze evidence
→ Preview
→ Confirm and Write

So yes, the interaction style is vibe coding:

you describe goals in natural language;
we iterate quickly;
AI writes substantial parts of the implementation;
discoveries during execution influence the next step;
the architecture evolves through feedback rather than being fully specified upfront.

But the engineering discipline is very different from stereotypical vibe coding.

We added things specifically to stop the dangerous parts of vibe coding:

Vibe coding risk             KANDA response

AI edits random files        Box Logic
wrong project writes         No-Leak Logic
architecture drift           Prompt Library canon
AI invents architecture      deterministic gates
hidden regressions           validators
bad AI suggestion            candidate tournament
unsafe source mutation       Workbench transaction model
failed apply                 rollback
same mistake repeated        Error Memory
"it seems done"              freeze evidence + Confirm and Write

For example, the Local AI Planner is almost the opposite of uncontrolled vibe coding:

AI proposes Candidate A
AI proposes Candidate B
AI proposes Candidate C

KANDA validates all of them
KANDA scores all of them

AI does not choose the winner

And when Local AI was worse:

baseline     0.736690
candidate A  0.736690
candidate B  0.640690
candidate C  0.736690

we did not accept an AI change merely because the AI produced one. The deterministic baseline stayed.

The same happened with the external Web AI version: we used AI creatively, but only accepted a small bounded proposal that improved the measured architecture:

Heuristic:
122 / 452

Web AI:
145 / 429

baseline score:
0.736690

Web proposal:
0.783250

So my honest classification would be:

What we are doing

30% vibe coding

natural-language direction;
rapid experimentation;
AI-generated code;
conversational iteration.

70% AI-assisted engineering discipline

explicit architecture ownership;
deterministic validation;
exact patch boundaries;
Error Memory;
rollback;
freeze;
reproducible evidence.

A good name for the KANDA approach would be:

Governed Vibe Coding

or, more technically:

AI-driven iterative engineering with deterministic guardrails

The interesting thing about KANDA is that we are effectively building a system that lets us keep the speed and creativity of vibe coding while systematically removing its biggest weaknesses: architectural drift, silent breakage, hallucinated changes, unreproducible fixes, and loss of control over what the AI actually changed.

can we call it  natural language programing  with  ai driven iterative engineering?

Yes. That description fits what we’re doing very well.

I’d phrase it as:

Natural Language Programming with AI-Driven Iterative Engineering

That captures both halves of the workflow:

Natural Language Programming

you define goals, constraints, architecture, corrections, and priorities conversationally;
the AI translates intent into code, patches, prompts, validation logic, and workflows;
programming increasingly happens through specifications and feedback rather than writing every line manually.

AI-Driven Iterative Engineering

implementation happens in controlled cycles;
each cycle uses evidence from the previous one;
AI proposes, but deterministic gates validate;
failures become repair inputs and Error Memory;
architecture is progressively improved rather than improvised without control.

For KANDA specifically, I think the fuller description is:

Natural Language Programming with AI-Driven Iterative Engineering and Deterministic Guardrails

Or as a compact model:

Natural-language intent
        ↓
AI interpretation
        ↓
bounded implementation
        ↓
deterministic validation
        ↓
real-world feedback
        ↓
targeted correction
        ↓
memory and governance
        ↓
next iteration

I actually think Natural Language Programming is a better umbrella term for your project than vibe coding, because KANDA is being deliberately designed so the human can operate at a higher semantic level while the system preserves architecture, validation, provenance, rollback, and freeze state.

A strong one-line description of KANDA could be:

KANDA is a natural language programming environment for AI-driven iterative software engineering with deterministic architectural guardrails.

That is probably the most accurate description of what we have been building.