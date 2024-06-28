import scrapy


class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["olx.in"]
    start_urls = ["https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723"]

    def parse(self, response):
        property_links = response.css('li[data-aut-id="itemBox"] a._2cbZ2::attr(href)').extract()
        for link in property_links:
            yield response.follow(link, self.parse_property)
        
        next_page = response.css('a[data-aut-id="btnLoadMore"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
