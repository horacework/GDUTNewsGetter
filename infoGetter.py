# -*- coding: utf-8 -*-

# infoGetter.py 主要是周期性获取并静态化常用的数据（通知标题）

import time
import requests
import json
from bs4 import BeautifulSoup

import config

def LoginSystem():
    try:
        url = "http://news.gdut.edu.cn/UserLogin.aspx"
        UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"

        header = {"User-Agent": UA,
                  "Referer": "http://news.gdut.edu.cn/UserLogin.aspx"
                  }

        v2ex_session = requests.Session()
        f = v2ex_session.get(url, headers=header, allow_redirects=False)
        if f.status_code == 200:
            soup = BeautifulSoup(f.content, "html.parser")
            viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
            eventvalid = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
            login = soup.find('input', {'name': 'ctl00$ContentPlaceHolder1$Button1'})['value']

            postData = {'__VIEWSTATE': viewstate,
                        '__EVENTVALIDATION': eventvalid,
                        'ctl00$ContentPlaceHolder1$userEmail': 'gdutnews',
                        'ctl00$ContentPlaceHolder1$userPassWord': 'newsgdut',
                        'ctl00$ContentPlaceHolder1$Button1': login
                        }

            v2ex_session.post(url,
                              data=postData,
                              headers=header)
            return v2ex_session, header
        else:
            return None, None
    except (requests.ConnectionError, IndexError, UnicodeEncodeError, requests.HTTPError):
        return None, None


def GetTitleFromSystem(v2ex_session, header, category):

    categoryUrl = ""
    if category == "gongshi":
        categoryUrl = "category=5"
    elif category == "jianxun":
        categoryUrl = "category=6"
    elif category == "tongzhi":
        categoryUrl = "category=4"

    response = v2ex_session.get('http://news.gdut.edu.cn/ArticleList.aspx?'+categoryUrl, headers=header)
    if response.status_code != 200:
        print "获取通知标题失败"
        return 'False'

    soup = BeautifulSoup(response.text, "html.parser")

    jsonContent = {
        "status": 200,
        "update": time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(time.time())),
        "miniContent": {},
    }
    miniContent = []

    list = soup.find_all('p')
    for index in range(len(list)):
        for child in list[index].children:
            if child.name == 'a':
                HREF = child['href']
                TITLE = child['title']
                item = {
                    "title": TITLE,
                    "href": HREF
                }
                miniContent.append(item)
                print TITLE
                print 'http://news.gdut.edu.cn/' + HREF

    jsonContent["miniContent"] = miniContent

    with open(config.proPath+"dataStorage/news_"+category+".json", "w") as f:
        json.dump(jsonContent, f)


if __name__ == "__main__":

    v2ex_session, header = LoginSystem()
    if v2ex_session is None or header is None:
        print "登录教务系统失败"
        exit(0)

    while True:
        if config.endTime > time.strftime('%H:%M:%S', time.localtime(time.time())) > config.startTime:
            time.sleep(config.sleepTime)
            GetTitleFromSystem(v2ex_session, header, "all")
            GetTitleFromSystem(v2ex_session, header, "gongshi")
            GetTitleFromSystem(v2ex_session, header, "jianxun")
            GetTitleFromSystem(v2ex_session, header, "tongzhi")
            print '完成一次获取循环'
        else:
            time.sleep(config.m_sleepTime)
