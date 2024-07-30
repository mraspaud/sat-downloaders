"""Base classes."""

import logging
from abc import ABC, abstractmethod
from zipfile import BadZipfile, ZipFile
from pathlib import Path
from tempfile import NamedTemporaryFile
from contextlib import contextmanager


logger = logging.getLogger(__name__)
CHUNK_SIZE = 65536 * 200


def chunks(raw):
    """Get chunks from a stream."""
    while buff := raw.read(CHUNK_SIZE, decode_content=True):
        yield buff


@contextmanager
def dump_stream_to_temp_file(raw, dir):
    """Create a temporary file"""
    dir.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=dir, suffix=".zip") as fd:
        for chunk in chunks(raw):
            fd.write(chunk)
        yield Path(fd.name)


class Entry(ABC):
    """An entry in the list."""

    def extract_files(self, dest_dir):
        """Extract the files if they are zipped."""
        with self.open() as fo:
            try:
                with dump_stream_to_temp_file(fo, dir=Path(dest_dir) / "tmp") as path:
                    zip_file = ZipFile(path)
                    zip_file.extractall(dest_dir)
            except BadZipfile:
                logger.warning("Error downloading %s, skipping...", self.filename)
            else:
                logger.info("File extracted")
                return zip_file.namelist()

    @abstractmethod
    def open(self):
        """Open the entry."""
        raise NotImplementedError


class Downloader:
    """A downloader."""

    @staticmethod
    def _check_entries(entries):
        if len(entries) == 0:
            logger.warning("No results to the search query.")
        else:
            logger.info("Got %d hits", len(entries))
