#!/usr/bin/env python3
"""Run one command with a wall-clock timeout and record the outcome."""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Human-readable test name")
    parser.add_argument("--timeout", type=float, required=True, help="Timeout in seconds")
    parser.add_argument("--result-dir", default="test-results")
    parser.add_argument(
        "--metadata",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Extra metadata stored in the result record (repeatable)",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser.parse_args()


def terminate_process_tree(process):
    """Terminate a process and all of its children."""

    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return

    try:
        pgid = os.getpgid(process.pid)
    except ProcessLookupError:
        return

    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return

    # Give the launcher a chance to clean up, then make sure that any
    # remaining children (for example stragglers from an MPI launcher) are
    # also gone. Otherwise they can keep the output pipe open and make the
    # workflow hang even after the timeout has fired.
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass

    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def main():
    args = parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("No command specified.", file=sys.stderr)
        return 2

    metadata = {}
    for item in args.metadata:
        key, separator, value = item.partition("=")
        if not separator:
            print(f"Ignoring malformed metadata: {item}", file=sys.stderr)
            continue
        metadata[key] = value

    popen_kwargs = {}
    if os.name == "nt":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True

    started = time.monotonic()
    timed_out = False
    return_code = None
    output = ""

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            **popen_kwargs,
        )
        try:
            output, _ = process.communicate(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            print(
                f"::warning::{args.name} exceeded {args.timeout:g}s; "
                "killing process tree",
                flush=True,
            )
            terminate_process_tree(process)
            try:
                output, _ = process.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                try:
                    output, _ = process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    output = ""
        return_code = process.returncode
    except Exception as exc:  # noqa: BLE001 - report launch errors as failures
        output = f"Failed to run command: {exc}\n"
        return_code = -1

    elapsed = time.monotonic() - started

    if timed_out:
        status = "HANG"
    elif return_code == 0:
        status = "PASS"
    else:
        status = "FAIL"

    if output:
        sys.stdout.write(output)
        if not output.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()

    print(
        f"[{status}] {args.name}: {elapsed:.1f}s "
        f"(exit code {return_code}, timeout {args.timeout:g}s)",
        flush=True,
    )

    result = {
        "name": args.name,
        "status": status,
        "duration_seconds": round(elapsed, 3),
        "exit_code": return_code,
        "timeout_seconds": args.timeout,
        **metadata,
    }

    result_dir = Path(args.result_dir)
    result_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(
        character if character.isalnum() or character in "-_." else "_"
        for character in args.name
    )
    (result_dir / f"{safe_name}.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as handle:
            handle.write(f"| {args.name} | {status} | {elapsed:.1f} |\n")

    if status == "PASS":
        return 0
    if status == "HANG":
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
