import sys

USAGE = "Usage: generate-matrix.py [--skip-mpi] <python_versions> <os_types>"


def main():
    args = sys.argv[1:]
    skip_mpi = "--skip-mpi" in args
    args = [arg for arg in args if arg != "--skip-mpi"]
    if len(args) != 2:
        raise SystemExit(USAGE)

    python_versions_input = args[0].strip().replace(",", " ")
    os_types_input = args[1].strip().replace(",", " ")

    python_versions = python_versions_input.split()
    os_types = os_types_input.split()

    os_images = set()
    for os_t in os_types:
        if os_t.startswith("linux"):
            os_images.add("ubuntu-latest")
        elif os_t.startswith("osx-arm"):
            os_images.add("macos-15")
        elif os_t.startswith("win"):
            os_images.add("windows-2022")
    os_images = list(os_images)

    mpi_mapping = {
        "ubuntu-latest": "mpich",
        "macos-15": "mpich",
        "windows-2022": "msmpi",
    }

    matrix_list = []

    for os_img in os_images:
        for py_ver in python_versions:
            entry = {
                "os": os_img,
                "python": py_ver,
            }
            if not skip_mpi:
                entry["mpi"] = mpi_mapping[os_img]
            matrix_list.append(entry)

    print(str(matrix_list))


if __name__ == "__main__":
    main()
