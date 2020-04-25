from ranger import *
from processing import *
from stamford import *
import os
from draw_graph import *


path = os.path.dirname(os.path.dirname(__file__))
test_dir_path=path+"\\Test\\"

def arr_etap_one(a):
    f=open(path+"\\Files\\dicts\words_trash.txt","r",encoding="utf-8")
    words_trash=[]
    for line in f:
        line=line.strip().split()
        for x in line:
            words_trash.append(x)

    for i in range(len(a)):
        if a[i][2] in words_trash:
            a[i][2]="del"
            a[i][1]="del"

        if a[i][2]=="-":
            a[i][2]="-"
            a[i][5]="-"
          
        if a[i][2]=="и":
            if a[i][4]=="advmod":
                a[i][2]="del"
                a[i][1]="del"

            '''
            if a[i][4]=="cc":
                a[i][2]=","
                a[i][1]=","
            '''

        if a[i][4]=="flat:foreign":
            a[i][2]=a[i][1]
            
        if a[i][2]=="она":
            for k in range(i,0,-1):
                if a[k][5]=="NOUN":
                    if a[k][4]==a[i][4]:
                        a[i][2]=a[k][2]
                        a[i][1]=a[k][2]

        if a[i][2]=="это":
            if i<len(a)-1 and a[i+1][5]=="NOUN":
                for k in range(i,0,-1):
                    if a[k][2]==a[i+1][2]:
                        for p in range(k,len(a)):
                            if a[p][4]=="flat:foreign":
                                if a[p][3]==a[k][0]:
                                    a[i][2]=a[p][2]
                                    a[i][1]=a[p][1]
                                    a[i][3]=a[i+1][0]
                                    a[i][4]=a[p][4]

    return a

        

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

                        res[i][0+4*k]=r1

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
        
                        res[i][1+4*k]=r2
               
                   
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
    res=[]
    f=open(test_dir_path+in_text,"r",encoding="utf-8")
    for line in f:
        line=line.strip()
        text_list.append(line)
    f.close()

    sf=0
    for x in text_list:
        try:
            sf=0
            r=preprocessing(x,path)
            sf=1
            A=Stamford()
            c=A.main(r,1)
            res.append(c)
        except:
            res.append(['-1',str(sf)])

    f=open(test_dir_path+out_text,"w",encoding="utf-8")
    for i in range(len(res)):
        f.write(str(res[i])+'\n\n')
    f.close()

testing_block_one("test_lst.txt","test_in.txt","outname.txt","outname2.txt",-1,[2],0)
#testing_block_two("test_set.txt","out_test_set.txt")

