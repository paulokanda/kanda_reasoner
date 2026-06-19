# Project Folder Organization Canon

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Universal. Platform-agnostic. Framework-agnostic. AI-assisted or human-led.

Use this canon at the start of any software project before implementation. Its purpose is to keep the application clean, maintainable, patchable, validatable, and ready for future compilation or packaging.

This canon applies to Python, JavaScript, TypeScript, Rust, Go, C#, Java, desktop apps, web apps, CLI tools, mobile apps, compiled apps, Dockerized apps, and AI-assisted codebases.

---

## 1. Core principle

Every file belongs to exactly one responsibility zone.

No zone should pollute another.

The source tree must remain clean enough that compilation, packaging, testing, and auditing are predictable.

Before writing, moving, deleting, generating, or packaging any file, classify it.

The application source tree is not a dumping ground for:

* temporary files
* backups
* restore copies
* generated audit/evidence
* build outputs
* runtime output
* user data
* secrets
* downloaded external project files
* caches
* patch debris
* failed migrations

---

## 2. Required Step 0 before implementation

Before any code is written or any folder is created, the AI must produce:

1. Folder policy table.
2. Project-specific resolved paths.
3. Mode declaration: `dev`, `ci`, `production`, `docker`, or `mixed`.
4. Platform declaration: `windows`, `macos`, `linux`, or `cross-platform`.
5. App name and safe app slug.
6. Source root declaration.
7. Maintenance root declaration.
8. Build output model declaration.
9. User data location declaration.
10. Log location declaration.
11. Secret policy declaration.
12. External project/evidence policy, if applicable.
13. Generated-intentional source allowlist.
14. `.gitignore` baseline, if version control is used.
15. `.buildignore` or packaging exclusion baseline.
16. Risk list for this project.
17. Validation plan.
18. Implementation roadmap.
19. One-patch-per-gate rule.
20. Human acknowledgement before implementation.

Do not implement before Step 0 is clear.

---

## 3. Canonical responsibility zones

| Zone | Name                           |          Allowed inside source? | Purpose                                                               |
| ---- | ------------------------------ | ------------------------------: | --------------------------------------------------------------------- |
| 1    | Application source             |                             Yes | Source code, tests, docs, config, templates, required assets          |
| 2    | Development workbench          |                   Yes, dev only | Active development notes, patch manifests, experiments                |
| 3    | Generated-intentional source   |                   Yes, declared | Lock files, generated clients, compiled protos, i18n outputs          |
| 4    | App maintenance root           |                              No | Backups, restore points, scratch, quarantine, logs, migration records |
| 5    | Build/packaging output         | No, unless framework convention | Binaries, installers, bundles, release candidates                     |
| 6    | Logs                           |                              No | Runtime, install, patch, audit, CI logs                               |
| 7    | User data                      |                              No | Settings, local database, saved sessions, user documents              |
| 8    | Runtime generated output       |                              No | Exports, reports, transformed data generated during use               |
| 9    | External project evidence      |                              No | Audit/evidence files for projects managed or analyzed by the app      |
| 10   | External project snapshots     |                              No | Cloned/downloaded copies of external projects                         |
| 11   | Patch backups and restore data |                              No | Before-patch copies and rollback data                                 |
| 12   | Quarantine                     |                              No | Unknown, risky, stale, or manually reviewed debris                    |
| 13   | Secrets and credentials        |                           Never | API keys, tokens, passwords, certificates, private keys               |
| 14   | CI/CD workspace                |                              No | Pipeline-only workspace files                                         |
| 15   | Plugins/extensions             |                      Usually no | User-installed add-ons or extension bundles                           |
| 16   | Crash dumps/screenshots        |                   No by default | Diagnostics, bug reports, visual evidence                             |
| 17   | Staging                        |                              No | Files awaiting classification during migration                        |

---

## 4. Application source root

Placeholder:

```text
<APP_ROOT>
```

Allowed inside `<APP_ROOT>`:

```text
source code
tests
docs
project configuration
templates
static assets required by the app
intentional scripts
README and project metadata
small non-sensitive fixtures
development workbench, if intentionally part of the workflow
generated-intentional source, if declared in allowlist
```

Not allowed inside `<APP_ROOT>` before compilation:

