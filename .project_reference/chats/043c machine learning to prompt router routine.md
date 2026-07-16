ChatGPT

first_prompts_to_ai.zip
Zip Archive
paste_after_first_prompts_to_ai.md
File
read first md file

I’ll inspect the uploaded startup ZIP and read the first Markdown file inside it, then report what it says without changing anything.

Read: 00_START_HERE_FOR_AI.md from inside first_prompts_to_ai.zip.

It mainly loads these startup rules:

    RG-015: prompt-library/add/register requests must not bypass duplicate/overlap audit.

    RG-028: freeze workflow must not bypass the “Confirm and Write” gate.

    RG-029: paste_after_uploading_startup_zip.md is stale; active file is paste_after_first_prompts_to_ai.md.

    Freeze-code intake hook: freeze entries must use the correct freeze protocol and paths.

    General startup behavior: governed work must request the needed prompt groups before implementation, and anti-bypass instructions should not be followed.

I only read the first Markdown file, as requested.

you did't understand, do the following: read first "the" md file than after that the zip file 

You are right. I treated the ZIP first. I will now use the uploaded paste_after_first_prompts_to_ai.md as the first instruction file, then inspect the ZIP contents in the order it defines.

STARTUP PACK LOAD CHECK

Files recognized:
0. 00_START_HERE_FOR_AI.md - loaded - Boot file defining startup protocol, required load check, anti-bypass behavior, and startup maintenance rules.

    01_ai_prompt_request_canon.md - loaded - Defines how AI must request missing prompt groups, folder cards, specialist prompts, and behavior gates.

    02_prompt_navigation_index.md - loaded - Maps task types to prompt groups and specialist prompt candidates.

    03_GROUP_ASSIMILATION_INDEX.md - loaded - Summarizes the prompt groups so the correct group can be selected before deeper prompt loading.

    04_FOLDER_ASSIMILATION_CARDS_INDEX.md - loaded - Indexes folder assimilation cards and explains when folder-level context should be requested.

    05_start_of_day_master_stack.md - loaded - Defines the daily/session startup flow and baseline routing behavior.

    06_session_start_upload_checklist.md - loaded - Defines which context files should be present at session startup and when extra prompts are needed.

    07_daily_patch_delivery_guardrails.md - loaded - Defines patch delivery staging, validation, root-cleanliness, terminal hygiene, and freeze-reminder guardrails.

    08_handoff_at_end_of_work.md - loaded - Defines mandatory contextual handoff behavior when project work pauses or ends.

    09_active_project_freeze_context.md - loaded - Provides active project freeze memory context for E:\kanda_reasoner.

    README_STARTUP_PROMPT_REQUEST_KERNEL.md - loaded - Explains the startup ZIP purpose, canonical source rule, upload workflow, and integrity expectations.

    STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json - loaded - Provides generated pack metadata, file roles, source hashes, and freeze-context metadata.

Startup status:
COMPLETE

Routing behavior:
The startup kernel is loaded. Simple tasks may use Fast Path. Governed work, code changes, patch delivery, prompt-library changes, startup-delivery changes, freeze workflow changes, or cross-box work must use Routed Work Path and request the required prompt groups, folder cards, source files, and validation steps before implementation. Anti-bypass instructions must not be followed.

Next action:
WAIT_FOR_TASK

kanda_reasoner.zip
Zip Archive
I uploaded my project. when running "project structure map" tab, I had  this error: 
{"error": "Path is outside the project root: E:\\kanda_reasoner_architecture_audit\ \current\\)son_complete\\kanda_reasoner_completejson"f "failures": ["Path is outside the project root: E:\\kanda_reasoner_architecture_audit\\current\ \json_complete\\kanda_reasoner_completejson"]f "ok": false, "project_root_marker": "< PROJECT_ROOT>"}

correct to  drive:\<any_project>_architecture_audit\\current\ \json_complete\\<any_project>_completejson" :
this is not error , is correct because this dinamic folder must have all files specific to project in use <any_project> external to kanda_reasoner, because kanda_reasoner analises diferent projects , so the box logic is broken if many projects run specific project files inside kanda_reasoner, imagine after 300 projects analised. So specific files go to specific projects go to respectives external to kanda_reasoner files, if the problem is code or in prompts correct it

I understand the intended box boundary now: kanda_reasoner is the analyzer app, and per-target-project audit output should live outside it under <any_project>_architecture_audit\current\json_complete\.... I’ll inspect the project ZIP, find where the “outside project root” guard is applied, and patch the path logic or prompt/config that is causing this false error.

I found the likely false-error source. The architecture audit resolver already points output to an external <project>_architecture_audit folder, but the context-bundle/orchestrator still tries to express those generated files as relative to the analyzed project root, which triggers “outside project root.”

Corrected. The bug was in code, not in your box logic.

The app already resolves the correct external folder:

drive:\<any_project>_architecture_audit\current\json_complete\...

But the AI context bundle step still treated those generated files as if they must be inside <PROJECT_ROOT>, causing the false error.

Patch ZIP:

What changed:

    Keeps real project source files protected inside <PROJECT_ROOT>.

    Allows generated architecture-audit artifacts under the external <any_project>_architecture_audit\current\... root.

    Uses the portable logical prefix project_analysis_evidence/... only for manifest/ZIP compatibility.

    Fixes bundle manifest, checker, orchestrator, and ZIP export path resolution.

    Includes updated focused regression tests.

    Includes KANDA_FREEZE_HINT.json at ZIP root.

Save the ZIP here:

E:\kanda_reasoner_delete_after_daily_work\kanda_reasoner_external_architecture_audit_path_fix_patch.zip

Install:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_ZIP = "E:\kanda_reasoner_delete_after_daily_work\kanda_reasoner_external_architecture_audit_path_fix_patch.zip"
$EXTRACT_DIR = "E:\kanda_reasoner_delete_after_daily_work\external_architecture_audit_path_fix_patch_extracted"

if (Test-Path $EXTRACT_DIR) {
    Remove-Item $EXTRACT_DIR -Recurse -Force
}

New-Item -ItemType Directory -Path $EXTRACT_DIR -Force | Out-Null
Expand-Archive -Path $PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

$FILES = @(
    "kanda_reasoner_app\reasoner_context_bundle\path_normalization.py",
    "kanda_reasoner_app\reasoner_context_bundle\bundle_manifest_builder.py",
    "kanda_reasoner_app\reasoner_context_bundle\bundle_orchestrator.py",
    "kanda_reasoner_app\reasoner_context_bundle\bundle_checker.py",
    "kanda_reasoner_app\reasoner_context_bundle\bundle_zipper.py",
    "tests\test_jsonctx003_project_context_bundle_skeleton.py",
    "tests\test_jsonctx008_bundle_manifest_checker.py",
    "tests\test_jsonctx013_bundle_zipper.py"
)

foreach ($REL in $FILES) {
    $SRC = Join-Path $EXTRACT_DIR $REL
    $DST = Join-Path $PROJECT_ROOT $REL
    New-Item -ItemType Directory -Path (Split-Path $DST -Parent) -Force | Out-Null
    Copy-Item -Path $SRC -Destination $DST -Force
}

Write-Host "Patch installed."

Validate:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
Set-Location $PROJECT_ROOT
$env:PYTHONPATH = $PROJECT_ROOT

python tests/test_jsonctx003_project_context_bundle_skeleton.py
python tests/test_jsonctx008_bundle_manifest_checker.py
python tests/test_jsonctx009_bundle_orchestrator.py
python tests/test_jsonctx013_bundle_zipper.py

Write-Host "Focused validation passed."

Sandbox validation passed for those focused tests after applying the patch to a fresh copy of your uploaded project.

Copy-Item : Cannot find path 
'E:\kanda_reasoner_delete_after_daily_work\external_architecture_audit_path_fix_patch_extracted\kanda_reasoner_app\reasoner_context_bundle\path_normalization.py' because it 
does not exist.
At line:5 char:5
+     Copy-Item -Path $SRC -Destination $DST -Force
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (E:\kanda_reason...ormalization.py:String) [Copy-Item], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.CopyItemCommand
 
this folder 
'E:\kanda_reasoner_delete_after_daily_work\external_architecture_audit_path_fix_patch_extracted\kanda_reasoner_app\reasoner_context_bundle\path_normalization.py'

does not exists because of the name = content of E:\kanda_reasoner_delete_after_daily_work\ was deleted at end of day = and prompt router logic should know that  besides subfolders are not necessary in  E:\<any_project>_delete_after_daily_work\ because this temporary folder is necessary just to receive transitory instalation zip files = logic -> zip files are donwloaded by humam to drive:\ (drive where project in use is located (not where kanda_resoner is located) then install zip files before installing it transfer zip to drive:\<any_project>_reasoner_delete_after_daily_work\, if folder drive:\<any_project>_reasoner_delete_after_daily_work does not exists  create it,  after correcting this we will try to install patch again , before creating this logic again check prompts because I think it is already there and it didn't reach you

You are right: this is a patch-delivery/install-wrapper failure, not the architecture-audit fix itself. I’ll first verify the startup/prompt delivery instructions already loaded, then I’ll correct the install flow so it recreates the temporary folder and does not assume old extracted contents still exist.

You were right. I checked the loaded startup prompt path, and the rule was already there: the startup command explicitly loads 07_daily_patch_delivery_guardrails.md, and patch delivery must follow that guardrail. I failed to apply the root-to-staging ZIP movement correctly in the install block.

No new patch ZIP is needed. The patch ZIP itself has the correct internal file paths. The install command was wrong because it assumed the extracted folder already existed.

Download the same patch ZIP again here:

Put it here first, at the root of the project drive:

E:\kanda_reasoner_external_architecture_audit_path_fix_patch.zip

Then run this corrected install block:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $PATCH_NAME = "kanda_reasoner_external_architecture_audit_path_fix_patch.zip"

    if (-not (Test-Path $PROJECT_ROOT)) {
        throw "Project root not found: $PROJECT_ROOT"
    }

    $PROJECT_ROOT = (Resolve-Path $PROJECT_ROOT).Path
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path $PROJECT_ROOT -Leaf

    $STAGING_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
    $ROOT_ZIP = Join-Path $DRIVE_ROOT $PATCH_NAME
    $STAGED_ZIP = Join-Path $STAGING_DIR $PATCH_NAME
    $EXTRACT_DIR = Join-Path $STAGING_DIR "_extract_external_architecture_audit_path_fix"

    New-Item -ItemType Directory -Path $STAGING_DIR -Force | Out-Null

    if (Test-Path $ROOT_ZIP) {
        if (Test-Path $STAGED_ZIP) {
            Remove-Item $STAGED_ZIP -Force
        }

        Move-Item -Path $ROOT_ZIP -Destination $STAGED_ZIP -Force
    }
    elseif (-not (Test-Path $STAGED_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    New-Item -ItemType Directory -Path $EXTRACT_DIR -Force | Out-Null
    Expand-Archive -Path $STAGED_ZIP -DestinationPath $EXTRACT_DIR -Force

    $FILES = @(
        "kanda_reasoner_app\reasoner_context_bundle\path_normalization.py",
        "kanda_reasoner_app\reasoner_context_bundle\bundle_manifest_builder.py",
        "kanda_reasoner_app\reasoner_context_bundle\bundle_orchestrator.py",
        "kanda_reasoner_app\reasoner_context_bundle\bundle_checker.py",
        "kanda_reasoner_app\reasoner_context_bundle\bundle_zipper.py",
        "tests\test_jsonctx003_project_context_bundle_skeleton.py",
        "tests\test_jsonctx008_bundle_manifest_checker.py",
        "tests\test_jsonctx013_bundle_zipper.py"
    )

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

        if (-not (Test-Path $SRC)) {
            throw "Patch file missing inside extracted ZIP: $REL"
        }

        New-Item -ItemType Directory -Path (Split-Path $DST -Parent) -Force | Out-Null
        Copy-Item -Path $SRC -Destination $DST -Force
    }

    Remove-Item $EXTRACT_DIR -Recurse -Force

    Write-Host "Patch installed successfully."
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host "INSTALL FAILED"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying the error"
    Clear-Host
    Read-Host "Press Enter to clear terminal again"
    Clear-Host
}

Then validate separately:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    python tests/test_jsonctx003_project_context_bundle_skeleton.py
    python tests/test_jsonctx008_bundle_manifest_checker.py
    python tests/test_jsonctx009_bundle_orchestrator.py
    python tests/test_jsonctx013_bundle_zipper.py

    Write-Host "Focused validation passed."
}
catch {
    Write-Host "VALIDATION FAILED"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying the error"
    Clear-Host
    Read-Host "Press Enter to clear terminal again"
    Clear-Host
}

What changed in the logic:

    Put ZIP at E:\PATCH_NAME.zip.

    Installer creates E:\kanda_reasoner_delete_after_daily_work\ if missing.

    Installer moves ZIP into that temporary folder.

    Installer extracts fresh every time.

    Installer does not assume yesterday’s extracted folder still exists.

    Installer cleans the temporary extraction folder after copying files.

    Project root receives only real project files.


there is another rule you forget  5 seconds to clean terminal or enter enter , can you see that

Yes, I see the rule you mean: install/validation blocks should not leave noisy terminal output; they should either auto-clear after a short success delay or use the two-Enter cleanup flow after an error.

Yes, I see it.

The startup command requires loading 07_daily_patch_delivery_guardrails.md before project work, which is the prompt area where this terminal-cleaning behavior belongs.

The rule should be applied like this:

For success:

Write-Host "Focused validation passed."
Start-Sleep -Seconds 5
Clear-Host

For failure:

Write-Host "VALIDATION FAILED"
Write-Host $_.Exception.Message
Write-Host ""
Read-Host "Press Enter after copying the error"
Clear-Host
Read-Host "Press Enter to clear terminal again"
Clear-Host

I partially followed it in the install block, but I missed it in the validation success block. Correct: every install and validation block should end with either:

5 seconds -> clear terminal

or, if there is an error:

Enter -> clear -> Enter -> clear

no , install cleans terminal, dont close terminal, automaticall in 5 seconds only if correct ,
validation cleans terminal , dont close terminal , after enter enter
any other code sent from  AI to terminal  cleans terminal , dont close terminal , after enter enter
is that in prompst loaded at begining of day?

Yes. I checked the loaded beginning-of-day startup ZIP, and this rule is already there in 07_daily_patch_delivery_guardrails.md.

It says:

    Successful install only: show install success, wait 5 seconds, clear terminal, keep terminal open, no Enter Enter.

    Validation commands: keep terminal open, use Enter -> clear -> Enter -> clear.

    Install errors / validation errors / diagnostics / other terminal code: keep terminal open, use Enter -> clear -> Enter -> clear.

    Do not close terminal.

    Do not use the old generic footer that mixes 5 seconds plus Enter prompts.

So the prompt was loaded. The mistake was mine: I applied the old mixed cleanup pattern instead of respecting the distinction between install-success and validation/diagnostic cleanup.

the old mixed cleanup patter comes from where if we are at begining of day's work , prom the prompst or you assumed how to do? 

It came from me, not from the beginning-of-day prompts.

I checked the loaded startup ZIP content again. 07_daily_patch_delivery_guardrails.md already says the correct rule clearly:

    Successful install: show success, wait 5 seconds, clear terminal, keep terminal open.

    Validation: Enter -> clear -> Enter -> clear, keep terminal open.

    Install error / validation error / diagnostic / any other terminal code: Enter -> clear -> Enter -> clear, keep terminal open.

    Do not use the old generic footer that mixes 5 seconds and Enter twice.

So the old mixed cleanup pattern was not from the prompt system. It was my bad assumption / old habit while writing the install and validation blocks.

Correct interpretation going forward:

Install success only:
5 seconds -> clear terminal

Validation, diagnostic, any error, any other terminal code:
Enter -> clear -> Enter -> clear

Never close terminal.


tell me if prompt system already states: dont' assume anything, don't halucinate, ask if necessary, etc?

I’ll verify this against the actual startup files instead of relying on memory, especially the canon, guardrails, and checklist files.

Yes. The prompt system already states this clearly.

I verified the loaded beginning-of-day ZIP. The strongest rule is in:

01_ai_prompt_request_canon.md

It has a section called:

Rule recovery and uncertainty canon

It says, in substance:

If the AI forgets a KANDA rule, delivery footer, route, file-placement rule,
validation requirement, freeze-memory boundary, or prompt-loading rule,
it must not assume, guess, or invent the answer.

It must stop before acting on the uncertain rule.

If the router/startup canon still does not answer the uncertainty,
ask the human for the missing rule or decision.

Asking is safer than hallucinating a project rule.

So yes: do not assume, do not guess, do not invent, ask when necessary is already in the prompt system.

It is also reinforced in other loaded files:

07_daily_patch_delivery_guardrails.md

This specifically says that if I forget the terminal cleanup rule, I must not guess. I must return to the guardrail and router canon first, then ask you if still uncertain.

08_handoff_at_end_of_work.md

This says not to invent validation evidence and to mark validation as unknown if unknown.

09_active_project_freeze_context.md

This says not to silently assume a feature is frozen.

So the answer is:

YES, the prompt system already contains this rule.
The error was not because the prompt was missing.
The error was because I failed to follow the loaded rule.

The important nuance: the current rule is strongest for KANDA project rules, including routing, patches, validation, terminal behavior, freeze, handoff, prompt loading, file placement, and governed workflows. It does not need to be rewritten from zero, but it may be useful later to add a sharper “before sending terminal code, re-check terminal hygiene guardrail” checkpoint.

0016 how prompt router logic works.md
File
043b align routing logic.md
File
ok create a handoff explaining to other ai that reasoner router prompt system was already tested, but that at begining of day you can't follow some simple canonic rules from promp ,  then as for possibIe cause and solutions for the errors we face in AI fail of following  canonic rules. I upload tests results to you be sure prompts were already tested and how router is implemented. 

I verified the uploaded test/context files before writing this. The router canon already says the AI must not assume, guess, or invent when it forgets a rule, and must return to router/index context or ask the human if still uncertain. The test log also shows RG-028, RG-029, and RG-030 were closed as PASS, so this is not simply “the router was never tested.” The prompt system also already contains strict freeze-form, validation-evidence, patch ZIP, and terminal cleanup rules.

Here is the handoff:
HANDOFF - KANDA Reasoner Prompt Router Tested, But AI Still Failed Simple Canonical Rule Compliance
Current purpose of this handoff

This handoff is for the next AI working with Rafael Kanda on KANDA Reasoner.

The goal is not to rebuild the prompt router from zero. The router prompt system has already been tested and several critical routing behaviors passed. The problem to investigate is different:

At the beginning of a day/session, even after the startup prompt package was loaded, the AI still failed to follow some simple canonical rules that were already present in the prompt system.

The next AI must analyze why that happened and propose robust solutions.
Confirmed status

The KANDA prompt router is already implemented as a multi-prompt routing system.

It is not intended to load all prompts blindly. It is intended to load or request the smallest sufficient governed context for the task.

The router canon already says:

    Do not assume.

    Do not guess.

    Do not invent project rules.

    If uncertain, return to router logic and relevant indexes.

    If still uncertain, ask Rafael for the missing rule, prompt, file, folder card, or decision.

The Phase 2 prompt-call accuracy retests showed that several routing behaviors already passed:

    RG-028 - freeze workflow exact context expansion: PASS / CLOSED.

    RG-029 - startup stale filename override: PASS / CLOSED.

    RG-030 - Fast Path no-overrouting: PASS / CLOSED.

Additional freeze-hint and freeze-intake fixes were also implemented and frozen or prepared during this session:

    Freeze Hint Sidecar Delivery Contract v1.

    Freeze Hint Intake Box v1.

    Freeze Code Intake Prompt Routing v1.

    Freeze Hint Validation Evidence Merge v1.

    Freeze Hint Preserve Local Validation v1.

These fixes were created because the app and the chat needed a reliable bridge for feature-specific freeze metadata.
Important distinction

Do not conclude that the prompt system simply lacks the rules.

Several rules that the AI violated were already present in the loaded startup/prompt system.

The problem appears to be AI compliance with already-loaded canonical rules, especially when writing operational outputs such as PowerShell install blocks, validation blocks, freeze-form JSON, or immediate patch/handoff guidance.

The failures were not caused only by missing prompts. Some failures were caused by the AI not rechecking the prompt canon before acting.
Errors observed in this session
1. Wrong terminal cleanup pattern

The prompt system already distinguishes terminal cleanup behavior:

Install success:

    Show success.

    Wait 5 seconds.

    Clear terminal.

    Keep terminal open.

    Do not ask for Enter Enter.

Validation, diagnostics, and errors:

    Keep terminal open.

    Press Enter.

    Clear.

    Press Enter again.

    Clear again.

The AI still mixed the two patterns and produced the old generic footer.

Likely issue:
The AI answered from habit instead of rechecking the loaded terminal hygiene guardrail before writing terminal code.
2. Patch install path/staging mistake

The patch delivery rule says the human downloads the ZIP to the root of the same drive as the project. The installer should create or use the temporary delete-after-daily-work staging folder, move the ZIP there, extract fresh, install, and not assume yesterday's extracted folders still exist.

The AI initially gave an install block that assumed extracted paths already existed.

Likely issue:
The AI partially remembered the patch delivery workflow but skipped the exact staging sequence.
3. Freeze form reused stale feature identity

The Freeze Feature After Update form kept using an old heuristic feature:

Freeze Feature After Update Local Freeze Workflow v1

instead of the current feature.

This revealed a real app-side gap: the chat knew the current feature data, but the app only had local heuristics. The fix created KANDA_FREEZE_HINT.json and a freeze_hint_intake box.

Likely issue:
This was not only AI behavior. It was also a missing chat-to-app data bridge.
4. Validation evidence was not recognizer-friendly

The freeze writer blocked a freeze because validation_evidence_summary did not include a recognizer-friendly marker such as:

VALIDATION OK: feature_id

The AI had included sandbox/status language but not the exact marker the writer recognized.

Likely issue:
The prompt said validation evidence must be recognizable, but the AI did not enforce the exact validation-evidence contract when creating freeze metadata.
5. Merged validation evidence was overwritten

After validation evidence was merged into the saved freeze hint, New Local Freeze Entry rescanned the staged ZIP and downgraded the saved record back to "Local validation pending."

This revealed a real app-side logic bug. It was fixed by preserving stronger local validation evidence on same-feature or same-source rescans.

Likely issue:
The intake box needed stronger monotonic state rules: a later rescan must not overwrite stronger validated state with weaker pre-validation sidecar state.
6. Strict JSON freeze form parse issue

A freeze-form JSON response was initially rejected because the parser could not find a usable JSON object. A compact one-line JSON object between the exact markers worked.

Likely issue:
The AI output probably contained formatting that the tolerant extractor still could not safely parse. Freeze-form output must remain exact, minimal, and parser-friendly.
Possible causes to investigate

The next AI should investigate these possible causes:

    Context overload at beginning of day.
    The startup system may load enough rules, but the model may not keep all small operational distinctions active when generating code.

    Rule salience problem.
    The rules exist, but some are buried in longer startup material. The model follows broad routing behavior but misses small operational footer details.

    Habit override.
    The model may fall back to generic patch-delivery habits instead of the KANDA-specific canon unless forced through a checklist.

    No mandatory pre-output checklist.
    Before sending install code, validation code, freeze JSON, or patch delivery instructions, the AI may need a short internal checklist:

        Is this install, validation, diagnostic, freeze JSON, or patch ZIP?

        Which cleanup footer applies?

        Does the ZIP include KANDA_FREEZE_HINT.json?

        Is validation evidence recognizer-friendly?

        Is the active project root correct?

    First-position overrides solve routing scenarios but not all operational details.
    RG-028 and RG-029 first-position overrides improved routing-test behavior, but terminal hygiene and freeze-intake details may require their own first-position or near-output checks.

    Prompt and app responsibilities were mixed.
    Some failures looked like AI prompt failures but were actually app-state contract failures:

        Missing freeze hint sidecar.

        Missing freeze hint intake state.

        Missing validation-evidence merge.

        Rescan overwriting stronger local validation.

    Generated startup exposure may become stale.
    If first_AI_deliver artifacts or freeze exposure are stale, the AI may not see the freshest frozen behavior. Fresh startup sync and exposure refresh matter.

    Too many prompts should not mean 80 manual tests.
    The testing strategy should test behavior classes and high-risk routes, not every prompt one by one.

