# project-path: tests/test_engineering_diagnostics_wave2w_runtime_corrections.py
"""Runtime regression tests for the Wave 2W v1r2 collector correction."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from threading import Event
import tempfile
import textwrap
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    SHADOW_PRODUCER_ID,
    build_shadow_diagnostic_run,
    collect_shadow_findings,
    issue_fingerprint,
)
from kanda_reasoner_app.engineering_diagnostics.collectors.ruff_collector import (
    RuffCollectionError,
    collect_ruff_json,
)
from kanda_reasoner_app.engineering_diagnostics_gui.bom_provider import (
    SafetySuiteBomReportProvider,
)
from kanda_reasoner_app.source_hygiene.shadow_audit import (
    audit_project_for_shadow_conflicts,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_disposable_boundary_fixture,
)


def _tool_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _write_fake_ruff(path: Path, *, mode: str) -> None:
    if mode == "large":
        body = """
import json
import sys
if "--version" in sys.argv:
    print("ruff 0.99.0")
else:
    payload = [
        {
            "code": "E501",
            "filename": "pkg/mod.py",
            "location": {"row": i + 1, "column": 1},
            "end_location": {"row": i + 1, "column": 2},
            "message": "line too long",
            "fix": None,
            "noqa_row": i + 1,
            "url": "https://example.invalid/E501",
        }
        for i in range(30000)
    ]
    sys.stdout.write(json.dumps(payload))
"""
    elif mode == "sleep":
        body = """
import sys
import time
if "--version" in sys.argv:
    print("ruff 0.99.0")
else:
    time.sleep(5)
    print("[]")
"""
    else:
        raise AssertionError(mode)
    path.write_text(textwrap.dedent(body).lstrip(), encoding="utf-8", newline="\n")


def _shadow_runtime_fingerprints(root: Path) -> tuple[str, ...]:
    report = audit_project_for_shadow_conflicts(root)
    collection = collect_shadow_findings(
        root,
        auditor=lambda project_root, max_files=None: report,
        audit_source_path=Path(
            sys.modules[audit_project_for_shadow_conflicts.__module__].__file__
        ).resolve(strict=True),
    )
    with wave2qa_disposable_boundary_fixture() as boundary:
        # Normalize against the disposable boundary using an equivalent public report.
        target = boundary.active_project_root
        payload = report.to_dict()
        payload["project_root"] = str(target)
        second = collect_shadow_findings(
            target,
            auditor=lambda project_root, max_files=None: payload,
            audit_source_path=Path(
                sys.modules[audit_project_for_shadow_conflicts.__module__].__file__
            ).resolve(strict=True),
        )
        run = build_shadow_diagnostic_run(
            second,
            boundary=boundary,
            attempt_id="attempt-runtime-identity",
            source_fingerprint="source-runtime-identity",
            operation_generation=1,
        )
        return tuple(
            issue_fingerprint(SHADOW_PRODUCER_ID, finding)
            for finding in run.findings
            if finding.code == "RUNTIME_LOGIC_IN_FACADE"
        )


class EngineeringDiagnosticsWave2WRuntimeCorrectionTests(unittest.TestCase):
    def test_safety_suite_package_module_executes_bom_json_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "sample.py").write_text("value = 1\n", encoding="utf-8")
            environment = dict(os.environ)
            environment["PYTHONPATH"] = str(_tool_root())
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "kanda_reasoner_app.safety_suite_cli",
                    "bom-scan",
                    "--root",
                    str(root),
                    "--format",
                    "json",
                ],
                cwd=str(_tool_root()),
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=20,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["report_type"], "bom_scan")

    def test_bom_provider_receives_nonempty_public_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "sample.py").write_text("value = 1\n", encoding="utf-8")
            payload = SafetySuiteBomReportProvider(_tool_root()).collect(root, Event())
            self.assertEqual(payload["report_type"], "bom_scan")

    def test_ruff_large_json_stdout_is_drained_without_pipe_deadlock(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "ruff.toml").write_text("line-length = 88\n", encoding="utf-8")
            fake = root / "fake_ruff.py"
            _write_fake_ruff(fake, mode="large")
            result = collect_ruff_json(
                root,
                argv_prefix=(sys.executable, "-S", str(fake)),
                timeout_seconds=5.0,
            )
            self.assertEqual(len(result.raw_findings), 30000)

    def test_ruff_timeout_still_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "ruff.toml").write_text("line-length = 88\n", encoding="utf-8")
            fake = root / "fake_ruff.py"
            _write_fake_ruff(fake, mode="sleep")
            with self.assertRaisesRegex(RuffCollectionError, "RUFF_COLLECTION_TIMEOUT"):
                collect_ruff_json(
                    root,
                    argv_prefix=(sys.executable, "-S", str(fake)),
                    timeout_seconds=0.25,
                )

    def test_shadow_runtime_statements_receive_unique_issue_fingerprints(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            package = root / "pkg"
            package.mkdir()
            (package / "__init__.py").write_text(
                "x = build_one()\ny = build_two()\nz = build_three()\n",
                encoding="utf-8",
            )
            fingerprints = _shadow_runtime_fingerprints(root)
            self.assertEqual(len(fingerprints), 3)
            self.assertEqual(len(set(fingerprints)), 3)

    def test_shadow_runtime_identity_survives_line_insertion(self) -> None:
        snapshots: list[tuple[str, ...]] = []
        for prefix in ("", "\n\n\n"):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                package = root / "pkg"
                package.mkdir()
                (package / "__init__.py").write_text(
                    prefix + "x = build_one()\ny = build_two()\n",
                    encoding="utf-8",
                )
                snapshots.append(_shadow_runtime_fingerprints(root))
        self.assertEqual(snapshots[0], snapshots[1])


if __name__ == "__main__":
    unittest.main()
