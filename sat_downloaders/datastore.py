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

"""Downloader for the EUMETSAT Datastore."""
import logging
import netrc
from contextlib import contextmanager
from datetime import datetime, timedelta

import eumdac
from trollsift import parse

from sat_downloaders import Entry, Downloader

logger = logging.getLogger(__name__)


@contextmanager
def timer(title):
    start_time = datetime.now()
    yield
    logger.debug(title + " took %s", str(datetime.now() - start_time))


class DSEntry(Entry):

    def __init__(self, product, id_pattern):
        self._product = product
        self.filename = product._id
        self.mda = parse(id_pattern, self.filename)

    @contextmanager
    def open(self):
        with self._product.open() as raw:
            yield raw


class DataStoreDownloader(Downloader):

    def __init__(self, server, collection, search_days, query_args, entry_patterns):
        self.search_days = search_days
        self.query_args = query_args
        self.collection = collection
        client_id, _, client_secret = netrc.netrc().authenticators(server)
        credentials = (client_id, client_secret)
        with timer("token"):
            self._token = eumdac.AccessToken(credentials)
        self.name = "Eumetsat Datastore"
        self.entry_patterns = entry_patterns

    @classmethod
    def from_config(cls, config_item):
        return cls(**config_item)

    def query(self):
        logger.info(f"At {datetime.utcnow()}, requesting files over the baltic sea from {self.name}.")
        with timer("datastore"):
            datastore = eumdac.DataStore(self._token)
        with timer("collection"):
            # This is slow, creating the Collection directly instead
            # selected_collection = datastore.get_collection(self.collection)
            from eumdac.collection import Collection
            selected_collection = Collection(self.collection, datastore)

        # Set sensing start and end time
        end = datetime.utcnow()
        start = datetime.utcnow() - timedelta(days=self.search_days)

        # Retrieve datasets that match our filter
        with timer("search"):
            products = selected_collection.search(
                dtstart=start,
                dtend=end,
                **self.query_args,
            )
        entries = [DSEntry(prod, **self.entry_patterns) for prod in products]

        self._check_entries(entries)

        return entries
