from tkinter import *
from gui_function import *
from draw_graph import *
import os
import time

path = os.path.dirname(os.path.dirname(__file__))

'''чтобы работало Вырезать+Вставить в окне программы'''
def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

def extract():
    f=open(path+'\\Database\\theorem_list.txt',"r",encoding="utf-8")
    i=0
    text=""
    for x in f:
        i=i+1
        if i==int(input_ext.get()):
            text=x.strip()
            break
    f.close()
    in_entry_mid_left.insert(END,text+'\n\n')
    
    

def help_():
    clean()
    lst=[]
    f=open(path+"\\readme.txt","r",encoding="utf-8")
    for line in f:
        lst.append(line)
    f.close()

    for line in lst:
        in_entry_mid_right.insert(END,line)

    in_entry_mid_right.insert(END,'\n\n')

def database():
    clean()
    make_database()
    in_entry_mid_right.insert(END,'See database files in '+path+"\Database\n\n")

def test():
    clean()
    in_entry_mid_right.insert(END,'--- Test for ranking function ---\n\n')
    
    in_entry_mid_left.insert(END,'--- Test for ranking function ---\n\n')
    
    result=['0','0','0','0','0','0']

    for i in range(6):
        result[i]=test_general_sub_main(path_db+"theorem_list.txt",i)

    in_entry_mid_right.insert(END,'Algo #1: Treepath+Jaccard  (tree,standart): '+str(avg(result[0]))+'\n\n')
    in_entry_mid_right.insert(END,'Algo #2: Treepath+Jaccard  (tree,modify): '+str(avg(result[1]))+'\n\n')
    in_entry_mid_right.insert(END,'Algo #3: Keyword Search  (text): '+str(avg(result[2]))+'\n\n')
    in_entry_mid_right.insert(END,'Algo #4: Edit Distance  (text): - not using in this implementation too slow \n\n')
    in_entry_mid_right.insert(END,'Algo #5: Cos similarity  (text): '+str(avg(result[4]))+'\n\n')
    in_entry_mid_right.insert(END,'Algo #6: Jaccard similarity  (text): '+str(avg(result[5]))+'\n\n')
    
    for i in range(len(result[0])):
        check_best_in_line=max(result[0][i],result[1][i],result[2][i],result[4][i],result[5][i])
        tmp=[result[0][i],result[1][i],result[2][i],result[4][i],result[5][i]]
        index_of_best_inline='0'

        for k in range(len(tmp)):
            if tmp[k]==check_best_in_line:
                index_of_best_inline=str(k+1)
                break
        
        in_entry_mid_right.insert(END,str(i+1)+'. '+str(result[0][i])+'\t'+str(result[1][i])+'\t'+str(result[2][i])+'\t'+'-'+'\t'+str(result[4][i])+'\t'+str(result[5][i])+'\t\t'+index_of_best_inline+" | "+str(check_best_in_line))
        in_entry_mid_right.insert(END,'\n\n')


    in_entry_mid_right.insert(END,'--- Test_of_predicate_module_and_ranking ---')
    in_entry_mid_right.insert(END,'\n\n')
    testing_block_one("test_lst.txt","test_in.txt","outname.txt","outname2.txt",-1,[1],0)

    lst=[]
    lst_=[]
    f=open(path+"\\Test\\outname.txt","r",encoding="utf-8")
    for line in f:
        lst.append(line)
    f.close()

    f=open(path+"\\Test\\outname2.txt","r",encoding="utf-8")
    for line in f:
        lst_.append(line)
    f.close()

    in_entry_mid_left.insert(END,"Test_of_predicate_module_and_ranking\n\n")
    
    for line in lst_:
         in_entry_mid_left.insert(END,str(line)+'\n\n')

    for i in range(len(lst)):
         lst[i]=lst[i].split('\t')
         in_entry_mid_right.insert(END,str(i+1)+'\t'+str(lst[i][0])+'\t'+str(lst[i][1])+'\n\n')
         
    

def load_and_run():
   clean()
   tl,rl,el=make_load_and_run()
   for i in range(len(tl)):
        in_entry_mid_right.insert(END,str(i+1)+"."+tl[i])
        in_entry_mid_right.insert(END,'\n\n')

   for line in rl:
        in_entry_mid_left.insert(END,str(line))
        in_entry_mid_left.insert(END,'\n\n')

   if len(el)==0:
       in_entry_down.insert(END,'Ошибок не произошло')
       in_entry_down.insert(END,'\n\n')

   else:
       for line in el:
            in_entry_down.insert(END,line)
            in_entry_down.insert(END,'\n\n')


def edit_config():
    clean()
    config_file_path=path+"\\Files\\config.ini"
    f=open(config_file_path,"r",encoding="utf-8")

    for line in f:
        in_entry_mid_right.insert(END,line)
    f.close()
    
    button_save_config.pack(padx=10,pady=5)
    button_edit_config.pack_forget()
   

def save_config():
    config_file_path=path+"\\Files\\config.ini"
    t=in_entry_mid_right.get(1.0,END)

    f=open(config_file_path,"w",encoding="utf-8")
    if len(t)>0:
        f.write(t)
    f.close()
    
    button_edit_config.pack(padx=10,pady=5)
    button_save_config.pack_forget()

