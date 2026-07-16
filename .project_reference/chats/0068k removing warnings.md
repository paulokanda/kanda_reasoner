Yesterday 6:53 PM
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

Pasted text.txt
Document
is there an heuristic tool in project or to install in project that solve these warnings or it must be corrected via contextual AI?

warning_resolver_live_conflict_source.zip
Zip Archive

Pasted markdown(2).md
File
KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_BEGIN
Title: Last frozen feature entry
Project root: E:\kanda_reasoner
Entry count: 1
Instruction: Use this as read-only frozen feature memory. Do not edit these entries directly. Do not write project-specific memory into project_freeze_ledger.

--- FROZEN ENTRY 1 OF 1 ---
Path: E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update\frozen_features_memory\entries\freeze-20260709-warning-heuristic-resolver-phase-1-routing-foundation.md

---
freeze_id: "freeze-20260709-warning-heuristic-resolver-phase-1-routing-foundation"
feature_title: "Warning Heuristic Resolver - Phase 1 Routing Foundation"
box: "kanda_reasoner_app/manage_architecture"
status: "frozen"
date: "2026-07-09"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260709-warning-heuristic-resolver-phase-1-routing-foundation.md"
protected_paths:
  - "kanda_reasoner_app/manage_architecture"
  - "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
  - "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Resolver remains read-only until a warning-specific governed resolver is implemented and validated."
  - "Unknown or unregistered warning codes route to Web AI instead of receiving guessed automatic edits."
  - "Warning resolver output must not be reparsed as new Architecture Review WARNING lines."
  - "Feature-private mutable state must not be cached on the shared ArchitectureManagerWindow host."
  - "Every new public resolver module must have a direct focused test-protection import."
  - "Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260709-warning-heuristic-resolver-phase-1-routing-foundation

## freeze identity

Freeze ID: freeze-20260709-warning-heuristic-resolver-phase-1-routing-foundation

Feature title: Warning Heuristic Resolver - Phase 1 Routing Foundation

Date: 2026-07-09

Primary box: kanda_reasoner_app/manage_architecture

Box type: tool_owned_architecture_governance

Status: frozen after explicit human confirmation and validation evidence

## summary

Cumulative v1r1 rebase preserves the live AST Split Web AI risk-repair integration in architecture_review_subtabs.py while adding the Phase 1 Warning Heuristic Resolver button. The resolver remains read-only and routes difficult or unregistered warnings to Web AI. Freeze-intake data was loaded from <project>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake. Source patch ZIP: kanda_warning_heuristic_resolver_v1r1.zip.

## validated files

- kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py
- kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py
- kanda_reasoner_app/manage_architecture/warning_heuristic_resolver.py
- tools/validate_architecture_review_warning_heuristic_resolver_v1.py
- tools/test_architecture_review_warning_heuristic_resolver_contract.py

## generated files

- kanda_reasoner_app/manage_architecture/warning_heuristic_resolver.py
- tools/validate_architecture_review_warning_heuristic_resolver_v1.py
- tools/test_architecture_review_warning_heuristic_resolver_contract.py

## protected paths

- kanda_reasoner_app/manage_architecture
- kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py
- kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py
- project_freeze_after_update/frozen_features_memory

## do-not-regress rules

- Resolver remains read-only until a warning-specific governed resolver is implemented and validated.
- Unknown or unregistered warning codes route to Web AI instead of receiving guessed automatic edits.
- Warning resolver output must not be reparsed as new Architecture Review WARNING lines.
- Feature-private mutable state must not be cached on the shared ArchitectureManagerWindow host.
- Every new public resolver module must have a direct focused test-protection import.
- Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.
- Do not store project-specific frozen memory inside project_freeze_ledger.
- Preview Freeze Entry must remain read-only and must not write files.
- Confirm and Write must require explicit human confirmation before writing governed freeze memory.
- After a local freeze write, the AI startup freeze context must be refreshed.
- External AI review remains advanced/fallback, not the normal local freeze path.

## validation evidence

text
ZIP CONTRACT: PASS
{
"error_memory_lesson_blocks_checked": 0,
"feature_id": "architecture-review-warning-heuristic-resolver-v1",
"feature_title": "Warning Heuristic Resolver - Phase 1 Routing Foundation",
"ok": true,
"root_freeze_hint": true,
"zip_name": "kanda_warning_heuristic_resolver_v1r1.zip",
"zip_path": "E:\\kanda_reasoner_delete_after_daily_work\\kanda_warning_heuristic_resolver_v1r1.zip"
}
PATCH_PAYLOAD_HASHES: PASS
WARNING_HEURISTIC_RESOLVER_CORE: PASS
WARNING_HEURISTIC_RESOLVER_GUI_WIRING: PASS
WARNING_HEURISTIC_RESOLVER_READ_ONLY_PHASE1: PASS
VALIDATION OK: architecture-review-warning-heuristic-resolver-v1
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s
System.Management.Automation.RemoteException
OK
VALIDATION OK: architecture-review-local-subtabs-v1
VALIDATION OK: architecture-review-local-subtabs-v1-runtime-repair-v1
VALIDATION OK: architecture-review-subtab-style-repair-v1
VALIDATION OK: architecture-review-subtab-height-compact-v1
VALIDATION CHAIN COMPLETE: architecture-review-warning-heuristic-resolver-v1
FREEZE_HINT_EVIDENCE_MERGE_OK: architecture-review-warning-heuristic-resolver-v1



## known warnings

The current project contains pre-existing Architecture Review warnings. This Phase 1 feature only routes warnings and does not correct existing warning findings. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Warning Heuristic Resolver - Phase 1 Routing Foundation.

## planned next step

Implement and validate the TEST_PROTECTION_GAP warning-specific heuristic resolver.

## local freeze writer provenance

Generated by 
local_freeze_writer_engine_v1 at 2026-07-09T22:47:41Z.

This entry was created locally for the selected active project. The reusable project_freeze_ledger engine remains blueprint logic only and is not the owner of this project-specific memory.

KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_END


now this 

Pasted text(1).txt
Document
waati continue implementing correction of  

Pasted text(2).txt
Document
button  Warning Heuristic Resolver  seems to increase the number of errors?


Pasted text(3).txt
Document
wait I updated after button  Warning Heuristic Resolver, it seems that it doesn't  solve anything 

Pasted text(4).txt
Document
audit correct implement

Yesterday 11:09 PM
_RUN_COLLECTOR_STATUS(1).txt
Document
kanda_reasoner__ai_handoff_all_in_one(1).zip
Zip Archive
kanda_reasoner__ai_handoff_upload(1).zip
Zip Archive
kanda_reasoner__ai_handoff_upload_readme(1).txt
Document
kanda_reasoner__error_lessons_compact(1).json
File
kanda_reasoner__error_memory_ai_prompt(1).md
File
kanda_reasoner__error_memory_full(1).zip
Zip Archive
kanda_reasoner__error_memory_manifest(1).json
File
kanda_reasoner__png_assets_part01_of_01(1).zip
Zip Archive
kanda_reasoner__source_archive_part01_of_01(1).zip
Zip Archive
it is working , but many files need AI , is that possible local ai  qwen3-coder:30b be used to correct those warning test protection if so  add local AI to the process modify button Warning Heuristic Resolver to a dropdown with options "Warning Heuristic Resolver"  and  "Warning loca AI Resolver" plus a small dropdown button to activate dropdown options , of course create the correct logic to link local AI to fit the corrections and test in sandbox before sending for download. I upload the update project now because I don't want you to guess anything nor asssume anything , go to see evidence in code.

Recebi o snapshot atualizado. Vou usar o código enviado como fonte de verdade: primeiro identifico o padrão real do dropdown já existente, o caminho canônico para chamar qwen3-coder:30b, o contrato atual do resolver assíncrono/sonar e os validadores relacionados; depois implemento e testo a transição em sandbox antes de empacotar.

A primeira evidência importante do código real: o serviço compartilhado chat_with_local_model() pode cair para outro modelo instalado quando a seleção exata não é encontrada. Para esta feature, isso não é aceitável; o lane “Warning local AI Resolver” será fail-closed e só executará se qwen3-coder:30b estiver realmente disponível.

atention “Warning local AI Resolver” será fail-closed e só executará se qwen3-coder:30b"  use not only this but make it dinamic to accept any model ollama in options

Certo — ajuste aceito. O lane Warning local AI Resolver não ficará preso ao qwen3-coder:30b: ele vai detectar dinamicamente os modelos Ollama disponíveis, permitir seleção e usar exatamente o modelo escolhido, sem fallback silencioso para outro modelo.

Ajuste de escopo incorporado: o dropdown terá seleção dinâmica de modelo Ollama e guardará o modelo escolhido explicitamente para a execução local. Também vou evitar o comportamento atual do serviço compartilhado que, quando não encontra uma seleção exata, pode cair para outro modelo disponível.

ERROR MEMORY CHECK

Project slug: kanda_reasoner
Relevant lesson IDs: lesson-cumulative-patch-new-file-predecessor-hash-conflict-v1, lesson-planner-preference-shared-host-settings-cache-box-shield-gap-v1, lesson-complete-json-validator-ambient-collector-env-leak-v1
Confidence per match: exact / partial / partial
Applicable avoidance rules: exact predecessor hash allowlists for cumulative upgrades; no feature-private mutable state on the shared Architecture window; deterministic Local AI fixtures must not inherit ambient project scope unexpectedly.
Full Error Memory ZIP needed: NO.
May proceed: YES.
Reason: the compact lessons are sufficient and directly constrain installer, state ownership, and validation design. mplement against the uploaded source snapshot, keep model selection in a feature-owned QObject controller, and validate Local AI behavior through injected fake chat/model providers before real Ollama use.

o modelo ollama já é escolhido lá em cima , no dropdown novo  só use as opções heuristic or  Local AI

Today 8:44 AM
sonar is running 5 minutes and no change

Isso indica que o lane Local AI está parado antes do primeiro progress emit ou em uma chamada Ollama bloqueante sem timeout/progresso intermediário. Vou auditar o worker/controller e o adapter Ollama do snapshot que você enviou para localizar o ponto exato antes de propor o patch.

now it is gonit  but it is saying that  web Ai is necessary, model qwen3-codr:30b solved 1 case of 80, qwen2.5-coder:7b solved 1 case from 80. my gpu is a gforce rtx 4080 do you suggest any other ollama AI to install or we are done here? or can you improve local AI resolution to solve more of those problems?

Vou separar duas perguntas: hardware/modelo e qualidade do resolver. Primeiro vou revisar o prompt, contexto enviado ao Ollama e gates de aceitação no código atual; em paralelo, vou comparar modelos Ollama atuais que façam sentido para uma RTX 4080.

I would not call this finished, and I would not spend time installing many more models yet.

My conclusion after looking at the actual resolver code is:

    The main bottleneck is the resolver architecture, not Qwen3-Coder.

The fact that qwen3-coder:30b and qwen2.5-coder:7b both resolved only 1 of 80 strongly supports that conclusion.
Why the Local AI currently resolves almost nothing

The current Local AI lane is much narrower than it appears.

It does not ask the AI:

    “Can you solve this TEST_PROTECTION_GAP correctly?”

It effectively asks:

    “Among at most a few existing tests that my deterministic pre-filter selected, can you identify one that already protects this source strongly enough to pass another deterministic gate?”

The actual implementation currently has several limiting factors:

TEST_PROTECTION_GAP
        ↓
find candidate existing tests
        ↓
keep only top 4
        ↓
send truncated source excerpt
        ↓
send truncated test excerpts
        ↓
AI chooses one
        ↓
confidence must be >= 0.90
        ↓
candidate must ALSO pass deterministic relationship gate
        ↓
otherwise Web AI

So a more intelligent model cannot escape the deterministic gate.

More importantly, the Architecture Review warning itself explicitly says the correct remedy can be to add or link a focused test.

But our Local AI v1 only does:

LINK EXISTING TEST

It does not do:

CREATE MEANINGFUL TEST
EXTEND EXISTING TEST
ADD REAL ASSERTIONS
EXECUTE TARGETED PYTEST
VERIFY WARNING DISAPPEARS

Therefore, when a module genuinely lacks meaningful test coverage, even the best possible AI must return:

Web AI necessary

That is the biggest limitation.
About your RTX 4080

The desktop RTX 4080 has 16 GB of GDDR6X VRAM.

Your current:

qwen3-coder:30b

is about 19 GB in Ollama's default package.

So, as an inference from the published model size and your GPU VRAM, the model cannot reside entirely within 16 GB VRAM under ordinary conditions; some runtime memory pressure or offloading is likely. That is a plausible explanation for the very long execution time you saw.
Models I would actually test
1. qwen2.5-coder:14b — my first recommendation

ollama pull qwen2.5-coder:14b

Ollama lists it at approximately 9 GB, compared with 4.7 GB for the 7B version and 20 GB for the 32B version.

For your 4080, this is the most sensible test:

7B
fast but weaker

14B
good VRAM fit
more reasoning capacity
my preferred practical choice

32B
20 GB
again above your 16 GB VRAM

I would test 14B before buying into larger models.
2. devstral-small-2 — interesting second experiment

ollama pull devstral-small-2

Ollama describes it as a 24B software-engineering model and lists the default package at about 15 GB. It is explicitly designed for codebase exploration and software-engineering tasks.

This is interesting for your use case because your task is not ordinary code completion. It is closer to:

understand source module
+
understand several tests
+
infer behavioral relationship
+
make repository-level decision

That aligns more closely with a software-engineering model than a simple coding autocomplete model.

However, because the package itself is already near your 16 GB VRAM limit, context/KV-cache overhead may still make it less comfortable than a 9 GB model. That is an inference from the published model and GPU memory sizes.
Models I would not prioritize for this machine

I would not prioritize qwen3-coder-next locally: Ollama lists the Q4 model at about 52 GB, far beyond the 4080's 16 GB VRAM.

Likewise, qwen3.6:27b is listed at about 17 GB, already slightly larger than the card's VRAM before accounting for runtime overhead, while the 35B default is about 24 GB.

So my model recommendation is simply:

1. qwen2.5-coder:14b
2. devstral-small-2
3. keep qwen3-coder:30b for comparison

I would not install ten models and repeat an 80-file run for each.
What I think we should really improve

I recommend a Warning Local AI Resolver v2, but it should not merely relax confidence from 0.90 to 0.80.

That would be dangerous and would repeat the false-positive problem we had with the 22 links.

Instead:
Stage 1 — Better candidate discovery

Current:

filename similarity
symbol text match
sibling imports
top 4

Improved:

direct imports
transitive facade imports
public-symbol usage
pytest monkeypatch target paths
mock.patch paths
fixture dependency
test function names
assertion targets
called public functions
shared domain tokens
package topology
historical co-change, when available

This alone may expose real candidates that the AI currently never receives.
Stage 2 — Semantic context instead of text prefixes

Current code gives the AI truncated prefixes of source and tests.

That is weak.

For example:

source file: 450 lines
relevant public function: lines 330–410

current context:
first 5,200 chars

AI:
never sees relevant function

And:

test file: 500 lines
relevant test: lines 380–430

current context:
first 2,600 chars

AI:
never sees relevant test

I would replace that with AST-selected context:

source:
- __all__
- public signatures
- relevant public function/class bodies
- direct dependencies

test:
- relevant test functions
- fixtures they consume
- monkeypatch/mock targets
- assertions
- imports

That should improve accuracy much more than switching from one 30B model to another.
Stage 3 — Let Local AI create a real test proposal

This is the biggest improvement.

For findings where no existing test genuinely protects the module:

Local AI
    ↓
propose focused test change
    ↓
write only into sandbox candidate
    ↓
compile
    ↓
import test
    ↓
run targeted pytest
    ↓
run existing relevant regression tests
    ↓
rerun Architecture Review detector
    ↓
show diff to human
    ↓
Yes
    ↓
hash guard
backup
atomic apply

Then the Local AI could genuinely solve:

TEST_PROTECTION_GAP

instead of merely finding an existing file to attach a TYPE_CHECKING import to.

I would use a strict output contract like:

action:
    link_existing_test
    extend_existing_test
    create_focused_test
    web_ai

source_path:
    exact source

target_test_path:
    exact existing test
    OR governed new test path

public_contract_under_test:
    [...]

behavior_scenario:
    [...]

test_patch:
    bounded diff

required_validation:
    [...]

And every generated test must prove something behavioral. The validator should reject:

def test_imports():
    import module

or:

def test_smoke():
    assert True

Those are warning silencers, not test protection.
My honest recommendation

I would do this:

Do not declare Local AI finished
        ↓
Do not install many more giant models
        ↓
Install qwen2.5-coder:14b
        ↓
optionally test devstral-small-2
        ↓
but prioritize Resolver v2 architecture

My expectation is:

changing model only:
1/80 -> perhaps a few more

improving context + retrieval:
potentially materially more links

adding validated test creation:
can address genuinely untested modules

The last category is where the largest potential improvement lies.

My recommended next feature design is therefore not “use a bigger AI.” It is Warning Local AI Resolver v2: semantic retrieval + sandboxed real-test generation. That is the direction I would take before considering the Local AI lane complete.

gimme ollama code to remove qwen2.5-coder:7b

ollama rm qwen2.5-coder:7b

Para confirmar depois:

ollama list


update Resolver v2 architecture

Vou atualizar o Resolver v2 como uma evolução cumulativa do lane Local AI atual: melhor recuperação semântica de candidatos, contexto AST direcionado e geração/edição de testes reais em sandbox, sempre com execução e re-audit antes de permitir aplicação no projeto.

ERROR MEMORY CHECK

Project slug: kanda_reasoner
Relevant lesson IDs: lesson-cumulative-patch-new-file-predecessor-hash-conflict-v1, lesson-workbench-heuristic-correction-qthread-bounded-runtime-v2, lesson-planner-preference-shared-host-settings-cache-box-shield-gap-v1
Confidence: exact / exact / partial
Applicable rules: cumulative v2 must accept exact v1 predecessor hashes; Local AI must remain Qt-native and bounded with real progress; no feature-private mutable state may leak onto the shared Architecture window.
Full Error Memory ZIP needed: NO.
May proceed: YES.
Next safe action: build v2 over the exact v1 payload, not over the older source snapshot alone.

A primeira mudança estrutural será remover o gargalo que limitava a IA aos quatro “melhores” testes e aos primeiros caracteres dos arquivos. O v2 vai enviar contexto selecionado por AST: assinaturas públicas, corpos relevantes, imports, testes relacionados, fixtures, mocks e assertions.

Resolver v2 architecture is updated and packaged.

I built it from the updated project snapshot you provided. The collector status was complete, and the handoff explicitly identifies the source archive as the source for exact code inspection.

The cumulative design also followed the relevant Error Memory constraints: exact predecessor hashes, Qt-native bounded worker behavior, and no mutable feature state leaked onto the shared Architecture window.
Resolver v2 architecture

The important difference is that Local AI is no longer limited to:

Find one existing test
        ↓
add TYPE_CHECKING link

The new pipeline is:

TEST_PROTECTION_GAP
        │
        ▼
STRICT HEURISTIC
        │
        ├── existing safe relationship
        │       └── SAFE LINK
        │
        ▼
LOCAL AI V2
        │
        ├── AST source evidence
        │
        ├── public API
        │
        ├── relevant function/class bodies
        │
        ├── imports
        │
        ├── up to 8 candidate tests
        │
        ├── test functions
        │
        ├── fixtures
        │
        ├── mocks / monkeypatch targets
        │
        └── assertions
                │
                ▼
        selected Ollama model
                │
       ┌────────┼────────────┐
       │        │            │
       ▼        ▼            ▼
 link existing  extend       create focused
 test           existing     test
                test
       │        │            │
       └────────┼────────────┘
                ▼
      disposable project copy
                │
                ▼
        targeted pytest
                │
          PASS required
                │
                ▼
      fresh Architecture Review
                │
      gap disappeared required
                │
                ▼
          SAFE PROPOSAL
                │
        Human confirmation
                │
                ▼
       freshness hash check
       backup
       atomic write

Anything that fails any gate remains:

Web AI required

The AI now has four possible decisions

link_existing_test
extend_existing_test
create_focused_test
web_ai

This directly addresses the fundamental weakness of v1: a genuinely untested source module could never be resolved merely by switching to a smarter model.
Real test protection gates

The model cannot produce this:

def test_import():
    import some_module

or:

def test_smoke():
    assert True

and have it accepted.

The v2 checks for:

    real test_ functions;

    exact target-module relationship;

    public contract references;

    assertions or expected-exception behavior;

    exact governed paths;

    no invented existing-test path;

    no duplicate mutation target;

    targeted pytest success;

    fresh disappearance of the source's TEST_PROTECTION_GAP.

Better AI context

V1 effectively used:

first part of source file
+
first part of candidate test
+
top 4 candidates

V2 now uses AST-selected evidence:

SOURCE EVIDENCE
├── public API
├── public signatures
├── relevant public bodies
├── direct dependencies
└── imports

TEST EVIDENCE
├── relevant test functions
├── fixtures
├── assertion symbols
├── monkeypatch targets
├── mock.patch targets
├── imported modules
└── semantic relationship evidence

Candidate capacity increased from:

4

to:

8

but the acceptance gate remains strict.
Sonar progress

I also changed progress visibility.

Before the potentially slow model call, the worker now emits:

Local AI reviewing

Then additional phases include:

Local AI reviewing
Sandbox pytest
Sandbox Architecture Review
Sandbox validating
Validated test change
Web AI necessary

So a long Ollama inference should no longer look like a completely dead sonar even before the result returns.
Validation results
Cumulative install transition

CUMULATIVE_V1_TO_V2_SOURCE_FRESHNESS: PASS
CUMULATIVE_V1_TO_V2_PAYLOAD_HASHES: PASS
SANDBOX_INSTALL_TRANSITION: PASS

v2 core

WARNING_MODEL_RESOLVER_V2_PYTHON_SYNTAX: PASS
WARNING_MODEL_RESOLVER_V2_MODULE_SIZE_GATE: PASS

WARNING_MODEL_RESOLVER_V2_AST_SEMANTIC_RETRIEVAL: PASS

WARNING_MODEL_RESOLVER_V2_REAL_TEST_GENERATION_FAIL_CLOSED: PASS

WARNING_MODEL_RESOLVER_V2_DISPOSABLE_PROJECT_PYTEST_AND_AUDIT: PASS

WARNING_MODEL_RESOLVER_V2_PRE_CHAT_PROGRESS: PASS

WARNING_MODEL_RESOLVER_V2_HUMAN_CONFIRMATION_GATE: PASS

WARNING_MODEL_RESOLVER_V2_FOCUSED_TEST_PROTECTION_IMPORTS: PASS

Local AI behavior

