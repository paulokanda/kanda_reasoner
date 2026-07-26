# project-path: scripts/merge_freeze_validation_evidence.py
"""Merge local validation evidence into a matching KANDA freeze hint.

The helper is intentionally small and paste-safe for PowerShell validation
blocks. It can seed the freeze hint intake from the current patch ZIP sidecar
before merging evidence, so stale latest_freeze_hint.json records from a prior
feature do not block or receive evidence for the wrong feature.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _ensure_project_root_on_path() -> None:
    """Add the project root only when this command needs project imports."""
    project_root_text = str(PROJECT_ROOT)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)


def _freeze_hint_api() -> tuple[Any, Any, Any, Any]:
    """Return freeze-hint helpers after command-time import bootstrapping."""
    _ensure_project_root_on_path()
    from kanda_reasoner_app.freeze_hint_intake import (
        load_latest_freeze_hint_record,
        merge_validation_evidence_into_latest_hint,
        read_freeze_hint_from_patch_zip,
    )
    from kanda_reasoner_app.freeze_hint_intake.contract import save_freeze_hint_record

    return (
        load_latest_freeze_hint_record,
        merge_validation_evidence_into_latest_hint,
        read_freeze_hint_from_patch_zip,
        save_freeze_hint_record,
    )


class MergeEvidenceError(RuntimeError):
    """Raised when validation evidence cannot be merged safely."""


_ALLOWED_C0 = {"\t", "\r", "\n"}


def _reject_forbidden_control_characters(text: str) -> str:
    """Reject hidden C0 controls while preserving normal line separators."""
    for index, char in enumerate(text):
        if ord(char) < 32 and char not in _ALLOWED_C0:
            raise MergeEvidenceError(
                "FORBIDDEN_CONTROL_CHARACTER: "
                + f"U+{ord(char):04X} at character {index}."
            )
    return text


def _decode_evidence_bytes(data: bytes) -> str:
    """Decode governed evidence using explicit current and legacy contracts."""
    try:
        if data.startswith((b"\xff\xfe", b"\xfe\xff")):
            text = data.decode("utf-16", errors="strict")
        elif data.startswith(b"\xef\xbb\xbf"):
            text = data.decode("utf-8-sig", errors="strict")
        else:
            text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise MergeEvidenceError("EVIDENCE_ENCODING_INVALID: " + str(exc)) from exc
    return _reject_forbidden_control_characters(text)


def _read_text_file(path_text: str) -> str:
    """Read evidence with explicit UTF-8 and BOM-aware legacy support."""
    path = Path(path_text).expanduser().resolve()
    if not path.is_file():
        raise MergeEvidenceError("Evidence file not found: " + str(path))
    return _decode_evidence_bytes(path.read_bytes())


def _read_evidence(args: argparse.Namespace) -> str:
    """Support read evidence behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    
    Returns
    -------
    str
        The string result.
    """
    
    if args.evidence_file:
        return _read_text_file(args.evidence_file)
    if args.evidence_text:
        return str(args.evidence_text)
    if args.stdin:
        return sys.stdin.read()
    raise MergeEvidenceError(
        "Provide validation evidence with --evidence-file, --evidence-text, or --stdin."
    )


def _has_local_validation_marker(evidence: str) -> bool:
    """Support has local validation marker behavior.
    
    Parameters
    ----------
    evidence : str
        The evidence value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for raw_line in str(evidence or "").splitlines():
        line = raw_line.strip().lstrip("\ufeff")
        folded = line.casefold()
        if not line:
            continue
        if folded.startswith("validation ok:"):
            return True
        if folded.startswith("local validation passed"):
            return True
    return False


def _safe_feature_text(value: Any) -> str:
    """Support safe feature text behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(value or "").strip()


def _normalize_feature_id(value: Any) -> str:
    """Support normalize feature id behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = _safe_feature_text(value).casefold()
    normalized = []
    last_dash = False
    for char in text:
        if char.isalnum():
            normalized.append(char)
            last_dash = False
        else:
            if not last_dash:
                normalized.append("-")
                last_dash = True
    return "".join(normalized).strip("-")


def _feature_matches(left: Any, right: Any) -> bool:
    """Support feature matches behavior.
    
    Parameters
    ----------
    left : Any
        The left value.
    right : Any
        The right value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    left_id = _normalize_feature_id(left)
    right_id = _normalize_feature_id(right)
    return bool(left_id and right_id and left_id == right_id)


def _record_feature_id(record: Mapping[str, Any]) -> str:
    """Support record feature id behavior.
    
    Parameters
    ----------
    record : Mapping[str, Any]
        The record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    hint = record.get("hint")
    if isinstance(hint, Mapping):
        return _safe_feature_text(hint.get("feature_id"))
    return ""


