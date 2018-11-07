#!/usr/bin/env python

import argparse
import os

import requests
from bs4 import BeautifulSoup

def main(gerrit_url, output_dir, change_set_start, change_set_end):
    os.makedirs(output_dir, exist_ok=True)

    change = requests.get(gerrit_url + '/#/c/1')
    print(change_set_end)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create static website archive for a Gerrit Code Review instance.')
    parser.add_argument('gerrit_url', help='URL for the Gerrit instance.')
    parser.add_argument('output_dir', help='Output directory for the static website.')
    parser.add_argument('--change-set-start', '-s', type=int, default=1, help='First Change Set number to archive.')
    parser.add_argument('--change-set-end', '-e', type=int, default=30000, help='Last Change Set number to archive.')
    args = parser.parse_args()

    print(args)

    main(args.gerrit_url, args.output_dir, args.change_set_start,
            args.change_set_end)
