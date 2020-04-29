from processing import *
from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from utilities import *
from stamford import *
from testing_block import *

import sys

path = os.path.dirname(os.path.dirname(__file__))
path_old=path

def make_load_and_run():
    error_list=[]
    res_list=[]
    config_file_path=path+"\\Files\\config.ini"
    f=open(config_file_path,"r",encoding="utf-8")
    for line in f:
        line=line.strip().split(":")
        if line[0]=="Infile":
            line=line[1].strip()
            break

    f.close()

    lst=[]
    f=open(path+"/"+line,"r",encoding="utf-8")
    for line in f:
        lst.append(line.strip())
      
    f.close()

    nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,lemma,pos,depparse', models_dir=path_old, lang="ru",treebank='ru_syntagrus', use_gpu=True, pos_batch_size=3000)
    for i in range(len(lst)):
        try:
            b=eval(lst[i])
            if type(b)==str:
                theorem=preprocessing(b.strip(),path_old)   
                a=[]
                m=0
            
                doc = nlp(theorem)
                for sent in doc.sentences:
                    for wrd in sent.dependencies:
                        a.append([str(m+1),wrd[2].text,wrd[2].lemma,str(wrd[2].governor),wrd[2].dependency_relation,wrd[2].upos])
                        m=m+1
            else:
                a=arr_etap_one(b)
                
            A=Stamford()
            c=A.main(a,1)
            c=combine_formula_and_text(c,path_old)
            res_list.append(c)
        except:
            e_type, e_val, e_tb = sys.exc_info()
            res_list.append(['-1'])
            error_list.append(['Error in '+str(i+1)+'.'+str(e_type)+'\n'+str(e_val)])

    return lst,res_list,error_list
        


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
        c=A.main(a,db[i],2)
        ranking.append([str(i+1),c,db[i]])

    ranking.sort(key = lambda x: x[1],reverse=True)
    return ans,ranking

def make_razbor(theorem):
    '''
    если theorem - утверждение теоремы в текстовом виде (строка), то преобразуем его к таблице с синтаксическим разбором.
                 - утверждение теоремы уже в виде таблицы с синтаксическим разбором, то ничего не делаем
         представление в виде таблицы с синтаксическим разбором подаем на вход модуля преобразования на язык логики предикатов.
         затем подставляем в него разобранные формулы.
    '''
    if type(theorem)==str:
        theorem=preprocessing(theorem.strip(),path_old)
        lst=[]
        lst.append(theorem)

        nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,lemma,pos,depparse', models_dir=path_old, lang="ru",treebank='ru_syntagrus', use_gpu=True, pos_batch_size=3000)
        a=[]
        i=0
        for line in lst:
            doc = nlp(line)
            i=0
            a=[]
            for sent in doc.sentences:
                for wrd in sent.dependencies:
                    a.append([str(i+1),wrd[2].text,wrd[2].lemma,str(wrd[2].governor),wrd[2].dependency_relation,wrd[2].upos])
                    i=i+1
    else:
        a=theorem

    A=Stamford()
    c=A.main(a,1)
    c=combine_formula_and_text(c,path_old)
    return c

def make_tree(a,name,text):
    try:
        os.remove(path_old+"/Tree/"+name+".png")
        A=plot_tree(a,name,text)
        A.main("formula")
        return name
    except:
        return "-1"


