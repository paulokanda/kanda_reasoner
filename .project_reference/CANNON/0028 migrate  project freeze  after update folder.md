first_prompts_to_ai.zip
Zip Archive
prompt_library.zip
Zip Archive
tell_AI_read_before_all.md
File

Vou carregar apenas o pacote de startup agora, seguindo a ordem indicada: primeiro o arquivo de leitura inicial, depois o ZIP de startup. O prompt_library.zip ficará reservado para prompts sob demanda.

STARTUP PACK LOAD CHECK

Files recognized:
0. 00_START_HERE_FOR_AI.md - loaded - startup entry point and mandatory routing/override bootstrap.

    01_ai_prompt_request_canon.md - loaded - defines how missing prompts, groups, folder cards, and behavior gates must be requested.

    02_prompt_navigation_index.md - loaded - maps task intent to prompt groups, specialist prompts, and routing paths.

    03_GROUP_ASSIMILATION_INDEX.md - loaded - provides broad group-level routing and assimilation guidance.

    04_FOLDER_ASSIMILATION_CARDS_INDEX.md - loaded - controls when folder-level cards should be loaded.

    05_start_of_day_master_stack.md - loaded - defines the minimal safe daily startup stack.

    06_session_start_upload_checklist.md - loaded - defines session upload, box logic, and implementation readiness checks.

    07_daily_patch_delivery_guardrails.md - loaded - governs patch delivery, validation, install, and release safeguards.

    08_handoff_at_end_of_work.md - loaded - defines required end-of-work handoff behavior.

    09_patch_install_delivery_error_register.md - loaded - records patch/install delivery failure patterns and prevention rules.

    10_prompt_router_reasoner_startup_check.md - loaded - defines router startup readiness checks.

    11_chatgpt_kanda_routing_choice_output_protocol.md - loaded - defines prompt-library ZIP direct retrieval protocol.

    12_error_memory_ai_formulary_startup_canon.md - loaded - governs Error Memory formulary output after mistakes or failures.

    09_active_project_freeze_context.md - loaded - exposes read-only active project frozen-feature context.

    README_STARTUP_PROMPT_REQUEST_KERNEL.md - loaded - describes the startup pack purpose, source rules, and upload workflow.

    STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json - loaded - provides generation metadata, source mapping, and sync manifest.

Startup status:
COMPLETE

Routing behavior:
Startup routing is active. The startup ZIP was inspected in the required order after the read-before-all instruction. The prompt_library.zip is available as the canonical on-demand prompt source, but it was not opened at startup; it should be opened only when routing selects a specific prompt path that is not already present in the startup ZIP. Governed work must use the routing gates, required prompt groups, folder cards, validation rules, freeze rules, patch delivery guards, and anti-bypass behavior before implementation.

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

Recebi o segundo grupo do projeto. Vou verificar o status do coletor, o handoff principal, os arquivos compactos de Error Memory e o ZIP de handoff antes de marcar o projeto como pronto.

PROJECT READY CHECK

Project slug:
kanda_reasoner

Active project root:
E:\kanda_reasoner

KANDA tool root:
E:\kanda_reasoner_show_project_to_AI

Same physical root: NO

Compact Error Memory loaded:
YES. 10 active lessons loaded; full Error Memory ZIP not opened because the compact manifest says it should be opened only when needed.

Second-upload handoff loaded:
YES. Collector status is complete, ZIP export is complete, and the handoff upload ZIP was read in the required order.

Tier-1 gates active:
YES. Source summaries are orientation only; exact source files must still be inspected before any edit. Patch delivery, validation, freeze, Error Memory, and startup-routing gates remain active.

Next action:
WAIT_FOR_TASK

I want to know  how  safe is transfer folder project_freeze_after_update from <project folder> , in our case project forlder is  kanda_reasoner but project_freeze_after_update folder is dinamic and related to project  not to kanda_reasoner tool . I want E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update  that is to say logic must continue dinamic drive_where_project_is:\<project>_show_project_to_AI\project_freeze_after_update.

is it simple operation, because  are lot of  paths to be adjusted?

Vou tratar isso como análise de arquitetura, não como patch ainda. Vou checar o handoff e procurar referências reais a project_freeze_after_update para estimar se é uma mudança localizada ou espalhada.

Já encontrei um ponto importante: hoje existe um helper central para project_freeze_after_update em freeze_after_update/paths.py, mas também há referências diretas espalhadas em contrato de intake, startup freeze context, GUI/help, validações e prompts. Ou seja, não é só mover a pasta no Explorer.

Yes, your idea is architecturally reasonable, but it is not a simple folder transfer.

Moving:

E:\kanda_reasoner\project_freeze_after_update

to:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

with dynamic logic:

<drive_where_project_is>:\<project_name>_show_project_to_AI\project_freeze_after_update

is probably the better long-term boundary, because project_freeze_after_update is project-specific state, not KANDA Reasoner source code. But doing it safely requires updating several subsystems.

I inspected the handoff/source context and found that the current architecture still assumes this canonical source:

<active_project_root>\project_freeze_after_update\

especially for:

project_freeze_after_update\frozen_features_memory\
project_freeze_after_update\freeze_hint_intake\

The second upload package also confirms that source summaries are only routing/evidence and exact source must be inspected before editing, so this should be treated as a governed architecture change, not a manual folder move.
My assessment

Safety if done manually by moving the folder: low to moderate.
It can break freeze lookup, startup freeze context, Confirm and Write, freeze hint intake, validation scripts, and prompts that still tell the AI the old path.

Safety if done by adding a central resolver + migration compatibility: high.
The right implementation is not “replace strings everywhere”; it is to create one canonical path resolver:

freeze_state_root_for_project(project_root)
    -> <drive>:\<project_name>_show_project_to_AI\project_freeze_after_update

Then all freeze-memory code should call that resolver.
Is it simple?

Conceptually: yes.
Implementation-wise: medium complexity, not huge, but not tiny.

The core change is simple:

Old:
project_root / "project_freeze_after_update"

New:
show_project_to_ai_root_from_hint(project_root) / "project_freeze_after_update"

But the path is referenced in multiple layers:
Area	Risk
freeze_after_update/paths.py	central public path builder currently points inside project root
freeze_hint_intake/contract.py	uses hardcoded intake/index/entries paths
startup freeze context	reads freeze memory from active project root
GUI tab/help text	displays and opens old folder
freeze writer / generator / exposure tools	likely expect old project-root location
validation scripts	assert old path exists
prompt-library governance text	repeatedly says freeze memory belongs under <project_root>/project_freeze_after_update
Show Project to AI / source archive	must not accidentally delete or ignore new persistent freeze memory

