from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
# 크롤링할 댓글 리스트
comments_list = []

# 초기 화면 접근
driver.get('https://search.daum.net/search?w=news&q=%EC%A4%91%EA%B5%AD&DA=PGD&spacing=0&p=1')

count = 1  # 페이지 당 뉴스 기사 개수
page_num = 0 # 현재 페이지


'''
10개 기사의 댓글을 가져오면...
//*[@id="newsColl"]/div[4]/span/span[2]/a[ '1' ] -> 2페이지 이동
//*[@id="newsColl"]/div[4]/span/span[2]/a[ '2' ] -> 3페이지 이동
//*[@id="newsColl"]/div[4]/span/span[2]/a[ '3' ]  이런식으로 a[]의 값이 1 씩 증가
'''

'''
페이지가 10을 넘기면 자동으로 웹페이지 상 다음 페이지로 접근할 수 있는 버튼 증가함
따라서 페이지를 일일이 링크에 입력하기 보단 버튼 클릭을 자동화시켜 for문을 줄일 수 있음
아래 주의사항 참고 부탁드립니다.
'''
while True:
    if count == 11:
        count = 1
        page_num += 1
        page = driver.find_element_by_xpath(f'// *[ @ id = "newsColl"] / div[4] / span / span[2] / a[{page_num}]')
        page.click()

    # 다음뉴스 접근
    link = driver.find_element_by_xpath(f'//*[@id="clusterResultUL"]/li[{count}]/div[2]/div/span[1]/a')
    link.click()
    driver.switch_to.window(driver.window_handles[-1])  # 열린 탭으로 이동

    sleep(2)
    # comment = driver.find_elements_by_class_name('desc_txt font_size_17')
    # comment = [c.text for c in comment]

    # comment_list.extend(comment)


    driver.close()
    driver.switch_to.window(driver.window_handles[-1])  # 검색결과 탭으로 이동

    count += 1
'''
//*[@id="clusterResultUL"]/li[2]/div[2]/div/span[1]/a : 중국 군용기, 4일 연속 대만 향해 무력 시위
//*[@id="clusterResultUL"]/li[3]/div/div/span[1]/a : 농협금융, 중국 북경지점 예비인가
//*[@id="clusterResultUL"]/li[4]/div[2]/div/span[1]/a : 중국, 건강코드 상호 인증...
11시 53분 기준 2페이지 이 부분 간 html 코드의 구조가 일치하지 않음
따라서 예외처리를 통해 오류가 나는 부분을 그냥 통과하도록 추가하면 해결 가능
'''
