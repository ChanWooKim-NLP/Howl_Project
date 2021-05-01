from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import csv

# 중국 / 네이버 뉴스 외교파트 (하위파트 중 국방외교 부분) /
#
# 한 페이지 당 10개 존재
# 크롤링 갯수를 우선 한 페이지 대상, 인기 댓글 5개 씩 추출

options = Options()
# options.headless = True
driver = webdriver.Chrome(options=options)

driver.implicitly_wait(5)

search_word = input('검색어 입력 : ')

driver.get(f'https://search.naver.com/search.naver?where=news&query={search_word}')

class Crawler:
    # 원하는 갯수 받으면 그만큼 크롤링 반복하도록 해주세요.
    def __init__(self, target_num):
        self.target_num = target_num # 목표 크롤링 개수
        self.ar_per_page = 0 # 한 페이지에서 접근한 기사 (이 변수가 10이 되면 초기화를 하고 다시 10개를 긁고...)
        self.page = 1 # 기사 페이지, 1페이지부터 시작
        self.comment_list, self.like_list = [], []

    def Crawling(self):
        count = 0
        while True:
            count += 1
            if self.ar_per_page == 10:
                print('다음 페이지로 넘어갑니다.')
                self.page += 1
                next_page = driver.find_element_by_xpath(f'//*[@id="main_pack"]/div[2]/div/div/a[{self.page}]')
                next_page.click()
                self.ar_per_page = 0

            try:
                site = driver.find_element_by_xpath(f'// *[ @ id = "sp_nws{count}"] / div[1] / div / div[1] / div / a[2]')
                site.click()

                driver.switch_to.window(driver.window_handles[-1])  # 열린 탭으로 이동
                #sleep(3)

                #### 이 부분에 댓글 크롤링 기능 추가하면 됩니다. ###

                driver.close()
                driver.switch_to.window(driver.window_handles[-1])  # 닫힌 탭으로 이동
                self.ar_per_page += 1

            except:
                continue

        print('크롤링 완료')
        driver.quit()

        return self.comment_list, self.like_list

    # csv로 변환해주는 함수 추가 부탁드립니다.


crawl = Crawler(100)
crawl.Crawling()
