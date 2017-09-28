#! /usr/bin/python
# -*- coding: utf-8 -*-

#set up
design = 'RO_11'
directory = './'+design
ori_data = './'+design+'/'+design+'_pre.mt0@ra'

import re
import os
import string
import copy

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

#ori_str=[]
ori_str0=[]
ori_str1=[]
ori_str2=[]
ori_str=[ori_str0,ori_str1,ori_str2]

#read original data from mt0 with no monte
ori_data_handle = open(ori_data,'r')
for line in ori_data_handle.readlines():
    word = line.split()
    if word[0] == 'reltime':
        title0=word[0]
        title1=word[1]
        title2=word[2]
    elif re.search(r'[\d].[\d]{3}e-[\d]{2}',line):
        ori_str0.append(word[0])
        ori_str1.append(word[1])
        ori_str2.append(word[2])
ori_data_handle.close


#convert string to float for original data
title=[]

def str2f(x):
    return string.atof(x)

for i in range(len(ori_str)):
    ori_f=map(str2f,ori_str[i])
    title.append(ori_f)
    
#title=map(map(string.atof,),ori_str)

#plot

x=range(1,len(title[0])+1)
y_title1=title[1]
y_title2=title[2]

plt.figure(figsize=(8,6), dpi=98)
plt.subplot(1,1,1)
plt.plot(x,y_title1,color="blue",linewidth=1.0,linestyle="-",\
         label="INVX0_HVT")
plt.plot(x,y_title2,color="r",lw=4.0,ls="-",label="INVX32_LVT")
#plt.text(2,0.9,"100 cycles of 11-gates RO",fontsize=1,va="top",ha="center")
plt.legend()
plt.title('Delay difference between inverters under aging pressure')
#plt.text(0.5,0.8,'100 cycles of 11-gates RO',color='black',va='top',ha='center')
plt.xlabel('month')
plt.ylabel('delay time')
#plt.axis([0,40,0,8.500e-8])
plt.xticks([0,6,12,18,24,30,36],[0,6,12,18,24,30,36])
#plt.yticks([],[])
plt.savefig('RO_11.eps')
plt.savefig('RO_11.jpg')



