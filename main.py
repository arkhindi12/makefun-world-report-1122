"""Entry point the make.fun sandbox runs: puts the committed render in MAKEFUN_OUTPUT_DIR."""

import os
import shutil
import sys

LIMIT = 1048576
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    if os.path.abspath(dest) != os.path.abspath(SRC):
        shutil.copyfile(SRC, dest)
    size = os.path.getsize(dest)
    print(dest)
    print(size)
    return 1 if size > LIMIT else 0


if __name__ == "__main__":
    sys.exit(main())
