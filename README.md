**Development has stalled because there is currently [no _easy_ way to contribute bandwidth to peertube instances using HLS](https://github.com/Chocobozzz/PeerTube/issues/4895)**

`peertube-reseed` is an attempt at writing a... well... reseeder for peertube.

It reseeds a given number of trending videos.

# Compatibility

The server version must be >= 4.0

# Why ?

Instances are often hosted by people without the funds of a large company
 and bandwidth isn't free.
Even if WebTorrents are used, it only has an impact on bandwidth 
 if multiple people are watching the file together.

This tool will act as another seed for the video.

# Start

This script uses [`libtorrent`][libtorrent] which (at the time of writing) only has webtorrent support 
 on the `master` branch.
I can't be bothered writing a script to install libtorrent requirements and build it --> docker to the rescue.
The docker image builds upon [libtorrent-docker].

```shell
$ docker pull registry.gitlab.com/namingthingsishard/media_tools/peertube-reseed
$ alias peertube-reseed='docker run --rm registry.gitlab.com/namingthingsishard/media_tools/peertube-reseed'
# Install command globally
$ peertube-reseed --help
usage: peertube-reseed [-h] [--version] [-s SORTS]
                       [--active-downloads ACTIVE_DOWNLOADS] [-c COUNT]
                       [-o OUTPUT] [-d DOWNLOAD_PATH]
                       target_server

positional arguments:
  target_server         Which server to help reseed trending videos

optional arguments:
  -h, --help            show this help message and exit
  --version             Print the version number
  -s SORTS, --sorts SORTS
                        Which sort of video to reseed, in descending priority.
                        Allowed options hot,trending,likes,views,createdAt,pub
                        lishedAt,name,duration (default: ['hot', 'trending',
                        'likes', 'views', 'createdAt', 'publishedAt', 'name',
                        'duration'])
  --active-downloads ACTIVE_DOWNLOADS
                        Number torrents to download at the same time. Each
                        torrent has one video file in a specific resolution. A
                        video can thus have individual torrents for 360p,480p,
                        1080p (default: 3)
  -c COUNT, --count COUNT
                        Number of videos to reseed. Keep in mind that videos
                        have multiple files for each resolution they are
                        encoded in (default: 10)
  -o OUTPUT, --output OUTPUT
                        Provide a file path to where the progress will be
                        output. (default: /dev/stderr)
  -d DOWNLOAD_PATH, --download-path DOWNLOAD_PATH
                        Download dir of all videos (default: /tmp/peertube-
                        reseed)
```

**Example**

`peertube-reseed --count 15 https://tilvids.com`

# Development

I'm not going to bother with non-docker stuff, since I haven't tested it.
If someone wants to contribute a `default.nix`, feel free to.

You can make modifications to `peertube_reseed/__main__.py` and run 
`docker-compose up --no-log-prefix`.
You can pass other commands to the script e.g
`docker-compose run --rm reseed https://tilvids.com`


[libtorrent]: https://libtorrent.org/
[libtorrent-docker]: https://gitlab.com/NamingThingsIsHard/net/torrent/libtorrent-docker/
