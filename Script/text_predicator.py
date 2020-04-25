import os

parent_directory=os.path.dirname(os.path.dirname(__file__))
dict_path=parent_directory+"\\Files\\"

def checking(str1):
        str1=str1.split()
        a=['del']
        
        if len(str1)==1:
                if str1!='if' and str1!="then":
                        return False

        return True

class Text_predicator:
        def __init__(self):
               self.tmp=[]
               self.bad_construction=["на::case","в::case"]
               self.obj_list=[]
               ''' считаем список опорных слов (функция, точка)'''
               f=open(dict_path+"dicts/obj.txt","r",encoding="utf-8")
               for line in f:
                       line=line.split('\t')
                       for x in line:
                               self.obj_list.append(x.strip())

               f.close()

        def del_duplicates(self,tmp,mode):
                for i in range(len(tmp)-1,-1,-1):
                         for j in range(len(tmp[i])-1,-1,-1):
                                 for k in range(len(tmp[i])-1,-1,-1):
                                         if j!=k:
                                                 if mode==0:
                                                         if tmp[i][j]==tmp[i][k]:
                                                                 del tmp[i][k]
                                                         
                return tmp

        ''' Этап 1 '''
        
        def make_pass(self,l,str1):
                ''' рекурсивно обходим дерево - строим пути из вершины к листьям. В случае, неправильных листьев их не берем'''
                for i,elem in enumerate(l):
                    if not isinstance(elem,str):
                        l[i]=self.make_pass(elem,str1)
                    else:
                            if "del" in elem or elem in self.bad_construction:
                                    continue
                                
                            str1=str1+" "+elem
                            if checking(str1)==True:
                                    self.tmp.append(str1)

                return l


        def check_subset(self):
                '''если ветвь полностью содержится в соседней, то ее можно убрать'''
                for i in range(len(self.tmp)-1,-1,-1):
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

                for i in range(len(self.tmp)):
                        self.tmp[i]=self.tmp[i].split()


        def make_construction(self):
                '''сочетания объект+определение,объект+обозначение добавляем в конец разбора'''
                for i in range(len(self.tmp)-1,-1,-1):
                       for j in range(len(self.tmp[i])-1,-1,-1):
                               if self.tmp[i][j].split("::")[0] in self.obj_list:
                                       if j<len(self.tmp[i])-1:
                                               if "amod" in self.tmp[i][j+1]:
                                                       t=self.tmp[i][j]
                                                       for k in range(len(self.tmp)):
                                                               if len(self.tmp[k])==2:
                                                                       if self.tmp[k][0]==t:
                                                                               if "flat:foreign" in self.tmp[k][1]:
                                                                                       t=self.tmp[k][1]
                                                                                       break
                                                                       
                                                       self.tmp.append([self.tmp[i][j+1],t])
                                                       
                                                       del self.tmp[i][j+1]
                                                       continue
                                                
                                               if j<len(self.tmp[i])-1 and "flat:foreign" in self.tmp[i][j+1]:
                                                       self.tmp.append([self.tmp[i][j],self.tmp[i][j+1]])
                                                       del self.tmp[i][j]

                '''костыль.'''
                for i in range(len(self.tmp)-1,-1,-1):
                        flag=0
                        if flag==1:
                                break
                        
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if "der" in self.tmp[i][j]:
                                        if j<len(self.tmp[i])-1 and "flat:foreign" in self.tmp[i][j+1]:
                                                self.tmp[i][j]=self.tmp[i][j].split("::")[0]+"@"+self.tmp[i][j+1]
                                                del self.tmp[i][j+1]
                                                flag=1
                                                break
                                                
                                        
                '''если 2 элемента разбора начинаются с одинаковой вершины и не входят в список объектов, то объединяем'''
                for i in range(len(self.tmp)-1,-1,-1):
                        if i<len(self.tmp)-1 and self.tmp[i][0]==self.tmp[i+1][0] and not self.tmp[i][0].split("::")[0] in self.obj_list:
                                for x in self.tmp[i+1]:
                                        if not x in self.tmp[i]:
                                                self.tmp[i].append(x)

                                del self.tmp[i+1]

                '''если без специального слова (if,then) строка уже встречалась в разборе, то оставляем только спец.слово. Иначе, разделяем на спец.слово и остальную часть'''
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if "then" in self.tmp[i][j] or "if" in self.tmp[i][j]:
                                        temp=self.tmp[i]
                                        x=self.tmp[i][j]
                                        del temp[j]

                                        self.tmp[i]=temp
                                        self.tmp.insert(0,[x])
                                

                for i in range(len(self.tmp)-1,-1,-1):
                        if self.tmp[i]==[]:
                                del self.tmp[i]
                                        
                '''если какое-то слово осталось без указания типа связи'''
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if not "::" in self.tmp[i][j]:
                                        if j<len(self.tmp[i])-1:
                                                self.tmp[i][j]=self.tmp[i][j]+" "+self.tmp[i][j+1]
                                                del self.tmp[i][j+1]

                '''forall'''
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if "forall" in self.tmp[i][j]:
                                        temp=[]
                                        for k in range(j+1,len(self.tmp[i])):
                                                if "flat:foreign" in self.tmp[i][k]:
                                                        temp=[self.tmp[i][j],self.tmp[i][k]]
                                                        break
                                        
                                        del self.tmp[i][j]
                                        if temp==[]:
                                                continue
                                        if len(self.tmp[0])==1:
                                                self.tmp.insert(1,temp)
                                        else:
                                                self.tmp.insert(0,temp)
                                        break


               
                                                   
        ''' Этап 2 '''
        def make_predicate(self):
                '''удаляем дупликаты'''
                self.del_duplicates(self.tmp,0)

                for i in range(len(self.tmp)-1,-1,-1):
                        if type(self.tmp[i])==list:
                                if type(self.tmp[i][0])==list:
                                        self.tmp[i]=self.tmp[i][0]
                                        
                       
                for i in range(len(self.tmp)-1,-1,-1):
                        '''все, что содержит второй аргумент exists (forall) - в одну группу'''
                        if "exists" in self.tmp[i][0] or "forall" in self.tmp[i][0]:
                                temp=[]
                                for j in range(len(self.tmp)-1,i,-1):
                                        if self.tmp[i][1] in self.tmp[j]:
                                                temp.append(self.tmp[j])
                                                del self.tmp[j]
                                        else:
                                                if "obl" in self.tmp[j][0] or "amod" in self.tmp[j][0]:
                                                         temp.append(self.tmp[j])
                                                         del self.tmp[j]
                                                         
                                if len(temp)>1:
                                        temp=self.del_duplicates(temp,1)
                                        ##объединение по первому слову
                                        for j in range(len(temp)-1,-1,-1):
                                                '''если слово'''
                                                for k in range(len(temp[j])-1,-1,-1):
                                                       if k>1 and "obl" in temp[j][k] and "flat:foreign" in temp[j][k+1]:
                                                               del temp[j][k]
                                                        
                                                if j<len(temp)-1 and temp[j][0]==temp[j+1][0]:
                                                        for x in temp[j+1]:
                                                                temp[j].append(x)

                                                        del temp[j+1]
                                                
                                        temp=["&"]+temp

                                if temp!=[]:
                                        if len(temp)==1:
                                                temp=temp[0]
                                        self.tmp[i].append(temp)

                                '''если конструкция н-р состоит только из forall и имени параметр'''
                                if len(self.tmp[i])==2:
                                        if "flat:foreign" in self.tmp[i][1]:
                                                temp=self.tmp[i][1]
                                                self.tmp[i]=self.tmp[i][0]
                                                self.tmp.insert(i+1,temp)
                                              
                                                        
                                

                        if "then" in self.tmp[i][0]:
                                temp=self.tmp[i+1:]
                                del self.tmp[i+1:]
                                if len(temp)==1:
                                        temp=temp[0]
                                else:
                                        for j in range(len(temp)-1,-1,-1):
                                                if temp[j] in self.tmp:
                                                       del temp[j]

                                        if len(temp)==1:
                                                temp=temp[0]
                                        else:
                                                temp=["&"]+temp

                                if temp!=[]:
                                        self.tmp[i].append(temp)

                        if "if" in self.tmp[i][0]:
                                for j in range(i,len(self.tmp)):
                                     if "then" in self.tmp[j][0]:
                                             break

                                temp=self.tmp[i+1:j]
                                del self.tmp[i+1:j]
                                        
                                if i<len(self.tmp)-1 and not "then" in self.tmp[i+1][0]:
                                        temp.append(self.tmp[i+1])
                                        del self.tmp[i+1]
                                        
                                if len(temp)==1:
                                        temp=temp[0]
                                else:
                                        temp=["&"]+temp
                                self.tmp[i].append(temp)

        def correction(self):
                '''исправляем ошибки, которые не могли быть исправлены ранее'''
                for i in range(len(self.tmp)-1,-1,-1):
                        for j in range(len(self.tmp[i])-1,-1,-1):
                                if 'is' in self.tmp[i][j]:
                                        del self.tmp[i][j]
                                        continue
                                
                                if '@' in self.tmp[i][j]:
                                        self.tmp[i][j]=self.tmp[i][j].split('@')
                                if 'это::nmod' in self.tmp[i][j]:
                                        if j<len(self.tmp[i])-1:
                                                for k in range(i):
                                                        if len(self.tmp[k])==2:
                                                                if self.tmp[k][0].split("::")[0]==self.tmp[i][j+1].split("::")[0]:
                                                                        self.tmp[i][j]=self.tmp[k][1]
                                                                        del self.tmp[i][j+1]
                                                                        break

                        if "equal" in self.tmp[i][0]:
                                if len(self.tmp[i])==4:
                                        self.tmp[i][3],self.tmp[i][2]=self.tmp[i][2],self.tmp[i][3]
                        
                        if "-::punct" in self.tmp[i]:
                                for j in range(len(self.tmp[i])-1,-1,-1):
                                        if "где" in self.tmp[i][j] or "-::punct" in self.tmp[i][j]:
                                                del self.tmp[i][j]

                                        self.tmp[i].insert(0,"type")

                        if "=>" in self.tmp[i][0]:
                                k=round(0.5*len(self.tmp[i]))+1
                                a=self.tmp[i][1:k]
                                b=self.tmp[i][k:]
                                if len(a)==1:
                                        a=a[0]
                                if len(b)==1:
                                        b=b[0]
                                self.tmp[i]=["=>",a,b]
                                        

                               
                                        
                                                                
                        
        ''' Вспомогательные функции '''
        def print(self):
                print(self.tmp)
        

        def simplify_result(self,l):
                for i,elem in enumerate(l):
                    if not isinstance(elem,str):
                        l[i]=self.simplify_result(elem)
                    else:
                        l[i]=elem.split("::")[0]
                    
                    
                return l

        def clean_recursive(self,l):
                for i,elem in enumerate(l):
                    if not isinstance(elem,str):
                        temp=[]
                        for x in elem:
                                if x not in temp:
                                        temp.append(x)

                        elem=temp
                        
                        '''костыль'''
                        flag=1
                        for x in elem:
                                if type(x)!=str:
                                        flag=0
                                        break
                                
                        if len(elem)>2 and flag==1:
                                for k in range(1,len(elem)):
                                        elem[k]=[elem[k]]
                                flag=0
                                
                        l[i]=self.clean_recursive(elem)
                    
                    
                return l

        
        def main(self,a):
                '''этап 1'''
                tmp_res=[]
                for x in a:
                        self.make_pass(x[0],"")
                        self.check_subset()
                        self.make_construction()
                        for y in self.tmp:
                                tmp_res.append(y)
                        self.tmp=[]

                #print('!!!',tmp_res)
                self.tmp=tmp_res
                #'''этап 2 '''
                self.correction()
                self.make_predicate()
                self.simplify_result(self.tmp)
                self.clean_recursive(self.tmp)
                #self.print()
                return self.tmp



