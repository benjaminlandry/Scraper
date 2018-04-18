# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
#from datablogger_scraper.items import DatabloggerScraperItem
import re
from lxml import html
from scrapy.http import HtmlResponse
import requests
import urllib.request  # for python3
#import urllib # for python2
from treelib import Node, Tree
import sys, traceback
import logging
import time

class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "jobsTest"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ['142.133.174.148']
    
    # The URLs to start with
    start_urls = ['http://142.133.174.148:8888/TestSuites']
    #start_urls = ['http://142.133.174.148:8888/TestCases']

    method_index = True
    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        self.tree = Tree() 
        parent_link = self.start_urls[0].replace("http://142.133.174.148:8888/", "")
        logging.warning('THE BEGINNING')

        self.tree.create_node(parent_link, parent_link)
        yield scrapy.Request(self.start_urls[0], callback=self.parse, dont_filter=True)
        
    # Method for parsing items
    def parse(self, response):
        if(self.method_index == True):
            self.start_requests()
            self.method_index = False 
        
        parent_link = response.url
        parent_link = parent_link.replace("http://142.133.174.148:8888/", "")
        print(parent_link)

        # Fetch the html from the given url
        with urllib.request.urlopen(response.url) as response:
            current_page = response.read().decode('utf-8')
            # Filter and replace a string between two arguments using Regex
            regex = r"(Back to)(.|\n)*?<br><br>"
            regex_response = html.fromstring(re.sub(regex, "", current_page))
            # Extract URL from the html, using xpath
            links = regex_response.xpath('//div[@class="work_area_content"]//div[not(@class="footer") and not(@class="popup_window")]//@href | //div[@class="work_area_content"]/a[not(contains(text(),"shutdown"))]/@href')


        ## Store URLs in a tree or dictionary-list data structure | links stores all the children
        # set parent of a node e.g.(link) to the variable parent_link
        for link in links: ### HERE ###
            try:
                print('PARENT_LINK_A', parent_link)  ### HERE produces correct parent_link value
                # Turn the relative url to an absolute url
                absolute_url = "".join('http://142.133.174.148:8888/' + link)   
                data = [link, absolute_url]
                print("NODE_TREE", self.tree.create_node(link, link, parent=parent_link, data=data)) ### HERE does NOT produces correct parent_link value | issue is create_node function.

                request = scrapy.Request(absolute_url, callback=self.parse, dont_filter=False)
                # Callback Parse function if links variable contain urls
                logging.warning('YIELD')
                #yield {'data': data, 'link': link, 'parent_link': self.parent_link}
                yield request
            except:
                print('PARENT_LINK_C', parent_link)
                traceback.print_exc()
            time.sleep(1)

            #self.tree.show()
            #print(self.tree.to_json(with_data=True))
            ##

