# PROMPT LIBRARY QUICK START

Version: 1.0.0
Status: User-facing quick start
Scope: Tab 9 text-only Prompt Library

## What This Library Does

This library stores prompts that you can copy and present to an AI.

It is not a code editor and does not change source code.

## Fastest Use

1. Open the stack file:

```text
kanda_reasoner_app\prompt_library\stacks\GENERAL_PROJECT_DAILY_PROMPT_STACK.md
```

2. Copy the stack.
3. Replace placeholders such as:

```text
<PROJECT_ROOT>
<PROJECT_NAME>
<PRODUCT_PACKAGE>
<TASK_DESCRIPTION>
```

4. Paste the stack into an AI session.
5. Attach current source files, logs, and validation output when needed.

## How To Create A New Prompt

1. Open:

```text
kanda_reasoner_app\templates\prompt_library_templates\PROMPT_TEMPLATE_BLUEPRINT.md
```

2. Copy the template.
3. Fill the adaptation variables.
4. Save the new prompt under:

```text
kanda_reasoner_app\prompt_library\drafts\
```

5. Create a matching .meta.json file under:

```text
kanda_reasoner_app\prompt_library\metadata\
```

## Safe Rule

A prompt in this library prepares instructions for an AI. It does not apply the
instructions by itself.
