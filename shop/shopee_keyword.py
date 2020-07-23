"""
以關鍵字搜层蝦皮購物網站
"""

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from bs4 import BeautifulSoup
import requests
import MySQLdb
import json
import time

headers = {'User-Agent': 'Googlebot'}
keyword = 'LED數字時鐘'

source = 'shopee'
prod_check = 0

page = 0
while page >= 0 :
    keyword_url = 'https://shopee.tw/search?keyword=' + keyword + '&page=' + str(page)
    # print(keyword_url)
    keyword_res = requests.get(url=keyword_url, headers=headers)
    soup = BeautifulSoup(keyword_res.text, 'html.parser')

# 無商品即停止
    no_products = soup.select('div[class="shopee-search-empty-result-section__title"]')
    if no_products != []:
        break

# 各產品網址
    else:
        prod_urls = soup.select('div[class="col-xs-2-4 shopee-search-item-result__item"] a')
        for n in range(0, len(prod_urls)):
            prod_url = 'https://shopee.tw' + prod_urls[n]['href']

            prod_id = prod_urls[n]['href'].split('-i.')[-1] # prod_id
            prod_name = prod_urls[n]['href'].split('-i.')[0][1:] # prod_name

            spec_res = requests.get(url=prod_url, headers=headers)
            spec_soup = BeautifulSoup(spec_res.text, 'html.parser')
            price =  spec_soup.select('div[class="product-briefing flex card _2cRTS4"] [class="_3n5NQx"]')[0].text.strip('$') # 價格
            content_all =  spec_soup.select('div[class="_2aZyWI"]')
            content = content_all[0].text # 商品詳情
            spec = content_all[1].text.replace('\n', '') # 商品規格
            prod_intropic_all = spec_soup.select('div[class="F3D_QV"] [class="ZPN9uD"] [class="_3ZDC1p"] [class="_2Fw7Qu _3XaILN"]') # 圖片連結

            content_all = ''
            for n in range(0,len(prod_intropic_all)):
                prod_intropic = prod_intropic_all[n]['src']
                separate = ' '
                content_all += separate + prod_intropic
            # print(content_all)

            all = {'prod_check': prod_check,
                   'source': source,
                   'keyword': keyword,
                   'prod_id': prod_id,
                   'prod_url': prod_url,
                   'prod_name': prod_name,
                   'price': price,
                   'prod_intropic': content_all,
                   'content': content,
                   'spec': spec
                   }

            # print(all)

# 寫入MySQL
## 建立資料庫連線
            db = MySQLdb.connect(host='localhost', user='root', passwd='firstsql', db='shopping', port=3306,
                                 charset='utf8mb4')
            cursor = db.cursor()  # 建立游標
            db.autocommit(True)  # 設定自動確認

            ## 檢查資料庫是否已有資料
            sql_str = 'select * from pchome where prod_id = "%s"' % (prod_id)
            cursor.execute(sql_str)
            datarows = str(cursor.fetchall())
            if prod_id in datarows:
                print(source, prod_id, '已存在!')

## 新增一筆資料到MySQL
            else:
                try:
                    sql_str = 'insert into pchome(prod_check, source, keyword, prod_id, prod_url, prod_name, price, ' \
                              'prod_intropic, content, spec) ' \
                              'values(\'{}\', \'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');' \
                        .format(prod_check, source, keyword, prod_id, prod_url, prod_name, price, prod_intropic, content,
                                spec)
                    cursor.execute(sql_str)
                    db.close()
                    print(source, '已寫入:', all)
                except:
                    pass
                    print(source, 'pass: ', prod_url)
    page += 1


