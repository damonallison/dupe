import argparse
import os
import hashlib
from typing import Dict, List


def md5(fpath: str) -> str:
    """Computes the md5 hash of a file"""
    blocksize = 65536
    md5 = hashlib.md5()
    with open(fpath, 'rb') as f:
        for block in iter(lambda: f.read(blocksize), b''):
            md5.update(block)
    return md5.hexdigest()


def find(root: str = '.') -> Dict[str, List[str]]:
    """Finds duplicate files.

    Returns:
      A dictionary containing lists of duplicate files keyed by MD5 hash.

      {"md5" : ["./file1.txt", "./file2.txt"]}
    """
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
        nargs='?',
        default='.',
        help="the root directory to search for dupes. defaults to the current directory.")
    args = parser.parse_args()
    print(find(args.dir))
