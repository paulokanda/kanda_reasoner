first_prompts_to_ai.zip
Zip Archive
prompt_library.zip
Zip Archive
tell_AI_read_before_all.md
File

STARTUP PACK LOAD CHECK

Files recognized:
0. 00_START_HERE_FOR_AI.md - loaded - first boot file for startup inspection, routing readiness, and wait-state control.

    01_ai_prompt_request_canon.md - loaded - governs when loaded context is sufficient and when missing prompts, files, evidence, or decisions must be requested.

    02_prompt_navigation_index.md - loaded - authoritative human-readable router from task intent to prompt groups and specialist prompts.

    03_GROUP_ASSIMILATION_INDEX.md - loaded - broad group-level routing and minimum-context selection layer.

    04_FOLDER_ASSIMILATION_CARDS_INDEX.md - loaded - routes selected groups to folder-level boundary and responsibility cards when needed.

    05_start_of_day_master_stack.md - loaded - minimum safe daily bootstrap stack carrying high-risk startup bridges and routing discipline.

    06_session_start_upload_checklist.md - loaded - operational checklist for collecting project context, evidence, logs, and task materials before governed work.

    07_daily_patch_delivery_guardrails.md - loaded - always-startup safety rules for patch ZIP delivery, staging, validation, root cleanliness, and terminal hygiene.

    08_handoff_at_end_of_work.md - loaded - governs complete contextualized handoff creation when a project session pauses or ends.

    09_patch_install_delivery_error_register.md - loaded - records known patch/install delivery regressions and blocks their recurrence.

    10_prompt_router_reasoner_startup_check.md - loaded - defines startup readiness assessment for Prompt Router Reasoner frozen state and safety constraints.

    11_chatgpt_kanda_routing_choice_output_protocol.md - loaded - governs router-selected prompt addressing and selective on-demand retrieval from prompt_library.zip.

    12_error_memory_ai_formulary_startup_canon.md - loaded - canonical startup workflow for Error Memory AI formulary intake, staging, discovery, and human confirmation.

    09_active_project_freeze_context.md - loaded - exposes current project-specific frozen feature memory context for startup awareness.

    README_STARTUP_PROMPT_REQUEST_KERNEL.md - loaded - explains startup pack purpose, canonical-source rules, generation, and upload workflow.

    STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json - loaded - provides startup pack build metadata, inventory, source mapping, and synchronization information.

Beginning-of-day active bridges:

    Code Module Size Bridge - loaded - hard gate: ideal <=400 code lines; maximum <=500 physical lines; every new or touched code/source module must be <=500 lines after create, update, modify, refactor, or split work; route above-limit code work to large_module_refactor_protocol on demand

    Box Logic Startup Bridge - loaded - hard gate: mandatory beginning-of-chat box shield; identify active box, owner paths, allowed files, out-of-scope files, cross-box touches, public contracts, validation scope, and boundary risks before project work; keep code and responsibility inside the owning box; route boundary-risk work to box_architecture_canon on demand

    No-Leak Logic Bridge - loaded - hard gate: NO_LEAK_LOGIC_V1 prevents wrong-root writes, tool/project leakage, cross-box leakage, private reach-in, public API ownership leakage, hidden mutable state, generated-artifact-as-source leakage, and validation/freeze evidence leakage

    Terminal Cleanup Bridge - loaded - install success waits about 2 seconds then Clear-Host; validation, freeze, errors, diagnostics, and other terminal blocks use Enter Enter then one final Clear-Host; keep terminal open; freeze-prep evidence merge must use a temp .py helper, not python -c, with PYTHONPATH/sys.path set to the project root

Startup status:
COMPLETE

Routing behavior:
I will use Fast Path for explanation, discussion, brainstorming, reading-only analysis, and high-level planning that does not require governed implementation context. For governed work, I will use Routed Work Path: classify the task first, select the minimum required group through group routing, load a folder assimilation card only when folder boundaries or placement rules are needed, and retrieve only specifically addressed specialist prompts from prompt_library.zip when required. I will not load the full prompt library by default or bypass routing, box boundaries, validation, confirmation, freeze, or delivery safeguards.

Next action:
Waiting for all files (Project Files) from second_prompt_files folder

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

0068b Large File Refactor important update.md
File
dont point anything to "The Preview result still points to E:\kanda_reasoner_delete_after_daily_work\large_file_refactor_preview\2df0b9336704." because it is a transitory temp folder; install files go to kanda_reasoner_delete_after_daily_work, files related to kanda_reasoner toll stay in kanda_reasoner folder and files related to kanda_reasoner project stay in project folder , review in prompt library diference toll versus project , folder kanda_reasoner_delete_after_daily_work is canonically non related to project or toll , that folder is just for garbage, correct inforce in code

0030b Project Versus KANDA Reasoner Tool Boundary Canon Addendum.md
File
wait a minute, any file, even "preview files" related to project  (not to tool) must be in dinamic folder  <project>_show_project_to_AI

Pasted text.txt
Document

Pasted text.txt
Document

Pasted text.txt
Document

correct now:

outro problema independente no Show Project to AI: uma regra de exclusão *backup* aplicada como regra de pasta está excluindo um arquivo-fonte legítimo apenas porque backup aparece no nome do módulo:

source_apply_preflight_backup_contract.py

Isso merece uma correção separada depois. Não deve ser misturado silenciosamente com o patch atual.

Pasted text.txt
Document

Pasted text.txt
Document
Now let's solve another problem. When we are in architecture review, run selected mode runs okay. Then we go to large module AST split audit. In this sub-tab, when we look at the target.py, we don't see the path of the largest module found in run selected mode. This is wrong. When we open larger module AST split audit, target.py must be populated with the largest module of run selected mode list. Correct it.

