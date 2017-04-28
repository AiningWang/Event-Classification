#-*- coding:utf-8 -*-

import numpy as np
import time
import jieba.posseg as pseg
from sklearn import preprocessing


def Load_Keywords(file):
    keywords = []
    for line in file:
        line = line.strip("\n")
        keywords.append(line)
    return keywords


def Load_News(line):
    line = line.strip("\n").split("\t")
    type = line[3]
    content = line[2]
    title = line[1]
    label = int(line[0])
    news = title * 5 + content
    return label, type, news


def Get_Word_Vector(news, keywords):
    words = pseg.cut(news)
    keywords_counter = {}
    word_vector = []
    # set up counter
    for keyword in keywords:
        keywords_counter[keyword] = 0
    # count keywords
    for w in words:
        word = w.word.encode('utf-8')
        if word in keywords:
            keywords_counter[word] += 1
    # turn dict to list
    for i in range(len(keywords)):
        word_vector.append(keywords_counter[keywords[i]])
    # normalization
    word_vector = np.array(word_vector).reshape((1,-1))
    word_vector = preprocessing.normalize(word_vector)[0]
    return word_vector

def Output_Dataset(file, dataset):
    for type in dataset:
        for label in dataset[type]:
            for i in range(len(dataset[type][label])):
                file.write(str(dataset[type][label][i]) + "\t")
            file.write(type + "\t" + str(label) + "\n")


if __name__ == '__main__':
    
    file1 = open("cleaned_news.txt", "r")
    file2 = open("event_keyword.txt", "r")
    file3 = open("dataset.txt", "w")
    
    keyword_list = []
    all_data_set = {} # set[type][label] = word_vector
    train_data_set = {}
    test_data_set = {}
    
    # load keywords
    keywords = Load_Keywords(file2)
    
    # preprocess all data set
    j = 0
    for line in file1:
        j += 1
        if j % 100 == 0:
            print j
        try:
            t = line.strip("\n").split("\t")[3]
        except:
            continue
        else:
            label, type, news = Load_News(line)
            word_vector = Get_Word_Vector(news, keywords)
            if type not in all_data_set:
                all_data_set[type] = {}
            all_data_set[type][label] = word_vector
    Output_Dataset(file3, all_data_set)
