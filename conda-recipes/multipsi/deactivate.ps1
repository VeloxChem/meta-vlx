$env:KMP_DUPLICATE_LIB_OK="FALSE"
if (Test-Path Env:_OLD_PYTHONUTF8) {
    if ($null -ne $env:_OLD_PYTHONUTF8) {
        $env:PYTHONUTF8 = $env:_OLD_PYTHONUTF8
    } else {
        Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
    }
    Remove-Item Env:_OLD_PYTHONUTF8 -ErrorAction SilentlyContinue
} else {
    Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
}
