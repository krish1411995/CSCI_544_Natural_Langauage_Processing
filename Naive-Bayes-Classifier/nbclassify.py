#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 23:26:15 2018

@author: krishmehta
"""
import sys, string, math
stopwords=set()
def getStopWords():
    with open("stopwords.txt",'r') as stop:
        data=stop.readlines()
        for lines in data:
            stopwords.add(lines.strip('\n').translate(None,string.punctuation)) #get the stop words so that it can be removed from the corpus
getStopWords()
words_rec={}
class_tprior=0
class_fprior=0
class_pprior=0
class_nprior=0
count=0
with open("nbmodel.txt","r") as f:
    data=f.readlines()
    for lines in data:
        if count <=4:
            if "#Class" not in lines:
                if "True" in lines:
                    word=lines.split(' ')
                    class_tprior=float(word[1].strip('\n'))
                elif "Fake" in lines:
                    word=lines.split(' ')
                    class_fprior=float(word[1].strip('\n'))
                elif "Pos" in lines:
                    word=lines.split(' ')
                    class_pprior=float(word[1].strip('\n'))
                else:
                    word=lines.split(' ')
                    class_nprior=float(word[1].strip('\n'))
        else:
            word=lines.split(' ')
            othersplit=word[1].split(',')
            words_rec[word[0]]=[float(othersplit[0].strip('\n')),float(othersplit[1].strip('\n')),float(othersplit[2].strip('\n')),float(othersplit[3].strip('\n'))]
        count+=1
#print words_rec
writefile=open("nboutput.txt","w")
with open(sys.argv[1],'r') as f:
    data=f.readlines()
    for lines in data:
        splitted=lines.split(' ',1)  # Split only the 1st Space
        value_name=splitted[0]
        get_sentence=splitted[1].strip('\n')
        get_sentence=get_sentence.translate(None,string.punctuation) #remove puntuation mark
        get_sentence=get_sentence.lower() # lower case
        tokenized_words=get_sentence.split(' ')
        score_t=0
        score_f=0
        score_p=0
        score_n=0
        for token in tokenized_words:
            if ((token not in stopwords) and (not token.isspace()) and (not token.isdigit())):
                if (words_rec.has_key(token)):
                    score_t+=math.log(float(words_rec[token][0]))
                    score_f+=math.log(float(words_rec[token][1]))
                    score_p+=math.log(float(words_rec[token][2]))
                    score_n+=math.log(float(words_rec[token][3]))
        score_t+=math.log(float(class_tprior))
        score_f+=math.log(float(class_fprior))
        score_p+=math.log(float(class_pprior))
        score_n+=math.log(float(class_nprior))
        class1=""
        class2=""
        if score_t>score_f:
            class1="True"
        else:
            class1="Fake"
        if score_p>score_n:
            class2="Pos"
        else:
            class2="Neg"
        #print score_t
        writefile.write(value_name+" "+class1+" "+class2+"\n")
        
        
                    
    
    
