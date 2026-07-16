You are an AI assistant with high-precision state tracking and handoff capabilities.  
Your task is to generate a **handoff report** for another AI instance (or your future self)
to resume a complex, multi-step interaction without loss of context or progress.

**Handoff requirements:**  
- **Cannon** = All facts, decisions, user constraints, and outputs that have been explicitly 
- confirmed and cannot be changed retroactively.  
- **Frozen** = Any part of the current state (e.g., code structure, data schema, plan milestones) 
- that has been locked and should not be modified unless explicitly instructed.  
- **Current work** = The exact task being executed right now, including its inputs, 
- outputs, and any partial results.  
- **Methodology** = The step‑by‑step process, tools, APIs, or reasoning patterns used so far.  
- **Next steps** = The immediate actions the new AI should take, 
- including any pending decisions or verification checks.

**Output format (structured for machine parsing):**  

[HANDOFF_START]
CANON:

    <list each canonical fact as a key‑value or bullet>

FROZEN:

    <list each frozen element with its boundary conditions>

CURRENT_TASK:
Description: <one sentence>
Inputs: <references>
Partial_outputs: <any computed but not yet finalized results>
Blockers: <if any>

METHOD:
Tools/Frameworks: <e.g., Python 3.11, pandas, regex>
Workflow: <numbered steps from last confirmed checkpoint>
Assumptions: <explicit assumptions made>

NEXT:
Immediate: <first action>
Conditional: <if‑then scenarios>
Verification: <how to confirm success>

[HANDOFF_END]
text


**Important:**  
- Write directly **to the AI** (second person: "you will receive", "your state", "the following variables").  
- Avoid human‑friendly fluff; prioritize precision, completeness, and unambiguous references.  
- Include any unresolved exceptions or ambiguous states under `CURRENT_TASK.Blockers`.  
- If any information is missing, state `[UNKNOWN]` rather than guessing.

**Now generate the handoff based on the entire conversation history so far.**

