#!/usr/bin/env python3
"""Post-generation docstring validator with confidence scoring.

Every docstring produced by the AI is passed through :func:`validate` before
being accepted.  The function returns a :class:`ValidationResult` that carries:

- ``ok`` — whether the docstring may be used as-is.
- ``cleaned`` — the sanitised body (triple-quotes stripped, trailing whitespace
  removed, lines wrapped to the configured limit).
- ``confidence`` — ``"high"``, ``"medium"``, or ``"low"`` based on how many
  quality signals fire.
- ``issues`` — human-readable descriptions of every problem found, whether or
  not they triggered a rejection.

Design principles
-----------------
- Every check is a self-contained private function returning
  ``(passed: bool, issue: str | None)``.  Adding a new rule means adding one
  function and one entry in the ``_CHECKS`` list — nothing else changes.
- Checks are layered: *fatal* checks (empty output, markdown fence, code echo)
  cause immediate rejection.  *Warning* checks (TODO density, line length,
  section ordering, hallucinated names) lower confidence without necessarily
  rejecting.  The caller decides the rejection threshold via
  :attr:`ValidationConfig.min_confidence`.
- The parameter-name and exception-name guards cross-check against the AST
  ground truth stored in :class:`SymbolContext` — the AI cannot invent names
  that are not in the source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

from context_builder import SymbolContext


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# NumPy section headers in canonical order.
_NUMPY_SECTION_ORDER = [
    "Parameters", "Returns", "Yields", "Receives",
    "Raises", "Warns", "Attributes", "See Also",
    "Notes", "References", "Examples",
]

_SECTION_RE = re.compile(
    r"^(" + "|".join(re.escape(s) for s in _NUMPY_SECTION_ORDER) + r")\s*$",
    re.MULTILINE,
)

_UNDERLINE_RE = re.compile(r"^-{3,}\s*$", re.MULTILINE)

# Common stdlib / typing tokens that look like param names but aren't.
_TYPE_TOKENS: frozenset[str] = frozenset({
    "str", "int", "bool", "float", "list", "dict", "tuple", "set",
    "None", "object", "type", "bytes", "bytearray", "memoryview",
    "Any", "Optional", "Union", "Callable", "Iterable", "Iterator",
    "Generator", "Sequence", "Mapping", "MutableMapping", "Type",
    "ClassVar", "Final", "Literal", "TypeVar", "Generic",
    "Protocol", "NamedTuple", "TypedDict", "dataclass",
    "Path", "IO", "TextIO", "BinaryIO",
})

_SECTION_WORDS: frozenset[str] = frozenset(_NUMPY_SECTION_ORDER) | frozenset({
    "See", "Also",
})


@dataclass
class ValidationConfig:
    """Tunable parameters for the docstring validator.

    Parameters
    ----------
    max_line_length : int, optional
        Maximum permitted line length.  Lines longer than this are reported as
        warnings and lower confidence.  Default 88 (Black-compatible).
    max_todo_ratio : float, optional
        Maximum fraction of non-blank lines that may contain ``TODO``.
        Above this threshold the docstring is flagged as low-confidence.
        Default 0.5 — more than half TODO lines signals the AI gave up.
    min_confidence : str, optional
        Minimum confidence level required to accept a docstring.  One of
        ``"high"``, ``"medium"``, ``"low"``.  Default ``"low"`` — accept
        everything that passes the fatal checks.  Set to ``"medium"`` or
        ``"high"`` for stricter pipelines.
    max_length : int, optional
        Maximum total character length of the docstring body.  Bodies longer
        than this are rejected outright.  Default 4000.
    allow_invented_params : bool, optional
        When ``False`` (default), docstrings that name parameters not present
        in the AST ground truth are rejected.  Set to ``True`` only when
        debugging or when the AI consistently hallucinates for known reasons.
    allow_invented_raises : bool, optional
        When ``False`` (default), docstrings that document exception types not
        found by the AST raises-extractor are rejected.  Default ``False``.
    """

    max_line_length: int = 88
    max_todo_ratio: float = 0.5
    min_confidence: str = "low"      # "low" | "medium" | "high"
    max_length: int = 4000
    allow_invented_params: bool = False
    allow_invented_raises: bool = False


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass
class ValidationResult:
    """Outcome of validating one AI-generated docstring.

    Parameters
    ----------
    ok : bool
        Whether the docstring passed all fatal checks and meets the configured
        minimum confidence threshold.
    cleaned : str
        Sanitised docstring body.  Empty string when ``ok`` is ``False``.
    confidence : str
        Quality estimate: ``"high"``, ``"medium"``, or ``"low"``.
    issues : list[str]
        Human-readable descriptions of every problem found, in order of
        severity.  Non-empty even when ``ok`` is ``True`` — issues may be
        warnings rather than fatal errors.
    fatal_reason : str
        Non-empty only when a fatal check failed; describes why the docstring
        was rejected outright.
    ai_uncertain_comment : str
        When non-empty, this one-line comment should be appended as a
        ``# AI-UNCERTAIN`` annotation to the generated docstring so that
        developers know to review it.
    """

    ok: bool
    cleaned: str
    confidence: str = "high"
    issues: list[str] = field(default_factory=list)
    fatal_reason: str = ""
    ai_uncertain_comment: str = ""

    @classmethod
    def fatal(cls, reason: str) -> "ValidationResult":
        """Return a failed result for a fatal check.

        Parameters
        ----------
        reason : str
            Human-readable description of the fatal error.

        Returns
        -------
        ValidationResult
            A result with ``ok=False`` and ``confidence="low"``.
        """
        return cls(ok=False, cleaned="", confidence="low",
                   issues=[reason], fatal_reason=reason)


# ---------------------------------------------------------------------------
# Individual check functions
# Each returns (passed: bool, issue_message: str | None).
# passed=False on a *fatal* check triggers immediate rejection.
# passed=False on a *warning* check lowers confidence only.
# ---------------------------------------------------------------------------


def _check_empty(body: str, _ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    if not body:
        return False, "empty output"
    return True, None


def _check_markdown_fence(body: str, _ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    if body.startswith("```"):
        return False, "output wrapped in markdown code fence"
    return True, None


def _check_code_echo(body: str, _ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    first = body.splitlines()[0].strip() if body.splitlines() else ""
    if first.startswith(("def ", "class ", "async def ", "import ", "from ", "@")):
        return False, "first line looks like echoed source code"
    return True, None


def _check_too_long(body: str, _ctx: SymbolContext, cfg: ValidationConfig) -> tuple[bool, str | None]:
    if len(body) > cfg.max_length:
        return False, f"output too long ({len(body)} chars > {cfg.max_length})"
    return True, None


def _check_blank_first_line(body: str, _ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    first = body.splitlines()[0].strip() if body.splitlines() else ""
    if not first:
        return False, "first line is blank — one-line summary required"
    return True, None


def _check_summary_ends_period(body: str, _ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Warn (non-fatal) when the one-line summary doesn't end with a period."""
    first = body.splitlines()[0].strip() if body.splitlines() else ""
    if first and not first.endswith("."):
        return False, "one-line summary does not end with a period"
    return True, None