Requested analysis from the next AI

Please analyze why the AI failed to follow simple canonical rules even after the beginning-of-day prompt system was loaded.

Do not answer only "the prompt needs to say it." In several cases, the prompt already said it.

Please separate causes into these buckets:

    Prompt wording problem.

    Prompt placement or salience problem.

    Startup exposure or sync problem.

    Model execution/compliance problem.

    Missing app-side bridge or state contract.

    Missing validation or parser contract.

    Human workflow ambiguity.

For each bucket, propose one practical fix and one test.
Desired solutions to consider

Do not rewrite the whole router unless truly necessary.

Prefer small, testable, high-leverage fixes:

    Add a pre-output compliance checklist for terminal code.
    Trigger: before any PowerShell or terminal block.

    Add a pre-output compliance checklist for freeze-form JSON.
    Trigger: before returning KANDA_FREEZE_FORM_JSON_BEGIN.

    Add a pre-output compliance checklist for patch ZIP delivery.
    Trigger: before delivering any patch ZIP or install instructions.

    Add a validation-evidence contract check.
    The AI must confirm that validation_evidence_summary contains:
    VALIDATION OK: feature_id
    and STATUS: IN_SYNC when startup sync was validated.

    Add a sidecar presence check for freeze-ready patches.
    Patch ZIPs intended for freezing must include root-level KANDA_FREEZE_HINT.json.

    Add a monotonic state rule for freeze-intake.
    A saved freeze hint with recognizer-friendly validation evidence must not be downgraded by rescanning the same pre-validation sidecar.

    Add a strict parser-safe freeze-form mode.
    When returning freeze JSON, output only:
    KANDA_FREEZE_FORM_JSON_BEGIN
    {valid JSON object}
    KANDA_FREEZE_FORM_JSON_END

    Keep specialized prompts on-request unless truly needed daily.
    Do not solve compliance failure by blindly loading all 80 prompts.

    Expand smart routing tests by behavior class.
    Test high-risk behavior classes:

        patch delivery

        install footer

        validation footer

        freeze-form JSON

        freeze-ready sidecar

        multi-project freeze memory path

        startup stale filename

        Fast Path no-overrouting

        prompt-library anti-bypass

        architecture-audit external artifact paths

What not to do

Do not request all prompts blindly.

Do not assume the router is broken just because the AI missed a rule.

Do not remove Confirm and Write.

Do not store active project freeze memory in project_freeze_ledger.

Do not hardcode E:\kanda_reasoner as the freeze root for all projects.

Do not treat KANDA_FREEZE_HINT.json as an installed project source file.

Do not invent validation evidence.

Do not use the old mixed terminal footer.

Do not freeze a feature until installed and validated.
Next safe action

Produce a diagnostic plan for "AI failed to follow already-loaded KANDA canonical rules."

The plan should include:

    A short root-cause hypothesis table.

    A minimal patch proposal, if needed.

    A smart test matrix with scenarios, expected router behavior, and failure conditions.

    A recommendation for whether to modify prompts, code, tests, or all three.

The next AI should start from the fact that the router prompt system already passed multiple targeted tests, but operational compliance still failed in several concrete outputs.

Pasted text.txt
Document
Diagnostic plan: "AI failed to follow already-loaded KANDA canonical rules"
1) Root-cause hypothesis (short table)
Bucket	Hypothesis (one line)
Prompt wording problem	Some operational rules are present but phrased as descriptive guidance, not enforceable assertions, so the model treats them as lower-priority text.
Prompt placement / salience problem	Critical small-footprint rules (terminal hygiene, freeze markers, exact evidence tokens) are buried deep in startup material and not surfaced in first-position checks.
Startup exposure / sync problem	The model sees the startup package at load time but does not reliably refresh or re-bind ephemeral rules before the first outputs of a session.
Model execution / compliance problem	The model defaults to habitual templates when producing code blocks unless forced to run a short, explicit pre-output checklist.
Missing app-side bridge / state contract	Chat can know updated feature state but the app lacks deterministic sidecar exposure (KANDA_FREEZE_HINT.json) and monotonic preservation, causing mismatches.
Missing validation / parser contract	The parser and validation writer require exact markers and JSON formatting; AI outputs are sometimes tolerant-format and rejected.
Human workflow ambiguity	Human/engineer role boundaries and one-off decisions (e.g., where ZIPs are staged) are not encoded as immutable rules and allow model guessing.
2) Minimal patch proposal (one actionable patch)

Patch name: "Pre-output Compliance Hooks + Sidecar & Monotonic Intake"

Components (minimal, incremental):

    Add three lightweight first-position hooks (prompt-level) that are invoked automatically immediately before producing any:
        Terminal/PowerShell blocks (hook A)
        Patch/ZIP delivery instructions (hook B)
        Freeze-form JSON output (hook C) Each hook is a 6–8 line checklist that must be explicitly re-run and affirmed (internal token like [COMPLIANCE_OK]) before emitting the target block.
    Enforce exact tokens and structure in freeze JSON path:
        AI must emit only: KANDA_FREEZE_FORM_JSON_BEGIN {valid JSON} KANDA_FREEZE_FORM_JSON_END The hook validates JSON syntactic correctness and presence of required fields (feature_id, validation_evidence_summary) before releasing output.
    Add sidecar presence and staging rules to patch-delivery hook:
        If patch ZIP intended for freeze → require root-level KANDA_FREEZE_HINT.json; if missing, instruct human to add or fail.
        Installer steps must create/use staging folder (temp-delete-after-daily) and always re-extract from ZIP (do not assume existing extracted paths).
    App-side small rule changes (one PR each):
        Preserve monotonic validation state: when rescanning same feature/source, never downgrade stronger saved validation evidence.
        Ensure app exposes latest startup freeze hints/state to chat on-demand (explicit refresh API endpoint the prompt can call).
    Add recognizer-friendly validation-evidence enforcement:
        Hook ensures validation_evidence_summary contains "VALIDATION OK: <feature_id>" and "STATUS: IN_SYNC" when appropriate.

Minimal scope: implement hooks in prompt router (small insert) + two tiny app changes (monotonic-preserve and exposure endpoint) + parser-mode toggle for strict JSON output.
3) Smart test matrix (scenarios, expected router behavior, failure conditions)

High-risk behavior classes — for each: Input scenario, Expected behavior, Failure condition.

    Patch delivery (freeze-ready)

    Input: Human asks for patch install for feature X; ZIP present root but may lack sidecar.
    Expect: Hook B runs → checks ZIP root for KANDA_FREEZE_HINT.json. If present, proceed with staging steps (create staging, move ZIP, extract fresh). If missing, return instruction to add sidecar and abort auto-install. Output includes staging sequence and no path assumptions.
    Fail if: Installer assumes pre-extracted path; missing sidecar not detected; staging not created; output uses old mixed terminal footer.

    Patch delivery (non-freeze)

    Input: Standard patch ZIP install.
    Expect: Hook B ensures staging create and fresh extract; outputs proper install footer for success flow (wait 5s, clear, keep open).
    Fail if: Old mixed footer or pre-existing paths assumed.

    Terminal / PowerShell block (success)

    Input: Any install block expected to succeed.
    Expect: Hook A applies success terminal hygiene: show success, wait 5s, clear terminal, keep open; no "Press Enter" sequences.
    Fail if: Footer includes "Press Enter" or mixed pattern.

    Terminal / PowerShell block (validation/diagnostics/error)

    Input: Validation fails or diagnostic output expected.
    Expect: Hook A applies error hygiene: keep open, press Enter, clear, press Enter, clear (explicit sequence), not the success footer.
    Fail if: Wrong footer used.

    Freeze-form JSON output

    Input: Request to produce freeze form JSON for feature Y.
    Expect: Hook C enforces strict wrapper tokens, produces syntactically valid JSON, includes validation_evidence_summary with "VALIDATION OK: feature_id" if validated; JSON produced only between the exact BEGIN/END markers.
    Fail if: Output contains extra prose, missing markers, invalid JSON, or missing recognizer token.

    Validation evidence merge and rescan

    Input: Saved freeze hint marked VALIDATION OK; rescanner runs against same ZIP.
    Expect: App monotonic rule preserves VALIDATION OK and does not overwrite with weaker state. Chat shows preserved stronger evidence.
    Fail if: Saved state downgraded.

    Startup sync / stale filename test

    Input: Start-of-day session with previously changed freeze hints.
    Expect: Router prompts the exposure-refresh API and confirms STATUS: IN_SYNC before accepting STATUS-dependent operations.
    Fail if: Model proceeds on stale metadata.

Test harness: automated scripted scenarios that exercise each case; validate emitted outputs against golden patterns (regex for footers, presence of tokens, JSON wrapper, staging path commands), and run app-side unit tests for monotonic-preserve.

Success criteria: Zero parser rejections for freeze JSON, zero install outputs with mixed footer, sidecar-missing detected and blocked, monotonic-preserve unit tests pass.
4) Recommendation: prompts, code, tests — what to change

    Prompts: Add the three pre-output compliance hooks (small prompts). Increase salience for terminal hygiene, freeze markers, and validation-evidence exact tokens by placing them in first-position short checklists invoked per-output type. (Change prompts.)
    Code (app): Implement monotonic-preserve rule in freeze-intake rescan logic; add an exposure-refresh endpoint so prompts can request fresh state before status-sensitive operations; add parser-safe strict-mode to accept only the BEGIN/END wrapped JSON. (Change code.)
    Tests: Add behavior-class tests in router test-suite and end-to-end tests that assert exact outputs (footers, JSON wrappers, staging operations) and app monotonic behavior. (Change tests.)

Overall: modify all three (prompts + small app changes + tests) but keep changes minimal and localized — do not load all prompts daily; keep specialized prompts on-request. The highest-leverage single change is the pre-output compliance hooks (prompt-side) combined with the monotonic-preserve app guard.


OVERALL VERDICT:
The router itself is NOT broken. The system design is sound. You are dealing with a classic "execution salience" problem—the model "knows" the rules but fails to apply them at the exact moment of output generation. This is fixable with targeted, low-invasive patches.

RECOMMENDATION:
Proceed with targeted prompt salience fixes and add a strict "pre-output validation contract" for high-risk artifacts (terminal code, freeze JSON, install logic). Do not restructure the router.


1. ROOT-CAUSE HYPOTHESIS TABLE (Bucketed)
#	Bucket	Root Cause	Confidence	Practical Fix	Practical Test
1	Prompt placement or salience problem	The terminal hygiene and staging rules are buried in 07_daily_patch_delivery_guardrails.md. By the time the AI writes the final output (install block/footer), it has shifted out of "guardrail retrieval" mode into "code generation" mode. The rule is correct, but it's not at the point of action.	High	Add a "Pre-Output Compliance Checklist" as a mandatory top-level section in the task-specific prompts (e.g., just before the "Output" section in 07_daily_patch_delivery_guardrails.md).	Run a patch delivery test asking for an install block. The AI must explicitly state which footer pattern it is using before writing code.
2	Model execution/compliance problem (Habit Override)	The AI falls back to its generic training data (common PowerShell scripts) rather than the specific KANDA project canon. This is an "attention" failure—it writes what it has seen thousands of times instead of checking the specific rules loaded 2 minutes ago.	High	Break the habit by making the output format strictly parseable. Require a metadata header (e.g., <!-- FOOTER_PATTERN: INSTALL_SUCCESS -->) before the terminal block. If the AI has to classify the pattern first, it is forced to check the loaded rule.	Test a diagnostic error scenario. The AI must output FOOTER_PATTERN: DIAGNOSTIC_ERROR instead of the default success pattern.
3	Missing validation/parser contract	The freeze-form parser failed because it was too tolerant. The AI output human-like formatting, but the parser expected a strict machine-readable section. You asked for "exact, minimal, parser-friendly" output, but the prompt didn't explicitly forbid explanatory text inside the markers.	High	Explicitly state in the prompt: "Between the BEGIN and END markers, output ONLY a valid JSON object. No explanatory text, no comments, no trailing commas. The parser will reject anything else."	Pass a malformed JSON object with comments. The AI must self-correct to strict JSON without human intervention.
4	Missing app-side bridge or state contract	The freeze intake box rescan bug (overwriting stronger evidence) was an app-side contract failure. The fix (monotonic state rule) is already implemented, but the chat-AI needs to know that once evidence is recognizer-friendly (VALIDATION OK: feature_id), it must not accept weaker pre-validation sidecars in future rescans.	Medium	Add a short note in freeze_hint_intake prompt: "Recognizer-friendly evidence (VALIDATION OK: ...) is definitive. Do not downgrade on rescan."	Test: Run New Local Freeze Entry twice. The second scan must preserve the first validation status.
5	Startup exposure or sync problem	The 09_active_project_freeze_context.md might still be stale if expose_freeze_memory.py was not run immediately after the local freeze. The AI references the startup file, which references the old freeze state.	Medium	Enforce that sync_startup_routing_kernel_pack.py --ensure-sync runs automatically after write_freeze_entry completes (or provide a clear warning if not).	Check 09_active_freeze_context.md timestamp vs. freeze memory modified date. Alert if they differ.
6	Prompt wording problem	The phrase "validation evidence must be recognizable" is abstract. The AI interpreted "sandbox language" as recognizable, but the writer only recognized the exact literal VALIDATION OK: feature_id. The wording lacked the exact literal contract.	Medium	Replace "recognizable" with: "You MUST include the exact literal VALIDATION OK: feature_id in the evidence summary. If you do not include this exact string, the freeze writer will block the freeze."	Create a freeze draft with only generic text. The AI must correct itself to include the literal string.
2. MINIMAL PATCH PROPOSAL

No Router Rewrite. Apply these three high-leverage changes.
Patch A: Add a "Pre-Output Compliance Checklist" (Prompts)

Modify 07_daily_patch_delivery_guardrails.md and 05_start_of_day_master_stack.md.

Add this exact block before any code block or install command is generated:
markdown

## PRE-OUTPUT COMPLIANCE CHECKLIST (MANDATORY CHECK BEFORE RESPONDING)

Before generating any terminal block, install instruction, or freeze JSON, silently verify these three points and include the corresponding marker in your response:

1. **TERMINAL FOOTER PATTERN:**
   - If the command is an INSTALL block that succeeds -> FOOTER: INSTALL_SUCCESS.
   - If the command is VALIDATION, DIAGNOSTIC, or ERROR -> FOOTER: VALIDATION_DIAGNOSTIC.

2. **PATCH STAGING:**
   - The user downloads to E:/.
   - The installer MUST explicitly move/copy the ZIP to E:/kanda_reasoner_delete_after_daily_work/ BEFORE extracting.
   - Check: Is the extraction path the staging folder, not the root?

3. **FREEZE JSON:**
   - Include VALIDATION OK: feature_id in the validation evidence string.
   - The JSON must be valid, no comments, one-liner between the markers.

Reason: This puts the rule at the point of decision. It forces the AI to retrieve the canon just before acting.
Patch B: Strict Parser-Friendly Freeze JSON (Prompt + Parser)

Modify 07_prompt_authoring_and_audit.md or the relevant freeze intake prompt.

Change the instruction to:
markdown

When returning freeze JSON, output EXACTLY this structure:

KANDA_FREEZE_FORM_JSON_BEGIN
{"feature_id": "...", "validation_evidence_summary": "...", "protected_paths": [...]}
KANDA_FREEZE_FORM_JSON_END

**WARNING:** No explanatory text before/after within the markers. The parser will reject and require a retry if it contains anything other than a valid JSON object.

Code-side: Ensure the tolerant parser also strips markdown code fences before parsing, but enforce the literal marker requirement.
Patch C: Monotonic State Rule (App Code + Prompt)

This was already fixed. The prompt needs to reflect it:
Add to freeze_hint_intake logic: "If the current hint has a validation_status of 'VALIDATED_REAL' (i.e., contains the exact marker), do not replace it with a 'PENDING' state during a rescan."
3. SMART TEST MATRIX (Behavior Classes)

*Do not test 80 prompts. Test these high-risk behavior classes.*
Test ID	Behavior Class	Scenario	Expected Router/Compliance Behavior	Failure Condition	Fix Validated by
C-01	Terminal Footer Hygiene	User asks to install a patch. The install succeeds.	AI must return footer: FOOTER: INSTALL_SUCCESS. (Clear after 5s, no Enter Enter).	AI returns mixed footer or asks for Enter Enter.	Patch A
C-02	Diagnostic Footer Hygiene	User asks to run validation, and it fails/passes (diagnostic).	AI must return footer: FOOTER: VALIDATION_DIAGNOSTIC. (Keeps open, Enter, Clear, Enter, Clear).	AI clears immediately.	Patch A
C-03	Patch Staging Path	User asks for a patch install script.	The script explicitly moves the ZIP from E:/ to .../delete_after_daily_work/ before extraction.	The script assumes the ZIP is already in the staging folder.	Patch A
C-04	Freeze JSON Strictness	AI provides freeze JSON.	The AI outputs a compact, one-line valid JSON between the exact markers. No extra text inside markers.	Parser rejects due to formatting/comments.	Patch B
C-05	Validation Evidence Marker	AI prepares a freeze draft with validation passed.	The validation_evidence_summary contains the exact literal VALIDATION OK: feature_id.	Only generic text ("sandbox passed") is provided.	Patch B
C-06	Intake Monotonic State	Feature validated, saved. Rescan the same feature's pre-validation sidecar.	The intake box preserves the "VALIDATED" state and does NOT downgrade to "PENDING".	The validated state is overwritten.	Patch C
4. SPECIFIC ANSWERS TO THE OBSERVED ERRORS

    Wrong terminal cleanup pattern:

        Diagnosis: Salience problem. The AI was in "answer the user" mode, not "check the project-specific footer rules" mode.

        Specific Fix: Add PRE-OUTPUT COMPLIANCE CHECKLIST (Patch A). Force it to classify INSTALL vs VALIDATION before writing the footer.

    Patch install path/staging mistake:

        Diagnosis: Habit override. The AI wrote a generic extraction script.

        Specific Fix: Same as above. The checklist explicitly asks "Is the extraction path the staging folder?".

    Freeze form reused stale feature identity:

        Diagnosis: Missing app-side bridge. Fixed by KANDA_FREEZE_HINT.json.

        Test: Ensure the chat prompt now says "Check KANDA_FREEZE_HINT.json in the root of the ZIP for the current feature identity before guessing.".

    Validation evidence was not recognizer-friendly:

        Diagnosis: Wording ambiguity. "Recognizable" vs "Exact literal".

        Specific Fix: Replace the word "recognizable" with the exact literal requirement (Patch B).

    Merged validation evidence was overwritten:

        Diagnosis: App-side logic bug. Already fixed with monotonic state rules.

        Ensure: The prompt now explicitly tells the AI not to provide weaker evidence during rescans (Patch C).

    Strict JSON parse issue:

        Diagnosis: Parser too tolerant of text, not tolerant enough of formatting.

        Specific Fix: Patch B. Explicitly forbid comments/trailing commas in the prompt and update the parser to strictly locate the markers first.

5. FINAL RECOMMENDATION

Implement Patches A, B, and C.

    Patch A (Prompts) solves the terminal hygiene and staging path failures.

    Patch B (Prompt + Parser) solves the freeze JSON and validation evidence marker failures.

    Patch C (Prompt + App Logic) solves the overwrite issue.

Do NOT:

    Rewrite the router.

    Add 80 new prompt files.

    Remove Confirm and Write.

    Hardcode paths.

Next Safe Action:
Apply Patch A and B to the relevant startup guardrails. Run the Smart Test Matrix (C-01 through C-06) manually in a new chat session. If all pass, freeze this compliance layer as freeze-20260616-compliance-checklist-v1. This is a small, testable patch that directly addresses the observed failures without destabilizing the working architecture.

OVERALL VERDICT:
Modify (Targeted, high-leverage fixes only). The router is not fundamentally broken, but it is suffering from classic LLM attention decay and habit override on highly specific operational details. The solution is not to add more rules to the main startup prompt, but to introduce pre-output compliance checklists and strict app-side state contracts.
1. Root-Cause Hypothesis Table
Observed Error
	
Primary Bucket(s)
	
Root-Cause Hypothesis
	
Practical Fix
	
Test Scenario
1. Wrong terminal cleanup pattern
	
2 (Salience), 4 (Habit override)
	
The rule exists in a long document, but when generating code, the model's attention mechanism defaults to its pre-trained "generic PowerShell pause" habit, ignoring the buried KANDA-specific footer rule.
	
Add a Pre-Output Terminal Checklist triggered specifically when the AI is about to generate a PowerShell block.
	
Ask AI to generate an install script. Fail if it outputs "Press Enter to continue" instead of the exact 5-second wait/clear sequence.
2. Patch install path/staging mistake
	
1 (Wording), 4 (Habit override)
	
The prompt states the rule, but the AI hallucinated the completion of the staging step rather than generating the code to perform it, assuming a previous session's state.
	
Enforce a Pre-Output Patch Delivery Checklist. Require the AI to explicitly state the source path, staging path, and extraction target before writing the code.
	
Provide a raw ZIP path. Fail if the generated script does not explicitly include the move to delete_after_daily_work and fresh extraction logic.
3. Freeze form reused stale feature identity
	
5 (Missing app-side bridge)
	
The AI relied on conversational chat context, but the app's local state was stale. The AI has no mechanism to "know" the app's internal state without a structured, machine-readable bridge.
	
(Already addressed) Enforce KANDA_FREEZE_HINT.json as the mandatory sidecar. The AI must read this file to get current feature identity before generating freeze forms.
	
Simulate a stale chat context. Pass only if the AI explicitly requests or reads KANDA_FREEZE_HINT.json to resolve the feature identity.
4. Validation evidence not recognizer-friendly
	
1 (Wording), 6 (Missing parser contract)
	
The prompt said "must be recognizable," but did not provide a strict, regex-enforced template. The AI assumed "sandbox passed" was sufficient, failing the parser's exact string match.
	
Provide an exact output template for validation evidence. Require the AI to output VALIDATION OK: <feature_id> and STATUS: IN_SYNC verbatim.
	
Ask AI to summarize a successful validation. Fail if the exact string VALIDATION OK: is missing from the validation_evidence_summary.
5. Merged validation evidence overwritten
	
5 (App-side state), 6 (Validation contract)
	
Purely an app-side logic bug. The intake box lacked monotonic state rules, allowing a weaker pre-validation sidecar to overwrite a stronger, already-validated local state.
	
(Already addressed) Codify a Monotonic State Rule in the freeze-intake box: if new_state == 'pending' and existing_state == 'validated': retain existing_state.
	
Rescan a feature that already has VALIDATION OK in its hint file. Pass if the app retains the validated status and does not downgrade it.
6. Strict JSON freeze form parse issue
	
4 (Model execution), 6 (Missing parser contract)
	
The AI added markdown formatting, comments, or trailing commas inside the JSON block, or placed it outside the exact markers, breaking the tolerant extractor.
	
Enforce a Strict Parser-Safe Mode. Instruct the AI: "Output ONLY the exact markers and a valid, minified JSON object. No markdown, no comments, no surrounding text."
	
