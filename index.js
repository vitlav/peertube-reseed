#!/usr/bin/env node
const {program} = require('commander');
const {main} = require("./lib/main");

program
    .name("peertube-reseed")
    .version('0.0.1')
    .option("-c, --count <number>", "Number of videos to reseed", 10)
    .option("-d, --downloadPath <string>", "Download dir of all videos", "/tmp/peertube-reseed/")
    .arguments("<targetServer>")
    .description(
        "peertube-reseed", {
          targetServer: "Which server to help reseed trending videos"
        }
    )
    .action(async(targetServer, options, command) => {
      await main({targetServer, ...options})
    });

program.parse();
