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

    A=Ranger()
    a=d[0]
    index_list=d[1]
    ranking_ans=[]
   
    for i in range(len(db)):
        c=A.main(a,db[i],ra)
        ranking.append([str(i+1),c])

    ranking.sort(key = lambda x: x[1],reverse=True)
        
    for x in ranking:
        ranking_ans.append(x[0])
        
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

    mark=1+mark/len(ranking)
    mark=float("{:.2f}".format(mark))
    return str(mark),ranking_ans


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
    except:
        c=['-1']
        return c

    c_copy=c.copy()
    try:
        c=combine_formula_and_text(c,path_old)
    except:
        c=c_copy
    return c

    
def test_general_sub_main(mode):
    generate_label_list()
    make_razbor(path_db+"theorem_list.txt",path_db+"theorem_list_arr.txt")
    make_database(path_db+"theorem_list_arr.txt",path_db+"theorem_list_arr_razbor.txt")

    tmp=[]
    temp=[]
    temp_ra=[0,2]
    res=[]
    res_=[]
    tmp_res=[]
    
    temp=[]
    temp_=[]

    read_data_list=[]
    for k in range(8):
        d=reading_data(str(k+1),"arr")
        read_data_list.append(d)

    d=read_data_list.copy()
    for k in range(8):
        if d[k][0]=='-1':
            res[k][i]=-1
            res_[k][i]=-1
            continue

        a,b=testing_general_rank(path_db+"theorem_list_arr_razbor.txt",path+"theorem_list_arr_rank.txt",d[k],mode)
        res.append(a)
        res_.append(b)

          
    return res,res_,read_data_list


def test_general_main():
    a1,b1,c1=test_general_sub_main(0)
    a2,b2,c2=test_general_sub_main(1)
    a3,b3,c3=test_general_sub_main(2)
    index_table=[]
    ranking_table=[]
    
    for i in range(len(a1)):
        index_table.append([a1[i],a2[i],a3[i]])

    for i in range(len(b1)):
        ranking_table.append([b1[i],b2[i],b3[i]])

    return index_table,ranking_table,c1
    
def make_razbor(filein,fileout):
     lst=[]
     f=open(config_file_path,"r",encoding="utf-8")
     for line in f:
            line=line.split(":")
            if line[0]=="Infile":
                infile=line[1].strip()

     f.close()
    
     f=open(filein,"r",encoding="utf-8")
     for line in f:
            lst.append(preprocessing(line.strip(),path_old))
     f.close()

     nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,lemma,pos,depparse', models_dir=path_old, lang="ru",treebank='ru_syntagrus', use_gpu=True, pos_batch_size=3000)
     f=open(fileout,"w",encoding="utf-8")
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

            f.write(str(a))
            f.write('\n')
                
     f.close()


def make_database(filein,fileout):
     f=open(filein,"r",encoding="utf-8")
     a=[]
     for line in f:
            a.append(arr_etap_one(eval(line.strip())))
     f.close()

     razbor_one=[]
     razbor_two=[]
     A=Stamford()
     
     for i in range(len(a)):
         sf=0
         try:
             c=A.main(a[i],1)
             razbor_one.append(c)
             sf=1
             c=combine_formula_and_text(c,path_old)
             razbor_two.append(c)
         except:
             if sf==0:
                 razbor_one.append(['-1'])
                 razbor_two.append(['-1'])
             if sf==1:
                 razbor_two.append(['-1'])

     f=open(fileout,"w",encoding="utf-8")
     for x in razbor_two:
           f.write(str(x))
           f.write('\n')
     f.close()


   
    
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
    f=open(path_db+"file_list.txt","r",encoding="utf-8")
    for line in f:
        line=line.strip()
        file_list.append(line)
    f.close()


    for i in range(len(file_list)):
        f=open(path_db+"Теоремы/"+file_list[i]+".txt","r",encoding="utf-8")
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
               str1=str1+str(len(db_list)+1)+','
           else:
               str1=str1+str(len(db_list)+1)

           db_list.append(tmp[j])

        label_list.append(str1.split(','))

    #label_list,db_list=swapper(label_list,db_list,5)    
       
    f=open(path_db+"label_list.txt","w",encoding="utf-8")
    for x in label_list:
        f.write(str(x)+'\n')
    f.close()

    f=open(path_db+"theorem_list.txt","w",encoding="utf-8")
    for x in db_list:
        f.write(x)
        f.write('\n')
    f.close()


