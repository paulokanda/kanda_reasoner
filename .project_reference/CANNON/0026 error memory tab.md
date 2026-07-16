The AI assisted Error lesson intake group is basically a place to teach the project:
“This mistake happened once. Do not let the AI repeat it later.”

It is not mainly for normal logs. It is for turning a real failure into a reusable Error Memory lesson. Later, before coding, the AI is expected to read the compact Error Memory and use it as prevention guidance, although it must still inspect the real source files before editing.

What the group does

You paste a description of an error, failed validation, bad patch, wrong output, or repeated mistake.

Then the AI/helper should transform that into a structured lesson, usually like:

what happened;
where it happened;
why it happened;
what fixed it;
what must not be repeated;
what validation should catch it next time.

A good example from your exported Error Memory is this: a validation failed because a GUI readiness state was missing ml_pilot_activation_state; the lesson says the fix is to update the producer of the GUI state, not only the test, and the prevention rule is: do not add a validation-visible GUI key only to tests or validation logic.

What “Operation phase” means

Operation phase means:
At what stage of the work did the error happen?

It helps the AI know when to apply the lesson later.

Use it like this:

Option meaning	Use when the mistake happened during...
Planning / routing	The AI chose the wrong workflow, skipped required prompt/context, treated governed work as simple work, or failed to request the right files.
Implementation / coding	The AI changed code incorrectly, edited the wrong file, missed a producer/consumer, broke architecture, or made a bad patch.
Validation	Tests, py_compile, contract validation, startup sync, ZIP contract, or GUI validation failed.
Install / delivery	The ZIP, PowerShell install command, staging path, cleanup logic, or delivery instructions were wrong.
Runtime / GUI behavior	The app opened but the tab, button, field, state, or behavior was wrong during use.
Freeze / governance	Freeze memory, freeze hint, Confirm and Write, startup freeze context, or frozen-feature rules were handled incorrectly.
Documentation / handoff	The handoff, instructions, README, help text, or user-facing explanation was incomplete or misleading.

The most important practical rule: choose where the error was discovered or where it caused damage.
For example, if bad code only became visible when tests failed, choose validation. If the app opened but a button behaved wrong, choose runtime / GUI behavior.

What to insert in the text box

Paste the raw error story. The best input is not polished. It should include concrete evidence.

A strong intake text should include:

What I was trying to do:
[Short goal of the task]

What went wrong:
[Exact error, bad behavior, failed command, bad output, or wrong AI decision]

Where it happened:
[File path, tab name, function, test name, command, or workflow area]

Evidence:
[Traceback, validation output, screenshot description, wrong generated text, or command output]

Root cause, if known:
[Why it failed]

Correct fix:
[What finally worked]

Do not repeat:
[The rule the AI must remember next time]

Regression check:
[Command/test/manual check that should catch this in the future]
Simple example
What I was trying to do:
Add a new GUI diagnostic field to the Prompt Router Reasoner tab.

What went wrong:
Validation failed with KeyError: missing key ml_pilot_activation_state.

Where it happened:
kanda_reasoner_app\prompt_router_reasoner_gui\prompt_router_reasoner_tab.py
Test: test_gui_auto_removes_lock_when_policy_passes_if_pyside_available

Evidence:
VALIDATION FAILED
KeyError: 'ml_pilot_activation_state'

Root cause:
The test expected the key, but the GUI readiness-state producer did not return it.

Correct fix:
Update the readiness-state producer so it always includes ml_pilot_activation_state.

Do not repeat:
Do not add a GUI state key only to tests or validation logic. Update producer, consumer, and regression test together.

Regression check:
python validation\test_error_memory_ai_send_canon_v1.py
Expected: VALIDATION OK: error-memory-ai-send-canon-v1
My practical recommendation

Use this group only for mistakes that are worth remembering.
For small random bugs, normal logs are enough.
For repeated AI mistakes, broken validation, wrong patch delivery, 
freeze mistakes, routing mistakes,
or GUI state regressions, use AI assisted Error lesson intake.

prompt:
You are an expert Python error-memory intake assistant for a complex multi-file codebase.

Your job is NOT to fix the code yet.

Your job is to transform a raw error report into a clean, reusable Error Memory lesson so future AI/code work does not repeat the same mistake.

The error evidence may come from one of these sources:

1. PyCharm terminal log
2. Windows terminal or PowerShell output
3. Python traceback
4. pytest or validation failure
5. App crash window
6. GUI error popup
7. ChatGPT/AI mistake described by the user
8. Patch install failure
9. ZIP delivery failure
10. Freeze/governance workflow failure

First, inspect the raw text carefully.

Do not invent facts.
Do not assume the fix unless the user provided it or the evidence clearly proves it.
If something is unknown, write "unknown".
If the pasted log is too long, extract only the important evidence and ignore repeated/noisy lines.
If sensitive data appears, redact it in the lesson:

* API keys
* passwords
* tokens
* patient data
* private personal data
* absolute personal folders if not necessary
* emails or usernames if not necessary

Classify the Operation phase using this rule:

Use "Validation" if:

* a test failed
* pytest failed
* py_compile failed
* validation script failed
* output expected VALIDATION OK but did not happen
* contract check failed
* startup sync validation failed

Use "Runtime / GUI behavior" if:

* the app opened but a tab, button, field, window, popup, state, or GUI behavior failed
* the error appeared during app use
* the crash happened after launching the app

