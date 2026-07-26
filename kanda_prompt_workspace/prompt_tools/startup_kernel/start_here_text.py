"""Stable 00_START_HERE_FOR_AI.md generation."""

from __future__ import annotations

from typing import Iterable

from startup_kernel.boot_text import _prepend_startup_first_position_overrides
from startup_kernel.constants import (
    T9T013_RG015_BOOT_EXACTNESS_RULE,
    T9T013_RG015_HARD_OVERRIDE_RULE_V7,
    STABLE_BOOT_FILENAME,
)
from startup_kernel.start_here_body_intro import make_start_here_intro_section
from startup_kernel.start_here_body_routing import make_start_here_routing_section
from startup_kernel.start_here_lists import (
    build_active_bridge_report,
    build_numbered_startup_file_list,
    build_required_report_list,
)


__all__ = [
    "make_start_here_file",
]


def _append_prompt_authoring_overrides(content: str) -> str:
    """Append prompt-authoring override skeletons when missing."""
    if "Mandatory prompt-authoring RG-015 exact response skeleton loaded." not in content:
        content = content.rstrip() + "\n\n" + T9T013_RG015_BOOT_EXACTNESS_RULE.strip() + "\n"
    if "Mandatory prompt-authoring RG-015 hard override skeleton loaded." not in content:
        content = content.rstrip() + "\n\n" + T9T013_RG015_HARD_OVERRIDE_RULE_V7.strip() + "\n"
    return content


def make_start_here_file(
    date_cert: str,
    generated_at: str,
    expected_filenames: Iterable[str],
) -> tuple[str, str]:
    """Build the stable boot file used inside first_prompts_to_ai.zip."""
    expected = list(expected_filenames)
    content = make_start_here_intro_section(
        date_cert=date_cert,
        generated_at=generated_at,
        numbered_list=build_numbered_startup_file_list(expected),
        required_report_list=build_required_report_list(expected),
        active_bridge_report=build_active_bridge_report(),
        expected_count=len(expected),
    )
    content += make_start_here_routing_section()
    content = _append_prompt_authoring_overrides(content)
    content = _prepend_startup_first_position_overrides(content)
    return STABLE_BOOT_FILENAME, content
