# -*- coding: utf-8 -*-
"""
on_ev_phs_tool.py â€” "Every Push" Analyzer

Purpose
-------
A repeatable, on-every-push analysis that rebuilds **text/JSON/MD** reports about
your project (structure, flows, hotspots, tech-debt, complexity, etc.).
It **does not modify your code** â€” think of it as always-on x-ray vision.

Outputs are written to: results_report

What you get (no auto-fix)
--------------------------
- Architecture overview & flows (ASCII/TXT)
- Dependency hotspots (MD)
- Cyclomatic complexity per function/method
- Architecture violations (e.g., circular imports)
- Tech debt scan (TODO/FIXME)
- (Optional) similar code and simple performance hints
All saved under results_report/

Your constraints are respected
------------------------------
- Ignore any path containing the word "deprecated"
- Analyze only .py files (analyzer default)
- No PNG/HTML â€” only text/MD/JSON

Actionable Quality Gates (optional)
-----------------------------------
After generating reports, we evaluate simple gates and exit with non-zero
status if any gates fail (so CI can block the change). Defaults are sensible
and can be tuned via CLI flags or environment variables.

Usage (recommended)
-------------------
Run from the repository root using module form:

python -m dt_18_on_every_push_tool.on_ev_phs_tool run
python -m dt_18_on_every_push_tool.on_ev_phs_tool run --max-cx 15 --max-debt 0
python -m dt_18_on_every_push_tool.on_ev_phs_tool write-baseline
python -m dt_18_on_every_push_tool.on_ev_phs_tool summary

Convenience (local dev / IDE)
-----------------------------
--reports-only         Generate all reports + summary JSON, skip gates, exit 0
--no-exit-on-fail      Generate gates but always exit 0 (useful in PyCharm)
--exclude A,B,C        Extra substrings to exclude (in addition to 'deprecated')

Environment variables (optional)
--------------------------------
MAX_CX, MAX_DEBT, FAIL_ON_ARCH (1/0), FAIL_ON_DEPS (1/0)
"""

from __future__ import annotations

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Any, Dict

# ---------------------------------------------------------------------
# Ensure project root is on sys.path so imports work regardless of CWD
# ---------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
# .../on_every_push_tool -> repo root
PROJECT_ROOT = HERE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------
# Import analyzer with helpful diagnostics on failure
# ---------------------------------------------------------------------
try:
    # NOTE: File name intentionally uses "analizer": keep spelling consistent
    from temp.dt_19_project_analysis.project_analizer_2 import ProjectAnalyzer
except ModuleNotFoundError:
    diag = [
        "Import failed: cannot load 'dt_19_project_analysis.project_analizer_2'.",
        f"  __file__     = {__file__}",
        f"  HERE         = {HERE}",
        f"  PROJECT_ROOT = {PROJECT_ROOT}",
        f"  sys.path[0:5]= {sys.path[0:5]}",
        "",
        "Tips:",
        "  1) Run from repo root with module form:",
        "       python -m dt_18_on_every_push_tool.on_ev_phs_tool run",
        "  2) Ensure package markers exist (optional but recommended):",
        "       __init__.py",
        "       project_analysis/__init__.py",
        "       on_every_push_tool/__init__.py",
        "  3) Verify the file name is exactly 'project_analizer_2.py'.",
    ]
    print("\n".join(diag), file=sys.stderr)
    raise

# ----------------------------- helpers ---------------------------------

def _bool_env(name: str, default: bool) -> bool:
    v = os.environ.get(name, "")
    if v == "":
        return default
    return v.strip() not in ("0", "false", "False", "no", "No")

def _int_env(name: str, default: int) -> int:
    v = os.environ.get(name, "")
    try:
        return int(v) if v else default
    except Exception:
        return default

def _output_dir() -> Path:
    return PROJECT_ROOT / "dev_tools" / "results_report"

def _parse_excludes(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]

def _new_analyzer(
    *,
    enable_similarity: bool,
    enable_performance: bool,
    exclude_extras: list[str] | None = None,
) -> ProjectAnalyzer:
    out_dir = _output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    excludes = ["deprecated"] + (exclude_extras or [])
    # print(f"[Analyzer] Output dir â†’ {out_dir}")
    if exclude_extras:
        print(f"[Analyzer] Extra excludes â†’ {exclude_extras}")
    pa = ProjectAnalyzer(
        project_root=str(PROJECT_ROOT),
        output_dir=str(out_dir),
        exclude_dirs=excludes,               # skip any path containing these substrings
        generate_media_artifacts=False,      # no PNG/HTML
        enable_complexity_analysis=True,
        enable_git_history_analysis=True,
        enable_dependency_check=True,
        enable_similarity_check=enable_similarity,
        enable_architecture_check=True,
        enable_performance_metrics=enable_performance,
    )
    return pa

