# KANDA REASONER PORTABLE WINDOWS UPDATE HANDOFF

## Repeatable recipe for rebuilding, validating, packaging, and publishing the portable Windows version

Document status: Known-good build procedure  
Baseline release: KANDA Reasoner Windows Portable v0.1.0  
Baseline date: July 2026  
Project repository: `E:\kanda_reasoner`  
Canonical launcher: `reasoner_tools_gui.py`  
Canonical PyInstaller specification: `KandaReasonerWindows.spec`  
Packaging format: PyInstaller one-folder build  
Final executable: `dist\KandaReasoner\KandaReasoner.exe`  
Final distributable: `KandaReasoner-Windows-Portable.zip`

---

## 1. Purpose

Use this handoff whenever a new portable Windows version of KANDA Reasoner must be produced.

The goal is to make the update routine predictable:

```text
Update source
→ confirm source application
→ rebuild from the committed specification
→ test the packaged executable
→ test relocation
→ test a clean ZIP extraction
→ calculate SHA-256
→ commit and push source changes
→ publish the ZIP as a GitHub Release asset
```

Do not restart the packaging investigation from zero unless the architecture, launcher, dynamic import system, Qt usage, or asset layout has materially changed.

The existing `KandaReasonerWindows.spec` is the packaging authority. It already captures the discoveries required to make the application function outside the development environment.

---

## 2. Expected user experience

The released application must work as follows:

```text
Download KandaReasoner-Windows-Portable.zip
→ Extract All
→ open the extracted KandaReasoner folder
→ double-click KandaReasoner.exe
```

The target computer must not require:

- Python;
- PyCharm;
- a virtual environment;
- manual `PYTHONPATH` configuration;
- PowerShell installation commands;
- registry changes;
- administrator installation.

This is a portable one-folder application, not an installer and not a single-file executable.

The extracted folder must remain intact:

```text
KandaReasoner\
├── KandaReasoner.exe
└── _internal\
```

`KandaReasoner.exe` depends on the contents of `_internal`. Never distribute the executable by itself.

---

## 3. Known-good baseline

The first validated portable build used:

```text
Python:       3.12.10, 64-bit
PyInstaller:  6.21.0
PySide6:      6.9.2
shiboken6:    6.9.2
requests:     2.34.2
libcst:       1.8.6
Ruff:         0.15.21
```

Known-good source commits from the original packaging cycle:

```text
70bf6d5 Establish complete KANDA Reasoner project baseline
2e779dd Stop automatic Web AI credential loading
88e5899 Optimize Project Structure freeze protection matching
8ccb655 Add portable Windows build specification
```

The exact commit IDs will change in future releases. Their value is historical: they identify the fixes that established the portable baseline.

---

## 4. Golden rules

### Rule 1 — Reuse the committed specification

Build with:

```text
KandaReasonerWindows.spec
```

Do not create a new `.spec` file for each release.

Do not switch to a command containing dozens of temporary `--hidden-import` and `--add-data` options. The committed specification exists so packaging knowledge remains versioned with the project.

### Rule 2 — Use a one-folder build

Do not change to `--onefile` merely to create a smaller-looking distribution.

KANDA Reasoner uses PySide6, Qt WebEngine, Qt WebChannel, dynamic modules, help assets, and physical files. These are more reliable in a one-folder package.

### Rule 3 — Test the packaged application

A successful PyInstaller message does not prove that KANDA Reasoner works.

The real acceptance test is:

```text
dist\KandaReasoner\KandaReasoner.exe
```

Open the packaged executable and test the important tabs.

### Rule 4 — Test outside the source folder

A build that works only under `E:\kanda_reasoner` is not portable.

Always perform:

1. a relocated-folder test; and
2. a clean extraction test from the final ZIP.

### Rule 5 — Never publish secrets or development debris

The repository and ZIP must not contain:

- `.env` files;
- API keys or tokens;
- `.venv`;
- `build`;
- `dist` as committed source;
- private project archives;
- patient or customer information;
- development-only credentials;
- temporary validation folders.

### Rule 6 — Do not “fix” a warning without proving it affects runtime

The known developer-tools collection warning was nonfatal. Treat warnings as investigation signals, not automatic release blockers.

---

## 5. Known failures and the fixes that must be preserved

### 5.1 Web AI environment key loaded automatically

