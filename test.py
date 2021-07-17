# -*- coding:utf-8 -*-
import os
import re

import requests

ip = 'https://www.asmrv.com/'


def get_htmlUrl_01():
    r = requests.get('https://www.asmrv.com/280.html')
    reg = '<a class="item-thumb" href="(.*?)"'
    _url = re.findall(reg, r.text)
    return _url


def get_htmlUrl_02():
    global realUrl
    _url = get_htmlUrl_01()
    htmlUrl02 = []
    for url in _url:
        r = requests.get(url)
        reg = '<iframe src="(.*?)"'
        htmlUrl = re.findall(reg, r.text)
        realUrl = ip + htmlUrl[-1]
        htmlUrl02.append(realUrl)
    return htmlUrl02


i = get_htmlUrl_02()[0]
print(i)
r = requests.get("https://www.asmrv.com/parse_video?url=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2Fav79507547")
print(r.text)
