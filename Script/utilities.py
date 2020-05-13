import os

path = os.path.dirname(os.path.dirname(__file__))
path_db=path+"\\Database\\"

def read_formulas():
    formula_list=[]
    razbor_list=[]
    
    f=open(path+"\\Files\\formulas_.txt","r",encoding="utf-8")
    for line in f:
        formula_list.append(line.strip())  
    f.close()

    f=open(path+"\\Files\\test_razbor.txt","r",encoding="utf-8")
    for line in f:
        razbor_list.append(eval(line.strip()))  
    f.close()

    return formula_list,razbor_list

def write_formulas(formula_list,razbor_list):
    f=open(path+"\\Files\\formulas_.txt","a",encoding="utf-8")
    for line in formula_list:
        f.write(line+'\n')  
    f.close()

    f=open(path+"\\Files\\test_razbor.txt","a",encoding="utf-8")
    for line in razbor_list:
        f.write(str(line)+'\n')  
    f.close()
        

def formula_list_function(text_list):
    str1=""
    formulas_list=[]
    for text in text_list:
        count=0
        for i in range(len(text)):
            if text[i]=="{":
                count=count+1
               
            if text[i]=="}":
                count=count-1
            
            if count>0:
                str1=str1+text[i]

            if count==0 and len(str1)>0:
                str1=str1+text[i]
                formulas_list.append(str1)
                str1=""

    formulas_list=list(set(formulas_list))
    return formulas_list

## сбор теорем в один файл, создание списка соответствия теорем (txt,yml-формат)
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

def avg(arr):
    summ=0
    for i in range(len(arr)):
        summ=summ+float(arr[i])

    return summ/len(arr)

## модификация таблицы с синтаксической и морфологической информацией

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

### в преобразовании в язык логики предикатов
def checking(str1):
        str1=str1.split()
        a=['del']
        
        if len(str1)==1:
                if str1!='if' and str1!="then":
                        return False

        return True


##следующие функции, используется для преобразования матем. формул

def swap_to_first(arr,sign):
    for i in range(len(arr)):
        if arr[i]==sign:
            arr[i],arr[0]=arr[0],arr[i]

    return arr

def recursion_clean(l):
    for i,elem in enumerate(l):
            if not isinstance(elem,str):
                for k in range(len(elem)-1,-1,-1):
                    if elem[k]==[]:
                        del elem[k]
                        
                l[i]=recursion_clean(elem)
    return l

def swap_(arr,ast):
    for i in range(len(ast)):
        if type(ast[i]) is str:
            ast[i]=ast[i].strip()

    for j in range(len(ast)):
        if ast[j] in arr:
            ast[j],ast[0]=ast[0],ast[j]

    return ast

def clean_from_empty(ast):
    for i in range(len(ast)-1,-1,-1):
        if ast[i]==[]:
            del ast[i]

    return ast
                
def equalizer(ast,start):
    for i in range(start,len(ast)):
        if type(ast[i])==str:
            ast[i]=[ast[i]]

    return ast

def modifier_integral_summ(ast):
    for i in range(len(ast)):
            if i<len(ast)-1 and ast[i]=="_":
                ast[i]=[ast[i],ast[i+1]]
                ast[i+1]=[]
                
            if i<len(ast)-1 and ast[i]=="^":
                ast[i]=[ast[i],ast[i+1]]
                ast[i+1]=[]

    ast=clean_from_empty(ast)
    return ast


## для модуля тестирования
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
            tmp.append(x.strip());
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


def combine_formula_and_text_f(l,table):
    for i,elem in enumerate(l):
        if not isinstance(elem,str):
            l[i]=combine_formula_and_text_f(elem,table)
        else:
            if "formula" in l[i]:
                for k in range(len(table)):
                    if table[k][0]==l[i]:
                        l[i]=table[k][2]
    return l


def combine_formula_and_text(formula,table):
    r=combine_formula_and_text_f(formula,table)
    return r


