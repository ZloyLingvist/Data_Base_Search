import re

def check(elem):
    mathop=["+","/","*","-","<",">","\\leq","\\geq",'!','<=>']
    func=["\\int","\\sum","\\lim","\\abs","\\frac"]
    pr=['forall','exists','then','if','<=>']
    if elem in pr or elem in mathop or elem in func or (len(elem)==1 and bool(re.search('[а-яА-Я]',elem)==False)):
        return False
    return True

def path_to_leaves(l,tmp,str1):
    for i,elem in enumerate(l):
        if not isinstance(elem,str):         
            l[i]=path_to_leaves(elem,tmp,str1)
        else:
            if str1=="":
                str1=elem
            else:
                str1=str1+' '+elem
            tmp.append(str1)
                
    return l

def simplifier(a):
    str1=""
    tmp=[]
    path_to_leaves(a,tmp,str1)
    temp=[]
    for x in tmp:
        temp.append(x.split(' '))

    return temp

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
        
        mx=mx+max(v1,v2)
        mn=mn+min(v1,v2)

    return mn/mx

def make_dict(a,mydict):
    t=simplifier(a)
    for i in range(len(t)):
        for j in range(len(t[i])):
            if not t[i][j] in mydict:
                if check(t[i][j])==True:
                    mydict[t[i][j]]=2.0
            else:
                mydict[t[i][j]]=mydict[t[i][j]]+0.5**mydict[t[i][j]]

        '''
        if not " ".join(t[i]) in mydict:
            mydict[" ".join(t[i])]=1
        else:
            summ=0
            for k in range(len(t[i])):
                if t[i][k] in mydict:
                    summ=summ+mydict[t[i][k]]
                
            mydict[" ".join(t[i])]=0.5**(summ)
        '''
      
    return mydict

def calc_weight(t,mydict):
    dict_for_formula={}
    for i in range(len(t)):
        for j in range(len(t[i])):
            if bool(re.search('[а-яА-Я]',t[i][j]))==True:
                if t[i][j] in mydict:
                    if mydict[t[i][j]]==1.0 or mydict[t[i][j]]<0.25:
                        continue
            if not t[i][j] in mydict:
                dict_for_formula[t[i][j]]=2.0
            else:
                dict_for_formula[t[i][j]]=1/mydict[t[i][j]]

        '''
        if not " ".join(t[i]) in mydict:
            dict_for_formula[" ".join(t[i])]=2.0
        else:
            dict_for_formula[" ".join(t[i])]=1/mydict[" ".join(t[i])]
        '''
        
    return dict_for_formula


def hybrid_main(a,b,mydict):
    A=simplifier(a)
    B=simplifier(b)

    Aw=calc_weight(A,mydict)
    Bw=calc_weight(B,mydict)

    T=calc_similarity(Aw,Bw)
    return T

'''
mydict={}   

a=['if', [['C', [['function', [[['f', ['x']]]]], ['segment', [[[['a'], ['b']]]]], ['Dif', [['segment', [[[['a'], ['b']]]]]]]]], ['then', [['Decrease', [[['f', ['x']]], ['segment', [[[['a'], ['b']]]]]]], ['<=>', [['=>']]], ['forall', [[['\\in', 'x', [['a'], ['b']]]], [['\\leq', [['f', '^', ['\\prime']], '0']]]]]]]]]
b=['if', [['forall', [['less', [['point', [['segment']]], ['derivative', [[['g']]]], ['zero']]], ['then', [['Decrease', [['function', [[['g']]]], ['segment']]]]]]]]]

mydict=make_dict(a,mydict)
mydict=make_dict(b,mydict)

r=hybrid_main(a,b,mydict)
print(r)
'''
