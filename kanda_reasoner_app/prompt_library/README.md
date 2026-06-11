# Prompt Library

Status: Text-only library structure
Scope: Developer tools prompt storage and retrieval

This folder stores project-agnostic prompts that the user can inspect, copy,
assemble, export, and present to an AI.

Tab 9 rule:
- Tab 9 is an isolated text-library box.
- Tab 9 does not change project source code.
- Tab 9 does not edit Python files.
- Tab 9 does not modify Tabs 1 through 8.
- Tab 9 does not write active governance.
- Tab 9 does not execute prompts automatically.

Folder roles:
- active: library-selected prompts ready for manual copy or stack assembly.
- drafts: working prompt drafts; all edits start here.
- metadata: prompt sidecar metadata files.
- exports: generated prompt packs or copied prompt stacks.
- archive: retired prompt versions kept for traceability.
- usage: optional text or JSONL usage notes.
- profiles: per-project prompt library profiles.
- stacks: assembled prompt stacks for manual copy.
- imports: staging area for imported prompt packs before review.

Important distinction:
active prompts in this library are reference-active only. They are not
automatically loaded into runtime behavior. The user decides which prompt or
prompt stack to copy and present to an AI.

Project-agnostic rule:
Reusable prompts should use placeholders such as <PROJECT_ROOT>,
<PROJECT_NAME>, <PRODUCT_PACKAGE>, and <TASK_DESCRIPTION>. Project-specific
examples must be clearly marked as examples.
