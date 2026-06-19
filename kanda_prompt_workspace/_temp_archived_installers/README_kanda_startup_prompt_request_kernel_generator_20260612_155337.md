# KANDA Startup Prompt Request Kernel Generator v2.2

This patch implements Item 13 as a human-visible maintenance prompt in `first_AI_deliver`.

## Generated delivery folder

```text
first_AI_deliver/
  first_prompts_to_ai.zip
  send_this_first__CERT_<YYYYMMDD_HHMMSSZ>.md
  send_ai_just_if_modify_startup_delivery.md
```

## Normal use

For normal startup, send only:

```text
first_AI_deliver/first_prompts_to_ai.zip
```

Then paste the content of:

```text
first_AI_deliver/send_this_first__CERT_<date>.md
```

## Maintenance use

Only when asking AI to modify the startup delivery system, also send:

```text
first_AI_deliver/send_ai_just_if_modify_startup_delivery.md
```

This file is not inside `first_prompts_to_ai.zip`.
