#!/usr/bin/env bash

set -x
cd gerritbot
rm output.jl
mkdir -p mirror
cp patched/index.html ./mirror/
change_number_start=1
change_number_end=23900
change_number_chunk_size=500
change_number_chunk_start=${change_number_start}
change_number_chunk_end=${change_number_chunk_start}
let change_number_chunk_end+=${change_number_chunk_size}
while test ${change_number_chunk_end} -lt ${change_number_end}; do
  scrapy crawl change_number  -o output.jl \
    -a change_number_start=${change_number_chunk_start} \
    -a change_number_end=${change_number_chunk_end}
  sleep 180
  let change_number_chunk_start+=${change_number_chunk_size}
  let change_number_chunk_end+=${change_number_chunk_size}
done
scrapy crawl status  -o output.jl -a number_end=1000
python ../scripts/extract-changeid-map.py