#### Problem

The Web AI configuration screen automatically loaded an environment API key during startup or gateway changes.

This created an unnecessary credential-exposure risk in a distributable application.

#### Correct behavior

The environment key must remain blank until the user explicitly presses the manual load button.

The production fix removed automatic `_load_environment_key(silent=True)` calls from:

```text
kanda_reasoner_app\web_ai_configuration.py
```

The manual **Load environment key** action remains available.

#### Regression check

When the portable application starts:

- the key field must be blank;
- no environment credential should appear automatically;
- the manual button may load the environment key when deliberately used.

Do not reintroduce automatic credential loading during future refactoring.

---

### 5.2 Project Structure 3D froze during loading

#### Problem

Freeze protection was applied by repeatedly comparing every graph node with every protected path while repeatedly constructing path objects.

The behavior effectively became an expensive nested comparison and caused the Project Structure 3D tab to appear frozen on a large project.

The relevant file was:

```text
kanda_reasoner_app\project_structure_visualizer\graph_protection_status.py
```

#### Correct behavior

Protected paths are normalized once, indexed once, and checked through node path prefixes rather than repeated full nested matching.

#### Regression check

In both the source application and packaged application:

1. open Project Structure 3D;
2. select or load the KANDA Reasoner project;
3. wait for the real graph to render;
4. confirm the interface remains responsive;
5. confirm frozen/protected status is still represented correctly.

Do not replace the indexed matching logic with the old node-by-protected-path nested loop.

---

### 5.3 Dynamic and lazy modules were missing from the package

#### Problem

PyInstaller cannot always discover modules imported dynamically by tab registries, lazy loaders, string-based imports, or runtime module selection.

This caused packaged tabs to fail even though the source application worked.

#### Correct behavior

`KandaReasonerWindows.spec` must continue to collect KANDA submodules and explicitly include dynamic top-level engineering-safety modules.

Important explicit hidden imports include:

```text
PySide6.QtWebEngineCore
PySide6.QtWebEngineWidgets
PySide6.QtWebChannel
reasoner_tools_gui_engineering_safety_panel
_reasoner_tools_gui_engineering_safety_panel_catalog
_reasoner_tools_gui_engineering_safety_panel_commands
_reasoner_tools_gui_engineering_safety_full_audit
_reasoner_tools_gui_engineering_safety_sonar
_reasoner_tools_gui_ruff_correction_dialog
```

The specification also collects submodules under:

```text
kanda_reasoner_app
```

#### Regression check

Open every visible tab that matters to the release, especially:

- Audit Project;
- Show Project to AI;
- Project Structure 3D;
- Config Web AI;
- Engineering Safety-related interfaces;
- any newly added dynamically loaded tab.

When a new tab is added, confirm whether its import is statically visible to PyInstaller. If not, add it to the specification and document why.

---

### 5.4 Physical help/source files were absent

#### Problem

Some application behavior reads physical files through filesystem paths rather than importing them as Python modules.

`collect_submodules()` does not automatically include every physical file needed through path-based lookup.

The important directory identified during the original build was:

```text
kanda_reasoner_app\reasoner_context_collector\collector_main_help
```

#### Correct behavior

The specification explicitly adds this directory while preserving its package-relative destination.

It also collects KANDA application data files.

#### Regression check

Open **Show Project to AI** in the packaged application and exercise the actual workflow far enough to prove that required help/source fragments are present.

When new code loads HTML, JavaScript, Markdown, JSON, images, templates, prompts, help files, or source fragments through a path, add those files to `datas` in the specification.

---

### 5.5 Audit Project failed because top-level support modules were omitted

#### Problem

Several engineering-safety support modules live outside the normal package import tree or are loaded dynamically.

PyInstaller did not infer all of them.

#### Correct behavior

Keep their explicit hidden imports in `KandaReasonerWindows.spec`.

#### Regression check

Open **Audit Project** from the packaged executable and verify that the real tab loads without a missing-module traceback.

---

### 5.6 Machine-specific paths threatened portability

#### Problem

A packaging specification can accidentally capture paths such as:

```text
E:\kanda_reasoner
C:\Users\paulo
.venv absolute paths
PyCharm paths
the local Python installation path
```

Such a build may work on the development machine but fail after moving the repository.

#### Correct behavior

