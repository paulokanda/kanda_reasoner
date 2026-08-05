# KANDA REASONER PORTABLE WINDOWS — CURRENT CANONICAL HANDOFF

Status: current operational owner  
Feature: `kanda-reasoner-portable-builder-install-v1r6`  
Project: `E:\kanda_reasoner`  
Portable builder Box: `E:\kanda_reasoner\portable`  
Project Support: `E:\kanda_reasoner_show_project_to_AI`  
Transient build root: `E:\kanda_reasoner_delete_after_daily_work\portable_build\<run>`  
Final ZIP: `<user-selected-folder>\KandaReasoner-Windows-Portable.zip`

## 1. Authority and supersession

The older `KANDA_REASONER_PORTABLE_WINDOWS_UPDATE_HANDOFF` remains useful for
known runtime regressions, required PyInstaller contents, visible-tab smoke
tests, relocation, clean extraction, and publication hygiene.

Its old operational paths are superseded:

- do not use `E:\kanda_reasoner\build`;
- do not use `E:\kanda_reasoner\dist`;
- do not create the final ZIP inside `E:\kanda_reasoner`;
- do not require `E:\kanda_reasoner\.venv`;
- do not use `Compress-Archive` as the canonical ZIP owner;
- do not merge generated build results into project source;
- do not invoke or modify Show Project to AI.

## 2. Canonical owners

The committed packaging specification remains:

`E:\kanda_reasoner\KandaReasonerWindows.spec`

The public Portable creator is:

`E:\kanda_reasoner\portable\create_kanda_reasoner_portable.py`

The governed interpreter is:

`C:\Users\paulo\AppData\Local\Programs\Python\Python312\python.exe`

PyInstaller is pinned to:

`6.21.0`

## 3. Run

```powershell
& "C:\Users\paulo\AppData\Local\Programs\Python\Python312\python.exe" `
    "E:\kanda_reasoner\portable\create_kanda_reasoner_portable.py"
```

The creator must print:

```text
PORTABLE BUILDER VERSION: v1r6
PORTABLE BUILDER FEATURE ID: kanda-reasoner-portable-builder-install-v1r6
```

Do not continue when another revision is printed.

Type:

```text
BUILD KANDA PORTABLE
```

Choose an existing destination folder. The creator rejects a selection inside:

- `E:\kanda_reasoner`;
- `E:\kanda_reasoner_show_project_to_AI`;
- `E:\kanda_reasoner_delete_after_daily_work`.

## 4. External build boundary

PyInstaller uses:

```text
--workpath <external transient>\pyinstaller_work
--distpath <external transient>\pyinstaller_dist
PYINSTALLER_CONFIG_DIR=<external transient>\pyinstaller_config
TEMP=<external transient>\temp
TMP=<external transient>\temp
```

The creator must not write `build`, `dist`, candidate ZIPs, or extracted test
applications into the project.

## 5. Specification preflight

Before PyInstaller starts, the creator verifies that the committed spec:

- uses `reasoner_tools_gui.py`;
- uses `collect_data_files`;
- uses `collect_submodules`;
- includes Qt WebEngine Core and Widgets;
- includes Qt WebChannel;
- includes `collector_main_help`;
- contains no hardcoded `E:\kanda_reasoner`;
- contains no `C:\Users\paulo`;
- contains no `.venv` or PyCharm path.

## 6. Known nonfatal warning

This warning is known from the validated baseline:

```text
Failed to collect submodules for
kanda_reasoner_app.reasoner_context_collector.developer_tools
because collector_packaging_metadata is missing
```

It is not a release failure by itself. The current clean-extracted runtime tests
remain authoritative. Do not make speculative production changes only to
silence it.

## 7. Release-content hygiene

After PyInstaller, the creator copies the one-folder application into external
release staging.

It removes:

- the known non-runtime long-path documentation subtree;
- `__pycache__`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`;
- `.bak`, `.bak_*`, `.backup`, `.orig`, `.rej`, and editor debris.

