# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from datablogger_scraper.items import DatabloggerScraperItem
import re
from lxml import html
from scrapy.http import HtmlResponse



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
    #         callback="parse_items"
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
        # Only extract canonicalized and unique links (with respect to the current page)
        print(type(response))
        test_str = response.text
        # Removes string between two placeholders with regex
        regex = r"(Back to)(.|\n)*?<br><br>"
        regex_response = re.sub(regex, "", test_str)
        regex_response2 = HtmlResponse(regex_response) ##TODO: fix here!
        print(type(regex_response2))
        # matches = re.finditer(regex, regex_response)
        # print(matches)
        # for matchNum, match in enumerate(matches):
        #     matchNum = matchNum + 1

        #     print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

        #TODO: ensure regex_response2 has url data
        #TODO: apply xpath when extracting_links
        #print(regex_response2)
        links = LinkExtractor(canonicalize=True, unique=True, restrict_xpaths = ('//div[@class="work_area_content"]/a')).extract_links(regex_response2)
        print(type(links))
        # #Now go through all the found links
        print(links)
        for link in links:
            item = DatabloggerScraperItem()
            item['url_from'] = response.url
            item['url_to'] = link.url
            items.append(item)
            print(items)
        #Return all the found items
        return items