So the operation is not dangerous if routed correctly, but it is not safe as a raw folder move.
The safest migration strategy

I would do it in phases.
Phase 1: Add compatibility resolver

Create one canonical helper, probably near existing path infrastructure:

kanda_reasoner_app/project_analysis_evidence_paths.py

or in:

kanda_reasoner_app/freeze_after_update/paths.py

The helper should resolve:

E:\kanda_reasoner

to:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

It should also work for any external project:

D:\my_project
-> D:\my_project_show_project_to_AI\project_freeze_after_update

This keeps the dynamic rule project-based, not KANDA-tool-based.
Phase 2: Read old + write new temporarily

For safety, first patch should support:

read preferred new path
fallback read old path if new path missing
write only to new path

That prevents losing the existing freeze memory.
Phase 3: Migration command

Add a guarded migration:

old: <project_root>\project_freeze_after_update
new: <drive>:\<project>_show_project_to_AI\project_freeze_after_update

Rules:

If old exists and new does not exist:
    copy/migrate old to new
    do not delete old immediately

If both exist:
    do not auto-merge silently
    report conflict and require review

If new exists:
    use new as canonical

I would not delete the old folder in the first patch. At most, after validation, rename it to something like:

project_freeze_after_update_migrated_backup_YYYYMMDD

only after the new path is validated.
Phase 4: Update startup and validation

The startup freeze context must say the source is now:

<drive>:\<project>_show_project_to_AI\project_freeze_after_update\frozen_features_memory

not:

<active_project_root>\project_freeze_after_update\frozen_features_memory

Validation should prove:

old in-source folder is not required
new external folder is used
frozen_features_memory is found
freeze_hint_intake is found
Confirm and Write writes to new location
startup freeze context reads new location
Show Project to AI does not delete the folder

The biggest risk

The biggest risk is that _show_project_to_AI is currently treated partly as generated/export infrastructure. If we place persistent freeze memory there, we must explicitly mark:

<project>_show_project_to_AI\project_freeze_after_update

as persistent project state, not disposable generated output.

That is the most important boundary rule.

It should be similar to:

<project>_show_project_to_AI\project_error_memory

which is already project-related external state in the handoff system. The compact Error Memory manifest says compact Error Memory is always read and the full archive is only opened when needed, reinforcing that some project-specific state already lives outside the source tree and is loaded selectively.
My recommendation

Do not manually move the folder yet.

The safest implementation is:

1. Add central freeze storage resolver.
2. Make all freeze code use it.
3. Add old-path fallback.
4. Add migration validation.
5. Update GUI labels/help.
6. Update startup freeze context.
7. Update prompt/governance text after source validation.
8. Only then migrate existing folder.

So my answer is:

It is safe as a designed migration. It is not safe as a simple folder move.

I would classify it as a medium-sized governed architecture patch, not a risky rewrite. The logic is clear; the work is mostly making every consumer use the same resolver instead of scattered old path assumptions.

creat a handoff of what you intend to do and ask for suggestions to other AI , say to ai she is an specialist in the field with 20 year of experience

Here is a copy-paste handoff you can send to another AI:

You are a senior software architecture specialist with 20 years of experience in Python desktop applications, project-state management, migration design, validation architecture, and safe path refactoring.

I want your opinion before implementing a path/storage migration in my project.

Context:
The active project is:

E:\kanda_reasoner

There is a project-specific state folder currently located at:

E:\kanda_reasoner\project_freeze_after_update

This folder is not really part of the application source code. It stores project-specific freeze/update state, especially:

project_freeze_after_update\frozen_features_memory
project_freeze_after_update\freeze_hint_intake

The problem:
This folder is currently inside the project source root, but conceptually it belongs to the generated project-support/state area.

I want to move the canonical location to:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

More generally, the intended dynamic rule is:

<drive_where_project_is>:<project_name>_show_project_to_AI\project_freeze_after_update

Example:

E:\kanda_reasoner
-> E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

D:\my_project
-> D:\my_project_show_project_to_AI\project_freeze_after_update

Important architectural clarification:
The folder project_freeze_after_update is dynamic and project-related. It is not specifically tied to the KANDA Reasoner tool. Therefore, the resolver should derive the freeze-state root from the active project root, not from a hardcoded KANDA tool path.

Current concern:
I suspect there are many path assumptions still pointing to:

<active_project_root>\project_freeze_after_update

The path may be referenced in multiple areas, including:

    freeze_after_update path helpers

    freeze hint intake contract

    frozen feature memory reader/writer

    Confirm and Write workflow

    startup freeze context

    GUI labels/help text

    validation scripts

    prompt/governance text

    Show Project to AI export/handoff logic

    tests that assert old paths

My intended implementation:
I do not want to simply move the folder manually.

I intend to implement this as a safe migration:

    Create or update a central resolver function.

The resolver should take the active project root and return:

<drive>:<project_name>_show_project_to_AI\project_freeze_after_update

For example:

freeze_state_root_for_project("E:\kanda_reasoner")
-> "E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update"

    Make all freeze-related code use this central resolver.

The goal is to avoid scattered string replacements and prevent future drift.

    Add compatibility fallback.

During migration:

    Read from the new canonical location first.

    If the new location does not exist, optionally read from the old location.

    Write only to the new canonical location.

    Do not delete the old folder automatically.

    Add a guarded migration routine.

Suggested behavior:

    If old exists and new does not exist:
    copy old to new
    validate new
    keep old as backup

    If both old and new exist:
    do not merge silently
    report conflict
    require user review

    If only new exists:
    use new as canonical

    Update GUI/help/user-facing text.

Anywhere the app shows or explains freeze paths should reflect the new canonical location.

    Update startup freeze context.

Startup should read frozen feature memory from:

<drive>:<project_name>_show_project_to_AI\project_freeze_after_update\frozen_features_memory

not from:

<active_project_root>\project_freeze_after_update\frozen_features_memory

    Update validation.

Validation should prove:

    The new dynamic path is resolved correctly.

    Existing freeze entries are found after migration.

    Confirm and Write writes to the new location.

    freeze_hint_intake works in the new location.

    startup freeze context reads the new location.

    old in-project path is not required for normal operation.

    if old and new both exist, the system does not silently overwrite or merge.

    Show Project to AI does not treat the new folder as disposable generated output.

    Preserve safety boundaries.

The new folder must be considered persistent project state, even though it lives under:

<project_name>_show_project_to_AI

This is important because that area may otherwise be treated as generated/export infrastructure. The new project_freeze_after_update folder must not be deleted by cleanup/export routines.

