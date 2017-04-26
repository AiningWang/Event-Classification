#-*- coding:utf-8 -*-

import jieba.posseg as pseg
import re
import time

FILE1 = "sample.txt"


class NewsInfo:
	"""
		Store the basic infomation of one piece of news
	""" 
	def __init__(self):
		"""
			@type_num: 0: 融资事件 1: 产品发布 2: 其他 None: 未设置
			@token: tokenized news (title + content)
		"""
		self.title 		= ""
		self.content 	= ""
		self.type 		= ""
		self.type_num 	= 3
		self.news_num 	= None
		self.token_title	= []
		self.token_content 	= []
		self.predict_type_num= None


	def getInfo(self, line):
		"""
			format of line is as follows:
			news_num \t title \t content \t type \n
		"""
		type_dict = {"融资事件": 0, "产品发布": 1, "其他": 2}
		self.title 		= line[1]
		self.content	= line[2]
		self.type 		= line[3]
		self.news_num 	= int(line[0])
		self.type_num 	= type_dict[self.type]


	def tokenNewsTitle(self):
		words = pseg.cut(self.title)
		for w in words:
			word = w.word.encode('utf-8')
			self.token_title.append(word)
		words = pseg.cut(self.content)
		for w in words:
			word = w.word.encode('utf-8')
			self.token_content.append(word)
		print self.token_title



class NewsSet:
	"""
		Store infomation of all news 
		@ news_dict store infomation of all news, news_dict[news_num]:NewsInfo
	"""
	def __init__(self):
		self.num_of_news = 0
		self.news_dict = {}


	def loadBasicInfo(self, file):
		"""
			@one: temporarily store one piece of news
		"""
		for line in file:
			line = line.strip("\n").split("\t")
			one = NewsInfo()
			if len(line) == 4:
				one.getInfo(line)
				self.news_dict[one.news_num] = one
				self.num_of_news += 1
		file.close()
		del one


	def loadTokenInfo(self):
		for news_num in self.news_dict:
			self.news_dict[news_num].tokenNewsTitle()



class RegularExpression:
	"""
		use regular expression to analyze title of news
	"""

	def __init__(self):
		"""
			higher finance_score, more likely the news be "融资事件"
			higher product_score, more likely the news be "产品发布"
		"""
		self.finance_score = 0
		self.product_score = 0


	def financeEvalue(self, title):
		self.finance_score = 0
		pattern1 = re.compile(r'投.*?融资')
		pattern2 = re.compile(r'融资')
		pattern3 = re.compile(r'投资')
		pattern4 = re.compile(r'收购')
		r1 = re.match(pattern1, title)
		r2 = re.match(pattern2, title)
		r3 = re.match(pattern3, title)
		r4 = re.match(pattern4, title)
		if r1 != None:
			self.finance_score += 1
		if r2 != None:
			self.finance_score += 1
		if r3 != None:
			self.finance_score += 1
		if r4 != None:
			self.finance_score += 1


	def productEvalue(self, title):
		self.product_score = 0
		pattern1 = re.compile(r'发布')
		pattern2 = re.compile(r'上线')
		pattern3 = re.compile(r'产品')
		pattern4 = re.compile(r'推出')
		pattern5 = re.compile(r'市场')
		r1 = re.match(pattern1, title)
		r2 = re.match(pattern2, title)
		r3 = re.match(pattern3, title)
		r4 = re.match(pattern4, title)
		r5 = re.match(pattern5, title)
		if r1 != None:
			self.product_score += 1
		if r2 != None:
			self.product_score += 1
		if r3 != None:
			self.product_score += 1
		if r4 != None:
			self.product_score += 1
		if r5 != None:
			self.product_score += 1


	def financeEvalue2(self, title):
		self.finance_score = 0
		if title.find("融资") != -1:
			self.finance_score += 1
		if title.find("投资") != -1:
			self.finance_score += 1
		if title.find("收购") != -1:
			self.finance_score += 1
		if title.find("获投") != -1:
			self.finance_score += 1


	def productEvalue2(self, title):
		self.product_score = 0
		if title.find("发布") != -1:
			self.product_score += 1
		if title.find("上线") != -1:
			self.product_score += 1
		if title.find("产品") != -1:
			self.product_score += 1
		if title.find("推出") != -1:
			self.product_score += 1


	def regularEvalue(self, title, file):
		self.financeEvalue2(title)
		self.productEvalue2(title)
		file.write(str(self.finance_score) + "\t" + str(self.product_score) + "\t" + title + "\n")
		print self.finance_score, self.product_score
		if self.finance_score > self.product_score:
			return 0
		elif self.finance_score < self.product_score:
			return 1
		else:
			return None



if __name__ == '__main__':
	file = open("output.txt", "w")
	file2 = open("output2.txt", "w")
	p = NewsSet()
	p.loadBasicInfo(open(FILE1, "r"))
	print p.num_of_news
	q = RegularExpression()
	for news_num in p.news_dict:
		title = p.news_dict[news_num].title
		real = p.news_dict[news_num].type_num
		predict = q.regularEvalue(title, file2)
		file.write(str(news_num) + "\t" + str(real) + "\t" + str(predict) + "\t" + title + "\n")
	file.close()
	file2.close()


