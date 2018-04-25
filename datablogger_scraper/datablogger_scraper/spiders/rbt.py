# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy import signals
import re
from lxml import html
from scrapy.http import HtmlResponse
import requests
import urllib.request  # for python3
#import urllib # for python2
from treelib import Node, Tree
from anytree import Node, RenderTree, AnyNode
from anytree.exporter import JsonExporter, DictExporter
import pymongo
from pymongo import MongoClient

### Comand to execute webcrawler: scrapy crawl rbt ###

class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "rbt"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ['142.133.174.148']
    
    # The URLs to start with
    #start_urls = ['http://142.133.174.148:8888/AfgAfg4MasterSmokeTestSuites']
    #start_urls = ['http://142.133.174.148:8888/TestSuites']
    #start_urls = ['http://142.133.174.148:8888/TestCases']


    IPAndPort = 'http://142.133.174.148:8888/'
    mongoIP = 'localhost' 
    database = 'RBT'
    collection = 'tests'

    method_index = True

    # Method for parsing items
    def parse(self, response):
        ## Create root Node
        if(self.method_index == True):
            self.root_url = self.start_urls[0]
            self.root_link = self.start_urls[0].replace(self.IPAndPort, "")
            self.root = AnyNode(id=self.root_link)
            self.method_index = False 
        
        ## Replace current_URL to Parent_URL if first or non-first run
        parent_url = self.root_url
        parent_link = self.root_link
        parent = self.root
        if (response.url != self.root_url):
            parent_url = response.url
            parent_link = parent_url.replace(self.IPAndPort, "")
            parent = response.meta['parent']
            #print("I am your parent", parent)
        
        #NOTE: Change urllib.request.urlopen() block, e.g. regex and xpath, to filter out urls for desired target_tool.
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
            #print(links)
        
        ## Create multiple nodes for current_parent
        for link in links:
            ## Create a node for current_parent
            current_node = AnyNode(id=link, parent=parent)

            ## Recursively call parse function passing current_url and current_node (format url & NodeMixin, respectively)
            current_url = "".join(self.IPAndPort + link)
            request =  scrapy.Request(current_url, callback=self.parse, dont_filter=False)
            request.meta['parent'] = current_node
            yield request

        ## Print root-tree that displays a node's relationship between its parent and its potential children. Each node is in NodeMixin format.
        #print("RENDER:", RenderTree(self.root))
        #exporter = JsonExporter(indent=2, sort_keys=True)        
        #print(exporter.export(self.root))        
 
 

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """ https://linode.com/docs/development/python/use-scrapy-to-extract-data-from-html-tags/ """
        spider = super(DatabloggerSpider, cls).from_crawler(crawler, *args, **kwargs)
        # Register the spider_closed handler on spider_closed signal
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self):
        """ Handler for spider_closed signal."""
        print("Goodbye vermin")
        exporter = DictExporter()  
        exported_result = exporter.export(self.root)
        self.postToMongo(self.mongoIP, self.database, self.collection, exported_result)
    
        
    ## Post the Dictionary Results to Mongodb
    def postToMongo(self, mongoIP, database, collection, log):
        client = MongoClient(mongoIP, 27017) # connects client with the mongoserver
        db = client[database] # create/connect to a database
        col = db[collection]  # create/connect to a collection

        col.insert_one(log)  # insert log document in a collection
        
            