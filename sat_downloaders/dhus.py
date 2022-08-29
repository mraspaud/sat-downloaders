"""Downloader for DHUS instances."""

import logging
from contextlib import contextmanager
from datetime import datetime
from urllib.parse import urljoin

import feedparser
import requests
from trollsift import compose, parse

from sat_downloaders import Downloader, Entry

logger = logging.getLogger(__name__)


class DHUSEntry(Entry):
    """A dhus entry."""

    def __init__(self, r_entry, auth, title_pattern, filename_pattern):
        """Initialize the entry."""
        self.mda = parse(title_pattern, r_entry.title)
        self.filename = compose(filename_pattern, self.mda)
        self._url = r_entry["link"]
        self._auth = auth

    @contextmanager
    def open(self):
        """Open the entry."""
        with requests.get(self._url, auth=self._auth, stream=True) as response:
            response.raise_for_status()
            yield response.raw


class DHUSDownloader(Downloader):
    """A downloader for DHUS instances."""

    def __init__(self, server, query_args, entry_patterns, auth=None):
        """Initialize the instance."""
        self.server = server
        self.name = server
        self.query_args = query_args
        self.auth = auth
        self.entry_patterns = entry_patterns

    @classmethod
    def from_config(cls, config_item):
        """Instantiate from a config."""
        return cls(**config_item)

    def query(self):
        """Place the query."""
        logger.info(f"At {datetime.utcnow()}, requesting from {self.name}.")
        url = urljoin(self.server, f"search?q={'+AND+'.join(self.query_args)}&rows=100&start=0")
        res = requests.get(url)
        res.raise_for_status()
        d = feedparser.parse(res.text)
        try:
            logger.debug(str(d.feed.title))
        except AttributeError:
            raise IOError("Can't get data from the hub")

        entries = [DHUSEntry(entry, self.auth, **self.entry_patterns) for entry in d.entries]
        self._check_entries(entries)

        return entries
