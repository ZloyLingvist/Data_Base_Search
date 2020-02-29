import stanfordnlp
import os
import pickle

from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from combine_formula_text import *
from text_predicator import *


path = os.path.dirname(os.path.abspath(__file__))

class Stamford:
    def __init__(self):
        self.nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,lemma,pos,depparse', models_dir=path, lang="ru",treebank='ru_syntagrus', use_gpu=True, pos_batch_size=3000)
        self.text=""
        self.root=""
        self.arr=[]
        self.modify_text()
        
    def syntax_procedure(self,text):
        doc = self.nlp(text)
        self.arr=[]
        arr2=[]
        
        for sent in doc.sentences:
            for wrd in sent.dependencies:
                arr2.append(wrd[2].index) ##порядковый номер токен
                arr2.append(wrd[2].text) ##имя токена
                arr2.append(wrd[2].lemma)
                #arr2.append(wrd[2].feats) ##морфология
                arr2.append(wrd[2].governor) ##номер родителя
                arr2.append(wrd[2].dependency_relation) ## тип связи
                arr2.append(wrd[2].upos) ##часть речи токена
                self.arr.append(arr2)
                arr2=[]
      
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j]==None:
                    self.arr[i][j]="None"
                    
            if self.arr[i][3]==0:
                self.root=str(self.arr[i][0])

            self.arr[i][3]=str(self.arr[i][3])

        self.arr=[self.arr,self.root]
        
    def write_stamford(self,path_to_files,outfile,mode):
        text_list=[]
        f=open(path_to_files,"r",encoding="utf-8")
        for line in f:
            if line!='\n':
                text=line.strip()
                text_list.append(text)
        f.close()

        if mode==0:
             with open(outfile, 'a') as filehandle:
                 for x in text_list:
                     doc = self.nlp(x)
                     str2=""
                     for sent in doc.sentences:
                        for wrd in sent.dependencies:
                            str2=str2+str(wrd[2].index)+'\t' ##порядковый номер токен
                            str2=str2+str(wrd[2].text)+'\t' ##имя токена
                            str2=str2+str(wrd[2].lemma)+'\t'
                            str2=str2+str(wrd[2].upos)+'\t' ##часть речи токена
                            str2=str2+str(wrd[2].feats)+'\t' ##морфология
                            str2=str2+str(wrd[2].governor)+'\t' ##номер родителя
                            str2=str2+str(wrd[2].dependency_relation)+'\n' ## тип связи
                           

                     filehandle.write(str2)
                     str2=""
                

        if mode==1:
            with open(outfile, 'ab') as filehandle:
                for x in text_list:
                    self.syntax_procedure(x)
                
                    pickle.dump(self.arr, filehandle)
                    pickle.dump('\n',filehandle)

    def read_stamford(self,infile):
        database=[]
        with open(infile+".db","rb") as fileOpener:
            while True:
                try:
                    database.append(pickle.load(fileOpener))
                except EOFError:
                    break

        #A=Text_analyzer(database[12][0],database[12][1])
        #e=A.make_tree()
        #print(e)

    def modify_text(self):
        f=open("dicts/dict_stamford.txt","r",encoding="utf-8")
        for line in f:
            line=line.split('\t')
            if line[0] in self.text:
                self.text=self.text.replace(line[0],line[1].strip())
        f.close()
        
        return self.text

    def run(self,text,param):
        self.syntax_procedure(text)
        self.modify_tree()
        
        A=Text_analyzer(self.arr[0],self.arr[1])
        r=A.make_tree(param)
        return r

       

    def modify_tree(self):
        a=self.arr[0]
       
        for i in range(len(a)):
            if a[i][1]=="не":
                a[i+1][2]=a[i][1]+" "+a[i+1][2]

            if a[i][1]=="абсолютно":
                if a[i+1][2]=="непрерывно":
                    a[i+1][2]=a[i][1]+" "+a[i+1][2]

            if a[i][1]=="<=>":
                a[i][2]='<=>'

            if a[i][2]=="uniquely":
                a[i][3]=self.root

            if a[i][4]=="conj" and a[i][5]=="ADJ":
                a[i][3]=a[int(a[i][3])-1][3]

            if a[i][2]=="весь":
                a[i][2]="all"
                a[i][1]="all"
            
            if a[i][2]=="она" or a[i][2]=="они":
                 flag=1
                 for k in range(i,0,-1):
                    if a[k][5]=="NOUN":
                        a[i][1]=a[k][1]
                        a[i][2]=a[k][2]
                        flag=0
                        break

                 if flag==1:
                    for k in range(len(a)):
                        if a[k][5]=="PROPN":
                            a[i][1]=a[k][1]
                            a[i][2]=a[k][2]
                            flag=0
                            break
                        
        for i in range(len(a)):        
            if a[i][2]!=None and "f_" in a[i][2]:
                a[i][4]="flat:foreign"
                

