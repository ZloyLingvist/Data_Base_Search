from processing import *
from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from utilities import *
from stamford import *

path = os.path.dirname(os.path.dirname(__file__))
path_old=path


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
        A=plot_tree(a,name,text)
        A.main("formula")
        return name
    except:
        return "-1"
