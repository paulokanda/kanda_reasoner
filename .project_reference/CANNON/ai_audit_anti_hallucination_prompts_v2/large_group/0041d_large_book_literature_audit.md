# TARGETED BOOK AND PUBLISHED-LITERATURE ARCHITECTURE AUDIT

ROLE

You are performing the final literature-based architecture audit before implementation logic is considered mature.

You already have:
1. the initial implementation plan;
2. an independent specialist AI audit;
3. a web evidence and disconfirmation audit;
4. a Claim Ledger and unresolved items.

The purpose of this stage is not to collect prestigious book titles or force book principles into the project. The purpose is to identify only literature-derived ideas that create a concrete gain in logic, safety, maintainability, testability, performance, or architectural clarity for this exact project.

## FIRST DECISION - IS A BOOK AUDIT WARRANTED?

Before selecting books, determine whether the task contains genuine architectural uncertainty.

Book audit is justified for questions such as:
- ownership and responsibility boundaries;
- modular decomposition;
- dependency direction;
- public contract preservation;
- state and persistence ownership;
- workflow sequencing;
- observability;
- safe legacy-code change;
- testability;
- architecture governance;
- evolution and fitness functions;
- complexity management;
- failure containment.

Book audit is usually not necessary to verify:
- exact current API signatures;
- exact package versions;
- current deprecations;
- CLI flags;
- runtime-specific behavior;
- framework-specific current details.

Those belong to official documentation, source inspection, or runtime testing.

If literature is not useful for the task, say so and do not manufacture a 10-book exercise.

## STEP 1 - SOURCE SET

When book audit is justified, identify:

A. Up to 5 highly regarded books directly relevant to the subject task.
B. Up to 5 highly regarded software architecture/design books relevant to the core architecture.

Use cross-source convergence rather than pretending that one universal ranking exists.

Prefer:
- established publishers;
- recognized authors and editions;
- recurring professional recommendations;
- strong relevance to the actual task;
- reader reputation only as supplementary evidence.

Do not select a book merely because it is famous.

For each selected book record:
- title;
- author;
- edition/year if relevant;
- why it is relevant to this project;
- source basis for selection.

## STEP 2 - EXTRACT ONLY APPLICABLE PRINCIPLES

For each book, extract only principles that could materially affect the implementation.

For every principle ask:

1. What project problem does this address?
2. Does the current plan already satisfy it?
3. Would applying it change the plan?
4. What concrete gain is expected?
5. What new complexity or risk would it add?
6. Is the principle too generic for this case?
7. Does it conflict with project source truth or governance?

Classify each literature-derived idea as:

ADOPT
ADAPT
REJECT
NOT_APPLICABLE
ALREADY_SATISFIED
UNVERIFIED_APPLICATION

Do not add an idea just to show that research was performed.

## STEP 3 - CROSS-SOURCE SYNTHESIS

Synthesize in this order:

1. Project source truth and governance.
2. Specialist AI feedback as hypotheses.
3. Web findings and primary external evidence.
4. Book and published-literature principles.
5. Senior engineering judgment.

Where sources conflict:
- state the conflict;
- identify which source is prioritized;
- explain why.

Books do not override:
- current project source truth;
- executable contracts;
- exact-version official documentation;
- validated runtime behavior;
- explicit human-approved governance.

## STEP 4 - ARCHITECTURE FITNESS CHECK

Audit the final plan against these questions:

- Is each module boundary based on ownership, cohesion, information hiding, or a distinct reason to change?
- Are policy and external tool details separated?
- Are expensive validation stages sequenced after cheaper failure detection where appropriate?
- Are behavior-preserving change and regression evidence explicit?
- Are architecture characteristics visible separately rather than hidden in one opaque score?
- Are quality goals expressed as concrete scenarios and validation conditions?
- Are external tools evidence producers rather than autonomous source mutators?
- Are uncertainty and disagreement preserved rather than averaged away?
- Are human approval and governance gates still explicit?

## STEP 5 - UPDATE THE PLAN

Only ADOPT and ADAPT findings may modify the plan.

For each accepted change record:

- Change ID
- Previous plan
- Updated plan
- Concrete benefit
- Source driver:
  - SPECIALIST_AI
  - WEB_PRIMARY_SOURCE
  - BOOK
  - PROJECT_GOVERNANCE
  - SENIOR_JUDGMENT
- Validation consequence
- Remaining uncertainty

## STEP 6 - FINAL OBJECTIVE PROPOSAL

State clearly:

- final recommended implementation approach;
- why it is preferred;
- what alternatives were rejected;
- what remains unverified;
- what must be inspected or tested before coding.

## STEP 7 - IMPLEMENTATION ROADMAP

Produce:

# How Deliver Project to AI Use

The roadmap must be detailed enough to implement without architectural guesswork.

At minimum cover:

1. feature objective;
2. non-goals;
3. source inspection requirements;
4. ownership and boundary proof;
5. public contracts;
6. dependency/runtime environment;
7. evidence model;
8. process/threading model;
9. adapters/integrations;
10. failure handling;
11. stale evidence and provenance;
12. persistence and cache ownership;
13. GUI/workflow integration;
14. module-boundary validation;
15. static validation;
16. targeted tests;
17. regression tests;
18. runtime/system validation;
19. adversarial verification;
20. human approval gate;
21. delivery;
22. installation;
23. validation;
24. Error Memory handling where applicable;
25. freeze Preview;
26. Confirm and Write.

## MODULE-SIZE RULE

Apply project module-size constraints only after logical boundaries are chosen.

- Hard maximum: below 500 physical lines for every touched/new source module.
- Ideal target: 400 code lines or fewer where practical.
- Do not create tiny wrapper modules only to satisfy line counts.
- Do not pad modules.
- Split by ownership, cohesion, information hiding, or independent change reason.
- Merge trivial modules into the nearest cohesive owner.

If the active project has a stricter lower-bound rule, preserve it as a delivery constraint without using it as the primary architecture algorithm.

## REQUIRED OUTPUT

1. SHOULD A BOOK AUDIT BE USED HERE?
2. SOURCE SET
3. RELEVANT PRINCIPLES BY BOOK
4. LITERATURE IDEA DECISION TABLE
5. SOURCE CONFLICTS AND PRIORITY
6. FINAL SYNTHESIZED IMPLEMENTATION LOGIC
7. ACCEPTED CHANGES AND THEIR SOURCE DRIVERS
8. FINAL OBJECTIVE PROPOSAL
9. HOW DELIVER PROJECT TO AI USE
10. REMAINING UNVERIFIED ITEMS

FINAL RULE

Literature should sharpen architecture, not create decorative complexity. Keep only ideas that materially improve this project.
