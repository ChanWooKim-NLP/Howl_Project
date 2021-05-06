
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv

driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://everytime.kr/")

soup = BeautifulSoup(driver.page_source, "lxml")

#로그인
elem = driver.find_element_by_link_text("로그인")
elem.click()

id = driver.find_element_by_name('userid')
id.send_keys('') # 자신의 아이디 입력
id = driver.find_element_by_name('password')
id.send_keys('') # 자신의 비밀번호 입력
id.send_keys(Keys.RETURN)

# 페이지가 로드되기 전 크롤러가 먼저 클릭하는 현상 방지
time.sleep(2.5)

#시사이슈 페이지 클릭
elem = driver.find_element_by_link_text("시사·이슈")
elem.click()

#검색
search_word = input('검색어 입력 : ')
driver.get(f'https://everytime.kr/482580/all/{search_word}')

class Crawler:
    def __init__(self, num):
        self._count = 1
        self._num = num
        self._title, self._content, self._like = [], [], []
        # self._comment, self._comment_like = [], []
        self._ar_per_page = 0

    def com_crawl(self):
        for count in range(1, 11):
            #검색 결과 중 10개의 글의 제목, 내용, 좋아요 크롤링
            title = driver.find_elements_by_xpath(f'//*[@id="container"]/div[2]/article[{count}]/a/h2')
            content = driver.find_elements_by_xpath(f'//*[@id="container"]/div[2]/article[{count}]/a/p')                
            like = driver.find_elements_by_xpath(f'//*[@id="container"]/div[2]/article[{count}]/a/ul/li[2]')
            
            #이부분이 잘 동작하지 않는것같습니다. 
            # article = driver.find_element_by_xpath(f'//*[@id="container"]/div[2]/article[{count}]/a')
            # article.click()

            #글을 누른 다음 댓글, 댓글의 좋아요 크롤링 (댓글의 좋아요까진 안해도 될 것 같아요..!)
            #일단은 가장 윗 댓글 크롤링([1])
            # comment = driver.find_element_by_xpath('//*[@id="container"]/div[2]/article/div/article[1]/p')
            # comment_like = driver.find_element_by_xpath('//*[@id="container"]/div[2]/article/div/article[1]/ul[2]/li')
            
            title = [a.text for a in title]
            content = [b.text for b in content]
            like = [n.text for n in like]
            # comment = comment.text
            # comment_like = comment_like.text
                

            self._title.extend(title)
            self._content.extend(content)
            self._like.extend(like)
            # self._comment.extend(comment)
            # self._comment_like.extand(commend_like)

            #글을 누른 다음 목록으로 돌아가기 위하여 아래의 '글목록' 누름
            # back = driver.find_element_by_xpath('//*[@id="goListButton"]')
            # back.click()

            self._ar_per_page += 1

        print('크롤링 완료')
        driver.quit()

        return self._title, self._content, self._like

c = Crawler(10)
result = c.com_crawl()
print(list(zip(*result)), len(list(zip(*result))))

with open('result.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    for i in list(zip(*result)):
        writer.writerow(i)