```text
*.bak
*.backup
*_old.*
*_deprecated.*
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
.eslintcache
.parcel-cache
node_modules, unless framework convention and excluded
dist, unless framework convention and excluded
build, unless framework convention and excluded
temporary extraction folders
patch backups
restore copies
failed patch payloads
generated audit/evidence output
external project outputs
runtime output
large logs
user data
secrets
compiled binaries
installer outputs
local machine-specific files
```

The source root should pass source-cleanliness validation and compilation-readiness validation.

---

## 5. App maintenance root

Use `APP_MAINTENANCE_ROOT` as the primary name.

`APP_TEMP_ROOT` may be used only as a compatibility alias.

Purpose:

```text
APP_MAINTENANCE_ROOT = app-owned non-source maintenance area
```

It stores:

```text
patch backups
restore points
quarantine
scratch files
temporary extraction
install logs
runtime logs when not user-data
failed patch payloads
build outputs for simple projects
migration state
legacy absorbed folders
crash dumps if diagnostic
```

Resolution priority:

```text
1. Explicit project config setting
2. Environment variable: APP_MAINTENANCE_ROOT
3. Mode/platform default
4. Sibling of source: <APP_ROOT>/../_<app_slug>_maintenance
5. Last-resort platform temp fallback
```

Rules:

```text
never hardcode drive letters
never hardcode user names
never scatter multiple temp roots
never place maintenance root inside source unless explicitly approved and ignored
never package maintenance root into compiled builds
```

Suggested structure:

```text
<APP_MAINTENANCE_ROOT>/
    backups/
        patches/
        restore/
        pre_commit/
        failed_patches/
    scratch/
        extracts/
        cache/
        temp_work/
        downloads/
    quarantine/
        manual/
        autodelete/
    logs/
        install/
        runtime/
        audit/
        migration/
    build/
    releases/
    migration/
        legacy_absorbed/
        migrated_evidence/
        migration_state.json
        audit.jsonl
    diagnostics/
        crash_dumps/
        screenshots/
    staging/
```

`backups`, `restore`, `quarantine`, and `migration` are persistent until explicitly cleaned.

`scratch` is disposable and may be purged automatically according to policy.

---

## 6. Build output policy

Choose one model during Step 0.

Model A: simple project

```text
<APP_MAINTENANCE_ROOT>/build/
<APP_MAINTENANCE_ROOT>/releases/
```

Model B: formal release pipeline

```text
<APP_BUILD_ROOT>/
```

Use Model B when:

```text
releases are versioned formally
CI/CD produces artifacts
outputs are large
multiple OS targets exist
signed installers are produced
release candidates must be archived
```

Build outputs include:

```text
compiled binaries
installers
bundles
release candidates
distribution packages
build logs
intermediate build folders
```

Build output must not be shipped accidentally inside source packages.

---

## 7. Logs policy

Logs should be classified by purpose.

Suggested destinations:

```text
development logs -> <APP_MAINTENANCE_ROOT>/logs/install or logs/audit
patch/install logs -> <APP_MAINTENANCE_ROOT>/logs/install
migration logs -> <APP_MAINTENANCE_ROOT>/logs/migration
runtime logs -> <APP_USER_DATA_ROOT>/logs or <APP_MAINTENANCE_ROOT>/logs/runtime
CI logs -> CI workspace or pipeline log sink
crash logs -> <APP_MAINTENANCE_ROOT>/diagnostics/crash_dumps
```

Large logs must not be committed or packaged unless explicitly required.

Logs must not contain secrets.

---

## 8. User data policy

User data must not live inside source.

User data includes:

```text
settings
local databases
saved sessions
user documents
preferences
application state
local history
non-source persistent data
```

Platform defaults:

```text
Windows:
%APPDATA%/<AppName> or %LOCALAPPDATA%/<AppName>

macOS:
~/Library/Application Support/<AppName>

Linux:
~/.local/share/<app-name> or $XDG_DATA_HOME/<app-name>

CLI config:
~/.config/<app-name> or $XDG_CONFIG_HOME/<app-name>
```

The project may override these defaults, but the override must be declared.

---

## 9. Secrets policy

Secrets must never appear in:

```text
source tree
logs
generated evidence
build output
compiled packages
committed config files
debug dumps
screenshots
handoff bundles
```

Secrets include:

```text
API keys
tokens
passwords
private keys
certificates
database credentials
OAuth secrets
cloud credentials
private user data
```

Preferred locations:

```text
environment variables
OS credential store
secret manager
ignored local config file for development only
CI/CD secret store
```

A secret policy must be declared before config files are created.

Secret scan must run before:

```text
build
release
evidence generation
handoff bundle creation
external sharing
```

---

## 10. External project evidence policy

This applies when the app analyzes, audits, migrates, edits, or manages another project.

Generated evidence for an external project must not be written into that external project's source tree unless the user explicitly requests it.

Resolution priority:

```text
1. User-configured external evidence workspace
2. Adjacent-to-target-project pattern
3. Same drive/base as target project
4. App maintenance fallback if target drive/base is unwritable
```

Pattern:

```text
<external_project_base>/<external_project_slug>_<artifact_domain>/
```

Examples:

```text
D:/client_app_architecture_audit/
E:/legacy_project_migration_report/
/home/user/projects/my_project_analysis_evidence/
```

Preferred folder structure:

```text
<external_project_slug>_<artifact_domain>/
    current/
        <external_project_slug>__active_snapshot.json
        <external_project_slug>__bundle_manifest.json
        <external_project_slug>__complete.json
        <external_project_slug>__complete_runtime_trace.json
        <external_project_slug>__exclusion_rules.json
        <external_project_slug>__file_manifest.json
        <external_project_slug>__reconstruction_payload.json
        <external_project_slug>__validation_state.json
        EVIDENCE_README.md
        EVIDENCE_MANIFEST.json
    runs/
        YYYY-MM-DD_HH-MM-SS/
            same structure as current
```

Rules:

```text
project slug must be dynamic
do not hardcode the app name as project name
use double underscore between project slug and artifact name
evidence for different projects must never mix
valid evidence is not debris
stale evidence may move to maintenance/migration/migrated_evidence with confirmation
external evidence folders must not be included in compiled app builds
```

`EVIDENCE_MANIFEST.json` should include:

```json
{
  "generated_by_app": "<app_name>",
  "generated_by_version": "<app_version>",
  "generated_at": "<ISO8601 timestamp>",
  "source_project_root": "<absolute path>",
  "source_project_slug": "<slug>",
  "artifact_domain": "<artifact_domain>",
  "artifact_list": [],
  "current_or_run": "current",
  "can_regenerate": true
}
```

`EVIDENCE_README.md` should explain:

```text
what this folder is
which app generated it
which project it describes
how to regenerate it
whether it is safe to delete
where current and historical runs live
```

---

## 11. Mode-specific path behavior

Declare the mode during Step 0.

### Dev mode

```text
workbench allowed in source
local ignored config allowed for non-production secrets
maintenance root may be sibling to source
full temp/maintenance structure may be created lazily
warnings allowed for some source-cleanliness issues
```

### CI mode

```text
maintenance root lives inside CI workspace or runner temp
no drive-root folders
no user-home folders unless CI provider requires it
secrets only from CI secret store or environment
strict validation
warnings may fail
temp cleaned between runs unless cache explicitly configured
```

### Production mode

```text
no workbench in packaged build
maintenance root follows platform app-data/cache conventions
secrets from environment, OS credential store, or secret manager
compilation-readiness must pass before release
external evidence disabled unless feature is part of production behavior
```

### Docker mode

```text
maintenance root under /tmp/<app-slug> or configured mount
no drive letters
no user home assumptions
all writable paths must be explicit
secrets from environment, mounted secret files, or orchestrator secret store
```

---

## 12. File classification decision table

Before writing a file, ask:

```text
What zone does this file belong to?
Should this be source, maintenance, evidence, user data, build, log, secret, or quarantine?
```

Decision rules:

