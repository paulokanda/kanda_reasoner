# project-path: kanda_reasoner_app/manage_architecture/kanda_refactor_release_builder.py
"""Descriptor-driven governed release builder for AST-safe refactor delivery.

The builder is subordinate to the Large Module AST Split Audit workflow. It
assembles deterministic patch ZIPs from explicit descriptors and payload roots.
It never chooses architecture, installs into a live project, or writes frozen
memory. Generated Freeze logic only prepares evidence for the existing human
Preview -> Confirm and Write workflow.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

__all__ = [
    "PayloadSpec",
    "ReleaseDescriptor",
    "build_governed_release_zip",
    "descriptor_from_json",
    "manifest_from_descriptor",
]


@dataclass(frozen=True)
class PayloadSpec:
    """One governed payload file and its accepted predecessor identities."""

    relative_path: str
    accepted_existing_sha256: tuple[str, ...] = ()
    new_file: bool = False


@dataclass(frozen=True)
class ReleaseDescriptor:
    """Data-only release contract consumed by the generic builder."""

    feature_id: str
    feature_title: str
    zip_name: str
    payloads: tuple[PayloadSpec, ...]
    validator_relative_path: str
    required_markers: tuple[str, ...]
    protected_paths: tuple[str, ...]
    do_not_regress: tuple[str, ...]
    change_kind: str = "structural_refactor"
    behavior_change_expected: bool = False


def _sha256(path: Path) -> str:
    """Return lowercase SHA-256 for one file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: str) -> str:
    """Normalize and validate one project-relative payload path."""
    text = str(value or "").replace("\\", "/").strip("/")
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise ValueError("INVALID_RELEASE_RELATIVE_PATH: " + text)
    return path.as_posix()


def _as_string_tuple(value: Any, field_name: str) -> tuple[str, ...]:
    """Normalize one JSON list into a non-empty-or-empty tuple of text."""
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(field_name + " must be a JSON list")
    output: list[str] = []
    for item in value:
        text = str(item or "").strip()
        if not text:
            raise ValueError(field_name + " contains empty text")
        output.append(text)
    return tuple(output)


