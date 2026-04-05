#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path

from build_number_helper import (
    coerce_files,
    filter_files_by_version,
    get_build_number,
    load_payload,
    load_payload_from_args,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get the next conda build number from uploaded package files."
    )
    parser.add_argument(
        "--namespace",
        default="veloxchem",
        help="package namespace",
    )
    parser.add_argument("--package", default="veloxchem", help="package name")
    parser.add_argument("--version", required=True, help="package version")
    parser.add_argument(
        "--json-file",
        type=Path,
        help="read package metadata from a local JSON file",
    )
    return parser.parse_args()

def write_output(next_build_number):
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        return

    with open(github_output, "a", encoding="utf-8") as handle:
        handle.write(f"build_number={next_build_number}\n")


def main():
    args = parse_args()
    if args.json_file:
        payload = load_payload_from_args(args)
    else:
        payload = load_payload(args.namespace, args.package)
    file_records = filter_files_by_version(coerce_files(payload), args.version)

    build_numbers = []
    for file_record in file_records:
        build_number = get_build_number(file_record)
        if build_number is not None:
            build_numbers.append(build_number)

    max_build_number = max(build_numbers) if build_numbers else -1
    next_build_number = max_build_number + 1

    print(next_build_number)
    write_output(next_build_number)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