`KandaReasonerWindows.spec` uses paths derived from the specification/project location and relative source references.

The committed specification must not contain machine-specific development paths.

#### Regression check

Search the specification before release:

```powershell
Select-String `
    -Path .\KandaReasonerWindows.spec `
    -Pattern 'E:\\|C:\\Users\\paulo|PyCharm|\.venv'
```

Expected result: no machine-specific packaging path.

A Python installation path can legitimately appear in PyInstaller’s live build log. It must not be hardcoded into the committed specification or runtime code.

---

### 5.7 Ruff IDE popup was misleading

#### Problem

PyCharm repeatedly displayed:

```text
Ruff: Error while resolving settings from workspace e:\kanda_reasoner.
Please refer to the logs for more details.
```

The command-line Ruff installation still worked.

#### Correct interpretation

The IDE popup is not a portable-build failure when command-line Ruff passes.

Use the governed interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m ruff check <changed files>
```

Do not block a release solely because of that PyCharm popup.

---

### 5.8 Known nonfatal PyInstaller warning

The build may show:

```text
Failed to collect submodules for
'kanda_reasoner_app.reasoner_context_collector.developer_tools'
because:
No module named
'kanda_reasoner_app.reasoner_context_collector.developer_tools.collector_packaging_metadata'
```

This warning was present in the validated build.

It did not prevent:

- application startup;
- Project Structure 3D;
- Show Project to AI;
- Audit Project;
- Config Web AI;
- relocation;
- clean ZIP extraction.

#### Release rule

Do not call this warning fatal unless a current packaged workflow actually fails because of it.

If the module becomes required in the future, either:

- restore the missing module;
- remove the stale import/reference;
- or exclude the optional package from collection deliberately.

Do not make speculative source changes immediately before release merely to silence the warning.

---

## 6. Before starting a new portable update

Open PowerShell and move to the repository:

```powershell
Set-Location E:\kanda_reasoner
```

Confirm the repository state:

```powershell
git status --short
git branch --show-current
git log --oneline -5
```

Before building, the working tree should be understood.

A clean working tree is ideal. A build from intentional uncommitted changes is possible, but the exact source used for the binary must be committed before publication.

Confirm the canonical files exist:

```powershell
Test-Path .\reasoner_tools_gui.py
Test-Path .\KandaReasonerWindows.spec
Test-Path .\.venv\Scripts\python.exe
```

Expected:

```text
True
True
True
```

---

## 7. Source-update workflow

### Step 1 — Update the application source normally

Implement and validate the intended KANDA Reasoner changes before packaging.

Do not modify packaging merely because application code changed. Modify `KandaReasonerWindows.spec` only when the update introduces or changes:

- a dynamic import;
- a lazy-loaded module;
- a top-level module outside normal package collection;
- a new Qt module;
- a new physical asset;
- a new path-loaded help directory;
- a new subprocess resource;
- a renamed launcher;
- a changed application icon;
- a changed package root.

### Step 2 — Run focused Ruff checks

For every changed Python file:

```powershell
.\.venv\Scripts\python.exe -m ruff check `
    .\path\to\changed_file.py
```

For several files:

```powershell
.\.venv\Scripts\python.exe -m ruff check `
    .\file_one.py `
    .\file_two.py
```

Do not rely only on the PyCharm Ruff integration.

### Step 3 — Launch from source

```powershell
.\.venv\Scripts\python.exe .\reasoner_tools_gui.py
```

Confirm the source application works before packaging.

At minimum, test any tab affected by the update.

For a broad portable release, also reopen:

- Project Structure 3D;
- Show Project to AI;
- Audit Project;
- Config Web AI.

Close the source application cleanly before building.

---

## 8. Environment preparation

The existing virtual environment should normally be reused.

Confirm versions:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m PyInstaller --version
.\.venv\Scripts\python.exe -m pip show PySide6 shiboken6 requests libcst ruff pyinstaller
```

When rebuilding the virtual environment is necessary, use Python 3.12 64-bit and install the validated baseline:

```powershell
py -3.12 -m venv .venv
```

Then:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

Then:

```powershell
.\.venv\Scripts\python.exe -m pip install `
    PySide6==6.9.2 `
    shiboken6==6.9.2 `
    requests==2.34.2 `
    libcst==1.8.6 `
    pyinstaller==6.21.0 `
    ruff==0.15.21
