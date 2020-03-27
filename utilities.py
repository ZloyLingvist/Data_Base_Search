def swap_to_first(arr,sign):
    for i in range(len(arr)):
        if arr[i]==sign:
            arr[i],arr[0]=arr[0],arr[i]

    return arr

def recursion_clean(l):
    for i,elem in enumerate(l):
            if not isinstance(elem,str):
                for k in range(len(elem)-1,-1,-1):
                    if elem[k]==[]:
                        del elem[k]
                        
                l[i]=recursion_clean(elem)
    return l

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
    reserve=[]
    root=""
    f=open(infile,"r",encoding="utf-8")
    for line in f:
        if line=='\n':
            arr.append([a,root])
            a=[]
            
        tmp=line.split("\t")
        if len(tmp)>1:
            if tmp[5]=="0":
                root=tmp[0]

            if tmp[1]=="то":
                tmp[1]="тогда"
                tmp[2]="тогда"

            '''
            костыль
            '''
            if tmp[0]==tmp[5]:
                tmp[5]=str(int(tmp[5])+1)

            if tmp[2]=="он" or tmp[2]=="который":
                for i in reversed(range(len(reserve))):
                    if reserve[i][4].strip()==tmp[4] and reserve[i][6]==tmp[6]:
                        tmp[2]=reserve[i][2]
                        tmp[1]=reserve[i][1]
                        break
    
            reserve.append(tmp)
            a.append([tmp[0],tmp[1],tmp[2],tmp[5],tmp[6],tmp[3]])

    f.close()

    '''
    костыль
    '''
    for i in range(len(a)):
        if a[i][2]=="этот":
            if i<len(a)-1:
                for k in reversed(range(len(a))):
                    if a[k][2]==a[i+1][2]:
                        t=k
                        flag=1
                        for m in range(len(a)):
                            if "NonAgreedAttribute" in a[m][4] and a[m][3]==a[k][0]:
                                a[i][2]=a[m][2]
                                a[i][1]=a[m][1]
                                flag=0
                                break

                        if flag==0:
                            break
            
    if len(a)>0:
        arr.append([a,root])
    return arr

def make_predicate_form(l,tmp,str1,flag,word):
    for i,elem in enumerate(l):
            if i==0:
                tmp.append("(")
                
            if not isinstance(elem,str):
                if str1=="":
                    c=1
                    for x in elem:
                        if type(x)!=str:
                            c=0
                            break

                    if c==1:
                        flag=1
                        word=elem[-1]
                    
                str1=""
                l[i]=make_predicate_form(elem,tmp,str1,flag,word)
            else:
                str1=str1+" "+elem
                if str1.count(" ")>1 and flag==0:
                    tmp.append(",")
                if str1.count(" ")>1 and flag!=0:
                    tmp.append("(")
                    flag=0

                tmp.append(elem)

                if elem==word:
                    tmp.append(")")
                    word=""
                    
    tmp.append(")")
    return tmp

def make_predicate_form_main(a):
    str1=""
    tmp=[]
    a=make_predicate_form(a,tmp,"",0,"")
    str2=""
    a=" ".join(a)
    a=a.replace(") (","),(")
    return a


