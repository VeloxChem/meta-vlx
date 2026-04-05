#!/usr/bin/env python3

import json
import urllib.error
import urllib.request


def fetch_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "meta-vlx-build-helper",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def load_payload(namespace, package):
    endpoints = [
        f"https://api.anaconda.org/package/{namespace}/{package}/files",
        f"https://api.anaconda.org/package/{namespace}/{package}",
    ]

    errors = []
    for endpoint in endpoints:
        try:
            return fetch_json(endpoint)
        except urllib.error.HTTPError as exc:
            errors.append(f"{endpoint} -> HTTP {exc.code}")
        except urllib.error.URLError as exc:
            errors.append(f"{endpoint} -> {exc.reason}")

    raise RuntimeError(
        "Unable to fetch package metadata from anaconda.org:\n" + "\n".join(errors)
    )


def load_payload_from_args(args):
    if args.json_file:
        with args.json_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    return load_payload(args.namespace, args.package)


def coerce_files(payload):
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ("files", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value

    raise RuntimeError("Unexpected response format.")


def parse_int(value):
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None
    return None


def get_build_number(file_record):
    candidates = [file_record]

    attrs = file_record.get("attrs")
    if isinstance(attrs, dict):
        candidates.append(attrs)

    distribution = file_record.get("distribution")
    if isinstance(distribution, dict):
        candidates.append(distribution)
        distribution_attrs = distribution.get("attrs")
        if isinstance(distribution_attrs, dict):
            candidates.append(distribution_attrs)

    for candidate in candidates:
        for key in ("build_number", "build_no", "build"):
            parsed = parse_int(candidate.get(key))
            if parsed is not None:
                return parsed

    return None


def get_package_version(file_record):
    candidates = [file_record]

    attrs = file_record.get("attrs")
    if isinstance(attrs, dict):
        candidates.append(attrs)

    distribution = file_record.get("distribution")
    if isinstance(distribution, dict):
        candidates.append(distribution)
        distribution_attrs = distribution.get("attrs")
        if isinstance(distribution_attrs, dict):
            candidates.append(distribution_attrs)

    for candidate in candidates:
        for key in ("version", "package_version"):
            value = candidate.get(key)
            if value:
                return str(value)

    return None


def filter_files_by_version(file_records, version):
    if not version:
        return file_records

    return [
        file_record
        for file_record in file_records
        if get_package_version(file_record) == version
    ]