My current assessment:
This is not a safe manual folder move.

It is probably a medium-sized architecture patch:

    conceptually simple

    technically moderate

    path-sensitive

    validation-sensitive

    governance-sensitive

Main question for you:
As a specialist with 20 years of experience, do you agree with this migration approach?

Please review and suggest improvements, especially around:

    Best resolver function design.

    Whether new path should live under <project>_show_project_to_AI or another sibling folder.

    How to avoid accidental deletion of persistent state.

    How to structure old-path fallback safely.

    How to handle conflict when both old and new folders exist.

    What validations are mandatory before considering this safe.

    What files/subsystems are most likely to break.

    Whether the migration should happen in one patch or multiple smaller patches.

    Whether prompts/governance text should be updated in the same patch or after code validation.

    Any better architecture you recommend.

Please be critical. I do not want just agreement. I want risk analysis and a safer implementation plan if you see weaknesses.

Good clarification — that changes my assessment meaningfully, and I was wrong to treat the whole folder as a single disposable bucket. If _show_project_to_AI is actually the general external project-infrastructure root (everything that supports building the project but isn't the project's own source), with disposable install/patch staging as just one category living inside it alongside other categories, then nesting project_freeze_after_update there as a sibling category is architecturally reasonable. I retract the "don't put persistent state inside the export folder" objection as stated — the export folder isn't what I thought it was.
But this reframing sharpens rather than removes the real risk, and I want to be precise about what actually needs to change in the plan now.
What the clarification fixes, and what it doesn't
It fixes the conceptual objection — there's no longer a category mismatch between "this folder means disposable" and "I'm putting persistent state in it." But it doesn't fix the mechanical risk I was actually worried about underneath that: a future cleanup routine still has no way to know, by inspecting the folder tree, which children are safe to delete and which aren't — unless that distinction is made structural, not just understood by you and described in a chat. The danger isn't the parent folder's name; it's that "persistent" vs "disposable" currently only exists as a fact in your head and in this conversation, not as something the code can check.
Revised recommendation
Keep project_freeze_after_update under _show_project_to_AI, but make the lifecycle distinction explicit at the subfolder level, with a single manifest as source of truth:
<project>_show_project_to_AI\
  _lifecycle_manifest.json
  second_prompt_files\          <- disposable
  install_and_patch\            <- disposable
  project_freeze_after_update\  <- persistent
  project_error_memory\         <- persistent (same convention as Error Memory audit)
json// _lifecycle_manifest.json
{
  "persistent": ["project_freeze_after_update", "project_error_memory"],
  "disposable": ["second_prompt_files", "install_and_patch"]
}
Rule: any cleanup/reset utility must read this manifest before deleting anything under the root, and must refuse to delete a subfolder not listed as disposable, rather than defaulting to "delete everything except a hardcoded exception list." This is the same goal as my earlier sentinel-file idea, just done once at the manifest level instead of needing a marker file duplicated into every persistent subfolder — cleaner, and it also gives you one place to see the whole lifecycle map at a glance, which is useful documentation in its own right.
One more implication of your clarification worth surfacing: if _show_project_to_AI is genuinely general build-infrastructure now, not narrowly "AI export," the name itself may undersell what it holds — that's a naming question, not a safety one, so I'd treat it as optional and separate from this migration rather than bundling a rename into an already path-sensitive patch.
With that adjustment, my view on your original 10 points stands as written — resolver design, fallback, conflict handling, phased patches, prompts-after-code — except point 2 (destination) is now: yes, _show_project_to_AI\project_freeze_after_update is fine, conditioned on the manifest-driven persistent/disposable split being implemented in the same migration, not deferred. Without that condition, you're back to the original risk, just one level deeper in the tree.


As a senior architect, I applaud your instinct to centralize the resolver and implement a copy-not-move migration with conflict detection. You are absolutely right that a manual folder move is unacceptable.

However, I must raise a critical architectural red flag regarding your chosen destination. I will then dissect your 10 points with a brutally honest risk analysis and propose a safer, more maintainable architecture.
🚩 The Big Red Flag: _show_project_to_AI is the WRONG sibling

Your proposal places persistent, mutable, runtime state inside a folder semantically defined as "export/handoff/generated infrastructure."

    _show_project_to_AI is where you put ephemeral exports to feed the AI context.

    Cleanup scripts, export routines, and AI-handoff logic will (and should) treat this folder as disposable or regenerable.

    If you place critical freeze-state in there, you are guaranteeing a future disaster where a handoff cleanup routine deletes your persistent freeze memory.

Architectural Fix: Create a dedicated persistence sibling.
Do not use _show_project_to_AI. Use:

    E:\kanda_reasoner_state\project_freeze_after_update

    or E:\kanda_reasoner_persistence\freeze

    or follow XDG standards: %APPDATA%\KANDA_Reasoner\projects\kanda_reasoner\freeze.

Given your dynamic rule, I strongly suggest:
<drive>:<project_name>_state\project_freeze_after_update.
This semantically separates "runtime persistent state" from "AI handoff ephemera."
Deep-Dive Risk Analysis & Answers to Your 10 Points
1. Best Resolver Function Design

Do not just write a standalone function. Write a ProjectStateResolver class that caches the resolved path to avoid repeated disk I/O and string manipulation.
python

from pathlib import Path
from functools import lru_cache

class ProjectStateResolver:
    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
    
    @lru_cache(maxsize=1)
    def get_freeze_root(self) -> Path:
        # Explicitly avoid _show_project_to_AI
        return self.project_root.parent / (self.project_root.name + "_state") / "project_freeze_after_update"
    
    def get_legacy_freeze_root(self) -> Path:
        # The old in-source location
        return self.project_root / "project_freeze_after_update"

Critical improvement: The resolver must never use string concatenation like f"{drive}:{name}". Always use pathlib.Path.parent to guarantee OS-agnostic behavior.
2. New Path Location (Reiterated)

Verdict: Absolutely reject _show_project_to_AI. Use _state or _persistence.
Why? If you use _show_project_to_AI, any "Clean Project for AI Export" feature will inevitably nuke your freeze history.
3. How to Avoid Accidental Deletion of Persistent State

Add a "Canary File" to the new root.
When the resolver creates the new directory, it must write a .state_root_guard file containing: "PERSISTENT_PROJECT_STATE_DO_NOT_DELETE".
Then, modify your cleanup/export routines to explicitly skip any directory containing this guard file. This makes accidental deletion programmatically impossible.
4. How to Structure Old-Path Fallback Safely

Implement dual-read, single-write.
python

