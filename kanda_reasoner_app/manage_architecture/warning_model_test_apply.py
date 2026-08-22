# project-path: kanda_reasoner_app/manage_architecture/warning_model_test_apply.py
"""Apply validated Local AI test links and test-only mutations through one guarded writer."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from kanda_reasoner_app.project_source_proposal_boundary import (
    PROJECT_REPAIR_PROPOSAL_ONLY_MARKER,
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
    proposal_only: bool = False
    proposed_files: tuple[str, ...] = ()

    @property
    def applied_count(self) -> int:
        return self.linked_count + self.mutated_test_count


def _read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()



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


def apply_validated_model_test_changes(
    project_root: str | Path,
    link_decisions: tuple[TestProtectionGapDecision, ...],
    mutations: tuple[ModelTestMutationProposal, ...],
) -> ModelTestProtectionApplyResult:
    """Return proposal evidence for validated test changes without source writes."""
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
    proposed = tuple(
        path.relative_to(root).as_posix()
        for path, rendered in sorted(
            rendered_by_path.items(),
            key=lambda item: str(item[0]),
        )
        if rendered != original_by_path[path]
    )
    return ModelTestProtectionApplyResult(
        linked_count=0,
        mutated_test_count=0,
        changed_files=(),
        backup_root="",
        proposal_only=True,
        proposed_files=proposed,
    )
