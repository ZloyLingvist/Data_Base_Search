def jaccard_coeff_algo_three(tmp1,tmp2):
        S1=set(i for i in tmp1)
        S2=set(i for i in tmp2)
        intersection = len(list(S1.intersection(S2)))
        union = (len(S1) + len(S2)) - intersection
        if union!=0:
            res=float(intersection) / union
        else:
            res=0

        return res
            
def path_to_leaves_algo_three(l,tmp,str1):
        for i,elem in enumerate(l):
            if not isinstance(elem,str):         
                l[i]=path_to_leaves_algo_three(elem,tmp,str1)
            else:
                if str1=="":
                    str1=elem
                else:
                    str1=str1+' '+elem
                tmp.append(str1)
                
        return l
    
def simplifier_algo_three(a):
        str1=""
        tmp=[]
        path_to_leaves_algo_three(a,tmp,str1)
        temp=[]
        dict1={}
        for x in tmp:
            temp.append(x.split(' '))

        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if len(temp[i][j])==1:
                    if temp[i][j] in dict1.keys():
                        temp[i][j]=dict1[temp[i][j]]

        return temp

def algorithm_three_func(a,b):
    value=0
    ind=[]
    i,j=0,0
    coeff=1
    a=simplifier_algo_three(a)
    b=simplifier_algo_three(b)
    
    for x in a:
        i=i+1
        coeff=1
        for m in range(len(b)):
            if x==b[m]:
                coeff=coeff+1
        
        for y in b:
            j=j+1
            c=jaccard_coeff_algo_three(x,y)
            value=value+coeff*(c*i/len(a))

    return value         
            
