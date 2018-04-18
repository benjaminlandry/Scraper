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
from anytree import Node, RenderTree, AnyNode
from anytree.exporter import JsonExporter

class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "newJob"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ['142.133.174.148']
    
    # The URLs to start with
    start_urls = ['http://142.133.174.148:8888/TestSuites']
    #start_urls = ['http://142.133.174.148:8888/TestCases']

    method_index = True
    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self): 
        parent_link = self.start_urls[0].replace("http://142.133.174.148:8888/", "")
        self.root = AnyNode(id=parent_link)
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
            links = regex_response.xpath('//div[@class="work_area_content"]//div[not(@class="footer") and not(@class="popup_window")]//@href | \
             //div[@class="work_area_content"]/a[not(contains(text(),"Shutdown")) and not(contains(text(),"Guide")) and  not(contains(text(),"root"))]/@href')
            print(links)
            #//div[@class="work_area_content"]//a/@href | #//div[@class="work_area_content"]/a[not(contains(text(),"Shutdown"))]/@href')
            #make /a into //a, when parsing stable

        ## Store URLs in a tree or dictionary-list data structure | links stores all the children
        # set parent of a node e.g.(link) to the variable parent_link
        for link in links: ### HERE ###
            try:
                print('PARENT_LINK_A', parent_link)  ### HERE produces correct parent_link value
                # Turn the relative url to an absolute url
                absolute_url = "".join('http://142.133.174.148:8888/' + link)   
                parent_link2 = AnyNode(id=parent_link)
                
                child = AnyNode(id=link, parent=parent_link2)

                parent_link2.parent = self.root
                ##child.parent = self.root

                # Callback Parse function if links variable contain urls
                logging.warning('YIELD')
                yield scrapy.Request(absolute_url, callback=self.parse, dont_filter=False)

            except:
                print('PARENT_LINK_C', parent_link)
                traceback.print_exc()
            #time.sleep(1)

            print(RenderTree(self.root))
            # exporter = JsonExporter(indent=2, sort_keys=True)
            # print(exporter.export(self.root))
            ##