Perfeito — isso muda o desenho da auditoria: não basta corrigir o encadeamento dos botões. Vou também mapear cada estado de bloqueio e criar uma saída governada de correção: quando uma fase falhar, a UI deve expor o erro + contexto + evidência da fase + objetivo de saída (“corrigir até PASS”) e permitir enviar esse pacote ao Heuristic Corrector, Local AI ou Web AI, sem pular a validação nem habilitar a próxima fase artificialmente.

A auditoria confirmou que há dois problemas diferentes, e ambos precisam ser corrigidos juntos:

    Progressão: o Workbench já tem um modelo sequencial, mas o usuário só vê “próxima etapa desabilitada”; não existe um contrato de recuperação quando o resultado anterior vem blocked.

    Recovery UX: existem mecanismos de Heuristic, Local AI e Web AI no Planner, mas eles não estão conectados ao contexto de falha do Workbench. Portanto, um blocker estrutural/preflight/payload deixa o fluxo sem rota de correção.

Vou implementar uma Correction Lane governada: o próximo botão continua bloqueado, mas a fase bloqueada habilita Heuristic Correction, Local AI Correction e Web AI Correction Package/Receive. A correção gera uma nova versão do plano e recarrega o Workbench; nada “força PASS” nem habilita etapa seguinte sem revalidação.

O comportamento correto agora está implementado no desenho da correção:

    real_preview_written continua sendo o único estado que habilita Validate Real Preview;

    uma fase blocked não libera a seguinte;

    o próprio campo bloqueado ganha quatro rotas: Heuristic Correction, Local AI Correction, Copy Web AI Correction Package e Receive Web AI Correction;

    cada pacote leva estágio, status, blockers, warnings, output completo, target, cadeia de evidências e o objetivo explícito “corrigir até esta fase virar PASS/ready”;

    qualquer plano corrigido recarregado invalida evidência downstream e obriga recomeçar a sequência de validação, em vez de falsificar um PASS.

Também identifiquei que Legacy Apply Source Changes é propositalmente desabilitado pelo Workbench congelado, e Rollback Last Apply pertence ao caminho legado. O caminho governado atual é Completion Review → Refactor Large Module → Rollback Journaled Transaction; vou deixar isso explícito na UI para parar de parecer uma etapa quebrada.

Perfeito. A auditoria confirmou que o problema era maior do que simplesmente “alguns botões não funcionam”.

O Workbench tinha uma lógica fail-closed parcialmente correta, mas, quando uma etapa falhava, o operador ficava preso:

Stage A
→ BLOCKED

Stage B
→ disabled

e não existia:
→ Heuristic Correction
→ Local AI Correction
→ Web AI Correction

Isso criava um dead end.

Corrigi com uma Governed Blocked-Stage Correction Lane, sem enfraquecer a sequência:

PASS anterior
→ habilita próxima fase

BLOCKED anterior
→ próxima fase continua bloqueada
→ habilita rotas de correção
→ correção produz nova versão
→ Workbench invalida evidência downstream
→ sequência precisa ser executada novamente
→ somente PASS real habilita próxima fase

Isso respeita o frozen Card Machine Canon: a máquina pode analisar e corrigir o plano, mas o módulo e os resultados duráveis continuam pertencendo ao Active Project.
ZIP

Feature ID:

architecture-review-workbench-blocked-stage-correction-lane-v1

Feature title:

Architecture Review Workbench Blocked Stage Correction Lane v1

SHA-256:

cf3aecf8741f8b5f403fc0a72220aa1686452264c59262920b26355820f823fb

1. O que a auditoria encontrou

A sequência correta é:

Load Plan
    ↓
Dependency and Scope Readiness
    ↓ PASS
Real Moved Code Preview Generator
    ↓ PASS
Validate Real Preview
    ↓ PASS
Prepare Preflight Backup Readiness
    ↓ PASS
Build Source Apply Payloads
    ↓ PASS
Completion Evidence / Review
    ↓
Refactor Large Module
    ↓
Post-Apply Validation
    ↓
Receipt

A regra agora é estrita:

DEPENDENCY READY
→ Real Preview pode avançar

REAL PREVIEW READY
→ Validate Real Preview habilitado

STRUCTURAL VALIDATION PASSED
→ Prepare Preflight Backup Readiness habilitado

PREFLIGHT READY
→ Build Source Apply Payloads habilitado

PAYLOAD READY
→ Completion Evidence habilitado

COMPLETION READY
→ governed mutation workflow

Nenhum botão seguinte é liberado por:

texto parecido com PASS
status parcial
ausência de erro explícito
resultado vazio
falha silenciosa
correção da IA ainda não validada

Ele precisa da evidência exata esperada.
2. Nova Correction Lane

Agora cada estágio técnico possui quatro possíveis rotas de correção:

Heuristic Correction

Local AI Correction

Copy Web AI Correction Package

Receive Web AI Correction

Aplicadas aos estágios:

Plan Intake

Dependency Readiness

Real Preview

Structural Validation

Preflight Backup

Source Payload

Completion Evidence

Mas os botões de correção não ficam aparecendo como ação falsa em estágios saudáveis.

A lógica é:

stage not attempted
→ correction disabled

stage PASS / ready
→ correction disabled

stage BLOCKED / FAIL
→ correction routes enabled

3. O que o Corrector recebe

Esse era um ponto essencial da sua ideia, e foi implementado explicitamente.

A IA ou Heuristic Corrector não recebe apenas:

"there is an error, fix it"

Ela recebe um contexto estruturado:

ACTIVE PROJECT ROOT

TARGET MODULE

FAILED STAGE

CURRENT STATUS

BLOCKERS

WARNINGS

FULL STAGE OUTPUT

ERROR CONTEXT

UPSTREAM EVIDENCE CHAIN

CURRENT PLAN CONTEXT

EXACT NEXT-PHASE GOAL

CORRECTION OBJECTIVE

Em termos conceituais:

CURRENT STAGE:
Structural Validation

