# -*- coding: utf-8 -*-

import urllib
import urllib2
import re

page=1
url='http://www.qiushibaike.com/hot/page/'+str(page)
user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers={'User-Agent':user_agent}
try:
	request=urllib2.Request(url,headers=headers)
	response=urllib2.urlopen(request)
	content=response.read().decode("utf-8")
	pattern=re.compile('<div.*?author clearfix">.*?<a.*?<img.*?<a.*?>.*?<h2>(.*?)</h2>.*?<a.*?<span>(.*?)</span>.*?</a>.*?<div.*?<i class="number">(.*?)</i>.*?</div>',re.S)
	items=pattern.findall(content)
	for item in items:
		print u'发布人:'+item[0]
		print u'段子:'+item[1]
		print u'点赞数:'+item[2]
		print '\n'
except urllib2.URLError,e:
	if hasattr(e,"code"):
		print e.code
	if hasattr(e,"reason"):
		print e.reason