def read_freeze_file(filename: str) -> dict | None:
    # 1. Try canonical first
    canonical = resolver.get_freeze_root() / filename
    if canonical.exists():
        return load(canonical)
    # 2. Fallback to legacy
    legacy = resolver.get_legacy_freeze_root() / filename
    if legacy.exists():
        log_warning(f"Reading from LEGACY path: {legacy}. Please migrate.")
        return load(legacy)
    return None

Crucially: The write_freeze_file function must only write to the canonical path. This slowly starves the legacy path of updates without breaking existing reads.
5. Conflict Handling (Both Old and New Exist)

Your "do not merge silently" is 100% correct. But you need a tiered strategy:

    State 1 (Ambiguous): If canonical exists AND legacy exists. App starts, logs a CRITICAL warning, and chooses the canonical path as the source of truth (because it is the newer path).

    State 2 (Migration CLI): Provide a CLI command kanda migrate-freeze-state --resolve-conflict. When run:

        Compare last-modified timestamps.

        Offer options: --keep-new (default), --overwrite-new-from-old (force), or --abort.

        Never do an automatic union merge, as Freeze IDs might collide silently.

6. Mandatory Validations (Before Considered Safe)

You must pass these 5 gates before calling this done:

    Atomic Copy: The migration must copy the legacy folder to a temporary folder (_migrate_temp) first, validate its JSON structure, then rename it to the canonical path. This prevents a half-copied corrupted state.

    Write-Access Test: The resolver must attempt to create a ._test_write file in the canonical path on app startup. If it fails, the app must fall back to the legacy path and warn the user about permission issues.

    Checksum Manifest: Generate a checksums.sha256 of all migrated .json files during migration. Validate against this on every app start to catch disk corruption.

    Schema Version Gate: Before reading any freeze file, check the schema_version inside it. If the migration copied a corrupt JSON, the app crashes gracefully with "Corrupt Freeze State detected."

    Path Sanitization: Ensure the canonical path is not a subdirectory of the project root (to prevent recursive infinite loops during exports).

7. What Files/Subsystems Are Most Likely to Break (The Hit List)

With absolute certainty, these will fail first:

    Hardcoded GUI Labels: Some status bar might read Status: Freeze saved at ./project_freeze_after_update.

    Confirm and Write workflow: It likely uses os.path.join(project_root, "project_freeze_after_update") in a deep, un-refactored helper.

    Unit Test Fixtures: Tests often assert exact paths like assert "project_freeze_after_update" in freeze_path. They will break.

    Show Project to AI Export logic: It may have an explicit exclude_folders = ["project_freeze_after_update"] that currently works. When you move it, the exclusion list is useless, and the exporter might accidentally include the new persistent state in the AI handoff ZIP. You must explicitly add the new path to the exclusion list.

8. One Patch or Multiple Smaller Patches?

One atomic patch, but with a feature flag.
Scattering this over multiple patches creates a "twilight zone" where the resolver exists but the callers haven't been updated, or vice versa.
Implementation: One PR, but wrap the new resolver initialization in an environment variable KANDA_USE_STATE_SIBLING=1. Merge the code with the flag off (still using legacy paths). Turn the flag on, test, fix bugs, then remove the flag in a hotfix. This is production-safe.
9. Prompt/Governance Text Update: Before or After?

Strictly AFTER code validation.
If you update the governance text/prompts first, the AI will "know" the new path and might start suggesting it in discussions, but the application code won't support it yet. This causes cognitive dissonance.
Order: Code Patch -> Integration Tests Pass -> Update tell_AI_read_before_all.md and governance to reflect the new canonical state location.
10. Better Architecture I Recommend (Beyond this patch)

You are treating this as a "path migration." I see this as a symptom of a missing abstraction.
Implement a ProjectStateManager (Singleton):
python

class ProjectStateManager:
    def __init__(self, project_root):
        self.root = project_root
        self._resolver = ProjectStateResolver(project_root)
    
    @property
    def freeze(self): return FreezeStore(self._resolver)
    @property
    def error_memory(self): return ErrorMemoryStore(self._resolver)
    @property
    def lessons(self): return LessonStore(self._resolver)

Now, no subsystem ever constructs a path. They simply call StateManager.freeze.load("feature_x").
This completely decouples your application logic from the filesystem path. In 5 years, if you move to a SQLite database for state, you only change the FreezeStore internals; the GUI and validators don't change a single line.
The Safer Migration Implementation Plan

    Phase 0 (Prep): Write the ProjectStateResolver with the _state sibling.

    Phase 1 (Refactor): Replace all direct os.path.join(project_root, "project_freeze_after_update") with resolver.get_freeze_root().

    Phase 2 (Legacy Bridge): Implement the fallback reader (reads legacy, writes canonical).

    Phase 3 (Gate): Add the checksum and .state_root_guard canary file.

    Phase 4 (Migration CLI): Add kanda migrate-freeze command that uses shutil.copytree with dirs_exist_ok=False (to force failure if new exists) and copies with verification.

    Phase 5 (Exclusion): Update the Show Project to AI export logic to explicitly exclude the new _state sibling.

    Phase 6 (Validation): Write a test called test_freeze_state_independence that deletes the legacy folder, restarts the app, and proves the app reads/writes exclusively from the new canonical path without crashing.

Final Verdict

I agree with your methodology (resolver + copy-not-move + conflict detection), but I strongly veto your destination (_show_project_to_AI).

The risk of a persistent-state wipe due to a handoff-cleanup script is too high. Move it to a dedicated _state sibling, enforce the canary-guard file, and wrap it all in a centralized ProjectStateManager abstraction. If you follow this, this is a low-risk, high-value architectural fix that will make your project far more robust. If you stick with _show_project_to_AI, you are planting a time bomb for your future self.


audit these opinions

Vou auditar isso em duas camadas: primeiro a lógica arquitetural das duas opiniões; depois, contra o que já sabemos do handoff/projeto, vou separar o que deve entrar no patch inicial do que seria exagero ou risco de escopo.

I audited both opinions. My verdict: the corrected first opinion is the best direction; the second opinion has useful safety warnings, but its hard veto against _show_project_to_AI is not valid for your current architecture, because Error Memory already uses that exact external root pattern.
Bottom line

I would keep the destination as:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

with dynamic rule:

<drive_where_project_is>:\<project_name>_show_project_to_AI\project_freeze_after_update

But I would not implement it as just “add this folder there.” I would implement it as:

show_project_to_AI root
+ lifecycle manifest
+ central resolver
+ cleanup guard update
+ path-hint normalization update
+ old-read/new-write migration
+ validation