```

A later dependency upgrade should be treated as an intentional release change and revalidated fully.

Do not casually upgrade PySide6 or PyInstaller immediately before creating a routine application update.

---

## 9. Inspect the packaging specification

The committed `KandaReasonerWindows.spec` is expected to:

- use `reasoner_tools_gui.py` as the launcher;
- produce a one-folder application named `KandaReasoner`;
- collect data files for `kanda_reasoner_app`;
- collect submodules for `kanda_reasoner_app`;
- include Qt WebEngine and Qt WebChannel;
- include the engineering-safety hidden imports;
- add the physical `collector_main_help` directory;
- use relative or specification-derived paths;
- avoid machine-specific paths;
- produce `KandaReasoner.exe`;
- use `console=True` in the current debugging-friendly baseline.

Do not regenerate the file with `pyi-makespec` unless the existing specification is irreparably obsolete.

Before building:

```powershell
git diff -- .\KandaReasonerWindows.spec
```

Any change to the specification should be deliberate and reviewed.

---

## 10. Canonical clean build

Run exactly:

```powershell
Set-Location E:\kanda_reasoner

.\.venv\Scripts\python.exe -m PyInstaller `
    --noconfirm `
    --clean `
    .\KandaReasonerWindows.spec
```

Why these options matter:

- `--noconfirm` replaces prior output without interactive prompts;
- `--clean` clears cached PyInstaller analysis that could hide import or packaging changes;
- the `.spec` file supplies the complete packaging contract.

Expected final output folder:

```text
E:\kanda_reasoner\dist\KandaReasoner
```

Expected executable:

```text
E:\kanda_reasoner\dist\KandaReasoner\KandaReasoner.exe
```

Confirm:

```powershell
Test-Path .\dist\KandaReasoner\KandaReasoner.exe
```

Expected:

```text
True
```

---

## 11. Reading the build result correctly

A successful build normally ends with a message indicating that building completed and that results are available under `dist`.

Do not confuse these items:

### Build success

PyInstaller created:

```text
dist\KandaReasoner\KandaReasoner.exe
```

### Runtime success

The packaged executable opens and the required workflows function.

Both are required.

Review the generated warning file when a new problem appears:

```powershell
Get-ChildItem .\build\KandaReasoner -Filter 'warn-*.txt'
```

Do not attempt to eliminate every warning indiscriminately. Many Python and Qt packages contain optional imports.

Investigate warnings that correspond to actual application modules, dynamic tabs, required assets, or a runtime failure.

---

## 12. Packaged runtime validation

Launch:

```powershell
Start-Process .\dist\KandaReasoner\KandaReasoner.exe
```

Then perform the following manually.

### Main application

Confirm:

- the real KANDA Reasoner main window appears;
- the application does not close immediately;
- the interface is responsive;
- the expected application icon appears;
- the application can close normally;
- the application can reopen.

### Project Structure 3D

Confirm:

- the tab opens;
- the graph loads;
- no apparent infinite freeze occurs;
- the interface remains responsive;
- protection/freeze information still appears correctly.

### Show Project to AI

Confirm:

- the tab opens;
- its real content is present;
- required physical help/source files are found;
- no missing-file traceback occurs.

### Audit Project

Confirm:

- the tab opens;
- engineering-safety support modules load;
- no `ModuleNotFoundError` appears.

### Config Web AI

Confirm:

- the tab opens;
- the key is not automatically loaded or displayed;
- manual environment-key loading remains available.

### New or changed workflows

Every newly added or materially changed visible tab must be opened from the packaged executable.

A source-only test is insufficient.

---

## 13. Static package checks

Confirm core Qt content exists:

```powershell
Get-ChildItem `
    .\dist\KandaReasoner\_internal `
    -Recurse `
    -Filter QtWebEngineProcess.exe
```

Confirm Qt platform plugins exist:

```powershell
Get-ChildItem `
    .\dist\KandaReasoner\_internal `
    -Recurse `
    -Filter qwindows.dll
```

Confirm the application package is not unexpectedly tiny:

```powershell
$portableSize = (
    Get-ChildItem .\dist\KandaReasoner -Recurse -File |
    Measure-Object Length -Sum
).Sum

'{0:N2} MiB' -f ($portableSize / 1MB)
```

