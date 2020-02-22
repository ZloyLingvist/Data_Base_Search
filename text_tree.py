from utilities import *
from draw_graph import *
from text_predicator import *

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
                l[i]=self.a[int(l[i])-1][2]
                
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

                            break

                    continue
        
        visited=visited[0]
        visited=self.recreate(visited)
        dict1=[]
        for x in self.a:
            if x[4].strip()=="NonAgreedAttribute":
                dict1.append(x[1])

        #A=Text_predicator(visited,self.a)
        #visited=A.main()       
        return visited

'''
a=read_from_file("in")
A=Text_analyzer(a[0][0],a[0][1])
e=A.make_tree()
print(e)
'''