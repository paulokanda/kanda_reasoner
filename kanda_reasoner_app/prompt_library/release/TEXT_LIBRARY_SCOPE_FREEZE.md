# Text-Only Prompt Library Scope Freeze

Version: 1.0.0
Status: Frozen scope statement
Scope: Text-only Prompt Engineering Library

## Frozen rule

The Prompt Engineering Library is an isolated text-only library.

It stores reusable prompts and prompt-supporting documents for the user to copy,
assemble, review, or present to an AI.

It does not change code.

## Allowed file types

The text-only library may contain:

```text
.md
.txt
.json
```

## Forbidden file types for this text-only scope

Do not add these under the text-only library without a later approved phase:

```text
.py
.pyw
.ps1
.bat
.exe
.dll
.pyd
```

## Allowed folders

The current approved library folders are:

```text
kanda_reasoner_app\templates\prompt_library_templates\
kanda_reasoner_app\prompt_library\
kanda_reasoner_app\prompt_library\active\
kanda_reasoner_app\prompt_library\metadata\
kanda_reasoner_app\prompt_library\stacks\
kanda_reasoner_app\prompt_library\profiles\
kanda_reasoner_app\prompt_library\overlays\
kanda_reasoner_app\prompt_library\packs\
kanda_reasoner_app\prompt_library\qa\
kanda_reasoner_app\prompt_library\release\
```

## Not part of active project reference storage

The prompt library was intentionally relocated out of:

```text
_project_reference\
```

Reason:

```text
_project_reference is reference material and may be excluded from normal project
analysis. The prompt library is part of the developer_tools product package and
must be discoverable later by package-owned Tab 9 logic.
```

## No governance bypass

The Prompt Engineering Library may contain governance-related prompt templates
as text. It must not modify active governance files.

Governance updates remain separate and require explicit user approval,
validated evidence, and the official governance workflow.

## No runtime side effects

Reading, copying, or editing prompt text must not:

- change source files;
- run project analysis;
- change runtime artifacts;
- change cached evidence;
- change active governance;
- modify Tabs 1 through 8;
- load prompts automatically into an AI bridge.

## Future change rule

Any future code, GUI, validation, or engine support for this library must be a
new gate with a new roadmap. It must preserve this text-only scope unless the
user explicitly approves a scope expansion.
