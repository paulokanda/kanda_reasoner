# project_analysis/project_analizer_2_runner.py

# DIRECT CALL
# python -c "from dt_19_project_analysis.project_analizer_2_runner import main; main()"

"""
project_analizer_2_runner.py

IDE-friendly entry point for KANDA’s ProjectAnalyzer.
Uncomment one of the quick toggles in main() or use the CLI:

  # no-args (PyCharm run):
  #   - generate-dev_tools
  #   - then auto-run groups with auto: true in file_groups.yaml
  #   - and groups listed in env PA_AUTO_GROUPS (comma-separated)

  # CLI mode (examples):
  python project_analizer_2_runner.py generate-dev_tools
  python project_analizer_2_runner.py scaffold dropdown BandpassFilter
  python project_analizer_2_runner.py find filter -n 5
  python project_analizer_2_runner.py annotated-graph
  python project_analizer_2_runner.py metrics -n 10
  python project_analizer_2_runner.py export-model -f yaml -o model.yaml
  python project_analizer_2_runner.py git-meta
  python project_analizer_2_runner.py recent-changes --since "2 weeks ago"
  python project_analizer_2_runner.py web-explorer --port 8000
  python project_analizer_2_runner.py create-download-portal --port 8001

  # NEW:
  python project_analizer_2_runner.py group-report my_new_flow
  python project_analizer_2_runner.py ad-hoc-report k05_combobox_forge/**/*.py k03_tabs/k03_3_content/k03_3_eeg_traces_tab.py
"""

import sys
import os
import argparse
from glob import glob
from pathlib import Path

# ─── Path hack so we can import project_analysis/project_analizer_2.py ─────────
HERE = Path(__file__).resolve().parent          # .../project_analysis
dev_tools = HERE.parent                              # .../dev_tools
PROJECT_ROOT = parent                      # .../EEG_KANDA
sys.path.insert(0, str(PROJECT_ROOT))

# Import the analyzer
from temp.dt_19_project_analysis.project_analizer_2 import ProjectAnalyzer


def _run_auto_groups(pa: ProjectAnalyzer) -> None:
    """
    Auto-run group reports when launching with no CLI args.
    Priority:
      1) PA_AUTO_GROUPS env var: comma-separated list of group names.
      2) Groups in file_groups.yaml with `auto: true`.
    """
    # 1) PA_AUTO_GROUPS=group1,group2 (optional)
    env_groups = [g.strip() for g in os.environ.get("PA_AUTO_GROUPS", "").split(",") if g.strip()]

    # 2) file_groups.yaml entries with auto: true
    groups_yaml = pa.load_file_groups() or {}
    yaml_auto_groups = []
    for name, spec in groups_yaml.items():
        auto = False
        if isinstance(spec, dict):
            auto = bool(spec.get("auto", False))
        # lists don't support "auto", so they won't be auto-run unless in env var
        if auto:
            yaml_auto_groups.append(name)

    # de-dup while preserving order: env first (user override), then yaml
    seen = set()
    to_run = []
    for g in env_groups + yaml_auto_groups:
        if g not in seen:
            seen.add(g)
            to_run.append(g)

    if not to_run:
        print("No auto groups to run (set PA_AUTO_GROUPS or mark groups with `auto: true` in file_groups.yaml).")
        return

    print(f"\n— Auto-running group reports: {', '.join(to_run)} —")
    for name in to_run:
        try:
            pa.generate_group_report(name, png=True)
        except Exception as e:
            print(f"[auto-groups] Failed for '{name}': {e}")


def _expand_repo_relative(pa: ProjectAnalyzer, patterns: list[str]) -> list[str]:
    """
    Expand a list of repo-relative paths/globs to repo-relative .py files.
    Keeps inputs that are already repo-relative file paths.
    """
    root = pa.project_root
    results: list[str] = []
    for pat in patterns:
        # If pattern contains glob chars -> expand
        if any(ch in pat for ch in "*?[]"):
            abs_matches = glob(str(root / pat), recursive=True)
            for m in abs_matches:
                p = Path(m)
                if p.is_file() and p.suffix == ".py":
                    rel = p.relative_to(root).as_posix()
                    results.append(rel)
        else:
            # direct path (assume repo-relative)
            results.append(pat)
    # de-dup & keep order
    deduped = []
    seen = set()
    for r in results:
        if r not in seen:
            seen.add(r)
            deduped.append(r)
    return deduped


