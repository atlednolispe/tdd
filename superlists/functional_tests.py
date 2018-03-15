from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('/Applications/FirefoxDeveloperEdition.app/Contents/MacOS/firefox')
browser = webdriver.Firefox(firefox_binary=binary, executable_path='/usr/local/bin/geckodriver')  # browser = webdriver.Chrome()

browser.get('http://127.0.0.1:8000')

assert 'Django' in browser.title

print("browser's title:", browser.title)

import django
print("django's version:", django.__version__)

browser.quit()
