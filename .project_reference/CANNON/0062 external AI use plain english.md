# KANDA REASONER — HOW TO SET UP AND USE EXTERNAL WEB AI

## What External Web AI means

External Web AI lets KANDA Reasoner prepare a question for an AI website such as a browser-based AI assistant.

KANDA Reasoner will:

1. Prepare the message.
2. Copy the message to your clipboard.
3. Open the official AI website in your browser.

You must then:

1. Paste the message into the website.
2. Press Send.
3. Read the answer.
4. Copy the useful answer back into KANDA Reasoner when needed.

KANDA Reasoner does not automatically send the message or read the answer from the website.

This is intentional. It keeps you in control of what information leaves your computer.

---

# 1. External Web AI is different from OpenRouter and Kilo

KANDA Reasoner may show three different ways to use AI.

## OpenRouter

OpenRouter connects directly to KANDA Reasoner.

When it is properly configured, you can ask a question and receive the answer inside KANDA Reasoner.

It normally requires an API key or another type of account configuration.

## Kilo

Kilo is another direct AI connection.

Like OpenRouter, it may return the answer directly inside KANDA Reasoner.

## External Web AI

External Web AI uses an ordinary AI website opened in your browser.

KANDA Reasoner only copies the prepared question and opens the correct website.

It does not:

* Enter your username or password.
* Paste the question automatically.
* Press Send.
* Read the answer.
* Download the answer.
* Change your Project.
* Install code.
* Freeze a feature.
* Save an Error Memory lesson.

External Web AI is therefore a manual process.

---

# 2. How to configure External Web AI

## Step 1 — Open KANDA Reasoner

Start KANDA Reasoner normally.

## Step 2 — Open Config AI

Find and open:

```text
Config AI
```

Inside Config AI, look for the section or tab named:

```text
External AI
```

## Step 3 — Choose an AI assistant

Select one of the available external assistants.

KANDA Reasoner only lists assistants that are already approved in its configuration.

The assistant you choose will be used by all External AI buttons in KANDA Reasoner.

For example, after choosing an assistant in Config AI, that same assistant may open when you use External AI from:

* Show Project to AI.
* Project Web AI.
* Architecture Review.
* Large File Refactor Planner.
* Error Memory.
* Freeze Feature After Update.
* Prompt Router Reasoner.

You normally do not need to choose the assistant again in every screen.

## Step 4 — Save the selection

Use the available Save, Apply or Confirm button.

The selected assistant is a KANDA Reasoner setting. It is not saved inside the selected Project’s source code.

## Step 5 — Test the website

Click:

```text
Open Official Site
```

KANDA Reasoner should open the selected assistant’s official website in your normal browser.

You may need to sign in manually.

KANDA Reasoner does not know or store the password for the external website.

## Step 6 — Test copying a message

Click:

```text
Copy Test Prompt and Open
```

KANDA Reasoner should:

1. Copy a test message.
2. Open the external AI website.

Go to the website and press:

```text
Ctrl + V
```

The test message should appear.

You must press Send manually.

---

# 3. Run the Readiness Check

Inside Config AI, click:

```text
Run Readiness Check
```

This checks the AI list installed in KANDA Reasoner.

It may show one of these results:

## CURRENT

The installed AI list was reviewed recently.

## REVIEW_DUE

The AI list still works, but it should be reviewed soon.

## STALE

The AI list is old and should be checked before relying on it.

Important:

The Readiness Check does not contact the AI websites.

It only checks the information already installed in KANDA Reasoner.

To test whether a website currently opens, use:

```text
Open Official Site
```

---

# 4. How to use External Web AI

The normal process is:

```text
Open the correct KANDA Reasoner screen
-> prepare the question or Project information
-> click the External AI button
-> review the warning
-> approve copying
-> KANDA copies the message
-> KANDA opens the AI website
-> paste the message manually
-> press Send manually
-> read the answer
-> return to KANDA Reasoner
```

You remain responsible for reviewing both the message and the answer.

---

# 5. What happens when you click an External AI button

When you click an External AI button, KANDA Reasoner may show a warning.

The warning means that information is about to be copied from KANDA Reasoner and may be pasted into an external website.

Read the message before approving it.

After approval:

1. The message is copied to your clipboard.
2. The official website opens.
3. You paste the message.
4. You press Send.
5. The answer stays on the external website.

