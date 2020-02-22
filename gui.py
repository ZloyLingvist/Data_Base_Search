import tkinter
from tkinter import *
from tkinter import ttk
import pickle
import os
from dicts.script import *

###################

from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from combine_formula_text import *
from utilities import *


##################

path = os.path.dirname(os.path.abspath(__file__))

def clear():
    T.delete(1.0,END)
    T1.delete(1.0,END)

def help_1():
    T.delete(1.0,END)
    s=""
    help_list1=['Параметры:',
               '-- Чтение теоремы из файла - Разбор, указанный в файле с именем из поля Файл с теоремой при нажатии на кнопку СДЕЛАТЬ РАЗБОР будет преобразован в дерево разбора',
               'Справка - информация о программе',
               'Выйти - выход из программы']

    for i in range(len(help_list1)):
        s=s+' \n\n'+help_list1[i]

    T1.insert(tkinter.END,s)


def help_2():
    T.delete(1.0,END)
    s=""
    help_list2=['Кнопки:',
                'Очистка - очистка информационного и основного полей программы',
                'Показать дерево \n - заполнено поле Теорема и включен параметр Stanford - будет показано синт. дерево '+
                'предложения, введенного в поле Теорема \n включен параметр Abbyy (по умолчанию) - будет показано дерево разбора из файла с именем из поля имя файла (Abbyy)'+
                'если включен параметр показать дерево при помощи ОС программа постарается открыть изображение при помощи ОС',
                'Формула - будет показано дерево формулы, введенной в поле Формула ']

    for i in range(len(help_list2)):
        s=s+' \n\n'+help_list2[i]

    T1.insert(tkinter.END,s)

def predicate_work():
    text=e3.get()
    if len(text)==0:
        T1.insert(tkinter.END,'Введите теорему!')
    else:
        T.insert(tkinter.END,main_of_module(text))

def main_transform():
    import sys
    try:
        transform()
    except Exception as e:    
        e_type, e_val, e_tb = sys.exc_info()
        T1.insert(tkinter.END,str(e_type)+"\n"+str(e_val)+"\n")
      
    
def transform():
    T1.delete(1.0,END)
    text=e.get()
    text4=e4.get()

    v0=obj.get()
    if len(text)>0 and v0=="Формула": ##разбор формул
        A=Formula_Tree("","","grammar")
        T.insert(tkinter.END,str(A.run(text)))

    if len(text)>0 and (v0=="Теорема" or v0=="Дерево разбора"):
        T.insert(tkinter.END,'В процессе разработки')

    if v0=="Теорема в формате Abbyy":
        f=open(e5.get()+'.txt',"r",encoding="utf-8")
        line=f.read()
        a=line.split('\n')
        st=""

        for i in range(len(a)):
            if len(a[i].split('\t'))>1:
                st=st+a[i].split('\t')[1]+" "
        f.close()
        
        T.insert(tkinter.END,st)
        T.insert(tkinter.END,'\n\n')

        arr=read_from_file(e5.get())
        
        for k in range(len(arr)):
            if len(arr[k])>0:
                A=combine_formula_and_text(arr[k],"dicts/formulas_","")
                r=A.main()
    
                T.insert(tkinter.END,str(r))
                T.insert(tkinter.END,'\n\n')

        T.insert(tkinter.END,'\n\n')
        
              

def main_create_window():
    import sys
    T1.delete(1.0,END)
    try:
        create_window()
    except Exception as e:
        e_type, e_val, e_tb = sys.exc_info()
        T1.insert(tkinter.END,str(e_type)+"\n"+str(e_val))

        
    
