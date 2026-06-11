"""Result models for the AI docstring generator."""

from __future__ import annotations

__all__ = [
    "GenerationResult",
    "GenerationStats",
]

from dataclasses import dataclass, field


@dataclass
class GenerationResult:
    body: str
    source: str
    confidence: str
    issues: list[str]
    cache_hit: bool = False
    used_fallback: bool = False
    uncertain: bool = False
    uncertain_comment: str = ""
    generation_source: str = ""
    failure_reason: str = "none"
    failure_detail: str = ""


@dataclass
class GenerationStats:
    total: int = 0
    cached: int = 0
    ai_ok: int = 0
    fallback: int = 0
    low_confidence: int = 0
    medium_confidence: int = 0
    skipped_private: int = 0
    failure_reasons: dict[str, int] = field(default_factory=dict)

    def record_failure(self, failure_reason: str) -> None:
        """Record why AI generation was skipped, rejected, or downgraded."""
        key = (failure_reason or "unknown").strip() or "unknown"
        self.failure_reasons[key] = self.failure_reasons.get(key, 0) + 1

    @property
    def high_confidence(self) -> int:
        return max(0, self.ai_ok - self.medium_confidence - self.low_confidence)

    def summary_line(self) -> str:
        failure_summary = ""
        if self.failure_reasons:
            parts = [
                f"{reason}={count}"
                for reason, count in sorted(self.failure_reasons.items())
            ]
            failure_summary = "  failures=(" + ", ".join(parts) + ")"
        return (
            f"total={self.total}  cached={self.cached}  "
            f"ai_ok={self.ai_ok} (high={self.high_confidence} "
            f"med={self.medium_confidence} low={self.low_confidence})  "
            f"fallback={self.fallback}  skipped_private={self.skipped_private}"
            f"{failure_summary}"
        )
