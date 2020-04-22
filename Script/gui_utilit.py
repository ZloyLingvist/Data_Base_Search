import tkinter
from tkinter import *
from tkinter import ttk
import os
from tip_tkinter import *

###################

from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from utilities import *
from stamford import *


##################

path = os.path.dirname(os.path.abspath(__file__))

def edit_config():
    f=open("../Files/config.ini","r",encoding="utf-8")
    for line in f:
        T.insert(tkinter.END,line)
    f.close()
    
    button10.pack(padx=10,pady=10)
    button9.pack_forget()
   

def save_config():
    t=T.get(1.0,END)
    f=open("../Files/config.ini","w",encoding="utf-8")
    if len(t)>0:
        f.write(t)
    f.close()
    button9.pack(padx=10,pady=10)
    button10.pack_forget()

def clear():
    T.delete(1.0,END)
    T1.delete(1.0,END)

def create_stamford_corpus():
    f=open("../Files/config.ini","r",encoding="utf-8")
    for line in f:
        line=line.split(":")
        if line[0]=="Stamford_corpus":
            sc=line[1].strip()
            break

    f.close()
    A=Stamford()
    A.write_stamford(sc,sc.strip().replace(".txt","_stamford.txt"),0)
    T1.insert(tkinter.END,"Корпус "+sc+"_stamford.txt создан")


def create_razbor():
    v0=obj.get()
    f=open("../Files/config.ini","r",encoding="utf-8")
    for line in f:
        line=line.split(":")
        if line[0]=="Infile_Abbyy":
            infile=line[1].strip()
            out=line[1].strip().replace(".txt","_out.txt")
        if line[0]=="List_of_formulas":
            lst=line[1].strip()
        if line[0]=="Database_formula_path":
            dfp=line[1].strip()
            
        if line[0]=="Grammar_tatsu_path":
            grammar=line[1].strip()

        if line[0]=="Stamford_corpus":
            infile_stamford=line[1].strip()
            
    f.close()
    if v0=="Формула":
        res=[]
        A=Formula_Tree("","",grammar)
        f=open(dfp,"r",encoding="utf-8")
        for line in f:
            if line!='\n':
                line=line.strip()
                if not "#" in line:
                    try:
                        r=A.run(line)
                    except:
                        r=line
                else:
                    r=line.replace("#","")
                res.append([line,'\n',r])

        f.close()
        
        with open(dfp, 'ab') as filehandle:
            for x in res:
                pickle.dump(x,filehandle)
                pickle.dump('\n',filehandle)
                
        
        
    if v0=="Теорема в формате Abbyy":
        str1=""
        arr=read_from_file(infile)
        for i in range(len(arr)):
            try:
                str1=""
                for k in range(len(arr[i][0])):
                    str1=str1+' '+arr[i][0][k][1]

                A=combine_formula_and_text(arr[i],lst,out,str1,grammar)
                A.main()
            except:
                0
        T1.insert(tkinter.END,"База разборов "+out+" создана",out)

    if v0=="Теорема в формате Стэмфорд":
        A=Stamford()
        v1=var5.get()
        f=open(infile_stamford,"r",encoding="utf-8")
        for line in f:
            if line!='\n':
                line=line.strip()
                if len(line)>0:
                    try:
                        r=A.run(line,v1)
                        B=combine_formula_and_text(r,lst,out,line,grammar)
                        B.main_stamford(r)
                    except:
                        0
                    
                        
                
        f.close()
        T1.insert(tkinter.END,"База разборов "+out+" создана",out)
       
    
m = tkinter.Tk()
m.title("Модуль администрирования")
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

mymenu2.add_checkbutton(label='Синтакс.дерево/Формула логики предикатов(0/1)',variable=var5)
mymenu.add_cascade(label='Параметры разбора',menu=mymenu2)
mymenu.add_command(label='Выйти',command=m.destroy)

pane2 = tkinter.Frame(m)
pane2.pack(fill = "both", expand = "yes")

pane4 = tkinter.Frame(pane2)
pane4.pack(side=RIGHT,fill = "both", expand = "yes")

pane5 = tkinter.Frame(pane2)
pane5.pack(side=BOTTOM)

pane7 = tkinter.Frame(pane1)
pane7.pack(ipadx=10,ipady=10,padx=10,pady=10)


button7 = tkinter.Button(pane7, text='Создать базу разборов',width=25,command=create_razbor)

button7.pack(padx=10,pady=5)

button8 = tkinter.Button(pane6, text='Создать корпус Стэмфорд',width=25,command=create_stamford_corpus)
button8.pack(padx=10,pady=5)

button2 = tkinter.Button(pane1, text='Очистка', width=25, command=clear)
button9 = tkinter.Button(pane1, text='Редактировать config-файл', width=25, command=edit_config)
T1=Text(pane4,width=20,height=20)

w = Label(pane2, text="Теорема")
e=Entry(pane2,width=170)
T=Text(pane2,width=70,height=30)   

w.pack(padx=5,pady=5)
e.pack(ipadx=10,ipady=10,padx=10,pady=10)
T.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)

w8 = Label(pane4, text="Формат рабочих данных:")
w8.pack(padx=5,pady=4)

obj=ttk.Combobox(pane4, 
                            values=[ 
                                    "Теорема в формате Abbyy",
                                    "Формула",
                                    "Теорема в формате Стэмфорд"
                                    ], 
                            )

obj.pack(padx=10,pady=20)

button2.pack(padx=10,pady=10)
button9.pack(padx=10,pady=10)
T1.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)
button10 = tkinter.Button(pane1, text='Сохранить config-файл', width=25, command=save_config)
button10.pack(padx=10,pady=10)
button10.pack_forget()


m.mainloop()

