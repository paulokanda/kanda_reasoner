# project-path: tools/validate_workbench_patch5_executor_proof_status_projection_v1.py
"""Validate read-only Stage 7 projection of canonical Patch 5 executor proof."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
import sys
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_patch5_executor_proof as proof_module,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_patch5_executor_proof import (
    PATCH5_EXECUTOR_PROOF_FEATURE_ID,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_patch5_proof_status_gui import (
    read_and_render_patch5_executor_proof_status,
)
from kanda_reasoner_app.project_support_boundary import (
    canonical_project_support_root,
)

FEATURE_ID = "workbench-patch5-executor-proof-status-projection-v1"


class _Output:
    def __init__(self) -> None:
        self.text = ""

    def setPlainText(self, text: str) -> None:
        self.text = text


class _Window:
    def __init__(self) -> None:
        self._large_file_refactor_workbench_refactor_gate_output = _Output()


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(f"{marker}: PASS")


def _path_signature(path: Path) -> tuple[str, ...]:
    """Return a deterministic read-only signature for one path tree."""
    if not path.exists() and not path.is_symlink():
        return ("MISSING",)
    if path.is_symlink():
        return ("SYMLINK", str(path.resolve(strict=False)))
    if path.is_file():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return ("FILE", digest)
    rows: list[str] = ["DIRECTORY"]
    for child in sorted(path.rglob("*"), key=lambda item: item.as_posix()):
        relative = child.relative_to(path).as_posix()
        if child.is_symlink():
            rows.append("L:" + relative + ":" + str(child.resolve(strict=False)))
        elif child.is_dir():
            rows.append("D:" + relative)
        elif child.is_file():
            digest = hashlib.sha256(child.read_bytes()).hexdigest()
            rows.append("F:" + relative + ":" + digest)
    return tuple(rows)


def _write_frozen_patch5_entry(support_root: Path) -> Path:
    """Write one synthetic frozen proof only under isolated test support."""
    entries = (
        support_root
        / "project_freeze_after_update"
        / "frozen_features_memory"
        / "entries"
    )
    entries.mkdir(parents=True, exist_ok=True)
    entry = entries / "freeze-patch5-journaled-apply-proof.md"
    entry.write_text(
        "\n".join(
            [
                'status: "frozen"',
                f"feature_id: {PATCH5_EXECUTOR_PROOF_FEATURE_ID}",
                "journaled apply transaction",
                "rollback recovery",
                "sealed payload proof",
            ]
        ),
        encoding="utf-8",
    )
    return entry


def _source_contract(root: Path) -> None:
    gui = (
        root
        / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
        / "workbench_completion_gui.py"
    )
    text = gui.read_text(encoding="utf-8")
    require(
        "Patch 5 must canonically prove the journaled transaction apply executor"
        not in text,
        "PATCH5_STALE_PLACEHOLDER_GATE_TEXT_REMOVED",
    )
    require(
        text.count("read_and_render_patch5_executor_proof_status(") >= 3,
        "PATCH5_PROOF_STATUS_REFRESHED_AT_BUILD_PREPARE_AND_APPLY",
    )
    require(
        "button.setEnabled(enabled)" in text,
        "PATCH5_PROOF_STATUS_DOES_NOT_FORCE_ENABLE_FINAL_BUTTON",
    )


def main() -> int:
    root = PROJECT_ROOT
    _source_contract(root)
    with tempfile.TemporaryDirectory(prefix="kanda_patch5_status_") as temp:
        fixture_root = Path(temp)
        project_root = fixture_root / (fixture_root.name + "_project")
        isolated_support_root = fixture_root / "isolated_project_support"
        project_root.mkdir()
        window = _Window()
        callback = lambda _window: str(project_root)

        production_support_root = canonical_project_support_root(project_root)
        production_state_before = _path_signature(production_support_root)

        with patch.object(
            proof_module,
            "assert_no_forbidden_nested_support_root",
            return_value=isolated_support_root,
        ):
            unavailable = read_and_render_patch5_executor_proof_status(
                window,
                callback,
            )
            require(
                unavailable is not None and not unavailable.proof_available,
                "PATCH5_MISSING_CANONICAL_PROOF_REMAINS_UNAVAILABLE",
            )
            require(
                "Status: UNAVAILABLE"
                in window._large_file_refactor_workbench_refactor_gate_output.text,
                "PATCH5_UNAVAILABLE_STATUS_VISIBLE",
            )
            unavailable_text = (
                window._large_file_refactor_workbench_refactor_gate_output.text
            )
            require(
                "CANONICAL_FROZEN_FEATURE_ENTRIES_ROOT_MISSING"
                in unavailable_text
                or "PATCH5_EXECUTOR_CANONICAL_FREEZE_ENTRY_NOT_FOUND"
                in unavailable_text,
                "PATCH5_UNAVAILABLE_BLOCKER_VISIBLE",
            )

            entry = _write_frozen_patch5_entry(isolated_support_root)
            available = read_and_render_patch5_executor_proof_status(
                window,
                callback,
            )
            rendered = (
                window._large_file_refactor_workbench_refactor_gate_output.text
            )
            require(
                available is not None and available.proof_available,
                "PATCH5_CANONICAL_FROZEN_PROOF_DISCOVERED",
            )
            require(
                "Status: AVAILABLE" in rendered
                and "Proof available: YES" in rendered,
                "PATCH5_AVAILABLE_STATUS_VISIBLE",
            )
            require(
                str(entry.resolve()) in rendered,
                "PATCH5_MATCHED_FROZEN_ENTRY_VISIBLE",
            )
            require(
                "human review" in rendered
                and "remain independent and fail-closed" in rendered,
                "PATCH5_AVAILABLE_STATUS_PRESERVES_INDEPENDENT_GATES",
            )

        require(
            isolated_support_root.is_dir()
            and isolated_support_root.is_relative_to(fixture_root),
            "PATCH5_VALIDATION_SUPPORT_ISOLATED",
        )
        require(
            _path_signature(production_support_root) == production_state_before,
            "PATCH5_VALIDATION_DRIVE_ROOT_FIXTURE_STATE_UNCHANGED",
        )

    print("WORKBENCH_PATCH5_EXECUTOR_PROOF_STATUS_PROJECTION: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
