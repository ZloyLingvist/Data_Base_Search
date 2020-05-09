import re
import copy
from ranger_algo import *
import numpy as np
from collections import Counter

'''Класс ранжировщик
Входные параметры:
- массивы a,b
- номер алгоритма (0,1,2)
'''

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
        for x in tmp:
            temp.append(x.split(' '))

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
        best_score=self.jaccard_coeff(tmp1,tmp2)
        return best_score


    def main(self,a,b,mode):
        if mode==0:
            best_score=self.algorithm_one(a,b)

        if mode==1:
            a1=algorithm_three_func(a,a)
            a2=algorithm_three_func(a,b)
            b1=algorithm_three_func(b,b)
            b2=algorithm_three_func(b,a)
            
            best_score=0.5*(a2/a1+b2/b1)
            

        return best_score

