# CONTEXT ROUTING LAYER HUMAN REVIEW

Patch: kanda_context_routing_layer_phase5_human_review_v1
Status: review package
Scope: prompt_library prompt-staging folder only

## Purpose

This file guides the human review of the staged KANDA Context Routing Layer before the folder is marked as a clean staging baseline.

This is not live app integration.
This is not Tab Prompt Library integration.
This is not a dispatcher.

## Review targets

Review these files first:

1. ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md
2. ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md
3. ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
4. ROUTING/GROUP_ASSIMILATION_INDEX.md
5. ROUTING/group_assimilation_index.json
6. ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md
7. ROUTING/folder_assimilation_cards_index.json
8. ROUTING_TESTS/context_routing_test_cases.md
9. ROUTING_TESTS/context_routing_expected_outputs.json
10. TOOLS/validate_context_routing_layer.py

## Human review questions

1. Does the start-of-day stack stay small?
2. Does the AI request missing prompts only when needed?
3. Does the fast path avoid over-asking for simple explanation tasks?
4. Does prompt_navigation_index act as the main router?
5. Do folder assimilation cards stay as metadata only?
6. Are implementation tasks routed to architecture and delivery validation?
7. Are freeze tasks routed to governance and validation evidence?
8. Are prompt-audit tasks routed to prompt audit and routing groups?
9. Are productization tasks routed to release readiness?
10. Is any live app integration attempted too early?

## Pass condition

Phase 5 passes when the human accepts that:

- routing behavior is understandable;
- the map is not a master prompt;
- specialist prompts remain separate;
- no live app folder was modified;
- Phase 6 can mark prompt_library as a clean prompt-staging baseline.

## Fail condition

Phase 5 fails if:

- the router asks for too many prompts for simple tasks;
- folder cards contain behavioral rules;
- prompt_navigation_index duplicates specialist prompt content;
- a task route is unclear or unsafe;
- live app integration is attempted too early.

## Next step after review

If accepted, proceed to Phase 6:

Freeze the prompt_library staging folder as the clean prompt-routing baseline.
