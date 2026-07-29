Set-Location E:\kanda_reasoner

$SOURCE = "E:\kanda_reasoner\dist\kanda_reasoner"
$STAGE_PARENT = "E:\kanda_reasoner_release_stage"
$STAGE_APP = "$STAGE_PARENT\kanda_reasoner"
$ZIP = "E:\kanda_reasoner\KandaReasoner-Windows-Portable.zip"
$DESKTOP_ZIP = "$env:USERPROFILE\Desktop\KandaReasoner-Windows-Portable.zip"

Write-Host "=================================================="
Write-Host "Building GUI-Only Executable (--noconsole)..."
Write-Host "=================================================="

# Ensure PyInstaller builds the GUI executable without a console terminal window.
# Note: If you use a .spec file instead, ensure `console=False` is set in the EXE() block.
pyinstaller `
    --noconsole `
    --noconfirm `
    --onedir `
    --name "kanda_reasoner" `
    --distpath "E:\kanda_reasoner\dist" `
    --workpath "E:\kanda_reasoner\build" `
    E:\kanda_reasoner\main.py

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed with exit code $LASTEXITCODE."
}

# Confirm the latest GUI-only portable build exists.
if (-not (Test-Path "$SOURCE\kanda_reasoner.exe")) {
    throw "Portable executable not found: $SOURCE\kanda_reasoner.exe"
}

if (-not (Test-Path "$SOURCE\_internal")) {
    throw "Portable _internal folder not found: $SOURCE\_internal"
}

Write-Host "`nPreparing staging area..."

# Remove previous staging folder and ZIP files.
Remove-Item `
    -LiteralPath $STAGE_PARENT `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

Remove-Item `
    -LiteralPath $ZIP `
    -Force `
    -ErrorAction SilentlyContinue

Remove-Item `
    -LiteralPath $DESKTOP_ZIP `
    -Force `
    -ErrorAction SilentlyContinue

# Create a clean staging area.
New-Item `
    -ItemType Directory `
    -Path $STAGE_PARENT `
    -Force |
    Out-Null

# Copy the complete portable application into staging.
Copy-Item `
    -LiteralPath $SOURCE `
    -Destination $STAGE_PARENT `
    -Recurse `
    -Force

# Remove the known non-runtime directory containing paths that are too long
# for reliable Windows Explorer ZIP handling.
$NON_RUNTIME_LONG_PATH_DOCS = Join-Path `
    $STAGE_APP `
    "_internal\kanda_reasoner_app\routing_signal_scorer\mlrt_non_runtime_candidate_reliability"

if (Test-Path $NON_RUNTIME_LONG_PATH_DOCS) {
    Remove-Item `
        -LiteralPath $NON_RUNTIME_LONG_PATH_DOCS `
        -Recurse `
        -Force
}

# Confirm the staged application still contains its required files.
if (-not (Test-Path "$STAGE_APP\kanda_reasoner.exe")) {
    throw "Staged executable is missing."
}

if (-not (Test-Path "$STAGE_APP\_internal")) {
    throw "Staged _internal folder is missing."
}

# Reject accidental project-support folders inside the portable package.
$UNEXPECTED_SUPPORT_FOLDERS = @(
    Get-ChildItem `
        -LiteralPath $STAGE_APP `
        -Directory `
        -Recurse `
        -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -like "*_show_project_to_AI" -or
            $_.Name -like "*_delete_after_daily_work"
        }
)

if ($UNEXPECTED_SUPPORT_FOLDERS.Count -gt 0) {
    $UNEXPECTED_SUPPORT_FOLDERS |
        Select-Object FullName |
        Format-Table -AutoSize

    throw "Unexpected project-support folders exist inside the portable package."
}

# Measure internal archive paths.
$PATH_RESULTS = Get-ChildItem `
    -LiteralPath $STAGE_APP `
    -Recurse `
    -Force |
    ForEach-Object {
        $relative = $_.FullName.Substring(
            $STAGE_PARENT.Length + 1
        ).Replace("\", "/")

        [PSCustomObject]@{
            Bytes = [System.Text.Encoding]::UTF8.GetByteCount($relative)
            Path  = $relative
        }
    }

$MAX_PATH_BYTES = (
    $PATH_RESULTS |
    Measure-Object Bytes -Maximum
).Maximum

Write-Host "`nLongest paths remaining in release:"

$PATH_RESULTS |
    Sort-Object Bytes -Descending |
    Select-Object -First 5 |
    Format-Table -AutoSize

Write-Host "Maximum archive path length:" $MAX_PATH_BYTES

if ($MAX_PATH_BYTES -ge 260) {
    throw "Release still contains an archive path of 260 bytes or more."
}

# Create the Windows Explorer-compatible ZIP.
Add-Type `
    -AssemblyName System.IO.Compression.FileSystem

[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $STAGE_APP,
    $ZIP,
    [System.IO.Compression.CompressionLevel]::Optimal,
    $true
)

# Copy the final ZIP to the Desktop for GitHub upload.
Copy-Item `
    -LiteralPath $ZIP `
    -Destination $DESKTOP_ZIP `
    -Force

# Validate the ZIP using Windows Explorer's own ZIP parser.
$SHELL = New-Object `
    -ComObject Shell.Application

$ZIP_NAMESPACE = $SHELL.NameSpace($DESKTOP_ZIP)

if ($null -eq $ZIP_NAMESPACE) {
    throw "WINDOWS EXPLORER ZIP CHECK: FAIL"
}

$TOP_LEVEL_COUNT = $ZIP_NAMESPACE.Items().Count

if ($TOP_LEVEL_COUNT -ne 1) {
    throw "ZIP must contain exactly one top-level folder. Found: $TOP_LEVEL_COUNT"
}

Write-Host "`nWINDOWS EXPLORER ZIP CHECK: PASS"
Write-Host "Top-level entries:" $TOP_LEVEL_COUNT

# Show the final ZIP details.
Write-Host "`nRelease ZIP:"

Get-Item `
    -LiteralPath $DESKTOP_ZIP |
    Select-Object FullName, Length, LastWriteTime

Write-Host "`nSHA-256:"

Get-FileHash `
    -LiteralPath $DESKTOP_ZIP `
    -Algorithm SHA256

Write-Host "`nArchive created successfully."
Write-Host "GitHub upload file:"
Write-Host $DESKTOP_ZIP