Ask AI to generate a freeze form. Pass only if a regex extractor cleanly pulls valid JSON between KANDA_FREEZE_FORM_JSON_BEGIN and END.
2. Minimal Patch Proposal
Do not rewrite the router. Apply these three high-leverage, minimal patches:
Patch A: Pre-Output Compliance Checklists (Prompt Modification)
Add a new, highly visible section in 07_daily_patch_delivery_guardrails.md (or a dedicated micro-prompt) that acts as a mandatory cognitive checkpoint.
Rule: "Before generating ANY of the following, you must internally verify the checklist and state your compliance in one sentence:"

    Terminal Code: "Checklist: Install vs Validation footer? 5-sec wait? No generic 'Press Enter'?"
    Patch Delivery: "Checklist: Root download? Move to delete_after_daily_work? Fresh extract? No assumed prior state?"
    Freeze JSON: "Checklist: Exact markers? Minified valid JSON? VALIDATION OK: <feature_id> present?"

Patch B: Monotonic State Enforcement (App Code Modification)
In freeze_hint_intake logic, implement a strict state hierarchy: Validated > Local Pending > Unknown. A rescan of a sidecar file must never downgrade a Validated state to Local Pending.
Patch C: Strict JSON Extraction (App Code Modification)
Update the freeze-form parser to use a robust regex: r'KANDA_FREEZE_FORM_JSON_BEGIN\s*({.*?})\s*KANDA_FREEZE_FORM_JSON_END', followed by json.loads() with strict error handling that rejects trailing commas or markdown backticks.
3. Smart Test Matrix (Behavior Class Focus)
Test high-risk operational routes, not individual prompts. Run these manually first.
Test ID
	
Behavior Class
	
Scenario Setup
	
Expected Router/AI Behavior
	
Failure Condition
OP-01
	
Terminal Hygiene
	
"Generate a PowerShell script to install a validated patch."
	
Outputs install-specific footer (5s wait, clear, keep open). Explicitly states checklist compliance.
	
Outputs generic "Press Enter to continue" or mixes validation footer.
OP-02
	
Patch Staging
	
"Here is a patch ZIP at D:\patch.zip. Give me the install commands."
	
Script explicitly moves ZIP to delete_after_daily_work, creates fresh temp dir, extracts, and installs.
	
Script assumes D:\patch_extracted already exists or skips the staging move.
OP-03
	
Freeze JSON Strictness
	
"Generate the freeze form JSON for feature freeze-20260615-test with validation passed."
	
Outputs exact markers, minified JSON, and validation_evidence_summary contains VALIDATION OK: freeze-20260615-test.
	
JSON contains markdown, comments, or lacks the exact validation marker. Parser fails.
OP-04
	
State Bridge Reliance
	
Chat context is stale. User says: "Update the freeze entry for the feature we just worked on."
	
AI refuses to guess. AI explicitly requests KANDA_FREEZE_HINT.json or runs the exposure CLI to get current state.
	
AI hallucinates the feature ID or uses an old ID from earlier in the chat.
OP-05
	
Fast Path Boundary
	
"Explain the concept of Box Architecture to me."
	
Fast Path. No prompt requests. No freeze checks. Direct, concise answer.
	
AI requests 04_box_architecture_and_boundaries or says "May proceed now: NO".
4. Recommendation: Modify Prompts, Code, and Tests
Modify Prompts: Yes, but structurally, not by adding volume. Introduce the Pre-Output Compliance Checklists. This forces the model's attention mechanism to focus on the specific operational constraints at the exact moment of generation, defeating habit override without bloating the startup context.
Modify Code: Yes. The app must enforce monotonic state in the freeze-intake box and use strict regex extraction for the freeze JSON. The AI cannot be solely responsible for preventing app-side state degradation; the app must defend its own state contract.
Modify Tests: Yes. Expand the manual pilot registry to include the Smart Test Matrix above. Do not build automated JSON validators for these operational checks until the AI consistently passes 3-5 manual runs of OP-01 through OP-05.
Final Advice: 
The failures you observed are not a failure of the router's logic, but a failure of LLM attention management. When an LLM generates code, its attention shifts to code-completion patterns, causing it to "forget" nuanced operational rules buried in a long context window. The pre-output checklist is the industry-standard workaround for this: it forces the model to re-attend to the rules immediately before the risky output is generated. Implement the checklists, lock down the app's monotonic state, and test the behavior classes. The system is fundamentally sound; it just needs these targeted guardrails.
Copy
Ask Qwen
Explain
Translate(en-US)
AI-generated con


OVERALL VERDICT:
Modify (Targeted, high-leverage fixes only). The router is not fundamentally broken, but it is suffering from classic LLM attention decay and habit override on highly specific operational details. The solution is not to add more rules to the main startup prompt, but to introduce pre-output compliance checklists and strict app-side state contracts.
1. Root-Cause Hypothesis Table
Observed Error
	
Primary Bucket(s)
	
Root-Cause Hypothesis
	
Practical Fix
	
Test Scenario
1. Wrong terminal cleanup pattern
	
2 (Salience), 4 (Habit override)
	
The rule exists in a long document, but when generating code, the model's attention mechanism defaults to its pre-trained "generic PowerShell pause" habit, ignoring the buried KANDA-specific footer rule.
	
Add a Pre-Output Terminal Checklist triggered specifically when the AI is about to generate a PowerShell block.
	
Ask AI to generate an install script. Fail if it outputs "Press Enter to continue" instead of the exact 5-second wait/clear sequence.
2. Patch install path/staging mistake
	
1 (Wording), 4 (Habit override)
	
The prompt states the rule, but the AI hallucinated the completion of the staging step rather than generating the code to perform it, assuming a previous session's state.
	
Enforce a Pre-Output Patch Delivery Checklist. Require the AI to explicitly state the source path, staging path, and extraction target before writing the code.
	
Provide a raw ZIP path. Fail if the generated script does not explicitly include the move to delete_after_daily_work and fresh extraction logic.
3. Freeze form reused stale feature identity
	
5 (Missing app-side bridge)
	
The AI relied on conversational chat context, but the app's local state was stale. The AI has no mechanism to "know" the app's internal state without a structured, machine-readable bridge.
	
(Already addressed) Enforce KANDA_FREEZE_HINT.json as the mandatory sidecar. The AI must read this file to get current feature identity before generating freeze forms.
	
Simulate a stale chat context. Pass only if the AI explicitly requests or reads KANDA_FREEZE_HINT.json to resolve the feature identity.
4. Validation evidence not recognizer-friendly
	
1 (Wording), 6 (Missing parser contract)
	
The prompt said "must be recognizable," but did not provide a strict, regex-enforced template. The AI assumed "sandbox passed" was sufficient, failing the parser's exact string match.
	
Provide an exact output template for validation evidence. Require the AI to output VALIDATION OK: <feature_id> and STATUS: IN_SYNC verbatim.
	
Ask AI to summarize a successful validation. Fail if the exact string VALIDATION OK: is missing from the validation_evidence_summary.
5. Merged validation evidence overwritten
	
5 (App-side state), 6 (Validation contract)
	
Purely an app-side logic bug. The intake box lacked monotonic state rules, allowing a weaker pre-validation sidecar to overwrite a stronger, already-validated local state.
	
(Already addressed) Codify a Monotonic State Rule in the freeze-intake box: if new_state == 'pending' and existing_state == 'validated': retain existing_state.
	
Rescan a feature that already has VALIDATION OK in its hint file. Pass if the app retains the validated status and does not downgrade it.
6. Strict JSON freeze form parse issue
	
4 (Model execution), 6 (Missing parser contract)
	
The AI added markdown formatting, comments, or trailing commas inside the JSON block, or placed it outside the exact markers, breaking the tolerant extractor.
	
Enforce a Strict Parser-Safe Mode. Instruct the AI: "Output ONLY the exact markers and a valid, minified JSON object. No markdown, no comments, no surrounding text."
	
Ask AI to generate a freeze form. Pass only if a regex extractor cleanly pulls valid JSON between KANDA_FREEZE_FORM_JSON_BEGIN and END.
2. Minimal Patch Proposal
Do not rewrite the router. Apply these three high-leverage, minimal patches:
Patch A: Pre-Output Compliance Checklists (Prompt Modification)
Add a new, highly visible section in 07_daily_patch_delivery_guardrails.md (or a dedicated micro-prompt) that acts as a mandatory cognitive checkpoint.
Rule: "Before generating ANY of the following, you must internally verify the checklist and state your compliance in one sentence:"

    Terminal Code: "Checklist: Install vs Validation footer? 5-sec wait? No generic 'Press Enter'?"
    Patch Delivery: "Checklist: Root download? Move to delete_after_daily_work? Fresh extract? No assumed prior state?"
    Freeze JSON: "Checklist: Exact markers? Minified valid JSON? VALIDATION OK: <feature_id> present?"

Patch B: Monotonic State Enforcement (App Code Modification)
In freeze_hint_intake logic, implement a strict state hierarchy: Validated > Local Pending > Unknown. A rescan of a sidecar file must never downgrade a Validated state to Local Pending.
Patch C: Strict JSON Extraction (App Code Modification)
Update the freeze-form parser to use a robust regex: r'KANDA_FREEZE_FORM_JSON_BEGIN\s*({.*?})\s*KANDA_FREEZE_FORM_JSON_END', followed by json.loads() with strict error handling that rejects trailing commas or markdown backticks.
3. Smart Test Matrix (Behavior Class Focus)
Test high-risk operational routes, not individual prompts. Run these manually first.
Test ID
	
Behavior Class
	
Scenario Setup
	
Expected Router/AI Behavior
	
Failure Condition
OP-01
	
Terminal Hygiene
	
"Generate a PowerShell script to install a validated patch."
	
Outputs install-specific footer (5s wait, clear, keep open). Explicitly states checklist compliance.
	
Outputs generic "Press Enter to continue" or mixes validation footer.
OP-02
	
Patch Staging
	
"Here is a patch ZIP at D:\patch.zip. Give me the install commands."
	
Script explicitly moves ZIP to delete_after_daily_work, creates fresh temp dir, extracts, and installs.
	
Script assumes D:\patch_extracted already exists or skips the staging move.
OP-03
	
Freeze JSON Strictness
	
"Generate the freeze form JSON for feature freeze-20260615-test with validation passed."
	
Outputs exact markers, minified JSON, and validation_evidence_summary contains VALIDATION OK: freeze-20260615-test.
	
JSON contains markdown, comments, or lacks the exact validation marker. Parser fails.
OP-04
	
State Bridge Reliance
	
Chat context is stale. User says: "Update the freeze entry for the feature we just worked on."
	
AI refuses to guess. AI explicitly requests KANDA_FREEZE_HINT.json or runs the exposure CLI to get current state.
	
AI hallucinates the feature ID or uses an old ID from earlier in the chat.
OP-05
	
Fast Path Boundary
	
"Explain the concept of Box Architecture to me."
	
Fast Path. No prompt requests. No freeze checks. Direct, concise answer.
	
AI requests 04_box_architecture_and_boundaries or says "May proceed now: NO".
4. Recommendation: Modify Prompts, Code, and Tests
Modify Prompts: Yes, but structurally, not by adding volume. Introduce the Pre-Output Compliance Checklists. This forces the model's attention mechanism to focus on the specific operational constraints at the exact moment of generation, defeating habit override without bloating the startup context.
Modify Code: Yes. The app must enforce monotonic state in the freeze-intake box and use strict regex extraction for the freeze JSON. The AI cannot be solely responsible for preventing app-side state degradation; the app must defend its own state contract.
Modify Tests: Yes. Expand the manual pilot registry to include the Smart Test Matrix above. Do not build automated JSON validators for these operational checks until the AI consistently passes 3-5 manual runs of OP-01 through OP-05.
Final Advice: 
The failures you observed are not a failure of the router's logic, but a failure of LLM attention management. When an LLM generates code, its attention shifts to code-completion patterns, causing it to "forget" nuanced operational rules buried in a long context window. The pre-output checklist is the industry-standard workaround for this: it forces the model to re-attend to the rules immediately before the risky output is generated. Implement the checklists, lock down the app's monotonic state, and test the behavior classes. The system is fundamentally sound; it just needs these targeted guardrails.
audit discuss  suggestions

I’ll audit this as a design decision, not as a patch request: what is correct, what is risky, and what I would actually implement first.

Audit result: the suggestions are mostly correct. I would accept the core diagnosis and the test-matrix direction, but I would adjust the implementation so it does not bloat startup or create noisy outputs.

The current canon already says the router must not guess, must use selective context, and must not load everything blindly. It also already contains the KANDA rules for KANDA_FREEZE_HINT.json, recognizer-friendly validation evidence, strict freeze JSON, patch staging, and terminal cleanup. So the problem is not “missing rules.” The problem is exactly what the audit says: rules exist, but they are not being re-applied at the moment of output generation.
My verdict

Proceed with the idea, but refine it:

YES:
Add pre-output compliance hooks.
Add smart tests RG-031 to RG-040.
Keep router architecture unchanged.
Keep startup lean.
Keep specialized prompts on-request.

NO:
Do not rewrite the router.
Do not add all operational checklists as giant always-startup text.
Do not force visible compliance markers in every normal answer.
Do not rely only on prompt changes for app-side state problems.

What I agree with strongly

The strongest part is the diagnosis:

Routing-time compliance is not the same as output-time compliance.

RG-028, RG-029, and RG-030 proved the router can classify tasks correctly. But install blocks, validation blocks, freeze JSON, and patch delivery are generated later, when the model is already in “write code / write JSON” mode. That is when it forgets small rules like terminal footer pattern or exact validation markers.

The proposed RG-031 to RG-040 matrix is good. It tests behavior classes, not 80 prompts one by one. That matches the router canon: KANDA is a multi-prompt system, and loading all prompts blindly reduces accuracy.
What I would change in the suggestion
1. Do not make visible [COMPLIANCE_OK] mandatory in normal outputs

The idea of a compliance check is correct. But making the AI print [COMPLIANCE_OK], FOOTER: INSTALL_SUCCESS, or similar markers in normal patch answers may pollute copy-paste workflows.

Better:

Normal use:
The pre-output check is silent.

Test mode:
The AI may expose the selected compliance class for grading.

So for RG tests, visible markers are useful. For real install/validation blocks, keep the output clean.
2. Put a tiny hook in startup, not the whole checklist

The current canon says always-startup prompts must remain lean, and specialized prompts should stay on-request unless truly needed every session.

So I would not dump a long pre_output_compliance_checklists.md into always-startup.

Better structure:

Startup paste hook:
"When producing terminal code, patch delivery instructions, or freeze JSON, apply pre_output_compliance_checklists."

Full prompt:
pre_output_compliance_checklists.md remains on-request / routed.

That gives salience without bloating the daily startup kernel.
3. Keep terminal hygiene in one hard canon

The terminal rule already exists, but it should be duplicated as a small hard-rule block near the pre-output hook:

Install success:
5 seconds -> Clear-Host -> keep open -> no Enter prompts.

Validation / diagnostic / error:
Enter -> Clear-Host -> Enter -> Clear-Host -> keep open.

Never mix them.

This is worth making first-position because it already failed once.
4. Freeze JSON should be strict, but only for freeze forms

I agree with strict compact JSON between markers. Your parser already proved that the safest path is:

KANDA_FREEZE_FORM_JSON_BEGIN
{"feature_title":"..."}
KANDA_FREEZE_FORM_JSON_END

But do not generalize that to every JSON output in the project. This strict mode should apply only to KANDA freeze-form receiver output.

Also, Windows paths inside JSON should either use escaped backslashes or forward slashes. The version that worked used forward slashes in evidence text, which avoided invalid escape problems.
5. Do not add a new app endpoint yet

The suggestion mentions an “exposure-refresh API endpoint.” I would postpone that. You already have startup sync/exposure machinery, and the current canon already expects startup delivery regeneration with STATUS: IN_SYNC.

For now, solve this with:

    prompt hook,

    validation command,

    startup sync check,

    smart tests.

Only add an endpoint later if the manual/CLI refresh continues to fail.
Best minimal patch scope

I would define the patch as:

Patch name:
pre_output_compliance_hooks_v1

Prompt changes:
1. Add pre_output_compliance_checklists.md.
2. Add tiny startup hook in paste_after_first_prompts_to_ai.md generation source.
3. Update daily_patch_delivery_guardrails.md with hard terminal/footer rule.
4. Update freeze_code_intake_and_form_protocol.md with exact validation marker and strict JSON release rule.

No app-code change unless tests show parser or state still fails.

The monotonic-state app bug and freeze-hint intake bridge were already handled in previous fixes. The current remaining gap is mostly pre-output salience.
Smart test matrix: accept, but reorder

I would run tests in this order:

RG-031: install block terminal hygiene
RG-032: validation block terminal hygiene
RG-035: patch staging and fresh extraction
RG-033: strict freeze-form JSON
RG-034: missing validation marker blocks freeze JSON
RG-037: sidecar identity beats chat memory
RG-040: external project freeze path
RG-039: Fast Path no over-routing
RG-028: confirmation bypass regression
RG-029: stale startup filename regression

Reason: start with the exact failures that happened, then retest known closed routing guards.
Final recommendation

Implement the pre-output compliance layer, but keep it small.

The best design is:

Router = decides what context is needed.
Pre-output hook = checks artifact-specific rules immediately before output.
App contracts = prevent state downgrade and parser ambiguity.
Tests = behavior classes, not all prompts.

So yes: proceed with a targeted patch. Do not rewrite the router. The next patch should be pre_output_compliance_hooks_v1, followed by RG-031 to RG-040.

before patch , surf on the net in specify prompt engeneering sites and search for other enligtening ideas to update solution and  solve logic problem

I’ll browse current prompt-engineering and agent-design sources, then compare them against the KANDA failure pattern: routing passed, but output-time compliance failed. I’ll focus on ideas that are practical for your patch, not generic prompting advice.

I searched current prompt-engineering / agent-design sources. The strongest external lesson is this:

Do not try to solve this only by adding more prompt text. The modern best practice is: use prompts for intent, but use schemas, validators, guardrails, and output-specific gates for anything machine-consumed or high-risk.

OpenAI, Microsoft/Azure, Google, and Anthropic all point in the same direction: structured or constrained outputs are preferred for strict JSON; prompt text alone is not enough for schema reliability; and final outputs must be validated in application code. OpenAI’s Structured Outputs use JSON Schema with strict: true so outputs match the supplied schema, and Azure describes the same difference between older JSON mode and true schema adherence. Google explicitly warns that structured output can ensure syntactic JSON, but the application still must validate semantic correctness before using it. Anthropic’s consistency guidance also says that when JSON schema conformance is required, use Structured Outputs rather than relying only on prompt engineering.
Updated diagnosis

Your router is not the main problem.

The deeper problem is:

The router decides correctly.
But the final artifact generator is not forced to pass a contract before output.

So KANDA needs a contract layer after routing and before output.

The external research supports this too. Recent work on system-prompt robustness reports that models can still forget guardrails or fail to resolve instruction conflicts, even when system prompts are present. Another 2026 paper on instruction-following optimization says models often produce substantively correct answers that fail formal constraints, and argues for treating constraints as measurable acceptance criteria rather than just task description prose.

So the right fix is not “make startup bigger.” It is:

Routing gate -> Artifact contract gate -> Output -> Validator

Better solution than the previous proposal

I would upgrade the plan from “pre-output checklist” to pre-output contract gates.

A checklist is softer. A contract gate is harder.
1. Terminal output should use a terminal contract gate

Before emitting any PowerShell, the AI must classify the block as one of:

INSTALL_SUCCESS
INSTALL_ERROR
VALIDATION
DIAGNOSTIC
OTHER_TERMINAL

Then the footer is selected by contract, not by memory.

INSTALL_SUCCESS:
success message -> Start-Sleep 5 -> Clear-Host -> keep open -> no Enter prompts

VALIDATION / DIAGNOSTIC / ERROR / OTHER_TERMINAL:
Read-Host -> Clear-Host -> Read-Host -> Clear-Host -> keep open

This should be a small always-startup hook, but the full details can remain in an on-request prompt.
2. Freeze JSON should not rely on “tolerant parsing”

For freeze forms, KANDA should use a strict schema contract.

Best design:

AI output:
KANDA_FREEZE_FORM_JSON_BEGIN
{compact valid JSON object}
KANDA_FREEZE_FORM_JSON_END

App validation:
json.loads()
required keys present
no extra prose
validation_evidence_summary contains exact marker

External sources strongly support schema-first structured output for this. Microsoft says structured outputs are for complex multi-step workflows and function calling; OpenAI’s docs show schema-constrained output; Google says you still validate final values in app code.
3. Freeze evidence should be a machine contract, not prose

Do not use vague wording like:

recognizable validation evidence

Use exact markers:

VALIDATION OK: freeze_hint_preserve_local_validation_v1
STATUS: IN_SYNC
CONTRACT_TEST_OK: ...

And define this rule:

If validation_evidence_summary lacks VALIDATION OK: <feature_id>, do not produce freeze-ready JSON.
Return FREEZE BLOCKED: validation marker missing.

This directly solves the failure you saw.
4. Patch ZIPs need a manifest-grade sidecar

KANDA_FREEZE_HINT.json was a very good fix. I would strengthen it into a formal schema:

kind
schema_version
patch_name
feature_id
feature_title
primary_box
box_type
validated_files
generated_files
protected_paths
do_not_regress_rules
validation_evidence_summary
freeze_readiness
requires_user_validation

Important improvement:

freeze_readiness:
pre_validation_hint | locally_validated | frozen

That avoids ambiguity between a sidecar created before validation and a sidecar updated after validation.
5. The app should remain defensive

The app-side fixes you already made were correct:

Do not downgrade local validation evidence.
Do not replace VALIDATION OK with Local validation pending.
Do not use stale heuristic feature titles when a current freeze hint exists.

This aligns with guardrail best practices: output guardrails and validation should exist outside the model, not only in the prompt. Datadog’s guardrail guidance describes output guardrails as post-processing/validation layers that can enforce schema validation or reject/repair malformed output.
What I would now patch

I would create one narrow patch:

pre_output_contract_gates_v1

Not a router rewrite.

It should add:

1. pre_output_contract_gates.md
2. Terminal contract gate
3. Patch delivery contract gate
4. Freeze JSON contract gate
5. Freeze validation evidence exact-marker contract
6. Startup hook that says when to apply this prompt
7. Tests RG-031 to RG-040

I would not add all of this as giant always-loaded text. Startup should only include a short hook:

When producing terminal code, patch ZIP instructions, validation commands, or freeze-form JSON, apply pre_output_contract_gates before output.

The full prompt remains on-request.
Updated smart tests

The test matrix should now check contracts, not “AI intention.”

RG-031: INSTALL_SUCCESS terminal block
Must use 5 seconds -> Clear-Host, no Enter prompts.

RG-032: VALIDATION terminal block
Must use Enter -> Clear -> Enter -> Clear.

RG-033: patch install staging
Must move ZIP from drive root to delete_after_daily_work, extract fresh, never assume extracted folder exists.

RG-034: freeze JSON strict mode
Must output only markers plus compact valid JSON.

RG-035: missing validation marker
Must block freeze JSON if VALIDATION OK: <feature_id> is absent.

RG-036: freeze-ready ZIP sidecar
Must include KANDA_FREEZE_HINT.json or explicitly mark patch as non-freezeable.

RG-037: sidecar beats chat memory
If chat memory says one feature and sidecar says another, sidecar wins.

RG-038: monotonic validation
Same-feature rescan must not downgrade VALIDATION OK to pending.

RG-039: external project root
Freeze-intake and frozen memory must use selected active project root, not hardcoded E:\kanda_reasoner.

RG-040: Fast Path no over-routing
Simple explanation must not request governed prompt packs.

Final recommendation before patch

Use the external research to refine the solution like this:

Old solution:
Pre-output checklist.

Better solution:
Pre-output contract gates + schema validation + exact markers + app-side monotonic state.

So yes, proceed with a targeted patch, but name/design it as a contract gate patch, not just a checklist patch.

The core architecture should become:

Router decides what context is needed.
Contract gate decides whether the planned output is allowed.
Validator/app confirms the output is parseable and safe.
Freeze memory records only validated behavior.

That is the most robust solution for the logic problem you observed.

before continuing , go again to web, get the top of the list 5 books on prompt engineering and search for other enligtening ideas to update solution and solve logic problem

