# -*- coding: utf-8 -*-
# @Time    : 4/17/22 9:20 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : DoubanTools.py
# @Software: PyCharm
import requests as req
from bs4 import BeautifulSoup
import pandas as pd


def make_douban_url(uid, content='movie'):
    basic_url = "https://{content}.douban.com/people/{uid}/collect?start=%d&sort=time&rating=all&filter=all&mode=grid"
    douban_url = basic_url.format(content=content, uid=uid)
    return douban_url


def str2dict(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            li2[0] = li2[0].replace(':', '')
            res[li2[0]] = li2[1]

    if 'Content-Length' in res:
        del res['Content-Length']

    res['accept-encoding'] = 'gzip'

    return res


def single_movie_parser(single_item):
    tmp = single_item.ul.contents
    ul_contents = [li for li in tmp if li != '\n']  # only remain li element
    parsed_res = dict()

    # get title
    title = ul_contents[0].a.em.contents[0]
    parsed_res['title'] = title
    print(f"title:{title}")

    # get intro
    intro = ul_contents[1].contents[0]
    parsed_res['intro'] = intro
    #  print(f"intro:{intro}")

    # get rating & date & tags
    rating_date_tags = ul_contents[2].find_all('span')
    for span in rating_date_tags:
        class_name = span['class'][0]
        if class_name == 'date':
            parsed_res['date'] = span.contents[0]
        elif class_name == 'tags':
            parsed_res['tags'] = span.contents[0]
        elif class_name[:6] == 'rating':
            rating = int(class_name[6])
            parsed_res['rating'] = rating

    if 'rating' not in parsed_res:
        parsed_res['rating'] = None
    if 'tags' not in parsed_res:
        parsed_res['tags'] = None
    #  print(f"rating:{rating}\ndate:{date}")

    # get comments
    if len(ul_contents) > 3:
        comments = ul_contents[3].span.contents[0]
        parsed_res['comments'] = comments
    else:
        parsed_res['comments'] = None
    #  print(f"comments:{comments}")
    return parsed_res


def single_music_parser(single_album):
    tmp = single_album.ul.contents
    ul_contents = [li for li in tmp if li != '\n']  # only remain li element
    parsed_res = dict()

    # get title
    title = ul_contents[0].a.em.contents[0]
    parsed_res['title'] = title
    print(f"title: {title}")

    # get intro
    intro = ul_contents[1].contents[0]
    parsed_res['intro'] = intro

    # get rating & date & tags
    rating_date_tags = ul_contents[2].find_all('span')
    for span in rating_date_tags:
        class_name = span['class'][0]
        if class_name == 'date':
            parsed_res['date'] = span.contents[0]
        elif class_name == 'tags':
            parsed_res['tags'] = span.contents[0]
        elif class_name[:6] == 'rating':
            rating = int(class_name[6])
            parsed_res['rating'] = rating

    if 'rating' not in parsed_res:
        parsed_res['rating'] = None
    if 'tags' not in parsed_res:
        parsed_res['tags'] = None

    # get comments
    if len(ul_contents) > 3:
        comments = ul_contents[3].contents[0].strip()
        parsed_res['comments'] = comments
    else:
        parsed_res['comments'] = None

    return parsed_res


def single_book_parser(single_book):
    tmp = [item for item in single_book.contents if item != '\n']
    book_content = [item for item in tmp[1].contents if item != '\n']
    parsed_res = dict()

    title = book_content[0].a.contents[0].strip()
    parsed_res['title'] = title
    print(f"title: {title}")

    if len(book_content) > 1:
        pub = book_content[1].contents[0].strip()
        parsed_res['pub'] = pub

        rating_date_tags = book_content[2].find_all('span')
        for span in rating_date_tags:
            class_name = span['class'][0]
            if class_name == 'date':
                parsed_res['date'] = span.contents[0][:10]
            elif class_name == 'tags':
                parsed_res['tags'] = span.contents[0]
            elif class_name[:6] == 'rating':
                rating = int(class_name[6])
                parsed_res['rating'] = rating

        if 'rating' not in parsed_res:
            parsed_res['rating'] = None
        if 'tags' not in parsed_res:
            parsed_res['tags'] = None

        comments = book_content[2].p.contents[0].strip()
        parsed_res['comments'] = comments
    else:
        parsed_res['pub'] = None
        parsed_res['date'] = None
        parsed_res['rating'] = None
        parsed_res['tags'] = None

    return parsed_res
