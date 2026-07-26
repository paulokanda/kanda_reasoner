# KANDA REASONER PORTABLE WINDOWS UPDATE HANDOFF

## Repeatable recipe for rebuilding, validating, packaging, and publishing the portable Windows version

Document status: Updated known-good build and Windows-compatible ZIP procedure  
Baseline release: KANDA Reasoner Windows Portable v0.1.0  
Baseline date: July 2026  
Project repository: `E:\kanda_reasoner`  
Canonical launcher: `reasoner_tools_gui.py`  
Canonical PyInstaller specification: `KandaReasonerWindows.spec`  
Packaging format: PyInstaller one-folder build  
Final executable: `dist\kanda_reasoner\kanda_reasoner.exe`  
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
→ open the extracted kanda_reasoner folder
→ double-click kanda_reasoner.exe
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
kanda_reasoner\
├── kanda_reasoner.exe
└── _internal\
```

`kanda_reasoner.exe` depends on the contents of `_internal`. Never distribute the executable by itself.

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
dist\kanda_reasoner\kanda_reasoner.exe
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

### 5.7 Windows Explorer rejected an otherwise readable ZIP

#### Problem

The original archive could be read by Python, PowerShell, and `tar.exe`, but Windows Explorer reported that the compressed folder was invalid.

The decisive issue was the presence of packaged non-runtime planning documents whose internal archive paths reached 260 bytes or more. The longest observed path was over 300 characters.

#### Correct behavior

The final release ZIP must be created from a staged copy of `dist\kanda_reasoner`.

The staging procedure removes the known non-runtime long-path planning directory:

```text
_internal\kanda_reasoner_app\routing_signal_scorer\mlrt_non_runtime_candidate_reliability
```

The procedure then rejects the release when any remaining archive path is 260 UTF-8 bytes or longer and validates the completed ZIP through Windows Explorer's `Shell.Application` parser.

#### Regression check

Before publication:

- double-click the ZIP in Windows Explorer;
- confirm that it opens without an invalid-folder message;
- confirm exactly one top-level `kanda_reasoner` folder;
- extract it to a clean folder;
- run `kanda_reasoner.exe` from the extracted folder.

Do not replace the staged .NET ZIP procedure with `Compress-Archive`.

---

### 5.8 Release executable opened an unwanted terminal window

#### Problem

The PyInstaller specification used `console=True`, causing a terminal window to open beside the GUI and display repeated nonfatal Qt `connectSlotsByName` warnings.

#### Correct behavior

The release specification uses:

```python
console=False,
```

This produces a normal GUI application without an accompanying terminal window.

A temporary diagnostic build may use `console=True`, but that setting must not be committed as the normal release baseline.

---

### 5.9 Ruff IDE popup was misleading

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

### 5.10 Known nonfatal PyInstaller warning

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
- produce a one-folder application named `kanda_reasoner`;
- collect data files for `kanda_reasoner_app`;
- collect submodules for `kanda_reasoner_app`;
- include Qt WebEngine and Qt WebChannel;
- include the engineering-safety hidden imports;
- add the physical `collector_main_help` directory;
- use relative or specification-derived paths;
- avoid machine-specific paths;
- produce `kanda_reasoner.exe`;
- use `console=False` in the release baseline so the GUI opens without a terminal window.

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
E:\kanda_reasoner\dist\kanda_reasoner
```

Expected executable:

```text
E:\kanda_reasoner\dist\kanda_reasoner\kanda_reasoner.exe
```

Confirm:

```powershell
Test-Path .\dist\kanda_reasoner\kanda_reasoner.exe
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
dist\kanda_reasoner\kanda_reasoner.exe
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
Start-Process .\dist\kanda_reasoner\kanda_reasoner.exe
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
    .\dist\kanda_reasoner\_internal `
    -Recurse `
    -Filter QtWebEngineProcess.exe
```

Confirm Qt platform plugins exist:

```powershell
Get-ChildItem `
    .\dist\kanda_reasoner\_internal `
    -Recurse `
    -Filter qwindows.dll