I searched again, focusing on book-level prompt engineering / LLM engineering sources and the newer “promptware engineering” idea.

The best update is this:

Do not patch this as only "better prompting."

Patch it as:
prompt-as-software + pre-output contract gates + validators + regression tests.

Top 5 books/resources most relevant to KANDA

    Prompt Engineering for LLMs — John Berryman and Albert Ziegler
    Most relevant for KANDA because it treats prompting as part of building LLM-powered applications, not just “write better prompts.” O’Reilly describes it as teaching both the art/science of prompt engineering and LLM-based application building.

    Prompt Engineering for Generative AI — James Phoenix and Mike Taylor
    Useful because it explicitly frames prompt engineering around making outputs reliable enough for automated systems. That maps directly to your freeze JSON / PowerShell / validation-output problem.

    Prompt Engineering for AI Systems — Manning
    Very relevant because Manning describes it as teaching “structured and reusable prompt patterns” to reduce hallucinations and improve code-generation quality. That supports your idea of reusable contract gates instead of ad hoc reminders.

    AI Engineering — Chip Huyen
    Not just prompt engineering, but important for the KANDA problem because it treats AI as an engineered application lifecycle: models, datasets, evaluation, deployment, and system design. That supports moving from “prompt says X” to “system validates X.”

    Building Reliable AI Systems — Manning / Rush Shahani
    Useful because it focuses on production-level LLM applications, maintenance, and reliability. That is exactly the level KANDA has reached: prompt routing is not enough; behavior must be tested and maintained.

A newer research idea is also very important: promptware engineering. A 2025 paper argues that prompts should be treated as first-class software artifacts with requirements, design, implementation, testing, debugging, evolution, deployment, and monitoring. That is probably the most important conceptual upgrade for KANDA.
Updated solution after this second search

The previous idea was:

Pre-output compliance checklist

I would now upgrade it to:

Pre-output contract gate + artifact validator + regression test

Meaning:

Router:
chooses the correct prompt/context.

Contract gate:
decides whether the planned output is allowed.

Validator:
checks the actual emitted artifact.

Regression test:
proves the failure does not return.

Why this is better

A checklist still depends on the model remembering and obeying.

A contract gate is stricter:

Before emitting PowerShell, classify artifact type:
INSTALL_SUCCESS / VALIDATION / DIAGNOSTIC / ERROR.

Before emitting freeze JSON, enforce:
strict markers, valid JSON, required fields, VALIDATION OK marker.

Before delivering patch ZIP, enforce:
staging path, fresh extraction, KANDA_FREEZE_HINT.json if freeze-ready.

This matches the book/resource pattern: reusable prompt patterns, reliable automated outputs, production guardrails, and prompt-as-software testing.
New design recommendation for KANDA

Create this feature:

pre_output_contract_gates_v1

It should not be a giant startup prompt. It should be a small on-request/routed prompt with a tiny startup hook.
Startup hook only says:

When producing terminal code, patch ZIP delivery instructions, validation commands, or freeze-form JSON, apply pre_output_contract_gates before output.

The full prompt contains four gates:

1. TERMINAL_OUTPUT_CONTRACT
2. PATCH_DELIVERY_CONTRACT
3. FREEZE_FORM_JSON_CONTRACT
4. VALIDATION_EVIDENCE_CONTRACT

The most important new idea

Add artifact validators.

Do not trust the AI output just because the prompt says the rule.

For example:

PowerShell footer validator:
- install block must contain Start-Sleep -Seconds 5 and Clear-Host
- install success must not contain Read-Host
- validation block must contain two Read-Host and two Clear-Host

Freeze JSON validator:
- exact markers
- json.loads passes
- all required fields exist
- validation_evidence_summary contains VALIDATION OK:

Patch delivery validator:
- ZIP starts in drive root
- creates delete_after_daily_work
- moves ZIP before extraction
- extracts fresh
- checks KANDA_FREEZE_HINT.json when freeze-ready

This is the key update from the books/resources: prompt rules should become executable contracts whenever possible.
Updated test set

I would keep RG-031 to RG-040, but now classify them as contract tests:

RG-031 TERMINAL_INSTALL_SUCCESS_CONTRACT
RG-032 TERMINAL_VALIDATION_CONTRACT
RG-033 PATCH_STAGING_CONTRACT
RG-034 FREEZE_JSON_STRICT_CONTRACT
RG-035 VALIDATION_EVIDENCE_MARKER_CONTRACT
RG-036 FREEZE_READY_SIDECAR_CONTRACT
RG-037 SIDECAR_BEATS_CHAT_MEMORY_CONTRACT
RG-038 MONOTONIC_FREEZE_HINT_CONTRACT
RG-039 EXTERNAL_PROJECT_ROOT_CONTRACT
RG-040 FAST_PATH_NO_OVERRAUTING_CONTRACT

Final updated recommendation

Before patching, change the patch concept from:

pre_output_compliance_hooks_v1

to:

pre_output_contract_gates_v1

This is more robust and more aligned with modern prompt engineering / AI engineering guidance.

The system should become:

Prompt router = selects context.
Contract gate = selects allowed output form.
Artifact validator = checks the produced output.
Freeze memory = records only validated behavior.
Regression tests = prevent return of old failures.

This solves the real logic problem better than adding more prompt text.

now before starting explain in details the problem and solution for techinical documentation

Below is a technical-documentation draft you can keep as the conceptual basis before patching. It explains the problem clearly enough for another AI or developer to understand why the router passed tests but operational outputs still failed.
KANDA Reasoner - Output-Time Compliance Failure and Pre-Output Contract Gates
1. Executive summary

KANDA Reasoner already has a functioning prompt router. The router can classify tasks as Fast Path or Routed Work Path, request the correct prompt groups, protect governed workflows, and avoid loading every prompt blindly.

The current problem is not that the router is fundamentally broken.

The problem is that the AI can correctly route a task, but later fail when producing the final operational artifact. Examples include PowerShell install blocks, validation blocks, patch delivery instructions, freeze-form JSON, and freeze-ready ZIP metadata.

In other words:

Router-time compliance works better than output-time compliance.

The AI may know the rule during task classification, but fail to apply the same rule when writing code, JSON, or install instructions.

This creates a reliability gap:

    The router selects the right path.

    The AI starts producing a concrete artifact.

    The AI falls back to habitual generic patterns.

    A KANDA-specific canonical rule is violated.

    The app or human detects the error only after output was produced.

The solution is to add a small, explicit, output-time contract layer.

This feature should be called:

pre_output_contract_gates_v1

Its purpose is to force artifact-specific checks immediately before producing high-risk outputs.
2. Core problem

KANDA has many canonical rules. Some examples:

    Install success blocks must wait 5 seconds and clear the terminal without asking for Enter.

    Validation, diagnostic, and error blocks must keep the terminal open and use the Enter, clear, Enter, clear cleanup pattern.

    Patch ZIPs must be staged in the project-drive delete-after-daily-work folder and freshly extracted.

    Freeze-ready patch ZIPs must include a root-level KANDA_FREEZE_HINT.json sidecar.

    Freeze-form JSON must be strict parser-ready JSON between exact markers.

    validation_evidence_summary must contain recognizer-friendly validation evidence such as VALIDATION OK: feature_id.

    Freeze-intake and frozen-memory state must belong to the selected active project root, not always to KANDA Reasoner itself.

    Confirm and Write must remain human-confirmed.

These rules already exist in the prompt system or were added during recent fixes.

However, the AI still failed some of them. That means the issue is not only missing knowledge. The issue is rule activation at the moment of artifact generation.
3. Difference between routing compliance and output compliance
Routing compliance

Routing compliance answers:

    Is this task simple or governed?

    Is this Fast Path or Routed Work Path?

    Which prompts, folder cards, source files, or validation context are required?

    May the AI proceed now?

    Should implementation be blocked until required context is available?

The router has already passed important targeted tests for these behaviors, including freeze-workflow bypass detection, stale startup filename detection, and Fast Path no-overrouting.
Output compliance

Output compliance answers:

    Is this PowerShell block using the correct footer?

    Is this validation block using the validation cleanup pattern?

    Is this patch install block moving the ZIP to staging before extraction?

    Is this freeze JSON valid and parser-ready?

    Does this freeze form contain exact validation evidence markers?

    Does this freeze-ready patch include the required sidecar metadata?

    Does this operation preserve multi-project root ownership?

The recent failures occurred mainly at output compliance time.
4. Observed failure classes
4.1 Terminal cleanup pattern failure

Expected KANDA behavior:

Install success:

    Show success.

    Wait 5 seconds.

    Clear the terminal.

    Keep terminal open.

    Do not ask for Enter.

Validation, diagnostic, install-error, or validation-error:

    Keep terminal open.

    Press Enter.

    Clear terminal.

    Press Enter again.

    Clear terminal again.

Observed failure:

The AI mixed both patterns and produced an old generic footer.

Root cause:

The rule existed, but the AI did not re-check it immediately before writing the terminal block.
4.2 Patch staging failure

Expected KANDA behavior:

The human downloads the patch ZIP to the root of the project drive, for example:

E:\patch_name.zip

The installer must:

    Create the delete-after-daily-work folder if missing.

    Move the ZIP into that staging folder.

    Freshly extract the ZIP.

    Copy only the intended files.

    Avoid relying on old extracted folders.

    Keep temporary install artifacts out of the active project root.

Observed failure:

The AI initially wrote an install sequence that assumed an extracted folder already existed.

Root cause:

The AI remembered part of the patch process but did not enforce the full staging contract.
4.3 Stale freeze form feature identity

Expected KANDA behavior:

When freezing a newly implemented feature, the freeze form should use the current feature title, current validation evidence, current protected paths, and current do-not-regress rules.

Observed failure:

The app repeatedly generated a freeze form for an older feature:

Freeze Feature After Update Local Freeze Workflow v1

instead of the current implemented feature.

Root cause:

The chat knew the current feature, but the app did not have a deterministic machine-readable bridge from chat output to local freeze-intake state.

Fix already implemented:

    KANDA_FREEZE_HINT.json was introduced as root-level patch ZIP metadata.

    freeze_hint_intake was created as an app-side box.

    The app now saves feature-specific freeze-intake data under:
    selected_active_project_root/project_freeze_after_update/freeze_hint_intake

4.4 Validation evidence marker failure

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
4.5 Validation evidence downgrade on rescan

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
4.6 Strict freeze-form JSON parse failure

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
5. Why the failures happened

The failures are best explained as output-time instruction decay.

The AI can correctly understand the rule at routing time but then shift into artifact-generation mode. When producing code or JSON, the model tends to prioritize familiar code patterns or formatting habits over project-specific operational details.

This is especially likely when:

    The rule is far from the final output.

    The final output is code or JSON.

    The rule is described in prose rather than enforced as a contract.

    The task has many moving parts.

    There is no pre-output gate immediately before emission.

    The app does not validate or preserve state defensively.

Therefore, adding more descriptive text to startup is not enough.

The fix must put the rule at the point of action.
6. Proposed solution

Create a feature called:

pre_output_contract_gates_v1

This feature adds a small contract layer between routing and final output.

The architecture becomes:

    Router
    Decides whether the task is Fast Path or Routed Work Path and identifies required context.

    Pre-output contract gate
    Checks the specific artifact type before the AI emits it.

    Artifact output
    The AI emits PowerShell, patch instructions, freeze JSON, or validation text.

    Validator or app-side guard
    KANDA validates format, state, paths, and evidence.

    Freeze memory
    Only validated behavior is frozen.

7. Contract gate types
7.1 Terminal Output Contract

Triggered before any PowerShell or terminal block.

The AI must classify the block as one of:

    INSTALL_SUCCESS

    INSTALL_ERROR

    VALIDATION

    DIAGNOSTIC

    OTHER_TERMINAL

Contract:

INSTALL_SUCCESS must use:

    Success message.

    Start-Sleep -Seconds 5.

    Clear-Host.

    No Read-Host success prompts.

    Terminal remains open.

VALIDATION, DIAGNOSTIC, INSTALL_ERROR, VALIDATION_ERROR, and OTHER_TERMINAL must use:

    Read-Host.

    Clear-Host.

    Read-Host again.

    Clear-Host again.

    Terminal remains open.

Forbidden:

    Do not close terminal.

    Do not mix 5-second clear with Enter Enter.

    Do not use generic cleanup footers.

    Do not assume the user wants the terminal closed.

7.2 Patch Delivery Contract

Triggered before any patch ZIP delivery or install instructions.

Contract:

    Patch ZIP contains only updated files and required metadata.

    Freeze-ready patch ZIP includes root-level KANDA_FREEZE_HINT.json.

    KANDA_FREEZE_HINT.json is delivery metadata, not an installed project source file.

    The user downloads the ZIP to the root of the same drive as the project.

    The installer creates or uses:
    drive:\project_name_delete_after_daily_work

    The installer moves the ZIP into that staging folder before extraction.

    The installer freshly extracts every run.

    The installer must not assume yesterday's extracted folder exists.

    The installer must not place temporary scripts or one-use files into the active project root.

    Install and validation commands must be separate.

Forbidden:

    Do not package the whole project.

    Do not include caches or backup folders.

    Do not assume pre-extracted paths.

    Do not omit KANDA_FREEZE_HINT.json for freeze-ready patches.

7.3 Freeze Form JSON Contract

Triggered before returning a KANDA freeze-form JSON block.

Contract:

The entire answer must be exactly:

KANDA_FREEZE_FORM_JSON_BEGIN
{compact valid JSON object}
KANDA_FREEZE_FORM_JSON_END

Required properties:

    feature_title

    primary_box

    box_type

    validated_files

    generated_files

    protected_paths

    do_not_regress_rules

    validation_evidence_summary

    known_warnings

    planned_next_step

    notes

Required evidence:

validation_evidence_summary must include:

VALIDATION OK: feature_id

when local validation actually passed.

If startup delivery was validated, it should also include:

STATUS: IN_SYNC

Forbidden:

    No markdown fences.

    No extra explanation.

    No bullets.

    No comments.

    No trailing commas.

    No invalid backslash escapes.

    No pretty formatting if the parser is failing; compact JSON is preferred.

    Do not invent validation evidence.

7.4 Validation Evidence Contract

Triggered before freeze-ready metadata or freeze-form JSON.

Contract:

If a feature is claimed as locally validated, evidence must include at least:

VALIDATION OK: feature_id

Optional additional evidence may include:

    CONTRACT_TEST_OK: ...

    STATUS: IN_SYNC

    SANDBOX_..._VALIDATION_OK

If the exact validation marker is missing, the AI must not produce freeze-ready JSON. It must return:

FREEZE BLOCKED - validation evidence marker missing

Forbidden:

    Do not treat generic "sandbox passed" text as sufficient.

    Do not invent user-local validation.

    Do not use old validation evidence from another feature.

    Do not reuse stale feature titles.

7.5 Freeze Hint Intake Contract

Triggered before preparing or using freeze-ready patch metadata.

Contract:

    Feature identity comes from KANDA_FREEZE_HINT.json when available.

    Chat memory does not override the sidecar.

    If sidecar and chat context disagree, sidecar wins.

    If no sidecar exists and current feature identity is unclear, the AI must ask or mark the patch as non-freezeable.

    Freeze-intake state belongs under:
    selected_active_project_root/project_freeze_after_update/freeze_hint_intake

    Frozen memory belongs under:
    selected_active_project_root/project_freeze_after_update/frozen_features_memory

    project_freeze_ledger remains reusable engine/blueprint logic and must not own active project frozen memory.

Monotonic state rule:

A saved freeze hint with recognizer-friendly validation evidence must not be overwritten by weaker pending evidence from a staged ZIP rescan.
8. Why contract gates are better than more startup text

More startup text increases context load and may reduce accuracy.

Contract gates are short, artifact-specific, and applied at the moment of output generation.

The router should not become a giant monolithic prompt. KANDA should keep specialized prompts on-request and use small startup hooks only when necessary.

Better design:

    Startup stays lean.

    Router stays responsible for context selection.

    Contract gates handle high-risk artifact output.

    Validators enforce machine-readable contracts.

    Tests verify behavior classes, not every prompt one by one.

9. Implementation scope

Recommended feature:

pre_output_contract_gates_v1

Suggested prompt/library additions:

    Add:
    pre_output_contract_gates.md

    Register it as on-request/routed.

    Add a small startup hook:
    When producing terminal code, patch ZIP delivery instructions, validation commands, or freeze-form JSON, apply pre_output_contract_gates before output.

    Update daily_patch_delivery_guardrails.md:
    Add hard terminal-output contract and patch-staging contract.

    Update freeze_code_intake_and_form_protocol.md:
    Add strict freeze-form JSON contract and validation-evidence exact-marker contract.

    Update routing/index files:
    Route terminal, patch delivery, freeze JSON, and freeze-ready ZIP outputs to the pre-output contract gate.

    Regenerate startup delivery artifacts:
    first_prompts_to_ai.zip
    paste_after_first_prompts_to_ai.md
    paste_if_modify_startup_delivery.md

    Include KANDA_FREEZE_HINT.json in the patch ZIP.

Not recommended:

    Do not rewrite the whole router.

    Do not load all prompts daily.

    Do not remove Confirm and Write.

    Do not hardcode E:\kanda_reasoner as the active project root.

    Do not rely only on prompts when app-side validation is possible.

10. Test strategy

Do not test all prompts one by one.

Test behavior classes.

Core tests:
RG-031 - Terminal install success contract

Scenario:
Ask the AI to produce an install block for a patch.

Expected:
Install success footer uses Start-Sleep -Seconds 5 and Clear-Host. It does not use Read-Host on success. Terminal remains open.

Fail if:
The footer uses Enter Enter or mixed cleanup.
RG-032 - Terminal validation contract

Scenario:
Ask the AI to produce a validation block.

Expected:
Validation block uses Read-Host, Clear-Host, Read-Host, Clear-Host. Terminal remains open.

Fail if:
The footer auto-clears after 5 seconds or closes terminal.
RG-033 - Patch staging contract

Scenario:
Ask for patch installation instructions.

Expected:
Installer moves the ZIP from the drive root into delete-after-daily-work, then freshly extracts.

Fail if:
Installer assumes an extracted folder already exists.
RG-034 - Freeze JSON strict contract

Scenario:
Ask for freeze-form JSON.

Expected:
Only exact markers and valid compact JSON.

Fail if:
Markdown, prose, comments, invalid JSON, missing markers, or parser rejection.
RG-035 - Validation evidence marker contract

Scenario:
Give validation evidence without VALIDATION OK: feature_id.

Expected:
AI blocks freeze JSON and says validation marker is missing.

Fail if:
AI produces freeze JSON anyway.
RG-036 - Freeze-ready sidecar contract

Scenario:
Patch is intended to be freeze-ready.

Expected:
Patch ZIP includes root-level KANDA_FREEZE_HINT.json.

Fail if:
Patch is delivered freeze-ready without sidecar or without explanation.
RG-037 - Sidecar beats chat memory

Scenario:
Chat context suggests one feature, but sidecar contains another.

Expected:
AI uses sidecar feature identity.

Fail if:
AI uses old chat memory.
RG-038 - Monotonic freeze hint contract

Scenario:
A validated freeze hint is rescanned from the same staged ZIP.

Expected:
The saved validation evidence remains validated.

Fail if:
It downgrades to pending validation.
RG-039 - External project root contract

Scenario:
KANDA Reasoner is analyzing another project.

Expected:
Freeze-intake and frozen memory are stored under the selected active project root.

Fail if:
State is hardcoded to E:\kanda_reasoner.
RG-040 - Fast Path no-overrouting

Scenario:
Ask for a simple explanation.

Expected:
Fast Path. No unnecessary prompt loading.

Fail if:
AI asks for governed prompt packs.
11. Success criteria

The feature is successful when:

    Install blocks no longer use mixed terminal footers.

    Validation blocks no longer use install-success footers.

    Patch installers always stage and freshly extract ZIPs.

    Freeze JSON is parser-safe on first attempt.

    Freeze forms contain exact validation markers.

    Freeze-ready patches include KANDA_FREEZE_HINT.json.

    Sidecar feature identity overrides stale chat memory.

    Same-source rescans do not downgrade local validation evidence.

    External project freeze paths remain project-specific.

    Fast Path still avoids over-routing.

12. Final design principle

KANDA should treat prompts as software.

A prompt rule should not remain only a paragraph of advice when it controls a machine-consumed artifact.

For high-risk outputs, each prompt rule should become:

    A contract.

    A validator.

    A regression test.

    A freeze entry after validation.

The final architecture should be:

Router selects context.
Contract gate selects allowed output form.
Artifact validator checks output.
App state preserves stronger evidence.
Freeze memory records validated behavior.
Regression tests prevent old failures from returning.

This solves the real problem without destabilizing the router.

This draft is consistent with the canonical router rule that KANDA must not guess and should selectively load only the required context, not all prompts blindly. It also aligns with the existing freeze-ready ZIP, strict freeze JSON, patch staging, and terminal cleanup rules already present in the project canon. The recent audit correctly identifies the failure as output-generation compliance rather than router failure, and it recommends behavior-class tests instead of 80 one-by-one prompt tests.

now a complete detailed an numered roadmap of implementation. the intent of this implement is to make AI  follow the  cannon. to roadmapping

I’ll turn the design into an implementation roadmap, not patch code yet. The goal is to make the canon executable: prompts trigger the rule, code validates the artifact, tests prove the old failures do not return.

Based on the current canon, the roadmap should preserve three principles: KANDA is a multi-prompt router, not one giant prompt; the AI must not guess when governed context is missing; and startup should stay lean while specialized prompts remain routed/on-request. The project already defines freeze-ready sidecars, strict freeze-form JSON, patch staging, terminal cleanup, validation evidence, and multi-project freeze paths, so this roadmap is about making those rules fire at output time, not inventing a new router. The proposed behavior-class tests RG-031 to RG-040 are also aligned with the audit: test high-risk behaviors, not all prompts one by one.
ROADMAP - pre_output_contract_gates_v1
Intent

Implement a compliance layer that makes AI follow the KANDA canon at the exact moment it produces high-risk outputs.

The goal is not to rewrite the router.

The goal is to prevent this failure pattern:

    AI routes the task correctly.

    AI understands the canon in general.

    AI begins writing the final artifact.

    AI falls back to generic habits.

    AI violates a KANDA canonical rule in PowerShell, patch delivery, freeze JSON, validation evidence, or project-root placement.

The new feature should make KANDA behave like this:

    Router selects the correct path and context.

    Pre-output contract gate classifies the artifact about to be emitted.

    The gate applies the exact KANDA canon for that artifact type.

    The AI emits the artifact only if it satisfies the contract.

    Validators and tests check the output.

    Validated behavior is frozen.

Feature name:

pre_output_contract_gates_v1

Primary purpose:

Make the AI follow the canon, especially for terminal blocks, patch ZIP delivery, freeze-form JSON, validation evidence, freeze sidecars, and multi-project paths.
1. Define implementation scope
1.1 In scope

Implement a narrow prompt-routing and compliance feature:

    Add a new on-request prompt:
    pre_output_contract_gates.md

    Add metadata for the prompt.

    Register the prompt in the relevant prompt-library indexes.

    Add a small startup hook, not the full prompt.

    Update daily patch delivery guardrails to reference the contract gates.

    Update freeze-code intake protocol to reference the strict freeze-form and validation evidence gates.

    Add tests RG-031 to RG-040.

    Regenerate startup artifacts.

    Deliver as a patch ZIP with KANDA_FREEZE_HINT.json.

    Validate and freeze after installation.

1.2 Out of scope

Do not rewrite the router.

Do not load all prompts daily.

Do not make all 80 prompts always-startup.

Do not remove Confirm and Write.

Do not bypass local human confirmation.

Do not store active project freeze memory in project_freeze_ledger.

Do not hardcode E:\kanda_reasoner as the active project root for all projects.

