#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 22:06:56 2018

@author: krishmehta
"""
import sys, string
stopwords=set()
def getStopWords():
    with open("stopwords.txt",'r') as stop:
        data=stop.readlines()
        for lines in data:
            stopwords.add(lines.strip('\n').translate(None,string.punctuation)) #get the stop words so that it can be removed from the corpus
getStopWords()

weight_dic1={}
weight_dic2={}
b_class1=0.0
b_class2=0.0

count=0
def fetchthedata(krish,lines):
    global count
    global b_class1
    global b_class2
    if krish=="Bias":
        if count==0:
            b_class1=float(lines.strip())
            #print b_class1
            count=1
        else:
            b_class2=float(lines.strip()) 
            #print b_class2
    if krish=="truefake":
        splitspace=lines.split(" ")
        weight_dic1[splitspace[0]]=weight_dic1.get(splitspace[0],float(splitspace[1]))
        #print weight_dic1
    if krish=="posneg":
        splitspace=lines.split(" ")
        weight_dic2[splitspace[0]]=weight_dic2.get(splitspace[0],float(splitspace[1]))
        #print weight_dic2
        

flag="null"
with open(sys.argv[1],'r') as myfile:
    data=myfile.readlines()
    for lines in data:
        if lines.startswith("#Bias Value"):
            flag="Bias"
        elif lines.startswith("#weight of words for class True and Fake"):
            flag="truefake"
        elif lines.startswith("#weight of words for class Pos and Neg"):
            flag="posneg"
        else:
            fetchthedata(flag,lines)


dic={}
global sum1
global sum2
sum1=0.0
sum2=0.0

f1=open("percepoutput.txt",'w')
with open(sys.argv[2],'r') as myfile1:
    data=myfile1.readlines()
    for lines in data:
        splitted=lines.split(' ',1)
        get_sentence=splitted[1].strip('\n')
        get_sentence=get_sentence.translate(None,string.punctuation) #remove puntuation mark
        get_sentence=get_sentence.lower()# lower case
        tokenized_words=get_sentence.split(" ")
        for token in tokenized_words:
            if ((token not in stopwords) and (not token.isspace())):
                if dic.has_key(token):
                    dic[token]=dic[token]+1
                else:
                    dic[token]=1
        
        for key, value in dic.iteritems():
            if (weight_dic1.has_key(key)):
                sum1=sum1+(weight_dic1[key]*dic[key])
        sum1=sum1+b_class1
        for key, value in dic.iteritems():
            if (weight_dic2.has_key(key)):
                sum2=sum2+(weight_dic2[key]*dic[key])
        sum2=sum2+b_class2
        print sum2
        writing=""
        if sum1<=0:
            f1.write(splitted[0]+" "+"Fake"+" ")
        else:
            f1.write(splitted[0]+" "+"True"+" ")
        if sum2<=0:
            f1.write("Neg"+"\n")
        else:
            f1.write("Pos"+"\n")
        dic.clear()
        sum1=0.0
        sum2=0.0