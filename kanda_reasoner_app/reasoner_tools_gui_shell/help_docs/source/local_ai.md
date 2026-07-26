# Local AI

First-Time User Tutorial

Local AI lets you ask questions about the selected project using a model that runs through the configured local AI service. The tab combines project analysis, project JSON evidence, conversation memory, quick questions, source references, prompt inspection, and runtime logs in one place.

![Local AI opener](../assets/drawings/local_ai_opener_private_reference_desk.png)

Image note:

- Subject: Local AI as a private project reference desk.
- Asset path: `assets/drawings/local_ai_opener_private_reference_desk.png`.
- Alt text: An engineer and a private AI assistant review organized project folders, diagrams, and question-and-answer evidence at a quiet reference desk.
- Caption: Select the correct project evidence first, then ask the local model one focused question.
- Artwork status: `primary_contextual_local_ai_raster`.

## What Local AI Means

Local AI is an AI model connected through the KANDA local-model configuration.

It is designed to answer questions using project information that KANDA has loaded or generated.

**In plain English:** Local AI is like a private assistant sitting beside your project files. It can explain what it sees, but it does not automatically know the entire project until you give it the correct project context.

Local AI answers are guidance. They are not automatic approval to change source code.

## What This Tab Does

The Local AI tab can:

1. Select a project.
2. Run or load project analysis.
3. Load the project JSON used as evidence.
4. Ask questions about that evidence.
5. Show files and symbols related to the answer.
6. Keep conversation history in memory.
7. Show the exact prompt and diagnostic log when needed.
8. Offer quick questions for common architecture topics.

The tab does not automatically edit source files.

<div class="callout callout-note">
<div class="callout-icon">1</div>
<div><strong>The safest order is Select Project, Run Analysis, confirm the JSON, and then ask a focused question.</strong></div>
</div>

## Before You Start

![Selecting the correct project scope](../assets/drawings/local_ai_project_scope_selection.png)

Image note:

- Subject: Selecting the correct project root rather than an entire drive or wrong parent folder.
- Asset path: `assets/drawings/local_ai_project_scope_selection.png`.
- Alt text: A planning team compares incorrect folder scopes with one correctly bounded project area.
- Caption: Choose the project itself, not the whole drive or an unrelated parent folder.
- Artwork status: `primary_contextual_local_ai_raster`.

Before your first question:

1. Confirm that **Project root** points to the correct project.
2. Open **Config AI** and confirm that a local model is available.
3. Run project analysis or load a current project JSON.
4. Confirm the **JSON track** is the one you intend to use.
5. Start with one clear question.
6. Read the evidence and uncertainty, not only the final wording.

**Project root** means the main folder of the project you want Local AI to understand.

<div class="callout callout-warning">
<div class="callout-icon">!</div>
<div><strong>A correct-looking answer can still be based on the wrong project or old JSON.</strong> Check the project path and loaded evidence before trusting the answer.</div>
</div>

## The Safest First-Time Workflow

### Step 1 - Select the project

Click **Select Project** and choose the project root.

Read the final path before continuing.

### Step 2 - Run analysis

Click **Run Analysis**.

KANDA examines the project and prepares the structured project information used by Local AI.

When **Auto-load JSON after analysis** is enabled, the generated JSON is loaded automatically after analysis succeeds.

### Step 3 - Confirm analysis status

Check:

- **Analysis** - current analysis state.
- **Generated** - where the generated JSON was placed.
- **JSON track** - which kind of project JSON is loaded.
- **Detected** and **Active** profile - how KANDA classified the project.

Do not ask a project-specific question while these fields still say `Not loaded`.

### Step 4 - Confirm the local model

Click **Open Config AI**.

The Local AI tab uses the global Local AI configuration. The model is not edited independently inside this tab.

### Step 5 - Ask one focused question

Type a question in the message field and click the arrow button.

A focused question is easier to answer than a broad request such as `Explain everything`.

A good first question is:

`Which files own the startup sequence, and what evidence supports that answer?`

### Step 6 - Read the answer and evidence

Read the answer, then inspect:

- File evidence
- Symbol evidence
- Selected detail
- Prompt preview
- Log

### Step 7 - Ask a follow-up question

Use the same conversation when the next question depends on the previous answer.

Use **New session** when starting a separate topic.

## Project Context Controls

### Project root

Shows the selected project folder.

### Select Project

Opens a folder chooser for the project root.

### Run Analysis

Runs KANDA's project analysis for the selected project.

This may take time on a large project.

### Project JSON

Shows the JSON file currently used as project evidence.

A project JSON is a structured description of the project. It may include files, symbols, routes, manifests, validation state, and other collected information.

### Load JSON

Loads the selected project JSON.

Use this when a suitable JSON already exists.

### Static Context

Shows the static project context available to Local AI.

