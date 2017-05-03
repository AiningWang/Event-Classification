#-*- coding:utf-8 -*-

"""
	use strong rules analyze title of news and classify news
	if strong rules don't work, use classifier to finish the work
	Author: 	Aining Wang
	Reference: 	https://github.com/AiningWang/Event-Classification
"""

from strongRules import RegularExpression
from sklearn.externals import joblib
from sklearn import preprocessing

import jieba.posseg as pseg
import numpy as np
import pymongo
import time


EVENT_KEYWORD_FILE = 	"event_keyword.txt"
NEWS_KEYWORD_FILE = 	"news_keyword.txt"


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
		#map(preprocessing.normalize, self.word_vector)


	def Classification(self):
		"""
			analzye title
		"""
		p = RegularExpression()
		self.predict_type = p.regularEvalue(self.title)
		if self.predict_type == None:
			self.predict_type = self.clf.predict(self.word_vector)
		if type(self.predict_type) != type("s"):
			self.predict_type = self.predict_type[0]
		self.predict_type = self.predict_type.decode('utf-8')


	def execute(self, title, content):
		self.title = title
		self.content = content
		self.token()
		self.getWordVector()
		self.Classification()



			
class NewsClassification:
	def __init__(self):
		self.keywords 	= []
		self.title 		= ""
		self.content 	= ""
		self.token_title	= []
		self.token_content 	= []
		self.word_counter 	= {}
		self.word_vector 	= []
		self.predict_type	= ""
		self.clf 			= joblib.load("News_Classifier.pkl")


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
		self.word_vector = preprocessing.normalize(self.word_vector)


	def Classification(self):
		"""
			classify
		"""
		self.predict_type = []
		predict_type = []
		predict_value = self.clf.predict_proba(self.word_vector)[0]
		for i in range(len(predict_value)):
			if predict_value[i] >= 0.2:
				predict_type.append(i + 1)
				
		"""
			turn type num into type
		"""
		type_dict = {1: "教育", 2: "金融", 3: "汽车交通", 4: "房产服务", 5: "医疗健康", 6: "旅游", 7: "本地生活", 8: "游戏", 9: "广告营销", 10: "硬件", 11: "文化娱乐", 12: "企业服务", 13: "社交网络", 14: "电子商务", 15: "工具软件", 16: "体育运动", 17: "物流"}
		for i in range(len(predict_type)):
			self.predict_type.append(type_dict[predict_type[i]])
		for k in range(len(self.predict_type)):
			self.predict_type[k] = self.predict_type[k].decode('utf-8')
		
		
	def execute(self, title, content):
		self.title = title
		self.content = content
		self.token()
		self.getWordVector()
		self.Classification()




class Classify:
	def __init__(self):
		self.content 	= ""
		self.title 		= ""
		self.news_classify 	= NewsClassification()
		self.event_classify = EventClassification()
		self.news_classify.loadKeywords(open(NEWS_KEYWORD_FILE, "r"))
		self.event_classify.loadKeywords(open(EVENT_KEYWORD_FILE, "r"))
		
	
	def execute(self):
		client 		= pymongo.MongoClient("192.168.1.31", 27017)
		database 	= client["data"]
		collection 	= database["news_data"]
		while(1):
			document = collection.find_one({"classified": None})
			
			if document == None:
				"""
					if no news unclassified, sleep 20 second
				"""
				time.sleep(20)
				continue

			try:
				document["title"] + document["content"]
			except:
				collection.update({"_id": document["_id"]}, {"$set": {"classified": 0}})
			else:
				self.title = document["title"]
				self.content = document["content"]
				self.news_classify.execute(self.title, self.content)
				self.event_classify.execute(self.title, self.content)
				collection.update({"_id": document["_id"]}, {"$set": {"category": 	self.news_classify.predict_type}})
				collection.update({"_id": document["_id"]}, {"$set": {"event": 		self.event_classify.predict_type}})
				collection.update({"_id": document["_id"]}, {"$set": {"classified": 1}})
				print self.event_classify.predict_type, self.news_classify.predict_type
	
	
	def delect(self):
		client 		= pymongo.MongoClient("192.168.1.31", 27017)
		database 	= client["data"]
		collection 	= database["news_data"]
		while(1):
			document = collection.find_one({"classified": 1})
			collection.update({"_id": document["_id"]}, {"$set": {"classified": 2}})



