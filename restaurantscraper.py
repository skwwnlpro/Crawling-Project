from selenium.webdriver.common.by import By
import re

class RestaurantScraper:
    def __init__(self, web_crawler):
        self.web_crawler = web_crawler

    def get_restaurant_list(self, url):
        self.web_crawler.get_page_content(url)
        try:
            element = self.web_crawler.wait_for_element(
                By.CLASS_NAME, "book_contents_item"
            )
            content = element.get_attribute("innerHTML")
            items = content.split("<br>")
            return [
                re.sub(r"^\d+\s*", "", item.strip()) for item in items if item.strip()
            ]
        except Exception as e:
            print(f"An error occurred while getting restaurant list: {e}")
            return []