def create_window(): ####делаем картинку
    text=e.get()
    v0=obj.get()

    if len(text)>0 and v0=="Теорема": ##включен стэнфорд
        0
        '''
        from predicate_module.module_3 import syntax_procedure
        a=syntax_procedure(text,path+"\\predicate_module")
        drawgraph(a[0],"t1",text,1)
        t = Toplevel()
        img = PhotoImage(file='Trees/t1.png')
        label=Label(t,image=img)
        label.image=img
        label.pack()
        '''

    if len(text)>0 and v0=="Формула": ##разбор формул
        A=Formula_Tree("","","grammar")
        a=A.run(text)

        A=plot_tree(a,"f1",text)
        A.main("formula")

        t = Toplevel()
        img = PhotoImage(file='Trees/f1.png')
        label=Label(t,image=img)
        label.image=img
        label.pack()

    if v0=="Теорема в формате Abbyy":
        text=T.get(1.0,END)
        arr=text.split('\n')
        for i in range(len(arr)-1,-1,-1):
            if arr[i].strip()=="":
                del arr[i]
                
        for i in range(len(arr)-1,-1,-1):
            if i%2==1:
                arr[i]=eval(arr[i])
            else:
                del arr[i]
            

        A=plot_tree(arr[0],"at1",text)
        A.main("formula")
        
        t = Toplevel()
        img = PhotoImage(file='Trees/at1.png')
        label=Label(t,image=img)
        label.image=img
        label.pack()
        v0=var5.get()
        if v0==1:
            os.startfile(path+'\\Trees\\at1.png')
            

    
               
    

def sub_create_db(name,p):
     f=open("Temp/"+name+".txt", 'w')
     f.close()
     f=open("Temp/"+name+"_formula.txt","r",encoding="utf-8")
     task_list=[]
    
     for line in f:
        task_list.append(line.strip('\n'))
     f.close()

     res=[]
     for i in range(len(task_list)):
         if task_list[i]!="":
             res.append(main_converter(task_list[i],0))

     if p==0:
         with open("Temp/"+name+".db", 'wb') as filehandle:
             pickle.dump(res, filehandle)

     if p==1:
          with open("Temp/"+name+".db", 'ab') as filehandle:
             pickle.dump(res, filehandle)

     

def create_db():
    str1=T.get(1.0,END)
    str2=str1.split('\n')
    f=open('Temp/'+e2.get()+'_formula.txt','w',encoding="utf-8")
    for i in range(len(str2)):
        f.write(str2[i]+'\n')

    f.close()
    sub_create_db(e2.get(),0)

    T1.insert(tkinter.END,'\nБаза данных '+e2.get()+'_formula создана')


def create_db_razbor():
    text=T.get(1.0,END)
    arr=text.split('\n')
    for i in range(len(arr)):
        if arr[i].strip()!="":
            arr[i]=eval(arr[i])

    for i in range(len(arr)-1,-1,-1):
        if len(arr[i])==0:
            del arr[i]
        
    with open('Temp/'+e2.get()+'_razbor.db', 'wb') as filehandle:
         pickle.dump(arr, filehandle)

    T1.insert(tkinter.END,'\nБаза данных '+e2.get()+'_razbor создана')


def add_db_f():
    str1=T.get(1.0,END)
    str2=str1.split('\n')
    f=open('Temp/'+e2.get()+'_formula.txt','a',encoding="utf-8")
    for i in range(len(str2)):
        f.write(str2[i]+'\n')

    f.close()
    sub_create_db(e2.get(),1)

    T1.insert(tkinter.END,'\nФормула добавлена в базу данных '+e2.get()+'_formula')
    

def add_db_r():
    text=T.get(1.0,END)
    arr=text.split('\n')
    for i in range(len(arr)):
        if arr[i].strip()!="":
            arr[i]=eval(arr[i])

    for i in range(len(arr)-1,-1,-1):
        if len(arr[i])==0:
            del arr[i]
        
    with open('Temp/'+e2.get()+'_razbor.db', 'ab') as filehandle:
         pickle.dump(arr, filehandle)

    T1.insert(tkinter.END,'\nРазбор добавлен в базу разборов '+e2.get()+'_razbor')
    
            
def sub_range(formula,mode,varstate):
    a=main_converter(formula,0)
    T.insert(tkinter.END,'Тестируемая формула: '+formula+'\n'+str(a)+'\n')
    T.insert(tkinter.END,'\n')

    res=main_test(a,e2.get(),e2.get()+"_formula",varstate)
    if mode==0:
        k=0
        T.insert(tkinter.END,str(k+1)+" "+res[k][0]+" "+str(res[k][2])+"\n"+str(res[k][1])+"\n")
        T.insert(tkinter.END,'\n')
    else:  
        for k in range(len(res)):
            if k<5:
                T.insert(tkinter.END,str(k+1)+" "+res[k][0]+" "+str(res[k][2])+"\n"+str(res[k][1])+"\n")
                T.insert(tkinter.END,'\n')
            else:
                T.insert(tkinter.END,str(k+1)+" "+res[k][0]+" "+str(res[k][2])+"\n")
                T.insert(tkinter.END,'\n')

    
