
from bs4 import BeautifulSoup
import csv
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://everytime.kr/")

# filename = "에브리타임.csv"
# f = open(filename, "w", encoding="utf-8-sig", newline="")
# writer = csv.writer(f)

soup = BeautifulSoup(driver.page_source, "lxml")

#로그인
elem = driver.find_element_by_link_text("로그인")
elem.click()

id = driver.find_element_by_name('userid')
id.send_keys('gpdnjs0809') # 자신의 아이디 입력
id = driver.find_element_by_name('password')
id.send_keys('passe135!') # 자신의 비밀번호 입력
id.send_keys(Keys.RETURN)

# 페이지가 로드되기 전 크롤러가 먼저 클릭하는 현상 방지
time.sleep(2.5)

#시사이슈 페이지 클릭
elem = driver.find_element_by_link_text("시사·이슈")
elem.click()

#검색
search_word = input('검색어 입력 : ')
driver.get(f'https://everytime.kr/482580/all/{search_word}')

#이 부분부터 잘 모르겠습니다
#찾은 article갯수만큼 title, content, vote 크롤링
articles = driver.find_elements_by_class_name("article")

for article in articles:
    title = driver.find_element_by_class_name("medium")
    contents = driver.find_element_by_class_name("small")
    vote = driver.find_element_by_class_name("vote")
    
    print(f"제목 : {title}")
    print(f"내용 : {contents}")
    print(f"공감 : {vote}")
