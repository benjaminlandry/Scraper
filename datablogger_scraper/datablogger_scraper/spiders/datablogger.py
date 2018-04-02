# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from datablogger_scraper.items import DatabloggerScraperItem
import re
from lxml import html
from scrapy.http import HtmlResponse
import requests
import urllib.request


class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "jobs"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ['142.133.174.149']
    
    # The URLs to start with
    start_urls = ['http://142.133.174.149:8888/TestSuites']

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    # rules = [
    #     Rule(
    #         LinkExtractor(
                
    #         ),
    #         follow=True,
    #         callback="parse"
    #     )
    # ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse(self, response):
        # The list of items that are found on the particular page
        items = []
        # Fetch the html from the given url
        with urllib.request.urlopen(response.url) as response:
            current_page = response.read().decode('utf-8')
            # Filter and replace a string between two arguments using Regex
            regex = r"(Back to)(.|\n)*?<br><br>"
            regex_response = html.fromstring(re.sub(regex, "", current_page))
            print(type(regex_response))
            # Extract URL from the html, using xpath
            regex3 = regex_response.xpath('//div[@class="work_area_content"]/a/@href')
            print(regex3)
            print(type(regex3))

        # print(type(links))
        # # #Now go through all the found links
        # print(links)
        # for link in links:
        #     item = DatabloggerScraperItem()
        #     item['url_from'] = response.url
        #     item['url_to'] = link.url
        #     items.append(item)
        #     #print(items)
        #     yield scrapy.Request(link.url, callback=self.parse, dont_filter=True)

        # #Return all the found items
        # return items


