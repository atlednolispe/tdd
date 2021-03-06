from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Jack Ma访问首页,不小心提交了一个空代办事项
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # 首页刷新了,显示了一共错误提示: 待办事项不能为空
        # HTML default required verification
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # 他输入了一些文字,再次提交,这次没问题
        input_box = self.get_item_input_box()
        input_box.send_keys('我要准备退休啦!')
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: 我要准备退休啦!')

        # 他有点小调皮,又提交了一共空代办事项
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # 清单首页他看到了一共类似的错误消息
        self.check_for_row_in_list_table('1: 我要准备退休啦!')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # 输入文字后就没有问题
        input_box = self.get_item_input_box()
        input_box.send_keys('我要回去当老师!')
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('2: 我要回去当老师!')

    def test_cannot_add_duplicate_items(self):
        # Jack Ma访问首页,新建了一个清单
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('我要办个西湖大学\n')
        self.check_for_row_in_list_table('1: 我要办个西湖大学')

        # 他不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys('我要办个西湖大学\n')

        # 他看到一条有帮助的错误消息
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list")
