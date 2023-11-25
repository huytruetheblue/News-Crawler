import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    
    start_urls = [
        "https://www.bbc.com/sport/football/67500698",
    ]

    def parse(self, response):
            # yield {
            #     "title": quote.xpath("//h1/text()").get(),
            #     "time": quote.xpath("//time//span/text()").get() 
            # }\
        content = response.xpath("//p//span/text()").getall()
        content = " ".join(content)
        yield {
            "title": response.xpath("//h1/text()").get(),
            "time": response.xpath("//time//span/text()").get(),
            "content": content
        }