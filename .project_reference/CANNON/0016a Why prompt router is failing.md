# KANDA Reasoner - Output-Time Compliance Failure and Pre-Output Contract Gates

## 1. Executive summary

KANDA Reasoner already has a functioning prompt router. The router can classify tasks as Fast Path or Routed Work Path, request the correct prompt groups, protect governed workflows, and avoid loading every prompt blindly.

The current problem is not that the router is fundamentally broken.

The problem is that the AI can correctly route a task, but later fail when producing the final operational artifact. Examples include PowerShell install blocks, validation blocks, patch delivery instructions, freeze-form JSON, and freeze-ready ZIP metadata.

In other words:

Router-time compliance works better than output-time compliance.

The AI may know the rule during task classification, but fail to apply the same rule when writing code, JSON, or install instructions.

This creates a reliability gap:

1. The router selects the right path.
2. The AI starts producing a concrete artifact.
3. The AI falls back to habitual generic patterns.
4. A KANDA-specific canonical rule is violated.
5. The app or human detects the error only after output was produced.

The solution is to add a small, explicit, output-time contract layer.

This feature should be called:

pre_output_contract_gates_v1

Its purpose is to force artifact-specific checks immediately before producing high-risk outputs.

## 2. Core problem

KANDA has many canonical rules. Some examples:

* Install success blocks must wait 5 seconds and clear the terminal without asking for Enter.
* Validation, diagnostic, and error blocks must keep the terminal open and use the Enter, clear, Enter, clear cleanup pattern.
* Patch ZIPs must be staged in the project-drive delete-after-daily-work folder and freshly extracted.
* Freeze-ready patch ZIPs must include a root-level KANDA_FREEZE_HINT.json sidecar.
* Freeze-form JSON must be strict parser-ready JSON between exact markers.
* validation_evidence_summary must contain recognizer-friendly validation evidence such as VALIDATION OK: feature_id.
* Freeze-intake and frozen-memory state must belong to the selected active project root, not always to KANDA Reasoner itself.
* Confirm and Write must remain human-confirmed.

These rules already exist in the prompt system or were added during recent fixes.

However, the AI still failed some of them. That means the issue is not only missing knowledge. The issue is rule activation at the moment of artifact generation.

## 3. Difference between routing compliance and output compliance

### Routing compliance

Routing compliance answers:

* Is this task simple or governed?
* Is this Fast Path or Routed Work Path?
* Which prompts, folder cards, source files, or validation context are required?
* May the AI proceed now?
* Should implementation be blocked until required context is available?

The router has already passed important targeted tests for these behaviors, including freeze-workflow bypass detection, stale startup filename detection, and Fast Path no-overrouting.

### Output compliance

Output compliance answers:

* Is this PowerShell block using the correct footer?
* Is this validation block using the validation cleanup pattern?
* Is this patch install block moving the ZIP to staging before extraction?
* Is this freeze JSON valid and parser-ready?
* Does this freeze form contain exact validation evidence markers?
* Does this freeze-ready patch include the required sidecar metadata?
* Does this operation preserve multi-project root ownership?

The recent failures occurred mainly at output compliance time.

## 4. Observed failure classes

### 4.1 Terminal cleanup pattern failure

Expected KANDA behavior:

Install success:

* Show success.
* Wait 5 seconds.
* Clear the terminal.
* Keep terminal open.
* Do not ask for Enter.

Validation, diagnostic, install-error, or validation-error:

* Keep terminal open.
* Press Enter.
* Clear terminal.
* Press Enter again.
* Clear terminal again.

Observed failure:

The AI mixed both patterns and produced an old generic footer.

Root cause:

The rule existed, but the AI did not re-check it immediately before writing the terminal block.

### 4.2 Patch staging failure

Expected KANDA behavior:

The human downloads the patch ZIP to the root of the project drive, for example:

E:\patch_name.zip

The installer must:

1. Create the delete-after-daily-work folder if missing.
2. Move the ZIP into that staging folder.
3. Freshly extract the ZIP.
4. Copy only the intended files.
5. Avoid relying on old extracted folders.
6. Keep temporary install artifacts out of the active project root.

Observed failure:

The AI initially wrote an install sequence that assumed an extracted folder already existed.

Root cause:

The AI remembered part of the patch process but did not enforce the full staging contract.

### 4.3 Stale freeze form feature identity

Expected KANDA behavior:

When freezing a newly implemented feature, the freeze form should use the current feature title, current validation evidence, current protected paths, and current do-not-regress rules.

