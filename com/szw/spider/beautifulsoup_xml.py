#!/usr/bin/env python
# encoding: utf-8

"""
@author: WillSo
@license: Apache Licence 
@software: PyCharm
@file: beautifulsoup_xml.py
@time: 2017\10\11 0011 11:19
"""

from bs4 import BeautifulSoup

xml_text = """
<DOCUMENT>
<USER>
<NAME>WillSo</NAME>
<AGE>23</AGE>
</USER>
<USER2>
<NAME>King</NAME>
<AGE>33</AGE>
</USER2>
</DOCUMENT>
"""
soup = BeautifulSoup(xml_text, 'xml')

print(soup)

if __name__ == '__main__':
    pass