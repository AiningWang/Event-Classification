#-*- coding:utf-8 -*-

"""
	use strong rules analyze title of news and classify news
	if strong rules don't work, use classifier to finish the work
	Author: 	Aining Wang
	Reference: 	https://github.com/AiningWang/Event-Classification
"""

from strongRules import RegularExpression
from sklearn.externals import joblib

import jieba.posseg as pseg
import numpy as np

KEYWORD_FILE = "event_keyword.txt"


class EventClassification:

	def __init__(self):
		self.keywords 	= []
		self.title 		= ""
		self.content 	= ""
		self.token_title	= []
		self.token_content 	= []
		self.word_counter 	= {}
		self.word_vector 	= []
		self.predict_type	= ""
		self.clf 			= joblib.load("Event_Classifier.pkl")
	
	def loadKeywords(self, file):
		for line in file:
			line = line.strip("\n")
			self.keywords.append(line)
		return self.keywords


	def token(self):
		words = pseg.cut(self.title)
		for w in words:
			word = w.word.encode('utf-8')
			self.token_title.append(word)
		words = pseg.cut(self.content)
		for w in words:
			word = w.word.encode('utf-8')
			self.token_content.append(word)
	
	
	def getWordVector(self):
		"""
			count words
		"""
		for i in range(len(self.keywords)):
			self.word_counter[self.keywords[i]] = 0
		for i in range(len(self.token_title)):
			if self.token_title[i] in self.word_counter:
				self.word_counter[self.token_title[i]] += 5
		for i in range(len(self.token_content)):
			if self.token_content[i] in self.word_counter:
				self.word_counter[self.token_content[i]] += 1
		"""
			build word vector
		"""
		self.word_vector = []
		for i in range(len(self.keywords)):
			self.word_vector.append(self.word_counter[self.keywords[i]])
		self.word_vector = np.array(self.word_vector).reshape((1, -1))
	
	
	def Classification(self):
		"""
			analzye title
		"""
		p = RegularExpression()
		self.predict_type = p.regularEvalue(self.title)
		if self.predict_type == None:
			self.predict_type = self.clf.predict(self.word_vector)
		self.predict_type = self.predict_type[0].decode('utf-8')


	def execute(self, title, content):
		self.title = title
		self.content = content
		self.token()
		self.getWordVector()
		self.Classification()


if __name__ == '__main__':

	t1 = EventClassification()
	t1.loadKeywords(open(KEYWORD_FILE, "r"))
	title = "美国OpenFin升级技术基础设施"
	content = "2017年2月17日消息，专注于为金融服务公司升级技术基础设施的美国初创公司OpenFin宣布获得1500万美元B轮融资，本次交易的领投方为J.P.摩根、贝恩资本、Euclid Opportunities、DRW Venture Capital、Nyca Partners、Pivot Investment Partners以及部分天使投资人均参与了本轮融资。 　　据创投时报项目库数据显示，OpenFin成立于2010年8月，总部位于美国纽约，是一家专注于为金融服务公司升级技术基础设施的初创公司，通过让交易者以及其他终端客户在公司内部以及对交易买卖双方部署桌面应用从而实现资本市场的现代化。OpenFin将其定义为“资本市场的安卓系统”，该系统能够进行安全的部署并实现实时的更新。 　　OpenFin首席执行官兼联合创始人Mazy Dar表示：“在过去几年里，‘快速的发展以及颠覆性的创新’已经成为硅谷创业的真谛，并创造了加速发展有利可图的消费软件的思维倾向。现在我们这款软件引入华尔街。” 　　"
	t1.execute(title.decode('utf-8'), content.decode('utf-8'))
	print t1.predict_type
	"""
	t1 = EventClassification()
	t1.title = "美国OpenFin为金融公司升级技术基础设施"
	t1.content = "2017年2月17日消息，专注于为金融服务公司升级技术基础设施的美国初创公司OpenFin宣布获得1500万美元B轮融资，本次交易的领投方为J.P.摩根、贝恩资本、Euclid Opportunities、DRW Venture Capital、Nyca Partners、Pivot Investment Partners以及部分天使投资人均参与了本轮融资。 　　据创投时报项目库数据显示，OpenFin成立于2010年8月，总部位于美国纽约，是一家专注于为金融服务公司升级技术基础设施的初创公司，通过让交易者以及其他终端客户在公司内部以及对交易买卖双方部署桌面应用从而实现资本市场的现代化。OpenFin将其定义为“资本市场的安卓系统”，该系统能够进行安全的部署并实现实时的更新。 　　OpenFin首席执行官兼联合创始人Mazy Dar表示：“在过去几年里，‘快速的发展以及颠覆性的创新’已经成为硅谷创业的真谛，并创造了加速发展有利可图的消费软件的思维倾向。现在我们这款软件引入华尔街。” 　　"
	t1.loadKeywords(open(KEYWORD_FILE, "r"))
	t1.token()
	t1.getWordVector()
	print t1.word_vector
	t1.Classification()
	print t1.predict_type
	"""

	
	
	
	
	