from tkinter import *
from gui_function import *
import os

path = os.path.dirname(os.path.dirname(__file__))

def rank():
    try:
        text=in_entry.get(1.0,END)
        if text[0]=="[":
             text=eval(text.strip())
        else:
             text=text.strip()

        text=make_razbor(text)
        query,ranking_arr=make_ranking(text)
        in_entry_mid_left.insert(END,str(query))
        in_entry_mid_left.insert(END,'\n')
        
        for i in range(len(ranking_arr)):
             in_entry_mid_left.insert(END,str(ranking_arr[i][0])+'\t'+str(ranking_arr[i][1]))
             in_entry_mid_left.insert(END,'\n')

             in_entry_mid_right.insert(END,str(ranking_arr[i][2]))
             in_entry_mid_right.insert(END,'\n\n')    
    except:
        e_type, e_val, e_tb = sys.exc_info()
        in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")
    
def clean():
    in_entry.delete(1.0,END)
    in_entry_mid_left.delete(1.0,END)
    in_entry_mid_right.delete(1.0,END)
     
def razbor():
    clean()
    formula_text=""
    try:
        text=in_entry.get(1.0,END)
        if text[0]=="[":
             text=eval(text.strip())
        else:
             text=text.strip()
             formula_text=text

        text=make_razbor(text)
        in_entry_mid_left.insert(END,str(text))
    except Exception as e:    
        e_type, e_val, e_tb = sys.exc_info()
        in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")

    try:
        t = Toplevel()
        img_ = PhotoImage(file=path+'\\Tree\\pic_2.png')
        label=Label(t,image=img_)
        label.image=img_
        label.pack()
    except Exception as e:    
        e_type, e_val, e_tb = sys.exc_info()
        in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")
    

def picture():
    text=in_entry_mid_left.get(1.0,END)
    if text.strip()=="":
        in_entry_down.insert(END,"Нет входных данных")
        return 0
    else:
        try:
            text=eval(text)
            make_tree(text,"pic_1","")
            t = Toplevel()
            img_ = PhotoImage(file=path+'\\Tree\\pic_1.png')
            label=Label(t,image=img_)
            label.image=img_
            label.pack()
        except Exception as e:    
            e_type, e_val, e_tb = sys.exc_info()
            in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")
  
master=Tk()
master.state('zoomed')

frame_up=Frame(master)
frame_up.pack()

frame_down=Frame(master)
frame_down.pack()

frame_for_button=Frame(frame_down)
frame_for_button.pack(side=RIGHT)

frame_for_button_one=Frame(frame_for_button)
frame_for_button_one.pack(side=RIGHT)

in_entry=Text(frame_up,height=2,width=120)
in_entry.pack(side=TOP,ipadx=10,ipady=10,padx=10,pady=10)

in_entry_mid_left=Text(frame_up,height=30,width=60)
in_entry_mid_left.pack(side=LEFT,fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)

in_entry_mid_right=Text(frame_up,height=30,width=60)
in_entry_mid_right.pack(side=RIGHT,fill = "both", expand = "yes",ipadx=10,ipady=10,padx=10,pady=10)

in_entry_down=Text(frame_down,height=3,width=90)
in_entry_down.pack(side=LEFT,ipadx=10,ipady=10,padx=10,pady=10)

button = Button(frame_for_button_one, text='Разбор', width=5,command=razbor)
button.pack(padx=10,pady=10)

button = Button(frame_for_button_one, text='Rank', width=5,command=rank)
button.pack(padx=10,pady=10)

button_cl = Button(frame_for_button, text='Cln', width=5,command=clean)
button_cl.pack(padx=10,pady=10)

button_pic = Button(frame_for_button, text='Pic', width=5,command=picture)
button_pic.pack(padx=10,pady=10)

master.mainloop()