exact selected model: PASS
unavailable selected model fails closed: PASS
invented test path rejected: PASS
invalid JSON bounded retry: PASS
Auto dynamic Ollama selection: PASS
no model fallback: PASS

Generation behavior

AST semantic evidence: PASS

create focused test
-> sandbox accepted
-> guarded application available
PASS

sandbox rejection
-> Web AI
PASS

assert True warning silencer rejected: PASS

progress before blocking model call: PASS

Disposable project validation

targeted pytest PASS
+
fresh Architecture Review gap removed
=
accepted

Validated:

DISPOSABLE_COPY_TARGETED_PYTEST: PASS

FRESH_AUDIT_GAP_REMOVAL: PASS

PERSISTENT_GAP_REJECTION: PASS

TARGET_COLLISION_FAIL_CLOSED: PASS

Self-audit

Reconstructed v1 baseline:

623 issues
17 errors
606 warnings

v2 implementation:

623 issues
17 errors
606 warnings

And:

WARNING_MODEL_RESOLVER_V2_BASELINE_FINDING_ALLOWLIST: PASS
WARNING_MODEL_RESOLVER_V2_NEW_OWNER_ARCHITECTURE_FINDINGS: 0

VALIDATION OK:
architecture-review-warning-local-ai-resolver-architecture-delta-v2

The pre-existing MIXED_RESPONSIBILITY_FILE on architecture_audit_actions_gui.py remains identical to baseline; the delta validator allows only that exact baseline finding and rejects new findings.
Existing feature regressions

TEST_PROTECTION_GAP_FOCUSED_TESTS: PASS
PHASE1_ROUTING_AND_NO_REPARSE_REGRESSION: PASS

VALIDATION OK:
architecture-review-warning-heuristic-resolver-async-sonar-v1

WARNING_HEURISTIC_RESOLVER_CORE: PASS
WARNING_HEURISTIC_RESOLVER_GUI_WIRING: PASS
WARNING_HEURISTIC_RESOLVER_READ_ONLY_PHASE1: PASS

VALIDATION OK:
architecture-review-warning-heuristic-resolver-v1

Subtabs:

VALIDATION OK: architecture-review-local-subtabs-v1
VALIDATION OK: architecture-review-local-subtabs-v1-runtime-repair-v1
VALIDATION OK: architecture-review-subtab-style-repair-v1
VALIDATION OK: architecture-review-subtab-height-compact-v1

Download

Patch:

kanda_warning_local_ai_resolver_v2

Feature ID:

architecture-review-warning-local-ai-resolver-v2

SHA-256:

cc8c833747bed697efbc62cef893f1ee0369554a8112376fc19ea1a1797f03cd

Place it at:

E:\kanda_warning_local_ai_resolver_v2.zip

Install

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "kanda_warning_local_ai_resolver_v2"

$EXPECTED_SHA256 = `
    "cc8c833747bed697efbc62cef893f1ee0369554a8112376fc19ea1a1797f03cd"

$ErrorActionPreference = "Stop"
$InstallFailed = $false

try {
    $ProjectPath = (Resolve-Path $PROJECT_ROOT).Path
    $ProjectName = Split-Path $ProjectPath -Leaf
    $DriveRoot = [System.IO.Path]::GetPathRoot($ProjectPath)

    $RootZip = Join-Path `
        $DriveRoot `
        ($PATCH_NAME + ".zip")

    $WorkDir = Join-Path `
        $DriveRoot `
        ($ProjectName + "_delete_after_daily_work")

    $LauncherDir = Join-Path `
        $WorkDir `
        ($PATCH_NAME + "_launcher")

    if (-not (Test-Path $RootZip)) {
        throw (
            "Patch ZIP not found: " +
            $RootZip
        )
    }

    $ActualHash = (
        Get-FileHash `
            -Path $RootZip `
            -Algorithm SHA256
    ).Hash.ToLowerInvariant()

    if (
        $ActualHash -ne
        $EXPECTED_SHA256.ToLowerInvariant()
    ) {
        throw (
            "ZIP SHA256 mismatch. Actual: " +
            $ActualHash
        )
    }

    Write-Host "PATCH ZIP SHA256: PASS"

    if (-not (Test-Path $WorkDir)) {
        New-Item `
            -ItemType Directory `
            -Path $WorkDir `
            -Force |
            Out-Null
    }

    if (Test-Path $LauncherDir) {
        Remove-Item `
            -Path $LauncherDir `
            -Recurse `
            -Force
    }

    New-Item `
        -ItemType Directory `
        -Path $LauncherDir `
        -Force |
        Out-Null

    Expand-Archive `
        -Path $RootZip `
        -DestinationPath $LauncherDir `
        -Force

    $InstallerPath = Join-Path `
        $LauncherDir `
        "INSTALL.ps1"

    if (-not (Test-Path $InstallerPath)) {
        throw "INSTALL.ps1 not found."
    }

    & powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $InstallerPath

    $ManifestPath = Join-Path `
        $LauncherDir `
        "PACKAGE_MANIFEST.json"

    $Manifest = Get-Content `
        -Path $ManifestPath `
        -Raw `
        -Encoding UTF8 |
        ConvertFrom-Json

    foreach ($Item in $Manifest.files) {
        $RelativePath = [string]$Item.path

        $InstalledPath = Join-Path `
            $ProjectPath `
            $RelativePath

        if (-not (Test-Path $InstalledPath)) {
            throw (
                "Installed file missing: " +
                $RelativePath
            )
        }

        $InstalledHash = (
            Get-FileHash `
                -Path $InstalledPath `
                -Algorithm SHA256
        ).Hash.ToLowerInvariant()

        $ExpectedHash = (
            [string]$Item.payload_sha256
        ).ToLowerInvariant()

        if ($InstalledHash -ne $ExpectedHash) {
            throw (
                "POST-INSTALL HASH MISMATCH: " +
                $RelativePath
            )
        }
    }

    Write-Host ""
    Write-Host "INSTALL PAYLOAD VERIFICATION: PASS"
}
catch {
    $InstallFailed = $true

    Write-Host ""
    Write-Host "INSTALL ERROR. Review the error below."
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
    Write-Host "INSTALL VERIFIED. Terminal will clear in 2 seconds..."
    Start-Sleep -Seconds 2
    Clear-Host
}

Validate

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "kanda_warning_local_ai_resolver_v2"

$ErrorActionPreference = "Stop"

