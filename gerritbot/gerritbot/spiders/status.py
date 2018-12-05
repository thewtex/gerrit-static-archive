# -*- coding: utf-8 -*-
import os
import urllib
import re
from io import BytesIO
import zipfile
import shutil

import scrapy
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


class StatusSpider(scrapy.Spider):
    name = 'status'
    allowed_domains = ['kitware.com']
    mirror_path = os.path.join('.', 'mirror')
    screenshots_path = os.path.join('.', 'screenshots')

    def strip_site(self, url):
        if not url.startswith(self.site):
            return url
        return url[len(self.site):]

    def start_requests(self):
        number_start = int(getattr(self, 'number_start', 0))
        number_end = int(getattr(self, 'number_end', 50))
        self.site = getattr(self, 'site', 'http://review.source.kitware.com')

        status_path = os.path.join(self.mirror_path, '#', 'q')
        status_path_s = os.path.join(self.screenshots_path, '#', 'q')
        if not os.path.exists(status_path):
            os.makedirs(status_path)
        if not os.path.exists(status_path_s):
            os.makedirs(status_path_s)
        for status_number in range(number_start, number_end, 25):
            url = self.site + '/#/q/status:open,' + str(status_number)
            yield SeleniumRequest(url=url, callback=self.parse,
                    dont_filter=True,
                    screenshot=True,
                    wait_time=300,
                    wait_until=EC.presence_of_element_located((By.XPATH,
                        '//span[@class="rpcStatus"][@style="display: none;"]')))

    def parse(self, response):
        status_number = response.url[-1]

        status_path_s = os.path.join(self.screenshots_path, '#', 'q',
                response.url.split('/')[-1])
        if not os.path.exists(status_path_s):
            os.mkdir(status_path_s)
        screenshot_path = os.path.join(status_path_s, 'screenshot.png')
        with open(screenshot_path, 'wb') as image_file:
            image_file.write(response.meta['screenshot'])
        self.log('Saved file {}'.format(screenshot_path))

        status_path = os.path.join(self.mirror_path, '#', 'q', response.url.split('/')[-1])
        if not os.path.exists(status_path):
            os.mkdir(status_path)
        html_path = os.path.join(status_path, 'index.html')
        soup = BeautifulSoup(response.text, 'lxml')

        for link in soup.find_all('link'):
            url = response.urljoin(str(link['href']))
            link['href'] = self.strip_site(url)
            yield scrapy.Request(url=url, callback=self.parse_asset)

        for script in soup.find_all('script'):
            if script.get('src'):
                url = response.urljoin(str(script['src']))
                script['src'] = self.strip_site(url)
                yield scrapy.Request(url=url, callback=self.parse_asset)

        for anchor in soup.find_all('a'):
            if 'href' in anchor.attrs and anchor['href'][0] == '#':
                anchor['href'] = '/' + anchor['href']

        project = soup.find('div', string='Projects', class_='gwt-Label')
        if project:
            project.parent.extract()
        documentation = soup.find('div', string='Documentation', class_='gwt-Label')
        if documentation:
            documentation.parent.extract()

        for menuitem in ['Open', 'Merged', 'Abandoned']:
            link = soup.find('a', string=menuitem)
            link['href'] = '/' + menuitem + '.html'

        search_script = soup.new_tag('script', src='/goToChangeId.js')
        head = soup.find('head')
        head.append(search_script)
        search_button = soup.find('button', class_='searchButton')
        if search_button:
            search_button.string = 'Go to Change-Id'
            search_button['onclick'] = 'goToChangeId()'

        # Remove 'Sign In' link
        sign_in = soup.find('a', class_='menuItem', role='menuitem', string='Sign In')
        if sign_in:
            sign_in.parent.extract()

        powered_by = soup.find('a', string='Gerrit Code Review')
        powered_by.string = 'Gerrit Static Archive'
        powered_by['href'] = 'https://github.com/thewtex/gerrit-static-archive'

        shortcuts = soup.find('span', string="Press '?' to view keyboard shortcuts")
        shortcuts.extract()

        with open(html_path, 'w') as fp:
            fp.write(str(soup))
        self.log('Saved file {}'.format(html_path))

    def parse_asset(self, response):
        asset = { 'original_url': response.url }
        url = self.strip_site(response.url)
        asset['url'] = url
        asset_path = self.mirror_path + '/' +  os.path.dirname(url)
        if not os.path.exists(asset_path):
            os.makedirs(asset_path)
        asset_path = os.path.join(asset_path, os.path.basename(url))
        if not os.path.exists(asset_path):
            with open(asset_path, 'wb') as fp:
                fp.write(response.body)
            self.log('Saved file {}'.format(asset_path))
        item = { 'asset': asset }
        yield item