Static context is project information prepared outside the current chat turn, such as project summaries or governance material.

### Analysis, Generated, and JSON track

These status fields tell you:

- whether analysis is running or complete;
- where output was generated;
- whether the loaded JSON is the complete project copy or the Local-AI-focused copy.

### Create Local-AI Copy

Creates the Local-AI-specific JSON copy when it does not exist.

This copy is intended for Local AI consumption. It does not replace the canonical complete project JSON.

### Refresh Local-AI Copy

Rebuilds the Local-AI-specific copy from current project data.

Use it after meaningful project changes or after generating a newer complete JSON.

### Detected, Active, Override, and Reset Profile

KANDA may detect a project profile automatically.

- **Detected** shows the profile KANDA found.
- **Active** shows the profile currently used.
- **Override** lets you deliberately choose another available profile.
- **Reset Profile** removes the manual override and returns to automatic behavior.

Do not override the profile merely because another name looks familiar.

### Auto-load JSON after analysis

When enabled, successful analysis automatically loads its generated JSON.

This is convenient for normal first-time use.

## Local Runtime Controls

### Cache directory

Shows where Local AI runtime cache files are stored.

Cache files can improve repeated work, but they are not the canonical project source.

### Set Cache Dir

Selects the cache directory.

Use the default location unless you have a clear project reason to change it.

### Governance state

Shows an optional governance-state file used by the Local AI workflow.

### Set Governance State

Selects the governance-state file.

Do not choose a random JSON file. Use only the governance state intended for the current project and workflow.

### Open Config AI

Opens the single global Local AI configuration.

Use it to:

- select the local provider;
- refresh installed models;
- choose the active model;
- verify the local service.

### Verbosity

Controls the expected answer detail.

- **Concise** - brief explanation.
- **Detailed** - fuller explanation.
- **With Code** - explanation may include more code-oriented detail.

Verbosity changes answer length. It does not improve evidence quality by itself.

### Prefer code

Asks Local AI to emphasize source structure, symbols, paths, and code examples.

### Prefer prose

Asks Local AI to emphasize plain-language explanation.

### Debug Mode

Shows additional diagnostic information.

Use Debug Mode when investigating why an answer, prompt, evidence lookup, or runtime call failed.

Leave it off for normal reading.

## Quick Questions

The quick-question buttons fill and run common questions.

### Explain startup chain

Asks Local AI to describe how the application starts and which files participate.

### Explain topomap chain

Asks about the topomap-related workflow and wiring.

Use it only when the loaded project actually contains that feature.

### Explain timeline chain

Asks about timeline modules and their flow.

### Responsibility map

Asks which modules or files own important responsibilities.

### Uncertainty report

Asks Local AI to identify what is supported, what is uncertain, and where evidence may be incomplete.

<div class="callout callout-note">
<div class="callout-icon">i</div>
<div><strong>Quick questions are starting points.</strong> Follow them with narrower questions about specific files, symbols, or evidence.</div>
</div>

## Asking Questions

### Message field

Type the question you want Local AI to answer.

Press Enter or click the arrow button to send.

### Ask Local AI arrow button

Sends the current question.

The button may be disabled when required project evidence is missing or while another request is active.

### Good questions

Good questions are specific and ask for evidence.

Examples:

- `Which file owns the Help button for this tab?`
- `Where is the project JSON loaded?`
- `Which validator protects this workflow?`
- `What is uncertain about this answer?`
- `Show the path from the GUI button to the final service call.`

### Weak questions

Avoid questions such as:

- `Explain everything.`
- `Fix the project.`
- `Is the architecture good?`

These are too broad unless you define a specific area and expected evidence.

## Conversations and Memory

### New session

Clears the current visible conversation and starts a new session.

Use this when the next question is unrelated to the current topic.

### Conversations

Shows previous turns kept in the current memory-backed history.

Select a history item to inspect it.

### Clear memory

Removes the stored Local AI conversation memory.

Use it when:

- beginning work on a different project;
- old conversation context is confusing the answer;
- you need a clean test.

Clearing memory does not delete project source files.

<div class="callout callout-warning">
<div class="callout-icon">!</div>
<div><strong>Conversation memory can influence later answers.</strong> Clear it when changing projects or when old assumptions should no longer be used.</div>
</div>

## Reading the Answer

![Reviewing Local AI answer evidence](../assets/drawings/local_ai_answer_evidence_review.png)

Image note:

- Subject: Reviewing the Local AI answer together with files, symbols, prompt, and supporting evidence.
- Asset path: `assets/drawings/local_ai_answer_evidence_review.png`.
- Alt text: An analyst reviews answer panels while another person retrieves matching folders and evidence cards from an organized archive.
- Caption: Read the answer together with the files, symbols, prompt, and log that support it.
- Artwork status: `primary_contextual_local_ai_raster`.

