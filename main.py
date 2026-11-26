#!/usr/bin/env python3
"""Name the Robot Band — entry point.

The bounty asks for exactly one line naming an all-robot metal band.
This script assembles that line from its pieces and writes it, with no
trailing newline, to entry.txt inside the requested output folder.
"""

import os
import stat
import sys


# The band's name, its genre tag, and the punchline about the hit single —
# kept as separate fragments so each piece of the joke stays readable.
_BAND_LABEL = "Rust in Peace"
_GENRE_TAG = "the all-robot metal band"
_SINGLE_TAG = "whose hit single 'Error 404: Feelings Not Found'"
_TOASTER_TAG = "is just four toasters screaming in harmony"


def _compose_line():
    """Join the four fragments into the single required sentence."""
    fragments = (_BAND_LABEL, _GENRE_TAG, _SINGLE_TAG, _TOASTER_TAG)
    sentence = ", ".join(fragments[:2])
    sentence = sentence + " " + " ".join(fragments[2:])
    return sentence + "."


def _resolve_target_folder():
    """Pick the output folder from the environment, defaulting to /output."""
    chosen = os.environ.get("OUTPUT_DIR") or "/output"
    return chosen


def _write_entry(folder, line):
    """Create the folder if needed and write the line as UTF-8, mode 0644."""
    os.makedirs(folder, exist_ok=True)
    destination = os.path.join(folder, "entry.txt")
    payload = line.encode("utf-8")
    # Open with an explicit mode so the file lands at 0644 regardless of umask.
    handle = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(handle, payload)
    finally:
        os.close(handle)
    os.chmod(destination, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    return destination


def main():
    line = _compose_line()
    if len(line) != 132:
        sys.stderr.write("unexpected entry length: %d\n" % len(line))
        return 1
    folder = _resolve_target_folder()
    _write_entry(folder, line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
