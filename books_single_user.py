# -*- coding: utf-8 -*-
# @Time    : 4/17/22 9:20 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : books_single_user.py
# @Software: PyCharm
import DoubanTools
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

uid = ""  # TODO: check the user id from DouBan url
total_num = 0  # TODO: total number of books read by this user
item_each_page = 15
all_books = []

# TODO: past request header from Chrome browser using developer's tool
header_str = '''
[past request header from Chrome browser using developer's tool]
'''

headers = DoubanTools.str2dict(header_str, '\n', ': ')
book_collect_url = DoubanTools.make_douban_url(uid, 'book')

for start in range(0, total_num, item_each_page):
    print(
        f"Request for books {start} to {start + 15} ({100 * (start + 15) / total_num:.2f}%)...")
    response = req.get(book_collect_url % start, headers=headers)
    pagetxt = response.text

    single_page_items = []
    soup = BeautifulSoup(pagetxt)
    single_page_items += soup.find_all('li', class_='subject-item')
    if len(single_page_items) > 0:
        print(f"Page achieved: {len(single_page_items)} books")

    single_page_books = []
    for single_book in single_page_items:
        book_content = DoubanTools.single_book_parser(single_book)
        single_page_books.append(book_content)

    all_books.extend(single_page_books)
    print(f"Book {start} to {start + len(single_page_books)} parsing done.")

    books_df = pd.DataFrame(all_books)
    books_df.to_excel("./books_%s.xlsx" % uid)
    print(
        f"Books {start} to {start + len(single_page_books)} output done.\n\n")

    random_time = int(random.random() * 10)
    print(f"Sleep {random_time}s...")
    time.sleep(random_time)