try {
    $ProjectPath = (Resolve-Path $PROJECT_ROOT).Path
    $ProjectName = Split-Path $ProjectPath -Leaf
    $DriveRoot = [System.IO.Path]::GetPathRoot($ProjectPath)

    $WorkDir = Join-Path `
        $DriveRoot `
        ($ProjectName + "_delete_after_daily_work")

    $ExtractDir = Join-Path `
        $WorkDir `
        ($PATCH_NAME + "_extract")

    $ValidatePath = Join-Path `
        $ExtractDir `
        "VALIDATE.ps1"

    if (-not (Test-Path $ValidatePath)) {
        throw (
            "VALIDATE.ps1 not found: " +
            $ValidatePath
        )
    }

    & powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $ValidatePath
}
catch {
    Write-Host ""
    Write-Host "VALIDATION ERROR. Review the error below."
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host

The key final markers are:

VALIDATION OK:
architecture-review-warning-local-ai-resolver-v2

VALIDATION OK:
architecture-review-warning-local-ai-resolver-architecture-delta-v2

VALIDATION OK:
architecture-review-warning-heuristic-resolver-async-sonar-v1

VALIDATION OK:
architecture-review-warning-heuristic-resolver-v1

VALIDATION OK:
architecture-review-local-subtabs-v1

VALIDATION CHAIN COMPLETE:
architecture-review-warning-local-ai-resolver-v2

Important limitation

The v2 sandbox tests prove the architecture and acceptance gates, not that a real Ollama model will necessarily solve 20, 40, or 70 of your 80 findings.

The real outcome remains an empirical question:

v1 live:
1 solved / 80

versus:

v2 live:
unknown until run

My expectation is that v2 has a substantially better chance because it can now:

find a better existing test
OR
extend a real existing test
OR
create a focused behavioral test

instead of trying to solve almost every case through an existing-test link.

One security caveat: the production “sandbox” is a disposable project copy with bounded child processes and timeouts, not an OS/container security boundary. AI-generated tests are statically constrained and executed outside the GUI process, but the child Python process still runs with the Windows user's OS permissions.

check in your  logic where the found file candidates are updated and saved , because  I used qwen3-coder:30  it found 80 files 1 corrected, but after that I used  qwen2.5-coder:7b it found 80 files 1 corrected , but still 30 files. I believe local AI finds but do not  save correction. audit.

Vou auditar exatamente o fluxo candidate found → plan → human confirmation → apply → save → re-audit, porque o seu sintoma é consistente com uma destas falhas: o Local AI encontra proposta, mas ela não entra no plano aplicável; entra no plano, mas o writer não é chamado; ou escreve na cópia descartável e não promove para o projeto vivo.

Encontrei um ponto suspeito no writer: o resultado de aplicação conta len(selected_links) e len(mutations) como “aplicados”, mesmo quando rendered == original e nenhum arquivo entra em changed_files. Isso pode fazer a GUI dizer “1 corrigido” sem provar uma gravação real. Agora vou conferir o detector TEST_PROTECTION_GAP para ver se o tipo de link salvo é reconhecido no próximo audit.

Encontrei a causa principal no fluxo da GUI: o Local AI Resolver relê self._output.toPlainText(), ou seja, o texto antigo do audit que já estava na janela. Depois de aplicar uma correção, ele não roda um audit novo nem substitui a fila. Assim, o segundo modelo pode receber novamente os mesmos 80 findings antigos mesmo que um arquivo tenha sido corrigido no disco.

Yes — your suspicion was justified. I audited the actual resolver path from the uploaded source snapshot; the handoff confirms the collector completed and that the source archive is the correct artifact for exact code inspection.
Audit verdict

The Local AI does have a writer that can save corrections to the live project. However, the sequential workflow is flawed.

The biggest bug is:

    After applying a correction, the next Local AI run can process the old audit findings again instead of a fresh audit of the updated project.

This is exactly the type of serial-correction question already raised elsewhere in your project history: whether Local AI acts on the code after the previous correction or against the original state is a materially different workflow.

So I would not freeze the Resolver v2 in its current behavior.
What the code currently does
1. Local AI starts from the GUI text window

The current route effectively does:

run_warning_model_resolver()
        ↓
audit_text = self._output.toPlainText()
        ↓
resolve_warning_audit(audit_text)
        ↓
take 80 TEST_PROTECTION_GAP paths
        ↓
send them through heuristic + Local AI

The problem is that _output contains the previous audit plus appended resolver reports.

It is not guaranteed to be a newly generated Architecture Review audit.

So your sequence can currently behave like this:

AUDIT A
80 visible TEST_PROTECTION_GAP
        ↓
Qwen3-Coder
finds 1 safe correction
        ↓
human Yes
        ↓
test file may be written
        ↓
GUI appends result text

then:

Qwen2.5-Coder
        ↓
reads the same GUI output
        ↓
finds the original 80 WARNING lines
        ↓
processes 80 again

That directly explains why:

qwen3-coder:30b
80 analyzed
1 corrected

followed by:

qwen2.5-coder:7b
80 analyzed
1 corrected

does not necessarily mean that the first model's correction was lost.

The second model may simply be receiving the stale 80-item queue.
2. Where candidates are stored

The candidate flow is:

AI candidate
        ↓
ModelTestProtectionPlan
        ↓
in memory only

The AI decisions themselves are not maintained as a durable evolving correction queue.

They are not currently saved as something like:

run 1:
resolved:
- source A

remaining:
- source B
- source C
...

run 2 input:
only remaining paths

Instead, every resolver invocation reconstructs its work from the warning lines present in the text window.

That is the architectural defect.
3. Where actual corrections are saved

There are two application mechanisms.
Existing-test links

The writer changes the selected test file:

project root
    ↓
candidate test file
    ↓
backup
    ↓
temporary file
    ↓
os.replace()

For example:

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import exact.source.module as _test_protection_module

The Architecture Review detector's warning explicitly describes the problem as absence of a direct test import and recommends adding or linking a focused test that imports the module through its public contract.

Therefore, after a real write and a genuinely fresh audit, that exact source path should disappear from TEST_PROTECTION_GAP.
Generated or extended tests in v2

The v2 path is:

AI proposes test
        ↓
disposable copy
        ↓
pytest
        ↓
Architecture Review
        ↓
accepted proposal kept in plan
        ↓
human Yes
        ↓
apply_validated_model_test_changes()
        ↓
live project test path

So the promotion path does exist.

The fundamental missing piece is fresh post-apply live verification and queue replacement.
4. I found a second bug: “1 applied” can be misleading

This is serious.

The apply result currently derives success counters from the number of selected plan items.

Conceptually, the v1 path does:

applied_count = len(selected)

and the v2 path does:

linked_count = len(selected_links)

mutated_test_count = len(mutations)

But real filesystem writes are tracked separately:

changed_files

The writer also contains a legitimate no-op branch:

rendered == original
        ↓
continue
        ↓
no file write

Yet the selected item can still contribute to the reported count.

Therefore this is possible:

Local AI:
1 safe correction
        ↓
Apply
        ↓
selected_links = 1
        ↓
rendered == original
        ↓
changed_files = 0
        ↓
GUI can still report:
1 applied

That means “1 corrected” is not currently sufficient evidence that one live project file actually changed.

This is a real reporting bug.
My diagnosis of your exact sequence

Most likely:

Qwen3-Coder run
        ↓
80 stale/current warning identities
        ↓
1 candidate accepted
        ↓
possibly 1 real test file changed
        ↓
NO fresh audit

Qwen2.5-Coder run
        ↓
same old GUI audit lines
        ↓
80 items again
        ↓
1 candidate accepted

So I do not think the evidence proves:

AI found correction
but writer never saves anything

The more precise diagnosis is:

writer exists
+
correction may be saved
+
apply counters are unreliable
+
fresh audit is missing
+
queue is stale
+
second model may reprocess the original findings

Correct architecture

The workflow should be changed to this:

CLICK Warning Local AI Resolver
        ↓
RUN FRESH ARCHITECTURE AUDIT
        ↓
extract current TEST_PROTECTION_GAP identities
        ↓
Local AI
        ↓
candidate plan
        ↓
sandbox validation
        ↓
human confirmation
        ↓
live guarded write
        ↓
verify actual changed_files
        ↓
RUN FRESH ARCHITECTURE AUDIT AGAIN
        ↓
compare identities

BEFORE:
A B C D E

AFTER:
B C D E F

resolved:
A

still remaining:
B C D E

newly surfaced from suppression:
F
        ↓
next Local AI model receives:
B C D E F

Not:

model 1
        ↓
old 80

model 2
        ↓
same old 80

model 3
        ↓
same old 80

The counters also need correction

The result panel should show:

MODEL PLAN
Analyzed: 80
Proposed safe: 4
Sandbox validated: 2

LIVE APPLY
Requested writes: 2
Files actually changed: 2

FRESH AUDIT VERIFICATION
Resolved exact paths: 2
Still unresolved: 78
Newly surfaced from suppressed queue: 2
Current visible queue: 80

This is important because the detector has a visible finding cap. The total can remain at 80 while corrected paths disappear and previously suppressed paths surface.

So the correct success authority is:

exact path identity disappeared in fresh audit

not merely:

counter changed from 80 to 79

and definitely not:

plan said 1 corrected

Conclusion

Yes, there is a workflow bug.

The exact audit result is:

SAVE PATH EXISTS: YES

DURABLE EVOLVING AI QUEUE: NO

FRESH AUDIT BEFORE EACH AI MODEL: NO

FRESH LIVE AUDIT AFTER APPLY: NO

SECOND MODEL GUARANTEED TO USE UPDATED FINDINGS: NO

"APPLIED" COUNT GUARANTEED TO MEAN REAL FILE WRITE: NO

EXACT RESOLVED-PATH VERIFICATION: NO

My recommendation is a cumulative Resolver v2r1 State Refresh and Verified Apply Repair, without changing the AI prompt or test-generation strategy yet. The priority should be to fix the state machine so Qwen3 → Qwen2.5 → another model genuinely operates serially over the progressively updated project rather than repeatedly reviewing stale findings.

ERRORS:
- FREEZE BLOCKED - no recognizable validation evidence found in validation_evidence_summary.
---
freeze_id: "freeze-20260710-warning-local-ai-resolver-v2-semantic-evidence-and-disposable-test-generation"
feature_title: "Warning Local AI Resolver v2 - Semantic Evidence and Disposable Test Generation"
box: "kanda_reasoner_app/manage_architecture"
status: "frozen"
date: "2026-07-10"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260710-warning-local-ai-resolver-v2-semantic-evidence-and-disposable-test-generation.md"
protected_paths:
  - "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"
  - "kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py"
  - "kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py"
  - "kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py"
  - "kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py"
  - "kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py"
  - "kanda_reasoner_app/manage_architecture/warning_model_test_semantic_evidence.py"
  - "kanda_reasoner_app/manage_architecture/warning_model_test_generation_contract.py"
  - "kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py"
  - "kanda_reasoner_app/manage_architecture/warning_model_test_apply.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Warning Resolver split control remains exactly Heuristic and Local AI"
  - "the Local AI route consumes the existing top model selector and owns no second model selector."
  - "Explicit Ollama model selection remains exact and fail-closed"
  - "no silent fallback to another installed model is allowed."
  - "Heavy Local AI planning and validation remain off the GUI thread and use the existing shared QThread worker/controller lifecycle."
  - "Local AI v2 must emit visible reviewing progress before a blocking model call and must preserve sonar as presentation-only state."
  - "Existing-test linking remains allowed only for supplied candidate tests that satisfy deterministic behavioral relationship evidence."
  - "Local AI may propose extend_existing_test or create_focused_test only under the strict bounded JSON contract and exact governed paths."
  - "Generated or extended tests must contain real behavioral assertion/expected-exception evidence"
  - "import-only smoke tests and assert True silencers are rejected."
  - "AI test mutations are first overlaid only into a disposable project copy outside the canonical project root."
  - "A test mutation may become apply-eligible only after targeted pytest passes and fresh Architecture Review no longer reports TEST_PROTECTION_GAP for that source in the disposable copy."
  - "Pytest failure, timeout, malformed AI output, path invention, target collision, persistent Architecture Review gap, or insufficient evidence remain fail-closed Web AI outcomes."
  - "Accepted writes remain behind explicit human confirmation, exact SHA-256 freshness checks, backup, rollback support, and atomic replacement."
  - "AI-generated test code is never executed in the GUI process"
  - "validation occurs through bounded child Python processes in the disposable project copy."
  - "Feature-private state must not be cached as ad-hoc mutable state on the shared ArchitectureManagerWindow host."
  - "Architecture Review baseline findings may remain, but v2 must add zero new owner findings relative to the supplied v1 snapshot."
  - "Phase 1 routing, strict heuristic v3 evidence, async sonar lifecycle, split-control behavior, and local-subtab behavior must remain valid."
  - "Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260710-warning-local-ai-resolver-v2-semantic-evidence-and-disposable-test-generation

## freeze identity

Freeze ID: freeze-20260710-warning-local-ai-resolver-v2-semantic-evidence-and-disposable-test-generation

Feature title: Warning Local AI Resolver v2 - Semantic Evidence and Disposable Test Generation

Date: 2026-07-10

Primary box: kanda_reasoner_app/manage_architecture

Box type: tool_owned_architecture_governance

Status: frozen after explicit human confirmation and validation evidence

## summary

Built cumulatively over the uploaded current project snapshot plus the exact Warning Local AI Resolver v1 payload. V2 replaces raw-prefix/top-4-only review with AST-grounded semantic evidence, up to eight existing candidates, and bounded disposable-project validation of real test mutations. Freeze-intake data was loaded from <project>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake. Source patch ZIP: kanda_warning_local_ai_resolver_v2.zip.

## validated files

- kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py
- kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py
- kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py
- kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py
- kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py
- kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py
- kanda_reasoner_app/manage_architecture/warning_model_test_semantic_evidence.py
- kanda_reasoner_app/manage_architecture/warning_model_test_generation_contract.py
- kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py
- kanda_reasoner_app/manage_architecture/warning_model_test_apply.py
- tests/test_warning_model_test_protection_v2.py
- tests/test_warning_model_test_sandbox_validation.py
- tools/validate_architecture_review_warning_model_semantic_test_generation.py
- tools/validate_architecture_review_warning_model_semantic_test_generation_architecture_delta.py

## generated files

- kanda_reasoner_app/manage_architecture/warning_model_test_semantic_evidence.py
- kanda_reasoner_app/manage_architecture/warning_model_test_generation_contract.py
- kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py
- kanda_reasoner_app/manage_architecture/warning_model_test_apply.py
- tests/test_warning_model_test_protection_v2.py
- tests/test_warning_model_test_sandbox_validation.py
- tools/validate_architecture_review_warning_model_semantic_test_generation.py
- tools/validate_architecture_review_warning_model_semantic_test_generation_architecture_delta.py

## protected paths

- kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py
- kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py
- kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py
- kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py
- kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py
- kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py
- kanda_reasoner_app/manage_architecture/warning_model_test_semantic_evidence.py
- kanda_reasoner_app/manage_architecture/warning_model_test_generation_contract.py
- kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py
- kanda_reasoner_app/manage_architecture/warning_model_test_apply.py
- project_freeze_after_update/frozen_features_memory

## do-not-regress rules

- Warning Resolver split control remains exactly Heuristic and Local AI
- the Local AI route consumes the existing top model selector and owns no second model selector.
- Explicit Ollama model selection remains exact and fail-closed
- no silent fallback to another installed model is allowed.
- Heavy Local AI planning and validation remain off the GUI thread and use the existing shared QThread worker/controller lifecycle.
- Local AI v2 must emit visible reviewing progress before a blocking model call and must preserve sonar as presentation-only state.
- Existing-test linking remains allowed only for supplied candidate tests that satisfy deterministic behavioral relationship evidence.
- Local AI may propose extend_existing_test or create_focused_test only under the strict bounded JSON contract and exact governed paths.
- Generated or extended tests must contain real behavioral assertion/expected-exception evidence
- import-only smoke tests and assert True silencers are rejected.
- AI test mutations are first overlaid only into a disposable project copy outside the canonical project root.
- A test mutation may become apply-eligible only after targeted pytest passes and fresh Architecture Review no longer reports TEST_PROTECTION_GAP for that source in the disposable copy.
- Pytest failure, timeout, malformed AI output, path invention, target collision, persistent Architecture Review gap, or insufficient evidence remain fail-closed Web AI outcomes.
- Accepted writes remain behind explicit human confirmation, exact SHA-256 freshness checks, backup, rollback support, and atomic replacement.
- AI-generated test code is never executed in the GUI process
- validation occurs through bounded child Python processes in the disposable project copy.
- Feature-private state must not be cached as ad-hoc mutable state on the shared ArchitectureManagerWindow host.
- Architecture Review baseline findings may remain, but v2 must add zero new owner findings relative to the supplied v1 snapshot.
- Phase 1 routing, strict heuristic v3 evidence, async sonar lifecycle, split-control behavior, and local-subtab behavior must remain valid.
- Project-specific frozen memory must remain under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.
- Do not store project-specific frozen memory inside project_freeze_ledger.
- Preview Freeze Entry must remain read-only and must not write files.
- Confirm and Write must require explicit human confirmation before writing governed freeze memory.
- After a local freeze write, the AI startup freeze context must be refreshed.
- External AI review remains advanced/fallback, not the normal local freeze path.

## validation evidence

text
Sandbox focused validation passed AST semantic evidence extraction, richer candidate retrieval, real-test mutation contract, disposable project targeted pytest plus fresh Architecture Review confirmation, pre-chat progress, human confirmation gate, guarded apply writer, all v1 Warning Local AI runtime tests, new v2 semantic/generation tests, new sandbox validation tests, strict heuristic resolver regression, Phase 1 regression, local-subtab regressions, and Architecture Review owner delta checks. The reconstructed v1 snapshot and v2 implementation each reported 623 issues, 17 errors, and 606 warnings; the v2 new-owner finding count was zero and the one touched GUI baseline MIXED_RESPONSIBILITY_FILE finding remained unchanged.



## known warnings

Sandbox model behavior uses deterministic fake chat providers; the number of real findings solved by the user-selected Ollama model is unknown until live execution. The disposable project copy is a filesystem isolation boundary with subprocess timeouts, not an OS security container. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Warning Local AI Resolver v2 - Semantic Evidence and Disposable Test Generation. Human review is still required before Confirm and Write.

## planned next step

Install v2 over the exact v1 predecessor, run packaged validation, restart KANDA Reasoner, choose Warning Local AI Resolver, verify the selected top Ollama model, observe reviewing/pytest/audit progress, review safe links plus validated test changes, confirm only after inspecting the proposal, rerun Architecture Review, and freeze only after live acceptance evidence.

## local freeze writer provenance

Generated by 
local_freeze_writer_engine_v1 at 2026-07-10T12:39:09Z.

This entry was created locally for the selected active project. The reusable project_freeze_ledger engine remains blueprint logic only and is not the owner of this project-specific memory.

review theses errors and update  Resolver v1r1

Vou tratar isso como uma correção cumulativa Resolver v1r1 em duas frentes:

    reparar a evidência de validação para que o Freeze Preview reconheça os marcadores reais;

    corrigir o fluxo Local AI para usar audit fresco, contar apenas writes reais e verificar paths resolvidos após apply.
    Vou primeiro inspecionar o código exato do freeze intake/writer e do resolver atual antes de empacotar.

Já encontrei a lição exata no Error Memory: o erro de freeze é o paradigma conhecido em que a validação passa no terminal, mas o validation_evidence_summary continua com evidência não reconhecível porque o merge da evidência local não foi feito corretamente. Vou agora montar o v1r1 como correção cumulativa sobre o v2 instalado, incluindo o refresh de estado e contagem de writes reais.

O plano de correção está fechado:

    cada execução Local AI começa com Architecture Review fresco, não com _output.toPlainText();

    o apply passa a contar somente arquivos realmente alterados;

    após Yes, o apply + re-audit roda em background pelo mesmo lifecycle QThread;

    o resultado compara paths exatos before → after, mostrando resolvidos, ainda presentes e recém-expostos pela fila suprimida;

    o VALIDATE.ps1 passa a persistir UTF-8 e fazer o merge automático da evidência local no freeze hint antes de declarar freeze-ready.

Isso corrige tanto o erro de freeze quanto o bug serial Qwen3 → Qwen2.5.

Revisei os erros e atualizei o resolver.

Como a feature atual já é Warning Local AI Resolver v2, tratei a correção como v2r1, e não v1r1, para não criar uma regressão de nomenclatura.

O erro de Freeze que você mostrou corresponde exatamente ao padrão já registrado no Error Memory: a validação pode passar, mas o Freeze continua bloqueado quando a evidência local não é persistida e mesclada no validation_evidence_summary do freeze hint atual.
O que estava errado

A auditoria confirmou quatro problemas.
1. Freeze evidence incompleta

O v2 tinha no KANDA_FREEZE_HINT.json apenas uma narrativa como:

Sandbox focused validation passed AST semantic evidence extraction...

Mas o Freeze gate procura evidência reconhecível como:

VALIDATION OK: ...

Além disso, o VALIDATE.ps1 do v2:

rodava validators
        ↓
mostrava resultados no terminal
        ↓
terminava

mas não fazia automaticamente:

validation output
        ↓
UTF-8 evidence file
        ↓
merge_freeze_validation_evidence.py
        ↓
latest_freeze_hint.json

Esse é precisamente o paradigma do erro registrado anteriormente.
2. O próximo modelo podia receber novamente os mesmos 80 warnings

O código fazia:

audit_text = self._output.toPlainText()

Portanto:

Qwen3
    ↓
80 warnings
    ↓
1 proposta

Qwen2.5
    ↓
mesmo texto da janela
    ↓
mesmos 80 warnings novamente

O v2r1 não usa mais o texto da GUI como autoridade para a fila Local AI.

Agora:

CLICK Local AI Resolver
        ↓
background QThread
        ↓
FRESH Architecture Review
        ↓
extract current TEST_PROTECTION_GAP paths
        ↓
Local AI

3. “1 corrected” podia significar zero writes reais

O writer antigo contava:

linked_count = len(selected_links)
mutated_test_count = len(mutations)

mesmo quando:

rendered == original

e portanto nenhum arquivo era alterado.

Agora:

proposed correction
        ↓
rendered != original?
        │
        ├── NO
        │     └── applied count = 0
        │
        └── YES
              ↓
          real os.replace()
              ↓
          changed_files
              ↓
          actual applied count

4. Não havia verificação live após o apply

Agora, depois do Yes:

fresh audit before write
        ↓
verify requested gaps still exist
        ↓
stale?
    YES -> BLOCK BEFORE WRITE
        ↓
guarded apply
        ↓
fresh audit after write
        ↓
compare exact paths

O resultado agora mostra:

Files actually changed: 2

Exact source gaps verified resolved: 2

Requested source gaps still present: 0

Newly surfaced paths from fresh audit: 2

Isso resolve também o problema da fila suprimida: o total pode continuar em 80, mas agora sabemos exatamente quais paths desapareceram e quais novos paths foram revelados.
Novo fluxo serial correto

Agora uma sequência com vários modelos funciona assim:

Qwen3-Coder
        ↓
FRESH AUDIT A
        ↓
80 current gaps
        ↓
finds corrections
        ↓
human Yes
        ↓
actual writes
        ↓
FRESH AUDIT B
        ↓
exact resolved identities recorded


Qwen2.5-Coder
        ↓
FRESH AUDIT B
        ↓
receives CURRENT queue
        ↓
not original stale queue
        ↓
new corrections
        ↓
FRESH AUDIT C

Esse é o comportamento correto para testar modelos em sequência.
Freeze repair

O novo VALIDATE.ps1 agora faz:

validators
        ↓
collect output
        ↓
verify exact feature marker
        ↓
write UTF-8 without BOM
        ↓
re-read with strict UTF-8 decoder
        ↓
merge current evidence into matching freeze hint
        ↓
FREEZE_HINT_EVIDENCE_MERGE_OK

Testei o merge em uma fixture isolada. O latest_freeze_hint.json resultante recebeu:

PATCH_PAYLOAD_HASHES: PASS

WARNING_MODEL_FRESH_QUEUE_NOT_GUI_TEXT: PASS

WARNING_MODEL_ACTUAL_WRITE_COUNTS_ONLY: PASS

VALIDATION OK:
architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply

VALIDATION CHAIN COMPLETE:
architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply

FREEZE_HINT_EVIDENCE_MERGE_OK:
architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply

Validação realizada
Correção v2r1

WARNING_MODEL_V2R1_PYTHON_SYNTAX: PASS

WARNING_MODEL_V2R1_MODULE_SIZE_GATE: PASS

WARNING_MODEL_FRESH_QUEUE_NOT_GUI_TEXT: PASS

WARNING_MODEL_BACKGROUND_APPLY_VERIFY_QUEUE: PASS

WARNING_MODEL_SHARED_QTHREAD_FRESH_AUDIT_AND_VERIFY: PASS

WARNING_MODEL_ACTUAL_WRITE_COUNTS_ONLY: PASS

WARNING_MODEL_STATE_REFRESH_VERIFIED_APPLY_TESTS: PASS

VALIDATION OK:
architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply

Regressão do v2

WARNING_MODEL_RESOLVER_V2_AST_SEMANTIC_RETRIEVAL: PASS

WARNING_MODEL_RESOLVER_V2_REAL_TEST_GENERATION_FAIL_CLOSED: PASS

WARNING_MODEL_RESOLVER_V2_DISPOSABLE_PROJECT_PYTEST_AND_AUDIT: PASS

WARNING_MODEL_RESOLVER_V2_PRE_CHAT_PROGRESS: PASS

WARNING_MODEL_RESOLVER_V2_HUMAN_CONFIRMATION_GATE: PASS

WARNING_MODEL_RESOLVER_V2_FOCUSED_TESTS: PASS

VALIDATION OK:
architecture-review-warning-local-ai-resolver-v2

Architecture delta

WARNING_MODEL_RESOLVER_V2_BASELINE_FINDING_ALLOWLIST: PASS

WARNING_MODEL_RESOLVER_V2_NEW_OWNER_ARCHITECTURE_FINDINGS: 0

VALIDATION OK:
architecture-review-warning-local-ai-resolver-architecture-delta-v2

Heuristic resolver

WARNING_RESOLVER_ASYNC_QTHREAD: PASS

WARNING_RESOLVER_SONAR_COUNTERS: PASS

TEST_PROTECTION_GAP_FOCUSED_TESTS: PASS

PHASE1_ROUTING_AND_NO_REPARSE_REGRESSION: PASS

VALIDATION OK:
architecture-review-warning-heuristic-resolver-async-sonar-v1

Phase 1

WARNING_HEURISTIC_RESOLVER_CORE: PASS
WARNING_HEURISTIC_RESOLVER_GUI_WIRING: PASS
WARNING_HEURISTIC_RESOLVER_READ_ONLY_PHASE1: PASS

VALIDATION OK:
architecture-review-warning-heuristic-resolver-v1

Architecture self-audit

Baseline v2:

623 issues
17 errors
606 warnings

v2r1:

623 issues
17 errors
606 warnings

Portanto:

NEW ARCHITECTURE DELTA: 0

Patch

Patch:

kanda_warning_local_ai_resolver_v2r1

Feature ID:

architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply

SHA-256:

5cfa4b45d3237e66895df64e64a5c2775f48601e0322f37987cab0acdc181b40

Coloque em:

E:\kanda_warning_local_ai_resolver_v2r1.zip

Instalação

$PROJECT_ROOT = "E:\kanda_reasoner"
$PATCH_NAME = "kanda_warning_local_ai_resolver_v2r1"

$EXPECTED_SHA256 = `
    "5cfa4b45d3237e66895df64e64a5c2775f48601e0322f37987cab0acdc181b40"

$ErrorActionPreference = "Stop"
$LauncherFailed = $false

try {
    $ProjectPath = (Resolve-Path $PROJECT_ROOT).Path
    $DriveRoot = [System.IO.Path]::GetPathRoot($ProjectPath)

    $RootZip = Join-Path `
        $DriveRoot `
        ($PATCH_NAME + ".zip")

    $LauncherDir = Join-Path `
        $DriveRoot `
        (
            "kanda_reasoner_delete_after_daily_work\" +
            $PATCH_NAME +
            "_launcher"
        )

    if (-not (Test-Path $RootZip)) {
        throw (
            "Patch ZIP not found: " +
            $RootZip
        )
    }

    $ActualHash = (
        Get-FileHash `
            -Path $RootZip `
            -Algorithm SHA256
    ).Hash.ToLowerInvariant()

    if (
        $ActualHash -ne
        $EXPECTED_SHA256.ToLowerInvariant()
    ) {
        throw (
            "ZIP SHA256 mismatch. Actual: " +
            $ActualHash
        )
    }

    Write-Host "PATCH ZIP SHA256: PASS"

    if (Test-Path $LauncherDir) {
        Remove-Item `
            -Path $LauncherDir `
            -Recurse `
            -Force
    }

    New-Item `
        -ItemType Directory `
        -Path $LauncherDir `
        -Force |
        Out-Null

    Expand-Archive `
        -Path $RootZip `
        -DestinationPath $LauncherDir `
        -Force

    $InstallerPath = Join-Path `
        $LauncherDir `
        "INSTALL.ps1"

    if (-not (Test-Path $InstallerPath)) {
        throw "INSTALL.ps1 not found."
    }

    & powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $InstallerPath
}
catch {
    $LauncherFailed = $true

    Write-Host ""
    Write-Host "INSTALL LAUNCHER ERROR. Review the error below."
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }

    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
}