STATUS:
blocked

TARGET:
<active_project_root>/path/to/target.py

BLOCKERS:
- unresolved import migration
- public facade ownership mismatch

WARNINGS:
...

FULL FAILURE OUTPUT:
...

EVIDENCE CHAIN:
Dependency Readiness = PASS
Real Preview = READY
Structural Validation = BLOCKED
Preflight = NOT AUTHORIZED
Payload = NOT BUILT

OBJECTIVE:
Produce a bounded correction that,
after deterministic revalidation,
allows Structural Validation to become PASS.

DO NOT:
force-enable Preflight
synthesize PASS evidence
skip Preview
skip Structural Validation
write source directly
bypass transaction or Freeze governance

Esse é exatamente o contrato:

erro
+
contexto do erro
+
estado anterior
+
alvo
+
evidência
+
objetivo de saída
=
correction request

4. Heuristic Correction

O fluxo é:

Blocked Workbench Stage
    ↓
Heuristic Correction
    ↓
read current project-owned target source
    ↓
AST analysis
    ↓
rebuild Planner candidate
    ↓
regenerate bounded plan/docstrings
    ↓
store Heuristic version
    ↓
select Heuristic version
    ↓
reload through public Planner → Workbench handoff
    ↓
invalidate downstream evidence
    ↓
rerun Dependency Readiness

Importante:

Heuristic Correction
≠ writing source directly

Ela corrige a proposta/plano.

A fonte do projeto só muda posteriormente pelo caminho governado.
5. Local AI Correction

O Local AI recebe o erro real da fase.

Fluxo:

Blocked stage
    ↓
Local AI Correction
    ↓
exact Workbench failure context
    ↓
current plan
    ↓
target analysis
    ↓
bounded correction request
    ↓
Local AI candidate
    ↓
store Local AI version
    ↓
select version
    ↓
public Workbench reload
    ↓
downstream evidence invalidated
    ↓
rerun validation chain

Também corrigi uma questão importante de UI:

Local AI generation
→ background worker

GUI update
→ GUI thread

Portanto o trabalho pesado não deve ficar executando diretamente na GUI thread.
6. Web AI Correction

O fluxo é:

Blocked stage
    ↓
Copy Web AI Correction Package

O pacote contém:

Planner context
target context
blocked stage
status
blockers
warnings
full output
evidence chain
correction objective
blocked Workbench plan

Depois:

external Web AI
    ↓
solution
    ↓
Receive Web AI Correction
    ↓
governed imported-plan contract
    ↓
human review
    ↓
accepted Web AI version
    ↓
select Web AI version
    ↓
reload Workbench
    ↓
invalidate downstream evidence
    ↓
rerun sequence

A IA web não recebe autoridade para:

write source
force button enablement
change validation status
mark blocker resolved
bypass Preview
bypass Preflight
bypass Shadow
bypass transaction
bypass Freeze

7. O ponto mais importante: correção não significa PASS

A nova regra é:

AI says "fixed"
≠ PASS

A regra real é:

correction candidate generated
    ↓
candidate loaded
    ↓
old downstream evidence invalidated
    ↓
Dependency Readiness rerun
    ↓
Preview rerun
    ↓
Structural Validation rerun
    ↓
Preflight rerun
    ↓
Payload rebuilt

Somente a nova evidência produzida pela máquina governa a progressão.

O validator confirma explicitamente:

CORRECTION_ROUTES_DO_NOT_FORCE_ENABLE_NEXT_STAGE: PASS

8. Sobre Legacy Apply Source Changes

Esse botão:

Legacy Apply Source Changes (Disabled)

não estava quebrado.

Ele está desabilitado propositalmente pela arquitetura atual.

O fluxo governado é:

Completion Review
    ↓
Refactor Large Module
    ↓
Journaled Transaction
    ↓
Post-Apply Validation

E para recuperação:

Rollback Journaled Transaction

Portanto, agora a UI explica explicitamente:

Governed mutation path:
Completion Review
→ Refactor Large Module
→ Rollback Journaled Transaction.

Legacy direct apply remains disabled by design.

9. Sobre Rollback Last Apply

Também havia uma confusão de UX.

Rollback Last Apply pertence ao caminho legado:

Legacy Apply
→ Legacy Rollback Last Apply

Mas o fluxo atual é:

Refactor Large Module
→ journaled transaction
→ Rollback Journaled Transaction

Por isso o antigo rollback parecia “não funcionar”: o apply legado necessário para habilitá-lo é propositalmente impossível no fluxo governado atual.

Preservei o botão para compatibilidade e regressões congeladas, mas a UI agora diferencia claramente:

Legacy Apply Source Changes
→ compatibility control
→ disabled by design

Rollback Last Apply
→ legacy recovery only

Rollback Journaled Transaction
→ current governed recovery path

10. Validação já realizada

O ZIP passou:

ZIP CONTRACT: PASS

Com:

error_memory_lesson_blocks_checked: 1
root_freeze_hint: true

Os scripts passaram guard estrutural:

INSTALL.ps1_STATIC_PARSE_GUARD: PASS
VALIDATE.ps1_STATIC_PARSE_GUARD: PASS

O payload exato do ZIP passou:

REAL_PREVIEW_READY_ENABLES_VALIDATE_REAL_PREVIEW: PASS

BLOCKED_STAGE_EXPOSES_CORRECTION_CONTEXT: PASS

CORRECTION_PROMPT_INCLUDES_ERROR_CONTEXT_AND_PASS_GOAL: PASS

READY_STAGE_HIDES_CORRECTION_ROUTES: PASS

HEURISTIC_CORRECTION_REBUILDS_AND_RELOADS_PLAN: PASS

LOCAL_AI_RECEIVES_EXACT_BLOCKER_CONTEXT: PASS

WEB_AI_CORRECTION_PACKAGE_CONTAINS_WORKBENCH_FAILURE_CONTEXT: PASS

