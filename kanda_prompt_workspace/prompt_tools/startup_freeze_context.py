#!/usr/bin/env python3
"""Generate the active-project freeze context for the KANDA startup pack.

This module belongs to the startup delivery tool box:

    kanda_prompt_workspace/prompt_tools/

It creates a generated exposure copy for AI startup sessions from the active
project's canonical freeze memory:

    <active_project_root>/project_freeze_after_update/frozen_features_memory/

It does not write or repair freeze memory.  It only produces a compact Markdown
payload and a source fingerprint for sync/staleness checks.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

ACTIVE_FREEZE_CONTEXT_FILENAME = "09_active_project_freeze_context.md"
FREEZE_MEMORY_RELATIVE = Path("project_freeze_after_update") / "frozen_features_memory"
FREEZE_ENTRIES_RELATIVE = FREEZE_MEMORY_RELATIVE / "entries"
FREEZE_INDEX_RELATIVE = FREEZE_MEMORY_RELATIVE / "freeze_index.json"
FREEZE_STEPS_RELATIVE = FREEZE_MEMORY_RELATIVE / "project_frozen_implemented_steps.md"
EXPOSE_FREEZE_MEMORY_RELATIVE = Path("project_freeze_ledger") / "freeze_tools" / "expose_freeze_memory.py"


def resolve_active_project_root(workspace_root: Path, explicit_project_root: Path | None = None) -> Path:
    """Resolve the active project root used for freeze context exposure."""
    if explicit_project_root is not None:
        return explicit_project_root.expanduser().resolve(strict=False)
    # kanda_prompt_workspace lives directly under the active KANDA project root.
    return workspace_root.resolve(strict=False).parent


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_bytes_if_file(path: Path) -> bytes:
    try:
        if path.is_file():
            return path.read_bytes()
    except OSError as exc:
        return f"READ_ERROR:{path}:{exc}".encode("utf-8", errors="replace")
    return b""


def _iter_freeze_source_files(project_root: Path) -> list[Path]:
    """Return source files that affect the generated startup freeze context."""
    files: list[Path] = []
    freeze_index = project_root / FREEZE_INDEX_RELATIVE
    steps = project_root / FREEZE_STEPS_RELATIVE
    if freeze_index.is_file():
        files.append(freeze_index)
    entries_root = project_root / FREEZE_ENTRIES_RELATIVE
    if entries_root.is_dir():
        files.extend(sorted(path for path in entries_root.glob("freeze-*.md") if path.is_file()))
    if steps.is_file():
        files.append(steps)
    return files


def freeze_context_source_fingerprint(project_root: Path) -> str:
    """Hash active freeze-memory source state without using generated timestamps."""
    root = project_root.resolve(strict=False)
    digest = hashlib.sha256()
    digest.update(f"project_root={root}\n".encode("utf-8", errors="replace"))
    memory_root = root / FREEZE_MEMORY_RELATIVE
    digest.update(f"memory_exists={memory_root.exists()}\n".encode("utf-8"))
    for source in _iter_freeze_source_files(root):
        try:
            rel = source.relative_to(root).as_posix()
        except ValueError:
            rel = str(source)
        payload = _read_bytes_if_file(source)
        digest.update(rel.encode("utf-8", errors="replace"))
        digest.update(b"\0")
        digest.update(_sha256_bytes(payload).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _load_expose_freeze_memory_module(engine_root: Path) -> ModuleType:
    module_path = engine_root / EXPOSE_FREEZE_MEMORY_RELATIVE
    if not module_path.is_file():
        raise FileNotFoundError(f"Missing freeze exposure tool: {module_path}")
    spec = importlib.util.spec_from_file_location("kanda_expose_freeze_memory_for_startup", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module spec for {module_path}")
    module = importlib.util.module_from_spec(spec)
    # dataclasses expect their module to exist in sys.modules during execution.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _render_fallback_context(project_root: Path, generated_at: str, error: str) -> str:
    return f"""# ACTIVE PROJECT FREEZE CONTEXT

Generated: `{generated_at}`
Project root: `{project_root}`
Freeze memory source: `{FREEZE_MEMORY_RELATIVE.as_posix()}`
Freeze context status: `UNAVAILABLE`

## Purpose