Resultado esperado:

PATCH ZIP SHA256: PASS

SOURCE FRESHNESS: PASS
PAYLOAD HASHES: PASS

PATCH FILE INSTALLATION: PASS
POST-INSTALL PAYLOAD HASHES: PASS

INSTALL OK. Terminal will clear in 2 seconds...

Validação + Freeze intake automático

Depois da instalação:

$PROJECT_ROOT = "E:\kanda_reasoner"

$PATCH_NAME = `
    "kanda_warning_local_ai_resolver_v2r1"

$ErrorActionPreference = "Stop"

try {
    $ProjectPath = (Resolve-Path $PROJECT_ROOT).Path
    $ProjectName = Split-Path $ProjectPath -Leaf
    $DriveRoot = [System.IO.Path]::GetPathRoot($ProjectPath)

    $WorkDir = Join-Path `
        $DriveRoot `
        ($ProjectName + "_delete_after_daily_work")

    $ExtractDir = Join-Path `
        $WorkDir `
        ($PATCH_NAME + "_extract")

    $ValidatePath = Join-Path `
        $ExtractDir `
        "VALIDATE.ps1"

    if (-not (Test-Path $ValidatePath)) {
        throw (
            "VALIDATE.ps1 not found: " +
            $ValidatePath
        )
    }

    & powershell `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $ValidatePath
}
catch {
    Write-Host ""
    Write-Host "VALIDATION ERROR. Review the error below."
    Write-Host $_.Exception.Message

    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
}

Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host

O final correto agora deve conter:

VALIDATION OK:
architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply

VALIDATION CHAIN COMPLETE:
architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply

VALIDATION_EVIDENCE_UTF8_CONTRACT: PASS

FREEZE_HINT_EVIDENCE_MERGE_OK:
architecture-review-warning-local-ai-resolver-v2r1-state-refresh-verified-apply

VALIDATION AND FREEZE HINT INTAKE: PASS

Somente depois desses marcadores o novo Freeze Preview deve ser usado.

O validation_evidence_summary do novo preview deve conter os marcadores reais, não apenas a narrativa de sandbox que causou o bloqueio anterior.


