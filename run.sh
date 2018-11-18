#!/usr/bin/env bash

cd gerritbot
rm output.json
scrapy crawl change_number  -o output.json -a change_number_end=23829
