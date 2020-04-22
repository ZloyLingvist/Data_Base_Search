import os
import tkinter

from tkinter import *
from tkinter import ttk
from tip_tkinter import *

###################

from processing import *
from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from utilities import *
from stamford import *

path = os.path.dirname(os.path.dirname(__file__))
config_file_path=path+"\\Files\\config.ini"
dict_path=path+"\\Files\\"

'''чтобы работало Вырезать+Вставить в окне программы'''
def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

'''Имя в файле конфигурации (параметр Infile)'''

def fill_razbor():
     lst=[]
     f=open(config_file_path,"r",encoding="utf-8")
     for line in f:
            line=line.split(":")
            if line[0]=="Infile":
                infile=line[1].strip()

     f.close()
     v0=obj.get()

     f=open(path+"\\Infile.txt","r",encoding="utf-8")
     for line in f:
            lst.append(preprocessing(line.strip(),path))
     f.close()

     nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,lemma,pos,depparse', models_dir=path, lang="ru",treebank='ru_syntagrus', use_gpu=True, pos_batch_size=3000)
     f=open(path+"\\Infile_arr.txt","w",encoding="utf-8")
     a=[]
     i=0
     for line in lst:
            doc = nlp(line)
            i=0
            a=[]
            for sent in doc.sentences:
                for wrd in sent.dependencies:
                    a.append([str(i+1),wrd[2].text,wrd[2].lemma,str(wrd[2].governor),wrd[2].dependency_relation,wrd[2].upos])
                    i=i+1

            f.write(str(a))
            f.write('\n')
                
     f.close()
     T1.insert(tkinter.END,'Закончил!')

     

def formulas_mode():
    os.system("Script\gui_formula.py")

def admin_mode():
    os.system("Script\gui_utilit.py")

def edit_config():
    f=open(config_file_path,"r",encoding="utf-8")
    for line in f:
        T2.insert(tkinter.END,line)
    f.close()
    
    button10.pack(padx=10,pady=10)
    button9.pack_forget()
   

def save_config():
    t=T2.get(1.0,END)
    f=open(config_file_path,"w",encoding="utf-8")
    if len(t)>0:
        f.write(t)
    f.close()
    button9.pack(padx=10,pady=10)
    button10.pack_forget()

def clear():
    T.delete(1.0,END)
    T1.delete(1.0,END)



def main_transform():
    import sys
    #try:
    transform()
    #except Exception as e:    
        #e_type, e_val, e_tb = sys.exc_info()
        #T1.insert(tkinter.END,str(e_type)+"\n"+str(e_val)+"\n")
      
    
def transform():
    T1.delete(1.0,END)
    text=in_entry.get()
   
    f=open(config_file_path,"r",encoding="utf-8")
    for line in f:
        line=line.split(":")
        if line[0]=="Grammar_tatsu_path":
            grammar=path+"\\"+line[1].strip()
        if line[0]=="Infile_Abbyy":
            abbyy_infile=path+"\\"+line[1].strip()
        if line[0]=="List_of_formulas":
            list_of_formulas=path+"\\"+line[1].strip()
        if line[0]=="Infile":
            infile=path+"\\"+line[1].strip()

    f.close()
    v0=obj.get()

    if (v0=="Стэмфорд (текст)" or v0=="Стэмфорд (массив)"):
        '''считываем откуда считывать'''
        v=var9.get()
       
        if len(text)>0 and v==0:
            A=Stamford()
            r=A.main(preprocessing(text,path),var2.get())
            r=combine_formula_and_text(r,path)
           
            T.insert(tkinter.END,text+'\n')
            T.insert(tkinter.END,str(r))
            T.insert(tkinter.END,'\n\n')
            r=make_predicate_form_main(r)
            T.insert(tkinter.END,r)
            T.insert(tkinter.END,'\n\n')
            
        if v==1:
            lst=[]
            if (v0=="Стэмфорд (текст)"):
                f=open(infile,"r",encoding="utf-8")
                for line in f:
                    lst.append(line.strip())

                f.close()

            if (v0=="Стэмфорд (массив)"):
                f=open(infile.split(".")[0]+"_arr.txt","r",encoding="utf-8")
                for line in f:
                    lst.append(line.strip())

                f.close()

            A=Stamford()
            for i in range(len(lst)):
                if v0=="Стэмфорд (текст)":
                    r=A.main(lst[i],var2.get())

                if (v0=="Стэмфорд (массив)"):
                    r=A.main(eval(lst[i]),var2.get())

                r=combine_formula_and_text(r,path)
                       
                T.insert(tkinter.END,lst[i]+'\n')
                T.insert(tkinter.END,str(r))
                T.insert(tkinter.END,'\n\n')
                r=make_predicate_form_main(r)
                T.insert(tkinter.END,r)
                T.insert(tkinter.END,'\n\n')
            

    if v0=="Теорема в формате Abbyy":
        f=open(abbyy_infile,"r",encoding="utf-8")
        line=f.read()
        a=line.split('\n')
        st=""

        for i in range(len(a)):
            if len(a[i].split('\t'))>1:
                st=st+a[i].split('\t')[1]+" "
        f.close()
        
        T.insert(tkinter.END,st)
        T.insert(tkinter.END,'\n\n')

        arr=read_from_file(abbyy_infile)
        
        for k in range(len(arr)):
            if len(arr[k])>0:
                A=combine_formula_and_text(arr[k],list_of_formulas,"","",grammar)
                r=A.main(var2.get())
    
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
    text=in_entry.get()
    v0=obj.get()
    text=T.get(1.0,END)
    arr=text.split('\n')

    try:
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
        img = PhotoImage(file=path+'\\Tree\\at1.png')
        label=Label(t,image=img)
        label.image=img
        label.pack()
        v0=var5.get()
        if v0==1:
            os.startfile(path+'\\Tree\\at1.png')

    except Exception as e:    
        e_type, e_val, e_tb = sys.exc_info()
        T1.insert(tkinter.END,str(e_type)+"\n"+str(e_val)+"\n")
            
    