The answer does not return automatically to KANDA Reasoner.

---

# 6. How to paste the message

After the website opens:

1. Click inside the website’s message box.
2. Press:

```text
Ctrl + V
```

3. Read the pasted message.
4. Remove anything you do not want to send.
5. Press the website’s Send button.

Do not send the message without reviewing it.

---

# 7. How to bring the answer back

When the external AI gives you an answer:

1. Read the answer.
2. Select the useful part.
3. Copy it using:

```text
Ctrl + C
```

4. Return to KANDA Reasoner.
5. Paste it into the correct screen or input box.

The correct place depends on where the request started.

For example:

* An architecture answer should return to the architecture workflow.
* A Freeze draft should return to the Freeze form.
* An Error Memory draft should return to Error Memory.
* A refactoring proposal should return to the refactoring workflow.
* A general Project answer may be pasted into the relevant Project Web AI or review field.

Do not paste AI-generated code directly into Project files unless the normal KANDA Reasoner installation and validation process is used.

---

# 8. Using External AI from Project Web AI

Project Web AI has two different types of AI use.

## Direct AI conversation

OpenRouter or Kilo may answer directly inside KANDA Reasoner.

## External AI conversation

The External AI button opens a completely separate conversation in your browser.

The external conversation does not become part of the OpenRouter or Kilo conversation.

Nothing from the external website is imported automatically.

When you use the External AI option in Project Web AI:

1. KANDA Reasoner prepares the Project question.
2. It may include Project information.
3. It asks for your approval.
4. It copies the message.
5. It opens the website.
6. You paste and send it manually.

The external website cannot change your Project.

---

# 9. Using External AI with Freeze

External AI may help write a draft for a Freeze entry.

It cannot Freeze the feature by itself.

The correct process remains:

```text
Prepare Freeze information
-> optionally ask External AI for help
-> bring the draft back
-> Preview Freeze Entry
-> review everything
-> Confirm and Write
```

Important:

```text
Preview Freeze Entry does not save anything.
```

The Freeze is written only when a person clicks:

```text
Confirm and Write
```

Never accept a statement from an external AI saying that a feature has already been frozen.

Only KANDA Reasoner’s confirmed local Freeze process is authoritative.

---

# 10. Using External AI with Error Memory

External AI may help explain an error or draft an Error Memory lesson.

It cannot save the lesson.

The correct process is:

```text
Collect the real error
-> ask External AI for help
-> bring the suggested lesson back
-> review it
-> check whether a similar lesson already exists
-> click Memorize Error only after approval
```

The external AI cannot press Memorize Error.

It cannot activate, replace or delete lessons.

---

# 11. Using External AI for architecture reviews

External AI can provide a second opinion about the Project architecture.

The external answer is only advice.

KANDA Reasoner’s local checks and validators remain more important.

The external AI cannot:

* Modify files.
* Approve installation.
* Confirm validation.
* Freeze a feature.
* Save Error Memory.
* Change which Project is selected.

Use the external answer to help you think, not as automatic authority.

---

# 12. Privacy and sensitive information

Anything pasted into an external AI website may leave your computer.

Before pressing Send, check that the message does not contain:

* Passwords.
* API keys.
* Access tokens.
* Private account information.
* Confidential client information.
* Patient names or identifying medical information.
* Personal documents.
* Private source code that must not be shared.
* Content from `.env` files.
* Secret company information.

KANDA Reasoner asks for approval before copying Project information so that you have a chance to review it.

Do not approve automatically.

---

# 13. Understanding the Tool and Project boundary

KANDA Reasoner is the Tool.

The Project is the software currently selected inside KANDA Reasoner.

They must normally remain separate.

The main rule is:

```text
Do not place KANDA Reasoner Tool code inside an external Project.

Do not place external Project code inside KANDA Reasoner.
```

External AI does not have permission to break this rule.

A special support folder may contain copies and handoff files:

```text
<project name>_show_project_to_AI
```

That folder may contain:

* Project copies.
* Prompts.
* Reports.
* Manifests.
* Validation evidence.
* Freeze information.
* Error Memory information.

However, it is not the real Project source and should not be used as an installation folder.

When KANDA Reasoner itself is the selected Project, the Tool and Project may use the same physical folder. Even then, KANDA Reasoner must still check which part owns each file.

---

# 14. What External AI is allowed to do

