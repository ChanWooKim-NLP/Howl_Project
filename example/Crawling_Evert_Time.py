# 로그인 기능만 구현
# https://hufs.everytime.kr/login 에서 로그인 이후엔 https://hufs.everytime.kr/ 사이트로 이동, 추가적인 조작 필요

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get('https://hufs.everytime.kr/login')

#로그인
id = driver.find_element_by_name('userid')
id.send_keys('') # 자신의 아이디 입력
id = driver.find_element_by_name('password')
id.send_keys('') # 자신의 비밀번호 입력
id.send_keys(Keys.RETURN)

# 페이지가 로드되기 전 크롤러가 먼저 클릭하는 현상 방지
time.sleep(2.5)




