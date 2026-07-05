first_prompts_to_ai.zip
Zip Archive
prompt_library.zip
Zip Archive
tell_AI_read_before_all.md
File

_RUN_COLLECTOR_STATUS.txt
Document
kanda_reasoner__ai_handoff_all_in_one.zip
Zip Archive
kanda_reasoner__ai_handoff_upload.zip
Zip Archive
kanda_reasoner__ai_handoff_upload_readme.txt
Document
kanda_reasoner__error_lessons_compact.json
File
kanda_reasoner__error_memory_ai_prompt.md
File
kanda_reasoner__error_memory_full.zip
Zip Archive
kanda_reasoner__error_memory_manifest.json
File
kanda_reasoner__png_assets_part01_of_01.zip
Zip Archive
kanda_reasoner__source_archive_part01_of_01.zip
Zip Archive

0068 Large File Refactor Workbench.md
File
review last chat and the project structure carefully, we builded a refactor large module logic , in architecture review we press run selected mode button to get errors and warnings , there we have a list of large modules, them in tab large module AST split audit we can select one of those modules , after comprehensive review of project split a large medule , from this point ahead, you will create a step by step tutorial in plain english to  an user that is seen this app for the first time.  get from Large module ast split audit,   go through complete logic in large module ast split  audit , then complete large file refator planner  and large file refactor workbenck to at end have module splited  and its help files . in tutorial while going through each item explain each item clearly in plain english for an unexperient first time user.

Boa correção. Antes de codar, vou checar duas coisas: se existe ferramenta melhor e prática para esse tipo de classificação, e depois inserir isso como motor opcional sem criar dependência obrigatória que quebre o app.

Achei a melhor abordagem: AST continua sendo o motor principal porque é nativo, rápido e específico para dependências/refactor safety; Ruff pode entrar como acelerador/sinal auxiliar opcional, quando instalado, para detectar problemas de lint/import/sintaxe em JSON. Ruff é muito rápido, mas sozinho não sabe decidir se mover símbolos é seguro.

Implemented the safer version: AST is the mandatory classifier, and Ruff is an optional high-performance helper when installed.

Ruff is very fast and useful for lint/name/import evidence, but it is not enough by itself to decide if moving symbols across modules is safe. The app now uses deterministic AST evidence for actual refactor-safety classification, and the “Static tools” mode adds Ruff JSON lint evidence only when Ruff exists locally. Ruff supports JSON output and exit-code control, and its rules cover many common Python lint/import/name issues, but Python’s ast is still the correct built-in layer for structural refactor analysis.

What I implemented:

    Added a new read-only classifier module:

        large_module_split_safety_classifier.py

    Added two radio buttons in Large Module AST Split Audit:

        AST heuristic

        Static tools (AST + Ruff if available)

    Added a status label that changes after Run AST Split Audit:

        SAFE REFACTORING in bold green

        RISK REFACTORING in bold red

    Added classification into the audit Markdown and JSON report:

        label

        engine used

        score

        hard blockers

        warnings

        Ruff status if static-tools mode is selected

    Ruff is optional:

        if installed, it runs read-only with JSON output

        if missing, the app falls back to AST without breaking

        it never applies fixes

Patch ZIP:

SHA-256:

144fc46ee3eff56976b7b3146fb209d357ca67d400615ce4f91c248011977714

Sandbox validation completed:

VALIDATION OK: large-module-split-audit-safety-classifier-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

PowerShell is not available in this sandbox, so I validated the Python logic, module sizes, py_compile behavior, and ZIP contract here, but I could not execute the .ps1 scripts locally.
Install

Place the ZIP at:

E:\kanda_large_module_split_audit_safety_classifier_v1_patch.zip

Then run:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-module-split-audit-safety-classifier-v1"
    $PATCH_NAME = "kanda_large_module_split_audit_safety_classifier_v1_patch.zip"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")

    $ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT $PATCH_NAME
    $STAGED_PATCH_ZIP = Join-Path $DAILY_ROOT $PATCH_NAME
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")

    if (-not (Test-Path $PROJECT_ROOT)) {
        throw "Project root not found: $PROJECT_ROOT"
    }

    if (-not (Test-Path $DAILY_ROOT)) {
        New-Item -ItemType Directory -Path $DAILY_ROOT -Force | Out-Null
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $STAGED_PATCH_ZIP -Force

        if (-not (Test-Path $STAGED_PATCH_ZIP)) {
            throw "Patch ZIP staging failed: $STAGED_PATCH_ZIP"
        }

        Remove-Item -Path $ROOT_PATCH_ZIP -Force
    }

    if (-not (Test-Path $STAGED_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $EXTRACT_ROOT) {
        Remove-Item -Path $EXTRACT_ROOT -Recurse -Force
    }

    New-Item -ItemType Directory -Path $EXTRACT_ROOT -Force | Out-Null
    Expand-Archive -Path $STAGED_PATCH_ZIP -DestinationPath $EXTRACT_ROOT -Force

    $INSTALL_SCRIPT = Join-Path $EXTRACT_ROOT "INSTALL.ps1"

    if (-not (Test-Path $INSTALL_SCRIPT)) {
        throw "INSTALL.ps1 not found inside extracted daily-work patch: $INSTALL_SCRIPT"
    }

    powershell -NoProfile -ExecutionPolicy Bypass -File $INSTALL_SCRIPT -ProjectRoot $PROJECT_ROOT

    Write-Host ""
    Write-Host "INSTALL OK. Terminal will clear in 2 seconds..."
    Start-Sleep -Seconds 2
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }

    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validate + Freeze