The second AI was right about one thing: the risk is not the folder name itself. The risk is that the code must know which children are persistent and which are disposable.
What the second AI got wrong

The second AI says _show_project_to_AI is “wrong” because it is disposable/export-only. That does not match the current project evidence.

Your current Error Memory already uses:

E:\kanda_reasoner_show_project_to_AI\project_error_memory

as the canonical persistent Error Memory root. The uploaded Error Memory manifest explicitly identifies that as the canonical store.

The handoff system also treats _show_project_to_AI as a broader project-support root, not merely a throwaway folder: it contains second_prompt_files, Error Memory exports, source archive packages, and generated handoff artifacts. The handoff readme says the full Error Memory archive is separately generated and opened only when needed, while compact Error Memory is part of the normal project upload flow.

So I reject the second AI’s hard recommendation to move to:

E:\kanda_reasoner_state

or:

%APPDATA%\KANDA_Reasoner\...

That would create a second external-state convention and make the architecture less coherent.
What the second AI got right

The second AI correctly identified the real danger: cleanup and export code must never treat persistent state as disposable.

This is especially relevant because the current startup/governance text still says freeze-intake state belongs under:

<active_project_root>\project_freeze_after_update\freeze_hint_intake

and frozen memory under:

<active_project_root>\project_freeze_after_update\frozen_features_memory

That rule is explicitly present in the current startup contract, so this migration is a governed path change, not a simple internal refactor.
My corrected architecture recommendation

Use this structure:

E:\kanda_reasoner_show_project_to_AI\
  _lifecycle_manifest.json
  first_prompt_files\
  second_prompt_files\
  second_prompt_files_building\
  project_error_memory\
  project_freeze_after_update\

With manifest:

{
  "schema_version": "1.0",
  "persistent": [
    "project_error_memory",
    "project_freeze_after_update"
  ],
  "disposable": [
    "first_prompt_files",
    "second_prompt_files",
    "second_prompt_files_building",
    "json_splitted"
  ]
}

Important rule:

Cleanup may delete only folders explicitly listed as disposable.
Cleanup must skip persistent folders.
Unknown folders should be skipped, not deleted.

That is better than only a canary file. A canary file is okay as a secondary protection, but the parent lifecycle manifest should be the main source of truth.
Important source-level risks I found

From the source inspection, there are several real path assumptions that would need patching:

    freeze_after_update/paths.py currently builds:

project_root / "project_freeze_after_update"

This must become resolver-based.

    freeze_hint_intake/contract.py currently has:

INTAKE_REL = Path("project_freeze_after_update") / "freeze_hint_intake"

and builds intake under the active project root. This must move to the external project infrastructure root.

    startup_freeze_context.py currently fingerprints and renders freeze memory as:

<active_project_root>/project_freeze_after_update/frozen_features_memory

This must change, or startup will read stale/empty freeze memory after migration.

    The current _show_project_to_AI helper recognizes children like:

first_prompt_files
second_prompt_files
project_error_memory
json_splitted

It does not appear to recognize project_freeze_after_update yet. If not updated, giving the GUI or resolver a freeze-folder hint could accidentally derive nonsense such as:

project_freeze_after_update_show_project_to_AI

That is one of the most important details.

    Cleanup logic currently has allowed Show Project children like:

first_prompt_files
second_prompt_files
project_error_memory

It should add project_freeze_after_update, but better: replace or supplement this with the lifecycle manifest.
Audit of the proposed ideas
Idea	My audit
Keep freeze state under _show_project_to_AI	Yes, because Error Memory already uses this convention.
Add lifecycle manifest	Yes, strongly recommended. This is the key correction.
Add canary file	Useful, but secondary. Manifest is cleaner.
Use _state sibling instead	I would not do this now. It fragments architecture.
Dual-read, single-write	Yes. Read new first, fallback to old, write new only.
Conflict detection if both old/new exist	Yes. No silent merge.
Checksum manifest on every startup	Probably overkill. Use migration validation, not constant checksum policing.
Feature flag	Probably unnecessary for local desktop app if validation is strong.
ProjectStateManager singleton	Good future direction, but too broad for this patch. Use resolver first.
Prompt/governance updates after code validation	Mostly yes, but startup freeze context code must be updated in the same governed migration because otherwise startup becomes wrong.
Best implementation plan

I would do one governed migration patch, but limited in scope.

Patch should include:

1. Add central project infrastructure resolver, probably reusing show_project_to_ai_root_from_hint.
2. Add resolve_project_freeze_after_update_root(project_root).
3. Add lifecycle manifest creation/validation under *_show_project_to_AI.
4. Add project_freeze_after_update to accepted show-project children.
5. Update freeze_after_update path builder to use the new root.
6. Update freeze_hint_intake path builder to use the new root.
7. Update startup_freeze_context to read/fingerprint the new root.
8. Update cleanup_show_project_to_ai_root_after_success so it preserves persistent children.
9. Add old-path fallback readers.
10. Add migration validation.

I would not include a broad ProjectStateManager in this patch. That is a second architecture refactor.
Final decision

The safest final architecture is:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

not:

E:\kanda_reasoner_state\project_freeze_after_update

But only if the same patch adds explicit lifecycle protection for _show_project_to_AI.

So the answer is:

First corrected opinion wins. Second opinion’s safety concern is valid, but its destination veto is wrong for this project.

also audit sites specialized in python and programming architecture for strategies to implement this folder position update with maximun safety and minimun risk. bring just what is a real gain to this implementatino

Vou buscar apenas fontes úteis para reduzir risco real nesta migração: documentação Python oficial para filesystem/atomicidade, padrões de migração/feature flags e práticas de backup/cleanup seguro. Depois vou filtrar o que realmente muda o patch.

I audited Python/programming architecture sources and filtered out anything that does not give real gain for this migration.
Best external lessons to apply
1. Use “branch by abstraction,” not mass path replacement

The real gain is to create a single path abstraction seam first, then move callers to it. This matches the branch-by-abstraction strategy: large internal changes are safer when the system keeps working while implementation is swapped behind an abstraction.

For us, that means:

resolve_show_project_to_ai_root(project_root)
resolve_project_freeze_after_update_root(project_root)
resolve_legacy_project_freeze_after_update_root(project_root)

Then every freeze subsystem must call the resolver. Avoid scattered string edits like:

project_root / "project_freeze_after_update"

Real gain: one testable seam, less regression risk, easier future migration.
2. Treat this as data migration, not just refactor

Fowler’s migration warning applies directly: data migrations look simple but usually contain messy edge cases, so they should be tested incrementally and not left as a one-time manual operation.

