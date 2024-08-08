from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from dbconfig import DBConfig


class ReviewScraper:
    def __init__(self, web_crawler):
        self.web_crawler = web_crawler

    def get_blog_links(self, restaurant):
        url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={restaurant}"
        self.web_crawler.get_page_content(url)
        try:
            link = self.web_crawler.find_element(By.CLASS_NAME, "iBUwB").get_attribute(
                "href"
            )
            self.web_crawler.get_page_content(link)
            self.web_crawler.switch_to_frame(
                self.web_crawler.find_element(By.ID, "entryIframe")
            )
            time.sleep(1)

            pages = self.web_crawler.find_elements(By.CLASS_NAME, "veBoZ")
            for i in pages:
                if i.text == "리뷰":
                    i.click()
                    break
            time.sleep(1)

            self.web_crawler.find_elements(By.CLASS_NAME, "YsfhA")[1].click()
            time.sleep(1)

            return [
                element.get_attribute("href")
                for element in self.web_crawler.find_elements(By.CLASS_NAME, "uUMhQ")[
                    :10
                ]
            ]
        except NoSuchElementException:
            print(f"요소를 찾을 수 없습니다: {restaurant}")
            return []

    def get_blog_content(self, link):
        self.web_crawler.get_page_content(link)
        try:
            self.web_crawler.switch_to_frame(
                self.web_crawler.find_element(By.ID, "mainFrame")
            )
            title = self.web_crawler.find_element(By.CLASS_NAME, "se-fs-").text
            content = self.web_crawler.find_element(
                By.CLASS_NAME, "se-main-container"
            ).text[:30]

            return title, content
        except Exception as e:
            print(f"Error getting blog content: {e}")
            return None, None