def _check_line_length(body: str, _ctx: SymbolContext, cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Warn (non-fatal) when any line exceeds max_line_length."""
    violations = [
        i + 1 for i, line in enumerate(body.splitlines())
        if len(line) > cfg.max_line_length
    ]
    if violations:
        return False, (
            f"{len(violations)} line(s) exceed {cfg.max_line_length} chars "
            f"(first at line {violations[0]})"
        )
    return True, None


def _check_todo_density(body: str, _ctx: SymbolContext, cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Warn (non-fatal) when more than max_todo_ratio of lines contain TODO."""
    lines = [ln for ln in body.splitlines() if ln.strip()]
    if not lines:
        return True, None
    todo_count = sum(1 for ln in lines if "TODO" in ln)
    ratio = todo_count / len(lines)
    if ratio > cfg.max_todo_ratio:
        return False, (
            f"high TODO density ({todo_count}/{len(lines)} lines = "
            f"{ratio:.0%}) — AI may not have understood the code"
        )
    return True, None


def _check_invented_params(body: str, ctx: SymbolContext, cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Fatal (when enabled) when param names not in the AST appear in the body."""
    if cfg.allow_invented_params or not ctx.parameters:
        return True, None

    known = {p.name for p in ctx.parameters}
    known |= {a.name for a in ctx.class_attributes}

    # Extract "name :" patterns from Parameters section only.
    in_params = False
    found: set[str] = set()
    for line in body.splitlines():
        stripped = line.strip()
        if stripped == "Parameters":
            in_params = True
            continue
        if in_params and _UNDERLINE_RE.match(stripped):
            continue
        if in_params and _SECTION_RE.match(stripped):
            in_params = False
            continue
        if in_params:
            m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_*]*)\s*:", stripped)
            if m:
                found.add(m.group(1))

    invented = found - known - _TYPE_TOKENS - _SECTION_WORDS
    if invented:
        return False, f"invented parameter name(s) not in AST: {sorted(invented)}"
    return True, None


def _check_invented_raises(body: str, ctx: SymbolContext, cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Fatal (when enabled) when exception names not raised in the AST appear."""
    if cfg.allow_invented_raises:
        return True, None
    if not ctx.raises_types:
        return True, None
    if "Raises" not in body:
        return True, None

    known_exc = set(ctx.raises_types) | {"Exception", "BaseException", "StopIteration"}

    in_raises = False
    found: set[str] = set()
    for line in body.splitlines():
        stripped = line.strip()
        if stripped == "Raises":
            in_raises = True
            continue
        if in_raises and _UNDERLINE_RE.match(stripped):
            continue
        if in_raises and _SECTION_RE.match(stripped):
            in_raises = False
            continue
        if in_raises and re.match(r"^[A-Z][a-zA-Z0-9_]*$", stripped):
            found.add(stripped)

    invented = found - known_exc
    if invented:
        return False, f"invented exception type(s) not raised in AST: {sorted(invented)}"
    return True, None


def _check_property_has_params(body: str, ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Warn when a @property docstring contains a Parameters section."""
    if not (ctx.is_property or ctx.is_cached_property):
        return True, None
    if "Parameters\n----------" in body or "Parameters\n" in body:
        return False, "@property docstring contains a Parameters section — should be omitted"
    return True, None


def _check_section_ordering(body: str, _ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Warn when NumPy sections appear out of canonical order."""
    sections_found = [m.group(1) for m in _SECTION_RE.finditer(body)]
    ordered = [s for s in _NUMPY_SECTION_ORDER if s in sections_found]
    if sections_found != ordered:
        return False, f"NumPy sections out of order: got {sections_found}, expected {ordered}"
    return True, None


def _check_source_verbatim(body: str, ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Warn when a substantial span of the source code appears verbatim in the output."""
    if not ctx.source_lines:
        return True, None
    # Check for any run of 3+ consecutive source lines appearing in the body.
    for i in range(len(ctx.source_lines) - 2):
        run = "\n".join(ln.strip() for ln in ctx.source_lines[i:i + 3] if ln.strip())
        if len(run) > 40 and run in body:
            return False, "output appears to reproduce source code verbatim"
    return True, None


def _check_underlines_match_headers(body: str, _ctx: SymbolContext, _cfg: ValidationConfig) -> tuple[bool, str | None]:
    """Warn when a section header's underline length doesn't match the header."""
    lines = body.splitlines()
    for i, line in enumerate(lines[:-1]):
        stripped = line.strip()
        if _SECTION_RE.match(stripped):
            next_stripped = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if _UNDERLINE_RE.match(next_stripped) and len(next_stripped) != len(stripped):
                return False, (
                    f"section '{stripped}' underline length mismatch "
                    f"({len(next_stripped)} dashes vs {len(stripped)} chars)"
                )
    return True, None


# ---------------------------------------------------------------------------
# Check registry
# ---------------------------------------------------------------------------
# Each entry: (check_fn, is_fatal, confidence_penalty)
# confidence_penalty: 0=none, 1=drop to medium, 2=drop to low

_CheckEntry = tuple[
    Callable[[str, SymbolContext, ValidationConfig], tuple[bool, str | None]],
    bool,   # fatal?
    int,    # confidence penalty (0 | 1 | 2)
]

_FATAL_CHECKS: list[_CheckEntry] = [
    (_check_empty,              True,  2),
    (_check_markdown_fence,     True,  2),
    (_check_code_echo,          True,  2),
    (_check_too_long,           True,  2),
    (_check_blank_first_line,   True,  2),
    (_check_invented_params,    True,  2),
    (_check_invented_raises,    True,  2),
]

_WARNING_CHECKS: list[_CheckEntry] = [
    (_check_summary_ends_period,        False, 0),   # style note only
    (_check_line_length,                False, 1),
    (_check_todo_density,               False, 2),
    (_check_property_has_params,        False, 1),
    (_check_section_ordering,           False, 0),
    (_check_source_verbatim,            False, 2),
    (_check_underlines_match_headers,   False, 0),
]


# ---------------------------------------------------------------------------
# Sanitiser
# ---------------------------------------------------------------------------


def _sanitise(raw: str) -> str:
    """Strip triple quotes, normalise trailing whitespace, collapse blank runs.

    Parameters
    ----------
    raw : str
        Raw text from the language model.

    Returns
    -------
    str
        Cleaned docstring body.
    """
    body = raw.strip()

    # Strip accidental triple-quote wrapping.
    for delim in ('"""', "'''"):
        if (
            body.startswith(delim)
            and body.endswith(delim)
            and len(body) > len(delim) * 2
        ):
            body = body[len(delim):-len(delim)].strip()
            break

    # Strip trailing whitespace from every line.
    lines = [ln.rstrip() for ln in body.splitlines()]

    # Collapse runs of more than two consecutive blank lines.
    cleaned_lines: list[str] = []
    blank_run = 0
    for ln in lines:
        if ln == "":
            blank_run += 1
            if blank_run <= 2:
                cleaned_lines.append(ln)
        else:
            blank_run = 0
            cleaned_lines.append(ln)

    # Remove trailing blank lines.
    while cleaned_lines and cleaned_lines[-1] == "":
        cleaned_lines.pop()

    return "\n".join(cleaned_lines)


# ---------------------------------------------------------------------------
# Confidence arithmetic
# ---------------------------------------------------------------------------

_CONFIDENCE_LEVELS = {"high": 2, "medium": 1, "low": 0}
_CONFIDENCE_NAMES = {2: "high", 1: "medium", 0: "low"}
_MIN_CONF_VALUES = {"high": 2, "medium": 1, "low": 0}


def _confidence_ok(confidence: str, min_confidence: str) -> bool:
    return _CONFIDENCE_LEVELS.get(confidence, 0) >= _MIN_CONF_VALUES.get(min_confidence, 0)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate(
    raw: str,
    ctx: SymbolContext,
    config: ValidationConfig | None = None,
) -> ValidationResult:
    """Validate and clean one AI-generated docstring.

    Runs every check in :data:`_FATAL_CHECKS` (immediate rejection on failure)
    then every check in :data:`_WARNING_CHECKS` (confidence reduction only).

    Parameters
    ----------
    raw : str
        Raw text returned by the language model.
    ctx : SymbolContext
        Symbol context used for AST cross-checks (parameter names, raises).
    config : ValidationConfig, optional
        Tunable thresholds.  Defaults to :class:`ValidationConfig` with all
        defaults applied.

    Returns
    -------
    ValidationResult
        Structured result with ``ok``, ``cleaned``, ``confidence``,
        ``issues``, ``fatal_reason``, and ``ai_uncertain_comment``.
    """
    cfg = config or ValidationConfig()
    issues: list[str] = []
    confidence_score = 2   # start at "high"

    # ---- Sanitise first ----
    cleaned = _sanitise(raw)

    # ---- Fatal checks ----
    for check_fn, _is_fatal, penalty in _FATAL_CHECKS:
        passed, issue = check_fn(cleaned, ctx, cfg)
        if not passed:
            msg = issue or "unknown fatal error"
            return ValidationResult.fatal(msg)

    # ---- Warning checks ----
    for check_fn, _is_fatal, penalty in _WARNING_CHECKS:
        passed, issue = check_fn(cleaned, ctx, cfg)
        if not passed and issue:
            issues.append(issue)
            confidence_score = max(0, confidence_score - penalty)

    confidence = _CONFIDENCE_NAMES[confidence_score]

    # ---- Confidence gate ----
    if not _confidence_ok(confidence, cfg.min_confidence):
        reason = (
            f"confidence '{confidence}' below minimum '{cfg.min_confidence}': "
            + "; ".join(issues)
        )
        return ValidationResult(
            ok=False,
            cleaned="",
            confidence=confidence,
            issues=issues,
            fatal_reason=reason,
        )

    # ---- Uncertain annotation ----
    uncertain_comment = ""
    if confidence == "low":
        uncertain_comment = "# AI-UNCERTAIN: review this docstring before committing"
    elif confidence == "medium" and any("TODO" in i for i in issues):
        uncertain_comment = "# AI-UNCERTAIN: high TODO density — consider manual completion"

    return ValidationResult(
        ok=True,
        cleaned=cleaned,
        confidence=confidence,
        issues=issues,
        ai_uncertain_comment=uncertain_comment,
    )


def apply_uncertain_annotation(docstring_body: str, comment: str) -> str:
    """Append an ``# AI-UNCERTAIN`` comment to the last line of the docstring body.

    Parameters
    ----------
    docstring_body : str
        Raw docstring body (no triple-quote delimiters).
    comment : str
        The annotation comment to append.  If empty, the body is returned
        unchanged.

    Returns
    -------
    str
        Docstring body with the comment appended on a new line.
    """
    if not comment:
        return docstring_body
    return docstring_body.rstrip() + "\n" + comment