```

Confirm the application package is not unexpectedly tiny:

```powershell
$portableSize = (
    Get-ChildItem .\dist\kanda_reasoner -Recurse -File |
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
    .\dist\kanda_reasoner `
    E:\KandaReasonerPortableTest `
    -Recurse
```

Launch the relocated executable:

```powershell
Start-Process `
    E:\KandaReasonerPortableTest\kanda_reasoner.exe
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

## 15. Create the final Windows-compatible ZIP

Return to the source repository:

```powershell
Set-Location E:\kanda_reasoner
```

### Why the release ZIP uses a staging folder

Do not create the release archive directly with `Compress-Archive`.

The earlier archive was structurally readable by Python and PowerShell but Windows Explorer reported:

```text
Windows cannot open the folder.
The Compressed (zipped) Folder is invalid.
```

The packaged data also contained non-runtime planning documents with internal archive paths longer than 260 characters. Windows Explorer can reject the entire ZIP when such entries are present.

The release procedure therefore:

1. copies the built application to a temporary staging folder;
2. removes the known non-runtime long-path planning directory from the staged copy only;
3. verifies that every remaining archive path is shorter than 260 UTF-8 bytes;
4. creates the ZIP with .NET `System.IO.Compression.ZipFile`;
5. includes one top-level `kanda_reasoner` folder;
6. asks the Windows Explorer ZIP parser to open the archive before release.

This does not modify the source tree or the original `dist` output.

### Canonical ZIP command

Close KANDA Reasoner before packaging, then run:

```powershell
Set-Location E:\kanda_reasoner

$SOURCE = "E:\kanda_reasoner\dist\kanda_reasoner"
$STAGE_PARENT = "E:\kanda_reasoner_release_stage"
$STAGE_APP = "$STAGE_PARENT\kanda_reasoner"
$ZIP = "E:\kanda_reasoner\KandaReasoner-Windows-Portable.zip"
$DESKTOP_ZIP = "$env:USERPROFILE\Desktop\KandaReasoner-Windows-Portable.zip"

Remove-Item `
    -LiteralPath $STAGE_PARENT `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

Remove-Item `
    -LiteralPath $ZIP `
    -Force `
    -ErrorAction SilentlyContinue

Remove-Item `
    -LiteralPath $DESKTOP_ZIP `
    -Force `
    -ErrorAction SilentlyContinue

New-Item `
    -ItemType Directory `
    -Path $STAGE_PARENT `
    -Force |
    Out-Null

Copy-Item `
    -LiteralPath $SOURCE `
    -Destination $STAGE_PARENT `
    -Recurse `
    -Force

$NON_RUNTIME_LONG_PATH_DOCS = Join-Path `
    $STAGE_APP `
    "_internal\kanda_reasoner_app\routing_signal_scorer\mlrt_non_runtime_candidate_reliability"

if (Test-Path $NON_RUNTIME_LONG_PATH_DOCS) {
    Remove-Item `
        -LiteralPath $NON_RUNTIME_LONG_PATH_DOCS `
        -Recurse `
        -Force
}

Write-Host "`nLongest paths remaining in release:"

$PATH_RESULTS = Get-ChildItem `
    -LiteralPath $STAGE_APP `
    -Recurse `
    -Force |
    ForEach-Object {
        $relative = $_.FullName.Substring(
            $STAGE_PARENT.Length + 1
        ).Replace("\", "/")

        [PSCustomObject]@{
            Bytes = [System.Text.Encoding]::UTF8.GetByteCount($relative)
            Path  = $relative
        }
    }

$PATH_RESULTS |
    Sort-Object Bytes -Descending |
    Select-Object -First 5 |
    Format-Table -AutoSize

$MAX_PATH_BYTES = (
    $PATH_RESULTS |
    Measure-Object Bytes -Maximum
).Maximum

if ($MAX_PATH_BYTES -ge 260) {
    throw "Release still contains an archive path of 260 bytes or more."
}

Add-Type `
    -AssemblyName System.IO.Compression.FileSystem

[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $STAGE_APP,
    $ZIP,
    [System.IO.Compression.CompressionLevel]::Optimal,
    $true
)

Copy-Item `
    -LiteralPath $ZIP `
    -Destination $DESKTOP_ZIP `
    -Force

Write-Host "`nNew ZIP:"

Get-Item `
    -LiteralPath $DESKTOP_ZIP |
    Select-Object FullName, Length, LastWriteTime

Write-Host "`nSHA-256:"

