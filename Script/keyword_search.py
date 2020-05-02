import os
import warnings
import stanfordnlp

path=os.path.dirname(os.path.dirname(__file__))
warnings.simplefilter("ignore", UserWarning)

def amount_table(text):
    index_table_one={}
    index_table_two={}
    gramms_list_2=[]
    coeff=0

    res=[]
    ###посчитали сколько раз какое слово встретилось
    for i in range(len(text)):
        if text[i][0] in index_table_one:
            index_table_one[text[i][0]]=index_table_one[text[i][0]]+1
        else:
            index_table_one[text[i][0]]=1

    return index_table_one
            
    
def indexing(text):
    index_table_one={}
    index_table_two={}
    gramms_list_2=[]
    coeff=0

    ###посчитали сколько раз какое слово встретилось

    for i in range(len(text)):
        if text[i][0] in index_table_one:
            index_table_one[text[i][0]]=index_table_one[text[i][0]]+1
        else:
            index_table_one[text[i][0]]=1

    
    #### словосочетания ####
    
    for i in range(len(text)):
        for j in range(i+1,len(text)):
            if text[i][0]==text[j][0]:
                continue

            if text[i][1]=='ADP' or text[j][1]=='ADP' or text[i][0]=="," or text[i][0]=="," or text[i][0]=="." or text[j][0]==".":
                continue

            flag=1
            for m in range(len(text[i+1:j])):
                if text[i+1:j][m][0]=="," or text[i+1:j][m][0]==".":
                    flag=0
                    break

            if flag==0:
                continue
            
            if len(text[i+1:j])>0:
                a=text[i+1:j]
                for m in range(len(a)-1,-1,-1):
                    if a[m][1]=="ADP":
                        del a[m]

                if len(a)>0:    
                    coeff=coeff+1/len(a)

        
            for k in range(len(gramms_list_2)):
                p=gramms_list_2[k][0].split()
                if text[j][0] in p[0] and text[i][0] in p[len(p)-1]:
                    if len(text[j+1:i])>0:
                        a=text[j+1:i]
                        for m in range(len(a)-1,-1,-1):
                            if a[m][1]=="ADP":
                                del a[m]
                                
                        if len(a)>0:  
                            coeff=coeff+1/(2*len(a))

            str1=text[i][0]
            for x in range(len(text[i+1:j])):
                str1=str1+" "+text[i+1:j][x][0]

            str1=str1+" "+text[j][0]
            
            gramms_list_2.append([str1,coeff])
            coeff=0
            str1=""  
            

    for i in range(len(gramms_list_2)):
        a=gramms_list_2[i][0]

        if a in index_table_two:
            index_table_two[a]=index_table_two[a]+1
        else:
            index_table_two[a]=gramms_list_2[i][1]

    res=[] 
    for x in index_table_one.keys():
        res.append([x,index_table_one[x]])

    for x in index_table_two.keys():
        res.append([x,index_table_two[x]])
    
    return res


def stamford_analyze(text,nlp):
    lemma_list=[]
    stamford = nlp(text)
    
    for sent in stamford.sentences:
         for wrd in sent.dependencies:
                    lemma_list.append([wrd[2].lemma,wrd[2].upos])
                    
    return lemma_list
                    

def make_general_indexing(text_list,nlp):
     indexing_table=[]
     for i in range(len(text_list)):
         b=stamford_analyze(text_list[i],nlp)
         a=indexing(b)
        
         for x in a:
             flag=0
             for y in indexing_table:
                 if x[0]==y[0]:
                    y[1]=y[1]+x[1]
                    flag=1
                    break
                
             if flag==0:
                 indexing_table.append(x)
     '''
     f=open(path+"/Database/indexing_table.txt","w",encoding="utf-8")
     for i in range(len(indexing_table)):
        x=indexing_table[i]
        f.write(str(x[0])+'\t'+str(x[1])+'\n')

     f.close()
     '''
     
     ranking_list=[]
     ranking_list_gl=[]

     for m in range(len(text_list)):
         a_in=text_list[m]
         for t in range(len(text_list)):
             b_in=text_list[t]
            
             b_t=amount_table(a_in)
             A=[]
             for x in b_t:
                 for i in range(len(indexing_table)):
                     if x==indexing_table[i][0]:
                         b_t[x]=b_t[x]/indexing_table[i][1]
                         A.append(b_t[x])

             b_t=amount_table(b_in)
             B=[]
             for x in b_t:
                 for i in range(len(indexing_table)):
                     if x==indexing_table[i][0]:
                         b_t[x]=b_t[x]/indexing_table[i][1]
                         B.append(b_t[x])

             ##вычисляем коэффициент Жаккара
             S1=set(i for i in A)
             S2=set(i for i in B)
             intersection = len(list(S1.intersection(S2)))
             union = (len(S1) + len(S2)) - intersection

             if union!=0:
                 res=float(intersection) / union
             else:
                 res=0

             ranking_list.append([str(t+1),res])

         ranking_list.sort(key = lambda x: x[1],reverse=True)
         ranking_list_gl.append(ranking_list)
         ranking_list=[]

     
     return ranking_list_gl

'''   
text_list=[]
f=open(path+"/Database/theorem_list.txt","r",encoding="utf-8")
for line in f:
    text_list.append(line.strip())
f.close()

make_general_indexing(text_list)
'''
