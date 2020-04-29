import os
import random
import copy

from ranger import *
from processing import *
from stamford import *
from draw_graph import *
from utilities import *

path = os.path.dirname(os.path.dirname(__file__))
path_old=path
config_file_path=path_old+"\\Files\\config.ini"
path_db=path+"\\Database\\"
test_dir_path=path+"\\Test\\"


def reading_data(num,type_):
    ''' модуль чтения данных '''
    
    ''' входные параметры:

        num - (в виде строки) порядковый номер теоремы для тестирования
        type: "text" - будет взято математическое утверждение в виде текста и для него по новой будет произведен синт. разбор
              "arr"  - будет взят уже имеющуюся таблицу с синтаксическим разбором
              
        выходные даннык:
        
        массив, состоящий из трех элементов:
            1. - преобразованный текст утверждения (при параметре "text")
                 преобразованная таблица с синтаксическим разбором (при параметре "arr")
            2. строка таблицы, содержащей какие номера каким теоремам соответствую ищем строку с num
            3. num  в виде числа. Значение уменьшено на 1.
    '''
    tmp=[]
    tmp2=[]
    c=[]
    num_num=int(num)-1
    
    if type_=="text":
        f=open(path_db+"theorem_list.txt","r",encoding="utf-8")
        for x in f:
            tmp.append(x.strip());
        f.close()
        text=preprocessing(tmp[num_num],path_old)
    
    if type_=="arr":
        f=open(path_db+"theorem_list_arr.txt","r",encoding="utf-8")
        for x in f:
            tmp.append(eval(x.strip()));
        f.close()
       
        text=arr_etap_one(tmp[num_num])


    f=open(path_db+"label_list.txt","r",encoding="utf-8")
    for x in f:
        tmp2.append(eval(x.strip()));
    f.close()

    for i in range(len(tmp2)):
            if c!=[]:
                break
            for j in range(1,len(tmp2[i])):
                if tmp2[i][j]==num:
                    c=tmp2[i][1:]
                    d=tmp2[i][1:]
                    break

    text=razbor_theorem(text)
    tmp=[text,c,num_num,d] 
   
    return tmp
    
def razbor_theorem(theorem):
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
    try:
        c=A.main(a,1)
        c=combine_formula_and_text(c,path_old)

    except:
        c=['-1']
    return c

    
def test_general_main():
    #generate_label_list()
    #make_razbor(path+"theorem_list.txt",path+"theorem_list_arr.txt")
    #make_database(path+"theorem_list_arr.txt",path+"theorem_list_arr_razbor.txt")

    tmp=[]
    temp=[]
    temp_ra=[2]
    res=[]
    for i in range(8):
        for j in range(len(temp_ra)):
            temp.append(0)

        res.append(temp)
        temp=[]

    for i in range(len(temp_ra)):
        for k in range(8):
                d=reading_data(str(k+1),"arr")
                if d[0]=='-1':
                    res[k][i]=-1
                    continue

                tmp.append(d)
                a=testing_general_rank(path_db+"theorem_list_arr_razbor.txt",path+"theorem_list_arr_rank.txt",d,temp_ra[i])
                res[k][i]=a
          
    print(res)
    return res,tmp

def testing_general_rank(filein,fileout,d,ra):
    '''модуль тестирования'''
    '''входные параметры:
       filein - файл, содержащий базу разборов
       fileout - файл, куда следует записать полученный результат
       d -  массив, состоящий из трех элементов:
            1. - преобразованный текст утверждения (при параметре "text")
                 преобразованная таблица с синтаксическим разбором (при параметре "arr")
            2. строка таблицы, содержащей какие номера каким теоремам соответствую ищем строку с num
            3. num  в виде числа. Значение уменьшено на 1.
       ra - параметр выбора алгоритма работы ранжировщика
    '''

    f=open(filein,"r",encoding="utf-8")
    db=[]
    ranking=[]
   
    for line in f:
           db.append(eval(line.strip()))
    f.close()

    a=d[0]
    index_list=d[1]
   
    A=Ranger()
    for i in range(len(db)):
        c=A.main(a,db[i],ra)
        ranking.append([str(i+1),c])

    ranking.sort(key = lambda x: x[1],reverse=True)
    mark=0
    
    for i in range(len(ranking)):
        if index_list==[]:
            break

        flag=0
        for k in range(len(index_list)):
            if ranking[i][0]==index_list[k]:
                flag=1
                del index_list[k]
                break

        if flag==0:
            mark=mark-1
               
    mark=float("{:.2f}".format(mark))
    return str(mark)


test_general_main()
