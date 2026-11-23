"""Copies the day's front page to /output/entry.png.

The image is drawn by gen.py, whose output is committed beside this file, so the program
itself only has to place those bytes: it is deterministic, needs no network, and runs well
inside the sandbox's 60 seconds.

Why it is a copy and not a redraw: the sandbox ships no fonts, so a redraw there would
change every glyph. Copying keeps the image exactly the one that was checked.
"""

from __future__ import annotations

import os
import shutil
import sys


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    sys.stdout.write(f"wrote {dst} ({size} bytes)\n")
    if size > 1048576:
        sys.stderr.write("entry.png is over 1 MiB\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
