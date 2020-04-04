import warnings
warnings.simplefilter("ignore", UserWarning)
import stanfordnlp
import os

from text_tree import *

path = os.path.dirname(os.path.abspath(__file__))

class stamford_preprocessing:
    def __init__(self):
        self.text=""
      
    def modify_text_for_stamford(self):
        str2=self.text
        lst=[',',':']
        for i in range(len(lst)):
            str2=str2.replace(lst[i]," "+lst[i])

        lst=[', такой ']
        for i in range(len(lst)):
             str2=str2.replace(lst[i],"")

        lst={', причём такое представление единственно':'unique',
             'принимает значения противоположных знаков':'противоположнозначный'}

        for x in lst:
            if x in str2:
                str2=str2.replace(x,lst[x])

            if "числа" in str2 and not "натуральное число" in str2:
                str2=str2.replace("числа","")

        str2=str2.split()
        for i in range(len(str2)):
            if str2[i]=="противоположнозначный":
                str2[i-1],str2[i]=str2[i],str2[i-1]

        str2=" ".join(str2)
        self.text=str2
        return str2
    
    def punc_modify(self):
        for i in range(len(self.text)):
            if self.text[i]==".":
                if self.text[i].isnumeric() and i<len(self.text[i])-1 and self.text[i+1].isnumeric():
                    continue
                else:
                    self.text=self.text[:i]+" "+self.text[i:]


    def etap_one(self,text,arr):
        text=text.replace(","," ,")
        tmp=text.split()

        for i in range(len(arr)):
                if arr[i][0]=="и":
                    for p in range(i,len(arr)):
                        if (arr[p][2]=="VERB" or arr[p][2]=="ADJ") and arr[p][4]=="conj":
                            tmp[i]=","

                if arr[i][4]=="root" or (arr[i][4]=="conj" and (arr[i][2]=="VERB" or arr[i][2]=="ADJ")):
                    flag=0
                    for p in range(len(arr)):
                        if arr[p][4]=="nsubj" and arr[p][3]==i+1:
                            flag=1
                            break

                    if flag==0:
                        for k in range(i,0,-1):
                            if "nsubj" in arr[k][4]:
                                tmp[i]=arr[k][0]+" "+arr[i][0]
                                for p in range(len(arr)):
                                    if arr[p][3]==k+1 and (arr[p][4]=="flat:foreign" or "formula" in arr[p][0]):
                                        tmp[i]=arr[p][0]+" "+arr[i][0]
                                        break
                                break

                if arr[i][0]==",":
                    if arr[i+1][0]=="где":
                        tmp[i+1]=""
                        
                if arr[i][0]=="функция" or arr[i][0]=="точка":
                    flag=0
                    for m in range(len(arr)):
                        if arr[m][0]=="данный" or arr[m][0]=="этот":
                            flag=1
                            break
                        if arr[m][3]==i+1:
                            if arr[m][4]=="flat:foreign" or "formula" in arr[m][0]:
                                flag=1
                                break
                    
                    if flag==0 and arr[i][0]=="функция":
                        tmp[i]=tmp[i]+" "+"f"
                    if flag==0 and arr[i][0]=="точка":
                        tmp[i]=tmp[i]+" "+"a"
                            
                if arr[i][0]=="то":
                    tmp[i]="тогда"

       
        text=" ".join(tmp)
        return text

    def etap_two(self,text,arr):
        tmp=text.split()
        ls=['равенство','следующий','такой','что']
        for i in range(len(arr)):
                if arr[i][0] in ls:
                    tmp[i]=""
                    
                if arr[i][0]=="нуль":
                    tmp[i]="0"
                    
                if arr[i][0]=="это":
                    if arr[i+1][0]=="отрезка":
                        arr[i+1][0]="отрезок"
                        arr[i][0]="этот"
                        
                if arr[i][0]=="она" or arr[i][0]=='он':
                    for k in range(i):
                        if arr[k][2]=="NOUN":
                            if arr[i][1].replace("|Person=3","") in arr[k][1] or arr[i][1].replace("Masc","Neut").replace("|Person=3","") in arr[k][1]:
                                tmp[i]=arr[k][0]
                                for m in range(k,len(arr)):
                                    if arr[m][3]==k+1:
                                        if arr[m][4]=="flat:foreign" or "formula" in arr[m][0]:
                                            tmp[i]=arr[m][0]
                                            break
                                break

                if arr[i][0]=="данный" or arr[i][0]=="этот":
                    for k in range(i):
                        if arr[k][0]==arr[i+1][0]:
                            if arr[k+1][4]=="flat:foreign" or "formula" in arr[k+1][0]:
                                tmp[i]=arr[k+1][0]
                                tmp[i],tmp[i+1]=tmp[i+1],tmp[i]
                                break

                if arr[i][0]=='который':
                     for k in range(i,0,-1):
                        if arr[k][2]=="NOUN":
                            tmp[i]=arr[k][0]
                            flag=0
                            for m in range(k,len(arr)):
                                if arr[m][3]==k+1 and arr[m][4]=="flat:foreign" or "formula" in arr[m][0]:
                                        tmp[i]=""
                                        if arr[i-1][0]=="в":
                                            tmp.insert(len(tmp)-1,tmp[i-1])
                                            tmp[i]=""
                                            
                                        tmp.insert(len(tmp)-1,arr[m][0])
                                        break
                        
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
            if len(line)==2:
                self.dict1[line[0]]=line[1].strip()

        f.close()

        f=open("dicts/dict5.txt","r",encoding="utf-8")
        for line in f:
            self.dict5.append(line.strip())

        f.close()

    def parse(self,text):
        arr3=[]
        arr=[]
        doc = self.nlp(text)
        arr2=[]
        for sent in doc.sentences:
            for wrd in sent.dependencies:
                arr2.append(wrd[2].index) ##порядковый номер токен
                arr2.append(wrd[2].text) ##имя токена
                arr2.append(wrd[2].lemma)
                arr3.append(wrd[2].feats) ##морфология
                arr2.append(wrd[2].governor) ##номер родителя
                arr2.append(wrd[2].dependency_relation) ## тип связи
                arr2.append(wrd[2].upos) ##часть речи токена
                arr.append(arr2)
                arr2=[]

        return arr

        
    def syntax_procedure(self,text,param):
        self.arr=self.parse(text)
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

        lst=['гильбертово','простой','натуральный','евклидовать','липшицев','случайный']

        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j]==None:
                    self.arr[i][j]="None"

            if len(self.arr[i])<1:
                continue

            if self.arr[i][1]=="отрезка":
                self.arr[i][2]="отрезок"

            if self.arr[i][2]=="из" or self.arr[i][2]=="на" or self.arr[i][2]=="в":
                self.arr[i][2]="del"
                
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

        str1=""
        for i in range(len(self.arr)):
            if self.arr[i][2]=="равномерно":
                if i<len(self.arr[i])-1:
                    if self.arr[i+1][5]=="ADJ":
                        self.arr[i+1][2]=self.arr[i][2]+" "+self.arr[i+1][2]
                        self.arr[i+1][1]=self.arr[i+1][2]
                        self.arr[i][2],self.arr[i][1]="del","del"


            if self.arr[i][2]=="сходиться" or self.arr[i][1]=="последовательность":
               for k in range(len(self.arr)):
                   if self.arr[k][3]==self.arr[i][0]:
                       if self.arr[i][2]=="сходиться" and self.arr[k][2]=="вероятность" or self.arr[k][2]=="распределение":
                           if self.arr[k-1][2]=="по":
                               self.arr[i][2]=self.arr[i][2]+" "+self.arr[k-1][2]+" "+self.arr[k][2]
                               self.arr[i][1]=self.arr[i][2]
                               self.arr[k][2],self.arr[k][1]="del","del"
                               self.arr[k-1][2],self.arr[k-1][1]="del","del"
                               

                       if self.arr[i][1]=="последовательность":
                           if self.arr[k][5]=="NOUN":
                               self.arr[i][2]=self.arr[i][2]+" "+self.arr[k][2]
                               self.arr[i][1]=self.arr[i][2]
                               self.arr[k][2]="del"
                               self.arr[k][1]="del"
                               for m in range(len(self.arr)):
                                   if self.arr[m][3]==self.arr[k][0]:
                                       self.arr[m][3]=self.arr[i][0]
            

        self.arr=[self.arr,self.root]


    def extract_label_list(self,a):
        lst=[]

        for i in range(len(a)):
            if a[i][1]=="сходиться по распределение":
                a[i][2]="convergence_in_distribution"
            if a[i][2]=="сходиться по вероятность":
                a[i][2]="convergence_in_probability"
            if a[i][2]=="сходиться по мере":
                a[i][2]="convergence_in_measure"

                
        for x in self.dict4:
            for i in range(len(a)):
                if a[i][1]==x:
                    flag=0
                    for k in range(len(a)):
                        if a[k][3]==str(i+1) and (a[k][4]=="flat:foreign" or "formula" in a[k][2]):
                            if not a[i][2] in self.dict4 and not a[i][2]=="del":
                                lst.append([a[i][2].strip(),a[k][2]])
                            else:
                                lst.append([self.dict4[a[i][2]].strip(),a[k][2]])

                            a[i][2]=a[k][2]
                            a[i][1]=a[k][1]
                            a[k][2]="del"
                            a[k][1]="del"
                            flag=1

        for i in range(len(a)):
              if a[i][2]=="свой":
                  a[i][2]="del"
                  continue
                  
              if a[i][2]=="любой":
                  continue
                
              if a[i][5]=='ADJ' or a[i][5]=='DET':
                  ids=int(a[i][3])-1
                
                  if a[ids][5]=="NOUN" or "formula" in a[ids][1]:
                      if a[ids][1] in self.dict1:
                          a[ids][1]=self.dict1[a[ids][1]]
                      if a[i][1] in self.dict1:
                          a[i][1]=self.dict1[a[i][1]]

                      temp=[a[i][1],a[ids][1]]
                      if temp==['наибольший', 'значение']:
                          temp=['max']
                      if temp==['наименьший', 'значение']:
                          temp=['min']
                          
                      lst.append(temp)
                      a[i][2]="del"
                      a[i][1]="del"
                
        
        return lst

     
    def run(self,text,param):
        arr=[]
        text=replace_formulas(text)
       
        doc = self.nlp(text)
        for sent in doc.sentences:
            for wrd in sent.dependencies:
                arr.append([wrd[2].lemma,wrd[2].feats,wrd[2].upos,wrd[2].governor,wrd[2].dependency_relation])
                    
        text=self.B.etap_one(text,arr)
        arr=[]

        doc = self.nlp(text)
        for sent in doc.sentences:
            for wrd in sent.dependencies:
                arr.append([wrd[2].lemma,wrd[2].feats,wrd[2].upos,wrd[2].governor,wrd[2].dependency_relation])
                
        text=self.B.etap_two(text,arr)
        
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
                
                if '—' in x:
                    self.syntax_procedure(x,param)
                    tmp=['type']
                    tmp1=['property']
                    
                    for i in range(len(self.arr[0])):
                        if self.arr[0][i][4]=="nsubj" or self.arr[0][i][4]=="root":
                            tmp.append(self.arr[0][i][1])
                        if self.arr[0][i][4]=="amod":
                            tmp1.append(self.arr[0][i][1])

                    tmp.append(tmp1)
                    res.append(tmp)
                    continue

                if 'достигает' in x:
                    self.syntax_procedure(x,param)
                    tmp=['set']
                    for i in range(len(self.arr[0])):
                        if self.arr[0][i][5]=="NOUN" and self.arr[0][i][3]==self.arr[1]:
                            tmp.append(self.arr[0][i][1])

                    res.append([['достичь']+tmp])
                    continue
                    
            self.syntax_procedure(x,param)
            for i in range(len(self.arr[0])):
                if self.arr[0][i][2]=="равномерно непрерывно":
                    self.arr[0][i][2]="uniform_continuity"

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
            for i in range(len(res)-1,-1,-1):
                if not "if" in res[i] and not "then" in res[i] and not "type" in res[i] and not "<=>" in res[i]:
                    if i>0 and type(res[i-1])==list:
                        for x in res[i]:
                            res[i-1].append(x)
                        del res[i]

            A=Text_predicator([],[])
            res=A.make_predicate(res)
        
        return res


