"""
爬取mobile01旅遊版文章
將各篇文章存成json檔
爬完後以LINE通知
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from urllib import request
from bs4 import BeautifulSoup
import os
from os import listdir
import time
import requests
import json
import random

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

# 列表 =====
area = {188:'基隆市', 189:'台北市', 190:'新北市', 191:'桃園市', 192:'新竹市', 193:'新竹縣', 209:'宜蘭縣'}
print(area.items())
# num = input('請輸入縣市代碼: ')

# for num in (188, 189, 190, 191, 192, 193, 209):
for num in (188, 189):

# 爬取列表
    url_p1 = 'https://www.mobile01.com/topiclist.php?f=' + str(num) # https://www.mobile01.com/topiclist.php?f=188
    req = request.Request(url=url_p1, headers=headers)
    res = request.urlopen(req)
    # print(res.read().decode('utf-8')) # 查看列表原始碼
    content_p1 = BeautifulSoup(res, 'html.parser')
    # print(content_p1)
    title_txt = content_p1.select('div[class="c-listTableTd__title"] a[class="c-link u-ellipsis"]')

# 總頁數
    total_pages = int(content_p1.select('div[class="l-navigation__item l-navigation__item--min"], a[class="c-pagination"]')[-1].text) +1

# 列表頁
    page = 1
    while page < total_pages:
        url = 'https://www.mobile01.com/topiclist.php?f=' + str(num) + '&p={0}'.format(page)
        # https://www.mobile01.com/topiclist.php?f=188&p=26
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        content_all = BeautifulSoup(res, 'html.parser')
        title_txt = content_all.select('div[class="c-listTableTd__title"] a[class="c-link u-ellipsis"]')

        print('開始爬取:', area.get(int(num)), 'page', page)

# 文章網址
        for n in range(0, len(title_txt)):
            url_back = str(title_txt[n]['href']).split('=')[-1]
            url_article = 'https://www.mobile01.com/topicdetail.php?f=' + str(num) + '&t='+ url_back  # 文章網址

# 文章內容
            req_con = request.Request(url=url_article, headers=headers)
            res_con = request.urlopen(req_con)
            soup_con = BeautifulSoup(res_con, 'html.parser')
            # print('soup_con:', soup_con)

            article_title = soup_con.select('div[class="l-heading__title"] h1[class="t2"] ')[0].text # 標題
            article_content = soup_con.select('div[itemprop="articleBody"] ')[0].text.strip().replace('\n', '') # 內文
            postdate = soup_con.select('span[class="o-fNotes o-fSubMini"]')[0].text # 發文日期

            total = {'文章網址':url_article,
                     '發文時間':postdate,
                     '標題':article_title,
                     '文章內容':article_content,
                     '縣市':area.get(int(num))
                     }

            total_json = json.dumps(total, ensure_ascii=False) # dict→str

# 判斷文章是否已存在
            path_dir = '/Users/willy/Documents/python_works/web_crawler/mobile01/travel'

            if not os.path.exists(path_dir):
                os.mkdir(path_dir)
            os.chdir(path_dir)

            save_filename = area.get(int(num)) + '_' + url_back + '.json' # 要儲存的檔名
            check_files = listdir(path_dir) # 檢查資料夾是否有此檔名
            if save_filename in check_files:
                print(area.get(int(num)), 'Page', page, 'of', total_pages-1, ' 檔案已存在...', '檔名:', save_filename)

# 存檔
            else:
                # f = open(area.get(int(num)) + '_' + url_back + '.json', mode='a', encoding='utf8')
                # f.write(total_json)
                print(area.get(int(num)), 'Page', page, 'of', total_pages-1, ' 存檔完成......', '標題:', article_title)

            time.sleep(random.randint(1, 3))
        page += 1

print('所有文章存檔完成!!! at', time.asctime())

# Line通知
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

message = 'Mobile01的所有文章存檔完成 at ', time.asctime() # 修改為你要傳送的訊息內容

f = open(r'/Users/willy/Documents/python_works/linetoken.txt')
f.readlines()
f.close()
token = os.environ.get("linetk") # 修改為你的權杖內容

lineNotifyMessage(token, message)


# 學習
"""
-使用.strip()及.replace(' ', '')去掉空格
-jason存取
 json.dumps()	dict→str
 json.dump()	dict→str，並寫入到json檔案中
 json.load()	從json檔案中讀取資料
 json.loads()	str→dict
-檢查資料夾是否有此檔名: listdir(pathname)
"""