def _summarize(pa: ProjectAnalyzer) -> Dict[str, Any]:
    """Collect a compact metrics summary for gating & logging."""
    complexity_max = 0
    total_funcs = 0
    for _, entries in (pa.complexity_results or {}).items():
        for _, cx in entries:
            complexity_max = max(complexity_max, cx)
            total_funcs += 1

    arch_viol = len(getattr(pa, "architecture_violations", []) or [])
    dep_warns = len(getattr(pa, "dependency_warnings", []) or [])
    debt = len(getattr(pa, "debt_items", []) or [])
    similar = len(getattr(pa, "similar_code", []) or [])
    perf = len([
        1 for m in getattr(pa, "performance_metrics_results", {}).values()
        if (m.get("nested_loops", 0) > 2) or (m.get("large_structures"))
    ])

    return {
        "complexity_max": complexity_max,
        "functions_analyzed": total_funcs,
        "architecture_violations": arch_viol,
        "dependency_warnings": dep_warns,
        "tech_debt_items": debt,
        "similar_code_pairs": similar,
        "perf_flags": perf,
        "output_dir": str(_output_dir()),
    }

def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def _baseline_path() -> Path:
    return PROJECT_ROOT / "dev_tools" / "project_analysis" / "quality_baseline.json"

def _read_baseline() -> Dict[str, Any]:
    p = _baseline_path()
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

# ----------------------------- commands --------------------------------

def cmd_run(args: argparse.Namespace) -> int:
    pa = _new_analyzer(
        enable_similarity=args.enable_similarity,
        enable_performance=args.enable_performance,
        exclude_extras=_parse_excludes(args.exclude),
    )

    # Generate text/MD reports (no media)
    pa.generate_architecture_docs(
        onboarding=False,
        clean_flows=False,   # keep enriched ASCII flows
        dep_hotspots=True,
        tech_debt=True
    )

    # Summarize & persist machine-readable outputs
    summary = _summarize(pa)
    out_dir = _output_dir()
    _write_json(out_dir / "ci_quality_summary.json", summary)

    # Short-circuit for local "reports only"
    if args.reports_only:
        print("\n[EveryPush] Reports generated (reports-only mode). Skipping gates.")
        return 0

    # ---------------- quality gates ----------------
    max_cx = args.max_cx if args.max_cx is not None else _int_env("MAX_CX", 15)
    max_debt = args.max_debt if args.max_debt is not None else _int_env("MAX_DEBT", 0)
    fail_on_arch = args.fail_on_arch if args.fail_on_arch is not None else _bool_env("FAIL_ON_ARCH", True)
    fail_on_deps = args.fail_on_deps if args.fail_on_deps is not None else _bool_env("FAIL_ON_DEPS", True)

    # Optional baseline logic: compare debt with stored baseline
    baseline = _read_baseline() if args.use_baseline else {}
    baseline_debt = int(baseline.get("tech_debt_items", max_debt))

    failures = []

    # Gate 1: architecture violations
    if fail_on_arch and summary["architecture_violations"] > 0:
        failures.append(f"Architecture violations: {summary['architecture_violations']}")

    # Gate 2: max complexity
    if summary["complexity_max"] > max_cx:
        failures.append(f"Complexity exceeds threshold ({summary['complexity_max']} > {max_cx})")

    # Gate 3: dependency warnings
    if fail_on_deps and summary["dependency_warnings"] > 0:
        failures.append(f"Dependency warnings: {summary['dependency_warnings']}")

    # Gate 4: tech debt (compare against baseline when enabled)
    if args.use_baseline:
        if summary["tech_debt_items"] > baseline_debt:
            failures.append(f"Tech debt grew ({summary['tech_debt_items']} > baseline {baseline_debt})")
    else:
        if summary["tech_debt_items"] > max_debt:
            failures.append(f"Tech debt exceeds threshold ({summary['tech_debt_items']} > {max_debt})")

    # Persist gates result
    gates = {
        "thresholds": {
            "max_cx": max_cx,
            "max_debt": max_debt,
            "fail_on_arch": bool(fail_on_arch),
            "fail_on_deps": bool(fail_on_deps),
            "use_baseline": bool(args.use_baseline),
            "baseline_debt": baseline_debt if args.use_baseline else None,
        },
        "summary": summary,
        "failed": bool(failures),
        "failures": failures,
    }
    _write_json(out_dir / "ci_quality_gates.json", gates)

    # Print human summary
    print("\n=== Analyzer Summary ===")
    for k, v in summary.items():
        print(f"{k:>24}: {v}")
    if failures:
        print("\nâŒ Quality gates failed:")
        for f in failures:
            print(" - " + f)
        if args.no_exit_on_fail:
            print("\nâ„¹ï¸  no-exit-on-fail is set â†’ exiting 0 for local runs.")
            return 0
        return 1
    print("\nâœ… Quality gates passed.")
    return 0

