"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations
import os

import logging

import subprocess
from pathlib import Path


def _run_git_command(repo_root: Path, args: list[str]) -> tuple[bool, str]:
    """Run git with a short timeout and without interactive prompts."""
    timeout_raw = os.environ.get("PROJECT_REASONER_GIT_TIMEOUT_SECONDS", "2").strip()
    try:
        timeout_seconds = max(1.0, float(timeout_raw))
    except Exception:
        timeout_seconds = 2.0

    env = os.environ.copy()
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    env.setdefault("GIT_OPTIONAL_LOCKS", "0")

    try:
        completed = subprocess.run(
            ["git"] + args,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=False,
            stdin=subprocess.DEVNULL,
            timeout=timeout_seconds,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return False, ""
    except Exception:
        return False, ""

    if completed.returncode != 0:
        return False, completed.stderr.strip() or completed.stdout.strip()

    return True, completed.stdout


def _normalize_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _iter_git_root_candidates(repo_root: Path, file_path: Path):
    """Yield git-root candidates without escaping the selected project root."""
    seen: set[str] = set()

    try:
        root = repo_root.expanduser().resolve()
    except Exception:
        root = repo_root

    try:
        file_parent = file_path.expanduser().resolve().parent
    except Exception:
        file_parent = file_path.parent

    candidates: list[Path] = [root]
    try:
        if file_parent == root or root in file_parent.parents:
            current = file_parent
            while True:
                candidates.append(current)
                if current == root:
                    break
                current = current.parent
        else:
            candidates.append(file_parent)
    except Exception:
        candidates.append(file_parent)

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except Exception:
            resolved = candidate

        try:
            if resolved != root and root not in resolved.parents:
                continue
        except Exception:
            continue

        key = str(resolved).lower()
        if key in seen:
            continue
        seen.add(key)
        yield resolved


def _discover_git_root(repo_root: Path, file_path: Path) -> Path | None:
    for candidate in _iter_git_root_candidates(repo_root, file_path):
        ok, output = _run_git_command(candidate, ["rev-parse", "--show-toplevel"])
        if not ok:
            continue

        top_level = output.strip().splitlines()[-1].strip()
        if not top_level:
            continue

        try:
            return Path(top_level).resolve()
        except Exception:
            return Path(top_level)

    return None


def collect_git_metadata_for_file(repo_root: Path, file_path: Path) -> dict:
    git_root = _discover_git_root(repo_root, file_path)
    if git_root is None:
        return {
            "available": False,
            "last_commit_date": "",
            "commit_count": 0,
            "authors": [],
            "commit_subjects": [],
        }

    try:
        relative_path = file_path.resolve().relative_to(git_root.resolve())
    except Exception:
        logging.exception("Boundary failure in collect_git_metadata_for_file")
        try:
            relative_path = Path(
                str(file_path.resolve()).replace(str(git_root.resolve()) + "\\", "")
            )
        except Exception:
            return {
                "available": False,
                "last_commit_date": "",
                "commit_count": 0,
                "authors": [],
                "commit_subjects": [],
            }

    rel_text = relative_path.as_posix()

    ok, count_output = _run_git_command(
        git_root,
        ["log", "--follow", "--format=%H", "--", rel_text],
    )
    if not ok:
        return {
            "available": False,
            "last_commit_date": "",
            "commit_count": 0,
            "authors": [],
            "commit_subjects": [],
        }

    hashes = _normalize_lines(count_output)
    if not hashes:
        return {
            "available": False,
            "last_commit_date": "",
            "commit_count": 0,
            "authors": [],
            "commit_subjects": [],
        }

    ok, details_output = _run_git_command(
        git_root,
        ["log", "--follow", "--format=%cI%x1f%an%x1f%s", "--", rel_text],
    )
    if not ok:
        return {
            "available": False,
            "last_commit_date": "",
            "commit_count": len(hashes),
            "authors": [],
            "commit_subjects": [],
        }

    authors: list[str] = []
    commit_subjects: list[str] = []
    last_commit_date = ""

    for index, line in enumerate(_normalize_lines(details_output)):
        parts = line.split("\x1f")
        commit_date = parts[0].strip() if len(parts) > 0 else ""
        author = parts[1].strip() if len(parts) > 1 else ""
        subject = parts[2].strip() if len(parts) > 2 else ""

        if index == 0:
            last_commit_date = commit_date

        if author and author not in authors:
            authors.append(author)

        if subject:
            commit_subjects.append(subject)

    return {
        "available": True,
        "last_commit_date": last_commit_date,
        "commit_count": len(hashes),
        "authors": authors,
        "commit_subjects": commit_subjects,
    }

# PASS_068A_GIT_TIMEOUT_GUARD_START
# Git timeout and project-root candidate bounding are active.
# PASS_068A_GIT_TIMEOUT_GUARD_END
