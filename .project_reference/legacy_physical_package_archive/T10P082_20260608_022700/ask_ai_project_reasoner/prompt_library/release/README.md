# Prompt Library Release Folder

This folder contains text-only release and freeze documentation for the Prompt
Engineering Library.

The Prompt Engineering Library is an isolated text library. It stores reusable
project-agnostic prompts, prompt templates, metadata templates, overlays,
profiles, QA checklists, and pack/export guidance.

This folder does not contain Python code. It does not modify project source code.
It does not update active governance. It does not change Tabs 1 through 8.

## Files in this folder

- TEXT_LIBRARY_RELEASE_SUMMARY.md
- TEXT_LIBRARY_SCOPE_FREEZE.md
- TEXT_LIBRARY_FREEZE_HANDOFF.md
- FUTURE_TAB9_GUI_PHASES.md

Each main file has a matching `.meta.json` sidecar where appropriate.

## Allowed use

Use this folder to understand:

- what the text-only library contains;
- what is frozen;
- what is not yet implemented;
- what the next safe implementation phase would be;
- how future Tab 9 GUI work must remain separated from source patching and governance editing.

## Forbidden use

Do not use these files to:

- edit source code;
- modify active governance;
- run a freeze automatically;
- change runtime behavior;
- change Tabs 1 through 8;
- claim that a GUI Tab 9 exists before it is implemented.
