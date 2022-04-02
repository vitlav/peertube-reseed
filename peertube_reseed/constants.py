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
import operator
import typing
from collections import OrderedDict

CALLS_PER_SECOND = 2.5
"""For rate limiting"""

SORT_OPTIONS = [
    "hot",
    "trending",
    "likes",
    "views",
    "createdAt",
    "publishedAt",
    "name",
    "duration",
]
"""
Which sort of video the user can pick to reseed
List taken from https://docs.joinpeertube.org/api-rest-reference.html#operation/getVideos
"""

OUTPUT_HEADERS: typing.OrderedDict[
    str,
    typing.Callable[[lt.torrent_status], typing.Union[str, int]]
] = OrderedDict(
    [
        ("Path", operator.attrgetter("save_path")),
        ("State", lambda status: str(status.state)),
        ("Peers", operator.attrgetter("num_peers")),
        ("Progress %", lambda status: status.progress * 100),
        ("Down kB/s", lambda status: status.download_rate / 1000),
        ("Up kB/s", lambda status: status.upload_rate / 1000),
    ]
)
"""Headers for the table of status details for torrents"""
