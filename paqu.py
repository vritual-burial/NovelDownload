import requests
from lxml import etree
import sys
from bs4 import BeautifulSoup
import re
import urllib.parse

print("请输入下载小说的名字：")
name=input()

url1 = 'http://www.xqb5.cc/search/?searchkey=' + urllib.parse.quote(name)
print(url1)

url="http://www.xqb5.cc"
req=requests.get(url1)
list_page1=etree.HTML(req.text)
book_list = list_page1.xpath("//dt/a/@title")

found = False
book_index = None
for index, book in enumerate(book_list):
    if book == name:
        book_index = index
        break

if book_index is not None:
    print("找到小说，正在下载...")
    url2=list_page1.xpath("//dt/a/@href")[book_index]
    print(url2)  
else:
    print("未找到该书籍，请核实后重新运行")
    sys.exit()

full_url2 = urllib.parse.urljoin(url, url2)
print(full_url2)
req=requests.get(full_url2)

list_page2=etree.HTML(req.text)
print(list_page2)
#url3=list_page2.xpath("//div[@id='randbtn']/a//@href")
#req=requests.get('http://www.xqb5.cc'+url3)
url3_list = list_page2.xpath("//div[@class='readbtn']/a//@href")[1:2]
txt_name= list_page2.xpath("//h1/text()")

print(txt_name)

full_url3 = urllib.parse.urljoin(url, url3_list[0])
#req = requests.get('http://www.xqb5.cc' + url3_list[0])
req = requests.get(full_url3)
list_page3 = etree.HTML(req.text)
print(list_page3)



file_name=f'./{txt_name}.txt'
list_a=list_page3.xpath("//div[@id='content_1']/a//@href")[0:]
list_a=[url+i for i in list_a]
for i in list_a:
    req=requests.get(i)
    data_page=etree.HTML(req.text)
    data_title=data_page.xpath("//h1/text()")[0]
    data_list=data_page.xpath("//div[@id='booktxt']//text()")[1:]
    data="\n".join(data_list)
    this_chapter=f"\n{data_title}\n{data}"
    with open(file=file_name ,mode="a",encoding='UTF-8')as f:
        f.write(this_chapter)
    print(f'{data_title}--下载完成!')    

  