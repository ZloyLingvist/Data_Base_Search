import os
import random
import copy
from ranger import *
from draw_graph import *
from utilities import *
from cos_and_jaccard_for_text import *
from simple_ranger import *
from make_formula import *

path = os.path.dirname(os.path.dirname(__file__))
test_dir_path=path+"\\Test\\"

def testing_general_rank(ranking,index_list):    
    mark=0
    count=0
    
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

        count=count+1

    mark=1+mark/len(ranking)
    mark=float("{:.2f}".format(mark))
    return str(mark),str(count)


def test_general_sub_main(filein,mode):
    ranking=[]
    index_list=[]
    tmp=[]
    formulas_list=[]
    db_tmp=[]
    
    f=open(path+"\\Temp\\label_list.txt","r",encoding="utf-8")
    for line in f:
        index_list.append(eval(line.strip()))

    f.close()

    f=open(path+"\\Temp\\formulas_razbor.txt","r",encoding="utf-8")
    for line in f:
        formulas_list.append(eval(line.strip()))

    f.close()
   
    if mode==0: ##алгоритм ранжирования
        res=[]
        res2=[]
        t1=[]
        t2=[]

        db=reading_data(filein.split('.txt')[0]+"_arr_razbor.txt","predicate")
        for i in range(len(db)):
            subformulas(db[i],db_tmp)
            db[i]=db_tmp
            db_tmp=[]
            

        for i in range(len(db)):
            tmp=return_index_in_indexlist(i,index_list)
            if tmp==-1:
                tmp=[]
                res.append('-1')
                continue

            A=Ranger()
            for j in range(len(db)):
                t2=[]
                try:
                    ranking.append([str(j+1),A.main(db[i],db[j])])
                except:
                    ranking.append([str(j+1),-1])

            ranking.sort(key = lambda x: x[1],reverse=True)
            v1,v2=testing_general_rank(ranking,tmp.copy())
            res.append(v1)
            res2.append(v2)
            ranking=[]
            t1=[]
            t2=[]
        
        return res,res2

    if mode==1: ##по ключевым словам
        res=[]
        res2=[]
        res,ranking=keyword_search()
        
        for i in range(len(ranking)):
            tmp=return_index_in_indexlist(i,index_list)
            v1,v2=testing_general_rank(ranking[i],tmp.copy())
            res.append(v1)
            res2.append(v2)
        
        return res,res2

    if mode==2 or mode==3 or mode==4:
        text_list=[]
        ranking=[]
        tmp=[]
        res=[]
        res2=[]

        if mode==2:
            levenshtein_ranking=[]
            f=open(path+"\\Temp\\result_list_levenshtein.txt","r",encoding="utf-8")
            for line in f:
                line=line.strip().split(" ")
                levenshtein_ranking.append(line)
            f.close()
        
        f=open(filein,"r",encoding="utf-8")
        for line in f:
            text_list.append(line.strip())
        f.close()

        for i in range(len(text_list)):
            tmp=return_index_in_indexlist(i,index_list)
            if tmp==-1:
                res.append('-1')
                continue

            if mode==2:
                for j in range(len(levenshtein_ranking[i])):
                    ranking.append([str(j+1),levenshtein_ranking[i]])
                    
            if mode==3:
                for j in range(len(text_list)):
                    ranking.append([str(j+1),get_result(text_list[i],text_list[j],1)])

            if mode==4:
                for j in range(len(text_list)):
                    ranking.append([str(j+1),get_result(text_list[i],text_list[j],2)])
                    
            ranking.sort(key = lambda x: x[1],reverse=True)
            v1,v2=testing_general_rank(ranking,tmp.copy())
            res.append(v1)
            res2.append(v2)
            ranking=[]

        return res,res2

 