def _latest_hint_matches(project_root: str, feature_id: str) -> bool:
    """Support latest hint matches behavior.
    
    Parameters
    ----------
    project_root : str
        The project root path.
    feature_id : str
        The feature id value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    load_latest_freeze_hint_record, _merge_func, _read_hint, _save_hint = _freeze_hint_api()
    loaded = load_latest_freeze_hint_record(project_root)
    if not loaded.get("ok"):
        return False
    record = loaded.get("record")
    if not isinstance(record, Mapping):
        return False
    return _feature_matches(_record_feature_id(record), feature_id)


def _seed_matching_hint_from_patch_zip(
    project_root: str,
    feature_id: str,
    patch_zip: str,
) -> None:
    """Support seed matching hint from patch zip behavior.
    
    Parameters
    ----------
    project_root : str
        The project root path.
    feature_id : str
        The feature id value.
    patch_zip : str
        The patch zip value.
    """
    
    if not patch_zip:
        raise MergeEvidenceError(
            "latest_freeze_hint.json does not match the validation feature. "
            "Pass --patch-zip so the helper can load the matching KANDA_FREEZE_HINT.json."
        )
    _load_latest, _merge_func, read_freeze_hint_from_patch_zip, save_freeze_hint_record = _freeze_hint_api()
    hint = read_freeze_hint_from_patch_zip(patch_zip)
    hint_feature_id = _safe_feature_text(hint.get("feature_id"))
    if not _feature_matches(hint_feature_id, feature_id):
        raise MergeEvidenceError(
            "patch ZIP KANDA_FREEZE_HINT feature_id mismatch: patch has "
            + hint_feature_id
            + "; validation evidence is for "
            + feature_id
            + "."
        )
    save_freeze_hint_record(project_root, hint)


def _ensure_matching_latest_hint(args: argparse.Namespace) -> None:
    """Support ensure matching latest hint behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    """
    
    if _latest_hint_matches(args.project_root, args.feature_id):
        return
    _seed_matching_hint_from_patch_zip(
        args.project_root,
        args.feature_id,
        str(args.patch_zip or ""),
    )
    if not _latest_hint_matches(args.project_root, args.feature_id):
        raise MergeEvidenceError(
            "Could not activate a matching freeze hint for feature_id: "
            + str(args.feature_id)
        )


def _build_parser() -> argparse.ArgumentParser:
    """Support build parser behavior.
    
    Returns
    -------
    argparse.ArgumentParser
        The argument parser result.
    """
    
    parser = argparse.ArgumentParser(
        description="Merge passed local validation evidence into matching freeze hint intake."
    )
    parser.add_argument(
        "--project-root",
        required=True,
        help="Active project root, for example E:\\kanda_reasoner.",
    )
    parser.add_argument(
        "--feature-id",
        required=True,
        help="Feature ID validated by the local validation command.",
    )
    parser.add_argument(
        "--feature-title",
        default="",
        help="Optional feature title for mismatch warnings.",
    )
    parser.add_argument(
        "--patch-zip",
        default="",
        help="Staged patch ZIP containing the matching root-level KANDA_FREEZE_HINT.json.",
    )
    parser.add_argument(
        "--evidence-file",
        default="",
        help="UTF-8 text file containing validation output markers.",
    )
    parser.add_argument(
        "--evidence-text",
        default="",
        help="Inline validation evidence text. Prefer --evidence-file for long logs.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read validation evidence from stdin.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Support main behavior.
    
    Parameters
    ----------
    argv : Sequence[str] | None, optional
        The optional argv value.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        evidence = _read_evidence(args)
        if not _has_local_validation_marker(evidence):
            raise MergeEvidenceError(
                "Validation evidence must include a local marker such as "
                "VALIDATION OK: <feature_id>."
            )
        _ensure_matching_latest_hint(args)
        merge_marker = "FREEZE_HINT_EVIDENCE_MERGE_OK: " + args.feature_id
        final_evidence = evidence.rstrip()
        if merge_marker not in final_evidence:
            final_evidence = final_evidence + "\n" + merge_marker
        _load_latest, merge_validation_evidence_into_latest_hint, _read_hint, _save_hint = _freeze_hint_api()
        result = merge_validation_evidence_into_latest_hint(
            args.project_root,
            final_evidence,
            feature_id=args.feature_id,
            feature_title=args.feature_title,
        )
        if not result.get("ok"):
            details = "; ".join(str(item) for item in result.get("errors") or [])
            if not details:
                details = "Unknown freeze hint merge failure."
            raise MergeEvidenceError(details)
    except Exception as exc:
        print("FREEZE_HINT_EVIDENCE_MERGE: FAIL - " + str(exc))
        return 1

    print("FREEZE_HINT_EVIDENCE_MERGE_OK: " + args.feature_id)
    for warning in result.get("warnings") or []:
        print("FREEZE_HINT_EVIDENCE_MERGE_WARNING: " + str(warning))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
