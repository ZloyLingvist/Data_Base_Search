#from draw_graph import *
from ranger import *

def draw_tree(lst,txt):
    for i in range(len(lst)):
        A=plot_tree(lst[i],"pic_"+str(i+1),txt[i])
        A.main("formula")

def make_ranger(query_id,lst,txt):
    A=Ranger()
    res=[]
    for i in range(len(lst)):
        res_num=A.main(lst[query_id],lst[i],2)
        res.append([res_num,lst[i],txt[i],i])

    res.sort(key = lambda x: x[0],reverse=True)
    return res
            
f=open("list.txt","r",encoding="utf-8")
lst=[]
txt=[]
for line in f:
    line=line.strip()
    if len(line)>0:
        lst.append(eval(line))

f.close()

f=open("text.txt","r",encoding="utf-8")
for line in f:
    line=line.strip()
    if len(line)>0:
        txt.append(line)

f.close()

query_num=8
res=make_ranger(query_num,lst,txt)
print('Query:',txt[query_num],'\n')
for i in range(len(res)):
    print(res[i][0],res[i][3])
    print(res[i][1])


#draw_tree(lst,txt)
