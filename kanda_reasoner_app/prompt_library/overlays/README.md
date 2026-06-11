# Prompt Library Overlays

This folder stores reusable text-only overlay templates for Tab 9 - Prompt Engineering Library.

An overlay is a conditional prompt template used only when a task touches a special risk area, subsystem, domain, or workflow. Overlays are not active governance and are not source code.

Allowed content:

- Markdown prompt templates.
- JSON metadata sidecars.
- Plain text guidance.

Forbidden content:

- Python source files.
- GUI code.
- Runtime patch scripts.
- Active governance replacements.
- Automatic prompt runners.

Project-agnostic rule:

- Use <PROJECT_ROOT> instead of absolute paths.
- Use <PROJECT_NAME> instead of a fixed project name.
- Use <DOMAIN_NAME> for domain-specific overlays.
- Keep project-specific examples inside Example Usage sections only.

Use these overlays when building a project-specific prompt pack from the general prompt library.