def range_function():
    formula=in_entry.get()
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
    f=open(config_file_path,"r",encoding="utf-8")
    for line in f:
        line=line.split(":")
        if line[0]=="Grammar_tatsu_path":
            grammar=line[1].strip()
        if line[0]=="Infile_Abbyy":
            abbyy_infile=line[1].strip()
        if line[0]=="List_of_formulas":
            list_of_formulas=line[1].strip()
        if line[0]=="Database_abbyy_path":
            Database_abbyy_path=line[1].strip()
        if line[0]=="Database_stamford_path":
            Database_stamford_path=line[1].strip()
        if line[0]=="Amount_ranger_answer":
            amount=int(line[1])

    f.close()

    if obj.get()!="":
        top=[]
        ### считывание базы
        database=[]
        db=""
            
        if obj.get()=="Теорема в формате Abbyy":
            db=Database_abbyy_path
            
        if obj.get()=="Стэмфорд (текст)" or obj.get()=="Стэмфорд (массив)" :
            db=Database_stamford_path
        
            
        with open(db,"rb") as fileOpener:
            while True:
                try:
                    database.append(pickle.load(fileOpener))
                except EOFError:
                    break

        ###### считываем файл

        text=in_entry.get()
        if obj.get()=="Теорема в формате Abbyy":
            arr=read_from_file(abbyy_infile)
            str1=""
            for x in arr[0][0]:
               str1=str1+' '+x[1]
       
            A=combine_formula_and_text(arr[0],list_of_formulas,"","",grammar)
            a=A.main(var2.get())

        if obj.get()=="Стэмфорд (текст)":
            A=Stamford()
            a=A.main(text,var2.get())

        if obj.get()=="Стэмфорд (массив)":
            text=T.get(1.0,END).strip()
            A=Stamford()
            a=A.main(eval(text),var2.get())

       

        if obj.get()=="Разобранное дерево":
            text=T.get(1.0,END)
            a=text.split('\n')
            str1=""

            for i in range(len(a)):
                if a[i].strip()!="":
                    a[i]=eval(a[i])

            for i in range(len(a)-1,-1,-1):
                if len(a[i])==0:
                    del a[i]

            arr=a

        mode=0
        if obj2.get()=="":
            T1.insert(tkinter.END,'Использован режим по умолчанию (Свой алгоритм (v1))')
            
        if obj2.get()=="Свой алгоритм (v1)":
            mode=0
        if obj2.get()=="Minhash":
            mode=1

        if obj2.get()=="Свой алгоритм (v2)":
            mode=2
           
        B=Ranger()
        ####### ранжировка #######
        
        for i in range(len(database)):
            if len(database[i])>1:
                result=B.main(a,database[i][2],mode)
                top.append([i,result,database[i][0]])

        if mode==0 or mode==1:
            top.sort(key = lambda x: x[1],reverse=True)
        if mode==1:
            top.sort(key = lambda x: x[1],reverse=False)

        T.insert(tkinter.END,'Query:'+text+'\n\n')
        T.insert(tkinter.END,str(a)+'\n\n')
        
        for i in range(amount):
            T.insert(tkinter.END,str(i+1)+" "+str(top[i][0])+" "+str(top[i][1])+'\n\n')
            T.insert(tkinter.END,database[top[i][0]][0])
            T.insert(tkinter.END,'\n\n')
            T.insert(tkinter.END,str(database[top[i][0]][2]))
            T.insert(tkinter.END,'\n\n')

        T.insert(tkinter.END,'\n\n')
        

    
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
    if obj.get()=="Стэмфорд (текст)" or obj.get()=="Стэмфорд (массив)":
        w["text"]="Теорема"
        T.pack_forget()
        w.pack(padx=5,pady=5)
        in_entry.pack(ipadx=10,ipady=10,padx=10,pady=10)
        T["width"]=70
        T.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)
        
      
        
    if obj.get()=="Теорема в формате Abbyy":
        w.pack_forget()
        in_entry.pack_forget()
        T["width"]=170
        
    if obj.get()=="Разобранное дерево":
        w.pack_forget()
        in_entry.pack_forget()
        T["width"]=170
       


