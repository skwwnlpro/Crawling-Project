from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pymysql
import pymysql.cursors
import yaml
import time
import re
from datetime import datetime

# YAML 파일 경로
# config_file = "Crawling-Project/db_config.yml"
#
# # YAML 파일 읽기
# with open(config_file, "r") as file:
#     config = yaml.safe_load(file)

# YAML 파일에서 읽은 설정 사용
# conn = pymysql.connect(
#     host=config["database"]["host"],
#     user=config["database"]["user"],
#     password=config["database"]["password"],
#     db=config["database"]["db"],
#     charset=config["database"]["charset"],
#     cursorclass=getattr(pymysql.cursors, config["database"]["cursorclass"]),
# )

# 드라이버 절대 경로
# chrome_driver_path = "C:\\Users\\Pro\\.wdm\\drivers\\chromedriver\\win64\\126.0.6478.182\\chromedriver-win32"

# 드라이버 버전 직접 명시
chrome_version = "126.0.6478.182"
service = Service(ChromeDriverManager(chrome_version).install())
# driver = webdriver.Chrome(service=service)

browser = webdriver.Chrome()
# browser.find_element(By.CLASS_NAME, "uU7dJb").text


# url = "https://www.google.com"
# browser.get(url)

# url = "https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber=1&pageSize=24"
# browser.get(url)

# 1페이지 링크 데이터 전부 수집
### 한 개의 베스트 셀러 링크 수집
# browser.find_element(By.CLASS_NAME, "gd_name").get_attribute("href")

# ### 1페이지 전체의 링크 데이터
# # browser.find_element(By.CLASS_NAME, "gd_name") # element: 요소
# dates = browser.find_elements(By.CLASS_NAME, "gd_name")  # elements: 리스트

# 가게 리스트 (일부만 표시)

url = 'https://product.kyobobook.co.kr/detail/S000001865118'
browser.get(url)
try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "book_contents_item"))
    )
    content = element.get_attribute('innerHTML')

    # <br> 태그를 기준으로 분할
    items = content.split('<br>')

    # 숫자와 공백을 제거하고 리스트에 추가
    restaurant_list = [re.sub(r'^\d+\s*', '', item.strip()) for item in items if item.strip()]

    print("Restaurant List:")
    for restaurant in restaurant_list:
        print(restaurant)

    print(f"\nTotal restaurants: {len(restaurant_list)}")

except Exception as e:
    print(f"An error occurred: {e}")

url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={restaurant_list[0]}"
browser.get(url)
a = browser.find_element(By.CLASS_NAME, "iBUwB").get_attribute("href")
browser.get(a)
# a = browser.find_element(By.CLASS_NAME, "S8peq").get_attribute("a href")
# iframe 전환, Click 대기 상태
browser.switch_to.frame(browser.find_element(By.ID, "entryIframe"))

# 창 대기
time.sleep(3)

# 리뷰
browser.find_elements(By.CLASS_NAME, "veBoZ")[3].click()

# 블로그 리뷰
browser.find_elements(By.CLASS_NAME, "YsfhA")[1].click()


# browser.find_element(By.CLASS_NAME, "gd_name").get_attribute("href")
# ### 1페이지 전체의 링크 데이터
# # browser.find_element(By.CLASS_NAME, "gd_name") # element: 요소
# dates = browser.find_elements(By.CLASS_NAME, "gd_name")  # elements: 리스트

# for i in dates:
#     link = i.get_attribute("href")
#     link_list.append(link)

# time.sleep(1)

# link_list = []
# for i in range(1, 4):
#     print("*" * 10, f"현재 {i} 페이지 수집 중 입니다.", "*" * 10)

#     url = f"https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber={i}&pageSize=24"
#     browser.get(url)

#     browser.find_element(By.CLASS_NAME, "gd_name").get_attribute("href")
#     ### 1페이지 전체의 링크 데이터
#     # browser.find_element(By.CLASS_NAME, "gd_name") # element: 요소
#     dates = browser.find_elements(By.CLASS_NAME, "gd_name")  # elements: 리스트

#     for i in dates:
#         link = i.get_attribute("href")
#         link_list.append(link)

#     time.sleep(1)

# print(link_list)

# try:
#     with conn.cursor() as cursor:
#         for link in link_list:
#             browser.get(link)

#             title = browser.find_element(By.CLASS_NAME, "gd_name").text
#             author = browser.find_element(By.CLASS_NAME, "gd_auth").text
#             publisher = browser.find_element(By.CLASS_NAME, "gd_pub").text

#             # 2024년 07월 12일 -> 2024-07-12
#             publishing = browser.find_element(By.CLASS_NAME, "gd_date").text

#             match = re.search(r"(\d+)년 (\d+)월 (\d+)일", publishing)

#             if match:
#                 year, month, day = match.groups()
#                 data_obj = datetime(int(year), int(month), int(day))
#                 publishing = data_obj.strftime("%Y-%m-%d")
#             else:
#                 publishing = "2024-07-01"

#             rating = browser.find_element(By.CLASS_NAME, "yes_b").text

#             review = browser.find_element(By.CLASS_NAME, "txC_blue").text
#             review = int(review.replace(",", ""))

#             sales = browser.find_element(By.CLASS_NAME, "gd_sellNum").text.split(" ")[2]
#             sales = int(sales.replace(",", ""))

#             price = browser.find_element(By.CLASS_NAME, "yes_m").text[:-1]
#             price = int(price.replace(",", ""))

#             full_text = browser.find_element(By.CLASS_NAME, "gd_best").text
#             parts = full_text.split(" | ")

#             if len(parts) == 1:
#                 ranking = 0
#                 ranking_weeks = 0
#             else:
#                 try:
#                     ranking_part = parts[0]
#                     ranking = "".join(filter(str.isdigit, ranking_part))  # 숫자만 추춢
#                 except:
#                     ranking = 0

#                 try:
#                     # 국내도서 top20 3주
#                     ranking_weeks_part = parts[1]
#                     ranking_weeks = "".join(
#                         filter(str.isdigit, ranking_weeks.split()[-1])
#                     )
#                 except:
#                     ranking_weeks = 0

#             # ranking = browser.find_element(By.CLASS_NAME, "gd_best").text.split(" | ")[0].split(" ")[2][:-1]

#             # ranking_weeks = browser.find_element(By.CLASS_NAME, "gd_best").text.split(" | ")[1].split(" ")[2][:-1]

#             sql = """INSERT INTO Books (
#                 title, author, publisher, publishing, rating, review, sales, price, ranking, ranking_weeks
#                 )
#                 VALUES(
#                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
#                 )
#                 """

#             cursor.execute(
#                 sql,
#                 (
#                     title,
#                     author,
#                     publisher,
#                     publishing,
#                     rating,
#                     review,
#                     sales,
#                     price,
#                     ranking,
#                     ranking_weeks,
#                 ),
#             )
#             conn.commit()
#             time.sleep(1)
# except Exception as e:
#     print(e)
