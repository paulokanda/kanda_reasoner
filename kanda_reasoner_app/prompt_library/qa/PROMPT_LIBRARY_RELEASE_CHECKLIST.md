# Prompt Library Release Checklist

Version: 1.0.0
Status: Text-only manual release checklist
Use: Review the prompt library before publishing or exporting a release.

## Purpose

This checklist verifies that a prompt library release is internally
consistent, safe to export, and safe to import into another project.

## Release Identity

- Release name: <RELEASE_NAME>
- Release version: <RELEASE_VERSION>
- Release date: <YYYY-MM-DD>
- Source project: <PROJECT_NAME>
- Export target: <OUTPUT_FOLDER>

## Content Checks

- [ ] Active prompts selected for release are listed.
- [ ] Metadata sidecars are included for every prompt.
- [ ] Stack files are included when relevant.
- [ ] Profile templates are included when relevant.
- [ ] Overlay templates are included when relevant.
- [ ] Pack manifest is included when relevant.
- [ ] Deprecated or archive-only prompts are excluded unless intentional.

## Consistency Checks

- [ ] All metadata JSON files parse.
- [ ] All prompt versions match metadata versions.
- [ ] All dependencies reference included or documented prompts.
- [ ] All files use UTF-8 without BOM.
- [ ] Text is ASCII-safe unless the project explicitly allows otherwise.
- [ ] No hardcoded local path exists outside examples.

## Safety Checks

- [ ] The release does not include source-code patch files.
- [ ] The release does not include runtime artifacts.
- [ ] The release does not include active governance files unless this is a governance-specific pack.
- [ ] The release does not include private logs or secrets.
- [ ] The release does not silently change another project.

## Import Readiness

- [ ] Import instructions use <PROJECT_ROOT> placeholders.
- [ ] Import checklist is included.
- [ ] Required adaptation variables are documented.
- [ ] The target project can review before using prompts.

## Result

- [ ] PASS - Ready to export.
- [ ] FAIL - Do not export.
- [ ] PARTIAL - Reference-only release.

## Notes

<RELEASE_NOTES>
