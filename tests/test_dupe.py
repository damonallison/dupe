import logging
import os
from pathlib import Path

from dupe import dupe


#
# What is the difference between os.path and pathlib.Path?
#
# * os.path: lower level
#
class TestDupe:
    def print_Path(path: Path) -> None:
        pass

    def create_test_dir(root: Path) -> None:
        pass

    def test_find_dups(self) -> None:
        d = dupe.find(os.getcwd())
        for k, v in d.items():
            logging.debug(f"{k} = {v}")
