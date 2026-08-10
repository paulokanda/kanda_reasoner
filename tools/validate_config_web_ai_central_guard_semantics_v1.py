# project-path: tools/validate_config_web_ai_central_guard_semantics_v1.py
"""Validate semantic free-access guard checks in the central Web AI validator."""

from __future__ import annotations

import argparse
from pathlib import Path

FEATURE_ID = "config-web-ai-central-guard-semantics-v1"


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    """Read one UTF-8 Project file."""
    return (root / relative).read_text(encoding="utf-8")


def validate(root: Path) -> None:
    """Validate structural guard semantics and remove stale copy assertions."""
    central = read(root, "tools/validate_config_web_ai_central_v1.py")
    direct = read(
        root,
        "kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py",
    )

    obsolete = (
        "I confirm this key belongs to Mistral Free mode.",
        "I confirm Free Quota Only is enabled for this Qwen account.",
        "I confirm this key belongs to a Groq Free Plan organization.",
    )
    for marker in obsolete:
        require(marker not in central, "obsolete copy assertion remains: " + marker)
    print("OBSOLETE_PROVIDER_COPY_ASSERTIONS_ABSENT: PASS")

    semantic = (
        'form.addRow("Free access guard", self.free_access_checkbox)',
        "display_profile.requires_free_confirmation",
        "self.free_access_checkbox.setEnabled(required)",
        "self.free_access_checkbox.setText(label)",
    )
    for marker in semantic:
        require(marker in central, "central semantic assertion missing: " + marker)
        require(marker in direct, "direct guard implementation missing: " + marker)
    print("CENTRAL_DIRECT_PROVIDER_GUARD_SEMANTIC_CONTRACT: PASS")

    for provider_id in ("gemini", "mistral", "qwen", "groq"):
        require(
            'display_profile.gateway_id == "' + provider_id + '"' in direct,
            "provider-specific guard branch missing: " + provider_id,
        )
    print("DIRECT_PROVIDER_GUARD_BRANCHES_PRESENT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)


def main() -> int:
    """Run focused validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    validate(Path(args.root).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
