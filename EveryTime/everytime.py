from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv

options = Options()
options.add_argument('--start-fullscreen')

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

# #서울캠 자유게시판 클릭
# elem = driver.find_element_by_link_text("서울캠 자유게시판")
# elem.click()

#글로벌캠 자유게시판 클릭
elem = driver.find_element_by_link_text("글로벌캠 자유게시판")
elem.click()

#검색
search_word = input('검색어 입력 : ')
# driver.get(f'https://everytime.kr/370454/all/{search_word}') #서울캠
driver.get(f'https://everytime.kr/374012/all/{search_word}') #글로벌캠

class Crawler:
    def __init__(self, num):
        self._count = 1
        self._page = 1
        self._num = num
        self._title, self._content, self._like = [], [], []
        self._comment = []
        self._ar_per_page = 0

    def com_crawl(self):
        for page in range(1, 11): #10개의 페이지
            time.sleep(0.5)

            #20개의 글 크롤링 했으면 다음 클릭
            if self._ar_per_page == 20:
                # driver.get(f'https://everytime.kr/370454/all/%EC%A4%91%EA%B5%AD/p/{page}') #서울캠
                driver.get(f'https://everytime.kr/374012/all/%EC%A4%91%EA%B5%AD/p/{page}') #글로벌캠
                time.sleep(1)
            
            #초기화
            self._ar_per_page = 0

            for count in range(1, 21): #한 페이지당 20개의 글
                time.sleep(0.5)

                #게시글 클릭
                article = driver.find_element_by_xpath(f'//*[@id="container"]/div[2]/article[{count}]/a')
                article.click()
                time.sleep(1)

                #게시글의 제목, 내용, 좋아요 크롤링
                title = driver.find_element_by_xpath('//*[@id="container"]/div[2]/article/a/h2').text
                content = driver.find_element_by_xpath('//*[@id="container"]/div[2]/article/a/p').text
                like = driver.find_element_by_class_name('vote')
                
                #게시글의 댓글 크롤링
                comment_list = []
                comment_count = 1

                while True:
                    try:
                        comment = driver.find_element_by_css_selector(f'#container > div.wrap.articles > article > div > article:nth-child({comment_count}) > p')
                        comment_list.append(comment.text)
                        # print(comment_list)
                        comment_count += 1
                    except:
                        break
                print(comment_list)

                #'삭제된 댓글입니다.' 제외
                comment_list = [i for i in comment_list if i != "삭제된 댓글입니다."]

                self._title.append(title)
                self._content.append(content)
                self._like.append(like)
                self._comment.append(comment_list)

                driver.back()

                self._ar_per_page += 1

        print('크롤링 완료')
        driver.quit()

        return self._title, self._content, self._comment

c = Crawler(10)
result = c.com_crawl()
print(result)

print(list(zip(*result)), len(list(zip(*result))))

#result_seoul 파일 생성
# with open('result_seoul.csv', 'w', encoding='utf-8-sig', newline='') as f:
#     writer = csv.writer(f)
#     for i in list(zip(*result)):
#         writer.writerow(i)

#result_global 파일 생성
with open('result_global.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    for i in list(zip(*result)):
        writer.writerow(i)
