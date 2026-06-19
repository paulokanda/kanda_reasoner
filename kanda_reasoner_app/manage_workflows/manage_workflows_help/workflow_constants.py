"""Own workflow validator constants and import probe code."""

from __future__ import annotations

import argparse
import contextlib
import difflib
import fnmatch
import importlib.util
import io
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

__all__ = [
]

HISTORY_FILE = Path.home() / ".manage_workflows_history.json"

HISTORY_MAX_ROOTS = 10

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".coverage",
    "htmlcov",
    "build",
    "dist",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "dev_tools_docs",
    ".project_reference",
    "_project_reference",
    "project_freeze_ledger",
    "chat",
    "chats",
    "archive",
    "archives",
    "backup",
    "backups",
    "old",
    "older",
    "deprecated",
    "prompts",
    "prompt",
    "scratches",
    "scratch",
    "consoles",
    "console",
    "external libraries",
    "external_libraries",
}

GUI_IMPORT_MARKERS = (
    "PySide6",
    "PyQt6",
    "PyQt5",
    "tkinter",
    "wx",
    "kivy",
    "dearpygui",
)

ENTRY_FILENAMES = {
    "main.py",
    "app.py",
    "cli.py",
    "run.py",
    "server.py",
    "manage.py",
    "start.py",
}

WORKFLOW_MANIFEST_NAME = "workflow_manifest.json"

WORKFLOWS_DOC_NAME = "WORKFLOWS.md"

MANAGED_BY = "manage_workflows.py"

IMPORT_PROBE_CODE = r"""
import contextlib
import importlib
import io
import json
import os
import pathlib
import sys
import tempfile
import time

root = pathlib.Path(sys.argv[1]).resolve()
module_name = sys.argv[2]

temp_dir = pathlib.Path(tempfile.mkdtemp(prefix="workflow_import_probe_"))
os.chdir(temp_dir)
sys.path.insert(0, str(root))

stdout_buffer = io.StringIO()
stderr_buffer = io.StringIO()

before_cwd = os.getcwd()
before_path = list(sys.path)

payload = {
    "module": module_name,
    "status": "pass",
    "duration_seconds": 0.0,
    "stdout": "",
    "stderr": "",
    "cwd_changed": False,
    "sys_path_changed": False,
    "error": "",
}

start = time.perf_counter()
try:
    with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(
        stderr_buffer
    ):
        importlib.import_module(module_name)
except Exception as exc:
    payload["status"] = "fail"
    payload["error"] = f"{type(exc).__name__}: {exc}"
finally:
    payload["duration_seconds"] = round(time.perf_counter() - start, 4)
    payload["stdout"] = stdout_buffer.getvalue()
    payload["stderr"] = stderr_buffer.getvalue()
    payload["cwd_changed"] = os.getcwd() != before_cwd
    payload["sys_path_changed"] = sys.path != before_path

print(json.dumps(payload))
"""
