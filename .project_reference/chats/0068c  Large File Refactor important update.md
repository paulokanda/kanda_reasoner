
ChatGPT Plus

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

Esse erro significa que a feature ainda não foi instalada no Tool root. Vou conferir o ZIP e o INSTALL.ps1 real para te passar o fluxo correto de stage → extract → install → validate, sem repetir o erro anterior de validar antes da instalação.

Confirmei o pacote: o validator existe no ZIP, mas o INSTALL.ps1 é quem o copia para E:\kanda_reasoner\tools. Então o caminho correto agora é instalar primeiro e validar em seguida. Vou te dar um bloco único que faz isso sem pular etapas.

O erro agora é simples: o patch do prompt/router bridge não foi instalado. O validator existe dentro do ZIP, mas ainda não foi copiado para:

E:\kanda_reasoner\tools\
validate_project_tool_boundary_workbench_preview_router_bridge_v1.py

O log mostra exatamente que a checagem de pré-validação parou nesse ponto, antes de executar o validator.

Use o fluxo abaixo. Ele aceita o ZIP tanto em E:\ quanto já staged no daily-work, instala e depois valida.

Coloque em E:\ caso o ZIP não esteja mais staged.

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = `
    "kanda_project_tool_boundary_workbench_preview_router_bridge_v1.zip"

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
    "kanda_project_tool_boundary_workbench_preview_router_bridge_v1_bootstrap"

$EXTRACT_ROOT = Join-Path `
    $WORK_DIR `
    "kanda_project_tool_boundary_workbench_preview_router_bridge_v1_extract"

$INSTALLED_VALIDATOR = Join-Path `
    $PROJECT_ROOT `
    "tools\validate_project_tool_boundary_workbench_preview_router_bridge_v1.py"

try {
    New-Item `
        -ItemType Directory `
        -Force `
        -Path $WORK_DIR | Out-Null

    # ------------------------------------------------------------
    # 1. Stage ZIP
    # ------------------------------------------------------------

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

