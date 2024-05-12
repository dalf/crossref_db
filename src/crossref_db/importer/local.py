from pathlib import Path
from ._base import Importer, File
from tqdm import tqdm


class LocalImporter(Importer):
    def iterate(self):
        directory = Path(self.config.local.directory)
        files = directory.glob("*.gz")
        for file in tqdm(files):
            yield File(file)
