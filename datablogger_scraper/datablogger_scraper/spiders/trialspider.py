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
    name = "trialspider"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ['142.133.174.148']
    
    # The URLs to start with
    start_urls = ['http://142.133.174.148:8888/AfgSutTestSuites']
    #start_urls = ['http://142.133.174.148:8888/TestCases']

    method_index = True
    
    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self): 
        self.root_link = self.start_urls[0].replace("http://142.133.174.148:8888/", "")
        self.root = AnyNode(id=self.root_link)
        self.tree = [self.root]
        yield scrapy.Request(self.start_urls[0], callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse(self, response):
        if(self.method_index == True):
            self.start_requests()
            self.method_index = False 
        
        parent_url = self.start_urls[0]
        if 'parent' in response.meta: 
            parent_url = response.meta['parent']
            
        # Fetch the html from the given url
        with urllib.request.urlopen(parent_url) as response:
            current_page = response.read().decode('utf-8')
            # Filter and replace a string between two arguments using Regex
            regex = r"(Back to)(.|\n)*?<br><br>"
            regex_response = html.fromstring(re.sub(regex, "", current_page))
            # Extract URL from the html, using xpath
            links = regex_response.xpath('//div[@class="work_area_content"]//div[not(@class="footer") and not(@class="popup_window")]//@href | \
             //div[@class="work_area_content"]/a[not(contains(text(),"Shutdown")) and not(contains(text(),"Guide")) and  not(contains(text(),"root"))]/@href')
            print(links)
            #//div[@class="work_area_content"]//a/@href | #//div[@class="work_area_content"]/a[not(contains(text(),"Shutdown"))]/@href')
            # Make /a into //a, when parsing stable, xpath( 

        parent = parent_url.replace("http://142.133.174.148:8888/", "")
        print(parent)
        
        # s1 = AnyNode(id="abc", parent=self.root)
        # s2 = AnyNode(id="bbb", parent=s1)
        # print(s1.parent, s1)
        # print(s2)
        # print(RenderTree(self.root))

        # root = Node("root")
        # s0 = Node("sub0", parent=root)
        # s0b = Node("sub0B", parent=s0, foo=4, bar=109)
        # s0a = Node("sub0A", parent=s0)
        # print(s0)
        # print(RenderTree(root))

        
        # for i, value in enumerate(self.tree):
        #     print(i)
        #     print(AnyNode(id=parent) == self.tree[i])
        #     print(AnyNode(id=parent))
        #     print(self.tree[i].parent)

        # Create a node in a tree with each link | Set the current node to be a parent of another node
        for link in links: 
            try:
                #print('PARENT_LINK_A', parent)  
                # Turn the relative url to an absolute url
                absolute_url = "".join('http://142.133.174.148:8888/' + link)


                #if AnyNode(id=parent).parent in self.tree:
                current_node = AnyNode(id=link, parent=AnyNode(id=parent)) ## HERE
                self.tree.append(current_node)
                print(current_node, current_node.parent)
                logging.warning('Im a Parent')

                # Traverse links produced in absolute_url in queue recursively with parse function
                logging.warning('YIELD')
                request = scrapy.Request(absolute_url, callback=self.parse, dont_filter=False)
                request.meta['parent'] = absolute_url
                yield request

            except:
                print('PARENT_LINK_C', parent, link)
                traceback.print_exc()
            time.sleep(1)

            #print("RENDER:", RenderTree(self.root))
            # exporter = JsonExporter(indent=2, sort_keys=True)
            # print(exporter.export(self.root))
        ##