def range_function():
    formula=e.get()
    if len(formula)>0:
        sub_range(formula,1,0)
    else:
        f2=T1.get(1.0,END)
        if len(f2)>0:
           f2=f2.split('\n')
           for k in range(len(f2)):
               sub_range(f2[k],0,0)
        else:   
            T1.insert(tkinter.END,'Формула не введена')

def range_function_r():
    abb_text=e5.get()
    
    if obj.get()=="Теорема в формате Abbyy":
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
        arr=read_from_file("Test/"+abb_text)
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

        T.insert(tkinter.END,'Query:'+str1+'\n\n')
        T.insert(tkinter.END,str(arr)+'\n\n')
        
        for i in range(10):
            T.insert(tkinter.END,str(i+1)+" "+str(top[i][0])+" "+str(top[i][1])+'\n\n')
            T.insert(tkinter.END,database[top[i][0]][0])
            T.insert(tkinter.END,'\n\n')
            T.insert(tkinter.END,str(database[top[i][0]][2]))
            T.insert(tkinter.END,'\n\n')

        T.insert(tkinter.END,'\n\n')
        

      
    if obj.get()=="Разобранное дерево":
        text=T.get(1.0,END)
        arr=text.split('\n')

        for i in range(len(arr)):
            if arr[i].strip()!="":
                arr[i]=eval(arr[i])

        for i in range(len(arr)-1,-1,-1):
            if len(arr[i])==0:
                del arr[i]

        
    ############################

    T.insert(tkinter.END,'\n')


def install():
     T1.insert(tkinter.END,'Установка tatsu')
     os.system("pip install tatsu")
     T1.insert(tkinter.END,'Установка torch')
     os.system("pip install --no-cache-dir torch==1.2.0+cpu torchvision==0.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html")
     T1.insert(tkinter.END,'Установка stanfordnlp')
     os.system("pip install stanfordnlp")


def changemode(event):
    if obj.get()=="Теорема":
        w["text"]="Теорема"
        T.pack_forget()
        w.pack(padx=5,pady=5)
        e.pack(ipadx=10,ipady=10,padx=10,pady=10)
        T["width"]=70
        T.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)
        label2.pack_forget()
        e4.pack_forget()
        label3.pack_forget()
        e5.pack_forget()
        
    if obj.get()=="Теорема в формате Abbyy":
        w.pack_forget()
        e.pack_forget()
        T["width"]=170
        label2.pack(side="left")
        e4.pack(side="left",ipady=10,pady=10,padx=5)
        label3.pack(side="left")
        e5.pack(side="left",ipady=10,pady=10,padx=5)

    if obj.get()=="Формула":
        w["text"]="Формула"
        T.pack_forget()
        w.pack(padx=5,pady=5)
        e.pack(ipadx=10,ipady=10,padx=10,pady=10)
        T["width"]=70
        T.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)
        label2.pack_forget()
        e4.pack_forget()
        label3.pack_forget()
        e5.pack_forget()
        

    if obj.get()=="Разобранное дерево":
        w.pack_forget()
        e.pack_forget()
        T["width"]=170
        label2.pack_forget()
        e4.pack_forget()
        label2.pack(side="left")
        e4.pack(side="left",ipady=10,pady=10,padx=5)


m = tkinter.Tk()
m.title("Pr version 1")
pane1 = tkinter.Frame(m)
pane1.pack(side=LEFT)


pane6 = tkinter.Frame(pane1)
pane6.pack(ipadx=10,ipady=10,padx=10,pady=10)

w8 = Label(pane6, text="Работа с формулами:")
w8.pack(ipady=5,pady=5)

mymenu = tkinter.Menu(m)
m.config(menu=mymenu)

mymenu2 = tkinter.Menu(m,tearoff=0)
mymenu3 = tkinter.Menu(m,tearoff=0)

var3 = tkinter.IntVar()
var5 = tkinter.IntVar()
var2 = tkinter.IntVar()

var5.set(1)
var2.set(1)

mymenu2.add_checkbutton(label='Показать дерево при помощи ОС',variable=var5)
#mymenu3.add_command(label='Параметры',command=help_1)
#mymenu3.add_command(label='Кнопки',command=help_2)

#mymenu.add_cascade(label='Справка',menu=mymenu3)
#mymenu.add_cascade(label='Параметры',menu=mymenu2)
#mymenu.add_command(label='Выйти',command=m.destroy)

