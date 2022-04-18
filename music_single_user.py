# -*- coding: utf-8 -*-
# @Time    : 4/17/22 9:20 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : music_single_user.py
# @Software: PyCharm
import DoubanTools
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


uid = ""  # TODO: check the user id from DouBan url
total_num = 0  # TODO: total number of music listened by this user
item_each_page = 15

# TODO: past request header from Chrome browser using developer's tool
header_str = '''
[past request header from Chrome browser using developer's tool]
'''

headers = DoubanTools.str2dict(header_str, '\n', ': ')

music_collect_url = DoubanTools.make_douban_url(uid, 'music')

all_albums = []
for start in range(0, total_num, item_each_page):
    print(
        f"Request for album {start} to {start + 15} ({100 * (start + 15) / total_num:.2f}%)...")
    response = req.get(music_collect_url % start, headers=headers)
    pagetxt = response.text

    single_page_items = []
    soup = BeautifulSoup(pagetxt)
    single_page_items += soup.find_all('div', class_='item')
    if len(single_page_items) > 0:
        print(f"Page achieved: {len(single_page_items)} albums")

    single_page_albums = []
    for single_album in single_page_items:
        album_content = DoubanTools.single_music_parser(single_album)
        single_page_albums.append(album_content)

    all_albums.extend(single_page_albums)
    print(f"Movie {start} to {start + len(single_page_albums)} parsing done.")

    albums_df = pd.DataFrame(all_albums)
    albums_df.to_excel("./music_%s.xlsx" % uid)
    print(
        f"Movie {start} to {start + len(single_page_albums)} output done.\n\n")

    random_time = int(random.random() * 10)
    print(f"Sleep {random_time}s...")
    time.sleep(random_time)
