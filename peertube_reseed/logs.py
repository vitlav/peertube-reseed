"""
peertube-reseed
Copyright (C) 2021 LoveIsGrief

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import libtorrent as lt
from io import TextIOBase
from typing import List

from tabulate import tabulate

from peertube_reseed.constants import OUTPUT_HEADERS


def output_status(torrents: List[lt.torrent_handle], output_file: TextIOBase):
    # Generate rows from ordered headers and their getter functions
    torrent_stati = []
    for torrent in torrents:
        status: lt.torrent_status = torrent.status()
        torrent_stati.append(
            [
                getter(status)
                for getter in OUTPUT_HEADERS.values()
            ]
        )

    # The file handle stays open, so we can't just keep appending
    # Some files however are append-only e.g stderr
    if output_file.seekable():
        output_file.truncate(0)

    output_file.write(tabulate(torrent_stati, list(OUTPUT_HEADERS.keys())))
    output_file.write("\n")  # Append only files would otherwise mess up the first header line

    output_file.flush()
