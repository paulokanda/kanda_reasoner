
#!/usr/bin/env python3
"""Dynamic workflow manager for runtime-oriented project validation.

This tool complements static architecture validation by orchestrating dynamic
checks against a Python project. It is intentionally conservative:

- tests/import checks can run automatically,
- runtime/business/integration/GUI/performance checks are driven by an
  explicit workflow manifest so ownership stays canonical and deterministic,
- generated outputs are limited to a manifest template and a human-readable
  WORKFLOWS.md guide.

Supported modes:
    --scan      Print the generated workflow manifest template as JSON.
    --validate  Execute configured workflows and print a validation report.
    --diff      Show diffs for generated outputs.
    --write     Write generated workflow_manifest.json and WORKFLOWS.md
                when those files are absent or already managed by this tool.
"""

from __future__ import annotations

import argparse
import difflib
import fnmatch
import importlib.util
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

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


@dataclass(slots=True)
class CheckResult:
    category: str
    name: str
    status: str
    message: str
    duration_seconds: float = 0.0
    command: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "duration_seconds": self.duration_seconds,
            "command": self.command,
            "details": self.details,
        }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text_if_changed(path: Path, content: str) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def should_skip_dir(path: Path) -> bool:
    return path.name in DEFAULT_EXCLUDE_DIRS


def iter_python_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        path_obj = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not should_skip_dir(path_obj / d)]
        for filename in filenames:
            if filename.endswith(".py"):
                yield path_obj / filename


def has_main_guard(text: str) -> bool:
    return 'if __name__ == "__main__":' in text or "if __name__ == '__main__':" in text


def has_gui_marker(text: str) -> bool:
    for marker in GUI_IMPORT_MARKERS:
        if f"import {marker}" in text or f"from {marker}" in text:
            return True
    return False


