from collections import Counter

def calc_similarity(mydict,mydict2):
    a,b=[],[]
  
    for x in mydict:
        a.append(x)

    for y in mydict2:
        b.append(y)
        
    A=set(a)
    B=set(b)
    C=sorted(list(A|B))

    v1,v2,mx,mn=0,0,0,0

    for k in C:
        if not k and mydict:
            v1=0
        if not k in mydict2:
            v2=0
        if k in mydict:
            v1=float(mydict[k])
        if k in mydict2:
            v2=float(mydict2[k])
        
        mx=mx+max(v1, v2)
        mn=mn+min(v1,v2)

    return mn/mx

def subformulas(l,res_list):
     for i,elem in enumerate(l):
         if not isinstance(elem,str):
             res_list.append(elem)
             l[i]=subformulas(elem,res_list)

     return l
 
def make_(l,tmp):
    for i,elem in enumerate(l):
         if not isinstance(elem,str):
            l[i]=make_(elem,tmp)
         else:
             tmp.append(elem)
           
    return l

def generate_dict(a,mydict):
    temp=[]
    tmp=[]
    res=[]
    temp_gl=[]
    subformulas(a,tmp)

    for x in tmp:
        make_(x,temp)
        for y in temp:
            temp_gl.append(y)

        temp=[]

    p1=Counter(temp_gl).keys()
    p2=Counter(temp_gl).values()

    for x,y in zip(p1,p2):
        if x in mydict:
            mydict[x]=mydict[x]+y/(mydict[x]+1)
        else:
            mydict[x]=y

    return mydict

def calc_weight(a,mydict):
    dict_for_theorem={}
    temp=[]
    temp_gl=[]
    tmp=[]
    res=[]
    subformulas(a,tmp)

    for x in tmp:
        make_(x,temp)
        for y in temp:
            temp_gl.append(y)

        temp=[]
    
    for x in temp_gl:
        if x in mydict:
             dict_for_theorem[x]=1/mydict[x]
        else:
             dict_for_theorem[x]=1

    return dict_for_theorem
            