Expected one of:
$ROOT_ZIP
$WORK_ZIP
"@
    }

    Write-Host ""
    Write-Host "PATCH ZIP STAGED: PASS"
    Write-Host ""

    # ------------------------------------------------------------
    # 2. Bootstrap extraction
    # ------------------------------------------------------------

    Remove-Item `
        -LiteralPath $BOOTSTRAP_ROOT `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue

    Expand-Archive `
        -LiteralPath $WORK_ZIP `
        -DestinationPath $BOOTSTRAP_ROOT `
        -Force

    $INSTALL_SCRIPT = Join-Path `
        $BOOTSTRAP_ROOT `
        "INSTALL.ps1"

    if (-not (Test-Path -LiteralPath $INSTALL_SCRIPT -PathType Leaf)) {
        throw "INSTALL.ps1 missing: $INSTALL_SCRIPT"
    }

    # ------------------------------------------------------------
    # 3. Install
    # ------------------------------------------------------------

    Write-Host "STARTING INSTALL"
    Write-Host ""

    & $INSTALL_SCRIPT

    # ------------------------------------------------------------
    # 4. Confirm installation
    # ------------------------------------------------------------

    if (-not (Test-Path -LiteralPath $INSTALLED_VALIDATOR -PathType Leaf)) {
        throw @"
Install did not place the validator at:

$INSTALLED_VALIDATOR
"@
    }

    Write-Host ""
    Write-Host "INSTALLED VALIDATOR: PASS"
    Write-Host ""

    # ------------------------------------------------------------
    # 5. Validate
    # ------------------------------------------------------------

    $VALIDATE_SCRIPT = Join-Path `
        $EXTRACT_ROOT `
        "VALIDATE.ps1"

    if (-not (Test-Path -LiteralPath $VALIDATE_SCRIPT -PathType Leaf)) {
        throw "VALIDATE.ps1 missing after install: $VALIDATE_SCRIPT"
    }

    Write-Host "STARTING FULL VALIDATION"
    Write-Host ""

    & $VALIDATE_SCRIPT
}
catch {
    Write-Host ""
    Write-Host "INSTALL OR VALIDATION ERROR: $($_.Exception.Message)"
    Write-Host ""

    Read-Host "Press Enter after copying this output"
    Read-Host "Press Enter again to clear the terminal"
    Clear-Host
}

O resultado correto

Na instalação, antes do terminal limpar, o pacote deve executar a instalação da feature e colocar o validator no Tool root.

Depois, a validação deve mostrar:

PROJECT_TOOL_BOUNDARY_CANON_WORKBENCH_OWNERSHIP: PASS

ROUTER_BRIDGE_WORKBENCH_OWNERSHIP_GATE: PASS

PROMPT_ROUTER_WORKBENCH_BOUNDARY_ROUTE: PASS

ROUTING_METADATA_AND_INDEX_SYNC: PASS

NO_COMPETING_PROJECT_TOOL_BOUNDARY_PROMPT: PASS

VALIDATION OK:
project-tool-boundary-workbench-preview-router-bridge-v1

STATUS: IN_SYNC

Depois:

VALIDATION OK:
project-tool-boundary-canon-v1

e finalmente:

PROMPT_ROUTING_JSON_PARSE: PASS

ERROR_MEMORY_PENDING_INTAKE_OK:
KANDA_ERROR_LESSON_JSON_project_tool_boundary_workbench_preview_router_bridge_v1.txt

VALIDATION OK:
project-tool-boundary-workbench-preview-router-bridge-v1

STATUS: IN_SYNC

Depois desse resultado completo, a sequência é:

Error Memory
→ Review lesson
→ Memorize Error

Freeze Feature After Update
→ New Local Freeze Entry
→ Preview
→ Confirm and Write

Não cole o Frozen Feature Memory Snippet no PowerShell; ele é contexto read-only, não script.

KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_BEGIN
Title: Last frozen feature entry
Project root: E:\kanda_reasoner
Entry count: 1
Instruction: Use this as read-only frozen feature memory. Do not edit these entries directly. Do not write project-specific memory into project_freeze_ledger.

--- FROZEN ENTRY 1 OF 1 ---
Path: E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update\frozen_features_memory\entries\freeze-20260706-project-tool-boundary-workbench-preview-router-bridge-v1.md

---
freeze_id: "freeze-20260706-project-tool-boundary-workbench-preview-router-bridge-v1"
feature_title: "Project Tool Boundary Workbench Preview Router Bridge v1"
box: "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md"
status: "frozen"
date: "2026-07-06"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260706-project-tool-boundary-workbench-preview-router-bridge-v1.md"
protected_paths:
  - "<tool_source_root>"
  - "<active_project_root>"
  - "<project_drive>/<active_project_slug>_show_project_to_AI/project_error_memory"
  - "<project_drive>/<active_project_slug>_show_project_to_AI/project_freeze_after_update"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS"
  - "kanda_prompt_workspace/prompt_library/ROUTING"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Keep one stable Project Tool Boundary Canon identity: KPR-12-001 / project_tool_boundary_canon. Do not create a competing Tool-versus-Project prompt."
  - "Large File Refactor Workbench Preview is durable selected-project support state under <active_project_support_root>/large_file_refactor_workbench/preview/<preview_id>."
  - "Workbench Shadow is disposable and belongs under <active_project_daily_work_root>/large_file_refactor_shadow/<shadow_id>."
  - "Daily-work is garbage-only and must not own durable Preview truth, durable Workbench project-support state, project source, canonical Error Memory, or canonical freeze memory."
  - "The governed implementation router bridge must require project_tool_boundary_canon and explicit project support-state ownership plus Preview/Shadow classification for Workbench-related implementation."
  - "Self-hosting does not collapse Tool identity and Active Project identity even when tool_source_root and active_project_root physically coincide."
  - "NO_LEAK_LOGIC_V1 remains the named boundary object and must prevent wrong-root writes, Tool/Project leakage, cross-project leakage, Preview-to-daily-work leakage, generated-artifact-as-source leakage, and validation/freeze evidence leakage."
  - "Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260706-project-tool-boundary-workbench-preview-router-bridge-v1

## freeze identity

Freeze ID: freeze-20260706-project-tool-boundary-workbench-preview-router-bridge-v1

Feature title: Project Tool Boundary Workbench Preview Router Bridge v1

Date: 2026-07-06

Primary box: kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md

Box type: Prompt library canon and governed implementation router bridge

Status: frozen after explicit human confirmation and validation evidence

## summary

The existing KPR-12-001 canon already separated reusable KANDA Reasoner Tool identity from Active Project identity, but did not explicitly own Workbench Preview under project support, distinguish Preview from Shadow, or state daily-work garbage-only semantics. The governed router bridge also referenced the canon only generically. Freeze-intake data was loaded from <project>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake. Source patch ZIP: kanda_project_tool_boundary_workbench_preview_router_bridge_v1.zip.

## validated files

- kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md
- kanda_prompt_workspace/prompt_library/METADATA/project_tool_boundary_canon.meta.json
- kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md
- kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json
- kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md
- kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md
- kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md
- kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json
- tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py

## generated files

- tools/validate_project_tool_boundary_workbench_preview_router_bridge_v1.py
- KANDA_ERROR_LESSON_JSON_project_tool_boundary_workbench_preview_router_bridge_v1.txt

## protected paths

- <tool_source_root>
- <active_project_root>
- <project_drive>/<active_project_slug>_show_project_to_AI/project_error_memory
- <project_drive>/<active_project_slug>_show_project_to_AI/project_freeze_after_update
- kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS
- kanda_prompt_workspace/prompt_library/ROUTING
- project_freeze_after_update/frozen_features_memory

## do-not-regress rules

- Keep one stable Project Tool Boundary Canon identity: KPR-12-001 / project_tool_boundary_canon. Do not create a competing Tool-versus-Project prompt.
- Large File Refactor Workbench Preview is durable selected-project support state under <active_project_support_root>/large_file_refactor_workbench/preview/<preview_id>.
- Workbench Shadow is disposable and belongs under <active_project_daily_work_root>/large_file_refactor_shadow/<shadow_id>.
- Daily-work is garbage-only and must not own durable Preview truth, durable Workbench project-support state, project source, canonical Error Memory, or canonical freeze memory.
- The governed implementation router bridge must require project_tool_boundary_canon and explicit project support-state ownership plus Preview/Shadow classification for Workbench-related implementation.
- Self-hosting does not collapse Tool identity and Active Project identity even when tool_source_root and active_project_root physically coincide.
- NO_LEAK_LOGIC_V1 remains the named boundary object and must prevent wrong-root writes, Tool/Project leakage, cross-project leakage, Preview-to-daily-work leakage, generated-artifact-as-source leakage, and validation/freeze evidence leakage.
- Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.
- Do not store project-specific frozen memory inside project_freeze_ledger.
- Preview Freeze Entry must remain read-only and must not write files.
- Confirm and Write must require explicit human confirmation before writing governed freeze memory.
- After a local freeze write, the AI startup freeze context must be refreshed.
- External AI review remains advanced/fallback, not the normal local freeze path.

## validation evidence

text
Focused validation must prove Workbench Preview ownership in KPR-12-001, Workbench ownership classification in the governed router bridge, prompt router/navigation/routing-canon alignment, metadata and routing-index trigger synchronization, absence of a competing Tool/Project prompt, historical Project Tool Boundary validator compatibility, and STATUS: IN_SYNC.



## known warnings

Global architecture validation has unrelated pre-existing errors. This prompt/routing patch uses focused validation, the historical Project Tool Boundary validator, JSON parsing, and Python compile checks; it must not claim the global architecture baseline is clean. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Project Tool Boundary Workbench Preview Router Bridge v1. Human review is still required before Confirm and Write.

## planned next step

Install, run focused and historical validation, review the pending Error Memory lesson, then Preview and Confirm and Write a separate freeze entry.

## local freeze writer provenance

Generated by 
local_freeze_writer_engine_v1 at 2026-07-06T04:49:54Z.

This entry was created locally for the selected active project. The reusable project_freeze_ledger engine remains blueprint logic only and is not the owner of this project-specific memory.

KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_END

Perfeito. A feature agora está formalmente congelada com sucesso:

freeze-20260706-project-tool-boundary-workbench-preview-router-bridge-v1

Estado consolidado:

KPR-12-001
project_tool_boundary_canon
Version 1.2
STATUS: FROZEN

O Freeze protege explicitamente:

Workbench Preview
→ durable selected-project support state
→ <active_project_support_root>/
  large_file_refactor_workbench/
  preview/
  <preview_id>/

Workbench Shadow
→ disposable daily-work state
→ <active_project_daily_work_root>/
  large_file_refactor_shadow/
  <shadow_id>/

Daily-work
→ garbage-only

Também ficou congelado no routing contract que tarefas de Workbench relacionadas a Preview, Shadow, ownership de support state, preflight, rollback evidence ou final validation state devem carregar o project_tool_boundary_canon e exigir classificação explícita de ownership/lifetime.

E permanece protegido que:

Tool identity != Active Project identity

mesmo no self-hosting, quando fisicamente:

tool_source_root == active_project_root

mas logicamente continuam sendo caixas distintas.

O frozen entry está corretamente no owner canônico do projeto:

E:\kanda_reasoner_show_project_to_AI\
project_freeze_after_update\
frozen_features_memory\
entries\
freeze-20260706-project-tool-boundary-workbench-preview-router-bridge-v1.md

e não em project_freeze_ledger.

A partir daqui, qualquer patch futuro no Workbench, Preview, Shadow, daily-work ou project-support boundary deve respeitar esse Freeze antes de propor mudança.

now audit  Architecture Review tab and sub tabs logic = in an analogy  the logic of this tab and subtabs  must work like a card machine = you insert the card in it ( the module to refactor), card machine reads all information about the "large module  we are about to refactor" ( the  card ) ,  machine writes information in card (refactor the module) but when you remove the card (module refactored and help files associated) machine forgets the card, the card information belongs to the user (project that 's been created) so the module is updated inside the project not  inside kanda reasoner tool , even if we are creating kanda_reasoner project (remember canonic diference tool versus project) , now audit  Architecture Review tab and sub tabs correct to this cannon if necessary 

Vou auditar isso como um problema de ownership + lifecycle, usando sua analogia da máquina de cartão como regra operacional: a aba lê o módulo do projeto ativo, trabalha sobre estado transitório/durável do projeto, escreve apenas no projeto selecionado e não retém “identidade do cartão” dentro do Tool após a conclusão. Vou revisar o shell da Architecture Review, subtabs, seleção de alvo, handoff para o Large File Refactor Workbench e qualquer estado persistente que possa vazar para kanda_reasoner Tool.

Primeiro achado concreto: a camada AST Split já faz parte da analogia corretamente em um ponto importante — ela zera fila, índice, handoff e saída quando começa uma nova auditoria. O risco real está na passagem AST target → Planner → Workbench: parte do estado-alvo fica acumulada em atributos do window, e a troca de projeto/root não parece ter um lifecycle central único que invalide Planner, Workbench e transaction state juntos. Vou fechar essa trilha antes de editar.

Segundo achado confirmado: há uma violação direta do canon Tool/Project no Completion GUI. Ao preparar a transação, o código passa tool_root=project_root; para um projeto externo isso faz o Workbench classificá-lo falsamente como self-hosted. Além disso, a raiz do projeto pode mudar sem invalidar todo o estado AST/Planner/Workbench, permitindo que um “cartão” antigo continue carregado na máquina. Esses dois pontos exigem correção.

Sim — a auditoria encontrou correções necessárias. A Architecture Review já tinha várias peças corretas isoladamente, mas o conjunto ainda não funcionava integralmente como a sua “máquina de cartão”.

A correção está empacotada como feature separada:

Feature ID:

architecture-review-project-card-machine-lifecycle-boundary-v1

SHA-256 do ZIP:

6dc13e9ae45182b4adb98db5d1c5b935fceb76e41bca43e8654272b57e186d54

Resultado da auditoria

A arquitetura correta agora é:

KANDA REASONER TOOL
= máquina de cartão reutilizável

ACTIVE PROJECT
= dono do cartão e das informações escritas nele

LARGE MODULE
= cartão inserido

AST Split Audit
= leitura inicial do cartão

Planner
= interpretação e planejamento

Workbench
= preparação e execução controlada da escrita

Refactor Large Module
= escrita autorizada no cartão

Completion + Receipt
= confirmação da operação

Card Release
= Tool esquece o módulo concluído

Em termos concretos:

INSERT CARD
    ↓
Active Project Root
    ↓
Project-owned module
    ↓
AST Audit
    ↓
Planner
    ↓
Workbench Preview
    ↓
Validation
    ↓
Preflight
    ↓
Payload
    ↓
Shadow
    ↓
Review
    ↓
Transaction
    ↓
Refactor Active Project source
    ↓
Post-apply validation
    ↓
Receipt
    ↓
EJECT CARD
    ↓
Tool forgets target-specific GUI state

Mas permanecem no projeto:

updated project source
generated helper modules
Preview evidence
transaction records
mutation lane state
RefactorReceipt
durable validation evidence

1. Havia colapso real entre Tool e Project

Este foi o defeito canônico mais direto.

No Completion GUI havia essencialmente:

project_root = ...
...
prepare_completion_transaction(
    ...,
    tool_root=project_root,
)

Ou seja, para um projeto externo:

Active Project:
E:\meu_projeto

Tool:
E:\kanda_reasoner

o código passava conceitualmente:

project_root = E:\meu_projeto
tool_root    = E:\meu_projeto

Resultado:

external project
→ falsamente identificado como self-hosted

Isso viola diretamente o frozen KPR-12-001.

Foi corrigido para:

project_root
→ vem do Active Project selecionado

tool_root
→ vem da localização real do KANDA Reasoner Tool instalado

Portanto:

normal external project:

Tool    = E:\kanda_reasoner
Project = E:\my_project
→ NOT SELF-HOSTED

e:

KANDA self-hosting:

Tool physical root    = E:\kanda_reasoner
Project physical root = E:\kanda_reasoner

logical identities remain separate
→ SELF-HOSTING MODE

2. Não existia um único dono do lifecycle do “cartão”

AST Split, Planner e Workbench possuíam mecanismos próprios de reset.

O problema era este:

AST state
    reset A

Planner state
    reset B

Workbench state
    reset C

Completion state
    reset D

Isso permitia situações como:

cartão A inserido
    ↓
AST A
Planner A
Workbench A

troca target para B
    ↓
AST B
Planner parcialmente A
Workbench parcialmente A
Completion A

Esse é exatamente o tipo de cross-card leakage que sua analogia pretende impedir.

Criei um owner central:

kanda_reasoner_app/
└── manage_architecture/
    └── architecture_review_card_lifecycle.py

Ele agora governa:

Project Root identity
AST target identity
Planner target identity
Planner async work
Workbench state
Completion evidence
Completion transaction
Apply outcome
Rollback result
card release

3. Trocar o Project Root agora descarrega a máquina

Antes, trocar:

E:\project_a

para:

E:\project_b

não possuía garantia única de descarregar:

AST queue A
Planner candidates A
Planner analysis A
Planner plan A
Workbench snapshot A
Preview reference A
Completion evidence A
Transaction A
Outcome A

Agora:

PROJECT ROOT A
    ↓
card A loaded

change to PROJECT ROOT B
    ↓
atomic unload
    ├── AST state cleared
    ├── Planner candidates cleared
    ├── Planner results cleared
    ├── async Planner requests invalidated
    ├── Workbench state cleared
    ├── Completion evidence cleared
    ├── Completion transaction cleared
    └── Tool GUI ready for Project B

Importante: isso limpa memória da máquina, não dados do projeto.

Não apaga:

Project A source
Project A helpers
Project A Preview
Project A transaction records
Project A receipt
Project A support state

4. Uma operação em andamento impede retirar o cartão

Agora há comportamento fail-closed.

Durante:

Architecture Review worker running

ou:

AI Review worker running

não é permitido silenciosamente trocar o Project Root ou AST target.

Da mesma maneira:

OPEN MUTATION TRANSACTION
    ↓
cannot eject card
cannot switch Project Root
cannot replace Workbench snapshot
cannot switch target

Até:

terminal completion

ou:

verified rollback

Isso evita:

transaction from card A
+
UI showing card B

5. O browse manual do AST aceitava cartão de outro projeto

Encontrei outra quebra de ownership.

A seleção manual podia receber um arquivo absoluto fora de:

active_project_root

E a função core também aceitava isso.

Exemplo antigo:

Active Project:
E:\project_a

manual target:
E:\project_b\large_module.py

→ accepted

Agora tanto GUI quanto core bloqueiam:

TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT

Contrato:

Architecture Review machine
may only accept a card owned by
the currently selected Active Project.

6. Trocar o snapshot do Workbench não limpava Completion por inteiro

O reset do Workbench limpava fases iniciais, mas não contemplava todo o estado posterior:

completion evidence
completion transaction
completion apply outcome
completion rollback result

Portanto, um novo Planner snapshot podia entrar com parte da “transação do cartão anterior” ainda carregada.

Agora a troca invalida o conjunto completo:

Planner snapshot changed
    ↓
Dependency Readiness cleared
Preview cleared
Structural Validation cleared
Preflight cleared
Payload cleared
Completion Evidence cleared
Completion Transaction cleared
Apply Outcome cleared
Rollback Result cleared
all authorization checks reset

Com uma exceção intencional:

open mutation transaction
→ snapshot replacement BLOCKED

7. Depois da conclusão, a máquina retinha o cartão

Antes:

Refactor completed
    ↓
source updated
receipt produced
    ↓
GUI still holds:
target
Planner state
Workbench state
Completion state

Agora, após estado terminal concluído:

COMPLETED_*
    ↓
release_completed_architecture_review_card()

A máquina esquece:

target-specific Planner state
warning candidate snapshot
Workbench in-memory result
Completion evidence reference
Completion transaction reference
Apply outcome reference
Rollback result reference
completed AST queue item

Mas não apaga o que pertence ao usuário/projeto:

active project source
generated helper files
Preview evidence
transaction database
mutation lane database
RefactorReceipt

Isso implementa diretamente sua analogia.
Correção adicional importante: transaction state

Também encontrei um ownership path incorreto.

O transaction store usava o legado:

<project>_workbench_transactions/
└── large_file_refactor_workbench/

Agora o owner canônico é:

<project>_show_project_to_AI/
└── large_file_refactor_workbench/
    ├── transactions/
    └── project_mutation_lane.sqlite3

Ou seja:

Transaction truth
→ Active Project Support

NOT Tool source
NOT daily-work
NOT external sibling transaction root

Há uma migração bounded e fail-closed:

legacy exists
canonical absent
→ move legacy to canonical

legacy + canonical both contain durable state
→ BLOCK

legacy lane DB + canonical lane DB both exist
→ BLOCK

Não ocorre merge silencioso de duas verdades duráveis.
Arquivos alterados

kanda_reasoner_app/manage_architecture/
├── architecture_review_card_lifecycle.py
├── architecture_review_subtabs.py
├── large_module_split_audit.py
├── large_module_split_audit_gui.py
└── large_file_refactor_planner/
    ├── ast_audit_planner_sync.py
    ├── gui_warning_input_gate.py
    ├── workbench_snapshot_bridge.py
    ├── workbench_completion_gui.py
    ├── workbench_completion_workflow.py
    └── workbench_transaction_store.py

tools/
└── validate_architecture_review_project_card_lifecycle_v1.py

Todos os source modules tocados ficaram com até 500 linhas.
Validação já concluída no sandbox

O payload exato do ZIP foi aplicado sobre a árvore-base de auditoria e passou:

ROOT_CHANGE_UNLOADS_AST_PLANNER_WORKBENCH: PASS

TARGET_CHANGE_INVALIDATES_DOWNSTREAM_CARD_STATE: PASS

RUNNING_AUDIT_BLOCKS_PROJECT_CARD_SWITCH: PASS

OPEN_TRANSACTION_BLOCKS_CARD_EJECTION: PASS

COMPLETED_REFACTOR_RELEASES_TOOL_CARD_MEMORY: PASS

AST_TARGET_ACTIVE_PROJECT_ONLY: PASS

TOOL_PROJECT_IDENTITY_NOT_COLLAPSED: PASS

WORKBENCH_TRANSACTION_STATE_PROJECT_SUPPORT_ONLY: PASS

LEGACY_TRANSACTION_STATE_MIGRATION: PASS

TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS

ARCHITECTURE_REVIEW_CARD_MACHINE_LIFECYCLE: PASS

VALIDATION OK:
architecture-review-project-card-machine-lifecycle-boundary-v1

STATUS: IN_SYNC

Também passou:

VALIDATION OK:
project-tool-boundary-canon-v1

STATUS: IN_SYNC

e:

SQLITE_CONNECTION_CLOSURE: PASS
SERIAL_LANE: PASS
RESTART_RECOVERY: PASS
SQLITE_TRANSACTION_METADATA: PASS
SNAPSHOT_PERSISTENCE: PASS
NO_SOURCE_MUTATION: PASS

VALIDATION OK:
architecture-review-large-file-refactor-workbench-patch2-durable-transaction-serial-lane-v1

Além disso:

EXACT_PAYLOAD_OVERLAY_COMPILE: PASS
ZIP CONTRACT: PASS

O ZIP contém exatamente um:

KANDA_FREEZE_HINT.json

na raiz.
Limitação honesta da validação local daqui

As regressões Patch 4–6 não puderam completar neste sandbox porque o ambiente não possui libcst, e o source archive disponibilizado anteriormente também omite alguns módulos e validators devido às exclusões já conhecidas. Não estou classificando essas etapas como PASS.

No seu log local anterior, a cadeia Workbench v3 e Patch 2–6 havia passado até chegar à Architecture Validation global, que então reportou os 15 erros globais não relacionados a esta feature.

Por isso, o ZIP inclui um VALIDATE.ps1 que roda no seu ambiente real:

ZIP contract
↓
focused card-machine lifecycle validator
↓
historical Project Tool Boundary canon
↓
Workbench Project Support Boundary v3
↓
compileall
↓
Patch 2 transaction core
↓
Patch 4 completion gate
↓
Patch 5 journaled apply
↓
Patch 6 controlled real module
↓
Patch 6 final canon
↓
final integration hardening
↓
freeze evidence merge
↓
Error Memory intake check

Os 15 erros globais não relacionados não foram silenciosamente incluídos no escopo nem declarados como corrigidos.
Instalação

Salve o ZIP em:

E:\

Feche completamente o KANDA antes de instalar.

Use:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "kanda_architecture_review_project_card_machine_lifecycle_boundary_v1.zip"

$ProjectName = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

$WORK_DIR = Join-Path `
    $DRIVE_ROOT `
    ($ProjectName + "_delete_after_daily_work")

$ROOT_ZIP = Join-Path $DRIVE_ROOT $PATCH_NAME

$BOOTSTRAP_ROOT = Join-Path `
    $WORK_DIR `
    "kanda_architecture_review_project_card_machine_lifecycle_boundary_v1_bootstrap"

try {
    if (-not (Test-Path -LiteralPath $ROOT_ZIP -PathType Leaf)) {
        throw "Put the patch ZIP at exactly: $ROOT_ZIP"
    }

    New-Item `
        -ItemType Directory `
        -Force `
        -Path $WORK_DIR | Out-Null

    Remove-Item `
        -LiteralPath $BOOTSTRAP_ROOT `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue

    Expand-Archive `
        -LiteralPath $ROOT_ZIP `
        -DestinationPath $BOOTSTRAP_ROOT `
        -Force

    $INSTALL = Join-Path $BOOTSTRAP_ROOT "INSTALL.ps1"

    if (-not (Test-Path -LiteralPath $INSTALL -PathType Leaf)) {
        throw "INSTALL.ps1 missing: $INSTALL"
    }

    & $INSTALL
}
catch {
    Write-Host ""
    Write-Host "INSTALL LAUNCH ERROR: $($_.Exception.Message)"

    Read-Host "Press Enter after copying this output"
    Read-Host "Press Enter again to clear the terminal"
    Clear-Host
}

Depois, execute o validator empacotado:

$PROJECT_ROOT = "E:\kanda_reasoner"

$ProjectName = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

$VALIDATE = Join-Path `
    $DRIVE_ROOT `
    ($ProjectName + "_delete_after_daily_work\" +
     "kanda_architecture_review_project_card_machine_lifecycle_boundary_v1_extract\" +
     "VALIDATE.ps1")

& $VALIDATE

O final esperado é:

FREEZE_HINT_EVIDENCE_MERGE_OK:
architecture-review-project-card-machine-lifecycle-boundary-v1

ERROR_MEMORY_PENDING_INTAKE_OK:
KANDA_ERROR_LESSON_JSON_architecture_review_project_card_machine_lifecycle_v1.txt

ARCHITECTURE_REVIEW_PROJECT_CARD_MACHINE_LIFECYCLE_V1_VALIDATION_OK

Somente depois:

Error Memory
→ Review
→ Memorize Error

Freeze Feature After Update
→ New Local Freeze Entry
→ Preview
→ human review
→ Confirm and Write

Minha conclusão da auditoria: sua analogia da máquina de cartão estava correta e revelou um problema arquitetural real. O Workbench engine tinha várias proteções fortes, mas a Architecture Review como conjunto ainda não possuía um owner único para o ciclo insert → read → plan → refactor → verify → eject. Esse é precisamente o papel introduzido pelo novo architecture_review_card_lifecycle.py.

PS E:\kanda_reasoner> 
PS E:\kanda_reasoner> & $VALIDATE
At E:\kanda_reasoner_delete_after_daily_work\kanda_architecture_review_project_card_machine_lifecycle_boundary_
v1_extract\VALIDATE.ps1:171 char:21
+         $ProjectName
+                     ~
Missing closing ')' in expression.
At E:\kanda_reasoner_delete_after_daily_work\kanda_architecture_review_project_card_machine_lifecycle_boundary_
v1_extract\VALIDATE.ps1:56 char:5
+ try {
+     ~
Missing closing '}' in statement block or type definition.
At E:\kanda_reasoner_delete_after_daily_work\kanda_architecture_review_project_card_machine_lifecycle_boundary_
v1_extract\VALIDATE.ps1:173 char:22
+         + $LessonName
+                      ~
The Try statement is missing its Catch or Finally block.
At E:\kanda_reasoner_delete_after_daily_work\kanda_architecture_review_project_card_machine_lifecycle_boundary_
v1_extract\VALIDATE.ps1:174 char:5
+     )
+     ~
Unexpected token ')' in expression or statement.
At E:\kanda_reasoner_delete_after_daily_work\kanda_architecture_review_project_card_machine_lifecycle_boundary_
v1_extract\VALIDATE.ps1:182 char:1
+ }
+ ~
Unexpected token '}' in expression or statement.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : MissingEndParenthesisInExpression
 

Esse erro é do próprio VALIDATE.ps1 que eu empacotei: há uma expressão PowerShell malformada perto da montagem do caminho da lesson. Vou abrir exatamente essas linhas, corrigir o wrapper, testar a sintaxe com PowerShell e te devolver um ZIP reparado sem alterar a lógica funcional do patch.

Encontrei a causa exata: no VALIDATE.ps1, a concatenação do caminho foi quebrada em linhas começando por +. Em PowerShell isso encerra a expressão na linha anterior e gera exatamente os erros de parêntese/chave que você recebeu. O source patch já pode estar instalado; vou gerar um release reparado cumulativo com wrapper corrigido e manter a mesma feature lógica, sem pedir que você reverta nada.

Vou liberar isso como v1r1: mesma feature lógica e mesmo feature_id, mas com o wrapper de validação corrigido e o nome do artefato atualizado no freeze hint. Assim você pode instalar por cima do que já foi aplicado; o payload fonte é cumulativo e idêntico, e a diferença do release é o VALIDATE.ps1 reparado.

O erro era real e estava no VALIDATE.ps1 que eu empacotei. A expressão:

$LessonPath = Join-Path $DRIVE_ROOT (
    $ProjectName
    + "_show_project_to_AI\..."
    + $LessonName
)

é inválida em PowerShell porque a nova linha encerra $ProjectName antes do operador +.

Corrigi para uma composição segura com Join-Path separado e gerei um release cumulativo reparado:
Patch reparado v1r1

SHA-256:

df30c8f8c659f4aaf7ac53f712ed2ebc462c68b6a5a09dbf886f1787fdf78001

A identidade lógica continua a mesma:

feature_id:
architecture-review-project-card-machine-lifecycle-boundary-v1

O v1r1 é apenas um release repair do pacote/wrapper, não uma feature concorrente.
O que foi validado novamente

O ZIP reparado passou:

ZIP CONTRACT: PASS

O overlay exato do payload passou:

ROOT_CHANGE_UNLOADS_AST_PLANNER_WORKBENCH: PASS
TARGET_CHANGE_INVALIDATES_DOWNSTREAM_CARD_STATE: PASS
RUNNING_AUDIT_BLOCKS_PROJECT_CARD_SWITCH: PASS
OPEN_TRANSACTION_BLOCKS_CARD_EJECTION: PASS
COMPLETED_REFACTOR_RELEASES_TOOL_CARD_MEMORY: PASS
AST_TARGET_ACTIVE_PROJECT_ONLY: PASS
TOOL_PROJECT_IDENTITY_NOT_COLLAPSED: PASS
WORKBENCH_TRANSACTION_STATE_PROJECT_SUPPORT_ONLY: PASS
LEGACY_TRANSACTION_STATE_MIGRATION: PASS
TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS
ARCHITECTURE_REVIEW_CARD_MACHINE_LIFECYCLE: PASS

VALIDATION OK:
architecture-review-project-card-machine-lifecycle-boundary-v1

STATUS: IN_SYNC

Também passaram:

VALIDATION OK: project-tool-boundary-canon-v1
STATUS: IN_SYNC

e:

SQLITE_CONNECTION_CLOSURE: PASS
SERIAL_LANE: PASS
RESTART_RECOVERY: PASS
SQLITE_TRANSACTION_METADATA: PASS
SNAPSHOT_PERSISTENCE: PASS
NO_SOURCE_MUTATION: PASS

Além disso:

VALIDATE.ps1_STATIC_PARSE_GUARD: PASS
INSTALL.ps1_STATIC_PARSE_GUARD: PASS

O sandbox não possui PowerShell nativo para executar o parser oficial da Microsoft, então essa última checagem foi um guard estático de delimitadores, strings, here-strings e continuations. O erro específico que você encontrou foi removido e o wrapper foi reconstruído.
Agora faça assim

Coloque o novo ZIP em:

E:\

e execute este bloco:

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = `
    "kanda_architecture_review_project_card_machine_lifecycle_boundary_v1r1.zip"

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
    "kanda_architecture_review_project_card_machine_lifecycle_boundary_v1r1_bootstrap"