A major unexplained size reduction can indicate omitted dependencies or assets.

Do not use size alone as proof. Runtime testing remains authoritative.

---

## 14. Relocation test

Remove any old relocation folder:

```powershell
Remove-Item `
    E:\KandaReasonerPortableTest `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue
```

Copy the complete packaged folder:

```powershell
Copy-Item `
    .\dist\KandaReasoner `
    E:\KandaReasonerPortableTest `
    -Recurse
```

Launch the relocated executable:

```powershell
Start-Process `
    E:\KandaReasonerPortableTest\KandaReasoner.exe
```

Repeat the important smoke tests:

- main window;
- Project Structure 3D;
- Show Project to AI;
- Audit Project;
- Config Web AI.

The relocated copy must not depend on:

```text
E:\kanda_reasoner
the source tree
the virtual environment
PyCharm
the current working directory
```

Close the relocated application before continuing.

---

## 15. Create the final ZIP

Return to the source repository:

```powershell
Set-Location E:\kanda_reasoner
```

Remove an older ZIP:

```powershell
Remove-Item `
    .\KandaReasoner-Windows-Portable.zip `
    -Force `
    -ErrorAction SilentlyContinue
```

Create the ZIP from the contents of the built folder:

```powershell
Compress-Archive `
    -Path .\dist\KandaReasoner\* `
    -DestinationPath .\KandaReasoner-Windows-Portable.zip `
    -CompressionLevel Optimal
```

Confirm:

```powershell
Get-Item .\KandaReasoner-Windows-Portable.zip |
    Select-Object FullName, Length, LastWriteTime
```

Important: the ZIP should open directly to:

```text
KandaReasoner.exe
_internal\
```

It should not contain unnecessary nesting such as:

```text
dist\KandaReasoner\KandaReasoner.exe
```

The command above archives the contents of `dist\KandaReasoner`, which produces the intended layout.

---

## 16. Clean ZIP extraction test

Delete any previous extraction test folder:

```powershell
Remove-Item `
    E:\KandaReasonerZipValidation `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue
```

Create it:

```powershell
New-Item `
    -ItemType Directory `
    -Path E:\KandaReasonerZipValidation |
    Out-Null
```

Extract the exact final ZIP:

```powershell
Expand-Archive `
    -Path .\KandaReasoner-Windows-Portable.zip `
    -DestinationPath E:\KandaReasonerZipValidation `
    -Force
```

Confirm the executable:

```powershell
Test-Path `
    E:\KandaReasonerZipValidation\KandaReasoner.exe
```

Launch:

```powershell
Start-Process `
    E:\KandaReasonerZipValidation\KandaReasoner.exe
```

This is the most important distribution test because it validates the exact archive that users will download.

Repeat the essential smoke checks.

Do not publish a ZIP that was never extracted and executed.

---

## 17. Calculate and record SHA-256

Run:

```powershell
Get-FileHash `
    .\KandaReasoner-Windows-Portable.zip `
    -Algorithm SHA256
```

Record:

- filename;
- exact byte size;
- creation date;
- SHA-256.

For the original v0.1.0 baseline only:

```text
Filename:
KandaReasoner-Windows-Portable.zip

Size:
469499467 bytes

SHA-256:
DD2EF4D3000FB993B4D6BE2F7130C11B6AFEE534A87DE7B5C322A88CA96BFD95
```

Never reuse the old hash for a new ZIP. Every rebuilt archive requires a new hash.

---

## 18. Clean temporary validation folders

After all applications are closed:

```powershell
Set-Location E:\kanda_reasoner

Remove-Item `
    E:\KandaReasonerPortableTest, `
    E:\KandaReasonerZipValidation `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue
```

Keep:

```text
E:\kanda_reasoner\KandaReasonerWindows.spec
E:\kanda_reasoner\KandaReasoner-Windows-Portable.zip
```

`build` and `dist` may be kept locally for investigation, but should normally remain ignored by Git.

---

## 19. Git release hygiene

Check:

```powershell
git status --short
```

The following must not be committed:

```text
.venv\
build\
dist\
KandaReasoner-Windows-Portable.zip
```

Confirm whether the ZIP is ignored:

```powershell
git check-ignore -v `
    .\KandaReasoner-Windows-Portable.zip
