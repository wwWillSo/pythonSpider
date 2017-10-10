#!/usr/bin/env python
# encoding: utf-8

"""
@author: WillSo
@license: Apache Licence 
@software: PyCharm
@file: beautifulsoup_domtree.py
@time: 2017\10\11 0011 14:02
"""

from bs4 import BeautifulSoup
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html5lib')

#直接获取head或title
print(soup.head)
print(soup.title)
#获取body里面的第一个b
print(soup.body.b)
#获得当前名字的第一个tag
print(soup.a)
#获得所有的a标签
print(soup.find_all('a'))

print("""
================================子节点==============================
""")

#将tag的子节点以列表的方式输出
print(soup.head.contents)
print(soup.head.contents[0])
print(soup.head.contents[0].contents)
print(soup.head.contents[0].contents[0])

#BeautifulSoup本身一定会包含子节点
print(soup.contents[0].name)

#对子节点进行循环
for child in soup.head.contents[0] :
    print(child)

#循环tag下所有的子孙节点
for child in soup.head.descendants :
    print(child)
print(len(list(soup.children)))
print(len(list(soup.descendants)))

#如果tag只有navigableString类型子节点，可以使用.string获得子节点
print(soup.title.string)

#如果tag只有一个子节点，也可以用.string
print(soup.head.contents)
print(soup.head.string)
#如果tag不止一个子节点，那么.string会返回none
print(soup.html.string)

#如果tag中包含多个字符串，可以用.strings来循环获取
for string in soup.strings :
    print(repr(string))
#.stripped_strings可以去除多余空白内容
for string in soup.stripped_strings :
    print(string)

print("""
================================父节点==============================
""")

#通过.parent获取元素的父节点
print(soup.title,'是',soup.title.parent,'的子节点')
print(soup.title.string,'是',soup.title.string.parent,'的子节点')
#顶层html的父节点是beautifulSoup对象
print(type(soup.html),'是',type(soup.html.parent),'的子节点')
#beautifulSoup没有父节点
print('soup的父节点是',soup.parent)

#.parents可以获取所有父节点
print('将要遍历所有父节点的是',soup.a)
for parent in soup.a.parents :
    if parent is None :
        print(parent)
    else :
        print(parent.name)

print("""
================================兄弟节点==============================
""")

#兄弟节点
sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>", 'html5lib')
print(sibling_soup.prettify())
#通过.next_sibling和.previous_sibling查询兄弟节点
print(sibling_soup.b.next_sibling)
print(sibling_soup.c.previous_sibling)
#父节点不一样就不是兄弟节点了
print(sibling_soup.b.string.next_sibling)

#通过.next_siblings和.previous_siblings遍历兄弟节点
for sibling in soup.a.next_siblings :
    print(repr(sibling))
for sibling in soup.find(id='link3').previous_siblings :
    print(repr(sibling))

print("""
关于.next_element/.previous_element与.next_sibling/.previous_sibling的区别
""")

#关于.next_element/.previous_element与.next_sibling/.previous_sibling的区别
#拿出爱丽丝文档的最后一个a标签
last_a_tag = soup.find('a', id='link3')
print(last_a_tag)
print('next_sibling的结果是', last_a_tag.next_sibling)
print('next_element的结果是', last_a_tag.next_element)
print('previous_sibling的结果是', last_a_tag.previous_sibling)
print('previous_element的结果是', last_a_tag.previous_element)

#通过 .next_elements 和 .previous_elements 的迭代器就可以向前或向后访问文档的解析内容,就好像文档正在被解析一样
for element in last_a_tag.next_elements:
    print(repr(element))

print("""
================================搜索文档树==============================
""")

#搜索文档树
#字符串过滤器（查找名字为b的tag）
print(soup.find_all('b'))
#正则表达式过滤器（查找所有名字含b的tag）
for tag in soup.find_all(re.compile('b')) :
    print(tag.name)
#列表过滤器，与表中任意元素匹配的都会返回
print(soup.find_all(['a', 'b']))
#True过滤器，可以匹配任何值，查找到所有的tag，但不会返回字符串节点
for tag in soup.find_all(True) :
    print(tag.name)
#方法过滤器，可以定义方法方法只接受一个元素参数，如果这个方法返回True表示能找到
def has_class_but_no_id(tag) :
    return tag.has_attr('class') and not tag.has_attr('id')
print(soup.find_all(has_class_but_no_id))

if __name__ == '__main__':
    pass