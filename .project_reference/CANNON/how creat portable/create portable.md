& {
    $ToolRoot = "E:\kanda_reasoner"

    $Builder = Join-Path `
        $ToolRoot `
        "tools\BUILD_KANDA_REASONER_TOOL_PORTABLE.ps1"

    if (
        -not (
            Test-Path `
                -LiteralPath $Builder `
                -PathType Leaf
        )
    ) {
        throw "OFFICIAL PORTABLE BUILDER NOT FOUND: $Builder"
    }

    Write-Host ""
    Write-Host "KANDA REASONER OFFICIAL PORTABLE BUILD"
    Write-Host "======================================"
    Write-Host ("TOOL ROOT: " + $ToolRoot)
    Write-Host ("BUILDER: " + $Builder)
    Write-Host ""
    Write-Host "A folder-selection window will open."
    Write-Host "Choose the drive/folder where you want the Portable ZIP."
    Write-Host ""

    & $Builder `
        -ToolRoot $ToolRoot `
        -ReplaceExisting

    $BuildExitCode = $LASTEXITCODE

    Write-Host ""
    Write-Host (
        "OFFICIAL PORTABLE BUILD EXIT CODE: " +
        $BuildExitCode
    )

    if ($BuildExitCode -ne 0) {
        throw (
            "KANDA OFFICIAL PORTABLE BUILD FAILED. EXIT CODE: " +
            $BuildExitCode
        )
    }

    Write-Host ""
    Write-Host "KANDA OFFICIAL PORTABLE BUILD: PASS"
}