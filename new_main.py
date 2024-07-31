from restaurantreview import RestaurantReview


def main():
    # YAML 파일 경로
    config_file = "db_config.yml"

    # 드라이버 버전 직접 명시
    chrome_version = "126.0.6478.182"

    restaurant_list_url = "https://product.kyobobook.co.kr/detail/S000001865118"

    scrap = RestaurantReview(config_file, chrome_version)

    # Step 1: Scrape and store restaurant list
    scrap.scrape_and_store_restaurants(restaurant_list_url)

    # Step 2: Scrape and store reviews for each restaurant
    scrap.scrape_and_store_reviews()

    scrap.cleanup()


if __name__ == "__main__":
    main()
