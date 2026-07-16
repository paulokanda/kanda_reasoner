# Prompt Validation Report Template

Report ID: <VALIDATION_REPORT_ID>
Date: <YYYY-MM-DD>
Prompt or pack: <PROMPT_OR_PACK_ID>
Validator: manual | Tab 9 | external

## 1. Scope

Validated files:

- <FILE_1>
- <FILE_2>

Out of scope:

- <OUT_OF_SCOPE_ITEM>

## 2. Structural Checks

| Rule | Result | Notes |
|---|---|---|
| Prompt file readable | not_run | |
| Metadata JSON parses | not_run | |
| Required metadata fields present | not_run | |
| Required prompt sections present | not_run | |
| Version is present | not_run | |
| Change log is present | not_run | |

## 3. Project-Agnostic Checks

| Rule | Result | Notes |
|---|---|---|
| No hardcoded absolute Windows paths | not_run | |
| No hardcoded Unix paths | not_run | |
| Uses <PROJECT_ROOT> for project paths | not_run | |
| Uses <PROJECT_NAME> for project names | not_run | |
| Uses <PRODUCT_PACKAGE> for package names | not_run | |
| Examples are clearly marked | not_run | |

## 4. Safety Checks

| Rule | Result | Notes |
|---|---|---|
| Does not modify source code | not_run | |
| Does not write active governance | not_run | |
| Does not execute prompts automatically | not_run | |
| Governance-linked prompts marked protected | not_run | |
| Creates-files contract is documented | not_run | |

## 5. Findings

### Errors

- NONE

### Warnings

- NONE

### Notes

- NONE

## 6. Decision

Validation decision:

pass | pass_with_warnings | fail | not_run

Next action:

<NEXT_ACTION>
