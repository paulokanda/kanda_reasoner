# Navigation Index Coverage Report — v3

## Result

PASS: Every active prompt has an intent-routing entry.

## Counts

- Active prompts covered: 72
- Machine-readable route entries: 72
- Human-readable route sections: 72
- Metadata files updated with routing fields: 72
- Coverage table rows: 72

## Fields Present Per Prompt

Each prompt entry includes:

- trigger phrases
- user intent examples
- aliases
- when to load this prompt
- when not to load this prompt
- required companion prompts
- priority if multiple prompts match

## Files Added / Updated

- `ROUTING/PROMPT_NAVIGATION_INDEX.md`
- `ROUTING/prompt_navigation_index.json`
- `ROUTING/prompt_route_coverage_table.csv`
- `ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md`
- `METADATA/*.meta.json`

## Validation

- All active prompt IDs found: yes
- Duplicate prompt IDs: no
- Missing routing entries: no
- Box Logic Requirement retained in active prompts: checked separately in self-check

