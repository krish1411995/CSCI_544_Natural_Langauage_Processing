#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 16:48:25 2018

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

count_for_True=0
count_for_Fake=0
count_for_Pos=0
count_for_Neg=0
count_for_tclass=0
count_for_fclass=0
count_for_pclass=0
count_for_nclass=0
class_tprior=0
class_fprior=0
class_pprior=0
class_nprior=0

line_number=0
words_to_send={}
#True Fake Pos Neg

with open(sys.argv[1],'r') as f:
    data=f.readlines()
    for lines in data:
        splitted=lines.split(' ',3)  # Split only the 1st 3 Spaces
        if splitted[1]=="True":
            count_for_True+=1
            #print line_number
        else:
            count_for_Fake+=1
        if splitted[2]=="Pos":
            count_for_Pos+=1
        else:
            count_for_Neg+=1
        get_sentence=splitted[3].strip('\n')
        get_sentence=get_sentence.translate(None,string.punctuation) #remove puntuation mark
        get_sentence=get_sentence.lower()# lower case
        tokenized_words=get_sentence.split()
        for token in tokenized_words:
            if ((token not in stopwords) and (not token.isspace())):
                if words_to_send.has_key(token):
                    if splitted[1]=="True":
                        words_to_send[token][0]=int(words_to_send[token][0])+1
                    else:
                        words_to_send[token][1]=int(words_to_send[token][1])+1
                    if splitted[2]=="Pos":
                        words_to_send[token][2]=int(words_to_send[token][2])+1
                    else:
                        words_to_send[token][3]=int(words_to_send[token][3])+1
                else:
                    words_to_send[token]=[0,0,0,0]
                    if splitted[1]=="True":
                        
                        words_to_send[token][0]=int(words_to_send[token][0])+1
                    else:
                        words_to_send[token][1]=int(words_to_send[token][1])+1
                    if splitted[2]=="Pos":
                        words_to_send[token][2]=int(words_to_send[token][2])+1
                    else:
                        words_to_send[token][3]=int(words_to_send[token][3])+1
                #print token
                #words_to_send[token]=words_to_send.get(token,{})
                #words_to_send[token][splitted[1]]=words_to_send[token].get(splitted[1],0)+1
                #words_to_send[token][splitted[2]]=words_to_send[token].get(splitted[2],0)+1
   
    
    
    
    for key, value in words_to_send.items():#get the values of the total count of the number of words in that class 
        if (sum(value)<0 or key.isspace() or key.isdigit()):
            del words_to_send[key]# remove the words with frequency less than 5
        else:
            count_for_tclass+=value[0]
            count_for_fclass+=value[1]
            count_for_pclass+=value[2]
            count_for_nclass+=value[3]
    #print "After effect"
    #print words_to_send
    
    
#print count_for_tclass
class_tprior=float(count_for_True)/(count_for_True+count_for_Fake)
class_fprior=float(count_for_Fake)/(count_for_True+count_for_Fake)
class_pprior=float(count_for_Pos)/(count_for_Pos+count_for_Neg)
class_nprior=float(count_for_Neg)/(count_for_Pos+count_for_Neg)

#now calculate the probabilty for words with the smoothing

length_of_vocabulary=len(words_to_send)
print length_of_vocabulary
# print words_to_send
def smoothingwithprobability():
    for key,value in words_to_send.items():
        words_to_send[key][0]=float(words_to_send[key][0]+1)/(count_for_tclass+length_of_vocabulary)
        words_to_send[key][1]=float(words_to_send[key][1]+1)/(count_for_fclass+length_of_vocabulary)
        words_to_send[key][2]=float(words_to_send[key][2]+1)/(count_for_pclass+length_of_vocabulary)
        words_to_send[key][3]=float(words_to_send[key][3]+1)/(count_for_nclass+length_of_vocabulary)
smoothingwithprobability()




#print words_to_send