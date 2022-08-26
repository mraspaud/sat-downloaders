"""Base classes."""

import io
import logging
from abc import ABC, abstractmethod
from zipfile import BadZipfile, ZipFile

logger = logging.getLogger(__name__)


class Entry(ABC):
    """An entry in the list."""

    def extract_files(self, dest_dir):
        """Extract the files if they are zipped."""
        with self.open() as fo:
            try:
                zip_file = ZipFile(io.BytesIO(fo.read(decode_content=True)))
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
