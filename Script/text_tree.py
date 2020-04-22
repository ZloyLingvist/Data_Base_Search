def recursion_clean(l):
    for i,elem in enumerate(l):
            if not isinstance(elem,str):
                for k in range(len(elem)-1,-1,-1):
                    if elem[k]==[]:
                        del elem[k]
                        
                l[i]=recursion_clean(elem)
    return l

class Text_analyzer:
    def __init__(self,a,root):
        tmp=[]
        self.a=a
        self.dict={}
        self.dict_repl={}
        self.root=root
        
        tmp=[]
        for x in self.a:
            for y in self.a:
                if y[3]==x[0]:
                    tmp.append(y[0])

            self.dict[x[0]]=tmp
            tmp=[]

        
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
                try:
                    l[i]=self.a[int(l[i])-1][2]+"::"+self.a[int(l[i])-1][4]
                except:
                    0
                
        return l

    def recreate_2(self,l):
        for i,elem in enumerate(l):
            for x in elem:
                if x==['del'] or x==[]:
                    for y in range(len(elem)-1,-1,-1):
                        if elem[y]==['del'] or x==[]:
                            del elem[y]

                if x=="del":
                   for y in range(len(elem)-1,-1,-1):
                        if elem[y]=='del':
                            del elem[y]

            if not isinstance(elem,str):
                l[i]=self.recreate_2(elem)
        
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
                                visited[j][1][k]=[visited[i][0]]
                            else:
                                visited[j][1][k]=visited[i]
                    
       
        visited=visited[0]
        visited=self.recreate(visited)

        visited=self.recreate_2(visited)
        visited=recursion_clean(visited)
        
        return [visited,self.root]

