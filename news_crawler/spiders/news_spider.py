import scrapy
import re
from twisted.internet.error import ConnectionLost
from scrapy.spidermiddlewares.httperror import HttpError
from ..items import NewsCrawlerItem
class NewsSpider(scrapy.Spider):
    name = "news"
    
    custom_settings = {
        'RETRY_TIMES': 3,
        'RETRY_DELAY': 5,
        'DOWNLOAD_TIMEOUT': 30
    }
    
    allowed_domains = ['www.bbc.com']
    start_urls = [
        "https://www.bbc.com/sport/football/67470815",
    ]


    def parse(self, response):
        if isinstance(response.error, ConnectionLost):
            # Thử lại kết nối
            yield response.request.replace(dont_filter=True)
        
        news_links = response.css('a[href*="/sport/football/"]::attr(href)').getall()
    
        # Theo dõi các đường dẫn tin tức bóng đá
        for link in news_links:
            match = re.search(r'/(\d+)$', link)
            if match:
                yield response.follow(link, callback=self.parse_football)
    
    def parse_football(sefl, response):
        content = response.xpath("//p//span/text()").getall()
        content = " ".join(content)
        item = NewsCrawlerItem()
        item["title"] = response.xpath("//h1/text()").get()
        item["time"] = response.xpath("//time//span/text()").get()
        item["content"] = content
        item["url"] = response.url
        yield item