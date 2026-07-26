# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/behavior_test_presets.py
"""Read-only behavior-test preset discovery for Large File Refactor Workbench."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any, Iterable

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import SCHEMA_VERSION

__all__ = [
    "BEHAVIOR_TEST_PRESETS_FEATURE_ID",
    "BehaviorTestPreset",
    "BehaviorTestPresetReport",
    "build_behavior_test_presets",
    "write_behavior_test_presets",
]

BEHAVIOR_TEST_PRESETS_FEATURE_ID = "architecture-review-large-file-refactor-behavior-test-presets-v1"
_PRESET_REPORT = "BEHAVIOR_TEST_PRESETS.json"
_PRESET_VIEW = "BEHAVIOR_TEST_PRESETS.txt"
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_AI",
    "_show_project_to_AI",
}


@dataclass(frozen=True)
class BehaviorTestPreset:
    """One candidate behavior-validation command discovered without execution."""

    name: str
    command: str
    reason: str
    confidence: str
    discovered_paths: list[str] = field(default_factory=list)
    command_allowlisted: bool = True
    requires_human_review_before_run: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preset."""
        return asdict(self)


@dataclass(frozen=True)
class BehaviorTestPresetReport:
    """Read-only behavior-test preset discovery report."""

    schema_version: str
    feature_id: str
    status: str
    active_project_root: str
    preview_root: str
    report_path: str
    view_path: str
    presets: list[BehaviorTestPreset] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    source_mutation_enabled: bool = False
    test_execution_enabled: bool = False
    behavior_validation_claimed: bool = False
    apply_enabled: bool = False
    import_rewrite_apply_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready report."""
        payload = asdict(self)
        payload["presets"] = [preset.to_dict() for preset in self.presets]
        return payload


def build_behavior_test_presets(
    *,
    active_project_root: str,
    preview_root: str | None = None,
) -> BehaviorTestPresetReport:
    """Discover behavior-test command presets without executing tests."""
    project_root = Path(active_project_root).resolve()
    selected_preview_root = Path(preview_root).resolve() if preview_root else _daily_preview_root(project_root)
    blockers = _root_blockers(project_root, selected_preview_root)
    presets = [] if blockers else _discover_presets(project_root)
    status = _status(blockers, presets)
    return BehaviorTestPresetReport(
        schema_version=SCHEMA_VERSION,
        feature_id=BEHAVIOR_TEST_PRESETS_FEATURE_ID,
        status=status,
        active_project_root=str(project_root),
        preview_root=str(selected_preview_root),
        report_path=str(selected_preview_root / _PRESET_REPORT),
        view_path=str(selected_preview_root / _PRESET_VIEW),
        presets=presets,
        blockers=sorted(set(blockers)),
        warnings=_warnings(status, presets),
        checked_rules=_checked_rules(),
    )


def write_behavior_test_presets(report: BehaviorTestPresetReport) -> BehaviorTestPresetReport:
    """Write preset evidence under the governed project-support Preview root."""
    root = Path(report.preview_root).resolve()
    report_path = Path(report.report_path).resolve()
    view_path = Path(report.view_path).resolve()
    for output_path in (report_path, view_path):
        if not _is_relative_to(output_path, root):
            raise RuntimeError("Behavior preset output outside preview root: " + str(output_path))
    root.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    view_path.write_text(_format_text_view(report), encoding="utf-8")
    return report


def _discover_presets(project_root: Path) -> list[BehaviorTestPreset]:
    """Return deterministic project-specific behavior-test presets."""
    candidates: list[BehaviorTestPreset] = []
    pytest_config = _pytest_config_paths(project_root)
    test_dirs = _existing_dirs(project_root, ["tests", "test", "validation"])
    pytest_dirs = [path for path in test_dirs if _contains_python_tests(path)]
    if pytest_config:
        candidates.append(_preset("pytest_project", "python -m pytest", "pytest configuration file detected", pytest_config, "high"))
    for test_dir in pytest_dirs:
        rel = _rel_text(test_dir, project_root)
        candidates.append(
            _preset(
                "pytest_" + rel.replace("/", "_"),
                "python -m pytest " + rel,
                "Python test files detected in " + rel,
                [test_dir],
                "medium" if rel == "validation" else "high",
            )
        )
    unittest_dirs = [path for path in test_dirs if _contains_unittest_style_tests(path)]
    for test_dir in unittest_dirs:
        rel = _rel_text(test_dir, project_root)
        candidates.append(
            _preset(
                "unittest_" + rel.replace("/", "_"),
                "python -m unittest discover -s " + rel,
                "unittest-style test files detected in " + rel,
                [test_dir],
                "medium",
            )
        )
    return _deduplicate_presets(candidates)


def _preset(name: str, command: str, reason: str, paths: Iterable[Path], confidence: str) -> BehaviorTestPreset:
    """Build one normalized preset."""
    return BehaviorTestPreset(
        name=name,
        command=command,
        reason=reason,
        confidence=confidence,
        discovered_paths=[str(path.resolve()) for path in paths],
    )


def _deduplicate_presets(presets: list[BehaviorTestPreset]) -> list[BehaviorTestPreset]:
    """Deduplicate presets by command while preserving order."""
    seen: set[str] = set()
    result: list[BehaviorTestPreset] = []
    for preset in presets:
        if preset.command in seen:
            continue
        seen.add(preset.command)
        result.append(preset)
    return result


def _pytest_config_paths(project_root: Path) -> list[Path]:
    """Return pytest configuration paths discovered at project root."""
    candidates = ["pytest.ini", "tox.ini", "setup.cfg", "pyproject.toml"]
    paths: list[Path] = []
    for name in candidates:
        path = project_root / name
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")[:20000].lower()
        if name == "pytest.ini" or "pytest" in text or "tool.pytest" in text:
            paths.append(path)
    return paths


def _existing_dirs(project_root: Path, names: list[str]) -> list[Path]:
    """Return existing direct child test directories."""
    return [project_root / name for name in names if (project_root / name).is_dir()]


def _contains_python_tests(path: Path) -> bool:
    """Return True when a directory has likely Python tests."""
    for pattern in ("test_*.py", "*_test.py"):
        if any(item.is_file() for item in path.rglob(pattern)):
            return True
    return False


def _contains_unittest_style_tests(path: Path) -> bool:
    """Return True when a directory has tests suitable for unittest discover."""
    return any(item.is_file() for item in path.rglob("test*.py"))


def _root_blockers(project_root: Path, preview_root: Path) -> list[str]:
    """Return root containment blockers for behavior-test preset output."""
    blockers: list[str] = []
    if not project_root.exists():
        blockers.append("PROJECT_ROOT_NOT_FOUND")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    if _protected_parts(preview_root):
        blockers.append("PREVIEW_ROOT_IN_PROTECTED_ROOT")
    return blockers


def _daily_preview_root(project_root: Path) -> Path:
    """Return dynamic selected-project Preview support root."""
    return preview_runs_root(project_root)


def _protected_parts(path: Path) -> list[str]:
    """Return protected path parts found in a path."""
    return [part for part in path.resolve().parts if part in _PROTECTED_PARTS]


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return True if path is inside root after resolution."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _rel_text(path: Path, root: Path) -> str:
    """Return a stable POSIX relative path string."""
    return path.resolve().relative_to(root.resolve()).as_posix()


def _status(blockers: list[str], presets: list[BehaviorTestPreset]) -> str:
    """Return stable report status."""
    if blockers:
        return "blocked"
    if presets:
        return "behavior_test_presets_ready"
    return "no_behavior_test_presets_discovered"


def _warnings(status: str, presets: list[BehaviorTestPreset]) -> list[str]:
    """Return stable warning labels."""
    warnings = ["DISCOVERY_ONLY_TESTS_NOT_RUN", "BEHAVIOR_VALIDATION_NOT_CLAIMED"]
    if status == "no_behavior_test_presets_discovered":
        warnings.append("NO_PROJECT_TEST_PRESETS_DISCOVERED")
    if any(preset.confidence == "medium" for preset in presets):
        warnings.append("MEDIUM_CONFIDENCE_PRESETS_REQUIRE_REVIEW")
    if status == "blocked":
        warnings.append("BEHAVIOR_TEST_PRESET_DISCOVERY_BLOCKED")
    return warnings


def _checked_rules() -> list[str]:
    """Return stable checked-rule labels."""
    return [
        "project_tests_discovered_without_execution",
        "commands_are_behavior_validation_allowlist_compatible",
        "preset_artifacts_written_under_daily_work_preview_root",
        "preview_root_inside_project_source_blocked",
        "source_mutation_disabled",
        "test_execution_disabled",
        "behavior_validation_not_claimed",
    ]


def _format_text_view(report: BehaviorTestPresetReport) -> str:
    """Return a plain text view for GUI panels and manual review."""
    lines = [
        "Behavior Test Presets",
        "=====================",
        "status: " + report.status,
        "project: " + report.active_project_root,
        "preview_root: " + report.preview_root,
        "source_mutation_enabled: False",
        "test_execution_enabled: False",
        "behavior_validation_claimed: False",
        "",
    ]
    if report.blockers:
        lines.append("Blockers:")
        lines.extend("- " + blocker for blocker in report.blockers)
        lines.append("")
    if not report.presets:
        lines.append("No behavior-test presets discovered.")
    else:
        lines.append("Discovered presets:")
        for preset in report.presets:
            lines.append("- " + preset.name + ": " + preset.command)
            lines.append("  reason: " + preset.reason)
            lines.append("  confidence: " + preset.confidence)
    lines.append("")
    lines.append("Warnings:")
    lines.extend("- " + warning for warning in report.warnings)
    return "\n".join(lines) + "\n"
