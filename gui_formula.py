import tkinter
from tkinter import *
from tkinter import ttk
import pickle
import os
from Files.tip_tkinter import *
import datetime


###################

from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from combine_formula_text import *
from utilities import *

import sys
##################

path = os.path.dirname(os.path.abspath(__file__))

def edit_config():
    f=open("Files/config.ini","r",encoding="utf-8")
    for line in f:
        T.insert(tkinter.END,line)
    f.close()
    
    button10.pack(padx=10,pady=10)
    button9.pack_forget()
   

def save_config():
    t=T.get(1.0,END)
    f=open("Files/config.ini","w",encoding="utf-8")
    if len(t)>0:
        f.write(t)
    f.close()
    button9.pack(padx=10,pady=10)
    button10.pack_forget()
    T1.insert(tkinter.END,"Файл-конфигурации обновлен\n")

def save_result():
    t=T.get(1.0,END)
    name_of_file=Temporary_path+"/save_"+str(datetime.datetime.now().strftime("%H_%M_%S"))+".txt"
    f=open(name_of_file,"w",encoding="utf-8")
    f.write(str(t))
    f.close()
    T1.insert(tkinter.END,"В файл "+name_of_file+" добавлена запись"+"\n")
   

def clear():
    T.delete(1.0,END)
    T1.delete(1.0,END)

def main_transform():
    import sys
    try:
        transform()
    except Exception as e:    
        e_type, e_val, e_tb = sys.exc_info()
        T1.insert(tkinter.END,str(e_type)+"\n"+str(e_val)+"\n")
      
    
def transform():
    T1.delete(1.0,END)
    text=formula_entry.get()
   
    if len(text)>0: ##разбор формул
        A=Formula_Tree("","",Grammar_tatsu_path)
        T.insert(tkinter.END,str(A.run(text)))
    else:
        T1.insert(tkinter.END,"Поле для ввода пусто\n")
        


def main_create_window():
    T1.delete(1.0,END)
    try:
        create_window()
    except Exception as e:
        e_type, e_val, e_tb = sys.exc_info()
        T1.insert(tkinter.END,str(e_type)+"\n"+str(e_val))

def razbor_f():
    try:
        f=open(Infile_formulas,"r",encoding="utf-8")
        A=Formula_Tree("","",Grammar_tatsu_path)
        for line in f:
            text=line.strip()
            if len(text.strip())>0:
                a=A.run(text)
                T.insert(tkinter.END,line+str(a)+"\n\n")
        f.close()
    except Exception as e:
        e_type, e_val, e_tb = sys.exc_info()
        T1.insert(tkinter.END,str(e_type)+"\n"+str(e_val))
    
    
def create_window(): ####делаем картинку
    text=formula_entry.get()
    if len(text)>0: ##разбор формул
        A=Formula_Tree("","",Grammar_tatsu_path)
        a=A.run(text)

        A=plot_tree(a,"f1",text)
        A.main("formula")

        t = Toplevel()
        img = PhotoImage(file='Trees/f1.png')
        label=Label(t,image=img)
        label.image=img
        label.pack()
    else:
        T1.insert(tkinter.END,"Поле для ввода пусто\n")

               
def sub_range(formula,mode):
    A=Formula_Tree("","",Grammar_tatsu_path)
    a=A.run(formula)

    T.insert(tkinter.END,'Тестируемая формула: '+formula+'\n'+str(a)+'\n')
    T.insert(tkinter.END,'\n')

    B=Ranger()
    ### считывание базы
    database=[]
    with open(Database_formula_path,"rb") as fileOpener:
        while True:
            try:
                database.append(pickle.load(fileOpener))
            except EOFError:
                break
            
    ####### ранжировка #######
    for i in range(len(database)):
        if len(database[i])>1:
            result=B.main(a,database[i][2])
            top.append([i,result,database[i][0]])

    top.sort(key = lambda x: x[1],reverse=True)

    T.insert(tkinter.END,'Query:'+str1+'\n\n')
    T.insert(tkinter.END,str(a)+'\n\n')
        
    for i in range(Amount_ranger_answer):
        T.insert(tkinter.END,str(i+1)+" "+str(top[i][0])+" "+str(top[i][1])+'\n\n')
        T.insert(tkinter.END,database[top[i][0]][0])
        T.insert(tkinter.END,'\n\n')
        T.insert(tkinter.END,str(database[top[i][0]][2]))
        T.insert(tkinter.END,'\n\n')

    T.insert(tkinter.END,'\n\n')

    
