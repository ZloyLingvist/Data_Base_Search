from formula_tree import *
from ranger import *
from text_tree import *
from simple_ranger import *
from draw_graph import *
from utilities import *
from stamford import *
from testing_main_block import *
import sys
import os

path=os.path.dirname(os.path.dirname(__file__))
path_db=path+"\\Database\\"

def extract_formula_razbor():
    formulas_list=[]
    text_list=[]
    str1=""
    count=0

    f=open(path+"\\Database\\theorem_list.txt","r",encoding="utf-8")
    for line in f:
        text_list.append(line.strip())
    f.close()

    formulas_list=formula_list_function(text_list)
    f=open(path+"\\Files\\formulas_.txt","w",encoding="utf-8")
    
    for line in formulas_list:
        f.write(str(line)+'\n')
    f.close()

def make_formula_razbor(formulas_list):
    res=[]

    A=Formula_Tree()
    for x in formulas_list:
        if len(x)>0:
            try:
                result=A.main(x)
                res.append(result)
            except:
               res.append([x])

    return res


def make_ranking(a):
    filein=path+"/Database/theorem_list_arr_razbor.txt"
  
    f=open(filein,"r",encoding="utf-8")
    db=[]
    ranking=[]
    for line in f:
           db.append(eval(line.strip()))
    f.close()

    A=Ranger()
    ans=a
    
    for i in range(len(db)):
        try:
            c=A.main(ans,db[i],1)
            ranking.append([str(i+1),c,db[i]])
        except:
            ranking.append([str(i+1),-1,db[i]])
    
    ranking.sort(key = lambda x: x[1],reverse=True)
    return ans,ranking


def make_razbor(lst):
    '''
    если theorem - утверждение теоремы в текстовом виде (строка), то преобразуем его к таблице с синтаксическим разбором.
                 - утверждение теоремы уже в виде таблицы с синтаксическим разбором, то ничего не делаем
         представление в виде таблицы с синтаксическим разбором подаем на вход модуля преобразования на язык логики предикатов.
         затем подставляем в него разобранные формулы.
    '''
    if len(lst)>0:
        if type(lst[0])==str:
            nlp = stanza.Pipeline('ru',processors='tokenize,lemma,pos,depparse',dir=path+'\stanza_resources', package='syntagrus', use_gpu=True, pos_batch_size=3000)

    res_list=[]
    error_list=[]
    formula_list,razbor_list=read_formulas()
    formula_list_table=[]

    if len(formula_list)!=len(razbor_list):
        error_list.append(['Не совпадают размеры списка формул и списка разбора формул'])
        return [],[],error_list
   
    for i in range(len(lst)):
        try:
            if type(lst[i])==str:
                a,formula_list_table=parse_str_theorem(lst[i],nlp)
            else:
                a=lst[i]
                for k in range(len(formula_list)):
                    formula_list_table.append(["formula_"+str(k+1),formula_list[k],razbor_list[k]])

            A=Stamford()
            c=A.main(a,1)
            c=combine_formula_and_text(c,formula_list_table)
            res_list.append(c)
            formula_list_table=[]
        except:
            e_type, e_val, e_tb = sys.exc_info()
            res_list.append(['-1'])
            error_list.append(['Error in '+str(i+1)+'.'+str(e_type)+'\n'+str(e_val)])

    return lst,res_list,error_list


def make_tree(a,name,text):
    try:
        os.remove(path+"/Tree/"+name+".png")
        A=plot_tree(a,name,text)
        A.main("formula")
        return name
    except:
        return "-1"

def make_tex():
    filein=path+"/Database/theorem_list.txt"
    rd=reading_data(filein,"text")
    lst=["\\documentclass[12pt]{article}","\\usepackage[english,russian]{babel}","\\usepackage{amsmath,amssymb,amsthm,latexsym,amsfonts}",
         "\\usepackage[utf8]{inputenc}","\\usepackage[english,russian]{babel}","\\begin{document}"]

    for i in range(len(rd)):
        fl=formula_list_function([rd[i]])
        temp=rd[i]
        for j in range(len(fl)):
            if fl[j] in rd[i]:
                temp=temp.replace(fl[j],"$"+fl[j]+"$")

        rd[i]=temp
                
    f=open(path+"\\Database\\mytex.tex","w",encoding="utf-8")
    for x in lst:
         f.write(x)
         f.write('\n')

    for i in range(len(rd)):
        f.write(str(i+1)+'. '+rd[i]+"\\\\")
        f.write('\n\n')

    f.write("\\end{document}")
    f.close()

        
def make_database():
     temp=[]
     generate_label_list()
     make_tex()
     filein=path+"/Database/theorem_list.txt"
     rd=reading_data(filein,"text")

     nlp = stanza.Pipeline('ru',processors='tokenize,lemma,pos,depparse',dir=path+'\stanza_resources', package='syntagrus', use_gpu=True, pos_batch_size=3000)

     f=open(filein.split('.txt')[0]+"_arr.txt","w",encoding="utf-8")
     for i in range(len(rd)):
         a,_=parse_str_theorem(rd[i],nlp)
         temp.append(a)
         f.write(str(a)+'\n')

     f.close()

     f=open(filein.split('.txt')[0]+"_arr_syntax.txt","w",encoding="utf-8")
     A=Stamford()
     for i in range(len(temp)):
         r=A.main(temp[i],0)
         f.write(str(r)+'\n')
     f.close()
     
     f=open(filein.split('.txt')[0]+"_arr_razbor.txt","w",encoding="utf-8")
     _,rd,_=make_razbor(rd)
     for i in range(len(rd)):
         f.write(str(rd[i])+'\n')

     f.close()


def parse_str_theorem(lst,nlp):
    formula_list_table=[]
    formula_list,razbor_list=read_formulas()

    if len(formula_list)!=len(razbor_list):
        error_list.append(['Не совпадают размеры списка формул и списка разбора формул'])
        return error_list

    A=set(formula_list_function([lst]))
    B=set(formula_list)
    D=list(A.difference(B))
    A=list(A)+D
    R=[]

    A=Formula_Tree()
    
    for k in range(len(formula_list)):
        if formula_list[k] in lst:
            lst=lst.replace(formula_list[k],"formula_"+str(k+1))
            formula_list_table.append(["formula_"+str(k+1),formula_list[k],razbor_list[k]])

    for k in range(len(D)):
        lst=lst.replace(D[k],"formula_"+str(len(formula_list)+k+1))
        r=A.main(D[k])
        formula_list_table.append(["formula_"+str(len(formula_list)+k+1),D[k],r])
        R.append(r)

    write_formulas(D,R)
                
    a=[]
    k=0
    doc = nlp(lst)
    for sent in doc.sentences:
        for wrd in sent.dependencies:
            a.append([str(k+1),wrd[2].text,wrd[2].lemma,str(wrd[2].head),wrd[2].deprel,wrd[2].upos])
            k=k+1
            
    return a,formula_list_table

