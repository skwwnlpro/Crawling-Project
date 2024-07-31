from dbconfig import DBConfig
from webcrawler import WebCrawler
from restaurantscraper import RestaurantScraper
from reviewscraper import ReviewScraper
import time


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
            blog_links = self.review_scraper.get_blog_links(restaurant_title)
            for link in blog_links:
                title, contents = self.review_scraper.get_blog_content(link)
                if title and contents:
                    self.db_manager.insert_review(restaurant_id, title, contents)
                time.sleep(1)

    def cleanup(self):
        self.review_scraper.web_crawler.close_browser()
        self.db_manager.close_connection()
