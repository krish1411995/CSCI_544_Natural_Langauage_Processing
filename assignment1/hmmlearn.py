#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 19:13:15 2018

@author: krishmehta
"""
import sys
countofeachtag ={}
wordwithtag={}
tagwithtag={}
tagcountofstart={}



with open(sys.argv[1]) as myfile:
    data=myfile.readlines()
    for lines in data:
        start="#START#"
        end="#END#"
        words=lines.split() #Split the line in which has spaces in the middle
        for onebyone in words: #get each word one by one e.g. krish/NN
            splitwordtag=onebyone.rsplit('/',1)
            if splitwordtag[1]=='':
                splitwordtag[1]="''"
            wordwithtag[splitwordtag[0]]=wordwithtag.get(splitwordtag[0],{})
            wordwithtag[splitwordtag[0]][splitwordtag[1]]=wordwithtag[splitwordtag[0]].get(splitwordtag[1],0)+1  #incrementing the number of times the tag has appeared for that particular word
            tagwithtag[start]=tagwithtag.get(start,{})
            if start=='#START#':
                tagcountofstart[start]=tagcountofstart.get(start,0)+1
            tagwithtag[start][splitwordtag[1]]=tagwithtag[start].get(splitwordtag[1],0)+1  #incremanting the value of the transition for a tag to tag including the start tag
            start=splitwordtag[1]
            countofeachtag[splitwordtag[1]]=countofeachtag.get(splitwordtag[1],0)+1
        #Just for the end tag
        tagwithtag[start]=tagwithtag.get(start,{})
        tagwithtag[start][end]=tagwithtag[start].get(end,0)+1
            
            
with open("hmmdata.txt",'w') as myfile1:
    myfile1.write("#Emission Probabilities# \n")
    #print wordwithtag
    lengthofuniquewords=len(wordwithtag)
    lengthofuniquetag=len(countofeachtag)
    #print countofeachtag
    
    for key in wordwithtag:
        for key1 in wordwithtag[key]:
            myfile1.write(key+" "+key1+" "+str((float(wordwithtag[key][key1]))/(float(countofeachtag[key1])))+"\n")
    myfile1.write("#Transition Probabilities#\n")
    for key in tagwithtag:
        if key=='':
            key="''"
        di=tagwithtag[key]
        s = sum(di.values())
        for key1 in tagwithtag[key]:
            myfile1.write(key+" "+key1+" "+str((float(tagwithtag[key][key1])+1.0)/(s+lengthofuniquetag))+"\n")
    myfile1.write("#Tag Count#\n")
    for key in countofeachtag:
        myfile1.write(key+" "+str(countofeachtag[key])+"\n")
    myfile1.write("#START#"+" "+str(tagcountofstart["#START#"])+"\n")
    myfile1.write("#WordTag#\n")
    for key in  wordwithtag:
        string=""
        myfile1.write(key+" ")
        lengthofword=len(wordwithtag[key])
        i=1
        for key1 in wordwithtag[key]:
            if i<lengthofword:
                myfile1.write(key1+"##")
                i=i+1
            else:
                myfile1.write(key1)
        myfile1.write("\n")
        