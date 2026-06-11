#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_Road_map.py
==================
Produces **two artifacts** in your existing
`results_report/` folder (no new folders created):

1) A machine-readable roadmap (`.json` or `.py`)
2) A human-friendly architecture atlas (`.txt`)

- Parallelized analysis
- Optional linters/security tools (flake8/pylint/bandit/safety) with safe fallbacks
- Python â‰¥ 3.8

PyCharm Green-Button Behavior
-----------------------------
If launched with **no CLI args** (typical green â–¶ï¸):
  â€¢ Root auto-detected
  â€¢ Output goes to results_report
  â€¢ Defaults: --exclude dev_tools_old,k06_templates  --workers 0
  â€¢ If Safety is not installed, it auto-sets --skip-safety

You can still override everything via CLI flags when needed.
"""
from __future__ import annotations

import argparse
import ast
import datetime as _dt
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set

# ---------- optional deps ----------
try:
    from radon.visitors import ComplexityVisitor  # type: ignore
except ModuleNotFoundError:                        # pragma: no cover
    ComplexityVisitor = None  # type: ignore

###############################################################################
# Paths & constants
###############################################################################

HERE = Path(__file__).resolve().parent


def _find_project_root() -> Path:
    # Find a parent that contains results_report; else fall back to parent of dev_tools
    for up in [HERE, *HERE.parents]:
        if (up / "dev_tools" / "results_report").exists():
            return up
    return HERE.parents[1] if len(HERE.parents) >= 2 else HERE

PROJECT_ROOT = _find_project_root()
OUT_DIR = PROJECT_ROOT / "dev_tools" / "results_report"

if not OUT_DIR.exists():
    raise SystemExit(
        f"[RoadMap] Output folder not found:\n  {OUT_DIR}\n"
        "Please create it (or run the EveryPush analyzer once) and re-run."
    )

# Default filenames in the existing results_report folder
_stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M")
DEFAULT_JSON = OUT_DIR / f"road_map_{_stamp}.json"
DEFAULT_TXT  = OUT_DIR / f"architecture_atlas_{_stamp}.txt"

# Extensions & filters (new)
INCLUDE_EXTS = {".py", ".json"}
EXCLUDE_EXTS = {".md", ".txt"}  # explicit, per your request

# Signals & regex
_RE_TODO        = re.compile(r"#\s*(TODO|FIXME|XXX)", re.I)
_SECURITY_CALLS = {"eval", "exec", "execfile", "os.system", "subprocess", "pickle.loads"}

###############################################################################
# File-level analysis object
###############################################################################

class FileInfo:
    """Gather static facts (and optional external-tool counts) for one *.py* file."""

    def __init__(self, path: Path, encodings: Sequence[str]):
        self.path  = path
        self.error: Optional[str] = None
        self.text  = self._read(encodings)
        self.ast   = self._parse()

        # collected data
        self.imports, self.exports = set(), set()
        self.classes:   List[Dict[str, Any]] = []
        self.functions: List[Dict[str, Any]] = []
        self.todo_lines: List[int] = []
        self.security_flags: List[str] = []
        self.cc_scores: List[int] = []
        self.undefined_refs: Set[str] = set()

        # linter / security counts
        self.flake8 = self.pylint = self.bandit = None

        if self.text and self.ast:
            self._walk()
            self._external_metrics()

    # ---------- I/O ----------
    def _read(self, encs: Sequence[str]) -> Optional[str]:
        for enc in encs:
            try:
                return self.path.read_text(encoding=enc, errors="replace")
            except Exception:
                continue
        self.error = "Unreadable file"
        return None

    def _parse(self) -> Optional[ast.Module]:
        try:
            return ast.parse(self.text or "", filename=str(self.path))
        except SyntaxError as e:
            self.error = f"Syntax error: {e}"
            return None

    # ---------- AST walk ----------
    def _walk(self) -> None:
        assert self.ast
        defined: Set[str] = set()
        called_in: Dict[str, List[str]] = defaultdict(list)

        # imports
        for n in ast.walk(self.ast):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                for a in n.names:
                    self.imports.add(a.name.split(".")[0])

        # defs / calls / exports
        for n in ast.walk(self.ast):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                info = self._func_info(n, isinstance(n, ast.AsyncFunctionDef))
                self.functions.append(info)
                defined.add(n.name)
                for c in info["called_functions"]:
                    called_in[c].append(str(self.path))
            elif isinstance(n, ast.ClassDef):
                self.classes.append(self._class_info(n))
                defined.add(n.name)
            elif isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        self.exports.add(t.id)
            elif isinstance(n, ast.Call):
                if (cn := self._call_name(n.func)) in _SECURITY_CALLS:
                    self.security_flags.append(cn)

        # undefined refs & TODO lines
        used = {i.id for i in ast.walk(self.ast) if isinstance(i, ast.Name)}
        used_filtered = {
            u for u in used
            if u not in builtins_set() and not (u.startswith("__") and u.endswith("__"))
        }
        self.undefined_refs = used_filtered - defined - self.imports

        for ln, line in enumerate((self.text or "").splitlines(), 1):
            if _RE_TODO.search(line):
                self.todo_lines.append(ln)

        # back-fill "called_in"
        for f in self.functions:
            f["called_in"] = called_in.get(f["name"], [])

        # cyclomatic complexity
        if ComplexityVisitor:
            vis = ComplexityVisitor.from_ast(self.ast)
            self.cc_scores = [b.complexity for b in vis.functions]

    # ---------- node helpers ----------
    def _func_info(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool) -> Dict[str, Any]:
        params  = [a.arg for a in node.args.args]
        returns = self._ann(node.returns)
        dec     = node.decorator_list[0].id if node.decorator_list and isinstance(node.decorator_list[0], ast.Name) else None
        called  = [self._call_name(c.func) for c in ast.walk(node) if isinstance(c, ast.Call)]
        return {
            "name": node.name,
            "parameters": params,
            "return_type": returns,
            "decorator": dec,
            "defined_in": str(self.path),
            "called_in": [],
            "called_by": called,              # historical naming: actually "calls"
            "is_async": is_async,
            "docstring": ast.get_docstring(node),
            "called_functions": called,
        }

    def _class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        bases   = [self._name(b) for b in node.bases]
        methods = [m.name for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
        attrs   = [
            t.targets[0].id for t in node.body
            if isinstance(t, ast.Assign) and isinstance(t.targets[0], ast.Name)
        ]
        return {
            "name": node.name,
            "methods": methods,
            "inheritance": bases,
            "attributes": attrs,
            "docstring": (ast.get_docstring(node) or None),
        }

    def _name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._name(node.value)}.{node.attr}"
        return "<expr>"

    def _call_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._call_name(node.value)}.{node.attr}"
        return "<call>"

    def _ann(self, ann: Optional[ast.AST]) -> str:
        return self._name(ann) if ann else "None"

    # ---------- external tools ----------
    def _run(self, exe: str, *args: str) -> Optional[str]:
        bin_ = shutil.which(exe)
        if not bin_:
            return None
        cp = subprocess.run([bin_, *args], capture_output=True, text=True, check=False)
        return cp.stdout

    def _external_metrics(self) -> None:
        if out := self._run("flake8", str(self.path), "--format=%(code)s:%(text)s"):
            self.flake8 = len([l for l in out.splitlines() if l.strip()])
        if out := self._run("pylint", "--disable=all", "--enable=E,W", "--output-format=text", "--score=n", str(self.path)):
            self.pylint = len([l for l in out.splitlines() if ":" in l and not l[0].isdigit()])
        if out := self._run("bandit", "-q", "-f", "json", str(self.path)):
            try:
                self.bandit = len(json.loads(out or "{}").get("results", []))
            except json.JSONDecodeError:
                pass

###############################################################################
# Serialisation helpers
###############################################################################

    def _file_type(self) -> str:
        # NEW: label JSON files as 'json'
        if self.path.suffix.lower() == ".json":
            return "json"
        # existing Python heuristics:
        n = self.path.name
        norm = str(self.path).replace("\\", "/")
        if re.search(r"(^|/)(test_.*\.py|.*_test\.py)$", norm):
            return "test"
        if n == "__main__.py" or (self.path.stem.endswith("main") and n.endswith(".py")):
            return "script"
        return "module"

    def _clean_func(self, f: Dict[str, Any]) -> Dict[str, Any]:
        d = f.copy()
        d.pop("called_functions", None)
        return d

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self._file_type(),
            "size": self.path.stat().st_size,
            "last_modified": int(self.path.stat().st_mtime),
            "imports": sorted(self.imports),
            "exports": sorted(self.exports),
            "functions": [self._clean_func(f) for f in self.functions],
            "classes": self.classes,
            "flake8": self.flake8,
            "pylint": self.pylint,
            "bandit": self.bandit,
            "security_flags": self.security_flags,
        }

###############################################################################
# Project-level helpers
###############################################################################

def entry_points(root: Path) -> List[str]:
    return [str(p.relative_to(root))
            for p in (root/"__main__.py", root/"app.py", root/"main.py") if p.exists()]

def safety_vulns() -> Optional[int]:
    exe = shutil.which("safety")
    if not exe:
        return None
    cp = subprocess.run([exe, "check", "--json"], capture_output=True, text=True, check=False)
    try:
        return len(json.loads(cp.stdout or "[]"))
    except json.JSONDecodeError:
        return None

###############################################################################
# Tree renderer for architecture section
###############################################################################
BOX_MID, BOX_END, BOX_PIPE = " â”œâ”€ ", " â””â”€ ", " â”‚  "

def _icon(name: str, ftype: str) -> str:
    if ftype == "test":   return "ðŸ§ª"
    if ftype == "script": return "ðŸš€"
    return "ðŸ“„"

def render_tree(file_map: dict[str, Any]) -> List[str]:
    rels = sorted(file_map)

    def walk(base: str, subs: list[str], prefix=""):
        lines: List[str] = []
        last = len(subs) - 1
        for i, sub in enumerate(subs):
            join = BOX_END if i == last else BOX_MID
            if "/" in sub:
                folder = sub.split("/", 1)[0]
                lines.append(f"{prefix}ðŸ“‚ {folder}/")
                children = [c for c in subs if c.startswith(folder + "/")]
                lines += walk(folder, [c[len(folder)+1:] for c in children],
                              prefix + ("    " if i == last else BOX_PIPE))
            else:
                key = f"{base}{sub}" if base else sub
                ftype = file_map[key]["type"]
                lines.append(f"{prefix}{join}{_icon(sub, ftype)} {sub}")
        return lines

    return walk("", rels)

###############################################################################
# Road-map builder
###############################################################################

def build_map(
    root: Path,
    encs: Sequence[str],
    workers: int,
    skip_safety: bool,
    excludes: Sequence[str],
) -> Dict[str, Any]:
    """
    Build a project roadmap. Scans only .py and .json; excludes any path
    containing substrings in `excludes`, and files with EXCLUDE_EXTS.
    JSON files are included in file_structure as resources (no AST).
    """
    # Helper: exclusion by substring or extension
    def _excluded(p: Path) -> bool:
        s = str(p).lower()
        if any(x.lower() in s for x in excludes):
            return True
        if p.suffix.lower() in EXCLUDE_EXTS:
            return True
        return False

    # Collect targets (only .py and .json), respecting excludes
    candidates = (p for p in root.rglob("*") if p.is_file())
    target_files = [p for p in candidates
                    if p.suffix.lower() in INCLUDE_EXTS and not _excluded(p)]

    if not target_files:
        raise SystemExit("No target files found (after applying includes/excludes).")

    # Split by type so JSON files don't go through AST parsing
    py_files    = [p for p in target_files if p.suffix.lower() == ".py"]
    json_files  = [p for p in target_files if p.suffix.lower() == ".json"]

    infos: dict[Path, FileInfo] = {}
    skipped: List[str] = []

    # Decide worker count if <= 0
    if workers <= 0:
        workers = min(32, (os.cpu_count() or 4) + 4)

    # Analyze Python files in parallel
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(FileInfo, p, encs): p for p in py_files}
        for fut in as_completed(futs):
            fi = fut.result()
            p = futs[fut]
            infos[p] = fi
            if fi.error:
                skipped.append(f"{p.relative_to(root)}: {fi.error}")

    def rel(p):
        return str(p.relative_to(root))

    # Dependency graph (only meaningful for Python files)
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, str]] = []
    for p, fi in infos.items():
        nid = rel(p)
        nodes.append({
            "id": nid,
            "type": fi._file_type(),
            "weight": len(fi.functions) + len(fi.classes)
        })
        # file-level import edges
        for imp in fi.imports:
            edges.append({"source": nid, "target": imp, "relationship": "imports"})
        # function-level calls (best-effort)
        for f in fi.functions:
            for tgt in f["called_by"]:
                edges.append({"source": nid, "target": tgt, "relationship": "calls"})

    # Complexity aggregation (Python only)
    cc_map = {
        rel(p): round(sum(fi.cc_scores) / len(fi.cc_scores), 2)
        for p, fi in infos.items() if fi.cc_scores
    }
    cc_vals = list(cc_map.values())
    complexity = {
        "average": round(sum(cc_vals) / len(cc_vals), 2) if cc_vals else 0.0,
        "max": max(cc_vals) if cc_vals else 0,
        "files": cc_map,
    }

    # Unimplemented/Undefined refs & TODOs (Python only)
    unimpl: List[Dict[str, Any]] = []
    for p, fi in infos.items():
        rp = rel(p)
        for ref in sorted(fi.undefined_refs):
            unimpl.append({"signature": ref, "references": [rp], "confidence": 0.6})
        for ln in fi.todo_lines:
            unimpl.append({"signature": f"TODO@{rp}:{ln}", "references": [rp], "confidence": 0.9})

    # file_structure for Python + JSON
    file_structure: Dict[str, Any] = {rel(p): fi.to_dict() for p, fi in infos.items()}
    for jp in json_files:
        file_structure[rel(jp)] = {
            "type": "json",
            "size": jp.stat().st_size,
            "last_modified": int(jp.stat().st_mtime),
            "imports": [],
            "exports": [],
            "functions": [],
            "classes": [],
            "flake8": None,
            "pylint": None,
            "bandit": None,
            "security_flags": [],
        }

    # Totals
    total_files = len(target_files)
    total_py    = len(py_files)
    total_json  = len(json_files)

    project_sec = {
        "name": root.name,
        "version": "0.1.0",
        "entry_points": entry_points(root),
        "total_files": total_files,
        "total_py_files": total_py,
        "total_json_files": total_json,
        "language_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "excludes": list(excludes),
    }

    roadmap: Dict[str, Any] = {
        "project": project_sec,
        "file_structure": file_structure,
        "dependency_graph": {"nodes": nodes, "edges": edges},
        "code_metrics": {"complexity": complexity, "unimplemented": unimpl},
        "skipped_files": skipped,
    }
    if not skip_safety:
        roadmap["code_metrics"]["vulnerable_packages"] = safety_vulns()
    return roadmap

###############################################################################
# Built-in cache (filter false positives in â€œunimplementedâ€)
###############################################################################
_builtin_names: set[str] | None = None
def builtins_set() -> set[str]:
    global _builtin_names
    if _builtin_names is None:
        _builtin_names = set(dir(__builtins__))          # type: ignore[arg-type]
    return _builtin_names

###############################################################################
# Architecture-atlas TXT writer
###############################################################################
def write_txt_arch(roadmap: Dict[str, Any], txt_path: Path) -> None:
    """
    Emit a *comprehensive* text file with:
      â€¢ Header + timestamp
      â€¢ ðŸ“‚ / ðŸ“„ / ðŸš€ / ðŸ§ª tree of project structure
      â€¢ Skipped-file list
      â€¢ Key components (top-N classes by method count)
      â€¢ Basic testing overview
    """
    proj   = roadmap["project"]["name"] or Path.cwd().name
    stamp  = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    files  = roadmap["file_structure"]
    skipped= roadmap.get("skipped_files", [])

    # ---------- header --------------------------------------------------
    out = [
        "================================================================================",
        f" {proj.upper()} â€” ARCHITECTURE ATLAS",
        "================================================================================",
        f"Generated: {stamp}",
        "",
        "[PROJECT STRUCTURE]",
        "================================================================================",
        "",
    ]
    out += render_tree(files)

    # ---------- skipped files -------------------------------------------
    out += ["", "[SKIPPED FILES]", "================================================================================", ""]
    out += skipped if skipped else ["No files skipped"]

    # ---------- key components (largest classes) ------------------------
    cls_items: List[tuple[str, Dict[str, Any]]] = []
    for rel, fdat in files.items():
        for cls in fdat.get("classes", []):
            cls_items.append((rel, cls))
    cls_items.sort(key=lambda x: len(x[1].get("methods", [])), reverse=True)
    cls_items = cls_items[:15]

    out += ["", "[KEY COMPONENTS]", "================================================================================", ""]
    if cls_items:
        for rel, cls in cls_items:
            m_cnt = len(cls.get("methods", []))
            purpose = (cls.get("docstring") or "No docstring").splitlines()[0][:100]
            out.append(f"{cls['name']}:")
            out.append(f"  - Location: {rel}")
            out.append(f"  - Purpose: {purpose}")
            out.append(f"  - Methods: {m_cnt}")
            if m_cnt:
                mlist = ", ".join(cls["methods"][:10]) + ("..." if m_cnt > 10 else "")
                out.append(f"  - Key Methods: {mlist}")
            out.append("")
    else:
        out.append("No class large enough to highlight")

    # ---------- test overview -------------------------------------------
    tests = [rel for rel, d in files.items() if d.get("type") == "test"]
    out += ["", "[TESTING]", "================================================================================", ""]
    if tests:
        out += ["Test Files:", ""] + [f"  - {t}" for t in tests]
    else:
        out.append("No test files discovered")

    # ---------- write ----------------------------------------------------
    txt_path.write_text("\n".join(out), encoding="utf-8")
    print(f"âœ“ Architecture TXT written â†’ {txt_path}")

###############################################################################
# CLI
###############################################################################

# --- CLI defaults updated to your requested excludes ---

def parse_cli(argv: Sequence[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate roadmap JSON/py + architecture TXT in results_report/")
    p.add_argument("root", type=Path, nargs="?", default=PROJECT_ROOT, help="Project root (defaults to detected repo root)")
    p.add_argument("-o","--output", type=Path, default=DEFAULT_JSON,
                   help="Primary roadmap file (.json or .py). Defaults to results_report/road_map_YYYYMMDD_HHMM.json")
    p.add_argument("-e","--encodings", default="utf-8,latin-1,cp1252,utf-16",
                   help="Comma-separated fallback encodings")
    p.add_argument("-w","--workers", type=int, default=0, help="Thread workers (0 â†’ auto)")
    p.add_argument("--skip-safety", action="store_true", help="Skip Safety scan")
    # NEW: default excludes include deprecated, back, old, dev_tools
    p.add_argument("--exclude", default="deprecated,back,old,dev_tools",
                   help="Extra comma-separated substrings to exclude "
                        "(default: 'deprecated,back,old,dev_tools'). "
                        "Templates are NOT excluded by default.")
    return p.parse_args(argv)


def _ensure_ext(p: Path) -> Path:
    return p if p.suffix in (".json",".py") else p.with_suffix(".json")

def _is_pycharm_green_button(argv: Sequence[str] | None) -> bool:
    if argv is not None and len(list(argv)) > 0:
        return False
    if os.environ.get("PYCHARM_HOSTED"):
        return True
    try:
        import sys as _sys
        return _sys.gettrace() is not None
    except Exception:
        return False

###############################################################################
# main orchestrator
###############################################################################

def main(argv: Sequence[str] | None = None) -> None:
    if _is_pycharm_green_button(argv):
        argv = [
            str(PROJECT_ROOT),
            # NEW: your requested default excludes (no 'templates')
            "--exclude", "deprecated,back,old,dev_tools",
            "--workers", "0",
        ]
        if shutil.which("safety") is None:
            argv.append("--skip-safety")

    args   = parse_cli(argv)

    # Enforce writing to the existing results_report folder only
    out_js = _ensure_ext(args.output)
    if out_js.parent.resolve() != OUT_DIR.resolve():
        raise SystemExit(
            f"[RoadMap] Output path must be inside:\n  {OUT_DIR}\n"
            f"Got:\n  {out_js}\n"
            "Tip: omit -o to use the default in results_report."
        )
    out_tx = DEFAULT_TXT if out_js.stem.startswith("road_map_") else OUT_DIR / f"{out_js.stem}.txt"

    encs=[e.strip() for e in args.encodings.split(",") if e.strip()]
    excludes = ["deprecated"] + [s.strip() for s in args.exclude.split(",") if s.strip()]

    print(f"[RoadMap] Project root â†’ {args.root}")
    print(f"[RoadMap] Output dir   â†’ {OUT_DIR}")
    if excludes:
        print(f"[RoadMap] Excludes     â†’ {excludes}")

    roadmap=build_map(args.root, encs, args.workers, args.skip_safety, excludes)

    # ----- write JSON / py ----------------------------------------------
    if out_js.suffix==".py":
        out_js.write_text(f"ROAD_MAP = {json.dumps(roadmap,indent=2,sort_keys=False)}\n", encoding="utf-8")
    else:
        out_js.write_text(json.dumps(roadmap, indent=2, sort_keys=False), encoding="utf-8")
    print(f"âœ“ Road-map written     â†’ {out_js}")

    # ----- write architecture digest ------------------------------------
    write_txt_arch(roadmap, out_tx)

if __name__ == "__main__":
    main()