m = tkinter.Tk()
m.title("Pr version 1")
m.bind_all("<Key>", _onKeyRelease, "+")
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
var9 = tkinter.IntVar()

var5.set(1)
var2.set(1)
var9.set(1)

mymenu2.add_checkbutton(label='Показать дерево при помощи ОС',variable=var5)
mymenu2.add_checkbutton(label='Синтакс.дерево/Формула логики предикатов(0/1)',variable=var2)
mymenu2.add_checkbutton(label='Загрузить из файла',variable=var9)
mymenu.add_cascade(label='Параметры разбора',menu=mymenu2)
mymenu3.add_command(label='Работа с формулами',command=formulas_mode)
mymenu3.add_command(label='Режим разработчика',command=admin_mode)
mymenu.add_cascade(label='Режимы',menu=mymenu3)
mymenu.add_command(label='Выйти',command=m.destroy)

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

button9 = tkinter.Button(pane7, text='Ранжирование разборов', width=25, command=range_function_r)

button9.pack(padx=10,pady=5)

button2 = tkinter.Button(pane1, text='Очистка', width=25, command=clear)
button3 = tkinter.Button(pane1, text='Показать дерево', width=25, command=create_window)
button6 = tkinter.Button(pane1, text='Установка библиотек', width=25, command=install)
button4 = tkinter.Button(pane7, text='СДЕЛАТЬ РАЗБОР', width=25, command=main_transform)

T1=Text(pane4,width=20,height=20)

w = Label(pane2, text="Теорема")
in_entry=Entry(pane2,width=170)

w.pack(padx=5,pady=5)
in_entry.pack(ipadx=10,ipady=10,padx=10,pady=10)

'''
'''

T=Text(pane2,width=70,height=30)  
T.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)

w8 = Label(pane4, text="Режим ввода:")
w8.pack(padx=5,pady=4)

obj=ttk.Combobox(pane4, 
                            values=[ 
                                    "Теорема в формате Abbyy",
                                    "Стэмфорд (текст)",
                                    "Стэмфорд (массив)",
                                    "Разобранное дерево"
                                    ], 
                            )

obj.bind("<<ComboboxSelected>>", changemode)


obj2=ttk.Combobox(pane7, 
                            values=[ 
                                    "Свой алгоритм (v1)",
                                    "Minhash",
                                    "Свой алгоритм (v2)"
                                    ], 
                            )



obj.pack(padx=10,pady=20)
obj2.pack(padx=10,pady=20)


button2.pack(padx=10,pady=10)  
button3.pack(padx=10,pady=10)
button4.pack(padx=10,pady=10)
button6.pack(padx=10,pady=10)
T1.pack(fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)

button9 = tkinter.Button(pane1, text='Редактировать config-файл', width=25, command=edit_config)
button9.pack(padx=10,pady=10)
button10 = tkinter.Button(pane1, text='Сохранить config-файл', width=25, command=save_config)
button10.pack(padx=10,pady=10)

button11 = tkinter.Button(pane1, text='Заполнить файл с разборами', width=25, command=fill_razbor)
button11.pack(padx=10,pady=10)

button10.pack_forget()
m.mainloop()

