#coding=utf-8
import threading
import time
import re
import urllib2
import urllib
import requests
import lxml.html
from bs4 import BeautifulSoup
import cookielib
import gzip

#设置参数，主要有headers，post_data，url三个，返回一个字典类型
def SET_PARAMETER():
    headers = {"Host":"www.cnvd.org.cn",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer":"http://www.google.com",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "Content-Type":"application/x-www-form-urlencoded"}

    page_num = raw_input("Please input the page number:")
    data = {"keyword":"tomcat","offset":int(page_num)*20}
    post_data = urllib.urlencode(data)

    url = 'http://www.cnvd.org.cn/flaw/list.htm?flag=true'

    return {"url":url,"post_data":post_data,"headers":headers}

#传入url，headers和postdata，得到网站的html
def GET_HTML(url,headers,post_data):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    request = urllib2.Request(url,headers=headers,data=post_data)
    response = opener.open(request)
    html = response.read()
    return html

#处理html，匹配出漏洞标题，风险等级和发布时间
def MATCH(html):
    bsObj = BeautifulSoup(html,'lxml')
    for buginfo in bsObj.find_all("tr",class_=re.compile(r'')):
        title = re.findall(re.compile(r'<a href="/flaw/show/CNVD-\d{4}-\d{5}".*?title="(.*?)">'),str(buginfo))
        #print title
        title[0] = title[0].strip()
        level = re.findall(re.compile(r'</span>\s*?(.*?)\s*?</td>'),str(buginfo))
        #print level
        level[0] = level[0].strip()
        date = re.findall(re.compile(r'<td width="13%">\s*?(.*?)\s*?</td>'),str(buginfo))
        #print date
        date[0] = date[0].strip()
        buginfo_group = title+[" "]+level+[" "]+date+["\n"]
        LOG(buginfo_group)

#记录函数，将匹配结果输出到文本
def LOG(group):
    text = open("C:\\Users\\ChengWiLL\\Desktop\\hehe.txt",'ab')
    text.writelines(group)
    text.close()
def WORK():
    parameter = SET_PARAMETER()
    html = GET_HTML(parameter["url"],parameter["headers"],parameter["post_data"])
    MATCH(html)
WORK()
