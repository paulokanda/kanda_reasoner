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
    -AssemblyName System.IO.Compression

Add-Type `
    -AssemblyName System.IO.Compression.FileSystem

Write-Output "ZIP_COMPRESSION_ASSEMBLY_PRELOAD=PASS"

$SourceDirectory = (Resolve-Path -LiteralPath $SourceDirectory).Path
$SourceInfo = Get-Item -LiteralPath $SourceDirectory
$SourcePrefix = $SourceInfo.FullName.TrimEnd([char[]]"\/") + [System.IO.Path]::DirectorySeparatorChar
$TopLevelName = $SourceInfo.Name

if ([string]::IsNullOrWhiteSpace($TopLevelName)) {
    throw "Portable stage folder has no top-level name."
}

if (Test-Path -LiteralPath $DestinationZip) {
    Remove-Item `
        -LiteralPath $DestinationZip `
        -Force
}

$Archive = [System.IO.Compression.ZipFile]::Open(
    $DestinationZip,
    [System.IO.Compression.ZipArchiveMode]::Create
)

try {
    $Files = @(
        Get-ChildItem `
            -LiteralPath $SourceDirectory `
            -Recurse `
            -Force `
            -File |
        Sort-Object -Property FullName
    )

    foreach ($File in $Files) {
        $RelativePath = $File.FullName.Substring($SourcePrefix.Length)
        $RelativePath = $RelativePath.Replace([char]92, [char]47)
        $EntryName = $TopLevelName + "/" + $RelativePath

        if ($EntryName.Contains([char]92)) {
            throw "ZIP member normalization retained a backslash: $EntryName"
        }

        $Entry = $Archive.CreateEntry(
            $EntryName,
            [System.IO.Compression.CompressionLevel]::Optimal
        )
        $InputStream = [System.IO.File]::OpenRead($File.FullName)

        try {
            $OutputStream = $Entry.Open()

            try {
                $InputStream.CopyTo($OutputStream)
            }
            finally {
                $OutputStream.Dispose()
            }
        }
        finally {
            $InputStream.Dispose()
        }
    }
}
finally {
    $Archive.Dispose()
}

$ArchiveCheck = [System.IO.Compression.ZipFile]::OpenRead($DestinationZip)

try {
    foreach ($Entry in $ArchiveCheck.Entries) {
        if ($Entry.FullName.Contains([char]92)) {
            throw "ZIP member uses a backslash: $($Entry.FullName)"
        }
    }
}
finally {
    $ArchiveCheck.Dispose()
}

Write-Output "ZIP_MEMBER_SEPARATOR_CONTRACT=PASS"

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
