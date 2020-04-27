import os
path = os.path.dirname(os.path.dirname(__file__))

def arr_etap_one(a):
    f=open(path+"\\Files\\dicts\words_trash.txt","r",encoding="utf-8")
    words_trash=[]
    for line in f:
        line=line.strip().split()
        for x in line:
            words_trash.append(x)

    for i in range(len(a)):
        if a[i][2] in words_trash:
            a[i][2]="del"
            a[i][1]="del"

        if a[i][2]=="-":
            a[i][2]="-"
            a[i][5]="-"
          
        if a[i][2]=="и":
            if a[i][4]=="advmod":
                a[i][2]="del"
                a[i][1]="del"

            '''
            if a[i][4]=="cc":
                a[i][2]=","
                a[i][1]=","
            '''

        if a[i][4]=="flat:foreign":
            a[i][2]=a[i][1]
            
        if a[i][2]=="она":
            for k in range(i,0,-1):
                if a[k][5]=="NOUN":
                    if a[k][4]==a[i][4]:
                        a[i][2]=a[k][2]
                        a[i][1]=a[k][2]

        if a[i][2]=="это":
            if i<len(a)-1 and a[i+1][5]=="NOUN":
                for k in range(i,0,-1):
                    if a[k][2]==a[i+1][2]:
                        for p in range(k,len(a)):
                            if a[p][4]=="flat:foreign":
                                if a[p][3]==a[k][0]:
                                    a[i][2]=a[p][2]
                                    a[i][1]=a[p][1]
                                    a[i][3]=a[i+1][0]
                                    a[i][4]=a[p][4]

    return a

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
                str1=str1.strip()
               
                if str1.count(" ")>0 and flag==0:
                    if tmp[-1]!="forall" and tmp[-1]!="exists":
                        tmp.append(",")
                        
                if str1.count(" ")>1 and flag!=0:
                    tmp.append("(")
                    flag=0

                tmp.append(elem)

                if elem==word:
                    tmp.append(")")
                    word=""
                    
    tmp.append(")")
    if str1.count(" ")>0:
         tmp.append(",")
         
    return tmp

def make_simple(l):
     for i,elem in enumerate(l):
            if not isinstance(elem,str):
                 if len(elem)==1:
                     elem=elem[0]
                     
                 l[i]=make_simple(elem)

     return l

def make_predicate_form_main(a):
    str1=""
    tmp=[]
    a=make_predicate_form(a,tmp,"",0,"")
    str2=""
    a=" ".join(a)
    a=a.replace(") (","),(")
    return a

def replace_formulas(text):
        f=open("Files/config.ini","r",encoding="utf-8")
        for line in f:
            line=line.split(':')
            if line[0]=="List_of_formulas":
                lst_=line[1].strip()
                break
        f.close()
    
        ######## считываем из базы формул #####
        lst_gl=[]
        f=open(lst_,"r",encoding="utf-8")
        for line_ in f:
            lst_gl.append(line_.strip())
        f.close()
   
        lst=[]
        str1=""
        str2=""
        match=0

        for i in range(len(text)):
            if text[i]=="{":
                match=match+1

            if text[i]=="}":
                match=match-1
                
            if match>0:
                str1=str1+text[i]
           
            if match==0:
                if text[i]!="}":
                    str2=str2+text[i]

                if str1!="":
                    if not str1 in lst_gl:
                        if str1[-1]!="}":
                            str1=str1+"}"
                        lst.append(str1)
                        lst=list(set(lst))
                        str2=str2+"formula_"+str(len(lst)+len(lst_gl))
                    else:
                        for k in range(len(lst_gl)):
                            if lst_gl[k]==str1:
                                str2=str2+"formula_"+str(k+1)
                str1=""

        f=open(lst_,"a",encoding="utf-8")
        
        for i in range(len(lst)):
            f.write(lst[i]+'\n')
        f.close()
       
        return str2


