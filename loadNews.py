#-*- coding:utf-8 -*-

"""
	store infomation of news
	implement some basic NLP operation, including tokenization
	
	Author: 	Aining Wang
	Reference: 	https://github.com/AiningWang/Event-Classification
"""

import jieba.posseg as pseg


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
			if len(line) == 4 and len(line[2]) > 100:
				one.getInfo(line)
				self.news_dict[one.news_num] = one
				self.num_of_news += 1
		file.close()
		del one


	def loadTokenInfo(self):
		for news_num in self.news_dict:
			self.news_dict[news_num].tokenNewsTitle()


