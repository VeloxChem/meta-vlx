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
