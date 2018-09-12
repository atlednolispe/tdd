import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 3)

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        """
        即使测试报错也会执行,但如果setUp报错便不会执行
        """
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        rows = self.wait.until(
            # Firefox: presence/visibility: tag: tr会有奇怪的问题
            # StaleElementReferenceException
            EC.presence_of_all_elements_located((By.XPATH, '//tr'))
        )

        self.assertIn(
            row_text,
            (row.text for row in rows),
            f'"{row_text}" did not appear in table')