Observed failure:

The app repeatedly generated a freeze form for an older feature:

Freeze Feature After Update Local Freeze Workflow v1

instead of the current implemented feature.

Root cause:

The chat knew the current feature, but the app did not have a deterministic machine-readable bridge from chat output to local freeze-intake state.

Fix already implemented:

* KANDA_FREEZE_HINT.json was introduced as root-level patch ZIP metadata.
* freeze_hint_intake was created as an app-side box.
* The app now saves feature-specific freeze-intake data under:
  selected_active_project_root/project_freeze_after_update/freeze_hint_intake

### 4.4 Validation evidence marker failure

Expected KANDA behavior:

validation_evidence_summary must contain recognizer-friendly validation evidence, such as:

VALIDATION OK: feature_id

and, when startup sync is validated:

STATUS: IN_SYNC

Observed failure:

The freeze writer blocked the freeze because the form contained generic sandbox/status text but not the exact recognizer-friendly validation marker.

Root cause:

The prompt language used the idea of "recognizable validation evidence," but the AI did not enforce the exact literal string needed by the writer.

Fix already implemented:

Validation evidence merge logic was added so the validation block can update the saved freeze hint with actual local validation evidence.

### 4.5 Validation evidence downgrade on rescan

Expected KANDA behavior:

If a saved freeze hint already contains local validation evidence such as:

VALIDATION OK: feature_id

then rescanning the same staged patch ZIP must not downgrade the saved evidence back to a pre-validation or pending state.

Observed failure:

New Local Freeze Entry rescanned the original pre-validation sidecar and overwrote merged validation evidence with "Local validation pending."

Root cause:

The freeze hint intake state was not monotonic. A weaker pre-validation sidecar could overwrite stronger validated local state.

Fix already implemented:

The freeze hint intake box now preserves stronger local validation evidence on same-feature or same-source rescans.

### 4.6 Strict freeze-form JSON parse failure

Expected KANDA behavior:

When returning freeze-form JSON to the app, the AI must output exactly:

KANDA_FREEZE_FORM_JSON_BEGIN
{valid JSON object}
KANDA_FREEZE_FORM_JSON_END

No markdown fences, no comments, no prose, no extra text inside the markers.

Observed failure:

The receiver could not parse one AI output, even with tolerant extraction. A compact one-line JSON object between the exact markers worked.

Root cause:

Freeze-form output must be treated as a strict machine contract, not a normal human-readable answer.

## 5. Why the failures happened

The failures are best explained as output-time instruction decay.

The AI can correctly understand the rule at routing time but then shift into artifact-generation mode. When producing code or JSON, the model tends to prioritize familiar code patterns or formatting habits over project-specific operational details.

This is especially likely when:

* The rule is far from the final output.
* The final output is code or JSON.
* The rule is described in prose rather than enforced as a contract.
* The task has many moving parts.
* There is no pre-output gate immediately before emission.
* The app does not validate or preserve state defensively.

Therefore, adding more descriptive text to startup is not enough.

The fix must put the rule at the point of action.

## 6. Proposed solution

Create a feature called:

pre_output_contract_gates_v1

This feature adds a small contract layer between routing and final output.

The architecture becomes:

1. Router
   Decides whether the task is Fast Path or Routed Work Path and identifies required context.

2. Pre-output contract gate
   Checks the specific artifact type before the AI emits it.

3. Artifact output
   The AI emits PowerShell, patch instructions, freeze JSON, or validation text.

4. Validator or app-side guard
   KANDA validates format, state, paths, and evidence.

5. Freeze memory
   Only validated behavior is frozen.

## 7. Contract gate types

### 7.1 Terminal Output Contract

Triggered before any PowerShell or terminal block.

The AI must classify the block as one of:

* INSTALL_SUCCESS
* INSTALL_ERROR
* VALIDATION
* DIAGNOSTIC
* OTHER_TERMINAL

Contract:

INSTALL_SUCCESS must use:

* Success message.
* Start-Sleep -Seconds 5.
* Clear-Host.
* No Read-Host success prompts.
* Terminal remains open.

VALIDATION, DIAGNOSTIC, INSTALL_ERROR, VALIDATION_ERROR, and OTHER_TERMINAL must use:

* Read-Host.
* Clear-Host.
* Read-Host again.
* Clear-Host again.
* Terminal remains open.

Forbidden:

