import yaml
import os

path = os.path.dirname(os.path.dirname(__file__))

def load_synonyms(file):
    try:
        data = yaml.load(open(file, 'rt', encoding='utf8'), Loader=yaml.FullLoader)
        d = {}
        for k, v in data.items():
            for x in v: d[x] = k
        return d
    except FileNotFoundError:
        return {}


def read_dict():
     words_construction=[]
     morph=[]
     trash=[]
     
     f=open(path+"\\Files\\dicts\\words_construction.txt","r",encoding="utf-8")
     for line in f:
            line=line.split('\t')
            line[4]=line[4].strip()
            words_construction.append(line)
     f.close()

     f=open(path+"\\Files\\dicts\\error_morph.txt","r",encoding="utf-8")
     for line in f:
            line=line.split('\t')
            line[1]=line[1].strip()
            morph.append(line)
     f.close()

     f=open(path+"\\Files\\dicts\\trash.txt","r",encoding="utf-8")
     for line in f:
        line=line.split('\t')
        for x in line:
            trash.append(x)
     f.close()
     
     return words_construction,morph,trash

def recount_number(num,a,mode):
    for i in range(len(a)):
        if int(a[i][0])>num:
            if mode==0:
                a[i][0]=str(int(a[i][0])-1)
            if mode==1:
                a[i][0]=str(int(a[i][0])+1)

        if int(a[i][3])>num:
            if mode==0:
                a[i][3]=str(int(a[i][3])-1)
            if mode==1:
                a[i][3]=str(int(a[i][3])+1)

    return a

def candidate_for_delete(a,k):
    a[k][2]="del"
    a[k][1]="del"
    return a[k]

def tokenize_correction(a,wc,em,ts):
    count=0
    for i in range(len(a)):
        if a[i][2].count("formula")>1:
            tmp=a[i][2].split(",")
            a[i][2]=tmp[0]
            a[i][1]=tmp[0]
            
            for k in range(1,len(tmp)):
                a.insert(i+1,[str(int(a[i][0])+1), tmp[k], tmp[k], a[i-1][3], a[i][4], a[i][5]])
                a=recount_number(i+1,a,1)
                
                    
        if a[i][2]=="(":
            count=1
            for t in range(i+1,len(a)):
                if count==0:
                    break
                if a[t][2]=="(":
                    count=count+1
                if a[t][2]==")":
                    count=count-1

            for k in range(i,t):
                a[k]=candidate_for_delete(a,k)
               
                    
        for j in range(len(ts)):
            if ts[j]==a[i][2]:
                a[i]=candidate_for_delete(a,i)
                
        if a[i][2]=="," or a[i][2]==".":
            a[i]=candidate_for_delete(a,i)
            
        if a[i][2]=="не":
            if i<len(a)-1:
                if a[i+1][5]=="VERB":
                    a[i+1][2]=a[i][2]+" "+a[i+1][2]
                    a[i+1][1]=a[i][1]+" "+a[i+1][1]
                    a[i]=candidate_for_delete(a,i)
                    
        if i<len(a)-1 and a[i][1]=="formula_" and a[i+1][1].isnumeric():
            a[i][1]=a[i][1]+a[i+1][1]
            a[i][2]=a[i][2]+a[i+1][2]
            a[i+1]=candidate_for_delete(a,i+1)

        if i<len(a)-1 and a[i][1]=="formula" and a[i+1][1][0]=="_" and a[i+1][1][1:].isnumeric():
            a[i][1]=a[i][1]+a[i+1][1]
            a[i][2]=a[i][2]+a[i+1][2]
            a[i+1]=candidate_for_delete(a,i+1)

        if i<len(a)-2 and a[i][1]=="formula" and a[i+1][1]=="_" and a[i+2][1].isnumeric():
            a[i][1]=a[i][1]+a[i+1][1]+a[i+2][1]
            a[i][2]=a[i][2]+a[i+1][2]+a[i+2][1]
            a[i+1]=candidate_for_delete(a,i+1)
            a[i+2]=candidate_for_delete(a,i+2)

        if "formula_" in a[i][1]:
            if a[i][1]!=a[i][2]:
                a[i][2]=a[i][1]

        for k in range(len(em)):
            if em[k][0]==a[i][2]:
                a[i][2]=em[k][1]

        for k in range(len(wc)):
            if wc[k][0]==a[i][2] and (wc[k][3]=="join" or wc[k][3]=="del_full"):
                tmp=a[i:i+int(wc[k][2])]
                str1=""
                for x in tmp:
                    if str1=="":
                        str1=x[2]
                    else:
                        str1=str1+" "+x[2]

                if str1==wc[k][1]:
                    if wc[k][3]=="del_full":
                        for n in range(int(wc[k][2])):
                             a[i+n]=candidate_for_delete(a,i+n)

                    if wc[k][3]=="join":
                        for n in range(int(wc[k][2])):
                            a[i+n][2],a[i+n][1]="del","del"
                            ids=int(wc[k][4])-1
                            a[i+ids][2],a[i+ids][1]=str1,str1
           
    for i in range(len(a)):
        for k in range(len(wc)):
            if wc[k][0]==a[i][2] and (wc[k][3]=="parent_children"):
                for m in range(len(a)):
                    if a[m][2]==wc[k][1] and a[m][3]==a[i][0]:
                        a[i][2]=a[i][2]+" "+a[m][2]
                        a[i][1]=a[i][1]+" "+a[m][1]
                        a[m]=candidate_for_delete(a,m)
                        
        if a[i][2]=="она":
            for k in range(i-1,0,-1):
                if "nsubj" in a[k][4]:
                    a[i][2]=a[k][2]
                    a[i][1]=a[k][1]

    if "formula" in a[i][1]:
            if "formulaz" in a[i][2]:
                a[i][2]=a[i][2].replace("formulaz","formula_")
            if "formulam" in a[i][2]:
                a[i][2]=a[i][2].replace("formulam","formula_")

            if a[i][4]!="root":
                if i>0 and a[i-1][4]=="advmod":
                    a[i][3]=a[i-1][0]
                if i<len(a)-1 and "formula" in a[i-1][1]:
                    a[i][3]=a[i+1][0]
                
    if a[i][4]=="punct":
            a[i][3]=a[i-1][0]
                   
    for i in range(len(a)-1,-1,-1):
        if a[i][1]=="del":
            a=recount_number(i,a,0)
            del a[i]

    return a
    
