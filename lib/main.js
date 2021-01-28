const got = require("got");
const WebTorrent = require("webtorrent-hybrid");
const fs = require("fs/promises");
const path = require("path");


async function main({count, targetServer, downloadPath}) {
  count = Number.parseInt(count);
  let client = got.extend({
    prefixUrl: `${targetServer}/api/v1/`,
    headers: {
      "User-Agent": "peertube-reseed-js v0.0.1"
    }
  });


  const videos = await getVideos(client, count);

  // Keep track of the old downloads
  console.info("Creating target directory", downloadPath)
  await fs.mkdir(downloadPath, {recursive: true});
  let downloadDir = await fs.opendir(downloadPath);
  let oldPaths = new Set(await listDir(downloadDir, dirent => !dirent.isDirectory()));

  let webtorrent = new WebTorrent();
  webtorrent.on("torrent", (torrent) => {
    console.info("Started downloading", torrent.name);
    torrent.on("wire", (wire) => {
      console.info(`Setting keep alive for peer ${wire.peerId} to FALSE!`)
      wire.setKeepAlive(false)
    });
  });

  // Start new downloads
  let videoDownloadPaths = new Set();
  for (let video of videos) {
    let videoDownloadPath = path.join(downloadPath, `video-${video.id}`);
    videoDownloadPaths.add(videoDownloadPath);

    for (let file of video.files) {
      const fileDirDownloadPath = path.join(videoDownloadPath, file.resolution.label);
      webtorrent.add(file.magnetUri, {
        path: fileDirDownloadPath
      });
    }
  }
  // Clean up old downloads
  for (let oldPath of [...oldPaths].filter(oldPath => !videoDownloadPaths.has(oldPath))) {
    console.info("Removing old folder", oldPath)
    await fs.rmdir(oldPath, {recursive: true});
  }

}

/**
 * Get the list of directory contents
 *
 * @param dir {Dir}
 * @param [exclude] {function(fs.Dirent): Boolean} - Filter which entries to include
 * @returns {Promise<Array<String>>}
 */
async function listDir(dir,exclude) {
  let paths = [];
  for await (const dirent of dir) {
    if(exclude && exclude(dirent)){
      continue
    }
    paths.push(path.join(dir.path, dirent.name));
  }
  return paths;
}

/**
 *
 * @param client {got.Got}
 * @param count {Number}
 * @returns {Promise<Object[]>}
 */
async function getVideos(client, count) {
  let videoIDs = [];

  // Try to fill up the videoIDs
  // sometimes trending might not have enough videos
  let sortStrings = ["views", "likes", "trending"];
  while (videoIDs.length < count && sortStrings.length > 0) {

    const sort = sortStrings.pop();
    let result = await client("videos", {
      searchParams: {
        sort: `-${sort}`,
        // nsfw: true,
        count
      }
    }).json();

    // Add only the number of videoIDs we need
    let spliced = result.data.splice(0, Math.min(result.data.length, count));
    videoIDs = videoIDs.concat(spliced.map(video => video.id));
  }

  return Promise.all(videoIDs.map(id => client(`videos/${id}`).json()));
}

module.exports = {
  main
}
