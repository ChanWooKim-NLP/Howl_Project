# -*- coding: utf-8 -*-
"""
Created on Tue May  4 16:38:02 2021

@author: 장준호
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import csv



options = Options()
options.headless = True
driver = webdriver.Chrome("C:\\Users\\장준호\\Desktop\\chromedriver.exe")

driver.implicitly_wait(5)

search_word = input('검색어 입력: ')

driver.get(f'https://search.naver.com/search.naver?where=news&query={search_word}')
counting_comments = int(input())

class Crawler:
    # 원하는 갯수 받으면 그만큼 크롤링 반복하도록 해주세요.
    def __init__(self, target_num):
        self.target_num = target_num # 목표 크롤링 개수
        self.ar_per_page = 0 # 한 페이지에서 접근한 기사 (이 변수가 10이 되면 초기화를 하고 다시 10개를 긁고...)
        self.page = 1 # 기사 페이지, 1페이지부터 시작
        self.comment_list, self.like_list = [], []

    def Crawling(self):
        count = 0
        while len(self.comment_list) < counting_comments :
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
                

                #### 이 부분에 댓글 크롤링 기능 추가하면 됩니다. ###
                comment_list = driver.find_elements_by_class_name('u_cbox_contents')
                like_list = driver.find_elements_by_class_name('u_cbox_cnt_recomm')

                comment_list = [c.text for c in comment_list]
                like_list = [n.text for n in like_list]

                self.comment_list.extend(comment_list)
                self.like_list.extend(like_list)

                driver.close()
                driver.switch_to.window(driver.window_handles[-1])  # 닫힌 탭으로 이동

                self.ar_per_page += 1

            except:
                continue
        print("크롤링 완료")
        driver.quit()
        
        return self.comment_list, self.like_list
        #csv로 변환해주는 함수 추가 부탁드립니다. 
        
crawl = Crawler(10)
result = crawl.Crawling()
print(list(zip(*result)), len(list(zip(*result))))

f = open(f'{search_word}.csv', 'w', encoding = 'utf-8', newline = '') 
csvWriter = csv.writer(f)
for i in list(zip(*result)):
    csvWriter.writerow(i)

f.close()    
print('문서 생성 완료')     
            
            
            
            
            
            
