import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import random
import time



class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["olx.in"]
    start_urls = ["https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723"]

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def start_requests(self):
        driver = webdriver.Chrome()  
        for url in self.start_urls:
            crawlbase_url = f"https://api.crawlbase.com/?token=_JS_TOKEN_&url=https%3A%2F%2Fgithub.com%2Fcrawlbase%3Ftab%3Drepositories"
            yield SeleniumRequest(
                url=crawlbase_url,
                callback=self.parse,
                wait_time=15,
                meta={'driver': driver}
            )

    def parse(self, response):
        driver = response.request.meta['driver']
        if not driver:
            self.logger.error('No driver found in response meta.')
            return
        
        wait = WebDriverWait(driver, 30)

        while True:
            # Extract property links on the current page
            property_links = response.css('li[data-aut-id="itemBox"] a::attr(href)').extract()
            for link in property_links:
                yield response.follow(link, self.parse_property)
                time.sleep(random.uniform(1, 3))

            try:
                load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-aut-id="btnLoadMore"]')))
                
                if load_more_button:
                    self.logger.info('Found "Load More" button. Clicking...')
                    driver.execute_script("arguments[0].click();", load_more_button)
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-aut-id="itemBox"]')))
                else:
                    self.logger.info('No more items to load.')
                    break
            except NoSuchElementException as nse:
                self.logger.error(f'No more "Load More" button found: {nse}')
                break

    def parse_property(self, response):
        yield {
            'property_name': response.css('h1[data-aut-id="itemTitle"]::text').get(),
            'property_id': response.css('div._1-oS0 ::text')[-2].get(),
            'breadcrumbs': response.css('a._26_tZ::text').getall(),
            'amount': response.css('span[data-aut-id="itemPrice"]::text').get(),
            'image_url': response.css('figure img::attr(src)').get(),
            'description': response.css('div[data-aut-id="itemDescriptionContent"] p::text').get(),
            'seller_name': response.css('div.eHFQs::text').get(),
            'location': response.css('div._3Uj8e span::text').get(),
            'property_type': response.css('span[data-aut-id="value_type"] ::text').get(),
            'bathrooms': response.css('span[data-aut-id="value_rooms"] ::text').get(),
            'bedrooms': response.css('span[data-aut-id="value_bathrooms"] ::text').get(),
        }
