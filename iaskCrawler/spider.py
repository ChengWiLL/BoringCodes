# coding=utf-8
import urllib
import urllib2
import re
import time
import types
import page
import mysql
import sys
from bs4 import BeautifulSoup

class Spider:
	def __init__(self):
		self.page_num=1
		self.total_num=1
		self.page_spider=page.Page()
		self.mysql=mysql.Mysql()

	def getCurrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time() ))
	def getCurrentDate(self):
		return time.strftime('%Y-%m-%d',time.localtime(time.time() ) )
		
	def getPageURLByNum(self,page_num):
		page_url="http://iask.sina.com.cn/c/978-all-"+str(page_num)+"-new.html"
		return page_url
	
	def getPageByNum(self,page_num):
		request=urllib2.Request(self.getPageURLByNum(page_num) )
		try:
			response=urllib2.urlopen(request,data=None,timeout=3)
		except urllib2.URLError,e:
			if hasattr(e,"code"):
				print self.getCurrentTime(),"获取页面失败，错误代号",e.code
				return None
			if hasattr(e,"reason"):
				print self.getCurrentTime(),"获取页面失败，原因",e.reason
				return None
		else:
			pagecontent=response.read()
			return pagecontent
			
	def getTotalPageNum(self):
		print self.getCurrentTime(),"正在获取目录页面个数，请稍后"
		pagecontent=self.getPageByNum(1)
		pattern=re.compile(r'<div class="pages".*?"(.*?)".*?>')
		number=re.search(pattern,pagecontent)
		if number.group(1):
			return int(number.group(1))
		else:
			print self.getCurrentTime(),"获取总页码失败"
			return 0
			
	def getQuestionInfo(self,question):
		if not type(question) is types.StringType:
			question=str(question)
		pattern=re.compile(r'<div class="question-title">.*?<a href="(.*?)".*?>(.*?)</a>.*?<span class="fl answer_num db">(.*?)</span>.*?<span>(.*?)</span>')
		match=re.search(pattern,question)
		if match:
			questionLink=match.group(1)
			questTitle=match.group(2)
			answer_num=match.group(3)
			questTime=match.group(4)
			time_pattern=re.compile('\d{4}\-\d{2}\-\d{2}',re.S)
			time_match=re.search(time_pattern,questTime)
			if not time_match:
				time=self.getCurrentDate()
			return [questionLink,questTitle,answer_num,questTime]
		else:
			return None
			
	def getQuestions(self,page_num):
		pagecontent=self.getPageByNum(page_num)
		soup=BeautifulSoup(pagecontent,"lxml")
		questions=soup.select("div.q_questions_list ul li")
		for question in questions:
			info=self.getQuestionInfo(question)
			if info:
				url="http://iask.sina.com.cn"+info[0]
				ans=self.page_spider.getAnswer(url)
				print self.getCurrentTime(),"当前爬取第",page_num,"页的内容，发现一个问题",info[2],"回答数量",info[3]
				ques_dict={
							"text": info[1],
                            "ans_num": info[2],
                            "url": url
							}
				insert_id=self.mysql.insertData("iask_questions",ques_dict)
				good_ans=ans[0]
				print self.getCurrentTime(),"保存到数据库，此问题的ID为",insert_id
				if good_ans:
					print self.getCurrentTime(),insert_id,"号问题存在最佳答案",good_ans[0]
					good_ans_dict={
							"text": good_ans[0],
                            "answerer": good_ans[1],
                            "date": good_ans[2],
                            "is_good": str(good_ans[3]),
                            "question_id": str(insert_id)
							}
					if self.mysql.insertData("iask_answer",good_ans_dict):
						print self.getCurrentTime(),"保存最佳答案成功"
					else:
						print self.getCurrentTime(),"保存最佳答案失败"
				other_anses=ans[1]
				for other_ans in other_anses:
					if other_ans:
						print self.getCurrentTime(),insert_id,"号问题存在其他答案",other_ans[0]
						other_ans_dict={
								"text": other_ans[0],
                                "answerer": other_ans[1],
                                "date": other_ans[2],
                                "is_good": str(other_ans[3]),
                                "question_id": str(insert_id)
								}
						if self.mysql.insertData("iask_answers",other_ans_dict):
							print self.getCurrentTime(),"保存其他答案成功"
						else:
							print self.getCurrentTime(),"保存其他答案失败"
	def savePageNum(self):
		f_handler=open('out.log','w')
		sys.stdout=f_handler
		pagecontent=open('page.txt','ab+')
		content=pagecontent.readline()
		start_page=int(content.strip())
		pagecontent.close()
		print self.getCurrentTime(),"开始页码",start_page
		print self.getCurrentTime(),"爬虫正在启动，开始爬取爱问知识人的问题"
		self.total_num=self.getTotalPageNum()
		print self.getCurrentTime(),"获取到目录页面个数",self.total_num,"页"
		
		for x in range(start_page,self.total_num):
			print self.getCurrentTime(),"正在抓取第",x,"个页面"
			try:
				self.getQuestions(x)
			except urllib2.URLError,e:
				if hasattr(e,"reason"):
					print self.getCurrentTime(),"某总页面内抓取或提取失败，错误原因",e.reason
				if x<self.total_num:
					f=open('page.txt','w')
					f.write(str(x))
					print self.getCurrentTime(),"写入新页码",x
					f.close()
					pass

			except Exception,e:
				print self.getCurrentTime(),"某总页面内抓取或提取失败，错误原因",e
				if x<self.total_num:
					f=open('page.txt','w')
					f.write(str(x))
					print self.getCurrentTime(),"写入新页码",x
					f.close()
					pass

spider=Spider()
spider.savePageNum()
