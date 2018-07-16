#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 19:48:56 2018

@author: krishmehta
"""
import sys, string, random
stopwords=set()
def getStopWords():
    with open("stopwords.txt",'r') as stop:
        data=stop.readlines()
        for lines in data:
            stopwords.add(lines.strip('\n').translate(None,string.punctuation)) #get the stop words so that it can be removed from the corpus
getStopWords()

listfordic=[]
dic={}
#True=1 Fake=-1 Pos=1 Neg=-1
real_out_True_Fake=[]
real_out_Pos_Neg=[]
weight_dic={}
weight_dic1={}
weight_dic2={}
weight_dic3={}
update2={}
update3={}

with open(sys.argv[1],'r') as f:
    data=f.readlines()
    for lines in data:
        splitted=lines.split(' ',3)  # Split only the 1st 3 Spaces
        if splitted[1]=="True":
            real_out_True_Fake.append(1)
        else:
            real_out_True_Fake.append(-1)
        if splitted[2]=="Pos":
            real_out_Pos_Neg.append(1)
        else:
            real_out_Pos_Neg.append(-1)
    #print real_out_True_Fake
        get_sentence=splitted[3].strip('\n')
        get_sentence=get_sentence.translate(None,string.punctuation) #remove puntuation mark
        get_sentence=get_sentence.lower()# lower case
        tokenized_words=get_sentence.split(" ")
        for token in tokenized_words:
            if ((token not in stopwords) and (not token.isspace())):
                if dic.has_key(token):
                    dic[token]=dic[token]+1
                else:
                    dic[token]=1
                    weight_dic[token]=0
                    weight_dic1[token]=0
                    weight_dic2[token]=0.0
                    weight_dic3[token]=0.0
                    update2[token]=0.0
                    update3[token]=0.0
        listfordic.append(dic.copy())
        dic.clear()
length_of_list=len(listfordic)
sum1=0
sum2=0


b_class1=0
b_class2=0


##################### Vanilla Perceptron
for i in range(0,30):
    for j in range(0,length_of_list):
        #print "New line"+str(dic)
        dic=listfordic[j]
        #print j
        #print dic
        for key, value in dic.iteritems():
            sum1= sum1 + (value * weight_dic[key])
        sum1=sum1 + b_class1
        if real_out_True_Fake[j]*sum1<=0:
            for key, value in dic.iteritems():
                weight_dic[key]= weight_dic[key]+(real_out_True_Fake[j]*dic[key])
            b_class1=b_class1+real_out_True_Fake[j]
            #print b_class1
        #dic.clear()
        #print "this is dic"+str(dic)
        sum1=0
        for key, value in dic.iteritems():
            sum2= sum2 + (value * weight_dic1[key])
        sum2=sum2 + b_class2
        if real_out_Pos_Neg[j]*sum2<=0:
            for key, value in dic.iteritems():
                weight_dic1[key]= weight_dic1[key]+(real_out_Pos_Neg[j]*dic[key])
            b_class2=b_class2+real_out_Pos_Neg[j]
        #dic1.clear()
        sum2=0
#print b_class2
#print b_class1
with open("vanillamodel.txt","w") as f:
    f.write("#Bias Value"+"\n")
    f.write(str(b_class1)+"\n")
    f.write(str(b_class2)+"\n")
    f.write("#weight of words for class True and Fake"+"\n")
    for key,value in weight_dic.items():
        f.write(str(key)+" "+str(value)+"\n")
    f.write("#weight of words for class Pos and Neg"+"\n")
    for key,value in weight_dic1.items():
        f.write(str(key)+" "+str(value)+"\n")
f.close()
#print b_class2
#print weight_d










sum3=0.0
sum4=0.0
b_class3=0.0
b_class4=0.0
count =1
beta3=0.0
beta4=0.0
print len(weight_dic2)
print len(weight_dic)
print len(update2)
dic1={}
temp=[]

##################### Average Perceptron
for i in range(0,35):
    temp=zip(listfordic,real_out_True_Fake,real_out_Pos_Neg)
    random.seed(i)
    random.shuffle(temp)
    x=0
    for z in temp:
        #print x
        listfordic[x]=z[0]
        real_out_True_Fake[x]=z[1]
        real_out_Pos_Neg[x]=z[2]
        x=x+1
    for j in range(0,length_of_list):
        dic1=listfordic[j]
        for key, value in dic1.iteritems():
            sum3= sum3 + (value * weight_dic2[key])
        sum3=sum3 + b_class3
        if real_out_True_Fake[j]*sum3<=0:
            for key, value in dic1.iteritems():
                weight_dic2[key]= weight_dic2[key]+(real_out_True_Fake[j]*dic1[key])
                update2[key]=update2[key]+(real_out_True_Fake[j]*count*dic1[key])

            b_class3=b_class3+real_out_True_Fake[j]
            beta3=beta3+(real_out_True_Fake[j]*count)
        sum3=0.0




        for key, value in dic1.iteritems():
            sum4= sum4 + (value * weight_dic3[key])
        sum4=sum4 + b_class4
        if real_out_Pos_Neg[j]*sum4<=0:
            for key, value in dic1.iteritems():
                weight_dic3[key]= weight_dic3[key]+(real_out_Pos_Neg[j]*dic1[key])
                update3[key]=update3[key]+(real_out_Pos_Neg[j]*count*dic1[key])
            b_class4=b_class4+real_out_Pos_Neg[j]
            beta4=beta4+(real_out_Pos_Neg[j]*count)
        sum4=0.0
        count=count+1

for key, value in weight_dic2.iteritems():
    weight_dic2[key]= weight_dic2[key]-(update2[key]/count)
b_class3=b_class3-(beta3/count)

for key, value in weight_dic3.iteritems():
    weight_dic3[key]= weight_dic3[key]-(update3[key]/count)
b_class4=b_class4-(beta4/count)



#print b_class2
#print b_class1
with open("averagedmodel.txt","w") as f1:
    f1.write("#Bias Value"+"\n")
    f1.write(str(b_class3)+"\n")
    f1.write(str(b_class4)+"\n")
    f1.write("#weight of words for class True and Fake"+"\n")
    for key,value in weight_dic2.items():
        f1.write(str(key)+" "+str(value)+"\n")
    f1.write("#weight of words for class Pos and Neg"+"\n")
    for key,value in weight_dic3.items():
        f1.write(str(key)+" "+str(value)+"\n")
f1.close()
