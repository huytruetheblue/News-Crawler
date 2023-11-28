import scrapy
import re
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor
class NewsSpider(scrapy.Spider):
    name = "news"
    
    allowed_domains = ['www.bbc.com']
    start_urls = [
        "https://www.bbc.com/sport/football/67470815",
    ]
    
    rules = (
        Rule(
            LinkExtractor(allow=r'/sport/football/\d+$', deny=r'/sport/football/$'),
            callback="parse_item",
            follow=True
        ),
    )


    def parse(self, response):
        football_links = response.css('a.gs-c-promo-heading').getall()
        yield from response.follow_all(football_links, self.parse_author)
    
    def parse_football(sefl, response):
        content = response.xpath("//p//span/text()").getall()
        content = " ".join(content)
        yield {
            "title": response.xpath("//h1/text()").get(),
            "time": response.xpath("//time//span/text()").get(),
            "content": content,
            "url": response.url,
        }