def rank():
    clean()
    try:
        text=in_entry.get(1.0,END)
        if text[0]=="[":
             text=eval(text.strip())
        else:
             text=text.strip()

        text=make_razbor(text)
        query,ranking_arr=make_ranking(text)
        in_entry_mid_left.insert(END,str(query))
        in_entry_mid_left.insert(END,'\n\n')
        in_entry_mid_left.insert(END,'----------\n\n')
        
        for i in range(len(ranking_arr)):
             in_entry_mid_right.insert(END,str(ranking_arr[i][0])+'\t'+str(ranking_arr[i][1]))
             in_entry_mid_right.insert(END,'\n')

             in_entry_mid_left.insert(END,str(ranking_arr[i][2]))
             in_entry_mid_left.insert(END,'\n\n')    
    except:
        e_type, e_val, e_tb = sys.exc_info()
        in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")
    
def clean():
    #in_entry.delete(1.0,END)
    in_entry_mid_left.delete(1.0,END)
    in_entry_mid_right.delete(1.0,END)
    in_entry_down.delete(1.0,END)
     
def razbor():
    clean()
    formula_text=""
    try:
        text=in_entry.get(1.0,END)
        if text[0]=="[":
             text=eval(text.strip())
             formula_text=""
        else:
             text=text.strip()
             formula_text=text

        text=make_razbor(text)
        in_entry_mid_left.insert(END,str(text))
        A=plot_tree(text,"pic_1","")
        A.main("formula")
        
    except Exception as e:    
        e_type, e_val, e_tb = sys.exc_info()
        in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")

    try:
        t = Toplevel()
        img_ = PhotoImage(file=path+'\\Tree\\pic_1.png')
        label=Label(t,image=img_)
        label.image=img_
        label.pack()
    except Exception as e:    
        e_type, e_val, e_tb = sys.exc_info()
        in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")
   
    

def picture():
    text=in_entry.get(1.0,END)
    if text.strip()=="":
        in_entry_down.insert(END,"Нет входных данных")
        return 0
    else:
        try:
            text=eval(text)
            A=plot_tree(text,"pic_1","")
            A.main("formula")
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
master.bind_all("<Key>", _onKeyRelease, "+")

frame_up=Frame(master)
frame_up.pack()

frame_down=Frame(master)
frame_down.pack()

frame_for_down=Frame(frame_down)
frame_for_down.pack(side=BOTTOM)

frame_for_button=Frame(frame_down)
frame_for_button.pack(side=RIGHT)

frame_for_in_entry=Frame(frame_up)
frame_for_in_entry.pack(side=TOP)


frame_for_button_one=Frame(frame_for_button)
frame_for_button_one.pack(side=LEFT)

frame_for_button_two=Frame(frame_for_button)
frame_for_button_two.pack(side=RIGHT)

in_entry=Text(frame_for_in_entry,height=2,width=120)
in_entry.pack(side=LEFT,ipadx=10,ipady=5,padx=10,pady=5)

in_entry_mid_left=Text(frame_up,height=30,width=60)
in_entry_mid_left.pack(side=LEFT,fill = "both", expand = "yes",ipadx=10,ipady=5,padx=10,pady=5)

in_entry_mid_right=Text(frame_up,height=30,width=60)
in_entry_mid_right.pack(side=RIGHT,fill = "both", expand = "yes",ipadx=10,ipady=5,padx=10,pady=5)

in_entry_down=Text(frame_down,height=3,width=97)
in_entry_down.pack(side=LEFT,ipadx=10,ipady=5,padx=10,pady=5)

button_ps = Button(frame_for_button_one, text='Parse', width=10,command=razbor)
button_ps.pack(padx=10,pady=5)

button_rn = Button(frame_for_button_one, text='Rank', width=10,command=rank)
button_rn.pack(padx=10,pady=5)

button_ts = Button(frame_for_button, text='Test', width=10,command=test)
button_ts.pack(padx=10,pady=5)

button_hl=Button(frame_for_button_two, text='Help', width=10,command=help_)
button_hl.pack(padx=10,pady=5)

button_edit_config = Button(frame_for_button_two, text='Edit_config', width=10,command=edit_config)
button_edit_config.pack(padx=10,pady=5)

button_save_config = Button(frame_for_button_two, text='Save_config', width=10,command=save_config)
button_save_config.pack(padx=10,pady=5)
button_save_config.pack_forget()

button_opt = Button(frame_for_down, text='Make Database', width=13,command=database)
button_opt.pack(side=LEFT,padx=10,pady=5)

button_ext = Button(frame_for_down, text='Extract by id', width=10,command=extract)
button_ext.pack(side=LEFT,padx=10,pady=5)

input_ext = Entry(frame_for_down, text='Extract by id', width=5)
input_ext.pack(side=LEFT,padx=10,pady=5)

button_pic = Button(frame_for_button, text='Picture', width=10,command=picture)
button_pic.pack(padx=10,pady=5)

button_cl = Button(frame_for_in_entry, text='Clean', width=12,command=clean)
button_cl.pack(padx=10,pady=5)

button_ld = Button(frame_for_in_entry, text='Load_and_run', width=12,command=load_and_run)
button_ld.pack(padx=10,pady=5)

master.mainloop()