Get-FileHash `
    -LiteralPath $DESKTOP_ZIP `
    -Algorithm SHA256

Write-Host "`nTesting Windows Explorer ZIP parser:"

$SHELL = New-Object `
    -ComObject Shell.Application

$ZIP_NAMESPACE = $SHELL.NameSpace($DESKTOP_ZIP)

if ($null -eq $ZIP_NAMESPACE) {
    throw "WINDOWS EXPLORER ZIP CHECK: FAIL"
}

Write-Host "WINDOWS EXPLORER ZIP CHECK: PASS"
Write-Host "Top-level entries:" $ZIP_NAMESPACE.Items().Count
```

Required result:

```text
WINDOWS EXPLORER ZIP CHECK: PASS
Top-level entries: 1
```

The ZIP must contain:

```text
kanda_reasoner\
├── kanda_reasoner.exe
└── _internal\
```

Do not archive the contents with a wildcard. The top-level `kanda_reasoner` folder is intentional and prevents the executable and `_internal` directory from being scattered directly into the user's extraction destination.

Do not publish the ZIP when:

- the Windows Explorer parser returns `FAIL`;
- there is more than one top-level entry;
- any staged archive path is 260 bytes or longer;
- `kanda_reasoner.exe` or `_internal` is absent;
- project-support folders are embedded in the application package.

## 16. Windows Explorer and clean extraction test

The exact Desktop ZIP must first open by double-clicking in Windows Explorer.

Expected view:

```text
kanda_reasoner
```

If Windows Explorer reports that the compressed folder is invalid, the release fails even if Python, `tar.exe`, or `Expand-Archive` can read it.

After the double-click check passes, remove any previous extraction test folder:

```powershell
Remove-Item `
    E:\KandaReasonerZipValidation `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue
```

Extract the exact final ZIP:

```powershell
Expand-Archive `
    -Path .\KandaReasoner-Windows-Portable.zip `
    -DestinationPath E:\KandaReasonerZipValidation `
    -Force
```

Confirm the layout:

```powershell
Test-Path `
    E:\KandaReasonerZipValidation\kanda_reasoner\kanda_reasoner.exe

Test-Path `
    E:\KandaReasonerZipValidation\kanda_reasoner\_internal
```

Expected:

```text
True
True
```

Launch the extracted application:

```powershell
Start-Process `
    -FilePath E:\KandaReasonerZipValidation\kanda_reasoner\kanda_reasoner.exe `
    -WorkingDirectory E:\KandaReasonerZipValidation\kanda_reasoner
```

Confirm:

- the GUI opens without a terminal window;
- startup creates no `*_show_project_to_AI` or `*_delete_after_daily_work` folder;
- the important tabs load;
- the application closes normally;
- a selected nested project creates its support folders at the selected project's drive root.

Do not publish a ZIP that was never opened by Windows Explorer, extracted to a clean folder, and executed.

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

The original July 2026 ZIP hashes are obsolete and must not be copied into a new release.

The executable name, console mode, packaged data, staging cleanup, and ZIP format have changed. Every rebuilt archive requires a fresh size and SHA-256 calculated from the exact release asset.

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
[ ] dist\kanda_reasoner\kanda_reasoner.exe exists
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
[ ] Relocated kanda_reasoner.exe opens
[ ] Relocated critical tabs pass
[ ] Final ZIP created from the staged release copy with .NET ZipFile
[ ] Windows Explorer opens the final ZIP without an invalid-folder error
[ ] Windows Explorer parser reports exactly one top-level entry
[ ] No staged archive path is 260 bytes or longer
[ ] Final ZIP extracted to a clean folder
[ ] Extracted kanda_reasoner\kanda_reasoner.exe opens without a terminal window
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
Set-Location .\dist\kanda_reasoner
.\kanda_reasoner.exe
```

The release baseline uses `console=False`, so no terminal window opens. Diagnose packaged startup failures through persistent application logs or a temporary local debug build using `console=True`.

Look for:

- `ModuleNotFoundError`;
- missing DLL;
- missing Qt plugin;
- missing file;
- incorrect resource path;
- import-time exception.

Do not publish a console-enabled executable merely to expose nonfatal Qt warnings. Use `console=True` only in a temporary diagnostic build when necessary.

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

### Windows Explorer says the ZIP is invalid

