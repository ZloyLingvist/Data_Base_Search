from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from combine_formula_text import *
import pickle

'''
# разбор формул из файла
f=open("dicts/f.txt","r",encoding="utf-8")
fl=[]
for line in f:
    line=line.strip()
    fl.append(line)

f.close()

A=Formula_Tree("","","grammar")
for x in fl:
    if not '#' in x:
        a=A.run(x)
    else:
        a=x

    with open("formulas_razbor.db", 'ab') as filehandle:
            #print(a)
            pickle.dump(a, filehandle)
            pickle.dump('\n',filehandle)
'''

'''
#разбор теоремы (только текст из файла)
a=read_from_file("Temp/in")
A=Text_analyzer(a[1],a[0])
r=A.make_tree()
'''

##визуализация дерева
'''
A=plot_tree(r,"my","test")
A.main("formula")
'''


arr=read_from_file("Temp/razbor3")
for i in range(len(arr)):
    try:
        A=combine_formula_and_text(arr[i],"dicts/formulas_","Temp/out_test")
        A.main()
    except:
        0
        #print(arr[i])
        #break

