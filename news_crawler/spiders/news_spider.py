import scrapy
import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://huytrue02:huytrue2002@cluster0.bxyokxl.mongodb.net/?retryWrites=true&w=majority"
class NewsSpider(scrapy.Spider):
    name = "news"
    
    custom_settings = {
        'RETRY_TIMES': 3,
        'RETRY_DELAY': 5,
        'DOWNLOAD_TIMEOUT': 30
    }
    
    allowed_domains = ['www.bbc.com']
    start_urls = [
        "https://www.bbc.com/sport/football",
    ]
    
    def __init__(self, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        
        # Kết nối tới MongoDB
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['news-data']
        self.collection = self.db['news']


    def parse(self, response):
        news_links = response.css('a[href*="/sport/football/"]::attr(href)').getall()

        # Theo dõi các đường dẫn tin tức bóng đá
        for link in news_links:
            match = re.search(r'/(\d+)$', link)
            # Lưu thông tin các trang chi tiết
            if match:
                yield response.follow(link, callback = self.parse_football)
            else:
                yield response.follow(link, callback = self.parse)
                
    def parse_football (self, response):
        if self.collection.count_documents({'url': response.url}) > 0:
            return
        content = response.xpath("//p//span/text()").getall()[5:]
        content = " ".join(content)
        news_data = {
            "title":response.xpath("//h1/text()").get(),
            "content": content,
            "url": response.url
        }
        
        self.collection.insert_one(news_data)
        yield {
            "title":response.xpath("//h1/text()").get(),
            "content": content,
            "url": response.url
        }
        
    def closed(self, reason):
        # Đóng kết nối với MongoDB
        self.client.close()