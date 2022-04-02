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
import logging
import tempfile
from pathlib import Path
from typing import Dict, List

import requests


def download_file(url: str) -> Path:
    response = requests.get(url)
    response.raise_for_status()

    temp_dir = Path(tempfile.mkdtemp())
    torrent_file_path = (temp_dir / "torrent")
    torrent_file_path.write_bytes(response.content)

    return torrent_file_path


def make_torrent_params(torrent_urls: Dict[str, str], parent_folder: Path) -> List[dict]:
    """
    Generate torrent parameters that can be used by libtorrent to start a torrent

    :param torrent_urls: Pairs of labels and urls to .torrent files
    :param parent_folder: Where the subfolders to download each torrent will be created
    """
    torrent_params = []
    for label, torrent_url in torrent_urls.items():

        try:
            # libtorrent doesn't support downloading the file for us, so we do it ourselves
            torrent_path = download_file(torrent_url)
        except Exception as e:
            logging.error("Couldn't download torrent from %s : %s", torrent_url, e)
            continue

        file_dir_download_path = parent_folder / label
        torrent_params.append(
            {
                "ti": lt.torrent_info(str(torrent_path)),
                "save_path": str(file_dir_download_path)
            }
        )

    return torrent_params
