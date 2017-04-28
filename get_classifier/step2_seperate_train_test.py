#-*- coding:utf-8 -*-

import numpy as np
import time


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


def Output_Dataset(file, dataset):
    for type in dataset:
        for label in dataset[type]:
            for i in range(len(dataset[type][label])):
                file.write(str(dataset[type][label][i]) + "\t")
            file.write(type + "\t" + str(label) + "\n")


def Count_Type(dataset):
    counter = {}
    for type in dataset:
        counter[type] = 0
        for label in dataset[type]:
            counter[type] += 1
    return counter


def Seperate_Dataset(dataset, counter):
    test = {}
    train = {}
    for type in counter:
        test[type] = {}
        train[type] = {}
        i = 0
        for label in dataset[type]:
            i += 1
            if i < counter[type] / 4:
                test[type][label] = dataset[type][label]
            else:
                train[type][label] = dataset[type][label]
    return train, test



if __name__ == '__main__':
    
    file1 = open("dataset.txt", "r")
    file2 = open("train_set.txt", "w")
    file3 = open("test_set.txt", "w")
    
    all_data_set = {} # set[type][label] = word_vector
    type_counter = {}
    
    # load keywords
    all_data_set = Load_Data_Set(file1)
    type_counter = Count_Type(all_data_set)
    print type_counter
    train_data_set, test_data_set = Seperate_Dataset(all_data_set, type_counter)
    Output_Dataset(file2, train_data_set)
    Output_Dataset(file3, test_data_set)
