# peertube-reseed  Copyright (C) 2021  LoveIsGrief
# This program comes with ABSOLUTELY NO WARRANTY for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions type `show c' for details.
import argparse
import libtorrent as lt
import logging
import shutil
import signal
import time
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from io import TextIOBase
from pathlib import Path
from typing import List

from requests_toolbelt.sessions import BaseUrlSession

from peertube_reseed.cli import CommaSeparatedOption
from peertube_reseed.constants import SORT_OPTIONS
from peertube_reseed.files import list_dirs
from peertube_reseed.logs import output_status
from peertube_reseed.videos import get_videos
from peertube_reseed.web import download_file


def main(
        count: int,
        target_server: str,
        download_path: Path,
        active_downloads: int = 3,
        output_file: TextIOBase = None,
        sorts: List[str] = None,
):
    output_file = output_file or open("/dev/stderr", mode="w")
    client = BaseUrlSession(f"{target_server}/api/v1/", )
    client.headers["User-Agent"] = "peertube-reseed v0.0.1"

    videos = get_videos(client, count, sorts)

    # Keep track of the old downloads
    logging.info("Creating target directory %s", download_path)
    download_path.mkdir(parents=True, exist_ok=True)
    old_paths = set(list_dirs(download_path))

    # Gather torrents to download
    torrent_params = []
    video_download_paths = set()
    for video in videos:
        video_download_path = download_path / f"video-{video['id']}"
        video_download_path.mkdir(parents=True, exist_ok=True)
        video_download_paths.add(video_download_path)

        for file in video["files"]:
            torrent_url = file.get("torrentDownloadUrl")
            if not torrent_url:
                logging.warning("No torrent URL for %s", file)
                continue
            try:
                # libtorrent doesn't support downloading the file for us so we do it ourselves
                torrent_path = download_file(torrent_url)
            except Exception as e:
                logging.error("Couldn't download torrent from %s : %s", torrent_url, e)
                continue

            file_dir_download_path = video_download_path / file["resolution"]["label"]
            torrent_params.append(
                {
                    "ti": lt.torrent_info(str(torrent_path)),
                    "save_path": str(file_dir_download_path)
                }
            )

    # Create a session that can download and seed all the torrents
    file_count = len(torrent_params)
    logging.info("Files to download: %s", file_count)
    torrent_session = lt.session(
        {
            "active_downloads": active_downloads,
            "active_seeds": file_count,
            "active_limit": file_count,
        }
    )
    torrents = [torrent_session.add_torrent(torrent_param) for torrent_param in torrent_params]

    # Clean up old downloads
    for oldPath in (old_paths - video_download_paths):
        logging.info("Removing old folder %s", oldPath)
        shutil.rmtree(oldPath)
    d = {}

    def stop(*args):
        d["should_stop"] = True

    signal.signal(signal.SIGINT, stop)

    logging.info("Looping...")
    if output_file.seekable():
        logging.info("Read %s for more detailed progress", output_file.name)
    # Download and seed until Ctrl+C
    while True:
        if "should_stop" in d:
            logging.info("Stopping...")
            break

        output_status(torrents, output_file)

        # Print errors
        alerts = torrent_session.pop_alerts()
        for alert in alerts:
            if alert.category() & lt.alert.category_t.error_notification:
                logging.warning(alert)

        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser(
        prog="peertube-reseed",
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--version", help="Print the version number", action='version', version='%(prog)s 0.1.0')
    parser.add_argument(
        "-s", "--sorts",
        help="Which sort of video to reseed, in descending priority. Allowed options %s" % ",".join(SORT_OPTIONS),
        type=CommaSeparatedOption(SORT_OPTIONS),
        default=SORT_OPTIONS
    )
    parser.add_argument(
        "--active-downloads",
        help="Number torrents to download at the same time. Each torrent has one video file in a specific resolution. "
             "A video can thus have individual torrents for 360p,480p, 1080p",
        type=int,
        default=3
    )
    parser.add_argument(
        "-c", "--count",
        help="Number of videos to reseed. "
             "Keep in mind that videos have multiple files for each resolution they are encoded in",
        type=int,
        default=10
    )
    parser.add_argument(
        "-o", "--output",
        help="Provide a file path to where the progress will be output. (default: /dev/stderr)",
        type=argparse.FileType("w"),
        default=argparse.SUPPRESS
    )
    parser.add_argument(
        "-d", "--download-path", help="Download dir of all videos", type=Path, default=Path("/tmp/peertube-reseed/")
    )
    parser.add_argument("target_server", help="Which server to help reseed trending videos")

    args = parser.parse_args()

    main(
        args.count, args.target_server, args.download_path,
        active_downloads=args.active_downloads,
        sorts=args.sorts,
        output_file=getattr(args, "output", None),
    )
