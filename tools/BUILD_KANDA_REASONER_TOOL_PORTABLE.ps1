param(
    [string]$ToolRoot = "E:\kanda_reasoner",
    [string]$OutputDirectory = "E:\KandaReasoner_Portable_Output",
    [string]$ExternalProjectRoot = "E:\eeg_kanda",
    [switch]$ReplaceExisting,
    [switch]$SkipSmoke
)
$ErrorActionPreference = "Stop"
$ToolRoot = (Resolve-Path -LiteralPath $ToolRoot).Path
$Python = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"
$Unload = Join-Path $ToolRoot "tools\UNLOAD_PROJECT_FOR_TOOL_PORTABLE.ps1"
$Builder = Join-Path $ToolRoot "tools\build_kanda_reasoner_tool_portable.py"
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Governed Python 3.12 not found: $Python"
}
if (-not (Test-Path -LiteralPath $Unload -PathType Leaf)) {
    throw "Mandatory Project-unload command not found: $Unload"
}
if (-not (Test-Path -LiteralPath $Builder -PathType Leaf)) {
    throw "Canonical Tool Portable builder not found: $Builder"
}
$Evidence = Join-Path $env:TEMP ("kanda_tool_portable_unload_" + [guid]::NewGuid().ToString("N") + ".json")
try {
    & $Unload -ToolRoot $ToolRoot -EvidenceJson $Evidence
    if ($LASTEXITCODE -ne 0) {
        throw "Project unload failed. Tool Portable build is forbidden."
    }
    $Arguments = @(
        $Builder,
        "--tool-root", $ToolRoot,
        "--output-directory", $OutputDirectory,
        "--external-project-root", $ExternalProjectRoot,
        "--yes"
    )
    if ($ReplaceExisting) { $Arguments += "--replace-existing" }
    if ($SkipSmoke) { $Arguments += "--skip-smoke" }
    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "KANDA Reasoner Tool Portable build failed with exit code $LASTEXITCODE"
    }
}
finally {
    Remove-Item -LiteralPath $Evidence -Force -ErrorAction SilentlyContinue
}
