from ..config import Config
from ._base import File
from .ftp import FTPImporter
from .local import LocalImporter


__all__ = ["create_importer", "File"]


def create_importer(config: Config):
    if config.ftp:
        return FTPImporter(config)
    if config.local:
        return LocalImporter(config)
    raise ValueError("Importer configuration error")