if __name__ == '__main__':
	c = Classify()
	#c.delect()
	c.execute()
	"""
	t1 = EventClassification()
	t1.title = "美国OpenFin基础设施"
	t1.content = "2017年2月17日消息，专注于为金融服务公司升级技术基础设施的美国初创公司OpenFin宣布获得1500万美元B轮融资，本次交易的领投方为J.P.摩根、贝恩资本、Euclid Opportunities、DRW Venture Capital、Nyca Partners、Pivot Investment Partners以及部分天使投资人均参与了本轮融资。 　　据创投时报项目库数据显示，OpenFin成立于2010年8月，总部位于美国纽约，是一家专注于为金融服务公司升级技术基础设施的初创公司，通过让交易者以及其他终端客户在公司内部以及对交易买卖双方部署桌面应用从而实现资本市场的现代化。OpenFin将其定义为“资本市场的安卓系统”，该系统能够进行安全的部署并实现实时的更新。 　　OpenFin首席执行官兼联合创始人Mazy Dar表示：“在过去几年里，‘快速的发展以及颠覆性的创新’已经成为硅谷创业的真谛，并创造了加速发展有利可图的消费软件的思维倾向。现在我们这款软件引入华尔街。” 　　"
	t1.loadKeywords(open(EVENT_KEYWORD_FILE, "r"))
	t1.token()
	t1.getWordVector()
	t1.Classification()
	print t1.predict_type
	"""
	"""
	t1 = NewsClassification()
	t1.title = "美国OpenFin基础设施"
	t1.content = "滴滴出行与东方航空达成战略合作 打通旅游出行场景 阿克西姆 · 2016-10-10 10月10日消息，滴滴出行宣布已与东方航空达成战略合作伙伴关系，双方将在产品、会员权益、市场营销等方面展开合作，通过打通双方线上产品，连接机舱到车厢的整体出行场景，携手打造空地联运生态圈，为双方用户提供旅游出行一站式便捷服务。 据悉双方的移动应用程序上正在逐步接入对方产品，目前旅客在东方航空APP页面中选择“接送机”即可快速发出滴滴订单。未来东方航空的旅客在东方航空APP和官网购买机票和度假产品时，可打包一同购买滴滴专车的接送机服务。用户可提前预约好车辆，下了飞机后将由滴滴专车接机员在到达口接机并引导上车，遇到航班延误仍将有专车在机场守候，实现航空与地面交通的无缝衔接。东航飞机客舱、东航机场贵宾厅还将进一步整合滴滴专车产品，例如用户可在东航航班飞行中依靠空中互联技术预定接机专车。此外，在开放共享的合作基础上，滴滴将与东方航空在会员权益方面展开合作。 滴滴方面表示，滴滴一直不断尝试新的模式，以满足用户不断增长的多元化需求。目前滴滴已推出包括出租车、专车、快车、顺风车、代驾、试驾、公交、企业级以及租车在内的多种出行解决方案，并通过独有的平台优势使用户享有协同效应。 未来滴滴将进一步发展“潮汐战略”，通过大数据的深入挖掘与应用，智能调配体系连接多种交通工具，不断提升平台效率，降低成本，让用户出行更加高效便捷。此次与东航达成战略合作，依托其覆盖全球的航空资源和庞大用户基础，希望共同为商旅用户提供从乘车到登机的一站式服务，同时协助提升机场运行效率，让出行变得更加高效。 目前移动互联网、云计算和大数据技术的发展已经引起了交通领域的巨大变革，与以往多产业分离的单一生态环境不同，如今的“大交通”将是多方结合的协同产业。此次滴"
	t1.loadKeywords(open(NEWS_KEYWORD_FILE, "r"))
	t1.token()
	t1.getWordVector()
	t1.Classification()
	print t1.predict_type
	"""
	
	
	
	