import re
import copy
from ranger_algo import *
import numpy as np
from collections import Counter
from draw_graph import *

def jaccard_coeff_algo_three(tmp1,tmp2):
        S1=set(i for i in tmp1)
        S2=set(i for i in tmp2)
        intersection = len(list(S1.intersection(S2)))
        union = (len(S1) + len(S2)) - intersection
        if union!=0:
            res=float(intersection) / union
        else:
            res=0

        return res
            
def path_to_leaves_algo_three(l,tmp,str1):
        for i,elem in enumerate(l):
            if not isinstance(elem,str):         
                l[i]=path_to_leaves_algo_three(elem,tmp,str1)
            else:
                if str1=="":
                    str1=elem
                else:
                    str1=str1+' '+elem
                tmp.append(str1)
                
        return l
    
def simplifier_algo_three(a):
        str1=""
        tmp=[]
        path_to_leaves_algo_three(a,tmp,str1)
        temp=[]
        dict1={}
        for x in tmp:
            temp.append(x.split(' '))

        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if len(temp[i][j])==1:
                    if temp[i][j] in dict1.keys():
                        temp[i][j]=dict1[temp[i][j]]

        return temp

def algorithm_three_func(a,b):
    value=0
    ind=[]
    i,j=0,0
    coeff=1
    a=simplifier_algo_three(a)
    b=simplifier_algo_three(b)
    
    for x in a:
        i=i+1
        coeff=1
        '''
        for m in range(len(b)):
            if x==b[m]:
                coeff=coeff+1
        '''
        for y in b:
            j=j+1
            c=jaccard_coeff_algo_three(x,y)
            value=value+(c*i/len(a))

    return value  

class Ranger:
    def __init__(self):
        self.greek_alphabet=['\\alpha','\\beta','\\gamma','\\omega']
        
    def is_number_regex(self,s):
        if re.match("^\d+?\.\d+?$", s) is None:
            return s.isdigit()
        return True

    def path_to_leaves(self,l,tmp,str1):
        for i,elem in enumerate(l):
            if not isinstance(elem,str):         
                l[i]=self.path_to_leaves(elem,tmp,str1)
            else:
                if str1=="":
                    str1=elem
                else:
                    str1=str1+' '+elem
                tmp.append(str1)
                
        return l

    def simplifier(self,a):
        str1=""
        tmp=[]
        self.path_to_leaves(a,tmp,str1)
        temp=[]
        dict1={}
        for x in tmp:
            temp.append(x.split(' '))

        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if len(temp[i][j])==1:
                    if temp[i][j] in dict1.keys():
                        temp[i][j]=dict1[temp[i][j]]

        return temp

    def jaccard_coeff(self,tmp1,tmp2):
        S1=set(frozenset(i) for i in tmp1)
        S2=set(frozenset(i) for i in tmp2)
        intersection = len(list(S1.intersection(S2)))
        union = (len(S1) + len(S2)) - intersection
        if union!=0:
            res=float(intersection) / union
        else:
            res=0
        
        return res

    def algorithm_one(self,a,b):
        tmp1=self.simplifier(a)
        tmp2=self.simplifier(b)

        tmp1copy=copy.deepcopy(tmp1)
        tmp2copy=copy.deepcopy(tmp2)

        for i in range(len(tmp1copy)-1,-1,-1):
                if i==0:
                    del tmp1copy[i]
                else:
                    del tmp1copy[i][0]

        for i in range(len(tmp2copy)-1,-1,-1):
                if i==0:
                    del tmp2copy[i]
                else:
                    del tmp2copy[i][0]

        r1=self.jaccard_coeff(tmp1,tmp2)
        r2=self.jaccard_coeff(tmp1copy,tmp2)
        r3=self.jaccard_coeff(tmp1,tmp2copy)
        r4=self.jaccard_coeff(tmp1copy,tmp2copy)
        best_score=max(r1,r2,r3,r4)
        return best_score

    def algorithm_two(self,a,b):
        ##взято на данном этапе отсюда. https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation
        tmp1=self.simplifier(a)
        tmp2=self.simplifier(b)
        coeff_1=0
        coeff_2=0
        for i in range(len(tmp1)):
            vec1 = minhash(set(tmp1[i]))
            coeff_1=coeff_1+np.array(vec1) / max(vec1)

        for i in range(len(tmp2)):
            vec2 = minhash(set(tmp2[i]))
            coeff_2=coeff_2+np.array(vec2) / max(vec2)

        a=coeff_1
        b=coeff_2
        
        best_score = 1 - (a @ b.T) / (np.linalg.norm(a)*np.linalg.norm(b)) 
        return best_score


    def main(self,a,b,mode):
        if mode==0:
            best_score=self.algorithm_one(a,b)

        if mode==1:
            best_score=self.algorithm_two(a,b)

        if mode==2:
            a1=algorithm_three_func(a,a)
            b1=algorithm_three_func(b,b)
            a2=algorithm_three_func(a,b)
            b2=algorithm_three_func(b,a)
            
            if a2==0 or b2==0:
                best_score=0
                return 0

            best_score=min(a2/a1,b2/b1)
            
        return best_score



