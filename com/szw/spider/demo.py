#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: WillSo
@license: Apache Licence 
@file: demo.py
@time: 2017\10\10 0010 17:37
"""

from urllib import request,parse

values = {
    'username' : 'WillSo',
    'password' : '123456'
}

data = parse.urlencode(values).encode('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': 'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}

req = request.Request('http://www.baidu.com', headers = headers, data = data)
resp = request.urlopen(req)
# print(resp.read())
print(isinstance(bytes.decode(resp.read(), encoding='utf-8'), str))

if __name__ == '__main__':
    pass

