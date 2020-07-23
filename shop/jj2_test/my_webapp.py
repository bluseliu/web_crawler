# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import MySQLdb
import json

# from shop import pchome_select

app = Flask(__name__)
bootstrap = Bootstrap(app) # 建立bootstrap物件

@app.route('/', methods=['GET', 'POST'])
def my_index():
    if request.method == 'POST':
        input_name = request.form['inputtext']
        print(input_name)

        from shop import pchome_keyword
        from shop import shopee_keyword

        db = MySQLdb.connect(host='localhost', user='xxxxx', passwd='xxxxx', db='shopping', port=3306, charset='utf8')
        cursor = db.cursor()
        # names = 'select * from pchome'
        names = 'select * from pchome where keyword = "%s"' % (input_name)
        cursor.execute(names)
        prod_name = cursor.fetchall()

        return render_template("result.html", input_name=input_name, prod_name=prod_name, keyword=input_name)
    else:
        return render_template('index.html') # 將取得資料帶回頁面

@app.route('/result', methods=['GET', 'POST'])
def default():
    keyword = request.form['inputtext']
    print('/default', keyword)

    db = MySQLdb.connect(host='localhost', user='xxxxx', passwd='xxxxx', db='shopping', port=3306, charset='utf8')
    cursor = db.cursor()
    # names = 'select * from pchome'
    names = 'select * from pchome where keyword = "%s"' % (keyword)

    cursor.execute(names)
    prod_name = cursor.fetchall()

    return render_template('result.html', prod_name=prod_name, keyword=keyword)

@app.route('/new') # 利用裝飾器來定義路由
def new_data():
    return render_template('keyword.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_servaer_error(e):
    return render_template('500.html'), 500




@app.route('/test', methods=['get', 'post'])
def test():
    return render_template('testhtml.html')

if __name__ == '__main__':
    app.run()

