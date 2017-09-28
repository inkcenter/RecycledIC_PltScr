#! /usr/bin/python
# -*- coding: utf-8 -*-

#set up
design = 'buffer_mux_delay'
directory = './'+design
fresh_data= './'+design+'/'+design+'.mt0'
ori_data = './'+design+'/'+design+'.mt0@ra'

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

plt.figure(figsize=(8,6), dpi=98)
plt.subplot(1,1,1)
#plt.plot(x,y_title1,color="blue",linewidth=1.0,linestyle="-",\
#         label="INVX0_HVT")
#plt.plot(x,y_title2,color="r",lw=4.0,ls="-",label="INVX32_LVT")
#plt.text(2,0.9,"100 cycles of 11-gates RO",fontsize=1,va="top",ha="center")
num_label=y.shape[0]
for i in xrange(15):
    plt.plot(x,y[i],linewidth=1.0,linestyle="-",label=ori_label[i+1])
#    plt.plot(x,y[i],color="blue",linewidth=1.0,linestyle="-",label=ori_label[i+1])
    
plt.legend()
plt.title('Delay difference between inverters under aging pressure')
#plt.text(0.5,0.8,'100 cycles of 11-gates RO',color='black',va='top',ha='center')
plt.xlabel('month')
plt.ylabel('delay')
#plt.axis([0,40,0,8.500e-8])
plt.xticks(range(0,60+6,6),range(0,60+6,6))
#plt.yticks([],[])
plt.savefig(design+'.eps')
plt.savefig(design+'.jpg')



