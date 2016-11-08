import urllib
import urllib2
import re

class BDTB:
	def __init__(self,baseUrl,seeLZ):
		self.baseUrl=baseUrl
		self.seeLZ='?see_lz='+str(seeLZ)
	
	def getPage(self,pageNum):
		try:
			headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
			url=self.baseUrl+self.seeLZ+'&pn='+str(pageNum)
			request=urllib2.Request(url,headers=headers)
			response=urllib2.urlopen(request)
			#print response.read().decode("utf-8")
			return response
		except urllib2.URLError,e:
			if hasattr(e,"reason"):
				print u"Connect Failed:",e.reason
				return None
	
	def getTitle(self):
		page=self.getPage(1)
		pattern=re.compile('<h3 class="core_title_txt pull-left text-overflow ".*?>(.*?)</h3>',re.S)
		result=re.search(pattern,page.read())
		if result:
			return result.group(1).strip()
		else:
			return None
			
	def getPageNum(self):
		page=self.getPage(1)
		pattern=re.compile('<li class="l_reply_num".*?>.*?<span class="red">(.*?)</span>')
		result=re.search(pattern,page.read())
		if result:
			return result.group(1).strip()
		else:
			return None
			
	def getContent(self,page):
		pattern=re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items=re.findall(pattern,page.read().decode("utf-8"))
		return items
		#for item in items:
		#	print item

class Filter_vat:
	removeImg=re.compile('<img.*?>| {7}')
	removeLinks=re.compile('<a.*?>|</a>')
	replaceLine=re.compile('<tr>|<div>|</div>|</p>')
	replaceTD=re.compile('<td>')
	replacePara=re.compile('<p.*?>')
	replaceBR=re.compile('<br><br>|<br>')
	removeExtraTag=re.compile('<.*?>')
	def filter_and_replace(self,x):
		x=re.sub(self.removeImg,"",x)
		x=re.sub(self.removeLinks,"",x)
		x=re.sub(self.replaceLine,"\n",x)
		x=re.sub(self.replaceTD,"\t",x)
		x=re.sub(self.replacePara,"\n",x)
		x=re.sub(self.replaceBR,"\n",x)
		x=re.sub(self.removeExtraTag,"",x)
		return x.strip()
baseURL='http://tieba.baidu.com/p/3138733512'
bdtb=BDTB(baseURL,1)
#bdtb.getPageNum()
#bdtb.getTitle()
pageContents=bdtb.getContent(bdtb.getPage(1))
filter=Filter_vat()
for pageContent in pageContents:
	lz_invitation_post=filter.filter_and_replace(pageContent)
	print "----------------------------------------------------------------------------------------\n"
	print lz_invitation_post
	print '\n'
