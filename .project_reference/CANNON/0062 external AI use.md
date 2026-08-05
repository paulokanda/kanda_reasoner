# KANDA REASONER — EXTERNAL WEB AI CONFIGURATION AND USE HANDOFF

## Purpose of this handoff

This document explains how to configure and use External Web AI in KANDA Reasoner.

External Web AI means an approved AI assistant opened in the user’s normal web browser. KANDA Reasoner prepares a governed prompt, copies it to the clipboard after approval, and opens the selected assistant’s official website.

This is different from the direct Web AI connection through OpenRouter or Kilo.

The External Web AI route is intentionally manual.

KANDA Reasoner does not:

* Log in to an external AI account.
* Enter credentials.
* Paste the prompt into the website.
* Press the website’s Send button.
* Scrape or read the answer.
* Capture the browser response.
* Import the response automatically.
* Merge the response into the direct OpenRouter or Kilo conversation.
* Apply the answer to Project source.
* Write Freeze Memory.
* Memorize an error.

The user remains responsible for reviewing what is copied, manually submitting it to the external assistant, reviewing the answer, and returning the answer to the appropriate governed workflow when necessary.

The frozen rule is:

```text
External Web AI = manual copy and open only.
```

The single selected external assistant is application-scoped and is reused by all integrated workflows.

---

# 1. THE THREE AI MODES

KANDA Reasoner has three conceptually different AI routes.

## 1.1 OpenRouter

OpenRouter is a direct provider route.

KANDA Reasoner communicates with OpenRouter through the application’s direct Web AI runtime. It requires valid provider configuration and credentials.

The approved catalog is restricted to the configured free Python-coding models. Generic free routers and automatic paid fallbacks are rejected.

Use this route when you want an in-application AI conversation whose response returns directly to KANDA Reasoner.

## 1.2 Kilo

Kilo is also a direct provider route.

Like OpenRouter, it is part of the direct Web AI session. Its response can appear inside KANDA Reasoner because it uses the direct provider runtime.

Use this route when Kilo is configured and you want a direct in-application coding conversation.

## 1.3 External Web AI

External Web AI is not a direct API session.

KANDA Reasoner:

1. Builds the prompt.
2. Shows a warning or approval dialog when Project context will be copied.
3. Copies the prompt to the clipboard.
4. Opens the configured assistant’s official HTTPS website.

The user then:

1. Reviews the copied material.
2. Manually signs in to the external website when needed.
3. Manually pastes the prompt.
4. Manually submits it.
5. Reviews the answer.
6. Manually returns useful content to the correct KANDA Reasoner workflow.

External Web AI works independently of OpenRouter or Kilo credential readiness once the required Project context is available.

An unavailable OpenRouter API key does not prevent the manual External Web AI handoff.

---

# 2. CONFIGURING EXTERNAL WEB AI

## 2.1 Open KANDA Reasoner

Start KANDA Reasoner normally.

For general External AI configuration, a selected Project may not be required. Config AI is designed to remain usable without an active Project where its current contract permits it.

A selected Project is required when the prompt being exported depends on Project source, Project handoff information, architecture evidence, or another Project-owned artifact.

## 2.2 Open Config AI

In the main KANDA Reasoner interface, open:

```text
Config AI
```

The Config AI area contains the direct-provider configuration and the External AI configuration.

Open the External AI subtab or section.

The exact visible layout may change, but the current feature contract includes:

```text
External AI assistant selection
Open Official Site
Copy Test Prompt and Open
Run Readiness Check
```

## 2.3 Select the external assistant

Choose one assistant from the approved External AI list.

The list is controlled by KANDA Reasoner’s approved Python-coding AI catalog.

Do not manually type or substitute an unapproved website URL into Project files.

The selected assistant:

* Has a stable internal ID.
* Has a validated official HTTPS URL.
* Is restricted to the approved host allowlist.
* Is stored as an application-level Tool setting.
* Is reused by the integrated External AI workflows.
* Does not become Project authority.
* Does not grant the external service permission to modify Project source.

The selected assistant is shared across the integrated workflows. Changing it in Config AI changes which external website those workflows open.

## 2.4 Save or confirm the selection

Use the visible selection/save control provided by Config AI.

The application persists the selected assistant as Tool configuration.

This setting does not belong to the selected Project and must not be written into Project source merely because a Project is loaded.

## 2.5 Test the official website

