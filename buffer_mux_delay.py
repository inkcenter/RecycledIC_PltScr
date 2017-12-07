#! /usr/bin/python
# -*- coding: utf-8 -*-

#set up
design = 'buffer_mux_delay'
directory = './'+design+'/'
fresh_data= directory+design+'.mt0'
ori_data = directory+design+'.mt0@ra'

import re
import os
import string
import copy

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LogNorm
import numpy as np

#ori_str=[]
ori_label=[]
ori_str=[]
ori_str0=['0'] #reltime for fresh data

def read_data(file):
    file_handle = open(file,'r')
    for line in file_handle.readlines():
        word = line.split()
#        num_lists = len(word)-2
        if word[0] == 'reltime':
            ori_label.extend(word[:-2])
#            for i in xrange(num_lists):
#                ori_label.append(word[i])
#            ori_label=word[:-2] #failed
        elif re.match(r'[\d]\.[\d]{3}e\+[\d]{2}',word[0]): #mt0@ra
            ori_str.append(word[:-2])
        elif re.match(r'[\d]\.[\d]{3}e\-[\d]{2}',word[0]): #mt0
            ori_str0.extend(word[:-2])
#            for i in xrange(num_lists):
#                ori_str0.append(word[i]) 
    file_handle.close

read_data(fresh_data)
ori_str.append(ori_str0)
read_data(ori_data)

#==============================================================================
# #read fresh data from mt0
# fresh_data_handle = open(fresh_data,'r')
# for line in fresh_data.readlines():
#     word = line.split()
#     num_lists = len(word)-2
#     if re.search(r'[\d].[\d]{3}e-[\d]{2}',line):
#         for i in xrange(num_lists):
#             ori_str[i+1]=[] #ori_str[0] claimed before
#             ori_str[i+1].append(word[i]) #ori_str[i][0]
# fresh_data_handle.close
# 
# #read original data from mt0@ra
# ori_data_handle = open(ori_data,'r')
# for line in ori_data_handle.readlines():
#     word = line.split()
#     num_lists = len(word)-2 #except temper and alter#
#     if word[0] == 'reltime':
#         for i in xrange(num_lists):
#             ori_label.append(word[i])
#     elif re.search(r'[\d].[\d]{3}e-[\d]{2}',line):
#         for i in xrange(num_lists):
#             ori_str[i].append(word[i]) #ori_str[i]=[] claimed before
# ori_data_handle.close
#==============================================================================


#convert string to float for original data
tmp=[]

def str2f(x):
    return string.atof(x)

for i in xrange(len(ori_str)):
    ori_f=map(str2f,ori_str[i])
    tmp.append(ori_f)
#title=map(map(string.atof,),ori_str)

#plot
x=range(len(tmp)) #reltime
title=np.array(tmp).T
y=title[1:] #delay

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
for i in xrange(5):
    plt.figure(figsize=(8,6), dpi=98)
    plt.subplot(1,1,1)
    #plt.plot(x,y_title1,color="blue",linewidth=1.0,linestyle="-",\
    #         label="INVX0_HVT")
    #plt.plot(x,y_title2,color="r",lw=4.0,ls="-",label="INVX32_LVT")
    #plt.text(2,0.9,"100 cycles of 11-gates RO",fontsize=1,va="top",ha="center")
    num_label=y.shape[0]
    #different type of Voltage Threshold
    for j in xrange(3):
        plt.plot(x,y[i*3+j],linewidth=1.0,linestyle="-",label=ori_label[i*3+j+1])
    
    plt.plot(x,y[20-1],linewidth=1.0,linestyle="-",label=ori_label[20])
    #    plt.plot(x,y[i],color="blue",linewidth=1.0,linestyle="-",label=ori_label[i+1])
        
    plt.legend()
    plt.title('Delay difference between inverters(%s) under aging pressure'%gate_list[i])
    #plt.text(0.5,0.8,'100 cycles of 11-gates RO',color='black',va='top',ha='center')
    plt.xlabel('month')
    plt.ylabel('delay')
    #plt.axis([0,40,0,8.500e-8])
    plt.xticks(range(0,60+6,6),range(0,60+6,6))
    #plt.yticks([],[])
    plt.savefig(directory+design+gate_list[i]+'.eps')
    plt.savefig(directory+design+gate_list[i]+'.jpg')
    
for i in xrange(3):
    plt.figure(figsize=(8,6), dpi=98)
    plt.subplot(1,1,1)
    num_label=y.shape[0]
    for j in xrange(5):
        plt.plot(x,y[i+j*3],linewidth=1.0,linestyle="-",label=ori_label[i+j*3+1])

    plt.plot(x,y[20-1],linewidth=1.0,linestyle="-",label=ori_label[20])
#    plt.plot(x,y[16+i*4-1],linewidth=1.0,linestyle="-",label=ori_label[16+i*4])
    plt.legend()
    plt.title('Delay difference between thresholds(%s) under aging pressure'%threshold_list[i])
    plt.xlabel('month')
    plt.ylabel('delay')
    plt.xticks(range(0,60+6,6),range(0,60+6,6))
    plt.savefig(directory+design+threshold_list[i]+'.eps')
    plt.savefig(directory+design+threshold_list[i]+'.jpg')




