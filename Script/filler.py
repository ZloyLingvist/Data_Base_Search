import os
from formula_tree import *
from processing import *
path=os.path.dirname(os.path.dirname(__file__))

def fill_formulas(name):
    lst_gl=[]
    f=open(path+"\\Files\\"+name,"r",encoding="utf-8")
    for line_ in f:
        lst_gl.append(line_.strip())
    f.close()

    A=Formula_Tree()
    f=open(path+"\\Files\\"+name.split('.')[0]+"_razbor.txt","w",encoding='utf-8')
    for x in lst_gl:
        print(x)
        if not '#' in x:
            try:
                r=A.main(x)
                f.write(str(r))
            except:
                f.write(str([x]))
        else:
            f.write(str([x]))

        f.write('\n')

    f.close()


#fill_formulas("formulas_.txt")
    

def get_general():
    a=[]
    f=open(path+"\\Files\\formulas__razbor.txt","r",encoding="utf-8")
    for line in f:
        a.append(eval(line.strip()))

    f.close()
    
    for i in range(len(a)):
        a[i]=combine_formula_and_text(a[i],path)

    f=open(path+"\\Files\\formulas__razbor_general.txt","w",encoding="utf-8")
    for x in a:
        f.write(str(x))
        f.write('\n')

    f.close()


#get_general()
