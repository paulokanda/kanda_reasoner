# 🧠 `project_analizer_2_runner.py` — What Is It For?
Turn your codebase into living, navigable documentation and actionable insights.  
This runner is the **IDE‑friendly + CLI** entry point for **KANDA’s ProjectAnalyzer**. It orchestrates analysis passes (complexity, dependencies, hotspots), auto‑generates docs, serves a local web explorer, and can scaffold features — all from one file.

---

## ✨ Key Capabilities (at a glance)
- **Dev tools bootstrap**: generate docs & helpers with `generate-dev_tools`
- **Group & ad‑hoc reports**: document logical areas (via `file_groups.yaml`) or any file glob
- **Complexity metrics**: spot the top offenders quickly (`metrics`)
- **Dependency maps & hotspots**: reveal coupling risk (`dep-hotspots`, `flow-diagrams`)
- **Git metadata**: authorship, recency, churn (`git-meta`)
- **Tech debt surfacing**: `TODO`, `FIXME`, and friends (`debt-report`)
- **Interactive web explorer**: browse architecture in your browser (`web-explorer`)
- **Onboarding docs**: architecture, conventions, and diagrams for new devs
- **Feature scaffolding**: create boilerplate safely (`scaffold`)

> Works great with **PyCharm** (no‑args “Run” = auto docs + group reports), but also shines in CI/CD.

---

## 🚀 Quickstart
```bash
# Option A — Run a full dev-tools generation
python project_analizer_2_runner.py generate-dev_tools

# Option B — Explore metrics for the N most complex files
python project_analizer_2_runner.py metrics -n 10

# Option C — Launch the interactive web explorer (default port 8000)
python project_analizer_2_runner.py web-explorer --port 8000
```

**Windows / PyCharm tip**  
If you run with **no CLI args** (green ▶️), the runner enters **IDE mode**:  
1) builds/refreshes architecture docs; 2) auto‑executes **group reports** flagged with `auto: true` in `file_groups.yaml`, or from the `PA_AUTO_GROUPS` env var.

---

## 🧭 Command Overview
| Command | What it does | Typical Output |
|---|---|---|
| `generate-dev_tools` | One‑shot docs + tool bootstrap | Markdown/HTML docs, diagrams |
| `group-report <group>` | Document a named group from `file_groups.yaml` | Group overview, diagrams, hotspots |
| `ad-hoc-report <glob...>` | Report on any set of files | Localized complexity & coupling notes |
| `metrics [-n N]` | Top‑N complexity offenders | Sorted list with scores & paths |
| `dep-hotspots` | Modules with dangerous coupling | Tables + dependency graphs |
| `flow-diagrams` | Control/data‑flow visuals | Diagrams (Mermaid/Graphviz) |
| `git-meta [--since ...]` | Authors, churn, recency | Tabular git analytics |
| `debt-report` | TODO/FIXME/XXX harvest | File/line references |
| `find <term> [-n N]` | Grep‑like smart finder | Ranked matches |
| `export-model [-f yaml|json] [-o FILE]` | Export the internal project model | `model.yaml` / `model.json` |
| `web-explorer [--port P]` | Local interactive UI | Web server (localhost) |
| `scaffold <kind> <Name>` | Safe code boilerplate | Ready‑to‑fill stubs |
| `create-download-portal` | Local portal for artifacts | Static site under `dev_tools/` |

> **Flags** vary by command; run `python project_analizer_2_runner.py <cmd> -h` for specifics.

---

## 🧩 IDE Mode (No‑Args Behavior)
Running with **no arguments** (e.g., PyCharm “Run”) is a **curated pipeline**:
1. `generate_architecture_docs()` — refresh docs, structure, and diagrams  
2. `_run_auto_groups()` — executes groups where `auto: true` in `file_groups.yaml`  
3. If env `PA_AUTO_GROUPS` is set, it overrides/extends auto groups (comma‑separated list)

```yaml
# file_groups.yaml (example)
model_utils:
  name: "Model Utilities"
  description: "Data transforms, validators, loaders"
  include:
    - "eeg_data_graphs_stats/**/models/*.py"
  auto: true

gui_core:
  name: "GUI Core"
  include:
    - "KandaModules/**/eeg_visualizer*.py"
    - "KandaModules/**/interface_manager*.py"
  auto: false
```

Set **ad‑hoc** via environment:
```bash
# Linux/macOS
export PA_AUTO_GROUPS=model_utils,gui_core
# Windows (PowerShell)
$env:PA_AUTO_GROUPS="model_utils,gui_core"
```

---

## 🛠️ Typical Workflows

### 1) “What’s risky right now?”
```bash
python project_analizer_2_runner.py dep-hotspots
python project_analizer_2_runner.py metrics -n 15
python project_analizer_2_runner.py debt-report
```

