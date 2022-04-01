`peertube-reseed` is an attempt at writing a... well... reseeder for peertube.

It reseeds a given number of trending videos.

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
Usage: peertube-reseed [options] <targetServer>

peertube-reseed

Arguments:
  targetServer                 Which server to help reseed trending videos

Options:
  -V, --version                output the version number
  -c, --count <number>         Number of videos to reseed (default: 10)
  -d, --downloadPath <string>  Download dir of all videos (default: "/tmp/peertube-reseed/")
  -h, --help                   display help for command
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