def is_test_path(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    return "tests" in parts or "test" in parts or name.startswith("test_") or name.endswith("_test.py")


def module_id_for_path(root: Path, path: Path) -> str | None:
    rel = path.relative_to(root)
    if path.parent == root:
        return path.stem if path.name != "__init__.py" else None

    parents = list(rel.parts[:-1])
    current = root
    for part in parents:
        current = current / part
        if not (current / "__init__.py").exists():
            return None

    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
        if not parts:
            return None
    else:
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def scan_project(root: Path) -> dict[str, Any]:
    python_files: list[str] = []
    gui_files: list[str] = []
    entry_files: list[str] = []
    test_files: list[str] = []
    test_dirs: set[str] = set()
    package_roots: set[str] = set()
    importable_modules: list[str] = []

    for path in iter_python_files(root):
        rel = str(path.relative_to(root)).replace("\\", "/")
        python_files.append(rel)

        try:
            text = read_text(path)
        except Exception:
            text = ""

        if has_gui_marker(text):
            gui_files.append(rel)

        if path.name in ENTRY_FILENAMES or has_main_guard(text):
            entry_files.append(rel)

        if is_test_path(path):
            test_files.append(rel)
            if path.parent != root:
                test_dirs.add(str(path.parent.relative_to(root)).replace("\\", "/"))

        if path.name == "__init__.py":
            package_dir = path.parent.relative_to(root)
            if package_dir.parts:
                package_roots.add(".".join(package_dir.parts))

        module_id = module_id_for_path(root, path)
        if module_id:
            importable_modules.append(module_id)

    pytest_files = [
        name
        for name in ("pytest.ini", "conftest.py", "tox.ini", "pyproject.toml")
        if (root / name).exists()
    ]

    discovered = {
        "project_root": str(root),
        "generated_at_utc": utc_now_iso(),
        "python_file_count": len(python_files),
        "python_files": sorted(python_files),
        "package_roots": sorted(package_roots),
        "entry_files": sorted(dict.fromkeys(entry_files)),
        "gui_files": sorted(dict.fromkeys(gui_files)),
        "test_files": sorted(test_files),
        "test_dirs": sorted(test_dirs),
        "pytest_files": pytest_files,
        "importable_modules": sorted(dict.fromkeys(importable_modules)),
    }
    return discovered


def generate_manifest(root: Path, discovered: dict[str, Any]) -> dict[str, Any]:
    default_test_dir = discovered["test_dirs"][0] if discovered["test_dirs"] else "tests"

    return {
        "managed_by": MANAGED_BY,
        "version": 1,
        "generated_at_utc": utc_now_iso(),
        "project_root": str(root),
        "discovered": {
            "python_file_count": discovered["python_file_count"],
            "package_roots": discovered["package_roots"],
            "entry_files": discovered["entry_files"],
            "gui_files": discovered["gui_files"],
            "test_dirs": discovered["test_dirs"],
            "pytest_files": discovered["pytest_files"],
        },
        "workflows": {
            "tests": {
                "enabled": True,
                "runner": "auto",
                "pytest_args": ["-q"],
                "unittest_start_dir": default_test_dir,
                "timeout_seconds": 900,
            },
            "runtime_smoke": {
                "enabled": True,
                "commands": [],
                "note": (
                    "Add commands that exercise real entrypoints or runtime "
                    "flows. This category cannot be inferred safely."
                ),
            },
            "business_checks": {
                "enabled": True,
                "commands": [],
                "note": (
                    "Add domain-specific checks here. Business correctness "
                    "cannot be inferred generically."
                ),
            },
            "gui_workflows": {
                "enabled": True,
                "commands": [],
                "headless_env": {
                    "QT_QPA_PLATFORM": "offscreen",
                },
                "note": (
                    "Add GUI smoke-test commands here. The scanner only "
                    "discovers probable GUI files."
                ),
            },
            "integration": {
                "enabled": True,
                "commands": [],
                "note": "Add cross-module or external-system integration checks.",
            },
            "performance": {
                "enabled": True,
                "commands": [],
                "note": (
                    "Add performance commands with max_seconds thresholds. "
                    "Performance budgets are project-specific."
                ),
            },
            "imports": {
                "enabled": True,
                "module_limit": 25,
                "timeout_seconds": 20,
                "include_modules": [],
                "exclude_patterns": [
                    "*.tests*",
                    "*.test*",
                    "*_gui",
                    "*gui*",
                    "*window*",
                    "*dialog*",
                    "*widget*",
                    "*__main__",
                ],
            },
        },
    }


def generate_workflows_md(manifest: dict[str, Any]) -> str:
    discovered = manifest["discovered"]
    lines: list[str] = [
        "# WORKFLOWS",
        "",
        "> Generated by manage_workflows.py.",
        "",
        "This file describes how dynamic validation is configured for the project.",
        "",
        "## What this tool validates",
        "",
        "- Actual runtime behavior via configured smoke commands.",
        "- Business correctness via configured domain commands.",
        "- GUI workflows via configured GUI commands.",
        "- Integration behavior via configured integration commands.",
        "- Test pass/fail via pytest or unittest.",
        "- Performance via configured commands and optional thresholds.",
        "- Import-time side effects via isolated import probes.",
        "",
        "## Discovered project signals",
        "",
        f"- Python files: {discovered['python_file_count']}",
        f"- Package roots: {', '.join(discovered['package_roots']) or '(none)'}",
        f"- Entry files: {', '.join(discovered['entry_files']) or '(none)'}",
        f"- GUI files: {', '.join(discovered['gui_files']) or '(none)'}",
        f"- Test dirs: {', '.join(discovered['test_dirs']) or '(none)'}",
        f"- Pytest files: {', '.join(discovered['pytest_files']) or '(none)'}",
        "",
        "## Manifest ownership",
        "",
        f"- Canonical machine-readable file: `{WORKFLOW_MANIFEST_NAME}`",
        f"- Managed by: `{manifest['managed_by']}`",
        "",
        "## Command specification",
        "",
        "Each workflow command can be either:",
        "",
        "- a string, executed with the platform shell, or",
        "- an object with fields like:",
        "",
        "```json",
        "{",
        '  "name": "GUI smoke",',
        '  "args": ["{python}", "-m", "pytest", "-q", "tests/gui"],',
        '  "cwd": "{root}",',
        '  "env": {"QT_QPA_PLATFORM": "offscreen"},',
        '  "timeout_seconds": 120,',
        '  "expect_exit_code": 0,',
        '  "max_seconds": 10.0',
        "}",
        "```",
        "",
        "Supported placeholders:",
        "",
        "- `{root}` => selected project root",
        "- `{python}` => current Python executable",
        "",
        "## Recommended flow",
        "",
        "1. Run `python manage_workflows.py --root <project> --write` once.",
        "2. Fill in the command lists inside `workflow_manifest.json`.",
        "3. Run `python manage_workflows.py --root <project> --validate`.",
        "",
    ]
    return "\n".join(lines) + "\n"


def diff_text(current: str, desired: str, fromfile: str, tofile: str) -> str:
    return "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            desired.splitlines(keepends=True),
            fromfile=fromfile,
            tofile=tofile,
        )
    )


