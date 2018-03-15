from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('/Applications/FirefoxDeveloperEdition.app/Contents/MacOS/firefox')
browser = webdriver.Firefox(
    firefox_binary=binary,
    executable_path='/usr/local/bin/geckodriver'
)  # browser = webdriver.Chrome()

# Jack Ma听说有一个很酷炫的在线To-Do-List应用,他去访问了一下首页看一下情况。
browser.get('http://127.0.0.1:8000')

# 他发现了网页的标签页含有"To-Do"
assert 'To-Do' in browser.title, "Browser title was " + browser.title

# 应用邀请他输入一个To-Do-List

# 他在一个文本框输入了"收购饿了吗"
# 他还要邀请PaoLu Jia下周回国聊一聊

# 他输入回车后页面更新了
# 待办事项表格中显示"1: 收购饿了吗"

# 页面又显示了一个文本框,可以输入其它待办事项
# 他输入了"邀请PaoLu Jia下周回国"
# Jack Ma做事节奏感很强

# 页面再次更新,他的To-Do-List中显示了这两个待办事项

# Jack想知道这个网站是否能记住他的事项清单
# 他看到网站为他生成了一个唯一的URL
# 页面中还有一些文字解说这个功能

# 他访问了这个URL,发现他的To-Do-List还在

# Jack表示非常happy,表示他非常后悔尝试了这个应用,让他难以入睡。

browser.quit()
