"""Text templates for the external Freeze Feature After Update support box."""

from __future__ import annotations


__all__ = [
    'entries_readme',
    'initial_freeze_index',
    'initial_frozen_steps',
    'root_readme',
    'send_readme',
    'what_to_say',
]
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


SCHEMA_VERSION = "1.0"


def utc_now_iso() -> str:
    """Return a stable UTC timestamp for generated metadata."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def initial_freeze_index() -> str:
    """Return a valid empty freeze index JSON string."""
    return json.dumps(
        {
            "schema_version": SCHEMA_VERSION,
            "generated_by": "kanda_reasoner.freeze_after_update",
            "generated_at_utc": utc_now_iso(),
            "freezes": [],
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def root_readme() -> str:
    """Return the human README for the external project support box."""
    return """# Project Freeze After Update

This folder is an external support box for one selected project.

It lives under `<project>_show_project_to_AI/project_freeze_after_update`, not inside the selected project source root. KANDA Reasoner reads this folder when you use the **Freeze Feature After Update** tab, then it writes fresh AI-send files into `files_to_send_ai/`.

Do not move this folder into the KANDA Reasoner tool source. Do not merge it with another project. Each selected project keeps its own freeze memory here.

## Folder roles

```text
frozen_features_memory/
  Persistent memory of what has already been frozen in this project.

files_to_send_ai/
  Fresh output files that you upload to AI after updating the project.
```

Generated ZIP files may be recreated. The persistent source of truth for this selected project is inside
`frozen_features_memory/`.
"""


def send_readme() -> str:
    """Return README text for the AI-send output folder."""
    return """# Files To Send AI

This folder is refreshed by the **Freeze Feature After Update** tab.

Upload these generated files to AI when asking it to freeze a validated project
update:

```text
freeze_feature_ai_send_pack_<timestamp>.zip
what_to_say_to_ai_freeze_feature.md
```

The Markdown instruction file is intentionally kept outside the ZIP so you can
open it, copy it, and paste it into the AI chat.
"""


def entries_readme() -> str:
    """Return README text for freeze entry storage."""
    return """# Frozen Feature Entries

Store accepted freeze entries for this project here.

Valid freeze entry files should use this filename pattern:

```text
freeze-*.md
```

`README.md` and other non-matching Markdown files are ignored by the index
builder. A new project may have zero freeze entries. That is valid.

Do not copy freeze entries from KANDA Reasoner or from another project into
this folder unless you intentionally want this project to inherit that frozen
state.
"""


def initial_frozen_steps() -> str:
    """Return the initial persistent frozen-steps ledger."""
    return """# Project Frozen Implemented Steps

This file belongs to this project only.

It summarizes validated implementation steps that were accepted as frozen for
this project.

Current state:

```text
No frozen implemented steps have been recorded yet.
```

When AI creates a new accepted freeze entry, update this file so future AI-send
packs know what has already been frozen.
"""


def what_to_say(
    *,
    project_name: str,
    freeze_count: int,
    zip_path: Path,
    included_files: Iterable[Path],
    generated_at_utc: str,
) -> str:
    """Return the instruction file that remains outside the ZIP."""
    included = "\n".join(f"- `{path.as_posix()}`" for path in included_files)
    if not included:
        included = "- No files were included. This indicates a generation error."

    if freeze_count:
        freeze_context = (
            f"This project currently has {freeze_count} frozen feature entry file(s). "
            "Read the included freeze state before proposing a new freeze."
        )
    else:
        freeze_context = (
            "No prior freeze entries are recorded for this project yet. "
            "Treat this as the first freeze request for this project."
        )

    return f"""# What To Say To AI - Freeze Feature After Update

Generated at UTC: `{generated_at_utc}`
Project: `{project_name}`
AI-send ZIP: `{zip_path.name}`

## Message to paste to AI

```text
I updated this project and I want to freeze the validated feature safely.

Please read the uploaded ZIP first.
Use the frozen feature memory in the ZIP to understand what is already frozen.
Then help me create or update the appropriate freeze entry for this project.

Important rules:
- Do not assume KANDA Reasoner stores this project's freeze memory centrally or inside the reusable tool source.
- The project's freeze memory lives under <project_drive>/<project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory/.
- Do not copy freeze entries from another project.
- Do not freeze unvalidated behavior.
- Ask for validation evidence if it is not included in my message.
```

## Current freeze context

{freeze_context}

## Files included in the ZIP

{included}

## Human next step

Upload the ZIP and send this Markdown instruction text to AI.
"""
