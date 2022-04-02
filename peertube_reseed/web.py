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
import tempfile
from pathlib import Path

import requests


def download_file(url: str) -> Path:
    response = requests.get(url)
    response.raise_for_status()

    temp_dir = Path(tempfile.mkdtemp())
    torrent_file_path = (temp_dir / "torrent")
    torrent_file_path.write_bytes(response.content)

    return torrent_file_path