def range_function():
    try:
        formula=formula_entry.get()
        if len(formula)>0:
            sub_range(formula,1)
        else:
            T1.insert(tkinter.END,'Формула не введена')
    except Exception as e:    
        e_type, e_val, e_tb = sys.exc_info()
        T1.insert(tkinter.END,str(e_type)+"\n"+str(e_val)+"\n")

def install():
     T1.insert(tkinter.END,'Установка tatsu')
     os.system("pip install tatsu")

##### считывание ####
Database_formula_path=""
Grammar_tatsu_path=""
Amount_ranger_answer=""

f=open("Files/config.ini","r",encoding="utf-8")
for line in f:
    line=line.split(":")
    if line[0]=="Database_formula_path":
        Database_formula_path=line[1].strip()
    if line[0]=="Grammar_tatsu_path":
        Grammar_tatsu_path=line[1].strip()
    if line[0]=="Amount_ranger_answer":
        Amount_ranger_answer=int(line[1].strip())
    if line[0]=="Infile_formulas":
        Infile_formulas=line[1].strip()
    if line[0]=="Temporary_path":
        Temporary_path=line[1].strip()
    
f.close()


m = tkinter.Tk()
m.title("Модуль работы с формулами")
pane1 = tkinter.Frame(m)
pane1.pack(side=LEFT)

pane6 = tkinter.Frame(pane1)
pane6.pack(ipadx=10,ipady=10,padx=10,pady=10)

mymenu = tkinter.Menu(m)
m.config(menu=mymenu)

mymenu2 = tkinter.Menu(m,tearoff=0)
mymenu3 = tkinter.Menu(m,tearoff=0)

var3 = tkinter.IntVar()
var5 = tkinter.IntVar()
var2 = tkinter.IntVar()

var5.set(1)
var2.set(1)

mymenu.add_command(label='Выйти',command=m.destroy)

pane2 = tkinter.Frame(m)
pane2.pack(fill = "both", expand = "yes")

pane4 = tkinter.Frame(pane2)
pane4.pack(side=RIGHT,fill = "both", expand = "yes")

button1 = tkinter.Button(pane1, text='Ранжирование формул', width=25, command=range_function)
button2 = tkinter.Button(pane1, text='Очистка', width=25, command=clear)
button3 = tkinter.Button(pane1, text='Показать дерево', width=25, command=create_window)
button6 = tkinter.Button(pane1, text='Установка библиотек', width=25, command=install)
button4 = tkinter.Button(pane1, text='Разбор формулы', width=25, command=main_transform)

T1=Text(pane4,width=20,height=20)

pane5 = tkinter.Frame(pane4)
pane5.pack(ipadx=10,ipady=5,padx=10,pady=5)

pane51 = tkinter.Frame(pane4)
pane51.pack(ipadx=10,ipady=5,padx=10,pady=5)

w2 = Label(pane4, text="Информационное окно")
w2.pack(padx=5,pady=5)

w = Label(pane2, text="Формула")
formula_entry=Entry(pane2,width=170)
T=Text(pane2,width=70,height=30)   

w.pack(padx=5,pady=5)
formula_entry.pack(ipadx=10,ipady=10,padx=10,pady=10)
T.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)

button1.pack(padx=10,pady=5)

button2.pack(padx=10,pady=10)  
button3.pack(padx=10,pady=10)
button4.pack(padx=10,pady=10)
button6.pack(padx=10,pady=10)
T1.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)
button9 = tkinter.Button(pane1, text='Редактировать config-файл', width=25, command=edit_config)
button9.pack(padx=10,pady=10)
button10 = tkinter.Button(pane1, text='Сохранить config-файл', width=25, command=save_config)
button10.pack(padx=10,pady=10)
button11 = tkinter.Button(pane1, text='Разобрать формулы из файла', width=25, command=razbor_f)
button11.pack(padx=10,pady=10)
button12 = tkinter.Button(pane1, text='Сохранить результат', width=25, command=save_result)
button12.pack(padx=10,pady=10)
button10.pack_forget()

m.mainloop()