try {
    New-Item `
        -ItemType Directory `
        -Force `
        -Path $WORK_DIR | Out-Null

    if (-not (Test-Path -LiteralPath $ROOT_ZIP -PathType Leaf)) {
        throw "Put the repaired ZIP at exactly: $ROOT_ZIP"
    }

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
    Write-Host "INSTALL ERROR: $($_.Exception.Message)"

    Read-Host "Press Enter after copying this output"
    Read-Host "Press Enter again to clear the terminal"
    Clear-Host
}

Depois rode:

$PROJECT_ROOT = "E:\kanda_reasoner"

$ProjectName = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)

$VALIDATE = Join-Path `
    $DRIVE_ROOT `
    ($ProjectName + "_delete_after_daily_work\" +
     "kanda_architecture_review_project_card_machine_lifecycle_boundary_v1_extract\" +
     "VALIDATE.ps1")

& $VALIDATE

O final correto deve chegar a:

FREEZE_HINT_EVIDENCE_MERGE_OK:
architecture-review-project-card-machine-lifecycle-boundary-v1

ERROR_MEMORY_PENDING_INTAKE_OK:
KANDA_ERROR_LESSON_JSON_architecture_review_project_card_machine_lifecycle_v1.txt

ARCHITECTURE_REVIEW_PROJECT_CARD_MACHINE_LIFECYCLE_V1_VALIDATION_OK

Não use mais o ZIP ..._v1.zip para validação. O candidato atual é o ..._v1r1.zip.