def syntax_correction(a):
    for i in range(len(a)):
        if (a[i][2]=="определить" or a[i][2]=="дифференцировать") and a[i][3]!="0":
            for t in range(i-1,0,-1):
                if a[t][5]=="NOUN":
                    a[i][3]=a[t][0]
                     
        if i<len(a)-1 and a[i][2]=="этот":
            for k in range(i-1,0,-1):
                if a[k][2]==a[i+1][2]:
                    flag=1
                    for m in range(k,len(a)):
                        if a[m][3]==a[k][0]:
                            if "formula" in a[m][2]:
                                a[i][2]=a[m][2]
                                a[i][1]=a[m][2]
                                flag=0
                                break
                            
                    if flag==0:
                        break
                            
        

    return a



def word_with_synonyms(a,synonyms):
    for i in range(len(a)):
        if a[i][2] in synonyms:
            a[i][2]=synonyms[a[i][2]]
            a[i][1]=a[i][2]
            
    return a


path = os.path.dirname(os.path.dirname(__file__))

def read_formulas_():
    formula_list=[]
    razbor_list=[]
    
    f=open(path+"\\Temp\\formulas_.txt","r",encoding="utf-8")
    for line in f:
        formula_list.append(line.strip())  
    f.close()

    f=open(path+"\\Temp\\formulas_razbor.txt","r",encoding="utf-8")
    for line in f:
        razbor_list.append(eval(line.strip()))  
    f.close()

    return formula_list,razbor_list
    

def dfs(visited,graph,node,temp):
    if node not in visited:
        visited.add(node)
        temp.append([node,graph[node]])
        for neighbour in graph[node]:
            dfs(visited,graph,neighbour,temp)

def recreate(l,a):
    for i,elem in enumerate(l):
        if not isinstance(elem,str):
            l[i]=recreate(elem,a)
        else:
            try:
                l[i]=str(a[int(elem)-1][2])
            except:
                0
       
    return l

def insert_formula(l,rl):
    for i,elem in enumerate(l):
        if not isinstance(elem,str):
            l[i]=insert_formula(elem,rl)
        else:
            if "formula" in elem:
                if not '-' in elem:
                    idx=int(elem.split("_")[1])-1
                    l[i]=rl[idx]
                else:
                    st=elem.split("-")
                    idx=int(st[0].strip().split("_")[1])-1
                    l[i]=rl[idx]
                
               
    return l


def dict_(a,rl):
    mydict={}
    visited=set()
    tmp=[]
    root='1'
    
    for i in range(len(a)):
        tmp=[]
        if a[i][3]=="0":
            root=str(a[i][0])
            
        for k in range(len(a)):
            if a[k][3]==a[i][0]:
                tmp.append(a[k][0])

        mydict[str(i+1)]=tmp

    temp=[]

    dfs(visited,mydict,root,temp)
    
    for i in reversed(range(len(temp))):
            for j in reversed(range(len(temp))):
                if temp[i][0] in temp[j][1]:
                    for k in range(len(temp[j][1])):
                        if temp[i][0]==temp[j][1][k]:
                            if temp[i][1]==[]:
                                temp[j][1][k]=[temp[i][0]]
                            else:
                                temp[j][1][k]=temp[i]
                
    temp=temp[0]
    temp=recreate(temp,a)
    insert_formula(temp,rl)
    return temp


def create_formula_str():
    infile=path+"\\Temp\\theorem_list_arr.txt"
    outfile=path+"\\Temp\\theorem_list_arr_razbor.txt"
    
    synonyms = load_synonyms(path+'\\Files\\synonyms.yml')
    wc,em,ts=read_dict()
    fl,rl=read_formulas_()
    res=[]

    f=open(infile,"r",encoding="utf-8")
    for line in f:
        a=eval(line.strip())
        a=tokenize_correction(a,wc,em,ts)
        a=syntax_correction(a)
        a=word_with_synonyms(a,synonyms)
        res.append(a)

    f.close()

    f=open(outfile,"w",encoding="utf-8")
    for i in range(len(res)):
        a=str(dict_(res[i],rl))
        f.write(str(a)+'\n')
       
    f.close()


def create_formula_arr(a):
    synonyms = load_synonyms(path+'\\Files\\synonyms.yml')
    wc,em,ts=read_dict()
    fl,rl=read_formulas_()

    a=tokenize_correction(a,wc,em,ts)
    a=syntax_correction(a)
    a=word_with_synonyms(a,synonyms)
    a=dict_(a,rl)
    return a
