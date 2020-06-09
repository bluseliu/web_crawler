"""
爬取天天看小說全部的書籍
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from bs4 import BeautifulSoup
import requests
import json
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                         'Version/13.1.1 Safari/605.1.15'}

# 取得類別及連結
home_url = 'https://tw.ttkan.co'
home_res = requests.get(url=home_url, headers=headers)
home_soup = BeautifulSoup(home_res.text, 'html.parser')

# 所有類別
catagory_all = home_soup.select('div[class="novel_class_nav"] [aria-label]')

# 該類別所有書籍
for n in range(3, len(catagory_all)):
    catagory = catagory_all[n].text
    catagory_name_url = catagory_all[n]['href'] # 類別名稱
    catagory_engname = str(catagory_name_url).split('/')[-1]
    catagory_url = 'https://tw.ttkan.co' + catagory_name_url # 類別網址
    print(catagory, catagory_url)

    catagory_page = 1
    while True:
        test_url = 'https://tw.ttkan.co/api/nq/amp_novel_list?type=' + catagory_engname + '&filter=*&page=' + str(
            catagory_page) + '&limit=18&language=tw&__amp_source_origin=https%3A%2F%2Ftw.ttkan.co'
        # print(test_url)
        res = requests.get(url=test_url)
        js = json.loads(res.text)
        # print('js:', js)

        try:
            items = js.get('items')[0]
            novel_id = items.get('novel_id')

        except:
            break

        catagory_page += 1

# 取得各書籍網址
        book_url = 'https://tw.ttkan.co/novel/chapters/' + novel_id
        # 'https://tw.ttkan.co/novel/chapters/modaozushi-moxiangtongxiu'
        # print(book_url)

# 總章回數
        res_book = requests.get(book_url, headers=headers)
        soup_book = BeautifulSoup(res_book.text, 'html.parser')
        # print(soup_book)

        chapter_engname = str(soup_book.select('meta[content]')[8]).split('"')[1][35:] # 網址英文名
        total_pages = str(soup_book.select('div[class="chapters_frame"] '
                                           'button[class="show_all_chapters"] ')[0].text).split(' ')[8][4:-4]

# 書籍資訊
        book_brief = soup_book.select('div[class="pure-u-xl-5-6 pure-u-lg-5-6 pure-u-md-2-3 pure-u-1-2"] li')
        # print(book_brief)
        book_name = book_brief[0].text
        author = book_brief[1].text
        book_catagory = book_brief[2].text
        status = book_brief[3].text
        print(book_name)
        print(author, book_catagory, status)
        # print()

## 儲存書籍資訊
        path_dir = '/Users/willy/Documents/python_works/web_crawler/ttkan/' + catagory
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)
        os.chdir(path_dir)
        filename = book_name + '.txt'
        with open(filename, 'a') as f:
            f.write(book_name + '\n' + author + '\n' + book_catagory + '\n' + status + '\n' + '\n')

# 各章回網址
        all_chapter = soup_book.select(
            'div[class="pure-u-xl-1-4 pure-u-lg-1-3 pure-u-md-1-2 pure-u-sm-1-2 pure-u-1-1 chapter_cell"] a')[0]['href']
        for chapter_num in range(1, int(total_pages)+1):
            chapter_url = 'https://tw.kjasugn.top/novel/pagea' + chapter_engname + '_' + str(chapter_num) + '.html'
            # https://tw.kjasugn.top/novel/pagea/toumingguang-nikuang_1.html

# 各章回名稱
            res_chapter = requests.get(chapter_url, headers=headers)
            soup_chapter = BeautifulSoup(res_chapter.text, 'html.parser')
            # print(soup_chapter)
            chapter_title = soup_chapter.select('div[class="title"]')[0].text
            print(chapter_title)
            # print()

## 儲存章回名稱
            with open(filename, 'a') as f:
                f.write(chapter_title + '\n')

# 各章回內容
            content = soup_chapter.select('div[class="content"] p')
            for n in range(0, len(content)):
                chapter_content = content[n].text
                # print(chapter_content)
                # print()

## 儲存文章內容
                with open(filename, 'a') as f:
                    f.write(chapter_content + '\n' + '\n')

print()


"""
# 排行
url_rank = 'https://tw.ttkan.co/novel/rank'
catagory_res = requests.get(url=url_rank, headers=headers)
catagory_soup = BeautifulSoup(catagory_res.text, 'html.parser')
sub_catagory_all = catagory_soup.select('div[class="rank_nav"] a ')
for n in range(0, len(sub_catagory_all)):
    sub_catagory = sub_catagory_all[n].text
    sub_catagory_engname = sub_catagory_all[n]['href']
    sub_catagory_url = 'https://tw.ttkan.co' + sub_catagory_engname
    print('排行:', sub_catagory, sub_catagory_url)
"""
