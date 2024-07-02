from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scrapy.utils.project import get_project_settings

def get_driver():
    settings = get_project_settings()
    service = Service(settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH'))
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(service=service, options=options)
    return driver