```text
source code, tests, docs, templates, static assets -> Source

lock files, generated clients, compiled protos, i18n outputs -> Generated-intentional source, if declared

development notes, patch manifests, local workbench state -> Workbench, excluded from builds

backup before patch -> Maintenance/backups/patches

restore copy before risky operation -> Maintenance/backups/restore

pre-commit copy -> Maintenance/backups/pre_commit

failed patch payload -> Maintenance/backups/failed_patches

temporary extraction -> Maintenance/scratch/extracts

regenerable cache -> Maintenance/scratch/cache

unknown or risky file -> Maintenance/quarantine/manual

autodeletable debris -> Maintenance/quarantine/autodelete

build artifact -> Build root or Maintenance/build

release artifact -> Maintenance/releases or formal release root

runtime log -> Logs root

migration log -> Maintenance/logs/migration

runtime user data -> User data root

external project audit/evidence -> External evidence root

external project clone/snapshot -> External snapshots root

secret -> secret manager, environment variable, OS credential store, or ignored local config
```

---

## 13. Cleanup and migration safety policy

Never delete or move existing files blindly.

Required sequence:

```text
1. Detect
2. Report
3. Dry-run
4. Confirm
5. Copy or move according to value/risk
6. Verify file counts and hashes when practical
7. Quarantine uncertain files
8. Log operation
9. Validate
10. Freeze only after validation passes
```

Default behavior:

```text
report only
dry-run first
human confirmation before moving meaningful files
quarantine instead of delete
copy before delete when evidence or user data might matter
move + verify allowed for large evidence when explicitly approved
```

Migration state must be tracked:

```text
<APP_MAINTENANCE_ROOT>/migration/migration_state.json
<APP_MAINTENANCE_ROOT>/migration/audit.jsonl
```

Never re-run a completed migration step unless:

```text
--force is provided
or the human explicitly approves
```

---

## 14. Source-cleanliness validation

Source-cleanliness validation answers:

```text
Is the source tree free of obvious debris?
```

Fail on:

```text
*.bak
*.backup
*_old.*
*_deprecated.*
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
.eslintcache
.parcel-cache
temporary extraction folders
generated audit/evidence folders
external project output
secrets
user data
compiled binaries
patch backups
restore copies
failed patch payloads
```

Warn or fail depending on project policy:

```text
workbench
large sample data
local docs excluded from build
generated manifests
test fixture databases
framework build folders
```

Allow if declared:

```text
lock files
compiled protos
generated clients
i18n outputs
framework-required generated source
```

---

## 15. Compilation-readiness validation

Compilation-readiness validation answers:

```text
Can this source tree be safely compiled or packaged now?
```

It should include:

```text
source-cleanliness validation
secret scan
symlink audit
build output exclusion check
package-data allowlist check
dependency declaration check
entry point check
external evidence exclusion check
workbench exclusion check
```

Fail hard on:

```text
secrets
external project evidence inside source
backup files
restore copies
user data
compiled binaries accidentally inside source
symlinks pointing outside source
undeclared generated artifacts
```

Warn, configurable to fail:

```text
workbench
large fixtures
local docs
test-only datasets
```

---

## 16. Mandatory validation gates

Every project should define equivalents for these gates.

```text
Gate 1: syntax or type check
Gate 2: focused tests for the changed behavior
Gate 3: regression tests
Gate 4: source-cleanliness validation
Gate 5: secret scan
Gate 6: symlink audit
Gate 7: workflow validation, if project has workflow contracts
Gate 8: architecture validation, if project has architecture contracts
Gate 9: compilation-readiness validation
Gate 10: build or package dry-run, if applicable
Gate 11: GUI/manual smoke check, if visual behavior changed
Gate 12: human freeze command
```

Run gates in order.

Stop at first failure.

Classify the failure before fixing it.

Never freeze with a red gate.

Only the human can freeze.

---

## 17. Git and packaging ignore baseline

If the project uses Git, create `.gitignore` before implementation.

At minimum, ignore:

```text
maintenance root
scratch
cache
quarantine
build outputs
release outputs, unless intentionally versioned
logs
local config
secrets
user data
external evidence
external snapshots
temporary extraction folders
language-specific caches
OS metadata files
IDE files unless intentionally shared
```

Create `.buildignore`, packaging exclusions, or equivalent.

At minimum, exclude:

```text
tests, if not shipped
workbench
maintenance root
external evidence
logs
cache
quarantine
local config
secrets
build scratch
migration scratch
temporary files
```

