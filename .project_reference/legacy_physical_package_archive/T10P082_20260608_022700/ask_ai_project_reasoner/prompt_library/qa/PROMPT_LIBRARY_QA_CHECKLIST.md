# Prompt Library QA Checklist

Version: 1.0.0
Status: Text-only manual QA checklist
Use: Review the prompt library before using or exporting prompts.

## Purpose

This checklist verifies that the prompt library is usable, organized,
project-agnostic, and safe to copy into an AI session.

## Review Status

- Reviewer: <REVIEWER_NAME>
- Project: <PROJECT_NAME>
- Date: <YYYY-MM-DD>
- Prompt library root: <PROJECT_ROOT>\kanda_reasoner_app\prompt_library

## Structure Checks

- [ ] active folder exists.
- [ ] metadata folder exists.
- [ ] stacks folder exists.
- [ ] profiles folder exists.
- [ ] overlays folder exists.
- [ ] packs folder exists.
- [ ] qa folder exists.
- [ ] README files explain each folder purpose.

## Prompt Checks

- [ ] Every active prompt has a clear name.
- [ ] Every active prompt has a matching .meta.json file.
- [ ] Every prompt has a version.
- [ ] Every prompt has a purpose section.
- [ ] Every prompt has a project-agnostic contract.
- [ ] Every prompt lists required inputs.
- [ ] Every prompt states output contract.
- [ ] Every prompt states safety boundaries.
- [ ] Every prompt states validation expectations.
- [ ] Every prompt has a change log.

## Copy and Use Checks

- [ ] The prompt can be copied without hidden dependencies.
- [ ] Required adaptation variables are clear.
- [ ] The prompt tells the AI what evidence it needs.
- [ ] The prompt does not ask the AI to implement from memory.
- [ ] The prompt separates roadmap, implementation, handoff, and governance.

## Safety Checks

- [ ] No prompt silently edits active governance.
- [ ] No prompt silently changes source code.
- [ ] No prompt claims exhaustive testing without evidence.
- [ ] No prompt hardcodes a project root outside examples.
- [ ] No prompt uses a fixed package name outside examples.
- [ ] No prompt treats examples as source truth.

## Result

- [ ] PASS - Ready to use.
- [ ] FAIL - Needs correction.
- [ ] PARTIAL - Safe for reference only.

## Notes

<QA_NOTES>
