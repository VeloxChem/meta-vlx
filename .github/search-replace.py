#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


class SearchReplace(dict):
    """All-in-one multiple-string-substitution class."""

    def _make_regex(self):
        """Build re object based on the keys of the current dictionary."""
        return re.compile("|".join(map(re.escape, self.keys())))

    def __call__(self, match):
        """Handler invoked for each regex match."""
        return self[match.group(0)]

    def replace(self, text):
        """Translate text, returns the modified text."""
        return self._make_regex().sub(self, text)


def main():

    parser = argparse.ArgumentParser(description="Search and replace in file.")

    parser.add_argument(
        "--replace",
        dest="replace",
        action="store",
        nargs="*",
        type=str,
        required=True,
        help="`search=replace` pairs: `--replace 's0=r0' 's1=r1'`. `search` can be a Python regex.",
    )
    parser.add_argument(
        "--file",
        dest="asset",
        action="store",
        type=Path,
        required=True,
        help="location of final file. The corresponding template file with suffix `.in` will be read-in.",
    )

    args = parser.parse_args()

    conf = {x[0]:x[1] for x in [tuple(_.split("=")) for _ in args.replace]}
    replacer = SearchReplace(conf)

    asset = args.asset.resolve()

    template = asset.parent / (asset.name + ".in")
    with template.open("r") as f:
        contents = f.read()

    with asset.open("w") as f:
        f.write(replacer.replace(contents))


if __name__ == "__main__":
    main()