pane2 = tkinter.Frame(m)
pane2.pack(fill = "both", expand = "yes")

pane4 = tkinter.Frame(pane2)
pane4.pack(side=RIGHT,fill = "both", expand = "yes")

pane5 = tkinter.Frame(pane2)
pane5.pack(side=BOTTOM)

pane7 = tkinter.Frame(pane1)
pane7.pack(ipadx=10,ipady=10,padx=10,pady=10)
w9 = Label(pane7, text="Работа с текстом и формулами:")
w9.pack(ipady=5,pady=5)

#button7 = tkinter.Button(pane7, text='Создать базу разборов',width=25,command=create_db_razbor)
#button8 = tkinter.Button(pane7, text='Добавить в базу разборов',width=25,command=add_db_r)
button9 = tkinter.Button(pane7, text='Ранжирование разборов', width=25, command=range_function_r)

#button7.pack(padx=10,pady=5)
#button8.pack(padx=10,pady=5)
button9.pack(padx=10,pady=5)


#button0 = tkinter.Button(pane6, text='Создать базу формул',width=25,command=create_db)
#button5 = tkinter.Button(pane6, text='Добавить в базу формул',width=25,command=add_db_f)
button1 = tkinter.Button(pane6, text='Ранжирование формул', width=25, command=range_function)

button2 = tkinter.Button(pane1, text='Очистка', width=25, command=clear)
button3 = tkinter.Button(pane1, text='Показать дерево', width=25, command=create_window)
button6 = tkinter.Button(pane1, text='Установка библиотек', width=25, command=install)
button4 = tkinter.Button(pane7, text='СДЕЛАТЬ РАЗБОР', width=25, command=main_transform)
T1=Text(pane4,width=20,height=20)

#button0_ttp = CreateToolTip(button0, 'Перед нажатием вставить формулы в основное окно программы')
#button7_ttp = CreateToolTip(button7,'Перед нажатием в параметрах поставить галочку Чтение теоремы из файла. Затем Преобразовать, чтобы в основном окне появились результаты разбора.')
button9_ttp = CreateToolTip(button9,'Разбор, находящийся в файле с именем из поля Файл с теоремой берется как основной и сравнивается с разборами из файла с именем из поля База данных')
button1_ttp = CreateToolTip(button1, 'Перед нажатием отключить параметр Чтение теоремы из файла и ввести формулу в поле Формула')
button3_ttp = CreateToolTip(button3, 'Если включен параметр Дерево формулы будет показана формула')

w = Label(pane2, text="Теорема")
e=Entry(pane2,width=170)
T=Text(pane2,width=70,height=30)   

w.pack(padx=5,pady=5)
e.pack(ipadx=10,ipady=10,padx=10,pady=10)
T.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)

w8 = Label(pane4, text="Режим ввода:")
w8.pack(padx=5,pady=4)

obj=ttk.Combobox(pane4, 
                            values=[ 
                                    "Теорема в формате Abbyy",
                                    "Формула",
                                    ], 
                            )

obj.bind("<<ComboboxSelected>>", changemode)


obj.pack(padx=10,pady=20)
#button0.pack(padx=10,pady=5)
#button5.pack(padx=10,pady=10)
button1.pack(padx=10,pady=5)


e2=Entry(pane5,width=8)
label1=tkinter.Label(pane5,text="База данных:",height=4)
label1.pack(side="left")
e2.pack(side="left",ipady=10,pady=10,padx=5)
e2.insert(0,'db')

e4=Entry(pane5,width=8)
label2=tkinter.Label(pane5,text="Файл с теоремой:",height=4)
label2.pack(side="left")
label2.pack_forget()

e4.pack(side="left",ipady=10,pady=10,padx=5)
e4.insert(0,'1')
e4.pack_forget()

e5=Entry(pane5,width=8)
label3=tkinter.Label(pane5,text="Имя файла (Abbyy):",height=4)
label3.pack(side="left")
label3.pack_forget()
e5.pack(side="left",ipady=10,pady=10,padx=5)
e5.insert(0,'in')
e5.pack_forget()

button2.pack(padx=10,pady=10)  
button3.pack(padx=10,pady=10)
button4.pack(padx=10,pady=10)
button6.pack(padx=10,pady=10)
T1.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)

m.mainloop()

