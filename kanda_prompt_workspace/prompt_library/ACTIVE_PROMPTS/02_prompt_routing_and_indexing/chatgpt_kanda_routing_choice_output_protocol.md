---
prompt_id: chatgpt_kanda_routing_choice_output_protocol
prompt_code: KPR-02-001
title: ChatGPT KANDA Routing Choice Output Protocol
version: 3.1
status: active
load_type: on_request
owner_box: 02_prompt_routing_and_indexing
source_stage: prompt-audit-wave3a-session-startup-kernel-v1
---

# ChatGPT KANDA Routing Choice Output Protocol

## Mission

Define the optional advisory route-choice block that browser ChatGPT may emit for manual capture by Prompt Router Reasoner.

The block is advisory only. It does not load prompts, mutate local state, authorize work, grant ML authority, validate code, or freeze anything.

## Direct retrieval rule

The startup pack and `KPR-02-004 prompt_navigation_index` decide which exact prompt path is needed. When the selected prompt is not already in the startup ZIP, retrieve only that addressed path from `prompt_library.zip`. Do not open the whole library and do not ask the user to paste a prompt already available in the uploaded ZIP.

## When to emit a route-choice block

Emit the block only when:

- the user explicitly requests machine-readable route output;
- manual Prompt Router Reasoner capture is the intended next step; or
- another current owner requires this exact advisory exchange format.

Otherwise provide normal human-readable routing.

## Receive-ready format

The first visible characters must be `KANDA_ROUTING_CHOICE_START` and the last visible characters must be `KANDA_ROUTING_CHOICE_END`.

Between the markers return one valid JSON object:

```text
KANDA_ROUTING_CHOICE_START
{
  "schema_version": "1.0",
  "event_type": "kanda_routing_choice",
  "prompt_code": "KPR-xx-xxx or empty",
  "prompt_id": "current prompt ID",
  "folder_id": "current folder ID",
  "prompt_path": "ACTIVE_PROMPTS/.../prompt.md",
  "required_companion_prompt_ids": [],
  "reason": "brief evidence-based reason",
  "confidence": "high | medium | low",
  "advisory_only": true,
  "may_mutate": false,
  "may_freeze": false,
  "may_activate_ml": false
}
KANDA_ROUTING_CHOICE_END
```

## Validation rules

- Use a prompt code only when current metadata proves it.
- The prompt ID and path must resolve in current route data.
- `advisory_only`, `may_mutate`, `may_freeze`, and `may_activate_ml` must have the exact safe values shown.
- Do not include comments, trailing commas, markdown fences, or prose outside the markers.
- Ambiguous routing must use empty code only when no current code exists and must state low confidence.
- Never invent a path or substitute a historical alias as active.

## Authority boundary

The local application, current routing owners, Brick Wall, validators, and human decisions remain authoritative. This protocol is only an exchange format.

## Version history

- 3.1: removed normal-startup loading; the advisory exchange remains available on request.
- 3.0: restored KPR-02-001 advisory output identity and retained only a compact direct-retrieval bridge.
