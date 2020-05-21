import yaml
import os

path = os.path.dirname(os.path.dirname(__file__))

def load_synonyms(file):
    try:
        data = yaml.load(open(file, 'rt', encoding='utf8'), Loader=yaml.FullLoader)
        d = {}
        for k, v in data.items():
            for x in v: d[x] = k
        return d
    except FileNotFoundError:
        return {}


def read_dict():
     words_construction=[]
     morph=[]
     trash=[]
     
     f=open(path+"\\Files\\dicts\\words_construction.txt","r",encoding="utf-8")
     for line in f:
            line=line.split('\t')
            line[4]=line[4].strip()
            words_construction.append(line)
     f.close()

     f=open(path+"\\Files\\dicts\\error_morph.txt","r",encoding="utf-8")
     for line in f:
            line=line.split('\t')
            line[1]=line[1].strip()
            morph.append(line)
     f.close()

     f=open(path+"\\Files\\dicts\\trash.txt","r",encoding="utf-8")
     for line in f:
        line=line.split('\t')
        for x in line:
            trash.append(x)
     f.close()
     
     return words_construction,morph,trash

def recount_number(num,a,mode):
    for i in range(len(a)):
        if int(a[i][0])>num:
            if mode==0:
                a[i][0]=str(int(a[i][0])-1)
            if mode==1:
                a[i][0]=str(int(a[i][0])+1)

        if int(a[i][3])>num:
            if mode==0:
                a[i][3]=str(int(a[i][3])-1)
            if mode==1:
                a[i][3]=str(int(a[i][3])+1)

    return a

def candidate_for_delete(a,k):
    a[k][2]="del"
    a[k][1]="del"
    return a[k]

