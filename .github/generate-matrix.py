import sys


def main():

    python_versions_input = sys.argv[1].strip().replace(',', ' ')
    os_types_input = sys.argv[2].strip().replace(',', ' ')

    python_versions = python_versions_input.split()
    os_types = os_types_input.split()

    os_images = set()
    for os_t in os_types:
        if os_t.startswith('linux'):
            os_images.add('ubuntu-latest')
        elif os_t.startswith('osx-arm'):
            os_images.add('macos-14')
        elif os_t.startswith('osx'):
            os_images.add('macos-13')
        elif os_t.startswith('win'):
            os_images.add('windows-2022')
    os_images = list(os_images)

    mpi_mapping = {
        "ubuntu-latest": "mpich",
        "macos-14": "mpich",
        "macos-13": "mpich",
        "windows-2022": "msmpi",
    }

    matrix_list = []

    for os_img in os_images:
        for py_ver in python_versions:
            matrix_list.append({
                "os": os_img,
                "python": py_ver,
                "mpi": mpi_mapping[os_img],
            })

    print(str(matrix_list))


if __name__ == "__main__":
    main()
