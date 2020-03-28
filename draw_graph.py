import pydotplus as ptp
import os

path = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] += os.pathsep + path+'/bin/'

class plot_tree:
    def __init__(self,a,name,text):
        self.a=a
        self.str=""
        self.table=[]
        self.name=name
        self.text=text
       
        
    def make_pass(self,l,tmp,str1):
        for i,elem in enumerate(l):
            if not isinstance(elem,str):
                l[i]=self.make_pass(elem,tmp,str1)
            else:
                str1=str1+" "+elem
                tmp.append(str1)

    def modify_pass(self,l):
        for i,elem in enumerate(l):
            if not isinstance(elem,str):
                flag=1
                for k in range(len(elem)):
                    if type(elem[k])!=str:
                        flag=0
                        break
                    
                if flag==1:
                    for k in range(1,len(elem)):
                        elem[k]=[elem[k]]
                        
                l[i]=self.modify_pass(elem)

        return l
            

    def make_table(self):
        tmp=[]
        str1=""
        self.a=self.modify_pass(self.a)
        self.make_pass(self.a,tmp,str1)
        
        for i in range(len(tmp)):
            temp=tmp[i].split()
            temp.reverse()
            if i==0:
                self.str=[str(i+1),temp[0],temp[0],"0"]
                root=temp[0]
            else:
                if len(temp)>1:
                    self.str=[str(i+1),temp[0],temp[1],"_"]
                else:
                    self.str=[str(i+1),temp[0],root,"_"]

            self.table.append(self.str)

        for i in range(len(self.table)):
            for j in range(i,0,-1):
                if self.table[i][2]==self.table[j][1]:
                    self.table[i][3]=self.table[j][0]
                    break
                
        for i in range(len(self.table)):
            if self.table[i][3]=="_":
                self.table[i][3]="1"

                
    def main(self,mode):
        if mode=="formula":
            self.make_table()
        if mode=="syntax_tree":
            self.table=self.a
            
        graph = ptp.Dot(graph_name="syntax_tree",graph_type='digraph',label="\n"+self.text)
        graph.set_node_defaults(color='black', shape='box')

     
        for i in range(len(self.table)):
            if self.table[i][1]=="," or self.table[i][1]==".":
                self.table[i][1]=" "+self.table[i][1]

            id_1=str(self.table[i][0])

            if i<len(self.table)-1:
                id_2=str(self.table[i+1][0])

            line=str(self.table[i][1])

            node=ptp.Node(id_1,label=line,fillcolor="white",style="filled")
            graph.add_node(node)

            if i<len(self.table)-1:
                if self.table[i+1][1]=="," or self.table[i+1][1]==".":
                    self.table[i+1][1]=" "+self.table[i+1][1]
                
                graph.add_node(ptp.Node(id_2,label=str(self.table[i+1][1]),style="dashed"))

        for i in range(len(self.table)):
            id_1=str(self.table[i][0])
            id_2=str(self.table[i][3])

            if (self.table[i][3]!=str(0)):
                edge=ptp.Edge(id_2,id_1)
                graph.add_edge(edge)

        graph.write_png(path+"\\Trees\\"+self.name+".png")

