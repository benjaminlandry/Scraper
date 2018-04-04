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

    # Method which starts the requests by visiting all URLs specified in start_urls
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse(self, response):
        # The list of items that are found on the particular page
        items = {}
        # Fetch the html from the given url
        with urllib.request.urlopen(response.url) as response:
            current_page = response.read().decode('utf-8')
            # Filter and replace a string between two arguments using Regex
            regex = r"(Back to)(.|\n)*?<br><br>"
            regex_response = html.fromstring(re.sub(regex, "", current_page))
            #print(type(regex_response))
            # Extract URL from the html, using xpath
            links = regex_response.xpath('//div[@class="work_area_content"]/a/@href')
            #print(links)
            #print(type(links))
   
        # Store URLs in a dictionary-list data structure
        for link in links:
            # Turn the relative url to an absolute url
            absolute_url = "".join('http://142.133.174.149:8888/' + link)   
            #TODO: add each section of the url in a list of the dictionary & make the dictionary multi-layered
            #seperated_link | absolute_url => link is dictionary-key | absolute_url in list
            seperated_link = link.split(".")
            # TODO: create tree structure with each element of link







            
            for key in seperated_link:
                if(key in items):

                    pass
                    # Add extra dict layer then add url in that layer
                else:
                    items[link] = absolute_url # Add url to current layer



            #print(len(seperated_link))
            #print(seperated_link)

            # Callback Parse function if links variable contain urls
            #TODO: how to callback itself without overriding previous data in for-loop
            yield scrapy.Request(items[link], callback=self.parse, dont_filter=True)


        # #Return all the found items
        # return items


