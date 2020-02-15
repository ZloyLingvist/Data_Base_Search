def swap_to_first(arr,sign):
    for i in range(len(arr)):
        if arr[i]==sign:
            arr[i],arr[0]=arr[0],arr[i]

    return arr

def swap_(arr,ast):
    for i in range(len(ast)):
        if type(ast[i]) is str:
            ast[i]=ast[i].strip()

    for j in range(len(ast)):
        if ast[j] in arr:
            ast[j],ast[0]=ast[0],ast[j]

    return ast

def clean_from_empty(ast):
    for i in range(len(ast)-1,-1,-1):
        if ast[i]==[]:
            del ast[i]

    return ast
                

def equalizer(ast,start):
    for i in range(start,len(ast)):
        if type(ast[i])==str:
            ast[i]=[ast[i]]

    return ast

def modifier_integral_summ(ast):
    for i in range(len(ast)):
            if i<len(ast)-1 and ast[i]=="_":
                ast[i]=[ast[i],ast[i+1]]
                ast[i+1]=[]
                
            if i<len(ast)-1 and ast[i]=="^":
                ast[i]=[ast[i],ast[i+1]]
                ast[i+1]=[]

    ast=clean_from_empty(ast)
    return ast


def read_from_file(infile):
    a=[]
    arr=[]
    root=""
    f=open(infile+".txt","r",encoding="utf-8")
    for line in f:
        if line=='\n':
            arr.append([a,root])
            a=[]
            
        tmp=line.split("\t")
        if len(tmp)>1:
            if tmp[5]=="0":
                root=tmp[0]

            '''
            костыль
            '''
            if tmp[0]==tmp[5]:
                tmp[5]=str(int(tmp[5])+1)
                
            a.append([tmp[0],tmp[1],tmp[2],tmp[5],tmp[6]])

    f.close()
    if len(a)>0:
        arr.append([a,root])
    return arr

