# -*- coding: utf-8 -*-
import os
import urllib
import re

import scrapy
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


class ChangeNumberSpider(scrapy.Spider):
    name = 'change_number'
    allowed_domains = ['kitware.com']
    mirror_path = os.path.join('.', 'mirror')
    screenshots_path = os.path.join('.', 'screenshots')
    site = 'http://review.source.kitware.com'

    def strip_site(self, url):
        if not url.startswith(self.site):
            return url
        return url[len(self.site):]

    def start_requests(self):
        change_number_start = int(getattr(self, 'change_number_start', 23828))
        change_number_end = int(getattr(self, 'change_number_end', 23829))

        change_number_path = os.path.join(self.mirror_path, '#', 'c')
        change_number_path_s = os.path.join(self.screenshots_path, '#', 'c')
        if not os.path.exists(change_number_path):
            os.makedirs(change_number_path)
        if not os.path.exists(change_number_path_s):
            os.makedirs(change_number_path_s)
        for change_number in range(change_number_start, change_number_end + 1):
            url = self.site + '/#/c/' + str(change_number) + '/'
            self.log('url: {}'.format(url))
            yield SeleniumRequest(url=url, callback=self.parse,
                    dont_filter=True,
                    screenshot=True,
                    wait_time=300,
                    wait_until=EC.presence_of_element_located((By.XPATH,
                        '//span[@class="rpcStatus"][@style="display: none;"]')))

    def parse(self, response):
        change_number = response.url.split("/")[-2]

        change_path_s = os.path.join(self.screenshots_path, '#', 'c', change_number)
        if not os.path.exists(change_path_s):
            os.mkdir(change_path_s)
        screenshot_path = os.path.join(change_path_s, 'screenshot.png')
        with open(screenshot_path, 'wb') as image_file:
            image_file.write(response.meta['screenshot'])
        self.log('Saved file {}'.format(screenshot_path))

        change_path = os.path.join(self.mirror_path, '#', 'c', change_number)
        if not os.path.exists(change_path):
            os.mkdir(change_path)
        html_path = os.path.join(change_path, 'index.html')
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
            if hasattr(anchor, 'href') and anchor['href'][0] == '#':
                anchor['href'] = '/' + anchor['href']

        project = soup.find('div', string='Projects', class_='gwt-Label')
        if project:
            project.parent.extract()
        documentation = soup.find('div', string='Documentation', class_='gwt-Label')
        if documentation:
            documentation.parent.extract()

        search_script = soup.new_tag('script', src='/goToChangeId.js')
        head = soup.find('head')
        head.append(search_script)
        search_button = soup.find('button', class_='searchButton')
        if search_button:
            search_button.string = 'Go to Change-Id'
            search_button['onclick'] = 'goToChangeId()'
        change_id = soup.find_all('span', class_='com-google-gwtexpui-clippy-client-ClippyCss-label')[2].string
        yield { 'ChangeIdToChangeNumber': { change_id: change_number } }

        # Remove 'Sign In' link
        sign_in = soup.find('a', class_='menuItem', role='menuitem', string='Sign In')
        self.log('SignIn' + str(sign_in))
        if sign_in:
            sign_in.parent.extract()

        reply = soup.find('button', title='Reply…')
        if reply:
            reply.parent.extract()

        patch_sets = soup.find('div', string=re.compile(r'^Patch Sets'))
        self.log('Status Right!!!: ' + str(patch_sets))
        if patch_sets:
            patch_sets.parent.extract()

        # Make sure all comments are expanded
        for div in soup.find_all('div', class_='com-google-gerrit-client-change-Message_BinderImpl_GenCss_style-closed'):
            div['class'].remove('com-google-gerrit-client-change-Message_BinderImpl_GenCss_style-closed')
        for div in soup.find_all('div', class_='com-google-gerrit-client-change-Message_BinderImpl_GenCss_style-summary'):
            div['style'] = 'display: none;'
            div['aria-hidden'] = 'true'
        for div in soup.find_all('div', stylename='com-google-gerrit-client-change-Message_BinderImpl_GenCss_style-comment'):
            div['style'] = ''
            div['aria-hidden'] = 'false'

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
