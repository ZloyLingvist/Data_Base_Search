import re
import copy
from ranger_algo import *
import numpy as np
from collections import Counter

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

'''
a=[['if', ['&', ['function', ['f','x']], ['C', ['f'], ['closed_interval',['a', 'b']]],
['dif', ['f'], ['open_interval',['a', 'b']]],['=',['f','a'],['f','b']]]],
['then',['exists',['c',['&',['point','c'],['in',['c'],['closed_interval',['a','b']]],['in',['equal', [['der','f'], '0']], 'c']]]]]]

b=[['if', ['&', ['function', 'f'], ['Real', 'f'], ['C', ['f'],['\\closedinterval', ['a', 'b']]], 
['dif', ['f'], ['open_interval',['a', 'b']]], 
['принимать', ['конец', ['\\closedinterval', ['a', 'b']]], ['одинаковый', 'значение']]]], 
['then', ['exists', ['c', ['&', ['point', 'c'], ['in',['c'],['open_interval', ['a', 'b']]], ['in',['equal', [['der','f'], '0']], 'c']], 
['function', 'f']]]]]


c=[['if', ['&', ['function', 'f'], ['dif', 'f', ['open_interval',['a', 'b']]],['C',['конец', ['open_interval',['a', 'b']]]],['equal',['f','a'],['f','b']]]],
['then', ['exists', ['c', ['&', ['point','c'],['in',['equal', [['der','f'], '0']], 'c']]]]]]


d=[['if', ['&', ['function', 'f'], ['C', ['f'], ['closed_interval',['a', 'b']]],
['forall','c',['&',['point','c'],['in',['c'],['open_interval',['a','b']]],['dif', 'f', 'c'],['внутренний','c']]],
['equal',['f','a'],['f','b']]]],['then',['exists',['c',['&',['point','c'],['\in',['c'],['open_interval',['a','b']]],
['in',['equal', [['der','f'], '0']], 'c']]]]]]

               
x=[a,b,c,d]
y=["Пусть функция {\displaystyle f(x)} непрерывна на отрезке {\displaystyle [a,b]} и дифференцируема на интервале {\displaystyle (a,b)}, причем {\displaystyle f(a)=f(b)} , тогда существует точка {\displaystyle c \in [a, b]} такая, что {\displaystyle f'(c)=0} . " ,
   "Если вещественная функция, непрерывная на отрезке {\displaystyle [a,b]} и дифференцируемая на интервале {\displaystyle (a,b)} ,принимает на концах отрезка {\displaystyle [a,b]} одинаковые значения, то на интервале {\displaystyle (a,b)} найдётся хотя бы одна точка,в которой производная функции равна нулю. ",
   "Пусть функция  дифференцируема в открытом промежутке  , на концах этого промежутка сохраняет непрерывность и принимает одинаковые значения: {\displaystyle f(a)=f(b)} , тогда существует точка  , в которой производная функции  равна нулю : {\displaystyle f'(c)=0}  . ",
    "Если функция f непрерывна на {\displaystyle [a,b]}, функция f дифференцируема во всех внутренних точках {\displaystyle [a,b]} и {\displaystyle f(a)=f(b)}, тогда существует точка {\displaystyle c\in (a,b)}, в которой {\displaystyle f^{\prime}(c)=0} ."
    ]


A=Ranger()
print(A.main(a,c,2))
'''
