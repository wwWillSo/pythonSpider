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
import re, os, traceback, time
from urllib import request,parse

# 页码组成规则
def getPageNo(count) :
    return '?p=%s&o=1' % count

def do(url, path, count=1, source='hupu') :
    if source == 'hupu':
        url_tail = ''
        url_collect = url.split('/')

        while True:
            temp = url_collect.pop()
            url_tail = temp + '/' + url_tail
            if temp == 'tag' :
                break

        url_tail = url_tail[:-1]
        url_front = url.replace(url_tail, '')
        startSpider(url_front, url_tail, path, count)
    else :
        print('此source未开发')

def startSpider(url_front, url_tail, path, count):
    url = url_front + url_tail + getPageNo(count)
    req = request.Request(url)
    resp = None
    try:
        resp = request.urlopen(req)
    except:
        resp = connectToUrl(url, 1)

    if resp is None:
        print('startSpider连接失败...终止程序...')
        return

    html_doc = resp.read()

    soup = BeautifulSoup(html_doc, 'html5lib')

    piclist3 = soup.find('div', {'class': 'piclist3'})

    a_nextPage = list(soup.find('div', {'class' : 'page right'}).find_all('a')).pop()
    pageNo = a_nextPage.get('href')

    a_prevPage = list(soup.find('div', {'class' : 'page right'}).find_all('a')).pop(0)

    if (not a_prevPage.string.endswith('上一页')) :
        print('首页', '开始爬取...' + url_front + url_tail + getPageNo(count))
        startSpiderOperator(url_front, url_tail, piclist3, path+ '第' + str(count) + '页' + '/')
    elif (a_nextPage.string.startswith('下一页')) :
        print('当前页码'+getPageNo(count), '开始爬取...' + url_front + url_tail + getPageNo(count))
        # time.sleep(3)
        startSpiderOperator(url_front, url_tail, piclist3, path+ '第' + str(count) + '页' + '/')
    else :
        print('到达最后一页' + getPageNo(count), '开始爬取...' + url_front + url_tail + getPageNo(count))
        # time.sleep(3)
        startSpiderOperator(url_front, url_tail, piclist3, path+ '第' + str(count) + '页' + '/')
        print('startSpider工作完毕...')
        return

    startSpider(url_front, url_tail, path, count+1)

def startSpiderOperator(url_front, url_tail, piclist3, path) :
    start = time.clock()
    # 所有tr
    tr_list = piclist3.table.tbody.find_all('tr')

    url_list = []
    # 将所有dt放到一个list中
    for tr in tr_list:
        dt_list = tr.find_all('dt')
        for dt in dt_list:
            url = str.split(dt.a.get('href'), '/').pop()
            url_list.append(url)

    for url_tail in url_list:
        # 读取当前页面的所有图集
        readKu(url_front, url_tail, 1, path)

    end = time.clock()
    print('已完成，耗时：%f s' % (end - start))

def readKu(url_front, url_tail, count, path) :
    #初始化工作
    req = request.Request(url_front + url_tail)
    try:
        resp = request.urlopen(req)
    except:
        resp = connectToUrl(url_front + url_tail)

    if resp is None:
        print('readKu连接失败...终止程序...')
        return

    html_doc = resp.read()
    soup = BeautifulSoup(html_doc, 'html5lib')

    title = str(soup.head.title.string).replace('"', '') + '/'
    # folderName = "E:/hoopPics/" + title
    folderName = path + title

    if count == 1:
        print('本机保存图片路径：' + folderName)

    try:
        os.makedirs(folderName)
    except:
        pass
        # traceback.print_exc()

    # 下一张按钮, 如果此按钮不存在则再递归多一次再退出递归
    a_nextPage = soup.find('a', text='下一张')
    if a_nextPage is not None :
        a_nextPage = a_nextPage.get('href')
        readKuOperator(soup, url_front, url_tail, count, folderName)
    else :
        readKuOperator(soup, url_front, url_tail, count, folderName)
        return

    return readKu(url_front, a_nextPage, count+1, path)

def readKuOperator(soup, url_front, url_tail, count, folderName) :
    # 查看原图的div
    div_sourcePic = soup.find_all('div', class_='tag')

    # 当前页的图片
    url_sourcePic = None
    for div in div_sourcePic:
        if (div.text.startswith('查看原图：')):
            url_sourcePic = 'http:' + div.text.replace('查看原图：', '').strip()

    #保存图片到本地
    path = folderName + str(count) + '.jpg'
    # f = request.urlretrieve('http:' + url_sourcePic, path)
    try :
        img = request.urlopen(url_sourcePic)
    except:
        if (count == 1):
            print('访问到空的图集，跳过...')
        return
    img = img.read()
    f = open(path, 'wb')
    f.write(img)
    f.close()

    # 组装下一页的url
    # print('当前计数：' + str(count))
    # print('本机保存图片路径：' + path)
    # print('图片Url：' + url_sourcePic)
    # print('当前页url：' + url_front + url_tail)

def connectToUrl(url, count):
    time.sleep(1)
    if count == 1:
        print(url, '准备重连...')
    try:
        if count <= 3:
            resp = request.urlopen(url)
            return resp
        else:
            return None
    except :
        print('连接超时...正在自动重连...次数：' + str(count))
        connectToUrl(url, count+1)

if __name__ == '__main__':
    start = time.clock()

    #http://photo.hupu.com/tag/%E8%B4%B9%E5%BE%B7%E5%8B%92
    #http://photo.hupu.com/nba/tag/%E7%A7%91%E6%AF%94
    #http://photo.hupu.com/tag/%E8%B4%B9%E5%BE%B7%E5%8B%92
    #http://photo.hupu.com/soccer/tag/%E6%A2%85%E8%A5%BF
    # startSpider('http://photo.hupu.com/nba/', 'tag/%E8%A9%B9%E5%A7%86%E6%96%AF', 'E:/hoopPics/詹姆斯/', 1)
    # startSpider('http://photo.hupu.com/', 'tag/%E8%B4%B9%E5%BE%B7%E5%8B%92', 'E:/hoopPics/费德勒/', 1)
    # readKu('http://photo.hupu.com/nba/', 'p35233.html', 1)

    do('http://photo.hupu.com/tag/%E8%B4%B9%E5%BE%B7%E5%8B%92', 'E:/hoopPics/费德勒/', count=1, source='hupu')

    end = time.clock()
    print('总计耗时：%f s' % (end - start))