External AI may:

* Read the message you manually send.
* Explain code or architecture.
* Suggest changes.
* Suggest a refactoring plan.
* Suggest a Freeze draft.
* Suggest an Error Memory lesson.
* Give a second opinion.
* Help you understand an error.

---

# 15. What External AI is not allowed to do

External AI cannot:

* Access your computer automatically.
* Browse your Project files unless you send them.
* Install a patch.
* Change Project source.
* Validate local code.
* Confirm that installation succeeded.
* Confirm a Freeze.
* Memorize an error.
* Change KANDA Reasoner settings.
* Merge its answer into KANDA Reasoner automatically.
* Read other conversations inside KANDA Reasoner.
* Control the direct OpenRouter or Kilo conversation.

---

# 16. Common problems

## The External AI button is disabled

Check:

1. An external assistant was selected in Config AI.
2. The correct Project is selected.
3. The current screen has finished preparing its message.
4. The required Project information exists.
5. The external assistant has a valid official website.

## The wrong website opens

Return to:

```text
Config AI
-> External AI
```

Select the correct assistant and save it.

The selected assistant is shared by the External AI buttons.

## The website does not open

Try:

```text
Open Official Site
```

Also check:

* Your internet connection.
* Your default browser.
* Whether the website is temporarily unavailable.
* Whether the Readiness Check says REVIEW_DUE or STALE.

## Nothing is pasted automatically

This is normal.

KANDA Reasoner does not paste into external websites.

Press:

```text
Ctrl + V
```

manually.

## The answer does not appear inside KANDA Reasoner

This is also normal.

Copy the answer manually and paste it into the correct KANDA Reasoner screen.

## OpenRouter is not configured

External Web AI may still work.

External Web AI does not require KANDA Reasoner to read the website’s answer.

It only needs to copy the message and open the website.

## The AI answer includes code

Do not install it directly.

The code still needs:

* Review.
* Correct Project placement.
* Installation procedure.
* Validation.
* Regression checks.
* Freeze when appropriate.

## The AI says validation passed

Do not trust that statement as local validation.

Validation is authoritative only when it runs on your own Project and produces the required KANDA Reasoner success messages.

---

# 17. First-time setup checklist

```text
[ ] Open KANDA Reasoner.

[ ] Open Config AI.

[ ] Open External AI.

[ ] Select an approved assistant.

[ ] Save the selection.

[ ] Click Open Official Site.

[ ] Confirm that the correct website opens.

[ ] Sign in manually when needed.

[ ] Click Copy Test Prompt and Open.

[ ] Paste using Ctrl + V.

[ ] Send the test manually.

[ ] Run Readiness Check.

[ ] Read whether the result is CURRENT, REVIEW_DUE or STALE.
```

---

# 18. Normal use checklist

```text
[ ] Select the correct Project.

[ ] Open the correct KANDA Reasoner screen.

[ ] Prepare the question or task.

[ ] Click the External AI button.

[ ] Read the warning.

[ ] Review what will be copied.

[ ] Approve only when it is safe.

[ ] Wait for the AI website to open.

[ ] Paste using Ctrl + V.

[ ] Review the pasted message.

[ ] Press Send manually.

[ ] Read the external answer.

[ ] Copy the useful part.

[ ] Return to KANDA Reasoner.

[ ] Paste it into the correct workflow.

[ ] Run the required local checks before changing files.
```

---

# 19. Important rules to remember

```text
External Web AI is manual.

KANDA Reasoner copies and opens.

You paste and send.

The external website does not control your Project.

The answer does not return automatically.

External AI answers are suggestions, not proof.

Local validation remains authoritative.

Freeze requires human confirmation.

Memorize Error requires human confirmation.

Review all information before sending it outside your computer.
```

---

# 20. Simple example

Imagine you are reviewing a Project and want a second opinion.

You would:

1. Open the correct KANDA Reasoner review screen.
2. Click the External AI button.
3. Read the warning.
4. Approve copying.
5. Wait for the website to open.
6. Click the website’s message box.
7. Press `Ctrl + V`.
8. Read the message.
9. Press Send.
10. Read the answer.
11. Copy the useful part.
12. Return to KANDA Reasoner.
13. Paste the answer into the correct review area.
14. Use KANDA Reasoner’s normal validation before making any change.

That is the complete External Web AI process.
