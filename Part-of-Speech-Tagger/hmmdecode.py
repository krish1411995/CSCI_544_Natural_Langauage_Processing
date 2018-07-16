#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:24:26 2018

@author: krishmehta
"""
import sys
from collections import OrderedDict
import math
emission={}
transition={}
tagcount={}
wordwithtags={}
storingthevalues={}
backtrack={}
myfile2=open("hmmoutput.txt","w")

def fetchthedata(krish,lines):
    if krish=="emission":
        splitspace=lines.split(" ")
        emission[splitspace[0]]=emission.get(splitspace[0],{})
        emission[splitspace[0]][splitspace[1]]=emission[splitspace[0]].get(splitspace[1],float(splitspace[2]))
    if krish=="transition":
        splitspace=lines.split(" ")
        transition[splitspace[0]]=transition.get(splitspace[0],{})
        transition[splitspace[0]][splitspace[1]]=transition[splitspace[0]].get(splitspace[1],float(splitspace[2]))
    if krish=="tagcount":
        splitspace=lines.split(" ")
        tagcount[splitspace[0]]=tagcount.get(splitspace[0],float(splitspace[1]))
    if krish=="wordtag":
        splitspace=lines.split(" ")
        #j=set()
        wordwithtags[splitspace[0]]=set()
        splitspace1=splitspace[1].split("##")
        for i in splitspace1:
            wordwithtags[splitspace[0]].add(i.strip())
        
        
        
def ViterbiAlgorithm():
    tagforunknown=""
    sorted_x = OrderedDict(sorted(tagcount.items(),key=lambda x:x[1],reverse=True))
    for b in sorted_x:
        if b.startswith("N") or  b.startswith("R") or b.startswith("V") or b.startswith("J"):
            tagforunknown=b
            break
    for tag in tagcount:
        print "This is the tag",tag,"This is the count",tagcount[tag]
    
    with open(sys.argv[1]) as myfile1:
        data=myfile1.readlines()
        #print "in viterbi"
        #print data
        for lines in data:
            start1={} # value with the state and its probability
            temp1={}
            temp=set()
            start=set() # just to know how many states are there like Qi-1
            start.add("#START#")
            start1[0]=start1.get(0,{})
            start1[0]["#START#"]=start1[0].get("#START#",0.0)
            index=0  # used to know the number of words covered
            currentstate=set()
            words=lines.split() #Split the line in which has spaces in the middle
            #print "the value of words are::::::::::::::::::::::::::::::::::::::",words
            for onebyone in words:
                if onebyone not in wordwithtags:
                    #print "inside to get the value for the word tag with the tagforunknown be",tagforunknown
                    wordwithtags[onebyone]=set()
                        #wordwithtags[onebyone].add(tagforunknown)
                        #emission[onebyone]=emission.get(onebyone,{})
                        ############value for emission
                        #di=transition[tagforunknown]
                        #s = sum(di.values())
                        #valueofemission=1/(len(wordwithtags)+s)
                        ############value for emission
                    for tag in tagcount:
                        wordwithtags[onebyone].add(tag)
                        emission[onebyone]=emission.get(onebyone,{})
                        valueofemission=1/(len(wordwithtags)+tagcount[tag])
                        emission[onebyone][tag]=emission[onebyone].get(tag,1.0)
                    #print "Value of the word",onebyone,"will have tag",emission[onebyone],"################"
                    #print "WORD WITH TAG",wordwithtags[onebyone]
                #print  wordwithtags[onebyone]   
                for tagofwords in wordwithtags[onebyone]:
                    currentstate.add(tagofwords)
                #print "The tag of words for the word:",onebyone,"is", currentstate
                   
                for j in currentstate:#here j is the state e.g. NN which is the current state
                    max=-float("inf")
                    for i in start: #i is the previos state
                        """if i=='':
                            i="''"
                            """
                        if i in transition:
                            if j not in transition[i]:
                                transition[i]=transition.get(i,{})
                                #di=transition[i]
                                #s = sum(di.values())
                                #print s
                                transition[i][j]=transition[i].get(j,0.0)+(1/(len(tagcount)+float(tagcount[i])))
                                #print "Something is going on here for state::::::::",i,"  too state::",j,"with value",transition[i][j]
                        transp=float(transition[i].get(j,0.0))
                        #print transp,"   ",i,"   ",j 
                        qi=float(start1[index].get(i,0.0))
                        #print "this is the value of the previous state",qi
                        #qi=0
                        
                        emissionp=float(emission[onebyone].get(j,0.0))
                        #print "This is the emission value of word:::",onebyone,"given tag::::",j,":::",emissionp
                        #print "The value to compare with max will be :::::",(math.log(transp,10)+math.log(emissionp,10)+qi)
                        #print "The max value till now is::",max
                        #print transp
                        #print emissionp
                        if max<(math.log(transp,10)+math.log(emissionp,10)+qi):
                            max=math.log(transp,10)+math.log(emissionp,10)+qi
                            #print "The value of the max is:::: ",max
                            backtrack[index+1]=backtrack.get(index+1,{})
                            #print "the value of the previous is:::",i
                            backtrack[index+1][j]=i
                            #print "for now the value of backtrack for index:::::",index+1,"::will be",backtrack[index+1][j]
                    temp1[index+1]=temp1.get(index+1,{})
                    temp1[index+1][j]=temp1[index+1].get(j,max*1.0)
                    #print "the max value obtained for index:::",index+1,"and for current state ::",j,":: is the previos state",backtrack[index+1][j]
                    #print j, "with the index", index+1," value ", temp1[index+1][j]
                    temp.add(j)
                start1=temp1.copy()#deep copy
                start=temp.copy()
                #print "The valu of the start1::::",start1
                #print "this is just the start",start
                temp1.clear()
                temp.clear()
                currentstate.clear()
                index=index+1
            #print "This is just the start",start
            max=-float("inf")
            for i in start:
                #print "the type willl ====================================",i
                """if i=='':
                    #print "the value odf i is what we go"
                    #print float(transition["''"].get("#END#",0.0))
                    i="''"
                    """
                
                transp=float(transition[str(i)].get("#END#",0.0))
                if transp==0.0:
                    di=transition[i]
                    s = sum(di.values())
                    transition[i][j]=transition[i].get(j,0.0)+(1/(len(tagcount)+float(tagcount[i])))
                    transp=transition[i][j]
                #print "the transition value is::",(math.log(transp,10))
                qi=float(start1[index].get(i,0.0))
                #print "The value of the previos state:",i,"with index",index,"is:::",qi
                emissionp=1.0
                #print "The value to compare with the max:::",max,":::is::::",(math.log(transp,10)+math.log(emissionp,10)+qi)
                #print math.log(transp,10)+math.log(emissionp,10)+qi
                if max<(math.log(transp,10)+math.log(emissionp,10)+qi):
                    max=(math.log(transp,10)+math.log(emissionp,10)+qi)
                    backtrack[index+1]=backtrack.get(index+1,{})
                    backtrack[index+1]["#END#"]=i
            #print "this is backtrack",backtrack
            k=len(backtrack)
            valueoftag="#END#"
            list1=[]
            while k>1:
                """if valueoftag not in backtrack[k]:
                    valueoftag="''"
                if valueoftag not in backtrack[k]:
                    valueoftag=''"""
                valueoftag=backtrack[k][valueoftag]
                #print valueoftag
                k=k-1
                list1.append(valueoftag)
                
            list1.reverse()
            backtrack.clear()
            for k in range(len(words)):
                #print(words[k]+"/"+list1[k]+" ")
                myfile2.write(words[k]+"/"+list1[k]+" ")
            myfile2.write("\n")
                
                           
                    
                            
                        
            
                    
                    
                
            
        

flag="null"
# Fetch and use the HMM Viterbi Algorithm
with open("hmmdata.txt",'r') as myfile:
    data=myfile.readlines()
    for lines in data:
        if lines.startswith("#Emission Probabilities#"):
            flag="emission"
        elif lines.startswith("#Transition Probabilities#"):
            flag="transition"
        elif lines.startswith("#Tag Count#"):
            flag="tagcount"
        elif lines.startswith("#WordTag#"):
            flag="wordtag"
        else:
            fetchthedata(flag,lines)
    ViterbiAlgorithm()
        

    
    
            

        