def tokenize_correction(a,wc,em,ts):
    count=0
    for i in range(len(a)):
        if a[i][2].count("formula")>1:
            tmp=a[i][2].split(",")
            a[i][2]=tmp[0]
            a[i][1]=tmp[0]
            
            for k in range(1,len(tmp)):
                a.insert(i+1,[str(int(a[i][0])+1), tmp[k], tmp[k], a[i-1][3], a[i][4], a[i][5]])
                a=recount_number(i+1,a,1)
                
                    
        if a[i][2]=="(":
            count=1
            for t in range(i+1,len(a)):
                if count==0:
                    break
                if a[t][2]=="(":
                    count=count+1
                if a[t][2]==")":
                    count=count-1

            for k in range(i,t):
                a[k]=candidate_for_delete(a,k)
               
                    
        for j in range(len(ts)):
            if ts[j]==a[i][2]:
                a[i]=candidate_for_delete(a,i)
                
        if a[i][2]=="," or a[i][2]==".":
            a[i]=candidate_for_delete(a,i)
            
        if a[i][2]=="не":
            if i<len(a)-1:
                if a[i+1][5]=="VERB":
                    a[i+1][2]=a[i][2]+" "+a[i+1][2]
                    a[i+1][1]=a[i][1]+" "+a[i+1][1]
                    a[i]=candidate_for_delete(a,i)
                    
        if i<len(a)-1 and a[i][1]=="formula_" and a[i+1][1].isnumeric():
            a[i][1]=a[i][1]+a[i+1][1]
            a[i][2]=a[i][2]+a[i+1][2]
            a[i+1]=candidate_for_delete(a,i+1)

        if i<len(a)-1 and a[i][1]=="formula" and a[i+1][1][0]=="_" and a[i+1][1][1:].isnumeric():
            a[i][1]=a[i][1]+a[i+1][1]
            a[i][2]=a[i][2]+a[i+1][2]
            a[i+1]=candidate_for_delete(a,i+1)

        if i<len(a)-2 and a[i][1]=="formula" and a[i+1][1]=="_" and a[i+2][1].isnumeric():
            a[i][1]=a[i][1]+a[i+1][1]+a[i+2][1]
            a[i][2]=a[i][2]+a[i+1][2]+a[i+2][1]
            a[i+1]=candidate_for_delete(a,i+1)
            a[i+2]=candidate_for_delete(a,i+2)


        if "-" in a[i][2][0]:
            if len(a[i][2].strip())>0:
                a[i-1][1]=a[i-1][1]+a[i][1]
                a[i-1][2]=a[i-1][2]+a[i][1]
                a[i]=candidate_for_delete(a,i)

        if "formula_" in a[i][1]:
            if a[i][1]!=a[i][2]:
                a[i][2]=a[i][1]

        for k in range(len(em)):
            if em[k][0]==a[i][2]:
                a[i][2]=em[k][1]

        for k in range(len(wc)):
            if wc[k][0]==a[i][2] and (wc[k][3]=="join" or wc[k][3]=="del_full"):
                tmp=a[i:i+int(wc[k][2])]
                str1=""
                for x in tmp:
                    if str1=="":
                        str1=x[2]
                    else:
                        str1=str1+" "+x[2]

                if str1==wc[k][1]:
                    if wc[k][3]=="del_full":
                        for n in range(int(wc[k][2])):
                             a[i+n]=candidate_for_delete(a,i+n)

                    if wc[k][3]=="join":
                        for n in range(int(wc[k][2])):
                            a[i+n]=candidate_for_delete(a,i+n)
                            ids=int(wc[k][4])-1
                            a[i+ids][2],a[i+ids][1]=str1,str1
           
    for i in range(len(a)):
        for k in range(len(wc)):
            if wc[k][0]==a[i][2] and (wc[k][3]=="parent_children"):
                for m in range(len(a)):
                    if a[m][2]==wc[k][1] and a[m][3]==a[i][0]:
                        a[i][2]=a[i][2]+" "+a[m][2]
                        a[i][1]=a[i][1]+" "+a[m][1]
                        a[m]=candidate_for_delete(a,m)
                        
        if a[i][2]=="она":
            for k in range(i-1,0,-1):
                if "nsubj" in a[k][4]:
                    a[i][2]=a[k][2]
                    a[i][1]=a[k][1]

        if "formula" in a[i][1]:
            if "formulaz" in a[i][2]:
                a[i][2]=a[i][2].replace("formulaz","formula_")
            if "formulam" in a[i][2]:
                a[i][2]=a[i][2].replace("formulam","formula_")

            if a[i][4]!="root":
                if i>0 and a[i-1][4]=="advmod":
                    a[i][3]=a[i-1][0]
                if i<len(a)-1 and "formula" in a[i-1][1]:
                    a[i][3]=a[i+1][0]

        if a[i][1]=="т.е" or a[i][1]=="т.е.":
            for k in range(i,len(a)):
                if a[k][3]==a[i][0]:
                    a[k][3]=a[i][3]

            a[i]=candidate_for_delete(a,i)
                
        if a[i][4]=="punct":
            a[i][3]=a[i-1][0]
                   
    for i in range(len(a)-1,-1,-1):
        if a[i][1]=="del":
            a=recount_number(i,a,0)
            del a[i]

    return a

def word_with_synonyms(a,synonyms):
    sp_words=[]
    eq_words={}
    flag=1
   
    f=open(path+"\\Files\\dicts\\special.txt","r",encoding="utf-8")
    for line in f:
        line=line.split('\t')
        for x in line:
            sp_words.append(x)
    f.close()
   
    for i in range(len(a)):
        if a[i][2] in synonyms:
            a[i][2]=synonyms[a[i][2]]
            a[i][1]=a[i][2]

    for i in range(len(a)):
        if a[i][2] in sp_words:
            for k in range(len(a)):
                if a[k][3]==a[i][0]:
                    if a[i][4]=="flat:foreign":
                        a[i][2]=a[k][2]
                        a[k][2]="del"
                        a[k][1]="del"
                        
                    break
                
            a[i][2]="del"
            a[i][1]="del"

        

    for i in range(len(a)-1,-1,-1):
        if a[i][1]=="del":
            a=recount_number(i,a,0)
            del a[i]

            
    return a

def read_formulas_():
    formula_list=[]
    razbor_list=[]
    
    f=open(path+"\\Temp\\formulas_.txt","r",encoding="utf-8")
    for line in f:
        formula_list.append(line.strip())  
    f.close()

    f=open(path+"\\Temp\\formulas_razbor.txt","r",encoding="utf-8")
    for line in f:
        razbor_list.append(eval(line.strip()))  
    f.close()

    return formula_list,razbor_list
    

