# -*- coding: utf-8 -*-
import scrapy


class ChangeNumberSpider(scrapy.Spider):
    name = 'change_number'
    allowed_domains = ['kitware.com']

    def start_requests(self):
        change_number_start = 23649
        change_number_end = 23650
        for change_number in range(change_number_start, change_number_end + 1):
            url = 'http://review.source.kitware.com/#/c/' + str(change_number) + '/'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass
