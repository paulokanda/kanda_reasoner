# Future Tab 9 GUI Phases

Version: 1.0.0
Status: Future-only planning document
Scope: Not implemented

## Purpose

This document lists possible future phases for turning the text-only Prompt
Engineering Library into a real Tab 9 GUI.

It is not implementation authorization.

## Phase G0 - Roadmap only

Create a roadmap for a read-only Tab 9 GUI.

No code.

The roadmap must define:

- owner box;
- source files needed;
- GUI integration point;
- files not to touch;
- validation gates;
- rollback plan;
- manual GUI checklist.

## Phase G1 - Read-only viewer

Possible features:

- list prompt library folders;
- show prompt files;
- show metadata;
- show Explain text;
- show How It Works text;
- show Files Created text;
- copy prompt text to clipboard;
- open file location.

Forbidden in G1:

- editing;
- saving;
- deleting;
- promotion;
- governance writes;
- runtime prompt injection.

## Phase G2 - Draft editor

Possible features:

- create draft from existing prompt;
- save draft under prompt library drafts;
- compare draft vs active prompt;
- copy draft to clipboard.

Forbidden in G2:

- overwrite active prompts directly;
- write active governance;
- change source code.

## Phase G3 - Validator

Possible features:

- validate metadata fields;
- detect hardcoded paths;
- check project-agnostic placeholders;
- check required sections;
- show validation results.

Forbidden in G3:

- automatic correction without user review;
- source code edits;
- governance edits.

## Phase G4 - Stack builder

Possible features:

- select prompts;
- assemble prompt stack;
- insert adaptation variables;
- copy final stack to clipboard;
- export stack as text.

Forbidden in G4:

- automatic prompt execution;
- AI bridge integration without separate approval;
- runtime behavior changes.

## Phase G5 - Controlled active library operations

Possible features:

- promote draft to active prompt;
- archive active prompt;
- export prompt pack.

Required before G5:

- separate roadmap;
- explicit user approval;
- validation rules;
- backup behavior;
- no governance bypass.

## Final future rule

Every future phase must preserve the text-only library as the source of prompt
reference truth. GUI and engine code may inspect the library, but must not make
it a hidden runtime dependency without a separate approved integration contract.
