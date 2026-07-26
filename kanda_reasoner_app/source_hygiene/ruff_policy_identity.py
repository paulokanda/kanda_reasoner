# project-path: kanda_reasoner_app/source_hygiene/ruff_policy_identity.py
"""Resolve canonical Ruff policy identity without mutating project state."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import re

__all__ = [
    "RUFF_POLICY_FILE_NAME",
    "RuffPolicyIdentity",
    "resolve_ruff_policy_identity",
]

RUFF_POLICY_FILE_NAME = "ruff.toml"
_RUFF_CONFIG_PRECEDENCE = (".ruff.toml", "ruff.toml", "pyproject.toml")
_STRING_SETTING_PATTERN = re.compile(
    r'^\s*(?P<key>[A-Za-z0-9_-]+)\s*=\s*"(?P<value>[^"]*)"\s*(?:#.*)?$'
)
_INTEGER_SETTING_PATTERN = re.compile(
    r"^\s*(?P<key>[A-Za-z0-9_-]+)\s*=\s*(?P<value>[0-9]+)\s*(?:#.*)?$"
)


@dataclass(frozen=True)
class RuffPolicyIdentity:
    """Canonical Ruff configuration identity for one active project."""

    project_root: str
    config_path: str
    config_relative_path: str
    config_sha256: str
    required_version: str
    target_version: str
    line_length: int
    competing_config_paths: tuple[str, ...] = ()

    @property
    def identity_token(self) -> str:
        """Return a stable identity token for reports and validation evidence."""
        return (
            self.config_relative_path
            + ":"
            + self.config_sha256
            + ":required-version="
            + self.required_version
            + ":target-version="
            + self.target_version
            + ":line-length="
            + str(self.line_length)
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible policy identity dictionary."""
        return {
            "project_root": self.project_root,
            "config_path": self.config_path,
            "config_relative_path": self.config_relative_path,
            "config_sha256": self.config_sha256,
            "required_version": self.required_version,
            "target_version": self.target_version,
            "line_length": self.line_length,
            "competing_config_paths": list(self.competing_config_paths),
            "identity_token": self.identity_token,
        }


def resolve_ruff_policy_identity(
    project_root: str | Path,
) -> RuffPolicyIdentity:
    """Resolve one canonical root Ruff policy and its stable identity."""
    root = Path(project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError("RUFF_POLICY_PROJECT_ROOT_NOT_DIRECTORY")

    candidates = _ruff_config_candidates(root)
    selected = _select_config(candidates)
    if selected.name != RUFF_POLICY_FILE_NAME:
        raise ValueError(
            "RUFF_POLICY_CANONICAL_CONFIG_REQUIRED:"
            + selected.relative_to(root).as_posix()
        )

    data = selected.read_bytes()
    text = data.decode("utf-8", errors="strict")
    settings = _top_level_settings(text)
    required_version = _required_string(settings, "required-version")
    target_version = _required_string(settings, "target-version")
    line_length = _required_integer(settings, "line-length")

    competing = tuple(
        path.relative_to(root).as_posix() for path in candidates if path != selected
    )
    if competing:
        raise ValueError("RUFF_POLICY_MULTIPLE_ROOT_CONFIGS:" + "|".join(competing))

    return RuffPolicyIdentity(
        project_root=str(root),
        config_path=str(selected),
        config_relative_path=selected.relative_to(root).as_posix(),
        config_sha256=hashlib.sha256(data).hexdigest(),
        required_version=required_version,
        target_version=target_version,
        line_length=line_length,
        competing_config_paths=competing,
    )


def _ruff_config_candidates(root: Path) -> tuple[Path, ...]:
    """Return root Ruff configuration files that contain Ruff policy."""
    candidates: list[Path] = []
    for name in _RUFF_CONFIG_PRECEDENCE:
        path = root / name
        if not path.is_file():
            continue
        if name == "pyproject.toml" and not _pyproject_has_ruff(path):
            continue
        candidates.append(path)
    if not candidates:
        raise ValueError("RUFF_POLICY_CONFIG_MISSING")
    return tuple(candidates)


def _select_config(candidates: tuple[Path, ...]) -> Path:
    """Select the first config according to Ruff root precedence."""
    order = {name: index for index, name in enumerate(_RUFF_CONFIG_PRECEDENCE)}
    return min(candidates, key=lambda path: order[path.name])


def _pyproject_has_ruff(path: Path) -> bool:
    """Return whether a pyproject file declares a Ruff section."""
    text = path.read_text(encoding="utf-8", errors="strict")
    return any(line.strip() == "[tool.ruff]" for line in text.splitlines())


def _top_level_settings(text: str) -> dict[str, str | int]:
    """Parse the small top-level Ruff settings needed for identity."""
    values: dict[str, str | int] = {}
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("["):
            break
        string_match = _STRING_SETTING_PATTERN.match(raw_line)
        if string_match:
            values[string_match.group("key")] = string_match.group("value")
            continue
        integer_match = _INTEGER_SETTING_PATTERN.match(raw_line)
        if integer_match:
            values[integer_match.group("key")] = int(integer_match.group("value"))
    return values


def _required_string(
    settings: dict[str, str | int],
    key: str,
) -> str:
    """Return one required non-empty string setting."""
    value = settings.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError("RUFF_POLICY_SETTING_MISSING:" + key)
    return value.strip()


def _required_integer(
    settings: dict[str, str | int],
    key: str,
) -> int:
    """Return one required positive integer setting."""
    value = settings.get(key)
    if not isinstance(value, int) or value <= 0:
        raise ValueError("RUFF_POLICY_SETTING_INVALID:" + key)
    return value
