from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Browser:

    def __init__(self, url: str):
        self.url = url
        self.driver = None

    def start(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        self.driver.get(self.url)
        
    def get_driver(self):
        return self.driver
                                                                                                                                                                                    
    def close(self):
        if self.driver:
            self.driver.quit()