# project-path: kanda_prompt_workspace/prompt_tools/startup_kernel/maintenance_text.py
"""Startup delivery maintenance protocol public entrypoint."""

from __future__ import annotations

from startup_kernel.maintenance_body import make_modify_startup_delivery_protocol_body


def make_modify_startup_delivery_protocol(generated_at: str, zip_filename: str) -> str:
    """Return the startup-delivery maintenance guardrail document."""
    return make_modify_startup_delivery_protocol_body(generated_at, zip_filename)
