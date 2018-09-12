from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Jack Ma访问首页,不小心提交了一个空代办事项

        # 首页刷新了,显示了一共错误提示: 待办事项不能为空

        # 他输入了一些文字,再次提交,这次没问题

        # 他有点小调皮,又提交了一共空代办事项

        # 清单首页他看到了一共类似的错误消息

        # 输入文字后就没有问题
        self.fail('write me!')