WEB_AI_RECEIVE_RELOADS_ACCEPTED_VERSION: PASS

CORRECTION_ROUTES_DO_NOT_FORCE_ENABLE_NEXT_STAGE: PASS

LEGACY_APPLY_ROLLBACK_EXPLAINED_AS_NON_SEQUENTIAL: PASS

TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS

WORKBENCH_BLOCKED_STAGE_CORRECTION_LANE: PASS

VALIDATION OK:
architecture-review-workbench-blocked-stage-correction-lane-v1

STATUS: IN_SYNC

Compilação:

EXACT_RELEASE_COMPILE: PASS

E KPR-12-001 continuou válido:

VALIDATION OK:
project-tool-boundary-canon-v1

BOUNDARY_CANON:
tool and selected project identities remain separate

PATH_RESOLUTION:
selected project support roots are external and dynamic

STATUS: IN_SYNC

Limitação honesta

No sandbox, algumas regressões históricas completas não podem ser executadas porque o source archive disponível aqui omite arquivos conhecidos, especialmente módulos cujo basename contém backup, além de algumas features instaladas posteriormente.

Por isso, não estou declarando essas regressões como PASS no sandbox.

O VALIDATE.ps1 do pacote executa no seu projeto Windows completo:

Focused Correction Lane
↓
Workbench GUI Progression
↓
Architecture Review Card Lifecycle
↓
KPR-12-005 Card Machine Canon
↓
KPR-12-001 Tool/Project Boundary
↓
Workbench Project Support Boundary v3
↓
Patch 4 Completion GUI Gate
↓
Compile
↓
Freeze Evidence Merge
↓
Error Memory check

Não há alegação de que os erros globais de Architecture Validation preexistentes foram corrigidos.
ZIP → INSTALL

Feche o KANDA GUI.

Coloque:

E:\kanda_architecture_review_workbench_blocked_stage_correction_lane_v1.zip

Execute:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = `
    "kanda_architecture_review_workbench_blocked_stage_correction_lane_v1.zip"

$ProjectName = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

$WORK_DIR = Join-Path `
    $DRIVE_ROOT `
    ($ProjectName + "_delete_after_daily_work")

$ROOT_ZIP = Join-Path `
    $DRIVE_ROOT `
    $PATCH_NAME

$WORK_ZIP = Join-Path `
    $WORK_DIR `
    $PATCH_NAME

$BOOTSTRAP_ROOT = Join-Path `
    $WORK_DIR `
    "kanda_architecture_review_workbench_blocked_stage_correction_lane_v1_bootstrap"

try {
    New-Item `
        -ItemType Directory `
        -Force `
        -Path $WORK_DIR | Out-Null

    if (Test-Path -LiteralPath $ROOT_ZIP -PathType Leaf) {

        Copy-Item `
            -LiteralPath $ROOT_ZIP `
            -Destination $WORK_ZIP `
            -Force

        if (-not (Test-Path -LiteralPath $WORK_ZIP -PathType Leaf)) {
            throw "ZIP staging failed: $WORK_ZIP"
        }

        Remove-Item `
            -LiteralPath $ROOT_ZIP `
            -Force
    }
    elseif (-not (Test-Path -LiteralPath $WORK_ZIP -PathType Leaf)) {

        throw @"
Patch ZIP not found.

Expected:
$ROOT_ZIP

or staged:
$WORK_ZIP
"@
    }

    Remove-Item `
        -LiteralPath $BOOTSTRAP_ROOT `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue

    Expand-Archive `
        -LiteralPath $WORK_ZIP `
        -DestinationPath $BOOTSTRAP_ROOT `
        -Force

    $INSTALL = Join-Path `
        $BOOTSTRAP_ROOT `
        "INSTALL.ps1"

    if (-not (Test-Path -LiteralPath $INSTALL -PathType Leaf)) {
        throw "INSTALL.ps1 missing: $INSTALL"
    }

    & $INSTALL
}
catch {
    Write-Host ""
    Write-Host "INSTALL LAUNCH ERROR: $($_.Exception.Message)"
    Write-Host ""

    Read-Host "Press Enter after copying this output"
    Read-Host "Press Enter again to clear the terminal"
    Clear-Host
}

O installer deve emitir antes do terminal limpar:

INSTALL_MARKER:
ARCHITECTURE_REVIEW_WORKBENCH_BLOCKED_STAGE_CORRECTION_LANE_V1_INSTALLED

TOOL_ROOT:
E:\kanda_reasoner

ACTIVE_PROJECT_ROOT:
E:\kanda_reasoner

PRIMARY_BOX:
kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_gui.py

ERROR_MEMORY_LESSON_STAGED:
KANDA_ERROR_LESSON_JSON_workbench_blocked_stage_correction_lane_v1.txt

VALIDATE

Depois da instalação:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"

$ProjectName = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

$WORK_DIR = Join-Path `
    $DRIVE_ROOT `
    ($ProjectName + "_delete_after_daily_work")

$EXTRACT_ROOT = Join-Path `
    $WORK_DIR `
    "kanda_architecture_review_workbench_blocked_stage_correction_lane_v1_extract"

$VALIDATE = Join-Path `
    $EXTRACT_ROOT `
    "VALIDATE.ps1"

if (-not (Test-Path -LiteralPath $VALIDATE -PathType Leaf)) {
    throw "VALIDATE.ps1 not found: $VALIDATE"
}

& $VALIDATE

O final precisa chegar a:

FREEZE_HINT_EVIDENCE_MERGE_OK:
architecture-review-workbench-blocked-stage-correction-lane-v1

ERROR_MEMORY_PENDING_INTAKE_OK:
KANDA_ERROR_LESSON_JSON_workbench_blocked_stage_correction_lane_v1.txt

