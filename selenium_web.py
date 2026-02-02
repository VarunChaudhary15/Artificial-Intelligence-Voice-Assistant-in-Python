from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class infow:
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def get_info(self, query):
        print("Opening Wikipedia...")
        self.driver.get("https://www.wikipedia.org")

        # Correct search input box
        search = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
        search.send_keys(query)

        # Correct search button
        button = self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button')
        button.click()

        time.sleep(5)  # Wait to show result




# Keep browser open
input("Press ENTER to exit...")