def main():
    # default project root
    project_root = str(parent)  # .../EEG_KANDA

    parser = argparse.ArgumentParser(description="KANDA Project Analyzer CLI")

    # Global analysis toggles
    parser.add_argument('--no-complexity', action='store_false', dest='analyze_complexity',
                        help='Skip complexity analysis')
    parser.add_argument('--no-git-history', action='store_false', dest='analyze_git_history',
                        help='Skip git history analysis')
    parser.add_argument('--no-dependency-check', action='store_false', dest='check_dependencies',
                        help='Skip dependency vulnerability check')
    parser.add_argument('--similarity-check', action='store_true', dest='check_similarity',
                        help='Enable code similarity analysis')
    parser.add_argument('--no-architecture-check', action='store_false', dest='check_architecture',
                        help='Skip architecture rules check')
    parser.add_argument('--performance-metrics', action='store_true', dest='performance_metrics',
                        help='Enable performance metrics analysis')

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # generate-dev_tools
    generate_docs_p = subparsers.add_parser("generate-dev_tools", help="Generate all architecture documents.")
    generate_docs_p.add_argument('--no-complexity', action='store_false', dest='analyze_complexity',
                                 help='Skip complexity analysis')
    generate_docs_p.add_argument('--no-git-history', action='store_false', dest='analyze_git_history',
                                 help='Skip git history analysis')
    generate_docs_p.add_argument('--no-dependency-check', action='store_false', dest='check_dependencies',
                                 help='Skip dependency vulnerability check')
    generate_docs_p.add_argument('--similarity-check', action='store_true', dest='check_similarity',
                                 help='Enable code similarity analysis')
    generate_docs_p.add_argument('--no-architecture-check', action='store_false', dest='check_architecture',
                                 help='Skip architecture rules check')
    generate_docs_p.add_argument('--performance-metrics', action='store_true', dest='performance_metrics',
                                 help='Enable performance metrics analysis')

    # other commands
    subparsers.add_parser("annotated-graph", help="Generate Graphviz dependency diagram.")
    subparsers.add_parser("onboarding-readme", help="Generate one-page developer onboarding README.")
    subparsers.add_parser("flow-diagrams", help="Generate clean (Mermaid) flow diagrams.")

    dep_hotspots_p = subparsers.add_parser("dep-hotspots", help="Report on dependency hotspots (most coupled modules).")
    dep_hotspots_p.add_argument("-n", "--num", type=int, default=20, help="Top N results.")

    subparsers.add_parser("debt-report", help="Scan for TODO/FIXME and generate a report.")
    subparsers.add_parser("all-extras", help="Run all optional doc generation steps.")

    # scaffold
    scaffold_p = subparsers.add_parser("scaffold", help="Scaffold a new component.")
    scaffold_p.add_argument("type", choices=["dropdown", "manager", "helper"], help="Component type.")
    scaffold_p.add_argument("name", help="Feature name (e.g., BandpassFilter).")

    # find
    find_p = subparsers.add_parser("find", help="Find files related to a feature.")
    find_p.add_argument("feature", help="Keyword to search for (e.g., 'filter').")
    find_p.add_argument("-n", "--num", type=int, default=5, help="Max results.")

    # metrics
    metrics_p = subparsers.add_parser("metrics", help="Show complexity metrics.")
    metrics_p.add_argument("-n", "--num", type=int, default=10, help="Top N results.")

    # export
    export_p = subparsers.add_parser("export-model", help="Export project model.")
    export_p.add_argument("-f", "--format", choices=["json", "yaml"], default="json")
    export_p.add_argument("-o", "--output", help="Output file path.")

    # git
    subparsers.add_parser("git-meta", help="Show recent Git metadata.")
    recent_p = subparsers.add_parser("recent-changes", help="List recent commits.")
    recent_p.add_argument("--since", default="1 week ago")

    # web
    web_p = subparsers.add_parser("web-explorer", help="Serve interactive web view.")
    web_p.add_argument("--port", type=int, default=8000, help="Server port.")
    web_p.add_argument("--dir", help="Directory for web files (defaults to web_explorer).")

    # download portal
    download_p = subparsers.add_parser("create-download-portal",
                                       help="Creates a local webpage to download the analyzer scripts.")
    download_p.add_argument("--port", type=int, default=8001, help="Server port.")
    download_p.add_argument("--dir", help="Directory for the download portal (defaults to download_portal).")

    # ── NEW: group-report
    grp = subparsers.add_parser("group-report", help="Generate relationship report for a named file group.")
    grp.add_argument("name", help="Group name from project_analysis/file_groups.yaml")
    grp.add_argument("--no-png", action="store_true", help="Skip PNG/HTML rendering")

    # ── NEW: ad-hoc-report
    ad = subparsers.add_parser("ad-hoc-report", help="Report for an explicit list of files (space-separated).")
    ad.add_argument("files", nargs="+", help="Repo-relative .py files or globs")
    ad.add_argument("--no-png", action="store_true")

    # Parse CLI
    args = parser.parse_args()

    # Create analyzer with options
    pa = ProjectAnalyzer(
        project_root=project_root,
        exclude_dirs=["docs_old", "tests_json", "legacy_code", "k05_eeg_filters_deprecated"],
        generate_media_artifacts=False,
        enable_complexity_analysis=getattr(args, 'analyze_complexity', True),
        enable_git_history_analysis=getattr(args, 'analyze_git_history', True),
        enable_dependency_check=getattr(args, 'check_dependencies', True),
        enable_similarity_check=getattr(args, 'check_similarity', True),
        enable_architecture_check=getattr(args, 'check_architecture', True),
        enable_performance_metrics=getattr(args, 'performance_metrics', True)
    )

    # If no CLI args, do a full run and then auto-run groups
    if not args.command:
        print("No command specified. Running default `generate-dev_tools`...")
        pa.generate_architecture_docs(
            onboarding=True,
            clean_flows=False,  # do not emit flow_* files
            dep_hotspots=True,
            tech_debt=True
        )
        # Optional: build a full model before group resolution
        pa.scan_project_structure()
        for f in pa.all_files:
            pa.analyze_file(Path(pa.project_root) / f)
        pa._build_method_index()

        # Auto-run configured groups
        _run_auto_groups(pa)
        return

    # Pre-scan for commands that need the model
    if args.command not in ['scaffold', 'git-meta', 'create-download-portal', 'recent-changes', 'export-model']:
        pa.scan_project_structure()
        print("\n--- Analyzing all source files for command ---")
        for f in pa.all_files:
            pa.analyze_file(Path(pa.project_root) / f)
        pa._build_method_index()

    # Command handlers
    if args.command == "generate-dev_tools":
        pa.generate_architecture_docs(
            onboarding=True,
            clean_flows=True,
            dep_hotspots=True,
            tech_debt=True,
            enable_complexity_analysis=getattr(args, 'analyze_complexity', True),
            enable_git_history_analysis=getattr(args, 'analyze_git_history', True),
            enable_dependency_check=getattr(args, 'check_dependencies', True),
            enable_similarity_check=getattr(args, 'check_similarity', True),
            enable_architecture_check=getattr(args, 'check_architecture', True),
            enable_performance_metrics=getattr(args, 'performance_metrics', True)
        )

    elif args.command == "scaffold":
        pa.scaffold_component(args.type, args.name)

    elif args.command == "find":
        pa.build_feature_index()
        results = pa.find_feature_location(args.feature, max_results=args.num)
        print(f"Found {len(results)} files for '{args.feature}':")
        for r in results:
            print(f"- {r}")

    elif args.command == "annotated-graph":
        pa._generate_dependency_graph()

    elif args.command == "metrics":
        # If your analyzer exposes generate_complexity_report, call it;
        # otherwise use run_complexity_analysis + report_metrics.
        try:
            pa.generate_complexity_report(top_n=args.num)  # optional API
        except AttributeError:
            pa.run_complexity_analysis()
            pa.report_metrics(top_n=args.num)

    elif args.command == "export-model":
        fmt = getattr(args, "format", "json")
        out = getattr(args, "output", None)
        pa.export_model(fmt=fmt, out_path=out)

    elif args.command == "git-meta":
        pa.analyze_git_metadata()
        if getattr(pa, "git_metadata", None):
            for f, meta in sorted(pa.git_metadata.items()):
                print(f"{f}: {meta['author']} @ {meta['date']}")
        else:
            print("No git metadata found (not a git repo or files not tracked).")

    elif args.command == "recent-changes":
        pa.generate_recent_changes(since=args.since)
        for c in getattr(pa, "recent_changes", []):
            print(f"{c['hash']} | {c['author']} | {c['date']} | {c['msg']}")

    elif args.command == "debt-report":
        pa.scan_debt()
        pa.generate_debt_report()

    elif args.command == "onboarding-readme":
        pa.generate_onboarding_readme()

    elif args.command == "flow-diagrams":
        pa._generate_enriched_ascii_flows()

    elif args.command == "dep-hotspots":
        pa.generate_dependency_hotspots_report(top_n=args.num)

    elif args.command == "all-extras":
        pa.generate_all_extras()

    elif args.command == "web-explorer":
        out_dir = Path(args.dir) if args.dir else (Path(project_root) / "dev_tools" / "web_explorer")
        out_dir.mkdir(parents=True, exist_ok=True)
        pa.export_for_web(out_dir)
        pa.serve_web_explorer(out_dir, port=args.port)

    elif args.command == "create-download-portal":
        out_dir = Path(args.dir) if args.dir else (Path(project_root) / "dev_tools" / "download_portal")
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            pa.generate_download_page(out_dir)
        except AttributeError:
            # Optional helper not present in some versions
            (out_dir / "README.txt").write_text("Download portal placeholder.\n", encoding="utf-8")
        pa.serve_web_explorer(out_dir, port=args.port)

    elif args.command == "group-report":
        # Build a rich model (helps resolve imports/method owners)
        pa.generate_group_report(args.name, png=not args.no_png)

    elif args.command == "ad-hoc-report":
        expanded = _expand_repo_relative(pa, args.files)
        if not expanded:
            print("[ad-hoc-report] No files matched.")
            return
        pa.generate_relationship_report(
            expanded,
            title="Ad-hoc Relationship Report",
            out_stem="ad_hoc_subset",
            png=not args.no_png,
        )


if __name__ == "__main__":
    main()

