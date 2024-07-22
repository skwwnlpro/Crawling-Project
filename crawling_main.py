import requests
from bs4 import BeautifulSoup
import time
import random
import csv
from datetime import datetime


def get_reviews(store_name):
    url = f"https://search.naver.com/search.naver?query={store_name}&where=view"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    reviews = []
    blog_posts = soup.find_all("a", class_="title_link")
    for post in blog_posts[:10]:
        reviews.append(post.text.strip()[:20])
    return reviews


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

# CSV 파일명 설정 (현재 날짜와 시간 포함)
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"restaurant_reviews_{current_time}.csv"

# CSV 파일 생성 및 데이터 쓰기
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        [
            "가게이름",
            "리뷰1",
            "리뷰2",
            "리뷰3",
            "리뷰4",
            "리뷰5",
            "리뷰6",
            "리뷰7",
            "리뷰8",
            "리뷰9",
            "리뷰10",
        ]
    )

    for store in stores:
        print(f"\n{store}의 리뷰 수집 중...")
        reviews = get_reviews(store)
        if reviews:
            # CSV에 데이터 쓰기
            row = (
                [store] + reviews + [""] * (10 - len(reviews))
            )  # 빈 리뷰는 빈 문자열로 채움
            csv_writer.writerow(row)

            # 콘솔에 출력
            for review in reviews:
                print(review)
        else:
            # 리뷰가 없는 경우
            csv_writer.writerow([store] + [""] * 10)
            print("리뷰를 찾을 수 없습니다.")

        time.sleep(1)  # 랜덤 대기 시간

print(f"\n리뷰 수집 완료. 결과가 {csv_filename} 파일에 저장되었습니다.")
