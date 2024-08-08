from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class WebCrawler:
    # 드라이버 버전 초기화
    def __init__(self, chrome_version):
        """initiation Driver Version
        Selenium 웹드라이버 초기화
        """
        self.service = Service(ChromeDriverManager(chrome_version).install())
        self.options = self.set_chrome_options()
        self.browser = webdriver.Chrome(service=self.service, options=self.options)

    # Selenium 옵션 설정
    def set_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        return chrome_options

    def get_page_content(self, url):
        self.browser.get(url)
        return self.browser.page_source

    def find_element(self, by, value):
        return self.browser.find_element(by, value)

    def find_elements(self, by, value):
        return self.browser.find_elements(by, value)

    def switch_to_frame(self, frame_reference):
        self.browser.switch_to.frame(frame_reference)

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def close_browser(self):
        self.browser.quit()
