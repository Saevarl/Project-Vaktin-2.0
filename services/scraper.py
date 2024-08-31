from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

class Scraper:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def get_page_source(self, url):
        self.driver.get(url)
        page_source = self.driver.page_source
        return page_source

    def close_driver(self):
        self.driver.quit()
    
