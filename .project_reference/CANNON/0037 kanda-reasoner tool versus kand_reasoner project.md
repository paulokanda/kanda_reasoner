# HANDOFF: KANDA Reasoner Tool vs KANDA Reasoner Project Boundary

## Purpose of this handoff

This handoff explains a critical boundary rule for all KANDA Reasoner work.

KANDA Reasoner has two identities that must never be confused:

1. **KANDA Reasoner as the tool**
2. **KANDA Reasoner as the active project currently being edited**

Sometimes we are working on KANDA Reasoner itself. In that situation, the same repository may appear to be both the tool and the project. Even then, the AI must preserve the distinction between tool-owned logic and project-owned source/output.

This distinction is mandatory before editing code, creating files, generating patches, writing validation scripts, refactoring modules, or producing freeze/handoff artifacts.

---

## 1. KANDA Reasoner as the tool

KANDA Reasoner as the tool is the reusable system that helps build, inspect, refactor, validate, patch, document, and maintain code projects.

Tool-owned files are reusable application logic. They belong to the KANDA Reasoner tool/runtime, not to the selected project output.

Examples of tool-owned logic:

* Architecture Review GUI tabs
* Large File Refactor Planner GUI
* large-module analyzers
* AST or LibCST refactor engines
* code analyzers
* import rewriters
* docstring insertion engines
* prompt routers
* validation generators
* patch creation tools
* freeze-prep tools
* handoff generators
* Error Memory tools
* startup delivery generators
* project collectors
* path resolvers
* no-leak validators
* box/shielding validators

In short:

**If the code performs reusable work on projects, it belongs to the KANDA Reasoner tool.**

Example:

A module that analyzes a selected Python file and proposes a safe split into helper modules is tool-owned.

A module that inserts missing docstrings into selected source files is tool-owned.

A GUI tab that lets the user preview a refactor plan is tool-owned.

A validator that checks whether the proposed split preserves public API and avoids circular imports is tool-owned.

---

## 2. KANDA Reasoner as the project

KANDA Reasoner as the project is the active selected codebase being edited. In many sessions, the selected project is KANDA Reasoner itself, but it must still be treated as a project target when the task is modifying its project source.

Project-owned files are the actual source files, generated output files, helper files, reports, previews, freeze records, or validation artifacts that belong to the active project being worked on.

Examples of project-owned files:

* selected source file being refactored
* split/refactored modules produced for that selected project
* project-specific helper modules generated as the result of a refactor
* project-specific validation evidence
* project-specific freeze hints
* project-specific handoff output
* project-specific Error Memory intake
* project-specific preview files
* project-specific generated documentation
* project-specific temporary work output

In short:

**If the file is the result or target of work on a selected project, it belongs to the active project.**

Example:

If the tool refactors `large_module.py` from the active project into:

* `large_module.py`
* `_large_module_analysis.py`
* `_large_module_validation.py`
* `_large_module_io.py`

those output files belong to the active project, not to the reusable tool layer.

---

## 3. The key distinction

The same repository can contain tool logic and project source, especially when the active project is KANDA Reasoner itself.

Therefore, the AI must not decide ownership only by repository path or project name.

The AI must classify by responsibility.

### Tool-owned

A file is tool-owned when it implements reusable machinery that can operate on any project.

Examples:

* refactor planner engine
* refactor planner GUI
* docstring generator engine
* import migration engine
* AST/CST symbol analyzer
* architecture validator
* patch builder
* startup delivery generator

### Project-owned

A file is project-owned when it is the selected project source or a generated result for that selected project.

Examples:

* the actual module being split
* the generated split helper files
* project-specific preview output
* project-specific patch payload
* project-specific validation evidence
* project-specific freeze hint

---

## 4. Concrete example: Large File Refactor Planner

We are planning a new Architecture Review sub-tab for refactoring large Python files.

This feature must follow the tool/project boundary.

### Tool side

These belong to KANDA Reasoner as the reusable tool:

