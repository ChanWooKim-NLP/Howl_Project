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
    def __init__(self, num):
        self._count = 1 # 크롤링할 기사 개수
        self._num = num # 무시
        self._comment, self._like = [], [] # 댓글하고 좋아요 수를 저장할 리스트
        self.ar_per_page = 0 # 한 페이지에서 접근한 기사 (이 변수가ㅓ 10이 되면 초기화를 하고 다시 10개를 긁고...)

    def com_crawl(self):
        #while self._num != len(self._comment): # 원하는 갯수를 얻을 때 까지 반복
        for count in range(1, 11):
            try:
                site = driver.find_element_by_xpath(f'// *[ @ id = "sp_nws{count}"] / div[1] / div / div[1] / div / a[2]')
                site.click()

                driver.switch_to.window(driver.window_handles[-1])  # 열린 탭으로 이동
                sleep(1)

                comment = driver.find_elements_by_class_name('u_cbox_contents') # 댓글을 한꺼번에 크롤링
                like = driver.find_elements_by_class_name('u_cbox_cnt_recomm') # 좋아요수를 한꺼번에 크롤링

                comment = [c.text for c in comment]
                like = [n.text for n in like]

                self._comment.extend(comment)
                self._like.extend(like)

                driver.close()
                driver.switch_to.window(driver.window_handles[-1])  # 닫힌 탭으로 이동

                self.ar_per_page += 1

            except:
                continue

        print('크롤링 완료')
        driver.quit()

        return self._comment, self._like

c = Crawler(10)
result = c.com_crawl()
print(list(zip(*result)), len(list(zip(*result))))

with open('result.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in list(zip(*result)):
        writer.writerow(i)