def descriptor_from_json(path: Path | str) -> ReleaseDescriptor:
    """Load and validate one release descriptor JSON file."""
    descriptor_path = Path(path).expanduser().resolve()
    payload = json.loads(descriptor_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Release descriptor must be a JSON object")
    payload_specs: list[PayloadSpec] = []
    for item in payload.get("payloads", []):
        if not isinstance(item, dict):
            raise ValueError("payloads entries must be JSON objects")
        relative_path = _safe_relative_path(str(item.get("relative_path", "")))
        accepted = _as_string_tuple(
            item.get("accepted_existing_sha256", []),
            "accepted_existing_sha256",
        )
        payload_specs.append(
            PayloadSpec(
                relative_path=relative_path,
                accepted_existing_sha256=accepted,
                new_file=bool(item.get("new_file", False)),
            )
        )
    feature_id = str(payload.get("feature_id", "")).strip()
    feature_title = str(payload.get("feature_title", "")).strip()
    zip_name = str(payload.get("zip_name", "")).strip()
    validator = _safe_relative_path(str(payload.get("validator_relative_path", "")))
    if not feature_id or not feature_title or not zip_name:
        raise ValueError("feature_id, feature_title, and zip_name are required")
    if not zip_name.lower().endswith(".zip"):
        raise ValueError("zip_name must end with .zip")
    if not payload_specs:
        raise ValueError("Release descriptor payloads must not be empty")
    return ReleaseDescriptor(
        feature_id=feature_id,
        feature_title=feature_title,
        zip_name=zip_name,
        payloads=tuple(payload_specs),
        validator_relative_path=validator,
        required_markers=_as_string_tuple(payload.get("required_markers", []), "required_markers"),
        protected_paths=_as_string_tuple(payload.get("protected_paths", []), "protected_paths"),
        do_not_regress=_as_string_tuple(payload.get("do_not_regress", []), "do_not_regress"),
        change_kind=str(payload.get("change_kind", "structural_refactor")),
        behavior_change_expected=bool(payload.get("behavior_change_expected", False)),
    )


def manifest_from_descriptor(
    descriptor: ReleaseDescriptor,
    payload_root: Path | str,
) -> dict[str, Any]:
    """Build exact payload hash manifest from one candidate payload root."""
    root = Path(payload_root).resolve()
    files: list[dict[str, Any]] = []
    for spec in descriptor.payloads:
        relative = _safe_relative_path(spec.relative_path)
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ValueError("PAYLOAD_OUTSIDE_ROOT: " + relative) from exc
        if not path.is_file():
            raise FileNotFoundError(str(path))
        files.append({
            "relative_path": relative,
            "sha256": _sha256(path),
            "accepted_existing_sha256": list(spec.accepted_existing_sha256),
            "new_file": spec.new_file,
        })
    return {
        "schema_version": "1.0",
        "feature_id": descriptor.feature_id,
        "feature_title": descriptor.feature_title,
        "zip_name": descriptor.zip_name,
        "change_kind": descriptor.change_kind,
        "behavior_change_expected": descriptor.behavior_change_expected,
        "files": files,
        "validator_relative_path": descriptor.validator_relative_path,
        "required_markers": list(descriptor.required_markers),
        "protected_paths": list(descriptor.protected_paths),
        "do_not_regress": list(descriptor.do_not_regress),
    }


def _quote_ps(value: str) -> str:
    """Quote text for a generated single-quoted PowerShell literal."""
    return "'" + value.replace("'", "''") + "'"


def _render_install_script(descriptor: ReleaseDescriptor) -> str:
    """Render generic freshness-guarded payload installation logic."""
    feature_literal = _quote_ps(descriptor.feature_id)
    lines = [
        "param(",
        "    [Parameter(Mandatory = $true)][string]$ProjectRoot,",
        "    [switch]$ManagedByCaller",
        ")",
        "",
        '$ErrorActionPreference = "Stop"',
        "$InstallFailed = $false",
        "",
        "try {",
        "    $ProjectPath = (Resolve-Path $ProjectRoot).Path",
        '    $ManifestPath = Join-Path $PSScriptRoot "PACKAGE_MANIFEST.json"',
        '    $PayloadRoot = Join-Path $PSScriptRoot "payload"',
        '    if (-not (Test-Path $ManifestPath)) { throw "PACKAGE_MANIFEST.json missing." }',
        '    if (-not (Test-Path $PayloadRoot)) { throw "payload folder missing." }',
        "    $Manifest = Get-Content -Raw -Encoding UTF8 $ManifestPath | ConvertFrom-Json",
        "",
        "    foreach ($Item in $Manifest.files) {",
        "        $RelativePath = [string]$Item.relative_path",
        "        $PayloadPath = Join-Path $PayloadRoot ($RelativePath -replace '/', '\\')",
        "        $DestinationPath = Join-Path $ProjectPath ($RelativePath -replace '/', '\\')",
        '        if (-not (Test-Path $PayloadPath)) { throw "Payload file missing: $RelativePath" }',
        "        $PayloadHash = (Get-FileHash -Algorithm SHA256 $PayloadPath).Hash.ToLowerInvariant()",
        "        if ($PayloadHash -ne ([string]$Item.sha256).ToLowerInvariant()) {",
        '            throw "PAYLOAD HASH MISMATCH: $RelativePath"',
        "        }",
        "        if (Test-Path $DestinationPath) {",
        "            $CurrentHash = (Get-FileHash -Algorithm SHA256 $DestinationPath).Hash.ToLowerInvariant()",
        "            $AllowedHashes = @(([string]$Item.sha256).ToLowerInvariant())",
        "            foreach ($Digest in @($Item.accepted_existing_sha256)) {",
        "                $AllowedHashes += ([string]$Digest).ToLowerInvariant()",
        "            }",
        "            if ($AllowedHashes -notcontains $CurrentHash) {",
        '                throw "SOURCE FRESHNESS CONFLICT: $RelativePath"',
        "            }",
        "        } elseif (-not [bool]$Item.new_file) {",
        '            throw "SOURCE MISSING: $RelativePath"',
        "        }",
        "    }",
        '    Write-Host "SOURCE FRESHNESS GUARD: PASS"',
        "",
        "    foreach ($Item in $Manifest.files) {",
        "        $RelativePath = [string]$Item.relative_path",
        "        $PayloadPath = Join-Path $PayloadRoot ($RelativePath -replace '/', '\\')",
        "        $DestinationPath = Join-Path $ProjectPath ($RelativePath -replace '/', '\\')",
        "        $DestinationDir = Split-Path -Parent $DestinationPath",
        "        if (-not (Test-Path $DestinationDir)) {",
        "            New-Item -ItemType Directory -Path $DestinationDir -Force | Out-Null",
        "        }",
        "        Copy-Item -Path $PayloadPath -Destination $DestinationPath -Force",
        "    }",
        '    Write-Host "PAYLOAD HASH VERIFICATION: PASS"',
        '    Write-Host "BOX SHIELDING INSTALL BOUNDARY: PASS"',
        "    Write-Host (\"INSTALL OK: \" + " + feature_literal + ")",
        "}",
        "catch {",
        "    $InstallFailed = $true",
        '    Write-Host "INSTALL ERROR"',
        "    Write-Host $_.Exception.Message",
        "    if ($_.ScriptStackTrace) { Write-Host $_.ScriptStackTrace }",
        "    if ($ManagedByCaller) { throw }",
        "}",
        "",
        "if (-not $ManagedByCaller -and $InstallFailed) {",
        '    Read-Host "Press Enter to clear terminal"',
        '    Read-Host "Press Enter again to clear"',
        "    Clear-Host",
        "}",
        "",
    ]
    return "\n".join(lines)


def _render_validate_script(descriptor: ReleaseDescriptor) -> str:
    """Render validation wrapper that preserves complete native stderr evidence."""
    validator_literal = _quote_ps(descriptor.validator_relative_path.replace("/", "\\"))
    markers_literal = ",\n        ".join(_quote_ps(item) for item in descriptor.required_markers)
    feature_literal = _quote_ps(descriptor.feature_id)
    return f'''param(
    [Parameter(Mandatory = $true)][string]$ProjectRoot,
    [Parameter(Mandatory = $true)][string]$PatchZipPath,
    [Parameter(Mandatory = $true)][string]$EvidenceFile,
    [switch]$ManagedByCaller
)

$ErrorActionPreference = "Stop"
$EvidenceLines = New-Object System.Collections.Generic.List[string]

function Add-EvidenceLine {{
    param([string]$Line)
    Write-Host $Line
    $EvidenceLines.Add($Line) | Out-Null
}}

try {{
    $ProjectPath = (Resolve-Path $ProjectRoot).Path
    $PatchPath = (Resolve-Path $PatchZipPath).Path
    $ValidatorPath = Join-Path $ProjectPath {validator_literal}
    if (-not (Test-Path $ValidatorPath)) {{ throw "Focused validator missing: $ValidatorPath" }}
    $PreviousPreference = $ErrorActionPreference
    try {{
        $ErrorActionPreference = "Continue"
        $Output = & python $ValidatorPath --patch-zip $PatchPath 2>&1
        $Code = $LASTEXITCODE
    }} finally {{
        $ErrorActionPreference = $PreviousPreference
    }}
    foreach ($Line in @($Output)) {{ Add-EvidenceLine ([string]$Line) }}
    if ($Code -ne 0) {{ throw "Focused validation failed." }}
    foreach ($Marker in @(
        {markers_literal}
    )) {{
        if (-not (($EvidenceLines -join "`n").Contains($Marker))) {{
            throw "Validation evidence marker missing: $Marker"
        }}
    }}
    Add-EvidenceLine ("VALIDATION OK: " + {feature_literal})
    Add-EvidenceLine "STATUS: IN_SYNC"
    $EvidenceDir = Split-Path -Parent $EvidenceFile
    if (-not (Test-Path $EvidenceDir)) {{ New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null }}
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false, $true)
    [System.IO.File]::WriteAllLines($EvidenceFile, $EvidenceLines, $Utf8NoBom)
    Add-EvidenceLine "VALIDATION_EVIDENCE_UTF8_CONTRACT: PASS"
    [System.IO.File]::WriteAllLines($EvidenceFile, $EvidenceLines, $Utf8NoBom)
}}
catch {{
    Write-Host "VALIDATION ERROR"
    Write-Host $_.Exception.Message
    if ($_.ScriptStackTrace) {{ Write-Host $_.ScriptStackTrace }}
    if ($ManagedByCaller) {{ throw }}
}}
'''


def _render_freeze_script(descriptor: ReleaseDescriptor) -> str:
    """Render freeze-evidence preparation that delegates to the existing merger."""
    feature_literal = _quote_ps(descriptor.feature_id)
    title_literal = _quote_ps(descriptor.feature_title)
    return f'''param(
    [Parameter(Mandatory = $true)][string]$ProjectRoot,
    [Parameter(Mandatory = $true)][string]$PatchZipPath,
    [Parameter(Mandatory = $true)][string]$ValidationEvidenceFile,
    [switch]$ManagedByCaller
)

$ErrorActionPreference = "Stop"
try {{
    $ProjectPath = (Resolve-Path $ProjectRoot).Path
    $PatchPath = (Resolve-Path $PatchZipPath).Path
    $EvidencePath = (Resolve-Path $ValidationEvidenceFile).Path
    $MergeScript = Join-Path $ProjectPath "scripts\\merge_freeze_validation_evidence.py"
    if (-not (Test-Path $MergeScript)) {{ throw "Freeze evidence merger missing." }}
    & python $MergeScript `
        --project-root $ProjectPath `
        --feature-id {feature_literal} `
        --feature-title {title_literal} `
        --patch-zip $PatchPath `
        --evidence-file $EvidencePath
    if ($LASTEXITCODE -ne 0) {{ throw "Freeze evidence preparation failed." }}
    Write-Host "FREEZE PREPARATION: PASS"
    Write-Host "Next: Preview Freeze Entry, review evidence, then Confirm and Write."
}}
catch {{
    Write-Host "FREEZE ERROR"
    Write-Host $_.Exception.Message
    if ($_.ScriptStackTrace) {{ Write-Host $_.ScriptStackTrace }}
    if ($ManagedByCaller) {{ throw }}
}}
'''


def _freeze_hint(descriptor: ReleaseDescriptor) -> dict[str, Any]:
    """Build root-level freeze hint without writing canonical frozen memory."""
    return {
        "schema_version": "1.0",
        "feature_id": descriptor.feature_id,
        "feature_title": descriptor.feature_title,
        "status": "prepared_not_frozen",
        "change_kind": descriptor.change_kind,
        "behavior_change_expected": descriptor.behavior_change_expected,
        "protected_paths": list(descriptor.protected_paths),
        "do_not_regress": list(descriptor.do_not_regress),
        "human_governance": "Preview Freeze Entry then explicit Confirm and Write",
    }


def _write_zip_text(archive: zipfile.ZipFile, name: str, text: str) -> None:
    """Write deterministic UTF-8 text with LF newlines into a ZIP archive."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    archive.writestr(name, normalized.encode("utf-8"))


def build_governed_release_zip(
    descriptor: ReleaseDescriptor,
    *,
    payload_root: Path | str,
    output_path: Path | str,
) -> Path:
    """Build one governed descriptor-driven ZIP without installing it."""
    root = Path(payload_root).resolve()
    output = Path(output_path).expanduser().resolve()
    manifest = manifest_from_descriptor(descriptor, root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        _write_zip_text(archive, "PACKAGE_MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        _write_zip_text(archive, "INSTALL.ps1", _render_install_script(descriptor))
        _write_zip_text(archive, "VALIDATE.ps1", _render_validate_script(descriptor))
        _write_zip_text(archive, "FREEZE.ps1", _render_freeze_script(descriptor))
        _write_zip_text(archive, "KANDA_FREEZE_HINT.json", json.dumps(_freeze_hint(descriptor), indent=2, sort_keys=True) + "\n")
        for spec in descriptor.payloads:
            relative = _safe_relative_path(spec.relative_path)
            archive.write(root / relative, "payload/" + relative)
    return output
