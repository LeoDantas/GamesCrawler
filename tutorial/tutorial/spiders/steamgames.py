import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "steam" #Crawler name
    i = 1
    start_urls = [
        'https://store.steampowered.com/search/?category1=998',
    ]
    def parse(self, response):
        # gonna locate its price and check if it's a number or a string
        # if its a number put them together, if not put what is in the String (Free or Unavailable)
        # We use extract_first() so we won't get the item with the [ that comes with it 
        for steamgames in response.css('#search_result_container div:not([class^="search_pagination"]) a'):
            priceTxt = steamgames.css('div div div.search_price::text').extract_first()
            discount = steamgames.css('div div div.search_discount span::text').extract_first()
            # removing the spaces if it's not a number
            priceTxt = re.sub(r"[\s]", "", priceTxt)
            if(discount is not None and priceTxt == ""):
                priceTxt = re.sub(r"[\s]", "",steamgames.css("div div.discounted::text")[1].extract())
            if ("Free" in priceTxt or "Play" in priceTxt):
                priceTxt = "0,0"
            if(priceTxt != "" and priceTxt != "Third-party"):
                yield {
                    'nameSteam': steamgames.css('div.search_name span.title::text').extract_first(),
                    'priceSteam': priceTxt,
                    'linkSteam': steamgames.css('::attr(href)').extract_first(),
                    'imgSteam': steamgames.css("div.search_capsule img::attr(src)").extract_first()
                    }
        # Goes to next item on the list with the links, so the crawler goes to the next page
        self.i +=1
        if (self.i == 2):
            next_page = response.css("div.search_pagination_right a.pagebtn::attr(href)").extract_first()
        else:
            next_page = response.css("div.search_pagination_right a.pagebtn::attr(href)")[1].extract()
        if (next_page is not None):    
            next_page = next_page
            yield scrapy.Request(next_page, callback=self.parse)


