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
import logging
from time import sleep
from typing import List

from requests_toolbelt.sessions import BaseUrlSession

from peertube_reseed.constants import CALLS_PER_SECOND, SORT_OPTIONS


def get_videos(client: BaseUrlSession, count: int, sorts: List[str] = None) -> list:
    video_ids = []

    # Try to fill up the video_ids
    # sometimes trending might not have enough videos
    sort_strings = list(reversed(sorts if sorts else SORT_OPTIONS))
    while len(video_ids) < count and len(sort_strings) > 0:
        sort = sort_strings.pop()
        logging.info("Retrieving videos of sort: %s", sort)
        result = client.get(
            "videos", params={
                "sort": f"-{sort}",
                # nsfw: true,
                "count": count,
                "hasWebtorrentFiles": True
            }
        ).json()

        # Add only the number of video_ids we need
        data = result["data"]
        spliced = data[:min(len(data), count)]
        video_ids.extend([video["id"] for video in spliced])

    logging.info("Downloading video information at %s calls per second", CALLS_PER_SECOND)
    videos = []
    for i, _id in enumerate(video_ids, start=1):
        videos.append(client.get(f"videos/{_id}").json())

        # Don't pass the rate limit of 5 calls per second
        # Be safe and limit to 2.5 per second
        sleep(1 / CALLS_PER_SECOND)
        logging.info("video info: %s/%s", i, len(video_ids))

    return videos
