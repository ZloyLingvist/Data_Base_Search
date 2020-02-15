from utilities import *

class Text_analyzer:
    def __init__(self,a,root):
        tmp=[]
        self.a=a
        self.dict={}
        self.dict_repl={}
        self.root=root
        
        #self.replace_on_equiv()

        for i in range(len(self.a)):
            if self.a[i][3]=="0" and self.a[0][1]=="if":
                self.root=self.a[0][0]
                self.a[0][3]="0"
                self.a[i][3]="1"
        
        tmp=[]
        for x in self.a:
            for y in self.a:
                if y[3]==x[0]:
                    tmp.append(y[0])

            self.dict[x[0]]=tmp
            tmp=[]

    def replace_on_equiv(self):
        f=open("dicts/dict2.txt","r",encoding="utf-8")
        lst=[]
        for line in f:
            a=line.split('|')
            lst=a[0].split()
            for i in range(len(self.a)):
                if len(self.a[i])>1 and self.a[i][2]==lst[0]:
                    flag=1
                    t=i+1
                    for k in range(1,len(lst)):
                        if self.a[t][2]!=lst[k]:
                            flag=0
                            break
                        
                        t=t+1

                    if flag==1:
                        self.a[i][2]=a[1].strip()
                        self.a[i][1]=a[1].strip()

                        ##############
                        if self.a[i][4]=="AgreedAttribute\n":
                            for k in range(i+1,len(self.a)):
                                if self.a[i][3]==self.a[k][0]:
                                    self.a[i][4]=self.a[k][4]
                                    self.a[i][3]=self.a[k][3]
                                    break

                        ##############
                        
                        t=i+1
                        for k in range(len(lst)-1):
                            self.a[t][2]="delete"
                            self.a[t][1]="delete"
                            t=t+1

        f.close()
        
        f=open("dicts/dict1.txt","r",encoding="utf-8")
        for line in f:
            a=line.split('\t')
            self.dict_repl[a[0]]=[a[1],a[2].strip('\n')]
        f.close()

        for i in range(len(self.a)):
            if len(self.a[i])>1 and self.a[i][2]=="быть":
                self.a[i][1]="is"
                self.a[i][2]="is"
                
            for x in self.dict_repl:
                if len(self.a[i])>1 and self.a[i][2]==x:
                    if self.dict_repl[x][1]=="r":
                        self.a[i][2]=self.dict_repl[x][0]
                        self.a[i][1]=self.dict_repl[x][0]

                    if self.dict_repl[x][1]=="d":
                        self.a[i][2]="delete"
                        self.a[i][1]="delete"

                    if self.dict_repl[x][1]=="rd":
                        if i<len(self.a)-1:
                            for k in range(i,len(self.a)):
                                if len(self.a[k])>5 and self.a[k][4]==self.a[i][0] and self.a[k][4].strip('\n')=="NonAgreedAttribute":
                                    self.a[i][1]=self.a[k][2]
                                    self.a[i][2]=self.a[k][2]
                                    self.a[k][2]="delete"
                                    self.a[k][1]="delete"

       
        
    def dfs(self,graph,node,visited):
        if node not in visited:
            visited.append([node,graph[node]])
            for n in graph[node]:
                self.dfs(graph,n,visited)

    def recreate(self,l):
        for i,elem in enumerate(l):
            if not isinstance(elem,str):
                l[i]=self.recreate(elem)
            else:
                l[i]=self.a[int(l[i])-1][2]

        return l

    def modifier(self,l,label_list):
        del_words=['delete',' ,','такой','условие','is','что']
        for i,elem in enumerate(l):
            if not isinstance(elem,str):                
                for k in range(len(elem)-1,-1,-1):
                    if elem[k]==['delete'] or elem[k]==[' ,'] or elem==[' .'] or elem==['.']:
                        del elem[k]

                for k in range(len(elem)-1,-1,-1):
                    if elem[k] in del_words :
                        del elem[k]
                    
                l[i]=self.modifier(elem,label_list)
            
        return l

    def clean(self,l):
        for i,elem in enumerate(l):
            if not isinstance(elem,str):
                if len(elem)==1:
                    elem=elem[0]
                    
                if len(elem)==2:
                    if elem[1]==[[]]:
                        elem=elem[0]
                    
                for k in range(len(elem)-1,-1,-1):
                    if elem[k]==[]:
                        del elem[k]

                l[i]=self.clean(elem)

        return l
              
    

    def make_tree(self):
        visited=[]
        self.dfs(self.dict,self.root,visited)
        
        for i in reversed(range(len(visited))):
            for j in reversed(range(len(visited))):
                if visited[i][0] in visited[j][1]:
                    for k in range(len(visited[j][1])):
                        if visited[i][0]==visited[j][1][k]:
                            if visited[i][1]==[]:
                                visited[j][1][k]=visited[i][0]
                            else:
                                visited[j][1][k]=visited[i]

                            break

                    continue

        visited=visited[0]
        visited=self.recreate(visited)

        dict1=[]
        for x in self.a:
            if x[4].strip()=="NonAgreedAttribute":
                dict1.append(x[1])
    
        #self.modifier(visited,dict1)
        #self.clean(visited)
        return visited
'''
a=read_from_file("Temp/in")
A=Text_analyzer(a[1],a[0])
r=A.make_tree()
print(r)
'''
    
