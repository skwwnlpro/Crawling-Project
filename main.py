from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pymysql
import pymysql.cursors
import yaml
import time
import re


# YAML 파일 경로
config_file = "./db_config.yml"

# YAML 파일 읽기
with open(config_file, "r") as file:
    config = yaml.safe_load(file)

# YAML 파일에서 읽은 설정 사용
conn = pymysql.connect(
    host=config["database"]["host"],
    user=config["database"]["user"],
    password=config["database"]["password"],
    db=config["database"]["db"],
    charset=config["database"]["charset"],
    cursorclass=getattr(pymysql.cursors, config["database"]["cursorclass"]),
)

# 드라이버 절대 경로
# chrome_driver_path = "C:\\Users\\Pro\\.wdm\\drivers\\chromedriver\\win64\\126.0.6478.182\\chromedriver-win32"

# 드라이버 버전 직접 명시
chrome_version = "126.0.6478.182"
service = Service(ChromeDriverManager(chrome_version).install())
# driver = webdriver.Chrome(service=service)


# Selenium 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

# Selenium 웹드라이버 초기화
browser = webdriver.Chrome(options=chrome_options)

# 가게 리스트 (일부만 표시)
url = "https://product.kyobobook.co.kr/detail/S000001865118"
browser.get(url)
try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "book_contents_item"))
    )
    content = element.get_attribute("innerHTML")

    # <br> 태그를 기준으로 분할
    items = content.split("<br>")

    # 숫자와 공백을 제거하고 리스트에 추가
    restaurant_list = [
        re.sub(r"^\d+\s*", "", item.strip()) for item in items if item.strip()
    ]

    print("Restaurant List:")
    for restaurant in restaurant_list:
        print(restaurant)

    print(f"\nTotal restaurants: {len(restaurant_list)}")

except Exception as e:
    print(f"An error occurred: {e}")
i = 0


for restaurant in restaurant_list:
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={'마코토'}"
    browser.get(url)
    try:
        link = browser.find_element(By.CLASS_NAME, "iBUwB").get_attribute("href")

        browser.get(link)
        # iframe 전환, Click 대기 상태
        browser.switch_to.frame(browser.find_element(By.ID, "entryIframe"))
        time.sleep(1)

        pages = browser.find_elements(By.CLASS_NAME, "veBoZ")
        # 리뷰
        for i in pages:
            if i.text == "리뷰":
                i.click()
                break
        time.sleep(2)

        # 블로그 리뷰
        browser.find_elements(By.CLASS_NAME, "YsfhA")[1].click()

        time.sleep(1)
        print("Test3")
        # 블로그 link 수집
        link_list = []
        for i in range(10):
            a = browser.find_elements(By.CLASS_NAME, "uUMhQ")[i].get_attribute("href")
            link_list.append(a)
            print(link_list[i])

    except NoSuchElementException as e:
        print("요소를 찾을 수 없습니다.")
        # print(e)
        with conn.cursor() as cursor:
            title = "가게 정보가 없습니다."
            content = "이하 동문"
            sql = """INSERT INTO Review (
            title, content
            )
            VALUES
                (%s, %s)
            """
            cursor.execute(
                sql,
                (
                    title,
                    content,
                ),
            )
            conn.commit()
        continue

    with conn.cursor() as cursor:

        # 10개 블로그에 대한 title, Content 수집
        for i in link_list:
            browser.get(i)

            # iframe 전환, Click 대기 상태
            browser.switch_to.frame(browser.find_element(By.ID, "mainFrame"))
            title = browser.find_element(By.CLASS_NAME, "se-fs-").text
            content = browser.find_element(By.CLASS_NAME, "se-main-container").text[:30]
            print(title)
            print(content)
            sql = """INSERT INTO Review (
            title, content
            )
            VALUES(
                %s, %s
            )
            """

            cursor.execute(
                sql,
                (
                    title,
                    content,
                ),
            )
            conn.commit()
            time.sleep(1)
