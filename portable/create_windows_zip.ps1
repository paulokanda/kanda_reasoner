param(
    [Parameter(Mandatory = $true)]
    [string]$SourceDirectory,

    [Parameter(Mandatory = $true)]
    [string]$DestinationZip
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SourceDirectory -PathType Container)) {
    throw "Portable stage folder not found: $SourceDirectory"
}

Add-Type `
    -AssemblyName System.IO.Compression.FileSystem

if (Test-Path -LiteralPath $DestinationZip) {
    Remove-Item `
        -LiteralPath $DestinationZip `
        -Force
}

[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $SourceDirectory,
    $DestinationZip,
    [System.IO.Compression.CompressionLevel]::Optimal,
    $true
)

$Shell = New-Object `
    -ComObject Shell.Application

$Namespace = $null

for ($Attempt = 0; $Attempt -lt 30; $Attempt++) {
    $Namespace = $Shell.NameSpace($DestinationZip)

    if ($null -ne $Namespace) {
        break
    }

    Start-Sleep -Milliseconds 500
}

if ($null -eq $Namespace) {
    throw "WINDOWS EXPLORER ZIP CHECK: FAIL"
}

Write-Output "WINDOWS_EXPLORER_ZIP_CHECK=PASS"
Write-Output (
    "TOP_LEVEL_ENTRIES=" +
    $Namespace.Items().Count
)
