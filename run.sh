#!/usr/bin/env bash

cd gerritbot
rm output.jl
mkdir -p mirror
cp patched/index.html ./mirror/
#scrapy crawl change_number  -o output.jl -a change_number_end=23829
scrapy crawl status  -o output.jl -a number_end=1000
python ../scripts/extract-changeid-map.py