For us, the migration must be code-backed:

old path:
E:\kanda_reasoner\project_freeze_after_update

new path:
E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

Use this policy:

read new first
fallback read old
write new only
never silently delete old
never silently merge old and new

Real gain: existing freeze entries keep working while the new canonical path becomes active.
3. Use copytree(..., dirs_exist_ok=False) for migration

Python’s shutil.copytree() raises FileExistsError by default if the destination already exists, while dirs_exist_ok=True may overwrite files inside the destination.

So for this patch, the safer rule is:

shutil.copytree(old_root, temp_new_root, dirs_exist_ok=False)

Then validate the copied content before promoting it.

Do not use:

dirs_exist_ok=True

for freeze-memory migration.

Real gain: prevents accidental overwrite of an already-existing new freeze state.
4. Do not rely on “atomic move” for directory migration

Python’s os.replace() can be atomic if successful, but it may fail across filesystems, and replacing non-empty directories is not a safe general strategy. Python’s docs also note that os.rename() may fail across filesystems and recommends shutil.move() when cross-filesystem movement is needed.

Your dynamic rule keeps old and new on the same drive:

E:\kanda_reasoner
E:\kanda_reasoner_show_project_to_AI

so we should avoid cross-drive complexity. But even on the same drive, I would not “replace” a freeze directory. I would do:

copy old -> temp folder
validate temp
rename temp -> final only if final does not exist
keep old untouched

Real gain: avoids half-migrated or overwritten freeze memory.
5. Use atomic file writes for small control files

For small files such as:

_lifecycle_manifest.json
migration_report.json
freeze_root_state.json

use the standard safe pattern:

write temp file in same directory
flush/close
os.replace(temp, final)

os.replace() is the right primitive for cross-platform overwrite of a file when the source and destination are on the same filesystem.

Real gain: prevents corrupted manifest/control files if the app crashes mid-write.
6. Centralize deletion behind a lifecycle manifest

Python’s shutil.rmtree() is powerful and recursively deletes directory trees; the docs also highlight platform-specific safety details around symlinks/junctions. So cleanup must not be scattered across the codebase.

Use:

{
  "schema_version": "1.0",
  "persistent": [
    "project_error_memory",
    "project_freeze_after_update"
  ],
  "disposable": [
    "first_prompt_files",
    "second_prompt_files",
    "second_prompt_files_building",
    "install_and_patch",
    "json_splitted"
  ]
}

Cleanup rule:

Delete only children listed as disposable.
Skip persistent children.
Skip unknown children.
Never delete the root itself.

This also fits your existing architecture because current project artifacts already place persistent Error Memory under:

E:\kanda_reasoner_show_project_to_AI\project_error_memory

Real gain: prevents future cleanup routines from deleting freeze memory.
7. Use a temporary canary/dry-run mode, not a permanent feature flag

Feature toggles can help deliver changes safely, but they add validation complexity and carrying cost if they remain around. Google SRE’s canary guidance is more useful here: expose a change to a small controlled path first, evaluate it, then expand.

For this local desktop app, I would not add a long-term environment flag. Instead add a validation-only mode:

--dry-run-freeze-root-migration

or a validation script that simulates:

old only
new only
both old and new
neither
cleanup attempt
startup freeze-context read
Confirm and Write write target

Real gain: canary safety without long-term feature-flag debt.
What I would add to the patch because of this audit

Only these items give real value:

1. Central resolver seam.
2. Lifecycle manifest under <project>_show_project_to_AI.
3. Cleanup must delete disposable-listed children only.
4. Old-read/new-write compatibility.
5. Migration copy through temp directory with dirs_exist_ok=False.
6. Atomic writes for lifecycle/migration metadata.
7. Conflict detection when both old and new freeze roots exist.
8. Validation-only dry-run/canary test.
9. Startup freeze-context validation must require STATUS: IN_SYNC.

The current startup contract already requires freeze paths and startup sync behavior to be governed, so this migration must also update the freeze path rules and validate startup sync after code changes.
What I would not add now

I would not add these to the first patch:

1. Full ProjectStateManager singleton.
2. New <project>_state sibling folder.
3. Checksums on every app start.
4. Permanent feature flag.
5. SQLite or database-backed freeze storage.
6. Automatic deletion or renaming of the old folder.
7. Silent merge if old and new both exist.

Those either increase scope or add maintenance burden without reducing the main migration risk.
Final refined implementation strategy

The safest high-value version is:

E:\kanda_reasoner_show_project_to_AI\
  _lifecycle_manifest.json
  project_error_memory\
  project_freeze_after_update\
  second_prompt_files\
  first_prompt_files\

Canonical freeze root:

<drive_where_project_is>:\<project_name>_show_project_to_AI\project_freeze_after_update

Migration behavior:

If new exists:
    use new

If new missing and old exists:
    read old as fallback
    migration tool copies old -> temp -> validate -> new
    keep old untouched

If both exist:
    use new as canonical
    warn/report conflict
    do not merge silently

If neither exists:
    create new canonical root

Validation must prove:

resolver returns the correct dynamic path
legacy fallback works
writes go only to new path
Confirm and Write writes new path
freeze_hint_intake uses new path
frozen_features_memory uses new path
startup freeze context reads new path
cleanup preserves persistent folders
old path is no longer required
STATUS: IN_SYNC is printed after validation

My updated verdict: keep _show_project_to_AI, but make lifecycle explicit and code-enforced in the same migration patch.

now write down the complete organized updated safe migration process , to , each time we start a chat you will know exactly what to do based in this doc. 

Here is the updated migration document to paste at the start of future chats after the project startup/handoff files are loaded. It is based on the current project handoff model, where _show_project_to_AI is a broader external project-support root and Error Memory already lives there as project-specific external state. The second-upload readme confirms this upload/handoff structure, and the Error Memory manifest confirms that project_error_memory is canonical external project state.
Safe Migration Handoff: Move project_freeze_after_update to the external project-support root
1. Purpose

We need to safely migrate the project-specific freeze/update state folder:

Old location:

E:\kanda_reasoner\project_freeze_after_update

New canonical location:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

General dynamic rule:

<drive_where_project_is>:<project_name>_show_project_to_AI\project_freeze_after_update

Examples:

E:\kanda_reasoner
-> E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

D:\my_project
-> D:\my_project_show_project_to_AI\project_freeze_after_update

This folder is dynamic and project-related. It is not specifically tied to the KANDA Reasoner tool source code.

The goal is to move project freeze state out of the active project source root and into the external project-support root, alongside other external project state such as project_error_memory.

