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
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6
Cache-Control: no-cache
Connection: keep-alive
Cookie: bid=m7he76iTio4; __gads=ID=45d1323a93ec3722-224c78f095c7002e:T=1621140676:RT=1621140676:S=ALNI_MbYPNF0rnnEdD-Cbos3ouGvge9d3A; gr_user_id=c854ba0b-a4e4-415c-b61b-a03744d6b7db; _ga=GA1.2.787692321.1621140691; ll="108258"; douban-fav-remind=1; __utmv=30149280.11961; _vwo_uuid_v2=DD4F0995C21FD06F0DF4897C4A0DD6EB5|7a0feada129fc9e63c7515888dfde7c1; UM_distinctid=17e543c4707957-0cb5fa9161d5d6-75236433-5d279-17e543c4708b6a; Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1642090752; viewed="34672176_26803179_30403492"; __utmc=30149280; __utmc=223695111; dbcl2="119619987:Jys7L2cJh5o"; ck=uaMd; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=DD4F0995C21FD06F0DF4897C4A0DD6EB5|7a0feada129fc9e63c7515888dfde7c1; __utmz=30149280.1650214789.42.16.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/121920872/; ap_v=0,6.0; __utma=30149280.787692321.1621140691.1650261340.1650266506.44; __utmt=1; __utmb=30149280.6.10.1650266506; __utma=223695111.787692321.1621140691.1650206840.1650266578.5; __utmb=223695111.0.10.1650266578; __utmz=223695111.1650266578.5.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/166820507/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1650266578%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F166820507%2F%3F_i%3D0266542m7he76i%22%5D; _pk_id.100001.4cf6=0a1eeea1bbeceaf1.1650187069.5.1650266578.1650207725.; _pk_ses.100001.4cf6=*
DNT: 1
Host: movie.douban.com
Pragma: no-cache
Referer: https://www.douban.com/people/166820507/?_i=0266542m7he76i
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-site
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36
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