It preserves legitimate runtime modules whose names contain phrases such as
`first_prompt_files_private_impl.py`.

It rejects real generated handoff families and Portable ZIPs.

## 8. Windows ZIP contract

The creator uses the packaged .NET ZIP helper, not `Compress-Archive`.

The final candidate must:

- be accepted by Windows Explorer;
- have exactly one top-level application folder;
- pass CRC;
- contain one direct application executable;
- contain no path traversal;
- contain no case-insensitive duplicate members;
- contain no member path longer than 259 UTF-8 bytes;
- contain no Show Project output;
- contain no backup/cache debris;
- contain no nested Portable ZIP;
- contain no `.env` credential file.

## 9. Required static runtime files

The packaged output must contain:

- `QtWebEngineProcess.exe`;
- `qwindows.dll`;
- the direct KANDA executable;
- `_internal`.

A major unexplained size reduction remains an investigation signal, not proof.

## 10. Human runtime validation

The creator extracts the exact candidate ZIP into external clean storage and
launches it twice.

First launch:

- main window opens and remains responsive;
- Project Structure 3D loads;
- Show Project to AI loads;
- Audit Project loads;
- Config Web AI does not automatically display credentials;
- changed or important visible tabs open.

Type:

```text
FIRST PASS
```

The creator closes that process and relaunches the same clean-extracted
application.

After successful relaunch, type:

```text
PORTABLE TESTS PASS
```

Do not type either phrase unless the checks were actually performed.

## 11. Publication

Only after static, archive, source-immutability, Project-Support-immutability,
clean-extraction, first-launch, and relaunch checks pass may the candidate be
published to the selected folder.

An existing final ZIP is not silently overwritten. Use `--replace-existing`
and type `REPLACE KANDA PORTABLE`.

The final report must include:

- output path;
- exact byte size;
- SHA-256;
- ZIP member count;
- maximum member path;
- `STATUS: PORTABLE READY`.

## 12. Git and GitHub

Do not commit the Portable ZIP to normal repository history.

Upload the validated ZIP as a GitHub Release asset and publish its new SHA-256.
The ZIP generated automatically by GitHub under “Source code” is not the
Portable application asset.

## 13. Definition of done

```text
PORTABLE CANONICAL SPECIFICATION: PASS
PORTABLE SPEC MACHINE-SPECIFIC PATHS: ABSENT
PORTABLE PYINSTALLER BUILD: PASS
PORTABLE BUILD PRODUCTS OUTSIDE PROJECT: PASS
PORTABLE QT WEBENGINE PROCESS: PASS
PORTABLE QT WINDOWS PLATFORM PLUGIN: PASS
PORTABLE NON-RUNTIME DEBRIS ABSENT: PASS
PORTABLE WINDOWS EXPLORER ZIP CHECK: PASS
PORTABLE ZIP INTEGRITY: PASS
PORTABLE CLEAN ZIP EXTRACTION: PASS
PORTABLE APPLICATION FIRST LAUNCH: PASS
PORTABLE APPLICATION RELAUNCH: PASS
PORTABLE PROJECT SOURCE UNCHANGED: PASS
SHOW PROJECT SUPPORT UNCHANGED: PASS
PORTABLE BUILD RESULTS NOT MERGED INTO PROJECT: PASS
STATUS: PORTABLE READY
```


## Installer transaction correction

The installer validates the incoming builder from external transient staging
under a child folder named exactly `portable`. It never renames the candidate
package to `portable.__installing__...` and never places the unvalidated
candidate inside the project. This preserves canonical imports such as
`portable.policy` during extracted, incoming, and installed validation.

Required package-time markers:

```text
PORTABLE INSTALLER EXTERNAL CANDIDATE CONTRACT: PASS
PORTABLE INCOMING PACKAGE IMPORT FIXTURE: PASS
PORTABLE INSTALLED PACKAGE IMPORT FIXTURE: PASS
```