```

Commit source, specification, documentation, and intentional configuration changes only.

Example:

```powershell
git add `
    .\KandaReasonerWindows.spec `
    .\README.md `
    .\LICENSE.md `
    <other intentional source files>
```

Then:

```powershell
git commit -m "Prepare KANDA Reasoner portable Windows release"
```

Push the release branch:

```powershell
git push
```

For a new branch:

```powershell
git push -u origin <branch-name>
```

---

## 20. GitHub release workflow

Do not commit the large portable ZIP to the normal repository history.

Upload it as a GitHub Release asset.

On GitHub:

1. Open the repository.
2. Open `/releases`.
3. Select **Draft a new release**.
4. Create a new version tag.
5. Target the exact tested commit or release branch.
6. Enter the release title.
7. Paste the release description.
8. Upload `KandaReasoner-Windows-Portable.zip`.
9. Confirm the upload finishes.
10. Publish the release.

Recommended release description elements:

- what this release is;
- download instructions;
- extraction instructions;
- the requirement to keep `_internal` beside the executable;
- major changes;
- validated workflows;
- unsigned SmartScreen warning;
- exact SHA-256.

Use the new hash generated for that release.

---

## 21. Windows SmartScreen and antivirus

The executable is currently unsigned.

Windows may display SmartScreen warnings because the application is unfamiliar or lacks a trusted code-signing certificate.

This does not automatically indicate malware.

Users should:

- download only from the official GitHub Release;
- verify the published SHA-256;
- extract the ZIP before launching;
- keep the folder intact.

Do not claim that antivirus warnings are impossible.

Code signing is a separate future improvement and is not required to produce the current portable build.

---

## 22. Full release checklist

Do not publish until every applicable item is complete.

### Source

```text
[ ] Intended source update is complete
[ ] Changed Python files pass command-line Ruff
[ ] Source application launches
[ ] Changed workflows pass source smoke tests
[ ] Web AI key does not auto-load
[ ] Project Structure 3D does not regress to nested path matching
```

### Specification

```text
[ ] KandaReasonerWindows.spec is present
[ ] Specification uses relative/spec-derived paths
[ ] No E:\ or C:\Users\paulo path is hardcoded
[ ] QtWebEngineCore is included
[ ] QtWebEngineWidgets is included
[ ] QtWebChannel is included
[ ] Dynamic engineering-safety modules remain included
[ ] kanda_reasoner_app data files are collected
[ ] kanda_reasoner_app submodules are collected
[ ] collector_main_help physical files are included
```

### Build

```text
[ ] Build used --noconfirm --clean
[ ] dist\KandaReasoner\KandaReasoner.exe exists
[ ] Build completion was reported
[ ] Known developer-tools warning was assessed, not blindly treated as fatal
```

### Packaged application

```text
[ ] Main application opens
[ ] Main application closes cleanly
[ ] Main application reopens
[ ] Project Structure 3D loads and remains responsive
[ ] Show Project to AI loads
[ ] Audit Project loads
[ ] Config Web AI starts with blank key
[ ] Any new visible tab opens
[ ] QtWebEngineProcess.exe exists
[ ] qwindows.dll exists
```

### Portability

```text
[ ] Complete folder copied to another path
[ ] Relocated KandaReasoner.exe opens
[ ] Relocated critical tabs pass
[ ] Final ZIP created
[ ] Final ZIP extracted to a clean folder
[ ] Executable from the extracted ZIP opens
[ ] Critical tabs pass from the extracted ZIP
```

### Publication

```text
[ ] New SHA-256 calculated
[ ] New file size recorded
[ ] ZIP is ignored by Git
[ ] .venv is not committed
[ ] build is not committed
[ ] dist is not committed
[ ] Source changes committed
[ ] Release branch pushed
[ ] Correct tag targets exact tested source
[ ] ZIP uploaded as a Release asset
[ ] Release notes contain the new SHA-256
```

Only after these checks should the release be marked complete.

---

## 23. Troubleshooting decision tree

### The build command fails immediately

Check:

```powershell
Test-Path .\.venv\Scripts\python.exe
Test-Path .\KandaReasonerWindows.spec
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m PyInstaller --version
```

Do not run a global PyInstaller accidentally.

---

### The executable opens and immediately closes

Run it from PowerShell so console output remains visible:

```powershell
Set-Location .\dist\KandaReasoner
.\KandaReasoner.exe
```

The current baseline uses `console=True`, which is useful for diagnosing startup failures.

Look for:

- `ModuleNotFoundError`;
- missing DLL;
- missing Qt plugin;
- missing file;
- incorrect resource path;
- import-time exception.

Do not change `console=False` until the release is stable and an equivalent persistent logging path exists.

---

### A tab fails only in the packaged application

Most likely causes:

1. dynamic import not collected;
2. physical asset not included;
3. path incorrectly assumes source-tree layout;
4. optional dependency absent;
5. a top-level module was missed.

Actions:

- identify the exact missing module or file from the traceback;
- add a precise hidden import or data entry to the existing specification;
- rebuild with `--clean`;
- retest the real packaged tab;
- document the reason in the specification.

Do not add unrelated hidden imports blindly.

---

### Qt says no platform plugin could be initialized

Confirm `qwindows.dll` exists under the packaged `_internal` tree.

Rebuild from the committed specification and the governed virtual environment.

Do not manually copy arbitrary Qt DLLs from a different PySide6 installation unless the package hook is proven defective.

---

### A WebEngine tab is blank or crashes

Confirm:

- `PySide6.QtWebEngineCore` is included;
- `PySide6.QtWebEngineWidgets` is included;
- `PySide6.QtWebChannel` is included;
- `QtWebEngineProcess.exe` exists;
- Qt WebEngine resources and localization files exist;
- HTML/JavaScript assets loaded by path are included.

Test the same workflow from the relocated and clean-extraction folders.

---

### Show Project to AI reports a missing physical file

Inspect the missing path.

When the application opens a file directly by path, add its directory or file to `datas`.

Remember:

```text
collect_submodules()
```

collects importable Python modules, not every physical file used through filesystem lookup.

Preserve the destination path expected by the application.

---

### Audit Project reports a missing engineering-safety module

Check the explicit hidden imports in `KandaReasonerWindows.spec`.

Top-level and underscore-prefixed support modules are not guaranteed to be inferred.

Add only the exact required module, rebuild with `--clean`, and retest Audit Project.

---

### Project Structure 3D freezes again

Check whether `graph_protection_status.py` was changed.

Reject any reintroduction of repeated path normalization or an every-node-by-every-protected-path nested comparison.

Use `faulthandler` or a runtime stack dump to confirm the active call path rather than guessing.

The original confirmed freeze path passed through freeze-path construction, freeze state, graph protection status, semantic enrichment, snapshot building, and lazy tab loading.

---

### The package works under `dist` but not after relocation

Search for hardcoded paths:

```powershell
Get-ChildItem . -Recurse -File -Include *.py,*.spec |
    Select-String `
        -Pattern 'E:\\kanda_reasoner|C:\\Users\\paulo|PyCharm'
```

