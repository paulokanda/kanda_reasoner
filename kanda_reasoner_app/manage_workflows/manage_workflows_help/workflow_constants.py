# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_constants.py
"""Own workflow validator constants and import probe code."""

from __future__ import annotations

from pathlib import Path

__all__ = []

HISTORY_FILE = Path.home() / ".manage_workflows_history.json"

HISTORY_MAX_ROOTS = 10

HARD_EXCLUDE_DIRS = {
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
    "consoles",
    "console",
    "external libraries",
    "external_libraries",
}

DEPRECATED_DIR_NAMES = {
    "archive",
    "archives",
    "deprecated",
    "legacy",
    "old",
    "older",
}

BACKUP_DIR_NAMES = {
    "backup",
    "backups",
    "_patch_backups",
}

TEMPORARY_DIR_NAMES = {
    "_bundle_temp",
    "scratch",
    "scratches",
    "temp",
    "tmp",
}

GENERATED_DIR_NAMES = {
    "first_prompt_files",
    "second_prompt_files",
}

SEMANTIC_EXCLUDE_DIR_PREFIXES = (
    "backup_",
)

SEMANTIC_EXCLUDE_DIR_SUFFIXES = (
    "_deprecated",
    "_delete_after_daily_work",
    "_show_project_to_ai",
)

VALIDATION_ONLY_TOP_LEVEL_DIRS = {
    "scripts",
    "tools",
}

VALIDATION_ONLY_FILE_PATTERNS = (
    "validate_*.py",
    "*_validate_manifests.py",
)

DISCOVERY_SAMPLE_LIMIT = 8

DEFAULT_EXCLUDE_DIRS = (
    HARD_EXCLUDE_DIRS
    | DEPRECATED_DIR_NAMES
    | BACKUP_DIR_NAMES
    | TEMPORARY_DIR_NAMES
    | GENERATED_DIR_NAMES
    | {"prompt", "prompts"}
)


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