def dfs(visited,graph,node,temp):
    if node not in visited:
        visited.add(node)
        temp.append([node,graph[node]])
        for neighbour in graph[node]:
            dfs(visited,graph,neighbour,temp)

def recreate(l,a):
    for i,elem in enumerate(l):
        if not isinstance(elem,str):
            l[i]=recreate(elem,a)
        else:
            try:
                l[i]=str(a[int(elem)-1][2])+"::"+a[int(elem)-1][4]
            except:
                0
       
    return l


def dict_(a,rl):
    mydict={}
    visited=set()
    tmp=[]
    root='1'
    
    for i in range(len(a)):
        tmp=[]
        if a[i][3]=="0":
            root=str(a[i][0])
            
        for k in range(len(a)):
            if a[k][3]==a[i][0]:
                tmp.append(a[k][0])

        mydict[str(i+1)]=tmp

    temp=[]

    dfs(visited,mydict,root,temp)
    
    for i in reversed(range(len(temp))):
            for j in reversed(range(len(temp))):
                if temp[i][0] in temp[j][1]:
                    for k in range(len(temp[j][1])):
                        if temp[i][0]==temp[j][1][k]:
                            if temp[i][1]==[]:
                                temp[j][1][k]=[temp[i][0]]
                            else:
                                temp[j][1][k]=temp[i]
                
    temp=temp[0]
    temp=recreate(temp,a)
    temp=antirecreate(temp)
    insert_formula(temp,rl)
    return temp

def syntax_correction(a):
    for i in range(len(a)):
        if i<len(a)-1 and a[i][2]=="этот":
            for k in range(i-1,0,-1):
                if a[k][2]==a[i+1][2]:
                    flag=1
                    for m in range(k,len(a)):
                        if a[m][3]==a[k][0]:
                            if "formula" in a[m][2]:
                                a[i][2]=a[m][2]
                                a[i][1]=a[m][2]
                                flag=0
                                break
                            
                    if flag==0:
                        break
                        
    return a



def create_formula_str():
    infile=path+"\\Temp\\theorem_list_arr.txt"
    outfile=path+"\\Temp\\theorem_list_arr_razbor.txt"
   
    synonyms = load_synonyms(path+'\\Files\\synonyms.yml')
    wc,em,ts=read_dict()
    fl,rl=read_formulas_()
    res=[]
    lst=[]

    f=open(infile,"r",encoding="utf-8")
    for line in f:
        a=eval(line.strip())
        lst.append(a)
    f.close()

    for i in range(len(lst)):
        a=tokenize_correction(lst[i],wc,em,ts)
        a=syntax_correction(a)
        a=word_with_synonyms(a,synonyms)
        a=post_correction(a)
        res.append(a)

    f=open(outfile,"w",encoding="utf-8")
    for i in range(len(res)):
        a=str(antirecreate(dict_(res[i],rl)))
        f.write(str(a)+'\n')
       
    f.close()


def create_formula_arr(a):
    synonyms = load_synonyms(path+'\\Files\\synonyms.yml')
    wc,em,ts=read_dict()
    fl,rl=read_formulas_()
    a=tokenize_correction(a,wc,em,ts)
    a=syntax_correction(a)
    a=word_with_synonyms(a,synonyms)
    
    a=post_correction(a)
    a=dict_(a,rl)

    return a