Project-specific allowlist must be declared for generated-intentional source.

---

## 18. Language and framework debris examples

Add project-specific patterns as needed.

Common examples:

```text
Python:
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
*.pyc
.coverage
htmlcov/

JavaScript/TypeScript:
node_modules/
.npm/
.yarn/
.pnpm-store/
.next/
.nuxt/
.svelte-kit/
dist/
build/
coverage/
.eslintcache
.parcel-cache/

Rust:
target/

Go:
bin/
coverage.out

Java/Kotlin:
target/
build/
.gradle/
*.class

C#/.NET:
bin/
obj/
TestResults/

Mobile:
DerivedData/
.gradle/
build/
Pods/
```

Framework conventions may allow some folders inside source during development, but packaging must exclude or intentionally include them.

---

## 19. Questions to ask once at project start

Ask once, record in project config, and do not re-ask every session unless the user changes the policy.

```text
1. What is the app name and slug?
2. What is the app root path?
3. What platform(s) must this project support?
4. What mode are we in: dev, ci, production, docker, or mixed?
5. What is the app package/root module?
6. Where should the maintenance root live?
7. Should maintenance root use explicit config, environment variable, platform default, or sibling folder?
8. Which build output model should be used: simple or formal?
9. Where should user data live?
10. Where should logs live?
11. What is the secret policy?
12. Does this app analyze or manage external projects?
13. If yes, where should external evidence live?
14. What generated files are intentional source artifacts?
15. Should workbench warn or fail compilation-readiness?
16. Should caches be auto-deletable or confirmation-only?
17. Should old legacy folders be detected only or migrated with confirmation?
18. Should valid old evidence be auto-migrated after dry-run confirmation?
19. What version control system is used?
20. What CI/CD platform is used?
21. What validation commands must pass before freeze?
22. What packaging/compilation commands must pass before release?
```

---

## 20. Implementation roadmap for adding this canon to an existing app

Implement one patch per gate.

Do not implement all at once.

```text
Patch 0: OS-aware path resolver
- app slug
- platform detection
- mode detection
- path normalization
- no hardcoded drive/user paths

Patch 1: maintenance root resolver
- APP_MAINTENANCE_ROOT resolution
- env/config override
- platform default
- sibling fallback
- writability check

Patch 2: ignore baseline
- .gitignore baseline
- .buildignore or packaging exclusion baseline
- generated-intentional source allowlist stub

Patch 3: maintenance subfolder policy
- backups
- scratch
- quarantine
- logs
- build
- releases
- migration
- diagnostics
- staging

Patch 4: legacy debris detector
- scan only
- report only
- no movement
- human-readable and machine-readable report

Patch 5: backup path resolver
- get backup path
- find restore path
- new path first
- legacy fallback second

Patch 6: debris/source-cleanliness validator
- scans source tree
- reports by category
- reads allowlist
- no moving or deletion

Patch 7: secret scan gate
- source scan
- evidence scan
- log scan when relevant
- fail hard on detected secrets

Patch 8: external evidence resolver
- external project slug
- evidence root
- current folder
- runs folder
- README generator
- manifest generator

Patch 9: compilation-readiness validator
- combines debris validator
- secret scan
- symlink audit
- build exclusion check
- package-data check

Patch 10: migration state tracker
- migration_state.json
- audit.jsonl
- no re-run without force

Patch 11: evidence migrator
- dry-run first
- human confirmation
- copy/move according to policy
- verify
- update migration state

Patch 12: cleanup scheduler, optional
- scratch retention
- quarantine/autodelete retention
- report before purge unless configured
```

Each patch must include:

```text
focused tests
syntax/type check
regression tests
architecture/workflow validation if available
manual smoke check if UI/runtime behavior changes
human freeze after clean validation
```

---

## 21. Absolute rules

```text
Never write secrets into source, logs, evidence, or build output.
Never delete meaningful files without dry-run and confirmation.
Never hardcode drive letters, home paths, usernames, or project names in reusable code.
Never mix external evidence from different projects.
Never write external project evidence inside that project's source tree without explicit request.
Never package maintenance, scratch, quarantine, logs, or evidence by accident.
Never skip secret scan before build or evidence generation.
Never re-run a completed migration without force or human approval.
Never freeze if a validation gate is red.
Never let the AI auto-freeze. Only the human freezes.
```

