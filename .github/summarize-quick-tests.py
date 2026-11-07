#!/usr/bin/env python3
"""Collate timed quick-test results into a Markdown summary."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

TEST_COMBINATIONS = ((1, 1), (1, 2), (2, 1))
OS_ORDER = {"linux": 0, "osx-arm": 1, "win": 2}
MPI_ORDER = {
    "mpich": 0,
    "openmpi": 1,
    "impi_rt": 2,
    "msmpi": 3,
    "impi": 4,
    "default": 5,
}
MATH_ORDER = {"default": 0, "mkl": 1, "openblas": 2}


def load_records(results_dir):
    records = {}
    if not results_dir.exists():
        return records

    for path in sorted(results_dir.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
            continue

        if not isinstance(data, dict) or "status" not in data:
            continue

        try:
            key = (
                str(data.get("os", "")),
                str(data.get("mpi_backend", "")),
                str(data.get("math_backend", "")),
                int(data.get("mpi_ranks", 0)),
                int(data.get("omp_threads", 0)),
            )
        except (TypeError, ValueError) as exc:
            print(f"Warning: invalid metadata in {path}: {exc}", file=sys.stderr)
            continue

        records[key] = data

    return records


def expected_keys(matrix_json):
    keys = {}
    if not matrix_json:
        return keys

    try:
        matrix = json.loads(matrix_json)
    except json.JSONDecodeError as exc:
        print(f"Warning: invalid matrix JSON: {exc}", file=sys.stderr)
        return keys

    entries = matrix.get("include", []) if isinstance(matrix, dict) else matrix
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        os_name = str(entry.get("os", ""))
        mpi = str(entry.get("mpi", ""))
        math = str(entry.get("math", ""))
        for ranks, threads in TEST_COMBINATIONS:
            keys[(os_name, mpi, math, ranks, threads)] = entry

    return keys


def sort_key(key):
    os_name, mpi, math, ranks, threads = key
    return (
        OS_ORDER.get(os_name, 99),
        os_name,
        MPI_ORDER.get(mpi, 99),
        mpi,
        MATH_ORDER.get(math, 99),
        math,
        ranks,
        threads,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("test-results"),
        help="Directory containing result JSON files",
    )
    parser.add_argument(
        "--matrix",
        default="",
        help="JSON matrix used to determine which combinations were expected",
    )
    parser.add_argument(
        "--package-info",
        default="",
        help="Package description shown in the summary",
    )
    args = parser.parse_args()

    records = load_records(args.results_dir)
    expected = expected_keys(args.matrix)
    all_keys = sorted(set(records) | set(expected), key=sort_key)

    rows = []
    for key in all_keys:
        record = records.get(key)
        status = str(record["status"]) if record else "NOT RUN"
        raw_duration = record.get("duration_seconds") if record else None
        try:
            duration = float(raw_duration) if raw_duration is not None else None
        except (TypeError, ValueError):
            duration = None
        rows.append((key, status, duration))

    lines = ["## VeloxChem quick test summary", ""]
    if args.package_info:
        lines += [args.package_info, ""]

    lines += [
        "| OS | MPI backend | Math backend | MPI ranks | OMP threads | Status | Duration (s) |",
        "|---|---|---|---:|---:|---|---:|",
    ]

    for (os_name, mpi, math, ranks, threads), status, duration in rows:
        duration_text = f"{duration:.1f}" if duration is not None else "-"
        lines.append(
            f"| {os_name} | {mpi} | {math} | {ranks} | {threads} | "
            f"{status} | {duration_text} |"
        )

    total_duration = sum(
        duration for _, _, duration in rows if duration is not None
    )
    status_counts = {}
    for _, status, _ in rows:
        status_counts[status] = status_counts.get(status, 0) + 1

    lines += [""]
    lines.append(f"Total time spent in tests: {total_duration:.1f} s")
    lines.append("")
    lines.append(
        "Status counts: "
        + (", ".join(f"{name}={count}" for name, count in sorted(status_counts.items())))
    )

    details = []
    for key, status, _ in rows:
        record = records.get(key)
        if not record or status == "PASS":
            continue
        message = str(record.get("message", "")).strip()
        if not message:
            continue
        details.append((key, status, " ".join(message.splitlines())))

    if details:
        lines += ["", "### Failure details", ""]
        for key, status, message in details:
            os_name, mpi, math, ranks, threads = key
            lines.append(
                f"- {os_name} / {mpi} / {math} / mpi {ranks} / omp {threads}: "
                f"**{status}** — {message}"
            )

    summary = "\n".join(lines) + "\n"
    print(summary)

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as handle:
            handle.write(summary)

    failures = [
        (key, status) for key, status, _ in rows if status != "PASS"
    ]
    if failures:
        print("", file=sys.stderr)
        for key, status in failures:
            os_name, mpi, math, ranks, threads = key
            print(
                f"{status}: {os_name} / {mpi} / {math} / "
                f"mpi {ranks} / omp {threads}",
                file=sys.stderr,
            )
        return 1

    if not rows:
        print("No test combinations were found.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
