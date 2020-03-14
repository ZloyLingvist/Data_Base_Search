import stanfordnlp
import os

from text_tree import *

path = os.path.dirname(os.path.abspath(__file__))

class stamford_preprocessing:
    def __init__(self):
        self.text=""
      
    def modify_text_for_stamford(self):
        f=open("Files/config.ini","r",encoding="utf-8")
        for line in f:
            line=line.split(':')
            if line[0]=="List_of_formulas":
                lst_=line[1].strip()
                break
        f.close()
    
        ######## считываем из базы формул #####
        lst_gl=[]
        f=open(lst_,"r",encoding="utf-8")
        for line_ in f:
            lst_gl.append(line_.strip())
        f.close()
   
        lst=[]
        str1=""
        str2=""
        match=0

        for i in range(len(self.text)):
            if self.text[i]=="{":
                match=match+1

            if self.text[i]=="}":
                match=match-1
                str1=str1+self.text[i]
             
            if match>0:
                str1=str1+self.text[i]
           
            if match==0:
                if self.text[i]!="}":
                    str2=str2+self.text[i]

                if str1!="":
                    if not str1 in lst_gl:
                        lst.append(str1)
                        lst=list(set(lst))
                        str2=str2+"formula_"+str(len(lst)+len(lst_gl))
                    else:
                        for k in range(len(lst_gl)):
                            if lst_gl[k]==str1:
                                str2=str2+"formula_"+str(k+1)
                str1=""

        f=open(lst_,"a",encoding="utf-8")
        for i in range(len(lst)):
            f.write(lst[i]+'\n')
        f.close()

        lst=[',',':']
        for i in range(len(lst)):
            str2=str2.replace(lst[i]," "+lst[i])

        lst=[', такой ']
        for i in range(len(lst)):
             str2=str2.replace(lst[i],"")

        lst={', причём такое представление единственно':'unique'}
        for x in lst:
            if x in str2:
                str2=str2.replace(x,lst[x])

            if "числа" in str2 and not "натуральное число" in str2:
                str2=str2.replace("числа","")

        self.text=str2
    
    def punc_modify(self):
        for i in range(len(self.text)):
            if self.text[i]==".":
                if self.text[i].isnumeric() and i<len(self.text[i])-1 and self.text[i+1].isnumeric():
                    continue
                else:
                    self.text=self.text[:i]+" "+self.text[i:]


    def main(self,text,arr):
        tmp=text.split()
       
        for i in range(len(arr)):
                #if arr[i][0]=="то":
                    #print(arr[i],tmp[i])
                    #tmp[i]="тогда"
                
                if arr[i][0]=="она":
                    for k in range(i):
                        if arr[k][2]=="NOUN":
                            if arr[i][1].replace("|Person=3","") in arr[k][1]:
                                tmp[i]=arr[k][0]
                                break

                if arr[i][0]=="данный":
                    for k in range(i):
                        if arr[k][0]==arr[i+1][0]:
                            if "formula_" in arr[k+1][0]:
                                tmp[i]=arr[k+1][0]
                                break
                    
        self.text=" ".join(tmp)
        self.modify_text_for_stamford()
        return self.text



