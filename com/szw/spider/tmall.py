#!/usr/bin/env python
# encoding: utf-8

"""
@author: WillSo
@license: Apache Licence 
@software: PyCharm
@file: tmall.py
@time: 2017\10\12 0012 18:59
"""

from urllib import request,parse
from bs4 import BeautifulSoup
import re
import os

url = 'C:/Users/Administrator/Desktop/python_about.html'

htmlFile = open(url, 'r', encoding='UTF-8')

soup = BeautifulSoup(htmlFile, 'html5lib')

def print_meta() :
    print("""===================================
        【head】里面的meta
===================================""")
    for meta in soup.find_all('meta'):
        print(meta)

def print_title() :
    print(soup.head.title.string)

def print_all_pictures_url() :
    imgs = soup.find_all('img')
    for img in imgs :
        print(img.attrs['src'])

def print_all_url() :
    tag_a_list = soup.find_all('a')
    for tag_a in tag_a_list :
        if tag_a.attrs['href'] != '' and tag_a.attrs['href'].startswith('http') :
            print(tag_a.attrs['href'])

print_title()

print_all_pictures_url()

print_all_url()

if __name__ == '__main__':
    pass