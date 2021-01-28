#!/usr/bin/env node
// peertube-reseed-js  Copyright (C) 2021  LoveIsGrief
// This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
// This is free software, and you are welcome to redistribute it
// under certain conditions; type `show c' for details.

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
