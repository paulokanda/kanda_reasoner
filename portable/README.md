# KANDA Reasoner Portable Builder

This folder is the independent Portable Distribution Box.

It never invokes, refreshes, publishes, moves, deletes, or owns Show Project
to AI output.

## Run

```powershell
& "C:\Users\paulo\AppData\Local\Programs\Python\Python312\python.exe" `
    "E:\kanda_reasoner\portable\create_kanda_reasoner_portable.py"
```

Type:

```text
BUILD KANDA PORTABLE
```

After the clean extracted application opens, test the main application,
Project Structure 3D, Show Project, Audit Project, and confirm Web AI credentials
start blank. Then type:

```text
YES
```

Final output:

```text
E:\KandaReasoner-Windows-Portable.zip
```

## Replace an existing output

```powershell
& "C:\Users\paulo\AppData\Local\Programs\Python\Python312\python.exe" `
    "E:\kanda_reasoner\portable\create_kanda_reasoner_portable.py" `
    --replace-existing
```

The script additionally requires:

```text
REPLACE KANDA PORTABLE
```

The existing drive-root ZIP is not replaced until the new candidate passes all
build, archive, clean-extraction, GUI-smoke, project-immutability, and Project
Support immutability checks.

## Box boundaries

Project source:

```text
E:\kanda_reasoner
```

Project Support:

```text
E:\kanda_reasoner_show_project_to_AI
```

Transient build:

```text
E:\kanda_reasoner_delete_after_daily_work\portable_build\<run>
```

Final Portable:

```text
E:\KandaReasoner-Windows-Portable.zip
```


## Non-interactive destination

Use an existing folder explicitly:

```powershell
C:\Users\paulo\AppData\Local\Programs\Python\Python312\python.exe `
    E:\kanda_reasoner\portable\create_kanda_reasoner_portable.py `
    --output-dir E:\
```