Run after install:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-module-split-audit-safety-classifier-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")
    $VALIDATE_SCRIPT = Join-Path $EXTRACT_ROOT "VALIDATE.ps1"
    $FREEZE_SCRIPT = Join-Path $EXTRACT_ROOT "FREEZE.ps1"

    if (-not (Test-Path $PROJECT_ROOT)) {
        throw "Project root not found: $PROJECT_ROOT"
    }

    if (-not (Test-Path $VALIDATE_SCRIPT)) {
        throw "VALIDATE.ps1 not found: $VALIDATE_SCRIPT"
    }

    if (-not (Test-Path $FREEZE_SCRIPT)) {
        throw "FREEZE.ps1 not found: $FREEZE_SCRIPT"
    }

    powershell -NoProfile -ExecutionPolicy Bypass -File $VALIDATE_SCRIPT -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Validation failed; freeze blocked."
    }

    powershell -NoProfile -ExecutionPolicy Bypass -File $FREEZE_SCRIPT -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Freeze evidence merge failed."
    }
}
catch {
    Write-Host ""
    Write-Host "VALIDATE/FREEZE ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host

Expected markers:

VALIDATION OK: large-module-split-audit-safety-classifier-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
FREEZE_HINT_EVIDENCE_MERGE_OK: large-module-split-audit-safety-classifier-v1
FREEZE HINT MERGE OK: large-module-split-audit-safety-classifier-v1
STATUS: IN_SYNC

Then run:

Freeze Feature After Update -> Preview -> Confirm and Write

This keeps the audit read-only and uses the label only to guide whether the user should continue into Planner/Workbench or choose another refactor strategy.

eacht time a new file is in path of  Target.py in "Large Module AST split  Audit" tab,  make it automatically load in  path of Target.py in "Large File  Refactor  Planner" tab when we click in its tab ear and also populate all fields of "Large file refactor  Planner" tab 

Vou fazer essa ligação como sincronização de seleção entre abas, não como cópia manual de texto: ao entrar em Large File Refactor Planner, ele deve ler o Target.py atual do AST Split Audit, carregar o mesmo arquivo e disparar a rotina oficial de preenchimento dos campos do Planner. Primeiro vou localizar os pontos reais de troca de aba e as rotinas existentes de “load target/populate fields” para reutilizá-las sem duplicar lógica.

A ligação mais segura ficou clara: a aba Planner continuará aceitando apenas alvos que ainda pertencem à fila WARNING MODULE_TOO_LARGE. Ao abrir a aba Planner, ela refresca a fila, encontra o mesmo Target .py do AST Audit, seleciona-o, executa a análise read-only, gera o split plan determinístico e as propostas de docstring, e limpa qualquer estado downstream antigo desse Planner para não misturar dois arquivos.

Encontrei um detalhe importante no handoff: o __init__.py do pacote referencia um módulo criado por um train anterior que não está no source archive exportado. Para não mascarar isso nem depender de um archive incompleto, estou validando a nova sincronização de forma isolada e contratual, sem usar esse __init__.py inconsistente como fonte de verdade.

Implemented.

The behavior is now:

Large Module AST Split Audit
    -> Target .py changes
    -> user clicks Large File Refactor Planner tab ear
    -> Planner refreshes current WARNING MODULE_TOO_LARGE candidates
    -> finds the same Target .py
    -> selects that candidate
    -> populates Target .py
    -> populates candidate queue and metrics
    -> runs read-only AST analysis
    -> populates Analysis Evidence
    -> generates deterministic Split Plan
    -> generates Docstring Proposals
    -> refreshes Planner status and button states

The user's current Planner settings, such as ideal lines, maximum lines, and minimum helper size, are preserved and used rather than reset.

A target that is no longer part of the current WARNING MODULE_TOO_LARGE queue is fail-closed instead of silently loading a different module.

The sync also clears old target-specific Planner state such as previous preview, validation, patch, payload, and apply-gate objects, preventing one module's state from contaminating another.
PATCH DELIVERY GATE

ZIP purpose:
Synchronize the current Large Module AST Split Audit Target .py into the
Large File Refactor Planner when the Planner tab ear is opened.

ZIP placement path:
E:\kanda_large_file_refactor_planner_ast_target_auto_sync_v1_patch.zip

What this ZIP is:
A focused GUI synchronization patch for Architecture Review and the
Large File Refactor Planner box.

What this ZIP is not:
It is not a source-refactor payload.
It does not split modules.
It does not generate preview files.
It does not mutate selected project source.
It does not rewrite imports.

Install code present: YES

Validation code present: YES

Expected validation markers:
VALIDATION OK: large-file-refactor-planner-ast-target-auto-sync-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
FREEZE_HINT_EVIDENCE_MERGE_OK: large-file-refactor-planner-ast-target-auto-sync-v1
FREEZE HINT MERGE OK: large-file-refactor-planner-ast-target-auto-sync-v1

Changed files:
1. kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py
2. kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py
3. kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ast_audit_planner_sync.py
4. validation/test_large_file_refactor_planner_ast_target_auto_sync_v1.py
5. tools/validate_large_file_refactor_planner_ast_target_auto_sync_v1.py

Allowed write paths:
Only the five listed installed project files.
Daily-work staging and freeze-evidence paths during delivery/validation/freeze.

Forbidden write paths:
Selected project refactor target source files.
.project_reference.
_project_reference.
Generated startup delivery artifacts.
Frozen feature memory by direct file writing.
Unrelated boxes and modules.

Freeze/freeze-intake:
Root-level KANDA_FREEZE_HINT.json is present.
FREEZE.ps1 reruns focused validation, writes UTF-8 no-BOM evidence,
and merges current evidence into the feature-specific local freeze intake.

Error Memory payload:
None. This is a requested feature addition, not an Error Memory correction package.

Post-validation steps:
Run FREEZE.ps1.
Then use Freeze Feature After Update -> Preview -> Confirm and Write.

What not to do:
Do not manually copy payload files.
Do not bypass INSTALL.ps1.
Do not freeze before local validation succeeds.
Do not use a stale AST target that is no longer in the warning candidate queue.

Beginner-safe: YES

GATE STATUS: PASS

Exact final ZIP validation:

VALIDATION OK: large-file-refactor-planner-ast-target-auto-sync-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

SHA-256:

2a4edf1af37aa90f17b4ea1ad3e4ca82a74c06b5005b41e4eef1d37486517c07

Install

Place the ZIP at:

E:\kanda_large_file_refactor_planner_ast_target_auto_sync_v1_patch.zip

Then run:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-ast-target-auto-sync-v1"
    $PATCH_NAME = "kanda_large_file_refactor_planner_ast_target_auto_sync_v1_patch.zip"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")

    $ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT $PATCH_NAME
    $STAGED_PATCH_ZIP = Join-Path $DAILY_ROOT $PATCH_NAME
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")

    if (-not (Test-Path $PROJECT_ROOT)) {
        throw "Project root not found: $PROJECT_ROOT"
    }

    if (-not (Test-Path $DAILY_ROOT)) {
        New-Item -ItemType Directory -Path $DAILY_ROOT -Force | Out-Null
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $STAGED_PATCH_ZIP -Force

        if (-not (Test-Path $STAGED_PATCH_ZIP)) {
            throw "Patch ZIP staging failed: $STAGED_PATCH_ZIP"
        }

        Remove-Item -Path $ROOT_PATCH_ZIP -Force
    }

    if (-not (Test-Path $STAGED_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $EXTRACT_ROOT) {
        Remove-Item -Path $EXTRACT_ROOT -Recurse -Force
    }

    New-Item -ItemType Directory -Path $EXTRACT_ROOT -Force | Out-Null
    Expand-Archive `
        -Path $STAGED_PATCH_ZIP `
        -DestinationPath $EXTRACT_ROOT `
        -Force

    $INSTALL_SCRIPT = Join-Path $EXTRACT_ROOT "INSTALL.ps1"

    if (-not (Test-Path $INSTALL_SCRIPT)) {
        throw "INSTALL.ps1 not found: $INSTALL_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $INSTALL_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "INSTALL.ps1 returned a nonzero exit code."
    }

    Write-Host ""
    Write-Host "INSTALL OK: $FEATURE_ID"
    Start-Sleep -Seconds 2
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validate

Run separately after successful installation:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-ast-target-auto-sync-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")
    $VALIDATE_SCRIPT = Join-Path $EXTRACT_ROOT "VALIDATE.ps1"

    if (-not (Test-Path $VALIDATE_SCRIPT)) {
        throw "VALIDATE.ps1 not found: $VALIDATE_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $VALIDATE_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Validation returned a nonzero exit code."
    }
}
catch {
    Write-Host ""
    Write-Host "VALIDATION ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to continue"
Read-Host "Press Enter again to clear"
Clear-Host

Expected:

VALIDATION OK: large-file-refactor-planner-ast-target-auto-sync-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Freeze evidence merge

Run only after validation passes:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-ast-target-auto-sync-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")
    $FREEZE_SCRIPT = Join-Path $EXTRACT_ROOT "FREEZE.ps1"

    if (-not (Test-Path $FREEZE_SCRIPT)) {
        throw "FREEZE.ps1 not found: $FREEZE_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $FREEZE_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Freeze evidence merge returned a nonzero exit code."
    }
}
catch {
    Write-Host ""
    Write-Host "FREEZE ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to continue"
Read-Host "Press Enter again to clear"
Clear-Host

After the merge succeeds:

Freeze Feature After Update
-> Preview
-> Confirm and Write

The key behavior to test manually is simple: select module A in AST Split Audit, open Planner and confirm module A is fully populated; return to AST Audit, change to module B, reopen Planner, and confirm that the analysis and plan now belong only to module B, with no leftover downstream state from module A.

Part C: Large File Refactor Planner =in practicla terms what we do here because we have few buttons  and none seems to modify anything , or this tab is just for review?

Yes. In practical terms, the Large File Refactor Planner is mainly a planning and review station. It is not the place where the final source module is really split.

The intended separation is:

Large Module AST Split Audit
    -> is this file safe or risky to refactor?

Large File Refactor Planner
    -> how should this file be split?

Large File Refactor Workbench
    -> generate the real split, validate it, apply it, and rollback if needed

That separation is intentional: the Planner owns analysis and the validated refactor plan, while the Workbench owns real preview generation, structural validation, guarded source apply, post-apply validation, and rollback.
What the Planner actually does

With the current logic, the Planner answers these practical questions:
1. Which large file are we planning to split?

Now, after the synchronization patch, when you select:

Large Module AST Split Audit
Target .py = module_a.py

and open:

Large File Refactor Planner

the Planner should automatically load module_a.py and populate its analysis and plan fields.
2. What is inside this module?

The Analyze File action examines the module and produces read-only evidence such as:

    functions;

    classes;

    imports;

    public symbols;

    missing docstrings;

    global-state risks;

    dependency information;

    external importer evidence;

    architecture warnings.

So this button means:

    “Understand this file before deciding how to split it.”

It does not change the file.
3. How does the tool propose splitting it?

The Generate Split Plan button is probably the most important Planner action.

Its job is to say something like:

Current module:
large_file.py
Lines: 1,420

Proposed structure:

large_file.py
    Public facade and orchestration
    Estimated: 280 lines

_large_file_analysis.py
    Analysis functions
    Estimated: 330 lines

_large_file_validation.py
    Validation functions
    Estimated: 260 lines

_large_file_io.py
    File reading/writing responsibilities
    Estimated: 210 lines

In other words:

    It proposes the architecture of the future split.

It does not yet perform the final source refactor.
4. What happens to missing docstrings?

The Generate Docstring Plan button identifies missing docstrings and proposes what should be documented.

The practical question it answers is:

    “When we split this module, which modules, classes, functions, and methods need documentation?”

Again, this is planning evidence.

It does not modify the original module.
5. What is the local LLM button for?

Ask Local LLM for Ambiguous Symbols is intended only for uncertain planning decisions.

Example:

function normalize_report_data()

The deterministic planner may be uncertain whether it belongs in:

_analysis.py

or:

_formatting.py

The local AI can help classify that ambiguous symbol.

It should not rewrite the code.

The role is:

    “Help decide where difficult symbols belong.”

The confusing part: Preview, Validate Preview, Create Patch ZIP, Prepare Apply Gate

This is where the GUI can be misleading.

The current Planner code contains buttons such as:

Generate Preview
Validate Preview
Create Patch ZIP
Prepare Apply Gate

Historically, the Planner grew into a planner/previewer/validator/patch-preparation workflow. But after we created the Workbench architecture, the conceptual responsibility became clearer:

    The Planner prepares and reviews the plan. The Workbench is the real refactoring production line.

The frozen architecture explicitly states that the Planner should produce or prepare a structured plan artifact and should not become a new source-mutation path.

So I would explain those buttons this way:
Generate Preview

In the Planner context, this is a planning preview artifact, not the final source mutation.

It answers:

    “What would the proposed structure look like?”

The real source-ready split should continue through the Workbench.
Validate Preview

Checks whether the planning preview is internally acceptable.

It does not mean:

    “The project has now been safely refactored.”

Create Patch ZIP

Prepares a governed project payload only after validation.

But conceptually, now that the Workbench exists, I would treat this as a legacy/advanced Planner route rather than the normal first-time-user route.
Prepare Apply Gate

This creates apply-gate evidence.

It should not itself mutate source.

Again, for the normal user workflow, the Workbench is the clearer continuation point.
My honest view of the current UI

I think your confusion is completely justified.

The Planner currently looks more complicated than its true conceptual role because it contains buttons inherited from its earlier evolution.

For a beginner, I would simplify its meaning to this:
Large File Refactor Planner

Use it to:

    inspect the selected large module;

    review its risks;

    decide how responsibilities should be grouped;

    generate the proposed helper-module structure;

    review docstrings;

    optionally use the local LLM for ambiguous grouping;

    produce the validated plan that the Workbench will consume.

Then stop.

The normal route should be:

AST Split Audit
    -> classify safety

Planner
    -> decide architecture of the split

Workbench
    -> generate real files
    -> validate
    -> backup
    -> build payload
    -> exact-token apply
    -> post-apply validation
    -> rollback

That Planner/Workbench split is also the documented architecture: Planner produces the validated plan; Workbench consumes it, generates real refactored preview files, validates, applies through exact confirmation, and preserves rollback.
What I would do as the user today

For your workflow, I would use the Planner only up to:

Analyze File
Generate Split Plan
Generate Docstring Plan
Ask Local LLM for Ambiguous Symbols  [optional]

Then open:

Large File Refactor Workbench

The Workbench should receive that Planner state and continue the real process.
My recommendation

I think the next UI improvement should be to make this distinction visually obvious inside the Planner:

PLANNER PURPOSE
Review and prepare the refactor architecture.
This tab does not directly refactor project source.

Recommended next step:
Open Large File Refactor Workbench

And possibly rename or visually separate the older advanced buttons into something like:

Advanced / Legacy Planner Artifacts

because right now Generate Preview, Create Patch ZIP, and Prepare Apply Gate make the tab look like it is also the final refactoring engine, while the newer architecture assigns that production role to the Workbench.

where is generate split plan button in  largefile refacro planner?

Vou conferir o código real da aba antes de responder, porque pelo que você descreveu há boa chance de eu ter citado um botão que não existe com esse nome.

You are not missing a separate hidden screen. I checked the actual gui_shell.py from the project source archive.

The button does exist in the current code:

5. Preview, validation, and patch panel

[Analyze File]
[Generate Split Plan]
[Generate Docstring Plan]
[Ask Local LLM for Ambiguous Symbols]
[Generate Preview]
[Validate Preview]
[Create Patch ZIP]
[Prepare Apply Gate]
[Open Preview Folder]
[Copy Summary]
[Cancel]

So Generate Split Plan is the second button, immediately after Analyze File.

The Planner is intended to propose the split architecture before the Workbench consumes it.
Why you may not be seeing it

I found a GUI design problem: all 11 buttons are placed in one single horizontal row.

So on a normal-width window, the row can become crowded or clipped. There is no multi-row button layout in that part of the current source.

Also, Generate Split Plan starts disabled. Its normal sequence is:

1. Select Target .py
2. Analyze File
3. Generate Split Plan becomes enabled
4. Click Generate Split Plan

With the recent auto-sync behavior, the Planner may already populate analysis and plan state when you enter the tab, but the physical button still exists in the source.
My conclusion

The button exists, but the Planner GUI layout is poor. I would restructure that bottom area into clear stages instead of one enormous horizontal row, for example:

PLANNING
[Analyze File]
[Generate Split Plan]
[Generate Docstring Plan]
[Ask Local AI]

ADVANCED PLANNER OUTPUT
[Generate Preview]
[Validate Preview]
[Create Patch ZIP]
[Prepare Apply Gate]

UTILITIES
[Open Preview Folder]
[Copy Summary]
[Cancel]

That would make the Planner much easier to understand and would stop buttons from disappearing visually on narrower windows.

I clicked in generate split plan and it and all buttons after it continue grey inactive  and dont return to normal 

Vou rastrear o estado dos botões no código real do Planner: quem desabilita o bloco, qual sinal deveria reabilitá-lo e se o auto-sync recente deixou algum estado preso. Depois corrijo o fluxo e entrego um patch focado.

Encontrei o primeiro defeito real: quando o plano retorna blocked, o próprio Generate Split Plan é desabilitado. Isso deixa a interface presa, porque o usuário não consegue ajustar os limites e gerar o plano novamente. Agora vou verificar por que o plano está retornando blocked com tanta facilidade e corrigir sem liberar Preview quando houver bloqueador verdadeiro.

O problema é mais específico do que parecia: a GUI usa um único enum de estado para controlar todos os botões. Quando o plano entra em BLOCKED, ela desliga inclusive o próprio Generate Split Plan, criando um beco sem saída. Vou trocar apenas a lógica de habilitação por pré-requisitos reais: análise existente, plano existente, plano sem blockers, preview existente etc.

I found the bug and fixed it.

The problem was in the Planner's button-state logic, not in the button itself.

After Generate Split Plan, when the plan returned blocked, the GUI entered PlannerState.BLOCKED. The old logic then disabled Generate Split Plan itself, leaving the user in a dead end.

The old logic effectively behaved like this:

PLAN_READY
    -> buttons enabled

BLOCKED
    -> Generate Split Plan disabled
    -> Generate Docstring Plan disabled
    -> LLM disabled
    -> Generate Preview disabled
    -> user cannot recover

I changed the Planner to use actual prerequisites and artifacts, instead of using one global state value to control every button.

After the patch:

Analysis exists
    -> Generate Split Plan enabled
    -> Generate Docstring Plan enabled

Plan exists
    -> Local LLM review enabled

Plan status = planned
    -> Generate Preview enabled

Plan status = blocked
    -> Generate Split Plan stays enabled
    -> Generate Docstring Plan stays enabled
    -> Local LLM review stays enabled
    -> Generate Preview stays disabled for safety

Preview exists
    -> Validate Preview enabled

Validation passed
    -> Create Patch ZIP enabled

Payload ready
    -> Prepare Apply Gate enabled

So there is an important distinction:

The user can always recover from a blocked plan, but a genuinely blocked plan still cannot proceed into preview generation.

I also fixed another unsafe state transition: generating docstring proposals or running LLM review on a blocked plan can no longer silently convert the Planner into a ready state.
Patch

SHA-256:

ab00c2927b55dce60ba017f93ae1d5d9cfde0b7d0c3bfdd213f044711260b90e

Validation completed:

VALIDATION OK: large-file-refactor-planner-button-state-recovery-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Exact final ZIP contract validation also passed:

ZIP CONTRACT: PASS

No split-planning algorithm was changed in this patch. It only repairs the GUI state progression and recovery logic.
Install

Place the ZIP at:

E:\kanda_large_file_refactor_planner_button_state_recovery_v1_patch.zip

Then run:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-button-state-recovery-v1"
    $PATCH_NAME = "kanda_large_file_refactor_planner_button_state_recovery_v1_patch.zip"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")

    $ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT $PATCH_NAME
    $STAGED_PATCH_ZIP = Join-Path $DAILY_ROOT $PATCH_NAME
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")

    if (-not (Test-Path $PROJECT_ROOT)) {
        throw "Project root not found: $PROJECT_ROOT"
    }

    if (-not (Test-Path $DAILY_ROOT)) {
        New-Item -ItemType Directory -Path $DAILY_ROOT -Force | Out-Null
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $STAGED_PATCH_ZIP -Force

        if (-not (Test-Path $STAGED_PATCH_ZIP)) {
            throw "Patch ZIP staging failed: $STAGED_PATCH_ZIP"
        }

        Remove-Item -Path $ROOT_PATCH_ZIP -Force
    }

    if (-not (Test-Path $STAGED_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $EXTRACT_ROOT) {
        Remove-Item -Path $EXTRACT_ROOT -Recurse -Force
    }

    New-Item -ItemType Directory -Path $EXTRACT_ROOT -Force | Out-Null

    Expand-Archive `
        -Path $STAGED_PATCH_ZIP `
        -DestinationPath $EXTRACT_ROOT `
        -Force

    $INSTALL_SCRIPT = Join-Path $EXTRACT_ROOT "INSTALL.ps1"

    if (-not (Test-Path $INSTALL_SCRIPT)) {
        throw "INSTALL.ps1 not found: $INSTALL_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $INSTALL_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "INSTALL.ps1 returned a nonzero exit code."
    }

    Write-Host ""
    Write-Host "INSTALL OK: $FEATURE_ID"
    Start-Sleep -Seconds 2
    Clear-Host
}
catch {
    Write-Host ""
    Write-Host "INSTALL ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Validate

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-button-state-recovery-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")
    $VALIDATE_SCRIPT = Join-Path $EXTRACT_ROOT "VALIDATE.ps1"

    if (-not (Test-Path $VALIDATE_SCRIPT)) {
        throw "VALIDATE.ps1 not found: $VALIDATE_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $VALIDATE_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Validation returned a nonzero exit code."
    }
}
catch {
    Write-Host ""
    Write-Host "VALIDATION ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to continue"
Read-Host "Press Enter again to clear"
Clear-Host

Expected:

VALIDATION OK: large-file-refactor-planner-button-state-recovery-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Freeze evidence merge

Run after validation succeeds:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-button-state-recovery-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")
    $FREEZE_SCRIPT = Join-Path $EXTRACT_ROOT "FREEZE.ps1"

    if (-not (Test-Path $FREEZE_SCRIPT)) {
        throw "FREEZE.ps1 not found: $FREEZE_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $FREEZE_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Freeze evidence merge returned a nonzero exit code."
    }
}
catch {
    Write-Host ""
    Write-Host "FREEZE ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to continue"
Read-Host "Press Enter again to clear"
Clear-Host

Then:

Freeze Feature After Update
-> Preview
-> Confirm and Write

After installation, the key manual test is:

1. Open Planner with a populated target.
2. Click Generate Split Plan.
3. If plan is valid:
      Generate Preview should activate.
4. If plan is blocked:
      Generate Split Plan must remain active.
      Generate Docstring Plan must remain active.
      LLM review must remain available.
      Generate Preview must remain disabled.
5. Adjust Planner settings if appropriate.
6. Click Generate Split Plan again.

This removes the dead-end behavior while preserving the safety blockers.

KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_BEGIN
Title: Last frozen feature entry
Project root: E:\kanda_reasoner
Entry count: 1
Instruction: Use this as read-only frozen feature memory. Do not edit these entries directly. Do not write project-specific memory into project_freeze_ledger.

--- FROZEN ENTRY 1 OF 1 ---
Path: E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update\frozen_features_memory\entries\freeze-20260704-large-file-refactor-planner-button-state-recovery.md

---
freeze_id: "freeze-20260704-large-file-refactor-planner-button-state-recovery"
feature_title: "Large File Refactor Planner Button State Recovery"
box: "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
status: "frozen"
date: "2026-07-04"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260704-large-file-refactor-planner-button-state-recovery.md"
protected_paths:
  - "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py"
  - "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_action_enablement.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Generate Split Plan must remain available whenever a current analysis artifact exists, including after a blocked plan result."
  - "Generate Docstring Plan is review-only and may remain available when analysis exists, but it must not convert a blocked plan into an unblocked preview state."
  - "Local LLM arbitration remains advisory and may remain available when a plan exists, but it must not bypass a blocked plan."
  - "Generate Preview must remain disabled when the current split plan status is blocked."
  - "Validate Preview requires an actual preview bundle and preview write result."
  - "Create Patch ZIP requires passed preview validation."
  - "Prepare Apply Gate requires payload_ready status."
  - "Planner warning gating, AST-target auto-sync, source mutation gates, import rewrite gates, and Workbench contracts must remain unchanged."
  - "All touched/new source modules must remain <=500 physical lines."
  - "The small pure enablement helper is a justified stable UI-state seam and must not become a second workflow truth source."
  - "Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260704-large-file-refactor-planner-button-state-recovery

## freeze identity

Freeze ID: freeze-20260704-large-file-refactor-planner-button-state-recovery

Feature title: Large File Refactor Planner Button State Recovery

Date: 2026-07-04

Primary box: kanda_reasoner_app/manage_architecture/large_file_refactor_planner

Box type: tool-owned Architecture Review Planner GUI state-control repair

Status: frozen after explicit human confirmation and validation evidence

## summary

This patch repairs GUI state progression only. It does not alter split-plan algorithms, preview generation logic, source apply behavior, Workbench behavior, or import rewrite behavior. Freeze-intake data was loaded from <project>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake. Source patch ZIP: kanda_large_file_refactor_planner_button_state_recovery_v1_patch.zip.

## validated files

- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py
- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_action_enablement.py
- validation/test_large_file_refactor_planner_button_state_recovery_v1.py
- tools/validate_large_file_refactor_planner_button_state_recovery_v1.py

## generated files

- No project source refactor outputs are generated by this patch. Runtime behavior only changes in-memory GUI action enablement.

## protected paths

- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py
- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_action_enablement.py
- project_freeze_after_update/frozen_features_memory

## do-not-regress rules

- Generate Split Plan must remain available whenever a current analysis artifact exists, including after a blocked plan result.
- Generate Docstring Plan is review-only and may remain available when analysis exists, but it must not convert a blocked plan into an unblocked preview state.
- Local LLM arbitration remains advisory and may remain available when a plan exists, but it must not bypass a blocked plan.
- Generate Preview must remain disabled when the current split plan status is blocked.
- Validate Preview requires an actual preview bundle and preview write result.
- Create Patch ZIP requires passed preview validation.
- Prepare Apply Gate requires payload_ready status.
- Planner warning gating, AST-target auto-sync, source mutation gates, import rewrite gates, and Workbench contracts must remain unchanged.
- All touched/new source modules must remain <=500 physical lines.
- The small pure enablement helper is a justified stable UI-state seam and must not become a second workflow truth source.
- Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.
- Do not store project-specific frozen memory inside project_freeze_ledger.
- Preview Freeze Entry must remain read-only and must not write files.
- Confirm and Write must require explicit human confirmation before writing governed freeze memory.
- After a local freeze write, the AI startup freeze context must be refreshed.
- External AI review remains advanced/fallback, not the normal local freeze path.

## validation evidence

text
VALIDATION OK: large-file-refactor-planner-button-state-recovery-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
FREEZE_HINT_EVIDENCE_MERGE_OK: large-file-refactor-planner-button-state-recovery-v1



## known warnings

['If the split plan itself reports validation blockers, Generate Preview remains intentionally disabled. The repair prevents UI dead-end but does not bypass plan safety blockers.', 'The source archive handoff omitted one unrelated previously frozen planner module referenced by package __init__; focused validation loads the pure state helper directly and does not treat that archive inconsistency as source truth.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Large File Refactor Planner Button State Recovery.

## planned next step

Install, run focused validation, merge freeze evidence, then Freeze Feature After Update -> Preview -> Confirm and Write.

## local freeze writer provenance

Generated by 
local_freeze_writer_engine_v1 at 2026-07-04T06:57:03Z.

This entry was created locally for the selected active project. The reusable project_freeze_ledger engine remains blueprint logic only and is not the owner of this project-specific memory.

KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_END

divide content of "Large file refactor Planner" tab in two colums to improve use of space 
 update 

1. Open Planner with a populated target.
2. Click Generate Split Plan.
3. If plan is valid - implement check with local AI if it is valid = if not correct until it become correct 
      Generate Preview should activate.
4. If plan is blocked:
      Generate Split Plan must remain active.
      Generate Docstring Plan must remain active.
      LLM review must remain available.
      Generate Preview must remain disabled.
5. Adjust Planner settings if appropriate.
6. Click Generate Split Plan again.










Vou tratar isso em duas mudanças coordenadas: primeiro reorganizar o Planner em duas colunas sem mexer na lógica congelada; depois transformar a revisão local por IA em um ciclo explícito de validação/correção do plano, mantendo Generate Preview bloqueado até o plano ficar válido. Vou partir do código real atual e preservar os gates já congelados.

one more thing if AI local not present -pass  steps that use local ai and continue heuristically

Entendido. O fluxo será AI-optional: quando o modelo local existir, ele revisa/corrige o plano em loop até ficar válido; quando não existir, essa etapa é pulada automaticamente e o Planner continua pelo caminho heurístico, sem bloquear o usuário.

IMPLEMENTATION GATE

Task domain: Large File Refactor Planner GUI layout plus AI-optional plan review/correction loop.
Router bridge selected: governed implementation inside the existing large-file refactor box.
Required prompt path: large_module_refactor_protocol + box/shielding canon + Python refactoring + implementation/delivery protocol.
Target box: kanda_reasoner_app/manage_architecture/large_file_refactor_planner.
Forbidden box: Workbench source-apply behavior, import rewrite behavior, startup delivery, freeze memory direct writes, unrelated Architecture Review boxes.
Source files inspected: current Planner GUI/state modules and local-AI integration modules from the uploaded source archive, plus the latest frozen button-state recovery patch.
Generated-vs-canonical status: source modules are canonical; patch ZIPs and reports are delivery/evidence only.
Project/tool disambiguation needed: YES - this is KANDA Reasoner tool GUI logic, not a refactor of the active project target module.
Line-count risk: active; every touched/new Python module must remain <=500 physical lines.
GUI-resolution risk: active; two-column layout must remain usable on laptop widths and larger displays.
May implement: YES.

O desenho final será conservador: a IA local não ganha poder para “inventar” uma nova arquitetura livremente. Ela pode revisar o plano heurístico e propor apenas correções estruturadas dentro dos módulos candidatos já conhecidos; cada correção é revalidada deterministicamente. O loop é limitado a três rodadas para evitar travamento infinito, e qualquer indisponibilidade da IA cai automaticamente para o plano heurístico.

Implemented with the additional rule you requested: local AI is optional and never becomes a dependency of the Planner workflow.

The resulting logic is:

Generate Split Plan
        |
        v
Deterministic heuristic plan
        |
        +---- local AI available and enabled?
        |             |
        |             YES
        |              |
        |              v
        |       Review plan in background
        |              |
        |       valid? -------- YES ------> final deterministic validation
        |         |
        |         NO
        |         |
        |         v
        |   bounded correction proposal
        |         |
        |         v
        |   deterministic revalidation
        |         |
        |         +---- repeat, maximum 3 rounds
        |
        NO
        |
        v
AI step is skipped
Continue with heuristic plan

Important safety behavior:

    If the heuristic plan is valid and no local AI exists, Preview becomes available normally.

    If the heuristic plan is genuinely blocked and no local AI exists, it remains blocked. Missing AI does not bypass a real blocker.

    AI corrections are limited to structured helper-to-helper symbol reassignment among already proposed modules.

    AI cannot rewrite source code, invent files, change facade ownership, apply source changes, or rewrite imports.

    Every AI correction is deterministically revalidated.

    The AI loop is limited to three rounds to prevent infinite correction loops.

    Local-AI work runs in a background thread so the GUI does not freeze.

The Planner layout is also changed to a resizable two-column interface, and the former single crowded button row is split into planning and workflow rows.
PATCH DELIVERY GATE

PATCH DELIVERY GATE

ZIP purpose:
Improve Large File Refactor Planner space usage with a resizable two-column
layout and add optional bounded local-AI plan review/correction with automatic
heuristic fallback.

ZIP placement path:
E:\kanda_large_file_refactor_planner_two_column_ai_optional_review_v1_patch.zip

What this ZIP is:
A focused tool-owned Planner GUI and plan-review workflow update.

What this ZIP is not:
It is not a selected-project source refactor payload.
It does not split the selected target module.
It does not apply source changes.
It does not rewrite project imports.
It does not change Workbench exact-token apply behavior.

Install code present: YES

Validation code present: YES

Expected validation markers:
VALIDATION OK: large-file-refactor-planner-two-column-ai-optional-review-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS
FREEZE_HINT_EVIDENCE_MERGE_OK: large-file-refactor-planner-two-column-ai-optional-review-v1
FREEZE HINT MERGE OK: large-file-refactor-planner-two-column-ai-optional-review-v1

Changed files:
1. kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py
2. kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_action_enablement.py
3. kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_two_column_layout.py
4. kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_plan_review.py
5. kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_review_gui.py
6. kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_review_formatting.py
7. validation/test_large_file_refactor_planner_two_column_ai_optional_review_v1.py
8. tools/validate_large_file_refactor_planner_two_column_ai_optional_review_v1.py

Allowed write paths:
Only the listed project files during installation.
Dynamic daily-work staging.
Feature-specific validation/freeze evidence paths.

Forbidden write paths:
Selected project refactor target modules.
.project_reference.
_project_reference.
Startup delivery artifacts.
Direct frozen-memory writes.
Unrelated Architecture Review boxes.
Workbench source-apply logic.
Import-rewrite apply logic.

Freeze/freeze-intake:
Root-level KANDA_FREEZE_HINT.json is present.
FREEZE.ps1 re-runs focused validation and merges current evidence into the
feature-specific local freeze intake.

Error Memory payload:
None. This is a requested feature extension, not a new error-repair lesson.

Post-validation steps:
Run FREEZE.ps1.
Then use Freeze Feature After Update -> Preview -> Confirm and Write.

What not to do:
Do not treat local AI as mandatory.
Do not install preview artifacts manually.
Do not bypass a heuristic blocker because AI is absent.
Do not freeze before local validation succeeds.

Beginner-safe: YES

GATE STATUS: PASS

Exact final ZIP checks:

VALIDATION OK: large-file-refactor-planner-two-column-ai-optional-review-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Exact final ZIP contract:

ZIP CONTRACT: PASS

The final ZIP was also re-opened and inspected after packaging. Cache files were removed before the final build.

SHA-256:

bd9aabab82d7e87c4aed2a96cb7581e12790351670c59850c7bcc6f7d28c6bea

What the Planner flow becomes

For the user, the intended sequence is now:

1. Open Planner with a populated Target .py.

2. Click Generate Split Plan.

3. Planner always creates the deterministic heuristic plan first.

4. If local AI is enabled and available:
      AI reviews the plan in the background.

      If valid:
          deterministic validation confirms the result;
          Generate Preview becomes available.

      If AI requests correction:
          only bounded structured reassignment is accepted;
          correction is deterministically revalidated;
          AI reviews again;
          maximum 3 rounds.

5. If local AI is unavailable:
      AI stage is marked skipped;
      Planner continues using the heuristic plan.

6. If final plan is valid:
      Generate Preview becomes active.

7. If final plan is blocked:
      Generate Split Plan remains available.
      Generate Docstring Plan remains available.
      Local AI review remains available if a model becomes available.
      Generate Preview remains disabled.

8. Adjust settings when appropriate and regenerate the plan.

Install

Place the ZIP at:

E:\kanda_large_file_refactor_planner_two_column_ai_optional_review_v1_patch.zip

Then run:

$ErrorActionPreference = "Stop"
$InstallFailed = $false

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-two-column-ai-optional-review-v1"
    $PATCH_NAME = "kanda_large_file_refactor_planner_two_column_ai_optional_review_v1_patch.zip"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")

    $ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT $PATCH_NAME
    $STAGED_PATCH_ZIP = Join-Path $DAILY_ROOT $PATCH_NAME
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")

    if (-not (Test-Path $PROJECT_ROOT)) {
        throw "Project root not found: $PROJECT_ROOT"
    }

    if (-not (Test-Path $DAILY_ROOT)) {
        New-Item -ItemType Directory -Path $DAILY_ROOT -Force | Out-Null
    }

    if (Test-Path $ROOT_PATCH_ZIP) {
        Copy-Item -Path $ROOT_PATCH_ZIP -Destination $STAGED_PATCH_ZIP -Force

        if (-not (Test-Path $STAGED_PATCH_ZIP)) {
            throw "Patch ZIP staging failed: $STAGED_PATCH_ZIP"
        }

        Remove-Item -Path $ROOT_PATCH_ZIP -Force
    }

    if (-not (Test-Path $STAGED_PATCH_ZIP)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $EXTRACT_ROOT) {
        Remove-Item -Path $EXTRACT_ROOT -Recurse -Force
    }

    New-Item -ItemType Directory -Path $EXTRACT_ROOT -Force | Out-Null

    Expand-Archive `
        -Path $STAGED_PATCH_ZIP `
        -DestinationPath $EXTRACT_ROOT `
        -Force

    $INSTALL_SCRIPT = Join-Path $EXTRACT_ROOT "INSTALL.ps1"

    if (-not (Test-Path $INSTALL_SCRIPT)) {
        throw "INSTALL.ps1 not found: $INSTALL_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $INSTALL_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "INSTALL.ps1 returned a nonzero exit code."
    }
}
catch {
    $InstallFailed = $true

    Write-Host ""
    Write-Host "INSTALL ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }

    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
}

if (-not $InstallFailed) {
    Write-Host ""
    Write-Host "INSTALL OK. Terminal will clear in 2 seconds..."
    Start-Sleep -Seconds 2
    Clear-Host
}

Validate

Run after successful installation:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-two-column-ai-optional-review-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")
    $VALIDATE_SCRIPT = Join-Path $EXTRACT_ROOT "VALIDATE.ps1"

    if (-not (Test-Path $VALIDATE_SCRIPT)) {
        throw "VALIDATE.ps1 not found: $VALIDATE_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $VALIDATE_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Validation returned a nonzero exit code."
    }
}
catch {
    Write-Host ""
    Write-Host "VALIDATION ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host

Expected:

VALIDATION OK: large-file-refactor-planner-two-column-ai-optional-review-v1
STATUS: IN_SYNC
ZIP CONTRACT: PASS

Freeze evidence merge

Run only after validation succeeds:

$ErrorActionPreference = "Stop"

try {
    $PROJECT_ROOT = "E:\kanda_reasoner"
    $FEATURE_ID = "large-file-refactor-planner-two-column-ai-optional-review-v1"

    $PROJECT_ROOT = [System.IO.Path]::GetFullPath($PROJECT_ROOT)
    $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
    $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT).TrimEnd("\")
    $DAILY_ROOT = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
    $EXTRACT_ROOT = Join-Path $DAILY_ROOT ($FEATURE_ID + "_extract")
    $FREEZE_SCRIPT = Join-Path $EXTRACT_ROOT "FREEZE.ps1"

    if (-not (Test-Path $FREEZE_SCRIPT)) {
        throw "FREEZE.ps1 not found: $FREEZE_SCRIPT"
    }

    powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $FREEZE_SCRIPT `
        -ProjectRoot $PROJECT_ROOT

    if ($LASTEXITCODE -ne 0) {
        throw "Freeze evidence merge returned a nonzero exit code."
    }
}
catch {
    Write-Host ""
    Write-Host "FREEZE ERROR"
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host

Then:

Freeze Feature After Update
-> Preview
-> Confirm and Write

For the first manual GUI test, use these two scenarios:

TEST A - Local AI available

1. Open Planner.
2. Confirm Target .py is populated.
3. Leave "Use local AI when available" checked.
4. Click Generate Split Plan.
5. Confirm AI review status changes to reviewing.
6. Confirm GUI remains responsive.
7. Confirm final status becomes validated, corrected, or remains blocked.
8. Confirm Generate Preview activates only when final plan status is planned.

TEST B - No local AI available

1. Stop or make the local Ollama model unavailable.
2. Open Planner.
3. Click Generate Split Plan.
4. Confirm AI status becomes skipped_unavailable.
5. Confirm the heuristic plan remains present.
6. If heuristic plan is valid, Generate Preview activates.
7. If heuristic plan is blocked, Generate Preview stays disabled while
   Generate Split Plan and Generate Docstring Plan remain available.

The GUI-specific runtime interaction still requires your local PySide6 app test; sandbox validation covered the pure correction loop, AI-unavailable heuristic fallback, action gates, source contracts, Python compilation, line limits, clean ZIP contents, and exact ZIP contract.


