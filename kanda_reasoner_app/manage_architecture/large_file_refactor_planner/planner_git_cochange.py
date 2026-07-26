# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_git_cochange.py
"""Optional read-only Git history evidence for heuristic cluster affinity."""
from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .dependency_clusterer import DependencyCluster
from .models import ModuleAnalysisReport, RefactorSymbol

__all__ = [
    "GitCochangeEvidence",
    "HistoricalAffinity",
    "collect_git_cochange_evidence",
]

_HASH_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")


@dataclass(frozen=True)
class HistoricalAffinity:
    """Bounded historical coupling evidence for two candidate clusters."""

    score: float
    shared_commit_count: int
    left_commit_count: int
    right_commit_count: int
    available: bool
    confidence_weight: float = 0.0
    effective_score: float = 0.0


@dataclass(frozen=True)
class GitCochangeEvidence:
    """Read-only Git history evidence without exposing repository-local hashes."""

    status: str
    source_relative_path: str = ""
    queried_cluster_count: int = 0
    history_commit_count: int = 0
    pair_affinities: list[dict[str, object]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    confidence_label: str = "none"
    confidence_weight: float = 0.0
    confidence_reason: str = "No usable history evidence."
    _symbol_commit_sets: dict[str, frozenset[str]] = field(
        default_factory=dict,
        repr=False,
        compare=False,
    )

    @property
    def available(self) -> bool:
        """Return whether usable history evidence was collected."""
        return self.status in {"ready", "partial"} and bool(self._symbol_commit_sets)

    def affinity_for_symbols(
        self,
        left_symbols: list[str] | tuple[str, ...],
        right_symbols: list[str] | tuple[str, ...],
    ) -> HistoricalAffinity:
        """Return Jaccard co-change affinity for two symbol groups."""
        if not self.available:
            return HistoricalAffinity(0.0, 0, 0, 0, False, 0.0, 0.0)
        left_commits = _union_commit_sets(self._symbol_commit_sets, left_symbols)
        right_commits = _union_commit_sets(self._symbol_commit_sets, right_symbols)
        if not left_commits or not right_commits:
            return HistoricalAffinity(
                0.0,
                0,
                len(left_commits),
                len(right_commits),
                False,
                self.confidence_weight,
                0.0,
            )
        shared = left_commits & right_commits
        union = left_commits | right_commits
        score = len(shared) / len(union) if union else 0.0
        effective = score * self.confidence_weight
        return HistoricalAffinity(
            round(score, 6),
            len(shared),
            len(left_commits),
            len(right_commits),
            True,
            self.confidence_weight,
            round(effective, 6),
        )

    def to_dict(self) -> dict[str, object]:
        """Return export-safe history evidence without commit hashes or absolute paths."""
        return {
            "status": self.status,
            "source_relative_path": self.source_relative_path,
            "queried_cluster_count": self.queried_cluster_count,
            "history_commit_count": self.history_commit_count,
            "confidence_label": self.confidence_label,
            "confidence_weight": self.confidence_weight,
            "confidence_reason": self.confidence_reason,
            "pair_affinities": list(self.pair_affinities),
            "warnings": list(self.warnings),
            "policy": {
                "optional_supporting_signal": True,
                "can_override_ast_must_link": False,
                "can_override_size_gate": False,
                "can_override_cycle_gate": False,
                "can_override_public_facade_ownership": False,
            },
        }


def collect_git_cochange_evidence(
    source_path: str | Path | None,
    report: ModuleAnalysisReport,
    base_clusters: list[DependencyCluster],
    *,
    max_cluster_queries: int = 24,
    max_commits_per_cluster: int = 80,
    command_timeout_seconds: float = 3.0,
) -> GitCochangeEvidence:
    """Collect optional cluster history using bounded, read-only ``git log -L`` queries."""
    if source_path is None or not str(source_path).strip():
        return GitCochangeEvidence(
            status="unavailable_no_source_path",
            warnings=["GIT_HISTORY_SOURCE_PATH_UNAVAILABLE"],
        )
    git_executable = shutil.which("git")
    if not git_executable:
        return GitCochangeEvidence(
            status="unavailable_git_not_found",
            warnings=["GIT_EXECUTABLE_NOT_FOUND"],
        )
    source = Path(source_path).expanduser().resolve(strict=False)
    if not source.exists() or not source.is_file():
        return GitCochangeEvidence(
            status="unavailable_source_missing",
            warnings=["GIT_HISTORY_SOURCE_FILE_MISSING"],
        )
    repository_root = _repository_root(
        git_executable,
        source.parent,
        command_timeout_seconds,
    )
    if repository_root is None:
        return GitCochangeEvidence(
            status="unavailable_not_git_repo",
            warnings=["GIT_REPOSITORY_NOT_FOUND"],
        )
    try:
        relative_path = source.relative_to(repository_root).as_posix()
    except ValueError:
        return GitCochangeEvidence(
            status="unavailable_outside_repo",
            warnings=["SOURCE_OUTSIDE_GIT_REPOSITORY"],
        )
    if not _is_tracked(
        git_executable,
        repository_root,
        relative_path,
        command_timeout_seconds,
    ):
        return GitCochangeEvidence(
            status="unavailable_untracked",
            source_relative_path=relative_path,
            warnings=["GIT_HISTORY_TARGET_UNTRACKED"],
        )

    symbol_by_name = {symbol.name: symbol for symbol in report.symbols}
    ordered_clusters = sorted(
        base_clusters,
        key=lambda item: _cluster_start_line(item, symbol_by_name),
    )
    warnings: list[str] = []
    if len(ordered_clusters) > max_cluster_queries:
        warnings.append("GIT_HISTORY_QUERY_BUDGET_PARTIAL")
        ordered_clusters = ordered_clusters[:max_cluster_queries]

    cluster_commit_sets: dict[str, frozenset[str]] = {}
    symbol_commit_sets: dict[str, frozenset[str]] = {}
    query_failures = 0
    for cluster in ordered_clusters:
        line_span = _cluster_line_span(cluster, symbol_by_name)
        if line_span is None:
            query_failures += 1
            continue
        commits = _line_history_commits(
            git_executable,
            repository_root,
            relative_path,
            line_span,
            max_commits_per_cluster,
            command_timeout_seconds,
        )
        if commits is None:
            query_failures += 1
            continue
        frozen = frozenset(commits)
        cluster_commit_sets[cluster.cluster_id] = frozen
        for symbol_name in cluster.symbols:
            symbol_commit_sets[symbol_name] = frozen

    if query_failures:
        warnings.append("GIT_HISTORY_QUERY_FAILURE_PARTIAL")
    all_commits = set().union(*cluster_commit_sets.values()) if cluster_commit_sets else set()
    if not cluster_commit_sets or not all_commits:
        return GitCochangeEvidence(
            status="unavailable_no_history",
            source_relative_path=relative_path,
            queried_cluster_count=len(cluster_commit_sets),
            warnings=sorted(set(warnings + ["GIT_HISTORY_NO_USABLE_COMMITS"])),
        )

    confidence_label, confidence_weight, confidence_reason = _history_confidence(len(all_commits))
    pair_affinities = _pair_affinity_records(
        ordered_clusters,
        cluster_commit_sets,
        confidence_weight=confidence_weight,
    )
    status = "partial" if warnings else "ready"
    return GitCochangeEvidence(
        status=status,
        source_relative_path=relative_path,
        queried_cluster_count=len(cluster_commit_sets),
        history_commit_count=len(all_commits),
        pair_affinities=pair_affinities,
        warnings=sorted(set(warnings)),
        confidence_label=confidence_label,
        confidence_weight=confidence_weight,
        confidence_reason=confidence_reason,
        _symbol_commit_sets=symbol_commit_sets,
    )


def _history_confidence(commit_count: int) -> tuple[str, float, str]:
    """Return bounded evidence confidence from observed history depth."""
    if commit_count <= 0:
        return "none", 0.0, "No usable history commits were observed."
    if commit_count <= 2:
        return "very_low", 0.15, "Only one or two history commits were observed; co-change is heavily discounted."
    if commit_count <= 5:
        return "low", 0.35, "Three to five history commits were observed; co-change remains weak supporting evidence."
    if commit_count <= 15:
        return "moderate", 0.65, "Six to fifteen history commits were observed; co-change is moderately weighted."
    return "high", 1.0, "More than fifteen history commits were observed; full supporting weight is allowed."


def _repository_root(
    git_executable: str,
    cwd: Path,
    timeout_seconds: float,
) -> Path | None:
    result = _run_git(
        git_executable,
        cwd,
        ["rev-parse", "--show-toplevel"],
        timeout_seconds,
    )
    if result is None or result.returncode != 0:
        return None
    text = result.stdout.strip()
    if not text:
        return None
    return Path(text).resolve(strict=False)


def _is_tracked(
    git_executable: str,
    repository_root: Path,
    relative_path: str,
    timeout_seconds: float,
) -> bool:
    result = _run_git(
        git_executable,
        repository_root,
        ["ls-files", "--error-unmatch", "--", relative_path],
        timeout_seconds,
    )
    return result is not None and result.returncode == 0


def _line_history_commits(
    git_executable: str,
    repository_root: Path,
    relative_path: str,
    line_span: tuple[int, int],
    max_commits: int,
    timeout_seconds: float,
) -> set[str] | None:
    start_line, end_line = line_span
    result = _run_git(
        git_executable,
        repository_root,
        [
            "log",
            "--format=%H",
            "--no-patch",
            f"--max-count={max(1, int(max_commits))}",
            "-L",
            f"{start_line},{end_line}:{relative_path}",
        ],
        timeout_seconds,
    )
    if result is None or result.returncode != 0:
        return None
    return {
        line.strip().lower()
        for line in result.stdout.splitlines()
        if _HASH_RE.fullmatch(line.strip())
    }


def _run_git(
    git_executable: str,
    cwd: Path,
    arguments: list[str],
    timeout_seconds: float,
) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            [git_executable, "-C", str(cwd), *arguments],
            capture_output=True,
            text=True,
            check=False,
            timeout=max(0.5, float(timeout_seconds)),
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def _cluster_line_span(
    cluster: DependencyCluster,
    symbol_by_name: dict[str, RefactorSymbol],
) -> tuple[int, int] | None:
    symbols = [symbol_by_name[name] for name in cluster.symbols if name in symbol_by_name]
    if not symbols:
        return None
    return (
        min(symbol.start_line for symbol in symbols),
        max(symbol.end_line for symbol in symbols),
    )


def _cluster_start_line(
    cluster: DependencyCluster,
    symbol_by_name: dict[str, RefactorSymbol],
) -> int:
    symbols = [symbol_by_name[name] for name in cluster.symbols if name in symbol_by_name]
    return min((symbol.start_line for symbol in symbols), default=0)


def _pair_affinity_records(
    clusters: list[DependencyCluster],
    commit_sets: dict[str, frozenset[str]],
    *,
    confidence_weight: float,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for left_index, left in enumerate(clusters):
        left_commits = set(commit_sets.get(left.cluster_id, frozenset()))
        if not left_commits:
            continue
        for right in clusters[left_index + 1 :]:
            right_commits = set(commit_sets.get(right.cluster_id, frozenset()))
            if not right_commits:
                continue
            shared = left_commits & right_commits
            union = left_commits | right_commits
            score = len(shared) / len(union) if union else 0.0
            records.append(
                {
                    "left_cluster_id": left.cluster_id,
                    "right_cluster_id": right.cluster_id,
                    "score": round(score, 6),
                    "effective_score": round(score * confidence_weight, 6),
                    "confidence_weight": confidence_weight,
                    "shared_commit_count": len(shared),
                    "left_commit_count": len(left_commits),
                    "right_commit_count": len(right_commits),
                }
            )
    return sorted(
        records,
        key=lambda item: (
            float(item["score"]),
            int(item["shared_commit_count"]),
            str(item["left_cluster_id"]),
            str(item["right_cluster_id"]),
        ),
        reverse=True,
    )


def _union_commit_sets(
    symbol_commit_sets: dict[str, frozenset[str]],
    symbols: list[str] | tuple[str, ...],
) -> set[str]:
    result: set[str] = set()
    for symbol_name in symbols:
        result.update(symbol_commit_sets.get(symbol_name, frozenset()))
    return result
