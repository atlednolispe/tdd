from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

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
