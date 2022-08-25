#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2014-2022 Martin Raspaud

# Author(s):

#   Martin Raspaud <martin.raspaud@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Downloader for DHUS instances."""
import logging
import sys
from contextlib import contextmanager
from datetime import datetime

import feedparser
import requests
from trollsift import parse, compose

from sat_downloaders import Entry, Downloader

logger = logging.getLogger(__name__)


class DHUSEntry(Entry):
    def __init__(self, r_entry, auth, title_pattern, filename_pattern):
        self.mda = parse(title_pattern, r_entry.title)
        self.filename = compose(filename_pattern, self.mda)
        self._url = r_entry["link"]
        self._auth = auth

    @contextmanager
    def open(self):
        with requests.get(self._url, auth=self._auth, stream=True) as response:
            response.raise_for_status()
            yield response.raw


class DHUSDownloader(Downloader):

    def __init__(self, server, query_args, entry_patterns, auth=None):
        self.server = server
        self.name = server
        self.query_args = query_args
        self.auth = auth
        self.entry_patterns = entry_patterns

    @classmethod
    def from_config(cls, config_item):
        return cls(**config_item)

    def query(self):
        logger.info(f"At {datetime.utcnow()}, requesting files over the baltic sea from {self.name}.")
        url = self.server + f"/search?q={' AND '.join(self.query_args)}&rows=100&start=0"
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