'''Блок тестирования модуля преобразования на язык логики предикатов'''
    
def testing_block_one(f1,f2,outname,outname2,index,algo,graph_mode):
    '''f1-файл со ответами'''
    f=open(test_dir_path+f1,"r",encoding="utf-8")
    a=[]
    b=[]
    for line in f:
        if line!='\n':
            a.append(eval(line.strip()))   
    f.close()

    '''f2-файл с разборами'''
    f=open(test_dir_path+f2,"r",encoding="utf-8")
    b=[]
    for line in f:
         if line!='\n':
             b.append(eval(line.strip()))
    f.close()

    '''f3-файл с предыдущими результатом'''
    f=open(test_dir_path+outname,"r",encoding="utf-8")
    res=[]
    for line in f:
         line=line.strip().split('\t');
         if len(line)!=(len(algo)*4):
             for i in range(len(algo)*4):
                 line.append('0')
            
         res.append(line)
    f.close()

    f=open(test_dir_path+"test_text.txt","r",encoding="utf-8")
    text=[]
    for line in f:
         line=line.strip()
         text.append(line)

    f.close()
         
    for i in range(len(a)-len(res)):
         tmp=[]
         for i in range(len(algo)*4):
             tmp.append('0')

         res.append(tmp)
            

    razbor=[]

    for i in range(len(a)):
            if index!=-1:
                if i!=index:
                    continue
            try:
                A=Stamford()
                B=Ranger()
                c=A.main(arr_etap_one(b[i]),1)

                for k in range(len(algo)):
                        r1=B.main(a[i],c,algo[k])
                        p1=float(r1)-float(res[i][0+4*k])
                    
                        if p1>0.0:
                            res[i][2+4*k]="+"+str(p1)
                        if p1<0.0 or p1==0.0:
                            res[i][2+4*k]=str(p1)

                        res[i][0+4*k]=float("{:.2f}".format(r1))

                if graph_mode==1:
                    C=plot_tree(a[i],"test_pic_"+str(i+1)+"0",text[i])
                    C.main("formula")

                b[i]=combine_formula_and_text(c,path)      
                razbor.append(b[i])

                if graph_mode==1:
                    C=plot_tree(b[i],"test_pic_"+str(i+1)+"1",text[i])
                    C.main("formula")

                for k in range(len(algo)):
                        r2=B.main(a[i],b[i],algo[k])
                        p2=float(r2)-float(res[i][1+4*k])
                    
                        if  p2>0.0:
                            res[i][3+4*k]="+"+str(p2)
                        if p2<0.0 or p2==0.0:
                            res[i][3+4*k]=str(p2)
        
                        res[i][1+4*k]=float("{:.2f}".format(r2))
               
                   
            except:
                for k in range(len(algo)*4):
                    res[i][k]='-1'
                
                razbor.append([])
        
     
          
    f=open(test_dir_path+outname,"w",encoding="utf-8")
    for i in range(len(res)):
        str1=""
        for k in range(len(algo)*4):
            str1=str1+str(res[i][k])+'\t'
                      
        f.write(str1+'\n')

    f.close()

    f=open(test_dir_path+outname2,"w",encoding="utf-8")
    for i in range(len(razbor)):
        f.write(str(razbor[i])+'\n\n')

    f.close()

def testing_block_two(in_text,out_text):
    text_list=[]
    text="Если непрерывная функция, определённая на вещественном интервале, принимает два значения, то она принимает и любое значение между ними ."
    text_list.append(text)
    '''
    res=[]
    f=open(test_dir_path+in_text,"r",encoding="utf-8")
    for line in f:
        line=line.strip()
        text_list.append(line)
    f.close()
    '''
    sf=0
    res=[]
    for x in text_list:
            sf=0
            r=preprocessing(x,path)
            sf=1
            A=Stamford()
            c=A.main(r,1)
            c=combine_formula_and_text(c,path)
            res.append(c)

    print(res)

    '''
    f=open(test_dir_path+out_text,"w",encoding="utf-8")
    for i in range(len(res)):
        f.write(str(res[i])+'\n\n')
    f.close()
    '''

#testing_block_two("","")
#test_general_main()

