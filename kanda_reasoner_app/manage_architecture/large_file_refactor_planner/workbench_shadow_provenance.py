# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_shadow_provenance.py
"""Runtime provenance proof that shadow validation imports only shadow project code."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from .models import SCHEMA_VERSION
from .workbench_shadow_backend import ShadowMaterializationResult

__all__ = [
    "SHADOW_PROVENANCE_FEATURE_ID",
    "ShadowImportOrigin",
    "ShadowProvenanceResult",
    "prove_shadow_runtime_provenance",
]

SHADOW_PROVENANCE_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-shadow-provenance-v1"
)
_TIMEOUT_SECONDS = 45


@dataclass(frozen=True)
class ShadowImportOrigin:
    """Resolved runtime location for one module imported in the shadow process."""

    module_name: str
    module_file: str
    module_origin: str
    inside_shadow_root: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ShadowProvenanceResult:
    """Evidence that the interpreter, path configuration, and imports belong to shadow."""

    schema_version: str
    feature_id: str
    status: str
    backend_name: str
    python_executable: str
    cwd: str
    pythonpath: str
    sys_path: tuple[str, ...]
    site_enabled: bool
    package_installation_mode: str
    import_origins: tuple[ShadowImportOrigin, ...]
    collection_root: str
    blockers: tuple[str, ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["sys_path"] = list(self.sys_path)
        data["import_origins"] = [item.to_dict() for item in self.import_origins]
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        return data


def prove_shadow_runtime_provenance(
    *,
    materialization: ShadowMaterializationResult,
    module_names: list[str] | tuple[str, ...],
    collection_root: str = "",
) -> ShadowProvenanceResult:
    """Import requested modules in a clean subprocess and prove their shadow origin."""
    shadow = Path(materialization.shadow_root).resolve()
    blockers: list[str] = list(materialization.blockers)
    if materialization.status != "shadow_materialized":
        blockers.append("SHADOW_NOT_MATERIALIZED")
    modules = tuple(sorted({str(item).strip() for item in module_names if str(item).strip()}))
    if not modules:
        blockers.append("SHADOW_PROVENANCE_MODULE_SET_EMPTY")
    if blockers:
        return _blocked(materialization, blockers)

    probe = _probe_source(modules)
    env = _shadow_environment(shadow)
    try:
        completed = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=str(shadow),
            env=env,
            text=True,
            capture_output=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return _blocked(materialization, ["SHADOW_PROVENANCE_TIMEOUT"], stderr=str(exc))
    except OSError as exc:
        return _blocked(materialization, [f"SHADOW_PROVENANCE_PROCESS_FAILED:{exc}"])
    if completed.returncode != 0:
        return _blocked(
            materialization,
            ["SHADOW_PROVENANCE_PROBE_FAILED"],
            stderr=completed.stderr,
        )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return _blocked(materialization, [f"SHADOW_PROVENANCE_JSON_INVALID:{exc}"])

    origins: list[ShadowImportOrigin] = []
    for item in payload.get("imports", []):
        module_file = str(item.get("module_file") or "")
        module_origin = str(item.get("module_origin") or "")
        inside = _inside_shadow(module_file or module_origin, shadow)
        origin = ShadowImportOrigin(
            module_name=str(item.get("module_name") or ""),
            module_file=module_file,
            module_origin=module_origin,
            inside_shadow_root=inside,
        )
        origins.append(origin)
        if not inside:
            blockers.append(f"SHADOW_IMPORT_ORIGIN_OUTSIDE_SHADOW:{origin.module_name}")
    if len(origins) != len(modules):
        blockers.append("SHADOW_PROVENANCE_IMPORT_COUNT_MISMATCH")

    sys_path = tuple(str(item) for item in payload.get("sys_path", []))
    cwd = str(payload.get("cwd") or "")
    if Path(cwd).resolve() != shadow:
        blockers.append("SHADOW_PROVENANCE_CWD_MISMATCH")
    if not sys_path or Path(sys_path[0] or cwd).resolve() != shadow:
        blockers.append("SHADOW_ROOT_NOT_FIRST_EFFECTIVE_IMPORT_PATH")

    package_mode = _package_installation_mode(sys_path, shadow)
    warnings: list[str] = []
    if package_mode == "editable_or_external_path_present":
        warnings.append("EXTERNAL_OR_EDITABLE_INSTALL_PATH_PRESENT_BUT_SHADOW_ORIGIN_PROVEN")
    unique = tuple(sorted(set(blockers)))
    return ShadowProvenanceResult(
        schema_version=SCHEMA_VERSION,
        feature_id=SHADOW_PROVENANCE_FEATURE_ID,
        status="shadow_provenance_pass" if not unique else "shadow_provenance_failed",
        backend_name=materialization.backend_name,
        python_executable=str(payload.get("python_executable") or sys.executable),
        cwd=cwd,
        pythonpath=env.get("PYTHONPATH", ""),
        sys_path=sys_path,
        site_enabled=bool(payload.get("site_enabled", True)),
        package_installation_mode=package_mode,
        import_origins=tuple(origins),
        collection_root=str(Path(collection_root).resolve()) if collection_root else str(shadow),
        blockers=unique,
        warnings=tuple(sorted(set(warnings))),
    )


def _probe_source(modules: tuple[str, ...]) -> str:
    encoded = json.dumps(list(modules))
    return f'''import importlib, json, os, site, sys\nmodules = {encoded!r}\nmodules = json.loads(modules)\nimports = []\nfor name in modules:\n    module = importlib.import_module(name)\n    spec = getattr(module, "__spec__", None)\n    imports.append({{\n        "module_name": name,\n        "module_file": str(getattr(module, "__file__", "") or ""),\n        "module_origin": str(getattr(spec, "origin", "") or ""),\n    }})\nprint(json.dumps({{\n    "python_executable": sys.executable,\n    "cwd": os.getcwd(),\n    "sys_path": list(sys.path),\n    "site_enabled": "site" in sys.modules,\n    "imports": imports,\n}}, sort_keys=True))\n'''


def _shadow_environment(shadow: Path) -> dict[str, str]:
    env = dict(os.environ)
    previous = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(shadow) if not previous else str(shadow) + os.pathsep + previous
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _inside_shadow(candidate: str, shadow: Path) -> bool:
    if not candidate or candidate in {"built-in", "frozen"}:
        return False
    try:
        Path(candidate).resolve().relative_to(shadow)
        return True
    except (ValueError, OSError):
        return False


def _package_installation_mode(sys_path: tuple[str, ...], shadow: Path) -> str:
    external_paths = []
    for item in sys_path:
        if not item:
            continue
        try:
            resolved = Path(item).resolve()
        except OSError:
            continue
        if resolved == shadow:
            continue
        if "site-packages" in resolved.parts or "dist-packages" in resolved.parts:
            external_paths.append(str(resolved))
    return "editable_or_external_path_present" if external_paths else "shadow_path_only_for_project_imports"


def _blocked(
    materialization: ShadowMaterializationResult,
    blockers: list[str],
    *,
    stderr: str = "",
) -> ShadowProvenanceResult:
    warnings = () if not stderr else ("PROVENANCE_STDERR:" + stderr[:1000],)
    return ShadowProvenanceResult(
        schema_version=SCHEMA_VERSION,
        feature_id=SHADOW_PROVENANCE_FEATURE_ID,
        status="shadow_provenance_failed",
        backend_name=materialization.backend_name,
        python_executable=sys.executable,
        cwd=materialization.shadow_root,
        pythonpath="",
        sys_path=(),
        site_enabled=True,
        package_installation_mode="unknown",
        import_origins=(),
        collection_root=materialization.shadow_root,
        blockers=tuple(sorted(set(blockers))),
        warnings=warnings,
    )