Use:

```text
Open Official Site
```

This opens the selected assistant’s validated website.

This action is useful for checking that:

* The correct assistant is selected.
* The website opens.
* The browser is available.
* You can manually authenticate when the website requires an account.

KANDA Reasoner does not authenticate for you.

## 2.6 Test clipboard handoff

Use:

```text
Copy Test Prompt and Open
```

This should:

1. Build a harmless test prompt.
2. Copy the exact test prompt to the clipboard.
3. Open the selected assistant’s official website.

Manually paste the clipboard content into the external website to confirm the full handoff.

The test does not prove that KANDA Reasoner can read an answer back. Automatic answer intake is intentionally absent.

---

# 3. RUNNING THE READINESS CHECK

In Config AI, use:

```text
Run Readiness Check
```

The readiness check is local and network-free.

It evaluates the installed catalog and configuration. It does not contact the assistant websites and does not prove that an external provider is currently online.

The readiness result may show:

```text
CURRENT
REVIEW_DUE
STALE
```

Meaning:

* `CURRENT`: the installed catalog verification date is within the current review window.
* `REVIEW_DUE`: the catalog should be reviewed because its verification age passed the normal review interval.
* `STALE`: the catalog is old enough that its URLs or free-model assumptions should be checked before relying on them.

The current policy uses catalog-age thresholds, including a normal review age and a later stale age.

The readiness display may also show counts for:

* Approved OpenRouter models.
* Approved Kilo models.
* Approved external assistants.
* Validated HTTPS assistant URLs.

Important:

```text
Readiness check = local configuration health.
Readiness check ≠ live provider availability test.
```

Use `Open Official Site` for a manual live website check.

---

# 4. GENERAL EXTERNAL WEB AI WORKFLOW

The standard External Web AI flow is:

```text
select assistant in Config AI
-> open the relevant KANDA Reasoner workflow
-> prepare the exact task or package
-> click the External AI copy/open control
-> review the disclosure warning
-> approve clipboard and remote-site transfer
-> KANDA copies the prompt
-> KANDA opens the official website
-> user manually pastes and submits
-> user reviews the external answer
-> user manually returns the answer to the correct governed workflow
-> local validator or human review decides what may happen next
```

Do not treat an external answer as automatically trusted.

An external AI answer is advisory input.

It is not:

* Source truth.
* Validation evidence.
* Installation authority.
* Freeze authority.
* Error Memory authority.
* Permission to overwrite current source.
* Permission to cross the Tool-versus-Project boundary.

---

# 5. INTEGRATED WORKFLOWS

The selected External AI assistant is integrated into several KANDA Reasoner workflows.

Current frozen integration includes:

## 5.1 AST Split

Use External AI when you want an outside assistant to review or propose a bounded AST-based split.

Typical flow:

```text
open AST Split
-> prepare the split context
-> use the External AI copy/open control
-> manually submit the prompt
-> review the answer
-> return the proposed result through the AST Split workflow’s governed review path
```

The external assistant cannot modify source directly.

The AST Split workflow remains the owner of:

* Its prompt.
* Its package.
* Its return validation.
* Its Project boundary.
* Its eventual source action.

## 5.2 Large File Refactor Planner

Use External AI to obtain an external refactoring opinion or plan.

Typical flow:

```text
open Large File Refactor Planner
-> select or generate the candidate context
-> copy/open with the configured External AI
-> manually send the prompt
-> review the answer
-> bring useful material back to the planner
-> validate it locally before any source action
```

The external answer is a proposal, not an approved refactor.

## 5.3 External AI Candidate Exchange

This workflow is designed for a bounded candidate exchange with an external assistant.

It may prepare:

* Candidate content.
* Task boundaries.
* Package paths.
* Package SHA-256.
* Explicit return instructions.

The user manually sends that package or prompt to the external assistant.

Any returned candidate must go through the existing governed intake and validation route.

## 5.4 Main Workbench

Use External AI when the Main Workbench has prepared a bounded task that would benefit from an outside opinion.

The Main Workbench remains the owner of its task context and return handling.

The external website cannot become the Workbench owner.

## 5.5 Prompt Router Reasoner

The current Prompt Router can export its final prepared prompt to the selected External AI.

Use it when:

* The Prompt Router has already assembled the correct prompt.
* You want to ask a browser-based assistant instead of a direct OpenRouter/Kilo model.
* You want to keep the external conversation separate.

