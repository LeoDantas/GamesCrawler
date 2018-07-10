import scrapy
import re
from selenium import webdriver

class QuotesSpider(scrapy.Spider):
    name = "g2a" #Crawler name
    i = 0
    handle_httpstatus_list = [404]
    start_urls = [
        'https://www.g2a.com/pt-br/category/games?platform=1'
    ]
    def parse(self, response):
        # gonna locate its price and check if it's a number or a string
        # if its a number put them together, if not put what is in the String (Free or Unavailable)
        # We use extract_first() so we won't get the item with the [ that comes with it 
        for game in response.css("#app div.content section.products div ul.products-grid li"):
            nameG2a = game.css("div.Card__headings h3.Card__title a::text").extract_first()
            imgG2a = game.css("div.Card__media a div.Card__cover img::attr(src)").extract_first()

            if (imgG2a is None):
                imgG2a = "http://www.womenshealthapta.org/wp-content/plugins/wp-blog-manager-lite/images/no-image-available.png"

            if ("Steam Key" in nameG2a):
                nameG2a = re.sub(r' Steam Key.*', "", nameG2a)
            if ("Key Steam" in nameG2a):
                nameG2a = re.sub(r' Key Steam.*', "", nameG2a)
            yield {
                'nameG2a': nameG2a,
                'priceG2a': game.css("div.Card__body div.Card__price span.Card__price-cost::text").extract_first(),
                'linkG2a': response.urljoin(game.css("a::attr(href)").extract_first()),
                'imgG2a': imgG2a
            }
        # Goes to next item on the list with the links, so the crawler goes to the next page
        self.i +=1
        next_page = response.urljoin(response.css("nav.pagination a.btn-next::attr(href)").extract_first())
        if (self.i <= 818):
            next_page = next_page
            yield scrapy.Request(next_page, callback=self.parse, dont_filter = True)


