#-*- coding:utf-8 -*-


"""
	use strong rules analyze title of news
	as there are wrong labeled data in dataset, we use the result of strong rules to correct them

	Author: 	Aining Wang
	Reference: 	https://github.com/AiningWang/Event-Classification
"""

INPUT_FILE = "news_itjz_event_0411.txt"
OUTPUT_FILE = "cleaned_news.txt"


from loadNews import NewsSet


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
		if title.find(("融资").decode('utf-8')) != -1:
			self.finance_score += 1
		if title.find(("投资").decode('utf-8')) != -1:
			self.finance_score += 1
		if title.find(("收购").decode('utf-8')) != -1:
			self.finance_score += 1
		if title.find(("获投").decode('utf-8')) != -1:
			self.finance_score += 1


	def productEvalue(self, title):
		self.product_score = 0
		if title.find(("发布").decode('utf-8')) != -1:
			self.product_score += 1
		if title.find(("上线").decode('utf-8')) != -1:
			self.product_score += 1
		if title.find(("产品").decode('utf-8')) != -1:
			self.product_score += 1
		if title.find(("推出").decode('utf-8')) != -1:
			self.product_score += 1


	def regularEvalue(self, title):
		self.financeEvalue(title)
		self.productEvalue(title)
		if self.finance_score > self.product_score:
			return "融资事件"
		elif self.finance_score < self.product_score:
			return "产品发布"
		else:
			return None



class CleanLabeledData:
	"""
		Rules:
		1. if the type is "其他", but the title is labeled as "融资事件" or "产品发布" according to strong rules, we change the label
		2. we store the cleaned data into new file
	"""

	def __init__(self):
		self.real 	= ""
		self.predict= ""
		self.title 	= ""


	def clean(self, input_filename, output_filename):
		data = NewsSet()
		data.loadBasicInfo(open(input_filename, "r"))
		evalue = RegularExpression()
		output_file = open(OUTPUT_FILE, "w")
		for news_num in data.news_dict:
			self.real = data.news_dict[news_num].type
			self.title = data.news_dict[news_num].title
			self.predict = evalue.regularEvalue(self.title)
			if self.real == "其他" and (self.predict == "融资事件" or self.predict == "产品发布"):
				print self.real, self.predict
				output_file.write(str(data.news_dict[news_num].news_num) + "\t" + self.title + "\t" + str(data.news_dict[news_num].content)+ "\t" + self.predict +"\n")
			else:
				output_file.write(str(data.news_dict[news_num].news_num) + "\t" + self.title + "\t" + str(data.news_dict[news_num].content)+ "\t" + self.real +"\n")
		output_file.close()
		del data
		del evalue



if __name__ == '__main__':
	p = CleanLabeledData()
	p.clean(INPUT_FILE, OUTPUT_FILE)