Do not revive or assume an older retired “Ask AI” control. Use the current configured external handoff control.

---

# 6. USING EXTERNAL WEB AI FROM PROJECT WEB AI

Project Web AI has two distinct paths.

## 6.1 Direct Project Web AI path

The direct path uses OpenRouter or Kilo.

This path:

* Runs inside KANDA Reasoner.
* Maintains its own direct session history.
* Can receive the provider response.
* Remains connected to the direct provider runtime.
* Uses the governed local Shadow Preview and source-apply architecture.

## 6.2 External Project Web AI export

The external path uses:

```text
Copy and Open External AI
```

This creates a separate browser conversation.

The exported prompt may include:

* The current question.
* Project architecture context.
* Earlier advisory content.
* Selected Project evidence.
* Explicit boundary instructions.
* A declaration that there is no automatic response intake.
* A declaration that the external service has no source-write authority.

Before copying Project context, KANDA Reasoner requires explicit approval.

The approval means:

```text
You authorize this exact prompt to be copied to the clipboard
and sent manually to a remote external website.
```

It does not mean:

```text
You authorize the website to modify the Project.
```

After approval:

1. KANDA copies the prompt.
2. KANDA opens the selected official site.
3. You paste and submit it manually.
4. The answer remains in the external browser.
5. Nothing returns automatically to Project Web AI.

The external conversation does not change the direct OpenRouter/Kilo history.

The external route must not:

* Call browser automation.
* Use Selenium or Playwright.
* Use HTTP scraping.
* Paste automatically.
* Submit automatically.
* Capture the response.
* Start a direct Project Web AI chat turn.
* append tokens to the direct chat.
* write Project source.
* confirm Freeze.
* memorize an error.

The Project Web AI external route is intentionally independent from direct API readiness after Project context has been loaded.

---

# 7. USING EXTERNAL WEB AI FOR FREEZE

External AI can assist with a Freeze draft, but it cannot Freeze the feature.

The normal local Freeze path remains:

```text
New Local Freeze Entry
-> Preview Freeze Entry
-> human review
-> Confirm and Write
```

External AI is an advanced or fallback advisory route.

Typical external Freeze flow:

```text
prepare the Freeze formulary or evidence
-> use the External AI handoff button
-> manually submit the bounded prompt
-> receive a draft from the external assistant
-> manually return the draft to the Freeze form
-> Preview
-> validate the preview
-> human Confirm and Write
```

The returned external text remains a draft.

It cannot:

* Write the frozen entry.
* Claim that validation passed.
* Confirm the feature.
* Replace the local evidence.
* Bypass Preview.
* Bypass human confirmation.

---

# 8. USING EXTERNAL WEB AI FOR ERROR MEMORY

External AI may help draft or review an Error Memory lesson.

It cannot memorize the lesson.

Typical flow:

```text
collect exact error evidence
-> prepare the bounded Error Memory prompt
-> copy/open the selected External AI
-> manually submit
-> receive a draft lesson
-> manually return it to Error Memory
-> check duplicate and overlap rules
-> review the pending lesson
-> human selects Memorize Error
```

The external assistant cannot:

* Save the lesson.
* Activate it.
* Supersede another lesson.
* Mark it canonical.
* Execute Memorize Error.

A lesson must still be verified, reusable and non-duplicative.

---

# 9. USING EXTERNAL WEB AI FOR ARCHITECTURE AUDIT

External AI architecture review is read-only and advisory.

Typical flow:

```text
run the deterministic local architecture audit
-> prepare the external review package
-> copy/open the configured assistant
-> manually submit
-> review the advisory answer
-> compare it with the deterministic local result
```

The deterministic KANDA Reasoner audit remains authoritative for the workflow.

The external assistant cannot:

* Modify files.
* Write Freeze Memory.
* Create Error Memory.
* Replace the local audit result.
* Change Project-selection authority.

---

# 10. RETURNING AN EXTERNAL ANSWER SAFELY

External Web AI has no universal automatic answer receiver.

How you return an answer depends on the originating workflow.

## When the originating workflow has a receive/import field

Return to the same workflow and use its governed receive or validation control.

Do not paste directly into Project source.

## When Project Web AI created the external export

The external Project Web AI route itself does not import the answer.

Treat the answer as advisory.

To act on it:

1. Review it manually.
2. Identify the correct KANDA Reasoner workflow.
3. Paste only the relevant proposal into that workflow’s governed input.
4. Run the workflow’s validator.
5. Use Shadow Preview or another local preview when available.
6. Require human approval before a source write.

## When the answer includes code

Do not automatically install it.

First verify:

* The selected Project identity.
* Tool-versus-Project ownership.
* Current exact source.
* Baseline hashes.
* Changed files.
* Protected files.
* Module-size limits.
* Syntax.
* Tests.
* Rollback.
* INSTALL/VALIDATE/FREEZE separation.

External code is untrusted candidate material until validated locally.

---

# 11. PRIVACY AND DISCLOSURE

Before using External Web AI, assume that anything copied to the clipboard and pasted into the external website leaves the local KANDA Reasoner environment.

Review the prompt before submitting it.

Do not send:

* Passwords.
* API keys.
* Access tokens.
* Private signing keys.
* Patient-identifying data.
* Confidential customer data.
* Proprietary source that the external service is not allowed to receive.
* Unredacted secrets from `.env` files.
* Personal information not needed for the task.

KANDA Reasoner’s manual approval step is intentional. It provides a moment to review the information before sending it remotely.

The application does not capture external credentials.

---

# 12. TOOL-VERSUS-PROJECT BOUNDARY

External Web AI does not weaken the Tool-versus-Project boundary.

The external assistant must be told:

```text
Do not write KANDA Tool-owned code into an external selected Project source tree.

Do not write external selected-Project code into KANDA Tool source.
```

The Project Support folder may contain copies, prompts, manifests and evidence used for handoff, but it is not canonical source and is not an installation target.

When KANDA Reasoner itself is the selected Project, physical roots may coincide, but logical ownership must still be resolved before a write.

An external assistant’s answer never overrides this rule.

---

# 13. TROUBLESHOOTING

## Problem: External AI button is disabled

Check:

1. An approved assistant is selected in Config AI.
2. The assistant’s URL is valid.
3. The workflow has the required Project context.
4. The selected Project is loaded when the prompt requires Project evidence.
5. The workflow has finished preparing its prompt or package.

## Problem: Website does not open

Use `Open Official Site` in Config AI.

Check:

* Default browser configuration.
* Local browser security.
* Whether the official site is available.
* Whether the selected assistant is still current.
* Whether the readiness status is `REVIEW_DUE` or `STALE`.

The readiness check itself does not contact the website.

## Problem: Wrong external assistant opens

Return to:

```text
Config AI
-> External AI
```

Select the correct assistant and save the configuration.

Because the selection is application-scoped, changing it affects all integrated external handoffs.

## Problem: Clipboard contains unexpected text

Cancel the external submission.

Do not paste it into the website.

Return to the originating workflow and confirm:

* The correct Project is selected.
* The correct task is active.
* The correct package or prompt was generated.
* No stale workflow state remains.

Then generate the handoff again.

## Problem: External answer does not appear in KANDA Reasoner

This is expected.

External Web AI has no automatic response capture.

Copy the useful answer manually and return it through the originating workflow’s governed input or validation route.

## Problem: OpenRouter or Kilo credentials are missing

This does not necessarily block External Web AI.

The manual external route is designed to remain usable independently of direct API credential readiness once its required context is available.

## Problem: External answer proposes direct source edits

Do not apply them directly.

Treat the answer as a candidate proposal.

Use the governed local patch lifecycle:

```text
inspect current source
-> determine owner
-> prepare patch
-> INSTALL
-> VALIDATE
-> FREEZE
-> ERROR MEMORY when justified
```

## Problem: External answer claims validation passed

Ignore that claim unless local KANDA Reasoner validation produced the required markers.

An external assistant cannot generate authoritative local validation evidence.

## Problem: External answer claims the feature is frozen

Ignore that claim.

Freeze requires:

```text
Preview Freeze Entry
-> human Confirm and Write
```

---

# 14. NORMAL RECOMMENDED USE

Use direct OpenRouter or Kilo when:

* Credentials are configured.
* You want an answer returned inside KANDA Reasoner.
* You want direct conversation history.
* The normal direct provider route is sufficient.

Use External Web AI when:

* Direct credentials are unavailable.
* You want a second opinion from a browser-based assistant.
* A specific external assistant is better suited to the task.
* You want to compare multiple assistants manually.
* You are using an advanced/fallback review route.
* You understand that the answer will not return automatically.