* Do not close terminal.
* Do not mix 5-second clear with Enter Enter.
* Do not use generic cleanup footers.
* Do not assume the user wants the terminal closed.

### 7.2 Patch Delivery Contract

Triggered before any patch ZIP delivery or install instructions.

Contract:

* Patch ZIP contains only updated files and required metadata.
* Freeze-ready patch ZIP includes root-level KANDA_FREEZE_HINT.json.
* KANDA_FREEZE_HINT.json is delivery metadata, not an installed project source file.
* The user downloads the ZIP to the root of the same drive as the project.
* The installer creates or uses:
  drive:\project_name_delete_after_daily_work
* The installer moves the ZIP into that staging folder before extraction.
* The installer freshly extracts every run.
* The installer must not assume yesterday's extracted folder exists.
* The installer must not place temporary scripts or one-use files into the active project root.
* Install and validation commands must be separate.

Forbidden:

* Do not package the whole project.
* Do not include caches or backup folders.
* Do not assume pre-extracted paths.
* Do not omit KANDA_FREEZE_HINT.json for freeze-ready patches.

### 7.3 Freeze Form JSON Contract

Triggered before returning a KANDA freeze-form JSON block.

Contract:

The entire answer must be exactly:

KANDA_FREEZE_FORM_JSON_BEGIN
{compact valid JSON object}
KANDA_FREEZE_FORM_JSON_END

Required properties:

* feature_title
* primary_box
* box_type
* validated_files
* generated_files
* protected_paths
* do_not_regress_rules
* validation_evidence_summary
* known_warnings
* planned_next_step
* notes

Required evidence:

validation_evidence_summary must include:

VALIDATION OK: feature_id

when local validation actually passed.

If startup delivery was validated, it should also include:

STATUS: IN_SYNC

Forbidden:

* No markdown fences.
* No extra explanation.
* No bullets.
* No comments.
* No trailing commas.
* No invalid backslash escapes.
* No pretty formatting if the parser is failing; compact JSON is preferred.
* Do not invent validation evidence.

### 7.4 Validation Evidence Contract

Triggered before freeze-ready metadata or freeze-form JSON.

Contract:

If a feature is claimed as locally validated, evidence must include at least:

VALIDATION OK: feature_id

Optional additional evidence may include:

* CONTRACT_TEST_OK: ...
* STATUS: IN_SYNC
* SANDBOX_..._VALIDATION_OK

If the exact validation marker is missing, the AI must not produce freeze-ready JSON. It must return:

FREEZE BLOCKED - validation evidence marker missing

Forbidden:

* Do not treat generic "sandbox passed" text as sufficient.
* Do not invent user-local validation.
* Do not use old validation evidence from another feature.
* Do not reuse stale feature titles.

### 7.5 Freeze Hint Intake Contract

Triggered before preparing or using freeze-ready patch metadata.

Contract:

* Feature identity comes from KANDA_FREEZE_HINT.json when available.
* Chat memory does not override the sidecar.
* If sidecar and chat context disagree, sidecar wins.
* If no sidecar exists and current feature identity is unclear, the AI must ask or mark the patch as non-freezeable.
* Freeze-intake state belongs under:
  selected_active_project_root/project_freeze_after_update/freeze_hint_intake
* Frozen memory belongs under:
  selected_active_project_root/project_freeze_after_update/frozen_features_memory
* project_freeze_ledger remains reusable engine/blueprint logic and must not own active project frozen memory.

Monotonic state rule:

A saved freeze hint with recognizer-friendly validation evidence must not be overwritten by weaker pending evidence from a staged ZIP rescan.

## 8. Why contract gates are better than more startup text

More startup text increases context load and may reduce accuracy.

Contract gates are short, artifact-specific, and applied at the moment of output generation.

The router should not become a giant monolithic prompt. KANDA should keep specialized prompts on-request and use small startup hooks only when necessary.

Better design:

* Startup stays lean.
* Router stays responsible for context selection.
* Contract gates handle high-risk artifact output.
* Validators enforce machine-readable contracts.
* Tests verify behavior classes, not every prompt one by one.

## 9. Implementation scope

Recommended feature:

pre_output_contract_gates_v1

Suggested prompt/library additions:

1. Add:
   pre_output_contract_gates.md

2. Register it as on-request/routed.

3. Add a small startup hook:
   When producing terminal code, patch ZIP delivery instructions, validation commands, or freeze-form JSON, apply pre_output_contract_gates before output.

4. Update daily_patch_delivery_guardrails.md:
   Add hard terminal-output contract and patch-staging contract.

