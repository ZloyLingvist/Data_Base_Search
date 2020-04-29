from formula_tree import *

def preprocessing(text,path):
    f=open(path+"\\Files\\config.ini","r",encoding="utf-8")
    for line in f:
        line=line.split(':')
        if line[0]=="Formulas_razbor":
                lst_=line[1].strip()
                break
    f.close()

    ######## считываем из базы формул #####
    lst_gl=[]
    f=open(path+"\\Files\\formulas_.txt","r",encoding="utf-8")
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
                str1=str1+text[i]
             
            if match>0:
                str1=str1+text[i]
           
            if match==0:
                if text[i]!="}":
                    str2=str2+text[i]

                if str1!="":
                    if not str1 in lst_gl:
                        lst.append(str1)
                        lst=list(set(lst))
                        str2=str2+"formula_"+str(len(lst)+len(lst_gl))
                    else:
                        for k in range(len(lst_gl)):
                            if lst_gl[k]==str1:
                                str2=str2+"formula_"+str(k+1)
                str1=""

    f=open(path+"\\Files\\formulas_.txt","a",encoding="utf-8")
    for i in range(len(lst)):
            f.write(lst[i]+'\n')
    f.close()

    A=Formula_Tree()
    f=open(path+"\\Files\\"+lst_,"a",encoding="utf-8")
    for i in range(len(lst)):
        try:
            f.write(str(A.main(lst[i]))+'\n')
        except:
            f.write(str([lst[i]])+'\n')

    f.close()
        
    return str2

def combine_formula_and_text_f(l,fl):
    for i,elem in enumerate(l):
        if not isinstance(elem,str):
            l[i]=combine_formula_and_text_f(elem,fl)
        else:
            if "formula" in l[i]:
                t=int(l[i].split("_")[1])-1
                l[i]=fl[t]
          
    return l

def combine_formula_and_text_modify(l):
    for i,elem in enumerate(l):
        if not isinstance(elem,str):
            if len(elem)==2:
                if type(elem[0])==str and type(elem[1])==list:
                    if elem[0] in elem[1][0]:
                        elem[1][0]=elem[0]
                        elem=elem[1]
                    
            l[i]=combine_formula_and_text_modify(elem)
        
    return l

def combine_formula_and_text(formula,path):
    f=open(path+"\\Files\\config.ini","r",encoding="utf-8")
    for line in f:
        line=line.split(':')
        if line[0]=="Formulas_razbor":
                lst_=line[1].strip()
                break
    f.close()
    
    ######## считываем из базы формул #####
    lst_gl=[]
    f=open(path+"\\Files\\"+lst_,"r",encoding="utf-8")
    for line_ in f:
        if len(line_.strip())>0:
            try:
                lst_gl.append(eval(line_.strip()))
            except:
                lst_gl.append([line_.strip()])
    f.close()

    r=combine_formula_and_text_f(formula,lst_gl)
    r=combine_formula_and_text_modify(r)
    return r



