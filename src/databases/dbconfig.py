import pymysql
import pymysql.cursors
import yaml


# DB Config를 받아서 직접 연결
# 데이터를 받아서 실제 DB에 쿼리 실행하는 메소드들 모음
class DBConfig:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.connection = self.create_connection()

    # YAML 파일 읽기
    def load_config(self, config_file):
        with open(config_file, "r") as file:
            return yaml.safe_load(file)

    # YAML 파일에서 읽은 설정 사용
    def create_connection(self):
        return pymysql.connect(
            host=self.config["database"]["host"],
            user=self.config["database"]["user"],
            password=self.config["database"]["password"],
            db=self.config["database"]["db"],
            charset=self.config["database"]["charset"],
            cursorclass=getattr(
                pymysql.cursors, self.config["database"]["cursorclass"]
            ),
        )

    # 가게 이름 넣기
    def insert_restaurant(self, title):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO Restaurant (title) VALUES (%s)"
            cursor.execute(sql, (title,))
            self.connection.commit()

    # 가게 ID에 대한 블로그 제목/내용
    def insert_review(
        self, restaurant_id, title, contents, blog_start_time, blog_end_time
    ):
        # Contents 내용 길이 확인
        if len(contents) > 100:
            raise ValueError("Contents must be 100 characters or less.")

        with self.connection.cursor() as cursor:
            sql = "INSERT INTO Blog (restaurant_id, title, contents, blog_start_time, blog_end_time) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(
                sql, (restaurant_id, title, contents, blog_start_time, blog_end_time)
            )
            self.connection.commit()

    def get_restaurants(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT restaurant_id, title FROM Restaurant"
            cursor.execute(sql)
            return cursor.fetchall()

    def update_review_status(self, link, status):
        with self.connection.cursor() as cursor:
            sql = "UPDATE Blog SET status = %s WHERE link = %s"
            cursor.execute(sql, (status, link))
            self.connection.commit()

    def close_connection(self):
        self.connection.close()
