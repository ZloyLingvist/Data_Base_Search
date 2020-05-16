from formula_tree import *
from ranger import *
from simple_ranger import *
from draw_graph import *
from utilities import *
from testing_block import *
from make_formula import *
import sys
import os
import stanza

path=os.path.dirname(os.path.dirname(__file__))
path_db=path+"\\Database\\"

def extract_formula_razbor():
    formulas_list=[]
    text_list=[]
    str1=""
    count=0

    f=open(path+"\\Temp\\theorem_list.txt","r",encoding="utf-8")
    for line in f:
        text_list.append(line.strip())
    f.close()

    formulas_list=formula_list_function(text_list)
    f=open(path+"\\Temp\\formulas_.txt","w",encoding="utf-8")
    
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


def make_ranking(a,p):
    filein=path+"\\Temp\\theorem_list_arr_razbor.txt"
  
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
            c=A.main(ans,db[i],p)
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
   
    for i in range(len(lst)):
            if type(lst[i])==str:   
                a=parse_str_theorem(lst[i],nlp)
            else:
                a=lst[i]
                
            c=create_formula_arr(a)
            res_list.append(c)
            
        #except:
            #e_type, e_val, e_tb = sys.exc_info()
            #res_list.append(['-1'])
            #error_list.append(['Error in '+str(i+1)+'.'+str(e_type)+'\n'+str(e_val)])

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
    filein=path+"\\Temp\\theorem_list.txt"
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
                
    f=open(path+"\\Temp\\mytex.tex","w",encoding="utf-8")
    for x in lst:
         f.write(x)
         f.write('\n')

    for i in range(len(rd)):
        f.write(str(i+1)+'. '+rd[i]+"\\\\")
        f.write('\n\n')

    f.write("\\end{document}")
    f.close()


def parse_str_theorem(lst,nlp):      
    a=[]
    k=0
    fl=[]
    f2=[]
    
    f=open(path+"\\Temp\\formulas_.txt","r",encoding="utf-8")
    for line in f:
        fl.append(line.strip())
    f.close()

    cf=formula_list_function([lst]) ##вытащим формулы из утверждения
    tmp=[]
    for i in range(len(cf)):
        if not cf[i] in fl:
            nlp=nlp.replace(cf[i],"formula_"+str(len(fl)+i+1))
            tmp.append(cf[i])
        else:
            for m in range(len(fl)):
                if fl[m]==cf[i]:
                    lst=lst.replace(cf[i],"formula_"+str(m+1))
                    break
        

    r=make_formula_razbor(tmp)

    f=open(path+"\\Temp\\formulas_.txt","a",encoding="utf-8")
    for x in tmp:
        f.write(str(x)+'\n')
    f.close()

    f=open(path+"\\Temp\\formulas_razbor.txt","a",encoding="utf-8")
    for x in r:
        f.write(str(x)+'\n')
    f.close()
    
    doc = nlp(lst)
    for sent in doc.sentences:
        for wrd in sent.dependencies:
            a.append([str(k+1),wrd[2].text,wrd[2].lemma,str(wrd[2].head),wrd[2].deprel,wrd[2].upos])
            k=k+1
            
    return a

        
def make_database():
     temp=[]
     generate_label_list()
     make_tex()
     filein=path+"\\Temp\\theorem_list.txt"
     rd=reading_data(filein,"text")

     nlp = stanza.Pipeline('ru',processors='tokenize,lemma,pos,depparse',dir=path+'\stanza_resources', package='syntagrus', use_gpu=True, pos_batch_size=3000)

     f=open(filein.split('.txt')[0]+"_arr.txt","w",encoding="utf-8")
     for i in range(len(rd)):
         a=parse_str_theorem(rd[i],nlp)
         temp.append(a)
         f.write(str(a)+'\n')
         
     f.close()
     create_formula_str()


