# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_encoding_profile.py
"""Source encoding and newline profiling for refactor preview safety."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from pathlib import Path
import tokenize

from .models import FEATURE_ID, SCHEMA_VERSION

__all__ = ["SourceEncodingProfile", "build_source_encoding_profile", "read_source_text"]


@dataclass(frozen=True)
class SourceEncodingProfile:
    """Stable text profile used before CST preview generation."""

    schema_version: str
    feature_id: str
    source_path: str
    byte_size: int
    byte_hash: str
    text_hash: str
    encoding: str
    has_utf8_bom: bool
    newline_style: str
    final_newline: bool
    encoding_cookie_present: bool
    read_errors: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready source encoding profile."""
        return asdict(self)


def build_source_encoding_profile(path: str | Path) -> SourceEncodingProfile:
    """Inspect source bytes without mutating the target file."""
    source_path = Path(path).expanduser().resolve()
    data = source_path.read_bytes()
    errors: list[str] = []
    encoding = _detect_encoding(source_path, errors)
    text = _decode_source(data, encoding, errors)
    return SourceEncodingProfile(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        source_path=str(source_path),
        byte_size=len(data),
        byte_hash=hashlib.sha256(data).hexdigest(),
        text_hash=hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest(),
        encoding=encoding,
        has_utf8_bom=data.startswith(b"\xef\xbb\xbf"),
        newline_style=_newline_style(data),
        final_newline=data.endswith((b"\n", b"\r")),
        encoding_cookie_present=_has_encoding_cookie(data),
        read_errors=errors,
    )


def read_source_text(path: str | Path, profile: SourceEncodingProfile | None = None) -> str:
    """Read source using the detected encoding profile."""
    source_path = Path(path).expanduser().resolve()
    data = source_path.read_bytes()
    errors: list[str] = []
    encoding = profile.encoding if profile is not None else _detect_encoding(source_path, errors)
    return _decode_source(data, encoding, errors)


def _detect_encoding(path: Path, errors: list[str]) -> str:
    """Return tokenizer-detected encoding, falling back to UTF-8."""
    try:
        with path.open("rb") as handle:
            encoding, _ = tokenize.detect_encoding(handle.readline)
        return encoding
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        errors.append(f"ENCODING_DETECTION_FAILED: {exc}")
        return "utf-8"


def _decode_source(data: bytes, encoding: str, errors: list[str]) -> str:
    """Decode source bytes with a safe fallback for reporting."""
    try:
        return data.decode(encoding)
    except (LookupError, UnicodeDecodeError) as exc:
        errors.append(f"SOURCE_DECODE_FALLBACK_UTF8_REPLACE: {exc}")
        return data.decode("utf-8", errors="replace")


def _newline_style(data: bytes) -> str:
    """Classify source newline style without normalizing it."""
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    cr = data.count(b"\r") - crlf
    kinds = sum(1 for count in (crlf, lf, cr) if count)
    if kinds > 1:
        return "mixed"
    if crlf:
        return "crlf"
    if lf:
        return "lf"
    if cr:
        return "cr"
    return "none"


def _has_encoding_cookie(data: bytes) -> bool:
    """Return whether the first two lines include a PEP 263 coding cookie."""
    lines = data.splitlines()[:2]
    lowered = b"\n".join(lines).lower()
    return b"coding" in lowered or b"coding:" in lowered or b"coding=" in lowered