ARCHITECTURE_REVIEW_WORKBENCH_BLOCKED_STAGE_CORRECTION_LANE_V1_VALIDATION_OK

Não faça Freeze se um validator anterior falhar, mesmo que algum marcador parcial apareça.
ERROR MEMORY

Após Validation PASS:

Error Memory
→ Pending AI-assisted Error Lesson Intake

Selecione:

KANDA_ERROR_LESSON_JSON_workbench_blocked_stage_correction_lane_v1.txt

Depois:

Review
→ Memorize Error

Princípio central:

Never leave a blocked governed Workbench stage
with only disabled downstream controls.

Expose exact-context correction routes.

But never:
force-enable downstream stages
synthesize PASS
skip validation

Accepted correction
→ reload governed plan
→ invalidate downstream evidence
→ deterministic sequential revalidation

FREEZE

Depois:

VALIDATION PASS
+
ERROR MEMORY MEMORIZED

Use:

Freeze Feature After Update
→ New Local Freeze Entry
→ Preview

Feature ID

architecture-review-workbench-blocked-stage-correction-lane-v1

Feature title

Architecture Review Workbench Blocked Stage Correction Lane v1

Primary box

kanda_reasoner_app/manage_architecture/
large_file_refactor_planner/
workbench_stage_correction_gui.py

Box type

Large File Refactor Workbench fail-closed stage correction routing

Summary para revisar

The Large File Refactor Workbench preserves strict sequential fail-closed progression while adding a governed recovery route for blocked stages. A downstream phase is enabled only after exact ready/PASS evidence from the preceding phase. When a technical stage has attempted evidence and remains blocked, the Workbench exposes Heuristic Correction, Local AI Correction, Copy Web AI Correction Package, and Receive Web AI Correction routes. Correction requests contain Active Project root, project-owned target module, stage, status, blockers, warnings, stage output, evidence-chain statuses, and the exact next-phase PASS objective. Corrections never force-enable downstream controls or synthesize PASS. Accepted corrections reload a governed plan through the public Planner-to-Workbench handoff, invalidate downstream evidence, and require deterministic sequential revalidation. Legacy Apply Source Changes remains disabled by design; the governed mutation and recovery path remains Completion Review -> Refactor Large Module -> Rollback Journaled Transaction.

Do-not-regress

Every sequential Workbench phase enables the next phase only after exact ready/PASS evidence.

A blocked technical stage must expose:
Heuristic Correction,
Local AI Correction,
Copy Web AI Correction Package,
and Receive Web AI Correction.

Every correction request must include:
Active Project root,
target module,
stage,
status,
blockers,
warnings,
full stage output,
evidence-chain status,
and exact PASS objective.

Correction routes must never force-enable downstream controls.

Correction routes must never synthesize PASS evidence.

Heuristic Correction rebuilds from current project-owned source and reloads through the public Planner-to-Workbench handoff.

Local AI receives the exact blocker context and remains bounded to Planner correction.

Web AI uses the governed imported-plan artifact contract and requires human review.

Accepted corrections invalidate downstream evidence and require sequential rerun.

Legacy Apply Source Changes remains disabled by design.

The governed mutation path remains:
Completion Review
-> Refactor Large Module
-> Rollback Journaled Transaction.

KPR-12-005 Architecture Review Card Machine Canon remains authoritative.

KPR-12-001 Tool/Project Boundary remains authoritative.

Depois:

Preview
→ review evidence
→ review protected paths
→ Confirm and Write

Agora a arquitetura não fica mais entre duas opções ruins:

FAIL
→ stuck forever

ou:

FAIL
→ force next button

O novo contrato é:

FAIL
→ exact failure context
→ governed correction route
→ corrected candidate
→ invalidate stale evidence
→ deterministic revalidation
→ real PASS
→ next phase enabled

Esse é o comportamento correto para o Workbench.

KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_BEGIN
Title: Last frozen feature entry
Project root: E:\kanda_reasoner
Entry count: 1
Instruction: Use this as read-only frozen feature memory. Do not edit these entries directly. Do not write project-specific memory into project_freeze_ledger.

--- FROZEN ENTRY 1 OF 1 ---
Path: E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update\frozen_features_memory\entries\freeze-20260706-architecture-review-workbench-blocked-stage-correction-lane-v1.md

---
freeze_id: "freeze-20260706-architecture-review-workbench-blocked-stage-correction-lane-v1"
feature_title: "Architecture Review Workbench Blocked Stage Correction Lane v1"
box: "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_gui.py"
status: "frozen"
date: "2026-07-06"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260706-architecture-review-workbench-blocked-stage-correction-lane-v1.md"
protected_paths:
  - "<tool_source_root>"
  - "<active_project_root>"
  - "<project_drive>/<active_project_slug>_show_project_to_AI/project_error_memory"
  - "<project_drive>/<active_project_slug>_show_project_to_AI/project_freeze_after_update"
  - "<active_project_support_root>/large_file_refactor_workbench"
  - "<active_project_daily_work_root>/large_file_refactor_shadow"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Every sequential Workbench phase must enable the next phase only after its exact ready/PASS evidence is present."
  - "A blocked technical stage must expose Heuristic Correction, Local AI Correction, Copy Web AI Correction Package, and Receive Web AI Correction routes instead of leaving the operator with only disabled downstream buttons."
  - "Every correction request must include Active Project root, target module, stage, status, blockers, warnings, stage error output, evidence-chain statuses, and the exact next-phase PASS objective."
  - "Correction routes must never force-enable a downstream button or synthesize PASS evidence."
  - "Heuristic correction must rebuild from current project-owned source and reload through the public Planner-to-Workbench handoff."
  - "Local AI correction must receive the exact blocker context, remain bounded to Planner correction, and return a candidate that is deterministically revalidated."
  - "Web AI correction must use the governed imported-plan artifact contract and human review before loading the imported version."
  - "Any accepted correction must invalidate downstream Workbench evidence and require sequential rerun from Dependency Readiness onward."
  - "Legacy Apply Source Changes remains disabled by design. The governed mutation path is Completion Review -> Refactor Large Module -> Rollback Journaled Transaction."
  - "KPR-12-005 Architecture Review Project Card Machine Canon and KPR-12-001 Tool/Project boundary remain authoritative."
  - "Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260706-architecture-review-workbench-blocked-stage-correction-lane-v1