### Main answer area

Shows the Local AI response.

The answer may be streamed gradually.

### File evidence

Lists files considered relevant to the answer.

Select a file to view more detail.

### Symbol evidence

Lists classes, functions, methods, or other symbols considered relevant.

Select a symbol to inspect it.

### Selected detail

Shows more information about the selected file or symbol.

### Prompt preview

Shows the prompt prepared for Local AI.

Use it to understand what context and instructions the model received.

### Log

Shows runtime events and errors.

Use it when the model does not respond, evidence is missing, or loading fails.

## What Local AI Can and Cannot Prove

Local AI can summarize and reason about the evidence it receives.

It cannot guarantee that:

- every source file was included;
- the project JSON is current;
- runtime behavior matches static source;
- a proposed code change is safe;
- an answer is correct merely because it is fluent.

When runtime behavior matters, ask for logs, tests, or current execution evidence.

When exact source matters, inspect the cited file.

## What Success Looks Like

A successful first session usually has all of these:

1. Correct project root.
2. Successful analysis or current JSON loaded.
3. Recognized JSON track.
4. Active local model configured.
5. One focused question.
6. A readable answer.
7. Relevant file or symbol evidence.
8. No unexplained runtime error in the Log.
9. Clear distinction between confirmed evidence and uncertainty.
10. Follow-up questions remain tied to the same project.

## Common Mistakes

### Asking before loading project evidence

**Result:** The question may be blocked or the answer may lack project grounding.

**Safer action:** Run analysis or load the correct JSON first.

### Selecting an entire drive

**Result:** Analysis may be slow, noisy, or point at the wrong scope.

**Safer action:** Select the project root itself.

### Using stale JSON

**Result:** Local AI may describe an older project state.

**Safer action:** Refresh analysis after meaningful project changes.

### Treating the answer as source truth

**Result:** A fluent explanation may be accepted without checking files.

**Safer action:** Inspect file and symbol evidence.

### Keeping old memory after changing projects

**Result:** Previous context may influence the new conversation.

**Safer action:** Use Clear memory.

### Turning on Debug Mode for normal reading

**Result:** The interface becomes noisy.

**Safer action:** Use it only for troubleshooting.

### Changing cache or governance paths without knowing why

**Result:** The runtime may use the wrong support state.

**Safer action:** Preserve the established defaults.

## If Something Goes Wrong

### Run Analysis does not start

Check:

- Project root exists;
- another analysis is not already running;
- the selected folder is readable.

### Analysis finishes but JSON is not loaded

Check **Generated**, then use **Load JSON**. Confirm that Auto-load is enabled if you expect automatic loading.

### Local model is unavailable

Open **Config AI**, refresh models, confirm the local model service is running, and select an available model.

### Ask button is disabled

Check:

- a project JSON is loaded;
- the question field is not empty;
- another request is not active.

### Answer never appears

Open the Log and check for:

- local service connection failure;
- model error;
- malformed response;
- project context loading failure.

### Answer is unrelated

Check the project root, JSON track, active profile, and conversation memory.

### Evidence lists are empty

The retriever may not have found strong matches, or the question may be too broad.

Ask a narrower question containing a file name, feature name, symbol, or workflow.

## First-Time Checklist

Before analysis:

- [ ] Correct project root
- [ ] Local AI configured
- [ ] Appropriate project scope
- [ ] Auto-load preference checked

Before asking:

- [ ] Current JSON loaded
- [ ] JSON track recognized
- [ ] Active profile reasonable
- [ ] One focused question
- [ ] Correct conversation or new session

Before trusting an answer:

- [ ] File evidence checked
- [ ] Symbol evidence checked
- [ ] Prompt preview available when needed
- [ ] Log has no unexplained failure
- [ ] Uncertainty separated from confirmed evidence
- [ ] Exact source inspected for important decisions

## Important Safety Boundary

![Local AI safety boundary](../assets/drawings/local_ai_safety_boundary.png)

Image note:

- Subject: Local AI reading and explaining evidence while source changes remain behind a separate protected workflow.
- Asset path: `assets/drawings/local_ai_safety_boundary.png`.
- Alt text: Two people consult project records with a Local AI assistant while locked source cabinets and a separate governed work area remain protected.
- Caption: Local AI can read and explain available evidence. Source changes require a separate governed implementation workflow.
- Artwork status: `primary_contextual_local_ai_raster`.

The Local AI Help page is read-only.

The Local AI tab explains and analyzes project evidence. It does not automatically install patches, edit project files, validate releases, or freeze project behavior.

Use the appropriate governed workflow before implementing any suggested change.

## Final Rule

**Select the correct project, load current evidence, ask one focused question, and verify the answer against files, symbols, and runtime evidence before acting on it.**
