# -*- coding: utf-8 -*-
import os

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
            url = 'http://review.source.kitware.com/#/c/' + str(change_number) + '/'
            self.log('url: {}'.format(url))
            yield SeleniumRequest(url=url, callback=self.parse,
                    dont_filter=True,
                    screenshot=True,
                    wait_time=300,
                    wait_until=EC.element_to_be_clickable((By.ID, 'gerrit_body')))

    def parse(self, response):
        change_number = response.url.split("/")[-2]

        change_path = os.path.join(self.mirror_path, '#', 'c', change_number)
        if not os.path.exists(change_path):
            os.mkdir(change_path)
        body_path = os.path.join(change_path, 'index.html')
        with open(body_path, 'wb') as f:
            f.write(response.body)
        self.log('Saved file {}'.format(body_path))

        change_path_s = os.path.join(self.screenshots_path, '#', 'c', change_number)
        if not os.path.exists(change_path_s):
            os.mkdir(change_path_s)
        screenshot_path = os.path.join(change_path_s, 'screenshot.png')
        with open(screenshot_path, 'wb') as image_file:
            image_file.write(response.meta['screenshot'])
        self.log('Saved file {}'.format(screenshot_path))
