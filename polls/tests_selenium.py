from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class PollsUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Chrome 브라우저 열기 (자동화 모드)
        cls.browser = webdriver.Chrome()  
        # chromedriver 경로가 PATH에 있어야 함

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_homepage_has_title(self):
        """홈페이지에 '설문조사(polls)' 관련 텍스트가 있는지 
        확인"""
        self.browser.get(self.live_server_url + "/polls/")
        time.sleep(1)  
        # 페이지 로딩 대기 (학습 목적이므로 잠시 사용)

        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("poll", body.text.lower())  
        # 대소문자 무시하고 확인
