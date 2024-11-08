from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os 
import time
import shutil
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def move_files_to_folder(src_folder, dest_folder):
    for file_name in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file_name)
        dest_file = os.path.join(dest_folder, file_name)
        if os.path.isfile(src_file):
            shutil.move(src_file, dest_file)

def notice_search(search_keyword,notice_list,notice_titles):
    # Chrome 브라우저 옵션 생성
    chrome_options = Options()

    # User-Agent 설정
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    # 다운로드 폴더 설정
    download_folder_path = os.path.abspath('C:/develops/bepet_scraping/notice_list')
    prefs = {
        'download.default_directory': download_folder_path,
        'download.prompt_for_download': False,
        'safebrowsing.enabled': True
    }
    chrome_options.add_experimental_option('prefs', prefs)

    # WebDriver 생성
    webdriver_manager_directory = ChromeDriverManager().install()
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory), options=chrome_options)
    browser_url = "https://infose.info21c.net/info21c/bids/list/index?bidtype=ser&bid_suc=bid&division=1&mode=&searchtype=condition&page=1&pageSize=100&bid_kind=&conlevel=&searchWord=&word_type=&sort=-writedt&detailSearch=&search_code%5B%5D=&search_code%5B%5D=&search_code%5B%5D=&search_loc%5B%5D=&search_local%5B%5D=&search_loc%5B%5D=&search_local%5B%5D=&search_loc%5B%5D=&search_local%5B%5D=&date_column=writedt&from_date=2024-10-06&to_date=2024-11-06&price_column=basic&from_price=&to_price=&search_org=&word_column=constnm&word={}&apt_vw=N&sortList=-writedt".format(search_keyword)
    browser.get(browser_url)                                     # - 주소 입력
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
    search_option = browser.find_element(by=By.CSS_SELECTOR,value='#conditionSearch')
    search_option.click()
    time.sleep(1)
    period_select = browser.find_element(by=By.CSS_SELECTOR,value='#condition_search_form > table > tbody > tr:nth-child(4) > td > div:nth-child(1) > div > button:nth-child(2)')
    period_select.click()
    search_btn = browser.find_element(by=By.CSS_SELECTOR,value='#conditionSearchBtn')
    search_btn.click()
    time.sleep(1)
    
    notice_elements = browser.find_elements(by=By.CSS_SELECTOR,value='#w0 > table > tbody > tr > td:nth-child(2) > a')
    for i in range(len(notice_elements)):
        notice_elements = browser.find_elements(by=By.CSS_SELECTOR,value='#w0 > table > tbody > tr > td:nth-child(2) > a')
        notice_title = notice_elements[i].text
        if notice_title not in notice_titles:
            notice_elements[i].click()
            folder_path = os.path.join(download_folder_path, notice_title)
            os.makedirs(folder_path, exist_ok=True)
            notice_id = browser.find_element(by=By.CSS_SELECTOR,value='#basicInfo > table > tbody > tr:nth-child(1) > td:nth-child(4)').text
            notice_price = browser.find_element(by=By.CSS_SELECTOR,value='#basicInfo > table > tbody > tr:nth-child(7) > td:nth-child(4) > b').text
            notice_start_date = browser.find_element(by=By.CSS_SELECTOR,value='body > div> div > div.contents > div.left-content > table > tbody > tr:nth-child(3) > td:nth-child(4)').text
            if notice_start_date != '':
                notice_start_date = datetime.strptime(notice_start_date, "%Y년 %m월 %d일 %H시 %M분")
                notice_start_date = notice_start_date.strftime("%Y/%m/%d %H:%M")
            notice_end_date = browser.find_element(by=By.CSS_SELECTOR,value='body > div > div > div.contents > div.left-content > table > tbody > tr:nth-child(4) > td:nth-child(2) > span').text
            if notice_end_date != '':
                notice_end_date = datetime.strptime(notice_end_date, "%Y년 %m월 %d일 %H시 %M분")
                notice_end_date = notice_end_date.strftime("%Y/%m/%d %H:%M")
            publishing_agency = browser.find_element(by=By.CSS_SELECTOR,value='#basicInfo > table > tbody > tr:nth-child(3) > td:nth-child(4)').text.split('\n')[-1]
            requesting_agency = browser.find_element(by=By.CSS_SELECTOR,value='#basicInfo > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.split('\n')[-1]
            try:
                notice_link = browser.find_element(by=By.CSS_SELECTOR,value='#contentBid > table > tbody > tr:nth-child(2) > td > span:nth-child(2)')
                onclick_text = notice_link.get_attribute("onclick")
                bid_id = onclick_text.split("g2bBidLink('")[1].split("'")[0]
                notice_link = 'https://www.g2b.go.kr/pt/menu/selectSubFrame.do?framesrc=/pt/menu/frameTgong.do?url=https://www.g2b.go.kr:8101/ep/invitation/publish/bidInfoDtl.do?bidno='+bid_id
            except:
                try:
                    notice_link = browser.find_element(by=By.CSS_SELECTOR,value='#contentBid > table > tbody > tr > td > button')
                    onclick_attribute = notice_link.get_attribute("onclick")
                    # onclick 속성에서 링크 추출
                    start_index = onclick_attribute.find("http")
                    end_index = onclick_attribute.find("')", start_index)
                    notice_link = onclick_attribute[start_index:end_index]
                except:
                    notice_link = browser.find_element(by=By.CSS_SELECTOR,value='#contentBid > table > tbody > tr > td > a').get_attribute('href')
                pass
            dict_notice = {'notice_id':notice_id,'notice_title':notice_title,'notice_price':notice_price,'publishing_agency':publishing_agency,'requesting_agency':requesting_agency,'notice_start_date':notice_start_date,'notice_end_date':notice_end_date,'notice_link':notice_link}
            notice_list.append(dict_notice)
            file_list = []
            file_list = browser.find_elements(by=By.CSS_SELECTOR,value='#contentBid > table > tbody > tr:nth-child(1) > td > ul > li > a')
            for j in range(len(file_list)):
                file_list = browser.find_elements(by=By.CSS_SELECTOR,value='#contentBid > table > tbody > tr:nth-child(1) > td > ul > li > a')
                browser.execute_script("arguments[0].scrollIntoView();", file_list[j]) 
                time.sleep(1)
                file_list[j].click()
                time.sleep(2)
            move_files_to_folder(download_folder_path, folder_path)    
            back_btn = browser.find_element(by=By.CSS_SELECTOR, value='#top_wrap > div.top_btn > div.top-left_btn.pull-left > span')
            back_btn.click()
            time.sleep(1)
    browser.quit()
    return notice_list
def move_folders_without_hwp(src_folder,notice_list):
    # check_list 폴더 경로 설정
    dest_folder = os.path.join(src_folder, 'check_list')
    # check_list 폴더가 없으면 생성
    os.makedirs(dest_folder, exist_ok=True)
    check_list = []
    # 공고 폴더들 탐색
    for folder_name in os.listdir(src_folder):
        folder_path = os.path.join(src_folder, folder_name)
        
        # 공고 폴더인지 확인 (check_list 폴더는 제외)
        if os.path.isdir(folder_path) and folder_name not in ['ai_notice_list', 'check_list','delete_list']:
            # 해당 폴더 안의 파일들 탐색
            has_hwp_file = False
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith('.hwp'):
                    has_hwp_file = True
                    break            
            # hwp 파일이 없으면 check_list로 이동
            if not has_hwp_file:
                for notice in notice_list:
                    if notice['notice_title'] == folder_name:
                        notice['type'] = 'check'
                        check_list.append(notice)
                        break
                dest_path = os.path.join(dest_folder, folder_name)
                shutil.move(folder_path, dest_path)
    return notice_list,check_list
import os
import shutil
import olefile
import zlib
import struct

def get_hwp_text(filename):
    try:
        with olefile.OleFileIO(filename) as f:
            dirs = f.listdir()

            # HWP 파일 검증
            if ["FileHeader"] not in dirs or ["\x05HwpSummaryInformation"] not in dirs:
                print("Not a valid HWP file.")
                return None

            # 문서 포맷 압축 여부 확인
            header = f.openstream("FileHeader")
            header_data = header.read()
            is_compressed = (header_data[36] & 1) == 1

            # Body Sections 불러오기
            nums = []
            for d in dirs:
                if d[0] == "BodyText":
                    nums.append(int(d[1][len("Section"):]))
            sections = ["BodyText/Section" + str(x) for x in sorted(nums)]

            # 전체 text 추출
            text = ""
            for section in sections:
                bodytext = f.openstream(section)
                data = bodytext.read()
                if is_compressed:
                    unpacked_data = zlib.decompress(data, -15)
                else:
                    unpacked_data = data

                # 각 Section 내 text 추출    
                section_text = ""
                i = 0
                size = len(unpacked_data)
                while i < size:
                    header = struct.unpack_from("<I", unpacked_data, i)[0]
                    rec_type = header & 0x3ff
                    rec_len = (header >> 20) & 0xfff

                    if rec_type in [67]:
                        rec_data = unpacked_data[i+4:i+4+rec_len]
                        section_text += rec_data.decode('utf-16', errors='ignore')
                        section_text += "\n"

                    i += 4 + rec_len

                text += section_text
                text += "\n"

            return text
    except Exception as e:
        return None


def search_keywords_in_hwp(file_name,file_path, keywords):
    """HWP 파일 내에 특정 키워드가 포함되어 있는지 확인"""
    text = get_hwp_text(file_path)
    if text:
        for keyword in keywords:
            if keyword in text:
                print("파일명 : ", file_name)
                print("키워드 : ", keyword)
                return True
    return False

def move_folders_with_keywords(src_folder, keywords,notice_list):
    """공고 폴더 내 HWP 및 PDF 파일에서 키워드 검색 후 해당 폴더 이동"""
    # ai_notice_list 폴더 경로 설정
    dest_folder = os.path.join(src_folder, 'ai_notice_list')
    os.makedirs(dest_folder, exist_ok=True)
    ai_notice_list = []

    for folder_name in os.listdir(src_folder):
        folder_path = os.path.join(src_folder, folder_name)
        
        # 폴더인지 확인 (ai_notice_list 및 check_list 폴더는 제외)
        if os.path.isdir(folder_path) and folder_name not in ['ai_notice_list', 'check_list','delete_list']:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if file_name.lower().endswith('.hwp'):
                    if search_keywords_in_hwp(file_name,file_path, keywords):
                        for notice in notice_list:
                            if notice['notice_title'] == folder_name:
                                ai_notice_list.append(notice)
                                notice['type'] = 'ai_notice'
                                break
                        time.sleep(1)
                        dest_path = os.path.join(dest_folder, folder_name)
                        shutil.move(folder_path, dest_path)                        
                        break
    return notice_list,ai_notice_list
                    
def move_folder_to_delete(src_folder,notice_list):
    dest_folder = os.path.join(src_folder, 'delete_list')
    os.makedirs(dest_folder, exist_ok=True)
    for folder_name in os.listdir(src_folder):
        folder_path = os.path.join(src_folder, folder_name)        
        # 폴더인지 확인 (ai_notice_list 및 check_list 폴더는 제외)
        if os.path.isdir(folder_path) and folder_name not in ['ai_notice_list', 'check_list','delete_list']:
            for notice in notice_list:
                if notice['notice_title'] == folder_name:
                    notice['type'] = 'delete'
                    break
            dest_path = os.path.join(dest_folder, folder_name)
            shutil.move(folder_path, dest_path)                        
    return notice_list

import json

def load_notice_titles_from_json(file_path):
    # JSON 파일에서 notice_title만 추출하여 리스트로 반환
    with open(file_path, 'r', encoding='utf-8') as json_file:
        notice_list = json.load(json_file)
    
    notice_titles = [notice['notice_title'] for notice in notice_list]
    return notice_titles


import json
import os

def save_notice_list_to_json(notice_list, file_path):
    """
    JSON 파일에 공지 목록을 저장합니다. 기존 내용이 있다면 추가합니다.

    Args:
        notice_list: 저장할 공지 목록 (list)
        file_path: 저장할 JSON 파일 경로 (str)
    """

    if os.path.exists(file_path):
        # 파일이 이미 존재하는 경우, 기존 내용을 읽어옵니다.
        with open(file_path, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
        # 기존 내용에 새로운 내용을 추가합니다.
        existing_data.extend(notice_list)
        # 업데이트된 내용을 다시 파일에 씁니다.
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
    else:
        # 파일이 없는 경우, 새로운 내용을 저장합니다.
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(notice_list, json_file, ensure_ascii=False, indent=4)


def g2b_notice_collection():
    src_folder = 'C:/develops/bepet_scraping/notice_list'
    keywords = ['AI', '인공지능', 'LLM','생성형']
    notice_list = []
    # 함수 호출
    notice_titles = load_notice_titles_from_json('C:/develops/bepet_scraping/notice_list.json')
    notice_list = notice_search('isp',notice_list,notice_titles)
    notice_list = notice_search('ismp',notice_list,notice_titles)
    notice_list,check_list = move_folders_without_hwp(src_folder,notice_list)
    notice_list,ai_notice_list = move_folders_with_keywords(src_folder, keywords,notice_list)
    notice_list = move_folder_to_delete(src_folder,notice_list)
    json_file_path = os.path.join('C:/develops/bepet_scraping/', 'notice_list.json')
    save_notice_list_to_json(notice_list, json_file_path)
    return ai_notice_list,check_list
