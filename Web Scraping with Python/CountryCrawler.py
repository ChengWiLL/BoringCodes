# coding=utf-8
import re
import urllib2
import urlparse
import robotparser
import time
import Queue
from datetime import datetime

rp=robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()

class Throttle:
    def __init__(self,delay):
        self.delay=delay
        self.domains={}
    def wait(self,url):
        domain=urlparse.urlparse(url).netloc
        last_accessed=self.domains.get(domain)
        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.datetime.now()-last_accessed).seconds
            if sleep_secs>0:
                time.sleep(sleep_secs)
        self.domains[domain]=datetime.datetime.now()

def download(url,user_agent='wswp',proxy=None,num_retries=2,delay=0):
    throttle=Throttle(delay)
    print 'Downloading:',url
    headers={'User-agent':user_agent}
    request=urllib2.Request(url, headers=headers)
    opener=urllib2.build_opener()
    if proxy:
        proxy_params={urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html=opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                throttle.wait(url)
                html=download(url,user_agent,proxy,num_retries-1,delay)
    return html

def link_crawler(seed_url,link_regex,max_depth=2):
    max_depth=2
    crawl_queue=[seed_url]
    seen={seed_url:0}

    while crawl_queue:
        url=crawl_queue.pop()
        if rp.can_fetch("user_agent",url):
            html=download(url)
            depth=seen[url]
            for link in get_links(html):
                if re.match(link_regex,link):
                    link=urlparse.urljoin(seed_url,link)
                    if depth!=max_depth:
                        if link not in seen:
                            seen[link]=depth+1
                            crawl_queue.append(link)
        else:
            print 'Blocked by robots.txt:',url

def get_links(html):
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    return webpage_regex.findall(html)
link_crawler('http://example.webscraping.com','/(index|view)')
