# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_generation.py
"""Own workflow manifest preparation and concise WORKFLOWS.md generation."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from .workflow_constants import (
    DISCOVERY_SAMPLE_LIMIT,
    MANAGED_BY,
    WORKFLOWS_DOC_NAME,
    WORKFLOW_MANIFEST_NAME,
)
from .workflow_io import (
    read_text,
    should_generate_json_manifest,
    should_generate_workflows_doc,
    utc_now_iso,
)

__all__ = [
    "collect_generated_outputs",
    "generate_manifest",
    "generate_workflows_md",
    "load_manifest_or_default",
]

_MANAGED_TOP_LEVEL_FIELDS = {
    "project_root",
    "generated_at_utc",
    "discovered",
}


def _manifest_discovery(discovered: dict[str, Any]) -> dict[str, Any]:
    """Return the bounded scanner-owned discovery payload for the manifest."""
    return {
        "python_file_count": discovered["python_file_count"],
        "active_python_file_count": discovered["active_python_file_count"],
        "validation_only_file_count": discovered["validation_only_file_count"],
        "test_python_file_count": discovered["test_python_file_count"],
        "excluded_directory_counts": discovered["excluded_directory_counts"],
        "package_roots": discovered["package_roots"],
        "entry_files": discovered["entry_files"],
        "gui_files": discovered["gui_files"],
        "test_dirs": discovered["test_dirs"],
        "pytest_files": discovered["pytest_files"],
    }


def generate_manifest(root: Path, discovered: dict[str, Any]) -> dict[str, Any]:
    """Generate a conservative manifest for a project without one."""
    default_test_dir = discovered["test_dirs"][0] if discovered["test_dirs"] else "tests"

    return {
        "managed_by": MANAGED_BY,
        "version": 1,
        "generated_at_utc": utc_now_iso(),
        "project_root": str(root),
        "discovered": _manifest_discovery(discovered),
        "workflows": {
            "tests": {
                "enabled": False,
                "runner": "auto",
                "pytest_args": ["-q"],
                "unittest_start_dir": default_test_dir,
                "timeout_seconds": 900,
                "note": "Enable after selecting the canonical active test scope.",
            },
            "runtime_smoke": {
                "enabled": False,
                "commands": [],
                "note": (
                    "Add commands that exercise real entrypoints or runtime "
                    "flows. This category cannot be inferred safely."
                ),
            },
            "business_checks": {
                "enabled": False,
                "commands": [],
                "note": (
                    "Add domain-specific checks here. Business correctness "
                    "cannot be inferred generically."
                ),
            },
            "gui_workflows": {
                "enabled": False,
                "commands": [],
                "headless_env": {"QT_QPA_PLATFORM": "offscreen"},
                "note": (
                    "Add GUI smoke-test commands here. The scanner only "
                    "discovers probable GUI files."
                ),
            },
            "integration": {
                "enabled": False,
                "commands": [],
                "note": "Add cross-module or external-system integration checks.",
            },
            "performance": {
                "enabled": False,
                "commands": [],
                "note": (
                    "Add performance commands with max_seconds thresholds. "
                    "Performance budgets are project-specific."
                ),
            },
            "imports": {
                "enabled": False,
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
                "note": "Enable after reviewing the active import surface.",
            },
        },
    }


def _read_existing_manifest(
    root: Path,
    *,
    fail_on_invalid_existing: bool,
) -> dict[str, Any] | None:
    """Read the existing manifest and distinguish missing from malformed."""
    path = root / WORKFLOW_MANIFEST_NAME
    if not path.exists():
        return None

    try:
        loaded = json.loads(read_text(path))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        if fail_on_invalid_existing:
            raise ValueError(
                f"Could not parse {WORKFLOW_MANIFEST_NAME}: {exc}"
            ) from exc
        return None

    if not isinstance(loaded, dict):
        if fail_on_invalid_existing:
            raise ValueError(
                f"{WORKFLOW_MANIFEST_NAME} must contain a JSON object."
            )
        return None
    return loaded


def prepare_effective_manifest(
    root: Path,
    discovered: dict[str, Any],
    *,
    fail_on_invalid_existing: bool = False,
) -> tuple[dict[str, Any], bool]:
    """Return curated configuration with refreshed scanner-managed fields."""
    generated = generate_manifest(root, discovered)
    existing = _read_existing_manifest(
        root,
        fail_on_invalid_existing=fail_on_invalid_existing,
    )
    if existing is None:
        return generated, False

    effective = copy.deepcopy(existing)
    effective.setdefault("managed_by", MANAGED_BY)
    effective.setdefault("version", generated["version"])
    effective["project_root"] = str(root)
    effective["generated_at_utc"] = utc_now_iso()
    effective["discovered"] = generated["discovered"]

    existing_workflows = effective.get("workflows")
    if existing_workflows is None:
        existing_workflows = {}
        effective["workflows"] = existing_workflows
    elif not isinstance(existing_workflows, dict):
        if fail_on_invalid_existing:
            raise ValueError(
                f"{WORKFLOW_MANIFEST_NAME} field 'workflows' must be a JSON object."
            )
        return generated, False

    for workflow_name, default_config in generated["workflows"].items():
        current = existing_workflows.get(workflow_name)
        if current is None:
            existing_workflows[workflow_name] = copy.deepcopy(default_config)
        elif not isinstance(current, dict):
            if fail_on_invalid_existing:
                raise ValueError(
                    f"Workflow '{workflow_name}' must be a JSON object."
                )
            return generated, False

    return effective, True


def load_manifest_or_default(
    root: Path,
    discovered: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    """Compatibility wrapper for effective manifest preparation."""
    return prepare_effective_manifest(
        root,
        discovered,
        fail_on_invalid_existing=False,
    )


def preservation_violations(
    root: Path,
    proposed: dict[str, Any],
) -> list[str]:
    """Return curated fields that the proposed write would unexpectedly change."""
    existing = _read_existing_manifest(root, fail_on_invalid_existing=True)
    if existing is None:
        return []

    violations: list[str] = []
    for key, value in existing.items():
        if key in _MANAGED_TOP_LEVEL_FIELDS:
            continue
        if key == "workflows":
            continue
        if proposed.get(key) != value:
            violations.append(f"Top-level field changed: {key}")

    existing_workflows = existing.get("workflows", {})
    proposed_workflows = proposed.get("workflows", {})
    if not isinstance(existing_workflows, dict):
        return ["Existing workflows field is not a JSON object."]
    if not isinstance(proposed_workflows, dict):
        return ["Proposed workflows field is not a JSON object."]

    for workflow_name, config in existing_workflows.items():
        if workflow_name not in proposed_workflows:
            violations.append(f"Workflow removed: {workflow_name}")
        elif proposed_workflows[workflow_name] != config:
            violations.append(f"Curated workflow changed: {workflow_name}")
    return violations


def _sample_lines(label: str, values: list[str]) -> list[str]:
    """Return bounded Markdown lines for one discovered path category."""
    if not values:
        return [f"- {label}: 0"]

    lines = [f"- {label}: {len(values)}"]
    for value in values[:DISCOVERY_SAMPLE_LIMIT]:
        lines.append(f"  - `{value}`")
    omitted = len(values) - DISCOVERY_SAMPLE_LIMIT
    if omitted > 0:
        lines.append(f"  - ... and {omitted} more")
    return lines


def generate_workflows_md(manifest: dict[str, Any]) -> str:
    """Generate concise human-readable workflow documentation."""
    discovered = manifest["discovered"]
    excluded = discovered.get("excluded_directory_counts") or {}

    lines: list[str] = [
        "# WORKFLOWS",
        "",
        "> Generated by manage_workflows.py.",
        "",
        "This file describes the effective dynamic validation configuration.",
        "",
        "## Discovery summary",
        "",
        f"- Scanner-visible Python files: {discovered['python_file_count']}",
        f"- Active Python source files: {discovered.get('active_python_file_count', 0)}",
        f"- Validation-only Python files: {discovered.get('validation_only_file_count', 0)}",
        f"- Test Python files: {discovered.get('test_python_file_count', 0)}",
        f"- Excluded directories: {sum(int(value) for value in excluded.values())}",
    ]

    if excluded:
        lines.extend(["", "### Excluded directory categories", ""])
        for category, count in sorted(excluded.items()):
            lines.append(f"- {category.replace('_', ' ').title()}: {count}")

    lines.extend(["", "## Representative active paths", ""])
    lines.extend(_sample_lines("Package roots", discovered.get("package_roots") or []))
    lines.extend(_sample_lines("Entry files", discovered.get("entry_files") or []))
    lines.extend(_sample_lines("GUI files", discovered.get("gui_files") or []))
    lines.extend(_sample_lines("Test directories", discovered.get("test_dirs") or []))

    lines.extend(
        [
            "",
            "## Manifest ownership",
            "",
            f"- Canonical machine-readable file: `{WORKFLOW_MANIFEST_NAME}`",
            f"- Managed by: `{manifest['managed_by']}`",
            "- Existing curated workflow settings are preserved during scan, diff, and write.",
            "",
            "## Command specification",
            "",
            "Each workflow command can be a shell string or an object containing",
            "`name`, `args`, `cwd`, `env`, `timeout_seconds`, `expect_exit_code`,",
            "and optional performance limits.",
            "",
            "Supported placeholders:",
            "",
            "- `{root}` => selected project root",
            "- `{python}` => selected Active Project `.venv` Python interpreter",
            "",
            "## Recommended flow",
            "",
            "1. Review `python manage_workflows.py --root <project> --diff`.",
            "2. Keep project-specific commands curated in `workflow_manifest.json`.",
            "3. Run `python manage_workflows.py --root <project> --validate`.",
            "4. Use `--write` only after the diff and validation are acceptable.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def collect_generated_outputs(
    root: Path,
    manifest: dict[str, Any],
) -> dict[Path, str]:
    """Return managed output paths and their desired serialized content."""
    outputs: dict[Path, str] = {}
    manifest_path = root / WORKFLOW_MANIFEST_NAME
    doc_path = root / WORKFLOWS_DOC_NAME

    if should_generate_json_manifest(manifest_path):
        outputs[manifest_path] = (
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
    if should_generate_workflows_doc(doc_path):
        outputs[doc_path] = generate_workflows_md(manifest)
    return outputs
