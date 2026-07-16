# Architecture

## Workflow
Load data
Analyze signals
Generate output

## Modules
Controller
Service
Parser
Bridge

## Run instructions
pytest -q
uvicorn sample_project.api:app --reload
