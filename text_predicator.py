class Text_predicator:
        def __init__(self,tmp,full_table):
                self.temp=tmp
                self.tmp=[]
                self.str=""
                self.subj_list=[]
                self.root=""
                self.label_list=[]
               
                for i in range(len(full_table)):
                        if "NonAgreedAttribute" in full_table[i][4]:
                                num=int(full_table[i][3])-1
                                self.label_list.append([full_table[num][2],full_table[i][2]])
                                
                        if full_table[i][5]=="0":
                                self.root=full_table[i][0]
                                for j in range(len(full_table)):
                                        if full_table[i][5]==root and "Subject" in full_table[i][6]:
                                                self.subj_list.append(full_table[i][2])


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

        def transform(self,d1,d2,d3,d4,d5,d6):
                ##сделали обход
                pr_list=['в','на','к','.','по','всюду','притом','свой','и','из','одновременно']
                self.make_pass(self.temp,self.str)
                
                for i in range(len(self.label_list)):
                        for x in d1:
                                if self.label_list[i][0]==x:
                                        self.label_list[i][0]=d1[x]
                                        
                for i in range(len(self.tmp)-1,-1,-1):
                        if i<len(self.tmp)-1:
                            check=all(item in self.tmp[i+1] for item in self.tmp[i])
                            if check==True and not "если" in self.tmp[i]:
                                del self.tmp[i]
                                continue

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

                
                for i in range(len(self.tmp)-1,-1,-1):
                       if len(self.tmp[i])==1:
                               if not self.tmp[i][0] in d4 and self.tmp[i][0]!="if" and self.tmp[i][0]!="then" and self.tmp[i][0]!="<=>" and self.tmp[i][0]!="а":
                                       del self.tmp[i]
                                       
                       if "exists" in self.tmp[i] and "forall" in self.tmp[i]:
                               for j in range(len(self.tmp[i])-1,-1,-1):
                                       if self.tmp[i][j]=="exists":
                                               del self.tmp[i][j]
                                       
                       if "if" in self.tmp[i]:
                                self.tmp[i]=["if"]
                        
                       if len(self.tmp[i])==2 and self.tmp[i][1] in d4:
                               self.tmp[i]=[self.tmp[i][1]]

                       if "then" in self.tmp[i]:
                                self.tmp[i]=["then"]
                                
                      
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if self.tmp[i][j] in pr_list:
                                        del self.tmp[i][j]                
               
                ## добавление недостающих обозначений
                for x in self.tmp:
                        for y in d3:
                                if x==[y]:
                                        x.append(d3[y])

                for i in range(len(self.tmp)-1,-1,-1):
                        if i<len(self.tmp)-1:
                            check=all(item in self.tmp[i+1] for item in self.tmp[i])
                            if check==True:
                                del self.tmp[i]

                for i in range(len(self.tmp)):
                        for j in range(len(self.tmp[i])):
                                if self.tmp[i][j] in d5 or self.tmp[i][j]=="forall":
                                        self.tmp[i][0],self.tmp[i][j]=self.tmp[i][j],self.tmp[i][0]
                                        
                
               
                for i in range(len(self.tmp)):
                        for j in range(len(self.tmp[i])):
                                if len(self.tmp[i])>0 and self.tmp[i][j] in d4:
                                        if j<len(self.tmp[i])-1:
                                                temp=[self.tmp[i][j],self.tmp[i][j+1]]
                                                if not temp in self.tmp and temp in self.label_list:
                                                        self.tmp.insert(i,temp)
                                                        break
                
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                for x in self.label_list:
                                        if len(self.tmp[i])>0 and self.tmp[i][j] in x[0] and self.tmp[i][j] in x[1] and not self.tmp[i] in self.label_list:
                                                del self.tmp[i][j]
                                                
                                        
                                        if len(self.tmp[i])>0 and self.tmp[i][j] in x[0] and not x[1] in self.tmp[i] and not self.tmp[i] in self.label_list:
                                                self.tmp[i][j]=x[1]
                '''
                for i in range(len(self.tmp)):
                        if len(self.tmp)==1:
                                continue
                        for j in range(i+1,len(self.tmp)):
                                if len(self.tmp[i])>0 and len(self.tmp[j])>0 and self.tmp[i][0]==self.tmp[j][0]:
                                        for k in range(len(self.tmp[j])):
                                                self.tmp[i].append(self.tmp[j][k])

                                        self.tmp[i]=list(set(self.tmp[i]))
                                        self.tmp[j]=[]
                '''

                lst=['lim']
                for i in range(len(self.tmp)):
                        for j in range(len(self.tmp[i])):
                                if self.tmp[i][j] in d4 or self.tmp[i][j] in lst:
                                        if self.tmp[i][0] in d5:
                                                self.tmp[i][1],self.tmp[i][j]=self.tmp[i][j],self.tmp[i][1]
                                        else:
                                                self.tmp[i][0],self.tmp[i][j]=self.tmp[i][j],self.tmp[i][0]
                temp=[]
                for i in range(len(self.tmp)-1,-1,-1):
                        if len(self.tmp[i])>0 and (self.tmp[i][0]=="forall"):
                                t=i+1
                                while(t<len(self.tmp)):
                                        temp.append(self.tmp[t])
                                        self.tmp[t]=[]
                                        t=t+1        

                                self.tmp[i].append(temp)
                                temp=["&"]
                

                temp=["&"]
                lst=[['if','then'],['if','а'],['а'],['then','.']]
                
                for p in range(len(lst)):
                        for i in range(len(self.tmp)):
                                if len(self.tmp[i])>0 and self.tmp[i][0]==lst[p][0]:
                                    t=i+1
                                    while(t<len(self.tmp)):
                                            if len(self.tmp[t])>0 and self.tmp[t][0]!=lst[p][1]:
                                                    temp.append(self.tmp[t])
                                                    self.tmp[t]=[]
                                            else:
                                                    break
                                            t=t+1
                                            
                                    self.tmp[i].append(temp)
                                    temp=["&"]

                
                ## перестраиваем формулу
                for i in range(len(self.tmp)-1,-1,-1):
                    if self.tmp[i]==[]:
                            del self.tmp[i]
                

        def make_pass(self,l,str1):
                for i,elem in enumerate(l):
                    if not isinstance(elem,str):
                        l[i]=self.make_pass(elem,str1)
                    else:
                            if elem!=",":
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


