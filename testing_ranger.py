import pickle
from ranger import *
from combine_formula_text import *

def ranger_test(filename,amount):
    top=[]
    ### считывание базы
    database=[]
    with open("Temp/new_test.db","rb") as fileOpener:
        while True:
            try:
                database.append(pickle.load(fileOpener))
            except EOFError:
                break

    ###### считываем файл
    arr=read_from_file("Test/"+filename)
    str1=""
    for x in arr[0][0]:
       str1=str1+' '+x[1]
       
    A=combine_formula_and_text(arr[0],"dicts/formulas_","","")
    a=A.main()

    B=Ranger()
    ####### ранжировка #######
    
    for i in range(len(database)):
        if len(database[i])>1:
            result=B.main(a,database[i][2])
            top.append([i,result,database[i][0]])

    top.sort(key = lambda x: x[1],reverse=True)

    print('Query',str1)
    for i in range(amount):
        print(str(i+1),top[i][0],top[i][1],'\n',database[top[i][0]][0],database[top[i][0]][2])
        print()
    
    

def compare(filename1,filename2):
    arr=read_from_file("Temp/"+filename1)
    A=combine_formula_and_text(arr[0],"dicts/formulas_","")
    a=A.main()

    brr=read_from_file("Temp/"+filename2)
    B=combine_formula_and_text(brr[0],"dicts/formulas_","")
    b=B.main()

    print(a)
    print(b)
    
#compare("in","in2")
ranger_test("in",5)
    



