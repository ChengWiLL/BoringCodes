# coding=utf-8
import urllib
import urllib2
import re
import time
import types 
import tool
from bs4 import BeautifulSoup

class Page:
	def __init__(self):
		self.tool=tool.Tool()
	def getCurrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time() ))
	def getCurrentDate(self):
		return time.strftime('%Y-%m-%d',time.localtime(time.time() ) )
	def getPageByURL(self,url):
		try:
			request=urllib2.Request(url)
			response=urllib2.urlopen(request)
			return response.read()
		except urllib2.URLError,e:
			if hasattr(e,"code"):
				print self.getCurrentTime(),"获取问题页面失败，错误代号",e.code
				return None
			if hasattr(e,"reason"):
				print self.getCurrentTime(),"获取页面失败，原因",e.reason
				return None
				
	def getText(self,html):
		if not type(html) is types.StringType:
			html=str(html)
		pattern=re.compile(r'<pre.*?>(.*?)</pre>',re.S)
		match=re.search(pattern,html)
		if match:
			return match.group(1)
		else:
			return None
			
	def getGoodAnswerInfo(self,html):
		pattern=re.compile(r'<div class="answer_tip clearfix">.*?>(.*?)</a>.*?> | (.*?)</span>',re.S)
		match=re.search(pattern,html)
		if match:
			Time=match.group(2)
			time_pattern=re.compile(r'\d{2}\-\d{2}\-\d{2}',re.S)
			time_match=re.search(time_pattern,Time)
			if not time_match:
				Time=self.getCurrentDate()
			else:
				Time="20"+Time
			return [match.group(1),Time]
		else:
			return [None,None]
	
	def getGoodAnswer(self,page):
		soup=BeautifulSoup(page,"lxml")
		text=soup.select("div.good_point div.answer_text pre")
		if len(text)>0:
			ansText=self.getText(str(text[0]) )
			ansText=self.tool.replace(ansText)
			info=soup.select("div.good_point div.answer_tip")
			ansInfo=self.getGoodAnswerInfo(str(info[0]) )
			answer=[ansText,ansInfo[0],ansInfo[1],1 ]
			return answer
		else:
			return None
			
	def getOtherAnswerInfo(self,html):
		if not type(html) is types.StringType:
			html=str(html)
		pattern=re.compile(r'<div id="answer_user_info".*?<a class="author_name".*?>(.*?)</a>.*?<span class="answer_t">(.*?)</span>',re.S)
		match=re.search(pattern,html)
		if match:
			Time=match.group(2)
			time_pattern=re.compile(r'\d{2}\-\d{2}\-\d{2}',re.S)
			time_match=re.search(time_pattern,Time)
			if not time_match:
				Time=self.getCurrentDate()
			else:
				Time="20"+Time
			return [match.group(1),Time]
		else:
			return [None,None]
			
	def getOtherAnswers(self,page):
		soup=BeautifulSoup(page,"lxml")
		results=soup.select("div.question_box li.clearfix .answer_info")
		answers=[]
		for result in results:
			ansSoup=BeautifulSoup(str(result),"lxml" )
			text=ansSoup.select(".answer_txt span pre")
			ansText=self.getText(str(text[0]) )
			ansText=self.tool.replace(ansText)
			info=ansSoup.select(".answer_tj")
			ansInfo=self.getOtherAnswerInfo(info[0])
			answer=[ansText,ansInfo[0],ansInfo[1],0]
			answers.append(answer)
		return answers
		
	def getAnswer(self,url):
		if not url:
			url="http://iask.sina.com.cn"
		page = self.getPageByURL(url)
		good_ans = self.getGoodAnswer(page)
		other_ans = self.getOtherAnswers(page)
		return [good_ans,other_ans]