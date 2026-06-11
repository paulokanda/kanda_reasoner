#!/usr/bin/env python3
"""AI-powered docstring generator with hardened validation and confidence scoring.

Phase 4 upgrades
----------------
- The inline ``_validate_docstring`` function is replaced by a call to the
  standalone :func:`docstring_validator.validate` which runs 14 independent
  checks organised into fatal and warning layers.
- :class:`ValidationConfig` is built from :class:`AIConfig` and forwarded on
  every call — thresholds are now configurable per-project without code changes.
- ``# AI-UNCERTAIN`` comments are appended to accepted low-confidence
  docstrings when ``AIConfig.uncertain_annotation`` is ``True``.
- :class:`GenerationStats` collects per-run counters (total, cached, ai_ok,
  fallback, low_confidence, medium_confidence) for GUI and log reporting.
- The ``include_private`` flag is surfaced: when ``AIConfig.include_private``
  is ``False``, private symbols (``_`` / ``__`` prefixed) are silently routed
  to the heuristic generator without an AI call.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from ai_config import AIConfig
from context_builder import AttributeInfo, ParameterInfo, SymbolContext
from docstring_validator import (
    ValidationConfig,
    ValidationResult,
    apply_uncertain_annotation,
    validate,
)


# ---------------------------------------------------------------------------
# Generation statistics
# ---------------------------------------------------------------------------


@dataclass
class GenerationStats:
    """Counters accumulated across one full project run.

    Parameters
    ----------
    total : int
        Total number of :meth:`AIDocstringGenerator.generate` calls.
    cached : int
        Calls resolved from the on-disk cache without an LLM request.
    ai_ok : int
        Calls where the AI produced an accepted docstring.
    fallback : int
        Calls that fell back to the heuristic generator.
    low_confidence : int
        Accepted AI docstrings rated ``"low"`` confidence.
    medium_confidence : int
        Accepted AI docstrings rated ``"medium"`` confidence.
    skipped_private : int
        Private-symbol calls routed directly to heuristic because
        ``include_private`` was ``False``.
    """

    total: int = 0
    cached: int = 0
    ai_ok: int = 0
    fallback: int = 0
    low_confidence: int = 0
    medium_confidence: int = 0
    skipped_private: int = 0

    @property
    def high_confidence(self) -> int:
        """Return the number of high-confidence AI docstrings.

        Returns
        -------
        int
            ``ai_ok - medium_confidence - low_confidence``.
        """
        return max(0, self.ai_ok - self.medium_confidence - self.low_confidence)

    def summary_line(self) -> str:
        """Return a one-line human-readable summary.

        Returns
        -------
        str
            Compact summary string suitable for log output or status bar.
        """
        return (
            f"total={self.total}  cached={self.cached}  "
            f"ai_ok={self.ai_ok} (high={self.high_confidence} "
            f"med={self.medium_confidence} low={self.low_confidence})  "
            f"fallback={self.fallback}  "
            f"skipped_private={self.skipped_private}"
        )


# ---------------------------------------------------------------------------
# Heuristic fallback
# ---------------------------------------------------------------------------


def _prettify(name: str) -> str:
    return " ".join(
        re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name.replace("_", " ")).split()
    ).lower()


def _heuristic_function_summary(name: str) -> str:
    lower = name.lower()
    PREFIX_MAP = {
        "get_": "Get", "set_": "Set", "build_": "Build", "create_": "Create",
        "make_": "Make", "load_": "Load", "save_": "Save", "update_": "Update",
        "compute_": "Compute", "normalize_": "Normalize", "resolve_": "Resolve",
        "detect_": "Detect", "extract_": "Extract", "apply_": "Apply",
        "render_": "Render", "show_": "Show", "hide_": "Hide", "emit_": "Emit",
        "handle_": "Handle", "run_": "Run", "scan_": "Scan",
        "validate_": "Validate",
    }
    for prefix, verb in PREFIX_MAP.items():
        if lower.startswith(prefix):
            tail = _prettify(name[len(prefix):])
            return f"{verb} {tail}."
    if lower.startswith("is_"):
        return f"Return whether {_prettify(name[3:])}."
    if lower.startswith("has_"):
        return f"Return whether {_prettify(name[4:])}."
    return f"Handle {_prettify(name) or name}."


def _heuristic_docstring(ctx: SymbolContext) -> str:
    """Generate a heuristic (no-AI) docstring from *ctx*.

    Parameters
    ----------
    ctx : SymbolContext
        Symbol context with name, kind, parameters, and return annotation.

    Returns
    -------
    str
        NumPy-style docstring body (no triple quotes, no indentation).
    """
    if ctx.kind == "module":
        stem = ctx.name.replace("_", " ").lower()
        if ctx.name == "__init__":
            return f"Package facade for {ctx.module_id.split('.')[-1] or ctx.name}."
        return f"Utilities and definitions for {stem or ctx.name}."

    if ctx.kind == "class":
        return f"Represent {_prettify(ctx.name) or ctx.name}."

    lines: list[str] = [_heuristic_function_summary(ctx.name), ""]
    if ctx.parameters:
        lines += ["Parameters", "----------"]
        for p in ctx.parameters:
            suffix = ", optional" if p.has_default else ""
            prefix = "**" if p.is_kwarg else ("*" if p.is_vararg else "")
            lines.append(f"{prefix}{p.name} : {p.annotation}{suffix}")
            lines.append(f"    TODO: describe {p.name}.")
        lines.append("")
    if ctx.return_annotation and ctx.return_annotation != "None":
        lines += ["Returns", "-------", ctx.return_annotation,
                  "    TODO: describe the return value.", ""]
    if ctx.raises_types:
        lines += ["Raises", "------"]
        for exc in ctx.raises_types:
            lines.append(exc)
            lines.append("    TODO: describe when this is raised.")
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------


def _build_system_prompt() -> str:
    return """\
