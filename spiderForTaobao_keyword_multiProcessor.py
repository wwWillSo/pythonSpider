# -*- coding: utf-8 -*
import multiprocessing

import requests
import re
import sys,locale, traceback
import easyquotation
from flask import Flask, request as flaskReq, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from urllib import request,parse
import re, os, traceback, time
import json
import configparser
from datetime import  datetime, timedelta
from multiprocessing import Pool, Process

# 读取配置
config=configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

baseUrl = "https://s.taobao.com/search?q="
page=int(config.get("taobao", 'page'))

#淘宝爬虫类
class TAOBAO:
    #初始化，传入基地址，页数
    def __init__(self,baseUrl,page,goods,username,):
        self.goods=goods
        self.username = username
        self.baseUrl=baseUrl+self.goods
        self.page=page
        self.defaultgoods=u"淘宝"
        self.ilt=[]
        self.file=None
    #传入url，获取页面代码
    def getHTMLText(self,url):
        headers={'user-agent':"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"}
        r=requests.get(url,headers=headers,timeout=30)
        r.encoding=r.apparent_encoding
        return r.text
    #摘取所要数据
    def parsePage(self,html):
        try:
            plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
            tlt = re.findall(r'\"raw_title\"\:\".*?\"',html)
            npl = re.findall(r'\"view_sales\"\:\"[\d]*',html)
            nik = re.findall(r'\"nick\"\:\"[\w]*\"',html)
            for i in range(len(plt)):
                price = eval(plt[i].split(':',1)[1])
                title = eval(tlt[i].split(':',1)[1])
                num   = eval(npl[i].split(':"',1)[1])
                nick = eval(nik[i].split(':',1)[1])
                self.ilt.append([price , num, title, nick])
        except:
            # traceback.print_exc()
            # print("摘取数据出错").encode('utf-8')
            return None
    #打印数据
    def printGoodsList(self):
        tplt = "{:^4}\t{:<14}\t{:<10}\t{:^80}\t{:^50}"
        print (tplt.format("序号", "价格","成交量", "商品名称", "商家用户名", ))#.decode('utf-8'))
        count = 0
        for g in self.ilt:
            count = count + 1
            print(tplt.format(count, g[0], g[1], g[2], g[3],chr(32)))
    #创建存入数据文件
    def setFileTitle(self):
            self.file = open('C:/Users/Administrator/Desktop/淘宝搜索结果/' + self.goods + ".txt","w+")

    #写入数据
    def writeData(self):
        self.setFileTitle()
        tplt = "{:^4}\t{:<14}\t{:<10}\t{:^80}\t{:^50}"
        self.file.write(tplt.format("序号", "价格","成交量", "商品名称", "商家用户名", )+"\n")
        count = 0
        for g in self.ilt:
            count = count + 1
            self.file.write(tplt.format(count, g[0], g[1], g[2], g[3],chr(100))+"\n")

    def printPosition(self):
        # print('第' + str(self.page) + '页，记录数：' + str(len(self.ilt)))
        results = []
        count = 0
        pos = 0
        for g in self.ilt:
            count = count + 1
            if str(g[3]).endswith(self.username) :
                pos = pos + 1
                results.insert(pos, str(count) + ':' + g[2])
                print(self.username + '的店铺在此搜索结果中的位置为：第' + str(self.page * len(self.ilt) + count) + '位，题目：' + g[2] + '，线程号：' + str(self.page))
        # print(self.username + '的店铺在此搜索结果中的位置为：第' + str(self.page + 1) + '页，' + str(results))
        return results

    def start(self):
        for i in range(self.page):
            try:
                url = self.baseUrl + '&s=' + str(44*i)
                html = self.getHTMLText(url)
                self.parsePage(html)
            except:
                continue
        return self.printPosition()

    def start_new(self, page):
        try:
            url = self.baseUrl + '&s=' + str(44 * page)
            # print(url)
            html = self.getHTMLText(url)
            self.parsePage(html)
            # print('第' + str(self.page) + '页，记录数：' + str(len(self.ilt)) + '-' + str(page_size_map[page]))
        except:
            traceback.print_exc()
        return self.printPosition()

@app.route('/getPosition')
def getPosition():
    username = flaskReq.args.get('u')
    goods = flaskReq.args.get('kw')
    tb = TAOBAO(baseUrl, page, goods, username)
    results = tb.start()
    return username + '的店铺在此搜索结果中的位置为：' + str(results)

def startPool(username, goods) :
    try :
        begin = datetime.now()
        pool = Pool(4)
        for i in range(page):
            result = pool.apply_async(processor, (username, goods, i))
        pool.close()
        pool.join()
        end = datetime.now()
        print('All subprocesses done in %d seconds.' % (end.timestamp()-begin.timestamp()))
    except :
        traceback.print_exc()

def processor(username, goods, page) :
    tb = TAOBAO(baseUrl, page, goods, username)
    results = tb.start_new(page)

def do ():
    goods = input("输入想要查询的标题:")
    startPool('空空空空白24', goods)
    do()

if __name__ == '__main__':
    # for i in range(page) :
    #     page_size_map[i] = 0
    do()
    # app.run(debug=True, host=config.get("taobao", 'host'), port=int(config.get("taobao", 'port')))