# USER READ THIS TO UNDERSTAND HOW TO USE PROMPTS

This file is for the human.

It explains how to use the KANDA prompt workspace after the cleanup and startup delivery migration.

CURRENT STRUCTURE:

kanda_prompt_workspace/
  USER_READ_THIS_TO_UNDERSTAND_HOW_TO_USE_PROMPTS.md
  prompt_library/
  prompt_tools/
  first_AI_deliver/

FOLDER MEANINGS:

prompt_library/
Canonical prompt source. This is where the real prompt library lives.

prompt_tools/
Tooling folder. It contains the generator script and source map.

Important files:
  prompt_tools/sync_startup_routing_kernel_pack.py
  prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json

first_AI_deliver/
Human-facing delivery folder. Open this folder when starting a serious AI session.

Normal startup files:
  first_AI_deliver/first_prompts_to_ai.zip
  first_AI_deliver/send_this_first__CERT_<date>.md

Maintenance-only file:
  first_AI_deliver/send_ai_just_if_modify_startup_delivery.md

NORMAL AI STARTUP WORKFLOW:

1. Open first_AI_deliver/
2. Upload first_prompts_to_ai.zip
3. Open the newest send_this_first__CERT_<date>.md
4. Copy and paste its content into the AI chat
5. Wait for STARTUP PACK LOAD CHECK
6. Only then give the project task

WHEN TO USE MAINTENANCE FILE:

Use send_ai_just_if_modify_startup_delivery.md only when asking AI to modify:
  prompt_tools/
  first_AI_deliver/
  STARTUP_ROUTING_KERNEL_SOURCES.json
  sync_startup_routing_kernel_pack.py
  first_prompts_to_ai.zip
  send_this_first__CERT_<date>.md
  startup delivery naming/content/validation

Do not send it during normal startup.

REGENERATE STARTUP DELIVERY FILES:

Run from the workspace root:

python .\prompt_tools\sync_startup_routing_kernel_pack.py --dry-run
python .\prompt_tools\sync_startup_routing_kernel_pack.py --sync --yes
python .\prompt_tools\sync_startup_routing_kernel_pack.py --check

RULES:

- prompt_library/ is canonical source.
- prompt_tools/ is machinery.
- first_AI_deliver/ is what the human sends to AI.
- Do not edit files inside the ZIP as canonical source.
- Do not send all prompts to AI by default.
- Start with maps first, not all 80 prompts.
- Install success is not validation.
- Validation output is the evidence.
