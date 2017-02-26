#coding=utf-8
import threading
import re
import urllib2
import urllib
import lxml.html
from bs4 import BeautifulSoup
import csv

text = open("C:\\Users\\ChengWiLL\\Desktop\\hehe.txt",'ab')
csvfile = open("C:\\Users\\ChengWiLL\\Desktop\\python\\crawl\\trsCrawl\\city.csv")
csvReader = csv.reader(csvfile)

def page_loop(city):
    beginPage = 1
    while(beginPage<3):
        targetUrl = "http://www.baidu.com/s?wd=inurl:/was5/web/&pn=%d&oq=inurl:/was5/web/&tn=monline_3_dg&ie=utf-8" % ((beginPage-1)*10)

        request = urllib2.Request(targetUrl)

        response = urllib2.urlopen(request)

        html = response.read()

        soup = BeautifulSoup(html,"lxml")

        infoGroup = soup.find_all("div","result c-container ")

        for info in infoGroup:
            title = info.h3.a.get_text().encode("utf-8")
            if re.search(city,title):
                target = info.select(".c-showurl")
                url = target[0].find_all(text=re.compile(r'gov'))
                text.writelines(str(url[0])+"\n")
        beginPage = beginPage+1

def city_loop():
    for row in csvReader:
        print "Crawling: ",row[0].decode('utf-8')
        page_loop(row[0])

city_loop()
csvfile.close()
text.close()
