from webdriver_manager.chrome import ChromeDriverManager

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
config_file = "Crawling-Project/db_config.yml"

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
stores = [
    "명동교자",
    "옛날민속집 본점",
    "만족 오항족발",
    "쟈니덤플링",
    "미즈컨테이너",
    "마코토",
    "을밀대",
    "혜화돌쇠아저씨",
    "우래옥",
    "바토스",
    "오율",
    "마리쿡",
    "청솔나무",
    "지하손만두",
    "초마",
    "삼청동수제비",
    "토속촌 삼계탕",
    "대원갈비",
    "청담돈가",
    "윤씨밀방",
    "바바인디아",
    "육회자매집",
    "청진옥",
    "하카다분코",
    "모모코",
    "툭툭누들타이",
    "귀족족발",
    "테이스팅룸 이태원점",
    "이문설농탕",
    "리틀사이공",
    "활화산 조개구이 칼국수",
    "홍스쭈꾸미",
    "어부와백정 영등포 본점",
    "아이해브어드림",
    "필동면옥",
    "대장장이화덕피자",
    "부자피자",
    "미진",
    "단",
    "서부면옥",
    "고상",
    "역전회관",
    "마론키친앤바",
    "더함",
    "새벽집",
    "떼아떼베네",
    "소프트리",
    "스테파니카페 2호점",
    "알리고떼",
    "연남 서서갈비",
    "대게나라 방이점",
    "올리아 키친 앤 그로서리",
    "서울서 둘째로 잘하는 집",
    "노블카페 강남점",
    "황소고집",
    "참설농탕 송파본점",
    "우노",
    "순희네빈대떡",
    "을지면옥",
    "돈코보쌈",
    "애플하우스",
    "봉우화로",
    "메리고라운드 신천점",
    "패션 5",
    "버터핑거팬케이크",
    "우대가",
    "성수족발",
    "마도니셰프 명동점",
    "노블카페 가로수길점",
    "먹쉬돈나 삼청동점",
    "부처스컷 청담",
    "군산오징어",
    "진주집",
    "웃사브",
    "미미네",
    "뿔레치킨 홍대본점",
    "남포면옥",
    "밀탑",
    "부첼라",
    "스시효 청담본점",
    "동빙고",
    "서린낙지",
    "오자오동 함흥냉면",
    "우성갈비",
    "평래옥",
    "피자힐",
    "호수삼계탕",
    "호우양꼬치",
    "마포 본점최대포",
    "비스떼까",
    "프로간장게장 본점",
    "피자리움",
    "마마스",
    "맛있는 교토 1호점",
    "영동왕족발",
    "커피스튜디오",
    "한일관 압구정본점",
    "계열사",
    "더 가든 키친",
    "더 스테이크 하우스",
]

url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={stores[0]}"
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
