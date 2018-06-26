#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:54:06 2017

@author: rsh
"""
import string
import re
import random

import numpy as np
import pandas as pd

import sklearn as skl
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.semi_supervised import label_propagation

#setup
design = 'NBUFFX32_HVT'
directory = './'+design+'_SVM/'
ori_fresh_data = directory+design+'_monte.mt0'
ori_aging_data = directory+design+'_post.mt0@ra'
csv_data = directory+design+'.csv'

num_month = 36

#convert string in file to N0
def str2N0(str_list):
    N0 = 0
    N0_list=[]
    for str_raw in str_list:
        if str_raw[:-3] == 'delay_sel_':
            N0 = int(str_raw[-3:])
            N0_list.append(N0)
        else:
            N0_list.append(str_raw)
    return N0_list

#convert second to month
#convert second to nano-second
def metricConvert(word_list):
    data = 0
    data_list=[]
    #fill reltime = 0 for fresh data
    #index = 1~100
    if re.match(r'^[\d]{1,3}$',word_list[0]):
        word_list.insert(0,'0')
    
    ori_data = map(string.atof,word_list)
    for i,word in enumerate(word_list):
        #reltime = 2.592e+06
        if re.match(r'[\d]\.[\d]{3}e\+[\d]{2}',word):
#            data = ori_data[i]
            data = int(round(ori_data[i]/(30*24*60*60)))
            data_list.append(data)
        #delay = 3.785e-09
        elif re.match(r'[\d]\.[\d]{3}e\-[\d]{2}',word):
            data = ori_data[i]*1e9
            data_list.append(data)
        else:
            data = int(ori_data[i])
            data_list.append(data)
    
    return data_list
        
#convert original data to csv
def ori2csv(fresh_file,aging_file,output_file):
    label_word=[]
    new_word=[]
    new_line=''
    new_line_list=[]
    
    with open(fresh_file,'r') as fresh_handle:
        line_list = fresh_handle.readlines()
        for line in line_list[3:]:
            word = line.split()[:-2]
            #index = 1~100
            if re.match(r'[\d]+',word[0]):
                new_word = metricConvert(word)
                new_line = ','.join(map(str,new_word))
                new_line_list.append(new_line)
                
    with open(aging_file,'r') as aging_handle:
        line_list = aging_handle.readlines()
        for line in line_list[3:]:
            word = line.split()[:-2]
            if word[0] == 'reltime':
                label_word = str2N0(word)
                new_line = ','.join(map(str,label_word))
                new_line_list.insert(0,new_line)
            #reltime = 2.592e+06
            elif re.match(r'[\d]\.[\d]{3}e\+[\d]{2}',word[0]):
                new_word = metricConvert(word)
                new_line = ','.join(map(str,new_word))
                new_line_list.append(new_line)
                
    with open(output_file,'w') as output_handle:
        for line in new_line_list:
            output_handle.writelines(line+'\n')
            
if __name__ == '__main__':
    ori2csv(ori_fresh_data,ori_aging_data,csv_data)
    
    df = pd.read_csv(csv_data,header=0)
    x_array = df['15'].values
    y_list = []
    for i in range(num_month+1):
        x_list = list(x_array)
        tmp_list = x_list[i*100:(i+1)*100]
        random.shuffle(tmp_list)
        y_list.extend(tmp_list)
    y_array = np.array(y_list)
    
    x_train = np.vstack((x_array,y_array)).T
    y_train = df['reltime'].values
    
    rbf_svc = (svm.SVC(kernel='rbf').fit(x_train, y_train), y_train)
    
    # step size in the mesh
    h = .02
    # create a mesh to plot in
    x_min, x_max = x_train[:, 0].min() - 0.1, x_train[:, 0].max() + 0.1
    y_min, y_max = x_train[:, 1].min() - 0.1, x_train[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
#    color_map = {0: (1, 1, 1), 
#                 1: (0, 0, .9), 
#                 2: (1, 0, 0), 
#                 3: (.8, .6, 0)}
    num_class = num_month + 1
    cm = plt.get_cmap('gist_rainbow')
    color_map = [cm(1.*i/num_class) for i in range(num_class)]
    
    
    plt.figure(figsize=(8,6), dpi=98)
    clf, y = rbf_svc
    
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z)
    #plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
    #plt.axis('off')
    
    # Plot also the training points
    colors = [color_map[j] for j in y_train]
    
#    # Plot and scatter in a simple way
#    scatter_step = 20
#    x_scatter = x_train[::scatter_step,:]
#    num_scatter = 100/scatter_step
#    sparse_step = 20
#    x_sparse = x_train[::sparse_step,:]
#    num_sparse = 100/sparse_step
###############################################################################
#       There is a odd/abnormal/suspicious mixed into the other area  
#    x_fresh_0 = x_scatter[0:1*num_scatter+1,0]
#    x_fresh_1 = x_scatter[0:1*num_scatter+1,1]
#    plt.scatter(x_fresh_0,x_fresh_1,marker='o',edgecolors='black')
#    
#    x_aged_0 = x_scatter[1*num_scatter+1:4*num_scatter+1,0]
#    x_aged_1 = x_scatter[1*num_scatter+1:4*num_scatter+1,1]
#    plt.scatter(x_aged_0,x_aged_1,marker='^',edgecolors='black')
#    
#    x_recycled_0 = x_scatter[13*num_scatter+1:37*num_scatter+1,0]
#    x_recycled_1 = x_scatter[13*num_scatter+1:37*num_scatter+1,1]
#    plt.scatter(x_recycled_0,x_recycled_1,marker='+',edgecolors='black')
###############################################################################
#    x_fresh_0 = x_scatter[0:1*num_scatter,0]
#    x_fresh_1 = x_scatter[0:1*num_scatter,1]
#    plt.scatter(x_fresh_0,x_fresh_1,marker='o',edgecolors='black')
#    
#    x_aged_0 = x_scatter[1*num_scatter:4*num_scatter+1,0]
#    x_aged_1 = x_scatter[1*num_scatter:4*num_scatter+1,1]
#    plt.scatter(x_aged_0,x_aged_1,marker='^',edgecolors='black')
#    
#    x_recycled_0 = x_sparse[13*num_sparse:37*num_sparse,0]
#    x_recycled_1 = x_sparse[13*num_sparse:37*num_sparse,1]
#    plt.scatter(x_recycled_0,x_recycled_1,marker='+',edgecolors='black')
###############################################################################
    
    IC_dict = dict(fresh=[0],aged=range(1,4),old=range(4,13),recycled=range(13,37))
    IC_type = ['fresh','aged','old','recycled']
    step_list = [5,10,20,30]
    marker_list = ['o','+','^','x']
    color_list = ['w','k','w','k']
    x_list_0 = [] #stores x_train array
    x_list_1 = []
    
    #Loop in a reversed sequence
    #To avoid that the fresh ICs are covered by those recycled
    scatter_step = step_list[::-1]
    scatter_marker = marker_list[::-1]
    scatter_color = color_list[::-1]
    for i,k in enumerate(IC_type[::-1]):
        # Plot and scatter in a simple way
        # Recycled will be more sparse 
        x_scatter = x_train[::scatter_step[i],:]
        num_scatter = 100.0/scatter_step[i]
        start = int(IC_dict[k][0]*num_scatter+1)
        stop = int((IC_dict[k][-1]+1)*num_scatter+1)
        x_list_0.append(x_scatter[start:stop,0])
        x_list_1.append(x_scatter[start:stop,1])
        plt.scatter(x_list_0[i],x_list_1[i],c=scatter_color[i],marker=scatter_marker[i],edgecolors='black')
        #plt.scatter(x_train[:, 0], x_train[:, 1], marker='^', cmap=colors, edgecolors='black')
    
    plt.savefig(directory+design+'.eps')
    plt.savefig(directory+design+'.png')
            
