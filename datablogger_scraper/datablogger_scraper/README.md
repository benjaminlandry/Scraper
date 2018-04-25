To Run WebCrawler use the command:
- cd scrapy/datablogger_scraper/spiders
- scrapy crawl rbt

In rbt.py file:

    If want to apply webcrawler to other target_tools:
    - change the following parameters for your target_tool and mongodb database:
        IPAndPort 
        mongoIP  
        database 
        collection 

    NOTE: Change urllib.request.urlopen() block, e.g. regex and xpath, to filter out urls from webpage as desired for target_tool.

https://python.gotrained.com/scrapy-tutorial-web-scraping-craigslist/
https://linode.com/docs/development/python/use-scrapy-to-extract-data-from-html-tags/


File Layout:
- /settings.py 
- /spiders/rbt.py
- filter.py