## freeze identity

Freeze ID: freeze-20260706-architecture-review-workbench-blocked-stage-correction-lane-v1

Feature title: Architecture Review Workbench Blocked Stage Correction Lane v1

Date: 2026-07-06

Primary box: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_gui.py

Box type: Large File Refactor Workbench fail-closed stage correction routing

Status: frozen after explicit human confirmation and validation evidence

## summary

Audit found that sequential fail-closed enablement was conceptually correct, but blocked stages had no recovery route. The correction lane connects exact Workbench failure context to deterministic Heuristic rebuild, bounded Local AI correction, and governed Web AI exchange/receive without bypassing any gate. Legacy direct apply/rollback are clarified as non-sequential compatibility controls. Freeze-intake data was loaded from <project>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake. Source patch ZIP: kanda_architecture_review_workbench_blocked_stage_correction_lane_v1.zip.

## validated files

- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui.py
- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_gui.py
- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_context.py
- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_service.py
- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_gui.py
- tools/validate_workbench_blocked_stage_correction_lane_v1.py

## generated files

- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_context.py
- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_service.py
- kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_gui.py
- tools/validate_workbench_blocked_stage_correction_lane_v1.py
- KANDA_ERROR_LESSON_JSON_workbench_blocked_stage_correction_lane_v1.txt

## protected paths

- <tool_source_root>
- <active_project_root>
- <project_drive>/<active_project_slug>_show_project_to_AI/project_error_memory
- <project_drive>/<active_project_slug>_show_project_to_AI/project_freeze_after_update
- <active_project_support_root>/large_file_refactor_workbench
- <active_project_daily_work_root>/large_file_refactor_shadow
- project_freeze_after_update/frozen_features_memory

## do-not-regress rules

- Every sequential Workbench phase must enable the next phase only after its exact ready/PASS evidence is present.
- A blocked technical stage must expose Heuristic Correction, Local AI Correction, Copy Web AI Correction Package, and Receive Web AI Correction routes instead of leaving the operator with only disabled downstream buttons.
- Every correction request must include Active Project root, target module, stage, status, blockers, warnings, stage error output, evidence-chain statuses, and the exact next-phase PASS objective.
- Correction routes must never force-enable a downstream button or synthesize PASS evidence.
- Heuristic correction must rebuild from current project-owned source and reload through the public Planner-to-Workbench handoff.
- Local AI correction must receive the exact blocker context, remain bounded to Planner correction, and return a candidate that is deterministically revalidated.
- Web AI correction must use the governed imported-plan artifact contract and human review before loading the imported version.
- Any accepted correction must invalidate downstream Workbench evidence and require sequential rerun from Dependency Readiness onward.
- Legacy Apply Source Changes remains disabled by design. The governed mutation path is Completion Review -> Refactor Large Module -> Rollback Journaled Transaction.
- KPR-12-005 Architecture Review Project Card Machine Canon and KPR-12-001 Tool/Project boundary remain authoritative.
- Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.
- Do not store project-specific frozen memory inside project_freeze_ledger.
- Preview Freeze Entry must remain read-only and must not write files.
- Confirm and Write must require explicit human confirmation before writing governed freeze memory.
- After a local freeze write, the AI startup freeze context must be refreshed.
- External AI review remains advanced/fallback, not the normal local freeze path.

## validation evidence

text
Focused validation must prove Real Preview readiness enables Structural Validation, blocked stages expose exact correction context and PASS objective, Heuristic/Local AI/Web AI routes are wired, accepted corrections reload through Workbench ownership, correction routes never force-enable downstream stages, legacy mutation path guidance is explicit, touched modules remain at or below 500 lines, and STATUS: IN_SYNC.



## known warnings

Global Architecture Validation may report unrelated pre-existing errors. This patch must not claim the global baseline is clean. Freeze readiness is based on focused correction-lane validation plus relevant progression, card lifecycle, card-machine canon, Tool/Project boundary, Workbench Project Support Boundary, and compile regressions. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Architecture Review Workbench Blocked Stage Correction Lane v1. Human review is still required before Confirm and Write.

## planned next step

Install with KANDA GUI closed, run packaged validation, review and Memorize the pending Error Memory lesson, then Preview and Confirm and Write a separate freeze entry.

## local freeze writer provenance

Generated by 
local_freeze_writer_engine_v1 at 2026-07-06T14:30:51Z.

This entry was created locally for the selected active project. The reusable project_freeze_ledger engine remains blueprint logic only and is not the owner of this project-specific memory.

KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_END

Perfeito. A feature agora está formalmente congelada:

freeze-20260706-architecture-review-workbench-blocked-stage-correction-lane-v1

O contrato protegido ficou claro:

PASS real
→ habilita próxima fase

BLOCKED / FAIL
→ próxima fase continua bloqueada
→ Correction Lane fica disponível

Correction Lane
→ Heuristic
→ Local AI
→ Web AI package
→ Web AI receive

correção aceita
→ recarrega plano governado
→ invalida evidência downstream
→ reexecuta sequência
→ somente novo PASS real libera a próxima fase

Também ficou congelado que:

correction
≠ force enable
≠ synthetic PASS
≠ bypass de validação

e que o fluxo de mutação permanece:

Completion Review
→ Refactor Large Module
→ Journaled Transaction
→ Post-Apply Validation
→ Receipt

com rollback governado por:

Rollback Journaled Transaction

enquanto:

Legacy Apply Source Changes

