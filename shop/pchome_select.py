"""
從MySQL查詢資料
"""

# -*- coding: gbk -*-
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import MySQLdb

# 建立資料庫連線
db = MySQLdb.connect(host='localhost', user='root', passwd='firstsql', db='shopping', port=3306, charset='utf8')
cursor = db.cursor()  # 建立游標
db.autocommit(True)  # 設定自動確認

# 查詢全部
sql_str = 'select * from pchome'
cursor.execute(sql_str)
datarows = cursor.fetchall()
for n in datarows:
    print(n)
"""
# 關鍵字查詢
keyword = 'LED'
sql_str = 'select * from pchome where prod_name like \"{}"'.format('%' + keyword + '%')
cursor.execute(sql_str)
datarows = cursor.fetchall()
for n in datarows:
    print(n)
"""
