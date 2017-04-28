#-*- coding:utf-8 -*-

import numpy as np
import time
from sklearn import svm
from sklearn.externals import joblib


def Load_Data_Set(file):
    dataset = {}
    for line in file:
        line = line.strip("\n").split("\t")
        label = int(line[len(line) - 1])
        type = line[len(line) - 2]
        word_vector = line[: len(line) - 2]
        if type not in dataset:
            dataset[type] = {}
        dataset[type][label] = word_vector
    return dataset


def SeperateXY(dataset):
    X = []
    Y = []
    for type in dataset:
        for label in dataset[type]:
            X.append(dataset[type][label])
            Y.append(type)
    return X, Y



if __name__ == '__main__':
    
    file1 = open("train_set.txt", "r")
    file2 = open("test_set.txt", "r")

    train_set = Load_Data_Set(file1)
    test_set = Load_Data_Set(file2)
    
    trainX, trainY = SeperateXY(train_set)
    testX, testY = SeperateXY(test_set)
    clf = svm.SVC(decision_function_shape='ovo',kernel='linear')
    clf.fit(trainX, trainY)  # training the svc model
    joblib.dump(clf, "Event2_Keyword_Classification.pkl")
    clf2 = joblib.load("Event2_Keyword_Classification.pkl")
    result = clf2.predict(testX) # predict the target of testing samples
    print result

