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

# 로그인
elem = driver.find_element_by_link_text("로그인")
elem.click()

id = driver.find_element_by_name('userid')
id.send_keys('')  # 자신의 아이디 입력
id = driver.find_element_by_name('password')
id.send_keys('')  # 자신의 비밀번호 입력
id.send_keys(Keys.RETURN)

# 페이지가 로드되기 전 크롤러가 먼저 클릭하는 현상 방지
time.sleep(2.5)

# 시사이슈 페이지 클릭
elem = driver.find_element_by_link_text("시사·이슈")
elem.click()

# 검색
search_word = input('검색어 입력 : ')
#driver.get(f'https://everytime.kr/482580/all/{search_word}')

keyword = driver.find_element_by_xpath('//*[@id="searchArticleForm"]/input')
keyword.send_keys(search_word)
keyword.send_keys(Keys.RETURN)





class Crawler:
    def __init__(self, num):
        self._count = 1
        self._num = num
        self._title, self._content, self._like = [], [], []
        self._comment = []
        #self._comment_like = []
        self._ar_per_page = 0

    def com_crawl(self):
        for count in range(1, 11):
            # 페이지가 불러오는 텀이 있어야함
            time.sleep(0.5)
            # 검색 결과 중 10개의 글의 제목, 내용, 좋아요 크롤링
            # 이부분이 잘 동작하지 않는것같습니다.

            article = driver.find_element_by_xpath(f'//*[@id="container"]/div[2]/article[{count}]')
            article.click()
            time.sleep(1)


            # 글을 누른 다음 댓글, 댓글의 좋아요 크롤링 (댓글의 좋아요까진 안해도 될 것 같아요..!)
            # 일단은 가장 윗 댓글 크롤링([1])

            # 김찬우 : large라는 클래스 이름에 제목, 게시글, 댓글이 전부 들어있음
            # 게시글 좋아요만 뽑고 댓글 좋아요는 뽑지 마세요
            # 처음이 제목, 두번째 리스트 요소가 게시글 내용
            like = driver.find_element_by_class_name('vote')
            title = driver.find_element_by_xpath('// *[ @ id = "container"] / div[2] / article / a / h2').text
            content = driver.find_element_by_xpath('// *[ @ id = "container"] / div[2] / article / a / p').text
            comment_list = []

            comment_count = 1
            # 댓글 하나하나씩 크롤링하여 임시 리스트에 추가
            while True:
                try:
                    comment = driver.find_element_by_css_selector(f'#container > div.wrap.articles > article > div > article:nth-child({comment_count}) > p')
                    comment_list.append(comment.text)
                    print(comment_list)
                    comment_count += 1
                except:
                    break

            self._title.append(title) # 제목
            self._content.append(content) # 게시물
            self._comment.append(comment_list) # 댓글
            self._like.append(like)

            #글을 누른 다음 목록으로 돌아가기 위하여 아래의 '글목록' 누름
            # 셀레니움 뒤로가기
            driver.back()

            self._ar_per_page += 1

        print('크롤링 완료')
        driver.quit()

        return self._title, self._content, self._comment


c = Crawler(10)
result = c.com_crawl()
print(result)

print(list(zip(*result)), len(list(zip(*result))))

with open('result.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    for i in list(zip(*result)):
        writer.writerow(i)
