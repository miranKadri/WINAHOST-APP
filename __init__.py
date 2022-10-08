# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from scrapy.crawler import CrawlerProcess
import time






class fotocasaSpider(scrapy.Spider):
    
    name = 'fotocasa'
    start_urls = [
        "https://www.fotocasa.es/es/alquiler/viviendas/barcelona-capital/todas-las-zonas/l",
    ]
   
    def parse_itemList(self, response):
        
        items =  response.xpath('.//section[@class="re-SearchResult"]')
        
        for item in items:
            
            title = item.css('a::attr(title)').extract()
            price = item.css('span.re-CardPrice::text').extract()
            desc = item.css('span.re-CardFeaturesWithIcons-feature-icon.re-CardFeaturesWithIcons-feature-icon--surface::text').extract()
            phone = item.css('span.sui-AtomButton-text::text').extract()
            yield {'Text': title,
                   'Price': price,
                   'Description': desc,
                   'Phone': phone}
            
        next_page_url = response.xpath('a.sui-AtomButton.sui-AtomButton--primary.sui-AtomButton--outline.sui-AtomButton--center.sui-AtomButton--small.sui-AtomButton--link.sui-AtomButton--empty.sui-AtomButton--rounded::attr(href)').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse_itemList)
            
process = CrawlerProcess ({
    "FEEDS": {"items.json": {"format": "csv", "overwrite": False}},
    'ROBOTSTXT_OBEY':'False',
    'USER_AGENT': 'Edge/5.0',
    
    })
process.crawl(fotocasaSpider)
process.start()