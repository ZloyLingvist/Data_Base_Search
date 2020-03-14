from text_tree import *

class Text_predicator:
        def __init__(self,tmp,label_list):
                self.temp=tmp
                self.tmp=[]
                self.str=""
                self.subj_list=[]
                self.label_list=label_list
                self.root=""

        def clean(self):
                for i in range(len(self.tmp)-1,-1,-1):
                        if self.tmp[i]==[]:
                                del self.tmp[i]
                                continue
                        for k in range(len(self.tmp[i])-1,-1,-1):
                                if self.tmp[i][k]==[]:
                                        del self.tmp[i][k]

        def make_predicate_stage_one(self,arr,d5):
                lst=['в','на','из']
                for i in range(len(arr)):
                        for k in range(i+1,len(arr)):
                                if len(arr[i])>0 and type(arr[i])==list and len(arr[k])>0 and arr[i][0]==arr[k][0]:
                                        for m in range(1,len(arr[k])):
                                                arr[i].append(arr[k][m])
                                        arr[k]=[]
                                else:
                                        break

                for i in range(len(arr)):
                        if type(arr[i])==list:
                                for j in range(len(arr[i])):
                                        if len(arr[i])>0 and j<len(arr[i])-1 and arr[i][j] in lst:
                                                if not arr[i][0] in d5:
                                                        arr[i]=["in",arr[i][:j]]
                                                else:
                                                        arr[i][j]=[]

                for i in range(len(arr)-1,-1,-1):
                        if arr[i]==[]:
                                del arr[i]
                                continue
                        
                        for j in range(len(arr[i])-1,-1,-1):
                                if arr[i][j]==[]:
                                        del arr[i][j]

                for i in range(len(arr)):
                        if len(arr[i])>0:
                                if arr[i][0]=="exists":
                                        for k in range(len(arr)):
                                                if type(arr[k])==list and i!=k:
                                                        arr[k],arr[i]=arr[i],arr[k]
                                                        break

                                if arr[i][0]=="=>":
                                        arr[i]=["=>",arr[i][1:]]
                
                                if arr[i]=="then":
                                        for k in range(len(arr)):
                                                if type(arr[k])==list and i!=k:
                                                        arr[k],arr[i]=arr[i],arr[k]
                                                        break

                for i in range(len(arr)-1,-1,-1):
                        if type(arr[i])==list:
                                for j in range(len(arr[i])-1,-1,-1):
                                        if len(arr[i][j])>0 and (arr[i][0]=="forall" or arr[i][0]=="exists"):
                                                arr[i].append(["&"]+arr[i+1:])
                                                arr[i+1:]=[]
                                        
        
                for i in range(len(arr)-1,-1,-1):
                        if len(arr)>0 and (arr[i]=="if" or arr[i]=="then"):
                                temp=["&"]+arr[i+1:]
                                for k in range(len(arr)-1,1,-1):
                                        del arr[k]   

                                if i<len(arr)-1:
                                        arr[i+1]=temp

                        if len(arr[i])>0 and arr[i][0]=="exists":
                                temp=[]
                                c=arr[i][1:]

                                for k in range(len(arr[i])-1,1,-1):
                                    del arr[i][k]
            
                                for m in range(len(c)):
                                    temp.append(c[m])

                                if i<len(arr)-1 and not "then" in arr[i+1:]:
                                    c=["&"]+arr[i+1:]
                                    temp.append(c)
                                    del arr[i+1:]
           
                                arr[i][1]=temp
           
    
                for k in range(len(arr)-1,-1,-1):
                        if arr[k]==[]:
                                del arr[k]
                                continue
        
                        for j in range(len(arr[k])-1,-1,-1):
                                if arr[k][j]==[]:
                                        del arr[k][j]
        
                return arr

        def make_predicate_sub_stage(self,arr):
                for j in range(len(arr)-1,-1,-1):
                        if type(arr[j])==list:
                                if len(arr[j])==1:
                                        arr[j]=arr[j][0]
                                        if "что" in arr[j]:
                                                for i in range(len(arr[j])-1,-1,-1):
                                                        if len(arr[j])>0 and (arr[j][i]=="что"):
                                                                del arr[j][i]
                                                                c=arr[j]
                                                                arr[j-1].append(c)

                                                del arr[j]
          
                for i in range(len(arr)):
                        if arr[i]=="<=>":
                                arr[0],arr[i]=arr[i],arr[0]

                return arr

        def make_predicate(self,arr):
                d5=self.read_from_file("dicts/dict5","list")
                for i in range(len(arr)):
                        arr[i]=self.make_predicate_stage_one(arr[i],d5)

                arr=self.make_predicate_sub_stage(arr)
                
                if len(arr)==1:
                        arr=arr[0]
        
                for i in range(len(arr)):
                        if type(arr[i])==list and len(arr[i])==1:
                                arr[i]=arr[i][0]
                return arr

               
                                        
        def canonizer_one(self,arr,d5):
                for i in range(len(arr)-1,-1,-1):
                        for j in range(len(arr[i])-1,-1,-1):
                                if j<len(arr[i])-1:
                                        if (arr[i][j] in d5 or arr[i][j]=="forall") and j!=0 and arr[i][0]!="=>":
                                                arr[i][0],arr[i][j]=arr[i][j],arr[i][0]
                                        
                                        if (arr[i][j] in d5 or arr[i][j]=="forall") and arr[i][0]=="=>":
                                                arr[i][1],arr[i][j]=arr[i][j],arr[i][1]
                                
                        
                return arr

                

        def read_from_file(self,infile,mode):
                lst=[]
                dict_tmp={}
                f=open(infile+".txt","r",encoding="utf-8")
                if mode=="dict" or mode=="dict_":
                        if mode=="dict_":
                                for line in f:
                                        line=line.strip().split('|')
                                        dict_tmp[line[0].strip()]=line[1].strip()
                                f.close()
                        else:
                                for line in f:
                                        line=line.strip().split()
                                        dict_tmp[line[0]]=line[1]
                                f.close()
                        
                        return dict_tmp
                
                if mode=="list":
                        for line in f:
                                line=line.strip()
                                lst.append(line)
                        f.close()
                        return lst

        

        def del_dupls(self,arr):
                seen=set()
                seen_add=seen.add
                return [x for x in arr if not (x in seen or seen_add(x))]

        def transform(self,d1,d2,d3,d4,d5,d6):
                ##сделали обход
                self.make_pass(self.temp,self.str)
               
                '''если строка полностью входит в соседнюю, то ее можно удалить'''
                for i in range(len(self.tmp)-1,-1,-1):
                        self.tmp[i]=self.tmp[i].replace("root","").strip()
                        self.tmp[i]=self.tmp[i].replace("являться","").strip()
                        
                        if i<len(self.tmp)-1:
                            check=False
                            a=self.tmp[i+1].split()
                            b=self.tmp[i].split()
        
                            if len(a)>len(b):
                                    check=all(item in a for item in b)
                                    if check==True:
                                            del  self.tmp[i]
                                            continue

                            if len(a)<len(b):
                                    check=all(item in b for item in a)
                                    if check==True:
                                            del self.tmp[i+1]
                                            continue

                
                '''устойчивые конструкции заменяем на эквиваленты'''
                for i in range(len(self.tmp)):
                        for x in d6:
                                if x in self.tmp[i]:
                                        self.tmp[i]=self.tmp[i].replace(x,d6[x])

               
                for i in range(len(self.tmp)):
                        ## удаляем ненужные слова (находятся в словаре dict2)
                        for x in d2:
                                if x in self.tmp[i]:
                                        self.tmp[i]=self.tmp[i].replace(x,'')
                                        
                        ## замена на эквиваленты
                        for x in d1:
                                if x in self.tmp[i]:
                                        self.tmp[i]=self.tmp[i].replace(x,d1[x])
                                
                        self.tmp[i]=self.tmp[i].split()

                
                for i in range(len(self.tmp)):
                        if type(self.tmp[i])==list:
                                for j in range(len(self.tmp[i])):
                                        if j<len(self.tmp[i])-1:
                                                if self.tmp[i][j]=="del":
                                                        self.tmp[i]=[]
                                        
                self.clean()
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if "forall" in self.tmp[i][j]:
                                        self.tmp.insert(i,self.tmp[i][:j])
                                        del self.tmp[i+1][0]
                                        break

                        if "if" in self.tmp[i]:
                                self.tmp[i]="if"

                        if "then" in self.tmp[i]:
                                self.tmp[i]="then"

                '''перемещаем конструкции с forall и exists в начало'''
                for i in range(len(self.tmp)):
                        if ("forall" in self.tmp[i] and i>0) or ("exists" in self.tmp[i] and i>0):
                                for k in range(len(self.tmp)):
                                        if type(self.tmp[k])==list:
                                                self.tmp[i],self.tmp[k]=self.tmp[k],self.tmp[i]
                                                break

                for i in range(len(self.tmp)-1,-1,-1):
                        if i<len(self.tmp)-1 and self.tmp[i][0]=="=>" and self.tmp[i+1][0]=="=>":
                                for x in range(len(self.tmp[i+1])-1,-1,-1):
                                        if not self.tmp[i+1][x] in self.tmp[i]:
                                                self.tmp[i].append(self.tmp[i+1][x])

                                        del self.tmp[i+1][x]

                for i in range(len(self.tmp)-1):
                        if len(self.tmp[i+1])<len(self.tmp[i]):
                                self.tmp[i+1],self.tmp[i]=self.tmp[i],self.tmp[i+1]
                
               
                '''конструкции с двумя одинаковывыми первыми словами объединяем'''
                temp=[]
                for i in range(len(self.tmp)):
                        for k in range(i+1,len(self.tmp)):
                                if len(self.tmp[i])>1 and type(self.tmp[i])==list and len(self.tmp[k])>1 and self.tmp[i][0]==self.tmp[k][0] and self.tmp[i][1]==self.tmp[k][1]:
                                        for m in range(1,len(self.tmp[k])):
                                                self.tmp[i].append(self.tmp[k][m])

                                        self.tmp[k]=[]
                                else:
                                        break
                

                
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if self.tmp[i][j] in d5 and j!=0:
                                        if self.tmp[i][0] in d5:
                                                del self.tmp[i][0]

                
                self.tmp=self.canonizer_one(self.tmp,d5)
               
                '''удаляем пустые и дубли в конструкциях'''
                self.clean()
              
                for i in range(len(self.tmp)):
                        if type(self.tmp[i])==list:
                                self.tmp[i]=self.del_dupls(self.tmp[i])

                
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if "exists" in self.tmp[i][j] and len(self.tmp[i])>2:
                                        if j<len(self.tmp[i])-1:
                                                self.tmp.append([self.tmp[i][j],self.tmp[i][j+1]])
                                                del self.tmp[i][j]

              
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                for x in self.label_list:
                                        if self.tmp[i][j]==x[0]: ##есть название объекта (функция, точка)
                                                if j<len(self.tmp[i])-1 and self.tmp[i][j+1]==x[1]: ##есть и обозначение данного объекта
                                                      if not self.tmp[i] in self.label_list: ##эта не пара название и обозначение
                                                            del self.tmp[i][j]

                                                if not x[1] in self.tmp[i]:
                                                        self.tmp[i][j]=x[1]

                
                for i in range(len(self.tmp)):
                        if i<len(self.tmp)-1 and len(self.tmp[i])>len(self.tmp[i+1]) and type(self.tmp[i])==list and type(self.tmp[i+1])==list:
                                self.tmp[i],self.tmp[i+1]=self.tmp[i+1],self.tmp[i]

                
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if j<len(self.tmp[i])-1:
                                        if self.tmp[i][j]=='не':
                                                del self.tmp[i][j]
                                                self.tmp[i]=["negation",self.tmp[i]]

                
                for x in range(len(self.tmp)):
                        for y in range(len(self.tmp)):
                                if x!=y and type(self.tmp[x])==list and type(self.tmp[y])==list:
                                        if len(self.tmp[x])>0 and len(self.tmp[y])>0 and self.tmp[x][0]==self.tmp[y][0]:
                                                for m in range(len(self.tmp[y])):
                                                        if not self.tmp[y][m] in self.tmp[x]:
                                                                self.tmp[x].append(self.tmp[y][m])
                                                self.tmp[y]=[]

                for i in range(len(self.tmp)):
                        for j in range(len(self.tmp[i])):
                                if self.tmp[i][j]=="forall" and j!=0:
                                        self.tmp[i][0],self.tmp[i][j]=self.tmp[i][j],self.tmp[i][0]

                for i in range(len(self.tmp)-1,-1,-1):
                        if type(self.tmp[i])==list and len(self.tmp[i])==1:
                                del self.tmp[i]
                                
                self.clean()
                for x in self.label_list:
                        self.tmp.append(x)
                
               
                
       
        def make_pass(self,l,str1):
                for i,elem in enumerate(l):
                    if not isinstance(elem,str):
                        l[i]=self.make_pass(elem,str1)
                    else:
                            str1=str1+" "+elem
                            self.tmp.append(str1)
                

        def main(self):   
                d1=self.read_from_file("dicts/dict1","dict")
                d2=self.read_from_file("dicts/dict2","list")
                d3=self.read_from_file("dicts/dict3","dict")
                d4=self.read_from_file("dicts/dict4","list")
                d5=self.read_from_file("dicts/dict5","list")
                d6=self.read_from_file("dicts/dict6","dict_")
                self.transform(d1,d2,d3,d4,d5,d6)
                return self.tmp




