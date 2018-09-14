from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jack Ma听说有一个很酷炫的在线To-Do-List应用,他去访问了一下首页看一下情况。
        self.browser.get(self.live_server_url)

        # 他发现了网页的标签页和标题含有"To-Do"
        self.assertIn('To-Do', self.browser.title)
        header_text = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        ).text
        self.assertIn('To-Do', header_text)

        # 应用邀请他输入一个To-Do-List
        input_box = self.get_item_input_box()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item')

        # 他在一个文本框输入了"收购饿了吗"
        input_box.send_keys("收购饿了吗")

        # 他输入回车后被带到一个新URL
        # 待办事项表格中显示"1: 收购饿了吗"
        input_box.send_keys(Keys.ENTER)

        # Firefox: current_url有延迟,需要添加time.sleep(0.5)
        jack_list_url = self.browser.current_url
        self.assertRegex(jack_list_url, '/lists/.+')

        self.check_for_row_in_list_table('1: 收购饿了吗')

        # 他还要邀请PaoLu Jia下周回国聊一聊
        # 页面又显示了一个文本框,可以输入其它待办事项
        # 他输入了"邀请PaoLu Jia下周回国"
        # Jack Ma做事节奏感很强
        input_box = self.get_item_input_box()
        input_box.send_keys("邀请PaoLu Jia下周回国")
        input_box.send_keys(Keys.ENTER)

        # 页面再次更新,他的To-Do-List中显示了这两个待办事项
        self.check_for_row_in_list_table('1: 收购饿了吗')
        self.check_for_row_in_list_table('2: 邀请PaoLu Jia下周回国')

        # Jack想知道这个网站是否能记住他的事项清单
        # 他看到网站为他生成了一个唯一的URL
        # 页面中还有一些文字解说这个功能

        # 他访问了这个URL,发现他的To-Do-List还在

        # 现在一个叫Pony Ma的新用户访问了网站

        # 我们使用一个新的浏览器会话
        # 确保Jack Ma的信息不会从cookies中泄露
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 3)

        # Pony Ma访问首页
        # 看不到Jack Ma的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('收购饿了吗', page_text)
        self.assertNotIn('邀请PaoLu Jia下周回国', page_text)

        # Pony Ma输入一个新To-Do,新建一个清单
        # 他不像Jack Ma那么感兴趣
        input_box = self.get_item_input_box()
        input_box.send_keys("入股斗鱼")
        input_box.send_keys(Keys.ENTER)

        # Pony Ma获得了他的唯一URL
        pony_list_url = self.browser.current_url
        self.assertRegex(pony_list_url, '/lists/.+')
        self.assertNotEqual(pony_list_url, jack_list_url)

        # 这个页面还是没有Jack Ma的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('收购饿了吗', page_text)
        self.assertNotIn('邀请PaoLu Jia下周回国', page_text)

        # 两人都很满意去睡觉了。