External AI review remains advanced or fallback behavior. It is not a replacement for:

* Local deterministic validation.
* Current source inspection.
* Shadow Preview.
* Transactional installation.
* Human approval.
* Freeze confirmation.
* Error Memory review.

---

# 15. QUICK CONFIGURATION CHECKLIST

```text
[ ] Open Config AI.
[ ] Open External AI.
[ ] Select one approved assistant.
[ ] Save or confirm the selection.
[ ] Click Open Official Site.
[ ] Manually verify that the correct website opened.
[ ] Click Copy Test Prompt and Open.
[ ] Manually paste and submit the test prompt.
[ ] Run Readiness Check.
[ ] Confirm CURRENT, REVIEW_DUE or STALE status.
[ ] Remember that readiness is local and network-free.
```

---

# 16. QUICK USE CHECKLIST

```text
[ ] Select the correct Project when Project context is required.
[ ] Open the correct KANDA Reasoner workflow.
[ ] Prepare the exact prompt or package.
[ ] Click the workflow’s External AI copy/open control.
[ ] Read the clipboard and remote-site disclosure.
[ ] Approve only when the content is safe to send.
[ ] Manually paste the prompt into the external website.
[ ] Manually submit it.
[ ] Review the answer as untrusted advisory material.
[ ] Return useful content through the correct governed workflow.
[ ] Run local validation.
[ ] Do not allow automatic source writes.
[ ] Do not treat the answer as Freeze or Error Memory authority.
```

---

# 17. CORE RULES TO PRESERVE

```text
EXTERNAL WEB AI IS MANUAL COPY AND OPEN ONLY.

THE SELECTED ASSISTANT IS APPLICATION-SCOPED.

KANDA DOES NOT LOGIN, PASTE, SUBMIT, SCRAPE OR CAPTURE RESPONSES.

EXTERNAL ANSWERS DO NOT ENTER DIRECT OPENROUTER OR KILO HISTORY.

EXTERNAL ANSWERS HAVE NO PROJECT SOURCE-WRITE AUTHORITY.

PROJECT WEB AI EXTERNAL EXPORT HAS NO AUTOMATIC RESPONSE INTAKE.

FREEZE PREVIEW IS READ-ONLY.

CONFIRM AND WRITE IS HUMAN-ONLY.

MEMORIZE ERROR IS HUMAN-ONLY.

LOCAL VALIDATION REMAINS AUTHORITATIVE.

TOOL AND PROJECT CODE MUST REMAIN IN THEIR CANONICAL OWNERS.
```

---

# 18. CURRENT FROZEN OWNERS

The principal current owners include:

```text
External assistant catalog:
kanda_reasoner_app/python_coding_ai_catalog.py

External assistant configuration:
kanda_reasoner_app/external_ai_configuration.py

Manual copy/open handoff:
kanda_reasoner_app/external_ai_handoff.py

Shared workflow facade:
kanda_reasoner_app/external_ai_workflow.py

Config AI External AI GUI:
kanda_reasoner_app/reasoner_engine/config_external_ai_tab.py

Project Web AI external export:
kanda_reasoner_app/reasoner_engine/project_web_ai_external_handoff.py

Direct provider runtime:
kanda_reasoner_app/web_ai_provider_runtime.py
```

Do not create a second assistant catalog, a second global selected-assistant setting, or another generic clipboard owner.

Each integrated workflow remains the owner of its own exact prompt, package, return validation and Project boundary.

---

# 19. FINAL HANDOFF STATUS

```text
EXTERNAL AI CONFIGURATION: AVAILABLE

EXTERNAL AI SELECTION SCOPE: APPLICATION

OFFICIAL URL POLICY: APPROVED HTTPS ALLOWLIST

HANDOFF MODE: MANUAL COPY AND OPEN

AUTOMATIC LOGIN: DISABLED

AUTOMATIC PASTE/SUBMIT: DISABLED

AUTOMATIC RESPONSE CAPTURE: DISABLED

DIRECT HISTORY MERGE: DISABLED

AUTOMATIC SOURCE WRITE: DISABLED

FREEZE AUTHORITY: HUMAN ONLY

ERROR MEMORY AUTHORITY: HUMAN ONLY

LOCAL VALIDATION AUTHORITY: PRESERVED
```