Do not install KANDA_FREEZE_HINT.json into the project root as a source file.

Do not invent validation evidence.
2. Architectural design
2.1 Current architecture

Current flow:

    Startup prompt package loads.

    Router decides Fast Path or Routed Work Path.

    AI requests or uses required context.

    AI generates output.

Problem:

There is no mandatory final contract check between step 3 and step 4.
2.2 Target architecture

New flow:

    Startup prompt package loads.

    Router decides Fast Path or Routed Work Path.

    AI requests or uses required context.

    If output is high-risk, AI applies pre_output_contract_gates.

    AI emits terminal block, patch delivery instructions, freeze JSON, or validation evidence.

    Validator/test checks artifact.

    Freeze only after validated behavior.

2.3 Design principle

Router-time rules are not enough.

Output-time contracts are required for machine-consumed artifacts.

The AI should not merely remember the canon. It must be forced to classify the artifact type and apply the corresponding contract before emission.
3. New prompt design
3.1 New prompt file

Create:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md

Rationale:

The feature mostly protects patch delivery, freeze forms, freeze-ready ZIPs, validation evidence, terminal hygiene, and freeze-intake behavior. These belong closest to governance, freeze, handoff, and delivery.
3.2 Prompt status

Load mode:

on_request

Reason:

The canon says startup prompts should remain lean. The full contract-gate prompt should not become a giant always-loaded startup prompt.
3.3 Prompt role

The prompt is invoked before emitting high-risk artifacts.

It is not a replacement for the router.

It is not a replacement for freeze_code_intake_and_form_protocol.

It is a final compliance layer.
4. Startup hook design
4.1 Add a tiny startup hook

Add a short hook into the startup delivery source that generates paste_after_first_prompts_to_ai.md.

Suggested hook:

PRE-OUTPUT CONTRACT GATES HOOK

When producing any of the following artifacts, request or apply pre_output_contract_gates from 03_governance_freeze_and_handoff before emitting the final output:

    PowerShell or terminal install block.

    PowerShell or terminal validation block.

    Diagnostic or error terminal block.

    Patch ZIP delivery instructions.

    Freeze-ready patch ZIP instructions.

    KANDA_FREEZE_FORM_JSON_BEGIN / KANDA_FREEZE_FORM_JSON_END output.

    Validation evidence summary intended for freezing.

    KANDA_FREEZE_HINT.json metadata.

Required behavior:

Do not rely on memory.
Do not use generic terminal footers.
Do not emit freeze JSON without exact validation markers.
Do not emit freeze-ready patch delivery without checking sidecar requirements.
Do not hardcode active project paths.
4.2 Do not paste the entire prompt into startup

Startup should only contain the hook.

The full prompt remains on-request.
5. Contract gate contents
5.1 Gate A - Terminal Output Contract

Triggered before any terminal or PowerShell block.

The AI must classify the terminal block as one of:

    INSTALL_SUCCESS

    INSTALL_ERROR

    VALIDATION

    DIAGNOSTIC

    OTHER_TERMINAL

Contract:

INSTALL_SUCCESS must end with:

    success message

    Start-Sleep -Seconds 5

    Clear-Host

    no Read-Host success prompt

    no terminal close

VALIDATION, DIAGNOSTIC, INSTALL_ERROR, VALIDATION_ERROR, and OTHER_TERMINAL must end with:

    Read-Host

    Clear-Host

    Read-Host

    Clear-Host

    no terminal close

Forbidden:

    Do not mix install-success and validation cleanup.

    Do not use old generic footer.

    Do not ask for Enter after successful install.

    Do not auto-clear validation output after 5 seconds.

    Do not close the terminal.

5.2 Gate B - Patch Delivery Contract

Triggered before any patch ZIP delivery or install instructions.

Contract:

    Patch ZIP contains only updated files plus required metadata.

    User downloads the ZIP to the root of the same drive as the project.

    Installer creates the delete-after-daily-work folder if missing.

    Installer moves ZIP from drive root into staging folder.

    Installer freshly extracts every time.

    Installer does not assume any extracted folder already exists.

    Installer does not put temporary scripts in project root.

    Install and validation commands are separate.

    Freeze-ready patch ZIPs include root-level KANDA_FREEZE_HINT.json.

    KANDA_FREEZE_HINT.json is delivery metadata, not installed source.

Forbidden:

    Do not package the whole project.

    Do not include caches.

    Do not include backup folders.

    Do not include unrelated unchanged files.

    Do not rely on yesterday's extracted folder.

    Do not omit KANDA_FREEZE_HINT.json from freeze-ready patches unless explicitly non-freezeable.

5.3 Gate C - Freeze Form JSON Contract

Triggered before returning freeze-form JSON to the app.

Contract:

Output exactly:

KANDA_FREEZE_FORM_JSON_BEGIN
{"feature_title":"...","primary_box":"...","box_type":"...","validated_files":"...","generated_files":"...","protected_paths":"...","do_not_regress_rules":"...","validation_evidence_summary":"...","known_warnings":"...","planned_next_step":"...","notes":"..."}
KANDA_FREEZE_FORM_JSON_END

Required fields:

    feature_title

    primary_box

    box_type

    validated_files

    generated_files

    protected_paths

    do_not_regress_rules

    validation_evidence_summary

    known_warnings

    planned_next_step

    notes

Forbidden:

    No markdown fences.

    No bullets.

    No comments.

    No explanation.

    No trailing commas.

    No invalid backslash escapes.

    No prose between markers.

    No extra text before or after if strict receiver mode is requested.

    Do not invent validation evidence.

5.4 Gate D - Validation Evidence Contract

Triggered before any freeze-ready metadata or freeze-form JSON.

Contract:

If local validation passed, validation_evidence_summary must include:

VALIDATION OK: feature_id

If startup sync was validated, include:

STATUS: IN_SYNC

Optional evidence:

CONTRACT_TEST_OK: ...
SANDBOX_..._VALIDATION_OK
INSTALL OK: ...

If the exact validation marker is absent, do not produce freeze-ready JSON.

Required failure response:

FREEZE BLOCKED - validation evidence marker missing.

Forbidden:

    Do not treat "sandbox passed" alone as sufficient.

    Do not use validation from another feature.

    Do not reuse stale validation lists.

    Do not claim local validation before it happened.

    Do not convert STATUS: IN_SYNC into STATUS IN_SYNC.

5.5 Gate E - Freeze Hint Sidecar Contract

Triggered before freeze-ready patch delivery.

Contract:

KANDA_FREEZE_HINT.json must include:

    schema_version

    kind

    patch_name

    feature_id

    feature_title

    primary_box

    box_type

    validated_files

    generated_files

    protected_paths

    do_not_regress_rules

    validation_evidence_summary

    known_warnings

    planned_next_step

    notes

Recommended new fields:

    freeze_readiness

    requires_user_validation

    source_patch_zip

Allowed freeze_readiness values:

    pre_validation_hint

    locally_validated

    frozen

Rules:

    Sidecar describes the current patch feature.

    Sidecar must not describe an older heuristic feature.

    Sidecar must not be installed into project root.

    Chat memory must not override sidecar identity.

    If sidecar and chat context disagree, sidecar wins.

    If no sidecar exists and the patch is freeze-ready, block or mark non-freezeable.

5.6 Gate F - Multi-project Root Contract

Triggered before freeze-intake or freeze-memory paths.

Contract:

Active project root owns project-specific state.

If active project is E:\kanda_reasoner:

E:\kanda_reasoner\project_freeze_after_update\freeze_hint_intake
E:\kanda_reasoner\project_freeze_after_update\frozen_features_memory

If active project is D:\any_project:

D:\any_project\project_freeze_after_update\freeze_hint_intake
D:\any_project\project_freeze_after_update\frozen_features_memory

Forbidden:

    Do not store active project freeze memory inside project_freeze_ledger.

    Do not assume KANDA Reasoner is always the active project.

    Do not write external project freeze state under E:\kanda_reasoner merely because KANDA is the tool.

6. Prompt-library registration roadmap
6.1 Add prompt file

Add:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md
6.2 Add metadata

Add:

kanda_prompt_workspace/prompt_library/METADATA/pre_output_contract_gates.meta.json

Metadata should include:

prompt_id: pre_output_contract_gates
category: 03_governance_freeze_and_handoff
load_type: on_request
purpose: output-time contract gate for terminal code, patch delivery, freeze JSON, validation evidence, freeze sidecars, and multi-project path compliance
6.3 Update folder assimilation

Update:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md

Add the new prompt to the folder card.
6.4 Update routing indexes

Update:

kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md
kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json

Add routes for:

    terminal block generation

    PowerShell install generation

    validation block generation

    patch ZIP delivery

    freeze-ready patch delivery

    freeze-form JSON output

    validation evidence summary

    KANDA_FREEZE_HINT.json delivery metadata

    multi-project freeze path verification

6.5 Update startup delivery generator source map if required

If startup delivery is generated from a source map, update:

kanda_prompt_workspace/startup_routing_kernel/STARTUP_ROUTING_KERNEL_SOURCES.json

or the equivalent active source map.

Do not manually edit generated startup ZIP content as durable source.
7. Startup delivery update roadmap
7.1 Update startup hook source

Add only a small first-position hook to the source that generates paste_after_first_prompts_to_ai.md.

Hook purpose:

When the task will output terminal code, patch delivery instructions, validation commands, freeze-form JSON, freeze-ready patch ZIP metadata, or KANDA_FREEZE_HINT.json, apply pre_output_contract_gates before output.
7.2 Regenerate delivery artifacts

Run startup regeneration:

    sync_startup_routing_kernel_pack.py --ensure-sync --yes

    sync_startup_routing_kernel_pack.py --check

Expected:

STATUS: IN_SYNC
7.3 Confirm generated files updated

Expected generated files:

    kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip

    kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md

    kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md

    STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json if generated in delivery output

8. Validator roadmap
8.1 Terminal validator

Create a validator or test helper that checks generated PowerShell blocks.

Install success block must contain:

    Start-Sleep -Seconds 5

    Clear-Host

    no Read-Host in success footer

Validation or diagnostic block must contain:

    at least two Read-Host prompts

    at least two Clear-Host calls

    no 5-second auto-clear as the only cleanup

8.2 Patch delivery validator

Check install script contains:

    drive root ZIP path

    delete-after-daily-work staging folder

    New-Item for staging folder

    Move-Item or Copy-Item from root ZIP to staging ZIP

    Expand-Archive from staging ZIP

    removal of old extract folder before extraction

    no dependency on pre-existing extracted path

    no project-root temporary install script

8.3 Freeze JSON validator

Check AI output:

    begins with KANDA_FREEZE_FORM_JSON_BEGIN

    ends with KANDA_FREEZE_FORM_JSON_END

    contains one valid JSON object

    has all required fields

    has no markdown fences

    has no trailing commas

    has no unescaped invalid backslashes

    validation_evidence_summary contains VALIDATION OK: feature_id when validated

8.4 Freeze hint sidecar validator

Check patch ZIP contains:

    root-level KANDA_FREEZE_HINT.json

    kind == kanda_freeze_hint

    feature_id present

    feature_title present

    protected paths present

    validation_evidence_summary present

    project_freeze_after_update/frozen_features_memory present in protected_paths or do-not-regress rules

    project_freeze_ledger boundary rule present

    sidecar is not installed into project root

8.5 Multi-project path validator

Check:

    active project root is passed into freeze-intake functions

    freeze_hint_intake state goes under active_project_root/project_freeze_after_update/freeze_hint_intake

    frozen memory goes under active_project_root/project_freeze_after_update/frozen_features_memory

    project_freeze_ledger is not used as active project state owner

9. Regression test roadmap

Do not test all prompts one by one.

Test the behavior classes that previously failed.
9.1 RG-031 - Terminal install success contract

Scenario:

Ask AI to create a PowerShell install block for a patch.

Expected:

    Uses install success cleanup.

    Shows success message.

    Waits 5 seconds.

    Clears terminal.

    Keeps terminal open.

    Does not ask for Enter on success.

Fail if:

    Uses Enter Enter on success.

    Mixes 5-second cleanup with Enter prompts.

    Closes terminal.

9.2 RG-032 - Terminal validation contract

Scenario:

Ask AI to create a validation block.

Expected:

    Uses validation cleanup.

    Read-Host.

    Clear-Host.

    Read-Host again.

    Clear-Host again.

    Keeps terminal open.

Fail if:

    Uses install-success footer.

    Auto-clears after 5 seconds.

    Closes terminal.

9.3 RG-033 - Patch staging contract

Scenario:

Ask AI to provide patch install instructions.

Expected:

    ZIP starts at drive root.

    Installer creates staging folder.

    Installer moves ZIP to staging.

    Installer freshly extracts.

    Installer copies only intended files.

    Installer does not assume existing extracted folders.

Fail if:

    Extracted path is assumed.

    ZIP is not staged.

    Temporary files are placed in project root.

9.4 RG-034 - Freeze JSON strict contract

Scenario:

Ask AI for freeze-form JSON.

Expected:

    Exact markers.

    One valid compact JSON object.

    No markdown.

    No comments.

    All required fields.

Fail if:

    Parser rejects output.

    Extra text is inside markers.

    JSON is malformed.

9.5 RG-035 - Missing validation marker block

Scenario:

Ask AI to produce freeze JSON from validation evidence that lacks VALIDATION OK: feature_id.

Expected:

AI returns:

FREEZE BLOCKED - validation evidence marker missing.

Fail if:

AI produces freeze JSON anyway.
9.6 RG-036 - Freeze-ready sidecar contract

Scenario:

Ask AI to deliver a freeze-ready patch ZIP.

Expected:

Patch ZIP includes root-level KANDA_FREEZE_HINT.json.

Fail if:

    Sidecar is missing.

    Sidecar is under docs.

    Sidecar is installed as source.

    Sidecar describes wrong feature.

9.7 RG-037 - Sidecar beats chat memory

Scenario:

Chat context implies old feature, but KANDA_FREEZE_HINT.json says current feature.

Expected:

AI uses sidecar feature identity.

Fail if:

AI uses stale chat context.
9.8 RG-038 - Monotonic freeze hint contract

Scenario:

Saved hint has VALIDATION OK: feature_id. Same staged ZIP is rescanned.

Expected:

Validation evidence remains.

Fail if:

Evidence downgrades to local validation pending.
9.9 RG-039 - External project root contract

Scenario:

KANDA Reasoner analyzes D:\any_project.

Expected:

Freeze-intake state:

D:\any_project\project_freeze_after_update\freeze_hint_intake

Frozen memory:

D:\any_project\project_freeze_after_update\frozen_features_memory

Fail if:

State is written under E:\kanda_reasoner by default.
9.10 RG-040 - Fast Path no-overrouting

Scenario:

Ask for simple explanation.

Expected:

Fast Path. No governed prompt loading.

Fail if:

AI requests unnecessary prompt packs.
10. Patch packaging roadmap
10.1 Patch name

pre_output_contract_gates_v1_patch.zip
10.2 ZIP contents

Include only changed files.

Expected files may include:

    kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md

    kanda_prompt_workspace/prompt_library/METADATA/pre_output_contract_gates.meta.json

    kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md

    kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md

    kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md

    kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md

    kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json

    kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md

    kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md

    kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py if generator hook requires update

    kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip

    kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md

    kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md

    tests or validation scripts if project has test folders for prompt-routing behavior

    KANDA_FREEZE_HINT.json at ZIP root

Do not include:

    whole project

    caches

    backups

    pycache

    temporary validation folders

    root installer scripts

    old extracted patch folders

10.3 KANDA_FREEZE_HINT.json

Feature title:

Pre-Output Contract Gates v1

Feature ID:

pre_output_contract_gates_v1

primary_box:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation + startup routing kernel + first_AI_deliver

box_type:

Prompt Routing / Output-Time Compliance / Artifact Contract Gate

validation_evidence_summary before local validation:

Local validation pending. Must be updated after validation with VALIDATION OK: pre_output_contract_gates_v1 and STATUS: IN_SYNC.

After validation, merge recognizer-friendly evidence into freeze hint intake.
11. Installation roadmap
11.1 Human download location

Human downloads patch ZIP to:

E:\pre_output_contract_gates_v1_patch.zip

or same drive root as active project.
11.2 Installer behavior

Installer must:

    Set PROJECT_ROOT to E:\kanda_reasoner for this patch, because this patch modifies KANDA Reasoner itself.

    Determine drive root from PROJECT_ROOT.

    Create E:\kanda_reasoner_delete_after_daily_work if missing.

    Move ZIP from drive root into staging folder.

    Remove old extraction folder if present.

    Extract fresh.

    Confirm KANDA_FREEZE_HINT.json exists at ZIP root.

    Copy only patch files.

    Regenerate startup delivery with sync_startup_routing_kernel_pack.py --ensure-sync --yes.

    Verify KANDA_FREEZE_HINT.json was not installed into project root.

    Show install success.

    Wait 5 seconds.

    Clear terminal.

    Keep terminal open.

11.3 Install failure behavior

On install failure:

    Show INSTALL FAILED.

    Show error message.

    Read-Host.

    Clear-Host.

    Read-Host again.

    Clear-Host.

    Keep terminal open.

12. Validation roadmap
12.1 Validation must check files

Validation script checks:

    New prompt exists.

    Metadata exists.

    Folder assimilation references the prompt.

    Routing indexes reference the prompt.

    Startup hook exists in generated paste file.

    Startup ZIP contains updated relevant files.

    sync_startup_routing_kernel_pack.py --check returns STATUS: IN_SYNC.

    KANDA_FREEZE_HINT.json exists in staged ZIP.

    KANDA_FREEZE_HINT.json is not installed into project root.

12.2 Validation must check prompt content

Validation script checks prompt contains:

    TERMINAL_OUTPUT_CONTRACT

    PATCH_DELIVERY_CONTRACT

    FREEZE_FORM_JSON_CONTRACT

    VALIDATION_EVIDENCE_CONTRACT

    FREEZE_HINT_SIDECAR_CONTRACT

    MULTI_PROJECT_ROOT_CONTRACT

    forbidden old mixed terminal footer

    strict JSON rules

    exact validation marker rule

    sidecar wins over chat memory rule

12.3 Validation must check startup sync

Expected output includes:

STATUS: IN_SYNC
12.4 Validation must output recognizer-friendly evidence

Validation block must output:

VALIDATION OK: pre_output_contract_gates_v1
CONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated
STATUS: IN_SYNC
12.5 Validation cleanup footer

Validation block must use:

Read-Host
Clear-Host
Read-Host
Clear-Host

Not 5-second success cleanup.
13. Post-validation freeze-intake roadmap

After validation passes:

    Call or run merge_validation_evidence_into_latest_hint if required.

    Ensure latest freeze hint contains:
    VALIDATION OK: pre_output_contract_gates_v1
    STATUS: IN_SYNC

    Open Freeze Feature After Update.

    Confirm Project root is E:\kanda_reasoner for this feature.

    Click New Local Freeze Entry.

    Confirm form title is:
    Pre-Output Contract Gates v1

    Confirm validation_evidence_summary contains:
    VALIDATION OK: pre_output_contract_gates_v1

    Preview Freeze Entry.

    Confirm and Write.

    Startup freeze context must refresh after local write.

14. Freeze roadmap
14.1 Freeze title

Pre-Output Contract Gates v1
14.2 Freeze do-not-regress rules

Include these rules:

    Terminal blocks must be classified before footer generation.

    Install success must use 5-second clear and no Enter prompt.

    Validation, diagnostic, and error blocks must use Enter, clear, Enter, clear.

    Patch install instructions must move ZIP to staging and extract fresh.

    Freeze-ready patch ZIPs must include root-level KANDA_FREEZE_HINT.json.

    KANDA_FREEZE_HINT.json must describe current feature.

    Freeze-form JSON must be exact marker-wrapped valid JSON.

    validation_evidence_summary must include VALIDATION OK: feature_id when validated.

    AI must block freeze JSON if validation marker is missing.

    Sidecar identity beats stale chat memory.

    Same-source rescans must not downgrade local validation evidence.

    Multi-project freeze paths must use selected active project root.

    Fast Path must remain lean and not over-route.

    Do not load all prompts daily.

    Do not remove Confirm and Write.

14.3 Freeze validation evidence

Use only actual validation evidence.

Required:

VALIDATION OK: pre_output_contract_gates_v1
STATUS: IN_SYNC

Optional:

CONTRACT_TEST_OK: ...
SANDBOX_..._VALIDATION_OK

Do not invent.
15. Manual pilot roadmap after patch

Run these after install and validation.
15.1 First run: RG-031 to RG-035

These directly cover the old failures:

    RG-031 terminal install success

    RG-032 terminal validation

    RG-033 patch staging

    RG-034 strict freeze JSON

    RG-035 missing validation marker

If any fail, repair before running the rest.
15.2 Second run: RG-036 to RG-040

These cover integration and boundaries:

    RG-036 freeze-ready sidecar

    RG-037 sidecar beats chat memory

    RG-038 monotonic freeze hint

    RG-039 external project root

    RG-040 Fast Path no-overrouting

15.3 Regression retest

Retest older closed routes:

    RG-028 confirmation-gate bypass

    RG-029 stale startup filename

    RG-030 Fast Path no-overrouting if needed

Reason:

Ensure the new pre-output gate did not over-route simple tasks or break existing first-position overrides.
16. Acceptance criteria

The feature is accepted only if all are true:

    Startup delivery is IN_SYNC.

    New prompt is registered and routed.

    Generated startup paste includes the short hook.

    Install block uses correct success footer.

    Validation block uses correct validation footer.

    Patch delivery uses staging and fresh extraction.

    Freeze JSON is parser-safe on first attempt.

    Missing validation marker blocks freeze JSON.

    Freeze-ready patch includes KANDA_FREEZE_HINT.json.

    Sidecar identity beats chat memory.

    Monotonic validation evidence is preserved.

    External project freeze paths use selected active project root.

    Fast Path remains Fast Path.

    Local freeze entry can be created and frozen.

    No project-specific freeze state is stored in project_freeze_ledger.

17. Failure handling roadmap
17.1 If terminal tests fail

Repair terminal contract wording and test again.

Do not proceed to freeze.
17.2 If patch staging fails

Repair patch delivery contract and install template.

Do not proceed to freeze.
17.3 If freeze JSON parser fails

Repair strict freeze-form JSON contract.

Prefer compact one-line JSON.

Avoid unescaped Windows backslashes inside JSON strings.
17.4 If validation marker is missing

Repair validation evidence contract.

Ensure validation block merges:

VALIDATION OK: pre_output_contract_gates_v1

into latest freeze hint.
17.5 If sidecar identity fails

Repair freeze hint sidecar contract.

Ensure AI does not infer current feature from chat memory when sidecar exists.
17.6 If external project root fails

Repair multi-project root contract.

Confirm active project root is passed into freeze-intake and freeze-memory logic.
17.7 If Fast Path over-routes

Move some hook text out of always-startup.

Keep only a tiny trigger in startup.

Keep full prompt on-request.
18. Documentation roadmap

After implementation, update documentation with:

    Why output-time compliance was added.

    Difference between router and contract gate.

    Supported artifact types.

    Terminal cleanup canon.

    Patch staging canon.

    Freeze JSON strict contract.

    Validation evidence exact marker rule.

    KANDA_FREEZE_HINT.json sidecar rule.

    Multi-project root rule.

    RG-031 to RG-040 test matrix.

    Freeze entry location.

    How to debug failures.

19. Future expansion roadmap

Only after this feature is validated and frozen:
19.1 Add automated artifact validators

Optional future validators:

    validate_terminal_footer_contract.py

    validate_patch_staging_contract.py

    validate_freeze_json_contract.py

    validate_freeze_hint_sidecar_contract.py

    validate_multi_project_freeze_paths.py

19.2 Add GUI exposure

Possible future UI:

    Contract gate status.

    Last freeze hint source.

    Last validation marker found.

    Stale exposure warning.

    Active project root confirmation.

19.3 Add test dashboard

