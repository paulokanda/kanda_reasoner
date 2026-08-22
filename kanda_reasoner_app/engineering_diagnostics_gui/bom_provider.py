# project-path: kanda_reasoner_app/engineering_diagnostics_gui/bom_provider.py
"""Public Safety Suite CLI adapter for completed BOM report payloads."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from threading import Event
from time import sleep
from typing import Mapping, Protocol

from kanda_reasoner_app.tool_process_environment import build_tool_child_environment

from .models import EngineeringDiagnosticsGuiCancelled

__all__ = ["BomReportProvider", "SafetySuiteBomReportProvider"]


class BomReportProvider(Protocol):
    """Provide one completed public BOM report without persistence writes."""

    def collect(
        self,
        project_root: Path,
        cancellation: Event,
    ) -> Mapping[str, object]:
        """Return a completed public report or raise on failure."""


class SafetySuiteBomReportProvider:
    """Collect BOM diagnostics through the public Safety Suite CLI contract."""

    def __init__(self, tool_root: str | Path, *, poll_seconds: float = 0.1) -> None:
        self._tool_root = Path(tool_root).expanduser().resolve(strict=True)
        self._poll_seconds = max(0.02, float(poll_seconds))

    def collect(
        self,
        project_root: Path,
        cancellation: Event,
    ) -> Mapping[str, object]:
        command = [
            sys.executable,
            "-m",
            "kanda_reasoner_app.safety_suite_cli",
            "bom-scan",
            "--root",
            str(project_root),
            "--format",
            "json",
        ]
        environment = build_tool_child_environment()
        process = subprocess.Popen(
            command,
            cwd=str(self._tool_root),
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        while process.poll() is None:
            if cancellation.is_set():
                process.terminate()
                try:
                    process.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=2.0)
                raise EngineeringDiagnosticsGuiCancelled(
                    "ENGINEERING_DIAGNOSTICS_GUI_OPERATION_CANCELLED"
                )
            sleep(self._poll_seconds)
        stdout, stderr = process.communicate()
        if cancellation.is_set():
            raise EngineeringDiagnosticsGuiCancelled(
                "ENGINEERING_DIAGNOSTICS_GUI_OPERATION_CANCELLED"
            )
        if process.returncode != 0:
            raise RuntimeError(
                "BOM_PUBLIC_CLI_FAILED:"
                + str(process.returncode)
                + ":"
                + stderr.strip()
            )
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("BOM_PUBLIC_CLI_JSON_INVALID:" + stdout[:500]) from exc
        if not isinstance(payload, dict):
            raise RuntimeError("BOM_PUBLIC_CLI_JSON_NOT_OBJECT")
        return payload