### 2) “I need docs a new dev can read in 10 minutes.”
```bash
python project_analizer_2_runner.py generate-dev_tools
python project_analizer_2_runner.py web-explorer --port 8000
```

### 3) “Just this area, please.”
```bash
python project_analizer_2_runner.py group-report model_utils
python project_analizer_2_runner.py ad-hoc-report "KandaModules/**/timeline*.py" "eeg_data_graphs_stats/**/*.py"
```

### 4) “Ship the internal map to CI.”
```bash
python project_analizer_2_runner.py export-model -f yaml -o artifacts/model.yaml
```

---

## 🌳 What the Runner Actually Does
At startup, it ensures the **project root** is importable:
```python
sys.path.insert(0, str(PROJECT_ROOT))
```
Then it uses `argparse` to route subcommands to the **ProjectAnalyzer** with the right feature toggles. Helper functions include:

- `_run_auto_groups(pa)` — resolves which groups to run (YAML + `PA_AUTO_GROUPS`)
- `_expand_repo_relative(pa, patterns)` — expands repo‑relative globs/paths for `ad-hoc-report`

The heavy lifting (parsing, modeling, rendering) lives in `ProjectAnalyzer` — the runner **just wires I/O and modes**.

---

## 🖥️ PyCharm Integration (Zero‑Friction)
1. Create a **Run configuration** for `project_analizer_2_runner.py` with **no parameters**.  
2. (Optional) Set `PA_AUTO_GROUPS` in the **Environment** section.  
3. Hit ▶️. Your docs refresh, groups run, and outputs land under your configured `dev_tools/` or docs folder.

For **command‑specific** runs, duplicate the config and add parameters, e.g.:
```
Parameters: metrics -n 20
Parameters: group-report gui_core
```

---

## 🌐 Web Explorer
Serve an interactive view of the project:
```bash
python project_analizer_2_runner_*.py web-explorer --port 8000
```
- Browse modules, edges, complexity
- Jump to source locations
- Filter by group

> Perfect for onboarding or architecture reviews.

---

## ⚙️ Environment Variables
- `PA_AUTO_GROUPS` — comma‑separated group names to auto‑run in IDE mode
- `PA_OUTPUT_DIR` — override default artifacts directory (if supported by your setup)
- `PA_VERBOSITY` — tune log verbosity (e.g. `INFO`, `DEBUG`)

Windows PowerShell:
```powershell
$env:PA_AUTO_GROUPS="model_utils,gui_core"
$env:PA_VERBOSITY="DEBUG"
```

---

## 🧭 Exit Codes (CI‑friendly)
- `0` — success
- `1` — generic error (bad args, unexpected exception)
- `2` — configuration issue (missing YAML, unreadable paths)
- `3` — analysis failure (parse error in target files, timeouts)

> Integrate into pipelines to **fail on risk** (e.g., too‑high complexity or debt counts).

---

## 🧪 Troubleshooting
- **Imports failing in analysis** — ensure runner added repo root to `sys.path` (it does by default). If you vendor submodules, check your `.pth` or local venv.
- **Empty group report** — confirm `file_groups.yaml` `include:` patterns match (globs are repo‑relative).
- **Web explorer won’t bind** — try another port, e.g., `--port 8088`. Confirm firewall rules on Windows.
- **Very large repos** — prefer `group-report` and `ad-hoc-report` for focused runs.

---

## 🧭 Design Philosophy
- **Single entry point** for analysts, devs, CI
- **Declarative groups** via YAML for repeatability
- **Safe defaults** in IDE mode; explicit power in CLI mode
- **Separation of concerns**: runner = orchestration; analyzer = domain logic

---

## 🗺️ Minimal Architecture (Mermaid)
```mermaid
flowchart LR
  A[project_analizer_2_runner.py] --> B[Argparse Router]
  B -->|generate-dev_tools| C[ProjectAnalyzer.generate_docs()]
  B -->|metrics / deps / flow| D[Analysis Passes]
  B -->|group-report| E[GroupResolver (file_groups.yaml)]
  B -->|ad-hoc| F[PathExpander (repo‑relative globs)]
  B -->|web-explorer| G[Web Server]
  C --> H[Artifacts (docs, diagrams)]
  D --> H
  E --> H
  F --> H
  G --> H
```

---

## 📌 FAQ
**Q. Do I need the whole KANDA stack?**  
A. No. The runner is thin; as long as `ProjectAnalyzer` and its deps are importable, you’re set.

**Q. Can I limit scope to speed it up?**  
A. Yes — use `group-report` or `ad-hoc-report` with tight globs.

**Q. Where do outputs go?**  
A. By default under your dev/docs artifacts folder; override via env or analyzer config if available.

---

## ✅ TL;DR
Use this runner to **generate architecture docs**, **find risks fast**, **serve an interactive explorer**, and **standardize analysis** across the team — in one consistent interface for IDEs, terminals, and CI.