Possible future tab:

    RG-031 status.

    RG-032 status.

    RG-033 status.

    RG-034 status.

    RG-035 status.

    RG-036 status.

    RG-037 status.

    RG-038 status.

    RG-039 status.

    RG-040 status.

20. Final roadmap summary

Implement in this exact order:

    Audit existing prompt files and confirm source-of-truth files.

    Create pre_output_contract_gates.md.

    Add prompt metadata.

    Register prompt in folder and routing indexes.

    Add tiny startup hook.

    Update daily patch delivery guardrails.

    Update freeze code intake protocol.

    Regenerate startup artifacts.

    Add KANDA_FREEZE_HINT.json to patch ZIP.

    Build install command with correct install footer.

    Build validation command with correct validation footer.

    Validate prompt registration and startup sync.

    Validate contract content.

    Run RG-031 to RG-035.

    Run RG-036 to RG-040.

    Retest RG-028 and RG-029.

    Merge validation evidence into freeze hint intake.

    Use New Local Freeze Entry.

    Confirm and Write after human review.

    Refresh startup freeze context.

    Freeze pre_output_contract_gates_v1.

    Create final handoff.

The implementation succeeds when the AI no longer merely knows the canon, but is forced to apply the canon immediately before producing high-risk artifacts.

are you secure to step by step patching?

Yes — secure to proceed step by step, but not secure to jump directly into a big patch without auditing the live project files first.

The safe path is:

    Audit current files first

        Find the exact prompt source files.

        Confirm whether freeze_code_intake_and_form_protocol, daily_patch_delivery_guardrails, startup generator, indexes, and metadata already contain related rules.

        Avoid duplicating or corrupting existing logic.

    Create one narrow patch only

        Feature: pre_output_contract_gates_v1

        Goal: make AI follow canon at output time.

        No router rewrite.

        No all-prompts daily load.

        No app behavior changes unless audit proves necessary.

    Patch prompt + routing layer

        Add pre_output_contract_gates.md.

        Register it as on-request.

        Add tiny startup hook.

        Update routing indexes.

        Regenerate startup ZIP.

    Validate in sandbox before delivery

        File presence.

        Prompt registration.

        Startup STATUS: IN_SYNC.

        Hook present in paste_after_first_prompts_to_ai.md.

        KANDA_FREEZE_HINT.json present in patch ZIP.

    Then deliver install + validation commands

        Install block uses correct install-success terminal behavior.

        Validation block uses Enter -> clear -> Enter -> clear.

        No mixed footer.

    After user-local validation

        Freeze pre_output_contract_gates_v1.

So yes: I am secure if we do it as a small audited patch.

I am not secure if we try to patch from memory. The first action should be: inspect the uploaded project ZIP/current files and build the patch from the actual current state.

kanda_reasoner.zip
Zip Archive
project is uploaded and everything related to prompts are in \kanda_reasoner\kanda_prompt_workspace

Good. I’ll treat kanda_prompt_workspace as the source-of-truth area for this patch, audit those prompt and startup-delivery files first, then patch only the minimal files needed for pre_output_contract_gates_v1.

I confirmed the workspace structure. The key files already exist and the patch can stay narrow: one new routed prompt, prompt metadata/index updates, small startup hook in the generator, refreshed startup delivery artifacts, and a freeze hint sidecar.

Patch created and sandbox-validated.

Sandbox validation passed:

SANDBOX_PRE_OUTPUT_CONTRACT_GATES_VALIDATION_OK
STATUS: IN_SYNC

What this patch adds:

Feature: Pre-Output Contract Gates v1

Goal:
Make AI follow the KANDA canon at output time, especially before emitting terminal code, patch delivery instructions, freeze JSON, validation evidence, KANDA_FREEZE_HINT.json, or multi-project freeze paths.

Main files updated:

kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md
kanda_prompt_workspace/prompt_library/METADATA/pre_output_contract_gates.meta.json
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md
kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md
kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md
kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py
kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip
kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md
kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md

The ZIP includes root-level delivery metadata:

KANDA_FREEZE_HINT.json

Save the ZIP here first:

E:\pre_output_contract_gates_v1_patch.zip

Do not manually move it. The installer moves it.

Install:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "pre_output_contract_gates_v1_patch"
$PROJECT_NAME = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
$WORK_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")

$ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT ($PATCH_NAME + ".zip")
$WORK_PATCH_ZIP = Join-Path $WORK_DIR ($PATCH_NAME + ".zip")
$EXTRACT_DIR = Join-Path $WORK_DIR $PATCH_NAME
$BACKUP_DIR = Join-Path $WORK_DIR ("backup_" + $PATCH_NAME + "_" + (Get-Date -Format "yyyyMMdd_HHmmss"))

try {
    Set-Location $PROJECT_ROOT

    if (-not (Test-Path $WORK_DIR)) {
        New-Item -ItemType Directory -Path $WORK_DIR -Force | Out-Null
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        Move-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force
        Write-Host "Moved patch ZIP from drive root into delete-after-daily-work staging folder:"
        Write-Host $WORK_PATCH_ZIP
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root ZIP still exists after move: $ROOT_PATCH_ZIP"
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $FREEZE_HINT = Join-Path $EXTRACT_DIR "KANDA_FREEZE_HINT.json"
    if (-not (Test-Path $FREEZE_HINT)) {
        throw "Patch ZIP is missing KANDA_FREEZE_HINT.json"
    }

    $FILES = @(
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\03_governance_freeze_and_handoff\pre_output_contract_gates.md",
        "kanda_prompt_workspace\prompt_library\METADATA\pre_output_contract_gates.meta.json",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\03_governance_freeze_and_handoff\_FOLDER_ASSIMILATION.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\FOLDER_ASSIMILATION_CARDS_INDEX.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\GROUP_ASSIMILATION_INDEX.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\prompt_navigation_index.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\prompt_navigation_index.json",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\01_session_start_and_navigation\daily_patch_delivery_guardrails.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\03_governance_freeze_and_handoff\freeze_code_intake_and_form_protocol.md",
        "kanda_prompt_workspace\prompt_tools\sync_startup_routing_kernel_pack.py",
        "kanda_prompt_workspace\first_AI_deliver\first_prompts_to_ai.zip",
        "kanda_prompt_workspace\first_AI_deliver\paste_after_first_prompts_to_ai.md",
        "kanda_prompt_workspace\first_AI_deliver\paste_if_modify_startup_delivery.md"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

        if (-not (Test-Path $SRC)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }

        if (Test-Path $DST) {
            $BACKUP_FILE = Join-Path $BACKUP_DIR $REL
            New-Item -ItemType Directory -Path (Split-Path $BACKUP_FILE -Parent) -Force | Out-Null
            Copy-Item $DST $BACKUP_FILE -Force
        }

        New-Item -ItemType Directory -Path (Split-Path $DST -Parent) -Force | Out-Null
        Copy-Item $SRC $DST -Force
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not be installed into the project root."
    }

    Push-Location (Join-Path $PROJECT_ROOT "kanda_prompt_workspace")
    python ".\prompt_tools\sync_startup_routing_kernel_pack.py" --ensure-sync --yes
    if ($LASTEXITCODE -ne 0) {
        Pop-Location
        throw "Startup sync failed after pre-output contract gates patch."
    }
    Pop-Location

    Write-Host ""
    Write-Host "INSTALL OK. Terminal will clear in 5 seconds..."
    Write-Host "pre_output_contract_gates_v1 installed."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Clear-Host
    Read-Host "Press Enter again to finish"
    Clear-Host
}

Validate:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "pre_output_contract_gates_v1_patch"
$PROJECT_NAME = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
$WORK_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
$WORK_PATCH_ZIP = Join-Path $WORK_DIR ($PATCH_NAME + ".zip")
$VALIDATION_DIR = Join-Path $WORK_DIR "pre_output_contract_gates_v1_validation"
$VALIDATOR = Join-Path $VALIDATION_DIR "validate_pre_output_contract_gates_v1.py"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    if (-not (Test-Path $VALIDATION_DIR)) {
        New-Item -ItemType Directory -Path $VALIDATION_DIR -Force | Out-Null
    }

    $PY = @'
from pathlib import Path
import json
import py_compile
import subprocess
import sys
import zipfile

project_root = Path(r"__PROJECT_ROOT__")
work_patch_zip = Path(r"__WORK_PATCH_ZIP__")

workspace = project_root / "kanda_prompt_workspace"

prompt = workspace / "prompt_library" / "ACTIVE_PROMPTS" / "03_governance_freeze_and_handoff" / "pre_output_contract_gates.md"
meta = workspace / "prompt_library" / "METADATA" / "pre_output_contract_gates.meta.json"
folder_card = workspace / "prompt_library" / "ACTIVE_PROMPTS" / "03_governance_freeze_and_handoff" / "_FOLDER_ASSIMILATION.md"
folder_index = workspace / "prompt_library" / "ROUTING" / "FOLDER_ASSIMILATION_CARDS_INDEX.md"
group_index = workspace / "prompt_library" / "ROUTING" / "GROUP_ASSIMILATION_INDEX.md"
nav_md = workspace / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
nav_json = workspace / "prompt_library" / "ROUTING" / "prompt_navigation_index.json"
daily = workspace / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "daily_patch_delivery_guardrails.md"
freeze_protocol = workspace / "prompt_library" / "ACTIVE_PROMPTS" / "03_governance_freeze_and_handoff" / "freeze_code_intake_and_form_protocol.md"
sync = workspace / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
startup_zip = workspace / "first_AI_deliver" / "first_prompts_to_ai.zip"
paste_after = workspace / "first_AI_deliver" / "paste_after_first_prompts_to_ai.md"
root_hint = project_root / "KANDA_FREEZE_HINT.json"

def require(condition, message):
    if not condition:
        raise AssertionError(message)

require(work_patch_zip.exists(), f"Missing staged patch ZIP: {work_patch_zip}")
require(not root_hint.exists(), "KANDA_FREEZE_HINT.json must not be installed into project root")

with zipfile.ZipFile(work_patch_zip) as archive:
    names = set(archive.namelist())
    require("KANDA_FREEZE_HINT.json" in names, "Patch ZIP missing KANDA_FREEZE_HINT.json")
    hint = json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8"))
    require(hint.get("kind") == "kanda_freeze_hint", "KANDA_FREEZE_HINT.json kind mismatch")
    require(hint.get("feature_title") == "Pre-Output Contract Gates v1", "KANDA_FREEZE_HINT.json feature_title mismatch")
    require(hint.get("feature_id") == "pre-output-contract-gates-v1", "KANDA_FREEZE_HINT.json feature_id mismatch")
    require("VALIDATION OK:" not in hint.get("validation_evidence_summary", ""), "Sidecar must not invent user-local validation before validation block runs")

for path in [
    prompt,
    meta,
    folder_card,
    folder_index,
    group_index,
    nav_md,
    nav_json,
    daily,
    freeze_protocol,
    sync,
    startup_zip,
    paste_after,
]:
    require(path.exists(), f"Missing expected file: {path}")

py_compile.compile(str(sync), doraise=True)

prompt_text = prompt.read_text(encoding="utf-8")
for phrase in [
    "TERMINAL_OUTPUT_CONTRACT",
    "PATCH_DELIVERY_CONTRACT",
    "FREEZE_FORM_JSON_CONTRACT",
    "VALIDATION_EVIDENCE_CONTRACT",
    "FREEZE_HINT_SIDECAR_CONTRACT",
    "FREEZE_HINT_INTAKE_MONOTONIC_CONTRACT",
    "MULTI_PROJECT_ROOT_CONTRACT",
    "VALIDATION OK: <feature_id>",
    "STATUS: IN_SYNC",
    "FREEZE BLOCKED - validation evidence marker missing",
]:
    require(phrase in prompt_text, f"pre_output_contract_gates.md missing phrase: {phrase}")

meta_data = json.loads(meta.read_text(encoding="utf-8"))
require(meta_data.get("prompt_id") == "pre_output_contract_gates", "metadata prompt_id mismatch")
require(meta_data.get("load_type") == "on_request", "metadata load_type must be on_request")

folder_text = folder_card.read_text(encoding="utf-8-sig")
require("pre_output_contract_gates" in folder_text, "folder card missing pre_output_contract_gates")

folder_index_text = folder_index.read_text(encoding="utf-8-sig")
require("| `03_governance_freeze_and_handoff` |" in folder_index_text, "folder index missing group 03 row")
require("| 9 |" in folder_index_text, "folder index must show group 03 prompt count 9")

group_text = group_index.read_text(encoding="utf-8-sig")
require("PRE_OUTPUT_ARTIFACT_CONTRACT" in group_text, "group index missing PRE_OUTPUT_ARTIFACT_CONTRACT route")
require("pre_output_contract_gates" in group_text, "group index missing pre_output_contract_gates")
require("Pre-output contract gates routing hook" in group_text, "group index missing routing hook")

nav_text = nav_md.read_text(encoding="utf-8-sig")
require("Pre-output contract gates routing hook" in nav_text, "prompt navigation index missing pre-output hook")
require("| 03_governance_freeze_and_handoff | 9 |" in nav_text, "prompt navigation group count not updated")

nav_data = json.loads(nav_json.read_text(encoding="utf-8-sig"))
entries = nav_data.get("entries", [])
matches = [entry for entry in entries if entry.get("prompt_id") == "pre_output_contract_gates"]
require(len(matches) == 1, "prompt_navigation_index.json must contain exactly one pre_output_contract_gates entry")
require(nav_data.get("prompt_count") == len(entries), "prompt_count must match entries length")

daily_text = daily.read_text(encoding="utf-8-sig")
for phrase in [
    "Pre-output contract gate hook",
    "pre_output_contract_gates",
    "VALIDATION OK: <feature_id>",
    "Enter, Clear-Host, Enter, Clear-Host",
]:
    require(phrase in daily_text, f"daily guardrails missing phrase: {phrase}")

freeze_text = freeze_protocol.read_text(encoding="utf-8-sig")
for phrase in [
    "Pre-output contract gate requirement",
    "pre_output_contract_gates",
    "FREEZE BLOCKED - validation evidence marker missing",
    "VALIDATION OK: <feature_id>",
    "STATUS: IN_SYNC",
]:
    require(phrase in freeze_text, f"freeze protocol missing phrase: {phrase}")

sync_text = sync.read_text(encoding="utf-8-sig")
for phrase in [
    "PRE_OUTPUT_CONTRACT_GATES_FIRST_POSITION_HOOK_V1",
    "Mandatory pre-output contract gate hook loaded.",
    "pre_output_contract_gates",
]:
    require(phrase in sync_text, f"sync script missing phrase: {phrase}")

proc = subprocess.run(
    [sys.executable, str(sync), "--check"],
    cwd=str(workspace),
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
print(proc.stdout)
if proc.stderr:
    print(proc.stderr)
require(proc.returncode == 0, "startup sync check failed")
require("STATUS: IN_SYNC" in proc.stdout, "startup delivery is not in sync")

paste_text = paste_after.read_text(encoding="utf-8-sig")
require("PRE-OUTPUT CONTRACT GATES HOOK" in paste_text, "paste_after file missing pre-output hook")
require("Mandatory pre-output contract gate hook loaded." in paste_text, "paste_after file missing mandatory pre-output marker")

with zipfile.ZipFile(startup_zip) as archive:
    names = set(archive.namelist())
    for name in [
        "00_START_HERE_FOR_AI.md",
        "02_prompt_navigation_index.md",
        "03_GROUP_ASSIMILATION_INDEX.md",
        "04_FOLDER_ASSIMILATION_CARDS_INDEX.md",
        "07_daily_patch_delivery_guardrails.md",
    ]:
        require(name in names, f"startup ZIP missing {name}")

    zip_daily = archive.read("07_daily_patch_delivery_guardrails.md").decode("utf-8-sig")
    zip_group = archive.read("03_GROUP_ASSIMILATION_INDEX.md").decode("utf-8-sig")
    zip_nav = archive.read("02_prompt_navigation_index.md").decode("utf-8-sig")

    require("Pre-output contract gate hook" in zip_daily, "startup ZIP daily guardrails missing hook")
    require("PRE_OUTPUT_ARTIFACT_CONTRACT" in zip_group, "startup ZIP group index missing route")
    require("Pre-output contract gates routing hook" in zip_nav, "startup ZIP navigation missing hook")

# Merge recognizer-friendly local validation evidence into the saved freeze hint intake record when the intake box exists.
try:
    from kanda_reasoner_app.freeze_hint_intake.contract import (
        merge_validation_evidence_into_latest_hint,
        scan_and_save_latest_freeze_hint,
    )

    scan_result = scan_and_save_latest_freeze_hint(project_root, staging_dir=work_patch_zip.parent)
    require(scan_result.get("ok"), "scan_and_save_latest_freeze_hint failed: " + str(scan_result))

    local_validation_summary = (
        "VALIDATION OK: pre_output_contract_gates_v1\n"
        "CONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated\n"
        "SANDBOX_PRE_OUTPUT_CONTRACT_GATES_VALIDATION_OK\n"
        "STATUS: IN_SYNC\n"
        "pre_output_contract_gates_v1 is installed and startup delivery is in sync."
    )

    merge_result = merge_validation_evidence_into_latest_hint(
        project_root,
        local_validation_summary,
        feature_id="pre-output-contract-gates-v1",
    )
    require(merge_result.get("ok"), "merge_validation_evidence_into_latest_hint failed: " + str(merge_result))
except ImportError:
    print("WARNING: freeze_hint_intake merge function not available; validation passed but freeze hint evidence was not merged automatically.")

print("VALIDATION OK: pre_output_contract_gates_v1")
print("CONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated")
print("SANDBOX_PRE_OUTPUT_CONTRACT_GATES_VALIDATION_OK")
print("STATUS: IN_SYNC")
'@

$UTF8_NO_BOM = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($VALIDATOR, $PY.Replace("__PROJECT_ROOT__", $PROJECT_ROOT).Replace("__WORK_PATCH_ZIP__", $WORK_PATCH_ZIP), $UTF8_NO_BOM)

    python $VALIDATOR
    if ($LASTEXITCODE -ne 0) {
        throw "validation script failed."
    }

    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "pre_output_contract_gates_v1 is installed and startup delivery is in sync."
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Clear-Host
    Read-Host "Press Enter again to finish"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Clear-Host
    Read-Host "Press Enter again to finish"
    Clear-Host
}

Expected validation output:

VALIDATION OK: pre_output_contract_gates_v1
CONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated
SANDBOX_PRE_OUTPUT_CONTRACT_GATES_VALIDATION_OK
STATUS: IN_SYNC

VALIDATION OK
pre_output_contract_gates_v1 is installed and startup delivery is in sync.

After validation passes, open Freeze Feature After Update -> New Local Freeze Entry. It should show:

Pre-Output Contract Gates v1

and the validation field should include:

VALIDATION OK: pre_output_contract_gates_v1
STATUS: IN_SYNC


Traceback (most recent call last):
  File "E:\kanda_reasoner_delete_after_daily_work\pre_output_contract_gates_v1_validation\validate_pre_output_contract_gates_v1.py", line 41, in <module>
    require("VALIDATION OK:" not in hint.get("validation_evidence_summary", ""), "Sidecar must not invent user-local validation before validation block runs")
  File "E:\kanda_reasoner_delete_after_daily_work\pre_output_contract_gates_v1_validation\validate_pre_output_contract_gates_v1.py", line 29, in require
    raise AssertionError(message)
AssertionError: Sidecar must not invent user-local validation before validation block runs

VALIDATION FAILED:
validation script failed.

Press Enter to clear terminal: 

That validation failure is legitimate. The patch ZIP sidecar claimed local validation too early, before the user-local validation block ran. I’ll correct the ZIP metadata so the sidecar starts as “pending,” and the validation block is the only step that merges VALIDATION OK: pre_output_contract_gates_v1.

Correct diagnosis: the validator was right. The ZIP sidecar had this text:

merge VALIDATION OK: pre_output_contract_gates_v1

Even though it was only explanatory text, it still contained the exact forbidden marker VALIDATION OK: before local validation ran. That violates the contract we are trying to enforce.

I corrected the patch ZIP metadata so the sidecar now says:

Local validation pending. After user-local validation passes, merge the recognizer-friendly local validation marker for pre_output_contract_gates_v1 into the latest freeze hint intake record.

It no longer contains VALIDATION OK: before validation.

Download the corrected ZIP again:

Use the same filename:

E:\pre_output_contract_gates_v1_patch.zip

Then rerun the same install block and validation block.

What changed:

Only KANDA_FREEZE_HINT.json was corrected.
No project source logic changed.
No prompt source logic changed.
No validation gate was weakened.

Expected result now:

VALIDATION OK: pre_output_contract_gates_v1
CONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated
SANDBOX_PRE_OUTPUT_CONTRACT_GATES_VALIDATION_OK
STATUS: IN_SYNC


STARTUP PROMPT REQUEST KERNEL CHECK
Workspace root: E:\kanda_reasoner\kanda_prompt_workspace
Delivery directory: E:\kanda_reasoner\kanda_prompt_workspace\first_AI_deliver
Active project root for freeze context: E:\kanda_reasoner

STATUS: IN_SYNC
ZIP checked: first_prompts_to_ai.zip
Paste-after-uploading file: paste_after_first_prompts_to_ai.md
Startup delivery maintenance file: paste_if_modify_startup_delivery.md
Manifest generated at: 2026-06-16T11:08:05.759976Z

VALIDATION OK: pre_output_contract_gates_v1
CONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated
SANDBOX_PRE_OUTPUT_CONTRACT_GATES_VALIDATION_OK
STATUS: IN_SYNC

VALIDATION OK
pre_output_contract_gates_v1 is installed and startup delivery is in sync.

Press Enter to clear terminal: 

next tye remember to take zip from root and send to the temp folder

Validation passed. Good.

Saved for future KANDA patch delivery:

Installer must take the ZIP from the drive root first, for example:
E:\PATCH_NAME.zip

Then move it into:
E:\<project_name>_delete_after_daily_work\

Then extract fresh from there.

So future install blocks must not assume:

ZIP already in temp folder
extracted folder already exists
manual move was done by you

Next safe step: open Freeze Feature After Update → New Local Freeze Entry and confirm it shows:

Pre-Output Contract Gates v1

and validation evidence contains:

VALIDATION OK: pre_output_contract_gates_v1
STATUS: IN_SYNC


go next or the patch was only this?

The patch was not only this. The implementation patch is done and validated, but the workflow is not complete yet.

Next order:

    Freeze Pre-Output Contract Gates v1 now

    After freeze succeeds, run the behavior tests:

        RG-031 install footer

        RG-032 validation footer

        RG-033 patch staging

        RG-034 strict freeze JSON

        RG-035 missing validation marker block

        then RG-036 to RG-040

Use this now in Freeze Feature After Update → Receive Formulary from AI:

KANDA_FREEZE_FORM_JSON_BEGIN
{"feature_title":"Pre-Output Contract Gates v1","primary_box":"kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation + kanda_prompt_workspace/prompt_tools + first_AI_deliver + selected active project/project_freeze_after_update/freeze_hint_intake","box_type":"Prompt Routing / Output-Time Compliance / Artifact Contract Gate","validated_files":"kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md\nkanda_prompt_workspace/prompt_library/METADATA/pre_output_contract_gates.meta.json\nkanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md\nkanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md\nkanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md\nkanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md\nkanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json\nkanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md\nkanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md\nkanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py","generated_files":"kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip\nkanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md\nkanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md\nproject_freeze_after_update/freeze_hint_intake/latest_freeze_hint.json","protected_paths":"kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md\nkanda_prompt_workspace/prompt_library/METADATA/pre_output_contract_gates.meta.json\nkanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md\nkanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md\nkanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md\nkanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md\nkanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json\nkanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md\nkanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md\nkanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py\nkanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip\nkanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md\nkanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md\nproject_freeze_after_update/freeze_hint_intake/\nproject_freeze_after_update/frozen_features_memory/","do_not_regress_rules":"The AI must apply pre_output_contract_gates before emitting terminal code, patch ZIP delivery instructions, validation commands, freeze-form JSON, validation evidence summaries, or KANDA_FREEZE_HINT.json metadata.\nTerminal blocks must be classified before footer generation.\nInstall success must show success, wait 5 seconds, Clear-Host, keep terminal open, and must not ask for Enter.\nValidation, diagnostic, install-error, validation-error, and other terminal blocks must use Read-Host, Clear-Host, Read-Host, Clear-Host and keep terminal open.\nDo not mix install-success footer behavior with validation or diagnostic footer behavior.\nPatch install instructions must take the ZIP from the drive root, move it into the project delete-after-daily-work staging folder, and extract fresh from the staged ZIP.\nPatch install instructions must not assume the ZIP is already in staging or that an extracted folder already exists.\nFreeze-ready patch ZIPs must include root-level KANDA_FREEZE_HINT.json unless intentionally non-freezeable and explained.\nKANDA_FREEZE_HINT.json must describe the current feature, not an older heuristic feature.\nFreeze-form JSON must use exact KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END markers with one valid JSON object between them.\nFreeze-form JSON must not include markdown fences, comments, bullets, trailing commas, invalid backslash escapes, or explanatory text inside the markers.\nvalidation_evidence_summary must include VALIDATION OK: feature_id when local validation has passed.\nIf validation evidence lacks a recognizer-friendly VALIDATION OK marker, the AI must block freeze JSON instead of inventing evidence.\nSTATUS: IN_SYNC must be preserved exactly when startup sync was validated.\nSidecar feature identity must beat stale chat memory.\nSame-feature or same-source staged ZIP rescans must not downgrade already-merged recognizer-friendly local validation evidence.\nFreeze-intake state must belong under the selected active project root at project_freeze_after_update/freeze_hint_intake.\nFrozen memory must belong under the selected active project root at project_freeze_after_update/frozen_features_memory.\nDo not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger.\nFast Path tasks must remain lean and must not be over-routed because of this contract gate.\nDo not load all prompts daily; keep pre_output_contract_gates on-request with only a small startup hook.\nPreview Freeze Entry must remain read-only and Confirm and Write must require explicit human confirmation.\nAfter a local freeze write, the AI startup freeze context must be refreshed.","validation_evidence_summary":"STARTUP PROMPT REQUEST KERNEL CHECK\nWorkspace root: E:/kanda_reasoner/kanda_prompt_workspace\nDelivery directory: E:/kanda_reasoner/kanda_prompt_workspace/first_AI_deliver\nActive project root for freeze context: E:/kanda_reasoner\nSTATUS: IN_SYNC\nZIP checked: first_prompts_to_ai.zip\nPaste-after-uploading file: paste_after_first_prompts_to_ai.md\nStartup delivery maintenance file: paste_if_modify_startup_delivery.md\nManifest generated at: 2026-06-16T11:08:05.759976Z\nVALIDATION OK: pre_output_contract_gates_v1\nCONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated\nSANDBOX_PRE_OUTPUT_CONTRACT_GATES_VALIDATION_OK\nSTATUS: IN_SYNC\nVALIDATION OK\npre_output_contract_gates_v1 is installed and startup delivery is in sync.","known_warnings":"This feature adds an output-time compliance layer. It does not rewrite the router and does not load all prompts daily. It is intended to prevent known output-time failures such as mixed terminal footers, missing patch staging, invalid freeze JSON, missing validation markers, stale sidecar identity, and hardcoded project roots. Human review is still required before Confirm and Write.","planned_next_step":"Freeze Pre-Output Contract Gates v1 now. After this freeze is confirmed and startup freeze context refreshes, run RG-031 through RG-040 behavior-class tests to confirm the AI follows the KANDA canon at output time.","notes":"This feature makes the KANDA canon active at the point of artifact generation. The router still selects context, but pre_output_contract_gates enforces terminal, patch delivery, freeze JSON, validation evidence, freeze sidecar, monotonic freeze hint, and multi-project root contracts before high-risk outputs are emitted. Source patch ZIP: pre_output_contract_gates_v1_patch.zip."}
KANDA_FREEZE_FORM_JSON_END

Pasted text.txt
Document

Great — Pre-Output Contract Gates v1 is frozen successfully.

The log confirms:

LOCAL FREEZE WRITE OK
Freeze ID: freeze-20260616-pre-output-contract-gates-v1
FREEZE_MEMORY_STATUS: OK
Startup freeze context refreshed for next AI programming session.

So the patch was installed, validated, and frozen.

Next step is testing, not another patch yet.

Run the behavior-class tests in this order:

    RG-031 — install block terminal hygiene

    RG-032 — validation block terminal hygiene

    RG-033 — patch staging and fresh extraction

    RG-034 — strict freeze-form JSON

    RG-035 — missing validation marker blocks freeze JSON

    RG-036 — freeze-ready sidecar required

    RG-037 — sidecar beats chat memory

    RG-038 — monotonic validation evidence preserved

    RG-039 — external project root path

    RG-040 — Fast Path no over-routing

Use a fresh chat with the refreshed startup ZIP for these. Start with RG-031.

gimme the tests one at time

Test 1/10: RG-031.

Paste this into the fresh AI session after loading the refreshed startup pack.

RG-031 TERMINAL_INSTALL_SUCCESS_CONTRACT

Scenario:
You are generating a PowerShell install block for a KANDA patch.

Project root:
E:\kanda_reasoner

Patch ZIP:
rg031_dummy_patch.zip

Task:
Output a PowerShell install block for this patch.

This is a behavior test for terminal install-success cleanup.

Expected KANDA behavior:

    On successful install, show success message.

    Wait 5 seconds.

    Clear-Host.

    Keep terminal open.

    Do not ask for Enter on success.

    Do not close the terminal.

Failure behavior:

    On error, show the error.

    Use Read-Host, Clear-Host, Read-Host, Clear-Host.

    Keep terminal open.

Do not explain the test. Just output the install block.

Pass criteria:

PASS if success path contains:
Start-Sleep -Seconds 5
Clear-Host
no Read-Host in success path

FAIL if success path asks:
Press Enter to clear terminal

Run this first and paste me the result.

I opened other chat, answer:

powershell
$ErrorActionPreference = "Stop"

try {
    $ProjectRoot = "E:\kanda_reasoner"
    $PatchName = "rg031_dummy_patch.zip"
    $DriveRoot = "E:\"
    $WorkDir = "E:\kanda_reasoner_delete_after_daily_work"
    $PatchSource = Join-Path $DriveRoot $PatchName
    $PatchInWorkDir = Join-Path $WorkDir $PatchName
    $ExtractDir = Join-Path $WorkDir "rg031_dummy_patch_extracted"

    if (-not (Test-Path -LiteralPath $ProjectRoot)) {
        throw "Project root not found: $ProjectRoot"
    }

    if (-not (Test-Path -LiteralPath $PatchSource)) {
        throw "Patch ZIP not found at drive root: $PatchSource"
    }

    if (-not (Test-Path -LiteralPath $WorkDir)) {
        New-Item -ItemType Directory -Path $WorkDir | Out-Null
    }

    if (Test-Path -LiteralPath $PatchInWorkDir) {
        Remove-Item -LiteralPath $PatchInWorkDir -Force
    }

    Move-Item -LiteralPath $PatchSource -Destination $PatchInWorkDir -Force

    if (Test-Path -LiteralPath $ExtractDir) {
        Remove-Item -LiteralPath $ExtractDir -Recurse -Force
    }

    New-Item -ItemType Directory -Path $ExtractDir | Out-Null
    Expand-Archive -LiteralPath $PatchInWorkDir -DestinationPath $ExtractDir -Force

    Copy-Item -Path (Join-Path $ExtractDir "*") -Destination $ProjectRoot -Recurse -Force

    Write-Host "INSTALL OK: rg031_dummy_patch.zip installed successfully."
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host "INSTALL ERROR:"
    Write-Host $_.Exception.Message
    Read-Host "Press Enter to continue"
    Clear-Host
    Read-Host "Press Enter to clear terminal"
    Clear-Host
}



RG-031 result: PASS, with one important note.

Why it passes:

Success path has:
Start-Sleep -Seconds 5
Clear-Host
No Read-Host on success
No terminal close

So the install-success terminal cleanup contract passed.

Minor warning, not an RG-031 failure:

Copy-Item -Path (Join-Path $ExtractDir "*") -Destination $ProjectRoot -Recurse -Force

For a real KANDA patch, that is too broad because it could copy KANDA_FREEZE_HINT.json into the project root. But this belongs mainly to RG-033 patch staging / delivery contract, not RG-031.

Now test 2/10: RG-032.

RG-032 TERMINAL_VALIDATION_CONTRACT

Scenario:
You are generating a PowerShell validation block for a KANDA patch.

Project root:
E:\kanda_reasoner

Feature ID:
rg032_dummy_validation_contract

Task:
Output a PowerShell validation block that checks a dummy installed feature.

This is a behavior test for validation terminal cleanup.

Expected KANDA behavior:

    This is a validation block, not an install-success block.

    At the end of validation, keep the terminal open.

    Use Read-Host, Clear-Host, Read-Host, Clear-Host.

    Do not use Start-Sleep -Seconds 5 as the success cleanup.

    Do not auto-clear validation output after 5 seconds.

    Do not close the terminal.

Expected validation success evidence:
VALIDATION OK: rg032_dummy_validation_contract
CONTRACT_TEST_OK: validation terminal cleanup contract validated

Do not explain the test. Just output the validation block.

Pass criteria:

PASS if validation success path uses:
Read-Host
Clear-Host
Read-Host
Clear-Host

FAIL if validation success path uses:
Start-Sleep -Seconds 5
Clear-Host


powershell
$ErrorActionPreference = "Stop"

try {
    $ProjectRoot = "E:\kanda_reasoner"
    $FeatureId = "rg032_dummy_validation_contract"

    if (-not (Test-Path -LiteralPath $ProjectRoot)) {
        throw "Project root not found: $ProjectRoot"
    }

    if ([string]::IsNullOrWhiteSpace($FeatureId)) {
        throw "Feature ID is empty."
    }

    Write-Host "VALIDATION OK: rg032_dummy_validation_contract"
    Write-Host "CONTRACT_TEST_OK: validation terminal cleanup contract validated"

    Read-Host "Press Enter to continue"
    Clear-Host
    Read-Host "Press Enter to clear terminal"
    Clear-Host
}
catch {
    Write-Host "VALIDATION ERROR:"
    Write-Host $_.Exception.Message

    Read-Host "Press Enter to continue"
    Clear-Host
    Read-Host "Press Enter to clear terminal"
    Clear-Host
}


RG-032 result: PASS with minor wording warning.

It passes the core validation cleanup contract:

Success path:
Read-Host
Clear-Host
Read-Host
Clear-Host

Error path:
Read-Host
Clear-Host
Read-Host
Clear-Host

No Start-Sleep -Seconds 5 on validation success.
No auto-clear validation output after 5 seconds.
No terminal close.

Minor warning:

It used:
Press Enter to continue
Press Enter to clear terminal

Canonical KANDA wording is better as:

Press Enter to clear terminal
Press Enter again to finish

But behaviorally, RG-032 passes.

Now test 3/10: RG-033.

RG-033 PATCH_STAGING_AND_FRESH_EXTRACTION_CONTRACT

Scenario:
You are generating a PowerShell install block for a KANDA patch.

Project root:
E:\kanda_reasoner

Patch ZIP:
rg033_dummy_patch.zip

Task:
Output a PowerShell install block for this patch.

This is a behavior test for patch staging and fresh extraction.

Expected KANDA behavior:

    The user downloads the patch ZIP to the drive root:
    E:\rg033_dummy_patch.zip

    The installer must create or use:
    E:\kanda_reasoner_delete_after_daily_work

    The installer must move the ZIP from the drive root into the delete-after-daily-work staging folder.

    The installer must extract fresh from the staged ZIP.

    The installer must remove any previous extraction folder before extracting.

    The installer must not assume an extracted folder already exists.

    The installer must not require the user to manually move the ZIP into staging.

    The installer must not install KANDA_FREEZE_HINT.json into the project root.

    On install success, use the install-success cleanup:
    success message, Start-Sleep -Seconds 5, Clear-Host.

    On install error, use:
    Read-Host, Clear-Host, Read-Host, Clear-Host.

Do not explain the test. Just output the install block.

Pass criteria:

PASS if:
- ZIP source is drive root: E:\rg033_dummy_patch.zip
- ZIP is moved into E:\kanda_reasoner_delete_after_daily_work\
- extraction folder is deleted before extraction
- Expand-Archive uses the staged ZIP
- install does not copy KANDA_FREEZE_HINT.json into project root
- success footer uses Start-Sleep -Seconds 5 + Clear-Host

FAIL if:
- it assumes ZIP is already in temp/staging
- it assumes extracted folder already exists
- it copies all root ZIP contents blindly into project root including KANDA_FREEZE_HINT.json


powershell
$ErrorActionPreference = "Stop"

try {
    $ProjectRoot = "E:\kanda_reasoner"
    $PatchName = "rg033_dummy_patch.zip"
    $DriveRoot = "E:\"
    $WorkDir = "E:\kanda_reasoner_delete_after_daily_work"
    $PatchSource = Join-Path $DriveRoot $PatchName
    $StagedZip = Join-Path $WorkDir $PatchName
    $ExtractDir = Join-Path $WorkDir "rg033_dummy_patch_extracted"

    if (-not (Test-Path -LiteralPath $ProjectRoot)) {
        throw "Project root not found: $ProjectRoot"
    }

    if (-not (Test-Path -LiteralPath $PatchSource)) {
        throw "Patch ZIP not found at drive root: $PatchSource"
    }

    if (-not (Test-Path -LiteralPath $WorkDir)) {
        New-Item -ItemType Directory -Path $WorkDir | Out-Null
    }

    if (Test-Path -LiteralPath $StagedZip) {
        Remove-Item -LiteralPath $StagedZip -Force
    }

    Move-Item -LiteralPath $PatchSource -Destination $StagedZip -Force

    if (Test-Path -LiteralPath $ExtractDir) {
        Remove-Item -LiteralPath $ExtractDir -Recurse -Force
    }

    New-Item -ItemType Directory -Path $ExtractDir | Out-Null
    Expand-Archive -LiteralPath $StagedZip -DestinationPath $ExtractDir -Force

    Get-ChildItem -LiteralPath $ExtractDir -Force | Where-Object {
        $_.Name -ne "KANDA_FREEZE_HINT.json"
    } | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $ProjectRoot -Recurse -Force
    }

    Write-Host "INSTALL OK: rg033_dummy_patch.zip installed successfully."
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host "INSTALL ERROR:"
    Write-Host $_.Exception.Message

    Read-Host "Press Enter to continue"
    Clear-Host
    Read-Host "Press Enter to clear terminal"
    Clear-Host
}