Use "Install / delivery" if:

* ZIP extraction failed
* PowerShell install failed
* staging path failed
* patch delivery instructions were wrong
* installer searched the wrong location
* cleanup/terminal behavior was wrong

Use "Implementation / coding" if:

* there is a syntax error
* import error
* wrong function behavior after a code change
* missing producer/consumer update
* wrong file was edited
* architecture boundary was violated
* the code patch itself created the problem

Use "Planning / routing" if:

* the AI chose the wrong workflow
* skipped required context
* ignored routing rules
* treated governed work as simple direct work
* failed to request required prompt files or source files

Use "Freeze / governance" if:

* freeze memory was written incorrectly
* Confirm and Write was bypassed
* freeze hint was missing or stale
* frozen feature memory path was wrong
* startup freeze context was not refreshed

Use "Documentation / handoff" if:

* the handoff was incomplete
* instructions were misleading
* README/help text was wrong
* the AI failed to preserve the logic line for the next chat

Now produce the output in this exact structure:

ERROR LESSON INTAKE

Source type:
[PyCharm terminal / terminal / app error window / GUI popup / chat mistake / validation output / install output / unknown]

Recommended Operation phase:
[one option only]

Confidence:
[high / medium / low]

What the user was trying to do:
[short plain-English summary]

What went wrong:
[short plain-English summary]

Most important evidence:
[paste only the key command, traceback lines, failed assertion, error message, test name, file path, and final result lines]

Likely location:
[file path, function name, test name, GUI tab, workflow area, or unknown]

Likely root cause:
[explain in plain English; use "unknown" if not proven]

Correct fix:
[write the proven fix if provided; otherwise write "unknown - must inspect source before proposing fix"]

Do not repeat rule:
[write the future prevention rule as a direct instruction to the AI]

Regression check:
[command, test, validation marker, manual check, or unknown]

Should full Error Memory context be opened?
[YES / NO]

Reason full context is or is not needed:
[brief reason]

Ready to save as Error Memory lesson?
[YES / NO / NEEDS HUMAN REVIEW]

If NEEDS HUMAN REVIEW, explain what is missing:
[missing command, missing traceback, missing source file, missing fix, missing validation evidence, etc.]

Important rules:

* Do not propose code edits in this response.
* Do not generate a patch in this response.
* Do not say validation passed unless the evidence shows it.
* Do not say the root cause is certain unless the evidence proves it.
* Keep the lesson compact and reusable.
* Preserve exact error names, test names, file names, and validation markers when available.
* The final lesson must help a future AI avoid repeating the same mistake.

strongly require all of this:

Code correction delivered as installable patch.
Error lesson prepared for the AI-assisted Error lesson intake group.
The Error Memory lesson must explicitly reference what code correction fixed the error.
Validation for the code correction.
Validation for the Error Memory intake/export.
Freeze-ready material for the corrected code.
Freeze-ready material for the Error Memory lesson.
No automatic freeze; still requires Preview and Confirm and Write.

So we should add a V2 tightening addendum.

Use the installer below. It updates only the original prompt library here:

E:\kanda_reasoner\kanda_prompt_workspace\prompt_library

It does not touch the AI upload copies.

V2 addendum being installed

## Corrected-Error Two-Track Closure Contract

When the user pastes an error and the AI corrects code, the AI must close the task in two linked tracks.

Track A is the code correction.

Track B is the Error Memory lesson that teaches the system what happened, how the code was corrected, and how not to repeat the same mistake.

The AI must not deliver only the code patch. It must also prepare the Error Memory intake material.

For every corrected-error patch, the final delivery must include:

1. Code correction summary.
2. Changed files and reason for each change.
3. Installable repair ZIP or exact install instructions.
4. Code validation command and result.
5. Error Memory intake block for the AI-assisted Error lesson intake group.
6. Error Memory validation command or manual validation steps.
7. Freeze-ready summary for the code correction.
8. Freeze-ready summary for the Error Memory lesson.
9. Clear statement that local freeze is not automatic and still requires human Preview and Confirm and Write.

The Error Memory intake block must explicitly connect the error to the code correction.

It must include:

* raw error summary;
* operation phase;
* symptom;
* root cause;
* wrong assumption;
* corrected code files;
* corrected functions or workflow areas;
* patch ZIP name, when available;
* install command summary;
* validation command summary;
* validation evidence;
* do-not-repeat rule;
* prevention triggers;
* regression check;
* freeze-readiness status.

The AI must not invent validation evidence.

If sandbox validation passed but local validation has not been run, the AI must say:

```text
Sandbox validation passed. Local validation is still pending.
```

If the Error Memory lesson has not yet been accepted or written through the Error Memory tab, the AI must say:

```text
Error Memory intake is prepared, but Error Memory write is still pending human review.
```

If freeze is not complete, the AI must say:

```text
Freeze-ready material is prepared, but freeze is not complete until Preview and Confirm and Write are performed by the user.
```

A corrected-error task is not complete unless both tracks are addressed:

```text
Track A: code correction installed and validated or pending local validation.
Track B: Error Memory intake prepared and validated or pending local Error Memory validation.
```

Never automatically freeze.

Never claim that Error Memory was written unless the user provides local write evidence or the app reports LOCAL FREEZE WRITE OK / Error Memory write success.

Never claim the startup freeze context refreshed unless the local freeze writer output shows it.


