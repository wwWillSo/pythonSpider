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

# 页码组成规则(虎扑)
def getPageNo(count) :
    return '?p=%s&o=1' % count

# 解析URL（虎扑）
def getSplitUrl(url) :
    url_tail = ''
    url_collect = url.split('/')
    while True:
        temp = url_collect.pop()
        url_tail = temp + '/' + url_tail
        if temp == 'tag':
            break
    url_tail = url_tail[:-1]
    url_front = url.replace(url_tail, '')
    return {
        'url_front' : url_front,
        'url_tail' : url_tail
    }

# 爬虫运行入口
def do(url, path, count=1, source='hupu') :
    # 区分网址类型
    if source == 'hupu':
        url_map = getSplitUrl(url)
        startSpider(url_map.get('url_front'), url_map.get('url_tail'), path, count)
    else :
        print('此source未开发')

# 递归方法，递归扫描“所有图集”页面
def startSpider(url_front, url_tail, path, count):
    url = url_front + url_tail + getPageNo(count)
    req = request.Request(url)

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

    if (a_nextPage.string.startswith('下一页')) :
        print('当前页码'+str(count), '开始爬取...' + url_front + url_tail + getPageNo(count))
        # time.sleep(3)
        startSpiderOperator(url_front, url_tail, piclist3, path+ '第' + str(count) + '页' + '/')
    else :
        print('到达最后一页'+str(count), '开始爬取...' + url_front + url_tail + getPageNo(count))
        # time.sleep(3)
        startSpiderOperator(url_front, url_tail, piclist3, path+ '第' + str(count) + '页' + '/')
        print('startSpider工作完毕...')
        return

    startSpider(url_front, url_tail, path, count+1)

# 上面startSpider的执行类
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
        # 读取当前图集的所有图片
        readKu(url_front, url_tail, 1, path)

    end = time.clock()
    print('已完成，耗时：%f s' % (end - start))

# 递归方法，递归扫描某图集下的所有图片
def readKu(url_front, url_tail, count, path) :
    #初始化工作
    url = url_front + url_tail
    req = request.Request(url)
    try:
        resp = request.urlopen(req)
    except:
        resp = connectToUrl(url)

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

    # 下一张按钮, 如果此按钮不存在则再递归多一次再退出递归
    a_nextPage = soup.find('a', text='下一张')
    #查看原图的div
    div_sourcePic = soup.find_all('div', class_='tag')

    if a_nextPage is not None :
        a_nextPage = a_nextPage.get('href')
        readKuOperator(div_sourcePic, count, folderName)
    else :
        readKuOperator(div_sourcePic, count, folderName)
        return

    return readKu(url_front, a_nextPage, count+1, path)

# 上面readKu的执行类
def readKuOperator(div_sourcePic, count, folderName) :

    # 当前页的图片
    url_sourcePic = None
    for div in div_sourcePic:
        if (div.text.startswith('查看原图：')):
            url_sourcePic = 'http:' + div.text.replace('查看原图：', '').strip()
    savePic(url_sourcePic, count, folderName)

# 保存图片
def savePic(url_sourcePic, count, folderName) :
    # 保存图片到本地
    path = folderName + str(count) + '.jpg'
    try:
        img = request.urlopen(url_sourcePic)
    except:
        if (count == 1):
            print('访问到空的图集，跳过...')
        return
    img = img.read()
    f = open(path, 'wb')
    f.write(img)
    f.close()

# 自动重连三次
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
    # startSpider('http://photo.hupu.com/nba/', 'tag/%E8%A9%B9%E5%A7%86%E6%96%AF', 'E:/hoopPics/詹姆斯/', 1)
    # print(parse.unquote('http://photo.hupu.com/tag/%E8%A9%B9%E5%A7%86%E6%96%AF'))
    # print(parse.quote('http://photo.hupu.com/tag/詹姆斯'))
    do('http://photo.hupu.com/nba/tag/%E8%A9%B9%E5%A7%86%E6%96%AF', 'E:/hoopPics/詹姆斯/', count=1, source='hupu')
    end = time.clock()
    print('总计耗时：%f s' % (end - start))