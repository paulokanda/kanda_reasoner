param(
    [string]$ToolRoot = "",
    [string]$OutputDirectory = "",
    [switch]$ReplaceExisting,
    [switch]$SkipSmoke
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
            "ToolRoot must match the Tool source owning this builder: " +
            $CanonicalToolRoot
        )
    }
}

$ToolRoot = $CanonicalToolRoot
$Python = Join-Path $ToolRoot ".venv\Scripts\python.exe"
$Builder = Join-Path $ToolRoot "tools\build_kanda_reasoner_tool_portable.py"
$EntrypointGate = Join-Path $ToolRoot (
    "tools\portable_entrypoint_shell_open_release_gate.py"
)
$BytecodeCleanup = Join-Path $ToolRoot (
    "tools\portable_source_bytecode_cleanup.ps1"
)

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Tool-owned Python was not found: $Python"
}

if (-not (Test-Path -LiteralPath $Builder -PathType Leaf)) {
    throw "Canonical Tool Portable builder was not found: $Builder"
}

if (-not (Test-Path -LiteralPath $EntrypointGate -PathType Leaf)) {
    throw "Portable entrypoint release gate was not found: $EntrypointGate"
}

if (-not (Test-Path -LiteralPath $BytecodeCleanup -PathType Leaf)) {
    throw "Portable source bytecode cleanup helper was not found: $BytecodeCleanup"
}

if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    Add-Type -AssemblyName System.Windows.Forms
    $Dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $Dialog.Description = (
        "Select where KandaReasoner_Portable_Output will be created"
    )
    $Dialog.ShowNewFolderButton = $true
    $Result = $Dialog.ShowDialog()

    if ($Result -ne [System.Windows.Forms.DialogResult]::OK) {
        throw "Portable destination-folder selection was cancelled."
    }

    $OutputDirectory = Join-Path (
        $Dialog.SelectedPath
    ) "KandaReasoner_Portable_Output"
}

$OutputDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)

if ((Split-Path -Leaf $OutputDirectory) -ne "KandaReasoner_Portable_Output") {
    throw (
        "Portable output folder must be named " +
        "KandaReasoner_Portable_Output: $OutputDirectory"
    )
}

$DeliveryRoot = Split-Path -Parent $OutputDirectory
$DeliveryNamePattern = (
    "^KandaReasoner-\d{8}_\d{6}-Windows-Portable\.zip$"
)
$ExistingDeliveryPaths = @()

if (Test-Path -LiteralPath $DeliveryRoot -PathType Container) {
    $ExistingDeliveryPaths = @(
        Get-ChildItem -LiteralPath $DeliveryRoot -File |
            Where-Object {
                $_.Name -match $DeliveryNamePattern
            } |
            ForEach-Object {
                $_.FullName
            }
    )
}

Write-Host "PORTABLE TOOL ROOT FROM BUILDER LOCATION: PASS"
Write-Host "PORTABLE TOOL VENV PYTHON: PASS"
Write-Host "PORTABLE PROJECT SELECTION MUTATION: ABSENT"
Write-Host "PORTABLE DESTINATION USER SELECTED: PASS"
Write-Host "PORTABLE OUTPUT FOLDER: $OutputDirectory"
Write-Host "PORTABLE DELIVERY ZIP NAMING: TIMESTAMPED BY CANONICAL BUILDER"
Write-Host "PORTABLE ENTRYPOINT SHELL OPEN RELEASE GATE: REQUIRED"

$Arguments = @(
    $Builder,
    "--tool-root", $ToolRoot,
    "--output-directory", $OutputDirectory,
    "--yes"
)

if ($ReplaceExisting) {
    $Arguments += "--replace-existing"
}

if ($SkipSmoke) {
    $Arguments += "--skip-smoke"
}

