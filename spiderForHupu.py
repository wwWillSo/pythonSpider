#!/usr/bin/env python
# encoding: utf-8

"""
@author: WillSo
@license: Apache Licence 
@software: PyCharm
@file: spiderForHupu.py
@time: 2017\10\24 0024 15:24
"""

from bs4 import BeautifulSoup
import re, os
from urllib import request,parse

def startSpider(url):
    req = request.Request(url)
    resp = request.urlopen(req)

    html_doc = resp.read()

    soup = BeautifulSoup(html_doc, 'html5lib')

    piclist3 = soup.find('div', {'class': 'piclist3'})

    trlist = piclist3.table.tbody.find_all('tr')

    print(trlist)


#计数器
def readKu(url_front, url_tail, count) :

    #初始化工作
    req = request.Request(url_front + url_tail)
    resp = request.urlopen(req)
    html_doc = resp.read()
    soup = BeautifulSoup(html_doc, 'html5lib')

    # 下一张按钮, 如果此按钮不存在则再递归多一次再退出递归
    a_nextPage = soup.find('a', text='下一张')
    if a_nextPage is not None :
        a_nextPage = a_nextPage.get('href')
        readKuOperator(soup, url_front, url_tail, count)
    else :
        readKuOperator(soup, url_front, url_tail, count)
        return

    return readKu(url_front, a_nextPage, count+1)

def readKuOperator(soup, url_front, url_tail, count) :
    # 查看原图的div
    div_sourcePic = soup.find_all('div', class_='tag')

    # 当前页的图片
    url_sourcePic = None
    for div in div_sourcePic:
        if (div.text.startswith('查看原图：')):
            url_sourcePic = 'http:' + div.text.replace('查看原图：', '').strip()

    path = "E:/hoopPics/" + str(count) + '.jpg'
    # f = request.urlretrieve('http:' + url_sourcePic, path)
    img = request.urlopen(url_sourcePic)
    img = img.read()
    f = open(path, 'wb')
    f.write(img)
    f.close()

    # 组装下一页的url
    print('当前计数：' + str(count))
    print('本机保存图片路径：' + path)
    print('图片Url：' + url_sourcePic)
    print('当前页url：' + url_front + url_tail)

if __name__ == '__main__':
    # startSpider('http://photo.hupu.com/nba/tag/%E8%A9%B9%E5%A7%86%E6%96%AF')
    readKu('http://photo.hupu.com/nba/', 'p35233.html', 1)