* the Architecture Review sub-tab UI
* the Large File Refactor Planner controller
* AST analysis code
* LibCST transformation code
* import rewrite engine
* dependency graph builder
* circular import validator
* docstring detection/generation engine
* local LLM arbitration wrapper
* preview generator
* validation runner
* patch ZIP builder
* no-leak gate

### Project side

These belong to the active selected project:

* the selected large source file
* generated split/refactored source files
* generated project helper files
* generated docstrings inserted into project code
* refactor preview files
* patch payload files for that project
* validation evidence for that project
* freeze hint for that project

### Critical rule

The refactor engine belongs to the tool.

The refactored output belongs to the project.

Do not put reusable refactor-engine code inside project output.

Do not put project-specific split files inside reusable tool source unless the selected project source itself is being intentionally patched.

---

## 5. Box Logic, Shielding Logic, and No-Leak Logic

The AI must use three related safety concepts before implementation.

### Box Logic

Box Logic asks:

* What box owns this file?
* What is the active box?
* What are the owner paths?
* Which files are allowed?
* Which files are out of scope?
* Are there cross-box touches?
* What public contracts are involved?
* What validation scope is needed?
* What boundary risks exist?

### Shielding Logic

Shielding Logic protects each box from accidental invasion.

It prevents:

* editing neighboring boxes without routing
* importing private internals from another box
* mixing UI logic with domain logic
* mixing validation logic with runtime logic
* changing generated artifacts instead of source truth
* bypassing public contracts
* bypassing confirmation gates

### No-Leak Logic

No-Leak Logic is a named first-class object inside Box Logic and Shielding Logic.

Use the name:

**NO_LEAK_LOGIC_V1**

No-Leak Logic prevents ownership, path, state, contract, evidence, and responsibility from leaking across boxes.

It specifically blocks:

1. tool/project leakage
2. wrong-root writes
3. cross-box leakage
4. private reach-in
5. public API ownership leakage
6. hidden mutable state leakage
7. generated-artifact-as-source leakage
8. validation/freeze evidence leakage
9. prompt/canon leakage
10. refactor-output leakage

---

## 6. Required NO-LEAK CHECK before coding

Before any implementation, refactor, patch, validation script, generated file, startup update, or freeze-ready work, the AI should output or internally complete this check:

```text
NO-LEAK CHECK

Active box:
Tool-owned files:
Project-owned files:
Project-specific support files:
Generated/evidence files:
Temporary daily-work files:
External boxes touched:
Out-of-scope files:
Leak risks:
Blocked writes:
Safe next action:
```

If any answer is uncertain, do not patch from memory. Inspect the actual source, routing manifest, prompt, path resolver, or validation context.

---

## 7. Required BOX CHECK before implementation

Before implementation, the AI should also complete:

```text
BOX CHECK

Task type:
Active box:
Owner path:
Allowed files:
Out-of-scope files:
Cross-box touches:
Public contracts:
Validation scope:
Boundary risks:
Tool/project ownership risk:
No-leak risk:
May proceed:
Next safe action:
```

If the task changes architecture, startup delivery, prompt-library canons, freeze behavior, patch delivery, validation behavior, GUI behavior, or project/tool path ownership, treat it as governed work.

---

## 8. Wrong patterns to avoid

### Wrong pattern 1: Treating KANDA Reasoner as always the project

Bad:

```text
All generated files go under E:\kanda_reasoner because the tool is KANDA Reasoner.
```

Correct:

```text
Generated project files go under the selected active project root.
Reusable tool logic goes under the KANDA Reasoner tool source.
```

### Wrong pattern 2: Treating generated output as source truth

Bad:

```text
Modify generated startup ZIP contents directly as if they are canonical source.
```

Correct:

```text
Modify canonical prompt/source files and regenerate generated delivery artifacts.
```

### Wrong pattern 3: Putting reusable refactor logic into project output

Bad:

```text
Generated split project helper files include the reusable refactor planner engine.
```

Correct:

```text
The refactor planner remains tool-owned. The project receives only the selected project's refactored source output.
```

### Wrong pattern 4: Hardcoding KANDA Reasoner as every target project

Bad:

```text
Write support files to E:\kanda_reasoner_show_project_to_AI for every project.
```

Correct:

```text
Use the selected active project root and derive:
<project_drive>\<active_project_slug>_show_project_to_AI
<project_drive>\<active_project_slug>_delete_after_daily_work
```

### Wrong pattern 5: Letting helper modules accidentally own facade API

Bad:

```text
A private helper module exports the same public symbol as the facade.
```

Correct:

```text
The facade owns public compatibility. Helpers stay private unless a governed architecture change says otherwise.
```

---

## 9. File ownership rules for refactoring work

When implementing a refactor feature, classify every file.

### Reusable refactor system files

These are tool-owned:

```text
large_file_refactor_planner.py
_large_file_refactor_analysis.py
_large_file_refactor_partition.py
_large_file_refactor_imports.py
_large_file_refactor_validation.py
_large_file_refactor_docstrings.py
_large_file_refactor_llm.py
architecture_review_large_file_refactor_tab.py
validation/test_large_file_refactor_planner_v1.py
```

### Refactored project output files

These are project-owned:

```text
selected_module.py
_selected_module_analysis.py
_selected_module_imports.py
_selected_module_validation.py
_selected_module_docstrings.py
```

Only generate these under the active selected project path or its preview/daily-work area.

---

## 10. Special rule when KANDA Reasoner is both tool and project

When the active selected project is KANDA Reasoner itself, the AI must be extra careful.

The same physical repository may contain:

1. tool code being enhanced
2. project code being refactored
3. generated support files
4. temporary daily-work files
5. freeze/handoff evidence

Do not assume everything in the repository has the same ownership.

Classify by responsibility:

```text
Is this reusable system machinery?
Then it is tool-owned.

Is this the selected source being changed or generated output for that source?
Then it is project-owned.

Is this freeze, validation, handoff, or preview state?
Then it is project-specific support/evidence.

Is this temporary installation or patch staging material?
Then it belongs in _delete_after_daily_work.
```

---

## 11. Startup and retrieval guidance for future chats

At the beginning of future chats, after loading startup files, the AI should look for or request these concepts if needed:

* Box Logic Startup Bridge
* No-Leak Logic Bridge
* box_architecture_canon.md
* kanda_box_shielding_canon.md
* project_tool_boundary_canon.md
* patch delivery guardrails
* active project freeze context
* compact Error Memory
* project handoff routing manifest
* source archive only when exact source inspection is needed

If the user asks to implement or patch code, the AI must not rely only on this handoff. It must inspect the actual source files first.

This handoff defines the rule. Source files define the implementation truth.

---

## 12. How this applies to the planned Large File Refactor Planner

The planned feature is:

```text
Architecture Review
  -> Large File Refactor Planner
```

The safest design is:

```text
1. proposal-first
2. preview-only before write
3. LibCST-backed for formatting-preserving edits
4. AST-backed for fast analysis
5. dependency-graph validated
6. public API preserving
7. docstring completion included
8. local LLM only for bounded semantic decisions
9. no direct auto-apply in v1
10. patch ZIP only after validation
```

The planner should include a Docstring Completion stage.

It should detect missing docstrings for:

* modules
* public classes
* public functions
* public methods
* complex private helpers when needed

It should propose docstrings in preview and never silently overwrite existing docstrings.

The generated docstrings belong to the selected project source because they are inserted into project code.

The docstring generation engine belongs to the KANDA Reasoner tool.

---

## 13. Final compact rule

Use this sentence as the shortest version:

**KANDA Reasoner as a tool owns reusable machinery; the active project owns selected source files and generated project outputs. Even when the active project is KANDA Reasoner itself, every file must be classified by responsibility before writing. Apply Box Logic, Shielding Logic, and NO_LEAK_LOGIC_V1 to prevent tool/project leakage, wrong-root writes, cross-box leakage, private reach-in, public API leakage, generated-artifact leakage, and validation/freeze evidence leakage.**

KANDA Reasoner as a tool owns reusable machinery; the active selected project owns selected source files and generated project outputs.