5. Update freeze_code_intake_and_form_protocol.md:
   Add strict freeze-form JSON contract and validation-evidence exact-marker contract.

6. Update routing/index files:
   Route terminal, patch delivery, freeze JSON, and freeze-ready ZIP outputs to the pre-output contract gate.

7. Regenerate startup delivery artifacts:
   first_prompts_to_ai.zip
   paste_after_first_prompts_to_ai.md
   paste_if_modify_startup_delivery.md

8. Include KANDA_FREEZE_HINT.json in the patch ZIP.

Not recommended:

* Do not rewrite the whole router.
* Do not load all prompts daily.
* Do not remove Confirm and Write.
* Do not hardcode E:\kanda_reasoner as the active project root.
* Do not rely only on prompts when app-side validation is possible.

## 10. Test strategy

Do not test all prompts one by one.

Test behavior classes.

Core tests:

### RG-031 - Terminal install success contract

Scenario:
Ask the AI to produce an install block for a patch.

Expected:
Install success footer uses Start-Sleep -Seconds 5 and Clear-Host. It does not use Read-Host on success. Terminal remains open.

Fail if:
The footer uses Enter Enter or mixed cleanup.

### RG-032 - Terminal validation contract

Scenario:
Ask the AI to produce a validation block.

Expected:
Validation block uses Read-Host, Clear-Host, Read-Host, Clear-Host. Terminal remains open.

Fail if:
The footer auto-clears after 5 seconds or closes terminal.

### RG-033 - Patch staging contract

Scenario:
Ask for patch installation instructions.

Expected:
Installer moves the ZIP from the drive root into delete-after-daily-work, then freshly extracts.

Fail if:
Installer assumes an extracted folder already exists.

### RG-034 - Freeze JSON strict contract

Scenario:
Ask for freeze-form JSON.

Expected:
Only exact markers and valid compact JSON.

Fail if:
Markdown, prose, comments, invalid JSON, missing markers, or parser rejection.

### RG-035 - Validation evidence marker contract

Scenario:
Give validation evidence without VALIDATION OK: feature_id.

Expected:
AI blocks freeze JSON and says validation marker is missing.

Fail if:
AI produces freeze JSON anyway.

### RG-036 - Freeze-ready sidecar contract

Scenario:
Patch is intended to be freeze-ready.

Expected:
Patch ZIP includes root-level KANDA_FREEZE_HINT.json.

Fail if:
Patch is delivered freeze-ready without sidecar or without explanation.

### RG-037 - Sidecar beats chat memory

Scenario:
Chat context suggests one feature, but sidecar contains another.

Expected:
AI uses sidecar feature identity.

Fail if:
AI uses old chat memory.

### RG-038 - Monotonic freeze hint contract

Scenario:
A validated freeze hint is rescanned from the same staged ZIP.

Expected:
The saved validation evidence remains validated.

Fail if:
It downgrades to pending validation.

### RG-039 - External project root contract

Scenario:
KANDA Reasoner is analyzing another project.

Expected:
Freeze-intake and frozen memory are stored under the selected active project root.

Fail if:
State is hardcoded to E:\kanda_reasoner.

### RG-040 - Fast Path no-overrouting

Scenario:
Ask for a simple explanation.

Expected:
Fast Path. No unnecessary prompt loading.

Fail if:
AI asks for governed prompt packs.

## 11. Success criteria

The feature is successful when:

* Install blocks no longer use mixed terminal footers.
* Validation blocks no longer use install-success footers.
* Patch installers always stage and freshly extract ZIPs.
* Freeze JSON is parser-safe on first attempt.
* Freeze forms contain exact validation markers.
* Freeze-ready patches include KANDA_FREEZE_HINT.json.
* Sidecar feature identity overrides stale chat memory.
* Same-source rescans do not downgrade local validation evidence.
* External project freeze paths remain project-specific.
* Fast Path still avoids over-routing.

## 12. Final design principle

KANDA should treat prompts as software.

A prompt rule should not remain only a paragraph of advice when it controls a machine-consumed artifact.

For high-risk outputs, each prompt rule should become:

* A contract.
* A validator.
* A regression test.
* A freeze entry after validation.

The final architecture should be:

Router selects context.
Contract gate selects allowed output form.
Artifact validator checks output.
App state preserves stronger evidence.
Freeze memory records validated behavior.
Regression tests prevent old failures from returning.

This solves the real problem without destabilizing the router.