def post_correction(a):
    tmp_ind=[]
    tmp=[]
    flag=0

    for m in range(len(a)):
        if a[m][2]=="<=>":
            flag=a[m][0]
            a[m][3]="0"
            a[m][4]="root"
            
    if flag!=0:
        for i in range(len(a)):
            if (a[i][4]=="root" or a[i][4]=="advcl") and int(a[i][0])<int(flag):
                a[i][3]=flag

            if flag!=0 and (a[i][2]=="if" or a[i][2]=="then" or a[i][2]=="forall" or a[i][2]=="exists"):
                 a[i][3]=flag
                 flag=a[i][0]

            if a[int(flag)-1][2]=="forall" and (a[i][5]=="NOUN" or "formula" in a[i][2]):
                a[i][3]=flag

        flag=0

    for i in range(len(a)):
         if a[i][2]=="if" and i==0:
             a[i][3]='0'
             a[i][4]="root"
             flag=a[i][0]
             continue
            
         if flag!=0 and (a[i][2]=="if" or a[i][2]=="then" or a[i][2]=="forall" or a[i][2]=="exists"):
            if a[int(flag)-2][2]=="и":
                a[i][3]=a[int(flag)-1][3]
            if a[int(flag)-2][2]!="и":
                a[i][3]=flag

            flag=a[i][0]
             
         if flag!=0 and (a[i][4]=="advcl" or a[i][4]=="root" or (a[i][4]=="conj" and a[i][5]=="VERB")):
             a[i][3]=flag

    for i in range(len(a)):
        if a[i][0]==a[i][3]:
            for t in range(i-1,0,-1):
                if a[t][2]=="forall" or a[t][2]=="exists" or a[t][2]=="then" or a[t][2]=="if" or a[t][2]=="<=>":
                    a[i][3]=a[t][0]
                    break

            if a[i][0]==a[i][3]:
                a[i][3]="1"
            
        if a[i][2]=="equal":
            for t in range(i-1,0,-1):
                if a[t][2]=="forall" or a[t][2]=="exists" or a[t][2]=="then" or a[t][2]=="if" or a[t][2]=="<=>":
                    a[i][3]=a[t][0]
                    break
                
            if i<len(a)-1:
                a[i+1][3]=a[i][0]
   
    return a
            

def antirecreate(l):
     for i,elem in enumerate(l):
        if not isinstance(elem,str):
            l[i]=antirecreate(elem)
        else:
            l[i]=elem.split("::")[0]
            
     return l

def insert_formula(l,rl):
    for i,elem in enumerate(l):
        if not isinstance(elem,str):
            l[i]=insert_formula(elem,rl)
        else:
            if "formula" in elem:
                if "." in elem:
                    elem=elem.replace(".","")
                    
                if not '-' in elem:
                    idx=int(elem.split("_")[1])-1
                    try:
                        l[i]=rl[idx]
                    except:
                        0
                else:
                    st=elem.split("-")
                    idx=int(st[0].strip().split("_")[1])-1
                    l[i]=rl[idx]
                 
    return l

