#!/usr/bin/env bash

cd gerritbot
rm output.json
mkdir -p mirror
cp patched/index.html ./mirror/
scrapy crawl change_number  -o output.json -a change_number_end=23829
