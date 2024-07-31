import pymysql
import pymysql.cursors
import yaml


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

    def insert_restaurant(self, title):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO Restaurant (title) VALUES (%s)"
            cursor.execute(sql, (title,))
            self.connection.commit()

    def insert_review(self, restaurant_id, title, contents):
        # Contents 내용 길이 확인
        if len(contents) > 100:
            raise ValueError("Contents must be 100 characters or less.")

        with self.connection.cursor() as cursor:
            sql = (
                "INSERT INTO Blog (restaurant_id, title, contents) VALUES (%s, %s, %s)"
            )
            cursor.execute(sql, (restaurant_id, title, contents))
            self.connection.commit()

    def get_restaurants(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT restaurant_id, title FROM Restaurant"
            cursor.execute(sql)
            return cursor.fetchall()

    def close_connection(self):
        self.connection.close()
