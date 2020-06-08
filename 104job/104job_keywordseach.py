"""
爬104人力銀行任意關鍵字
將公司名稱、職缺、所需技能整理成CSV儲存
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
import os
from urllib import request
from bs4 import BeautifulSoup
import json
import csv

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'br, gzip, deflate',
    'Host': 'www.104.com.tw',
    'Accept-Language': 'zh-tw',
    'Referer': 'https://www.104.com.tw/job/6psyi?jobsource=jolist_b_relevance',
    'Connection': 'keep-alive',
    'Cookie': 'luauid=1767450017; __asc=42c43cc9171dd6b413bc1891199; __auc=42c43cc9171dd6b413bc1891199; _gid=GA1.3.10201509.1588557726; _hjid=7738c069-bac6-4995-ae3d-b56af90ff98e; ALGO_EXP_6019=C; job_same_ab=2; lup=1767450017.4623532291991.5035849152215.1.4640712161167; lunp=5035849152215; TS016ab800=01180e452d7a1007d2684447c6533f8bdf007c67e917a91a364e61c8596583923c6380c78feb31b165fa4a327f7821f58ef490cc859a00c84fc0db914f65a13597ece0845407141c37d78fe2e5871da87fa505b17d; _ga=GA1.1.195299847.1588557726; _ga_W9X1GB1SVR=GS1.1.1588557726.1.1.1588558057.60; _ga_FJWMQR9J2K=GS1.1.1588557726.1.1.1588558057.0'}

# 使用關鍵字網址
seachword = input('請輸入要查詢的字串: ') # 資料科學家, 爬蟲工程師

# 製作檔案及建立欄位名稱
os.chdir(r'/Users/willy/Documents/python_works/web_crawler/104job')
filename = '104_' + seachword + '.csv'
with open(filename, 'a', newline='') as csvFile: # 開啟輸出的 CSV 檔案
    writer = csv.writer(csvFile) # 建立 CSV 檔寫入器
    writer.writerow(['公司名稱', '公司網址', '職務名稱', '職務網址', '接受身份', '工作經歷', '學歷要求',
                     '科系要求', '語文條件', '擅長工具', '工作技能', '其他條件'])

# 總頁數
# page_url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=資料科學家&order=14&asc=0&page=2&mode=s&jobsource=2018indexpoc'
page_url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=' + seachword + '&order=14&asc=0&page=2&mode=s&jobsource=2018indexpoc'
res = requests.get(page_url, headers=headers)
totalPage_soup = BeautifulSoup(res.text, 'html.parser')
totalPage_locate = str(totalPage_soup.select('body[class="job-list-body"] script')[3]).find('totalPage')
totalPage = str(totalPage_soup.select('body[class="job-list-body"] script')[3])[totalPage_locate + 11 :].split(',')[0]

# joblist頁網址
for page in range(1, int(totalPage)+1):
    # url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=資料科學家&order=14&asc=0&page=' + str(page) + '&mode=s&jobsource=2018indexpoc'
    url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=' + seachword + '&order=14&asc=0&page=' + str(page) + '&mode=s&jobsource=2018indexpoc'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

# 獲取job頁實際網址
    links = soup.select('div[class="b-block__left"] a[class="js-job-link"]')
    for link in range(0, len(links)):
        link = links[link]['href'].split('/')[4].split('?')[0]
        real_url = 'https://www.104.com.tw/job/ajax/content/' + link  # 內容有工作條件的url
        # print(real_url)

# 爬取職缺頁所有條件
        res = requests.get(real_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser').decode('utf8').split(' ')
        js = json.loads(res.text)
        # print(js)

# 各欄位
## 接受身份
        acceptRole = []
        acceptRole_origin = js["data"]["condition"]["acceptRole"]['role']
        for n in range(0, len(acceptRole_origin)):
            acceptRole_all = acceptRole_origin[n]['description']
            acceptRole.append((acceptRole_all))

## 科系要求
        major = '無' if js["data"]["condition"]["major"] == [] else js["data"]["condition"]["major"]

## 語文條件
        language = []
        language_origin = js["data"]["condition"]["language"]
        for n in range(0, len(language_origin)):
            language_a = language_origin[n]['language']
            language_b = language_origin[n]['ability']
            language_all = language_a + ':' + language_b
            language.append((language_all))

        language = '無' if language == [] else language

## 擅長工具
        specialty = []
        specialty_origin = js["data"]["condition"]["specialty"]
        for n in range(0, len(specialty_origin)):
            specialty_all = specialty_origin[n]['description']
            specialty.append((specialty_all))

        specialty = '無' if specialty == [] else specialty

## 工作技能
        skill = []
        skill_origin = js["data"]["condition"]["skill"]
        for n in range(0, len(skill_origin)):
            skill_all = skill_origin[n]['description']
            skill.append((skill_all))

        skill = '無' if skill == [] else skill

## 其他條件
        other = '無' if js["data"]["condition"]["other"] == '' else js["data"]["condition"]["other"].split()

# 將所需欄位整理成dict
        job_content = {
            '公司名稱': js["data"]["header"]["custName"],
            '公司網址': js["data"]["header"]["custUrl"],
            '職務名稱': js["data"]["header"]["jobName"],
            '職務網址': real_url,
            '接受身份': acceptRole,
            '工作經歷': js["data"]["condition"]["workExp"],
            '學歷要求': js["data"]["condition"]["edu"],
            '科系要求': major,
            '語文條件': language,
            '擅長工具': specialty,
            '工作技能': skill,
            '其他條件': other
        }

        print(job_content)

# 存檔
        with open(filename, 'a', newline='') as csvFile: # 開啟輸出的 CSV 檔案
            writer = csv.writer(csvFile) # 建立 CSV 檔寫入器
            writer.writerow([job_content.get('公司名稱'), job_content.get('公司網址'), job_content.get('職務名稱'),
                             job_content.get('職務網址'), job_content.get('接受身份'), job_content.get('工作經歷'),
                             job_content.get('學歷要求'), job_content.get('科系要求'), job_content.get('語文條件'),
                             job_content.get('擅長工具'), job_content.get('工作技能'), job_content.get('其他條件')
                             ])
print(filename, '已寫入')


# 學習:
"""
-headers只有user-agent無法抓到職務頁的資料, 把Headers中的Request都加進去即可抓到
-若內容為json, 用json.loads提取出來
-提取list中的dic: listname[0]['dictkey']
-可用空的list將迴圈整合在一起
-if...else寫成一行: 成立 if 條件 else 不成立
"""