This generated startup file is the AI access channel for project-specific frozen
feature memory.  It is an exposure copy only.  The source of truth remains under
the selected active project root.

## Exposure error

```text
{error}
```

## AI operating rule

If implementation touches frozen/governed behavior, request a fresh freeze
context or the relevant full freeze entry before patching.

## Post-validation freeze awareness rule

After you help install and validate a feature, do not silently assume it is
frozen.  Tell the user that the validated feature may need a freeze-memory
update and offer:

1. Freeze locally through the Freeze Feature After Update tab.
2. Ask AI to help prepare the freeze entry.
"""


def build_active_project_freeze_context(
    *,
    workspace_root: Path,
    active_project_root: Path,
    generated_at: str,
    max_items: int = 40,
) -> tuple[str, bytes, dict[str, Any]]:
    """Return generated filename, Markdown bytes, and manifest record."""
    project_root = active_project_root.resolve(strict=False)
    engine_root = workspace_root.resolve(strict=False).parent
    source_fingerprint = freeze_context_source_fingerprint(project_root)

    try:
        exposure = _load_expose_freeze_memory_module(engine_root)
        result = exposure.audit_freeze_memory(str(project_root), engine_root=str(engine_root))
        report = exposure.render_text_report(result, max_items=max_items)
        status = str(getattr(result, "status", "UNKNOWN"))
        index_entry_count = int(getattr(result, "index_entry_count", 0) or 0)
        entry_file_count = int(getattr(result, "entry_file_count", 0) or 0)
        active_entry_count = int(getattr(result, "active_entry_count", 0) or 0)
        body = f"""# ACTIVE PROJECT FREEZE CONTEXT

Generated: `{generated_at}`
Project root: `{project_root}`
Freeze memory source: `{FREEZE_MEMORY_RELATIVE.as_posix()}`
Freeze context status: `{status}`
Index entries: `{index_entry_count}`
Entry files: `{entry_file_count}`
Active/non-superseded entries: `{active_entry_count}`
Source fingerprint: `{source_fingerprint}`

## Purpose

This generated startup file is the AI access channel for project-specific frozen
feature memory at the beginning of a programming interaction.

This file is a generated exposure copy only.  The source of truth remains:

```text
<active_project_root>/{FREEZE_MEMORY_RELATIVE.as_posix()}/
```

## Compact freeze report

```text
{report.rstrip()}
```

## Post-validation freeze awareness rule

When you help implement, install, or validate a project change, check this
freeze context before concluding the work.

If the change is installed and validation evidence is clean, and the change
creates or updates governed behavior, protected paths, startup delivery,
prompt-library behavior, freeze workflow, or architecture-sensitive logic, tell
the user:

```text
This validated feature should now be considered for freeze-memory update.
```

Offer the user these choices:

1. Freeze it locally through the Freeze Feature After Update tab.
2. Ask AI to help prepare the freeze entry.

Do not silently assume the feature is frozen.
Do not update freeze memory without explicit human approval.
Do not treat project_freeze_ledger as active project memory.
"""
    except Exception as exc:  # startup generation should expose the failure, not crash blindly.
        status = "UNAVAILABLE"
        index_entry_count = 0
        entry_file_count = 0
        active_entry_count = 0
        body = _render_fallback_context(project_root, generated_at, str(exc))

    payload = body.encode("utf-8")
    record = {
        "load_order": 9,
        "prompt_id": "active_project_freeze_context",
        "load_mode": "always_startup_dynamic_context",
        "role": "Generated active-project freeze memory context and post-validation freeze-awareness rule for AI programming compliance.",
        "canonical_source": f"dynamic:{FREEZE_MEMORY_RELATIVE.as_posix()}",
        "resolved_source": str((project_root / FREEZE_MEMORY_RELATIVE).resolve(strict=False)),
        "generated_filename": ACTIVE_FREEZE_CONTEXT_FILENAME,
        "source_fingerprint": source_fingerprint,
        "generated_sha256": _sha256_bytes(payload),
        "size_bytes_generated": len(payload),
        "active_project_root": str(project_root),
        "freeze_context_status": status,
        "index_entry_count": index_entry_count,
        "entry_file_count": entry_file_count,
        "active_entry_count": active_entry_count,
        "in_sync_at_generation": True,
    }
    return ACTIVE_FREEZE_CONTEXT_FILENAME, payload, record
