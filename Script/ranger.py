import re
import os

'''Класс ранжировщик
Входные параметры:
- массивы a,b
'''

path=os.path.dirname(os.path.dirname(__file__))

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


    def main(self,a,b):
        best_score=self.algorithm_one(a,b)
        return best_score