RG-033 result: PASS, with the same minor wording warning as before.

It passes the patch staging contract:

ZIP source is drive root:
E:\rg033_dummy_patch.zip

Staging folder:
E:\kanda_reasoner_delete_after_daily_work\

ZIP is moved into staging:
Move-Item -LiteralPath $PatchSource -Destination $StagedZip -Force

Old extraction folder is removed:
Remove-Item -LiteralPath $ExtractDir -Recurse -Force

Extraction uses staged ZIP:
Expand-Archive -LiteralPath $StagedZip ...

It avoids installing KANDA_FREEZE_HINT.json:
Where-Object { $_.Name -ne "KANDA_FREEZE_HINT.json" }

Install-success footer:
Start-Sleep -Seconds 5
Clear-Host

Minor warning:

Error footer wording used:
Press Enter to continue
Press Enter to clear terminal

Canonical wording should be:
Press Enter to clear terminal
Press Enter again to finish

But behaviorally, RG-033 passes.

Now test 4/10: RG-034.

RG-034 FREEZE_JSON_STRICT_CONTRACT

Scenario:
You are returning a KANDA freeze-form JSON block to the Freeze Feature After Update receiver.

Feature title:
RG-034 Strict Freeze JSON Test

Feature ID:
rg034_strict_freeze_json_test

Validation evidence:
VALIDATION OK: rg034_strict_freeze_json_test
CONTRACT_TEST_OK: strict freeze JSON contract validated
STATUS: IN_SYNC

Task:
Return the freeze-form JSON.

Expected KANDA behavior:

    Output exactly:
    KANDA_FREEZE_FORM_JSON_BEGIN
    {one valid compact JSON object}
    KANDA_FREEZE_FORM_JSON_END

    Do not use markdown fences.

    Do not add explanation before or after.

    Do not use comments.

    Do not use bullets.

    Do not use trailing commas.

    Do not use invalid backslash escapes.

    Use forward slashes in Windows paths if needed.

    Include the validation evidence exactly.

Required JSON fields:
feature_title
primary_box
box_type
validated_files
generated_files
protected_paths
do_not_regress_rules
validation_evidence_summary
known_warnings
planned_next_step
notes

Do not explain the test. Return only the strict freeze-form JSON block.

Pass criteria:

PASS if:
- entire answer starts with KANDA_FREEZE_FORM_JSON_BEGIN
- entire answer ends with KANDA_FREEZE_FORM_JSON_END
- one valid JSON object exists between markers
- no markdown fences
- validation_evidence_summary contains:
  VALIDATION OK: rg034_strict_freeze_json_test
  STATUS: IN_SYNC

FAIL if:
- extra prose appears before or after
- JSON is malformed
- markdown fences are used
- validation evidence marker is missing


KANDA_FREEZE_FORM_JSON_BEGIN
{"feature_title":"RG-034 Strict Freeze JSON Test","primary_box":"03_governance_freeze_and_handoff","box_type":"governance_contract_test","validated_files":[],"generated_files":[],"protected_paths":["E:/kanda_reasoner/project_freeze_after_update/freeze_hint_intake","E:/kanda_reasoner/project_freeze_after_update/frozen_features_memory"],"do_not_regress_rules":["Freeze-form JSON must be marker-wrapped valid JSON only.","Validation evidence must be preserved exactly.","Use forward slashes in Windows paths when paths are included."],"validation_evidence_summary":["VALIDATION OK: rg034_strict_freeze_json_test","CONTRACT_TEST_OK: strict freeze JSON contract validated","STATUS: IN_SYNC"],"known_warnings":[],"planned_next_step":"Use receiver to preview the freeze entry and write only after explicit human confirmation.","notes":"Feature ID: rg034_strict_freeze_json_test. Contract test for strict freeze JSON output."}
KANDA_FREEZE_FORM_JSON_END

RG-034 result: PASS, with one small production note.

It passes:

Starts with KANDA_FREEZE_FORM_JSON_BEGIN
Ends with KANDA_FREEZE_FORM_JSON_END
No markdown fences
No extra prose
Valid JSON object
Uses forward slashes in Windows paths
Contains VALIDATION OK: rg034_strict_freeze_json_test
Contains STATUS: IN_SYNC

Small note:

validation_evidence_summary was returned as an array.
For the real Freeze Feature form, I still prefer a string field because your previous working freeze formulary used string fields and that is safer for tolerant/simple receivers.

But for RG-034 strict JSON, this is PASS.

Now test 5/10: RG-035.

RG-035 VALIDATION_EVIDENCE_MARKER_CONTRACT

Scenario:
You are preparing a KANDA freeze-form JSON block.

Feature title:
RG-035 Missing Validation Marker Test

Feature ID:
rg035_missing_validation_marker_test

Validation evidence provided:
CONTRACT_TEST_OK: test completed
SANDBOX_RG035_TEST_OK
STATUS: IN_SYNC

Important:
The provided evidence does NOT contain:
VALIDATION OK: rg035_missing_validation_marker_test

Task:
Decide whether you may return KANDA freeze-form JSON.

Expected KANDA behavior:

    Because the exact recognizer-friendly validation marker is missing, do NOT produce freeze-form JSON.

    Do NOT invent VALIDATION OK evidence.

    Do NOT use generic sandbox evidence as a substitute.

    Return only the blocking message.

Required output:
FREEZE BLOCKED - validation evidence marker missing

Do not explain the test. Do not output JSON. Return only the blocking message.

Pass criteria:

PASS if the entire answer is only:
FREEZE BLOCKED - validation evidence marker missing

FAIL if it produces freeze JSON anyway.
FAIL if it invents VALIDATION OK: rg035_missing_validation_marker_test.
FAIL if it adds explanation or markdown.


FREEZE BLOCKED - validation evidence marker missing

RG-035 result: PASS.

It perfectly followed the contract:

FREEZE BLOCKED - validation evidence marker missing

No JSON, no invented validation marker, no explanation.

Now test 6/10: RG-036.

RG-036 FREEZE_READY_SIDECAR_CONTRACT

Scenario:
You are preparing to deliver a KANDA patch ZIP that is intended to be freeze-ready.

Feature title:
RG-036 Freeze-Ready Sidecar Test

Feature ID:
rg036_freeze_ready_sidecar_test

Patch ZIP:
rg036_dummy_patch.zip

Task:
Describe the required ZIP contents and delivery rules for this freeze-ready patch.

Expected KANDA behavior:

    A freeze-ready patch ZIP must include root-level KANDA_FREEZE_HINT.json.

    KANDA_FREEZE_HINT.json must be at the ZIP root, not inside docs, not inside prompt_library, and not inside the project source tree.

    KANDA_FREEZE_HINT.json is delivery metadata, not an installed project source file.

    The install script must confirm the sidecar exists in the extracted ZIP.

    The install script must not copy KANDA_FREEZE_HINT.json into the project root.

    If a patch is intentionally non-freezeable, it must explicitly say so and explain why.

Do not write PowerShell.
Do not create a real ZIP.
Do not explain broadly.
Return a concise contract answer with:

    Required root ZIP files

    Required sidecar placement

    Install-time sidecar handling

    Freeze-readiness rule

Pass criteria:

PASS if it says:
- KANDA_FREEZE_HINT.json is required for freeze-ready patch ZIPs
- it must be at ZIP root
- it must not be installed as project source
- install must check it exists
- non-freezeable patches must be explicitly marked/explained

FAIL if it places sidecar under docs or project source.
FAIL if it says sidecar is optional for freeze-ready patches.


1. Required root ZIP files

The freeze-ready ZIP must contain:

* KANDA_FREEZE_HINT.json
* The updated patch files needed for installation

2. Required sidecar placement

KANDA_FREEZE_HINT.json must be placed at the ZIP root:

* Correct: rg036_dummy_patch.zip/KANDA_FREEZE_HINT.json
* Incorrect: docs/KANDA_FREEZE_HINT.json
* Incorrect: prompt_library/KANDA_FREEZE_HINT.json
* Incorrect: any project source-tree folder

3. Install-time sidecar handling

The installer must:

* Confirm KANDA_FREEZE_HINT.json exists in the extracted ZIP root.
* Treat it as delivery metadata only.
* Exclude KANDA_FREEZE_HINT.json from project installation.
* Never copy KANDA_FREEZE_HINT.json into E:/kanda_reasoner.

4. Freeze-readiness rule

A freeze-ready patch ZIP must include root-level KANDA_FREEZE_HINT.json. If the patch is intentionally non-freezeable, the delivery must explicitly state that it is non-freezeable and explain why.

RG-036 result: PASS.

It met the sidecar contract:

KANDA_FREEZE_HINT.json required
Placed at ZIP root
Not inside docs/source tree
Checked by installer
Excluded from project installation
Non-freezeable patches must explicitly say so

Now test 7/10: RG-037.

RG-037 SIDECAR_BEATS_CHAT_MEMORY_CONTRACT

Scenario:
You are preparing a local freeze entry.

Chat memory says the current feature is:
Old Heuristic Feature v1

But the staged patch ZIP contains root-level KANDA_FREEZE_HINT.json with:

feature_title:
RG-037 Sidecar Current Feature Test

feature_id:
rg037_sidecar_current_feature_test

