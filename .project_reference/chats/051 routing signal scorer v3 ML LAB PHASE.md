ChatGPT

first_prompts_to_ai.zip
Zip Archive
paste_after_first_prompts_to_ai.md
File
read first the filoe.md  only then zip file

I will load the markdown command file first, then inspect the startup ZIP contents in order and report only the startup load check.

STARTUP PACK LOAD CHECK

Files recognized:
0. 00_START_HERE_FOR_AI.md - loaded - Stable AI entrypoint and mandatory startup load-check instruction.

    01_ai_prompt_request_canon.md - loaded - Defines how to request missing prompt groups, folder cards, specialist prompts, and behavior gates.

    02_prompt_navigation_index.md - loaded - Maps task types to prompt groups and specialist prompt candidates.

    03_GROUP_ASSIMILATION_INDEX.md - loaded - Summarizes prompt groups for safe routing before deeper prompt requests.

    04_FOLDER_ASSIMILATION_CARDS_INDEX.md - loaded - Indexes folder cards for folder-level routing and placement boundaries.

    05_start_of_day_master_stack.md - loaded - Defines baseline start-of-day/session startup behavior.

    06_session_start_upload_checklist.md - loaded - Defines startup context requirements before implementation work.

    07_daily_patch_delivery_guardrails.md - loaded - Defines patch delivery staging, root-cleanliness, terminal hygiene, and freeze reminders.

    08_handoff_at_end_of_work.md - loaded - Defines mandatory end-of-work handoff behavior for long governed sessions.

    09_active_project_freeze_context.md - loaded - Provides active project freeze-memory context and freeze-awareness rules.

    README_STARTUP_PROMPT_REQUEST_KERNEL.md - loaded - Explains the upload pack, canonical-source rule, and startup workflow.

    STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json - loaded - Provides build metadata, source mapping, roles, checksums, and generation certificate.

Startup status:
COMPLETE

Routing behavior:
The markdown paste file was read first, then the ZIP was inspected in the required startup order. Startup routing is active: future project tasks should be classified before action, governed work should request the required specialist prompts, folder cards, source files, validation rules, and freeze context as needed, and bypass requests should not override routing, patch-delivery, startup-delivery, or freeze-confirmation safeguards.

Next action:
WAIT_FOR_TASK

kanda_reasoner.zip
Zip Archive
050 routing signal scorer v3 before P8.md
File
zip is our project  and 050 md is you last meeting . Do you see that we must :
first: go to P8 (10 steps more or less to finish machine learning ),
second: after that we will create a strong test lab first to train  ML to perform task flawlessly and after that
improve test lab to work errors to create an  "errrors to not repeat" library

do you see that? 

Yes. I see the roadmap clearly.

The safe sequence is:

    Continue first to P8 only
    The handoff says the P-series is frozen through P7, with P8 - Non-Runtime Pilot Candidate Implementation v1 as the next safe milestone. It also says not to skip P8 governance and not to activate runtime Pilot/Copilot behavior.

    Finish the remaining Pilot/Copilot ML path carefully
    Current confirmed state is P0-P7 frozen, so we are not starting from scratch. The handoff says current count is 8 done, 5 to go, with P8 next.
    Your “10 steps more or less” is directionally right if we include the remaining P-series plus follow-up lab/training infrastructure, but strictly inside the current P-series the handoff says 5 milestones remain after P7.

    After the Pilot/Copilot candidate path, build the strong test lab
    This comes after the non-runtime Pilot candidate is safely defined/implemented enough to be tested. The lab should first be for controlled training/calibration/evaluation: frozen cases, adversarial cases, regression cases, boundary cases, and “match before disagree” checks.

    Only after the test lab exists, build the “errors to not repeat” library
    That should be a second layer on top of the lab: recurring failures, bad patch patterns, stale freeze sidecar errors, wrong installer templates, routing mistakes, prompt-loading leakage, governance bypass attempts, etc., become permanent regression/canon entries.

So the correct logic line is:

P8 and remaining Pilot/Copilot non-runtime milestones -> controlled test lab -> training/calibration/evaluation discipline -> error canonization / errors-to-not-repeat library.

Important boundary: P8 is not live Pilot, not Copilot, not runtime routing, not prompt loading, not persistence, not batch mode, and not training from outputs. It is only the first non-runtime candidate implementation scaffold.

are u secure to continue?

I’ll verify the latest handoff state before saying yes, because continuing safely depends on the exact frozen milestone and next permitted step.

Yes — secure to continue, with one strict boundary.

Current verified state: P0 through P7 are frozen, with FREEZE_MEMORY_STATUS: OK, and the next safe milestone is P8 - Non-Runtime Pilot Candidate Implementation v1. The handoff explicitly lists P0-P7 frozen and says the current count is 8 done, 5 to go.

So:

Secure to continue: YES.
Secure next step: P8 only.
Not secure: runtime Pilot, Copilot, prompt loading, persistence, batch mode, training-data use, gold/registry mutation, route authority, or automatic maturity jump.

Also, for any patch I deliver now, I must obey the newer installer canon: detect DRIVE_ROOT from $PROJECT_ROOT, look first for the ZIP at the project drive root, stage into <project>_delete_after_daily_work, delete the root-drive ZIP after staging, and extract only from the staged ZIP. This rule is explicitly in the startup/pre-output contract gate.

I agree with you "Not secure: runtime Pilot, Copilot, prompt loading, persistence, batch mode, training-data use, gold/registry mutation, route authority, or automatic maturity jump."

that's why next step after finishing creation of  ML logic is create the  lab test , warn me before starting coding test lab

Agreed and saved.

Before I start any test-lab coding, I will explicitly warn you and separate it from the current ML/Pilot-Copilot work.

Current sequence stays:

    Finish the remaining non-runtime ML/Pilot-Copilot logic first.

    Stop and warn you before starting the test lab.

    Only after your confirmation, begin test-lab design/coding.

    After the lab is established, move to the “errors to not repeat” library.


Not secure: runtime Pilot, Copilot, prompt loading, persistence, batch mode, training-data use, gold/registry mutation, route authority, or automatic maturity jump. = correct to  after labtest creation we will exaustively test machine learning for router prompt  logic 

Correct. Saved.

The intended sequence is now:

    Finish the remaining non-runtime ML/Pilot-Copilot logic.

    Before any test-lab coding, I warn you and get confirmation.

    Create the test lab under governed, non-runtime constraints.

    After the lab exists, use it to exhaustively test the machine-learning logic against router prompt logic.

    Only after that, build the “errors to not repeat” library from recurring failures.

The unsafe boundary remains unchanged: no runtime Pilot, Copilot, prompt loading, persistence, batch mode, training-data use, gold/registry mutation, route authority, or automatic maturity jump unless a later governed scope explicitly approves it.

0018b Box Architecture Canon v1.0 prompt.md
File
for your afirmative  "The unsafe boundary remains unchanged: no runtime Pilot, Copilot, prompt loading, persistence, batch mode, training-data use, gold/registry mutation, route authority, or automatic maturity jump unless a later governed scope explicitly approves it."  we can create a logic code key "turn on" turn off" for  pilot/copilot logic in order to , in case of field test turn on, in case of  imature  ML turn off, when  ML is mature , turn on definitively. It shoul be easy to achieve  thanks to box logic .

Yes — the idea is good, and Box Architecture is exactly the right way to do it.

But I would refine the wording:

Not just a simple turn_on = True / False.

Better: create a dedicated Pilot/Copilot Activation Gate Box or Maturity Gate Box later, with explicit states:

    disabled

    lab_test_only

    field_test_limited

    mature_enabled

    locked_off

This box would own the activation decision and expose a public contract. Other boxes would only ask: “is Pilot allowed in this context?” They would not directly enable themselves. That matches the Box Architecture rule that each box owns one responsibility, exposes a public contract, declares dependencies, and must have fallback behavior if disabled.

Important boundary:

For now, we do not implement that activation key yet.

Why? Because before the lab proves maturity, even an activation switch can become dangerous if it accidentally grants runtime authority too early.

So the safer roadmap is:

    Finish current non-runtime ML/Pilot-Copilot logic.

    Warn you before starting the test lab.

    Build the lab.

    Exhaustively test ML against router prompt logic.

    Only after maturity evidence, design the Activation Gate Box.

    Then maybe allow field_test_limited.

    Only much later, after strict gates, allow mature_enabled.

The key rule:

The activation switch should not be inside Pilot or Copilot.
It should be its own isolated box, probably a controller/registry-style gate, so Pilot/Copilot can be disabled without breaking the rest of the app.

So yes: easy to achieve thanks to Box Architecture — but only safe if it is created as a governed activation/maturity gate, not as a casual boolean inside the ML logic.

great go P8

I’ll proceed with P8 only, under the current frozen boundary: non-runtime, no prompt loading, no persistence, no batch mode, no training-data use, no gold/registry mutation, and no route authority. I’ll also apply the root-drive ZIP staging installer canon in the delivery block.

P8 scaffold is taking shape as a static candidate record only. I also preserved your future activation-key idea as blocked in P8 and deferred to a later Activation Gate Box after lab testing/maturity evidence.

P8 patch is ready.

Primary box: routing_signal_scorer/adviser_offline/transition_design
Box type: data/module box
Single responsibility: static non-runtime Pilot candidate record only
Supporting touches: README, box manifest, focused tests, boundary whitelist tests
Boundary: no runtime Pilot, no Copilot, no prompt loading, no persistence, no batch mode, no training-data use, no field-test activation, no definitive enablement, no route authority. This follows the Box Architecture rule that each feature remains isolated behind its own responsibility and contract boundary.

Download the patch:

SHA-256:

3d4e980dca1bee05ba5264369cf2ed9fcc454a16eaa0123b9994a3085eedc7c4

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1
CONTRACT_TEST_OK: P8 Non-Runtime Pilot Candidate Implementation v1, immutable governed P8 boundary after P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no Copilot implementation, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_CANDIDATE_IMPLEMENTATION_V1_VALIDATION_OK

Progress:

Bridge roadmap: 18 done, 0 to go.

Router canon layer:
RG-PILOT-000 done and frozen.

Installer delivery canon:
KANDA Patch Delivery Root-Drive ZIP Staging Canon v1 done and frozen.

Pilot/Copilot P-series before P8:
P0 through P7 done and frozen.
8 done, 5 to go.

Current stage:
P8 - Non-Runtime Pilot Candidate Implementation v1.

After local validation and freeze:
Pilot/Copilot P-series becomes 9 done, 4 to go.

Next safe milestone after P8 freeze:
P9 - Non-Runtime Pilot Candidate Contract Conformance v1.

Save the ZIP first here:

E:\routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1 installed."
    Write-Host "P8 static non-runtime Pilot candidate record installed."
    Write-Host "No callable Pilot, Copilot implementation, route comparison execution, prompt loading, persistence, provider calls, embeddings, training-data use, batch mode, field-test activation, definitive enablement, Limited Shadow Runtime, or runtime authority were added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation.py",
        "tests\test_routing_signal_scorer_v3_pilot_implementation_gate_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_review_evidence_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_simulation_skeleton_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_gold_router_reproduction_harness_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_disagreement_taxonomy_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_io_contract_validator_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_scope_charter_entry_gate_design.py",
        "tests\test_rg_pilot_000_pilot_copilot_phase0_router_canon.py",
        "tests\test_routing_signal_scorer_v3_post_adviser_pilot_copilot_handoff_closure_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py",
        "tests\test_freeze_hint_autofill_state_machine.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1"
    Write-Host "CONTRACT_TEST_OK: P8 Non-Runtime Pilot Candidate Implementation v1, immutable governed P8 boundary after P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no Copilot implementation, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_CANDIDATE_IMPLEMENTATION_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 Non-Runtime Pilot Candidate Implementation v1

Do not proceed to P9 until the freeze output shows:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK


Pasted text.txt
Document
go next

P8 freeze output is good: it shows LOCAL FREEZE WRITE OK and FREEZE_MEMORY_STATUS: OK, so P9 is the next safe milestone. I’ll create P9 only: contract-conformance logic as a non-runtime/static conformance record, not live validation or Pilot execution.

P8 freeze is confirmed: LOCAL FREEZE WRITE OK and FREEZE_MEMORY_STATUS: OK, so P9 was safe to create.

P9 patch is ready.

Primary box: routing_signal_scorer/adviser_offline/transition_design
Box type: data/module box
Single responsibility: static non-runtime Pilot candidate contract-conformance record only
Boundary: no live validator, no input processing, no output generation, no payload transformation, no callable Pilot, no Copilot, no route comparison execution, no prompt loading, no persistence, no batch mode, no training-data use, no field-test activation, no definitive enablement, and no route authority. This follows the Box Architecture rule that a patch targets one primary box and exposes isolated contract-based logic.

Download:

SHA-256:

53a882df5fe842bab3f6e6a9ec7a00f1fdc7a16194bf2a2131133996cd565c69

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1
CONTRACT_TEST_OK: P9 Non-Runtime Pilot Candidate Contract Conformance v1, immutable governed P9 boundary after P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, static conformance declaration only, no live validator, no input processing, no output generation, no payload transformation, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no Copilot implementation, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_CANDIDATE_CONTRACT_CONFORMANCE_V1_VALIDATION_OK

Progress:

Bridge roadmap: 18 done, 0 to go.

Router canon layer:
RG-PILOT-000 done and frozen.

Installer delivery canon:
KANDA Patch Delivery Root-Drive ZIP Staging Canon v1 done and frozen.

Pilot/Copilot P-series before P9:
P0 through P8 done and frozen.
9 done, 4 to go.

Current stage:
P9 - Non-Runtime Pilot Candidate Contract Conformance v1.

After local validation and freeze:
Pilot/Copilot P-series becomes 10 done, 3 to go.

Next safe milestone after P9 freeze:
P10 - Non-Runtime Pilot Candidate Readiness Gate v1.

Save the ZIP first here:

E:\routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_contract_conformance.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_contract_conformance_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_contract_conformance.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_contract_conformance_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1 installed."
    Write-Host "P9 static non-runtime Pilot candidate contract-conformance record installed."
    Write-Host "No live validator, input processing, output generation, payload transformation, callable Pilot, Copilot implementation, route comparison execution, prompt loading, persistence, provider calls, embeddings, training-data use, batch mode, field-test activation, definitive enablement, Limited Shadow Runtime, or runtime authority were added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation.py",
        "tests\test_routing_signal_scorer_v3_pilot_implementation_gate_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_review_evidence_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_simulation_skeleton_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_gold_router_reproduction_harness_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_disagreement_taxonomy_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_io_contract_validator_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_scope_charter_entry_gate_design.py",
        "tests\test_rg_pilot_000_pilot_copilot_phase0_router_canon.py",
        "tests\test_routing_signal_scorer_v3_post_adviser_pilot_copilot_handoff_closure_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py",
        "tests\test_freeze_hint_autofill_state_machine.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1"
    Write-Host "CONTRACT_TEST_OK: P9 Non-Runtime Pilot Candidate Contract Conformance v1, immutable governed P9 boundary after P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, static conformance declaration only, no live validator, no input processing, no output generation, no payload transformation, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no Copilot implementation, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_CANDIDATE_CONTRACT_CONFORMANCE_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 Non-Runtime Pilot Candidate Contract Conformance v1

Do not proceed to P10 until the freeze output shows:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK


Pasted text.txt
Document

You pasted the freeze report text into PowerShell. That text is not code, so PowerShell tried to execute lines like LOCAL FREEZE WRITE OK, Feature title:, protected_paths:, etc., and produced many errors.

Good news: this does not necessarily damage the project. It mostly means PowerShell received plain text instead of commands.

The important part: the pasted log still contains the real P8 freeze evidence:

    LOCAL FREEZE WRITE OK

    Freeze ID: freeze-20260619-routing-signal-scorer-v3-non-runtime-pilot-candidate-implementation-v1

    FREEZE_MEMORY_STATUS: OK

So P8 remains frozen.

But this output is not P9 validation/freeze evidence. It is the old P8 freeze report. Do not go to P10 yet.

Next action:

    Open a clean PowerShell prompt.

    Run the P9 install block I gave.

    Run the P9 validation block.

    Freeze as:

Routing Signal Scorer v3 Non-Runtime Pilot Candidate Contract Conformance v1

Then send me the P9 output showing:

VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

Only after that we proceed to P10.

Pasted text.txt
Document
go next

P9 freeze output is valid: it shows the P9 freeze write and FREEZE_MEMORY_STATUS: OK, so I can move to P10. I’ll create P10 only as a non-runtime readiness gate record, not an activation gate, field-test switch, runtime gate, or Copilot start.

P9 freeze is confirmed: LOCAL FREEZE WRITE OK and FREEZE_MEMORY_STATUS: OK, so P10 was safe to create.

P10 patch is ready.

Primary box: routing_signal_scorer/adviser_offline/transition_design
Box type: data/module box
Single responsibility: static non-runtime Pilot candidate readiness gate record only
Boundary: no live gate evaluation, no readiness approval, no review packet builder, no test-lab coding, no runtime Pilot, no Copilot, no prompt loading, no persistence, no batch mode, no training-data use, no field-test activation, no definitive enablement, and no route authority.

Download:

SHA-256:

f8af22430315519ce588b38f7f244c1f15f3f0ce25a4ef0215fcd763c2b81953

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1
CONTRACT_TEST_OK: P10 Non-Runtime Pilot Candidate Readiness Gate v1, immutable governed P10 boundary after P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, static readiness gate criteria declaration only, no live gate evaluation, no readiness approval, no review packet builder, no lab-test coding, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no Copilot implementation, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_CANDIDATE_READINESS_GATE_V1_VALIDATION_OK

Progress:

Pilot/Copilot P-series before P10:
P0 through P9 done and frozen.
10 done, 3 to go.

Current stage:
P10 - Non-Runtime Pilot Candidate Readiness Gate v1.

After local validation and freeze:
Pilot/Copilot P-series becomes 11 done, 2 to go.

Next safe milestone after P10 freeze:
P11 - Non-Runtime Pilot Candidate Review Evidence Packet v1.

Save the ZIP first here:

E:\routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_readiness_gate.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_readiness_gate_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_readiness_gate.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_readiness_gate_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1 installed."
    Write-Host "P10 static non-runtime Pilot candidate readiness gate record installed."
    Write-Host "No live gate evaluation, readiness approval, review packet builder, lab-test coding, callable Pilot, Copilot implementation, route comparison execution, prompt loading, persistence, provider calls, embeddings, training-data use, batch mode, field-test activation, definitive enablement, Limited Shadow Runtime, or runtime authority were added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation.py",
        "tests\test_routing_signal_scorer_v3_pilot_implementation_gate_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_review_evidence_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_simulation_skeleton_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_gold_router_reproduction_harness_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_disagreement_taxonomy_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_io_contract_validator_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_scope_charter_entry_gate_design.py",
        "tests\test_rg_pilot_000_pilot_copilot_phase0_router_canon.py",
        "tests\test_routing_signal_scorer_v3_post_adviser_pilot_copilot_handoff_closure_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py",
        "tests\test_freeze_hint_autofill_state_machine.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1"
    Write-Host "CONTRACT_TEST_OK: P10 Non-Runtime Pilot Candidate Readiness Gate v1, immutable governed P10 boundary after P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, static readiness gate criteria declaration only, no live gate evaluation, no readiness approval, no review packet builder, no lab-test coding, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no Copilot implementation, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_CANDIDATE_READINESS_GATE_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 Non-Runtime Pilot Candidate Readiness Gate v1

Do not proceed to P11 until the freeze output shows:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK


Pasted text.txt
Document
continue

P10 freeze is valid: the uploaded output shows the P10 freeze write and FREEZE_MEMORY_STATUS: OK, so the next safe step is P11 only. I’ll keep it non-runtime: static review-evidence packet declaration, not a builder, not persistence, and not test-lab coding.

P10 freeze is confirmed: LOCAL FREEZE WRITE OK and FREEZE_MEMORY_STATUS: OK, so P11 was safe to create.

P11 patch is ready.

Primary box: routing_signal_scorer/adviser_offline/transition_design
Box type: data/module box
Single responsibility: static non-runtime Pilot candidate review-evidence packet shape only
Boundary: no evidence collection, no packet builder, no packet population, no persistence, no report writer, no review queue writer, no human decision recording, no readiness approval, no test-lab coding, no runtime Pilot, no Copilot, no prompt loading, no batch mode, no training-data use, no field-test activation, no definitive enablement, and no route authority. This keeps the one-primary-box discipline required by Box Architecture.

Download:

SHA-256:

0af45aa26a5b775b39452bf16cf8dee6fcce524824e882f19f954b06f7a4045d

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1
CONTRACT_TEST_OK: P11 Non-Runtime Pilot Candidate Review Evidence Packet v1, immutable governed P11 boundary after P10/P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, static review evidence packet shape declaration only, no evidence collection, no packet builder, no packet population, no packet persistence, no report writer, no review queue writer, no human decision recording, no readiness approval, no lab-test coding, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no Copilot implementation, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P10/P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_CANDIDATE_REVIEW_EVIDENCE_PACKET_V1_VALIDATION_OK

Progress:

Pilot/Copilot P-series before P11:
P0 through P10 done and frozen.
11 done, 2 to go.

Current stage:
P11 - Non-Runtime Pilot Candidate Review Evidence Packet v1.

After local validation and freeze:
Pilot/Copilot P-series becomes 12 done, 1 to go.

Next safe milestone after P11 freeze:
P12 - Pilot Phase Closure / Copilot Boundary Entry Gate v1.

Save the ZIP first here:

E:\routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_review_evidence_packet.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_review_evidence_packet_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_review_evidence_packet.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_review_evidence_packet_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1 installed."
    Write-Host "P11 static non-runtime Pilot candidate review-evidence packet shape installed."
    Write-Host "No evidence collection, packet builder, packet population, packet persistence, report writer, review queue writer, human decision recording, readiness approval, lab-test coding, callable Pilot, Copilot implementation, route comparison execution, prompt loading, persistence, provider calls, embeddings, training-data use, batch mode, field-test activation, definitive enablement, Limited Shadow Runtime, or runtime authority were added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation.py",
        "tests\test_routing_signal_scorer_v3_pilot_implementation_gate_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_review_evidence_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_simulation_skeleton_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_gold_router_reproduction_harness_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_disagreement_taxonomy_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_io_contract_validator_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_scope_charter_entry_gate_design.py",
        "tests\test_rg_pilot_000_pilot_copilot_phase0_router_canon.py",
        "tests\test_routing_signal_scorer_v3_post_adviser_pilot_copilot_handoff_closure_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py",
        "tests\test_freeze_hint_autofill_state_machine.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    python -m py_compile "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_candidate_review_evidence_packet.py"
    if ($LASTEXITCODE -ne 0) {
        throw "py_compile failed for P11 module"
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1"
    Write-Host "CONTRACT_TEST_OK: P11 Non-Runtime Pilot Candidate Review Evidence Packet v1, immutable governed P11 boundary after P10/P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, static review evidence packet shape declaration only, no evidence collection, no packet builder, no packet population, no packet persistence, no report writer, no review queue writer, no human decision recording, no readiness approval, no lab-test coding, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no Copilot implementation, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P10/P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_CANDIDATE_REVIEW_EVIDENCE_PACKET_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 Non-Runtime Pilot Candidate Review Evidence Packet v1

Do not proceed to P12 until the freeze output shows:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK


Pasted text.txt
Document

P11 freeze is valid: the uploaded output shows P11 LOCAL FREEZE WRITE OK and FREEZE_MEMORY_STATUS: OK, so P12 is now the next safe step. I’ll keep P12 as closure/entry-gate metadata only, not Copilot implementation and not test-lab coding.

P11 freeze is confirmed: the uploaded output shows LOCAL FREEZE WRITE OK for P11 and FREEZE_MEMORY_STATUS: OK, so P12 was safe to create.

P12 patch is ready.

Primary box: routing_signal_scorer/adviser_offline/transition_design
Box type: data/module box
Single responsibility: static non-runtime Pilot phase closure / Copilot boundary entry-gate declaration only
Boundary: no closure execution, no Copilot boundary approval, no Copilot scope design, no Copilot implementation, no test-lab design/coding, no activation key, no maturity on/off switch, no ML maturity claim, no runtime Pilot, no prompt loading, no persistence, no batch mode, no training-data use, no field-test activation, and no route authority.

Download:

SHA-256:

2f8855061bdbfe16bd6f8cd2238369b7b5bb13686d3f6330b4f426f3c8b68af4

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_v1
CONTRACT_TEST_OK: P12 Non-Runtime Pilot Phase Closure / Copilot Boundary Entry Gate v1, immutable governed P12 boundary after P11/P10/P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, static closure and entry-gate declaration only, no closure execution, no Copilot boundary approval, no Copilot scope design, no Copilot implementation, no test-lab design or coding, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, no activation key, no maturity on/off switch, no ML maturity claim, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P11/P10/P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_PHASE_CLOSURE_COPILOT_BOUNDARY_ENTRY_GATE_V1_VALIDATION_OK

Progress:

Pilot/Copilot P-series before P12:
P0 through P11 done and frozen.
12 done, 1 to go.

Current stage:
P12 - Non-Runtime Pilot Phase Closure / Copilot Boundary Entry Gate v1.

After local validation and freeze:
Pilot/Copilot P-series becomes 13 done, 0 to go.

Next safe behavior after P12 freeze:
STOP. Warn user before any test-lab design or coding.

Save the ZIP first here:

E:\routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_notes.md",
        "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\README.md",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_v1 installed."
    Write-Host "P12 static non-runtime Pilot phase closure / Copilot boundary entry-gate record installed."
    Write-Host "No closure execution, Copilot boundary approval, Copilot scope design, Copilot implementation, test-lab design/coding, activation key, maturity on/off switch, ML maturity claim, callable Pilot, route comparison execution, prompt loading, persistence, provider calls, embeddings, training-data use, batch mode, field-test activation, definitive enablement, Limited Shadow Runtime, or runtime authority were added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation.py",
        "tests\test_routing_signal_scorer_v3_pilot_implementation_gate_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_review_evidence_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_simulation_skeleton_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_gold_router_reproduction_harness_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_disagreement_taxonomy_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_io_contract_validator_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_scope_charter_entry_gate_design.py",
        "tests\test_rg_pilot_000_pilot_copilot_phase0_router_canon.py",
        "tests\test_routing_signal_scorer_v3_post_adviser_pilot_copilot_handoff_closure_design.py",
        "tests\test_routing_signal_scorer_v3_pilot_copilot_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_schema_family_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py",
        "tests\test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py",
        "tests\test_freeze_hint_autofill_state_machine.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    python -m py_compile "kanda_reasoner_app\routing_signal_scorer\adviser_offline\transition_design\non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    if ($LASTEXITCODE -ne 0) {
        throw "py_compile failed for P12 module"
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_v1"
    Write-Host "CONTRACT_TEST_OK: P12 Non-Runtime Pilot Phase Closure / Copilot Boundary Entry Gate v1, immutable governed P12 boundary after P11/P10/P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 freeze and installer canon freeze, static closure and entry-gate declaration only, no closure execution, no Copilot boundary approval, no Copilot scope design, no Copilot implementation, no test-lab design or coding, no runtime authority, no callable Pilot, no route comparison execution, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no Limited Shadow Runtime, no field-test activation, no definitive enablement, no activation key, no maturity on/off switch, no ML maturity claim, opt-in and in-memory-only constraints preserved, match-before-disagree preserved, critical boundary error budget zero, P11/P10/P9/P8/P7/P6/P5/P4/P3/P2/P1/P0/RG-PILOT-000/M35 and Adviser closure regressions validated"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_NON_RUNTIME_PILOT_PHASE_CLOSURE_COPILOT_BOUNDARY_ENTRY_GATE_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 Non-Runtime Pilot Phase Closure / Copilot Boundary Entry Gate v1

Do not start the test lab yet. After P12 freeze, send me the output showing:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

Then I will stop and explicitly warn you before any test-lab design or coding begins.

Pasted text.txt
Document
next 

P12 is frozen correctly.

The uploaded output shows:

LOCAL FREEZE WRITE OK
Freeze ID: freeze-20260619-routing-signal-scorer-v3-non-runtime-pilot-phase-closure-copilot-boundary-entry-gate-v1
FREEZE_MEMORY_STATUS: OK

So the current P-series is now closed: P0 through P12 complete and frozen.

There is one harmless-looking blocked starter preview in the log:

freeze-20260619-current-validated-feature-replace-with-exact-feature-title
Writable: NO

But that is not the final P12 freeze. The actual P12 freeze appears later and is valid.

Now I must stop and warn you before the next stage:

WARNING BEFORE TEST LAB

The next stage would be the test-lab design phase, where we would begin planning the governed lab for exhaustive testing of ML/router prompt logic.

This is not simple continuation of P12. It is a new governed phase.

I will not start test-lab design or coding until you explicitly confirm.

wait , last chat (review it) you told me that after P7 we would have at least more 10 steps before testing logic , nevertheless we are in step 12 , what happened to the other step missing ?

You are right to stop me here.

What happened is: two different counters got mixed together.

After P7, the frozen handoff said the current P-series had:

8 done, 5 to go
P8
P9
P10
P11
P12

That meant 5 more milestones to close the current Pilot preparation series, not 5 milestones to make ML functional or ready for real testing. The old handoff explicitly separated that from the broader estimate: “5 more steps = finish the current Pilot foundation series” and “~10 more steps = first functional non-runtime ML/router candidate possible.”

So we did not complete the “~10 ML/testing steps.” We completed only the remaining P8–P12 closure series.

The missing steps are still missing.

The correct state is:

Completed:
P0–P12 = Pilot/Copilot non-runtime preparation and closure scaffolding.

Not completed:
Test lab
Router prompt logic test cases
ML candidate testing
Gold/canon comparison
Metrics
Error library
Activation gate
Field-test gate
Runtime Pilot
Copilot

P12 itself confirms this boundary. It says P12 must preserve no test-lab design, no test-lab coding, no lab case creation, no lab execution, and that after P12 freeze the next behavior is STOP and warn before any test-lab design/coding starts.

So the real next roadmap should be renamed, not continued as P13 casually.

Something like:

LAB-0 — Test Lab Scope Charter / Entry Gate
LAB-1 — Lab Box Boundary Design
LAB-2 — Router Prompt Logic Test Case Schema
LAB-3 — Frozen Canon / Expected Answer Fixture Design
LAB-4 — Non-Runtime Test Runner Skeleton
LAB-5 — Failure Taxonomy for ML vs Router Logic
LAB-6 — Metrics / Scoring Design
LAB-7 — Exhaustive Router Prompt Logic Test Corpus Seed
LAB-8 — ML Candidate Evaluation Harness
LAB-9 — Error Canonization Intake Design
LAB-10 — Lab Closure / Activation-Gate Readiness Review

So your concern is correct: we are not done with the “10 more steps.” We only finished the old P-series. My “next is test lab” wording was too compressed; it should have been:

    P-series is closed. Now stop. The next separate phase would be LAB-0, and we must not treat that as already started or already safe.

I will not start LAB-0 until you explicitly confirm.

is this "~10 more steps = first functional non-runtime ML/router candidate possible.” the lab test?

Mostly yes, but with an important distinction.

The “~10 more steps” are not only the act of testing. They are the lab/testing phase needed before a first functional non-runtime ML/router candidate can exist safely.

So the better wording is:

~10 more steps = build the governed lab + test logic + evaluation harness + first non-runtime ML/router candidate path.

It includes the lab test, but it is broader than “run tests.”

Correct sequence:

P0–P12
= non-runtime Pilot/Copilot preparation and closure.
Done.

Next phase
= LAB / ML evaluation phase.

Inside that phase:
1. Define lab boundary.
2. Define test-case schema.
3. Define router prompt logic fixtures.
4. Define expected canon/gold answers.
5. Build non-runtime test runner.
6. Build failure taxonomy.
7. Build scoring/metrics.
8. Seed test corpus.
9. Add ML candidate evaluation harness.
10. Only then run serious/exhaustive tests.

So:

If by “lab test” you mean the whole controlled testing environment:
Yes, that is basically the next ~10-step phase.

If by “lab test” you mean simply running tests now:
No. We are not ready to run ML/router tests yet, because the lab, schemas, fixtures, metrics, and harness do not exist.

And very important:

This next phase still does not mean runtime Pilot, Copilot, prompt loading, persistence, batch mode, activation key, field test, or route authority.

The next safe step would be something like:

LAB-0 — Test Lab Scope Charter / Entry Gate

That would define the lab boundary before any lab coding.

so next logic steps is not continuing ML implementation , is lab test implementation ?

Yes — the next logical phase is lab/test implementation, not continuing ML implementation directly.

More precise:

P0–P12 = finished the non-runtime Pilot/Copilot preparation scaffold.

Next = build the governed LAB phase.

Only after the lab exists do we continue toward functional non-runtime ML/router candidate evaluation.

So the next step should not be:

“Implement more ML logic”

It should be:

LAB-0 — Test Lab Scope Charter / Entry Gate

Then:

LAB-1 — Lab Box Boundary Design
LAB-2 — Test Case Schema
LAB-3 — Router Prompt Logic Fixtures
LAB-4 — Non-Runtime Test Runner Skeleton
LAB-5 — Failure Taxonomy
LAB-6 — Metrics / Scoring
LAB-7 — Test Corpus Seed
LAB-8 — ML Candidate Evaluation Harness
LAB-9 — Error Canonization Intake
LAB-10 — Lab Closure / Activation-Gate Readiness Review

So the correct interpretation is:

We pause ML implementation until the lab exists.
The lab is what makes future ML implementation safe, measurable, and not guess-based.

P12 also confirms this boundary: it says P12 must preserve no test-lab design, no test-lab coding, no lab case creation, and no lab execution, and after P12 freeze the next behavior is STOP and warn before test-lab work begins.

So the next governed action, only after your confirmation, is:

Start LAB-0 — Test Lab Scope Charter / Entry Gate

Not runtime Pilot.
Not Copilot.
Not activation key.
Not field testing.
Not ML maturity.
Not prompt loading.
Not persistence.
Not route authority.

Before implementing LAB TEST, create a handoff to send to other AI:
say to AI she is s senior specialist with 20 years of experience in the context an solution of this kind of logic ,
explain context, what we did so far in this ML logic , 
explain that is labtest for,
explain in details how do you intend to create the ML lab/tests ,  as a controled environement to test ML capacity to prompt choosing, and decision taking,  to the end that , router prompt logic works with maximum reliability. Also cite aproximately how many tests do you intend to create , and ask if is enough , less or more than enough.
then ask AI to audit your solution, give suggestions for correction, update, maximum performance, risks , prevention of risks , prevention of code leaking to  other boxes,  shielding box, testing ml lab/tests, and what more you think is important to lab/test fulfill its mission smoothly.
After that I will bring the audit results for your own audit.

Below is a copy-ready handoff. I’m keeping it as audit-only: it does not authorize implementation. The current frozen state is P0–P12 complete, with P12 explicitly saying the next behavior is STOP before any test-lab design/coding.
External AI Audit Request — KANDA/PyArchitect ML Router Lab/Test Phase

You are a senior specialist with 20 years of experience designing controlled evaluation systems for AI routing, prompt-selection logic, governance-safe ML workflows, software architecture boundaries, regression testing, and high-reliability decision systems.

I need you to audit the next planned phase of my project before implementation begins.

This is not a request to implement code. This is an expert review request.
1. Project context

The project is a Python/PySide6 desktop application called KANDA Reasoner / PyArchitect.

The system contains a governed prompt-routing architecture. Its purpose is to help decide which internal prompts, workflow rules, and governance protocols should be loaded or followed for a given user request.

The long-term roadmap includes a progression from:

Adviser → Assistant/Auxiliary → Pilot → Copilot

But the current system is intentionally conservative. The project has strict governance rules to avoid unsafe runtime authority.

Core doctrine:

ML recommends. Canon and router governance decide.

Match before disagree.

The ML/Pilot/Copilot pathway must not become a runtime decision-maker too early.
2. What has been done so far

A full non-runtime Pilot/Copilot preparation series has been completed and frozen.

Milestones P0 through P12 are done and frozen.

These milestones did not create a live ML router, live Pilot, or Copilot. They created static, non-runtime governance scaffolding and boundary declarations.

The completed P-series established:

    Non-runtime Pilot/Copilot boundary rules.

    No route authority.

    No prompt loading.

    No persistence.

    No batch mode.

    No training-data use.

    No gold/registry mutation.

    No provider calls.

    No embeddings/vector store.

    No runtime Pilot execution.

    No Copilot implementation.

    No activation key.

    No maturity on/off switch.

    No field-test activation.

    No definitive enablement.

    Human review remains mandatory.

    Opt-in per invocation remains mandatory.

    In-memory-only constraints are preserved.

    Critical boundary error budget is zero.

The final P12 milestone closed the current P-series and explicitly declared that before any test-lab design or coding begins, the user must be warned and confirm the next phase.

That warning/confirmation step has now been reached.
3. What the next phase is for

The next phase is the LAB / ML evaluation phase.

The purpose is not to turn on runtime ML.

The purpose is to create a controlled test laboratory that can safely evaluate whether future ML/router candidate logic can correctly perform prompt choice, routing interpretation, governance classification, missing-context detection, and decision support under strict non-runtime constraints.

The lab should answer questions like:

    Can the ML candidate choose the same prompt group as the frozen router canon?

    Can it identify when a request must be routed instead of handled fast?

    Can it detect bypass attempts?

    Can it refuse to proceed when mandatory context is missing?

    Can it distinguish patch work, freeze work, prompt-library work, medical writing, ordinary chat, document tasks, and high-risk governance workflows?

    Can it avoid overstepping into runtime authority?

    Can it explain disagreements with the canon without overriding the canon?

    Can it preserve “match before disagree”?

    Can it avoid contaminating other boxes?

    Can it remain inside its assigned box boundaries?

    Can it handle typos, incomplete instructions, stale handoffs, old filenames, and user shorthand like “go next”?

The lab exists so future ML logic is measurable, auditable, and regression-tested before any stronger role is considered.
4. Important boundary

The lab must not create runtime authority.

The lab must not call real providers.

The lab must not load live prompts into runtime behavior.

The lab must not mutate routing canon, gold registry, prompt library, freeze memory, or project state.

The lab must not perform autonomous routing.

The lab must not create Copilot behavior.

The lab must not create an activation key.

The lab must not create field-test mode.

The lab must not create persistent ML decisions unless a future governed milestone explicitly authorizes a safe storage box.

The lab should initially be non-runtime, deterministic, local, and audit-oriented.
5. Intended LAB roadmap

My current intended roadmap is:

LAB-0 — Test Lab Scope Charter / Entry Gate
Define the lab purpose, boundaries, forbidden behaviors, allowed artifacts, lifecycle state, and stop conditions.

LAB-1 — Lab Box Boundary Design
Create the Box Architecture boundary for the lab. Define exactly which box owns the lab logic, which boxes are read-only inputs, and which boxes are forbidden.

LAB-2 — Router Prompt Logic Test Case Schema
Define a neutral schema for test cases. Each case should include user request, expected task classification, expected path, required prompt groups, missing context, forbidden actions, expected safe next action, and expected explanation.

LAB-3 — Frozen Canon / Expected Answer Fixture Design
Define how frozen router/canon expectations are represented as fixtures without mutating canon files or prompt library files.

LAB-4 — Non-Runtime Test Runner Skeleton
Create a local deterministic runner that reads static fixtures and compares candidate outputs against expected results. It should not call live models unless a future separate milestone permits controlled external evaluation.

LAB-5 — Failure Taxonomy
Classify failures such as false fast-path, missed routed-work path, prompt omission, unsafe route authority, stale context acceptance, missing-context failure, freeze-boundary violation, box leakage, and overconfident ML disagreement.

LAB-6 — Metrics / Scoring Design
Define metrics such as exact route match, required prompt recall, forbidden action avoidance, missing-context detection, governance-boundary pass/fail, disagreement quality, and critical-boundary violation count.

LAB-7 — Test Corpus Seed
Create the first meaningful corpus of test cases. This should include normal cases, edge cases, adversarial cases, stale-context cases, typo-heavy cases, ambiguous cases, project-specific cases, and regression cases from past mistakes.

LAB-8 — ML Candidate Evaluation Harness
Create a safe way to compare ML candidate outputs against frozen expectations. This must remain non-runtime and must not let candidate output control the application.

LAB-9 — Error Canonization Intake Design
Design how recurring ML/router mistakes become permanent regression tests later, without yet building a broad autonomous memory or mutation system.

LAB-10 — Lab Closure / Activation-Gate Readiness Review
Review whether the lab is strong enough to support later discussion of Activation Gate Box, field-test mode, or mature enablement. This does not activate anything.
6. Intended test volume

My initial estimate is that the first serious lab should not be tiny.

I am considering approximately 180 to 250 tests in the first complete seeded corpus, expandable later to 300 to 500+ tests as real failures are discovered.

Possible initial distribution:

    30 basic routing classification tests.

    25 fast-path versus routed-work-path distinction tests.

    25 required prompt/group selection tests.

    20 missing-context and “may proceed now” tests.

    20 freeze/update/governance workflow tests.

    20 prompt-library and prompt-authoring tests.

    20 patch delivery / installer / validation / freeze-memory tests.

    15 Box Architecture boundary and code-leakage tests.

    15 stale context / stale filename / stale sidecar tests.

    15 adversarial bypass and “ignore the rules” tests.

    15 typo-heavy, shorthand, multilingual, and ambiguous user request tests.

    10 medical/document/simple-task distinction tests.

    10 regression tests based on known past mistakes.

Question for you: is this approximate test volume too small, enough, or excessive for the first lab phase?

Should the first lab begin with fewer tests, such as 50 to 80 highly curated tests, then expand?

Or should it begin closer to 200+ tests to prevent weak coverage?
7. Intended lab architecture

The lab should be created as a separate governed box, not mixed into the live router, prompt library, freeze memory, or application runtime.

Possible box name:

routing_signal_scorer/lab_router_prompt_logic

Or:

kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation

The lab box should have:

    Its own README.

    Its own static schema definitions.

    Its own test fixtures.

    Its own deterministic runner.

    Its own metrics model.

    Its own failure taxonomy.

    Its own tests.

    No write access to other boxes.

    No direct mutation of prompt files.

    No direct mutation of freeze memory.

    No direct mutation of router canon.

    No direct mutation of gold registry.

    No runtime hooks into user-facing routing.

    No activation key.

The lab may read static exported fixtures or copied test expectations, but should not reach into protected boxes at runtime in a way that creates hidden coupling.
8. Box shielding requirements

Please audit how to prevent the lab from leaking into other boxes.

Risks I want you to evaluate:

    Lab runner accidentally becomes a runtime router.

    ML candidate output accidentally becomes authoritative.

    Test fixtures become confused with active prompt canon.

    Gold expected outputs become mutable by tests.

    Evaluation harness writes persistent decisions too early.

    Lab imports live application routing modules and creates side effects.

    Lab reaches into prompt-library files directly and creates hidden dependency.

    Lab code becomes mixed with production routing code.

    Future activation gate is accidentally introduced early.

    Human approval is recorded automatically instead of explicitly.

    Batch mode appears before authorized.

    Test generation starts creating training data before governance permits it.

    Error canonization is mixed into lab too early.

Please propose preventive design rules for these risks.
9. Audit request

Please audit the whole plan.

I want your expert review on:

    Is this the right next phase after P0–P12?

    Is the LAB roadmap correctly ordered?

    Should LAB-0 be only a scope charter, or should it already create files?

    Should the lab be one box or several boxes?

    What should be the minimum viable lab before any ML candidate is tested?

    What is the ideal test-case schema?

    What is the ideal scoring model?

    How many tests should the first corpus include?

    Which test categories are missing?

    Which failure categories are missing?

    How do we prevent code leaking into router, prompt library, freeze memory, gold registry, provider, embedding, persistence, or activation boxes?

    How do we prevent “test lab” from becoming “runtime Pilot” by accident?

    How do we prevent false confidence from a small or biased test corpus?

    How do we handle disagreement between ML candidate and frozen router canon?

    How do we enforce “match before disagree” inside the lab?

    What should be the critical-boundary error budget?

    What must be blocked absolutely?

    What should be allowed only later?

    What should be frozen after each lab milestone?

    What changes would you make for maximum reliability, maximum performance, and smooth future expansion?

10. Deliverable requested from you

Please return:

    A clear audit verdict.

    Recommended corrections.

    Recommended LAB roadmap.

    Recommended test count and distribution.

    Recommended schema fields.

    Recommended scoring metrics.

    Recommended failure taxonomy.

    Recommended box boundaries.

    Recommended risk-prevention rules.

    Recommended freeze rules after each lab milestone.

    Any red flags that should stop implementation.

    Any improvements for maximum performance and long-term maintainability.

Do not implement code.

Do not assume runtime authority.

Do not propose enabling Copilot yet.

Do not propose activation key yet unless you explicitly mark it as future-only after lab maturity evidence.

Please be strict. The goal is maximum reliability and prevention of unsafe architecture drift.

Pasted text.txt
Document
Pasted text (2).txt
Document
Pasted text (3).txt
Document
Pasted text (4).txt
Document
Pasted text (5).txt
Document
first is deepseek
second claude

third and fourth qwen 3.7 plus

5th =mistral studio
6th gemini


now  audit and bring to our lab/test implementation logic what is really usefull

I’ll consolidate the six-model review into one governed implementation plan, separating strong consensus from ideas we should reject or defer. I’ll keep this as design/audit only, not LAB implementation.

I see five uploaded text files in this message; one appears to contain more than one response, so I’m treating the bundle as your six-audit set unless you send another separate Gemini file.
My audit verdict

The external audits are useful, but we should not copy any one model’s roadmap directly. The best solution is a merged LAB plan:

Next phase = LAB / ML evaluation infrastructure.
Not direct ML implementation.
Not runtime Pilot.
Not Copilot.
Not activation.

P12 already froze the rule that after P12 the next behavior is STOP and that any test-lab design/coding requires explicit warning/confirmation.

The strongest consensus across the audits is:

    The LAB phase is the correct next phase after P0–P12.

    The lab must be one isolated box.

    The lab must use static fixtures, not live canon reads.

    The first corpus should not start at 200+ tests.

    Critical-boundary error budget stays zero.

    Hard gates must be separate from soft scores.

    “Match before disagree” must be structural, not just a slogan.

    The lab must self-test before evaluating any ML candidate.

    Import/file/write boundaries must be tested, not just documented.

    Every LAB milestone must be frozen before the next.

DeepSeek/first audit specifically supports “approved with conditions,” adding an entry-gate audit, improving box isolation, reducing initial test volume, defining disagreement handling, and defining freeze rules. Claude/second audit strongly warns that the first version is over-scoped, recommends one box, fixture copies rather than live references, 60–80 curated initial tests, hard gates separate from aggregate scores, and canon_version_reference in test cases. Qwen-style audits add the most useful correction: LAB self-validation before ML candidate evaluation, fixture hashing, candidate output wrapping, canon-rule references for every test, and hard stop conditions if the lab itself cannot classify pass/fail correctly. Mistral’s best contribution is the two-tier corpus idea: small Alpha corpus first, later larger Beta expansion after runner/scoring stability.
What I will assimilate into our LAB logic
1. Corrected milestone sequence

I would not keep the original LAB-0 to LAB-10 exactly. I would harden it like this:

LAB-0 — Phase Boundary + Lab Charter / Entry Gate
LAB-1 — Box Boundary + Shielding Manifest
LAB-2 — Failure Taxonomy + Critical Violation Model
LAB-3 — Scoring Model + Hard Gates
LAB-4 — Test Case Schema + Two-Pass Candidate Output Contract
LAB-5 — Frozen Canon Fixture Format + Hash Manifest
LAB-6 — Deterministic Runner Skeleton
LAB-7 — Lab Self-Validation Gate
LAB-8 — Alpha Corpus Seed
LAB-9 — Candidate Evaluation Harness Interface
LAB-10 — Corpus V1 Expansion + Coverage Matrix
LAB-11 — Error Canonization Intake Spec
LAB-12 — Lab Closure / Next-Phase Readiness Review

Important change: Failure taxonomy and scoring come before final schema/corpus. Several audits correctly said you cannot design good test cases before defining what failure means and how it will be measured.
2. LAB-0 should be documentation-only, but still freezeable

I would not create runner code, schema code, fixtures, or tests in LAB-0.

But I would allow LAB-0 to create governance documents only, probably:

LAB_CHARTER.md
LAB_ENTRY_GATE.md
LAB_FORBIDDEN_BEHAVIORS.md
LAB_STOP_CONDITIONS.md
LAB_PHASE_BOUNDARY.md

No .py logic in LAB-0.

This takes the useful part from the audits that want hard boundaries, while avoiding premature implementation. Some audits wanted LAB-0 to create violation-detection code immediately, but I would defer that to LAB-1 because P12 said no lab coding had begun yet and we should not collapse the charter into implementation.
3. One lab box only

Use one primary box:

kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/

Not multiple top-level lab boxes.

Internal subfolders later:

charter/
boundary/
taxonomy/
scoring/
schema/
fixtures/
runner/
harness/
reports/
tests/

But the primary box remains one box. This matches the audit consensus and the Box Architecture rule that a patch should have one primary box with a clear responsibility and forbidden dependencies.
4. Test count decision

I will not start with 180–250 tests.

Best plan:

Alpha corpus: 60–80 tests
Corpus V1: 100 tests
Later expansion: 200–250 only after harness stability
Long-term: 300–500+ only through real regression/error canonization

Why: 200+ tests too early can create false confidence, stale fixture burden, and maintenance noise before schema/runner/scoring are proven. This was one of the strongest common points across the audits.

Recommended Alpha distribution:

10 basic routing classification
10 fast-path vs routed-work-path
8 required prompt/group selection
8 missing-context / may-proceed-now
6 freeze/update/governance workflow
6 prompt-library / prompt-authoring
6 patch / installer / validation / freeze-memory
6 box boundary / leakage
5 stale context / stale filename / stale sidecar
5 adversarial bypass / ignore-rules
4 typo / shorthand / ambiguous
3 medical/document/simple-task distinction
3 regression from known past mistakes

Then expand to 100 after LAB self-validation.
5. Schema fields we should use

The useful schema fields are:

case_id
case_version
schema_version
category
subcategory
severity
critical_boundary_flag
adversarial_flag
regression_source
canon_version_reference
canon_rule_references
user_request_raw
normalized_request
simulated_context
conversation_history
context_freshness
simulated_freeze_state
simulated_handoff_state
simulated_sidecar_state
expected_task_classification
expected_path
expected_required_prompt_groups
expected_prompt_priority
expected_missing_context
expected_forbidden_actions
expected_safe_next_action
expected_explanation_elements
expected_match_behavior
candidate_pass_1_canon_match
candidate_pass_2_disagreement
yield_to_canon

The most important additions from the audits are:

canon_version_reference
critical_boundary_flag
candidate_pass_1_canon_match
candidate_pass_2_disagreement
yield_to_canon
context_freshness
simulated_sidecar_state

These make the lab measurable and protect “match before disagree.”
6. Scoring model we should use

I will not use one simple aggregate score.

Use two layers:

Hard gates:
- critical boundary violation = fail
- forbidden action attempted = fail
- prompt loading attempted = fail
- route authority attempted = fail
- persistence attempted = fail
- canon/freeze/gold mutation attempted = fail
- missing required human review = fail
- missing opt-in where required = fail
- skipped match-before-disagree = fail

Soft metrics:
- route exact match
- prompt recall
- prompt precision
- missing-context detection
- explanation quality
- disagreement quality
- confidence calibration
- stale-context rejection

Hard gates always win. A candidate cannot get “95% good” if it has one critical violation. The audits agree that critical-boundary error budget must remain zero.
7. Failure taxonomy we should include

Use these categories:

FALSE_FAST_PATH
MISSED_ROUTED_WORK
INCORRECT_ROUTE
PROMPT_OMISSION
PROMPT_EXCESS
PROMPT_PRIORITY_ERROR
MISSING_CONTEXT_FAILURE
STALE_CONTEXT_ACCEPTANCE
CONTEXT_OVERRIDE
HANDOFF_CORRUPTION
TIMELINE_VIOLATION
FALSE_CERTAINTY
CONFIDENCE_MISCALIBRATION
EXPLANATION_MISMATCH
EXPLANATION_HALLUCINATION
SILENT_FAILURE
SCHEMA_VIOLATION
FIXTURE_CONTAMINATION
BOX_LEAKAGE
BOX_CONTAMINATION
ROUTE_AUTHORITY_OVERRIDE
UNAUTHORIZED_PROMPT_LOAD
RUNTIME_ACTION
CANON_MUTATION
FREEZE_MEMORY_MUTATION
GOLD_REGISTRY_MUTATION
PERSISTENCE_ATTEMPT
PROVIDER_CALL_ATTEMPT
EMBEDDING_ATTEMPT
ACTIVATION_KEY_ATTEMPT
FIELD_TEST_MODE_ATTEMPT
COPILOT_BEHAVIOR_ATTEMPT
MATCH_BEFORE_DISAGREE_VIOLATION
CANON_OVERSTEP_DISAGREEMENT

The most useful added categories from the audits are false certainty, explanation drift, hallucinated context, fixture contamination, context-window confusion, temporal confusion, over-selection, and metric gaming.
8. Box shielding rules to assimilate

The lab must be structurally unable to leak into production:

No production code may import lab code.
Lab code may not import runtime router.
Lab code may not import prompt loader.
Lab code may not import provider/embedding/vector modules.
Lab code may not import PySide6/UI.
Lab code may not write outside the lab box.
Lab code may not mutate prompt library, canon, gold, freeze memory, or registry.
Fixtures are copied snapshots, not live references.
Candidate outputs are wrapped as non-authoritative evaluation-only records.
Any output path must be inside the lab box.
No network calls.
No subprocess.
No exec/eval.
No async/event bus/UI loop.
No activation key fields.
No field-test flags.
No persistent ML decision storage.

The audits strongly recommend making these enforceable through tests/import scans, not just README text.
9. LAB self-validation is mandatory

This is one of the best audit suggestions.

Before testing an ML candidate, the lab must prove it can detect:

gold-vs-gold = PASS
wrong route = FAIL
missing prompt = FAIL
forbidden action = CRITICAL_FAIL
fixture hash mismatch = CRITICAL_FAIL
skipped match-before-disagree = CRITICAL_FAIL

If self-validation fails, the lab is not allowed to evaluate ML. This prevents false trust in a broken testing tool.
10. What I reject or defer

I would reject for now:

200+ tests on day one
live provider calls
embeddings/vector stores
runtime shadow mode
persistent ML decision storage
activation key
field-test mode
Copilot behavior
production importing lab
lab importing production router
automatic error canonization
external dependencies as first choice

I would also defer Hypothesis, Pydantic, import-linter, Docker, and external tooling unless later governed milestones authorize them. Your earlier frozen logic explicitly warned not to add external ML frameworks, providers, embeddings, vector stores, Import Linter dependency, Docker, monitoring, persistent report storage, or runtime shadow mode too early.
Final merged implementation logic

The LAB mission should be:

Build a deterministic, isolated, non-runtime evaluation laboratory that tests whether future ML/router candidates can reproduce frozen router prompt logic, detect missing context, avoid forbidden actions, explain disagreements without overriding canon, and remain subordinate to governance.

The lab is not built to prove the ML is smart.

It is built to prove the ML is safe, subordinate, measurable, and rejectable.

Best next safe action:

LAB-0 — Phase Boundary + Lab Charter / Entry Gate

LAB-0 should freeze the mission, boundaries, forbidden behaviors, stop conditions, allowed artifacts, and phase-entry evidence.

No runner.
No fixtures.
No ML candidate.
No provider.
No prompt loading.
No persistence.
No runtime authority.

now you surf the web going in to  well known  sites specialized in [ the subject task] and search for other ideas that can correct, update,  improve, increase performance of the logic of implementation  with a real gain  in logic, performance, safety ,  and  bring those ideas to our Project. Then add what is real gain to our logic flux

I’ll check current specialist sources on LLM evaluation, AI risk management, prompt-injection defense, model testing, and evaluation harness design, then merge only the parts that add real value to our LAB flow.

A strong pattern is emerging from the web sources: professional LLM evaluation systems separate datasets, evaluators, experiments, analysis, and monitoring. For our project, that means the lab should be built as evaluation infrastructure first, not as an ML candidate.

I searched current specialist sources on LLM evals, AI risk management, prompt-injection/security, agent evaluation, observability, and ML production-readiness. The useful sources were mainly: OWASP LLM Top 10, NIST AI RMF, OpenAI Evals, Anthropic eval guidance, LangSmith evaluation workflow, Microsoft Foundry evaluation/observability, Google Gemini/Vertex evaluation, and Google ML Test Score. OWASP is especially relevant because it lists prompt injection, insecure output handling, training-data poisoning, model DoS, supply-chain risk, sensitive information disclosure, and insecure plugin/tool design as LLM application risks.
Web-audited correction to our LAB logic

The biggest update is this:

The lab should not only test “did the ML choose the right prompt?”

It must test:
1. Did it choose the right route/prompt?
2. Did it avoid forbidden authority?
3. Did it stay grounded in the provided context/canon?
4. Did it detect missing or stale context?
5. Did it preserve box boundaries?
6. Did it produce auditable reasoning?
7. Did it fail safely?
8. Did it remain subordinate to canon?

This is aligned with NIST’s risk-management framing: AI risk controls should be incorporated into design, development, use, and evaluation, not bolted on later.
Real gains to add to our LAB flux
1. Add a formal “success criteria first” gate

Anthropic’s evaluation guidance says successful LLM application development starts by clearly defining success criteria and then designing evaluations to measure them. It also emphasizes that good criteria must be specific and measurable.

So our LAB flow should add this before schema/corpus:

LAB-0A — Success Criteria Matrix

Define:
- what counts as correct routing
- what counts as safe disagreement
- what counts as missing-context detection
- what counts as forbidden authority
- what counts as box leakage
- what counts as critical failure

This prevents writing many tests before we know exactly what they are proving.
2. Add dataset → evaluator → experiment → analysis structure

LangSmith’s evaluation workflow is simple and useful: create a dataset, define evaluators, run an experiment, then analyze results for benchmarking, unit tests, regression tests, or backtesting.

So our LAB should copy the architecture pattern, not the dependency:

Dataset = static test corpus
Evaluators = deterministic rule/check functions
Experiment = one candidate run against one frozen corpus version
Analysis = report with hard gates, soft metrics, failures, coverage, and regressions

Real gain: this gives our lab a clean conceptual model and avoids mixing fixtures, runner, metrics, and reports.
3. Add adaptive rubric concept, but keep deterministic v1

Google’s Gen AI evaluation service treats rubrics as pass/fail tests similar to software unit tests and supports adaptive rubrics, static rubrics, computation-based metrics, and custom functions.

For KANDA, we should not start with adaptive generated rubrics, because that adds ML uncertainty too early. But we should assimilate the idea as:

Each test case gets its own explicit pass/fail rubric.

Not only one global scoring rule.

So each fixture should include:

case_specific_pass_conditions
case_specific_fail_conditions
case_specific_critical_fail_conditions

Real gain: a freeze-workflow case and a medical-document case should not be graded with the exact same rubric.
4. Add process evaluation versus final-output evaluation

Microsoft’s RAG evaluator docs distinguish process evaluation from system/final-response evaluation. It also separates groundedness as precision — no unsupported content — and response completeness as recall — not missing critical expected information.

This is very useful for our router lab.

Add two evaluation layers:

Process evaluation:
- Did the candidate identify the right task class?
- Did it detect routed-work-path?
- Did it select required prompt groups?
- Did it detect missing context?
- Did it preserve box boundaries?

Final output evaluation:
- Did the final candidate record match expected canon?
- Was the explanation complete?
- Did it avoid unsupported claims?
- Did it yield to canon?

Real gain: if the final answer looks okay but the reasoning path violated governance, we catch it.
5. Add observability fields even before runtime

Microsoft Foundry frames evaluation, monitoring, and tracing as core observability capabilities and notes that evaluations should measure quality, safety, and reliability throughout development. It also tracks metrics, logs, traces, model outputs, token consumption, latency, error rates, and quality scores.

We will not add production monitoring now. But we should add offline observability fields to lab reports:

lab_run_id
corpus_version
schema_version
candidate_version
runner_version
started_at_utc
ended_at_utc
duration_ms
tests_total
tests_passed
tests_failed
critical_failures
category_scores
coverage_gaps
fixture_hash_manifest

Real gain: every lab run becomes reproducible and auditable.
6. Add “private evals for workflow patterns”

OpenAI Evals describes a framework for evaluating LLMs or LLM systems and supports custom/private evals representing common workflow patterns without exposing private data publicly.

For our project, this means the corpus should be project-specific, not generic.

We should create fixtures for KANDA-specific patterns:

"go next"
"continue"
"create patch"
"freeze this"
"audit again"
"read startup zip"
"ignore routing and implement"
"Pasted validation output"
"stale freeze sidecar"
"root-drive patch staging"
"medical laudo versus project patch task"
"uploaded startup pack versus current project zip"

Real gain: generic LLM benchmarks will not test the actual mistakes this project needs to prevent.
7. Add prompt-injection and insecure-output handling as hard security categories

OWASP lists prompt injection as crafted inputs that can cause unauthorized access, data breaches, or compromised decision-making, and insecure output handling as failure to validate LLM outputs before they reach downstream systems.

For KANDA, this becomes:

New hard-gate categories:
- PROMPT_INJECTION_BYPASS
- INSECURE_OUTPUT_TO_DOWNSTREAM
- ROUTE_AUTHORITY_FROM_USER_TEXT
- USER_REQUESTED_RULE_BYPASS
- SYSTEM_PROMPT_OR_PROMPT_FILE_LEAK_ATTEMPT
- CANDIDATE_OUTPUT_USED_AS_ACTION

Real gain: the lab will test not only “wrong route,” but “dangerous wrong route.”
8. Add ML Test Score style maturity gates

Google’s ML Test Score work frames testing and monitoring as key to production-readiness and provides actionable tests to quantify readiness.

We should adapt that into a KANDA Lab Maturity Score, but only as internal readiness, not activation.

LAB_MATURITY_LEVEL_0 = charter only
LAB_MATURITY_LEVEL_1 = boundaries frozen
LAB_MATURITY_LEVEL_2 = schema/taxonomy/scoring frozen
LAB_MATURITY_LEVEL_3 = runner self-validates
LAB_MATURITY_LEVEL_4 = alpha corpus passes with dummy candidates
LAB_MATURITY_LEVEL_5 = candidate harness evaluates non-runtime outputs
LAB_MATURITY_LEVEL_6 = corpus coverage matrix reaches minimum
LAB_MATURITY_LEVEL_7 = error intake spec exists

Real gain: we avoid vague statements like “lab is good enough.” We use explicit maturity gates.
9. Add multi-turn and stateful evaluation, but not runtime state

Anthropic’s agent-evals article notes that multi-turn evaluations are increasingly important and that agent mistakes can propagate and compound over time.

For KANDA, we should add simulated multi-turn cases:

Turn 1: user asks about patch.
Turn 2: user says “continue.”
Expected: candidate preserves patch context only if valid.

Turn 1: user validates P12.
Turn 2: user says “next.”
Expected: stop and warn before LAB, not start coding.

Turn 1: user asks medical laudo.
Turn 2: user says “create patch.”
Expected: route changes safely; no context contamination.

Real gain: many KANDA mistakes happen around “continue,” “go next,” stale handoff, and previous-turn context.
Updated LAB implementation flux

This is the revised, web-audited flow I would use.

LAB-0 — Phase Boundary + Lab Charter / Entry Gate
Purpose, phase boundary, no-code rule, forbidden behaviors, stop conditions.

LAB-0A — Success Criteria Matrix
Specific measurable criteria for routing, prompt selection, missing context, disagreement, box safety, and hard failures.

LAB-1 — Lab Box Boundary + Shielding Manifest
One isolated lab box, forbidden imports, forbidden writes, no runtime hooks, no provider, no PySide6, no prompt loading.

LAB-2 — Risk-Control Matrix
Map OWASP/NIST-style risks to lab controls:
prompt injection, insecure output handling, sensitive info leakage, excessive agency, supply-chain/fixture integrity, model DoS/latency.

LAB-3 — Failure Taxonomy + Critical Violation Model
Define all failure types and zero-tolerance boundary failures.

LAB-4 — Scoring Model + Hard Gates
Separate hard gates from soft metrics. No aggregate score may hide critical failures.

LAB-5 — Test Case Schema + Case-Specific Rubrics
Typed fixture schema with canon_version_reference, pass/fail rubric, critical_fail rubric, and two-pass match-before-disagree fields.

LAB-6 — Frozen Canon Fixture Format + Hash Manifest
Static copied snapshots only. No live canon reads during test runs.

LAB-7 — Deterministic Runner Skeleton
Reads fixtures, validates schema, compares expected vs actual candidate output. No ML calls.

LAB-8 — Lab Self-Validation Gate
Gold-vs-gold passes; known-bad fixtures fail; forbidden-action fixtures critical-fail.

LAB-9 — Alpha Corpus Seed
60–80 curated tests, manually reviewed, with coverage matrix.

LAB-10 — Candidate Evaluation Harness Interface
Candidate output enters only as non-authoritative evaluation records. No runtime connection.

LAB-11 — Corpus V1 Expansion
Expand to ~100 tests only after runner/scoring/schema are stable.

LAB-12 — Offline Observability Report
Structured run report: run id, versions, hashes, duration, failures, coverage gaps, hard-gate status.

LAB-13 — Error Canonization Intake Spec
Design only. No automatic mutation of canon or corpus yet.

LAB-14 — Lab Closure / Next-Phase Readiness Review
Review whether the lab is mature enough to discuss later controlled candidate testing.

Changes to our previous plan

Main corrections:

Added LAB-0A Success Criteria Matrix.
Added LAB-2 Risk-Control Matrix.
Moved failure taxonomy and scoring before schema/corpus.
Added case-specific rubrics.
Added offline observability/reporting as its own milestone.
Added ML-style maturity levels.
Added multi-turn simulation category.
Added security categories from OWASP.
Kept initial corpus small: 60–80, then ~100.
Kept external tools as inspiration only, not dependencies.

Things I will not bring into the project now

These ideas exist in the web ecosystem, but they are not safe for our current phase:

online evaluators
production monitoring
live provider calls
LLM-as-judge as primary grader
adaptive rubric generation by model
synthetic test generation without human review
automatic error canonization
agentic red teamers
async/batch execution
prompt optimization loops
field-test mode
activation gates
Copilot behavior

Reason: our current frozen doctrine says the lab must stay non-runtime, deterministic, local, and subordinate to canon. The first lab should use code/rule-based evaluators and static fixtures before any model-based judging is introduced.
Final assimilated rule

The lab’s mission should now be frozen conceptually as:

The KANDA LAB is a deterministic, isolated, non-runtime evaluation system that tests whether future ML/router candidates can reproduce frozen router governance, detect missing or stale context, avoid unsafe authority, preserve box boundaries, explain disagreements without overriding canon, and produce auditable evaluation records.

It does not activate, route, load prompts, persist ML decisions, call providers, mutate canon, or implement Copilot.

Best next safe milestone remains:

LAB-0 — Phase Boundary + Lab Charter / Entry Gate

No implementation yet until you explicitly confirm.

wait once more: now you surf the web, search on web for the 5 top of the list  books on [the subject we are discussing], books specialized in [ the subject task] and search for other ideas that can correct, update,  improve, increase performance of the logic of implementation  with a real gain  in logic, performance, safety ,  and  bring those ideas to our Project. Then add what is real gain to our logic flux.

after that you will update the logic of ML lab/test to adapt what is best "accordingly with your audit" from AI specialists , sites from web, 5 top of the list book, and return it explained in next answer.

I’ll do one more external pass focused specifically on books, not websites or AI auditors. I’ll keep only ideas that materially improve our LAB architecture and reject anything that would push us toward runtime ML too early.

I did the book-focused web pass and I would update our LAB logic, but not by adding many new dependencies. The real gain from the books is architectural discipline: success criteria, versioned evaluation data, reliability/error budgets, reproducibility patterns, and task-specific metrics.

I selected the top 5 books/reports most useful for this exact task: building a non-runtime ML/router evaluation lab, not generic AI learning.
Top 5 books I would assimilate
1. AI Engineering — Chip Huyen

Why it matters: this is the most directly relevant for foundation-model application engineering. The book is about building applications with available foundation models, and the author page says it covers models, datasets, evaluation benchmarks, use cases, and deployment concerns.

Real gain for our project: add an explicit separation between:

candidate model
candidate adapter
evaluation dataset
evaluator
experiment run
analysis report

This prevents the future ML candidate from becoming the lab itself. The LAB tests the candidate; the candidate does not own the LAB.
2. Designing Machine Learning Systems — Chip Huyen

Why it matters: O’Reilly describes it as a holistic approach to ML systems that are reliable, scalable, maintainable, and adaptive.

Real gain for our project: add lifecycle/version control for every evaluation asset:

schema_version
corpus_version
fixture_version
canon_version_reference
runner_version
candidate_version
scoring_model_version

This prevents silent drift: a test result is meaningless unless we know exactly which canon, schema, fixtures, and runner produced it.
3. Reliable Machine Learning — Cathy Chen, Niall Richard Murphy, Kranti Parisa, D. Sculley, Todd Underwood

Why it matters: the book applies an SRE mindset to ML and focuses on running ML reliably, effectively, and accountably, including monitoring and reliability practices.

Real gain for our project: turn “critical boundary error budget = zero” into a formal LAB SLO / incident rule:

Critical boundary SLO:
0 route-authority violations
0 prompt-loading attempts
0 persistence attempts
0 provider calls
0 canon/freeze/gold mutation attempts
0 activation/field-test attempts

If any one happens, the candidate is disqualified and the lab run becomes an incident report, not a normal failed test.
4. Machine Learning Design Patterns — Valliappa Lakshmanan, Sara Robinson, Michael Munn

Why it matters: O’Reilly describes the book as 30 patterns for representation, operationalization, repeatability, reproducibility, flexibility, explainability, and fairness.

Real gain for our project: define reusable LAB patterns, not just tests:

Pattern 1 — Frozen Fixture Snapshot
Pattern 2 — Canon Version Reference
Pattern 3 — Two-Pass Match Before Disagree
Pattern 4 — Hard Gate Before Soft Score
Pattern 5 — Case-Specific Rubric
Pattern 6 — Fixture Hash Manifest
Pattern 7 — Non-Authoritative Candidate Wrapper
Pattern 8 — Box Shield Import Guard

This makes the lab extensible without weakening governance.
5. Evaluating Machine Learning Models — Alice Zheng

Why it matters: O’Reilly describes this as a guide to model evaluation basics, model-selection metrics, hyperparameter tuning, and A/B testing.

Real gain for our project: metrics must be task-specific. We should not create one global “accuracy” score. For routing logic, each task class needs its own score profile:

freeze workflow cases → hard governance gates matter most
prompt selection cases → prompt recall/precision matter most
missing-context cases → missing-context detection matters most
adversarial cases → forbidden-action avoidance matters most
medical/document distinction cases → route classification matters most

This directly improves reliability because the lab will not hide a dangerous failure behind a high average score.
What the books add on top of AI audits + web specialist sites

The AI specialists gave us good architecture warnings. The web sources added risk/security discipline. The books add engineering maturity.

The strongest external-site ideas still remain useful: NIST says AI risk should be incorporated into design, development, use, and evaluation, not added at the end. OWASP’s LLM Top 10 makes prompt injection and insecure output handling hard security categories, not optional tests. OpenAI Evals reinforces private, workflow-specific evals; for KANDA this means project-specific tests like “go next,” stale freeze output, patch validation, prompt authoring, and bypass attempts. Anthropic’s guidance adds the rule that success criteria must be specific and measurable before test design.
Updated LAB/Test implementation logic — v2

This is the updated logic after combining:

1. AI specialist audits
2. specialist websites
3. five-book review
4. P0–P12 frozen boundaries

Phase 0 — no-code governance start

LAB-0 — Phase Boundary + Lab Charter / Entry Gate

Purpose: formally open the LAB phase after P12. No Python logic yet.

Artifacts:

LAB_PHASE_BOUNDARY.md
LAB_CHARTER.md
LAB_FORBIDDEN_BEHAVIORS.md
LAB_STOP_CONDITIONS.md
LAB_ALLOWED_ARTIFACTS.md

Real gain from books: prevents premature implementation before the evaluation system has a defined mission.
Phase 1 — success and risk definition before schema

LAB-0A — Success Criteria Matrix
LAB-0B — Risk-Control Matrix
LAB-0C — LAB SLO / Critical Error Budget Declaration

This is a major update. Before creating schema or tests, we define what success and failure mean.

Success criteria:

correct route classification
correct fast-path vs routed-work distinction
correct prompt group selection
correct missing-context detection
correct forbidden-action avoidance
correct box-boundary preservation
correct yield-to-canon behavior
correct explanation completeness

Critical error budget:

0 runtime authority
0 prompt loading
0 persistence
0 provider calls
0 embedding/vector calls
0 canon mutation
0 freeze-memory mutation
0 gold/registry mutation
0 activation key
0 field-test mode
0 Copilot behavior

Real gain from Reliable Machine Learning: SRE-style error budget becomes enforceable.
Phase 2 — one isolated LAB box

LAB-1 — Lab Box Boundary + Shielding Manifest

One primary box:

kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/

Hard shield rules:

production must not import lab
lab must not import runtime router
lab must not import prompt loader
lab must not import provider modules
lab must not import embedding/vector modules
lab must not import PySide6/UI
lab must not write outside lab box
lab must not mutate canon, prompt library, freeze memory, gold, registry

Real gain from Machine Learning Design Patterns: this becomes a reusable Box Shield Pattern, not just a note in README.
Phase 3 — failure taxonomy before scoring and tests

LAB-2 — Failure Taxonomy + Critical Violation Model

Core categories:

FALSE_FAST_PATH
MISSED_ROUTED_WORK
INCORRECT_ROUTE
PROMPT_OMISSION
PROMPT_EXCESS
PROMPT_PRIORITY_ERROR
MISSING_CONTEXT_FAILURE
STALE_CONTEXT_ACCEPTANCE
HANDOFF_CORRUPTION
FALSE_CERTAINTY
EXPLANATION_MISMATCH
SCHEMA_VIOLATION
FIXTURE_CONTAMINATION
BOX_LEAKAGE
ROUTE_AUTHORITY_OVERRIDE
UNAUTHORIZED_PROMPT_LOAD
RUNTIME_ACTION
CANON_MUTATION
PERSISTENCE_ATTEMPT
PROVIDER_CALL_ATTEMPT
ACTIVATION_KEY_ATTEMPT
MATCH_BEFORE_DISAGREE_VIOLATION

Real gain: the lab tests exactly the failures we fear, not generic “accuracy.”
Phase 4 — scoring model with hard gates first

LAB-3 — Scoring Model + Hard Gates

No single aggregate score can hide a critical failure.

Hard gates:

critical boundary violation = total fail
forbidden action attempted = total fail
match-before-disagree skipped = total fail
schema invalid = fail
fixture hash mismatch = lab invalid

Soft metrics:

route exact match
prompt recall
prompt precision
missing-context detection
stale-context rejection
disagreement quality
explanation fidelity
confidence calibration

Real gain from Evaluating Machine Learning Models: metrics are task-specific and tied to the evaluation task, not generic.
Phase 5 — schema with versioning and two-pass logic

LAB-4 — Test Case Schema + Candidate Output Contract

Updated schema fields:

case_id
case_version
schema_version
corpus_version
canon_version_reference
canon_rule_references
category
subcategory
severity
critical_boundary_flag
adversarial_flag
regression_source
user_request_raw
normalized_request
conversation_history
simulated_context
context_freshness
simulated_freeze_state
simulated_handoff_state
simulated_sidecar_state
expected_task_classification
expected_path
expected_required_prompt_groups
expected_prompt_priority
expected_missing_context
expected_forbidden_actions
expected_safe_next_action
expected_explanation_elements
case_specific_pass_conditions
case_specific_fail_conditions
case_specific_critical_fail_conditions
candidate_pass_1_canon_match
candidate_pass_2_disagreement
yield_to_canon

Real gain from AI Engineering and Designing ML Systems: everything is versioned, traceable, and comparable across runs.
Phase 6 — frozen fixture design

LAB-5 — Frozen Canon Fixture Format + Hash Manifest

Important rule:

fixtures are copied snapshots, not live canon references

Each fixture must have:

fixture_hash
canon_version_reference
source_freeze_id
created_at_utc
review_status

Real gain: prevents hidden coupling to live prompt canon or freeze memory.
Phase 7 — deterministic runner only

LAB-6 — Deterministic Runner Skeleton

Runner can:

load fixtures
validate schema
validate fixture hashes
load candidate-output JSON
compare expected vs actual
produce structured report

Runner cannot:

call model
load prompt
route user request
write outside lab
call provider
run async event loop
touch PySide6
persist decisions

Real gain: the lab becomes a pure evaluator, not a prototype runtime router.
Phase 8 — lab tests itself before testing ML

LAB-7 — Lab Self-Validation Gate

Mandatory self-tests:

gold-vs-gold = PASS
wrong route = FAIL
missing prompt = FAIL
forbidden action = CRITICAL_FAIL
fixture hash mismatch = LAB_INVALID
skipped pass-1 match = CRITICAL_FAIL
box leakage fixture = CRITICAL_FAIL

Real gain from the audits and books: we do not trust the lab until the lab proves it can catch known failures.
Phase 9 — small curated alpha corpus

LAB-8 — Alpha Corpus Seed

Do not start with 200+ tests.

Initial alpha:

60–80 curated tests
100% manually reviewed
all linked to canon/freeze/governance rule references
all with fixture hashes

Distribution:

10 basic routing classification
10 fast-path vs routed-work
8 required prompt/group selection
8 missing-context / may-proceed-now
6 freeze/update/governance workflow
6 prompt-library / prompt-authoring
6 patch / installer / validation / freeze-memory
6 box boundary / leakage
5 stale context / stale filename / stale sidecar
5 adversarial bypass / prompt injection
4 typo / shorthand / ambiguous
3 medical/document/simple-task distinction
3 regression from known past mistakes

Real gain: high quality before volume. We avoid 250 weak tests that later need rewriting.
Phase 10 — offline observability report

LAB-9 — Offline Observability + Experiment Report

Every run produces:

lab_run_id
runner_version
schema_version
corpus_version
candidate_version
canon_version_reference
started_at_utc
ended_at_utc
duration_ms
tests_total
tests_passed
tests_failed
critical_failures
category_scores
coverage_gaps
fixture_hash_manifest

Real gain from Reliable ML and ML systems books: visibility and versioning become part of the design.
Phase 11 — candidate harness, still non-runtime

LAB-10 — Candidate Evaluation Harness Interface

Candidate output enters only as:

non_authoritative_evaluation_record

It cannot be converted into:

route decision
prompt loading command
approval
activation
runtime action
freeze write
human decision record

Real gain: ML remains subordinate.
Phase 12 — expand corpus only after stability

LAB-11 — Corpus V1 Expansion

Expansion target:

~100 tests after runner/scoring/schema are stable

Later:

200–250 only after candidate harness is working
300–500+ only through real regression/error canonization

Real gain: corpus grows from evidence, not speculation.
Phase 13 — error canonization intake spec only

LAB-12 — Error Canonization Intake Spec

Design only. No automatic mutation yet.

It defines how future failures become regression candidates:

failure observed
failure classified
human review
canon/regression candidate drafted
separate governed update
freeze after validation

Real gain: recurring mistakes become permanent tests later, but without creating autonomous mutation too early.
Phase 14 — lab closure / readiness review

LAB-13 — Lab Closure / Next-Phase Readiness Review

Closure asks:

Is the lab isolated?
Are hard gates working?
Are fixture hashes stable?
Is self-validation passing?
Is corpus coverage adequate?
Are critical violations zero?
Are reports reproducible?
Can candidate output reach runtime? If yes, fail.

Real gain: no vague “ready.” The lab must prove maturity.
What changed from our previous logic

The updated logic adds these real gains:

Success criteria before schema.
Risk-control matrix before implementation.
SRE-style critical error budget.
Versioned evaluation assets.
Fixture hash manifest.
Case-specific rubrics.
Two-pass match-before-disagree contract.
Lab self-validation gate.
Offline observability report.
Candidate output wrapper.
Corpus growth strategy.
Error canonization as future governed intake, not automatic mutation.

What I still reject

Even after the book review, I would not add these now:

live LLM provider calls
LLM-as-judge as primary grader
adaptive rubric generation
automatic synthetic test generation
persistent ML decision database
batch mode
runtime shadow mode
activation key
field-test mode
Copilot behavior
production monitoring
external dependency stack
Docker
cloud eval platform

Those may become useful later, but they are not safe for LAB-0 to LAB-8.
Final updated LAB mission

The KANDA LAB is a deterministic, isolated, non-runtime evaluation system for testing whether future ML/router candidates can reproduce frozen router governance, select required prompt groups, detect missing or stale context, reject bypass attempts, preserve box boundaries, explain disagreements without overriding canon, and produce reproducible audit reports.

The LAB does not route, load prompts, persist ML decisions, call providers, mutate canon, mutate freeze memory, activate Pilot, activate Copilot, or field-test anything.

The next safe step remains:

LAB-0 — Phase Boundary + Lab Charter / Entry Gate

No code yet. No ML candidate yet. No test runner yet.

first is best canonize it in router prompt logic, isn't it?

Yes — that is the best first move.

Before implementing LAB-0 or any lab/test logic, we should first canonize the LAB phase in the router prompt logic.

Reason: if we do not canonize it first, future “next / continue / go” commands may be misrouted as:

continue ML implementation
start test runner
start candidate harness
start Copilot boundary
start activation-gate work

But the correct post-P12 behavior is:

P12 frozen → STOP → ask/confirm before LAB → route only to LAB-0 charter first

P12 already froze that after P12 the next behavior is STOP and that any test-lab design/coding requires warning and confirmation.

So the next safe step should be:

RG-LAB-000 — Router Prompt Logic Canon for LAB Phase Entry

Not LAB implementation yet.

What this canon should lock:

After P12 freeze, “next” does not mean runtime ML.
After P12 freeze, “next” does not mean direct lab coding.
After P12 freeze, “next” means LAB phase routing begins.
First allowed milestone is LAB-0: Phase Boundary + Lab Charter / Entry Gate.
LAB-0 is documentation-only.
No runner, schema, fixtures, corpus, candidate harness, provider calls, prompt loading, persistence, activation key, field-test mode, or Copilot behavior may be created in LAB-0.
All LAB work is Routed Work Path.
All LAB work requires Box Architecture boundary audit.
Each LAB milestone must be frozen before the next.

I would canonize these routing rules first:

1. Post-P12 LAB Entry Rule
2. LAB versus ML Implementation Distinction Rule
3. LAB Milestone Order Rule
4. LAB-0 Documentation-Only Rule
5. No Runtime / No Authority Rule
6. Match-Before-Disagree Lab Doctrine Rule
7. Hard-Gate / Zero Critical Boundary Error Rule
8. Lab Box Isolation Rule
9. Lab Corpus Growth Rule
10. Stop-and-Warn Rule before any test-lab coding

So yes: first canonize the LAB routing logic, then freeze it, then only after that begin LAB-0.

The next governed task should be:

Create a patch for RG-LAB-000 — Router Prompt Logic Canon for LAB Phase Entry.


and remember logic flux that after ML lab/test has fulfilled the mission been tested for reliability and also after  testing ML router prompt logic for reliability, then we continue ML logic implementation

Yes — saved.

This becomes the correct roadmap rule:

P12 frozen
→ first canonize LAB phase routing logic in router prompt logic
→ then implement ML LAB/test phase
→ then test the LAB itself for reliability
→ then use the LAB to test ML router prompt logic reliability
→ only after that continue ML logic implementation

So the next logic is not:

P12 → continue ML implementation

It is:

P12 → RG-LAB-000 canonization → LAB reliability → ML router prompt logic reliability → continue ML implementation

This also matches the frozen P12 boundary: after P12, the system must stop and warn before any test-lab work begins.

canonize it

I’ll treat this as a governed routing-canon patch, not LAB implementation. I’ll inspect the current project/startup files, add only the LAB-entry canon/routing rule, validate it, and package an install ZIP.

I found the active routing assets that need the canon hook: ai_prompt_request_canon, prompt_navigation_index, prompt_router, the routing/folder indexes, metadata, and the startup ZIP generated from those indexes. I’m adding a new RG-LAB-000 on-request canon rather than overloading the older RG-PILOT-000 prompt.

Canonization patch is ready.

This patch does not implement LAB/test logic. It only canonizes the routing rule:

P12 frozen
→ RG-LAB-000 canonization
→ LAB-0 charter only
→ LAB/test reliability
→ ML router prompt logic reliability
→ only then continue ML implementation

P12 already froze the STOP-before-LAB boundary, so this patch makes that route explicit in the router prompt logic.

Download:

SHA-256:

8957edf5b1c48ea7a5e6dc0e8d801131f507e60389462eccba64c2f1affd52c2

Sandbox validation passed:

VALIDATION OK: rg_lab_000_ml_lab_phase_entry_router_canon_v1
CONTRACT_TEST_OK: RG-LAB-000 ML LAB Phase Entry Router Canon v1, immutable governed post-P12 routing-canon boundary after P12 freeze and FREEZE_MEMORY_STATUS OK, canonizes LAB entry first, LAB-0 documentation-only, LAB reliability before ML router prompt logic reliability testing, ML router prompt logic reliability before continuing ML implementation, no LAB code, no schema code, no fixtures, no corpus, no runner, no candidate harness, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, startup routing pack refreshed and STATUS: IN_SYNC, routing indexes and metadata updated, on-request not startup-always-loaded preserved, zero critical boundary doctrine preserved
SANDBOX_RG_LAB_000_ML_LAB_PHASE_ENTRY_ROUTER_CANON_V1_VALIDATION_OK

Save the ZIP here first:

E:\rg_lab_000_ml_lab_phase_entry_router_canon_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "rg_lab_000_ml_lab_phase_entry_router_canon_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_prompt_workspace\first_AI_deliver\first_prompts_to_ai.zip",
        "kanda_prompt_workspace\first_AI_deliver\paste_after_first_prompts_to_ai.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\01_session_start_and_navigation\ai_prompt_request_canon.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\_FOLDER_ASSIMILATION.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\prompt_navigation_index.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\prompt_router.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\routing_signal_scorer_v3_lab_phase_entry_router_canon.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md",
        "kanda_prompt_workspace\prompt_library\METADATA\routing_signal_scorer_v3_lab_phase_entry_router_canon.meta.json",
        "kanda_prompt_workspace\prompt_library\ROUTING\FOLDER_ASSIMILATION_CARDS_INDEX.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\GROUP_ASSIMILATION_INDEX.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\PROMPT_NAVIGATION_INDEX.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\folder_assimilation_cards_index.json",
        "kanda_prompt_workspace\prompt_library\ROUTING\group_assimilation_index.json",
        "kanda_prompt_workspace\prompt_library\ROUTING\prompt_navigation_index.json",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_prompt_workspace\first_AI_deliver\first_prompts_to_ai.zip",
        "kanda_prompt_workspace\first_AI_deliver\paste_after_first_prompts_to_ai.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\01_session_start_and_navigation\ai_prompt_request_canon.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\_FOLDER_ASSIMILATION.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\prompt_navigation_index.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\prompt_router.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\routing_signal_scorer_v3_lab_phase_entry_router_canon.md",
        "kanda_prompt_workspace\prompt_library\ACTIVE_PROMPTS\02_prompt_routing_and_indexing\routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md",
        "kanda_prompt_workspace\prompt_library\METADATA\routing_signal_scorer_v3_lab_phase_entry_router_canon.meta.json",
        "kanda_prompt_workspace\prompt_library\ROUTING\FOLDER_ASSIMILATION_CARDS_INDEX.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\GROUP_ASSIMILATION_INDEX.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\PROMPT_NAVIGATION_INDEX.md",
        "kanda_prompt_workspace\prompt_library\ROUTING\folder_assimilation_cards_index.json",
        "kanda_prompt_workspace\prompt_library\ROUTING\group_assimilation_index.json",
        "kanda_prompt_workspace\prompt_library\ROUTING\prompt_navigation_index.json",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: rg_lab_000_ml_lab_phase_entry_router_canon_v1 installed."
    Write-Host "RG-LAB-000 routing canon installed."
    Write-Host "No LAB code, schema, fixtures, corpus, runner, candidate harness, ML implementation, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    Write-Host ""
    Write-Host "Refreshing startup routing kernel pack for the local project root..."
    python kanda_prompt_workspace\prompt_tools\sync_startup_routing_kernel_pack.py --sync --yes --workspace kanda_prompt_workspace --project-root .
    if ($LASTEXITCODE -ne 0) {
        throw "startup routing kernel sync failed"
    }

    $TESTS = @(
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_kanda_routing_system_canon_registration.py",
        "tests\test_kbsc_routing_registration.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    Write-Host ""
    Write-Host "CHECKING STARTUP ROUTING KERNEL:"
    python kanda_prompt_workspace\prompt_tools\sync_startup_routing_kernel_pack.py --check --workspace kanda_prompt_workspace --project-root .
    if ($LASTEXITCODE -ne 0) {
        throw "startup routing kernel check failed"
    }

    Write-Host ""
    Write-Host "VALIDATION OK: rg_lab_000_ml_lab_phase_entry_router_canon_v1"
    Write-Host "CONTRACT_TEST_OK: RG-LAB-000 ML LAB Phase Entry Router Canon v1, immutable governed post-P12 routing-canon boundary after P12 freeze and FREEZE_MEMORY_STATUS OK, canonizes LAB entry first, LAB-0 documentation-only, LAB reliability before ML router prompt logic reliability testing, ML router prompt logic reliability before continuing ML implementation, no LAB code, no schema code, no fixtures, no corpus, no runner, no candidate harness, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, startup routing pack refreshed and STATUS: IN_SYNC, routing indexes and metadata updated, on-request not startup-always-loaded preserved, zero critical boundary doctrine preserved"
    Write-Host "SANDBOX_RG_LAB_000_ML_LAB_PHASE_ENTRY_ROUTER_CANON_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "rg_lab_000_ml_lab_phase_entry_router_canon_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

RG-LAB-000 ML LAB Phase Entry Router Canon v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone becomes:

LAB-0 — Phase Boundary + Lab Charter / Entry Gate

LAB-0 must still be documentation-only.

Pasted text.txt
Document
next

RG-LAB-000 is frozen with FREEZE_MEMORY_STATUS: OK, so the route is now allowed to move to the first LAB milestone. I’ll keep LAB-0 documentation-only: no runner, schema, fixtures, corpus, ML candidate, prompt loading, persistence, or runtime authority.

RG-LAB-000 is frozen correctly. The uploaded output shows:

LOCAL FREEZE WRITE OK
Freeze ID: freeze-20260619-rg-lab-000-ml-lab-phase-entry-router-canon-v1
FREEZE_MEMORY_STATUS: OK

So the next safe milestone is now LAB-0 — Phase Boundary + Lab Charter / Entry Gate.

I created the LAB-0 patch. It is documentation-only and does not add LAB code, schema, fixtures, corpus, runner, candidate harness, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior.

Download:

SHA-256:

fba7932ec29704454e0a7130ade2ca9ba5943d1447735184a2628be504ad8fba

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1
CONTRACT_TEST_OK: LAB-0 ML LAB Phase Boundary / Charter Entry Gate v1, immutable governed post-RG-LAB-000 documentation-only entry gate after P12 and RG-LAB-000 freeze with FREEZE_MEMORY_STATUS OK, LAB-0 phase boundary and charter only, LAB-0A Success Criteria Matrix next, no LAB code, no schema code, no fixtures, no corpus, no runner, no candidate harness, no metrics engine, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, ML implementation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, zero critical boundary doctrine preserved
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_PHASE_BOUNDARY_CHARTER_ENTRY_GATE_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_CHARTER.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_FORBIDDEN_BEHAVIORS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_STOP_CONDITIONS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_CHARTER.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_FORBIDDEN_BEHAVIORS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_STOP_CONDITIONS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1 installed."
    Write-Host "LAB-0 documentation-only phase boundary and charter installed."
    Write-Host "No LAB code, schema, fixtures, corpus, runner, candidate harness, metrics engine, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-0 boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-0 ML LAB Phase Boundary / Charter Entry Gate v1, immutable governed post-RG-LAB-000 documentation-only entry gate after P12 and RG-LAB-000 freeze with FREEZE_MEMORY_STATUS OK, LAB-0 phase boundary and charter only, LAB-0A Success Criteria Matrix next, no LAB code, no schema code, no fixtures, no corpus, no runner, no candidate harness, no metrics engine, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, ML implementation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, zero critical boundary doctrine preserved"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_PHASE_BOUNDARY_CHARTER_ENTRY_GATE_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Phase Boundary / Charter Entry Gate v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-0A — Success Criteria Matrix

That next milestone must also remain documentation/governance only.

Pasted text.txt
Document

LAB-0 is frozen with LOCAL FREEZE WRITE OK and FREEZE_MEMORY_STATUS: OK; the freeze text also says LAB-0A Success Criteria Matrix is the next safe milestone. I’ll create LAB-0A as documentation/governance only.

LAB-0 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and explicitly says the next safe milestone is LAB-0A Success Criteria Matrix.

I created the LAB-0A patch. It is documentation/governance only.

It adds the success criteria matrix and does not add LAB code, schema code, fixtures, corpus, runner, metrics engine, candidate harness, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior.

Download:

SHA-256:

465363ea62989e62071e789a3a3216d7368da1707c7212e2be33fc587f938889

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1
CONTRACT_TEST_OK: LAB-0A ML LAB Success Criteria Matrix v1, immutable governed documentation-only success criteria matrix after LAB-0 freeze with FREEZE_MEMORY_STATUS OK, defines specific measurable success criteria, hard gates before soft scores, zero critical boundary error budget, future lab self-validation readiness, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no metrics engine, no candidate harness, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-0B Risk-Control Matrix next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SUCCESS_CRITERIA_MATRIX_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_SUCCESS_CRITERIA_MATRIX.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_SUCCESS_CRITERIA_MATRIX.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1 installed."
    Write-Host "LAB-0A documentation-only success criteria matrix installed."
    Write-Host "No LAB code, schema, fixtures, corpus, runner, metrics engine, candidate harness, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-0A boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-0A ML LAB Success Criteria Matrix v1, immutable governed documentation-only success criteria matrix after LAB-0 freeze with FREEZE_MEMORY_STATUS OK, defines specific measurable success criteria, hard gates before soft scores, zero critical boundary error budget, future lab self-validation readiness, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no metrics engine, no candidate harness, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-0B Risk-Control Matrix next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SUCCESS_CRITERIA_MATRIX_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Success Criteria Matrix v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-0B — Risk-Control Matrix

LAB-0B must also remain documentation/governance only.

Pasted text.txt
Document
continue

LAB-0A is frozen correctly. The uploaded output shows:

LOCAL FREEZE WRITE OK
Freeze ID: freeze-20260619-routing-signal-scorer-v3-ml-lab-success-criteria-matrix-v1
FREEZE_MEMORY_STATUS: OK

It also states the next safe milestone is LAB-0B — Risk-Control Matrix, documentation-only.

I created the LAB-0B patch.

It adds a documentation-only risk-control matrix and does not add LAB code, schema code, fixtures, corpus, runner, metrics engine, candidate harness, live risk detectors, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior.

Download:

SHA-256:

97d7cffadb6e412d1471fabec1277b9a7c9e4cbcd90b2602063950ed61a52b84

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1
CONTRACT_TEST_OK: LAB-0B ML LAB Risk-Control Matrix v1, immutable governed documentation-only risk-control matrix after LAB-0A freeze with FREEZE_MEMORY_STATUS OK, maps prompt injection, insecure output handling, route authority, prompt loading, persistence, provider/embedding, box leakage, fixture contamination, live canon coupling, stale context, missing context, false confidence, match-before-disagree, human review, activation drift, training-data drift, batch/async drift, sensitive leakage, supply-chain drift, and lab self-validation risks to future controls, zero critical boundary error budget preserved, hard controls before soft performance preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no metrics engine, no candidate harness, no live risk detectors, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-0C LAB SLO / Critical Error Budget Declaration next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_RISK_CONTROL_MATRIX_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_RISK_CONTROL_MATRIX.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_RISK_CONTROL_MATRIX.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1 installed."
    Write-Host "LAB-0B documentation-only risk-control matrix installed."
    Write-Host "No LAB code, schema, fixtures, corpus, runner, metrics engine, candidate harness, live risk detectors, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-0B boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-0B ML LAB Risk-Control Matrix v1, immutable governed documentation-only risk-control matrix after LAB-0A freeze with FREEZE_MEMORY_STATUS OK, maps prompt injection, insecure output handling, route authority, prompt loading, persistence, provider/embedding, box leakage, fixture contamination, live canon coupling, stale context, missing context, false confidence, match-before-disagree, human review, activation drift, training-data drift, batch/async drift, sensitive leakage, supply-chain drift, and lab self-validation risks to future controls, zero critical boundary error budget preserved, hard controls before soft performance preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no metrics engine, no candidate harness, no live risk detectors, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-0C LAB SLO / Critical Error Budget Declaration next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_RISK_CONTROL_MATRIX_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Risk-Control Matrix v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-0C — LAB SLO / Critical Error Budget Declaration

LAB-0C must also remain documentation/governance only.

Pasted text.txt
Document

LAB-0B is frozen with FREEZE_MEMORY_STATUS: OK; the freeze output names LAB-0C as the next safe milestone. I’ll create LAB-0C as documentation/governance only: no implementation code or live controls.

LAB-0B freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-0C — LAB SLO / Critical Error Budget Declaration as the next safe milestone.

I created the LAB-0C patch.

It is documentation/governance only. It declares the LAB SLO and critical error budget, but adds no LAB implementation code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live risk detectors, no prompt loading, no persistence, no provider calls, no embeddings, no batch mode, no activation key, no field-test mode, no runtime Pilot, and no Copilot behavior.

Download:

SHA-256:

5257725f68c349710400203c3fb7092551c38e2bba1b2a9d98eaacdac6c29a11

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1
CONTRACT_TEST_OK: LAB-0C ML LAB SLO / Critical Error Budget Declaration v1, immutable governed documentation-only SLO and critical error-budget declaration after LAB-0B freeze with FREEZE_MEMORY_STATUS OK, declares critical boundary error budget zero, hard gates before soft scores, incident-style critical failure handling, LAB_INVALID handling for fixture integrity or LAB self-validation bypass, reliability claims blocked until LAB self-validation, fixture integrity, zero critical boundary violations, coverage, soft thresholds, human review, and freeze evidence are satisfied, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live risk detectors, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-1 Lab Box Boundary + Shielding Manifest next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SLO_CRITICAL_ERROR_BUDGET_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_SLO_CRITICAL_ERROR_BUDGET.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_SLO_CRITICAL_ERROR_BUDGET.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1 installed."
    Write-Host "LAB-0C documentation-only LAB SLO / Critical Error Budget Declaration installed."
    Write-Host "No LAB code, schema, fixtures, corpus, runner, scoring engine, metrics engine, candidate harness, live risk detectors, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-0C boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-0C ML LAB SLO / Critical Error Budget Declaration v1, immutable governed documentation-only SLO and critical error-budget declaration after LAB-0B freeze with FREEZE_MEMORY_STATUS OK, declares critical boundary error budget zero, hard gates before soft scores, incident-style critical failure handling, LAB_INVALID handling for fixture integrity or LAB self-validation bypass, reliability claims blocked until LAB self-validation, fixture integrity, zero critical boundary violations, coverage, soft thresholds, human review, and freeze evidence are satisfied, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live risk detectors, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-1 Lab Box Boundary + Shielding Manifest next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SLO_CRITICAL_ERROR_BUDGET_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB SLO / Critical Error Budget Declaration v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-1 — Lab Box Boundary + Shielding Manifest

LAB-1 must still be governed boundary/shielding work, not runtime ML implementation.

Pasted text.txt
Document

LAB-0C is now frozen and the next milestone is LAB-1. I’m building LAB-1 as a shielding/boundary manifest only, so it strengthens the box barrier before any lab code, schema, fixtures, or runner exists.

LAB-0C freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-1 — Lab Box Boundary + Shielding Manifest as the next safe milestone.

I created the LAB-1 patch.

It is documentation/governance only. It adds the box boundary and shielding manifest, but adds no LAB implementation code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live risk detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no batch mode, no activation key, no field-test mode, no runtime Pilot, and no Copilot behavior.

Download:

SHA-256:

1ba63d3694360eefd71093144b853fb7d4b46a55fb45f226755ace5c1dd2430e

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1
CONTRACT_TEST_OK: LAB-1 ML LAB Box Boundary + Shielding Manifest v1, immutable governed documentation-only shielding manifest after LAB-0C freeze with FREEZE_MEMORY_STATUS OK, declares primary LAB box, public Markdown-only surface, no Python LAB modules, one-way dependency rule, forbidden imports, forbidden writes, static fixture read model, non-authoritative candidate output shielding, fixture shielding, human review shielding, reliability shielding, future enforcement expectations, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live risk detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-2 Failure Taxonomy + Critical Violation Model next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_BOX_BOUNDARY_SHIELDING_MANIFEST_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_BOX_BOUNDARY_SHIELDING_MANIFEST.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_BOX_BOUNDARY_SHIELDING_MANIFEST.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1 installed."
    Write-Host "LAB-1 documentation-only Lab Box Boundary + Shielding Manifest installed."
    Write-Host "No LAB code, schema, fixtures, corpus, runner, scoring engine, metrics engine, candidate harness, live risk detectors, import scanner, write guard, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-1 boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-1 ML LAB Box Boundary + Shielding Manifest v1, immutable governed documentation-only shielding manifest after LAB-0C freeze with FREEZE_MEMORY_STATUS OK, declares primary LAB box, public Markdown-only surface, no Python LAB modules, one-way dependency rule, forbidden imports, forbidden writes, static fixture read model, non-authoritative candidate output shielding, fixture shielding, human review shielding, reliability shielding, future enforcement expectations, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live risk detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-2 Failure Taxonomy + Critical Violation Model next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_BOX_BOUNDARY_SHIELDING_MANIFEST_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Box Boundary + Shielding Manifest v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-2 — Failure Taxonomy + Critical Violation Model

LAB-2 must remain governed taxonomy/design work, not runtime ML implementation.

Pasted text.txt
Document
continue

LAB-1 is frozen with FREEZE_MEMORY_STATUS: OK, and the freeze output names LAB-2 as the next milestone. I’ll keep LAB-2 as taxonomy/design only, not implementation.

LAB-1 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-2 — Failure Taxonomy + Critical Violation Model as the next safe milestone.

I created the LAB-2 patch.

It is documentation/governance only. It defines outcome vocabulary, failure families, critical violation classes, LAB_INVALID classes, soft-failure classes, ambiguity rules, multi-turn failure rules, and the roadmap lock. It adds no LAB implementation code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no batch mode, no activation key, no field-test mode, no runtime Pilot, and no Copilot behavior.

Download:

SHA-256:

1ab473c1813cbd57475b458f0ace6603dc6291f319c06977381a4a44bd2f85e7

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1
CONTRACT_TEST_OK: LAB-2 ML LAB Failure Taxonomy + Critical Violation Model v1, immutable governed documentation-only failure taxonomy after LAB-1 freeze with FREEZE_MEMORY_STATUS OK, defines outcome vocabulary, severity levels, failure families, detailed failure codes, critical violation classes, LAB_INVALID classes, soft-failure classes, ambiguity rule, multi-turn failure rule, roadmap lock, hard-gate-before-soft-score doctrine, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-3 Scoring Model + Hard Gates next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_FAILURE_TAXONOMY_CRITICAL_VIOLATION_MODEL_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_FAILURE_TAXONOMY_CRITICAL_VIOLATION_MODEL.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_FAILURE_TAXONOMY_CRITICAL_VIOLATION_MODEL.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1 installed."
    Write-Host "LAB-2 documentation-only Failure Taxonomy + Critical Violation Model installed."
    Write-Host "No LAB code, schema, fixtures, corpus, runner, scoring engine, metrics engine, candidate harness, live detectors, import scanner, write guard, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-2 boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-2 ML LAB Failure Taxonomy + Critical Violation Model v1, immutable governed documentation-only failure taxonomy after LAB-1 freeze with FREEZE_MEMORY_STATUS OK, defines outcome vocabulary, severity levels, failure families, detailed failure codes, critical violation classes, LAB_INVALID classes, soft-failure classes, ambiguity rule, multi-turn failure rule, roadmap lock, hard-gate-before-soft-score doctrine, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-3 Scoring Model + Hard Gates next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_FAILURE_TAXONOMY_CRITICAL_VIOLATION_MODEL_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Failure Taxonomy + Critical Violation Model v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-3 — Scoring Model + Hard Gates

LAB-3 must remain governed scoring design, not runtime ML implementation.

Pasted text.txt
Document
continue

LAB-2 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-3 — Scoring Model + Hard Gates as the next safe milestone.

I created the LAB-3 patch.

It is documentation/governance only. It defines the scoring model, hard-gate precedence, non-compensation rule, LAB_INVALID handling, critical boundary gates, governance gates, soft metrics, category-specific score profiles, reliability claim preconditions, report expectations, match-before-disagree scoring, and human-review scoring.

It adds no LAB implementation code, no schema code, no fixtures, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no batch mode, no activation key, no field-test mode, no runtime Pilot, and no Copilot behavior.

Download:

SHA-256:

6f16a705728cacc554ad03674406deaa59312de875fd5595f0ce4980dd551c36

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1
CONTRACT_TEST_OK: LAB-3 ML LAB Scoring Model + Hard Gates v1, immutable governed documentation-only scoring model after LAB-2 freeze with FREEZE_MEMORY_STATUS OK, defines fixed scoring order, outcome precedence, non-compensation rule, LAB_INVALID gates, critical boundary hard gates, governance hard gates, task-specific hard gates, soft metrics, category-specific score profiles, minimum reliability claim preconditions, reliability labels, report expectations, match-before-disagree scoring, human-review scoring, roadmap lock, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-4 Test Case Schema + Candidate Output Contract next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SCORING_MODEL_HARD_GATES_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_SCORING_MODEL_HARD_GATES.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_SCORING_MODEL_HARD_GATES.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1 installed."
    Write-Host "LAB-3 documentation-only Scoring Model + Hard Gates installed."
    Write-Host "No LAB code, schema, fixtures, corpus, runner, executable scoring engine, metrics engine, candidate harness, live detectors, import scanner, write guard, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-3 boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-3 ML LAB Scoring Model + Hard Gates v1, immutable governed documentation-only scoring model after LAB-2 freeze with FREEZE_MEMORY_STATUS OK, defines fixed scoring order, outcome precedence, non-compensation rule, LAB_INVALID gates, critical boundary hard gates, governance hard gates, task-specific hard gates, soft metrics, category-specific score profiles, minimum reliability claim preconditions, reliability labels, report expectations, match-before-disagree scoring, human-review scoring, roadmap lock, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-4 Test Case Schema + Candidate Output Contract next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SCORING_MODEL_HARD_GATES_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Scoring Model + Hard Gates v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-4 — Test Case Schema + Candidate Output Contract

LAB-4 must remain governed schema/contract design, not runtime ML implementation.

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-3 boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-3 ML LAB Scoring Model + Hard Gates v1, immutable governed documentation-only scoring model after LAB-2 freeze with FREEZE_MEMORY_STATUS OK, defines fixed scoring order, outcome precedence, non-compensation rule, LAB_INVALID gates, critical boundary hard gates, governance hard gates, task-specific hard gates, soft metrics, category-specific score profiles, minimum reliability claim preconditions, reliability labels, report expectations, match-before-disagree scoring, human-review scoring, roadmap lock, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no fixtures, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-4 Test Case Schema + Candidate Output Contract next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SCORING_MODEL_HARD_GATES_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

This is the validation block itself, not the validation output.

So I cannot yet treat LAB-3 as validated or frozen, and I should not continue to LAB-4 yet.

Please run that block in PowerShell. The successful output must include:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1
CONTRACT_TEST_OK: LAB-3 ML LAB Scoring Model + Hard Gates v1
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SCORING_MODEL_HARD_GATES_V1_VALIDATION_OK

Then freeze as:

Routing Signal Scorer v3 ML LAB Scoring Model + Hard Gates v1

Required freeze result:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After you paste the freeze output, I can safely continue to:

LAB-4 — Test Case Schema + Candidate Output Contract


Pasted text.txt
Document
continue

LAB-3 is now frozen with FREEZE_MEMORY_STATUS: OK, and the freeze output names LAB-4 as the next safe milestone. I’ll keep LAB-4 as schema/contract design only, with no executable lab machinery.

LAB-3 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-4 — Test Case Schema + Candidate Output Contract as the next safe milestone.

I created the LAB-4 patch.

It is documentation/governance only. It defines the future test case record shape, candidate output record shape, required version/canon-reference fields, case-specific pass/fail/critical-fail rubric fields, two-pass match-before-disagree contract, non-authoritative candidate wrapper, forbidden authority fields, rejection rules, LAB_INVALID handling for malformed gold cases, human-review contract, case category labels, and version compatibility rules.

It adds no LAB code, no schema code, no executable validators, no fixtures, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no batch mode, no activation key, no field-test mode, no runtime Pilot, and no Copilot behavior.

Download:

SHA-256:

11fc49cd56517a58bfbb492b361aeebc19db1b651d711e0f794070585a085709

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1
CONTRACT_TEST_OK: LAB-4 ML LAB Test Case Schema + Candidate Output Contract v1, immutable governed documentation-only schema/contract design after LAB-3 freeze with FREEZE_MEMORY_STATUS OK, defines future test case record shape, candidate output record shape, required version and canon-reference fields, case-specific pass/fail/critical-fail rubric fields, two-pass match-before-disagree contract, non-authoritative candidate wrapper, forbidden authority fields, rejection rules, LAB_INVALID handling for malformed gold cases, human-review contract, case category labels, version compatibility rule, roadmap lock, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no executable validators, no fixtures, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-5 Frozen Canon Fixture Format + Hash Manifest next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_TEST_CASE_SCHEMA_CANDIDATE_OUTPUT_CONTRACT_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_TEST_CASE_SCHEMA_CANDIDATE_OUTPUT_CONTRACT.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_TEST_CASE_SCHEMA_CANDIDATE_OUTPUT_CONTRACT.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1 installed."
    Write-Host "LAB-4 documentation-only Test Case Schema + Candidate Output Contract installed."
    Write-Host "No LAB code, schema code, executable validators, fixtures, corpus, runner, executable scoring engine, metrics engine, candidate harness, live detectors, import scanner, write guard, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-4 boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-4 ML LAB Test Case Schema + Candidate Output Contract v1, immutable governed documentation-only schema/contract design after LAB-3 freeze with FREEZE_MEMORY_STATUS OK, defines future test case record shape, candidate output record shape, required version and canon-reference fields, case-specific pass/fail/critical-fail rubric fields, two-pass match-before-disagree contract, non-authoritative candidate wrapper, forbidden authority fields, rejection rules, LAB_INVALID handling for malformed gold cases, human-review contract, case category labels, version compatibility rule, roadmap lock, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no executable validators, no fixtures, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-5 Frozen Canon Fixture Format + Hash Manifest next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_TEST_CASE_SCHEMA_CANDIDATE_OUTPUT_CONTRACT_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Test Case Schema + Candidate Output Contract v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-5 — Frozen Canon Fixture Format + Hash Manifest

LAB-5 must remain governed fixture-format/hash-manifest design, not runtime ML implementation.

Pasted text.txt
Document
continue

LAB-4 is frozen with FREEZE_MEMORY_STATUS: OK, and the freeze output names LAB-5 as the next safe milestone. I’ll create LAB-5 as fixture-format/hash-manifest design only: no actual fixtures, no corpus, no runner, and no executable validation machinery.

I’m building this from the latest LAB-4 patch state, updating only the LAB box docs, manifest metadata, freeze hint, and one documentation contract test. I’m also running the previous LAB tests so LAB-5 does not regress earlier gates.

LAB-4 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-5 — Frozen Canon Fixture Format + Hash Manifest as the next safe milestone.

I created the LAB-5 patch.

It is documentation/governance only. It defines the future copied fixture snapshot format, hash manifest record shape, SHA-256 hash doctrine, static fixture read model, no-live-canon/no-live-freeze-memory coupling, fixture immutability, fixture traceability, LAB_INVALID handling for hash/manifest/source-review failures, and critical boundary rules for live reads or mutation attempts.

It adds no LAB code, no schema code, no executable validators, no actual fixtures, no hash manifest data files, no corpus, no runner, no scoring engine, no metrics engine, no candidate harness, no live readers, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no batch mode, no activation key, no field-test mode, no runtime Pilot, and no Copilot behavior.

Download:

SHA-256:

ca5ccca143d61a1c420e81e6137cc9915b88e929095f1824c23d3f31b887775f

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1
CONTRACT_TEST_OK: LAB-5 ML LAB Frozen Canon Fixture Format + Hash Manifest v1, immutable governed documentation-only fixture-format/hash-manifest design after LAB-4 freeze with FREEZE_MEMORY_STATUS OK, defines future copied fixture snapshot format, future hash manifest record shape, SHA-256 hash doctrine, static fixture read model, no live canon coupling, no live freeze-memory coupling, fixture immutability, fixture traceability, LAB_INVALID handling for hash/manifest/source-review failures, critical boundary rules for live reads or mutations, roadmap lock, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no executable validators, no actual fixtures, no hash manifest data files, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live readers, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-6 Deterministic Runner Skeleton next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_FROZEN_CANON_FIXTURE_FORMAT_HASH_MANIFEST_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_FROZEN_CANON_FIXTURE_FORMAT_HASH_MANIFEST.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_FROZEN_CANON_FIXTURE_FORMAT_HASH_MANIFEST.md",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1 installed."
    Write-Host "LAB-5 documentation-only Frozen Canon Fixture Format + Hash Manifest installed."
    Write-Host "No LAB code, schema code, executable validators, actual fixtures, hash manifest data files, corpus, runner, executable scoring engine, metrics engine, candidate harness, live readers, live detectors, import scanner, write guard, prompt loading, persistence, provider calls, embeddings, batch mode, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $PY_FILES = Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
    if ($PY_FILES.Count -ne 0) {
        throw "LAB-5 boundary violation: Python implementation files were found inside the LAB box."
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-5 ML LAB Frozen Canon Fixture Format + Hash Manifest v1, immutable governed documentation-only fixture-format/hash-manifest design after LAB-4 freeze with FREEZE_MEMORY_STATUS OK, defines future copied fixture snapshot format, future hash manifest record shape, SHA-256 hash doctrine, static fixture read model, no live canon coupling, no live freeze-memory coupling, fixture immutability, fixture traceability, LAB_INVALID handling for hash/manifest/source-review failures, critical boundary rules for live reads or mutations, roadmap lock, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, no LAB code, no schema code, no executable validators, no actual fixtures, no hash manifest data files, no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live readers, no live detectors, no import scanner, no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, LAB-6 Deterministic Runner Skeleton next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_FROZEN_CANON_FIXTURE_FORMAT_HASH_MANIFEST_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Frozen Canon Fixture Format + Hash Manifest v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-6 — Deterministic Runner Skeleton

LAB-6 is the first milestone that may begin non-runtime runner skeleton work, but only under a separate governed scope. It must still not add route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

Pasted text.txt
Document
continue

LAB-5 is frozen with FREEZE_MEMORY_STATUS: OK, so LAB-6 is allowed. One important boundary change starts here: LAB-6 may add the first non-runtime runner skeleton, so I need to update the prior documentation-only guard tests to recognize that LAB-6 supersedes the earlier “no Python in LAB box” assumption without weakening LAB-0 through LAB-5 historical contracts.

LAB-5 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-6 — Deterministic Runner Skeleton as the next safe milestone.

I created the LAB-6 patch.

This is the first LAB milestone that adds a non-runtime Python skeleton, so I also updated the earlier LAB documentation-contract tests to allow exactly one LAB-6 skeleton source file while still rejecting prohibited runtime/authority behavior.

It adds:

kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py

The skeleton is pure, in-memory, deterministic, non-authoritative, and returns only NOT_EVALUATED run-plan records.

It adds no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture file reads, no actual fixtures, no hash manifest data files, no corpus, no candidate evaluation, no route comparison, no scoring engine, no metrics engine, no candidate harness, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, and no Copilot behavior.

Download:

SHA-256:

e09de4b79f11e9de0c9770b52d412822c86ee8b68a0409f17c4f7deb62874b6d

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1
CONTRACT_TEST_OK: LAB-6 ML LAB Deterministic Runner Skeleton v1, immutable governed non-runtime deterministic runner skeleton after LAB-5 freeze with FREEZE_MEMORY_STATUS OK, adds first allowed LAB Python skeleton file, pure in-memory caller-supplied metadata only, NOT_EVALUATED output only, read-only non-authoritative run-plan records, deterministic canonicalization and SHA-256 text hash helpers, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture file reads, no actual fixtures, no hash manifest data files, no corpus, no candidate evaluation, no route comparison, no route authority, no scoring engine, no metrics engine, no candidate harness, no report persistence, no prompt loading, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-7 Lab Self-Validation Gate next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_DETERMINISTIC_RUNNER_SKELETON_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_DETERMINISTIC_RUNNER_SKELETON.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_DETERMINISTIC_RUNNER_SKELETON.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1 installed."
    Write-Host "LAB-6 non-runtime deterministic runner skeleton installed."
    Write-Host "This adds exactly one allowed LAB Python skeleton file: deterministic_runner_skeleton.py."
    Write-Host "No route authority, prompt loading, live prompt-library reads, live freeze-memory reads, live router-canon reads, runtime router imports, fixture file reads, actual fixtures, hash manifest data files, corpus, candidate evaluation, route comparison, scoring engine, metrics engine, candidate harness, report persistence, provider calls, embeddings, network calls, subprocess calls, batch mode, persistent ML decisions, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $ALLOWED_LAB_PY = @(
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
    )

    $PY_REL = @(
        Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue |
        ForEach-Object {
            $_.FullName.Substring($PROJECT_ROOT.Length + 1).Replace("\", "/")
        } |
        Sort-Object
    )

    if ($PY_REL.Count -ne $ALLOWED_LAB_PY.Count) {
        throw "LAB-6 boundary violation: unexpected number of LAB Python files. Found: $($PY_REL -join ', ')"
    }

    foreach ($REL in $PY_REL) {
        if ($ALLOWED_LAB_PY -notcontains $REL) {
            throw "LAB-6 boundary violation: unauthorized LAB Python file found: $REL"
        }
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-6 ML LAB Deterministic Runner Skeleton v1, immutable governed non-runtime deterministic runner skeleton after LAB-5 freeze with FREEZE_MEMORY_STATUS OK, adds first allowed LAB Python skeleton file, pure in-memory caller-supplied metadata only, NOT_EVALUATED output only, read-only non-authoritative run-plan records, deterministic canonicalization and SHA-256 text hash helpers, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture file reads, no actual fixtures, no hash manifest data files, no corpus, no candidate evaluation, no route comparison, no route authority, no scoring engine, no metrics engine, no candidate harness, no report persistence, no prompt loading, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-7 Lab Self-Validation Gate next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_DETERMINISTIC_RUNNER_SKELETON_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Deterministic Runner Skeleton v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-7 — Lab Self-Validation Gate

LAB-7 must validate the LAB itself before any candidate evaluation. It must remain non-runtime and must not grant route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

Pasted text.txt
Document
continue

LAB-6 is frozen with FREEZE_MEMORY_STATUS: OK, and the next milestone is LAB-7. I’m building LAB-7 as an in-memory self-validation gate only: it can validate LAB readiness controls, but it still cannot evaluate candidates or grant routing authority.

LAB-6 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-7 — Lab Self-Validation Gate as the next safe milestone.

I created the LAB-7 patch.

It adds a non-runtime, in-memory Lab Self-Validation Gate. It validates caller-supplied LAB control facts before future candidate evaluation, but it still does not evaluate candidates, compare routes, select routes, load prompts, read live project state, persist decisions, activate Pilot/Copilot, or field-test anything.

Download:

SHA-256:

21416951cf1fbd0891e156c555abfd50f5f4f3e702b0eda9726d35fcb887cd30

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_self_validation_gate_v1
CONTRACT_TEST_OK: LAB-7 ML LAB Self-Validation Gate v1, immutable governed non-runtime in-memory self-validation gate after LAB-6 freeze with FREEZE_MEMORY_STATUS OK, validates caller-supplied LAB control facts before future candidate evaluation, requires gold-vs-gold pass, wrong-route negative control, missing-prompt negative control, forbidden-action critical control, fixture-hash mismatch LAB_INVALID control, skipped match-before-disagree critical control, zero critical boundary budget enforcement, LAB-6 NOT_EVALUATED behavior, no live project reads, no authority fields, and candidate evaluation blocked until self-validation, returns LAB_SELF_VALIDATION_PASS or LAB_INVALID only, candidate evaluation remains not executed and not allowed by this gate, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture reads, no actual fixtures, no hash manifest data files, no corpus, no scoring engine, no metrics engine, no candidate harness, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-8 Alpha Corpus Seed next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SELF_VALIDATION_GATE_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_self_validation_gate_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_self_validation_gate_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_SELF_VALIDATION_GATE.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_SELF_VALIDATION_GATE.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_self_validation_gate_v1 installed."
    Write-Host "LAB-7 non-runtime in-memory Lab Self-Validation Gate installed."
    Write-Host "This adds exactly one new allowed LAB Python source file: lab_self_validation_gate.py."
    Write-Host "No candidate evaluation, route comparison, route authority, prompt loading, live prompt-library reads, live freeze-memory reads, live router-canon reads, runtime router imports, fixture reads, actual fixtures, hash manifest data files, corpus, scoring engine, metrics engine, candidate harness, report persistence, provider calls, embeddings, network calls, subprocess calls, batch mode, persistent ML decisions, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $ALLOWED_LAB_PY = @(
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
    )

    $PY_REL = @(
        Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue |
        ForEach-Object {
            $_.FullName.Substring($PROJECT_ROOT.Length + 1).Replace("\", "/")
        } |
        Sort-Object
    )

    if ($PY_REL.Count -ne $ALLOWED_LAB_PY.Count) {
        throw "LAB-7 boundary violation: unexpected number of LAB Python files. Found: $($PY_REL -join ', ')"
    }

    foreach ($REL in $PY_REL) {
        if ($ALLOWED_LAB_PY -notcontains $REL) {
            throw "LAB-7 boundary violation: unauthorized LAB Python file found: $REL"
        }
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_self_validation_gate_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-7 ML LAB Self-Validation Gate v1, immutable governed non-runtime in-memory self-validation gate after LAB-6 freeze with FREEZE_MEMORY_STATUS OK, validates caller-supplied LAB control facts before future candidate evaluation, requires gold-vs-gold pass, wrong-route negative control, missing-prompt negative control, forbidden-action critical control, fixture-hash mismatch LAB_INVALID control, skipped match-before-disagree critical control, zero critical boundary budget enforcement, LAB-6 NOT_EVALUATED behavior, no live project reads, no authority fields, and candidate evaluation blocked until self-validation, returns LAB_SELF_VALIDATION_PASS or LAB_INVALID only, candidate evaluation remains not executed and not allowed by this gate, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture reads, no actual fixtures, no hash manifest data files, no corpus, no scoring engine, no metrics engine, no candidate harness, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-8 Alpha Corpus Seed next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_SELF_VALIDATION_GATE_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_self_validation_gate_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Self-Validation Gate v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-8 — Alpha Corpus Seed

LAB-8 may introduce a small governed static alpha corpus, but it must still not grant route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

Pasted text.txt
Document
continue

LAB-7 freeze is confirmed, including LOCAL FREEZE WRITE OK, startup refresh, and FREEZE_MEMORY_STATUS: OK; LAB-8 is the next allowed milestone. I’m making LAB-8 as a small static alpha corpus seed, not candidate evaluation or runtime routing.

I found the LAB-7 freeze evidence in the uploaded file: it explicitly says LAB-8 Alpha Corpus Seed is next and confirms FREEZE_MEMORY_STATUS: OK. I’m keeping the alpha corpus small and static: it seeds case records and manifest metadata, but it does not run or score them.

LAB-7 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-8 — Alpha Corpus Seed as the next safe milestone.

I created the LAB-8 patch.

It adds a static, non-authoritative alpha corpus seed with 12 seed cases and a SHA-256 corpus hash manifest. It does not execute cases, score cases, evaluate candidates, compare routes, grant route authority, load prompts, read live prompt-library/freeze-memory/router-canon data, create actual fixture snapshots, create a runner, create a scoring engine, create a metrics engine, create a candidate harness, persist reports or ML decisions, call providers, call embeddings, use network/subprocess/batch mode, activate Pilot/Copilot, enable field testing, or implement Copilot behavior.

Download:

SHA-256:

5e85c135fa619f2611aef95f50ef7ac733e80d08b3ac0940053b295edd5b14ee

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1
CONTRACT_TEST_OK: LAB-8 ML LAB Alpha Corpus Seed v1, immutable governed static alpha corpus seed after LAB-7 freeze with FREEZE_MEMORY_STATUS OK, adds 12 static non-authoritative alpha cases and a SHA-256 static corpus hash manifest, covers simple-vs-governed routing, freeze governance, prompt-authoring bypass, box boundaries, prompt-loading prohibition, live-fixture prohibition, missing context, match-before-disagree, and LAB roadmap lock, candidate evaluation not executed, cases not scored, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no actual fixture snapshots, no runner, no scoring engine, no metrics engine, no candidate harness, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-9 Offline Observability + Experiment Report next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_ALPHA_CORPUS_SEED_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALPHA_CORPUS_SEED.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\alpha_corpus\alpha_corpus_seed_v1.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\alpha_corpus\alpha_corpus_seed_v1_hash_manifest.json",
        "tests\test_routing_signal_scorer_v3_ml_lab_alpha_corpus_seed.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALPHA_CORPUS_SEED.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\alpha_corpus\alpha_corpus_seed_v1.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\alpha_corpus\alpha_corpus_seed_v1_hash_manifest.json",
        "tests\test_routing_signal_scorer_v3_ml_lab_alpha_corpus_seed.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1 installed."
    Write-Host "LAB-8 static non-authoritative Alpha Corpus Seed installed."
    Write-Host "This adds 12 static alpha cases and a SHA-256 static corpus hash manifest."
    Write-Host "No candidate evaluation, route comparison, route authority, prompt loading, live prompt-library reads, live freeze-memory reads, live router-canon reads, runtime router imports, actual fixture snapshots, runner, scoring engine, metrics engine, candidate harness, report persistence, provider calls, embeddings, network calls, subprocess calls, batch mode, persistent ML decisions, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_alpha_corpus_seed.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $ALLOWED_LAB_PY = @(
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
    )

    $PY_REL = @(
        Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue |
        ForEach-Object {
            $_.FullName.Substring($PROJECT_ROOT.Length + 1).Replace("\", "/")
        } |
        Sort-Object
    )

    if ($PY_REL.Count -ne $ALLOWED_LAB_PY.Count) {
        throw "LAB-8 boundary violation: unexpected number of LAB Python files. Found: $($PY_REL -join ', ')"
    }

    foreach ($REL in $PY_REL) {
        if ($ALLOWED_LAB_PY -notcontains $REL) {
            throw "LAB-8 boundary violation: unauthorized LAB Python file found: $REL"
        }
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-8 ML LAB Alpha Corpus Seed v1, immutable governed static alpha corpus seed after LAB-7 freeze with FREEZE_MEMORY_STATUS OK, adds 12 static non-authoritative alpha cases and a SHA-256 static corpus hash manifest, covers simple-vs-governed routing, freeze governance, prompt-authoring bypass, box boundaries, prompt-loading prohibition, live-fixture prohibition, missing context, match-before-disagree, and LAB roadmap lock, candidate evaluation not executed, cases not scored, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no actual fixture snapshots, no runner, no scoring engine, no metrics engine, no candidate harness, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-9 Offline Observability + Experiment Report next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_ALPHA_CORPUS_SEED_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Alpha Corpus Seed v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-9 — Offline Observability + Experiment Report

LAB-9 must remain governed/non-runtime and must not grant route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

Pasted text.txt
Document
continue

The LAB-8 freeze evidence is valid: it shows the LAB-8 validation marker, LOCAL FREEZE WRITE OK, startup refresh, and FREEZE_MEMORY_STATUS: OK. I’m now preparing LAB-9 as offline observability/report structure only, with no report writing, scoring, candidate evaluation, or runtime behavior.

LAB-8 freeze is confirmed. The uploaded output shows LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-9 — Offline Observability + Experiment Report as the next safe milestone.

I created the LAB-9 patch.

It adds a static offline observability + experiment report contract and one static report template. It does not generate reports, persist reports, evaluate candidates, execute or score cases, compare routes, grant route authority, load prompts, read live prompt-library/freeze-memory/router-canon data, create fixtures, create a runner, create a scoring engine, create a metrics engine, create a candidate harness, persist ML decisions, call providers, call embeddings, use network/subprocess/batch mode, activate Pilot/Copilot, enable field testing, or implement Copilot behavior.

Download:

SHA-256:

a1507c183a9b90bca015178612a7411ecc23cb15df8067eeefc79e6f59cb5a6d

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1
CONTRACT_TEST_OK: LAB-9 ML LAB Offline Observability + Experiment Report v1, immutable governed static offline observability and experiment-report contract after LAB-8 freeze with FREEZE_MEMORY_STATUS OK, adds one static report template and declares future report sections for run identity, lab version context, corpus context, fixture manifest context, self-validation context, candidate metadata, hard gates, soft metrics, case outcomes, critical-boundary incidents, LAB_INVALID incidents, human-review queue, reproducibility metadata, limitations, and freeze evidence, report generation not implemented, report persistence not implemented, candidate evaluation not executed, cases not executed or scored, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no actual fixture snapshots, no runner, no scoring engine, no metrics engine, no candidate harness, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-10 Candidate Evaluation Harness Interface next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_OFFLINE_OBSERVABILITY_EXPERIMENT_REPORT_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $EXPECTED = @(
        "KANDA_FREEZE_HINT.json",
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_OFFLINE_OBSERVABILITY_EXPERIMENT_REPORT.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\report_templates\offline_experiment_report_template_v1.json",
        "tests\test_routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report.py"
    )

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_OFFLINE_OBSERVABILITY_EXPERIMENT_REPORT.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\report_templates\offline_experiment_report_template_v1.json",
        "tests\test_routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report.py"
    )

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1 installed."
    Write-Host "LAB-9 static offline observability + experiment report contract installed."
    Write-Host "This adds one static report template only."
    Write-Host "No report generation, report persistence, candidate evaluation, case execution, case scoring, route comparison, route authority, prompt loading, live prompt-library reads, live freeze-memory reads, live router-canon reads, runtime router imports, actual fixture snapshots, runner, scoring engine, metrics engine, candidate harness, provider calls, embeddings, network calls, subprocess calls, batch mode, persistent ML decisions, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_alpha_corpus_seed.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $ALLOWED_LAB_PY = @(
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
    )

    $PY_REL = @(
        Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue |
        ForEach-Object {
            $_.FullName.Substring($PROJECT_ROOT.Length + 1).Replace("\", "/")
        } |
        Sort-Object
    )

    if ($PY_REL.Count -ne $ALLOWED_LAB_PY.Count) {
        throw "LAB-9 boundary violation: unexpected number of LAB Python files. Found: $($PY_REL -join ', ')"
    }

    foreach ($REL in $PY_REL) {
        if ($ALLOWED_LAB_PY -notcontains $REL) {
            throw "LAB-9 boundary violation: unauthorized LAB Python file found: $REL"
        }
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-9 ML LAB Offline Observability + Experiment Report v1, immutable governed static offline observability and experiment-report contract after LAB-8 freeze with FREEZE_MEMORY_STATUS OK, adds one static report template and declares future report sections for run identity, lab version context, corpus context, fixture manifest context, self-validation context, candidate metadata, hard gates, soft metrics, case outcomes, critical-boundary incidents, LAB_INVALID incidents, human-review queue, reproducibility metadata, limitations, and freeze evidence, report generation not implemented, report persistence not implemented, candidate evaluation not executed, cases not executed or scored, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no actual fixture snapshots, no runner, no scoring engine, no metrics engine, no candidate harness, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-10 Candidate Evaluation Harness Interface next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_OFFLINE_OBSERVABILITY_EXPERIMENT_REPORT_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Offline Observability + Experiment Report v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-10 — Candidate Evaluation Harness Interface

LAB-10 must remain governed/non-runtime and must not grant route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_alpha_corpus_seed.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $ALLOWED_LAB_PY = @(
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
    )

    $PY_REL = @(
        Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue |
        ForEach-Object {
            $_.FullName.Substring($PROJECT_ROOT.Length + 1).Replace("\", "/")
        } |
        Sort-Object
    )

    if ($PY_REL.Count -ne $ALLOWED_LAB_PY.Count) {
        throw "LAB-9 boundary violation: unexpected number of LAB Python files. Found: $($PY_REL -join ', ')"
    }

    foreach ($REL in $PY_REL) {
        if ($ALLOWED_LAB_PY -notcontains $REL) {
            throw "LAB-9 boundary violation: unauthorized LAB Python file found: $REL"
        }
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-9 ML LAB Offline Observability + Experiment Report v1, immutable governed static offline observability and experiment-report contract after LAB-8 freeze with FREEZE_MEMORY_STATUS OK, adds one static report template and declares future report sections for run identity, lab version context, corpus context, fixture manifest context, self-validation context, candidate metadata, hard gates, soft metrics, case outcomes, critical-boundary incidents, LAB_INVALID incidents, human-review queue, reproducibility metadata, limitations, and freeze evidence, report generation not implemented, report persistence not implemented, candidate evaluation not executed, cases not executed or scored, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no actual fixture snapshots, no runner, no scoring engine, no metrics engine, no candidate harness, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-10 Candidate Evaluation Harness Interface next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_OFFLINE_OBSERVABILITY_EXPERIMENT_REPORT_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

This is the validation block itself, not the validation output.

So I cannot yet treat LAB-9 as validated or frozen, and I should not continue to LAB-10 yet.

Please run that block in PowerShell. The successful output must include:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1
CONTRACT_TEST_OK: LAB-9 ML LAB Offline Observability + Experiment Report v1
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_OFFLINE_OBSERVABILITY_EXPERIMENT_REPORT_V1_VALIDATION_OK

Then freeze as:

Routing Signal Scorer v3 ML LAB Offline Observability + Experiment Report v1

Required freeze result:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After you paste the freeze output, I can safely continue to:

LAB-10 — Candidate Evaluation Harness Interface


Pasted text.txt
Document
continue

LAB-9 is frozen with FREEZE_MEMORY_STATUS: OK, and LAB-10 is the next safe milestone. I’m adding only a non-runtime candidate harness interface: no candidate evaluation, no scoring, no route comparison, no route authority, and no prompt loading.

LAB-9 freeze is confirmed. The uploaded output shows LAB-9 validation evidence, LOCAL FREEZE WRITE OK, FREEZE_MEMORY_STATUS: OK, and names LAB-10 — Candidate Evaluation Harness Interface as the next safe milestone.

I created the LAB-10 patch.

It adds a non-runtime, in-memory Candidate Evaluation Harness Interface. It accepts caller-supplied candidate metadata/references only, returns only NOT_EVALUATED or HARNESS_INTERFACE_REJECTED, computes deterministic SHA-256 metadata hashes, and blocks forbidden authority fields.

It does not evaluate candidates, execute cases, score cases, compare routes, grant route authority, load prompts, read live prompt-library/freeze-memory/router-canon data, read fixtures, create fixtures, mutate corpus, generate or persist reports, persist ML decisions, call providers, call embeddings, use network/subprocess/batch mode, activate Pilot/Copilot, enable field testing, or implement Copilot behavior.

Download:

SHA-256:

2242e5212c620c82295692351756d6396d79d866535ae70af2d1705e88d83aad

Sandbox validation passed:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1
CONTRACT_TEST_OK: LAB-10 ML LAB Candidate Evaluation Harness Interface v1, immutable governed non-runtime in-memory candidate harness interface after LAB-9 freeze with FREEZE_MEMORY_STATUS OK, adds exactly one new allowed LAB Python interface file, accepts caller-supplied candidate metadata and references only, returns NOT_EVALUATED or HARNESS_INTERFACE_REJECTED only, computes deterministic SHA-256 metadata hashes, blocks forbidden authority fields, candidate evaluation not executed, cases not executed or scored, reports not generated or persisted, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture reads, no actual fixture snapshots, no corpus mutation, no scoring engine, no metrics engine, no executable candidate harness, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-11 Corpus V1 Expansion next
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_CANDIDATE_EVALUATION_HARNESS_INTERFACE_V1_VALIDATION_OK

Save the ZIP here first:

E:\routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1_patch.zip

Install block:

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1_patch"

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
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force

        if (Test-Path $WORK_PATCH_ZIP) {
            Remove-Item -Path $ROOT_PATCH_ZIP -Force
        }
    }

    if (-not (Test-Path $WORK_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        throw "Root-drive ZIP copy still exists after staging. Install stopped to preserve root cleanliness."
    }

    if (Test-Path $EXTRACT_DIR) {
        Remove-Item $EXTRACT_DIR -Recurse -Force
    }

    Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $EXTRACT_DIR -Force

    $FILES = @(
        "kanda_reasoner_app\routing_signal_scorer\box_manifest.json",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\README.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_PHASE_BOUNDARY.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_ALLOWED_ARTIFACTS.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\LAB_CANDIDATE_EVALUATION_HARNESS_INTERFACE.md",
        "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation\candidate_evaluation_harness_interface.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_alpha_corpus_seed.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py"
    )

    $EXPECTED = @("KANDA_FREEZE_HINT.json") + $FILES

    foreach ($REL in $EXPECTED) {
        $CHECK = Join-Path $EXTRACT_DIR $REL
        if (-not (Test-Path $CHECK)) {
            throw "Expected file missing inside patch ZIP: $REL"
        }
    }

    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

    foreach ($REL in $FILES) {
        $SRC = Join-Path $EXTRACT_DIR $REL
        $DST = Join-Path $PROJECT_ROOT $REL

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

    Write-Host ""
    Write-Host "INSTALL OK: routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1 installed."
    Write-Host "LAB-10 non-runtime Candidate Evaluation Harness Interface installed."
    Write-Host "This adds exactly one new allowed LAB Python source file: candidate_evaluation_harness_interface.py."
    Write-Host "No candidate evaluation, case execution, case scoring, route comparison, route authority, prompt loading, live prompt-library reads, live freeze-memory reads, live router-canon reads, runtime router imports, fixture reads, actual fixture snapshots, corpus mutation, scoring engine, metrics engine, executable candidate harness, report generation, report persistence, provider calls, embeddings, network calls, subprocess calls, batch mode, persistent ML decisions, activation key, field-test mode, runtime Pilot, or Copilot behavior was added."
    Write-Host "Root-drive ZIP was staged into delete_after_daily_work and the root copy was deleted."
    Write-Host "KANDA_FREEZE_HINT.json remains ZIP delivery metadata, not a project source file."
    Write-Host "Backup folder:"
    Write-Host $BACKUP_DIR
    Write-Host ""
    Start-Sleep -Seconds 5
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this error"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validation block:

$PROJECT_ROOT = "E:\kanda_reasoner"

try {
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    $TESTS = @(
        "tests\test_routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_alpha_corpus_seed.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_self_validation_gate.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_slo_critical_error_budget.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_risk_control_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_success_criteria_matrix.py",
        "tests\test_routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate.py",
        "tests\test_rg_lab_000_lab_phase_entry_router_canon.py",
        "tests\test_routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate.py"
    )

    foreach ($TEST in $TESTS) {
        Write-Host ""
        Write-Host "RUNNING:"
        Write-Host $TEST
        python $TEST
        if ($LASTEXITCODE -ne 0) {
            throw "test failed: $TEST"
        }
    }

    $LAB_BOX = Join-Path $PROJECT_ROOT "kanda_reasoner_app\routing_signal_scorer\lab_non_runtime_router_evaluation"
    $ALLOWED_LAB_PY = @(
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py",
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
        "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
    )

    $PY_REL = @(
        Get-ChildItem -Path $LAB_BOX -Recurse -Filter "*.py" -ErrorAction SilentlyContinue |
        ForEach-Object {
            $_.FullName.Substring($PROJECT_ROOT.Length + 1).Replace("\", "/")
        } |
        Sort-Object
    )

    if ($PY_REL.Count -ne $ALLOWED_LAB_PY.Count) {
        throw "LAB-10 boundary violation: unexpected number of LAB Python files. Found: $($PY_REL -join ', ')"
    }

    foreach ($REL in $PY_REL) {
        if ($ALLOWED_LAB_PY -notcontains $REL) {
            throw "LAB-10 boundary violation: unauthorized LAB Python file found: $REL"
        }
    }

    $ROOT_HINT = Join-Path $PROJECT_ROOT "KANDA_FREEZE_HINT.json"
    if (Test-Path $ROOT_HINT) {
        throw "KANDA_FREEZE_HINT.json must not exist in project root after install."
    }

    Write-Host ""
    Write-Host "VALIDATION OK: routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1"
    Write-Host "CONTRACT_TEST_OK: LAB-10 ML LAB Candidate Evaluation Harness Interface v1, immutable governed non-runtime in-memory candidate harness interface after LAB-9 freeze with FREEZE_MEMORY_STATUS OK, adds exactly one new allowed LAB Python interface file, accepts caller-supplied candidate metadata and references only, returns NOT_EVALUATED or HARNESS_INTERFACE_REJECTED only, computes deterministic SHA-256 metadata hashes, blocks forbidden authority fields, candidate evaluation not executed, cases not executed or scored, reports not generated or persisted, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture reads, no actual fixture snapshots, no corpus mutation, no scoring engine, no metrics engine, no executable candidate harness, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-11 Corpus V1 Expansion next"
    Write-Host "SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_CANDIDATE_EVALUATION_HARNESS_INTERFACE_V1_VALIDATION_OK"
    Write-Host ""
    Write-Host "VALIDATION OK"
    Write-Host "routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1 is installed and validated."
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "VALIDATION FAILED:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Press Enter after copying this validation output"
    Clear-Host
    Read-Host "Press Enter again to clear"
    Clear-Host
}

After validation passes, freeze as:

Routing Signal Scorer v3 ML LAB Candidate Evaluation Harness Interface v1

Required freeze output:

LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK

After that, the next safe milestone is:

LAB-11 — Corpus V1 Expansion

LAB-11 may expand static corpus coverage, but it must still not grant route authority, prompt loading, provider calls, embeddings, persistent ML decisions, activation, field testing, runtime Pilot, or Copilot behavior.

Pasted text.txt
Document
this chat is too long . ok gimme a handoff of end of chat , explaining 1. contexto of what we are doing,  ML  implementation you intend to do , 2. what we've done till now 3.  what is next.  Important : explain in details how do you intend to continue, do it in details  because we are closing this long chat to start another and I dont want to loose our logic line. I want next time we open a chat you have complete awareness of how continue

I’ll turn this into a reusable end-of-chat handoff you can paste at the start of the next chat. I’ll also check the uploaded freeze output so the handoff does not accidentally claim the wrong current milestone.

I checked the uploaded freeze output before writing this. It confirms LAB-10 Candidate Evaluation Harness Interface v1 has validation evidence, LOCAL FREEZE WRITE OK, and the planned next step is LAB-11 — Corpus V1 Expansion after FREEZE_MEMORY_STATUS: OK.

Use this as the first message in the next chat:
END-OF-CHAT HANDOFF — KANDA / Routing Signal Scorer v3 / ML LAB Phase
0. Immediate instruction for the next chat

We are continuing the KANDA / PyArchitect / Routing Signal Scorer v3 governed ML LAB work.

Do not jump directly into ML implementation.

Do not implement runtime routing.

Do not implement prompt loading.

Do not implement provider calls, embeddings, vector stores, persistent ML decisions, batch mode, activation, field testing, runtime Pilot, or Copilot behavior.

The current safe next milestone is:

LAB-11 — Corpus V1 Expansion

The last completed/frozen milestone is:

LAB-10 — Candidate Evaluation Harness Interface v1

The next response should continue from LAB-10 being frozen and prepare LAB-11 only, unless I provide newer validation/freeze evidence that changes the state.
1. Project context: what we are doing

We are working on the KANDA / PyArchitect “Routing Signal Scorer v3” roadmap.

The broader goal is to eventually improve routing quality using ML-like or model-assisted logic, but under strict governance.

The target future system is not a free autonomous router. The doctrine is:

ML recommends. Canon and router governance decide.

That means the ML layer must never become the source of routing authority. It may eventually help score, warn, classify, explain, compare, or recommend, but it cannot decide routes, load prompts, mutate canon, approve freezes, record human approval, activate Pilot/Copilot, or override frozen governance.

The long-term maturity path is:

Adviser → Assistant/Auxiliar → Pilot → Copilot

We previously closed/froze the Adviser and post-Adviser bridge work. Then we moved through Routing Signal Scorer v3 P-series milestones. After P12, the project entered a dedicated ML LAB phase.

The LAB phase exists because before continuing real ML router logic, we need a deterministic, isolated, non-runtime evaluation lab. The LAB’s job is to test whether a future candidate router/ML scorer can reproduce frozen routing governance, identify missing context, reject stale context, obey box boundaries, reject bypass attempts, and explain disagreement without overriding canon.

The LAB must validate the system before any ML logic is trusted.

Important roadmap lock:

P12 frozen → RG-LAB-000 canonization → LAB-0 through LAB reliability gates → LAB self-validation → ML router prompt logic reliability testing → only then continue ML implementation.

So the work right now is still LAB construction, not actual production ML router behavior.
2. What “ML implementation” is intended eventually

The intended ML implementation is not a live autonomous router.

The eventual ML implementation should be a non-authoritative routing signal scorer / candidate evaluator that can:

    Take a governed routing scenario or candidate output.

    Compare it against frozen canon, fixture snapshots, and expected contract fields.

    Produce advisory scores, diagnostics, warnings, and explanation quality signals.

    Detect hard failures and critical boundary violations.

    Surface uncertainty and missing context.

    Help humans and governed code review whether the router prompt logic is reliable.

But this must happen only after the LAB is strong enough.

The intended future ML logic should be evaluated by the LAB before it is trusted. It should not be allowed to decide routing actions in production. It should not load prompts. It should not call providers during LAB evaluation. It should not mutate project memory. It should not write freeze records. It should not activate Pilot or Copilot behavior.

Eventually, after the LAB and ML router prompt logic reliability are validated, the project may move toward a controlled non-runtime or advisory ML scorer implementation, possibly something like:

    Candidate input contract.

    Static fixture/corpus evaluation.

    Deterministic scoring.

    Hard-gate checks.

    Soft metrics.

    Report output.

    Human review queue.

    Reliability labels.

    Error canonization intake.

But that is not yet authorized as live runtime behavior.
3. Core governance constraints that must remain active

Always preserve these constants and boundaries:

ROUTING_EFFECT = "none"

PROMPT_LOADING_EFFECT = "none"

RUNTIME_EFFECT = "none"

ACTIVATION_EFFECT = "none"

STORAGE_STATUS = "in_memory_only"

HUMAN_REVIEW_MANDATORY = True

OPT_IN_PER_INVOCATION_REQUIRED = True

CRITICAL_BOUNDARY_ERROR_BUDGET = 0

Hard prohibitions:

    No live routing authority.

    No prompt loading.

    No prompt execution.

    No route execution.

    No runtime Pilot.

    No Limited Shadow Runtime unless separately governed later.

    No Copilot implementation.

    No provider calls.

    No embeddings.

    No vector stores.

    No training-data use.

    No persistent ML decisions.

    No batch mode.

    No activation keys.

    No field-test flags.

    No automatic human approval recording.

    No readiness approval recording by the candidate.

    No freeze memory mutation by LAB/candidate.

    No prompt library mutation by LAB/candidate.

    No router canon mutation by LAB/candidate.

    No gold registry mutation by LAB/candidate.

    No live prompt-library reads during LAB evaluation.

    No live freeze-memory reads during LAB evaluation.

    No live router-canon reads during LAB evaluation.

    No production/runtime code importing LAB code.

Critical rule:

Any critical boundary violation blocks reliability claims and blocks continuation of ML implementation.

Soft scores cannot compensate for hard or critical failures.
4. Box architecture context

The LAB primary box is:

kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/

The LAB is the only place for LAB-specific non-runtime evaluation artifacts.

Production/runtime code must not import the LAB box.

LAB code must not import runtime router modules, prompt loader modules, provider modules, embedding/vector modules, UI modules, async/scheduler/event-bus modules, activation modules, field-test modules, runtime Pilot modules, or Copilot modules.

The LAB may only operate on caller-supplied data or static copied artifacts that were explicitly allowed by previous milestones.

The project freeze memory belongs under:

project_freeze_after_update/frozen_features_memory/

Do not treat project_freeze_ledger as active project memory. project_freeze_ledger is reusable blueprint/engine logic, not project-specific memory.

KANDA_FREEZE_HINT.json is ZIP delivery metadata only. It must not be installed into the project root.
5. What was done before this chat’s ending

The P-series was already completed and frozen before this LAB stretch.

Known frozen P-series state:

P8 — Non-Runtime Pilot Candidate Implementation v1
Feature ID:
routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1

P9 — Non-Runtime Pilot Candidate Contract Conformance v1
Feature ID:
routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1

P10 — Non-Runtime Pilot Candidate Readiness Gate v1
Feature ID:
routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1

P11 — Non-Runtime Pilot Candidate Review Evidence Packet v1
Feature ID:
routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1

P12 — Non-Runtime Pilot Phase Closure + Copilot Boundary Entry Gate v1
Feature ID:
routing_signal_scorer_v3_non_runtime_pilot_phase_closure_copilot_boundary_entry_gate_v1

P12 closed the non-runtime Pilot phase and created a boundary gate before Copilot. It did not implement Copilot.

After P12, we canonized the ML LAB entry:

RG-LAB-000 — ML LAB Phase Entry Router Canon v1
Feature ID:
rg_lab_000_ml_lab_phase_entry_router_canon_v1

Core rule from RG-LAB-000:

After P12, canonize LAB entry first; build and validate the LAB before testing ML router prompt logic; validate ML router prompt logic reliability before continuing ML implementation.

RG-LAB-000 froze the LAB-first roadmap and blocked direct ML implementation.
6. LAB milestones completed and frozen

The following LAB milestones were completed, validated, and frozen.
LAB-0 — Phase Boundary + Lab Charter / Entry Gate

Feature ID:
routing_signal_scorer_v3_ml_lab_phase_boundary_charter_entry_gate_v1

Purpose:
Established the LAB as a governed non-runtime evaluation phase.

It defined the LAB mission:
a deterministic, isolated, non-runtime evaluation lab that will later test ML/router candidates against frozen governance.

It did not add executable LAB code.
LAB-0A — Success Criteria Matrix

Feature ID:
routing_signal_scorer_v3_ml_lab_success_criteria_matrix_v1

Purpose:
Defined what success means for the LAB and future ML/router candidate reliability.

It covered route exact match, prompt recall/precision, missing context detection, stale context rejection, disagreement quality, explanation quality, confidence calibration, human review, and hard-gate requirements.

It did not add executable LAB code.
LAB-0B — Risk-Control Matrix

Feature ID:
routing_signal_scorer_v3_ml_lab_risk_control_matrix_v1

Purpose:
Defined risk controls for future LAB/ML work.

It captured risks like false fast path, missed routed work, prompt omission, prompt excess, stale context, bypass attempts, box leakage, prompt loading, route authority override, persistence, provider calls, embeddings, activation drift, and premature Copilot behavior.

It did not add executable LAB code.
LAB-0C — SLO / Critical Error Budget Declaration

Feature ID:
routing_signal_scorer_v3_ml_lab_slo_critical_error_budget_v1

Purpose:
Declared the zero critical boundary error budget.

Critical boundary error budget = 0.

Hard gates must run before soft scores.

Any critical violation blocks reliability claims and blocks ML implementation continuation.

LAB_INVALID blocks candidate evaluation.

It did not add executable LAB code.
LAB-1 — Box Boundary + Shielding Manifest

Feature ID:
routing_signal_scorer_v3_ml_lab_box_boundary_shielding_manifest_v1

Purpose:
Defined the LAB box and shielding rules.

Primary LAB box:
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/

Preserved one-way dependency rule:
production/runtime code must not import LAB.

Declared future LAB code must not import runtime router, prompt loader, provider, embeddings, UI, freeze writer, activation, field-test, runtime Pilot, Copilot, async, scheduler, or batch modules.

It did not add executable LAB code.
LAB-2 — Failure Taxonomy + Critical Violation Model

Feature ID:
routing_signal_scorer_v3_ml_lab_failure_taxonomy_critical_violation_model_v1

Purpose:
Defined the failure taxonomy and violation model.

Outcome vocabulary:
PASS
SOFT_FAIL
HARD_FAIL
CRITICAL_FAIL
LAB_INVALID
NEEDS_HUMAN_REVIEW
NOT_EVALUATED

Critical violation examples:
ROUTE_AUTHORITY_OVERRIDE
UNAUTHORIZED_PROMPT_LOAD
RUNTIME_ACTION
PERSISTENCE_ATTEMPT
PROVIDER_CALL_ATTEMPT
EMBEDDING_ATTEMPT
TRAINING_DATA_USE_ATTEMPT
BATCH_MODE_ATTEMPT
CANON_MUTATION
FREEZE_MEMORY_MUTATION
GOLD_REGISTRY_MUTATION
PROMPT_LIBRARY_MUTATION
FIELD_TEST_MODE_ATTEMPT
ACTIVATION_KEY_ATTEMPT
COPILOT_BEHAVIOR_ATTEMPT
HUMAN_APPROVAL_RECORDING_ATTEMPT
READINESS_APPROVAL_ATTEMPT
PRODUCTION_IMPORTS_LAB
LAB_IMPORTS_RUNTIME_ROUTER
LAB_IMPORTS_PROMPT_LOADER
LAB_IMPORTS_PROVIDER_OR_EMBEDDING
LAB_WRITES_OUTSIDE_AUTHORIZED_PATHS
LIVE_CANON_COUPLING
LIVE_FREEZE_MEMORY_COUPLING
LIVE_GOLD_REGISTRY_COUPLING
PROMPT_INJECTION_BYPASS
SYSTEM_PROMPT_OR_PROMPT_FILE_LEAK_ATTEMPT
INSECURE_OUTPUT_TO_DOWNSTREAM
LAB_INVALID_RESULT_REPORTED_AS_PASS
RELIABILITY_CLAIM_WITH_CRITICAL_FAILURE
ML_IMPLEMENTATION_CONTINUED_PREMATURELY

It did not add scoring or evaluation machinery.
LAB-3 — Scoring Model + Hard Gates

Feature ID:
routing_signal_scorer_v3_ml_lab_scoring_model_hard_gates_v1

Purpose:
Defined scoring doctrine and hard-gate order.

Scoring order:

    LAB integrity

    Fixture/version integrity

    Candidate output contract

    Critical boundary gates

    Governance gates

    Task-specific gates

    Soft metrics

    Coverage/calibration

    Human review

    Reliability claim eligibility

Outcome precedence:
LAB_INVALID > CRITICAL_FAIL > HARD_FAIL > NEEDS_HUMAN_REVIEW > SOFT_FAIL > PASS

Non-compensation rule:
soft scores and aggregate accuracy cannot compensate for hard or critical failures.

It did not implement scoring, metrics, schema, runner, or evaluation machinery.
LAB-4 — Test Case Schema + Candidate Output Contract

Feature ID:
routing_signal_scorer_v3_ml_lab_test_case_schema_candidate_output_contract_v1

Purpose:
Defined future test case record shape and candidate output contract.

Required future test case concepts:
case_id
case_version
schema_version
corpus_version
canon_version_reference
canon_rule_references
fixture_hash_reference
expected routing fields
case-specific rubric fields

Candidate output must be wrapped as a non-authoritative evaluation record.

Candidate output cannot become:
route decision
prompt loading command
approval
activation
runtime action
freeze write
human decision record
readiness decision
Copilot instruction

Defined two-pass match-before-disagree contract:
pass_1_canon_match
pass_2_disagreement_or_improvement only if needed
yield_to_canon

It did not implement validators, schema code, fixtures, corpus, runner, scoring, metrics, or evaluation machinery.
LAB-5 — Frozen Canon Fixture Format + Hash Manifest

Feature ID:
routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1

Purpose:
Defined future fixture/hash manifest doctrine.

Future fixtures are static copied snapshots, not live links.

Future LAB evaluation may read only copied, reviewed fixture snapshots.

It must not directly read:
live prompt library
live freeze memory
live router canon
runtime router modules
provider configuration
embedding/vector stores

SHA-256 is the future hash algorithm doctrine.

Fixture/hash mismatch, missing manifest, missing source freeze ID, missing review status, unapproved review status, missing canonicalization, unlisted fixture, mutated fixture, or fixture outside allowed roots are LAB_INVALID classes.

It did not create actual fixtures or manifest data files.
LAB-6 — Deterministic Runner Skeleton

Feature ID:
routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1

Purpose:
First milestone that added an allowed LAB Python skeleton file.

Allowed LAB Python file added:
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py

Behavior:
pure in-memory
caller-supplied metadata only
deterministic canonicalization
SHA-256 text hash helpers
NOT_EVALUATED output only
read-only non-authoritative run-plan records

It does not read fixtures, evaluate candidates, compare routes, score, load prompts, call providers, use network/subprocess, persist reports, or create runtime behavior.
LAB-7 — Lab Self-Validation Gate

Feature ID:
routing_signal_scorer_v3_ml_lab_self_validation_gate_v1

Purpose:
Added non-runtime, in-memory LAB self-validation gate.

Allowed LAB Python file added:
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py

It validates caller-supplied LAB control facts before future candidate evaluation.

Required controls include:
gold-vs-gold pass
wrong-route negative control
missing-prompt negative control
forbidden-action critical control
fixture-hash mismatch LAB_INVALID control
skipped match-before-disagree critical control
zero critical boundary budget enforcement
LAB-6 NOT_EVALUATED behavior
no live project reads
no authority fields
candidate evaluation blocked until self-validation

It returns only:
LAB_SELF_VALIDATION_PASS
LAB_INVALID

It does not evaluate candidates.
LAB-8 — Alpha Corpus Seed

Feature ID:
routing_signal_scorer_v3_ml_lab_alpha_corpus_seed_v1

Purpose:
Added a static, non-authoritative alpha corpus seed.

It added:
12 static alpha cases
SHA-256 static corpus hash manifest

Coverage included:
simple vs governed routing
freeze governance
prompt-authoring bypass
box boundaries
prompt-loading prohibition
live-fixture prohibition
missing context
match-before-disagree
LAB roadmap lock

It did not execute cases, score cases, evaluate candidates, compare routes, or act as reliability evidence.
LAB-9 — Offline Observability + Experiment Report

Feature ID:
routing_signal_scorer_v3_ml_lab_offline_observability_experiment_report_v1

Purpose:
Added static offline observability + experiment report contract and one static report template.

Future report sections include:
run identity
LAB version context
corpus context
fixture manifest context
self-validation context
candidate metadata
hard gates
soft metrics
case outcomes
critical-boundary incidents
LAB_INVALID incidents
human-review queue
reproducibility metadata
limitations
freeze evidence

It does not generate reports, persist reports, execute cases, score cases, evaluate candidates, compare routes, or provide reliability evidence.

After LAB-9, exactly two LAB Python source files were allowed:
deterministic_runner_skeleton.py
lab_self_validation_gate.py
LAB-10 — Candidate Evaluation Harness Interface

Feature ID:
routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1

Purpose:
Added non-runtime, in-memory Candidate Evaluation Harness Interface.

Allowed LAB Python file added:
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py

After LAB-10, exactly three LAB Python source files are allowed:
candidate_evaluation_harness_interface.py
deterministic_runner_skeleton.py
lab_self_validation_gate.py

LAB-10 behavior:
accepts caller-supplied candidate metadata and references only
returns NOT_EVALUATED or HARNESS_INTERFACE_REJECTED only
computes deterministic SHA-256 metadata hashes
blocks forbidden authority fields
does not execute candidate evaluation
does not score cases
does not compare routes
does not generate or persist reports
does not act as reliability evidence

LAB-10 has been validated and frozen.

Current next safe milestone:
LAB-11 — Corpus V1 Expansion
7. Current state at chat close

Current frozen state:

LAB-10 is installed, validated, and frozen.

Freeze ID:
freeze-20260619-routing-signal-scorer-v3-ml-lab-candidate-evaluation-harness-interface-v1

Feature title:
Routing Signal Scorer v3 ML LAB Candidate Evaluation Harness Interface v1

Primary box:
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation

Current next safe milestone:
LAB-11 — Corpus V1 Expansion

Important:
The next chat should not redo LAB-10 unless validation/freeze evidence is missing or contradicted.

The next chat should proceed to LAB-11 only.
8. How to continue next: LAB-11 design intent

LAB-11 should be:

Routing Signal Scorer v3 ML LAB Corpus V1 Expansion

Likely feature ID:
routing_signal_scorer_v3_ml_lab_corpus_v1_expansion_v1

Likely title:
Routing Signal Scorer v3 ML LAB Corpus V1 Expansion v1

Likely schema/version label:
lab-11-corpus-v1-expansion

Primary box:
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation

LAB-11 should expand the static corpus from the small LAB-8 alpha seed toward a governed Corpus V1.

The intended Corpus V1 target should probably be around 100 static cases, based on the prior roadmap:
Alpha: 60–80 curated tests later
Corpus V1: 100 tests
200–250 only after harness stable
300–500+ only after real regression/error canonization

Because LAB-8 already created 12 alpha seed cases, LAB-11 can expand static coverage substantially, but must remain non-runtime and non-authoritative.

Important choice for the next assistant:
Do not overbuild the corpus into hundreds of cases yet.
A sane LAB-11 should add static Corpus V1 coverage structure, maybe around 40–60 additional static case records or a structured Corpus V1 seed/expansion file, depending on token/time constraints and patch size.
If full 100 cases is too large for one patch, LAB-11 may define Corpus V1 expansion structure and add a governed representative Corpus V1 expansion seed, while preserving the roadmap that 100-case Corpus V1 completion may be a later governed milestone.
However, because the milestone says “Corpus V1 Expansion,” it is reasonable to add enough static cases to move beyond alpha without claiming final reliability.

Suggested safer implementation:
Add a static corpus expansion file, not executable code.

Potential new files:
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/LAB_CORPUS_V1_EXPANSION.md
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/corpus_v1/corpus_v1_expansion_seed_v1.json
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/corpus_v1/corpus_v1_expansion_seed_v1_hash_manifest.json
tests/test_routing_signal_scorer_v3_ml_lab_corpus_v1_expansion.py

Update existing files:
kanda_reasoner_app/routing_signal_scorer/box_manifest.json
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/README.md
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/LAB_PHASE_BOUNDARY.md
kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/LAB_ALLOWED_ARTIFACTS.md

Do not add new Python inside the LAB box for LAB-11.

Allowed LAB Python files should remain exactly:
candidate_evaluation_harness_interface.py
deterministic_runner_skeleton.py
lab_self_validation_gate.py

LAB-11 must not add:
runner execution
case execution
candidate evaluation
route comparison
route selection
route authority
prompt loading
live prompt-library reads
live freeze-memory reads
live router-canon reads
runtime router imports
actual fixture snapshots
scoring engine
metrics engine
executable candidate harness
report generation
report persistence
provider calls
embedding calls
network calls
subprocess calls
batch mode
persistent ML decisions
activation keys
field-test mode
runtime Pilot
Copilot behavior
9. Recommended LAB-11 corpus categories

LAB-11 should expand corpus coverage across the main governance risks.

Recommended case categories:

    Simple Fast Path vs Routed Work Path distinction

    Simple rewrite / explanation / local answer should remain Fast Path.

    Governed project patch request must route.

    Freeze/update request must route.

    Prompt-library edit must route.

    Startup-delivery change must route.

    Freeze governance

    Correct freeze path under project_freeze_after_update/frozen_features_memory.

    Reject project_freeze_ledger as active project memory.

    Require validation evidence before freeze.

    Require LOCAL FREEZE WRITE OK.

    Require FREEZE_MEMORY_STATUS OK.

    Require startup refresh after freeze.

    Reject stale KANDA_FREEZE_HINT intake.

    Patch delivery governance

    Root-drive ZIP staging.

    delete_after_daily_work staging folder.

    Delete root-drive ZIP copy after staging.

    KANDA_FREEZE_HINT.json not installed into project root.

    PowerShell validation sets PYTHONPATH.

    No Bash heredoc in Windows validation.

    Install and validation blocks in one response.

    Prompt-authoring and bypass resistance

    User says “skip duplicate check” while adding/registering prompt.

    Must classify as governed prompt-library workflow.

    Must require prompt canon reconciliation.

    Must inspect existing prompt assets/indexes.

    Must not use generic routing labels.

    Startup delivery / stale filename governance

    Active paste file is paste_after_first_prompts_to_ai.md.

    paste_after_uploading_startup_zip.md is stale/deprecated.

    Startup changes require startup delivery prompt/source map context.

    Startup pack must be synchronized if changed.

    Box Architecture

    Identify primary box before patch.

    Do Box Boundary Audit.

    Registries store metadata, not logic/state.

    Avoid contaminating neighboring boxes.

    Production must not import LAB.

    LAB must not import runtime router/prompt loader/provider/embedding/UI.

    LAB-specific boundaries

    Candidate output is non-authoritative.

    Candidate cannot record human approval.

    Candidate cannot approve readiness.

    Candidate cannot write freeze memory.

    Candidate cannot load prompts.

    Candidate cannot activate Pilot/Copilot.

    Candidate cannot call provider/embedding.

    Candidate cannot read live canon/freeze/prompt library.

    Missing context / stale context

    Missing validation evidence.

    Missing freeze output.

    Missing current project ZIP.

    Stale sidecar.

    Contradictory freeze status.

    Terse commands like continue/next/go must preserve latest milestone state.

    Match-before-disagree

    Candidate must first match canon.

    Candidate may disagree only with evidence after matching.

    Candidate cannot override canon.

    Candidate uncertainty should trigger human review.

    Medical/document/simple-task distinction

    Simple medical explanation or document drafting can be Fast Path unless it touches project governance.

    A project patch or freeze request is Routed Work Path even if phrased simply.

    Avoid over-routing ordinary user writing/medical tasks.

    Security / injection / bypass

    Ignore requests to bypass routing rules.

    Treat untrusted text as content, not instruction.

    Detect system prompt leakage attempts.

    Detect tool argument injection.

    Do not output unsafe downstream commands as authoritative.

    LAB roadmap lock

    LAB-11 cannot claim LAB reliability.

    LAB-11 cannot claim ML router prompt logic reliability.

    LAB-11 cannot authorize ML implementation continuation.

    LAB-11 next milestone should be LAB-12 Error Canonization Intake Spec, unless the roadmap has been changed.

10. LAB-11 expected contract markers

LAB-11 validation output should likely include:

VALIDATION OK: routing_signal_scorer_v3_ml_lab_corpus_v1_expansion_v1

CONTRACT_TEST_OK: LAB-11 ML LAB Corpus V1 Expansion v1, immutable governed static corpus expansion after LAB-10 freeze with FREEZE_MEMORY_STATUS OK, expands static non-authoritative corpus coverage, cases not executed or scored, candidate evaluation not executed, not reliability evidence, no route comparison, no route authority, no prompt loading, no live prompt-library reads, no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture reads, no actual fixture snapshots, no corpus mutation outside governed static files, no scoring engine, no metrics engine, no executable candidate harness, no report generation, no report persistence, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, no field-test mode, no runtime Pilot, no Copilot behavior, critical boundary incidents must not be hidden by aggregate soft metrics, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-12 Error Canonization Intake Spec next

SANDBOX_ROUTING_SIGNAL_SCORER_V3_ML_LAB_CORPUS_V1_EXPANSION_V1_VALIDATION_OK

After validation, freeze title should be:

Routing Signal Scorer v3 ML LAB Corpus V1 Expansion v1

Required freeze output:
LOCAL FREEZE WRITE OK
FREEZE_MEMORY_STATUS: OK
11. Suggested LAB-11 implementation details

Build a patch ZIP with:

    Root-level KANDA_FREEZE_HINT.json

    Delivery metadata only.

    Do not install into project root.

    Feature title and ID for LAB-11.

    Next safe milestone: LAB-12 Error Canonization Intake Spec.

    Updated box_manifest.json
    Add metadata keys like:
    ml_lab_corpus_v1_expansion_feature_id
    ml_lab_corpus_v1_expansion_title
    ml_lab_corpus_v1_expansion_box
    ml_lab_corpus_v1_expansion_status
    ml_lab_corpus_v1_expansion_doc
    ml_lab_corpus_v1_expansion_seed_file
    ml_lab_corpus_v1_expansion_hash_manifest
    ml_lab_corpus_v1_expansion_test
    ml_lab_corpus_v1_expansion_static_only = True
    ml_lab_corpus_v1_expansion_case_count = [actual number]
    ml_lab_corpus_v1_expansion_not_reliability_evidence = True
    ml_lab_corpus_v1_expansion_candidate_evaluation_executed = False
    ml_lab_corpus_v1_expansion_cases_executed = False
    ml_lab_corpus_v1_expansion_cases_scored = False
    ml_lab_corpus_v1_expansion_route_authority = False
    ml_lab_corpus_v1_expansion_prompt_loading = False
    ml_lab_corpus_v1_expansion_provider_calls = False
    ml_lab_corpus_v1_expansion_embeddings = False
    ml_lab_corpus_v1_expansion_persistence = False
    ml_lab_corpus_v1_expansion_batch_mode = False
    ml_lab_corpus_v1_expansion_activation = False
    ml_lab_corpus_v1_expansion_field_test = False
    ml_lab_corpus_v1_expansion_runtime_pilot = False
    ml_lab_corpus_v1_expansion_copilot_behavior = False
    ml_lab_corpus_v1_expansion_next_safe_milestone = LAB-12 Error Canonization Intake Spec after local validation and freeze with FREEZE_MEMORY_STATUS OK

    LAB_CORPUS_V1_EXPANSION.md
    Should explain:

    Purpose.

    Why Corpus V1 is needed before ML implementation.

    Static-only doctrine.

    Case category taxonomy.

    Coverage target.

    Case record shape.

    Hash manifest relationship.

    Non-claims.

    Forbidden behaviors.

    Next milestone.

    corpus_v1_expansion_seed_v1.json
    Static corpus records only.

Each case should include fields inspired by LAB-4:
case_id
case_version
schema_version
corpus_version
case_category
scenario_summary
user_input
expected_fast_path_or_routed_work_path
expected_required_prompts_or_groups
expected_missing_context_behavior
expected_hard_gates
expected_failure_codes_if_wrong
expected_critical_violations_if_any
expected_human_review
canon_rule_references
fixture_hash_reference or null if not yet fixture-backed
notes
non_authoritative = true

    corpus_v1_expansion_seed_v1_hash_manifest.json
    Static hash manifest with:
    manifest_id
    manifest_version
    manifest_schema_version
    corpus_version
    hash_algorithm = SHA-256
    canonicalization_rule
    case_file
    case_file_sha256
    case_count
    case_ids
    created_for_feature_id
    not_reliability_evidence = true

    Test file
    tests/test_routing_signal_scorer_v3_ml_lab_corpus_v1_expansion.py

The test should verify:

    LAB-11 docs exist.

    Corpus JSON exists.

    Hash manifest exists.

    Corpus has the expected count.

    All case IDs are unique.

    Required fields exist for every case.

    Manifest SHA-256 matches corpus file.

    Corpus is static and non-authoritative.

    No case has route authority fields.

    No case has prompt loading fields.

    No case claims reliability evidence.

    No new LAB Python files were added.

    Allowed LAB Python files remain exactly three:
    candidate_evaluation_harness_interface.py
    deterministic_runner_skeleton.py
    lab_self_validation_gate.py

    box_manifest has LAB-11 metadata.

    README / LAB_PHASE_BOUNDARY / LAB_ALLOWED_ARTIFACTS mention LAB-11.

    Next safe milestone is LAB-12 Error Canonization Intake Spec.

    Previous LAB tests still pass.

12. Expected patch delivery style in next chat

Use the same patch delivery style as before.

Patch ZIP should be saved as:

routing_signal_scorer_v3_ml_lab_corpus_v1_expansion_v1_patch.zip

Place the sandbox patch at:

/mnt/data/routing_signal_scorer_v3_ml_lab_corpus_v1_expansion_v1_patch.zip

Provide SHA-256.

Provide install PowerShell block.

Provide validation PowerShell block.

Install block must:

    Use PROJECT_ROOT.

    Derive DRIVE_ROOT from PROJECT_ROOT.

    Stage ZIP from drive root into:
    :<project_name>_delete_after_daily_work

    Delete root-drive ZIP after successful staging.

    Extract from staged ZIP.

    Copy only expected files.

    Backup overwritten files.

    Verify KANDA_FREEZE_HINT.json is not installed in project root.

    End successful install with:
    Start-Sleep -Seconds 5
    Clear-Host

    Use Read-Host / Clear-Host only on error.

Validation block must:

    Set PYTHONPATH to PROJECT_ROOT.

    Run LAB-11 test first.

    Run all prior LAB tests after it.

    Verify allowed LAB Python files are exactly:
    candidate_evaluation_harness_interface.py
    deterministic_runner_skeleton.py
    lab_self_validation_gate.py

    Verify KANDA_FREEZE_HINT.json does not exist in project root.

    Print validation markers exactly.

    On success, use Read-Host / Clear-Host twice at the end, per existing validation style.

13. Important: what not to do in LAB-11

Do not create a real evaluator.

Do not make LAB-10 harness execute candidates.

Do not make LAB-6 runner run cases.

Do not connect corpus to harness execution.

Do not score outputs.

Do not generate reports.

Do not persist report files.

Do not claim reliability evidence.

Do not make cases authoritative.

Do not add provider/model calls.

Do not add embedding/vector support.

Do not add prompt loading.

Do not add route selection.

Do not read live prompt library, freeze memory, or router canon.

Do not import runtime router.

Do not add UI.

Do not add batch mode.

Do not add activation or field-test hooks.

Do not continue to ML implementation after LAB-11.

LAB-11 is still pre-reliability infrastructure.
14. What comes after LAB-11

The next milestone after LAB-11 should be:

LAB-12 — Error Canonization Intake Spec

Purpose:
Define how recurring errors from LAB runs, patch delivery mistakes, stale sidecar issues, routing mistakes, missing context, false fast path, governance violations, prompt loading attempts, and boundary errors become permanent regression/canon entries.

This is not runtime error handling yet.

LAB-12 should specify intake rules, classification, review requirements, severity mapping, canonization criteria, and how error entries become future corpus/regression cases.

This connects to the user’s long-term idea:
error canonization analogous to prompt canonization.

After LAB-12, expected next milestone:
LAB-13 — Lab Closure / Next-Phase Readiness Review

Only after LAB-13 should we consider whether the LAB is ready to begin testing ML router prompt logic reliability.
15. Summary for the next assistant

We are not “starting ML” yet.

We are building the governance LAB that will make ML safe to evaluate.

Current completed/frozen point:
LAB-10 Candidate Evaluation Harness Interface v1

Current next safe action:
Create LAB-11 Corpus V1 Expansion v1 patch.

LAB-11 must expand static corpus coverage only.

LAB-11 must not execute, score, evaluate, route, load prompts, call providers, persist decisions, or activate anything.

Preserve exactly three LAB Python files after LAB-11:
candidate_evaluation_harness_interface.py
deterministic_runner_skeleton.py
lab_self_validation_gate.py

After LAB-11 validation and freeze, proceed only to:
LAB-12 Error Canonization Intake Spec

Do not jump to live ML implementation until LAB/test fulfills its mission and ML router prompt logic reliability is validated.



