from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.binary = FirefoxBinary('/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox')
        self.firefox_options = FirefoxOptions()
        self.firefox_options.headless = True
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 3)

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
        input_box = self.wait.until(
            EC.presence_of_element_located((By.ID, 'id_new_item'))
        )
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
        input_box = self.wait.until(
            EC.presence_of_element_located((By.ID, 'id_new_item'))
        )
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

    def test_layout_and_styling(self):
        # Jack Ma访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 他看到输入框完美
        input_box = self.wait.until(
            EC.presence_of_element_located((By.ID, 'id_new_item'))
        )
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        # 他新建了一个清单,看到输入框仍完美居中
        input_box.send_keys('testing\n')
        input_box = self.wait.until(
            EC.presence_of_element_located((By.ID, 'id_new_item'))
        )
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
