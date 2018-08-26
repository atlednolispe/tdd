import unittest

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.binary = FirefoxBinary('/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox')
        self.firefox_options = FirefoxOptions()
        self.firefox_options.headless = True
        self.browser = webdriver.Firefox(
            firefox_binary=self.binary,
            executable_path='/usr/local/bin/geckodriver',
            # options=self.firefox_options,
        )
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 3)

    def tearDown(self):
        """
        即使测试报错也会执行,但如果setUp报错便不会执行
        """
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        rows = self.wait.until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, 'tr'))
        )
        self.assertIn(
            row_text,
            (row.text for row in rows),
            f'"{row_text}" did not appear in table')

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jack Ma听说有一个很酷炫的在线To-Do-List应用,他去访问了一下首页看一下情况。
        self.browser.get('http://127.0.0.1:8000')

        # 他发现了网页的标签页和标题含有"To-Do"
        self.assertIn('To-Do', self.browser.title)
        header_text = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        ).text
        self.assertIn('To-Do', header_text)

        # 应用邀请他输入一个To-Do-List
        input_box = self.wait.until(
            EC.presence_of_element_located((By.ID, 'id_new_item'))
        )
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item')

        # 他在一个文本框输入了"收购饿了吗"
        input_box.send_keys("收购饿了吗")

        # 他输入回车后页面更新了
        # 待办事项表格中显示"1: 收购饿了吗"
        input_box.send_keys(Keys.ENTER)

        # import ipdb; ipdb.set_trace()
        self.check_for_row_in_list_table('1: 收购饿了吗')

        # 他还要邀请PaoLu Jia下周回国聊一聊
        # 页面又显示了一个文本框,可以输入其它待办事项
        # 他输入了"邀请PaoLu Jia下周回国"
        # Jack Ma做事节奏感很强
        input_box = self.wait.until(
            EC.presence_of_element_located((By.ID, 'id_new_item'))
        )
        input_box.send_keys("邀请PaoLu Jia下周回国")
        input_box.send_keys(Keys.ENTER)

        # 页面再次更新,他的To-Do-List中显示了这两个待办事项
        self.check_for_row_in_list_table('1: 收购饿了吗')
        self.check_for_row_in_list_table('2: 邀请PaoLu Jia下周回国')

        # Jack想知道这个网站是否能记住他的事项清单
        # 他看到网站为他生成了一个唯一的URL
        # 页面中还有一些文字解说这个功能

        # 他访问了这个URL,发现他的To-Do-List还在

        # Jack表示非常happy,表示他非常后悔尝试了这个应用,让他难以入睡。

        self.fail('Finish the test!')  # 无论如何都会抛异常


if __name__ == '__main__':
    unittest.main()