def normalize_generated_output_for_diff(path: Path, text: str) -> str:
    if path.name != WORKFLOW_MANIFEST_NAME:
        return text
    try:
        data = json.loads(text)
    except Exception:
        return text
    if isinstance(data, dict) and "generated_at_utc" in data:
        data["generated_at_utc"] = "<normalized>"
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def should_generate_json_manifest(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        data = json.loads(read_text(path))
    except Exception:
        return False
    return isinstance(data, dict) and data.get("managed_by") == MANAGED_BY


def should_generate_workflows_doc(path: Path) -> bool:
    if not path.exists():
        return True
    text = read_text(path)
    return text.lstrip().startswith("# WORKFLOWS") and "Generated by manage_workflows.py." in text


def collect_generated_outputs(root: Path, manifest: dict[str, Any]) -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    manifest_path = root / WORKFLOW_MANIFEST_NAME
    doc_path = root / WORKFLOWS_DOC_NAME

    if should_generate_json_manifest(manifest_path):
        outputs[manifest_path] = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    if should_generate_workflows_doc(doc_path):
        outputs[doc_path] = generate_workflows_md(manifest)

    return outputs


def load_manifest_or_default(root: Path, discovered: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    path = root / WORKFLOW_MANIFEST_NAME
    generated = generate_manifest(root, discovered)
    if not path.exists():
        return generated, False

    try:
        loaded = json.loads(read_text(path))
    except Exception as exc:
        loaded = generated
        loaded.setdefault("load_warnings", []).append(
            f"Could not parse {WORKFLOW_MANIFEST_NAME}: {exc}"
        )
        return loaded, False

    if not isinstance(loaded, dict):
        generated.setdefault("load_warnings", []).append(
            f"{WORKFLOW_MANIFEST_NAME} is not a JSON object. Using generated defaults."
        )
        return generated, False

    loaded.setdefault("managed_by", MANAGED_BY)
    loaded["project_root"] = str(root)
    loaded["generated_at_utc"] = utc_now_iso()
    loaded["discovered"] = generated["discovered"]

    default_workflows = generated["workflows"]
    loaded_workflows = loaded.setdefault("workflows", {})
    for key, default_value in default_workflows.items():
        if key not in loaded_workflows or not isinstance(loaded_workflows[key], dict):
            loaded_workflows[key] = default_value
        else:
            merged = dict(default_value)
            merged.update(loaded_workflows[key])
            loaded_workflows[key] = merged

    return loaded, True


def replace_placeholders(value: str, *, root: Path) -> str:
    return value.replace("{root}", str(root)).replace("{python}", sys.executable)


def maybe_stringify_command(args: list[str], shell: bool) -> str:
    if shell:
        return args[0]
    return " ".join(args)


def build_command(
    spec: Any,
    *,
    category: str,
    root: Path,
    default_timeout: int | float,
    extra_env: dict[str, str] | None = None,
) -> tuple[str, list[str], bool, Path, dict[str, str], int | float, int, float | None]:
    if isinstance(spec, str):
        command = replace_placeholders(spec, root=root)
        env = dict(os.environ)
        if extra_env:
            env.update({k: replace_placeholders(v, root=root) for k, v in extra_env.items()})
        return (
            command,
            [command],
            True,
            root,
            env,
            default_timeout,
            0,
            None,
        )

    if not isinstance(spec, dict):
        raise TypeError(f"{category} command spec must be a string or object.")

    name = str(spec.get("name") or f"{category} command")
    cwd_raw = str(spec.get("cwd") or root)
    cwd = Path(replace_placeholders(cwd_raw, root=root)).resolve()

    env = dict(os.environ)
    env_spec = spec.get("env") or {}
    if not isinstance(env_spec, dict):
        raise TypeError(f"{category} env must be a JSON object.")
    if extra_env:
        env.update({k: replace_placeholders(v, root=root) for k, v in extra_env.items()})
    env.update({str(k): replace_placeholders(str(v), root=root) for k, v in env_spec.items()})

    timeout = spec.get("timeout_seconds", default_timeout)
    expect_exit_code = int(spec.get("expect_exit_code", 0))
    max_seconds = spec.get("max_seconds")
    if max_seconds is not None:
        max_seconds = float(max_seconds)

    if "args" in spec:
        args_raw = spec["args"]
        if not isinstance(args_raw, list) or not args_raw:
            raise TypeError(f"{category} args must be a non-empty list.")
        args = [replace_placeholders(str(part), root=root) for part in args_raw]
        return name, args, False, cwd, env, timeout, expect_exit_code, max_seconds

    if "command" in spec:
        command = replace_placeholders(str(spec["command"]), root=root)
        return name, [command], True, cwd, env, timeout, expect_exit_code, max_seconds

    raise KeyError(f"{category} command spec requires 'args' or 'command'.")


def execute_command(
    *,
    category: str,
    spec: Any,
    root: Path,
    default_timeout: int | float,
    extra_env: dict[str, str] | None = None,
) -> CheckResult:
    name, args, shell, cwd, env, timeout, expect_exit_code, max_seconds = build_command(
        spec,
        category=category,
        root=root,
        default_timeout=default_timeout,
        extra_env=extra_env,
    )

    start = time.perf_counter()
    try:
        completed = subprocess.run(
            args[0] if shell else args,
            shell=shell,
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - start
        return CheckResult(
            category=category,
            name=name,
            status="fail",
            message=f"Timed out after {timeout} second(s).",
            duration_seconds=duration,
            command=maybe_stringify_command(args, shell),
            details={"stdout": exc.stdout or "", "stderr": exc.stderr or ""},
        )
    except Exception as exc:
        duration = time.perf_counter() - start
        return CheckResult(
            category=category,
            name=name,
            status="fail",
            message=f"Command failed to start: {exc}",
            duration_seconds=duration,
            command=maybe_stringify_command(args, shell),
        )

    duration = time.perf_counter() - start
    status = "pass"
    message = f"Exit code {completed.returncode}."
    if completed.returncode != expect_exit_code:
        status = "fail"
        message = f"Expected exit code {expect_exit_code}, got {completed.returncode}."
    elif max_seconds is not None and duration > max_seconds:
        status = "fail"
        message = (
            f"Duration {duration:.2f}s exceeded budget {max_seconds:.2f}s."
        )

    return CheckResult(
        category=category,
        name=name,
        status=status,
        message=message,
        duration_seconds=duration,
        command=maybe_stringify_command(args, shell),
        details={
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "returncode": completed.returncode,
            "cwd": str(cwd),
        },
    )


def command_list_results(
    *,
    category: str,
    cfg: dict[str, Any],
    root: Path,
    extra_env: dict[str, str] | None = None,
) -> list[CheckResult]:
    if not cfg.get("enabled", True):
        return [CheckResult(category, category, "skip", "Workflow disabled.")]
    commands = cfg.get("commands") or []
    if not isinstance(commands, list):
        return [CheckResult(category, category, "fail", "commands must be a list.")]
    if not commands:
        note = str(cfg.get("note") or "No commands configured.")
        return [CheckResult(category, category, "warn", note)]

    default_timeout = cfg.get("timeout_seconds", 300)
    results: list[CheckResult] = []
    for index, spec in enumerate(commands, start=1):
        name = f"{category} #{index}"
        if isinstance(spec, dict) and spec.get("name"):
            name = str(spec["name"])
        result = execute_command(
            category=category,
            spec=spec if isinstance(spec, dict) else {"name": name, "command": spec},
            root=root,
            default_timeout=default_timeout,
            extra_env=extra_env,
        )
        results.append(result)
    return results


def pytest_available() -> bool:
    return importlib.util.find_spec("pytest") is not None


def run_tests(root: Path, discovered: dict[str, Any], cfg: dict[str, Any]) -> list[CheckResult]:
    if not cfg.get("enabled", True):
        return [CheckResult("tests", "tests", "skip", "Workflow disabled.")]

    timeout = cfg.get("timeout_seconds", 900)
    runner = str(cfg.get("runner", "auto")).lower()
    pytest_args = cfg.get("pytest_args") or ["-q"]
    if not isinstance(pytest_args, list):
        return [CheckResult("tests", "tests", "fail", "pytest_args must be a list.")]

    should_try_pytest = runner in {"auto", "pytest"}
    has_pytest_signals = bool(discovered["pytest_files"] or discovered["test_dirs"])

    if should_try_pytest and pytest_available() and has_pytest_signals:
        result = execute_command(
            category="tests",
            spec={
                "name": "pytest",
                "args": [sys.executable, "-m", "pytest", *[str(x) for x in pytest_args]],
                "cwd": "{root}",
                "timeout_seconds": timeout,
            },
            root=root,
            default_timeout=timeout,
        )
        if result.status == "pass" or runner == "pytest":
            return [result]

    if runner in {"auto", "unittest"} and discovered["test_dirs"]:
        start_dir = str(cfg.get("unittest_start_dir") or discovered["test_dirs"][0])
        result = execute_command(
            category="tests",
            spec={
                "name": "unittest",
                "args": [
                    sys.executable,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    start_dir,
                ],
                "cwd": "{root}",
                "timeout_seconds": timeout,
            },
            root=root,
            default_timeout=timeout,
        )
        return [result]

    return [
        CheckResult(
            "tests",
            "tests",
            "warn",
            "No runnable test workflow discovered. Configure tests in workflow_manifest.json.",
        )
    ]


def run_import_checks(root: Path, discovered: dict[str, Any], cfg: dict[str, Any]) -> list[CheckResult]:
    if not cfg.get("enabled", True):
        return [CheckResult("imports", "imports", "skip", "Workflow disabled.")]

    include_modules = cfg.get("include_modules") or []
    if include_modules and not isinstance(include_modules, list):
        return [CheckResult("imports", "imports", "fail", "include_modules must be a list.")]

    exclude_patterns = cfg.get("exclude_patterns") or []
    if not isinstance(exclude_patterns, list):
        return [CheckResult("imports", "imports", "fail", "exclude_patterns must be a list.")]

    module_limit = int(cfg.get("module_limit", 25))
    timeout = cfg.get("timeout_seconds", 20)

    modules = [str(m) for m in include_modules] if include_modules else list(discovered["importable_modules"])

    filtered: list[str] = []
    for module in modules:
        if any(fnmatch.fnmatch(module, pattern) for pattern in exclude_patterns):
            continue
        filtered.append(module)

    if not filtered:
        return [CheckResult("imports", "imports", "warn", "No eligible modules for import probing.")]

    results: list[CheckResult] = []
    for module in filtered[:module_limit]:
        start = time.perf_counter()
        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-c", IMPORT_PROBE_CODE, str(root), module],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            results.append(
                CheckResult(
                    "imports",
                    module,
                    "fail",
                    f"Import probe timed out after {timeout} second(s).",
                    duration_seconds=time.perf_counter() - start,
                    command=f"{sys.executable} -I -c <probe> {module}",
                    details={"stdout": exc.stdout or "", "stderr": exc.stderr or ""},
                )
            )
            continue

        duration = time.perf_counter() - start
        if completed.returncode != 0:
            results.append(
                CheckResult(
                    "imports",
                    module,
                    "fail",
                    f"Import probe process exited with code {completed.returncode}.",
                    duration_seconds=duration,
                    command=f"{sys.executable} -I -c <probe> {module}",
                    details={"stdout": completed.stdout, "stderr": completed.stderr},
                )
            )
            continue

        try:
            payload = json.loads(completed.stdout.strip() or "{}")
        except Exception as exc:
            results.append(
                CheckResult(
                    "imports",
                    module,
                    "fail",
                    f"Import probe returned invalid JSON: {exc}",
                    duration_seconds=duration,
                    command=f"{sys.executable} -I -c <probe> {module}",
                    details={"stdout": completed.stdout, "stderr": completed.stderr},
                )
            )
            continue

        status = "pass"
        message_parts: list[str] = []
        if payload.get("status") != "pass":
            status = "fail"
            message_parts.append(payload.get("error") or "Import failed.")
        if payload.get("stdout"):
            status = "fail"
            message_parts.append("stdout emitted during import")
        if payload.get("stderr"):
            status = "fail"
            message_parts.append("stderr emitted during import")
        if payload.get("cwd_changed"):
            status = "fail"
            message_parts.append("cwd changed during import")
        if payload.get("sys_path_changed"):
            status = "fail"
            message_parts.append("sys.path changed during import")
        if not message_parts:
            message_parts.append("Import probe passed with no visible side effects.")

        results.append(
            CheckResult(
                "imports",
                module,
                status,
                "; ".join(message_parts),
                duration_seconds=float(payload.get("duration_seconds", duration)),
                command=f"{sys.executable} -I -c <probe> {module}",
                details=payload,
            )
        )

    if len(filtered) > module_limit:
        results.append(
            CheckResult(
                "imports",
                "imports",
                "warn",
                f"Only the first {module_limit} modules were probed. Increase module_limit to cover more.",
            )
        )

    return results


def print_results(results: list[CheckResult]) -> None:
    if not results:
        print("No workflow results.")
        return

    for result in results:
        duration = f"{result.duration_seconds:.2f}s" if result.duration_seconds else "-"
        print(
            f"{result.status.upper():5} {result.category:15} {result.name:30} "
            f"{duration:>8} :: {result.message}"
        )
        if result.command:
            print(f"      command: {result.command}")
        stdout = str(result.details.get("stdout", "")).strip()
        stderr = str(result.details.get("stderr", "")).strip()
        if stdout:
            print("      stdout:")
            for line in stdout.splitlines():
                print(f"        {line}")
        if stderr:
            print("      stderr:")
            for line in stderr.splitlines():
                print(f"        {line}")


def summarize_results(results: list[CheckResult]) -> dict[str, int]:
    summary = {"pass": 0, "fail": 0, "warn": 0, "skip": 0}
    for result in results:
        summary[result.status] = summary.get(result.status, 0) + 1
    return summary


def validate_project(root: Path) -> tuple[dict[str, Any], list[CheckResult]]:
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


def run(root: Path, mode: str) -> int:
    discovered = scan_project(root)
    manifest = generate_manifest(root, discovered)
    outputs = collect_generated_outputs(root, manifest)

    if mode == "scan":
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0

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
        changed = 0
        for path, content in outputs.items():
            if write_text_if_changed(path, content):
                print(f"WROTE {path}")
                changed += 1
        print(f"\nDone. Updated {changed} file(s).")
        return 0

    raise ValueError(f"Unsupported mode: {mode}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Manage runtime/business/gui/integration/test/performance/import "
            "validation workflows."
        )
    )
    parser.add_argument("--root", default=str(Path.cwd()), help="Project root path.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true", help="Print the generated workflow manifest template.")
    group.add_argument("--validate", action="store_true", help="Execute configured workflows.")
    group.add_argument("--diff", action="store_true", help="Show diffs for generated outputs.")
    group.add_argument("--write", action="store_true", help="Write workflow_manifest.json and WORKFLOWS.md.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    mode = (
        "scan"
        if args.scan
        else "validate"
        if args.validate
        else "diff"
        if args.diff
        else "write"
    )
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Project root does not exist: {root}", file=sys.stderr)
        return 2
    return run(root, mode)


if __name__ == "__main__":
    raise SystemExit(main())
