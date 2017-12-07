#! /usr/bin/python
# -*- coding: utf-8 -*-

#set up
design = 'NBUFFX32_HVT'
directory = './'+design+'_boundary/'
fresh_data = directory+design+'_monte.mt0'
ori_data = directory+design+'_post.mt0@ra'

import re
import os
import string
import copy

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LogNorm
import numpy as np

ori_label=[] #'delay_sel_022'
label=[] #22

ori_time=[]
ori_num=[]

#==============================================================================
# #t=6.048e+05
# class T_Occurence():
#     def __init__(self):
#         self.occur_num = 0
#     def num_increase(self):
#         self.occur_num += 1
# #N=22
# class N_Boundary():
#     def __init__(self):
#         self.time_list = []
#     def list_append(self,time):
#         self.time_list.append(time)
#==============================================================================

def cut_label(string):
    cut_string = int(string[-3:])
    return cut_string

def read_data(file,N,ori_num,aging):
    if aging == 0:
        ori_time.append('0')
        ori_num=[]
        j = 0 #index of ori_num
        with open(file,'r') as file_handle:
            for line in file_handle.readlines():
                word_list = line.split()
                if word_list[0] == 'index':
                    ori_label.extend(word_list[1:-2])
                    tmp_label=[]
                    tmp_label=map(cut_label,ori_label)
                    label.extend(tmp_label)
                    ori_num.append(0) #ori_num list setup
                elif re.match(r'[\d]\.[\d]{3}e\-[\d]{2}',word_list[1]): #mt0
                    ori_delay_list = map(string.atof,word_list[1:-2]) #float & seconds
                    delay_list = [second*1e9 for second in ori_delay_list] #float & nano-seconds
                    for i,delay in enumerate(delay_list):
                        if label[i] == N:
                            if 4.9 < delay < 5.0 and delay_list[i+1] >= 5.0:
                                ori_num[j] += 1
    elif aging == 1:
        j = 1
        with open(file,'r') as file_handle:
            for line in file_handle.readlines():
                word_list = line.split()
#                if word_list[0] == 'reltime':
#                    ori_label.extend(word_list[2:-2])
#                    label=map(cut_label,ori_label)
                if re.match(r'[\d]\.[\d]{3}e\+[\d]{2}',word_list[0]): #mt0@ra
                    ori_delay_list = map(string.atof,word_list[2:-2]) #float & seconds
                    delay_list = [second*1e9 for second in ori_delay_list] #float & nano-seconds
                    if word_list[1] == '1.0000':
                        ori_time.append(word_list[0])
                        ori_num.append(0)
                        j += 1
                    for i,delay in enumerate(delay_list):
                        if label[i] == N and word_list[0] == ori_time[j-1]:
                            if 4.9 < delay < 5.0 and delay_list[i+1] >= 5.0:
                                ori_num[j-1] += 1
    return ori_num
                                
N_list=[16,17,18,19,20,21]
aging_num_list=[]
for i,N in enumerate(N_list):
    fresh_num=read_data(fresh_data,N,ori_num,0)
    aging_num=read_data(ori_data,N,fresh_num,1)
    aging_num_list.append(aging_num)
    #plot
    plt.figure(figsize=(8,6), dpi=98)
    plt.bar(range(len(aging_num)),aging_num)
    plt.legend()
    plt.title('Aging Time Distribution (N=%d)'%N)
    plt.xlabel('time (Week)')
    plt.ylabel('occurence')
    plt.xticks(range(len(aging_num)))
    plt.savefig(directory+design+'_N'+str(N)+'.jpg')
