# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
#from datablogger_scraper.items import DatabloggerScraperItem
import re
from lxml import html
from scrapy.http import HtmlResponse
import requests
#import urllib.request  # for python3
import urllib # for python2
from treelib import Node, Tree

class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "jobs"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ['142.133.174.148']
    
    # The URLs to start with
    #start_urls = ['http://142.133.174.148:8888/TestSuites']
    start_urls = ['http://142.133.174.148:8888/TestCases']

    method_index = True
    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        self.tree = Tree()
        self.parent_link = self.tree.create_node(self.start_urls)
        
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

        
    # Method for parsing items
    def parse(self, response):
        if(self.method_index == True):
            self.start_requests()
            print('hello')
            self.method_index = False 
        
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
        
        # Try if parent_link exists at the start of crawling 
        try:
            self.parent_link = response.meta.parent_link 
        except AttributeError:
            pass
        # Store URLs in a tree or dictionary-list data structure
        for link in links:
            # Turn the relative url to an absolute url
            absolute_url = "".join('http://142.133.174.148:8888/' + link)   
            print(link)
            print(self.parent_link)
            # TODO: create tree structure with each element of link
            # TODO: Check what value link and absolute_link has | check if link is a unique name (the absolute path) or the latest name(relative path)
            data = [link, absolute_url]
            print
            self.tree.create_node(link, link, self.parent_link, data)

            request = scrapy.Request(absolute_url, callback=self.parse, dont_filter=True)
            request.meta['parent_link'] = link


            # Callback Parse function if links variable contain urls
            #TODO: how to callback itself without overriding previous data in for-loop
            yield request

        #self.tree.show()
        #print(self.tree.to_json(with_data=True))

