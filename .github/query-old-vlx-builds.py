#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path

from build_number_helper import (
    coerce_files,
    filter_files_by_version,
    get_build_number,
    load_payload_from_args,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "List uploaded package files whose build numbers are older than the "
            "latest distinct build numbers kept as recent."
        )
    )
    parser.add_argument(
        "--namespace",
        default="veloxchem",
        help="package namespace",
    )
    parser.add_argument("--package", default="veloxchem", help="package name")
    parser.add_argument("--version", required=True, help="package version")
    parser.add_argument(
        "--keep-builds",
        type=int,
        default=10,
        help="treat this many latest distinct build numbers as recent",
    )
    parser.add_argument(
        "--json-file",
        type=Path,
        help="read package metadata from a local JSON file",
    )
    return parser.parse_args()


def get_display_name(file_record):
    for key in ("full_name", "basename", "fn", "filename"):
        value = file_record.get(key)
        if value:
            return str(value)

    attrs = file_record.get("attrs")
    if isinstance(attrs, dict):
        for key in ("basename", "filename"):
            value = attrs.get(key)
            if value:
                return str(value)

    distribution = file_record.get("distribution")
    if isinstance(distribution, dict):
        for key in ("basename", "full_name"):
            value = distribution.get(key)
            if value:
                return str(value)

    return "<unknown>"


def get_package_ref(file_record):
    package_ref = get_display_name(file_record)
    if package_ref == "<unknown>":
        raise RuntimeError("Unable to determine exact package reference from file record.")

    if package_ref.count("/") < 3:
        raise RuntimeError(
            f"Package reference does not look like a full Anaconda package path: {package_ref}"
        )

    return package_ref


def build_summary_lines(
    total_files,
    total_build_numbers,
    recent_build_numbers,
    selected,
):
    lines = [
        f"Total uploaded files inspected: {total_files}",
        f"Distinct build numbers found: {total_build_numbers}",
        f"Recent build numbers kept: {', '.join(str(num) for num in recent_build_numbers) if recent_build_numbers else '<none>'}",
        f"Old files outside the latest build numbers: {len(selected)}",
    ]

    if selected:
        lines.append("")
        lines.append("Old files selected:")
        for item in selected:
            lines.append(f"- {item['name']} | build {item['build_number']}")

    return lines


def write_outputs(match_count, package_refs):
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as handle:
            handle.write(f"old_file_count={match_count}\n")
            handle.write(f"package_refs={json.dumps(package_refs)}\n")


def write_step_summary(lines):
    github_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not github_summary:
        return

    with open(github_summary, "a", encoding="utf-8") as handle:
        handle.write("## VeloxChem Build Audit\n\n")
        for line in lines:
            handle.write(f"{line}\n")


def main():
    args = parse_args()
    payload = load_payload_from_args(args)
    file_records = filter_files_by_version(coerce_files(payload), args.version)

    files_with_build_numbers = []
    skipped_files = 0

    for file_record in file_records:
        build_number = get_build_number(file_record)
        if build_number is None:
            skipped_files += 1
            continue

        files_with_build_numbers.append(
            {
                "name": get_display_name(file_record),
                "package_ref": get_package_ref(file_record),
                "build_number": build_number,
            }
        )

    if not files_with_build_numbers:
        raise RuntimeError(
            f"No uploaded package files with parseable build numbers were found for version {args.version}."
        )

    distinct_build_numbers = sorted(
        {item["build_number"] for item in files_with_build_numbers},
        reverse=True,
    )
    recent_build_numbers = distinct_build_numbers[: args.keep_builds]
    recent_build_number_set = set(recent_build_numbers)

    selected = [
        item for item in files_with_build_numbers if item["build_number"] not in recent_build_number_set
    ]
    selected.sort(key=lambda item: (item["build_number"], item["name"]), reverse=True)
    package_refs = [item["package_ref"] for item in selected]

    summary_lines = build_summary_lines(
        total_files=len(files_with_build_numbers),
        total_build_numbers=len(distinct_build_numbers),
        recent_build_numbers=recent_build_numbers,
        selected=selected,
    )

    if skipped_files:
        summary_lines.append("")
        summary_lines.append(f"Skipped files without parseable build numbers: {skipped_files}")

    for line in summary_lines:
        print(line)

    write_outputs(len(selected), package_refs)
    write_step_summary(summary_lines)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