This is not a manual folder move. It is a governed architecture migration.
2. Core architectural decision

The canonical freeze root should become:

<project>_show_project_to_AI\project_freeze_after_update

not:

<project_root>\project_freeze_after_update

and not a separate new sibling such as:

<project>_state

Reason:

The current architecture already uses:

<project>_show_project_to_AI\project_error_memory

as project-specific external state. Therefore, placing:

<project>_show_project_to_AI\project_freeze_after_update

as a sibling persistent project-state category is coherent.

However, the external project-support root must explicitly distinguish persistent folders from disposable/generated folders.
3. Safety principle

The main risk is not the folder name.

The main risk is accidental deletion or incorrect cleanup because the code may not know which folders under:

<project>_show_project_to_AI

are persistent and which are disposable.

Therefore, the migration must add a lifecycle rule that code can enforce.
4. Required external project-support root lifecycle manifest

Create or maintain this file:

<project>_show_project_to_AI_lifecycle_manifest.json

Suggested schema:

{
"schema_version": "1.0",
"persistent": [
"project_error_memory",
"project_freeze_after_update"
],
"disposable": [
"first_prompt_files",
"second_prompt_files",
"second_prompt_files_building",
"install_and_patch",
"json_splitted"
]
}

Cleanup rule:

    Cleanup may delete only children explicitly listed under "disposable".

    Cleanup must skip children listed under "persistent".

    Cleanup must skip unknown children by default.

    Cleanup must never delete the external project-support root itself.

    Cleanup must never use a broad "delete everything except hardcoded exceptions" strategy.

    If the lifecycle manifest is missing or invalid, cleanup must fail closed or enter dry-run/report-only mode.

Optional secondary guard:

Inside persistent roots, create a small guard file such as:

.project_state_guard

containing plain text:

PERSISTENT_PROJECT_STATE_DO_NOT_DELETE

This is secondary. The lifecycle manifest is the main source of truth.
5. Scope of migration

The migration affects at least these logical areas:

    Freeze path resolver.

    Freeze Feature After Update paths.

    Freeze hint intake paths.

    Frozen feature memory paths.

    Confirm and Write workflow.

    Startup freeze context.

    GUI labels and help text that display freeze paths.

    Validation scripts that assert freeze paths.

    Cleanup routines for <project>_show_project_to_AI.

    Show Project to AI folder-hint normalization and root derivation.

    Prompt/governance text that still says freeze memory belongs under <active_project_root>\project_freeze_after_update.

    Tests that expect the old path.

Before editing, inspect exact source files. Handoff summaries are orientation only, not source truth.
6. Implementation strategy

Use branch-by-abstraction style.

Do not mass-replace strings everywhere.

Create one central resolver seam first, then make all callers use it.

Required resolver functions:

resolve_show_project_to_ai_root(project_root_or_hint)

resolve_project_freeze_after_update_root(project_root_or_hint)

resolve_legacy_project_freeze_after_update_root(project_root_or_hint)

Expected behavior:

Given:

E:\kanda_reasoner

resolve_show_project_to_ai_root returns:

E:\kanda_reasoner_show_project_to_AI

resolve_project_freeze_after_update_root returns:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

resolve_legacy_project_freeze_after_update_root returns:

E:\kanda_reasoner\project_freeze_after_update

Important:

Use pathlib.Path operations. Avoid manual string concatenation whenever possible.
7. Path normalization requirement

The existing project-support-root derivation must understand that these are children of the show-project root:

first_prompt_files
second_prompt_files
second_prompt_files_building
project_error_memory
project_freeze_after_update
json_splitted
install_and_patch

This prevents a bad derivation such as:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update
-> E:\project_freeze_after_update_show_project_to_AI

or similar nonsense.

The resolver must be able to accept either:

    The active project root.

    The external project-support root.

    A known child inside the external project-support root.

and still return the correct project-support root.
8. Read/write migration policy

Use dual-read, single-write.

Read order:

    Try the new canonical path first:

<project>_show_project_to_AI\project_freeze_after_update

    If the new path is missing or lacks the requested file, optionally fall back to the legacy path:

<project_root>\project_freeze_after_update

Write rule:

All new writes must go only to the new canonical path.

Never write new freeze data to the legacy project-root path.

Never silently merge old and new data.

Never delete the old path automatically.
9. Conflict handling

Possible states:
State A: New exists, old missing

Use new canonical path.

No migration needed.
State B: New missing, old exists

Use legacy as read fallback.

Provide or run a guarded migration routine that copies old to new.

Keep old untouched as backup after migration.
State C: Both new and old exist

Use new as canonical.

Report conflict.

Do not silently merge.

Do not overwrite new from old.

Do not delete old.

Validation should surface this state clearly.
State D: Neither exists

Create new canonical root and required subfolders.
10. Migration routine

The migration routine must be copy-not-move.

Recommended steps:

    Resolve active project root.

    Resolve old freeze root.

    Resolve new freeze root.

    Ensure lifecycle manifest exists and marks project_freeze_after_update as persistent.

    If new root exists, stop migration and report conflict or already-migrated state.

    If old root does not exist, create new root normally.

    If old root exists and new root does not exist:
    a. Copy old root to a temporary migration folder under the same parent as new root.
    b. Use a temp name such as:

    project_freeze_after_update.migration_tmp

    c. Use copytree with destination-not-existing behavior.
    d. Validate copied contents.
    e. Rename temp folder to final new root.
    f. Leave old root untouched.
    g. Write a migration report file to the new root.

Do not use dirs_exist_ok=True for this migration.

Do not merge into an existing new root.

Do not perform destructive deletion.
11. Atomic write policy for control files

For small control files, use atomic file write pattern:

    Write to a temp file in the same directory.

    Flush and close.

    Replace final file using os.replace.

Apply this to:

_lifecycle_manifest.json
migration_report.json
any freeze root state file
any new metadata file used by the migration

Reason:

This prevents corrupted manifest/control files after crash or interruption.
12. Cleanup safety

Update cleanup logic for:

<project>_show_project_to_AI

so it uses the lifecycle manifest.

Cleanup must:

    Read _lifecycle_manifest.json.

    Delete only children listed in "disposable".

    Skip "persistent".

    Skip unknown.

    Report skipped unknown children.

    Never delete project_freeze_after_update.

    Never delete project_error_memory.

    Fail closed if lifecycle manifest is missing or invalid.

This lifecycle rule must be implemented in the same migration patch, not deferred.

Without this, placing project_freeze_after_update under _show_project_to_AI is not safe enough.
13. Specific source areas to inspect and likely patch

