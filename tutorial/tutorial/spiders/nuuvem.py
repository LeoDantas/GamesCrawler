import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "nuuvem" #Crawler name
    i = 0
    start_urls = [
        'https://www.nuuvem.com/catalog/types/games',
    ]
    def parse(self, response):
        # gonna locate its price and check if it's a number or a string
        # if its a number put them together, if not put what is in the String (Free or Unavailable)
        # We use extract_first() so we won't get the item with the [ that comes with it 
        for game in response.css('div.product-card--grid'): 
            priceInt = game.css('span span.integer::text').extract_first()
            priceDec = game.css('span span.decimal::text').extract_first()
            priceTxt = game.css('span.product-price--val::text').extract_first()
            # removing the spaces if it's not a number
            priceTxt = re.sub(r"[\s]", "", priceTxt)
            if (priceTxt != "Unavailable"):
                if priceInt is None:
                    priceInt = "0,0"
                else:
                    priceInt = priceInt+priceDec
                yield {
                    'nameNu': game.css('h3.product-title::text').extract_first(),
                    'priceNu': priceInt,
                    'linkNu': game.css('a.product-card--wrapper::attr(href)').extract_first(),
                    'imgNu': game.css('div.product-img img::attr(src)').extract_first()
                }
        # Goes to next item on the list with the links, so the crawler goes to the next page
        self.i +=1
        next_page = response.css('noscript a::attr(href)')[self.i].extract()
        if next_page is not None:
            next_page = next_page
            yield scrapy.Request(next_page, callback=self.parse)


