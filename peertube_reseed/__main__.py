# peertube-reseed  Copyright (C) 2021  LoveIsGrief
# This program comes with ABSOLUTELY NO WARRANTY for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions type `show c' for details.
import logging
import shutil
import signal
import tempfile
import time
from argparse import ArgumentParser
from pathlib import Path
from typing import List

import libtorrent as lt
import requests
from requests import Session
from requests_toolbelt.sessions import BaseUrlSession


def main(
        count: int,
        target_server: str,
        download_path: Path,
        active_downloads: int = 3
):
    client = BaseUrlSession(f"{target_server}/api/v1/", )
    client.headers["User-Agent"] = "peertube-reseed v0.0.1"

    videos = get_videos(client, count)

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
    torrent_session = lt.session(
        {
            "active_downloads": active_downloads,
            "active_seeds": len(torrent_params),
            "active_limit": len(torrent_params),
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

    # Download and seed until Ctrl+C
    while True:
        if "should_stop" in d:
            logging.info("Stopping...")
            break

        for torrent in torrents:
            status = torrent.status()
            print(
                '%s+ %.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
                    status.save_path,
                    status.progress * 100, status.download_rate / 1000, status.upload_rate / 1000,
                    status.num_peers, status.state),
                flush=True
            )

        # Print errors
        alerts = torrent_session.pop_alerts()
        for alert in alerts:
            if alert.category() & lt.alert.category_t.error_notification:
                logging.warning(alert)

        time.sleep(1)


def download_file(url: str) -> Path:
    response = requests.get(url)
    response.raise_for_status()

    temp_dir = Path(tempfile.mkdtemp())
    torrent_file_path = (temp_dir / "torrent")
    torrent_file_path.write_bytes(response.content)

    return torrent_file_path


def list_dirs(directory: Path) -> List[Path]:
    """
  List directories in the given directory
  """
    return [path for path in directory.iterdir() if path.is_dir()]


def get_videos(client: Session, count: int) -> list:
    video_ids = []

    # Try to fill up the video_ids
    # sometimes trending might not have enough videos
    sort_strings = ["trending", "views", "likes"]
    while len(video_ids) < count and len(sort_strings) > 0:
        sort = sort_strings.pop()
        result = client.get(
            "videos", params={
                "sort": f"-{sort}",
                # nsfw: true,
                "count": count,
            }
        ).json()

        # Add only the number of video_ids we need
        data = result["data"]
        spliced = data[:min(len(data), count)]
        video_ids.extend([video["id"] for video in spliced])

    return [client.get(f"videos/{_id}").json() for _id in video_ids]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser(prog="peertube-reseed")
    parser.add_argument("--version", help="Print the version number", action='version', version='%(prog)s 0.0.1')
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
        "-d", "--download-path", help="Download dir of all videos", type=Path, default=Path("/tmp/peertube-reseed/")
    )
    parser.add_argument("target_server", help="Which server to help reseed trending videos")

    args = parser.parse_args()

    main(args.count, args.target_server, args.download_path, active_downloads=args.active_downloads)