$DriveRoot = [System.IO.Path]::GetPathRoot($ToolRoot)
$ToolName = Split-Path $ToolRoot -Leaf
$TransientRoot = Join-Path $DriveRoot (
    $ToolName + "_delete_after_daily_work"
)
$PycacheRoot = Join-Path $TransientRoot (
    "portable_builder_pycache_" + [Guid]::NewGuid().ToString("N")
)
$PreviousPycachePrefix = [Environment]::GetEnvironmentVariable(
    "PYTHONPYCACHEPREFIX",
    "Process"
)

Write-Host "PORTABLE CANONICAL BUILDER PREEXISTING BYTECODE CLEANUP: REQUIRED"
& $BytecodeCleanup -PortableRoot (Join-Path $ToolRoot "portable")
Write-Host "PORTABLE CANONICAL BUILDER PREEXISTING BYTECODE CLEANUP: PASS"

New-Item -ItemType Directory -Path $PycacheRoot -Force | Out-Null
$env:PYTHONPYCACHEPREFIX = $PycacheRoot

Write-Host "PORTABLE CANONICAL BUILDER PYCACHE ISOLATION: ENABLED"
Write-Host "PORTABLE CANONICAL BUILDER PYCACHE ROOT: TRANSIENT DAILY-WORK"

& $Python @Arguments
$BuildExitCode = $LASTEXITCODE

Remove-Item Env:PYTHONPYCACHEPREFIX -ErrorAction SilentlyContinue
if (-not [string]::IsNullOrEmpty($PreviousPycachePrefix)) {
    $env:PYTHONPYCACHEPREFIX = $PreviousPycachePrefix
}

if (Test-Path -LiteralPath $PycacheRoot) {
    Remove-Item -LiteralPath $PycacheRoot -Recurse -Force
}

Write-Host "PORTABLE CANONICAL BUILDER PYCACHE CLEANUP: PASS"

if ($BuildExitCode -ne 0) {
    throw (
        "KANDA Reasoner Tool Portable build failed with exit code " +
        $BuildExitCode
    )
}

$CurrentDeliveryZips = @(
    Get-ChildItem -LiteralPath $DeliveryRoot -File |
        Where-Object {
            $_.Name -match $DeliveryNamePattern
        }
)

$NewDeliveryZips = @(
    $CurrentDeliveryZips |
        Where-Object {
            $ExistingDeliveryPaths -notcontains $_.FullName
        }
)

if ($NewDeliveryZips.Count -ne 1) {
    throw (
        "PORTABLE ENTRYPOINT RELEASE GATE NEW ZIP DISCOVERY FAILED: " +
        "expected=1;observed=" + $NewDeliveryZips.Count
    )
}

$PublishedZip = $NewDeliveryZips[0].FullName
Write-Host "PORTABLE ENTRYPOINT RELEASE GATE NEW ZIP DISCOVERY: PASS"
Write-Host ("PORTABLE ENTRYPOINT RELEASE GATE ZIP: " + $PublishedZip)

& $Python -B $EntrypointGate @(
    "--zip-path", $PublishedZip,
    "--work-root", $TransientRoot
)
$EntrypointGateExitCode = $LASTEXITCODE

if ($EntrypointGateExitCode -ne 0) {
    if (Test-Path -LiteralPath $PublishedZip -PathType Leaf) {
        Remove-Item -LiteralPath $PublishedZip -Force
    }

    if (Test-Path -LiteralPath $PublishedZip -PathType Leaf) {
        throw (
            "PORTABLE ENTRYPOINT RELEASE GATE FAILED AND REJECTED ZIP " +
            "COULD NOT BE REMOVED: $PublishedZip"
        )
    }

    Write-Host "PORTABLE ENTRYPOINT REJECTED PUBLIC ZIP REMOVAL: PASS"
    throw (
        "PORTABLE ENTRYPOINT SHELL OPEN RELEASE GATE FAILED WITH EXIT CODE " +
        $EntrypointGateExitCode
    )
}

Write-Host "PORTABLE ENTRYPOINT SHELL OPEN RELEASE GATE: PASS"
Write-Host "PORTABLE ENTRYPOINT PUBLIC ZIP RETAINED: PASS"
