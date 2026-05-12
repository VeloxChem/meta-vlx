if (Test-Path Env:_CONDA_BACKUP_KMP_DUPLICATE_LIB_OK) {
    if ($null -ne $env:_CONDA_BACKUP_KMP_DUPLICATE_LIB_OK) {
        $env:KMP_DUPLICATE_LIB_OK = $env:_CONDA_BACKUP_KMP_DUPLICATE_LIB_OK
    } else {
        Remove-Item Env:KMP_DUPLICATE_LIB_OK -ErrorAction SilentlyContinue
    }
    Remove-Item Env:_CONDA_BACKUP_KMP_DUPLICATE_LIB_OK -ErrorAction SilentlyContinue
} else {
    Remove-Item Env:KMP_DUPLICATE_LIB_OK -ErrorAction SilentlyContinue
}
if (Test-Path Env:_CONDA_BACKUP_PYTHONUTF8) {
    if ($null -ne $env:_CONDA_BACKUP_PYTHONUTF8) {
        $env:PYTHONUTF8 = $env:_CONDA_BACKUP_PYTHONUTF8
    } else {
        Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
    }
    Remove-Item Env:_CONDA_BACKUP_PYTHONUTF8 -ErrorAction SilentlyContinue
} else {
    Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
}
