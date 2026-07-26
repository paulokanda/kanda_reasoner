$PROJECT_ROOT = "{{PROJECT_ROOT}}"
$PATCH_NAME = "{{PATCH_NAME}}"
$PAYLOAD_FOLDER = "{{PAYLOAD_FOLDER}}"

$ErrorActionPreference = "Stop"

try {
    $ProjectPath = (Resolve-Path $PROJECT_ROOT).Path
    $ProjectName = Split-Path $ProjectPath -Leaf
    $DriveRoot = [System.IO.Path]::GetPathRoot($ProjectPath)
    $WorkDir = Join-Path $DriveRoot ($ProjectName + "_delete_after_daily_work")
    $RootPatchZip = Join-Path $DriveRoot ($PATCH_NAME + ".zip")
    $WorkPatchZip = Join-Path $WorkDir ($PATCH_NAME + ".zip")
    $ExtractDir = Join-Path $WorkDir ($PATCH_NAME + "_extract")

    if (-not (Test-Path $WorkDir)) {
        New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null
    }

    if (Test-Path $RootPatchZip) {
        Copy-Item -Path $RootPatchZip -Destination $WorkPatchZip -Force
        if (Test-Path $WorkPatchZip) {
            Remove-Item -Path $RootPatchZip -Force
        }
    } elseif (-not (Test-Path $WorkPatchZip)) {
        throw "zip is not in root of drive:\ where project is"
    }

    if (Test-Path $ExtractDir) {
        Remove-Item -Path $ExtractDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $ExtractDir -Force | Out-Null
    Expand-Archive -Path $WorkPatchZip -DestinationPath $ExtractDir -Force

    $PayloadDir = Join-Path $ExtractDir $PAYLOAD_FOLDER
    if (-not (Test-Path $PayloadDir)) {
        throw "Patch payload folder was not found inside the staged ZIP."
    }

    Copy-Item -Path (Join-Path $PayloadDir "*") -Destination $ProjectPath -Recurse -Force

    Write-Host ""
    Write-Host "INSTALL OK. Terminal will clear in 2 seconds..."
    Start-Sleep -Seconds 2
    Clear-Host
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