Also inspect:

- current-working-directory assumptions;
- paths derived from the source checkout;
- subprocess commands targeting `.venv`;
- resources opened without a packaged-resource resolver.

A packaged app must resolve its own read-only resources independently of the active project root.

---

### The ZIP works locally but users report missing files

Confirm the ZIP was built from:

```text
dist\KandaReasoner\*
```

not from the executable alone.

Extract the actual uploaded/downloaded ZIP into a new folder and test that exact copy.

Check whether antivirus quarantined a DLL or Qt subprocess.

Publish the SHA-256 so users can verify integrity.

---

### The ZIP is too large for a normal Git commit

This is expected.

Do not commit it to repository history.

Upload it to the GitHub Release.

Keep source code and the `.spec` file in Git; keep compiled distribution archives in Releases.

---

## 24. When the specification must be updated

Change `KandaReasonerWindows.spec` only when at least one of these is true:

- a new dynamically imported tab is added;
- a module is imported by string or registry and is absent from the package;
- a new top-level support module is required;
- a new Qt component is used;
- new HTML, JS, JSON, Markdown, image, prompt, help, or template files are read at runtime;
- a required physical source fragment is opened by path;
- the launcher changes;
- application naming or icon behavior changes;
- package-relative layout changes;
- the application starts a bundled helper executable or subprocess.

Every specification change requires:

```text
reason
→ exact entry changed
→ clean rebuild
→ affected packaged workflow test
→ relocation test
→ clean ZIP extraction test
```

---

## 25. Recommended future improvement: one canonical release script

The current manual procedure is validated and should remain the source of truth.

A future improvement may add one governed PowerShell script such as:

```text
build_portable_release.ps1
```

It should automate only deterministic steps:

1. confirm repository root;
2. confirm clean or acknowledged Git state;
3. confirm governed Python and PyInstaller;
4. run focused preflight checks;
5. delete previous `build` and `dist`;
6. run PyInstaller from `KandaReasonerWindows.spec`;
7. confirm executable and critical Qt files;
8. recreate the ZIP;
9. calculate SHA-256;
10. print output paths and a manual validation checklist.

It should not falsely declare GUI workflows successful without opening and testing them.

Human packaged-runtime validation remains required.

---

## 26. Canonical quick recipe

For an ordinary update where the existing specification remains valid:

```powershell
Set-Location E:\kanda_reasoner

git status --short

.\.venv\Scripts\python.exe -m ruff check `
    <changed Python files>

.\.venv\Scripts\python.exe .\reasoner_tools_gui.py
```

After source validation and closing the source application:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller `
    --noconfirm `
    --clean `
    .\KandaReasonerWindows.spec
```

Launch and manually validate:

```powershell
Start-Process .\dist\KandaReasoner\KandaReasoner.exe
```

Then relocate:

```powershell
Remove-Item `
    E:\KandaReasonerPortableTest `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

Copy-Item `
    .\dist\KandaReasoner `
    E:\KandaReasonerPortableTest `
    -Recurse

Start-Process `
    E:\KandaReasonerPortableTest\KandaReasoner.exe
```

Then create and extract the ZIP:

```powershell
Set-Location E:\kanda_reasoner

Remove-Item `
    .\KandaReasoner-Windows-Portable.zip `
    -Force `
    -ErrorAction SilentlyContinue

Compress-Archive `
    -Path .\dist\KandaReasoner\* `
    -DestinationPath .\KandaReasoner-Windows-Portable.zip `
    -CompressionLevel Optimal

Remove-Item `
    E:\KandaReasonerZipValidation `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

New-Item `
    -ItemType Directory `
    -Path E:\KandaReasonerZipValidation |
    Out-Null

Expand-Archive `
    -Path .\KandaReasoner-Windows-Portable.zip `
    -DestinationPath E:\KandaReasonerZipValidation `
    -Force

Start-Process `
    E:\KandaReasonerZipValidation\KandaReasoner.exe
```

After the extracted application passes:

```powershell
Get-Item .\KandaReasoner-Windows-Portable.zip |
    Select-Object FullName, Length, LastWriteTime

Get-FileHash `
    .\KandaReasoner-Windows-Portable.zip `
    -Algorithm SHA256
```

Finally:

```powershell
git status --short
git push
```

Upload the ZIP to a GitHub Release and publish the new SHA-256.

---

## 27. Definition of done

The portable update is complete only when:

```text
PORTABLE_BUILD_CONTENTS: PASS
PORTABLE_APPLICATION_LAUNCH: PASS
PORTABLE_VISIBLE_TABS: PASS
PORTABLE_QT_PLUGINS: PASS
PORTABLE_QWEBENGINE: PASS
PORTABLE_CLEAN_SHUTDOWN: PASS
PORTABLE_RELAUNCH: PASS
PORTABLE_RELOCATION: PASS
PORTABLE_ZIP_EXTRACTION: PASS
PORTABLE_CREDENTIAL_STARTUP_SAFETY: PASS
PORTABLE WINDOWS BUILD: PASS
```

Do not mark a check as passed unless it was actually performed against the current build.

---

## 28. Final operational summary

The reliable process is not:

```text
Keep changing PyInstaller options until the executable opens.
```

The reliable process is:

```text
Preserve the known-good source fixes
→ preserve one committed packaging specification
→ build cleanly
→ test the actual packaged workflows
→ test relocation
→ test the exact final ZIP
→ publish the archive with a fresh hash
```

That procedure prevents the original cycle of repeatedly discovering missing imports, missing physical files, Qt WebEngine requirements, machine-specific paths, credential-loading behavior, and a source-level performance freeze.

The committed specification is the packaging memory.

This handoff is the operational memory.

The packaged executable and extracted ZIP tests are the proof.
