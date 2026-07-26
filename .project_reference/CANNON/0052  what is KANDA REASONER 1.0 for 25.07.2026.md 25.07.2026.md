KANDA Reasoner is a local Windows workbench for using AI to understand and modify software projects more safely.

It is not just a chatbot and not simply a code editor. Its main purpose is to put a governance and validation layer between an AI model and your project files.

In practical terms

Suppose you have a large Python project and ask:

“Fix this error without breaking the rest of the application.”

A normal AI assistant may read a few files, suggest code, and hope the change works.

KANDA Reasoner is intended to help organize the complete process:

Understand the project
-> locate the correct files and owners
-> select the appropriate AI instructions
-> plan the change
-> prepare a controlled preview or patch
-> validate it
-> review the differences
-> apply it only through an authorized path
-> record the error and preserve validated behavior
Its main functions
1. Understand a software project

KANDA can collect and organize information about a project, including:

Source files and folders.
Python symbols and dependencies.
Architecture and module boundaries.
Workflows.
Validation state.
Relevant previous errors.
Project-specific instructions.

Features such as Project Q&A, Brain Navigator, Architecture Review, Workflow Review, and project-structure visualization are different ways of examining the same project.

The Project Q&A component is specifically described as an evidence-grounded, read-only question-and-answer tool for the selected project.

2. Give an AI the correct project context

KANDA maintains:

A prompt library.
Prompt-routing rules.
Project handoff packages.
Source archives.
Compact Error Memory.
Validation and architecture evidence.

This helps prevent the AI from answering based only on a vague description or a small random selection of files.

For example, KANDA can package a structured project handoff that another AI reads before inspecting the exact source files.

3. Prevent the AI from changing the wrong thing

A central KANDA rule is the separation between:

KANDA Reasoner as the reusable tool, and
the software project being analyzed or modified.

The tool owns analyzers, validators, GUI tabs, prompt machinery, and reusable workflows. The selected project owns its source code, generated modules, validation evidence, Error Memory, and Freeze Memory.

This is especially important because KANDA can analyze itself. Even when the tool and the active project occupy the same physical folder, their logical ownership must remain separate.

4. Enforce architectural boundaries

KANDA organizes responsibilities into bounded “boxes.”

Each box should have:

One clear responsibility.
Known owner files.
A public contract.
Defined inputs and outputs.
A specific validator.
Files and responsibilities it is forbidden to invade.

Its No-Leak rules are designed to prevent:

Writing into the wrong project.
Mixing reusable tool code with project-specific state.
One subsystem reaching into another subsystem’s private internals.
Temporary files becoming permanent truth.
Generated reports being mistaken for source code.
Old asynchronous results changing a newer task.
5. Make changes through a controlled workflow

The intended model is not:

AI writes directly into project

It is closer to:

Read
-> analyze
-> plan
-> preview
-> validate
-> authorize
-> write
-> verify
-> record

KANDA’s architecture calls this a card-machine model: the project owns the selected module, while KANDA temporarily reads and processes it without becoming its owner.

6. Remember previous failures

Error Memory records real mistakes and their prevention rules.

Examples from the current project include:

Wrong Python interpreter selection.
QWebEngine readiness failures.
Qt callbacks reaching deleted widgets.
Invalid freeze-intake sequencing.
Release-helper path mismatches.
AI-generated commands using invalid Windows path formatting.

The purpose is not merely to document errors. It is to stop future changes from repeating them.

7. Preserve validated behavior

Freeze Memory records features or behaviors that have been validated and deliberately preserved.

The AI can prepare freeze information, but KANDA keeps Preview read-only and requires explicit human confirmation before writing governed freeze memory.

This prevents an AI from silently declaring its own change correct.

8. Work with both local and online AI

KANDA has facilities for:

Local AI through Ollama.
Web AI providers.
Prompt routing.
Project-specific context assembly.
Project Q&A.

The intended separation is:

Browser ChatGPT: currently useful as your development partner for architecture, patches, ZIP creation, debugging, and complex implementation work.
KANDA Reasoner: your local project workbench for loading project context, routing prompts, running analysis, preserving evidence, and interacting with configured AI models.

A future local coding-agent workflow can edit and test code in an isolated workspace, but that requires additional bounded tooling and should not be confused with the existing read-only Project Q&A feature.

A concrete example

Imagine KANDA is analyzing another Python application.

You ask:

“Split this 1,200-line module without breaking its public API.”

KANDA should help:

Identify the selected project and module.
Determine which architecture box owns it.
Inspect callers and dependencies.
Retrieve relevant prompt and Error Memory guidance.
Prepare a refactoring plan.
Create a preview in an isolated workbench.
Show the exact multi-file diff.
Run focused validators.
Require human approval.
Apply the approved change.
Verify the installed result.
Record evidence and optionally freeze the validated behavior.
The simplest definition

KANDA Reasoner is a governed AI software-engineering workbench.

Its value is not that it makes an AI smarter in the abstract.

Its value is that it tries to make AI-assisted coding:

More informed.
More structured.
More traceable.
Less likely to edit the wrong files.
Less likely to repeat known mistakes.
Less likely to declare success without validation.

The long-term professional goal is for a developer who did not create KANDA to install it, select a project, understand the project, use AI safely, validate changes, and operate it without needing the original chat history.