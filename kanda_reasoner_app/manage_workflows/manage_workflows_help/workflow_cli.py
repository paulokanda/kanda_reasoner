# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_cli.py
"""Own CLI orchestration while leaving manage_workflows.py as facade."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .._workflow_command_isolation import (
    command_list_results,
)
from .workflow_command_runner import (
    run_tests,
)
from .workflow_constants import (
    HISTORY_FILE,
    WORKFLOWS_DOC_NAME,
    WORKFLOW_MANIFEST_NAME,
)
from .workflow_generation import (
    collect_generated_outputs,
    load_manifest_or_default,
    prepare_effective_manifest,
    preservation_violations,
)
from .workflow_history import (
    clear_history,
    get_history_roots,
    print_history,
    record_root,
)
from .workflow_import_checks import (
    run_import_checks,
)
from .workflow_io import (
    diff_text,
    normalize_generated_output_for_diff,
    read_text,
    write_text_if_changed,
)
from .workflow_models import (
    CheckResult,
)
from .workflow_project_scan import (
    scan_project,
)
from .workflow_reporting import (
    print_results,
    summarize_results,
)

__all__ = [
    "main",
    "run_workflow_detector_results",
    "validate_project",
]


def run_workflow_detector_results(
    root: Path,
    manifest: dict[str, Any],
    registry: Any | None = None,
) -> list[CheckResult]:
    """Run additive workflow detectors and convert issues to check results."""
    try:
        from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
            WorkflowDetectorContext,
        )
        from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
            run_workflow_detectors,
        )
        from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models import (  # noqa: E501
            workflow_issue_to_check_result,
        )
    except (ImportError, AttributeError, TypeError, ValueError, OSError) as canonical_exc:
        try:
            import importlib

            staged_package = "_".join(("ask", "ai", "project", "reasoner"))
            helper_base = staged_package + ".manage_workflows.manage_workflows_help"
            WorkflowDetectorContext = importlib.import_module(
                helper_base + ".workflow_detector_context"
            ).WorkflowDetectorContext
            run_workflow_detectors = importlib.import_module(
                helper_base + ".workflow_detector_registry"
            ).run_workflow_detectors
            workflow_issue_to_check_result = importlib.import_module(
                helper_base + ".workflow_issue_models"
            ).workflow_issue_to_check_result
        except (ImportError, AttributeError, TypeError, ValueError, OSError) as exc:
            return [
                CheckResult(
                    "workflow_detectors",
                    "workflow_detector_infrastructure",
                    "fail",
                    "Could not import workflow detector infrastructure: "
                    + type(exc).__name__
                    + ": "
                    + str(exc)
                    + " | canonical attempt: "
                    + type(canonical_exc).__name__
                    + ": "
                    + str(canonical_exc),
                    details={
                        "exception_type": type(exc).__name__,
                        "exception_message": str(exc),
                        "canonical_exception_type": type(canonical_exc).__name__,
                        "canonical_exception_message": str(canonical_exc),
                    },
                )
            ]

    workflows_doc = ""
    doc_path = root / WORKFLOWS_DOC_NAME
    if doc_path.exists():
        try:
            workflows_doc = read_text(doc_path)
        except (OSError, UnicodeError) as exc:
            return [
                CheckResult(
                    "workflow_detectors",
                    "workflow_detector_context",
                    "fail",
                    "Could not read WORKFLOWS.md for detector context: "
                    + type(exc).__name__
                    + ": "
                    + str(exc),
                    details={
                        "path": str(doc_path),
                        "exception_type": type(exc).__name__,
                        "exception_message": str(exc),
                    },
                )
            ]

    context = WorkflowDetectorContext(
        project_root=root,
        workflow_manifest=manifest,
        workflows_doc=workflows_doc,
    )

    issues = run_workflow_detectors(context, registry=registry)

    results: list[CheckResult] = []

    for issue in issues:
        payload = workflow_issue_to_check_result(issue)
        results.append(
            CheckResult(
                category=str(payload.get("category") or "workflow_detectors"),
                name=str(payload.get("name") or "workflow_detector_issue"),
                status=str(payload.get("status") or "warn"),
                message=str(payload.get("message") or "Workflow detector issue."),
                duration_seconds=float(payload.get("duration_seconds") or 0.0),
                command=str(payload.get("command") or ""),
                details=dict(payload.get("details") or {}),
            )
        )
    return results

def validate_project(root: Path) -> tuple[dict[str, Any], list[CheckResult]]:
    """Validate the project.
    
    Parameters
    ----------
    root : Path
        The root path.
    
    Returns
    -------
    tuple[dict[str, Any], list[CheckResult]]
        The tuple of values.
    """
    
    discovered = scan_project(root)
    manifest, loaded = load_manifest_or_default(root, discovered)
    workflows = manifest["workflows"]

    results: list[CheckResult] = []
    if not loaded:
        results.append(
            CheckResult(
                "manifest",
                WORKFLOW_MANIFEST_NAME,
                "warn",
                f"{WORKFLOW_MANIFEST_NAME} not found or unreadable. Using generated defaults.",
            )
        )

    results.extend(run_workflow_detector_results(root, manifest))
    results.extend(run_tests(root, discovered, workflows["tests"]))
    results.extend(command_list_results(category="runtime_smoke", cfg=workflows["runtime_smoke"], root=root))
    results.extend(command_list_results(category="business_checks", cfg=workflows["business_checks"], root=root))
    results.extend(
        command_list_results(
            category="gui_workflows",
            cfg=workflows["gui_workflows"],
            root=root,
            extra_env=dict(workflows["gui_workflows"].get("headless_env") or {}),
        )
    )
    results.extend(command_list_results(category="integration", cfg=workflows["integration"], root=root))
    results.extend(command_list_results(category="performance", cfg=workflows["performance"], root=root))
    results.extend(run_import_checks(root, discovered, workflows["imports"]))

    if discovered["gui_files"] and not (workflows["gui_workflows"].get("commands") or []):
        results.append(
            CheckResult(
                "gui_workflows",
                "gui_workflows",
                "warn",
                "GUI files were discovered but no GUI workflow commands are configured.",
                details={"gui_files": discovered["gui_files"]},
            )
        )

    if discovered["entry_files"] and not (workflows["runtime_smoke"].get("commands") or []):
        results.append(
            CheckResult(
                "runtime_smoke",
                "runtime_smoke",
                "warn",
                "Entrypoint files were discovered but no runtime smoke commands are configured.",
                details={"entry_files": discovered["entry_files"]},
            )
        )

    return manifest, results

def _run(root: Path, mode: str) -> int:
    # scan_project and generate_manifest are always needed; validate_project
    # does its own internal scan so we skip the redundant one for that mode.
    """Support run behavior.
    
    Parameters
    ----------
    root : Path
        The root path.
    mode : str
        The selected mode.
    
    Returns
    -------
    int
        The integer result.
    """
    
    if mode == "validate":
        loaded_manifest, results = validate_project(root)
        print_results(results)
        summary = summarize_results(results)
        print(
            "\nSummary:"
            f" pass={summary.get('pass', 0)}"
            f" fail={summary.get('fail', 0)}"
            f" warn={summary.get('warn', 0)}"
            f" skip={summary.get('skip', 0)}"
        )
        return 1 if summary.get("fail", 0) else 0

    discovered = scan_project(root)
    try:
        manifest, _ = prepare_effective_manifest(
            root,
            discovered,
            fail_on_invalid_existing=True,
        )
    except ValueError as exc:
        print(f"Workflow manifest error: {exc}", file=sys.stderr)
        return 1
    outputs = collect_generated_outputs(root, manifest)

    if mode == "scan":
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0

    if mode == "diff":
        exit_code = 0
        for path, desired in outputs.items():
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            current_norm = normalize_generated_output_for_diff(path, current)
            desired_norm = normalize_generated_output_for_diff(path, desired)
            diff = diff_text(current_norm, desired_norm, f"{path} (current)", f"{path} (generated)")
            if diff:
                print(diff)
                exit_code = 1
        if exit_code == 0:
            print("No diffs.")
        return exit_code

    if mode == "write":
        # Run a validate pass first so we refuse to write on hard failures,
        # matching the safety behaviour of manage_architecture.py.
        _, preflight = validate_project(root)
        if any(r.status == "fail" for r in preflight):
            print_results([r for r in preflight if r.status == "fail"])
            print("\nRefusing to write because validation has failures.")
            return 1

        violations = preservation_violations(root, manifest)
        if violations:
            print("Refusing to write because curated configuration changed:")
            for violation in violations:
                print(f"- {violation}")
            return 1

        changed = 0
        for path, content in outputs.items():
            if write_text_if_changed(path, content):
                print(f"WROTE {path}")
                changed += 1
        print(f"\nDone. Updated {changed} file(s).")
        return 0

    raise ValueError(f"Unsupported mode: {mode}")

def _build_parser() -> argparse.ArgumentParser:
    """Support build parser behavior.
    
    Returns
    -------
    argparse.ArgumentParser
        The argument parser result.
    """
    
    history_roots = get_history_roots()
    default_root = history_roots[0] if history_roots else str(Path.cwd())

    parser = argparse.ArgumentParser(
        description=(
            "Manage runtime/business/gui/integration/test/performance/import "
            "validation workflows."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "History is stored in: " + str(HISTORY_FILE) + "\n\n"
            "Examples:\n"
            "  %(prog)s --validate                        # uses last-used root\n"
            "  %(prog)s --root path/to/project --write   # sets a new root (remembered)\n"
            "  %(prog)s --history                        # show remembered roots\n"
            "  %(prog)s --use-root 2 --validate          # pick root #2 from history\n"
            "  %(prog)s --clear-history                  # wipe all history\n"
        ),
    )

    root_group = parser.add_argument_group("root selection")
    root_group.add_argument(
        "--root",
        default=default_root,
        metavar="PATH",
        help=(
            "Project root path. Defaults to the last used root, "
            f"currently: {default_root}"
        ),
    )
    root_group.add_argument(
        "--use-root",
        type=int,
        metavar="N",
        dest="use_root",
        help="Use the Nth entry from history (1-based) instead of --root.",
    )

    hist_group = parser.add_argument_group("history")
    hist_group.add_argument(
        "--history",
        action="store_true",
        help="Print remembered roots, then exit.",
    )
    hist_group.add_argument(
        "--clear-history",
        action="store_true",
        dest="clear_history",
        help="Clear all history and exit.",
    )

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--scan", action="store_true", help="Print the effective curated workflow manifest.")
    mode_group.add_argument("--validate", action="store_true", help="Execute configured workflows.")
    mode_group.add_argument("--diff", action="store_true", help="Show diffs for generated outputs.")
    mode_group.add_argument("--write", action="store_true", help="Write workflow_manifest.json and WORKFLOWS.md.")
    return parser

def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    parser = _build_parser()
    args = parser.parse_args()

    # -- History-only actions ----------------------------------------------
    if args.clear_history:
        clear_history()
        return 0

    if args.history:
        print_history()
        return 0

    # -- Mode is required for actual work ---------------------------------
    if not any([args.scan, args.validate, args.diff, args.write]):
        parser.error("One of --scan, --validate, --diff, --write is required.")

    # -- Resolve root ------------------------------------------------------
    if args.use_root is not None:
        history_roots = get_history_roots()
        idx = args.use_root - 1
        if idx < 0 or idx >= len(history_roots):
            print(
                f"Error: --use-root {args.use_root} is out of range "
                f"(history has {len(history_roots)} entr{'y' if len(history_roots) == 1 else 'ies'}).",
                file=sys.stderr,
            )
            return 2
        root = Path(history_roots[idx]).resolve()
        print(f"Using root from history [{args.use_root}]: {root}")
    else:
        root = Path(args.root).resolve()

    if not root.exists():
        print(f"Project root does not exist: {root}", file=sys.stderr)
        return 2

    record_root(root)

    mode = (
        "scan" if args.scan
        else "validate" if args.validate
        else "diff" if args.diff
        else "write"
    )
    return _run(root, mode)
