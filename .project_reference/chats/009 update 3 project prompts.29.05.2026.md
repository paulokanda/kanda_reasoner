0032C montage creator box edit derivations 19.05.2026.md
File
you are pyarchitect specialist in python , phd as a prompt engineer,  you nave 20 years of experien ce in the fiedl ,explain to me how updated files are delivery to user project , for example telme if: user asks a correction or code implementation, you build the file , in your sand box,  test it exaustivelyl for errors and if new or updated module  fits the project , chech if is created with interactions dinamically for use with multiple projects,  if the case check if  resolution goes from laptop to 4k, prevent bom,  keep files bellow 500 lines (ideally <=400 lines),  then backup original module for  the case when error occur with update( and restore if needed)  and  deliver resulted zip  to :\project_folder_base  , when I expand zip teh corrected files go directly to destiny folder adn dubstitute older file or create a new file ,  if during creation of file you detect error to be corrected alert user to correct it. Is that the whay the file is delivery in uploaded prompt? Do you understand that you willo audity chat uploaded , not implement it ?

I’ll treat this as an audit/explanation task only. I’ll inspect the uploaded handoff/prompt for the delivery protocol, compare it to your described workflow, and then state what is canon, what is recommended, and what must not be assumed.

Yes. I understand: this is an audit/explanation task, not an implementation task. I should inspect the uploaded chat/prompt and tell you whether the delivery workflow matches the PyArchitect/KANDA protocol.

Based on the uploaded handoff, the expected delivery workflow is essentially this:

    Audit first, do not patch blindly

        Identify the active box/owner.

        Ask for current live files if needed.

        Do not overwrite working code.

        Do not implement before target files, owner, and validation path are clear. The uploaded record repeatedly follows this pattern by requesting targeted ZIPs before patching and keeping each change as a focused gate.

    Build corrected files in the sandbox

        Reconstruct only the needed source files.

        Patch the smallest owner file/helper.

        Add focused checker and tests.

        Keep the bundle limited to one concern.

    Respect project architecture

        One box = one responsibility.

        Montage Creator cannot mutate RawCanonical/RawDerived, execute signal math, hydrate global dropdowns, or invade Diagnostic/qEEG boxes. The uploaded handoff explicitly repeats these no-cross-box rules for Montage Creator bundles.

    Use helper modules when needed

        If a module approaches the limit, split using <module_stem>_help.

        Helpers should have one responsibility, explicit imports, __all__, no circular imports.

        Keep files below 500 lines, ideally closer to 400. The uploaded handoff states this helper-module rule directly.

    Prevent encoding and platform problems

        New Python should be Windows/PyCharm compatible.

        UTF-8, no BOM.

        Avoid Unix-only assumptions.

        Use project-root arguments instead of hard-coded paths where possible.

    Validate before delivery

        At minimum: py_compile.

        Focused architecture checker.

        Focused pytest.

        For GUI features, also give manual GUI validation steps.

        The uploaded workflow repeatedly reports py_compile, architecture check, pytest result, line counts, and local validation commands.

    Deliver ZIP with correct folder structure

        ZIP root should contain project-relative folders such as:

            _bundle_temp/

            plugins/

            core/

            tools/

            dev_tools_tests/

        BUNDLE_MANIFEST...txt must be inside _bundle_temp.

        When you extract the ZIP inside the project base folder, corrected files should land directly in their real destination folders and replace/create files.

        The uploaded chat explicitly corrected a prior mistake where files were flattened and required preserving folder structure.

    Backup/restore

        This is a good requirement and should be part of the safest delivery model.

        Strictly speaking, the uploaded KANDA handoff emphasizes project-relative ZIP delivery, validation, and _bundle_temp manifest more than automated restore runners.

        For higher-risk patches, I should include either:

            backup instructions, or

            a patch runner that backs up originals before replacement and can restore on failure.

        For low-risk KANDA bundles, the current pattern has mostly been direct project-relative ZIP + validation commands.

So the answer is:

Yes, your described workflow is the correct PyArchitect direction, with one clarification: I can test thoroughly in the sandbox against the files you provide, but I cannot honestly claim “exhaustive” runtime/GUI testing unless the full app and runtime dependencies are available and executed. For GUI behavior, I must provide local PyCharm/Windows validation commands and a manual GUI checklist.

For this uploaded chat specifically, the delivery canon is:

audit -> request current files if needed -> focused patch in sandbox -> helper split if needed -> compile/check/test -> package ZIP with project-relative folders -> manifest inside _bundle_temp -> user extracts at project base -> user validates locally -> only then freeze/canonize.

And yes: I understand that right now you are asking me to audit the uploaded chat/prompt, not implement code.

you will create a state of art prompt ( to be used in any  project - project agnostic) to do all implementations discussed  and  add: for complex corrections do a roadmap of implementation ( inclusive to see it logic is correct because you can change it during roadmap). state for exaustive runtime testing "send complete project" if not sent do a regular testing. Warn user  "this is a complex update" risks. 
when requesting files  create a terminal  windows 11 in pycharm  code that scan project and create in root project a zip file to upload to you , when find large files (above 500 lines) ask use if  wnat to split in main file and help files.  the flus is ok , implement what is missing 

audit -> request current files if needed -> focused patch in sandbox -> helper split if needed -> compile/check/test -> package ZIP with project-relative folders -> manifest inside _bundle_temp -> user extracts at project base -> user validates locally -> only then freeze/canonize. Dit I miss something? Go

I’ll convert the whole workflow into a reusable master prompt, not tied to KANDA. I’ll also add the missing safety pieces: complexity warning, roadmap approval, full-project requirement for exhaustive runtime testing, rollback/backup discipline, and a Windows/PyCharm ZIP collector.

Yes. Your flow is correct. I would add a few missing safeguards:

    Classify task complexity before coding.

    For complex corrections, produce a roadmap first and let logic change during roadmap if problems are found.

    Warn the user clearly when the update is complex/risky.

    Never claim exhaustive runtime testing unless the complete project, dependencies, and runnable entry points were provided.

    If only targeted files were provided, say “regular targeted testing only.”

    Before patching, scan for large files over 500 lines and ask whether to split into main + help files.

    Always include backup/rollback guidance or backup runner for risky replacement.

    Always preserve project-relative folder structure in the ZIP.

    Freeze/canonize only after the user validates locally.

Below is the reusable project-agnostic master prompt.

You are PyArchitect, a senior Python software architect and implementation auditor.

Your job is to implement corrections safely in any Python project while preserving existing working code, architecture boundaries, runtime behavior, and user trust.

This prompt is project-agnostic. Do not assume any project-specific folder, framework, GUI library, runtime entry point, or architecture unless the user provides it.

CORE PRINCIPLES

1. Source of truth
- The current project files are the source of truth.
- Do not guess unseen code.
- Do not overwrite working code based on memory or assumptions.
- If required files are missing, ask the user to upload them using a Windows/PyCharm terminal ZIP command.

2. One concern per bundle
- One bundle must solve one clearly defined concern.
- Do not mix unrelated fixes.
- Do not touch unrelated boxes, modules, tabs, GUI areas, runtime systems, or data pipelines.

3. Respect architecture boundaries
- Identify the owner module, owner package, owner box, or owner layer before editing.
- Patch only the owning area unless a boundary adapter is strictly necessary.
- If another box must be touched, explicitly declare:
  - external owner
  - why it must be touched now
  - exact files touched
  - validation needed for both boxes

4. Preserve correct code
- Do not rewrite large working sections.
- Prefer narrow patches.
- Preserve public APIs unless the user explicitly approves a breaking change.
- Preserve existing names, imports, GUI behavior, storage formats, and tests unless the correction requires changing them.

5. No false testing claims
- If the complete project was not provided, do not claim exhaustive runtime testing.
- If only targeted files were provided, say:
  "Regular targeted testing was performed on the provided files only."
- To perform exhaustive runtime testing, request the complete project, dependencies, environment details, and runnable entry points.
- If GUI behavior must be verified, provide a manual GUI validation checklist.

TASK FLOW

Use this exact workflow unless the user explicitly requests otherwise:

audit -> request current files if needed -> classify complexity -> warn if complex -> roadmap for complex updates -> user approval if needed -> focused patch in sandbox -> helper split if needed -> compile/check/test -> package ZIP with project-relative folders -> manifest inside _bundle_temp -> user extracts at project base -> user validates locally -> only then freeze/canonize

STEP 1: AUDIT

Before implementation:
- Restate the target correction.
- Identify the owner files/modules.
- Identify what must not be touched.
- Identify expected behavior.
- Identify current known risk.
- Identify whether current files are sufficient.

Do not implement during audit unless the user explicitly asked for immediate implementation and all needed files are present.

STEP 2: REQUEST CURRENT FILES IF NEEDED

If files are missing or may be stale, ask the user to create a ZIP from the project root using a Windows 11 PyCharm terminal command.

Use this template and customize $IncludeHints for the current task.

WINDOWS 11 / PYCHARM TERMINAL ZIP COLLECTOR

Ask the user to run this from the project root in the PyCharm terminal:

