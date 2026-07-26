# project-path: kanda_reasoner_app/patch_governance/installer_template.py
"""Renderer for the canonical patch installer template."""

from __future__ import annotations

from pathlib import Path

_TEMPLATE_NAME = "installer_template.ps1"


class InstallerTemplateError(RuntimeError):
    """Raised when the installer template cannot be rendered safely."""


def render_installer_template(
    *,
    project_root_placeholder: str,
    patch_name: str,
    payload_folder: str,
) -> str:
    """Render the checked-in canonical PowerShell installer template.

    The renderer intentionally performs simple token replacement so it has no
    third-party dependency and stays compatible with standard Python.
    """
    if not patch_name or patch_name.endswith(".zip"):
        raise InstallerTemplateError("patch_name must be the ZIP basename without .zip")
    if not payload_folder:
        raise InstallerTemplateError("payload_folder is required")
    template_path = Path(__file__).with_name(_TEMPLATE_NAME)
    template = template_path.read_text(encoding="utf-8")
    replacements = {
        "{{PROJECT_ROOT}}": project_root_placeholder,
        "{{PATCH_NAME}}": patch_name,
        "{{PAYLOAD_FOLDER}}": payload_folder,
    }
    for token, value in replacements.items():
        template = template.replace(token, value)
    if "{{" in template or "}}" in template:
        raise InstallerTemplateError("Unresolved installer template token remains.")
    return template
