#!/usr/bin/env python3
"""Print runtime, CPU, NumPy, and BLAS diagnostics for quick tests."""

from __future__ import annotations

import ctypes
import ctypes.util
import glob
import os
import platform
import subprocess
import sys
import sysconfig
from pathlib import Path


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001 - diagnostics must not fail the job
        return f"<failed: {exc}>"
    output = (result.stdout or result.stderr).strip()
    return output or "<no output>"


def print_cpu_info():
    print("--- CPU information ---")
    print("platform.machine():", platform.machine())
    print("platform.processor():", platform.processor())
    print("os.cpu_count():", os.cpu_count())

    system = platform.system()
    if system == "Linux":
        cpuinfo = Path("/proc/cpuinfo")
        if cpuinfo.exists():
            text = cpuinfo.read_text(errors="replace")
            model = next(
                (
                    line.split(":", 1)[1].strip()
                    for line in text.splitlines()
                    if line.lower().startswith("model name")
                ),
                "unknown",
            )
            flags = next(
                (
                    line.split(":", 1)[1].strip()
                    for line in text.splitlines()
                    if line.lower().startswith("flags")
                ),
                "",
            )
            avx512_flags = sorted(
                flag for flag in flags.split() if flag.startswith("avx512")
            )
            print("Linux CPU model:", model)
            print("Linux AVX-512 flags:", " ".join(avx512_flags) or "<none>")
    elif system == "Darwin":
        print(
            "macOS CPU brand:",
            run_command(["sysctl", "-n", "machdep.cpu.brand_string"]),
        )
        print("macOS hardware model:", run_command(["sysctl", "-n", "hw.model"]))
    elif system == "Windows":
        powershell = (
            "Get-CimInstance Win32_Processor | "
            "ForEach-Object { '{0} | cores={1} | logical={2}' -f "
            "$_.Name,$_.NumberOfCores,$_.NumberOfLogicalProcessors }"
        )
        print(
            "Windows CPU:",
            run_command(["powershell", "-NoProfile", "-Command", powershell]),
        )
        print(
            "Windows PROCESSOR_IDENTIFIER:",
            os.environ.get("PROCESSOR_IDENTIFIER", ""),
        )


def get_numpy_cpu_features():
    try:
        from numpy._core._multiarray_umath import __cpu_features__ as features
    except ImportError:
        from numpy.core._multiarray_umath import __cpu_features__ as features
    return features


def print_numpy_info():
    import numpy
    import scipy

    print("--- Python / NumPy ---")
    print("Python:", sys.version.replace("\n", " "))
    print("NumPy:", numpy.__version__)
    print("SciPy:", scipy.__version__)

    features = get_numpy_cpu_features()
    print("NumPy CPU features:")
    for name in sorted(features):
        if (
            name.startswith("AVX512")
            or name in ("AVX", "AVX2", "FMA3", "SSE42")
        ):
            print(f"  {name}: {features[name]}")

    print("--- NumPy configuration ---")
    numpy.show_config()


def find_openblas_library(prefix):
    prefix = Path(prefix)
    patterns = []

    if platform.system() == "Windows":
        patterns += [
            prefix / "Library" / "bin" / "libopenblas*.dll",
            prefix / "Library" / "bin" / "openblas*.dll",
        ]
    elif platform.system() == "Darwin":
        patterns += [prefix / "lib" / "libopenblas*.dylib"]
    else:
        patterns += [
            prefix / "lib" / "libopenblas*.so",
            prefix / "lib" / "libopenblas*.so.*",
        ]

    try:
        site_packages = Path(sysconfig.get_paths()["purelib"])
        patterns += [site_packages.parent / "numpy.libs" / "libopenblas*"]
    except Exception:  # noqa: BLE001 - diagnostics must not fail the job
        pass

    candidates = []
    for pattern in patterns:
        candidates.extend(sorted(glob.glob(str(pattern))))

    if candidates:
        return candidates[0]

    found = ctypes.util.find_library("openblas")
    return found or ""


def print_openblas_info():
    print("--- OpenBLAS ---")
    prefix = os.environ.get("CONDA_PREFIX", "")
    library = find_openblas_library(prefix)
    if not library:
        print("OpenBLAS library: <not found>")
        return

    print("OpenBLAS library:", library)

    if os.name == "nt" and prefix:
        try:
            os.add_dll_directory(str(Path(prefix) / "Library" / "bin"))
        except OSError:
            pass

    try:
        lib = ctypes.CDLL(library)
    except OSError as exc:
        print("Could not load OpenBLAS library:", exc)
        return

    for function_name in ("openblas_get_corename", "openblas_get_config"):
        try:
            function = getattr(lib, function_name)
            function.restype = ctypes.c_char_p
            value = function()
            if isinstance(value, bytes):
                value = value.decode(errors="replace")
            print(f"OpenBLAS {function_name}:", value)
        except AttributeError:
            print(f"OpenBLAS {function_name}: <not available>")


def print_blas_files():
    print("--- BLAS/LAPACK/MKL files ---")
    prefix = Path(os.environ.get("CONDA_PREFIX", ""))
    try:
        site_packages = Path(sysconfig.get_paths()["purelib"])
    except Exception:  # noqa: BLE001 - diagnostics must not fail the job
        site_packages = prefix

    search_dirs = [
        prefix / "Library" / "bin",
        prefix / "lib",
        site_packages.parent / "numpy.libs",
        site_packages / "numpy" / ".libs",
    ]

    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for path in sorted(search_dir.iterdir()):
            lower_name = path.name.lower()
            if any(token in lower_name for token in ("blas", "lapack", "mkl")):
                print(path)


def main():
    print("Platform:", platform.platform())
    print("Conda prefix:", os.environ.get("CONDA_PREFIX", ""))
    print("UCX_TLS:", os.environ.get("UCX_TLS", ""))
    print("FI_PROVIDER:", os.environ.get("FI_PROVIDER", ""))
    print("OPENBLAS_CORETYPE:", os.environ.get("OPENBLAS_CORETYPE", ""))
    print("OPENBLAS_NUM_THREADS:", os.environ.get("OPENBLAS_NUM_THREADS", ""))

    print_cpu_info()
    print_numpy_info()
    print_openblas_info()
    print_blas_files()


if __name__ == "__main__":
    main()
