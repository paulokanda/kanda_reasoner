#!/usr/bin/env python3
"""Run repeatable benchmark and rollout checks for the docstring inserter."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import shutil
import tempfile
from pathlib import Path

import insert_missing_docstrings as worker


def _capture_run(project_root: Path, mode: str, **kwargs) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        exit_code = worker.run(project_root, mode, **kwargs)
    return exit_code, buffer.getvalue()


def _count_lines(prefix: str, text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith(prefix))


def run_benchmark(
    source_root: Path,
    *,
    ai_config_path: str | None,
    workers: int,
    include_private: bool,
    min_confidence: str,
    no_uncertain: bool,
) -> dict:
    with tempfile.TemporaryDirectory(prefix="docstring_benchmark_") as tmpdir:
        workspace = Path(tmpdir) / "workspace"
        shutil.copytree(source_root, workspace)

        scan_code, scan_output = _capture_run(
            workspace,
            "scan",
            ai_config_path=ai_config_path,
            workers=workers,
            include_private=include_private,
            min_confidence=min_confidence,
            no_uncertain=no_uncertain,
        )

        try:
            scan_summary = json.loads(scan_output)
        except json.JSONDecodeError:
            scan_summary = {"raw_output": scan_output}

        diff_code, diff_output = _capture_run(
            workspace,
            "diff",
            ai_config_path=ai_config_path,
            workers=workers,
            include_private=include_private,
            min_confidence=min_confidence,
            no_uncertain=no_uncertain,
        )

        write_code, write_output = _capture_run(
            workspace,
            "write",
            ai_config_path=ai_config_path,
            workers=workers,
            include_private=include_private,
            min_confidence=min_confidence,
            no_uncertain=no_uncertain,
        )

        remaining_code, remaining_output = _capture_run(
            workspace,
            "scan",
            ai_config_path=ai_config_path,
            workers=workers,
            include_private=include_private,
            min_confidence=min_confidence,
            no_uncertain=no_uncertain,
        )

        try:
            remaining_summary = json.loads(remaining_output)
        except json.JSONDecodeError:
            remaining_summary = {"raw_output": remaining_output}

        report = {
            "source_root": str(source_root),
            "workspace": str(workspace),
            "ai_enabled": ai_config_path is not None,
            "ai_config_path": ai_config_path,
            "workers": workers,
            "include_private": include_private,
            "min_confidence": min_confidence,
            "no_uncertain": no_uncertain,
            "scan": {
                "exit_code": scan_code,
                "summary": scan_summary,
            },
            "diff": {
                "exit_code": diff_code,
                "bytes": len(diff_output.encode("utf-8")),
                "fallbacks": _count_lines("FALLBACK ", diff_output),
                "low_confidence_events": _count_lines("LOW-CONFIDENCE ", diff_output),
                "skipped": _count_lines("SKIPPED ", diff_output),
            },
            "write": {
                "exit_code": write_code,
                "files_written": _count_lines("WROTE ", write_output),
                "fallbacks": _count_lines("FALLBACK ", write_output),
                "low_confidence_events": _count_lines("LOW-CONFIDENCE ", write_output),
                "uncertain_markers": sum(
                    p.read_text(encoding="utf-8").count("# AI-UNCERTAIN")
                    for p in workspace.rglob("*.py")
                ),
            },
            "post_write_scan": {
                "exit_code": remaining_code,
                "summary": remaining_summary,
            },
        }
        return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run benchmark corpus checks.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent / "benchmark_corpus"),
        help="Benchmark corpus root.",
    )
    parser.add_argument(
        "--ai",
        metavar="CONFIG",
        nargs="?",
        const="default",
        help="Enable AI mode. Optionally pass path to ai_config.json.",
    )
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers for AI mode.")
    parser.add_argument(
        "--private",
        action="store_true",
        default=True,
        help="Document private symbols. Default: on.",
    )
    parser.add_argument(
        "--no-private",
        dest="private",
        action="store_false",
        help="Skip private symbols.",
    )
    parser.add_argument(
        "--min-confidence",
        choices=["high", "medium", "low"],
        default="low",
        help="Minimum confidence required for AI acceptance.",
    )
    parser.add_argument(
        "--no-uncertain",
        action="store_true",
        help="Suppress # AI-UNCERTAIN annotations.",
    )
    parser.add_argument(
        "--output",
        default=str(Path.cwd() / "benchmark_report.json"),
        help="Write benchmark report JSON here.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    report = run_benchmark(
        Path(args.root).resolve(),
        ai_config_path=args.ai,
        workers=max(1, args.workers),
        include_private=args.private,
        min_confidence=args.min_confidence,
        no_uncertain=args.no_uncertain,
    )

    output_path = Path(args.output).resolve()
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote benchmark report to {output_path}")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
