import re
import copy

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

        ###удаление ветвей, где двуместная операция одноместная
        '''
        for i in range(len(temp)-1,-1,-1):
            print(temp[i])
            for j in range(len(temp[i])-1,-1,-1):
                if temp[i][j]=="-" or temp[i][j]=="+" or temp[i][j]=="/" or temp[i][j]=="*":
                    if abs(len(temp[i])-j-1)==1:
                        del temp[i]
        '''
                    
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if len(temp[i][j])==1:
                    if temp[i][j] in dict1.keys():
                        temp[i][j]=dict1[temp[i][j]]
                               
                if  not temp[i][j] in dict1.keys():
                    if len(re.sub("[A-Za-z]", '', temp[i][j]))==0 or temp[i][j] in self.greek_alphabet:
                        #dict1[temp[i][j]]="V_"+str(len(dict1))
                        #temp[i][j]="V_"+str(len(dict1)-1)
                        dict1[temp[i][j]]="V"
                        temp[i][j]="V"
                    if self.is_number_regex(temp[i][j]):
                        dict1[temp[i][j]]="N"
                        temp[i][j]="N"

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

    def main(self,a,b):
        tmp1=self.simplifier(a)
        tmp2=self.simplifier(b)

        #print(tmp1)
        #print()
        #print(tmp2)
    
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
       
        while True:
            if len(tmp1copy)<1 or len(tmp2copy)<1 or best_score==1:
                break

            t1=copy.deepcopy(tmp1copy)
            t2=copy.deepcopy(tmp2copy)
            
            for i in range(len(tmp1copy)-1,-1,-1):
                    if len(tmp1copy[i])>0:
                        del tmp1copy[i][0]
                    if tmp1copy[i]==[]:
                        del tmp1copy[i]


            for i in range(len(tmp2copy)-1,-1,-1):
                    if len(tmp2copy[i])>0:
                        del tmp2copy[i][0]
                    if tmp2copy[i]==[]:
                        del tmp2copy[i]

            r1=self.jaccard_coeff(t1,t2)
            r2=self.jaccard_coeff(t1,tmp2copy)
            r3=self.jaccard_coeff(tmp1copy,t2)
            r4=self.jaccard_coeff(tmp1copy,tmp2copy)
           
            if max(r1,r2,r3,r4)>best_score:
                best_score=max(r1,r2,r3,r4)
                
        return best_score
        
   