You are a Python documentation expert. Your sole task is to write one precise,
correct NumPy-style docstring for the Python symbol shown in the USER message.

Rules you MUST follow:
1. Read the source code carefully. Document only what the code provably does.
2. Never invent parameter names, types, or behaviour absent from the source.
3. If a parameter's role is genuinely unclear, write: TODO: describe <n>.
4. @property / @cached_property: omit the Parameters section entirely.
5. @staticmethod: describe behaviour; do not mention self.
6. @classmethod: first param is the class (cls), not an instance.
7. @abstractmethod: note the method defines a contract; subclasses must override.
8. @overload stubs are listed as OVERLOAD SIGNATURES — use them to understand
   the full call interface, but document the implementation, not each stub.
9. Private names (_name, __name) are documented identically to public ones.
10. Module docstrings: one concise sentence describing the module's overall purpose.
11. Class docstrings: describe the abstraction. Add an Attributes section ONLY
    when CLASS ATTRIBUTES are provided — use exactly those names and types.
12. __init__ docstrings: put constructor arguments in Parameters; put instance
    attributes (from CLASS ATTRIBUTES) in an Attributes section.
13. @dataclass classes: fields listed in CLASS ATTRIBUTES are auto-generated;
    document them in an Attributes section, not Parameters.
14. Raises section: include ONLY the exception types listed in RAISES — do not
    invent new ones. Write a one-line description of when each is raised.
15. Keep every line under 88 characters.
16. Every section header (Parameters, Returns, Raises, Attributes, Notes, etc.)
    must be followed immediately by a line of dashes the same length as the header.
    Example:
      Returns
      -------
17. Sections must appear in this order when present:
    Parameters → Returns → Raises → Attributes → Notes → References → Examples.

Output format — output ONLY the raw docstring body:
- Do NOT include the surrounding triple-quote delimiters.
- Do NOT include any indentation.
- Do NOT include prose, explanations, or markdown outside the body.

NumPy style template:
  <One-line summary ending with a period.>

  [Extended description — only when the one-liner is insufficient.]

  Parameters
  ----------
  name : type[, optional]
      Description.

  Returns
  -------
  type
      Description.

  Raises
  ------
  ExceptionType
      When this is raised.

  Attributes
  ----------
  name : type
      Description.

  Notes
  -----
  [Optional.]

