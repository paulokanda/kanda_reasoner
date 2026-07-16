


1. Create dated checkpoint ZIPs

Run before every new correction phase:


cd E:\

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$src = "E:\developer_tools"
$dst = "E:\developer_tools_CHECKPOINT_$stamp.zip"

Compress-Archive -Path $src -DestinationPath $dst -Force

Get-FileHash -Path $dst -Algorithm SHA256 | Format-List




2. Make a small checkpoint note:

cd E:\

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$note = "E:\developer_tools_CHECKPOINT_$stamp.txt"

@"
Checkpoint: $stamp
Project: E:\developer_tools
Status: Tab 1 architecture validation reached 0 errors.
Last completed pass: Pass 009.
Backup type: ZIP archive.
"@ | Set-Content -Path $note -Encoding UTF8




4. Restore from ZIP if anything breaks

Use this only if you need rollback:

cd E:\

Rename-Item "E:\developer_tools" "developer_tools_BROKEN_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

Expand-Archive -Path "E:\developer_tools_ZERO_ERRORS_checkpoint.zip" -DestinationPath "E:\" -Force