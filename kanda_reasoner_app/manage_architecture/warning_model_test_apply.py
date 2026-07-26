# project-path: kanda_reasoner_app/manage_architecture/warning_model_test_apply.py
"""Apply validated Local AI test links and test-only mutations through one guarded writer."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    canonical_transient_garbage_root,
)

from kanda_reasoner_app.manage_architecture.warning_model_test_generation_contract import (
    ACTION_CREATE_FOCUSED_TEST,
    ModelTestMutationProposal,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    ACTION_LINK_EXISTING_TEST,
    TestProtectionGapDecision,
    render_test_protection_link_text,
)

__all__ = [
    "ModelTestProtectionApplyResult",
    "apply_validated_model_test_changes",
]


@dataclass(frozen=True, slots=True)
class ModelTestProtectionApplyResult:
    """Report one atomic-enough guarded apply batch for Local AI test changes."""

    linked_count: int
    mutated_test_count: int
    changed_files: tuple[str, ...]
    backup_root: str

    @property
    def applied_count(self) -> int:
        return self.linked_count + self.mutated_test_count


def _read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _backup_root(project_root: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    daily_work = canonical_transient_garbage_root(project_root)
    return daily_work / "warning_local_ai_resolver" / "validated_test_changes" / timestamp


def _preflight_link(
    root: Path,
    decision: TestProtectionGapDecision,
) -> tuple[Path, str, str]:
    path = root / Path(decision.candidate_test_path)
    if not path.is_file():
        raise RuntimeError("TEST SOURCE MISSING: " + decision.candidate_test_path)
    current = _read_utf8(path)
    if _sha256_text(current) != decision.test_sha256_before:
        raise RuntimeError("TEST SOURCE FRESHNESS CONFLICT: " + decision.candidate_test_path)
    rendered = render_test_protection_link_text(current, decision.module_name)
    return path, current, rendered


def _preflight_mutation(
    root: Path,
    proposal: ModelTestMutationProposal,
) -> tuple[Path, str, str]:
    path = root / Path(proposal.target_test_path)
    if proposal.action == ACTION_CREATE_FOCUSED_TEST:
        if path.exists():
            raise RuntimeError("NEW TEST DESTINATION CONFLICT: " + proposal.target_test_path)
        return path, "", proposal.rendered_test_text
    if not path.is_file():
        raise RuntimeError("TEST SOURCE MISSING: " + proposal.target_test_path)
    current = _read_utf8(path)
    if _sha256_text(current) != proposal.test_sha256_before:
        raise RuntimeError("TEST SOURCE FRESHNESS CONFLICT: " + proposal.target_test_path)
    return path, current, proposal.rendered_test_text


def _collect_rendered_changes(
    root: Path,
    link_decisions: tuple[TestProtectionGapDecision, ...],
    mutations: tuple[ModelTestMutationProposal, ...],
) -> tuple[dict[Path, str], dict[Path, str]]:
    original_by_path: dict[Path, str] = {}
    rendered_by_path: dict[Path, str] = {}
    for decision in link_decisions:
        if decision.action != ACTION_LINK_EXISTING_TEST:
            continue
        path, original, rendered = _preflight_link(root, decision)
        if path in rendered_by_path:
            raise RuntimeError("LOCAL AI APPLY TARGET COLLISION: " + path.relative_to(root).as_posix())
        original_by_path[path] = original
        rendered_by_path[path] = rendered
    for proposal in mutations:
        path, original, rendered = _preflight_mutation(root, proposal)
        if path in rendered_by_path:
            raise RuntimeError("LOCAL AI APPLY TARGET COLLISION: " + path.relative_to(root).as_posix())
        original_by_path[path] = original
        rendered_by_path[path] = rendered
    return original_by_path, rendered_by_path


def _write_backups(
    root: Path,
    backup_root: Path,
    original_by_path: dict[Path, str],
) -> None:
    for path, original in original_by_path.items():
        if not path.exists():
            continue
        relative = path.relative_to(root)
        backup_path = backup_root / relative
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path.write_text(original, encoding="utf-8", newline="")


def _restore_after_failure(
    original_by_path: dict[Path, str],
) -> None:
    for path, original in original_by_path.items():
        try:
            if original:
                temporary = path.with_name(path.name + ".warning_model_rollback_tmp")
                temporary.write_text(original, encoding="utf-8", newline="")
                os.replace(temporary, path)
            elif path.exists():
                path.unlink()
        except OSError:
            pass


def apply_validated_model_test_changes(
    project_root: str | Path,
    link_decisions: tuple[TestProtectionGapDecision, ...],
    mutations: tuple[ModelTestMutationProposal, ...],
) -> ModelTestProtectionApplyResult:
    """Apply only prevalidated links and sandbox-approved test changes with backups."""
    root = Path(project_root).expanduser().resolve()
    selected_links = tuple(
        item for item in link_decisions if item.action == ACTION_LINK_EXISTING_TEST
    )
    if not selected_links and not mutations:
        return ModelTestProtectionApplyResult(0, 0, (), "")
    original_by_path, rendered_by_path = _collect_rendered_changes(
        root,
        selected_links,
        mutations,
    )
    backup_root = _backup_root(root)
    _write_backups(root, backup_root, original_by_path)
    changed: list[str] = []
    link_paths = {
        (root / Path(item.candidate_test_path)).resolve()
        for item in selected_links
    }
    mutation_paths = {
        (root / Path(item.target_test_path)).resolve()
        for item in mutations
    }
    changed_paths: set[Path] = set()
    try:
        for path, rendered in sorted(rendered_by_path.items(), key=lambda item: str(item[0])):
            original = original_by_path[path]
            if rendered == original:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(path.name + ".warning_model_tmp")
            temporary.write_text(rendered, encoding="utf-8", newline="")
            os.replace(temporary, path)
            resolved_path = path.resolve()
            changed_paths.add(resolved_path)
            changed.append(path.relative_to(root).as_posix())
    except Exception:
        _restore_after_failure(original_by_path)
        raise
    return ModelTestProtectionApplyResult(
        linked_count=len(changed_paths & link_paths),
        mutated_test_count=len(changed_paths & mutation_paths),
        changed_files=tuple(changed),
        backup_root=str(backup_root) if changed else "",
    )