a=[['1', 'Если', 'если', '3', 'mark', 'SCONJ'], ['2', 'formula_107', 'formula_107', '3', 'nsubj', 'PROPN'], ['3', 'непрерывна', 'непрерывный', '19', 'advcl', 'ADJ'], ['4', 'на', 'на', '5', 'case', 'ADP'], ['5', 'отрезке', 'отрезок', '3', 'obl', 'NOUN'], ['6', 'formula_76', 'formula_76', '5', 'flat:foreign', 'PROPN'], ['7', 'и', 'и', '5', 'cc', 'CCONJ'], ['8', 'formula_', 'formula_', '5', 'flat:foreign', 'PROPN'], ['9', '106', '106', '5', 'nummod', 'NUM'], ['10', '—', '—', '13', 'punct', 'PUNCT'], ['11', 'любая', 'любой', '13', 'det', 'DET'], ['12', 'её', 'ее', '13', 'det', 'DET'], ['13', 'первообразная', 'первообразный', '3', 'conj', 'ADJ'], ['14', 'на', 'на', '16', 'case', 'ADP'], ['15', 'этом', 'этот', '16', 'det', 'DET'], ['16', 'отрезке', 'отрезок', '13', 'nmod', 'NOUN'], ['17', ',', ',', '3', 'punct', 'PUNCT'], ['18', 'то', 'то', '19', 'mark', 'SCONJ'], ['19', 'имеет', 'иметь', '0', 'root', 'VERB'], ['20', 'место', 'место', '19', 'obj', 'NOUN'], ['21', 'равенство', 'равенство', '19', 'nsubj', 'NOUN'], ['22', 'formula_52', 'formula_52', '21', 'flat:foreign', 'PROPN'], ['23', '.', '.', '19', 'punct', 'PUNCT']]
b=[['1', 'Если', 'если', '6', 'mark', 'SCONJ'], ['2', 'formula_15', 'formula_15', '10', 'advcl', 'PROPN'], ['3', '–', '–', '6', 'punct', 'PUNCT'], ['4', 'любая', 'любой', '6', 'det', 'DET'], ['5', 'первообразная', 'первообразный', '6', 'amod', 'ADJ'], ['6', 'функции', 'функция', '10', 'advcl', 'NOUN'], ['7', 'formula_171', 'formula_171', '6', 'flat:foreign', 'PROPN'], ['8', ',', ',', '3', 'punct', 'PUNCT'], ['9', 'то', 'то', '10', 'mark', 'SCONJ'], ['10', 'справедливо', 'справедливый', '0', 'root', 'ADJ'], ['11', 'равенство', 'равенство', '10', 'nsubj', 'NOUN'], ['12', 'formula_53', 'formula_53', '11', 'flat:foreign', 'PROPN'], ['13', '.', '.', '10', 'punct', 'PUNCT']]
c=[['1', 'Пусть', 'пусть', '4', 'advmod', 'PART'], ['2', 'formula_188', 'formula_188', '4', 'nsubj', 'PROPN'], ['3', '-', '-', '2', 'punct', 'PUNCT'], ['4', 'функция', 'функция', '0', 'root', 'NOUN'], ['5', ',', ',', '6', 'punct', 'PUNCT'], ['6', 'интегрируема', 'интегрировать', '4', 'conj', 'VERB'], ['7', 'по', 'по', '8', 'case', 'ADP'], ['8', 'Риману', 'Риман', '6', 'obl', 'PROPN'], ['9', 'на', 'на', '10', 'case', 'ADP'], ['10', 'отрезке', 'отрезок', '6', 'obl', 'NOUN'], ['11', 'formula_40', 'formula_40', '10', 'flat:foreign', 'PROPN'], ['12', 'и', 'и', '15', 'cc', 'CCONJ'], ['13', 'функция', 'функция', '15', 'nsubj', 'NOUN'], ['14', 'formula_23', 'formula_23', '13', 'flat:foreign', 'PROPN'], ['15', 'непрерывна', 'непрерывный', '4', 'conj', 'ADJ'], ['16', 'на', 'на', '17', 'case', 'ADP'], ['17', 'отрезке', 'отрезок', '15', 'obl', 'NOUN'], ['18', 'formula_40', 'formula_40', '17', 'flat:foreign', 'PROPN'], ['19', 'и', 'и', '20', 'cc', 'CCONJ'], ['20', 'дифференцируема', 'дифференцируемый', '4', 'conj', 'ADJ'], ['21', 'в', 'в', '24', 'case', 'ADP'], ['22', 'каждой', 'каждый', '24', 'det', 'DET'], ['23', 'внутренней', 'внутренний', '24', 'amod', 'ADJ'], ['24', 'точке', 'точка', '20', 'obl', 'NOUN'], ['25', 'этого', 'этот', '26', 'det', 'DET'], ['26', 'отрезка', 'отрезок', '24', 'nmod', 'NOUN'], ['27', ',', ',', '34', 'punct', 'PUNCT'], ['28', 'причем', 'причем', '34', 'cc', 'CCONJ'], ['29', 'formula_21', 'formula_21', '34', 'nsubj', 'PROPN'], ['30', ',', ',', '31', 'punct', 'PUNCT'], ['31', 'formula_128', 'formula_128', '29', 'flat:foreign', 'PROPN'], ['32', ',', ',', '34', 'punct', 'PUNCT'], ['33', 'тогда', 'тогда', '34', 'advmod', 'ADV'], ['34', 'справедлива', 'справедливый', '4', 'conj', 'ADJ'], ['35', 'формула', 'формула', '34', 'nsubj', 'NOUN'], ['36', 'formula_60', 'formula_60', '35', 'flat:foreign', 'PROPN'], ['37', '.', '.', '4', 'punct', 'PUNCT']]


#for x in a:
    #print(x)

#r1=create_formula_arr(a)
#r2=create_formula_arr(b)
#r3=create_formula_arr(c)

#print(r1)
#print()
#print(r2)
#print()
#print(r3)

#print(r)
#print()
#print(r2)
#create_formula_str()
