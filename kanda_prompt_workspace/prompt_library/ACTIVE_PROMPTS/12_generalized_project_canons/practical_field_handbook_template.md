---
prompt_id: practical_field_handbook_template
prompt_code: KPR-12-008
title: Practical Field Handbook Template
version: 2.0.0
status: active_template
load_type: on_request
owner_box: 12_generalized_project_canons
classification: source_grounded_handbook_generation_template
source_stage: prompt-audit-wave8a-human-handbook-reclassification-v1
---

# Practical Field Handbook Template

## Purpose

Use this template to turn a supplied or reliably identified book, paper,
framework, standard, specification, or technical reference into a practical,
audience-specific handbook.

The handbook must distinguish source-derived content from user-provided context,
modern commentary, and implementation suggestions. It must not invent chapter
content, citations, edition details, quotations, or current best practices.

## Required inputs

Collect or visibly mark these fields:

```text
TITLE:
AUTHOR OR ISSUING BODY:
SOURCE TYPE:
EDITION / VERSION / PUBLICATION DATE:
SOURCE ACCESS MODE:
AUDIENCE:
USER LEVEL:
USER CONTEXT:
DESIRED DEPTH:
OUTPUT CONSTRAINTS:
```

Use one `SOURCE ACCESS MODE`:

- `FULL_SOURCE_SUPPLIED` — the relevant source text is available in the current
  context;
- `VERIFIED_REFERENCE_AVAILABLE` — a reliable reference can be consulted and
  cited;
- `USER_SUMMARY_ONLY` — only the user's summary or notes are available;
- `SOURCE_UNAVAILABLE` — the source cannot be inspected or verified.

Do not silently upgrade one mode to another.

## Source and edition identity

Record the exact work, edition, version, translation, publication date, or
standard revision when known. Distinguish similarly titled works and later
revisions.

If identity is uncertain, ask for the smallest missing identifier or proceed
with a clearly labeled limited handbook. Never fabricate a table of contents,
chapter sequence, quotation, or page reference.

## Provenance labels

Use these labels where provenance matters:

- `SOURCE-DERIVED` — supported by the supplied or verified source;
- `USER-PROVIDED` — supplied by the user and not independently verified;
- `MODERN COMMENTARY` — current interpretation or later practice;
- `IMPLEMENTATION SUGGESTION` — context-dependent advice, not source text;
- `UNKNOWN` — evidence is insufficient.

A modern example must not be presented as though it appeared in the original
work.

## Copyright-safe synthesis

Summarize and transform rather than reconstructing the work. Do not reproduce
long passages, a substitute chapter-by-chapter copy, proprietary exercises, or
an extensive sequence of quotations.

Use short quotations only when necessary and within applicable limits. Prefer
paraphrase, synthesis, comparison, and practical application. When the user
requests a near-complete substitute for a copyrighted work, provide a bounded
summary or study guide instead.

## Missing-source behavior

### FULL_SOURCE_SUPPLIED

You may organize the supplied material, summarize it, map concepts, and build
practical exercises while preserving source identity.

### VERIFIED_REFERENCE_AVAILABLE

Verify important factual and edition claims, cite the consulted sources, and
separate the original work from later commentary.

### USER_SUMMARY_ONLY

Build from the user's notes only. Label source claims as user-provided and avoid
claiming completeness or chapter-level fidelity.

### SOURCE_UNAVAILABLE

Do not pretend to know the work in detail. Offer one of:

- a generic handbook framework awaiting the source;
- a limited high-level orientation based on clearly identified knowledge;
- a request for the relevant excerpt, table of contents, notes, or exact
  edition.

## Adaptive handbook structure

Select only the sections supported by the source and the user's goal. Possible
sections include:

1. audience and use case;
2. one-paragraph thesis;
3. concept or dependency map;
4. source-grounded section notes;
5. practical rules and decision points;
6. examples adapted to the user's domain;
7. context-dependent advice and exceptions;
8. misconceptions and failure modes;
9. daily checklist or quick-reference table;
10. adoption or practice plan;
11. modern developments since publication;
12. companion resources with reasons;
13. provenance and limitations.

Do not invent a chapter-by-chapter structure when the source or table of
contents is unavailable. Do not force a 30-day plan, a fixed number of concepts,
or a fixed number of anti-patterns when the request does not support them.

## Evidence and current-practice rules

When describing current tools, standards, laws, security practices, APIs,
versions, or recommendations, verify them when current accuracy matters. Cite
reliable sources when available.

Separate:

- what the original source says;
- what later evidence or practice changed;
- what is a context-dependent implementation recommendation;
- what remains uncertain.

Do not claim that an example is current merely because the current year was
inserted into the prompt.

## Examples and implementation advice

Examples must match the stated audience and domain. Use realistic names and
state assumptions. Keep examples minimal enough to teach the concept.

Implementation suggestions remain advisory. Route actual source changes,
packages, terminal commands, validation evidence, and freeze work to their
current owners.

## Long-output behavior

Plan the response so each delivered section is complete. When the requested
handbook cannot fit comfortably, provide a coherent first part and state the
remaining sections. Continue only in the current interaction when the user asks
for continuation. Do not claim unseen sections are already complete.

## Required closing record

End a substantial handbook with:

```text
SOURCE ACCESS MODE:
SOURCE / EDITION IDENTITY:
SOURCE-DERIVED COVERAGE:
MODERN COMMENTARY INCLUDED:
IMPORTANT LIMITATIONS:
```

## Non-authorization statement

This template creates educational or operational guidance. It does not authorize
source mutation, package delivery, validation claims, or freeze.
