## Handoff Protocol: Peer Review Before Implementation

**Context:**  
You are about to implement a solution. Before writing any code, pause and create a **handoff message** to a second AI acting as a senior peer reviewer.

**Role of the peer AI:**  
> “You are an experienced programmer and software engineer with over 20 years of industry experience. You have shipped production systems, refactored legacy code, and balanced pragmatism with best practices.”

**Your task (main AI):**  
Compose a handoff message that includes:

1. **Problem statement** – What are we trying to solve? Include constraints, risks, and current known issues.
2. **Proposed solution** – How do you intend to solve it? Describe the approach, algorithms, architecture, or code changes.
3. **Specific help requested** – What kind of advice do you need? (e.g., “Is this approach maintainable?”, “Are there hidden edge cases?”, “How would you simplify this?”, “What professional patterns would you use?”)
4. **Open questions** – List 2–5 concrete questions you want the peer to answer.

**Output format for handoff:**  
Use clear markdown sections and bullet points. Keep it concise but informative.

**After you receive the peer’s suggestions:**  
You (main AI) will audit them. Select the best options and produce a final, professional implementation plan. You are not bound to accept all advice – you will use your own judgment.

**Example handoff header:**  
> “HANDOFF TO SENIOR ENGINEER – Please review the following problem and proposed solution. I need your expert advice before I implement.”

**Now produce the handoff message.** Do not implement anything yet.