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
    start_urls = ['http://142.133.174.148:8888/TestCases']
 
    def parse(self, response):
        hxs = scrapy.Selector(response)
        # extract all links from page
        all_links = hxs.xpath('*//a/@href').extract()
        # iterate over links
        for link in all_links:
            yield scrapy.http.Request(url=link, callback=self.print_this_link)
 
    def print_this_link(self, link):
        print ("LINK:", link)