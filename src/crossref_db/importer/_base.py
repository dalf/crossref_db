from typing import Iterator
from pathlib import Path

from ..config import Config


class File:
    """One .json.gz file"""

    def __init__(self, file_path: Path):
        self.path = file_path

    def done(self):
        """Call this method when the task is done
        Allow to delete the file if it is temporary.
        """
        pass


class Importer:
    def __init__(self, config: Config):
        self.config = config

    def iterate() -> Iterator[File]:
        for file in []:
            yield file
