# * 웹 크롤링 동작
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
webdriver_manager_directory = ChromeDriverManager().install()
import time
# ChromeDriver 실행
import pandas as pd 
from selenium.webdriver.chrome.options import Options

from pymongo import MongoClient  
import os 

def venture_doctors():
        crawling_count = 0
        mongo_url = os.getenv("DATABASE_URL")
        mongo_client = MongoClient(mongo_url)
        # database 연결
        database = mongo_client["news_scraping"]
        # collection 작업
        collection = database['venture_doctors']
        # Chrome 브라우저 옵션 생성
        chrome_options = Options()

        # User-Agent 설정
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

        # WebDriver 생성
        webdriver_manager_dricetory = ChromeDriverManager().install()

        browser = webdriver.Chrome(service = ChromeService(webdriver_manager_directory), options=chrome_options)                        # - chrome browser 열기

        # Chrome WebDriver의 capabilities 속성 사용
        capabilities = browser.capabilities

        pass
        browser.get("https://infose.info21c.net/info21c/bids/list/index?bidtype=ser&bid_suc=bid&division=1&mode=&searchtype=condition&page=1&pageSize=100&bid_kind=&conlevel=&searchWord=&word_type=&sort=-writedt&detailSearch=&search_code%5B%5D=&search_code%5B%5D=&search_code%5B%5D=&search_loc%5B%5D=&search_local%5B%5D=&search_loc%5B%5D=&search_local%5B%5D=&search_loc%5B%5D=&search_local%5B%5D=&date_column=writedt&from_date=2024-10-06&to_date=2024-11-06&price_column=basic&from_price=&to_price=&search_org=&word_column=constnm&word=isp&apt_vw=N&sortList=-writedt")                                     # - 주소 입력

                                                        # - 가능 여부에 대한 OK 받음
        pass
        html = browser.page_source                          # - html 파일 받음(and 확인)
        # print(html)

        from selenium.webdriver.common.by import By          # - 정보 획득
        time.sleep(1)
        id_input = browser.find_element(by=By.CSS_SELECTOR,value='#id')
        infose_id = os.getenv("infose_id")
        infose_password = os.getenv("infose_password")

        id_input.send_keys(infose_id)
        password_input = browser.find_element(by=By.CSS_SELECTOR,value='#pass')
        password_input.send_keys(infose_password)
        login_btn = browser.find_element(by=By.CSS_SELECTOR,value='#login_btn')
        login_btn.click()
        time.sleep(2)
        notice_elements = browser.find_elements(by=By.CSS_SELECTOR,value='#w0 > table > tbody > tr > td:nth-child(2) > a')
        notice_titles = []
        notice_list = []
        for i in range(len(notice_elements)):
                notice_elements = browser.find_elements(by=By.CSS_SELECTOR,value='#w0 > table > tbody > tr > td:nth-child(2) > a')
                notice_title = i.text
                if notice_title not in notice_titles: 
                        notice_elements[i].click()
                        time.sleep(1)
                        notice_id = browser.find_element(by=By.CSS_SELECTOR,value='#basicInfo > table > tbody > tr:nth-child(1) > td:nth-child(4)').text
                        notice_price = browser.find_element(by=By.CSS_SELECTOR,value='#basicInfo > table > tbody > tr:nth-child(7) > td:nth-child(4) > b').text
                        notice_start_date = browser.find_element(by=By.CSS_SELECTOR,value='body > div:nth-child(4) > div > div.contents > div.left-content > table > tbody > tr:nth-child(3) > td:nth-child(4)').text
                        notice_end_date = browser.find_element(by=By.CSS_SELECTOR,value='body > div:nth-child(4) > div > div.contents > div.left-content > table > tbody > tr:nth-child(4) > td:nth-child(2) > span').text
                        publishing_agency = browser.find_element(by=By.CSS_SELECTOR,value='#basicInfo > table > tbody > tr:nth-child(3) > td:nth-child(4)').text
                        requesting_agency = browser.find_element(by=By.CSS_SELECTOR,value='#basicInfo > table > tbody > tr:nth-child(4) > td:nth-child(2)')
                        notice_link = browser.find_element(by=By.CSS_SELECTOR,value='#contentBid > table > tbody > tr:nth-child(2) > td > span:nth-child(2)').get_attribute('href')
                        dict_notice = {'notice_id':notice_id,'notice_title':notice_title.text,'publishing_agency':publishing_agency,'requesting_agency':requesting_agency,'notice_start_date':notice_start_date,'notice_end_date':notice_end_date,'notice_link':notice_link}
                        notice_list.append(dict_notice)
                        file_list = browser.find_elements(by=By.CSS_SELECTOR,value='#contentBid > table > tbody > tr:nth-child(1) > td > ul > li > a')
                        for j in file_list:
                                j.click()
        browser.quit()                                      # - 브라우저 종료
venture_doctors()