---

## 22. Expected AI behavior when this canon is loaded

The AI must first output:

```text
1. Folder policy table
2. Resolved paths
3. Mode and platform
4. Risk list
5. Secret policy
6. Ignore/buildignore baseline
7. Allowlist
8. Validation plan
9. Roadmap
```

Then wait for human acknowledgement before implementation unless the user explicitly asks only for planning.

For complex tasks, the AI must provide a complete roadmap before implementation.

For implementation tasks, the AI must work in focused gates and report progress after each step.

---

## 23. Quick placeholder glossary

```text
<APP_ROOT>
Absolute application source folder.

<APP_SLUG>
Safe lowercase application name.

<APP_PACKAGE>
Primary package or root module.

<APP_MAINTENANCE_ROOT>
App-owned non-source maintenance folder.

<APP_BUILD_ROOT>
Formal build/release output folder, if used.

<APP_USER_DATA_ROOT>
Persistent user data root.

<APP_LOG_ROOT>
Log output root.

<EXTERNAL_PROJECT_ROOT>
Root of the external project being analyzed or managed.

<EXTERNAL_PROJECT_SLUG>
Safe slug derived from external project name.

<EXTERNAL_EVIDENCE_ROOT>
External audit/evidence folder for generated project evidence.

<ARTIFACT_DOMAIN>
Evidence type, such as architecture_audit, migration_report, analysis_evidence.

<MODE>
dev, ci, production, docker, or mixed.
```

---

## Canon status

Version: 3.1

Status: reusable project-agnostic canon

Use: load at the beginning of any software/app implementation project before code generation, patching, cleanup, migration, compilation, or packaging.

Purpose: keep source clean, maintenance files external, evidence external, secrets protected, validation explicit, rollback possible, and compilation predictable.


---

## 24. Project Reasoner reference-folder boundary overlay

This overlay records a Kanda Reasoner-specific rule derived from current canon
notes. It narrows placement decisions for Project Reasoner without changing the
project-agnostic responsibility zones above.

### `_project_reference` is not application source

`_project_reference/` and `project_freeze_ledger/` are external documentation,
governance, audit, and handoff areas. They are not runtime app folders.

Allowed there:

```text
canon and governance reference
AI handoff material
bundle manifests
validation reports
audit reports
prompt-audit output
historical reference notes
```

Forbidden there:

```text
runtime app files
GUI helper JSON used by the app
source modules
package imports
resources that the app depends on
detector code
workflow code
application icons or runtime assets
```

### App-owned resources live in the app package

If the application reads a file at runtime, the file must live under the owning
application package or a declared app data/resource location. For Project
Reasoner, app-owned runtime/helper assets normally belong under:

```text
kanda_reasoner_app/
```

Examples:

```text
kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json
kanda_reasoner_app/reasoner_tools_gui_help/tab2_workflow.json
kanda_reasoner_app/reasoner_tools_gui_help/kanda_reasoner_color_icon.png
```

### Project-local generated evidence

Generated project-analysis evidence belongs to the project being analyzed and
must be resolved dynamically from active project context, CLI `--root`, GUI
state, or a project registry. Do not hardcode `<PROJECT_ROOT>` or any other
single local root.

Example pattern, not a hardcoded path:

```text
<PROJECT_ROOT>/project_analysis_evidence/json_complete/<project_slug>__complete.json
<PROJECT_ROOT>/project_analysis_evidence/json_complete/<project_slug>__active_snapshot.json
<PROJECT_ROOT>/project_analysis_evidence/json_complete/<project_slug>__file_manifest.json
<PROJECT_ROOT>/project_analysis_evidence/json_complete/<project_slug>__exclusion_rules.json
<PROJECT_ROOT>/project_analysis_evidence/json_complete/<project_slug>__validation_state.json
<PROJECT_ROOT>/project_analysis_evidence/json_complete/<project_slug>__bundle_manifest.json
```

Evidence from one project must never leak into another project.

### Change log

- v3.1: Added Project Reasoner-specific `_project_reference` boundary rule,
  app-package runtime-resource rule, and project-local generated-evidence rule.
