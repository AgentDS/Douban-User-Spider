# -*- coding: utf-8 -*-
# @Time    : 4/17/22 9:20 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : movies_single_user.py
# @Software: PyCharm
import DoubanTools
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

uid = ""  # TODO: check the user id from DouBan url
total_num = 0  # TODO: total number of movies watched by this user
item_each_page = 15
all_movies = []

# TODO: past request header from Chrome browser using developer's tool
header_str = '''
[past request header from Chrome browser using developer's tool]
'''

headers = DoubanTools.str2dict(header_str, '\n', ': ')
movie_collect_url = DoubanTools.make_douban_url(uid, 'movie')

for start in range(0, total_num, item_each_page):
    print(
        f"Request for movies {start} to {start + 15} ({100 * (start + 15) / total_num:.2f}%)...")
    response = req.get(movie_collect_url % start, headers=headers)
    pagetxt = response.text

    single_page_items = []
    soup = BeautifulSoup(pagetxt)
    single_page_items += soup.find_all('div', class_='item')
    if len(single_page_items) > 0:
        print(f"Page achieved: {len(single_page_items)} movies")

    single_page_movies = []
    for single_movie in single_page_items:
        movie_content = DoubanTools.single_movie_parser(single_movie)
        single_page_movies.append(movie_content)

    all_movies.extend(single_page_movies)
    print(f"Movie {start} to {start + len(single_page_movies)} parsing done.")

    movies_df = pd.DataFrame(all_movies)
    movies_df.to_excel("./movies_%s.xlsx" % uid)
    print(
        f"Movie {start} to {start + len(single_page_movies)} output done.\n\n")

    random_time = int(random.random() * 10)
    print(f"Sleep {random_time}s...")
    time.sleep(random_time)
