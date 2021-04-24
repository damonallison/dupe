import argparse
import os
import hashlib
from typing import Dict, List
import logging
from pathlib import Path

#
# 1. Iterate directory
#
#    * number of files
#    * total size
#
# 2. md5 file
#
# 3. Add to dupe list
#
# 4. Decrement operation.
#
#
def md5(fpath: str) -> str:
    """Computes the md5 hash of a file"""
    blocksize = 65536
    md5 = hashlib.md5()
    with open(fpath, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            md5.update(block)
    return md5.hexdigest()


class DupeOperation:
    def __init__(self, root: Path):
        if not root.exists() or not root.is_dir():
            raise ValueError
        self.root = root.resolve(strict=True)

    def reset(self) -> None:
        self.remaining: List[Path] = []
        for path, _, files in os.walk(self.root):
            for fname in files:
                p = Path(path, fname)
                s = p.stat()
                self.remaining.append(Path(path, fname))


def find(root: str = ".") -> Dict[str, List[str]]:
    """Finds duplicate files.

    Returns:
      A dictionary containing lists of duplicate files keyed by MD5 hash.

      {"md5" : ["./file1.txt", "./file2.txt"]}
    """
    logging.info(f"starting find at {root}")
    d = dict()
    for path, _, files in os.walk(root):
        for fname in files:
            fpath = os.path.join(path, fname)
            hash = md5(fpath)
            if hash in d:
                d[hash].append(fpath)
            else:
                d[hash] = [fpath]
    return {k: v for k, v in d.items() if len(v) > 1}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dir",
        nargs="?",
        default=".",
        help="the root directory to search for dupes. defaults to the current directory.",
    )
    args = parser.parse_args()
    print(find(args.dir))
