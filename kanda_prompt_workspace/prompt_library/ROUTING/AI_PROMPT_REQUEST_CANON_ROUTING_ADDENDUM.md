# AI Prompt Request Canon Routing Addendum

Add `ai_prompt_request_canon` to the session-start/default prompt stack.

## Route

- prompt_id: `ai_prompt_request_canon`
- priority: 95
- load type: always at session start; also before non-trivial project actions

## Trigger phrases

- start the day
- continue project
- create new folder
- create database
- databank
- refactor module
- create patch
- freeze this
- create handoff
- audit prompts
- generalize prompts
- update prompt library

## Required companions

- `session_start_upload_checklist`
- `prompt_navigation_index`
- `box_architecture_canon`
- `bundle_gated_development_workflow`

## Behavior

When a task implies specialized workflow and the prompt stack/evidence is missing, the AI must ask for the missing prompts/files before implementation.