continua desabilitado por design.

A hierarquia canônica agora está bem definida:

KPR-12-001
→ Tool vs Active Project ownership

KPR-12-005
→ Architecture Review card-machine lifecycle

Blocked Stage Correction Lane v1
→ recovery path para fases bloqueadas do Workbench

Qualquer correção futura nessa área deve preservar esses três níveis ao mesmo tempo.

when press button  heurist  Correction , gui freezes eternally in generate real preview correctinon

Isso parece um bloqueio de GUI thread: o Heuristic Correction provavelmente está executando rebuild/preview de forma síncrona no callback do botão. Vou rastrear o handler e mover o trabalho pesado para worker thread, mantendo toda atualização de UI no thread principal e preservando os freezes da Correction Lane.

Achei a causa exata: Heuristic Correction executa analyze_python_file → build_split_plan → docstring proposals → reload Workbench diretamente no callback Qt. Diferente do Local AI, ele não usa worker thread. Vou separar em build candidate off-GUI-thread + apply candidate on GUI thread, adicionar estado de execução e watchdog para que a interface nunca fique eternamente travada mesmo se o cálculo não retornar.

O freeze anterior continua preservado: a Correction Lane permanece fail-closed e nenhuma etapa seguinte é habilitada artificialmente. A correção agora só muda o modo de execução do Heuristic route: cálculo pesado fora da GUI thread; aplicação do candidate e reload do Workbench de volta no GUI thread. O validator anterior da Correction Lane já continua passando após a mudança.

Found and corrected. The freeze was real.
Root cause

Heuristic Correction was doing this directly inside the Qt button callback:

click Heuristic Correction
→ analyze_python_file(...)
→ build_split_plan(...)
→ build_docstring_proposals(...)
→ store Heuristic version
→ reload Workbench
→ return control to Qt event loop

So the GUI event loop could not repaint or process clicks while the correction was being generated.

The corrected flow is:

click Heuristic Correction
        ↓
capture immutable correction context
        ↓
WORKER THREAD
├── analyze project-owned target
├── build split plan
├── generate docstring proposals
└── return candidate
        ↓
QTimer polls result queue
        ↓
GUI THREAD
├── store Heuristic version
├── select version
├── reload Workbench
├── invalidate downstream evidence
├── render result
└── refresh buttons

I also added a watchdog:

Heuristic running > 180 seconds
→ stop GUI waiting state
→ do NOT create PASS
→ do NOT enable next stage
→ disable Heuristic retry for that stage during the session
→ keep Local AI available
→ keep Web AI available

ZIP

Feature ID:

architecture-review-workbench-heuristic-correction-async-gui-v1

Feature title:

Architecture Review Workbench Heuristic Correction Async GUI v1

SHA-256:

c8e8a76c05d5b2c72f28ba25f1832f4179cc68f5cfb3c4b73e7527bec8d84aae

The exact ZIP passed:

ZIP CONTRACT: PASS

Exact release overlay passed:

HEURISTIC_HEAVY_BUILD_OFF_GUI_THREAD: PASS
HEURISTIC_CANDIDATE_BUILD_APPLY_SPLIT: PASS
HEURISTIC_GUI_APPLY_POLLED_ON_QT_TIMER: PASS
HEURISTIC_RUNNING_STATE_DISABLING: PASS
HEURISTIC_TIMEOUT_ESCAPE_ROUTE: PASS
LOCAL_AI_AND_WEB_AI_REMAIN_RECOVERY_ROUTES: PASS
HEURISTIC_ASYNC_DOES_NOT_FORCE_PASS: PASS
TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS
WORKBENCH_HEURISTIC_CORRECTION_ASYNC_GUI: PASS

VALIDATION OK:
architecture-review-workbench-heuristic-correction-async-gui-v1

STATUS: IN_SYNC

The frozen Correction Lane regression also remained valid:

WORKBENCH_BLOCKED_STAGE_CORRECTION_LANE: PASS

VALIDATION OK:
architecture-review-workbench-blocked-stage-correction-lane-v1

STATUS: IN_SYNC

And KPR-12-001 remained valid:

VALIDATION OK: project-tool-boundary-canon-v1
STATUS: IN_SYNC

1. INSTALL

Close KANDA GUI.

Place the ZIP at:

E:\kanda_architecture_review_workbench_heuristic_correction_async_gui_v1.zip

Run:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = `
    "kanda_architecture_review_workbench_heuristic_correction_async_gui_v1.zip"

$ProjectName = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

$WORK_DIR = Join-Path `
    $DRIVE_ROOT `
    ($ProjectName + "_delete_after_daily_work")

$ROOT_ZIP = Join-Path `
    $DRIVE_ROOT `
    $PATCH_NAME

$WORK_ZIP = Join-Path `
    $WORK_DIR `
    $PATCH_NAME

$BOOTSTRAP_ROOT = Join-Path `
    $WORK_DIR `
    "kanda_architecture_review_workbench_heuristic_correction_async_gui_v1_bootstrap"

try {
    New-Item `
        -ItemType Directory `
        -Force `
        -Path $WORK_DIR | Out-Null

    if (Test-Path -LiteralPath $ROOT_ZIP -PathType Leaf) {

        Copy-Item `
            -LiteralPath $ROOT_ZIP `
            -Destination $WORK_ZIP `
            -Force

        if (-not (Test-Path -LiteralPath $WORK_ZIP -PathType Leaf)) {
            throw "ZIP staging failed: $WORK_ZIP"
        }

        Remove-Item `
            -LiteralPath $ROOT_ZIP `
            -Force
    }
    elseif (-not (Test-Path -LiteralPath $WORK_ZIP -PathType Leaf)) {

        throw @"
Patch ZIP not found.

Expected:
$ROOT_ZIP

or already staged:
$WORK_ZIP
"@
    }

    Remove-Item `
        -LiteralPath $BOOTSTRAP_ROOT `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue

    Expand-Archive `
        -LiteralPath $WORK_ZIP `
        -DestinationPath $BOOTSTRAP_ROOT `
        -Force

    $INSTALL = Join-Path `
        $BOOTSTRAP_ROOT `
        "INSTALL.ps1"

    if (-not (Test-Path -LiteralPath $INSTALL -PathType Leaf)) {
        throw "INSTALL.ps1 missing: $INSTALL"
    }

    & $INSTALL
}
catch {
    Write-Host ""
    Write-Host "INSTALL LAUNCH ERROR: $($_.Exception.Message)"
    Write-Host ""

    Read-Host "Press Enter after copying this output"
    Read-Host "Press Enter again to clear the terminal"
    Clear-Host
}

