import os
import random
import copy

from ranger import *
from draw_graph import *
from utilities import *
from edit_distance import *
from cos_similarity import *
from simple_ranger import *

path = os.path.dirname(os.path.dirname(__file__))
test_dir_path=path+"\\Test\\"

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

    if mode==0 or mode==1 or mode==2: ##алгоритм ранжирования
        if mode!=2:
            db=reading_data(filein.split('.txt')[0]+"_arr_razbor.txt","predicate")
        else:
            db=reading_data(filein.split('.txt')[0]+"_arr_syntax.txt","predicate")
            mode=0
            
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

    if mode==3: ##по ключевым словам
        ranking=keyword_search()
        return ranking

    if mode==4 or mode==5 or mode==6:
        text_list=[]
        ranking=[]
        tmp=[]
        res=[]

        if mode==4:
            levenshtein_ranking=[]
            f=open(path+"\\Database\\result_list_levenshtein.txt","r",encoding="utf-8")
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

            if mode==4:
                for j in range(len(levenshtein_ranking[i])):
                    ranking.append([str(j+1),levenshtein_ranking[i]])
                    
            if mode==5:
                for j in range(len(text_list)):
                    ranking.append([str(j+1),get_result(text_list[i],text_list[j],1)])

            if mode==6:
                for j in range(len(text_list)):
                    ranking.append([str(j+1),get_result(text_list[i],text_list[j],2)])
                    
            ranking.sort(key = lambda x: x[1],reverse=True)
            res.append(testing_general_rank(ranking,tmp.copy()))
            ranking=[]

        return res

'''Блок тестирования модуля преобразования на язык логики предикатов'''
    
def testing_block_one(arr,test_example,outname):
    '''f1-файл со ответами'''
    f=open(test_dir_path+test_example,"r",encoding="utf-8")
    a=[]
    b=[]
    for line in f:
        if line!='\n':
            a.append(eval(line.strip()))   
    f.close()

    '''f3-файл с предыдущими результатом'''
    f=open(test_dir_path+outname,"r",encoding="utf-8")
    res=[]
    for line in f:
         line=line.strip().split('\t');
         res.append(line)
    f.close()

    

    ''''
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

    for i in range(len(arr)):
            if index!=-1:
                if i!=index:
                    continue
            try:
                B=Ranger()
                for k in range(len(arr[i])):
                        r2=B.main(arr[i],b[i],algo[k])
                        p2=float(r2)-float(res[i][0+4*k])
                    
                        if p2>0.0:
                            res[i][3+4*k]="+"+str(p2)
                        if p2<0.0 or p2==0.0:
                            res[i][3+4*k]=str(p2)
        
                        res[i][0+4*k]=float("{:.2f}".format(r2))
                        #razbor.append(res
                  
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
    '''
    #f.close()



#a=test_general_sub_main("C:\\Users\\Butuzov\\Desktop\\Version\\Database\\theorem_list.txt",2)
#testing_block_one("test_lst.txt","test_in.txt","outname.txt","outname2.txt",-1,[1],0)
