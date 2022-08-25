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

import io
from zipfile import ZipFile, BadZipfile
from abc import ABC, abstractmethod
import logging


logger = logging.getLogger(__name__)


class Entry(ABC):
    def extract_files(self, dest_dir):
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
        raise NotImplementedError


class Downloader:
    @staticmethod
    def _check_entries(entries):
        if len(entries) == 0:
            logger.warning("No results to the search query.")
        else:
            logger.info("Got %d hits", len(entries))