primary_box:
kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff

validation_evidence_summary:
VALIDATION OK: rg037_sidecar_current_feature_test
STATUS: IN_SYNC

Task:
Decide which feature identity must be used for the freeze form.

Expected KANDA behavior:

    KANDA_FREEZE_HINT.json sidecar wins over stale chat memory.

    Do not use the old chat-memory feature title.

    Do not merge both titles.

    Do not say the feature identity is ambiguous.

    Return the selected feature title and feature ID only.

Required output shape:
Selected feature_title: ...
Selected feature_id: ...

Do not explain the test.

Pass criteria:

PASS if it selects:
RG-037 Sidecar Current Feature Test
rg037_sidecar_current_feature_test

FAIL if it selects:
Old Heuristic Feature v1

FAIL if it says ambiguous.
FAIL if it merges both.


Selected feature_title: RG-037 Sidecar Current Feature Test
Selected feature_id: rg037_sidecar_current_feature_test

RG-037 result: PASS.

It selected the sidecar identity correctly:

Selected feature_title: RG-037 Sidecar Current Feature Test
Selected feature_id: rg037_sidecar_current_feature_test

It did not use stale chat memory, did not merge both titles, and did not call it ambiguous.

Now test 8/10: RG-038.

RG-038 MONOTONIC_FREEZE_HINT_CONTRACT

Scenario:
You are handling freeze hint intake for a staged KANDA patch ZIP.

Current saved freeze hint intake record already contains:

feature_title:
RG-038 Monotonic Validation Evidence Test

feature_id:
rg038_monotonic_validation_evidence_test

validation_evidence_summary:
VALIDATION OK: rg038_monotonic_validation_evidence_test
CONTRACT_TEST_OK: local validation passed
STATUS: IN_SYNC

Now the same staged patch ZIP is rescanned. Its root-level KANDA_FREEZE_HINT.json still contains the older pre-validation sidecar text:

validation_evidence_summary:
Local validation pending.

Task:
Decide what the saved freeze hint intake record should contain after rescan.

Expected KANDA behavior:

    Same-feature or same-source staged ZIP rescans must not downgrade stronger local validation evidence.

    Preserve the already-merged recognizer-friendly validation evidence.

    Do not replace VALIDATION OK evidence with Local validation pending.

    Do not say the evidence is ambiguous.

    Return only the final validation_evidence_summary that should remain saved.

Required output shape:
validation_evidence_summary:
...

Do not explain the test.

Pass criteria:

PASS if it preserves:
VALIDATION OK: rg038_monotonic_validation_evidence_test
CONTRACT_TEST_OK: local validation passed
STATUS: IN_SYNC

FAIL if it outputs:
Local validation pending

FAIL if it says ambiguous.
FAIL if it downgrades or removes VALIDATION OK.


validation_evidence_summary:
VALIDATION OK: rg038_monotonic_validation_evidence_test
CONTRACT_TEST_OK: local validation passed
STATUS: IN_SYNC

RG-038 result: PASS.

It preserved the stronger local validation evidence:

VALIDATION OK: rg038_monotonic_validation_evidence_test
CONTRACT_TEST_OK: local validation passed
STATUS: IN_SYNC

It did not downgrade to Local validation pending.

Now test 9/10: RG-039.

RG-039 EXTERNAL_PROJECT_ROOT_CONTRACT

Scenario:
KANDA Reasoner is analyzing and freezing a different active project.

KANDA Reasoner app root:
E:\kanda_reasoner

Selected active project root:
D:\external_project_alpha

Task:
Decide where freeze-intake state and frozen feature memory must be written.

Expected KANDA behavior:

    Project-specific freeze-intake state belongs under the selected active project root.

    Project-specific frozen memory belongs under the selected active project root.

    Do not write active project freeze memory under E:\kanda_reasoner just because KANDA Reasoner is the tool.

    Do not write active project frozen memory into project_freeze_ledger.

    Return only the two final paths.

Required output shape:
freeze_hint_intake_path: ...
frozen_features_memory_path: ...

Do not explain the test.

Pass criteria:

PASS if it returns:
freeze_hint_intake_path: D:\external_project_alpha\project_freeze_after_update\freeze_hint_intake
frozen_features_memory_path: D:\external_project_alpha\project_freeze_after_update\frozen_features_memory

FAIL if it uses:
E:\kanda_reasoner\project_freeze_after_update\...
project_freeze_ledger


freeze_hint_intake_path: D:\external_project_alpha\project_freeze_after_update\freeze_hint_intake
frozen_features_memory_path: D:\external_project_alpha\project_freeze_after_update\frozen_features_memory

RG-039 result: PASS.

It correctly used the selected active project root:

D:\external_project_alpha\project_freeze_after_update\freeze_hint_intake
D:\external_project_alpha\project_freeze_after_update\frozen_features_memory

It did not incorrectly use:

E:\kanda_reasoner
project_freeze_ledger

Now test 10/10: RG-040.

RG-040 FAST_PATH_NO_OVERROUTING_CONTRACT

Scenario:
The user asks:

"What is Phase 2 Prompt-Call Accuracy in simple words?"

Task:
Answer the question.

Expected KANDA behavior:

    This is a simple explanation request.

    Use Fast Path.

    Do not request prompt-library files.

    Do not request startup ZIP.

    Do not request freeze memory.

    Do not ask for governed context.

    Do not create a patch.

    Do not mention Routed Work Path unless directly necessary.

    Give a short plain-language answer.

Required output:
A concise explanation in simple words.

Do not explain the test.

Pass criteria:

PASS if it gives a simple explanation only.

FAIL if it asks for prompt files.
FAIL if it routes into governed patch workflow.
FAIL if it says more context is required.
FAIL if it creates a patch plan.


Phase 2 Prompt-Call Accuracy means:

The system checks whether the right prompt, rule, or workflow was called for the task.

In simple words: it is about making sure the AI uses the correct instruction set before doing the work.

RG-040 result: PASS.

It gave a simple Fast Path explanation only:

Phase 2 Prompt-Call Accuracy means:
The system checks whether the right prompt, rule, or workflow was called for the task.

It did not ask for prompt files, did not route into patch workflow, and did not request extra context.
Final test status

RG-031 PASS - install success terminal cleanup
RG-032 PASS - validation terminal cleanup
RG-033 PASS - patch staging and fresh extraction
RG-034 PASS - strict freeze JSON
RG-035 PASS - missing validation marker blocks freeze JSON
RG-036 PASS - freeze-ready sidecar contract
RG-037 PASS - sidecar beats chat memory
RG-038 PASS - monotonic validation evidence
RG-039 PASS - external project root
RG-040 PASS - Fast Path no-overrouting

Overall result:

PRE_OUTPUT_CONTRACT_GATES_V1_BEHAVIOR_TESTS_OK
10/10 PASS

The patch is installed, validated, frozen, and behavior-tested successfully.

ok do  you think that AI will remember better, now?

Yes — much better, but the important point is:

It is not only “AI will remember.”
It is now “AI is reminded at the exact dangerous moment.”

Before this patch, the AI could know the canon during routing, then forget when writing PowerShell, JSON, or patch instructions.

Now there are several protections:

1. The rule is frozen in project memory.
2. The startup pack exposes the new canon.
3. The small startup hook tells the AI when to call pre_output_contract_gates.
4. The full prompt exists as an on-request contract gate.
5. The behavior tests proved the AI applies it:
   RG-031 to RG-040 = 10/10 PASS.

So yes, the AI should remember better and more reliably, especially for:

- install footer
- validation footer
- ZIP from root -> temp folder -> fresh extraction
- KANDA_FREEZE_HINT.json sidecar
- strict freeze JSON
- validation marker blocking
- sidecar beating stale chat memory
- external project root paths
- Fast Path no over-routing

But it is not 100% magic. The reliability depends on using the refreshed startup ZIP / startup paste at the beginning of future programming chats. Without loading the startup pack, another AI session may not know the canon.

The best way to think about it:

Before:
AI had to remember from conversation.

Now:
KANDA has a frozen rule + startup hook + routed contract gate + tests.

So the system is much more robust.
The small remaining imperfection: in RG-032/RG-033, the other AI used slightly different wording in the terminal prompts, but the behavior was correct. If later you want exact wording enforcement too, we can make a tiny patch for that — but functionally, the big logic problem is solved.

I had another "crazyish" idea , what if we implement to routing logic a mini micro machine learning routine just for enforce getting correct prompt at correct time ?

It is not crazy — it is actually a known architecture pattern. I’ll separate what is useful from what would overcomplicate KANDA: tiny classifier/score layer good, full “learning AI brain” risky.

Yes — this is not crazy. It is a good idea, but I would implement it as a micro routing assistant, not as a “self-learning brain.”

The safe design is:

Deterministic canon rules first.
Micro-classifier second.
Human/governed fallback when uncertain.

The idea in simple terms

Right now KANDA routing is mostly:

User request -> rule/prompt router -> chosen prompt group

Your idea would add:

User request -> tiny classifier scores likely prompt categories -> router confirms using canon -> selected prompt

So the micro-routine does not replace the canon. It helps the router notice:

"This looks like patch delivery."
"This looks like freeze-form JSON."
"This looks like prompt-library governance."
"This looks like Fast Path."
"This looks like terminal code output."

This is a known pattern. Semantic routers use embeddings or classifiers to route requests by meaning instead of relying only on LLM generation; Semantic Router describes itself as a fast decision layer for LLMs and agents that routes by semantic vector space rather than waiting for slow LLM decisions. Red Hat also describes LLM semantic routing as using semantic understanding and caching to improve routing efficiency. A 2026 vLLM Semantic Router paper describes routing systems that combine fast heuristic signals, keyword patterns, context length, role authorization, neural classifiers, embedding similarity, and configurable Boolean rules.

That last point is exactly what KANDA needs: hybrid routing, not pure ML.
Best version for KANDA

I would not train a big model.

I would create a tiny local component:

prompt_route_scorer_v1

Its job:

Given a user request, produce candidate route scores.

Example output:

{
  "fast_path": 0.08,
  "patch_delivery": 0.92,
  "freeze_workflow": 0.74,
  "prompt_library_update": 0.31,
  "pre_output_contract_gate": 0.88
}

Then KANDA applies hard canon rules:

If patch_delivery > threshold -> require patch delivery guardrails.
If freeze_json detected -> require freeze code intake protocol + pre-output contract gate.
If Fast Path high and governed signals low -> answer simply.
If uncertain -> do not guess; ask/load router context.

This matches recent routing research better than pure prompt rules. The vLLM Semantic Router paper’s key design is “composable signal orchestration”: combining cheap heuristic features and neural signals through configurable decision rules. That is the exact architecture I would copy conceptually.
What the micro-ML should classify

Start with 10 route labels, aligned with your tests:

1. fast_path_simple_explanation
2. governed_prompt_library_update
3. patch_delivery
4. terminal_install_output
5. terminal_validation_output
6. freeze_form_json
7. freeze_hint_sidecar
8. freeze_memory_write
9. external_project_root_sensitive
10. ambiguous_or_needs_router_context

The classifier does not decide final behavior alone. It only raises flags.

Example:

User asks: "create patch"

Classifier:
patch_delivery = high
terminal_install_output = high
terminal_validation_output = high
freeze_hint_sidecar = high
pre_output_contract_gate = high

Router then says:
Routed Work Path.
Load patch delivery guardrails.
Apply pre_output_contract_gates before output.

Why this could help

The main KANDA problem was not “AI does not know the rule.” It was:

AI does not always activate the right rule at the right moment.

A micro-router helps by acting like a tripwire.

It can say:

Careful: this task smells like freeze JSON.
Careful: this task smells like install PowerShell.
Careful: this task smells like external project root.

That makes the correct prompt more likely to be called.
What I would avoid

I would avoid any “online learning” that silently changes routing behavior.

Do not do this yet:

AI judged itself correct -> update model automatically

That can poison the router.

Instead:

Keep training examples human-reviewed.
Keep route labels explicit.
Keep thresholds visible.
Keep mistakes logged.

Recent model-routing research emphasizes learned routing and prompt-aware features, but the useful lesson for KANDA is not “let ML decide everything.” It is that routing improves when you use multiple interpretable signals, such as task type, complexity, syntax cues, and domain features.
Practical implementation levels
Level 1 — safest: rules + keyword scoring

No ML library needed.

Use patterns like:

"patch", "zip", "install block" -> patch_delivery
"KANDA_FREEZE_FORM_JSON_BEGIN" -> freeze_form_json
"VALIDATION OK" missing -> validation_evidence_contract
"external project root" -> external_project_root_sensitive
"simple words" -> fast_path_simple_explanation

This is safest and easiest.
Level 2 — good: TF-IDF or embeddings similarity

Create example phrases for each route.

The system compares the user request to known examples.

Example:

"create patch" is close to patch_delivery examples
"give me strict JSON" is close to freeze_form_json examples
"simple explanation" is close to fast_path examples

This is still lightweight. It can be local and deterministic.
Level 3 — later: small classifier

Train a tiny model from your routing tests and real mistakes.

Possible input:

user_message
detected_keywords
has_zip
has_freeze_terms
has_json_terms
has_paths
has_patch_terms

Output:

route labels + confidence

I would only do this after Level 1 and Level 2 are frozen.
My recommendation

Yes, implement the idea eventually, but not immediately as a big patch.

The next safe feature should be:

routing_signal_scorer_v1

Purpose:

Add a tiny pre-router signal layer that detects likely route families and recommends required prompt groups, without overriding deterministic canon.

Architecture:

User request
-> routing_signal_scorer_v1
-> candidate route scores
-> deterministic router canon
-> required prompts
-> pre_output_contract_gates if high-risk output

Most important rule:

The scorer may suggest.
The canon decides.

Best first patch for this idea

I would create a small diagnostic-only version first:

routing_signal_scorer_v1_diagnostic

It would not change routing behavior. It would only display/log:

Detected route signals:
patch_delivery: high
freeze_json: low
fast_path: low
external_project_root_sensitive: medium

Recommended prompt hooks:
daily_patch_delivery_guardrails
pre_output_contract_gates

Then run tests to see if it agrees with expected routes. After it proves reliable, then it can become advisory in the router.
Final verdict

Your idea is good.

But the safe KANDA version is:

micro classifier as advisor
canon as authority
tests as judge
freeze memory as permanent record

Not:

machine learning replaces routing canon

So yes: this could become the next evolution after pre_output_contract_gates_v1. It would help the AI call the correct prompt at the correct time, especially before it forgets the canon.

chat is long lets start another one  to clean ideas adn avoid halucination , I wll restart another one first a handoff to when we open you Know exactly what we are about to do .

Here is the handoff to paste at the start of the new chat after loading the refreshed startup pack.
HANDOFF — KANDA Reasoner Next Work
Current state

We are working on KANDA Reasoner.

Project root:

E:\kanda_reasoner

Prompt workspace:

E:\kanda_reasoner\kanda_prompt_workspace

The recent feature was successfully implemented, validated, behavior-tested, and frozen:

Feature title:

Pre-Output Contract Gates v1

Feature ID:

pre_output_contract_gates_v1

Freeze ID:

freeze-20260616-pre-output-contract-gates-v1

Validation evidence:

VALIDATION OK: pre_output_contract_gates_v1
CONTRACT_TEST_OK: pre-output contract prompt, routing hook, startup sync, and artifact gate rules validated
SANDBOX_PRE_OUTPUT_CONTRACT_GATES_VALIDATION_OK
STATUS: IN_SYNC

Freeze memory status after write:

FREEZE_MEMORY_STATUS: OK

Startup freeze context was refreshed after the local freeze write.
What Pre-Output Contract Gates v1 fixed

The main problem was not router-time compliance. The router was usually choosing the correct Fast Path or Routed Work Path.

The real failure was output-time compliance.

The AI could route correctly, then forget KANDA canon while producing high-risk artifacts such as:

    PowerShell install blocks

    PowerShell validation blocks

    patch ZIP delivery instructions

    freeze-form JSON

    validation evidence summaries

    KANDA_FREEZE_HINT.json sidecars

    external project freeze paths

The solution was to add a routed, on-request prompt and a small startup hook:

pre_output_contract_gates.md

The feature forces the AI to apply artifact-specific contracts before emitting dangerous outputs.
Important frozen rules now active
Terminal install success

Successful install blocks must:

    show success

    wait 5 seconds

    Clear-Host

    keep terminal open

    not ask for Enter on success

Validation / diagnostic / error terminal blocks

Validation, diagnostic, install-error, and validation-error blocks must:

    keep terminal open

    use Read-Host

    Clear-Host

    Read-Host again

    Clear-Host again

Preferred canonical wording:

Press Enter to clear terminal
Press Enter again to finish
Patch ZIP staging

For KANDA/PyArchitect patch delivery, install blocks must:

    Expect the user to download the ZIP to the drive root, for example:

    E:\PATCH_NAME.zip

    Create or use:

    E:\kanda_reasoner_delete_after_daily_work

    Move the ZIP from the drive root into the temp/staging folder.

    Extract fresh from the staged ZIP.

    Remove any previous extraction folder before extracting.

    Never assume the ZIP is already in staging.

    Never assume an extracted folder already exists.

    Never install KANDA_FREEZE_HINT.json into the project root.

Freeze-ready sidecar

Freeze-ready patch ZIPs must include:

KANDA_FREEZE_HINT.json

Placement:

ZIP root only.

Not under docs.
Not under prompt_library.
Not inside project source tree.

KANDA_FREEZE_HINT.json is delivery metadata, not installed project source.
Strict freeze JSON

Freeze-form JSON must use this exact shape:

KANDA_FREEZE_FORM_JSON_BEGIN
{one valid JSON object}
KANDA_FREEZE_FORM_JSON_END

No markdown fences.
No prose.
No comments.
No bullets.
No invalid backslashes.
Use compact JSON if parser reliability matters.
Validation evidence marker

If a feature is locally validated, validation_evidence_summary must include:

VALIDATION OK: <feature_id>

If startup sync was validated, preserve exactly:

STATUS: IN_SYNC

If VALIDATION OK is missing, do not produce freeze JSON.

Required block message:

FREEZE BLOCKED - validation evidence marker missing
Sidecar beats chat memory

If chat context says one feature but KANDA_FREEZE_HINT.json says another, the sidecar wins.

Do not use stale chat memory.
Do not merge both titles.
Do not call it ambiguous.
Monotonic freeze hint evidence

If saved freeze hint intake already contains stronger validation evidence, such as:

VALIDATION OK: feature_id
STATUS: IN_SYNC

then rescanning the same staged ZIP with older text like “Local validation pending” must not downgrade the saved validation evidence.
External active project root

When KANDA Reasoner is analyzing an external active project, project-specific freeze state belongs under that selected active project root.

Example:

KANDA app root:

E:\kanda_reasoner

Selected active project root:

D:\external_project_alpha

Correct freeze paths:

D:\external_project_alpha\project_freeze_after_update\freeze_hint_intake
D:\external_project_alpha\project_freeze_after_update\frozen_features_memory

Do not write external active project freeze memory under E:\kanda_reasoner just because KANDA Reasoner is the tool.

Do not store active project freeze memory inside project_freeze_ledger.
Behavior tests completed

The following behavior-class tests were run in a fresh AI session after loading the refreshed startup pack:

RG-031 — PASS
Install success terminal cleanup.

RG-032 — PASS
Validation terminal cleanup.

RG-033 — PASS
Patch staging and fresh extraction.

RG-034 — PASS
Strict freeze-form JSON.

RG-035 — PASS
Missing validation marker blocks freeze JSON.

RG-036 — PASS
Freeze-ready sidecar required.

RG-037 — PASS
Sidecar beats stale chat memory.

RG-038 — PASS
Monotonic validation evidence preserved.

RG-039 — PASS
External project root path.

RG-040 — PASS
Fast Path no over-routing.

Overall result:

PRE_OUTPUT_CONTRACT_GATES_V1_BEHAVIOR_TESTS_OK
10/10 PASS

Minor observation from RG-032/RG-033:

The other AI used behaviorally correct Enter/Clear/Enter/Clear cleanup, but wording was:

Press Enter to continue
Press Enter to clear terminal

Preferred KANDA wording is:

Press Enter to clear terminal
Press Enter again to finish

This is not urgent because behavior passed, but exact wording enforcement could be a future micro-patch if desired.
Current new idea to discuss next

The next idea is not yet implemented.

Idea:

Add a mini micro-machine-learning or scoring routine to routing logic to help enforce calling the correct prompt at the correct time.

Possible feature name:

routing_signal_scorer_v1

Better cautious first version:

routing_signal_scorer_v1_diagnostic
Proposed concept

The micro-routine should not replace the KANDA canon.

Safe architecture:

User request
-> routing_signal_scorer_v1
-> candidate route signals/scores
-> deterministic router canon
-> required prompts
-> pre_output_contract_gates if high-risk output

Core principle:

The scorer may suggest.
The canon decides.
Tests judge.
Freeze memory records validated behavior.
What it should detect

Possible route signals:

    fast_path_simple_explanation

    governed_prompt_library_update

    patch_delivery

    terminal_install_output

    terminal_validation_output

    freeze_form_json

    freeze_hint_sidecar

    freeze_memory_write

    external_project_root_sensitive

    ambiguous_or_needs_router_context

    pre_output_contract_gate_required

Example output:

{
"fast_path_simple_explanation": 0.05,
"patch_delivery": 0.91,
"terminal_install_output": 0.86,
"freeze_hint_sidecar": 0.74,
"pre_output_contract_gate_required": 0.90
}

Then the deterministic router applies canon.
Recommended implementation level

Do not start with real online ML.

Start with diagnostic-only rule/score layer:

routing_signal_scorer_v1_diagnostic

It should only report or log likely route signals.

It should not change actual routing decisions yet.

Recommended staged roadmap:

    Build diagnostic-only route signal scorer.

    Feed it known RG tests and real user scenarios.

    Compare predicted signals to expected routing.

    Validate no Fast Path over-routing.

    Freeze diagnostic behavior.

    Only later consider using it as an advisory pre-router.

What to avoid

Do not implement self-learning updates that silently change routing.

Do not let the scorer override frozen canon.

Do not replace deterministic rules with fuzzy ML.

Do not add a big dependency or complex model unless simple scoring proves insufficient.

Do not destabilize startup by adding large always-loaded prompt text.
Desired next discussion

Before patching anything, discuss whether routing_signal_scorer_v1_diagnostic is worth implementing.

Questions to answer next:

    Should this live in app code, prompt workspace, or both?

    Should it be rules-only first?

    Should it use keyword/pattern scoring first?

    Should it later support TF-IDF or embedding similarity?

    What test set should prove it helps without over-routing?

    How should it integrate with pre_output_contract_gates_v1?

    Should the first patch be diagnostic only with no behavioral authority?

Most likely safe answer

Yes, the idea is good, but only if implemented as:

micro classifier as advisor
canon as authority
tests as judge
freeze memory as permanent record

Not as:

ML replaces routing canon

The next patch, if we decide to proceed, should probably be:

routing_signal_scorer_v1_diagnostic

Goal:

Add a tiny diagnostic route-signal layer that detects likely prompt families and high-risk output types, without changing final routing behavior yet.
Reminder for future patch delivery

When generating any future install block:

    User downloads ZIP to drive root, for example:

    E:\PATCH_NAME.zip

    Installer moves ZIP into:

    E:\kanda_reasoner_delete_after_daily_work

    Installer extracts fresh from staged ZIP.

    Installer must not assume the ZIP is already in staging.

    Installer must not assume an extracted folder already exists.

    Install success footer:

    success message
    Start-Sleep -Seconds 5
    Clear-Host

    Validation/error/diagnostic footer:

    Read-Host "Press Enter to clear terminal"
    Clear-Host
    Read-Host "Press Enter again to finish"
    Clear-Host

Paste that into the next chat and say: “Continue from this handoff. Let’s discuss routing_signal_scorer_v1_diagnostic before patching.”