```powershell
$ErrorActionPreference = "Stop"

$root = (Get-Location).Path
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$out = Join-Path $root ("_pyarchitect_requested_sources_" + $stamp + ".zip")
$temp = Join-Path $root ("_pyarchitect_requested_sources_" + $stamp)

if (Test-Path $temp) {
    Remove-Item $temp -Recurse -Force
}

New-Item -ItemType Directory -Path $temp | Out-Null

$ExcludeDirs = @(
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "build",
    "dist",
    ".eggs",
    "*.egg-info",
    "_pyarchitect_requested_sources_*",
    "_patch_backups",
    "_bundle_temp"
)

$AllowedExtensions = @(
    ".py",
    ".pyw",
    ".json",
    ".md",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".ps1",
    ".bat"
)

# Add task-specific path or filename hints here.
# Examples:
# $IncludeHints = @("montage", "creator", "diagnostic")
# $IncludeHints = @("main_window", "workflow", "validator")
$IncludeHints = @(
    "REPLACE_WITH_RELEVANT_HINT_1",
    "REPLACE_WITH_RELEVANT_HINT_2"
)

function Test-IsExcludedPath {
    param([string]$Path)

    foreach ($part in $ExcludeDirs) {
        if ($Path -like ("*" + [System.IO.Path]::DirectorySeparatorChar + $part + [System.IO.Path]::DirectorySeparatorChar + "*")) {
            return $true
        }
        if ($Path -like ("*" + [System.IO.Path]::DirectorySeparatorChar + $part)) {
            return $true
        }
    }
    return $false
}

function Test-MatchesHints {
    param([string]$RelativePath)

    if ($IncludeHints.Count -eq 0) {
        return $true
    }

    foreach ($hint in $IncludeHints) {
        if ([string]::IsNullOrWhiteSpace($hint)) {
            continue
        }
        if ($RelativePath.ToLower().Contains($hint.ToLower())) {
            return $true
        }
    }

    return $false
}

$allFiles = Get-ChildItem -Path $root -Recurse -File | Where-Object {
    -not (Test-IsExcludedPath $_.FullName) -and
    ($AllowedExtensions -contains $_.Extension.ToLower())
}

$selectedFiles = @()

foreach ($file in $allFiles) {
    $rel = Resolve-Path -Path $file.FullName -Relative
    $rel = $rel.TrimStart(".", "\", "/")

    if (Test-MatchesHints $rel) {
        $selectedFiles += $file
    }
}

# Always include likely governance and architecture files if present.
$AlwaysIncludePatterns = @(
    "*canon*",
    "*architecture*",
    "*manifest*",
    "*readme*",
    "*requirements*",
    "*pyproject*"
)

foreach ($pattern in $AlwaysIncludePatterns) {
    $matches = $allFiles | Where-Object { $_.Name.ToLower() -like $pattern.ToLower() }
    foreach ($match in $matches) {
        if ($selectedFiles.FullName -notcontains $match.FullName) {
            $selectedFiles += $match
        }
    }
}

$largeReport = Join-Path $temp "_pyarchitect_large_files_over_500_lines.txt"
"Large files over 500 lines:" | Out-File -FilePath $largeReport -Encoding utf8

foreach ($file in $allFiles) {
    if ($file.Extension.ToLower() -eq ".py") {
        $lineCount = (Get-Content -Path $file.FullName -ErrorAction SilentlyContinue).Count
        if ($lineCount -gt 500) {
            $rel = Resolve-Path -Path $file.FullName -Relative
            $rel = $rel.TrimStart(".", "\", "/")
            ($lineCount.ToString() + " lines - " + $rel) | Out-File -FilePath $largeReport -Append -Encoding utf8
        }
    }
}

foreach ($file in $selectedFiles) {
    $rel = Resolve-Path -Path $file.FullName -Relative
    $rel = $rel.TrimStart(".", "\", "/")
    $dst = Join-Path $temp $rel
    New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
    Copy-Item $file.FullName $dst -Force
}

if (Test-Path $out) {
    Remove-Item $out -Force
}

Compress-Archive -Path (Join-Path $temp "*") -DestinationPath $out -Force

Write-Host "Created ZIP:"
Write-Host $out
Write-Host ""
Write-Host "Upload this file to ChatGPT."
Write-Host ""
Write-Host "Large-file report is included at:"
Write-Host "_pyarchitect_large_files_over_500_lines.txt"

After receiving the ZIP:

    Inspect included files.

    Check the large-file report.

    If any relevant Python file is above 500 lines, ask:
    "This file is above 500 lines. Do you want me to split it into a small main file plus helper files before or during this correction?"

    Do not split large files without user approval unless the user already explicitly authorized it.

STEP 3: CLASSIFY COMPLEXITY

Classify the update:

Simple update:

    One small localized change.

    Low risk.

    No public API change.

    No GUI/routing/runtime behavior change.

    No large file refactor.

Moderate update:

    Multiple files.

    New helper.

    New test/checker.

    Some behavior change.

Complex update:

    GUI behavior.

    Runtime behavior.

    State management.

    Data persistence.

    Cross-module interactions.

    Large files.

    Public API changes.

    Refactor.

    Undo/redo/history.

    Async/threading/process behavior.

    Anything that can break existing workflows.

For complex updates, warn the user:

"This is a complex update. Risk areas are: [list]. I will not patch blindly. I will create a roadmap first, validate the logic, then implement one focused gate at a time."

STEP 4: ROADMAP FOR COMPLEX CORRECTIONS

For complex corrections, produce a roadmap before coding.

The roadmap must include:

    current problem

    desired behavior

    owner files

    files not to touch

    implementation gates

    validation for each gate

    rollback strategy

    risks

    what can change during the roadmap if audit reveals a better design

State clearly:
"The roadmap is allowed to change if the audit proves a different owner, safer sequence, or hidden dependency."

Do not implement the entire roadmap in one bundle.
Implement one gate at a time.

STEP 5: IMPLEMENTATION RULES

When implementing:

    Use the smallest safe patch.

    Keep project-root dynamic.

    Avoid hard-coded user-specific paths.

    Preserve imports and public APIs.

    Keep files below 500 lines whenever possible, ideally below 400.

    If adding helpers, use a clear helper folder pattern such as:
    <module_stem>_help

    Helper files should have:

        one responsibility

        explicit imports

        all when appropriate

        no circular imports

        no hidden runtime side effects

    Do not add broad framework dependencies unless the project already uses them.

    New Python files must be Windows/PyCharm compatible.

    Save as UTF-8 without BOM.

    Avoid terminal colors, emojis, control sequences, and platform-specific shell assumptions.

    Prefer standard Python 3.10+.

STEP 6: TESTING POLICY

Testing levels:

A. Regular targeted testing
Use when only targeted files were provided.
Run what is possible:

    py_compile for changed files

    import smoke test if possible

    focused architecture/check script if created

    focused unit tests if created

    static checks that do not need the full runtime

Required statement:
"Regular targeted testing was performed on the provided files only. This is not exhaustive runtime testing."

B. Exhaustive runtime testing
Only claim this if the user provided:

    complete project

    dependency list or working environment

    runnable entry points

    sample data if needed

    GUI/runtime instructions if relevant

If not provided, say:
"To perform exhaustive runtime testing, please send the complete project or a complete runnable project ZIP, plus dependency/environment instructions and the command used to launch the app."

For GUI features:

    Provide manual GUI validation checklist.

    Do not claim GUI validation unless actually run.

STEP 7: PACKAGING

Every implementation bundle must preserve project-relative folders.

Correct ZIP layout example:

bundle_temp/
BUNDLE_MANIFEST<gate_name>.txt

package_or_module/
corrected_file.py
helper_folder/
helper.py

tools/
architecture/
check_<gate_name>.py

dev_tools_tests/
test_<gate_name>.py

Rules:

    BUNDLE_MANIFEST must be inside _bundle_temp.

    Do not flatten files.

    Do not wrap the ZIP in an unnecessary top-level folder unless the user requested it.

    The user should be able to extract the ZIP at the project base folder and have files land directly in their destination folders.

STEP 8: BUNDLE MANIFEST

The manifest must include:

    gate name

    purpose

    files added

    files changed

    files not touched

    architecture boundaries respected

    validation performed

    local validation commands

    rollback notes

    whether testing was exhaustive or targeted

    warning if full project was not available

STEP 9: LOCAL VALIDATION COMMANDS

Always provide Windows/PyCharm terminal commands.

Example:

cd E:\path\to\project

python.exe -m py_compile path\to\changed_file.py
python.exe -m py_compile tools\architecture\check_gate_name.py
python.exe -m py_compile dev_tools_tests\test_gate_name.py

python.exe tools\architecture\check_gate_name.py --project-root .

$env:PYTHONPATH = "E:\path\to\project"
cd dev_tools_tests
python.exe -m pytest test_gate_name.py -q

Customize commands to the actual project root and files.

STEP 10: ROLLBACK / BACKUP

For risky patches, include backup or rollback guidance.

Options:

    user manually backs up affected files before extraction

    include backup instructions

    include a patch runner that backs up original files before replacing them

    include restore instructions

At minimum, say:
"Before extracting, make sure your project is under version control or back up the affected files."

For high-risk updates, do not rely only on manual backup.

STEP 11: USER VALIDATION BEFORE FREEZE

After delivering:

    Wait for user validation.

    If user reports failure, treat it as blocking.

    Do not canonize or freeze until the user validates locally.

When user validates:

    Mark the gate as validated.

    Then proceed to next gate or create governance/canon update if the project uses canon files.

STEP 12: CANON / FREEZE

Only freeze/canonize after:

    local user validation passed

    no blocking runtime/GUI issue remains

    the user explicitly confirms validation or the project protocol says this check is enough

If a later bug is found:

    reopen the box/gate

    correct the bug

    do not pretend the previous closure is still final

RESPONSE STYLE

When working:

    Keep the user informed with concise progress updates.

    Be honest about limitations.

    Do not claim unsupported validation.

    Do not say "done" if only code gates passed but GUI/manual validation is pending.

    For complex updates, explicitly say:
    "This is a complex update."

    For missing files, give a Windows/PyCharm ZIP command.

    For large files, ask whether to split into main + help files.

    For every bundle, give extraction and validation instructions.

FINAL DELIVERY CHECKLIST

Before answering with a delivery ZIP, confirm:

    Did I patch only the owner files?

    Did I avoid breaking correct code?

    Did I keep folder structure?

    Is BUNDLE_MANIFEST inside _bundle_temp?

    Did I include changed files?

    Did I include tests/checker when appropriate?

    Did I run py_compile?

    Did I run focused tests/checks?

    Did I state whether testing was targeted or exhaustive?

    Did I include local Windows validation commands?

    Did I include rollback/backup guidance?

    Did I wait for user validation before freeze/canon?

END OF PROMPT


This prompt includes everything we discussed. The one thing I would add operationally is: **for risky projects, prefer version control plus a backup runner**, not just ZIP extraction. That gives you a safer recovery path if a replacement breaks the app.


0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.0.md
File
do you think is better to update master prompt with this agnostic or send main "E:\developer_tools\_project_reference\PROMPTS\0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.2_BOX_LOGIC_CANON.md" and after send 0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md to AI or other better solution 

Yes — the better solution is not to paste the entire agnostic delivery protocol into every master prompt**.**

Best architecture:
Recommended prompt stack
1. Universal agnostic protocol

Create and maintain:

0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md

This file should contain only the reusable PyArchitect delivery workflow:

audit -> request current files if needed -> classify complexity -> warn if complex -> roadmap if complex -> focused patch -> helper split if needed -> compile/check/test -> ZIP with project-relative folders -> manifest inside _bundle_temp -> user extracts at project base -> user validates -> freeze/canonize

It should also include:

    Windows 11 / PyCharm ZIP collector.

    Large-file scanner over 500 lines.

    “Ask user before splitting large file.”

    Exhaustive runtime testing only if complete project is sent.

    Regular targeted testing if only targeted files are sent.

    Complex update warning.

    Roadmap-first rule.

    Backup/rollback rule.

    Correct ZIP delivery structure.

This becomes the universal delivery law for any project.
2. Project-specific startup canon

For each project, keep a project-specific master canon:

For Reasoner:

E:\developer_tools\_project_reference\PROMPTS\0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.2_BOX_LOGIC_CANON.md

For KANDA:

0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.0.md

The uploaded KANDA canon is clearly project-specific because it hardcodes the KANDA root, clinical EEG rules, RawCanonical/RawDerived, PySide6/MNE, and KANDA validation gates. It should not become the generic agnostic prompt.

So the project-specific master should contain:

    project root

    project boxes

    project validation gates

    project-specific safety laws

    project-specific canon update rules

    project-specific runtime constraints

It should reference the agnostic delivery protocol, not duplicate it fully.
3. Session handoff / current state file

At the start of a new chat, also send the latest current-state/handoff file:

0000 Canon Update Prompt use at start of each chat.md

This contains:

    last validated bundle

    open risks

    current box

    next step

    frozen contracts

    unfinished corrections

The uploaded canon already says the canon update file is the living session state and must be read at the start of each chat.
Best final setup

I recommend this hierarchy:

Layer 0 - Universal delivery protocol
0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md

Layer 1 - Project-specific startup canon
0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.2_BOX_LOGIC_CANON.md
or
0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.0.md

Layer 2 - Current session state / handoff
0000 Canon Update Prompt use at start of each chat.md

Precedence:

1. Actual source files and runtime logs
2. User’s current instruction
3. Current session handoff
4. Project-specific canon
5. Universal agnostic delivery protocol

But for delivery workflow, the universal protocol should override older delivery details if the project canon is outdated.
Important conflict to fix

Your uploaded KANDA canon still says the bundle manifest goes at the ZIP root.

But our newer validated workflow says:

BUNDLE_MANIFEST must be inside _bundle_temp

The Montage Creator handoff repeatedly corrected this and made _bundle_temp the active rule.

So I would update the project master prompts with a small compatibility patch:

Delivery protocol update:
If this project canon says BUNDLE_MANIFEST at ZIP root, that rule is superseded.
From now on, BUNDLE_MANIFEST_<gate>.txt must be inside _bundle_temp.
ZIP files must preserve project-relative folder structure.

Should you update the master prompt or send two files?

Best answer:
For long-term use

Update the master prompt with a short reference to the agnostic protocol, but keep the full agnostic protocol as a separate file.

Do not paste all of 0000 8 into every project canon. That makes the canon too large, hard to maintain, and more likely to conflict.

Add this block to each project master prompt:

UNIVERSAL DELIVERY PROTOCOL

This project follows:
0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md

That file controls:
- file request ZIP workflow
- complex-update warning
- roadmap-first rule
- regular vs exhaustive testing claims
- large-file scan and split decision
- project-relative ZIP delivery
- _bundle_temp manifest location
- backup/rollback expectations
- user validation before freeze/canon

If this project canon conflicts with the universal delivery protocol about delivery mechanics, the newer universal delivery protocol wins unless the user explicitly says otherwise.

Project-specific clinical/runtime/box rules still override the universal protocol for domain behavior.

For a new AI/chat before master is updated

Send both:

    Project-specific master canon

    0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md

    Current session handoff

That is safer because the AI cannot read your local E:\... path unless you upload the file.
My recommended naming

Use:

0000 8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.0.md

instead of:

0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md

The second name is understandable, but the first is cleaner and easier to reference inside other prompts.

For example:

0000 8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.0.md

Final recommendation

Use this system:

At start of any project chat, upload:

1. Project startup canon
2. Universal delivery protocol
3. Current session handoff
4. Relevant files or ZIP

Then, after you update the project startup canon to reference the universal protocol, you can usually upload only:

1. Project startup canon
2. Current session handoff
3. Relevant files or ZIP

But for maximum safety with a new AI, send all three.

So yes: update the master prompt, but do not merge everything into it.
Make the agnostic protocol a separate mandatory companion file and add a short “import/reference + precedence” block to each project-specific canon.

0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.0.md
File
0000 2.0 PYARCHITECT DAILY CANON STARTUP PROMPT.md
File
0000 3.5 KANDA PROFESSIONAL SOFTWARE ENGINEERING GOVERNANCE LAYER.md
File
0000 4.0 ACTIVE PROJECT GOVERNANCE RUN AT END OF CHAT.md
File
0000 5.4 updated V5 HOW REFACTOR LARGE MODULE 14.5.26.md
File
0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md
File
check_kanda_project_canon.py
Python
KANDA_PROJECT_CANON.json
File
KANDA_PROJECT_CANON.md
File
test_kanda_project_canon.py
Python
First I will send to you all prompts I send to you when whe start the day . Audit them , sugest changes if necessary , update names and version if necessary tell me the order to send . any correction  and implementation you think improve performance and correctness

I’ll audit these as a prompt stack, not as runtime code. I’ll look for overlap, contradictions, ordering problems, stale rules, and places where one file should be renamed or demoted to a companion protocol.

I found two real conflicts that should be fixed before you reuse this stack: manifest location and governance-file location. The rest is mostly good, but the stack can be made much shorter and safer by separating universal protocol, KANDA startup, current state, and end-of-chat governance.

Yes. I audited the prompt stack. The architecture is good, but it needs one cleanup pass because you currently have useful rules spread across files with a few contradictions.
Main audit result

Your prompt stack should not be one giant merged prompt. The best design is a layered prompt stack:

Layer 0 - Universal delivery protocol
Layer 1 - KANDA project startup canon
Layer 2 - Daily/current state canon
Layer 3 - Professional governance layer
Layer 4 - Special protocols only when needed
Layer 5 - Active governance files / current frozen state

This is better for performance because the AI receives the right rule at the right time, without duplicating everything every day.
The two conflicts to fix
1. Runtime/source bundle manifest location

Your KANDA startup canon still says:

Include a BUNDLE_MANIFEST_<descriptive_name>.txt at the ZIP root.

That appears in the bundle structure section.

But the newer professional governance layer says runtime/source bundles must place BUNDLE_MANIFEST files inside _bundle_temp.

Your active KANDA canon also confirms the newer rule:

Runtime/source bundles must keep BUNDLE_MANIFEST files inside _bundle_temp.

Correction: update KANDA Startup Canon v14.0 to v14.1 and replace “manifest at ZIP root” with:

Runtime/source bundles:
- BUNDLE_MANIFEST_<gate>.txt must be inside _bundle_temp.
- ZIP must preserve project-relative folder structure.
- Do not flatten files.
- Do not wrap in an unnecessary top-level folder.

Governance-only bundles:
- Follow the active governance delivery folder rule.

2. Governance file location conflict

Daily Canon Startup says all four governance files must live in:

tools\architecture

But the End-of-Chat Governance prompt says the governance-only ZIP must contain exactly the four files inside:

_project_reference/ACTIVE_PROJECT_GOVERNANCE/

and explicitly says not to place them under tools/architecture in that delivery ZIP.

The active KANDA canon agrees with _project_reference/ACTIVE_PROJECT_GOVERNANCE/ for governance-only delivery.

Correction: clarify there are two possible roles:

tools\architecture
= in-project executable/validator location, when the project itself expects the canon checker there.

_project_reference\ACTIVE_PROJECT_GOVERNANCE
= active reference/governance handoff location for end-of-chat governance-only ZIPs.

Do not mix the two in one delivery.

For your current workflow, I would make _project_reference\ACTIVE_PROJECT_GOVERNANCE the active end-of-chat governance delivery path, because your current canon, checker, and governance prompt already enforce it.
Prompt-by-prompt audit
0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md

Keep it, but rename and version it.

Recommended new name:

0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md

Why: it is project-agnostic and should load before KANDA-specific rules. It already has the strongest delivery workflow: no false runtime-testing claims, complete-project requirement for exhaustive runtime testing, exact task flow, and Windows/PyCharm ZIP collector.

Suggested changes:

    Add explicit “supersedes older manifest-at-root rules.”

    Add explicit “runtime/source manifest inside _bundle_temp.”

    Add “governance-only bundles may have a different folder rule if project canon says so.”

    Add “if complete project is not uploaded, validation is targeted only.”

Status: keep as universal law.
0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.0.md

Keep it, but update to:

0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md

It is excellent as the KANDA identity/project safety prompt. It defines clinical signal safety, RawCanonical/RawDerived, reference-before-montage, Windows/PyCharm, resolution independence, traceability, testing, and session start.

Required fixes:

    Replace manifest-at-ZIP-root with _bundle_temp.

    Remove or rename the section titled “GENERAL BOX POLICY FOR PROJECT REASONER” because this is a KANDA prompt. Keep the logic, but call it:

GENERAL BOX POLICY FOR ANY PYARCHITECT PROJECT

or

GENERAL BOX POLICY FOR KANDA AND OTHER PROJECTS

    Replace Unicode-heavy box headers in code examples with ASCII-only versions if you want maximum Windows/PyCharm safety. Your code-generation preferences ask for ASCII-safe Python, and some prompt headers currently use box-drawing characters.

    Add a short reference to the universal delivery protocol instead of duplicating delivery rules in full.

Status: keep as main KANDA startup, update to v14.1.
0000 2.0 PYARCHITECT DAILY CANON STARTUP PROMPT.md

Keep, but demote it into a daily loader, not a second canon.

Recommended new name:

0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md

Problem: it overlaps with KANDA Startup Canon and has the governance-location conflict. It says all four governance files must live inside tools\architecture, but your active governance workflow now uses _project_reference/ACTIVE_PROJECT_GOVERNANCE/.

Correction:

    Make it a short daily loader that asks for:

        current active governance ZIP,

        current handoff/session summary,

        current task,

        targeted source ZIP.

    Remove the long repeated box prompt from this file and reference the KANDA startup canon instead.

    Replace “manifest root” with _bundle_temp.

Status: keep, but shorten and reconcile.
0000 3.5 KANDA PROFESSIONAL SOFTWARE ENGINEERING GOVERNANCE LAYER.md

Keep as a companion governance layer.

Recommended new name:

0000 3.6 KANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md

This file is valuable because it adds requirements engineering, risk management, traceability, validation discipline, configuration management, migration discipline, and clinical software professionalism. It is explicitly subordinate to the clinical KANDA canon and says it must not override frozen clinical signal behavior.

Suggested change:

    Add one explicit pointer:

For delivery mechanics, use:
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md

    Keep the requirement that runtime/source bundles place manifests inside _bundle_temp.

Status: keep as high-risk/architecture companion.
0000 4.0 ACTIVE PROJECT GOVERNANCE RUN AT END OF CHAT.md

Keep, but rename to make its timing obvious.

Recommended new name:

0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md

This is not a start-of-day prompt. It is an end-of-chat governance update protocol. It correctly requires exactly four files, no runtime/source files, no unrelated manifests, and _project_reference/ACTIVE_PROJECT_GOVERNANCE/ as the ZIP internal path.

Status: send only at end of chat when updating governance, not every morning.
0000 5.4 updated V5 HOW REFACTOR LARGE MODULE 14.5.26.md

Keep, but only use when a large-module refactor is needed.

Recommended new name:

0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL v5.5.md

It has the right safety structure: Task 0 audit, Task 1 roadmap, stop points, line-count gates, ownership mapping, and no proceeding past Task 0 without actual files. It also bans passing 500 lines without split protocol and bans conflicting roadmaps.

Required cleanup:

    Remove the hardcoded scalp_landmark_seed.py execution demand at the end. That makes the prompt task-specific and dangerous for reuse.

    Add compatibility with the universal delivery protocol:

        manifest inside _bundle_temp for runtime/source bundles,

        no false exhaustive runtime testing claim,

        ask user before splitting unless already authorized.

Status: keep as special protocol, not daily startup.
Active governance files

Files:

KANDA_PROJECT_CANON.md
KANDA_PROJECT_CANON.json
check_kanda_project_canon.py
test_kanda_project_canon.py

These are the current frozen governance state. The markdown describes what each file is and records the active governance delivery path. The JSON has canon_version: 1.4.0, frozen gates, current box status, reference math canon, and LAR status.

Important: this current governance state is older than the Montage Creator derivations-editing work we just did. It still says Montage Creator is closed for this phase with bipolar transform-basis metadata freeze. In our recent work, Montage Creator was reopened for GUI editing workflow corrections. So the active governance files need an update later, but only after you decide which recent Montage Creator gates are validated/frozen and you explicitly approve the canon update.

Status: send at start if the AI needs current frozen state; update only after validated freeze.
Recommended daily send order

For a new chat starting KANDA work, send in this order:

1. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md
2. 0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md
3. 0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md
4. Current active governance ZIP or the four active governance files
5. Current session handoff / last-chat summary
6. Current task description
7. Relevant source ZIP

Only send these when needed:

0000 3.6 KANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md

Use for high-risk, architecture, signal, persistence, schema, runtime, or multi-box work.

0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL v5.5.md

Use only when a file is over 500 lines or you intentionally open a refactor pass.

0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md

Use only at the end of a chat when creating the governance-only ZIP.
Best performance improvement

Do not send all long prompts every time if the AI already has the project. Instead, create a very short Prompt Stack Loader:

0000 0.0 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md

Content should say:

Load these in order:
1. Universal Delivery Protocol
2. KANDA Startup Canon
3. Daily Startup Loader
4. Active Governance Files
5. Current Handoff
6. Current Task and Source ZIP

Precedence:
1. Current user instruction
2. Actual source files and runtime logs
3. Current active governance files
4. Current session handoff
5. KANDA startup canon
6. Universal delivery protocol
7. Professional governance layer
8. Large-module refactor protocol, only when invoked

Conflict rules:
- Runtime/source bundles use _bundle_temp for BUNDLE_MANIFEST.
- Governance-only bundles use _project_reference/ACTIVE_PROJECT_GOVERNANCE unless project explicitly opens tools/architecture governance.
- No exhaustive runtime testing claim unless complete project and runnable environment are provided.
- Complex updates require warning + roadmap first.

This loader would reduce confusion and tell the AI which file wins when prompts conflict.
Corrections I recommend implementing
Correction 1 — KANDA Startup v14.1

Change:

Include a BUNDLE_MANIFEST_<descriptive_name>.txt at the ZIP root.

to:

For runtime/source bundles, place:
_bundle_temp/BUNDLE_MANIFEST_<descriptive_name>.txt

For governance-only bundles, follow the active governance delivery path defined by the active governance canon.

Never flatten project-relative paths.

Correction 2 — Daily Startup v2.1

Replace the current long daily prompt with a short loader. It should no longer say all active governance files must live only in tools\architecture unless that is specifically the current project’s execution location.
Correction 3 — Large Refactor v5.5

Remove the scalp_landmark_seed.py request from the reusable prompt. Keep that as an example only, not an active command.
Correction 4 — Professional Governance v1.6

Add a cross-reference to the universal delivery protocol and preserve its _bundle_temp rule.
Correction 5 — Active governance canon v1.5.0 later

Once you approve, update active governance from 1.4.0 to 1.5.0 to record the validated Montage Creator derivations editing workflow corrections. Do not do this until you explicitly approve which gates are frozen.
My final recommendation

Use this as your standard system:

Daily start:
- 0000 0.0 Prompt Stack Load Order
- 0000 0.8 Universal Delivery Protocol
- 0000 1.0 KANDA Startup Canon
- 0000 2.1 Daily Startup Loader
- active governance files
- current handoff
- task/source ZIP

During work:
- add Professional Governance only for high-risk work
- add Large Refactor Protocol only for >500-line/refactor work

End of chat:
- use End-of-Chat Active Governance Update prompt

I would not merge everything into one master prompt. The better solution is a small load-order file plus specialized prompt layers.

ok add another feature :   Ai should orient user: "now I will need this or that prompt to implement... , upload to me" .
create all these new stat of art files, check for correctness in your sandbox , send in a zip , when zip is unziped in this case  only  they  are in _project_reference/PROMPTS and tell me which prompt each one substitute

I’ll create the updated prompt set as real .md files, validate them for consistency, package them so extraction places everything under _project_reference\PROMPTS, and include a substitution map.

I’m going to produce eight files: a new prompt-stack loader, six updated prompt files, and a substitution map. The key correction will be to keep runtime/source bundle manifests in _bundle_temp while preserving the separate active-governance ZIP rule.

Done. I created the updated prompt stack ZIP.

Download it here:

When unzipped, every file lands only under:

_project_reference/PROMPTS/

I validated in the sandbox:

PASS
Files: 8
ZIP structure: only _project_reference/PROMPTS/
UTF-8: no BOM
ASCII-safe: yes
Old runtime/source manifest-at-ZIP-root rule: removed
New _bundle_temp runtime/source manifest rule: present
Prompt-request behavior: present
Substitution map: included

Files created

_project_reference/PROMPTS/0000 0.0 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
_project_reference/PROMPTS/0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md
_project_reference/PROMPTS/0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md
_project_reference/PROMPTS/0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md
_project_reference/PROMPTS/0000 3.6 KANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md
_project_reference/PROMPTS/0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md
_project_reference/PROMPTS/0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL v5.5.md
_project_reference/PROMPTS/0000 PROMPT SUBSTITUTION MAP v1.0.md

Which prompt each one substitutes
New prompt	Substitutes
0000 0.0 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md	New file. No old direct equivalent.
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md	0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md
0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md	0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.0.md
0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md	0000 2.0 PYARCHITECT DAILY CANON STARTUP PROMPT.md
0000 3.6 KANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md	0000 3.5 KANDA PROFESSIONAL SOFTWARE ENGINEERING GOVERNANCE LAYER.md
0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md	0000 4.0 ACTIVE PROJECT GOVERNANCE RUN AT END OF CHAT.md
0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL v5.5.md	0000 5.4 updated V5 HOW REFACTOR LARGE MODULE 14.5.26.md
What I corrected

I added the new behavior you requested: the AI must now orient the user before implementation by saying which prompt is needed, for example: “For this task I need these prompt files before implementation: ... Please upload them or confirm they are already loaded.”

I also corrected the main contradictions from the old prompt stack. The old universal delivery prompt already had the right core flow and testing honesty rule, including targeted versus exhaustive testing and _bundle_temp delivery behavior. The old end-of-chat governance prompt required exactly four governance files inside _project_reference/ACTIVE_PROJECT_GOVERNANCE/, with no runtime files. The old daily prompt still centered canon delivery under tools\architecture, so I replaced that with a loader that respects the active governance path instead of hardcoding only one location. The old large-module prompt contained the correct Task 0/Task 1 approval discipline, but also had a task-specific scalp_landmark_seed.py execution demand at the end, so I removed that from the reusable version.
Suggested unzip command

From the folder where you want _project_reference\PROMPTS created:

$root = "E:\developer_tools"
$zipPath = "E:\pyarchitect_prompt_stack_v2026_05_29.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force

Write-Host "Prompt stack installed under:"
Write-Host "$root\_project_reference\PROMPTS"

If this is for KANDA instead of developer_tools, change $root to:

E:\eeg_kernel_ai_neural_data_analysis


these prompts are for E:\eeg_kernel_ai_neural_data_analysis , are they specific enough? If not do you want the project to make them specific or are they good enough?

Yes — for E:\eeg_kernel_ai_neural_data_analysis, the new prompts are specific enough for startup, delivery, safety, and governance workflow.

But they are not meant to replace the current project state. They are the stable operating system. The current project reality still comes from:

1. Active governance files
2. Current session handoff
3. Current source ZIP
4. Runtime logs / GUI observations

So the answer is:
They are good enough for daily use

The prompt stack is specific enough because it includes:

    KANDA project root: E:\eeg_kernel_ai_neural_data_analysis

    RawCanonical / RawDerived safety

    reference-before-montage rule

    Montage Creator / Diagnostic / Runtime box separation

    Windows/PyCharm delivery workflow

    _bundle_temp manifest rule

    active governance ZIP rule

    large-module refactor protocol

    prompt-request behavior: AI must tell user which prompt it needs before implementation

That is enough to guide safe work.
I do not recommend making the startup prompts too project-specific

Do not put every current module, file, gate, and feature state inside the startup prompt.

Reason: the project changes every day. If we make the startup prompt too specific, it becomes stale and may mislead the AI.

Better architecture:

Static prompts = permanent laws
Active governance = current frozen state
Session handoff = what happened last
Source ZIP = truth of current code

That is safer.
When would I need more project specificity?

Only if you want one more file:

0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md

This would not contain static laws. It would be a template you fill at the end of each work session with:

Current active box:
Last validated gate:
Last delivered ZIP:
Current GUI status:
Open bugs:
Next safe gate:
Do-not-touch boxes:
Files recently modified:
Validation results:

That would improve continuity more than making the master prompts larger.
Do I need the whole project to make these prompts more specific?

No, not for the prompt stack.

I only need the whole project if you want:

    project-wide architecture map

    current module ownership map

    current large-file list

    automatic box/file owner rules

    current validation command inventory

    full runtime testing guidance

For normal KANDA work, the current approach is better: upload targeted source ZIPs when needed.
My recommendation

Use the prompts as they are now, with one addition later:

Add:
0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md

Do not make the main startup prompt bigger.

The daily send order remains:

1. 0000 0.0 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md
3. 0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md
4. 0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md
5. Active governance files or active governance ZIP
6. Current handoff/session summary
7. Current task and source ZIP

Use special prompts only when needed:

Professional governance layer -> high-risk architecture/signal/persistence work
Large module refactor protocol -> files above 500 lines
End-of-chat governance update -> only when freezing/updating governance

So: they are good enough. I would not ask for the full project just to rewrite them. I would only add a lightweight current-handoff template.

you suggested "0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md"

but I have _project_reference/PROMPTS/0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md , is it the same content?

No. They are not the same.
0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md

This is for formal canon/governance update.

Use it only when you want the AI to create or update the official active governance files:

KANDA_PROJECT_CANON.md
KANDA_PROJECT_CANON.json
check_kanda_project_canon.py
test_kanda_project_canon.py

It is strict and governance-only. It says the ZIP must contain exactly those four files inside:

_project_reference/ACTIVE_PROJECT_GOVERNANCE/

and must not include runtime/source files. It also requires baseline governance files and consistent checker/test updates.

So this prompt is for:

"Update the official project constitution after a validated freeze."

0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md

This would be different.

It would be a lightweight session-continuity handoff, not a governance update.

It would record:

Current active box
Current task
Last validated gate
Last delivered ZIP
Open bugs
Known risks
Files recently modified
Next safe gate
What not to touch
Manual GUI validation status
Terminal validation status

It would not update the official canon.

It would not create the four active governance files.

It would not freeze behavior by itself.

So this prompt is for:

"Tell the next AI exactly where we stopped and what to do next."

Best analogy

0000 4.1 = official legal document update
0000 6.0 = shift handoff note between engineers

Both are useful, but they solve different problems.
My recommendation

Keep 0000 4.1 exactly for governance/canon updates.

Add 0000 6.0 as a short handoff template used at the end of any long work session, especially when you are not ready to freeze canon yet.

Example:

Use 0000 6.0 when:
- we made progress but did not finish the box
- GUI validation is pending
- bugs remain open
- next AI needs context
- canon should not be updated yet

Use 0000 4.1 when:
- a gate is validated
- you explicitly approve freeze/canon update
- the official governance files must be updated

So yes: I still recommend adding 0000 6.0. It complements 0000 4.1; it does not replace it.

0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md is also use at end of day's work?

Yes. 0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md is also used at the end of the day’s work, but with a different purpose from 0000 4.1.

Use it like this:

End of normal workday / break / unfinished task:
Use 0000 6.0

Purpose: create a handoff for the next AI/chat.

It should record:

Current active box
What we did today
Last validated gate
Last delivered ZIP
What passed
What failed
Open bugs
GUI validation still needed
Next safe step
Files recently touched
Do-not-touch boxes
Known risks

It does not freeze canon by itself.

Use this only when there is an official validated freeze:

End of chat with validated canon/governance update:
Use 0000 4.1

Purpose: create/update the official four governance files:

KANDA_PROJECT_CANON.md
KANDA_PROJECT_CANON.json
check_kanda_project_canon.py
test_kanda_project_canon.py

Best end-of-day rule:

Always use 0000 6.0 at the end of a work session.

Use 0000 4.1 only if a validated gate must be frozen into official governance.

So the end-of-day sequence can be:

1. Summarize current implementation state with 0000 6.0.
2. If something was validated and should become official canon, then also run 0000 4.1.
3. Next day, upload the startup prompts + active governance + latest 6.0 handoff.

In short:

0000 6.0 = daily engineering handoff
0000 4.1 = official governance/canon update


gimme 0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md

I’ll create the handoff template as a real Markdown file so you can place it directly under _project_reference\PROMPTS.

Created:

Use it at the end of the day or before a break to create a continuation handoff. It complements 0000 4.1; it does not replace the official governance update prompt.

do you remember all we did here?

Yes. We did three main things here:
1. Audited the PyArchitect/KANDA delivery workflow

We confirmed the correct implementation flow:

audit -> request current files if needed -> classify complexity -> warn if complex -> roadmap if complex -> focused patch in sandbox -> helper split if needed -> compile/check/test -> package ZIP with project-relative folders -> manifest inside _bundle_temp -> user extracts at project base -> user validates locally -> only then freeze/canonize

We also clarified:

    exhaustive runtime testing requires the complete project, dependencies, runnable entry points, and sample data if needed;

    otherwise the AI must say testing was only targeted/regular;

    complex updates require roadmap-first;

    large files over 500 lines should trigger a split discussion;

    the AI should ask which prompt it needs before implementation.

2. Audited and reorganized your daily prompt stack

You uploaded the KANDA startup canon, daily startup prompt, professional governance layer, end-of-chat governance update prompt, large-module refactor protocol, universal delivery protocol, and active governance files.

We found two important conflicts:

    Old prompt said BUNDLE_MANIFEST at ZIP root.

    New validated rule says runtime/source BUNDLE_MANIFEST must be inside _bundle_temp.

We also found the governance-location conflict:

    tools\architecture for in-project canon/governance files in some flows;

    _project_reference\ACTIVE_PROJECT_GOVERNANCE for end-of-chat governance-only ZIPs.

We decided the best architecture is a layered prompt stack, not one giant prompt.

Recommended order:

1. 0000 0.0 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md
3. 0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md
4. 0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md
5. Active governance files or active governance ZIP
6. Current handoff/session summary
7. Current task and source ZIP

Special prompts only when needed:

0000 3.6 KANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md
0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL v5.5.md
0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md

3. Created updated prompt files

I created a ZIP containing updated state-of-art prompt files that unzip only into:

_project_reference/PROMPTS/

The ZIP created was:

pyarchitect_prompt_stack_v2026_05_29.zip

It included:

0000 0.0 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md
0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md
0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md
0000 3.6 KANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md
0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md
0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL v5.5.md
0000 PROMPT SUBSTITUTION MAP v1.0.md

Then you asked whether they were specific enough for:

E:\eeg_kernel_ai_neural_data_analysis

I said yes: they are specific enough for startup, delivery, safety, and governance workflow, but should not replace current active governance, handoff, source ZIPs, or runtime logs.
4. Created the new daily handoff template

You asked about:

0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md

We clarified that it is different from 0000 4.1.

    0000 6.0 = daily engineering handoff / shift note.

    0000 4.1 = official governance/canon update.

Then I created the actual Markdown file:

0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md

It is meant to be used at the end of the day or before a break, especially when work is not ready for official canon freeze.

So yes: I remember the full direction. We built a cleaner PyArchitect prompt system for KANDA with better delivery discipline, prompt-request behavior, _bundle_temp manifests, governance separation, and a new daily handoff template.

which prompts I send to you every day?

Every day, for KANDA / E:\eeg_kernel_ai_neural_data_analysis, send these in this order:

1. 0000 0.0 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md
3. 0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md
4. 0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md
5. Current active governance files or active governance ZIP
6. Latest 0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE output
7. Current task description
8. Relevant source ZIP

Use these only when needed:

0000 3.6 KANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md

Send it when the task is high-risk: runtime signal, reference math, persistence, schema, clinical label logic, architecture, or multi-box work.

0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL v5.5.md

Send it when a file is above 500 lines or you are intentionally opening a large refactor.

0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md

Send it at the end only when you want to update/freeze the official governance files.

So the daily minimum is:

0.0 load order
0.8 universal delivery
1.0 KANDA startup canon
2.1 daily startup loader
active governance
latest 6.0 handoff
task
source ZIP


I changed name , send this too 0000 0.1 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md?

Yes. Send it too, but use the new name instead of the old one.

Replace:

0000 0.0 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md

with:

0000 0.1 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md

Daily order becomes:

1. 0000 0.1 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md
3. 0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md
4. 0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md
5. Current active governance files or active governance ZIP
6. Latest 0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF output
7. Current task description
8. Relevant source ZIP

The 0.1 name is fine. It actually makes sense because it marks the load-order prompt as an early controller file before the 0.8 universal delivery protocol.

0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.2_BOX_LOGIC_CANON.md
File
0000 2.0 PYARCHITECT DAILY REASONER CANON STARTUP PROMPT V14.0.md
File
0000 3.5 KANDA REASONER PROFESSIONAL SOFTWARE ENGINEERING GOVERNANCE LAYER.md
File
0000 4.10 ACTIVE PROJECT REASONER GOVERNANCE RUN AT END OF CHAT.md
File
0000 5 1b HOW REFACTOR LARGE MODULE 14.5.26_claude.md
File
0000 6 best techinic to split giant files.md
File
0000 6 HOW SEND FILES UPDATED.md
File
0000 6 zip_checkpoint.md
File
0000 7 SOLVE A SET OF PROBLEMS.28.06.2026.md
File
0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md
File
ok now same way we will audit  jetbrains://pycharm/navigate/reference?project=developer_tools&path> to correct and make prompts state of art 

I’ll do the same workflow for Project Reasoner: audit the uploaded prompt stack, correct contradictions, rename/version the prompt layers, add the “AI must ask for the needed prompt before implementation” rule, and package the upgraded files under _project_reference\PROMPTS.

The biggest Reasoner-specific conflict is delivery mechanics: one uploaded prompt says normal source bundles use _project_reference\BUNDLE_MANIFEST, while another generic/chunk rule still mentions _bundle_temp. I’ll resolve that by making Reasoner’s project-specific rule win: manifests go under _project_reference\BUNDLE_MANIFEST, patch runners under _patch_backups, and governance-only ZIPs under _project_reference\ACTIVE_PROJECT_ GOVERNANCE.

Done. I audited the Project Reasoner prompt stack and created the updated state-of-art prompt bundle.

Download:

When unzipped, it places files only under:

_project_reference/PROMPTS/

I validated in the sandbox:

PASS
Files: 11
ZIP structure: only _project_reference/PROMPTS/
UTF-8 without BOM: yes
ASCII-safe: yes
Old generic manifest-at-root rule removed from active replacements
Reasoner manifest rule preserved: _project_reference\BUNDLE_MANIFEST
Governance-only rule preserved: _project_reference\ACTIVE_PROJECT_ GOVERNANCE
Prompt-request behavior added
Substitution map included

What I corrected

The Reasoner startup canon already defines the correct product identity: E:\developer_tools, kanda_reasoner_app, dynamic PROJECT_ROOT, GUI-first workflow, static/runtime/reader separation, and source truth over guesses.

The daily and end-of-chat prompts both enforce the Reasoner governance path as:

_project_reference\ACTIVE_PROJECT_ GOVERNANCE\

with the space preserved, and they explicitly say not to normalize it or place those four governance files under tools\architecture.

The Reasoner startup prompt also had a specific bundle-manifest rule for source/code bundles:

_project_reference\BUNDLE_MANIFEST\BUNDLE_MANIFEST_<task_slug>.txt

so I kept that as the Reasoner-specific rule instead of forcing the KANDA _bundle_temp rule onto developer_tools.

I also merged the successful source-preserving facade split technique into the new large-module protocol, because that technique was developed after the MODULE_TOO_LARGE cleanup and is specifically useful when semantic extraction is too risky.
Files created

_project_reference/PROMPTS/0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.0.md
_project_reference/PROMPTS/0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.2.md
_project_reference/PROMPTS/0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.3.md
_project_reference/PROMPTS/0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.1.md
_project_reference/PROMPTS/0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md
_project_reference/PROMPTS/0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.2.md
_project_reference/PROMPTS/0000 5.6 REASONER LARGE MODULE REFACTOR AND SOURCE-PRESERVING FACADE PROTOCOL v5.6.md
_project_reference/PROMPTS/0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md
_project_reference/PROMPTS/0000 6.1 REASONER CHECKPOINT ZIP PROTOCOL v1.0.md
_project_reference/PROMPTS/0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.0.md
_project_reference/PROMPTS/0000 PROMPT SUBSTITUTION MAP REASONER v1.0.md

Which prompt each one substitutes
New prompt	Substitutes
0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.0.md	New file
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.2.md	0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md
0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.3.md	0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.2_BOX_LOGIC_CANON.md
0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.1.md	0000 2.0 PYARCHITECT DAILY REASONER CANON STARTUP PROMPT V14.0.md
0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md	0000 3.5 KANDA REASONER PROFESSIONAL SOFTWARE ENGINEERING GOVERNANCE LAYER.md
0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.2.md	0000 4.10 ACTIVE PROJECT REASONER GOVERNANCE RUN AT END OF CHAT.md
0000 5.6 REASONER LARGE MODULE REFACTOR AND SOURCE-PRESERVING FACADE PROTOCOL v5.6.md	0000 5 1b HOW REFACTOR LARGE MODULE 14.5.26_claude.md and 0000 6 best techinic to split giant files.md
0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md	New file
0000 6.1 REASONER CHECKPOINT ZIP PROTOCOL v1.0.md	0000 6 zip_checkpoint.md
0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.0.md	0000 7 SOLVE A SET OF PROBLEMS.28.06.2026.md
0000 6 HOW SEND FILES UPDATED.md	Merged into 0000 0.8 and 0000 1.0
Daily send order for developer_tools

1. 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.0.md
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.2.md
3. 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.3.md
4. 0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.1.md
5. Active governance ZIP or four active governance files
6. Latest 0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF output
7. Current task description
8. Relevant source ZIP, logs, and validation output

Use special prompts only when needed:

0000 3.6 -> high-risk architecture, schema, retrieval, prompt, AI bridge, runtime, GUI lifecycle, or multi-box work
0000 5.6 -> large-module or source-preserving facade refactor
0000 6.1 -> checkpoint before risky correction
0000 7.1 -> batch of problems requiring roadmap
0000 4.11 -> official governance update after validated freeze

Suggested unzip command

$root = "E:\developer_tools"
$zipPath = "E:\pyarchitect_reasoner_prompt_stack_v2026_05_29.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force

Write-Host "Prompt stack installed under:"
Write-Host "$root\_project_reference\PROMPTS"


this patch runner increases working time because we have to unzip it ,  then check if it exists (see uploaded chat ,  them run it and validade ti change to be as in eeg_kernel_ai_neural_data_analysis. sandbox file created or updated send files zipped in correct folders, and remove patch runners under _patch_backups and other logic in promps diferent from eeg_kernel_ai_neural_data_analysis promps to unify prompt logic. 

I agree. For Reasoner, the prompt stack should use the same delivery philosophy as KANDA: I create/update files in the sandbox, validate them, and deliver one ZIP with project-relative folders. No patch runner should be required just to install prompt/source updates.

I will replace the Reasoner-specific manifest path with the KANDA-style source bundle rule: implementation ZIPs include _bundle_temp\BUNDLE_MANIFEST_...txt and all changed files in final destination folders. The only separate rule I will keep is governance-only delivery, because Reasoner’s active governance folder is project-specific.

You are right. I corrected the Reasoner prompt stack to match the KANDA/eeg delivery logic:

    No required patch runner.

    No required _patch_backups workflow.

    No source-bundle manifest under the older Reasoner-specific manifest folder.

    Source/runtime/prompt bundles now use KANDA-style direct ZIP delivery.

    The AI creates or updates files in the sandbox, validates them, and sends one ZIP with final project-relative folders.

    Runtime/source BUNDLE_MANIFEST files go inside _bundle_temp.

    Governance-only ZIPs still use Reasoner’s active governance folder: _project_reference\ACTIVE_PROJECT_ GOVERNANCE\.

Download the corrected ZIP:

I validated:

PASS
Files: 10
ZIP structure: only _project_reference/PROMPTS/
UTF-8 without BOM: yes
ASCII-safe: yes
No _patch_backups reference
No patch-runner requirement
No source-bundle manifest-at-root rule
No older Reasoner-specific manifest-folder rule
KANDA-style _bundle_temp manifest rule present
Direct extract-to-project-root ZIP delivery present

The conflict existed because the uploaded Reasoner startup canon still had a separate source-bundle manifest location rule, while the daily/professional prompt also contained chunked _bundle_temp logic. I removed that divergence and made the Reasoner prompt stack follow the same source-bundle delivery model we established for KANDA. The governance-only path remains project-specific because the Reasoner daily and end-of-chat prompts explicitly protect _project_reference\ACTIVE_PROJECT_ GOVERNANCE\ as the active governance folder.
New files in the corrected ZIP

_project_reference/PROMPTS/0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
_project_reference/PROMPTS/0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3.md
_project_reference/PROMPTS/0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4.md
_project_reference/PROMPTS/0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2.md
_project_reference/PROMPTS/0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md
_project_reference/PROMPTS/0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.3.md
_project_reference/PROMPTS/0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md
_project_reference/PROMPTS/0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md
_project_reference/PROMPTS/0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.1.md
_project_reference/PROMPTS/0000 PROMPT SUBSTITUTION MAP REASONER v1.1.md

Main substitutions

0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4.md
replaces v14.3 / v14.2_BOX_LOGIC_CANON

0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2.md
replaces v14.1 / v14.0

0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md
replaces v5.6 and the older large-module/source-preserving prompts

0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md
replaces v1.0

Removed from active stack:
0000 6.1 REASONER CHECKPOINT ZIP PROTOCOL v1.0.md

Install

$root = "E:\developer_tools"
$zipPath = "E:\pyarchitect_reasoner_prompt_stack_unified_kanda_delivery_v2026_05_29.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force

Write-Host "Prompt stack installed under:"
Write-Host "$root\_project_reference\PROMPTS"


which files each one of new files substitute?
what send every start of chat?
what send in special ocasions?
does the updated prompt asks for a specific prompt  when necessary?

Yes.
1. Which new file substitutes each old file?
New file	Substitutes
0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md	New file. No old direct equivalent.
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3.md	0000 8 STATE OF ART AGNOSTIC HOW DELIVER FILE TO USER.md and most of 0000 6 HOW SEND FILES UPDATED.md
0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4.md	0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.2_BOX_LOGIC_CANON.md
0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2.md	0000 2.0 PYARCHITECT DAILY REASONER CANON STARTUP PROMPT V14.0.md
0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md	0000 3.5 KANDA REASONER PROFESSIONAL SOFTWARE ENGINEERING GOVERNANCE LAYER.md
0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.3.md	0000 4.10 ACTIVE PROJECT REASONER GOVERNANCE RUN AT END OF CHAT.md
0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md	0000 5 1b HOW REFACTOR LARGE MODULE 14.5.26_claude.md and 0000 6 best techinic to split giant files.md
0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md	New file. Daily/end-of-work handoff template.
0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.1.md	0000 7 SOLVE A SET OF PROBLEMS.28.06.2026.md
0000 PROMPT SUBSTITUTION MAP REASONER v1.1.md	New file. It documents the substitutions.

Removed from active stack:

0000 6 zip_checkpoint.md
0000 6.1 REASONER CHECKPOINT ZIP PROTOCOL v1.0.md

Reason: you asked to remove patch-runner/checkpoint style logic and unify Reasoner delivery with the KANDA style: sandbox-created files, validated, delivered as a direct ZIP in final folders.
2. What to send every start of chat?

For Project Reasoner / E:\developer_tools, send this every new work chat:

1. 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3.md
3. 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4.md
4. 0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2.md
5. Active governance ZIP or the four active governance files
6. Latest 0000 6.0 handoff output from the previous session
7. Current task description
8. Relevant source ZIP, logs, validation output, or screenshots

The active governance files are:

_project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.md
_project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.json
_project_reference\ACTIVE_PROJECT_ GOVERNANCE\check_reasoner_project_canon.py
_project_reference\ACTIVE_PROJECT_ GOVERNANCE\test_reasoner_project_canon.py

The latest 6.0 handoff output is not the template itself; it is the actual handoff note generated at the end of the last session.
3. What to send in special occasions?
High-risk architecture / runtime / GUI / schema / prompt work

Send:

0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md

Use for:

schema changes
retrieval changes
prompt builder changes
AI bridge behavior
runtime collector behavior
static/runtime boundary changes
GUI lifecycle
thread/process behavior
multi-box changes
architecture governance

Large files or refactor work

Send:

0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md

Use when:

a file is above 500 lines
a file is approaching 500 lines and will grow
a module needs helper-folder decomposition
a source-preserving facade split may be needed
a large refactor must be done safely

A batch of problems

Send:

0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.1.md

Use when you give the AI several warnings/errors/problems and want it to create an optimal correction roadmap.
End of day / break / unfinished task

Use:

0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md

Purpose: generate the next-chat handoff.

This does not update official governance. It is a shift note.
Official governance/canon update

Send only after a validated freeze:

0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.3.md

Use when you want the AI to update the official four governance files.
4. Does the updated prompt ask for a specific prompt when necessary?

Yes.

The updated stack tells the AI to orient you before implementation, for example:

For this task, I need the following prompt files before implementation:
1. 0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md
2. 0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md

Please upload them or confirm they are already loaded.

Examples:

If the task is a large module warning:

AI should request:
0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md

If the task changes retrieval/prompt/schema/GUI lifecycle:

AI should request:
0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md

If the task is to update official canon after validation:

AI should request:
0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.3.md

If the work is ending or being handed off:

AI should request or use:
0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md

So the answer is: yes, the updated prompts include the “ask the user for the needed prompt before implementation” behavior.

0000 6 best techinic to split giant files.md
File
0000 6 HOW SEND FILES UPDATED.md
File
0000 PROMPT SUBSTITUTION MAP REASONER v1.1.md
File
0002b PyArchitect v11.0 — Canonical Code Update ProtocoL.deepseek_09.05.2026.md
File
0003 HOW CONTINUE IN NEXT CHAT.md
File
0004 ALL_AT_ONCE_PROMPT.md
File
0029 audito canonical shadow conflicts 09.05.2026.md
File
kanda_reasoner_app Specialized Prompt_26.03.2026.md
File
PYARCHITECT_PROMPT_v5_kanda_reasoner_app.md
File
I also have these other prompts , audit if they are of use with new important commands of if I can deprecate then

I’ll classify each extra prompt as keep, merge, archive/reference-only, or deprecate. I’ll also identify any useful commands or rules that should be preserved in the active Reasoner stack.

Yes. Audit result: most of these can be deprecated because the important parts are already absorbed into the new Reasoner prompt stack.
Final decision
Uploaded prompt	Decision	Why
0000 6 best techinic to split giant files.md	Deprecate as active prompt. Archive as historical reference.	Its important content, especially the source-preserving facade split, unique shard symbols, CLI-safe facade, and validation lessons, is already merged into 0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md.
0000 6 HOW SEND FILES UPDATED.md	Deprecate.	It conflicts internally: first says no ZIP binary and structured text output, then later says “send all files in one zip.” The useful part, direct project-relative ZIP delivery, is already in the new universal delivery protocol.
0000 PROMPT SUBSTITUTION MAP REASONER v1.1.md	Keep active.	This is the current map that tells which new prompt replaces which old one and records the new direct-ZIP delivery logic.
0002b PyArchitect v11.0 — Canonical Code Update Protocol...	Deprecate.	It has older bundle rules, including manifest at ZIP root, and generic rules that can conflict with Reasoner because it treats developer_tools, _project_reference, and dev_tools_docs as non-canonical architecture truth. That is dangerous for Project Reasoner, where E:\developer_tools is the actual tool root.
0003 HOW CONTINUE IN NEXT CHAT.md	Deprecate.	Replaced by 0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md. The old prompt forces “implement missing filters/features” and “freeze every non-frozen item,” which is unsafe for the new governance flow.
0004 ALL_AT_ONCE_PROMPT.md	Deprecate as daily prompt. Optional archive only.	It is a one-module full-replacement workflow. The useful concepts, analyze-plan-implement-triple-check, are already covered by the universal delivery and large-module protocols.
0029 audito canonical shadow conflicts 09.05.2026.md	Archive as historical KANDA hardening evidence. Do not use as active Reasoner prompt.	It contains useful architecture-hardening ideas: public-symbol ownership, layer boundaries, duplicate normalizers, session cleanup, allowlists, and staged hardening. But it is KANDA/EEG-specific and includes old patch-script/bundle behavior.
kanda_reasoner_app Specialized Prompt_26.03.2026.md	Deprecate.	Its key Reasoner concepts, GUI-first, dynamic PROJECT_ROOT, static/runtime/V10 separation, prompt/retrieval ownership, are now covered more safely in Reasoner Startup Canon v14.4.
PYARCHITECT_PROMPT_v5_kanda_reasoner_app.md	Deprecate.	It is an older Reasoner operating protocol with stale roadmap steps and older one-edit/anchor workflow. The important rules are already incorporated into the new stack.
What should remain active

Keep only these for Project Reasoner:

0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3.md
0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4.md
0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2.md
0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md
0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.3.md
0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md
0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md
0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.1.md
0000 PROMPT SUBSTITUTION MAP REASONER v1.1.md

Useful content already preserved

The only older content I would not lose is:

    Source-preserving facade split from 0000 6 best techinic...
    Already preserved in 0000 5.7.

    Direct project-relative ZIP delivery from HOW SEND FILES UPDATED
    Already preserved in 0000 0.8, corrected to remove patch-runner friction.

    Architecture hardening checklist from 0029 audito canonical shadow conflicts...
    Not yet a clean active Reasoner prompt. I would either archive it or convert it later into a new optional prompt:

0000 8.0 REASONER ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md

Use that only if you want to run a structured hardening campaign: public facades, layer boundaries, session-state writes, duplicate normalizers, and staged allowlists.
My recommendation

Move deprecated files to:

_project_reference\PROMPTS\_deprecated\

Keep active files only in:

_project_reference\PROMPTS\

Do not send the deprecated files at chat startup. They increase prompt conflict and can make the AI follow older delivery rules.

gimme 0000 8.0 REASONER ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md

I’ll create it as a Markdown prompt file, aligned with the unified Reasoner delivery rules: direct ZIP delivery, _bundle_temp manifest, no patch runners, and explicit prompt-request behavior.

Created and validated:

Validation:

ASCII-safe: yes
UTF-8 without BOM: yes
Aligned with direct ZIP delivery: yes
No patch-runner requirement: yes
Uses _bundle_temp manifest rule: yes
Includes prompt-request behavior: yes


now a summary of what send at start of day

what send in special ocasions, by the way maim prompt asks for file when needed?

Yes. The main prompt stack now tells the AI to ask for the needed prompt/files before implementation.

For example, if the task is a large-module refactor, the AI should say:

For this task, I need:
0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md
Please upload it or confirm it is already loaded.

If the task is architecture hardening, it should ask for:

0000 8.0 REASONER ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md

Send at the start of every Reasoner workday/chat

For Project Reasoner / E:\developer_tools, send these every day, in this order:

1. 0000 0.1 PYARCHITECT REASONER PROMPT STACK LOAD ORDER v1.1.md

2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.3.md

3. 0000 1.0 PYARCHITECT REASONER STARTUP CANON v14.4.md

4. 0000 2.1 PYARCHITECT DAILY REASONER STARTUP LOADER v14.2.md

5. Active governance ZIP or the four active governance files:
   _project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.md
   _project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.json
   _project_reference\ACTIVE_PROJECT_ GOVERNANCE\check_reasoner_project_canon.py
   _project_reference\ACTIVE_PROJECT_ GOVERNANCE\test_reasoner_project_canon.py

6. Latest 0000 6.0 handoff output from the previous session

7. Current task description

8. Relevant source ZIP, logs, validation output, screenshots, or error text

Important: for item 6, send the actual handoff generated at the end of the last session, not just the template file.
Send only in special occasions
1. High-risk architecture, schema, runtime, GUI, prompt, retrieval, or multi-box work

Send:

0000 3.6 REASONER PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.7.md

Use when the task touches:

schema
collector output
index loader
retrieval
prompt builder
AI bridge
runtime collector
GUI lifecycle
thread/process behavior
project-root logic
cross-box boundaries

2. Large module or refactor work

Send:

0000 5.7 REASONER LARGE MODULE REFACTOR PROTOCOL v5.7.md

Use when:

a Python file is above 500 lines
a file is approaching 500 lines and will grow
helper-folder split is needed
source-preserving facade split may be needed
public API must be preserved during refactor

3. Architecture hardening / warning cleanup campaign

Send:

0000 8.0 REASONER ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md

Use when working on:

public facade warnings
__init__.py cleanup
layer-boundary violations
box-boundary violations
duplicate normalizers
session-state writes
project-root hardcoding
shadow paths
architecture warning cleanup

4. Several problems at once

Send:

0000 7.1 REASONER PROBLEM SET ROADMAP SOLVER v1.1.md

Use when you paste many warnings/errors and want the AI to prioritize them.
5. End of day / break / unfinished work

Use:

0000 6.0 REASONER CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md

Purpose: create the next-chat handoff.

This is not canon. It is an engineering shift note.
6. Official governance/canon update

Send only after a validated freeze:

0000 4.11 REASONER END-OF-CHAT ACTIVE GOVERNANCE UPDATE v14.3.md

Purpose: update the official four governance files.

Do not use it for normal work or unfinished tasks.
Main daily rule

Daily minimum:

0.1 load order
0.8 universal delivery
1.0 Reasoner startup canon
2.1 daily startup loader
active governance
latest 6.0 handoff output
task
source/log ZIP

Then let the AI request extra prompts when needed.
Final answer

Yes: the updated main prompt system should now orient you like this:

For this task, I need these additional prompt files before implementation:
...
Please upload them or confirm they are already loaded.

That behavior is now part of the Reasoner prompt workflow.

0000 PROMPT SUBSTITUTION MAP v1.0.md
File
0003_CANONIC_DROPDOWN.md
File
0004_One_module_at_Once.md
File
0006 JUST PRJECT INDEX CREATION.md
File
0006AJUST PRJECT INDEX CREATION TEXT.md
File
0008. MERGED PRJECT INDEX PLUS PY REFACTOR.md
File
0008.1 MERGED PRJECT INDEX PLUS PY REFACTOR TIERS.md
File
0011_ EEG_DECISION_TABLE_FROZEN_29.03.2026.md
File
0018 DETECT CANONICAL SHADOW CONFLICTS 09.05.2026.md
File
GENERAL_BOX_PROMPT_REUSABLE_ANY_PROJECT.txt
Document
GENERAL_SMALL_PROMPT.md
File
great I love your performance. thanks for your work. Do you remember  what we did in E:\eeg_kernel_ai_neural_data_analysis? I forgot to ask for other prompts if they are deprecated . Check files uploaded if any thing is usefull lets keep if not deprecate

I’ll separate this into two parts: what we already stabilized for E:\eeg_kernel_ai_neural_data_analysis, and what each newly uploaded old prompt should become: active, special-use, archive, or deprecated.

Yes, I remember what we did for E:\eeg_kernel_ai_neural_data_analysis.

We built the KANDA prompt stack, corrected the delivery workflow, added daily handoff logic, separated official governance from daily engineering handoff, and later canonized important project-specific rules like:

E:\eeg_kernel_ai_neural_data_analysis\developer_tools is non-canonical.

That means developer_tools inside the EEG project must be ignored for project architecture and should be removed/isolated if referenced by canonical project code. This rule appears explicitly in the uploaded 0003_CANONIC_DROPDOWN.md.

We also canonized the dropdown system: central dropdown sizing, scrollable left-anchored lanes, _dropdown_width_scale = 1.0, no editable QComboBox + lineEdit() caption path, and the non-editable caption adapter as the stable fix for the first-letter clipping bug. That same uploaded file preserves the dropdown inventory and final canonical dropdown state.
Audit of the newly uploaded KANDA/EEG prompts
File	Decision	Reason
0000 PROMPT SUBSTITUTION MAP v1.0.md	Keep, but update to v1.1	Useful. It documents the KANDA prompt replacements, daily upload order, _bundle_temp manifest rule, prompt-request behavior, targeted vs exhaustive testing, and roadmap-first behavior. It still says 0000 0.0 for the load-order file, but you renamed that to 0000 0.1, and it does not yet include 0000 6.0 handoff.
0003_CANONIC_DROPDOWN.md	Keep as special KANDA canon/reference	Very useful. It contains two important canonical blocks: developer_tools exclusion and final dropdown architecture. I would split or rename it into a cleaner prompt: 0000 8.0 KANDA CANONICAL DROPDOWN STATE DO NOT REGRESS v1.0.md.
0004_One_module_at_Once.md	Deprecate	Replaced by the new Universal Delivery Protocol and Large Module Refactor Protocol. Its “one module per reply” model is too narrow for the current ZIP-based workflow.
0006 JUST PRJECT INDEX CREATION.md	Deprecate / archive only	It is a structural navigation protocol requiring ARCHITECTURE.md, __init__.py, file docstrings, and navigation indexes. Useful historically, but too rigid as an active KANDA daily prompt. It also forces architecture artifacts on every split, which may conflict with current KANDA governance flow.
0006AJUST PRJECT INDEX CREATION TEXT.md	Deprecate as duplicate/older variant	Same structural-navigation content as above. Keep only as archive if you want history.
0008. MERGED PRJECT INDEX PLUS PY REFACTOR.md	Deprecate as active prompt	It merges structural navigation and refactor execution, but is too heavy and conflicts with our newer layered prompt stack. Useful ideas are already absorbed into KANDA startup + large-module refactor protocol.
0008.1 MERGED PRJECT INDEX PLUS PY REFACTOR TIERS.md	Archive only	The tier idea is good, but we already implemented it better as the KANDA prompt stack: load order, universal delivery, startup canon, daily loader, special prompts.
0011_ EEG_DECISION_TABLE_FROZEN_29.03.2026.md	Keep as active special clinical/domain canon	Very important. It freezes EEG acquisition inference, channel identity resolution, role classification, contradiction handling, registry integrity, and manual override rules. Use it whenever working on import, channel registry, acquisition profile, channel labels, EMG/ECG/EOG classification, or manual channel resolution.
0018 DETECT CANONICAL SHADOW CONFLICTS 09.05.2026.md	Keep the ideas, but update into a new KANDA v1.0 hardening prompt	Useful for architecture hardening: public facade conflicts, layer boundaries, runtime state mutation, duplicate normalizers, allowlists, and staged cleanup. But as-is it is older and should be modernized to match the new direct-ZIP delivery logic.
GENERAL_BOX_PROMPT_REUSABLE_ANY_PROJECT.txt	Deprecate as active prompt	Box logic is already inside the KANDA startup canon and daily loader. This file still contains older manifest-at-root wording, so sending it now could confuse delivery rules.
GENERAL_SMALL_PROMPT.md	Deprecate	Too generic. The same identity is already expressed in the KANDA startup canon and universal delivery protocol.
What I would keep active for KANDA

Daily/start-of-chat stack:

0000 0.1 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.1.md
0000 1.0 PYARCHITECT KANDA STARTUP CANON v14.1.md
0000 2.1 KANDA DAILY STARTUP LOADER v2.1.md
Active governance ZIP or four active governance files
Latest 0000 6.0 handoff output
Current task description
Relevant source ZIP/logs

Special-use prompts to keep:

0000 3.6 KANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.6.md
0000 4.1 KANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v2.0.md
0000 5.5 PYARCHITECT LARGE MODULE REFACTOR PROTOCOL v5.5.md
0000 6.0 KANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md
0011_ EEG_DECISION_TABLE_FROZEN_29.03.2026.md

I would add two cleaned special prompts:

0000 8.0 KANDA CANONICAL DROPDOWN STATE DO NOT REGRESS v1.0.md
0000 8.1 KANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md

Best deprecation action

Move these to:

_project_reference\PROMPTS\_deprecated\

0004_One_module_at_Once.md
0006 JUST PRJECT INDEX CREATION.md
0006AJUST PRJECT INDEX CREATION TEXT.md
0008. MERGED PRJECT INDEX PLUS PY REFACTOR.md
0008.1 MERGED PRJECT INDEX PLUS PY REFACTOR TIERS.md
GENERAL_BOX_PROMPT_REUSABLE_ANY_PROJECT.txt
GENERAL_SMALL_PROMPT.md

Keep these in active or special prompt folders:

0000 PROMPT SUBSTITUTION MAP v1.0.md -> update to v1.1
0003_CANONIC_DROPDOWN.md -> convert to 0000 8.0 KANDA CANONICAL DROPDOWN STATE DO NOT REGRESS v1.0.md
0011_ EEG_DECISION_TABLE_FROZEN_29.03.2026.md -> keep active special canon
0018 DETECT CANONICAL SHADOW CONFLICTS 09.05.2026.md -> convert to 0000 8.1 KANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md

So the short answer: yes, several files still contain useful canon, but most should not be sent anymore as daily prompts. The useful material should be preserved in cleaner special-purpose prompts, and the old overlapping prompts should be deprecated to avoid conflicting instructions.

0000 0.1 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
File
update name and content of  files to state of art prompt , they will stay at _project_reference/PROMPTS folder , update main prompt to also call them when needed :

0000 PROMPT SUBSTITUTION MAP v1.0.md -> update to v1.1
0003_CANONIC_DROPDOWN.md -> convert to 0000 8.0 KANDA CANONICAL DROPDOWN STATE DO NOT REGRESS v1.0.md
0011_ EEG_DECISION_TABLE_FROZEN_29.03.2026.md -> keep active special canon
0018 DETECT CANONICAL SHADOW CONFLICTS 09.05.2026.md -> convert to 0000 8.1 KANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md, test files in sand box for correctness and if they fit project before send.

I’ll update the KANDA prompt stack as a real prompt ZIP: revised load-order prompt, updated substitution map, cleaned dropdown canon, cleaned EEG decision-table canon, and KANDA hardening triage prompt. I’ll validate encoding, naming, internal references, and ZIP layout before sending.

I found the specific update needed in the uploaded load-order prompt: it still names itself internally as 0000 0.0 while your filename is 0000 0.1, and it does not yet call the dropdown, EEG decision-table, or KANDA hardening prompts. I’m correcting that in v1.1.

Done. I updated the KANDA prompt files, tested them in the sandbox, and packaged them so they extract directly into:

_project_reference\PROMPTS\

Download:

Validation report:

Validation passed:

PASS
Files: 5
ZIP structure: only _project_reference/PROMPTS/
UTF-8 without BOM: yes
ASCII-safe: yes
Internal prompt references: checked
Main load-order prompt updated to request special prompts when needed

Files in the ZIP

_project_reference/PROMPTS/0000 0.1 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.1.md
_project_reference/PROMPTS/0000 PROMPT SUBSTITUTION MAP v1.1.md
_project_reference/PROMPTS/0000 8.0 KANDA CANONICAL DROPDOWN STATE DO NOT REGRESS v1.0.md
_project_reference/PROMPTS/0000 8.1 KANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md
_project_reference/PROMPTS/0011 KANDA EEG DECISION TABLE FROZEN SPECIAL CANON v1.1.md

What each file substitutes
New file	Substitutes
0000 0.1 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.1.md	0000 0.1 PYARCHITECT KANDA PROMPT STACK LOAD ORDER v1.0.md
0000 PROMPT SUBSTITUTION MAP v1.1.md	0000 PROMPT SUBSTITUTION MAP v1.0.md
0000 8.0 KANDA CANONICAL DROPDOWN STATE DO NOT REGRESS v1.0.md	0003_CANONIC_DROPDOWN.md
0011 KANDA EEG DECISION TABLE FROZEN SPECIAL CANON v1.1.md	0011_ EEG_DECISION_TABLE_FROZEN_29.03.2026.md
0000 8.1 KANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md	0018 DETECT CANONICAL SHADOW CONFLICTS 09.05.2026.md
Main prompt updated

The load-order prompt now explicitly tells the AI to request:

0000 8.0 KANDA CANONICAL DROPDOWN STATE DO NOT REGRESS v1.0.md

when working on dropdowns, combobox sizing, caption adapters, scroll lanes, filter-panel lanes, or navbar/action dropdowns.

It now requests:

0011 KANDA EEG DECISION TABLE FROZEN SPECIAL CANON v1.1.md

when working on acquisition inference, EEG channel identity, EMG/ECG/EOG handling, T3/T4/T5/T6 alias rules, manual override, registry integrity, or contradictions.

It now requests:

0000 8.1 KANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md

when working on facade warnings, layer boundaries, developer_tools contamination, duplicate normalizers, session-state writes, or architecture hardening.

The uploaded old load-order prompt already had the prompt-request mechanism and fixed _bundle_temp delivery rule, but still had the old internal 0.0 name and lacked routing for these three special KANDA prompts.
Install

$root = "E:\eeg_kernel_ai_neural_data_analysis"
$zipPath = "E:\kanda_prompt_specials_v2026_05_29.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force

Write-Host "Updated prompts installed under:"
Write-Host "$root\_project_reference\PROMPTS"


0000 0.00 what send every day NOT PROMPT.md
File
now update this file 

I’ll update this as a practical checklist file, not as an AI prompt. I’ll replace the old v1.0 load-order name with v1.1, add the new special prompts, and fix the incomplete end-of-chat governance section.

The uploaded checklist is outdated in three places: it still points to 0.1 ... v1.0, omits the new dropdown/EEG/hardening special prompts, and has a broken governance/refactor section where two instructions run together.

The uploaded file is read-only in the sandbox, so I’ll create a v1.1 replacement file instead of overwriting the uploaded original.

Updated and validated.

Download the updated file:

Validation report:

I updated it from the old checklist, which still referenced 0000 0.1 ... v1.0, lacked the new special prompts, and had the governance/refactor lines merged incorrectly in the uploaded file.

Validation passed:

UTF-8 without BOM: yes
ASCII-safe: yes
Updated load-order prompt: v1.1
Dropdown prompt included: yes
EEG decision-table prompt included: yes
Architecture hardening prompt included: yes


.coverage
File
.pykanda_runtime_guard.json
File
__init__.py
Python
_pyarchitect_collect_errors.py
Python
_pyarchitect_fix_helper_without_main.py
Python
ARCHITECTURE.md
File
architecture_manifest.json
File
check_runtime_trace_schema.py
Python
collect_montage_reference_consistency_files.py
Python
eeg_amplitude_map.h5
File
electrode_lists.txt
Document
error_files.log
File
found_filter_toolbar_files.txt
Document
import_translation_map_v2.json
File
KANDA_PROJECT_CANON.md
File
kanda_prompt_specials_validation_report.json
File
plugins__montage_editor__montage_head_selector__fix14b.py
Python
README.md
File
remaining_legacy_import_scanner.py
Python
remaining legacy imports report
file	line	import_type	imported_module
plugins\filter_panel\helpers\default_custom_buttons_lane.py	21	from	k06_templates.tooltip_template
plugins\filter_panel\helpers\default_custom_buttons_lane.py	25	from	k06_templates.tooltip_template
tests\shell\viewer\test_initialize_main_plot.py	3	from	k01_core_eeg.k01_4_visualizer_render.visu_initialize_main_plot
now , the projet root is messy tell me what I can delete from these files in root

I’ll classify the root files into “keep in root,” “move to proper folder,” “safe to delete after backup,” and “do not delete unless you confirm obsolete.” I’ll treat deletion conservatively because some files may be generated evidence or one-off migration tools.

Yes. Based on the files you uploaded, your project root contains several temporary PyArchitect/migration artifacts that should not stay at root.

I would not delete immediately. First move them to a quarantine folder, run the app/tests, then delete after a few days.

Recommended quarantine folder:

E:\eeg_kernel_ai_neural_data_analysis\_cleanup_quarantine_root_2026_05_29\

Safe to move out of root now

These look like temporary reports, generated evidence, one-off tools, or stale root artifacts.
File	Recommendation	Why
.coverage	Move/delete	Coverage cache. Regenerates when running coverage.
.pykanda_runtime_guard.json	Move/delete if you do not need old guard state	It shows zero failures and old runtime-guard state.
_pyarchitect_collect_errors.py	Move/delete	Temporary PyArchitect evidence collector that creates _pyarchitect_error_batch. Not normal root source.
_pyarchitect_fix_helper_without_main.py	Move/delete	One-off repair script for a previous helper-folder naming problem. Not normal app source.
collect_montage_reference_consistency_files.py	Move/delete	One-off collector that zips selected montage files. Also has BOM in the uploaded file, so it should not stay as active source.
kanda_prompt_specials_validation_report.json	Move to _project_reference\PROMPTS\_validation_reports\ or delete	It is only a validation report for prompt files.
found_filter_toolbar_files.txt	Move/delete	Search-result list, not source. It even includes old DEVELOPER TOOLS paths.
error_files.log	Move/delete	Temporary log; points to migration_auditor_v2.py.
remaining_legacy_imports_report.csv	Move to migration archive or delete after use	Output report from legacy-import scanner.
plugins__montage_editor__montage_head_selector__fix14b.py	Move/delete after confirming applied	Flattened patch artifact. The real file should live at plugins\montage_editor\montage_head_selector.py, not project root.
Move, but keep for reference

These are useful but should not be in root.
File	Move to	Why
import_translation_map_v2.json	_project_reference\migration\import_translation_map_v2.json	Useful migration map from old imports to new imports.
remaining_legacy_import_scanner.py	tools\migration\remaining_legacy_import_scanner.py or _project_reference\migration\tools\	Useful scanner, but it is a dev/migration tool, not root source.
check_runtime_trace_schema.py	tools\runtime\check_runtime_trace_schema.py if still used	Useful validator, but should live under tools, not root.
electrode_lists.txt	_project_reference\clinical_reference\electrode_lists.txt	Useful reference list of primary, extended, ear, and posterior-ear electrodes.
KANDA_PROJECT_CANON.md	_project_reference\ACTIVE_PROJECT_GOVERNANCE\KANDA_PROJECT_CANON.md	Active governance should not sit loose in root. The file contains frozen canon and roadmap sections.
eeg_amplitude_map.h5	data\, outputs\, or _runtime_outputs\ depending on your app convention	It is an HDF5 data/output file, not root source. I would not delete until you confirm it is not a real saved amplitude map.
Probably delete/archive, but verify first

These look like artifacts from the older “project index / module map” approach that we have now deprecated.
File	Recommendation	Why
__init__.py at project root	Strong candidate to remove from root after testing	It is auto-generated and imports migration tools. It also creates __module_map__, which belongs to the older indexing approach, not the cleaned KANDA prompt system.
ARCHITECTURE.md	Archive, then remove from root if not actively used	It says it is generated from architecture_manifest.json, so it is derived, not primary truth.
architecture_manifest.json	Archive, then remove from root if not actively used	Generated on 2026-05-02 and includes root artifacts like plugins__montage_editor__montage_head_selector__fix14b.py, suggesting stale/contaminated indexing.
README.md	Review before deleting	It says the project uses the __module_map__ pattern, which we have been moving away from. If this is not your real README, archive/delete it.
What I would keep in root

From this uploaded set: probably none of these must stay in root, except possibly README.md if you want a project README there.

A clean KANDA root should mostly contain true project entry/config items, for example:

shell\
core\
plugins\
common\
tests\
_project_reference\
tools\
pyproject.toml / requirements.txt if present
README.md only if it is the real current README

Safe cleanup command

Use move-to-quarantine first:

$root = "E:\eeg_kernel_ai_neural_data_analysis"
$quarantine = Join-Path $root "_cleanup_quarantine_root_2026_05_29"

New-Item -ItemType Directory -Path $quarantine -Force | Out-Null

$items = @(
    ".coverage",
    ".pykanda_runtime_guard.json",
    "__init__.py",
    "_pyarchitect_collect_errors.py",
    "_pyarchitect_fix_helper_without_main.py",
    "ARCHITECTURE.md",
    "architecture_manifest.json",
    "check_runtime_trace_schema.py",
    "collect_montage_reference_consistency_files.py",
    "eeg_amplitude_map.h5",
    "electrode_lists.txt",
    "error_files.log",
    "found_filter_toolbar_files.txt",
    "import_translation_map_v2.json",
    "KANDA_PROJECT_CANON.md",
    "kanda_prompt_specials_validation_report.json",
    "plugins__montage_editor__montage_head_selector__fix14b.py",
    "remaining_legacy_import_scanner.py",
    "remaining_legacy_imports_report.csv"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $quarantine -Force
        Write-Host "Moved: $item"
    }
}

Then run your app:

cd E:\eeg_kernel_ai_neural_data_analysis
E:\mne_py3.10\python.exe shell\run_kanda_no_coverage.py

If the app opens and your main workflows still work, you can later delete the quarantine folder. If anything breaks, restore the specific file from quarantine.

quarantine in this folder E:\eeg_kernel_ai_neural_data_analysis\workbench

Use this quarantine target instead:

E:\eeg_kernel_ai_neural_data_analysis\workbench\root_cleanup_quarantine_2026_05_29

Run from PowerShell/PyCharm terminal:

$root = "E:\eeg_kernel_ai_neural_data_analysis"
$quarantine = Join-Path $root "workbench\root_cleanup_quarantine_2026_05_29"

New-Item -ItemType Directory -Path $quarantine -Force | Out-Null

$items = @(
    ".coverage",
    ".pykanda_runtime_guard.json",
    "__init__.py",
    "_pyarchitect_collect_errors.py",
    "_pyarchitect_fix_helper_without_main.py",
    "ARCHITECTURE.md",
    "architecture_manifest.json",
    "check_runtime_trace_schema.py",
    "collect_montage_reference_consistency_files.py",
    "eeg_amplitude_map.h5",
    "electrode_lists.txt",
    "error_files.log",
    "found_filter_toolbar_files.txt",
    "import_translation_map_v2.json",
    "KANDA_PROJECT_CANON.md",
    "kanda_prompt_specials_validation_report.json",
    "plugins__montage_editor__montage_head_selector__fix14b.py",
    "remaining_legacy_import_scanner.py",
    "remaining_legacy_imports_report.csv"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $quarantine -Force
        Write-Host "Moved: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

Write-Host ""
Write-Host "Quarantine complete:"
Write-Host $quarantine

Then validate:

cd E:\eeg_kernel_ai_neural_data_analysis
E:\mne_py3.10\python.exe shell\run_kanda_no_coverage.py

If something breaks, restore from:

E:\eeg_kernel_ai_neural_data_analysis\workbench\root_cleanup_quarantine_2026_05_29


README.md
File
remaining_legacy_imports_report.json
File

remaining legacy imports report postfix
Unable to display visualization
just these three  remains?

Yes — if only these three remain in the project root, then root cleanup is almost done.
What to do with each one
File	Keep in root?	Action
README.md	No, not this version	Move to workbench\root_cleanup_quarantine_2026_05_29 or replace later with a clean real README. This one is auto-generated for the old __module_map__ pattern and says it was generated by the __init__.py Generator Tool.
remaining_legacy_imports_report.json	No	Keep for now, but move to workbench\legacy_import_reports\. It is useful because it shows 4 remaining legacy import hits: 3 in main code and 1 in tests.
remaining_legacy_imports_report_postfix.csv	No	Move with the JSON report to workbench\legacy_import_reports\. It is a report artifact, not root source.
Recommended command

$root = "E:\eeg_kernel_ai_neural_data_analysis"
$quarantine = Join-Path $root "workbench\root_cleanup_quarantine_2026_05_29"
$reports = Join-Path $root "workbench\legacy_import_reports"

New-Item -ItemType Directory -Path $quarantine -Force | Out-Null
New-Item -ItemType Directory -Path $reports -Force | Out-Null

$toQuarantine = @(
    "README.md"
)

$toReports = @(
    "remaining_legacy_imports_report.json",
    "remaining_legacy_imports_report_postfix.csv"
)

foreach ($item in $toQuarantine) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $quarantine -Force
        Write-Host "Moved to quarantine: $item"
    }
}

foreach ($item in $toReports) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $reports -Force
        Write-Host "Moved to legacy reports: $item"
    }
}

Then validate:

cd E:\eeg_kernel_ai_neural_data_analysis
E:\mne_py3.10\python.exe shell\run_kanda_no_coverage.py

After this, the project root should be clean. Later, create a new real README.md only if you want a concise human-facing project description.

pykanda.7z
File
0002b_PYARCHITECT_v8_CANON_BATCH_CODE.deepseek_09.05.2026.md
File
0005.1 FULL ANALISE OF CHAT CALL THIS PROMPT AT END OF WORKING DAY 3,3,26.MD
File
0006.ONE_MODULE_COMPLETE_AT_TIME_26.03.2026.md
File
0012 HOW REFACTOR LARGE MODULE 4.4.26.md
File
0029 audito canonical shadow conflicts 09.05.2026.md
File
CANONIC_MAIN_PROMPT_03.03.2026.md
File
CANONIC_MAIN_PROMPT_BATCH_MODE_09.04.2026.md
File
CANONICAL WHAT AI IS.md
File
CANONICAL_DAILY_REFACTOR_APP_FOR_JSON_on_deman 4.4 PROMPT COMAND IS summary js.md
File
CANONICAL_HUMAN_SUMMARY_END_OF_DAY.4.3.2026.md
File
COMPLETE UPDATE OF MODULE TO SAVE TOLKENS 2.0.md
File
COMPLETE UPDATE OF MODULE TO SAVE TOLKENS.md
File
PyKanda CANONICAL READER & MERGE PROMPT v1.0.md
File
PyKANDA Core Canonical Engineering Prompt_26.03.2026.md
File
perfect now we will review the prompts of other project to make prompts adapt to "E:\eeg_kernel_ai_neural_data_analysis  way" but with use specific to "E:\pykanda" project and I will upload project to facilitate your decisions. SAme procedure update name and logic in prompts, make then state of art using smae principles we use here before, classify deprecatede,  update to work like in  \eeg_kernel_ai_neural_data_analysis  way

I’ll audit the old PyKANDA prompts against the project archive, then generate a cleaned prompt stack for E:\pykanda using the same delivery model we stabilized for EEG: direct ZIP delivery, _bundle_temp manifests, no patch runners, prompt-request routing, daily handoff, and special prompts only when needed.

One limitation: the uploaded project archive is .7z, and this sandbox does not have a 7z extractor available. I can still audit and modernize the uploaded prompt files, but for source-code-specific tuning I will note that a future .zip upload would let me inspect the actual project tree.

Done. I created the new PyKANDA prompt stack adapted to the same workflow we stabilized for E:\eeg_kernel_ai_neural_data_analysis, but project-specific for:

E:\pykanda

Download:

Validation report:

Validation passed:

PASS
Files: 14
ZIP structure: only _project_reference/PROMPTS/
UTF-8 without BOM: yes
ASCII-safe: yes
Direct ZIP delivery model: yes
_bundle_temp manifest rule: yes
No patch-runner requirement: yes
Prompt-request behavior: yes

One limitation: the uploaded project archive was .7z, and this sandbox does not have a 7z extractor available. So I could audit and modernize the prompt files, but I could not inspect the full E:\pykanda source tree. For source-specific refinement later, upload a normal .zip.
Files created

_project_reference/PROMPTS/0000 0.00 what send every day PYKANDA NOT PROMPT v1.0.md
_project_reference/PROMPTS/0000 0.1 PYARCHITECT PYKANDA PROMPT STACK LOAD ORDER v1.0.md
_project_reference/PROMPTS/0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.4.md
_project_reference/PROMPTS/0000 1.0 PYARCHITECT PYKANDA STARTUP CANON v6.1.md
_project_reference/PROMPTS/0000 2.1 PYKANDA DAILY STARTUP LOADER v1.0.md
_project_reference/PROMPTS/0000 3.6 PYKANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.0.md
_project_reference/PROMPTS/0000 4.1 PYKANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v1.0.md
_project_reference/PROMPTS/0000 5.5 PYKANDA LARGE MODULE REFACTOR PROTOCOL v1.0.md
_project_reference/PROMPTS/0000 6.0 PYKANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md
_project_reference/PROMPTS/0000 7.1 PYKANDA PROBLEM SET ROADMAP SOLVER v1.0.md
_project_reference/PROMPTS/0000 8.1 PYKANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md
_project_reference/PROMPTS/0000 8.2 PYKANDA SUMMARY JS SPECIAL PROTOCOL v1.0.md
_project_reference/PROMPTS/0000 8.3 PYKANDA CANONICAL READER AND MERGER PROTOCOL v1.1.md
_project_reference/PROMPTS/0000 PROMPT SUBSTITUTION MAP PYKANDA v1.0.md

What changed

I kept the useful PyKANDA-specific canon from the newer core prompt: project_root authority, get_ltm_paths(project_root), Creator-Creature separation, the frozen public front door PrefrontalCortexActionRouter, and the rule that ModelHubWrapper.ask(...), Qwen, and direct connectors are internal service boundaries.

I removed or superseded older logic that conflicts with the EEG-style delivery model, especially old “manifest at ZIP root” and patch-script/one-edit-first workflows. The old generic protocol still required BUNDLE_MANIFEST at ZIP root, which we replaced with _bundle_temp for normal runtime/source/prompt bundles.

I converted the older large-module/refactor logic into the new 0000 5.5 protocol, preserving the useful staged roadmap discipline while aligning it with direct ZIP delivery. The older refactor prompt already had the right “roadmap first, helper decomposition, manifest, validator” idea, but needed modernization.

I preserved the useful summary js behavior as a special prompt instead of daily prompt bloat. The old file defined behavior for the exact command summary js, incremental JSON vectors, confirmation between parts, and resume behavior, so I converted it into 0000 8.2.

I preserved the report/chunk reader logic as 0000 8.3, because the old reader/merger prompt is useful when you upload prior reports or project chunks, but it should be special-use only, not daily startup.
What to send at the start of every PyKANDA chat

For E:\pykanda, send:

1. 0000 0.1 PYARCHITECT PYKANDA PROMPT STACK LOAD ORDER v1.0.md
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.4.md
3. 0000 1.0 PYARCHITECT PYKANDA STARTUP CANON v6.1.md
4. 0000 2.1 PYKANDA DAILY STARTUP LOADER v1.0.md
5. Current active governance files or active governance ZIP
6. Latest 0000 6.0 handoff output from previous session
7. Current task description
8. Relevant source ZIP, logs, validation output, screenshots, or error text

Send only in special occasions

0000 3.6 PYKANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.0.md

Use for high-risk/multi-box work: project_root, get_ltm_paths, LTM, governance, freeze semantics, AI front door, model routing, storage, schema, persistence.

0000 5.5 PYKANDA LARGE MODULE REFACTOR PROTOCOL v1.0.md

Use for files above 500 lines, helper split, source-preserving facade split, or large refactor.

0000 8.1 PYKANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.0.md

Use for public facade warnings, __init__.py, shadow conflicts, duplicate ownership, path authority, layer-boundary cleanup.

0000 8.2 PYKANDA SUMMARY JS SPECIAL PROTOCOL v1.0.md

Use only when you type summary js.

0000 8.3 PYKANDA CANONICAL READER AND MERGER PROTOCOL v1.1.md

Use when uploading old reports, milestone files, daily reports, project chunks, or split JSON exports.

0000 7.1 PYKANDA PROBLEM SET ROADMAP SOLVER v1.0.md

Use when you paste many warnings/errors and want a safe correction roadmap.

0000 6.0 PYKANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.0.md

Use at end of day, break, or unfinished work.

0000 4.1 PYKANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v1.0.md

Use only after validated freeze and explicit approval to update official governance.
Deprecated as daily prompts

Move these to:

_project_reference\PROMPTS\_deprecated\

0002b_PYARCHITECT_v8_CANON_BATCH_CODE.deepseek_09.05.2026.md
0005.1 FULL ANALISE OF CHAT  CALL THIS PROMPT AT END OF WORKING DAY 3,3,26.MD
0006.ONE_MODULE_COMPLETE_AT_TIME_26.03.2026.md
0012 HOW  REFACTOR LARGE MODULE 4.4.26.md
0029 audito canonical shadow conflicts 09.05.2026.md
CANONIC_MAIN_PROMPT_03.03.2026.md
CANONIC_MAIN_PROMPT_BATCH_MODE_09.04.2026.md
CANONICAL WHAT AI IS.md
CANONICAL_DAILY_REFACTOR_APP_FOR_JSON_on_deman 4.4 PROMPT COMAND IS summary js.md
CANONICAL_HUMAN_SUMMARY_END_OF_DAY.4.3.2026.md
COMPLETE UPDATE OF MODULE TO SAVE TOLKENS 2.0.md
COMPLETE UPDATE OF MODULE TO SAVE TOLKENS.md
PyKanda CANONICAL READER & MERGE PROMPT v1.0.md
PyKANDA Core Canonical Engineering Prompt_26.03.2026.md

Install

$root = "E:\pykanda"
$zipPath = "E:\pykanda_prompt_stack_v2026_05_29.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force

Write-Host "Prompt stack installed under:"
Write-Host "$root\_project_reference\PROMPTS"


001_pykanda__complete.chunk.json
File
002_pykanda__complete.chunk.json
File
003_pykanda__complete.chunk.json
File
004_pykanda__complete.chunk.json
File
005_pykanda__complete.chunk.json
File
006_pykanda__complete.chunk.json
File
008_pykanda__complete.chunk.json
File
009_pykanda__complete.chunk.json
File
010_pykanda__complete.chunk.json
File
011_pykanda__complete.chunk.json
File
012_pykanda__complete.chunk.json
File
013_pykanda__complete.chunk.json
File
014_pykanda__complete.chunk.json
File
015_pykanda__complete.chunk.json
File
016_pykanda__complete.chunk.json
File
017_pykanda__complete.chunk.json
File
018_pykanda__complete.chunk.json
File
019_pykanda__complete.chunk.json
File
020_pykanda__complete.chunk.json
File
wait before downloading files, see the actual roject json (zip is too large , I will send in chunks

Understood. Do not use/download the prompt ZIP yet. I will treat that earlier ZIP as a draft only, pending the real E:\pykanda project JSON review.

From the chunks already received, the real project export says:

Project root: E:\pykanda
Total parts: 40
Python files: 702
Walked Python files: 750
Entry files: 134
Parse errors: 48

The export metadata confirms this is pykanda__complete.json, part 1 of 40, with project root E:\pykanda.

I currently see these chunks uploaded:

001-006
008-020

Missing:

007
021-040

After all 40 chunks are uploaded, I will redo the prompt audit using the actual project structure, then produce a corrected final ZIP for:

E:\pykanda\_project_reference\PROMPTS

I will specifically re-check whether the new prompt stack should include stronger rules for the actual PyKANDA architecture, including project_root, get_ltm_paths(project_root), PrefrontalCortexActionRouter, ModelHubWrapper, Qwen connector boundaries, workbench quarantine, Tab 1/Tab 3/Tab 6 boundaries, parse-error handling, and large prompt/refactor workflows.

021_pykanda__complete.chunk.json
File
022_pykanda__complete.chunk.json
File
023_pykanda__complete.chunk.json
File
024_pykanda__complete.chunk.json
File
025_pykanda__complete.chunk.json
File
026_pykanda__complete.chunk.json
File
027_pykanda__complete.chunk.json
File
028_pykanda__complete.chunk.json
File
029_pykanda__complete.chunk.json
File
030_pykanda__complete.chunk.json
File
031_pykanda__complete.chunk.json
File
032_pykanda__complete.chunk.json
File
033_pykanda__complete.chunk.json
File
034_pykanda__complete.chunk.json
File
035_pykanda__complete.chunk.json
File
036_pykanda__complete.chunk.json
File
037_pykanda__complete.chunk.json
File
038_pykanda__complete.chunk.json
File
039_pykanda__complete.chunk.json
File
040_pykanda__complete.chunk.json
File
and remember to enforce box logic

Yes. I’ll enforce box logic as a first-class rule in the PyKANDA prompt stack: identify the active tab/box, patch only that owner box by default, validate the touched box plus global safety gates, and document any necessary cross-box touch explicitly.

The actual export reinforces the need for box logic. PyKANDA has multiple active boxes: root GUI, pykanda_ai, Tab 1, Tab 2, Tab 3 Memory Map/LTM, Tab 6 visualization, synaptic_utils, and workbench; the prompts must prevent fixes in one box from silently changing another.

Done. I rebuilt the PyKANDA prompt stack after reviewing the actual project JSON chunks, and I enforced box logic as a mandatory rule, not just a suggestion.

Use this final ZIP, not the earlier draft:

Validation report:

Validation passed:

PASS
Files: 15
ZIP structure: only _project_reference/PROMPTS/
UTF-8 without BOM: yes
ASCII-safe: yes
Box logic enforced: yes
Direct ZIP delivery model: yes
_bundle_temp manifest rule: yes
No default patch-runner logic: yes

Important note: I received 39 of 40 declared JSON chunks. Chunk 007 is still missing. I still proceeded because the available chunks were enough to identify the main architecture, but the validation report records this limitation.

The project export confirms the PyKANDA root as E:\pykanda, with 702 Python files, 750 walked Python files, 134 entry files, and 48 parse errors. I also used the actual source index evidence showing tab3_memory_map/core/canonical_paths.py exposes get_ltm_paths, which is now frozen in the prompt stack as the canonical LTM path authority. The updated prompts also freeze pykanda_ai/runtime/run_actions.py as the public AI runtime front door, matching the file’s own boundary marker that product and UI callers must use PrefrontalCortexActionRouter with ThalamusActionRequest.
Files in the final ZIP

_project_reference/PROMPTS/0000 0.00 what send every day PYKANDA NOT PROMPT v1.1.md
_project_reference/PROMPTS/0000 0.1 PYARCHITECT PYKANDA PROMPT STACK LOAD ORDER v1.1.md
_project_reference/PROMPTS/0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.5.md
_project_reference/PROMPTS/0000 1.0 PYARCHITECT PYKANDA STARTUP CANON v6.2.md
_project_reference/PROMPTS/0000 2.1 PYKANDA DAILY STARTUP LOADER v1.1.md
_project_reference/PROMPTS/0000 3.6 PYKANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.1.md
_project_reference/PROMPTS/0000 4.1 PYKANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v1.1.md
_project_reference/PROMPTS/0000 5.5 PYKANDA LARGE MODULE REFACTOR PROTOCOL v1.1.md
_project_reference/PROMPTS/0000 6.0 PYKANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md
_project_reference/PROMPTS/0000 7.1 PYKANDA PROBLEM SET ROADMAP SOLVER v1.1.md
_project_reference/PROMPTS/0000 8.1 PYKANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.1.md
_project_reference/PROMPTS/0000 8.2 PYKANDA SUMMARY JS SPECIAL PROTOCOL v1.1.md
_project_reference/PROMPTS/0000 8.3 PYKANDA CANONICAL READER AND MERGER PROTOCOL v1.2.md
_project_reference/PROMPTS/0000 8.4 PYKANDA TAB BOX BOUNDARY PROTOCOL v1.0.md
_project_reference/PROMPTS/0000 PROMPT SUBSTITUTION MAP PYKANDA v1.1.md

Main updates after reviewing the real project JSON

I added mandatory active-box declaration before implementation. The AI must now identify whether the work belongs to root GUI, pykanda_ai/runtime, connectors, Tab 1, Tab 2, Tab 3, Tab 6, synaptic_utils, tools, or workbench.

I added a new special protocol:

0000 8.4 PYKANDA TAB BOX BOUNDARY PROTOCOL v1.0.md

This is for cross-box or multi-tab changes. It forces the AI to declare external box touches, why they are necessary, and how each touched box will be validated.

I strengthened the rule that workbench is staging/audit/prototype by default, not production authority. The prompt stack now warns not to treat workbench/*_UPDATED.py, step21_residue_quarantine, _phase3_tmp_project, demo files, or copied files as canonical production source unless explicitly selected.

I updated the large-module protocol using the real source index. The available JSON shows many files above 500 lines, so the new rule is: do not mass-refactor; handle one owner box at a time, with Task 0 audit and Task 1 roadmap before implementation.
What each prompt substitutes

The full substitution map is inside:

0000 PROMPT SUBSTITUTION MAP PYKANDA v1.1.md

Main replacements:
New prompt	Replaces / supersedes
0000 0.1 ... LOAD ORDER v1.1	Earlier PyKANDA load-order draft v1.0 and old main routers
0000 0.8 ... UNIVERSAL DELIVERY PROTOCOL v1.5	Old delivery prompts using root manifests, default patch runners, or _patch_backups
0000 1.0 ... STARTUP CANON v6.2	Old PyKANDA core canonical engineering prompts
0000 5.5 ... LARGE MODULE REFACTOR v1.1	0012 HOW REFACTOR LARGE MODULE... and one-module-at-a-time legacy prompts
0000 8.1 ... ARCHITECTURE HARDENING v1.1	Old canonical shadow conflict audit prompt
0000 8.2 ... SUMMARY JS v1.1	Old summary js JSON prompt
0000 8.3 ... READER AND MERGER v1.2	Old PyKANDA reader/merge prompt
0000 8.4 ... TAB BOX BOUNDARY v1.0	Scattered old box/one-module guidance
Install

Extract at the project root:

$root = "E:\pykanda"
$zipPath = "E:\pykanda_prompt_stack_v2026_05_29_final.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force

Write-Host "Installed under:"
Write-Host "$root\_project_reference\PROMPTS"

After this, start future PyKANDA chats with the daily stack listed in:

0000 0.00 what send every day PYKANDA NOT PROMPT v1.1.md


007_pykanda__complete.chunk.json
File
pykanda_split_index.json
File
pykanda_split_manifest.json
File

Now that chunk 007 and the split manifest arrived, I’ll clear the previous “missing chunk” limitation and re-check whether chunk 007 adds prompt rules that the final ZIP did not already cover.

Chunk 007 changes the final status in one important way: the reader/merger prompt still says chunk 007 was missing. I’m going to issue a corrected “complete40” ZIP and validation report so the prompt stack no longer carries that obsolete limitation.

Done. Chunk 007 is now incorporated, and the previous “chunk 007 missing” limitation is cleared.

Use this corrected final package:

Validation report:

Validation passed:

PASS
Prompt files: 15
Chunks available: 40
Missing chunks: []
UTF-8 without BOM: yes
ASCII-safe: yes
ZIP layout: _project_reference/PROMPTS/

What changed from the previous final ZIP:

0000 8.3 PYKANDA CANONICAL READER AND MERGER PROTOCOL v1.2.md

was updated to:

0000 8.3 PYKANDA CANONICAL READER AND MERGER PROTOCOL v1.3.md

because the old version still said chunk 007 was missing.

I also updated:

0000 1.0 PYARCHITECT PYKANDA STARTUP CANON v6.3.md
0000 0.1 PYARCHITECT PYKANDA PROMPT STACK LOAD ORDER v1.2.md
0000 0.00 what send every day PYKANDA NOT PROMPT v1.2.md
0000 2.1 PYKANDA DAILY STARTUP LOADER v1.2.md
0000 PROMPT SUBSTITUTION MAP PYKANDA v1.2.md

Chunk 007 adds important registries for feature ownership, migration hotspots, schema risk, lifecycle risk, high-risk edits, active-code status, untested-critical hotspots, and runtime trace evidence. The split index and manifest both confirm the complete export has 40 parts, and the manifest records chunk 007 as part 7 of 40.

Install with:

$root = "E:\pykanda"
$zipPath = "E:\pykanda_prompt_stack_v2026_05_29_complete40.zip"

Expand-Archive -Path $zipPath -DestinationPath $root -Force


0000 PROMPT SUBSTITUTION MAP PYKANDA v1.1.md
File
0000 PROMPT SUBSTITUTION MAP PYKANDA v1.2.md
File
0002b_PYARCHITECT_v8_CANON_BATCH_CODE.deepseek_09.05.2026.md
File
0005.1 FULL ANALISE OF CHAT CALL THIS PROMPT AT END OF WORKING DAY 3,3,26.MD
File
0006.ONE_MODULE_COMPLETE_AT_TIME_26.03.2026.md
File
0012 HOW REFACTOR LARGE MODULE 4.4.26.md
File
0029 audito canonical shadow conflicts 09.05.2026.md
File
CANONIC_MAIN_PROMPT_03.03.2026.md
File
CANONIC_MAIN_PROMPT_BATCH_MODE_09.04.2026.md
File
CANONICAL WHAT AI IS.md
File
CANONICAL_DAILY_REFACTOR_APP_FOR_JSON_on_deman 4.4 PROMPT COMAND IS summary js.md
File
CANONICAL_HUMAN_SUMMARY_END_OF_DAY.4.3.2026.md
File
COMPLETE UPDATE OF MODULE TO SAVE TOLKENS 2.0.md
File
COMPLETE UPDATE OF MODULE TO SAVE TOLKENS.md
File
PyKanda CANONICAL READER & MERGE PROMPT v1.0.md
File
pykanda_prompt_stack_validation_report_complete40.json
File
now, which of these prompts is usefull and you will return am updated version and which is deprecated to delete? 

I’ll classify each uploaded prompt against the final PyKANDA complete40 stack: active keep, useful-but-superseded, and delete/archive. The key rule is: keep only the new complete40 prompt stack active; old prompts can be archived if their logic was absorbed.

Yes. Use this rule:

Active folder = only the complete40 prompt stack
Old uploaded prompts = deprecated after their logic was absorbed

Your active updated package is already the corrected one:

The validation report confirms: 40 chunks available, no missing chunks, complete JSON export verified, 15 prompt files, UTF-8 without BOM, ASCII-safe, and no errors.
Keep active

Keep these. These are useful and already updated in the complete40 ZIP.
Prompt	Status
0000 0.00 what send every day PYKANDA NOT PROMPT v1.2.md	Active user checklist
0000 0.1 PYARCHITECT PYKANDA PROMPT STACK LOAD ORDER v1.2.md	Active daily first prompt
0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.5.md	Active delivery protocol
0000 1.0 PYARCHITECT PYKANDA STARTUP CANON v6.3.md	Active PyKANDA canon
0000 2.1 PYKANDA DAILY STARTUP LOADER v1.2.md	Active daily loader
0000 3.6 PYKANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.1.md	Special/high-risk prompt
0000 4.1 PYKANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v1.1.md	Special official governance update
0000 5.5 PYKANDA LARGE MODULE REFACTOR PROTOCOL v1.1.md	Special large-module/refactor prompt
0000 6.0 PYKANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md	Special handoff prompt
0000 7.1 PYKANDA PROBLEM SET ROADMAP SOLVER v1.1.md	Special many-errors roadmap prompt
0000 8.1 PYKANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.1.md	Special hardening/security prompt
0000 8.2 PYKANDA SUMMARY JS SPECIAL PROTOCOL v1.1.md	Special summary js prompt
0000 8.3 PYKANDA CANONICAL READER AND MERGER PROTOCOL v1.3.md	Special reader/merger prompt
0000 8.4 PYKANDA TAB BOX BOUNDARY PROTOCOL v1.0.md	Special box-logic prompt
0000 PROMPT SUBSTITUTION MAP PYKANDA v1.2.md	Active substitution map

The active substitution map v1.2 explicitly supersedes the older v1.1 final package because v1.1 still marked chunk 007 as missing.
Delete from active prompts folder

These should not remain active in _project_reference\PROMPTS. Move to _deprecated or delete after confirming the complete40 ZIP is installed.
Uploaded prompt	Decision	Replaced by
0000 PROMPT SUBSTITUTION MAP PYKANDA v1.1.md	Delete/archive	0000 PROMPT SUBSTITUTION MAP PYKANDA v1.2.md
0002b_PYARCHITECT_v8_CANON_BATCH_CODE.deepseek_09.05.2026.md	Deprecated	0000 0.8, 0000 1.0, 0000 7.1, 0000 8.1
0005.1 FULL ANALISE OF CHAT CALL THIS PROMPT AT END OF WORKING DAY 3,3,26.MD	Deprecated	0000 4.1 for official governance, 0000 6.0 for handoff
0006.ONE_MODULE_COMPLETE_AT_TIME_26.03.2026.md	Deprecated	0000 5.5, 0000 8.4
0012 HOW REFACTOR LARGE MODULE 4.4.26.md	Deprecated, logic absorbed	0000 5.5 PYKANDA LARGE MODULE REFACTOR PROTOCOL v1.1.md
0029 audito canonical shadow conflicts 09.05.2026.md	Deprecated, logic absorbed	0000 8.1 PYKANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.1.md
CANONIC_MAIN_PROMPT_03.03.2026.md	Deprecated	0000 1.0 PYKANDA STARTUP CANON v6.3.md
CANONIC_MAIN_PROMPT_BATCH_MODE_09.04.2026.md	Deprecated	0000 0.1, 0000 1.0, 0000 2.1, 0000 7.1
CANONICAL WHAT AI IS.md	Deprecated	0000 1.0, 0000 3.6
CANONICAL_DAILY_REFACTOR_APP_FOR_JSON_on_deman 4.4 PROMPT COMAND IS summary js.md	Deprecated, logic absorbed	0000 8.2 PYKANDA SUMMARY JS SPECIAL PROTOCOL v1.1.md
CANONICAL_HUMAN_SUMMARY_END_OF_DAY.4.3.2026.md	Deprecated	0000 6.0 and 0000 4.1
COMPLETE UPDATE OF MODULE TO SAVE TOLKENS 2.0.md	Deprecated	0000 5.5, 0000 7.1, 0000 8.4
COMPLETE UPDATE OF MODULE TO SAVE TOLKENS.md	Deprecated	0000 5.5, 0000 7.1, 0000 8.4
PyKanda CANONICAL READER & MERGE PROMPT v1.0.md	Deprecated, logic absorbed	0000 8.3 PYKANDA CANONICAL READER AND MERGER PROTOCOL v1.3.md
Why these are deprecated

The old batch/update prompt still uses older delivery ideas like ZIP-root BUNDLE_MANIFEST, whereas the new PyKANDA stack uses the EEG-style _bundle_temp manifest rule and direct project-relative ZIP delivery.

The old one-module prompt is useful historically, but it enforces “one module per reply” and full-module output, which conflicts with the newer workflow: audit, box ownership, sandbox patch, validate, package ZIP, and only then freeze.

The old large-module refactor prompt had valuable ideas: roadmap first, helper folder, manifest, validator, and approval before implementation. That logic was preserved and modernized into 0000 5.5.

The old summary js prompt remains useful only as a special command. Its behavior is now kept as 0000 8.2, not as a daily prompt.

The old reader/merger prompt is also useful, but it has been replaced by the updated 0000 8.3 ... v1.3, aligned with complete40 and box logic.
Recommended cleanup command

$root = "E:\pykanda"
$prompts = Join-Path $root "_project_reference\PROMPTS"
$deprecated = Join-Path $prompts "_deprecated_2026_05_29"

New-Item -ItemType Directory -Path $deprecated -Force | Out-Null

$oldPrompts = @(
    "0000 PROMPT SUBSTITUTION MAP PYKANDA v1.1.md",
    "0002b_PYARCHITECT_v8_CANON_BATCH_CODE.deepseek_09.05.2026.md",
    "0005.1 FULL ANALISE OF CHAT  CALL THIS PROMPT AT END OF WORKING DAY 3,3,26.MD",
    "0006.ONE_MODULE_COMPLETE_AT_TIME_26.03.2026.md",
    "0012 HOW  REFACTOR LARGE MODULE 4.4.26.md",
    "0029 audito canonical shadow conflicts 09.05.2026.md",
    "CANONIC_MAIN_PROMPT_03.03.2026.md",
    "CANONIC_MAIN_PROMPT_BATCH_MODE_09.04.2026.md",
    "CANONICAL WHAT AI IS.md",
    "CANONICAL_DAILY_REFACTOR_APP_FOR_JSON_on_deman 4.4 PROMPT COMAND IS summary js.md",
    "CANONICAL_HUMAN_SUMMARY_END_OF_DAY.4.3.2026.md",
    "COMPLETE UPDATE OF MODULE TO SAVE TOLKENS 2.0.md",
    "COMPLETE UPDATE OF MODULE TO SAVE TOLKENS.md",
    "PyKanda CANONICAL READER & MERGE PROMPT v1.0.md"
)

foreach ($file in $oldPrompts) {
    $src = Join-Path $prompts $file
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $deprecated -Force
        Write-Host "Archived: $file"
    } else {
        Write-Host "Not found: $file"
    }
}

After cleanup, the active prompt folder should contain only the 15 complete40 files.

now which prompt call every time we start chat and which are called in special situations and , didi you update main prompt to advise user when a special prompt is needed?

Yes. The main PyKANDA prompt was updated to tell the AI to ask you for the right special prompt when needed. The complete40 validation confirms the final prompt stack has 15 files, all 40 JSON chunks available, no missing chunks, UTF-8 without BOM, ASCII-safe, and no validation errors.
Send at every start of PyKANDA chat

For E:\pykanda, send in this order:

1. 0000 0.1 PYARCHITECT PYKANDA PROMPT STACK LOAD ORDER v1.2.md
2. 0000 0.8 PYARCHITECT UNIVERSAL DELIVERY PROTOCOL v1.5.md
3. 0000 1.0 PYARCHITECT PYKANDA STARTUP CANON v6.3.md
4. 0000 2.1 PYKANDA DAILY STARTUP LOADER v1.2.md
5. Current active governance files or governance ZIP
6. Latest 0000 6.0 handoff output from the previous session
7. Current task description
8. Relevant source ZIP, logs, validation output, screenshots, or error text

The file:

0000 0.00 what send every day PYKANDA NOT PROMPT v1.2.md

is only your personal checklist. Keep it, but you do not need to paste it as a prompt.
Send only in special situations
Situation	Send this prompt
High-risk architecture, runtime, storage, schema, LTM, AI routing, governance, or multi-box work	0000 3.6 PYKANDA PROFESSIONAL ENGINEERING GOVERNANCE LAYER v1.1.md
Official governance/canon update after validated freeze	0000 4.1 PYKANDA END-OF-CHAT ACTIVE GOVERNANCE UPDATE v1.1.md
Large file above 500 lines, helper split, source-preserving facade, or large refactor	0000 5.5 PYKANDA LARGE MODULE REFACTOR PROTOCOL v1.1.md
End of day, break, unfinished work, or next-chat continuation	0000 6.0 PYKANDA CURRENT ACTIVE WORKFLOW HANDOFF TEMPLATE v1.1.md
Many warnings/errors/problems that need prioritization	0000 7.1 PYKANDA PROBLEM SET ROADMAP SOLVER v1.1.md
Architecture hardening, public facades, shadow conflicts, path authority, state mutation, boundary cleanup	0000 8.1 PYKANDA ARCHITECTURE HARDENING TRIAGE PROTOCOL v1.1.md
You type the exact command summary js	0000 8.2 PYKANDA SUMMARY JS SPECIAL PROTOCOL v1.1.md
Uploading old reports, milestone files, split JSON chunks, or needing project-state merge	0000 8.3 PYKANDA CANONICAL READER AND MERGER PROTOCOL v1.3.md
Work touches tabs/boxes or risks cross-box interference	0000 8.4 PYKANDA TAB BOX BOUNDARY PROTOCOL v1.0.md

These active daily and special prompts are listed in the final substitution map v1.2.
Did the main prompt advise the user when a special prompt is needed?

Yes. The updated main prompt stack includes prompt-request behavior. The AI should say something like:

For this task, I need these additional prompt files before implementation:
- 0000 8.4 PYKANDA TAB BOX BOUNDARY PROTOCOL v1.0.md
Please upload it or confirm it is already loaded.

Examples:

Large module -> ask for 0000 5.5
Architecture hardening -> ask for 0000 8.1
Cross-tab or cross-box task -> ask for 0000 8.4
summary js -> use 0000 8.2
End-of-day handoff -> use 0000 6.0
Official canon update -> ask for 0000 4.1

Active folder rule

After installing the complete40 ZIP, the active prompt folder should contain only the 15 complete40 prompt files. Old prompts should go to _deprecated_2026_05_29 or be deleted after backup.

01_pkanda_10_3_26.json
File
0002 CANONICAL BRAIN MAPPING STRUCTORE.4.3.26.md
File
02_pkanda_10_3_26.json
File
003_build_daily_refactor_report_engine_28_fev_26.md
File
03_pkanda_10_3_26.json
File
004_build_daily_refactor_report_engine_28_fev_26.md
File
04_pkanda_10_3_26.json
File
05_pkanda_10_3_26.json
File
006CORTEX_IMPLEMENTATION_v1_01.03.2026.md
File
06_pkanda_10_3_26.json
File
007AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL_0.md
File
07_pkanda_10_3_26.json
File
008AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL.md
File
08_pkanda_10_3_26.json
File
09_pkanda_10_3_26.json
File
010AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL_ 3_first_steps_01.md
File
10_pkanda_10_3_26.json
File
011HOW_WARNING_SYSTEM_WORKS_01_03_2026.md
File
012 BIGGEST AI IMPROVEMENT 01.03.2026.md
File
lets clean project , can we delete

Yes — based on the uploaded files, these should not stay in the active PyKANDA root.

I would not permanently delete immediately. Move them to a cleanup archive first, then delete later if the project still works.
Decision
Safe to archive/delete from active root

These are old generated maps/reports, not active source:

01_pkanda_10_3_26.json
02_pkanda_10_3_26.json
03_pkanda_10_3_26.json
04_pkanda_10_3_26.json
05_pkanda_10_3_26.json
06_pkanda_10_3_26.json
07_pkanda_10_3_26.json
08_pkanda_10_3_26.json
09_pkanda_10_3_26.json
10_pkanda_10_3_26.json

Reason: the uploaded JSON maps are old structural exports from 2026-03-10 and include .venv\Lib\site-packages content, meaning they captured external libraries rather than only PyKANDA source. That is not clean project truth.
Archive as historical docs, not active prompts

Move these to a historical folder:

0002 CANONICAL BRAIN MAPPING STRUCTORE.4.3.26.md
003_build_daily_refactor_report_engine_28_fev_26.md
004_build_daily_refactor_report_engine_28_fev_26.md
006CORTEX_IMPLEMENTATION_v1_01.03.2026.md
007AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL_0.md
008AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL.md
010AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL_ 3_first_steps_01.md
011HOW_WARNING_SYSTEM_WORKS_01_03_2026.md
012 BIGGEST AI IMPROVEMENT 01.03.2026.md

The AI migration docs are useful historically because they define the correct direction: pykanda_ai becomes the shared Creator-domain AI layer, Tab3 stops owning base AI runtime, UI stays UI, canonical path authority stays centralized, and compatibility shims are preserved.

But they should not remain loose in root because the active prompt system has already replaced old routers and prompt fragments with the complete40 stack. The current substitution map says v1.2 is the active map and explicitly supersedes the earlier v1.1 final package.
Best action

Move all uploaded cleanup candidates to:

E:\pykanda\workbench\root_cleanup_archive_2026_05_29

Use this:

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "01_pkanda_10_3_26.json",
    "02_pkanda_10_3_26.json",
    "03_pkanda_10_3_26.json",
    "04_pkanda_10_3_26.json",
    "05_pkanda_10_3_26.json",
    "06_pkanda_10_3_26.json",
    "07_pkanda_10_3_26.json",
    "08_pkanda_10_3_26.json",
    "09_pkanda_10_3_26.json",
    "10_pkanda_10_3_26.json",
    "0002 CANONICAL BRAIN MAPPING STRUCTORE.4.3.26.md",
    "003_build_daily_refactor_report_engine_28_fev_26.md",
    "004_build_daily_refactor_report_engine_28_fev_26.md",
    "006CORTEX_IMPLEMENTATION_v1_01.03.2026.md",
    "007AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL_0.md",
    "008AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL.md",
    "010AI_MIGRATION_TO_PYKANDA_AI_TUTORIAL_ 3_first_steps_01.md",
    "011HOW_WARNING_SYSTEM_WORKS_01_03_2026.md",
    "012 BIGGEST AI IMPROVEMENT 01.03.2026.md"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

Write-Host ""
Write-Host "Archive complete:"
Write-Host $archive

After moving, validate

cd E:\pykanda
E:\envs\pykanda\python.exe -m py_compile pykanda_gui.py

Then launch your normal PyKANDA entry point.
Final answer

Yes: these can be removed from the active root.
Best practice: archive now, delete later after PyKANDA opens normally.

audit_gui_helpers_report.json
File
audit_gui_helpers_report.txt
Document
CAN i DELEte those?

Yes — you can delete/archive these two report files:

audit_gui_helpers_report.json
audit_gui_helpers_report.txt

They are audit outputs only. They do not appear to be source files or active runtime modules. The JSON says files_fixed: 0, meaning the report did not apply changes. The TXT is just a classification summary of GUI helper files into SAFE, MEDIUM, and SENSITIVE.

Important: delete only the report files, not the actual files listed inside them, such as:

pykanda_gui_helpers\...

Those are real project helper modules.

Safer option: move them to workbench first:

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "audit_gui_helpers_report.json",
    "audit_gui_helpers_report.txt"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

After a few days, you can delete them from workbench if nothing is missing.

cna I delete this empty folder  E:\pykanda\.qodo?

Yes — if this folder is truly empty:

E:\pykanda\.qodo

you can delete it safely.

It is likely a tool/config folder from Qodo/Codium-style AI code tooling. If it is empty, it is not carrying project code, prompts, reports, or runtime state.

Use:

Remove-Item -Path "E:\pykanda\.qodo" -Force

Or manually delete it in File Explorer.

Only keep it if you actively use Qodo in that project and it recreates settings there.

demo_module.py.json
File
demo_module.py.json
File
__init__.py
Python
demo_module.py
Python
demo_module.cpython-312.pyc
File
can I delete "E:\pykanda\_phase3_tmp_project" and its content?

Yes — you can delete:

E:\pykanda\_phase3_tmp_project

The uploaded contents show it is a temporary/demo project, not active PyKANDA source:

demo_module.py
demo_module.py.json
__init__.py
demo_module.cpython-312.pyc

demo_module.py only contains a simple add() function and Calc.mul() class method.
The __init__.py is just a minimal demo facade exporting Calc and add.
The JSON files are generated semantic/vector artifacts for demo_module.py, not production code.

Safer option first:

$root = "E:\pykanda"
$src = Join-Path $root "_phase3_tmp_project"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29\_phase3_tmp_project"

New-Item -ItemType Directory -Path (Split-Path $archive) -Force | Out-Null

if (Test-Path $src) {
    Move-Item -Path $src -Destination $archive -Force
    Write-Host "Archived _phase3_tmp_project"
}

Then, after PyKANDA opens normally, delete the archived copy.

Direct delete, if you are sure:

Remove-Item -Path "E:\pykanda\_phase3_tmp_project" -Recurse -Force


model_settings.json
File
ca I delete

I would not delete it immediately if this file is in the active PyKANDA project root:

model_settings.json

It contains the active model setting:

active_model: local-qwen2.5

So it may be used by PyKANDA to remember which local AI model is selected.

Best action: move it to workbench first, then launch PyKANDA. If PyKANDA recreates it automatically or works normally, you can delete the archived copy later.

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

Move-Item -Path "E:\pykanda\model_settings.json" -Destination $archive -Force

Then test PyKANDA. If the model selection resets or AI connection changes, restore it.

current_state.json.back1
File
current_state.json.back2
File
state_history.json.back1
File
state_history.json.back2
File
dependency_graph.json
File
project_snapshot.json
File
stability_analysis.json
File
symbol_churn.json
File
symbol_index.json
File
symbol_index.previous.json
File
can I delete this ?

Yes — you can remove these from the active PyKANDA root, but I recommend archiving first, not permanent delete immediately.

These are generated state/report artifacts, not active source code:

current_state.json.back1
current_state.json.back2
state_history.json.back1
state_history.json.back2
dependency_graph.json
project_snapshot.json
stability_analysis.json
symbol_churn.json
symbol_index.json
symbol_index.previous.json

Why: dependency_graph.json is a generated dependency report for E:\pykanda\dev_tools, with no cycles detected. project_snapshot.json is also a generated snapshot for E:\pykanda\dev_tools, timestamped 2026-03-06, with 12 Python files and no parse errors. stability_analysis.json reports low combined risk, and symbol_churn.json shows zero added/removed symbols, so these are analysis outputs, not runtime-critical files. The symbol index files are generated symbol maps with 66 symbols.

Use archive first:

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29\old_state_reports"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "current_state.json.back1",
    "current_state.json.back2",
    "state_history.json.back1",
    "state_history.json.back2",
    "dependency_graph.json",
    "project_snapshot.json",
    "stability_analysis.json",
    "symbol_churn.json",
    "symbol_index.json",
    "symbol_index.previous.json"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

After PyKANDA opens normally, you can delete the archived folder later.

Do not delete the actual dev_tools folder just because these reports mention it. These files are reports; dev_tools may contain real tools.

prefrontal_reflection.json
File
cna I delete?

Yes — you can delete it:

prefrontal_reflection.json

The uploaded file content is just an empty JSON array:

[]

So it does not contain active project state, reflections, logs, or configuration data.

Delete directly:

Remove-Item -Path "E:\pykanda\prefrontal_reflection.json" -Force

Or archive first:

Move-Item -Path "E:\pykanda\prefrontal_reflection.json" -Destination "E:\pykanda\workbench\root_cleanup_archive_2026_05_29" -Force


ai_context_history.json
File
cognitive_reflections.json
File
cognitive_signals.json
File
governance_state.json
File
project_brain_log.json
File
project_registry.json
File
pykanda_tree.json
File
ca I delete this?

Yes — you can remove these from the active PyKANDA root, but I recommend archive first, then delete later after PyKANDA opens normally.

These are state/log/snapshot artifacts, not active source modules:

ai_context_history.json
cognitive_reflections.json
cognitive_signals.json
governance_state.json
project_brain_log.json
project_registry.json
pykanda_tree.json

Why: ai_context_history.json is just a short cognitive-reflection history log. cognitive_reflections.json and cognitive_signals.json are old reflection/signal records from March 2026. governance_state.json only stores mode: 0 and cooldown_counter: 0. project_brain_log.json is a run log with old temp/test paths and some PyKANDA/EEG workbench entries. project_registry.json points to old E:\EEG_KANDA, not the current E:\pykanda project. pykanda_tree.json is a generated tree snapshot from 2026-05-03, useful as archive only.

Use this:

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29\old_runtime_state"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "ai_context_history.json",
    "cognitive_reflections.json",
    "cognitive_signals.json",
    "governance_state.json",
    "project_brain_log.json",
    "project_registry.json",
    "pykanda_tree.json"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

After PyKANDA launches normally, you can delete the archived copies.

creator_paths.py
Python
file_dialog_context.py
Python
global_signal_bus.py
Python
project_state.py
Python
safe_paths_patch.py
Python
delete?

No — do not delete these from active PyKANDA.

These are real shared source modules, not cleanup artifacts:

shared\creator_paths.py
shared\file_dialog_context.py
shared\global_signal_bus.py
shared\project_state.py
shared\safe_paths_patch.py

Why:

    creator_paths.py defines CREATOR_BASE, CREATOR_STATE_DIR, and PROJECT_STATE_FILE, which are core runtime path/state locations.

    file_dialog_context.py imports PROJECT_STATE_FILE from shared.project_state and persists last_dialog_dir. Deleting it can break file dialog memory.

    global_signal_bus.py defines the central global_signals, set_project_root(), and get_project_root(). This is active box-boundary infrastructure.

    project_state.py saves and loads the active project root from PROJECT_STATE_FILE.

    safe_paths_patch.py patches Path.cwd() behavior. It may need review later, but do not delete it blindly.

My decision:

Do not delete.
Keep in active project.

If you suspect one is obsolete, first run an import-usage search. But for root cleanup, these are not trash.

f9d86028c6e0d64e225186f96acb69338b2c59764df79162107f5c4bb34d1310.json
File
delete?

Yes — you can delete this file:

f9d86028c6e0d64e225186f96acb69338b2c59764df79162107f5c4bb34d1310.json

It only contains:

{
  "b": 2
}

So it looks like a tiny test/cache artifact, not an active PyKANDA source or configuration file.

Delete directly:

Remove-Item -Path "E:\pykanda\f9d86028c6e0d64e225186f96acb69338b2c59764df79162107f5c4bb34d1310.json" -Force


gui_runtime.log
File
can I delete?

Yes, you can delete/archive:

gui_runtime.log

It is a runtime log, not source code. PyKANDA should recreate it when it runs again.

However, I would archive it first because it contains useful recent startup diagnostics from 2026-05-29, including:

HyppocampusWatcher.__init__() got an unexpected keyword argument 'results_dir'
[PrefrontalDecisionTab] Failed to initialize paths: 'reflection_dir'
Plugin discovery incomplete: No module named 'openai'
Application started successfully

So it is safe to remove from active root/log location, but useful for debugging.

Use:

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29\logs"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

Move-Item -Path "E:\pykanda\creator_logs\gui_runtime.log" -Destination $archive -Force

If your file is actually in root, use:

Move-Item -Path "E:\pykanda\gui_runtime.log" -Destination $archive -Force

After PyKANDA launches normally, you can delete the archived copy later.

ai_model_in_use.json
File
project_in_use.json
File
cna I delelte ?

I would not delete them permanently right now.

These two look like active PyKANDA state/config files:

ai_model_in_use.json
project_in_use.json

ai_model_in_use.json stores the selected model:

qwen2.5-coder:7b

So deleting it may reset the selected AI model.

project_in_use.json stores the active project root, last memorize mode/path, filter tags, live refresh setting, and last dialog directory. It currently points to:

E:\eeg_kernel_ai_neural_data_analysis

and keeps live_refresh: true plus the last dialog path.
Best action

Archive first, then launch PyKANDA. If PyKANDA recreates them normally, you can delete the archived copies later.

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29\creator_state"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "creator_state\ai_model_in_use.json",
    "creator_state\project_in_use.json"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

My decision:

Do not delete directly.
Archive first.
Restore if model selection or project selection breaks.


PHASE9_PATCH_010_move_gui_specific_incremental_update_adapter_out_of_runtime.md
File
PHASE9_PATCH_020_convert_compatibility_surface_to_strict_facade_after_extracting_logic.md
File
PHASE9_PATCH_030_separate_memory_event_bus_implementation_from_compatibility_facade_role.md
File
PHASE9_PATCH_040_tighten_project_root_and_results_dir_ownership.md
File
PHASE9_PATCH_050_convert_highest_risk_qt_lifecycle_warnings_into_explicit_cleanup.md
File
PHASE9_PATCH_100_classify_and_optionally_convert_duplicate_symbol_send_chat.md
File
PHASE9_PATCH_110_classify_and_optionally_convert_duplicate_symbol_send_chat.md
File
PHASE9_PATCH_120_classify_and_optionally_convert_duplicate_symbol_get_available_models.md
File
PHASE9_PATCH_130_classify_and_optionally_convert_duplicate_symbol_get_available_models.md
File
PHASE9_PATCH_140_classify_and_optionally_convert_duplicate_symbol_activeapiwatcher.md
File
PHASE9_PATCH_150_classify_and_optionally_convert_duplicate_symbol_current_api_key.md
File
PHASE9_PATCH_160_classify_and_optionally_convert_duplicate_symbol_current_temperature.md
File
PHASE9_PATCH_170_classify_and_optionally_convert_duplicate_symbol_current_timeout.md
File
PHASE9_PATCH_180_classify_and_optionally_convert_duplicate_symbol_get_ai_base.md
File
PHASE9_PATCH_190_classify_and_optionally_convert_duplicate_symbol_get_ai_url.md
File
can I delete?

Yes — you can remove them from the active PyKANDA root, but I would not permanently delete all of them immediately.

These are Phase 9 patch/backlog templates, not source code. They describe future cleanup tasks such as runtime-router cleanup, compatibility facade conversion, memory event bus facade cleanup, project-root ownership tightening, and Qt lifecycle cleanup.
Best decision

Move them to:

E:\pykanda\workbench\phase9_patch_templates_archive_2026_05_29

Then later delete only after you are sure Phase 9 is obsolete or already absorbed into the new PyKANDA prompt stack.
Important duplicates

These are duplicates and can be safely reduced after archiving:

PHASE9_PATCH_100...send_chat.md
PHASE9_PATCH_110...send_chat.md

Both target the same send_chat duplicate-symbol cleanup.

PHASE9_PATCH_120...get_available_models.md
PHASE9_PATCH_130...get_available_models.md

Both target the same get_available_models cleanup.
Command to archive

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\phase9_patch_templates_archive_2026_05_29"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "PHASE9_PATCH_010_move_gui_specific_incremental_update_adapter_out_of_runtime.md",
    "PHASE9_PATCH_020_convert_compatibility_surface_to_strict_facade_after_extracting_logic.md",
    "PHASE9_PATCH_030_separate_memory_event_bus_implementation_from_compatibility_facade_role.md",
    "PHASE9_PATCH_040_tighten_project_root_and_results_dir_ownership.md",
    "PHASE9_PATCH_050_convert_highest_risk_qt_lifecycle_warnings_into_explicit_cleanup.md",
    "PHASE9_PATCH_100_classify_and_optionally_convert_duplicate_symbol_send_chat.md",
    "PHASE9_PATCH_110_classify_and_optionally_convert_duplicate_symbol_send_chat.md",
    "PHASE9_PATCH_120_classify_and_optionally_convert_duplicate_symbol_get_available_models.md",
    "PHASE9_PATCH_130_classify_and_optionally_convert_duplicate_symbol_get_available_models.md",
    "PHASE9_PATCH_140_classify_and_optionally_convert_duplicate_symbol_activeapiwatcher.md",
    "PHASE9_PATCH_150_classify_and_optionally_convert_duplicate_symbol_current_api_key.md",
    "PHASE9_PATCH_160_classify_and_optionally_convert_duplicate_symbol_current_temperature.md",
    "PHASE9_PATCH_170_classify_and_optionally_convert_duplicate_symbol_current_timeout.md",
    "PHASE9_PATCH_180_classify_and_optionally_convert_duplicate_symbol_get_ai_base.md",
    "PHASE9_PATCH_190_classify_and_optionally_convert_duplicate_symbol_get_ai_url.md"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

Final answer

Yes, remove them from root.
Best action: archive first, delete later. They are useful as Phase 9 backlog notes, but they should not stay loose in the active project root.

main.js
JavaScript
a.htm
File
ansi-1f6vhsjh.css
File
conversation-small-lq38g8zw.css
File
FormattedText-cp0srdqe.css
File
js
JavaScript
product-variants-gcznzbx5.css
File
root-hstv7y8e.css
File
table-components-iztk4amh.css
File
can I delete?

Yes — these can be removed from the active PyKANDA root if they are loose files in root.

They look like downloaded web-page/cache assets, not PyKANDA source:

main.js
js
a.htm
ansi-1f6vhsjh.css
conversation-small-lq38g8zw.css
FormattedText-cp0srdqe.css
product-variants-gcznzbx5.css
root-hstv7y8e.css
table-components-iztk4amh.css

a.htm is just a small HTML page loading Cloudflare challenge/script assets, not project code. The CSS files are generic UI/web styling assets, including ANSI colors, ChatGPT/Tailwind-style UI CSS, formatted text CSS, product variants CSS, and table CSS.

For the images/icons:

53E2BF11-45A8-452D-9914-9F965AE361E2.jpeg
6073fcf8-e1c7-4b38-8dce-465b566f9b77.png
unnamed.png
WhatsApp Image 2025-04-04 at 1.15.13 PM.jpeg

They look like loose icons/images. You can delete them unless one is intentionally used as a PyKANDA logo/app icon. Safer: archive first.

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29\web_export_assets"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "main.js",
    "js",
    "a.htm",
    "ansi-1f6vhsjh.css",
    "conversation-small-lq38g8zw.css",
    "FormattedText-cp0srdqe.css",
    "product-variants-gcznzbx5.css",
    "root-hstv7y8e.css",
    "table-components-iztk4amh.css",
    "53E2BF11-45A8-452D-9914-9F965AE361E2.jpeg",
    "6073fcf8-e1c7-4b38-8dce-465b566f9b77.png",
    "unnamed.png",
    "WhatsApp Image 2025-04-04 at 1.15.13 PM.jpeg"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

Final decision: yes, remove from root; archive first, delete later after PyKANDA opens normally.

.docstring_cache.json
File
.docstring_run_report.jsonl
File
.gitignore
File
.pykanda_runtime_guard.json
File
__init__.py
Python
ARCHITECTURE.md
File
architecture_manifest.json
File
BUNDLE_MANIFEST_PYKANDA_PHASE0C_BASELINE.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE0D_PUBLIC_SYMBOLS.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE1_CANONICAL_OWNER_FREEZE.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE2_COMPATIBILITY_FACADE_CLEANUP.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE3_STATE_OWNERSHIP.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE4_GUI_LIFECYCLE.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE5_RUNTIME_ACTION_ROUTER_CLEANUP.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE6_VALIDATION_EXPANSION.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE7_ONE_COMMAND_VALIDATION.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE7_ONE_COMMAND_VALIDATION.txt - Shortcut.lnk
File
BUNDLE_MANIFEST_PYKANDA_PHASE8_RESIDUE_WORKBENCH_QUARANTINE.txt
Document
BUNDLE_MANIFEST_PYKANDA_PHASE9_REAL_REFACTOR_CONTROL.txt
Document
conftest.py
Python
can I delete from root?


,0

Yes, but not all. Here is the decision.
Delete/archive from root

These can be removed from the active root. I recommend archiving first:

.docstring_cache.json
.docstring_run_report.jsonl
.pykanda_runtime_guard.json
ARCHITECTURE.md
architecture_manifest.json
BUNDLE_MANIFEST_PYKANDA_PHASE0C_BASELINE.txt
BUNDLE_MANIFEST_PYKANDA_PHASE0D_PUBLIC_SYMBOLS.txt
BUNDLE_MANIFEST_PYKANDA_PHASE1_CANONICAL_OWNER_FREEZE.txt
BUNDLE_MANIFEST_PYKANDA_PHASE2_COMPATIBILITY_FACADE_CLEANUP.txt
BUNDLE_MANIFEST_PYKANDA_PHASE3_STATE_OWNERSHIP.txt
BUNDLE_MANIFEST_PYKANDA_PHASE4_GUI_LIFECYCLE.txt
BUNDLE_MANIFEST_PYKANDA_PHASE5_RUNTIME_ACTION_ROUTER_CLEANUP.txt
BUNDLE_MANIFEST_PYKANDA_PHASE6_VALIDATION_EXPANSION.txt
BUNDLE_MANIFEST_PYKANDA_PHASE7_ONE_COMMAND_VALIDATION.txt
BUNDLE_MANIFEST_PYKANDA_PHASE7_ONE_COMMAND_VALIDATION.txt - Shortcut.lnk
BUNDLE_MANIFEST_PYKANDA_PHASE8_RESIDUE_WORKBENCH_QUARANTINE.txt
BUNDLE_MANIFEST_PYKANDA_PHASE9_REAL_REFACTOR_CONTROL.txt

Reason: .docstring_cache.json is empty ({}), so it is only cache. .pykanda_runtime_guard.json only stores guard/cooldown state with failures: 0, so it can be archived and recreated if needed. ARCHITECTURE.md is explicitly a derived view generated from architecture_manifest.json, not primary source. The manifest itself is a generated architecture snapshot from 2026-05-02, so archive rather than keep loose in root.

The BUNDLE_MANIFEST... files are old phase bundle descriptions/install manifests, not runtime source. They document validation/control bundles from Phase 0C through Phase 9.
Do not delete

Keep these in root:

.gitignore
__init__.py
conftest.py

__init__.py declares the project metadata: project name, acronym, version, and tagline. conftest.py is active pytest configuration: it adds the project root to sys.path, tries optional auto_module_shims, patches submodule paths, and defines fixtures. Deleting it can break tests.
Archive command

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29\root_generated_manifests"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    ".docstring_cache.json",
    ".docstring_run_report.jsonl",
    ".pykanda_runtime_guard.json",
    "ARCHITECTURE.md",
    "architecture_manifest.json",
    "BUNDLE_MANIFEST_PYKANDA_PHASE0C_BASELINE.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE0D_PUBLIC_SYMBOLS.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE1_CANONICAL_OWNER_FREEZE.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE2_COMPATIBILITY_FACADE_CLEANUP.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE3_STATE_OWNERSHIP.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE4_GUI_LIFECYCLE.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE5_RUNTIME_ACTION_ROUTER_CLEANUP.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE6_VALIDATION_EXPANSION.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE7_ONE_COMMAND_VALIDATION.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE7_ONE_COMMAND_VALIDATION.txt - Shortcut.lnk",
    "BUNDLE_MANIFEST_PYKANDA_PHASE8_RESIDUE_WORKBENCH_QUARANTINE.txt",
    "BUNDLE_MANIFEST_PYKANDA_PHASE9_REAL_REFACTOR_CONTROL.txt"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

Final answer: yes for the generated/cache/manifest files; no for .gitignore, __init__.py, and conftest.py.

.gitignore
File
__init__.py
Python
conftest.py
Python
demo_script.py
Python
demo_script_corrected.py
Python
llm_runtime_summary.py
Python
pykanda_gui.py
Python
pykanda_gui_help.json
File
pykanda_gui_validate_manifests.py
Python
refactor_move_daily_helpers.py
Python
requirements.lock
File
run_ai_report.py
Python
runtime_map.py
Python
tools_refactor_remove_dev_tools.py
Python
unknown_logic_commented.py
Python
what can I delete

Yes. From these uploaded root files, this is the safest decision.
Keep in root

Do not delete these:

.gitignore
__init__.py
conftest.py
requirements.lock
pykanda_gui.py
pykanda_gui_help.json
pykanda_gui_validate_manifests.py

Why: __init__.py contains the project metadata/version. conftest.py configures pytest, adds the project root and subpackages to sys.path, and defines fixtures. pykanda_gui.py is the current main GUI launcher and imports the pykanda_gui_help helper modules. pykanda_gui_help.json is the manifest for that refactor and explicitly says to read it before editing the helper folder. pykanda_gui_validate_manifests.py validates the *_help.json manifests, so it belongs with the helper-split workflow.
Can remove from root

Archive first, then delete later:

demo_script.py
demo_script_corrected.py
llm_runtime_summary.py
refactor_move_daily_helpers.py
run_ai_report.py
runtime_map.py
tools_refactor_remove_dev_tools.py
unknown_logic_commented.py

Why: both demo scripts only print hello. llm_runtime_summary.py is an old API URL monitor/patcher for ai_starter. refactor_move_daily_helpers.py is a one-time mass-moving refactor script. run_ai_report.py is an old report generator. runtime_map.py even references old E:/EEG_KANDA, so it should not be active PyKANDA root code. tools_refactor_remove_dev_tools.py edits imports across the project, so it is risky to leave loose in root. unknown_logic_commented.py is old API patch-integrity logic for dev_tools.
Command

$root = "E:\pykanda"
$archive = Join-Path $root "workbench\root_cleanup_archive_2026_05_29\old_root_tools"

New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "demo_script.py",
    "demo_script_corrected.py",
    "llm_runtime_summary.py",
    "refactor_move_daily_helpers.py",
    "run_ai_report.py",
    "runtime_map.py",
    "tools_refactor_remove_dev_tools.py",
    "unknown_logic_commented.py"
)

foreach ($item in $items) {
    $src = Join-Path $root $item
    if (Test-Path $src) {
        Move-Item -Path $src -Destination $archive -Force
        Write-Host "Archived: $item"
    } else {
        Write-Host "Not found: $item"
    }
}

Final answer: delete/archive the old root tools and demo files; keep .gitignore, __init__.py, conftest.py, requirements.lock, pykanda_gui.py, pykanda_gui_help.json, and pykanda_gui_validate_manifests.py.

._tmp_format.cpython-312.pyc
File
__init__.cpython-310.pyc
File
__init__.cpython-312.pyc
File
__init__.cpython-313.pyc
File
conftest.cpython-310-pytest-8.4.2.pyc
File
conftest.cpython-312.pyc
File
conftest.cpython-312-pytest-9.0.2.pyc
File
conftest.cpython-313-pytest-9.0.1.pyc
File
emoji_cleaner.cpython-312.pyc
File
pykanda_gui.cpython-310.pyc
File
pykanda_gui.cpython-312.pyc
File
pykanda_gui.cpython-313.pyc
File
run_cognitive_awareness_test.cpython-313-pytest-9.0.1.pyc
File
run_sync_test.cpython-312-pytest-9.0.2.pyc
File
test_cognitive_query.cpython-312-pytest-9.0.2.pyc
File
test_embedding.cpython-312-pytest-9.0.2.pyc
File
test_find_project_mind_graph_json.cpython-312-pytest-9.0.2.pyc
File
test_find_project_mind_graph_json.cpython-313-pytest-9.0.1.pyc
File
test_mode_transition_rewrite.cpython-312-pytest-9.0.2.pyc
File
test_query.cpython-312-pytest-9.0.2.pyc
File
can I remove 

Yes — you can remove all of these .pyc files.

They are Python bytecode cache files, not source code. Python and pytest recreate them automatically when needed.

These are safe to delete:

*.cpython-310.pyc
*.cpython-312.pyc
*.cpython-313.pyc
*-pytest-*.pyc

Use this from PowerShell:

$root = "E:\pykanda"

Get-ChildItem -Path $root -Recurse -Filter "*.pyc" -File | Remove-Item -Force
Get-ChildItem -Path $root -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

Write-Host "Removed Python bytecode cache files and __pycache__ folders."

Final decision: yes, delete them. Keep the matching .py files such as pykanda_gui.py, conftest.py, and __init__.py.