Expected installation marker:

INSTALL_MARKER:
ARCHITECTURE_REVIEW_WORKBENCH_HEURISTIC_CORRECTION_ASYNC_GUI_V1_INSTALLED

2. VALIDATE

Run:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"

$ProjectName = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

$WORK_DIR = Join-Path `
    $DRIVE_ROOT `
    ($ProjectName + "_delete_after_daily_work")

$EXTRACT_ROOT = Join-Path `
    $WORK_DIR `
    "kanda_architecture_review_workbench_heuristic_correction_async_gui_v1_extract"

$VALIDATE = Join-Path `
    $EXTRACT_ROOT `
    "VALIDATE.ps1"

if (-not (Test-Path -LiteralPath $VALIDATE -PathType Leaf)) {
    throw "VALIDATE.ps1 not found: $VALIDATE"
}

& $VALIDATE

The validation chain runs:

ZIP contract
↓
Async Heuristic focused validator
↓
Frozen Blocked Stage Correction Lane regression
↓
Workbench GUI progression regression
↓
Architecture Review card lifecycle regression
↓
KPR-12-005 card-machine canon regression
↓
KPR-12-001 Tool/Project boundary regression
↓
compile checks
↓
freeze evidence merge
↓
Error Memory intake verification

The end must reach:

FREEZE_HINT_EVIDENCE_MERGE_OK:
architecture-review-workbench-heuristic-correction-async-gui-v1

ERROR_MEMORY_PENDING_INTAKE_OK:
KANDA_ERROR_LESSON_JSON_workbench_heuristic_correction_async_gui_v1.txt

ARCHITECTURE_REVIEW_WORKBENCH_HEURISTIC_CORRECTION_ASYNC_GUI_V1_VALIDATION_OK

3. ERROR MEMORY

After full validation PASS:

Error Memory
→ Pending AI-assisted Error Lesson Intake

Select:

KANDA_ERROR_LESSON_JSON_workbench_heuristic_correction_async_gui_v1.txt

Then:

Review
→ Memorize Error

The principle is:

Never execute heavy Heuristic correction work
inside a Qt button callback.

Worker thread:
→ source analysis
→ split-plan construction
→ docstring proposal generation
→ candidate creation

GUI thread:
→ store version
→ select version
→ reload Workbench
→ render result
→ synchronize controls

Timeout:
→ release GUI waiting state
→ preserve fail-closed gates
→ keep Local AI/Web AI recovery available

4. FREEZE

After:

VALIDATION PASS
+
ERROR MEMORY MEMORIZED

Use:

Freeze Feature After Update
→ New Local Freeze Entry
→ Preview

Verify:
Feature ID

architecture-review-workbench-heuristic-correction-async-gui-v1

Feature title

Architecture Review Workbench Heuristic Correction Async GUI v1

Primary box

kanda_reasoner_app/manage_architecture/
large_file_refactor_planner/
workbench_stage_correction_gui.py

Box type

Large File Refactor Workbench correction execution thread ownership

Summary

Heuristic Correction no longer performs source analysis, split-plan construction, and docstring proposal generation synchronously inside the Qt clicked callback. Heavy deterministic candidate generation runs in a daemon worker thread. A QTimer polls a thread-safe result queue, and only the GUI-thread apply path mutates Planner version state, selects the Heuristic version, reloads Workbench ownership, renders output, and synchronizes controls. The Correction Lane remains fail-closed: async execution never force-enables a downstream phase or synthesizes PASS evidence. A 180-second watchdog releases the GUI waiting state if the Heuristic worker does not return, disables Heuristic retry for that stage during the current session, and preserves Local AI and Web AI recovery routes.

Do-not-regress

Heuristic Correction heavy candidate generation must never run synchronously inside a Qt clicked callback.

Source analysis, split-plan construction, and docstring proposal generation must run off the GUI thread.

Planner version storage, version selection, Workbench reload, result rendering, and control synchronization belong to the GUI-thread apply path.

A running-state guard must prevent duplicate correction launches.

The GUI must remain responsive while Heuristic Correction runs.

A Heuristic timeout must never synthesize PASS evidence.

A Heuristic timeout must never enable the next Workbench stage.

After timeout, Local AI and Web AI recovery routes must remain available.

Accepted corrections must continue invalidating downstream evidence.

Sequential deterministic revalidation remains mandatory.

The frozen Blocked Stage Correction Lane v1 remains authoritative.

KPR-12-005 remains the Architecture Review card-machine lifecycle owner.

KPR-12-001 remains the general Tool/Project boundary owner.

Then:

Preview
→ review evidence
→ Confirm and Write

The key correction is now:

BEFORE

button click
→ heavy rebuild on GUI thread
→ Qt event loop starved
→ GUI appears frozen forever

NOW

button click
→ worker thread performs heavy rebuild
→ GUI remains responsive
→ QTimer receives candidate
→ GUI thread applies candidate
→ deterministic rerun required

And if the Heuristic path itself truly stalls:

180-second watchdog
→ escape waiting state
→ no fake PASS
→ no next-stage enablement
→ Local AI/Web AI remain available


