"""
在天天看小說網站首頁輸入書名搜尋
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                         'Version/13.1.1 Safari/605.1.15'}

# 首頁輸入書名搜尋
book_name = input('請輸入書名: ') # 透明光, 倚天屠龍記
# book_name = '倚天屠龍記'
url = 'https://tw.ttkan.co/novel/search?q=' + book_name
res = requests.get(url=url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
book_content = soup.select(
    'div[class="pure-u-1-1 pure-u-xl-1-3 pure-u-lg-1-3 pure-u-md-1-2 novel_cell"] [data-v-079d8739] a')
if book_name not in str(book_content):
    print('查無此書')
    pass

else:
    book_url = 'https://tw.ttkan.co' + book_content[0]['href']
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
    author = book_brief[1].text
    catagory = book_brief[2].text
    status = book_brief[3].text
    print(book_name)
    print(author, catagory, status)
    print()

# 各章回網址
    all_chapter = soup_book.select('div[class="pure-u-xl-1-4 pure-u-lg-1-3 pure-u-md-1-2 pure-u-sm-1-2 pure-u-1-1 chapter_cell"] a')[0]['href']
    for chapter_num in range(1, int(total_pages)+1):
        chapter_url = 'https://tw.kjasugn.top/novel/pagea' + chapter_engname + '_' + str(chapter_num) + '.html'
        # https://tw.kjasugn.top/novel/pagea/toumingguang-nikuang_1.html
        
# 各章回名稱
        res_chapter = requests.get(chapter_url, headers=headers)
        soup_chapter = BeautifulSoup(res_chapter.text, 'html.parser')
        # print(soup_chapter)
        chapter_title = soup_chapter.select('div[class="title"]')[0].text
        print(chapter_title)
        print()

# 各章回內容
        content = soup_chapter.select('div[class="content"] p')
        for n in range(0, len(content)):
            print(content[n].text)
            print()