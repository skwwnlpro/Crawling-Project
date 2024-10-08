from databases.dbconfig import DBConfig
from web_crawler import WebCrawler
from restaurant_scraper import RestaurantScraper
from review_scraper import ReviewScraper
import time
from datetime import datetime


# 명시한 매소드들에 맞춰 DB에 데이터를 넣는 클래스로 전달
class RestaurantReview:
    def __init__(self, config_file, chrome_version):
        self.db_manager = DBConfig(config_file)
        web_crawler = WebCrawler(chrome_version)
        self.restaurant_scraper = RestaurantScraper(web_crawler)
        self.review_scraper = ReviewScraper(web_crawler)

    def scrape_and_store_restaurants(self, url):
        restaurants = self.restaurant_scraper.get_restaurant_list(url)
        for restaurant in restaurants:
            self.db_manager.insert_restaurant(restaurant)
        print(f"Added {len(restaurants)} restaurants to the database.")

    def scrape_and_store_reviews(self):
        restaurants = self.db_manager.get_restaurants()
        print(restaurants)
        for restaurant in restaurants:
            restaurant_id = restaurant["restaurant_id"]
            restaurant_title = restaurant["title"]
            print(f"Processing restaurant: {restaurant_title}")

            # 블로그 리뷰 수집 시작 시간 기록
            blog_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            blog_links = self.review_scraper.get_blog_links(restaurant_title)
            for link in blog_links:
                title, contents = self.review_scraper.get_blog_content(link)
                if title and contents:
                    # 블로그 리뷰 수집 완료 시간 기록
                    blog_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.db_manager.insert_review(
                        restaurant_id, title, contents, blog_start_time, blog_end_time
                    )
                time.sleep(1)

    def cleanup(self):
        self.review_scraper.web_crawler.close_browser()
        self.db_manager.close_connection()
