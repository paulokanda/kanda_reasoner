# Project-Agnostic Delivery Planning Template

Version: 2.0.0
Status: draft-only reusable template
Authority: none

## Purpose

Help an external software project describe a cautious delivery plan when no
project-specific delivery canon exists. Project-specific governance always
wins. This template cannot authorize implementation, installation, validation,
or freeze.

## Required adaptation variables

```text
<PROJECT_ROOT>
<PROJECT_NAME>
<TASK_DESCRIPTION>
<TASK_SLUG>
<SOURCE_FILES>
<VALIDATION_COMMANDS>
<DELIVERY_METHOD>
```

Do not use the template until every placeholder has been replaced and current
source has been inspected.

## Planning sequence

```text
inspect current source
-> classify risk and ownership
-> choose the smallest intervention
-> define changed and out-of-scope files
-> define validation and rollback
-> use the project's approved delivery method
-> disclose what was and was not executed
-> wait for local acceptance
```

## Boundaries

- Never hardcode a project path or assume direct ZIP extraction is safe.
- Never prohibit an installer when project governance requires one.
- Never treat generated artifacts as canonical source.
- Never claim exhaustive testing without actual execution evidence.
- Never use this template to override KANDA Reasoner governance.
