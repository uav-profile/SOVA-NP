# -*- coding: utf-8 -*-
# Author: U.A.V.
# 2020-12
# License : MIT


import feedparser
from dateutil import parser  #, tz
from datetime import datetime


def return_news(link):
    entries = feedparser.parse(link)["entries"]
    news = []
    for i in entries:
        tag = (i['tags'][0]['term']).replace("/", "")
        dt_ = parser.parse(i['published'])
        dt_ = str(dt_.strftime("%Y-%m-%d %H:%M:%S"))
        news.append({'CODE': 'RUS', 'SRC':'RSS', 'TITLE':i['title'], 'URL':i['links'][0]['href'], 'DT':dt_, 'TAGS':tag, 'TEXT':i['summary']})
    return news