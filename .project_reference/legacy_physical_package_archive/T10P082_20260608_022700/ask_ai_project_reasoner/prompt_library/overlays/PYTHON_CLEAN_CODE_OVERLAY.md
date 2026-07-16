# PYTHON CLEAN CODE OVERLAY

Version: 1.0.0
Status: Reusable Python code-quality overlay
Prompt ID: python_clean_code_overlay
Prompt type: optional implementation overlay
Scope: Python source code generation, refactor, and repair work

## Purpose

Use this overlay when an AI is asked to generate, refactor, or repair Python code.

This overlay adapts Clean Code principles and Python best practices to Kanda
Reasoner work without overriding Kanda Bundle-Gated Development, box logic, or
local validation gates.

## Relationship to Kanda Bundle-Gated Development

Kanda Bundle-Gated Development answers:

```text
How do we safely deliver changes?
```

This overlay answers:

```text
How should Python code be written inside a safe bundle?
```

Use both for Python code bundles.

Do not use this overlay for text-only, governance-only, or handoff-only bundles
unless Python code is also being changed.

## Core rule

Write Python that is clear, maintainable, testable, and box-safe.

## Naming rules

Use intention-revealing names.

Prefer:

```text
build_safety_report
write_markdown_report
has_validation_errors
project_root
```

Avoid vague names unless the context is obvious:

```text
data
stuff
thing
manager
helper
```

Boolean names should usually start with:

```text
is_
has_
can_
should_
allow_
```

Classes should use nouns or noun phrases.

Functions should use verbs or verb phrases.

Avoid abbreviations that make code harder to search or read.

## Function rules

Functions should do one clear job.

Separate these concerns when practical:

```text
parse input
validate input
build data
format text
write files
call external services
coordinate GUI actions
```

Prefer small focused helpers over one large mixed function.

Avoid boolean flags that create separate workflows. If a flag switches between
two different workflows, split the behavior into two named functions.

Prefer separating query functions from command functions:

```text
builders return data or text
writers write files
validators return structured findings
GUI handlers coordinate and delegate
```

Small formatting flags are allowed when they improve clarity.

## Comments and docstrings

Prefer expressive code over comments.

Use comments to explain why a non-obvious decision exists, not to narrate what
the code already says.

Public modules, public classes, and public functions should have useful PEP 257
docstrings.

Private helpers may have docstrings when behavior is non-obvious.

Avoid noisy docstrings that only repeat the function name.

Long historical reasoning belongs in bundle manifests, governance notes, or
handoff documents rather than production code.

## Formatting rules

Use standard Python formatting:

```text
4 spaces for indentation
snake_case for functions and variables
PascalCase for classes
UPPER_SNAKE_CASE for constants
one import per line when clearer
standard library imports before third-party imports before local imports
```

Prefer readable line lengths.

Do not damage clarity only to satisfy a rigid line limit.

Use only ASCII text in generated Python files unless the project explicitly
allows otherwise.

## Error handling rules

Use specific exceptions.

Do not use bare except.

Catch only what can be handled.

When raising an exception, include useful context.

Do not silently swallow exceptions.

If recovery is impossible, re-raise or return a structured failure depending on
the caller contract.

Do not use None as a hidden error code. If None is a valid result, type it
explicitly and handle it explicitly.

## File and resource rules

Use context managers for file operations and resources.

Use explicit encoding for text files:

```python
path.read_text(encoding="utf-8")
path.write_text(text, encoding="utf-8", newline="\n")
```

When reading external or uncertain text, use explicit error handling only when
appropriate:

```python
errors="replace"
errors="ignore"
```

Do not use file writes inside pure builders.

## Class and module rules

Classes should have one clear reason to change.

If a class mixes UI, domain logic, file IO, and validation, split it by
responsibility.

Avoid deep inheritance trees unless they are already part of the project design.

Prefer composition and small adapters.

Use architecture validation and focused tests to decide when a split is needed.

## Boundary and dependency rules

Respect Kanda box logic.

GUI modules may call service modules.

Service modules should not import GUI modules.

External systems should be wrapped behind adapters when practical:

```text
local AI bridge
file-system writer
runtime trace reader
prompt-library catalog reader
```

Pass important dependencies explicitly:

```text
project_root
config
output_dir
adapter
clock
```

Avoid hidden global state.

Local imports are allowed when they protect startup safety, optional
dependencies, or box boundaries. Explain the reason when it is non-obvious.

## Test rules

Every code bundle should include focused tests.

Prefer fast, deterministic, local tests.

Use one behavior per test.

Multiple assertions are allowed when they validate the same behavior.

Use Arrange, Act, Assert structure where practical.

Test edge cases when they matter:

```text
empty inputs
missing files
invalid JSON
paths outside project root
duplicate identifiers
failed writes
```

Do not add network calls or slow external dependencies to unit tests.

## Type hint rules

Use Python 3.10+ type hints for public functions, dataclasses, and class
attributes when practical.

Use standard-library typing.

Avoid over-engineered type systems.

Use dataclasses for structured records when many related values travel together.

## Kanda-specific source rules

For Kanda Reasoner work:

```text
respect active box ownership
preserve public import paths
prefer compatibility facades for structural moves
keep runtime code out of text-only prompt bundles
write reports/drafts under workbench when appropriate
include focused tests in code bundles
run architecture and workflow validation locally
```

## Soft rules, not rigid law

The following are useful signals, not absolute bans:

```text
short parameter lists are better than long ones
boolean flags can be a smell
large classes need scrutiny
deep object navigation can reveal boundary leakage
long lines can reduce readability
```

Do not create artificial abstractions just to satisfy a numeric rule.

## Output expectation for AI code generation

When this overlay is loaded, generated Python should include:

```text
clear file purpose
focused public API
useful docstrings
type hints for public functions
explicit exception behavior
focused tests when part of a bundle
install and validation commands when delivering a bundle
```

## Non-goals

This overlay does not replace:

```text
Kanda Bundle-Gated Development
architecture validation
workflow validation
governance freeze protocol
manual GUI validation
```

This overlay does not authorize automatic production source modification.

## Final reminder

Readable, boring, explicit Python is preferred over clever Python.
