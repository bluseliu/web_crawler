"""
以關鍵字搜层PChome網站
將各產品資訊以json格式顯示
將資料存入MySQL
"""

# -*- coding: gbk -*-
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from bs4 import BeautifulSoup
import requests
import json
import time
import MySQLdb
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/13.1.1 Safari/605.1.15',
    'Cookie': 'ECC=9eb667a9b577246c547264373ed52dddfad64a5c.1592298978; _gcl_au=1.1.786593296.1592298982; gsite=24h; venguid=10c9a9c5-7baa-45b4-8cd9-a1a9816eb419.wg1-36wz20200616; vensession=d40a9e1a-fbdf-4901-9ced-b8f547208372.wg1-1n4020200616.se; _gid=GA1.3.1203920636.1592298984; uuid=xxx-0097aed4-a643-479e-a403-d10779d55185; _fbp=fb.2.1592298984461.413809676; puuid=K.20200616171624.3; U=43a3a3475f0e4dcbb2c71babbd12295839ac78f7; _ga=GA1.1.837176670.1592298982; _ga_9CE1X6J1FG=GS1.1.1592298981.1.1.1592299054.0; ECWEBSESS=4b852bae8a.7b98740f6acadf2a21d5bea4b98d4876b4d02d3b.1592299054'}

source = 'pchome'

keyword = 'LED數字時鐘'
# keyword = input('PLS input keyword: ') # switch 動物森友會 主機

prod_check = 0
keyword_url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=' + str(keyword) + '&page=1&sort=sale/dc'
print(keyword_url)
keyword_res = requests.get(url=keyword_url, headers=headers)
# soup = BeautifulSoup(keyword_res.text, 'html.parser').decode('utf-8')
keyword_js = json.loads(keyword_res.text)

# 總頁數
totalPage = int(keyword_js['totalPage']) + 1

# 列表頁js網址
for page in range(1, totalPage):
    keyword_js_url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=' + keyword + '&page=' + \
                     str(page) + '&sort=sale/dc'
    # print('keyword_js_url:', keyword_js_url)

# 列表頁各產品資訊
    list_res = requests.get(url=keyword_js_url, headers=headers)
    list_all = json.loads(list_res.text)['prods']
    for ids in range(0, len(list_all)):
        prod_id = list_all[ids].get('Id') # 產品編號
        prod_name = list_all[ids].get('name') # 產品名稱
        prod_url = 'https://24h.pchome.com.tw/prod/' + prod_id # 前台看到的url
        price = list_all[ids].get('price') # 產品價格
        prod_intropic = 'https://b.ecimg.tw/' + list_all[ids].get('picS') # 圖片連結

# 產品頁說明內容(中間)
        prod_js_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/prod/' + prod_id + '/intro&fields=Id,Pic,Pstn,Intro,Sort&_callback=jsonp_intro?_callback=jsonp_intro'
        res = requests.get(url=prod_js_url, headers=headers)
        prod_soup = BeautifulSoup(res.text, 'html.parser').text.replace('try', '').replace(
            ');}catch(e){if(window.console){console.log(e);}}', '').replace('{jsonp_intro(', '')
        prod_js = json.loads(prod_soup)
        prod_content = prod_js[prod_id]

        content = '' # 說明內容 + 圖片網址
        for n in range(0, len(prod_content)):
            intro = prod_content[n].get('Intro')
            prod_pic = 'https://f.ecimg.tw' + str(prod_content[n].get('Pic'))
            # print('intro:', intro)
            # print('prod_pic:', prod_pic)
            separate = ' '
            content += intro + separate + prod_pic
        # print('content:', content)

# 產品頁本商品規格(下方)
        spec_url = 'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/prod/' + prod_id + '/desc&fields=Id,Stmt,' \
                   'Equip,Remark,Liability,Kword,Slogan,Author,Transman,Pubunit,Pubdate,Approve&_callback=' \
                   'jsonp_desc?_callback=jsonp_desc'

        spec_res = requests.get(url=spec_url, headers=headers)
        spec_soup = BeautifulSoup(spec_res.text, 'html.parser').text.replace('try', '').replace('{jsonp_desc(', '')\
            .replace(');}catch(e){if(window.console){console.log(e);}}', '').replace('{jsonp_intro(', '')
        spec_js = json.loads(spec_soup)
        spec_content = spec_js[prod_id]

        spec = spec_content.get('Stmt') # 本商品規格

        all = {'prod_check': prod_check,
               'source': source,
               'keyword': keyword,
               'prod_id': prod_id,
               'prod_url': prod_url,
               'prod_name': prod_name,
               'price': price,
               'prod_intropic': prod_intropic,
               'content': content,
               'spec': spec
               }

        print(all)
        # print()

"""
# 寫入MySQL
## 建立資料庫連線
        db = MySQLdb.connect(host='localhost', user='xxxxx', passwd='xxxxx', db='shopping', port=3306, charset='utf8mb4')
        cursor = db.cursor()  # 建立游標
        db.autocommit(True)  # 設定自動確認

## 檢查資料庫是否已有資料
        sql_str = 'select * from pchome where prod_id = "%s"' % (prod_id)
        cursor.execute(sql_str)
        datarows = str(cursor.fetchall())
        if prod_id in datarows:
            print(prod_id, '已存在!')

## 新增一筆資料到MySQL
        else:
            sql_str = 'insert into pchome(prod_check, source, keyword, prod_id, prod_url, prod_name, price, ' \
                      'prod_intropic, content, spec) ' \
                      'values(\'{}\', \'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'\
                .format(prod_check, source, keyword, prod_id, prod_url, prod_name, price, prod_intropic, content, spec)
            cursor.execute(sql_str)
            db.close()
            print('已寫入:', all)

        # print()

        time.sleep(1)
"""

"""
學習:
-內容有字無法摐取dict,使用replace('{jsonp_prod(', '')
-從產品頁網址爬取的原始碼無法找到內容, 檢視SOURCE的內容有網頁上的文字, 該連結即可抓到要的資訊
-減少被擋的做法:
 1.每筆間隔1秒
 2.header資訊增加cookie
-安裝Mac版MySQLdb: https://github.com/PyMySQL/mysqlclient-python
"""
