# project-path: scripts/update_no_isolated_zip_freeze_hint_after_validation.py
"""Update the No Isolated ZIP freeze hint after local validation passes.

This script never invents validation evidence. It reads a local validation
transcript, requires all expected markers, then updates the staged freeze hint
for the No Isolated ZIP Patch Delivery Gate v1 feature.
"""

from __future__ import annotations


__all__ = ['require_markers', 'update_freeze_hint']
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from kanda_reasoner_app.project_analysis_evidence_paths import analysis_project_freeze_after_update_dir

DEFAULT_FEATURE_ID = "kanda-router-bridge-no-isolated-zip-gate-v1"
DEFAULT_FEATURE_TITLE = "No Isolated ZIP Patch Delivery Gate v1"
DEFAULT_UPDATE_MARKER = "FREEZE HINT UPDATE OK: no-isolated-zip-gate-v1"

DEFAULT_REQUIRED_MARKERS = [
    "VALIDATION OK: kanda-router-bridge-no-isolated-zip-gate-v1",
    "PATCH DELIVERY RESPONSE CONTRACT: PASS",
    "ZIP CONTRACT: PASS",
    "STATUS: IN_SYNC",
]


def read_text(path: Path) -> str:
    """Read text using UTF-8 with replacement for safety."""
    return path.read_text(encoding="utf-8", errors="replace")


def require_markers(text: str, markers: Iterable[str]) -> list[str]:
    """Return missing markers from validation output."""
    return [marker for marker in markers if marker not in text]


def load_json(path: Path) -> dict:
    """Load a JSON object from disk."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return data


def save_json(path: Path, data: dict) -> None:
    """Save a JSON object using UTF-8 without BOM."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2, sort_keys=False)
        handle.write("\n")


def update_freeze_hint(
    project_root: Path,
    transcript_path: Path,
    feature_id: str,
    required_markers: list[str],
    update_marker: str,
) -> Path:
    """Update the staged freeze hint after transcript marker verification."""
    if not project_root.exists():
        raise FileNotFoundError(f"Project root not found: {project_root}")
    if not transcript_path.exists():
        raise FileNotFoundError(f"Validation transcript not found: {transcript_path}")

    transcript_text = read_text(transcript_path)
    missing = require_markers(transcript_text, required_markers)
    if missing:
        details = "; ".join(missing)
        raise RuntimeError(f"Validation transcript is missing required marker(s): {details}")

    hint_name = f"{feature_id}__KANDA_FREEZE_HINT.json"
    hint_path = analysis_project_freeze_after_update_dir(project_root) / "freeze_hint_intake" / hint_name
    if not hint_path.exists():
        raise FileNotFoundError(f"Staged freeze hint not found: {hint_path}")

    hint = load_json(hint_path)
    if hint.get("feature_id") != feature_id:
        raise RuntimeError(
            "The freeze hint feature_id does not match the requested feature."
        )

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    backup_path = hint_path.with_suffix(hint_path.suffix + ".before_validation_update.bak")
    if not backup_path.exists():
        save_json(backup_path, hint)

    evidence_lines = [
        f"Local validation accepted at {timestamp}.",
        "Required local validation markers were found in the validation transcript.",
    ]
    evidence_lines.extend(required_markers)

    hint["validation_evidence_summary"] = (
        "Local validation passed for "
        + str(hint.get("feature_title") or feature_id)
        + ". Markers captured: "
        + "; ".join(required_markers)
        + "."
    )
    hint["validation_evidence"] = evidence_lines
    hint["local_validation_markers"] = required_markers
    hint["local_validation_transcript"] = str(transcript_path)
    hint["local_validation_verified_at_utc"] = timestamp
    hint["freeze_readiness"] = "local_validation_passed"
    hint["requires_user_validation"] = False
    hint["known_warnings"] = (
        "Validation evidence was captured locally. Review the preview entry, "
        "then use Confirm and Write only if the human reviewer approves."
    )
    hint["planned_next_step"] = (
        "Open Freeze Feature After Update, preview the freeze entry, and Confirm "
        "and Write only after human review."
    )

    save_json(hint_path, hint)
    print(update_marker)
    return hint_path


def parse_args() -> argparse.Namespace:
    """Parse the args.
    
    Returns
    -------
    argparse.Namespace
        The namespace result.
    """
    
    parser = argparse.ArgumentParser(
        description="Update a staged No Isolated ZIP freeze hint after local validation."
    )
    parser.add_argument("--project-root", required=True, help="Path to the active project root.")
    parser.add_argument(
        "--validation-transcript",
        required=True,
        help="Path to a text file containing local validation output markers.",
    )
    parser.add_argument(
        "--feature-id",
        default=DEFAULT_FEATURE_ID,
        help="Feature ID of the staged freeze hint to update.",
    )
    parser.add_argument(
        "--marker",
        action="append",
        default=None,
        help="Required validation marker. Repeat for multiple markers. Defaults to Patch 1 markers.",
    )
    parser.add_argument(
        "--update-marker",
        default=DEFAULT_UPDATE_MARKER,
        help="Output marker printed after the freeze hint is updated.",
    )
    return parser.parse_args()


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    transcript_path = Path(args.validation_transcript).resolve()
    required_markers = args.marker if args.marker else DEFAULT_REQUIRED_MARKERS
    updated_path = update_freeze_hint(
        project_root,
        transcript_path,
        args.feature_id,
        required_markers,
        args.update_marker,
    )
    print(f"Updated freeze hint: {updated_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
