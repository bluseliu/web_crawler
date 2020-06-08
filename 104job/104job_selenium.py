"""
使用selenium, 爬104人力銀行任意關鍵字
將公司名稱、職缺、所需技能存成excel檔
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
from bs4 import BeautifulSoup
import json
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from time import sleep
import openpyxl
from openpyxl import Workbook

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'br, gzip, deflate',
    'Host': 'www.104.com.tw',
    'Accept-Language': 'zh-tw',
    'Referer': 'https://www.104.com.tw/job/6psyi?jobsource=jolist_b_relevance',
    'Connection': 'keep-alive',
    'Cookie': 'luauid=1767450017; __asc=42c43cc9171dd6b413bc1891199; __auc=42c43cc9171dd6b413bc1891199; _gid=GA1.3.10201509.1588557726; _hjid=7738c069-bac6-4995-ae3d-b56af90ff98e; ALGO_EXP_6019=C; job_same_ab=2; lup=1767450017.4623532291991.5035849152215.1.4640712161167; lunp=5035849152215; TS016ab800=01180e452d7a1007d2684447c6533f8bdf007c67e917a91a364e61c8596583923c6380c78feb31b165fa4a327f7821f58ef490cc859a00c84fc0db914f65a13597ece0845407141c37d78fe2e5871da87fa505b17d; _ga=GA1.1.195299847.1588557726; _ga_W9X1GB1SVR=GS1.1.1588557726.1.1.1588558057.60; _ga_FJWMQR9J2K=GS1.1.1588557726.1.1.1588558057.0'}

# 輸入關鍵字
seachword = input('請輸入要查詢的字串: ') # python爬蟲, blockchain

# 使用 selenium
driver = Chrome('/Users/willy/Documents/python_works/web_crawler/chromedriver')
url = 'https://www.104.com.tw/jobs/main/'

driver.get(url)
driver.find_element_by_id('ikeyword').send_keys("") # 清除搜尋輸入框中的內容
driver.find_element_by_id('ikeyword').send_keys(seachword) # 在搜尋輸入框中輸入關鍵字
driver.find_element_by_id('ikeyword').send_keys(Keys.RETURN) # 觸發搜尋輸入框的 ENTER 指令
sleep(2)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") # 滾輪到第1頁最下方
sleep(3)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # 滾輪到第2頁最下方
joblist_url = driver.current_url # joblist頁的網址
# print(joblist_url)

# 製作檔案及建立欄位名稱
column_name = ['公司名稱', '公司網址', '職務名稱', '職務網址', '接受身份', '工作經歷', '學歷要求', '科系要求',
               '語文條件', '擅長工具', '工作技能', '其他條件']

excel_file = Workbook() # 建立一個空白活頁簿
sheet = excel_file.active # 選取正在使用的sheet
sheet.append(column_name) # 建立欄位名稱
filename = '104_' + seachword + '_selenium.xlsx' # 設定檔名: 104_python爬蟲_selenium.xlsx
excel_file.save(filename)
excel_file.close()

# 總頁數
res = requests.get(joblist_url, headers=headers)
totalPage_soup = BeautifulSoup(res.text, 'html.parser')
totalPage_locate = str(totalPage_soup.select('body[class="job-list-body"] script')[3]).find('totalPage')
totalPage = str(totalPage_soup.select('body[class="job-list-body"] script')[3])[totalPage_locate + 11 :].split(',')[0]

# 各joblist頁網頁
for page in range(1, int(totalPage)+1):
    page_location = joblist_url.find('page') # page的位置
    joblist_url = joblist_url[:page_location + 5] + str(page) + joblist_url[page_location + 6 :]
    # print(joblist_url)

# 獲取job頁實際網址
    res = requests.get(joblist_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('div[class="b-block__left"] a[class="js-job-link"]')
    for link in range(0, len(links)):
        try:
            link = links[link]['href'].split('/')[4].split('?')[0]
            real_url = 'https://www.104.com.tw/job/ajax/content/' + link  # 內容有工作條件的url
            # print(real_url)

# 爬取職缺頁所有條件
            res = requests.get(real_url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser').decode('utf8')
            js = json.loads(res.text)
            # print(js)

        except:
            pass

# 各欄位
## 接受身份
        acceptRole_list = []
        acceptRole_origin = js["data"]["condition"]["acceptRole"]['role']
        for n in range(0, len(acceptRole_origin)):
            acceptRole_all = acceptRole_origin[n]['description']
            acceptRole_list.append(acceptRole_all)
        acceptRole = ','.join(acceptRole_list)

## 科系要求
        major = '無' if js["data"]["condition"]["major"] == [] else ','.join(js["data"]["condition"]["major"])

## 語文條件
        language = []
        language_origin = js["data"]["condition"]["language"]
        for n in range(0, len(language_origin)):
            language_a = language_origin[n]['language']
            language_b = language_origin[n]['ability']
            language_all = language_a + ':' + language_b
            language.append(language_all)

        language = '無' if language == [] else ','.join(language)

## 擅長工具
        specialty = []
        specialty_origin = js["data"]["condition"]["specialty"]
        for n in range(0, len(specialty_origin)):
            specialty_all = specialty_origin[n]['description']
            specialty.append(specialty_all)

        specialty = '無' if specialty == [] else ','.join(specialty)

## 工作技能
        skill = []
        skill_origin = js["data"]["condition"]["skill"]
        for n in range(0, len(skill_origin)):
            skill_all = skill_origin[n]['description']
            skill.append(skill_all)

        skill = '無' if skill == [] else ','.join(skill)

## 其他條件
        other = '無' if js["data"]["condition"]["other"] == '' else ','.join(js["data"]["condition"]["other"].split())

# 定義value名稱
        company_name = js["data"]["header"]["custName"]
        company_url = js["data"]["header"]["custUrl"]
        job_name = js["data"]["header"]["jobName"]
        job_url = real_url
        workExp = js["data"]["condition"]["workExp"]
        edu =  js["data"]["condition"]["edu"]

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

# 存成Excel檔
        openpyxl.load_workbook(filename)
        sheet = excel_file.active  # 選取正在使用的sheet
        sheet.append(list(job_content.values()))
        excel_file.save(filename)
        excel_file.close()

driver.close()
print(filename, '已寫入')


# 學習:
"""
-如果是滾輪到頁面最下方時自動產生第2頁, driver.execute_script是到第一頁的最下方
-用join將list轉成str, 例: a = ['上班族', '應屆畢業生'] ; a_list = ','.join(a) -> 上班族,應屆畢業生
-openpyxl對Excel的修改不是即時, 當寫入一筆後, 游標還會在原位置, 再寫入就會覆蓋, 所以要先存檔才會往下寫
"""



"""
# 將所需欄位轉成DataFrame
        job_content = [company_name, company_url, job_name, job_url, acceptRole, workExp, edu, major, language, specialty, skill, other]
        columns = ['公司名稱', '公司網址', '職務名稱', '職務網址', '接受身份', '工作經歷', '學歷要求', '科系要求', '語文條件', '擅長工具', '工作技能', '其他條件']
        index = ''

        df = DataFrame(job_content, columns=columns, index=index)
        print(df)
"""
