from text_predicator import *
from text_tree import *

import os
path = os.path.dirname(os.path.abspath(__file__))

import warnings
warnings.simplefilter("ignore", UserWarning)
import stanfordnlp

parent_directory=os.path.dirname(os.path.dirname(__file__))
dict_path=parent_directory+"\\Files\\"

'''Класс Stamford
Входные параметры:
param1 - текст или массив с синтаксическим разбором
param2 - параметр, отвечающий на каком этапе нужно остановить работу
'''

class Stamford:
    def __init__(self):
        self.a=[]

        f=open(dict_path+"dicts/words_obj.txt","r",encoding="utf-8")
        self.words_obj=[]
        self.words_replace=[]
        self.words_construction=[]
        
        for line in f:
            line=line.split('\t')
            line[1]=line[1].strip()
            self.words_obj.append(line)
        f.close()

        
        f=open(dict_path+"dicts/words_replace.txt","r",encoding="utf-8")
        for line in f:
            if '#' in line:
                continue
            line=line.split('\t')
            line[1]=line[1].strip()
            self.words_replace.append(line)
        f.close()

        f=open(dict_path+"dicts/words_construction.txt","r",encoding="utf-8")
        for line in f:
            line=line.split('\t')
            line[4]=line[4].strip()
            self.words_construction.append(line)
        f.close()
        
    def split(self,a):
        tst=[]
        tst_=[]

        for i in range(len(a)):
            if a[i][2]=="который":
                for k in range(i,0,-1):
                    if a[k][5]=="NOUN":
                        a[i][2]=a[k][2]
                        a[i][1]=a[k][1]
                        break
                    
            if a[i][1]=="и":
                if a[i+1][5]=="VERB":
                        a[i]=[a[i][0],',', ',', '1', 'punct', 'PUNCT']
                               
        for x in a:
            tst_.append(x)
            if x[1]==',':        
                tst.append(tst_)
                tst_=[]

        if tst_!=[]:
            tst.append(tst_)
            
        ids=0
        for k in range(len(tst)):
            '''последний элемент меняем на .'''
            
            if tst[k][0][5]=="VERB":
                tst[k][0][3]="0"
                        
            for m in range(len(tst[k])):
                tst[k][m][0]=str(int(tst[k][m][0])-ids)
                tst[k][m][3]=int(tst[k][m][3])-ids

                if tst[k][m][3]<0:
                    tst[k][m][3]=str(0)
                else:
                    tst[k][m][3]=str(tst[k][m][3])

                if int(tst[k][m][3])>len(tst[k]):
                    if tst[k][0][2]=="если" or tst[k][0][2]=="то" or tst[k][0][2]=="тогда":
                        tst[k][0][3]="0"
                        for j in range(1,len(tst[k])):
                            if tst[k][j][3]=="0":
                                tst[k][j][3]="1"
                       
                    for j in range(len(tst[k])):
                        if tst[k][j][3]=="0":
                            tst[k][m][3]=tst[k][j][0]

            ids=ids+len(tst[k])
            self.a=tst
            

    def extract_label_list(self,a):
        lst=[]

        self.dict4={'функция':'function'}
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

        return lst

    def correction(self):
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                if self.a[i][j][5]=="PUNCT":
                    self.a[i][j][2],self.a[i][j][1]="del","del"
                    
                if self.a[i][j][5]=="ADJ":
                    if self.a[i][j][3]=="0" or (self.a[i][j][3]!="0" and self.a[i][int(self.a[i][j][3])-1][5]!="NOUN"):
                        if i>0:
                            for k in range(len(self.a[i-1])-1,0,-1):
                                if self.a[i-1][k][5]=="NOUN":
                                    self.a[i].append([str(len(self.a)),self.a[i-1][k][1],self.a[i-1][k][2],self.a[i][j][0],self.a[i-1][k][4],self.a[i-1][k][5]])
                                    break
       
        for i in range(len(self.a)):
             for j in range(len(self.a[i])):
                for k in range(len(self.words_construction)):
                     if self.words_construction[k][0]==self.a[i][j][2]:
                         tmp=self.a[i][j:j+int(self.words_construction[k][2])]
                         
                         str1=""
                         for x in tmp:
                             if str1=="":
                                 str1=x[2]
                             else:
                                 str1=str1+" "+x[2]

                         if str1==self.words_construction[k][1]:
                             if self.words_construction[k][3]=="del_full":
                                 for n in range(int(self.words_construction[k][2])):
                                     self.a[i][j+n][2],self.a[i][j+n][1]="del","del"

                             if self.words_construction[k][3]=="join":
                                 for n in range(int(self.words_construction[k][2])):
                                     self.a[i][j+n][2],self.a[i][j+n][1]="del","del"

                                 ids=int(self.words_construction[k][4])-1
                                 self.a[i][j+ids][2],self.a[i][j+ids][1]=str1,str1
                             
                                          
                for k in range(len(self.words_obj)):
                    if self.words_obj[k][0]==self.a[i][j][1]:
                        flag=1
                        for m in range(len(self.a[i])):
                            if self.a[i][m][3]==self.a[i][j][0]:
                                 if self.a[i][m][4]=="flat:foreign" or "formula" in self.a[i][m][2]:
                                     flag=0
                                     break

                        if flag==1:
                            self.a[i].append([str(len(self.a[i])+1),self.words_obj[k][1],self.words_obj[k][1],self.a[i][j][0],'flat:foreign','PROPN'])
                            self.a[i][-1],self.a[i][-2]=self.a[i][-2],self.a[i][-1]

        
        for i in range(len(self.a)):
             for j in range(len(self.a[i])):
                for k in range(len(self.words_replace)):
                     if self.words_replace[k][0]==self.a[i][j][2]:
                         self.a[i][j][1],self.a[i][j][2]=self.words_replace[k][1],self.words_replace[k][1]

                if j<len(self.a[i])-1:
                    if int(self.a[i][j][0])>int(self.a[i][j+1][0]):
                        self.a[i][j],self.a[i][j+1]=self.a[i][j+1],self.a[i][j]

        
                         

    def main(self,a,mode):
        if type(a)==str:
            nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,lemma,pos,depparse', models_dir=parent_directory, lang="ru",treebank='ru_syntagrus', use_gpu=True, pos_batch_size=3000)
            doc = nlp(a)
            i=0
            a=[]
            for sent in doc.sentences:
                for wrd in sent.dependencies:
                    a.append([str(i+1),wrd[2].text,wrd[2].lemma,str(wrd[2].governor),wrd[2].dependency_relation,wrd[2].upos])
                    i=i+1

        if mode==0:
            roots=0
            for i in range(len(a)):
                if a[i][3]=="0" and a[i][1]!="del":
                        roots=a[i][0]

            A=Text_analyzer(a,roots)
            p2=A.make_tree()
            return p2

        self.split(a)
        self.correction()
        roots=[]
        res=[]
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                if self.a[i][j][3]=="0" and self.a[i][j][1]!="del":
                    roots.append(self.a[i][j][0])

        for i in range(len(self.a)):
            A=Text_analyzer(self.a[i],roots[i])
            r=A.make_tree()
            res.append(r)

        A=Text_predicator()
        p2=A.main(res)
        return p2


