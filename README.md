# Event-Classification
## Dataset
* total 36497 chinese news, which is collected from the Internet
* the news in the dataset may be classified into wrong class
## Purpose
* build a classifier, which classifies Chinese news into three events: "financing event"(融资事件), "products release"(产品发布), "other"(其他)
* use the classifier to classify the news we collect on the Internet, which is stored on mongoDB
* provide service to a bussiness intelligence product
## Method
### regular expression
* use regular expression to analyze the title of the news.    For example: if "融资" appear in the title, the news is likely to be "融资事件"
* clearn data:  if the title of "其他" fit the regular expression of other two classes, change the label according to regular expression
### support vector classification
* use jieba to tokenize cleaned data
* use TF-IDF and x2test to select keywords
* set the keywords frequent vector as word vector
* set word vector as X, class of the news as Y, use SVC to implement classification and build classifier
### combine SVC & rules
* use regular expression to clean training data
* if the title of news fits regular expression, apply it;
* if the title of news doesn't fit regular expression, use SVC classifier we built
## Documents
#### clean_data
* loadNews.py: store info of news
* strongRules.py: use regular expression to analzye title; clean data
#### get_classifier
* step1_get_word_vector.py
* step2_seprerate_train_test.py
* step3_classification.py
#### classification
* classify.py: classify the news in the MongoDB
* Event_Classifier.pkl: the SVC classifier
* News_Classifer.pkl: the news classifer (classify news into 17 classes)(method is quite similiar as event classification, as the news label is quite near, we implement mutilabel classification.)
## Products

------------------------
##### Date:   5/4/2017
##### Author: Aining Wang
