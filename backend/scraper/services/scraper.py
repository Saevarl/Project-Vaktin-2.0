from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self, headless=True):
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=self.chrome_options)
    
    def get_page_source(self, url, wait_condition=(By.TAG_NAME, 'body'), timeout=30, retries=3):
        """
        Retrieve page source from the given URL.
        
        Parameters:
        - url: str, URL to scrape.
        - wait_condition: tuple, Selenium locator for the element to wait for before scraping.
        - timeout: int, max time to wait for the page to load (default: 30 seconds).
        - retries: int, number of retry attempts if page doesn't load as expected (default: 3).
        
        Returns:
        - page_source: str, HTML source of the page.
        """
        self.wait = WebDriverWait(self.driver, timeout)
        
        for attempt in range(retries):
            try:
                self.driver.get(url)
                # Wait for the specified condition before grabbing the page source
                self.wait.until(EC.presence_of_element_located(wait_condition))
                # Retrieve the page source after the condition is met
                page_source = self.driver.page_source
                return page_source
            except Exception as e:
                if attempt == retries - 1:
                    raise e  # Raise the exception if final retry fails
                print(f"Retrying... attempt {attempt + 1}")

    def scroll_page(self, pixels=1000):
        """
        Scrolls the page by a specified number of pixels to trigger lazy loading or additional content.
        
        Parameters:
        - pixels: int, number of pixels to scroll down (default: 1000).
        """
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        
    def close_driver(self):
        """
        Closes the WebDriver instance.
        """
        self.driver.quit()

# Usage example
# scraper = Scraper()
# page_source = scraper.get_page_source('https://example.com', wait_condition=(By.ID, 'content'), timeout=40)
# scraper.close_driver()
