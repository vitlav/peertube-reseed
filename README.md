`peertube-reseed-js` is an attempt at writing a... well... reseeder for peertube.

It reseeds a given number of trending videos.

# Why ?

Instances are often hosted by people without the funds of a large company
 and bandwidth isn't free.
Even if WebTorrents are used, it only has an impact on bandwidth 
 if multiple people are watching the file together.

This tool will act as another seed for the video.

# Start

```shell
# Install command globally
$ npm install -g
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

You will need the node version defined in `.nvmrc`. 
It's the one the project's been tested with.

Node can easily be installed with wth Node Version Manager [nvm]

Then run `npm install` and you're ready to go.


[nvm]: https://github.com/creationix/nvm
