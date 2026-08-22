param(
    [string]$ToolRoot = "",
    [string]$EvidenceJson = ""
)

$ErrorActionPreference = "Stop"

$CanonicalToolRoot = (
    Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
).Path

if (-not [string]::IsNullOrWhiteSpace($ToolRoot)) {
    $RequestedToolRoot = (
        Resolve-Path -LiteralPath $ToolRoot
    ).Path

    if (
        -not $RequestedToolRoot.Equals(
            $CanonicalToolRoot,
            [System.StringComparison]::OrdinalIgnoreCase
        )
    ) {
        throw (
            "ToolRoot must match the Tool source owning this command: " +
            $CanonicalToolRoot
        )
    }
}

$ToolRoot = $CanonicalToolRoot
$Python = Join-Path $ToolRoot ".venv\Scripts\python.exe"
$Helper = Join-Path $ToolRoot "tools\unload_project_for_tool_portable.py"

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Tool-owned Python was not found: $Python"
}

if (-not (Test-Path -LiteralPath $Helper -PathType Leaf)) {
    throw "Project-unload helper was not found: $Helper"
}

$Names = @(
    "kanda_reasoner_project_root",
    "KANDA_REASONER_PROJECT_ROOT",
    "KANDA_RUNTIME_PROJECT_ROOT",
    "PROJECT_REASONER_PROJECT_ROOT",
    "PROJECT_REASONER_SCAN_ROOT",
    "KANDA_REASONER_SCAN_ROOT"
)

foreach ($Name in $Names) {
    Remove-Item -LiteralPath ("Env:" + $Name) -ErrorAction SilentlyContinue
}

Get-ChildItem Env: | Where-Object {
    $_.Name.StartsWith("KANDA_") -or
    $_.Name.StartsWith("PROJECT_REASONER_")
} | ForEach-Object {
    Remove-Item -LiteralPath ("Env:" + $_.Name) -ErrorAction SilentlyContinue
}

$Arguments = @(
    $Helper,
    "--tool-root", $ToolRoot
)

if ($EvidenceJson) {
    $Arguments += @("--json-output", $EvidenceJson)
}

& $Python @Arguments

if ($LASTEXITCODE -ne 0) {
    throw "Project unload failed with exit code $LASTEXITCODE."
}
