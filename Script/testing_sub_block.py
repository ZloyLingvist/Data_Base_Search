import os
import random
from processing import *
from stamford import *

path = os.path.dirname(os.path.dirname(__file__))
path_old=path
config_file_path=path_old+"\\Files\\config.ini"
path_db=path+"\\Database\\"
test_dir_path=path+"\\Test\\"

def ranking_submodule(filein,d,ra):
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

    ranking_ans=[]
    db=[]
    ranking=[]
   
    f=open(filein,"r",encoding="utf-8")
    for line in f:
           db.append(eval(line.strip()))
    f.close()

    A=Ranger()
    a=d[0]
    index_list=d[1]
    
    for i in range(len(db)):
        c=A.main(a,db[i],ra)
        ranking.append([str(i+1),c])

    ranking.sort(key = lambda x: x[1],reverse=True)
    return ranking

def return_index_in_indexlist(i,index_list):
    for m in range(len(index_list)):
        for k in range(1,len(index_list[m])):
            if index_list[m][k]==str(i+1):
                return index_list[m][1:]

    return -1
                

def reading_data(filein,type_):
    tmp=[]
    if type_=="text":
        f=open(filein,"r",encoding="utf-8")
        for x in f:
            tmp.append(preprocessing(x.strip(),path));
        f.close()
        
    if type_=="arr":
        f=open(filein,"r",encoding="utf-8")
        for x in f:
            tmp.append(arr_etap_one(eval(x.strip())));
        f.close()

    if type_=="predicate":
        f=open(filein,"r",encoding="utf-8")
        for x in f:
            tmp.append(eval(x.strip()));
        f.close()
       
    return tmp
    
def razbor_theorem(theorem,nlp):
    '''
    если theorem - утверждение теоремы в текстовом виде (строка), то преобразуем его к таблице с синтаксическим разбором.
                 - утверждение теоремы уже в виде таблицы с синтаксическим разбором, то ничего не делаем
         представление в виде таблицы с синтаксическим разбором подаем на вход модуля преобразования на язык логики предикатов.
         затем подставляем в него разобранные формулы.
    '''
    if type(theorem)==str:
        lst=[]
        lst.append(theorem)

        a=[]
        i=0
        for line in lst:
            doc = nlp(line)
            i=0
            a=[]
            for sent in doc.sentences:
                for wrd in sent.dependencies:
                    a.append([str(i+1),wrd[2].text,wrd[2].lemma,str(wrd[2].head),wrd[2].deprel,wrd[2].upos])
                    i=i+1
    else:
        a=theorem

    return a


def make_formula(a):
    A=Stamford()
    
    try:
        c=A.main(a,1)
    except:
        c=['-1']
        return c

    c_copy=c.copy()
    try:
        c=combine_formula_and_text(c,path_old)
    except:
        c=c_copy
    return c


def swapper(ll,dl,k):
    for i in range(k):
        rn1=random.randrange(1,len(dl)-1)
        rn2=random.randrange(1,len(dl)-1)
        while rn1==rn2:
            rn2=random.randrange(1,len(dl))

        for j in range(len(ll)):
            t=-1
            for m in range(1,len(ll[j])):
                if int(ll[j][m])==min(rn1,rn2):
                    ll[j][m]=str(max(rn1,rn2))
                    continue
                        
                if int(ll[j][m])==max(rn1,rn2):
                    ll[j][m]=str(min(rn1,rn2))
                    continue
                          
        dl[rn1],dl[rn2]=dl[rn2],dl[rn1]
        
    return ll,dl
    

def generate_label_list():
    file_list=[]
    label_list=[]
    db_list=[]
    db_tmp_list=[]

    f=[]
    (_,_,file_list)=next(os.walk(path_db+"Теоремы/"))

    index=0
    for i in range(len(file_list)):
        f=open(path_db+"Теоремы/"+file_list[i],"r",encoding="utf-8")
        tmp=[]
        for line in f:
            line=line.split('\n')
            for x in line:
                if len(x.strip())==0:
                    continue

                tmp.append(x)
        f.close()

        str1=file_list[i]+","
        for j in range(len(tmp)):
           if j<len(tmp)-1:
               str1=str1+str(index+1)+','
           else:
               str1=str1+str(index+1)

           db_tmp_list.append(tmp[j])
           index=index+1

        db_list.append(db_tmp_list)
        db_tmp_list=[]
        label_list.append(str1.split(','))

    f=open(path_db+"label_list.yml","w",encoding="utf-8")
    for i in range(len(file_list)):
        for k in range(len(db_list[i])):
                f.write('- '+file_list[i].split('.txt')[0]+': > \n')
                f.write('   '+db_list[i][k]+'\n')
       
    f.close()
       
    f=open(path_db+"label_list.txt","w",encoding="utf-8")
    for x in label_list:
        f.write(str(x)+'\n')
    f.close()

    f=open(path_db+"theorem_list.txt","w",encoding="utf-8")
    for i in range(len(db_list)):
        for j in range(len(db_list[i])):
            f.write(str(db_list[i][j])+'\n')
        
    f.close()

#generate_label_list()
