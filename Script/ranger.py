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

