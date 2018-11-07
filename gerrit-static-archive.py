#!/usr/bin/env python

import argparse
import os

import requests
from bs4 import BeautifulSoup

def main(gerrit_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    change = requests.get(gerrit_url + '/#/c/1')
    print(change)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create static website archive for a Gerrit Code Review instance.')
    parser.add_argument('gerrit_url', help='URL for the Gerrit instance.')
    parser.add_argument('output_dir', help='Output directory for the static website.')
    args = parser.parse_args()

    main(args.gerrit_url, args.output_dir)
