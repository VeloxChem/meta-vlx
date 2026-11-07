#!/usr/bin/env python3
"""Check quick-test result records and fail if any status is unexpected."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Result JSON files")
    args = parser.parse_args()

    allowed = {"PASS"}
    files = [Path(path) for path in args.paths if Path(path).is_file()]
    if not files:
        print("No quick-test result files found.", file=sys.stderr)
        return 1

    failures = []
    for path in files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append((str(path), "UNREADABLE", str(exc)))
            continue

        status = str(record.get("status", "UNKNOWN"))
        name = str(record.get("name", path.name))
        print(f"{status}: {name}")

        if status not in allowed:
            message = str(record.get("message", "")).strip()
            failures.append((name, status, message))

    if failures:
        print("", file=sys.stderr)
        for name, status, message in failures:
            detail = f" ({message})" if message else ""
            print(f"Unexpected result: {status}: {name}{detail}", file=sys.stderr)
        return 1

    print(f"All {len(files)} result record(s) have acceptable statuses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