class Stamford:
    def __init__(self):
        self.nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,lemma,pos,depparse', models_dir=path, lang="ru",treebank='ru_syntagrus', use_gpu=True, pos_batch_size=3000)
        self.text=""
        self.root=""
        self.arr=[]
        self.B=stamford_preprocessing()
        self.dict4={}
        self.dict1={}
        self.dict5=[]
        
        f=open("dicts/dict4.txt","r",encoding="utf-8")
        for line in f:
            line=line.split('\t')
            self.dict4[line[0]]=line[1]

        f.close()

        f=open("dicts/dict1.txt","r",encoding="utf-8")
        for line in f:
            line=line.split('\t')
            self.dict1[line[0]]=line[1].strip()

        f.close()

        f=open("dicts/dict5.txt","r",encoding="utf-8")
        for line in f:
            self.dict5.append(line.strip())

        f.close()
        
    def syntax_procedure(self,text,param):
        doc = self.nlp(text)
        
        arr2=[]
        arr3=[]
        for sent in doc.sentences:
            for wrd in sent.dependencies:
                arr2.append(wrd[2].index) ##порядковый номер токен
                arr2.append(wrd[2].text) ##имя токена
                arr2.append(wrd[2].lemma)
                arr3.append(wrd[2].feats) ##морфология
                arr2.append(wrd[2].governor) ##номер родителя
                arr2.append(wrd[2].dependency_relation) ## тип связи
                arr2.append(wrd[2].upos) ##часть речи токена
                self.arr.append(arr2)
                arr2=[]

        if param==0:
            for i in range(len(self.arr)):
                for j in range(len(self.arr[i])):
                    if self.arr[i][j]==None:
                        self.arr[i][j]="None"

                if self.arr[i][3]==0:
                    self.root=str(self.arr[i][0])
                    
                self.arr[i][1]=self.arr[i][2]
                self.arr[i][3]=str(self.arr[i][3])

            self.arr=[self.arr,self.root]
            
            return 0

        lst=['гильбертово','простой','натуральный','евклидовать','липшицев']

        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j]==None:
                    self.arr[i][j]="None"

            if len(self.arr[i])<1:
                continue

            if self.arr[i][5]=="ADJ":
                ids=int(self.arr[i][3])-1
                if self.arr[ids][4]=="root":
                    self.arr[i][3]=str(i+2)

            if "formula" in self.arr[i][2]:
                ids=int(self.arr[i][3])-1
              
                if self.arr[ids][2]=="где":
                    for k in range(len(self.arr)):
                        if self.arr[k][5]=="NOUN":
                            self.arr[i][3]=str(k+1)
                            break

            for x in lst:
                    if self.arr[i][2]==x:
                        for k in range(i+1,len(self.arr)):
                            if self.arr[k][5]=="NOUN":
                                self.arr[k][2]=self.arr[i][2]+" "+self.arr[k][2]
                                self.arr[i][2]="del"
                                break

            if self.arr[i][1]=="не":
                self.arr[i+1][1]=self.arr[i][1]+" "+self.arr[i+1][1]
                self.arr[i+1][2]=self.arr[i][2]+" "+self.arr[i+1][2]
                self.arr[i][2]="del"

          
            for x in self.dict5:
                if self.arr[i][2] in self.dict1:
                    y=self.dict1[self.arr[i][2]]
                    if x==y:
                        ids=int(self.arr[i][3])-1
                        if self.arr[ids][2]=="." and self.arr[i][5]=="ADJ":
                            for k in range(i-1,0,-1):
                                if self.arr[k][5]=="NOUN":
                                    self.arr[i][3]=str(k+1)
                                    break
            
            if self.arr[i][4]=="conj":
                for k in range(i-1,0,-1):
                    if self.arr[i][5]==self.arr[k][5]:
                        self.arr[i][3]=self.arr[k][3]
                        break

            for x in self.dict4:
                x=x.split()
                if len(x)>1:
                    if self.arr[i][2]==x[0]:
                        for k in range(i,len(self.arr)):
                            if str(self.arr[k][3])==str(self.arr[i][0]) and self.arr[i][5]=="NOUN" and self.arr[k][2]==x[1]:
                                self.arr[i][2]=self.arr[i][2]+" "+self.arr[k][2]
                                self.arr[k][2]="del"
                                for m in range(len(self.arr)):
                                    if str(self.arr[m][3])==self.arr[k][0]:
                                        self.arr[m][3]=self.arr[i][0]

            if self.arr[i][2]=="." or self.arr[i][2]=="," or self.arr[i][2]=="и":
                self.arr[i][2]="del"

            if self.arr[i][4]=="root":
                self.root=str(self.arr[i][0])
                if self.arr[i][3]!=0:
                    self.arr[i][3]=0
               
            self.arr[i][1]=self.arr[i][2]
            self.arr[i][3]=str(self.arr[i][3])

        
        self.arr=[self.arr,self.root]


    def extract_label_list(self,a):
        lst=[]

        for x in self.dict4:
            for i in range(len(a)):
                if a[i][1]==x:
                    flag=0
                    for k in range(len(a)):
                        if a[k][3]==str(i+1) and (a[k][4]=="flat:foreign" or "formula" in a[k][2]):
                            if not a[i][2] in self.dict4:
                                continue
                            lst.append([self.dict4[a[i][2]].strip(),a[k][2]])
                            a[i][2]=a[k][2]
                            a[i][1]=a[k][1]
                            a[k][2]="del"
                            a[k][1]="del"
                            flag=1

                    
                    if flag==0:
                        '''
                        b={'функция':'f','множество':'a'}
                        lst.append([self.dict4[a[i][2]].strip(),b[a[i][2]]])
                        a[i][2]=b[a[i][1]]
                        a[i][1]=b[a[i][1]]
                        '''
                    

        for x in self.dict5:
            for i in range(len(a)):
                if a[i][1] in self.dict1:
                    if x==self.dict1[a[i][1]]:
                        if a[i][4]!="root" and a[i][4]!="conj":
                            id_=int(a[i][0])
                        
                            if a[id_][1]!="del":
                                lst.append([self.dict1[a[i][1]],a[id_][1]])
                                a[i][2]="del"
                                a[i][1]="del"

        
        return lst

     
    def run(self,text,param):
        arr=[]
        doc = self.nlp(text)
        for sent in doc.sentences:
            for wrd in sent.dependencies:
                arr.append([wrd[2].lemma,wrd[2].feats,wrd[2].upos,wrd[2].governor,wrd[2].dependency_relation])
                    
        text=self.B.main(text,arr)
       
        text=text.split(",")
        for i in range(len(text)):
            if "если" in text[i]:
                text[i-1],text[i]=text[i],text[i-1]


        res=[]

        for x in text:
            if not "." in x:
                x=x+"."

            if param==1:
                if 'необходимо и достаточно' in x:
                    res.append(["<=>"])
                    continue

            self.syntax_procedure(x,param)

            if param==1:
                a=self.extract_label_list(self.arr[0])

            A=Text_analyzer(self.arr[0],self.arr[1])
            r=A.make_tree(0)
            
            if param==1:
                b=['root']
                b.append(r[0])
                B=Text_predicator(b,a)
                r=B.main()
                res.append(r)
            else:
                res.append(r[0])

            self.arr=[]
                
        if param==1:
            A=Text_predicator([],[])
            res=A.make_predicate(res)
        
        return res

'''
text="Любая непрерывная функция f на компактном пространстве A ограниченна и достигает своих наибольших и наименьших значений ."
A=Stamford()
r=A.run(text,1)
print(r)
'''
