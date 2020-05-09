import os
import random
import copy

from ranger import *
from draw_graph import *
from utilities import *
from edit_distance import *
from cos_similarity import *
from simple_ranger import *
from testing_sub_block import *

import stanza

path = os.path.dirname(os.path.dirname(__file__))

def testing_general_rank(ranking,index_list):    
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
    return str(mark)

   
def test_general_sub_main(filein,mode):
    ranking=[]
    index_list=[]
    tmp=[]
    
    f=open(path_db+"label_list.txt","r",encoding="utf-8")
    for line in f:
        index_list.append(eval(line.strip()))

    f.close()

    if mode==0 or mode==1: ##алгоритм ранжирования
        db=reading_data(filein.split('.txt')[0]+"_arr_razbor.txt","predicate")
        res=[]
        for i in range(len(db)):
            tmp=return_index_in_indexlist(i,index_list)
            if tmp==-1:
                tmp=[]
                res.append('-1')
                continue
                
            A=Ranger()
            for j in range(len(db)):
                try:
                    ranking.append([str(j+1),A.main(db[i],db[j],mode)])
                except:
                    ranking.append([str(j+1),-1])

            ranking.sort(key = lambda x: x[1],reverse=True)
            res.append(testing_general_rank(ranking,tmp.copy()))
            ranking=[]
        
        return res

    if mode==2: ##по ключевым словам
        ranking=keyword_search()
        return ranking

    if mode==3 or mode==4 or mode==5:
        text_list=[]
        ranking=[]
        tmp=[]
        res=[]
        
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
                for j in range(len(text_list)):
                    #ranking.append([str(j+1),levenshtein(text_list[i],text_list[j])])
                    ranking.append([str(j+1),-1])

            if mode==4:
                for j in range(len(text_list)):
                    ranking.append([str(j+1),get_result(text_list[i],text_list[j],1)])

            if mode==5:
                for j in range(len(text_list)):
                    ranking.append([str(j+1),get_result(text_list[i],text_list[j],2)])
                    
            ranking.sort(key = lambda x: x[1],reverse=True)
            res.append(testing_general_rank(ranking,tmp.copy()))
            ranking=[]

        return res



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


#a=test_general_sub_main("C:\\Users\\Butuzov\\Desktop\\Version\\Database\\theorem_list.txt",2)
#testing_block_one("test_lst.txt","test_in.txt","outname.txt","outname2.txt",-1,[1],0)
