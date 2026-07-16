# Prompt Template: Top-5 Book Research for Python Architecture & Performance

A reusable prompt. Replace `{SUBJECT}` and `{PROJECT_CONTEXT}` with your actual values before sending to the AI.

---

```
ROLE
You are a senior Python architect and technical researcher with deep expertise in
software design, performance engineering, and system architecture.

TASK
Search the internet and identify the 5 most authoritative, currently top-ranked books
on the subject: "{SUBJECT}".

Use signals such as: Amazon/Goodreads bestseller & rating rank, O'Reilly/Manning/
Packt/No Starch catalog prominence, citation frequency in engineering blogs, "best
books on {SUBJECT}" roundup articles, and recency (prefer editions from the last 5
years unless a book is a recognized classic/reference standard).

For EACH of the 5 books, extract and report:
1. Title, author(s), edition/year, and why it ranks highly (1-2 sentences).
2. The 3-5 core ideas, patterns, or techniques from the book that are MOST relevant
   to improving performance, scalability, or maintainability in a Python project.
3. Concrete, actionable takeaways — not generic summaries. Prefer things like:
   - specific design patterns or architectural styles it recommends
   - specific Python idioms, libraries, or profiling/optimization techniques
   - anti-patterns it warns against
   - benchmarks, complexity trade-offs, or measurable performance claims it makes
4. One short pseudo-code or Python snippet illustrating the idea, where applicable.

SYNTHESIS (after covering all 5 books)
- Cross-reference the 5 books: which recommendations overlap or reinforce each other?
- Flag any direct contradictions between authors and briefly explain the trade-off.
- Produce a prioritized action list (High / Medium / Low impact) of improvements to
  apply, specifically tailored to this context:

  {PROJECT_CONTEXT}
  (e.g., "a Django REST API handling 200 req/s", "a data pipeline processing CSVs
  with pandas", "a CLI tool with a plugin architecture", etc. — describe your
  current stack, pain points, and constraints here.)

OUTPUT FORMAT
- Use a numbered section per book.
- End with a single consolidated Markdown table: | Idea | Source Book | Impact | Effort | Applies to our code? |
- Keep prose concise; prioritize actionable bullet points over narrative.
- Cite sources (book titles, and article/URL where you found ranking info) so the
  recommendations can be verified.

CONSTRAINTS
- Do not invent books or claims — if uncertain about a ranking or fact, say so
  explicitly rather than guessing.
- Focus strictly on ideas applicable to Python and software architecture/
  implementation logic (design, structure, performance, scalability, testing,
  maintainability) — skip unrelated business/soft-skills content even if the book
  covers it.
```

---

## How to use this template

1. Fill in `{SUBJECT}` with whatever you're working on right now — examples:
   - "event-driven microservices architecture"
   - "high-performance data pipelines in Python"
   - "domain-driven design"
   - "concurrency and async Python"
   - "clean architecture / hexagonal architecture"
2. Fill in `{PROJECT_CONTEXT}` with a short description of your actual project
   (stack, scale, bottlenecks, constraints). The more specific this is, the more
   actionable the synthesis section will be.
3. Optionally paste a code snippet or architecture diagram right after the prompt
   so the AI can map book recommendations directly onto your real implementation.
4. Reuse as-is for every new subject — only the two placeholders change.

## Why this template works
- **Forces source grounding**: requiring ranking signals and citations prevents
  the AI from just listing "famous" books from memory without checking freshness.
- **Separates extraction from synthesis**: books are mined individually first,
  then cross-referenced — this avoids shallow, generic summaries.
- **Ties everything back to your project**: the prioritized action list is the
  actual deliverable; the book research is just the means to get there.
- **Structured output**: the impact/effort table makes it trivial to turn results
  into a backlog or sprint task list.
