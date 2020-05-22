import os
import random
import copy
from ranger import *
from draw_graph import *
from utilities import *
from cos_and_jaccard_for_text import *
from simple_ranger import *
from make_formula import *
from new_hybrid import *

path = os.path.dirname(os.path.dirname(__file__))
test_dir_path=path+"\\Test\\"

def testing_general_rank(ranking,ind,index_list):
    k=0
    r=0
    count=0
    idx=0

    for i in range(len(ranking)):
        if i==0 and i==ind:
            continue
        if ranking[i][0] in index_list:
            count=count+i+1
            r=k
        else:
            k=k+1

    for i in range(1,len(index_list)):
        count=count-i-1

    count=1-(count/len(index_list))/len(ranking)

    mark= str(float("{:.3f}".format(1 - r / len(ranking))))
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
            v1,v2=testing_general_rank(ranking,i,tmp)
            res.append(v1)
            res2.append(v2)
            ranking=[]
            t1=[]
            t2=[]
        
        return res,res2

    if mode==1: ##по ключевым словам
        ranking=[]
        res2=[]
        res,tmp_ranking=keyword_search()
        
        for i in range(len(tmp_ranking)):
            tmp=return_index_in_indexlist(i,index_list)
            for j in range(len(tmp_ranking[i])):
                ranking.append([str(int(tmp_ranking[i][j][0])+1),tmp_ranking[i][j][1]])

            _,v2=testing_general_rank(ranking,i,tmp)
            res2.append(v2)
            ranking=[]
                    
        return res,res2

    if mode==2:
        res=[]
        res2=[]

        db=reading_data(filein.split('.txt')[0]+"_arr_razbor.txt","predicate")
        global_dict={}

        for i in range(len(db)):
            global_dict=make_dict(db[i],global_dict)

        for i in range(len(db)):
            tmp=return_index_in_indexlist(i,index_list)
           
            for j in range(len(db)):
                 ranking.append([str(j+1),hybrid_main(db[i],db[j],global_dict)])

            ranking.sort(key = lambda x: x[1],reverse=True)
            v1,v2=testing_general_rank(ranking,i,tmp)
            res.append(v1)
            res2.append(v2)
            ranking=[]
            
        return res,res2

    if mode==3 or mode==4 or mode==5:
        text_list=[]
        ranking=[]
        tmp=[]
        res=[]
        res2=[]

        if mode==3:
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

            if mode==3:
                for j in range(len(levenshtein_ranking[i])):
                    ranking.append([str(j+1),levenshtein_ranking[i][j]])
                    
            if mode==4:
                for j in range(len(text_list)):
                    ranking.append([str(j+1),get_result(text_list[i],text_list[j],1)])

            if mode==5:
                for j in range(len(text_list)):
                    ranking.append([str(j+1),get_result(text_list[i],text_list[j],2)])
                    
            ranking.sort(key = lambda x: x[1],reverse=True)
            v1,v2=testing_general_rank(ranking,i,tmp)
            res.append(v1)
            res2.append(v2)
            ranking=[]

        return res,res2

 
