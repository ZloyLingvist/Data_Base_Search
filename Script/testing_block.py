from ranger import *
from processing import *
from stamford import *
import os

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
            a[i][5]="-"


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

    print(a)
    return a

def testing_block_one(f1,f2,outname,outname2,index):
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
         if len(line)!=4:
             line=['0','0','0','0']
             
         res.append(line)
    f.close()

    for i in range(len(a)-len(res)):
            res.append(['0','0','0','0'])

    razbor=[]
        
    for i in range(len(a)):
        if index!=-1:
            if i!=index:
                continue
        try:
            A=Stamford()
            B=Ranger()
            r=A.main(arr_etap_one(b[i]),1)
            r1=B.main(a[i],r,2)
                
            b[i]=combine_formula_and_text(r,path)
   
            r2=B.main(a[i],b[i],2)

            p1=float(r1)-float(res[i][0])
            if  p1>0.0:
                res[i][2]="+"+str(p1)
            if p1<0.0 or p1==0.0:
                res[i][2]=str(p1)
            
            p2=float(r2)-float(res[i][1])
            if p2>0.0:
                res[i][3]="+"+str(p2)
            if p2<0.0 or p2==0.0:
                res[i][3]=str(p2)
            
            res[i][0]=r1
            res[i][1]=r2
            razbor.append(b[i])

        except:
            res[i][0]='-1'
            res[i][1]='-1'
            res[i][2]='-1'
            res[i][3]='-1'
            razbor.append([])
        
     
          
    f=open(test_dir_path+outname,"w",encoding="utf-8")
    for i in range(len(res)):
        f.write(str(res[i][0])+'\t'+str(res[i][1])+'\t'+str(res[i][2])+'\t'+str(res[i][3])+'\n')

    f.close()

    f=open(test_dir_path+outname2,"w",encoding="utf-8")
    for i in range(len(razbor)):
        f.write(str(razbor[i])+'\n\n')

    f.close()
   

testing_block_one("test_lst.txt","test_in.txt","outname.txt","outname2.txt",15)