Omit any section that does not apply. The one-line summary is always required.
"""


# ---------------------------------------------------------------------------
# User prompt builder (unchanged from Phase 3 — imported cleanly)
# ---------------------------------------------------------------------------


def _build_user_prompt(ctx: SymbolContext) -> str:
    """Build the complete user-turn prompt from *ctx*.

    Parameters
    ----------
    ctx : SymbolContext
        Fully populated symbol context.

    Returns
    -------
    str
        Complete user prompt string ready to send to the LLM.
    """
    parts: list[str] = []

    if ctx.module_summary_block:
        parts.append("MODULE CONTEXT:")
        parts.append(ctx.module_summary_block)
    else:
        parts.append(f"MODULE: {ctx.module_id}")
        if ctx.module_docstring:
            brief = ctx.module_docstring.strip().splitlines()[0]
            parts.append(f"MODULE DOCSTRING: {brief}")

    if ctx.enclosing_class:
        parts.append(f"\nENCLOSING CLASS: {ctx.enclosing_class}")
        if ctx.class_docstring:
            brief = ctx.class_docstring.strip().splitlines()[0]
            parts.append(f"CLASS DOCSTRING: {brief}")

    if ctx.decorators:
        parts.append(f"\nDECORATORS: {', '.join('@' + d for d in ctx.decorators)}")
    if ctx.is_async:
        parts.append("NOTE: This is an async function.")
    if ctx.is_property:
        parts.append("NOTE: @property getter — omit the Parameters section entirely.")
    if ctx.is_cached_property:
        parts.append("NOTE: @cached_property — omit Parameters; value computed once and cached.")
    if ctx.is_abstract:
        parts.append("NOTE: @abstractmethod — document the contract; note subclasses must override.")
    if ctx.is_staticmethod:
        parts.append("NOTE: @staticmethod — no implicit self/cls; describe as standalone function.")
    if ctx.is_classmethod:
        parts.append("NOTE: @classmethod — cls receives the class, not an instance.")
    if ctx.is_overload:
        parts.append("NOTE: This is an @overload stub — document the implementation using "
                     "OVERLOAD SIGNATURES as the full call interface.")
    if ctx.is_dataclass and ctx.kind == "class":
        parts.append("NOTE: @dataclass — CLASS ATTRIBUTES are auto-generated fields; "
                     "document them in an Attributes section, not Parameters.")
    if ctx.is_init:
        parts.append("NOTE: __init__ — put constructor params in Parameters; "
                     "put CLASS ATTRIBUTES in an Attributes section.")

    parts.append(f"\nKIND: {ctx.kind}")
    parts.append(f"NAME: {ctx.name}")
    if ctx.signature:
        parts.append(f"SIGNATURE: {ctx.signature}")

    if ctx.overload_siblings:
        parts.append("\nOVERLOAD SIGNATURES (all accepted call forms):")
        for sig in ctx.overload_siblings:
            parts.append(f"  {sig}")

    if ctx.parameters:
        parts.append("\nPARAMETERS (AST ground truth — do not invent extras):")
        for p in ctx.parameters:
            prefix = "**" if p.is_kwarg else ("*" if p.is_vararg else "")
            optional = " [optional]" if p.has_default else ""
            kwonly = " [keyword-only]" if p.is_kwonly else ""
            parts.append(f"  {prefix}{p.name}: {p.annotation}{optional}{kwonly}")
    elif ctx.kind in ("function", "method") and not ctx.is_property and not ctx.is_cached_property:
        parts.append("\nPARAMETERS: none")

    if ctx.return_annotation:
        parts.append(f"\nRETURN ANNOTATION: {ctx.return_annotation}")

    if ctx.raises_types:
        parts.append("\nRAISES (document ONLY these — do not invent others):")
        for exc in ctx.raises_types:
            parts.append(f"  {exc}")

    if ctx.class_attributes:
        parts.append("\nCLASS ATTRIBUTES (self.* assignments — use in Attributes section):")
        for attr in ctx.class_attributes:
            type_part = f": {attr.type_hint}" if attr.type_hint else ""
            hint_part = f"  # {attr.description_hint}" if attr.description_hint else ""
            parts.append(f"  {attr.name}{type_part}{hint_part}")

    if ctx.imports:
        parts.append("\nMODULE IMPORTS (for type resolution, first 10):")
        for line in ctx.imports[:10]:
            parts.append(f"  {line}")

    if ctx.sibling_docstrings:
        parts.append("\nSIBLING DOCSTRINGS (mirror this style and level of detail):")
        for doc in ctx.sibling_docstrings[:2]:
            first_line = doc.strip().splitlines()[0][:120]
            parts.append(f"  • {first_line}")

    parts.append("\nSOURCE CODE:")
    parts.append("```python")
    parts.extend(ctx.source_lines[:60])
    parts.append("```")

    parts.append(
        f"\nWrite the NumPy-style docstring body for the {ctx.kind} '{ctx.name}'."
        " Output ONLY the raw body — no triple quotes, no indentation, no extra text."
    )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------


class _DocstringCache:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._data: dict[str, str] = {}
        if path.exists():
            try:
                self._data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                self._data = {}

    def get(self, key: str) -> str | None:
        return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        self._data[key] = value

    def flush(self) -> None:
        try:
            self._path.write_text(
                json.dumps(self._data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except Exception:
            pass


def _cache_key(ctx: SymbolContext) -> str:
    payload = "\n".join(ctx.source_lines) + ctx.signature + ctx.module_id
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _is_private_symbol(ctx: SymbolContext) -> bool:
    """Return True when *ctx* names a private Python symbol.

    Parameters
    ----------
    ctx : SymbolContext
        Symbol context to test.

    Returns
    -------
    bool
        True when ``ctx.name`` starts with an underscore.
    """
    return ctx.name.startswith("_")


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


class AIDocstringGenerator:
    """Generate precise, AI-powered docstrings using a local LLM endpoint.

    Phase 4: validation is delegated to :func:`docstring_validator.validate`,
    which runs 14 independent checks and returns structured
    :class:`~docstring_validator.ValidationResult` objects.  Low-confidence
    accepted docstrings are optionally annotated with ``# AI-UNCERTAIN``.
    :class:`GenerationStats` accumulates per-run counters for GUI reporting.

    Parameters
    ----------
    config : AIConfig, optional
        Connection and behaviour settings.
    project_root : Path, optional
        Used to locate the on-disk cache.  Caching is disabled when omitted.
    on_fallback : callable, optional
        Called with ``(symbol_name, reason)`` on every heuristic fallback.
    on_low_confidence : callable, optional
        Called with ``(symbol_name, issues)`` when a docstring is accepted but
        rated ``"low"`` confidence.  Useful for GUI highlights.
    """

    def __init__(
        self,
        config: AIConfig | None = None,
        project_root: Path | None = None,
        on_fallback: Callable[[str, str], None] | None = None,
        on_low_confidence: Callable[[str, list[str]], None] | None = None,
    ) -> None:
        self._config = config or AIConfig.default()
        self._on_fallback = on_fallback
        self._on_low_confidence = on_low_confidence
        self._system_prompt = _build_system_prompt()
        self._val_config: ValidationConfig = self._config.validation_config()
        self.stats = GenerationStats()

        self._cache: _DocstringCache | None = None
        if self._config.cache_enabled and project_root is not None:
            self._cache = _DocstringCache(project_root / self._config.cache_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, ctx: SymbolContext) -> str:
        """Generate a docstring body for *ctx*, AI-first with heuristic fallback.

        ``@overload`` stubs always return the heuristic one-liner immediately.
        Private symbols (``_`` / ``__`` prefix) are routed to heuristic when
        ``AIConfig.include_private`` is ``False``.

        Parameters
        ----------
        ctx : SymbolContext
            Fully populated symbol context.

        Returns
        -------
        str
            Raw docstring body (no triple quotes, no indentation).
            May include a trailing ``# AI-UNCERTAIN`` comment when confidence
            is low and ``AIConfig.uncertain_annotation`` is ``True``.
        """
        self.stats.total += 1

        # Fast-path: @overload stubs are never individually documented.
        if ctx.is_overload:
            return _heuristic_docstring(ctx)

        # Fast-path: private symbol routing.
        if not self._config.include_private and _is_private_symbol(ctx):
            self.stats.skipped_private += 1
            return _heuristic_docstring(ctx)

        # Cache hit.
        key = _cache_key(ctx)
        if self._cache is not None:
            cached = self._cache.get(key)
            if cached is not None:
                self.stats.cached += 1
                return cached

        # AI call + validation.
        reason = "unknown"
        try:
            raw = self._call_llm(ctx)
            result: ValidationResult = validate(raw, ctx, self._val_config)

            if result.ok:
                body = result.cleaned
                self.stats.ai_ok += 1

                if result.confidence == "low":
                    self.stats.low_confidence += 1
                    if self._on_low_confidence:
                        self._on_low_confidence(ctx.name, result.issues)
                elif result.confidence == "medium":
                    self.stats.medium_confidence += 1

                # Append AI-UNCERTAIN annotation when configured.
                if self._config.uncertain_annotation and result.ai_uncertain_comment:
                    body = apply_uncertain_annotation(body, result.ai_uncertain_comment)

                if self._cache is not None:
                    self._cache.set(key, body)
                return body

            reason = result.fatal_reason

        except Exception as exc:
            reason = str(exc)

        # Fallback.
        self.stats.fallback += 1
        if self._config.fallback_to_heuristic:
            if self._on_fallback:
                self._on_fallback(ctx.name, reason)
            return _heuristic_docstring(ctx)

        raise RuntimeError(
            f"AI generation failed for '{ctx.name}' in {ctx.module_id}: {reason}"
        )

    def flush_cache(self) -> None:
        """Persist the in-memory docstring cache to disk.

        Call once after all files in a project have been processed.
        """
        if self._cache is not None:
            self._cache.flush()

    def reset_stats(self) -> None:
        """Reset :attr:`stats` to zero for a new run.

        Useful when the generator instance is reused across multiple
        ``collect_changes`` calls (e.g. in interactive GUI sessions).
        """
        self.stats = GenerationStats()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _call_llm(self, ctx: SymbolContext) -> str:
        """Send a chat-completions request and return the raw model output.

        Parameters
        ----------
        ctx : SymbolContext
            Symbol context used to build the user prompt.

        Returns
        -------
        str
            Raw content string from the first choice.

        Raises
        ------
        RuntimeError
            On HTTP error, timeout, or malformed JSON response.
        """
        payload = json.dumps({
            "model": self._config.model,
            "max_tokens": self._config.max_tokens,
            "temperature": self._config.temperature,
            "messages": [
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": _build_user_prompt(ctx)},
            ],
        }).encode("utf-8")

        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self._config._api_key:
            headers["Authorization"] = f"Bearer {self._config._api_key}"

        req = urllib.request.Request(
            self._config.chat_endpoint,
            data=payload,
            method="POST",
            headers=headers,
        )
        try:
            with urllib.request.urlopen(req, timeout=self._config.timeout_seconds) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"LLM HTTP {exc.code}: {exc.reason}") from exc
        except TimeoutError as exc:
            raise RuntimeError(
                f"LLM timed out after {self._config.timeout_seconds}s"
            ) from exc
        except OSError as exc:
            raise RuntimeError(f"LLM connection error: {exc}") from exc

        try:
            data = json.loads(body)
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Unexpected LLM response: {exc}") from exc


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------


def make_build_functions(
    generator: AIDocstringGenerator,
) -> tuple[
    Callable[[SymbolContext], str],
    Callable[[SymbolContext], str],
    Callable[[SymbolContext], str],
]:
    """Return three callables replacing the heuristic ``build_*_docstring`` functions.

    Parameters
    ----------
    generator : AIDocstringGenerator
        Configured generator instance.

    Returns
    -------
    tuple
        ``(build_module, build_class, build_function)`` callables, each
        accepting a :class:`SymbolContext` and returning a docstring body string.

    Examples
    --------
    >>> cfg = AIConfig(model="codellama:13b")
    >>> gen = AIDocstringGenerator(config=cfg, project_root=Path("."))
    >>> build_module, build_class, build_function = make_build_functions(gen)
    >>> body = build_function(my_ctx)
    """
    def build_module(ctx: SymbolContext) -> str:
        return generator.generate(ctx)

    def build_class(ctx: SymbolContext) -> str:
        return generator.generate(ctx)

    def build_function(ctx: SymbolContext) -> str:
        return generator.generate(ctx)

    return build_module, build_class, build_function