Before implementing, inspect the real source files. The exact names may differ, but the likely areas are:

    freeze_after_update/paths.py

Look for:

project_root / "project_freeze_after_update"

Replace with the new resolver.

    freeze_hint_intake/contract.py

Look for path constants like:

Path("project_freeze_after_update") / "freeze_hint_intake"

Update to use the external project-support root.

    startup_freeze_context.py

Update rendering, fingerprinting, and reading logic from:

<active_project_root>\project_freeze_after_update\frozen_features_memory

to:

<project>_show_project_to_AI\project_freeze_after_update\frozen_features_memory

    Confirm and Write workflow

Make sure actual local freeze writes go to the new root.

Preview remains read-only.

Confirm and Write remains explicitly human-confirmed.

    GUI/help text

Update displayed path descriptions so the user sees the new canonical folder.

    Show Project to AI root helper

Make sure project_freeze_after_update is recognized as a project-support-root child.

    Cleanup/export logic

Make sure cleanup is manifest-driven and cannot delete persistent folders.

    Validation scripts

Add or update tests for resolver, fallback, migration, startup sync, cleanup, and Confirm and Write.

    Prompt/governance text

Only update after code validation, except startup freeze context behavior must be updated in the same governed migration because startup would otherwise read the wrong location.
14. Validation requirements

A patch is not complete unless validation proves:

    Dynamic resolver correctness:

E:\kanda_reasoner
-> E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

    External root child normalization:

A path inside:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

still resolves back to:

E:\kanda_reasoner_show_project_to_AI

    Legacy fallback works:

If only old path exists, readers can still find existing freeze entries.

    Writes go only to new canonical path.

    Confirm and Write writes to:

<project>_show_project_to_AI\project_freeze_after_update

    freeze_hint_intake uses:

<project>_show_project_to_AI\project_freeze_after_update\freeze_hint_intake

    frozen_features_memory uses:

<project>_show_project_to_AI\project_freeze_after_update\frozen_features_memory

    startup freeze context reads the new path.

    cleanup preserves persistent folders.

    cleanup deletes only disposable-listed folders.

    if old and new both exist, the system reports conflict and does not merge.

    if lifecycle manifest is missing or invalid, cleanup does not proceed destructively.

    old in-project path is not required for normal operation after migration.

    validation output includes the required success marker.

    validation output includes:

STATUS: IN_SYNC

when startup sync or freeze context sync is part of the validation contract.
15. Error Memory lessons to respect

Before coding, run the Error Memory check.

Relevant lessons likely include:

    validation-output-status-in-sync-required
    Avoid freezing or considering sync complete without STATUS: IN_SYNC when required.

    freeze-code intake and form protocol
    Freeze-ready patches must include accurate freeze metadata and must not use stale feature titles or validation lists.

    patch install delivery error register
    Patch ZIP delivery must follow the current safe install and validation contract.

    prompt-router bridge / active-ready correction lessons
    Do not handcraft active Error Memory JSON from memory if Error Memory correction is needed.

The full Error Memory ZIP should not be opened by default. Open it only if compact lessons are insufficient, repeated-error debugging is involved, or the current plan conflicts with a prior lesson.
16. Patch scope recommendation

Do this as one governed migration patch, but keep the scope tight.

Include in the patch:

    Central resolver seam.

    Lifecycle manifest support.

    Cleanup protection.

    New canonical freeze path.

    Legacy read fallback.

    Copy-not-move migration routine or validation utility.

    Startup freeze context update.

    Confirm and Write path update.

    freeze_hint_intake path update.

    Validation.

Do not include in the first patch:

    Full ProjectStateManager singleton.

    SQLite/database migration.

    New <project>_state sibling.

    Permanent feature flag.

    Checksums on every app startup.

    Automatic deletion of the old folder.

    Automatic silent merge of old and new roots.

    Broad unrelated refactors.

    Rename of _show_project_to_AI.

These are either over-scope or create avoidable risk.
17. Required routing classification for future chats

When this task is resumed, classify it as:

Governed architecture/path migration for project freeze-state storage and startup freeze context.

Fast Path or Routed Work Path:

Routed Work Path.

Required context:

    Current startup pack already loaded.

    Second-upload project handoff already loaded.

    Compact Error Memory loaded.

    Exact source files inspected before editing.

    Freeze Feature After Update source files.

    Show Project to AI source files.

    Startup freeze context source files.

    Cleanup/export source files.

    Validation command or manual validation plan.

    Patch delivery and validation guardrails.

    Freeze code intake protocol if delivering freeze-ready patch metadata.

Do not implement directly from memory.
18. First steps for the next AI session

After STARTUP PACK LOAD CHECK and PROJECT READY CHECK are complete, do this:

    Return an ERROR MEMORY CHECK.

    Search exact source for:

project_freeze_after_update
frozen_features_memory
freeze_hint_intake
project_error_memory
show_project_to_AI
_show_project_to_AI
cleanup_show_project_to_ai
startup_freeze_context
Confirm and Write
KANDA_FREEZE_HINT
_lifecycle_manifest

    Identify all path constructors and cleanup routines.

    Build a patch plan before modifying files.

    Confirm that the patch preserves:
    a. read-only Preview
    b. explicit human Confirm and Write
    c. no automatic freeze write bypass
    d. no deletion of old freeze folder
    e. no deletion of persistent external state

19. Expected final behavior after successful migration

After the migration patch:

Active project root:

E:\kanda_reasoner

External project-support root:

E:\kanda_reasoner_show_project_to_AI

Canonical freeze state root:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update

Freeze hint intake:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update\freeze_hint_intake

Frozen feature memory:

E:\kanda_reasoner_show_project_to_AI\project_freeze_after_update\frozen_features_memory

The old folder:

E:\kanda_reasoner\project_freeze_after_update

may still exist as backup or legacy fallback, but new writes must not go there.
20. Final implementation rule

This migration is safe only if all of the following are true:

    There is one central resolver for the new freeze root.

    All freeze-related code uses the resolver.

    The external project-support root has a lifecycle manifest.

    Cleanup is lifecycle-manifest-driven.

    Persistent folders are protected.

    Old-path read fallback exists during transition.

    New writes go only to the new canonical path.

    Existing old data is copied, not moved.

    Conflict states are reported, not silently merged.

    Startup freeze context reads the new path.

    Validation proves the above.

    Validation prints STATUS: IN_SYNC when required.

Do not treat this as a simple folder move.
Do not manually move/delete folders before the resolver and validation are in place.
Do not update governance prompts to the new path before code support exists, except for startup freeze context behavior included in the governed migration patch.


