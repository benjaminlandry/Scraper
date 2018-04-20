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
    name = "trialspider2"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ['142.133.174.148']
    
    # The URLs to start with
    start_urls = ['http://142.133.174.148:8888/AfgOpenIdConnectTestSuites']
    #start_urls = ['http://142.133.174.148:8888/TestCases']

    method_index = True

    # Method for parsing items
    def parse(self, response):
        ## Create root Node
        if(self.method_index == True):
            self.root_url = self.start_urls[0]
            self.root_link = self.start_urls[0].replace("http://142.133.174.148:8888/", "")
            self.root = AnyNode(id=self.root_link)
            self.method_index = False 
        
        ## Replace current_URL to Parent_URL if first or non-first run
        parent_url = self.root_url
        parent_link = self.root_link
        parent = self.root
        if (response.url != self.root_url):
            parent_url = response.url
            parent_link = parent_url.replace("http://142.133.174.148:8888/", "")
            parent = response.meta['parent']
            print("I am your parent", parent)
        
        ## GET and Filter out links from webpage
        # Fetch the html from webpage using provided url
        with urllib.request.urlopen(parent_url) as response:
            current_page = response.read().decode('utf-8')
            # Filter and replace a string between two arguments using Regex
            regex = r"(Back to)(.|\n)*?<br><br>"
            regex_response = html.fromstring(re.sub(regex, "", current_page))
            # Extract URL from the html, using xpath
            links = regex_response.xpath('//div[@class="work_area_content"]//div[not(@class="footer") and not(@class="popup_window")]//@href | \
             //div[@class="work_area_content"]/a[not(contains(text(),"Shutdown")) and not(contains(text(),"Guide")) and  not(contains(text(),"root"))]/@href')
            print(links)
        
        ## Create multiple nodes for current_parent
        for link in links:
            ## Create a node for current_parent
            current_node = AnyNode(id=link, parent=parent)

            ## Recursively call parse function passing current_url and current_node (format url & NodeMixin, respectively)
            current_url = "".join('http://142.133.174.148:8888/' + link)
            request =  scrapy.Request(current_url, callback=self.parse)
            request.meta['parent'] = current_node
            yield request

        ## Print root-tree that displays a node's relationship between its parent and its potential children. Each node is in NodeMixin format.
        print("RENDER:", RenderTree(self.root))
        # exporter = JsonExporter(indent=2, sort_keys=True)
        # print(exporter.export(root))
        
            