Do not assume the archive is acceptable merely because Python, `tar.exe`, or `Expand-Archive` can read it.

Check:

1. the archive was created through the canonical staged .NET ZIP procedure;
2. the Windows Explorer `Shell.Application` parser returns a namespace;
3. the ZIP contains one top-level `kanda_reasoner` folder;
4. no archive path is 260 bytes or longer;
5. the known non-runtime long-path planning directory was removed from the staged release copy.

Recreate the ZIP rather than reusing an older archive.

### The ZIP opens but users report missing files

Confirm the ZIP contains the complete staged folder:

```text
kanda_reasoner\
├── kanda_reasoner.exe
└── _internal\
```

Do not distribute the executable alone.

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
Start-Process .\dist\kanda_reasoner\kanda_reasoner.exe
```

Then relocate:

```powershell
Remove-Item `
    E:\KandaReasonerPortableTest `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

Copy-Item `
    .\dist\kanda_reasoner `
    E:\KandaReasonerPortableTest `
    -Recurse

Start-Process `
    E:\KandaReasonerPortableTest\kanda_reasoner.exe
```

Then create and extract the Windows-compatible ZIP:

```powershell
Set-Location E:\kanda_reasoner

$SOURCE = "E:\kanda_reasoner\dist\kanda_reasoner"
$STAGE_PARENT = "E:\kanda_reasoner_release_stage"
$STAGE_APP = "$STAGE_PARENT\kanda_reasoner"
$ZIP = "E:\kanda_reasoner\KandaReasoner-Windows-Portable.zip"

Remove-Item `
    -LiteralPath $STAGE_PARENT `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

Remove-Item `
    -LiteralPath $ZIP `
    -Force `
    -ErrorAction SilentlyContinue

New-Item `
    -ItemType Directory `
    -Path $STAGE_PARENT `
    -Force |
    Out-Null

Copy-Item `
    -LiteralPath $SOURCE `
    -Destination $STAGE_PARENT `
    -Recurse `
    -Force

$NON_RUNTIME_LONG_PATH_DOCS = Join-Path `
    $STAGE_APP `
    "_internal\kanda_reasoner_app\routing_signal_scorer\mlrt_non_runtime_candidate_reliability"

if (Test-Path $NON_RUNTIME_LONG_PATH_DOCS) {
    Remove-Item `
        -LiteralPath $NON_RUNTIME_LONG_PATH_DOCS `
        -Recurse `
        -Force
}

$PATH_RESULTS = Get-ChildItem `
    -LiteralPath $STAGE_APP `
    -Recurse `
    -Force |
    ForEach-Object {
        $relative = $_.FullName.Substring(
            $STAGE_PARENT.Length + 1
        ).Replace("\", "/")

        [PSCustomObject]@{
            Bytes = [System.Text.Encoding]::UTF8.GetByteCount($relative)
            Path  = $relative
        }
    }

if ((($PATH_RESULTS | Measure-Object Bytes -Maximum).Maximum) -ge 260) {
    throw "Release still contains an archive path of 260 bytes or more."
}

Add-Type `
    -AssemblyName System.IO.Compression.FileSystem

[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $STAGE_APP,
    $ZIP,
    [System.IO.Compression.CompressionLevel]::Optimal,
    $true
)

$SHELL = New-Object -ComObject Shell.Application
$ZIP_NAMESPACE = $SHELL.NameSpace($ZIP)

if ($null -eq $ZIP_NAMESPACE) {
    throw "WINDOWS EXPLORER ZIP CHECK: FAIL"
}

Write-Host "WINDOWS EXPLORER ZIP CHECK: PASS"
Write-Host "Top-level entries:" $ZIP_NAMESPACE.Items().Count
```

Then double-click the ZIP in Windows Explorer. After it opens successfully:

```powershell
Remove-Item `
    E:\KandaReasonerZipValidation `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

Expand-Archive `
    -Path .\KandaReasoner-Windows-Portable.zip `
    -DestinationPath E:\KandaReasonerZipValidation `
    -Force

Start-Process `
    -FilePath E:\KandaReasonerZipValidation\kanda_reasoner\kanda_reasoner.exe `
    -WorkingDirectory E:\KandaReasonerZipValidation\kanda_reasoner
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