def cmd_summary(args: argparse.Namespace) -> int:
    # Light scan just to read last summary file (if exists), otherwise run minimal analysis
    out_dir = _output_dir()
    f = out_dir / "ci_quality_summary.json"
    if f.exists():
        print(f.read_text(encoding="utf-8"))
        return 0

    # Fallback: quick run (no gating), then print
    pa = _new_analyzer(enable_similarity=False, enable_performance=False)
    pa.generate_architecture_docs(onboarding=False, clean_flows=False, dep_hotspots=True, tech_debt=True)
    summary = _summarize(pa)
    _write_json(out_dir / "ci_quality_summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0

def cmd_write_baseline(args: argparse.Namespace) -> int:
    """Write/update a baseline file from a fresh analysis."""
    pa = _new_analyzer(enable_similarity=False, enable_performance=False)
    pa.generate_architecture_docs(onboarding=False, clean_flows=False, dep_hotspots=True, tech_debt=True)
    summary = _summarize(pa)
    baseline = {
        "tech_debt_items": summary["tech_debt_items"],
        "complexity_max": summary["complexity_max"],
        "architecture_violations": summary["architecture_violations"],
        "dependency_warnings": summary["dependency_warnings"],
    }
    p = _baseline_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    _write_json(p, baseline)
    print(f"ðŸ“Œ Baseline written to {p}:\n" + json.dumps(baseline, indent=2))
    return 0

# ------------------------------ CLI ------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Run text/JSON analyzer on every push and enforce simple quality gates."
    )
    sub = p.add_subparsers(dest="command", required=True)

    # run (main command)
    run = sub.add_parser("run", help="Generate reports and evaluate quality gates.")
    run.add_argument("--max-cx", type=int, default=None, help="Maximum allowed cyclomatic complexity (default: env MAX_CX or 15).")
    run.add_argument("--max-debt", type=int, default=None, help="Maximum allowed TODO/FIXME items (default: env MAX_DEBT or 0).")
    run.add_argument("--fail-on-arch", type=int, choices=[0, 1], default=None, help="Fail on any architecture violation (default: env FAIL_ON_ARCH or 1).")
    run.add_argument("--fail-on-deps", type=int, choices=[0, 1], default=None, help="Fail on any dependency warning (default: env FAIL_ON_DEPS or 1).")
    run.add_argument("--use-baseline", action="store_true", help="Compare tech debt to quality_baseline.json instead of threshold.")
    run.add_argument("--enable-similarity", action="store_true", help="Enable similar-code analysis (slower).")
    run.add_argument("--enable-performance", action="store_true", help="Enable basic performance metrics (slightly slower).")
    # Convenience flags for local dev / IDE
    run.add_argument("--reports-only", action="store_true", help="Generate reports and summary JSON, skip gates and exit 0.")
    run.add_argument("--no-exit-on-fail", action="store_true", help="Generate gates but always exit 0 (useful in IDE).")
    run.add_argument("--exclude", type=str, default="", help="Comma-separated dir substrings to exclude in addition to 'deprecated'.")
    run.set_defaults(func=cmd_run)

    # summary
    summ = sub.add_parser("summary", help="Print latest summary JSON (or run a quick pass if missing).")
    summ.set_defaults(func=cmd_summary)

    # write-baseline
    base = sub.add_parser("write-baseline", help="Write/update quality_baseline.json from current project state.")
    base.set_defaults(func=cmd_write_baseline)

    return p

def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()

    # Default to "run --reports-only" when launched with no args (e.g., PyCharm green button),
    # but keep strict behavior in CI if CI env var is set.
    if not argv:
        if os.environ.get("CI"):
            argv = ["run"]  # CI stays strict
        else:
            argv = ["run", "--reports-only"]  # local/IDE: generate reports, exit 0

    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())

