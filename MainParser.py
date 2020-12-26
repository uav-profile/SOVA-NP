# -*- coding: utf-8 -*-
# Author: U.A.V.
# 2020-12
# License : MIT

import time
from datetime import datetime
from PyQt5 import QtCore, QtGui

from lib.parsers.RUS.ria import return_news as RUS1
from lib.parsers.RUS.r_today import return_news as RUS2
from lib.parsers.RUS.k_uzel import return_news as RUS3
from lib.parsers.RUS.rbc import return_news as RUS4
from lib.parsers.RUS.rg import return_news as RUS5
from lib.parsers.RUS.izvestiya import return_news as RUS6

# СПИСОК СТРАН -> ФУНКЦИЯ: URL
URLS = {
    
    'RUS':  {
            RUS1: 'https://ria.ru/export/rss2/archive/index.xml',
            RUS2: 'https://russian.rt.com/rss',
            RUS3: 'https://www.kavkaz-uzel.eu/articles.rss',
            RUS4: 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss',
            RUS5: 'https://rg.ru/xml/index.xml',
            RUS6: 'https://iz.ru/xml/rss/all.xml',
            },
        }


def return_all_news(str_codes, make_model_on_table = True):
    overall_news = []
    model = QtGui.QStandardItemModel()
    model.setHorizontalHeaderLabels(['Дата/время', ' ', ' ', 'Заголовок', 'Тема/Тэги', 'Ссылка', 'Текст новости'])
    if "#" in str_codes:
        list_codes = str_codes.split("#")
    else:
        list_codes = [str_codes]
    count_model = 0
    with open("timings.log", "at+", encoding = "utf-8") as f2:
        f2.write("\n")
    for code in list_codes:
        funcs = URLS.get(code)
        for function, url in funcs.items():
            start_time = time.time()
            try:
                news = function(url)
                overall_news = overall_news + news
                if make_model_on_table:
                    for n in news:
                        item1 = QtGui.QStandardItem()
                        item2 = QtGui.QStandardItem()
                        item3 = QtGui.QStandardItem()
                        item4 = QtGui.QStandardItem()
                        item5 = QtGui.QStandardItem()
                        item6 = QtGui.QStandardItem()
                        item7 = QtGui.QStandardItem()
                        item1.setText(n['DT'])
                        item2.setText(n['CODE'])
                        item3.setText(n['SRC'])
                        item4.setText(n['TITLE'])
                        item5.setText(n['TAGS'])
                        item6.setText(n['URL'])
                        TEXT_NEWS = n['TEXT']
                        TEXT_NEWS = TEXT_NEWS.replace("<br />\n<br />", "<br>")
                        TEXT_NEWS = TEXT_NEWS.replace("<br /><br />", "<br>")
                        TEXT_NEWS = TEXT_NEWS.replace("<br />\n\n<br />", "<br>")
                        TEXT_NEWS = TEXT_NEWS.replace("<br />\ <br />", "<br>")
                        TEXT_NEWS = TEXT_NEWS.replace("<br />\  <br />", "<br>")
                        TEXT_NEWS = TEXT_NEWS.replace("<br />\   <br />", "<br>")
                        item7.setText(TEXT_NEWS)
                        item1.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        item4.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        item5.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        item6.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        item7.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                        model.setItem(count_model, 0, item1)
                        model.setItem(count_model, 1, item2)
                        model.setItem(count_model, 2, item3)
                        model.setItem(count_model, 3, item4)
                        model.setItem(count_model, 4, item5)
                        model.setItem(count_model, 5, item6)
                        model.setItem(count_model, 6, item7)
                        count_model += 1
            except Exception as e:
                with open("errors.log", "at+") as file_log:
                    current_time = datetime.now()
                    current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
                    str_to_log = current_time + ": [PARSING ERROR] ["
                    str_to_log += str(code) +  "] => " + str(url) + " (" + str(function) + " : \"" + str(e) + "\")"
                    file_log.write(str_to_log + "\n")
            with open("timings.log", "at+", encoding = "utf-8") as f2:
                current_time = datetime.now()
                current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
                str_to_log = current_time + ": [PARSING TIME] ["
                timing = "%s sec." % (time.time() - start_time)
                str_to_log += str(code) +  "] => " + str(url) + " : " + timing
                f2.write(str_to_log + "\n")
    return model, overall_news