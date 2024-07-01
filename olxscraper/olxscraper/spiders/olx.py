import scrapy


class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["olx.in"]
    start_urls = ["https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723"]

    def parse(self, response):
        property_links = response.css('li[data-aut-id="itemBox"] a::attr(href)').extract()
        for link in property_links:
            yield response.follow(link, self.parse_property)
        
        next_page = response.css('a[data-aut-id="btnLoadMore"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_property(self, response):
            yield {
                'property_name': response.css('h1[data-aut-id="itemTitle"]::text').get(),
                'property_id': response.css('div._1-oS0 ::text')[-2].get(),
                'breadcrumbs': response.css('a._26_tZ::text').extract(),
                'amount': response.css('span[data-aut-id="itemPrice"]::text').get(),
                'image_url': response.css('figure img::attr(src)').get(),
                'description': response.css('div[data-aut-id="itemDescriptionContent"] p::text').get(),
                'seller_name': response.css('div.eHFQs::text').get(),
                'location': response.css('div._3Uj8e span::text').get(),
                'property_type': response.css('span[data-aut-id="value_type"] ::text').get(),
                'bathrooms': response.css('span[data-aut-id="value_rooms"] ::text').get(),
                'bedrooms': response.css('span[data-aut-id="value_bathrooms"] ::text').get(),
             }
