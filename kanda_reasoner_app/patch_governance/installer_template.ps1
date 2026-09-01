param(
    [Parameter(Mandatory = $false)]
    [string]$ProjectRoot = "{{PROJECT_ROOT}}"
)

$PROJECT_ROOT = $ProjectRoot
$PATCH_NAME = "{{PATCH_NAME}}"
$PAYLOAD_FOLDER = "{{PAYLOAD_FOLDER}}"

$ErrorActionPreference = "Stop"

function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Resolve-GovernedDestination {
    param(
        [Parameter(Mandatory = $true)][string]$ProjectPath,
        [Parameter(Mandatory = $true)][string]$RelativePath
    )

    if ([string]::IsNullOrWhiteSpace($RelativePath)) {
        throw "Manifest path is empty."
    }
    if ([System.IO.Path]::IsPathRooted($RelativePath)) {
        throw "Manifest path must be project-relative: $RelativePath"
    }
    $Parts = $RelativePath -split '[\\/]'
    if ($Parts.Count -eq 0 -or $Parts -contains ".." -or $Parts -contains ".") {
        throw "Manifest path contains traversal components: $RelativePath"
    }

    $Destination = [System.IO.Path]::GetFullPath((Join-Path $ProjectPath $RelativePath))
    $ProjectPrefix = $ProjectPath.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
    if (-not $Destination.StartsWith(
        $ProjectPrefix,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw "Manifest destination escapes Project root: $RelativePath"
    }
    return $Destination
}

function Ensure-ParentDirectory {
    param([Parameter(Mandatory = $true)][string]$Path)
    $Parent = Split-Path -Parent $Path
    if (-not [string]::IsNullOrWhiteSpace($Parent)) {
        New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    }
}

function Invoke-GovernedRollback {
    param(
        [Parameter(Mandatory = $true)][object[]]$Plan,
        [Parameter(Mandatory = $true)][string]$BackupDir
    )

    Write-Host "ROLLBACK: restoring pre-install state"
    foreach ($Item in @($Plan | Where-Object { $_.State -eq "APPLY" })) {
        $Operation = [string]$Item.Record.operation
        $Destination = [string]$Item.Destination
        $Relative = [string]$Item.Record.path
        $BackupPath = Join-Path $BackupDir $Relative

        if ($Operation -eq "add") {
            if (Test-Path -LiteralPath $Destination -PathType Leaf) {
                Remove-Item -LiteralPath $Destination -Force
            }
            continue
        }

        if (-not (Test-Path -LiteralPath $BackupPath -PathType Leaf)) {
            throw "Rollback backup missing: $Relative"
        }
        Ensure-ParentDirectory -Path $Destination
        Copy-Item -LiteralPath $BackupPath -Destination $Destination -Force

        $Expected = ([string]$Item.Record.baseline_sha256).ToLowerInvariant()
        $Observed = Get-Sha256Lower -Path $Destination
        if ($Observed -ne $Expected) {
            throw "Rollback hash mismatch: $Relative"
        }
    }
    Write-Host "ROLLBACK: verified"
}

try {
    $ProjectPath = (Resolve-Path -LiteralPath $PROJECT_ROOT).Path
    $ProjectName = Split-Path $ProjectPath -Leaf
    $DriveRoot = [System.IO.Path]::GetPathRoot($ProjectPath)
    $WorkDir = Join-Path $DriveRoot ($ProjectName + "_delete_after_daily_work")
    $RootPatchZip = Join-Path $DriveRoot ($PATCH_NAME + ".zip")
    $WorkPatchZip = Join-Path $WorkDir ($PATCH_NAME + ".zip")
    $ExtractDir = Join-Path $WorkDir ($PATCH_NAME + "_extract")
    $BackupDir = Join-Path $WorkDir ($PATCH_NAME + "_backup")

    if (-not (Test-Path -LiteralPath $WorkDir -PathType Container)) {
        New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null
    }

    if (Test-Path -LiteralPath $RootPatchZip -PathType Leaf) {
        Copy-Item -LiteralPath $RootPatchZip -Destination $WorkPatchZip -Force
        if (Test-Path -LiteralPath $WorkPatchZip -PathType Leaf) {
            Remove-Item -LiteralPath $RootPatchZip -Force
        }
    }
    elseif (-not (Test-Path -LiteralPath $WorkPatchZip -PathType Leaf)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path -LiteralPath $ExtractDir) {
        Remove-Item -LiteralPath $ExtractDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $ExtractDir -Force | Out-Null
    Expand-Archive -LiteralPath $WorkPatchZip -DestinationPath $ExtractDir -Force

    $PayloadDir = Join-Path $ExtractDir $PAYLOAD_FOLDER
    if (-not (Test-Path -LiteralPath $PayloadDir -PathType Container)) {
        throw "Patch payload folder was not found inside the staged ZIP."
    }

    $ManifestPath = Join-Path $ExtractDir "INSTALL_MANIFEST.json"
    if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
        throw "INSTALL_MANIFEST.json was not found in the staged patch."
    }
    $Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    if ([string]$Manifest.patch_name -ne $PATCH_NAME) {
        throw "INSTALL_MANIFEST patch_name does not match the staged patch."
    }
    $Records = @($Manifest.files)
    if ($Records.Count -eq 0) {
        throw "INSTALL_MANIFEST files list is empty."
    }

    $Plan = @()

    # Complete preflight for every operation before any Project source mutation.
    foreach ($Record in $Records) {
        $Relative = [string]$Record.path
        $Operation = ([string]$Record.operation).ToLowerInvariant()
        $Baseline = ([string]$Record.baseline_sha256).ToLowerInvariant()
        $Installed = ([string]$Record.installed_sha256).ToLowerInvariant()
        $Destination = Resolve-GovernedDestination `
            -ProjectPath $ProjectPath `
            -RelativePath $Relative
        $PayloadPath = Join-Path $PayloadDir $Relative

        if ($Operation -notin @("add", "replace", "delete")) {
            throw "Unsupported install operation: $Operation for $Relative"
        }
        if ($Installed -notmatch '^[0-9a-f]{64}$') {
            throw "Invalid installed_sha256 for $Relative"
        }
        if ($Operation -eq "add" -and -not [string]::IsNullOrWhiteSpace($Baseline)) {
            throw "New file must not declare baseline_sha256: $Relative"
        }
        if ($Operation -in @("replace", "delete") -and $Baseline -notmatch '^[0-9a-f]{64}$') {
            throw "Invalid baseline_sha256 for $Relative"
        }

        if ($Operation -in @("add", "replace")) {
            if (-not (Test-Path -LiteralPath $PayloadPath -PathType Leaf)) {
                throw "Payload file missing: $Relative"
            }
            $PayloadHash = Get-Sha256Lower -Path $PayloadPath
            if ($PayloadHash -ne $Installed) {
                throw "Payload installed hash mismatch: $Relative"
            }
        }

        $Exists = Test-Path -LiteralPath $Destination -PathType Leaf
        $State = "APPLY"
        if ($Operation -eq "add") {
            if ($Exists) {
                $Current = Get-Sha256Lower -Path $Destination
                if ($Current -eq $Installed) {
                    $State = "CURRENT"
                }
                else {
                    throw "Baseline mismatch: $Relative expected ABSENT or already-current installed_sha256."
                }
            }
        }
        elseif ($Operation -eq "replace") {
            if (-not $Exists) {
                throw "Baseline mismatch: $Relative expected existing baseline file."
            }
            $Current = Get-Sha256Lower -Path $Destination
            if ($Current -eq $Installed) {
                $State = "CURRENT"
            }
            elseif ($Current -ne $Baseline) {
                throw "Baseline mismatch: $Relative has unknown predecessor hash $Current"
            }
        }
        else {
            if (-not $Exists) {
                $State = "CURRENT"
            }
            else {
                $Current = Get-Sha256Lower -Path $Destination
                if ($Current -ne $Baseline) {
                    throw "Baseline mismatch: $Relative has unknown predecessor hash $Current"
                }
            }
        }

        $Plan += [PSCustomObject]@{
            Record = $Record
            Destination = $Destination
            PayloadPath = $PayloadPath
            State = $State
        }
    }

    if (Test-Path -LiteralPath $BackupDir) {
        Remove-Item -LiteralPath $BackupDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

    foreach ($Item in @($Plan | Where-Object { $_.State -eq "APPLY" })) {
        $Operation = ([string]$Item.Record.operation).ToLowerInvariant()
        if ($Operation -in @("replace", "delete")) {
            $BackupPath = Join-Path $BackupDir ([string]$Item.Record.path)
            Ensure-ParentDirectory -Path $BackupPath
            Copy-Item -LiteralPath $Item.Destination -Destination $BackupPath -Force
            $BackupHash = Get-Sha256Lower -Path $BackupPath
            $ExpectedBaseline = ([string]$Item.Record.baseline_sha256).ToLowerInvariant()
            if ($BackupHash -ne $ExpectedBaseline) {
                throw "Backup baseline hash mismatch: $($Item.Record.path)"
            }
        }
    }

    try {
        foreach ($Item in @($Plan | Where-Object { $_.State -eq "APPLY" })) {
            $Operation = ([string]$Item.Record.operation).ToLowerInvariant()
            if ($Operation -eq "delete") {
                Remove-Item -LiteralPath $Item.Destination -Force
            }
            else {
                Ensure-ParentDirectory -Path $Item.Destination
                Copy-Item -LiteralPath $Item.PayloadPath -Destination $Item.Destination -Force
            }
        }

        foreach ($Item in $Plan) {
            $Operation = ([string]$Item.Record.operation).ToLowerInvariant()
            $Relative = [string]$Item.Record.path
            if ($Operation -eq "delete") {
                if (Test-Path -LiteralPath $Item.Destination -PathType Leaf) {
                    throw "Installed delete verification failed: $Relative"
                }
                continue
            }
            if (-not (Test-Path -LiteralPath $Item.Destination -PathType Leaf)) {
                throw "Installed file missing: $Relative"
            }
            $Observed = Get-Sha256Lower -Path $Item.Destination
            $Expected = ([string]$Item.Record.installed_sha256).ToLowerInvariant()
            if ($Observed -ne $Expected) {
                throw "Installed hash mismatch: $Relative"
            }
        }
    }
    catch {
        $InstallFailure = $_
        Invoke-GovernedRollback -Plan $Plan -BackupDir $BackupDir
        throw $InstallFailure
    }

    Write-Host ""
    Write-Host "INSTALL OK. Press Enter twice to clear terminal."
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
    $global:LASTEXITCODE = 0
}
catch {
    Write-Host ""
    Write-Host "INSTALL ERROR. Review the error below before clearing the terminal."
    Write-Host $_.Exception.Message
    if ($_.ScriptStackTrace) {
        Write-Host $_.ScriptStackTrace
    }
    Write-Host ""
    Read-Host "Press Enter to clear terminal"
    Read-Host "Press Enter again to clear"
    Clear-Host
    $global:LASTEXITCODE = 1
    return
}
