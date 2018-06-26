#! /usr/bin/python
# -*- coding: utf-8 -*-

#set up
design = 'buffer_mux_delay'
directory = './'+design+'/'
fresh_data= directory+design+'.mt0'
ori_data = directory+design+'.mt0@ra'

import sys
import re
import os
import string
import copy

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LogNorm
import numpy as np

sys.path.append('/home/rsh/Desktop/run_area/python/recycled_ic_plt/')
from NBUFFX32_HVT_SVM import metricConvert


#ori_str=[]
ori_label=[]
ori_str=[]
ori_str0=['0'] #reltime for fresh data
rel_time_list=[]

def read_data(file):
    with open(file,'r') as file_handle:
        for line in file_handle.readlines():
            mt0ra_pattern = re.compile(r'[\d]\.[\d]{3}e\+[\d]{2}')
            mt0_pattern  = re.compile(r'[\d]\.[\d]{3}e\-[\d]{2}')
            word = line.split()
        #        num_lists = len(word)-2
            if word[0] == 'reltime':
                ori_label.extend(word[:-2])
        #            for i in xrange(num_lists):
        #                ori_label.append(word[i])
        #            ori_label=word[:-2] #failed
            elif re.match(mt0ra_pattern,word[0]): #mt0@ra
                ori_str.append(word[:-2])
            elif re.match(mt0_pattern,word[0]): #mt0
                ori_str0.extend(word[:-2])
        #            for i in xrange(num_lists):
        #                ori_str0.append(word[i]) 

def percentConvert(str_matrix):
    ns_matrix=[]
    for index,str_list in enumerate(str_matrix):
        f_list=map(string.atof,str_matrix[index]) #list of data in float type
        ns_list=[]
        rel_time_list.append(f_list[0])
        for f in f_list[1:]:
            ns_list.append(f*1e9)
        ns_matrix.append(ns_list)
        
    x=range(len(ns_matrix))
    y_old=np.array(ns_matrix).T #data in ns
    
    y_new=np.zeros(np.shape(y_old))
    for i,y_row in enumerate(y_old):
        ori_delay=y_row[0]                              #original gate delay
        for j,y_col in enumerate(y_row):
            percent = (y_col - ori_delay)/ori_delay*100 #delay degradation
            y_new[i,j]=percent
    return x,y_old,y_new

#convert the original label to a simple and capital one
def str2cap(label_list):
    capital_list=[]
    for label in label_list:
        if re.search(r'delay',label):
            capital=label.strip('delay_').upper()
            capital_list.append(capital)
    return capital_list
            
read_data(fresh_data)
ori_str.append(ori_str0)
read_data(ori_data)

#convert string to float for original data
x_old,y_old,y_new = percentConvert(ori_str)
#30 months is suggested
num_month=30
x=x_old[:num_month+1]
y=y_new[:,:num_month+1]
new_label=str2cap(ori_label)

buf_type=['NBUFFX2_RVT','NBUFFX2_LVT','NBUFFX2_HVT',\
          'NBUFFX4_RVT','NBUFFX4_LVT','NBUFFX4_HVT',\
          'NBUFFX8_RVT','NBUFFX8_LVT','NBUFFX8_HVT',\
          'NBUFFX16_RVT','NBUFFX16_LVT','NBUFFX16_HVT',\
          'NBUFFX32_RVT','NBUFFX32_LVT','NBUFFX32_HVT']
mux_type=['MUX21X1_RVT','MUX21X1_LVT','MUX21X1_HVT',\
          'MUX21X2_RVT','MUX21X2_LVT','MUX21X2_HVT',\
          'MUX41X1_RVT','MUX41X1_LVT','MUX41X1_HVT',\
          'MUX41X2_RVT','MUX41X2_LVT','MUX41X2_HVT']
gate_list=['NBUFFX2','NBUFFX4','NBUFFX8','NBUFFX16','NBUFFX32',\
           'MUX21X1','MUX21X2','MUX41X1','MUX41X2']
threshold_list=['RVT','LVT','HVT']

#different type of buffer
marker_list=['o','^','s']
plt.figure(figsize=(10,8), dpi=98)
y_sub=np.delete(y,[4,5,6],axis=0)   #throw NBUFFX4 away
label_sub=new_label[:3]+new_label[6:]

for i in xrange(4):
    plt.subplot(2,2,i+1)
    #different type of Voltage Threshold
    for j in xrange(3):
        #line
        plt.plot(x,y_sub[i*3+j],color="k",linestyle="-",linewidth=2)
        #marker corlorful (x[::4] scat sparsely)
        plt.plot(x[::3],y_sub[i*3+j,::3],marker_list[j],label=label_sub[i*3+j])
    #delay of MUX21X1_LVT as reference
    plt.plot(x,y_sub[20-1],color="k",linestyle="--",linewidth=2,label=label_sub[19])
    #    plt.plot(x,y[i],color="blue",linewidth=1.0,linestyle="-",label=ori_label[i+1])
        
    plt.legend()
    #plt.title('Delay difference between inverters(%s) under aging pressure'%gate_list[i])
    plt.xlabel('Aging Time (Month)',fontsize=14)
    plt.ylabel('Delay Degradation (%)',fontsize=14)
    plt.xticks(range(0,num_month+6,6),range(0,num_month+6,6))
    #plt.yticks()
    plt.xlim(0,)
    plt.ylim(0,)
    plt.grid(True, linestyle = "-.", color = "gray", linewidth = "0.5")

plt.savefig(directory+design+'.eps')
plt.savefig(directory+design+'.jpg')