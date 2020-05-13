from tkinter import *
from gui_function import *
from draw_graph import *
from datetime import datetime
from tkinter import ttk
from subprocess import PIPE, run

import os
path = os.path.dirname(os.path.dirname(__file__))

'''чтобы работало Вырезать+Вставить в окне программы'''

class Graphic_interface():
    def subprocess_cmd(self,command):
        process = run(command, stdout=PIPE, stderr=PIPE,shell=True)
        return process.returncode

    def create(self):
        self.open_option=0
        self.master=Tk()
        self.master.state('zoomed')
        self.master.bind_all("<Key>", self._onKeyRelease, "+")

        self.menu=Menu(self.master)
        self.master.config(menu=self.menu)
        
        filemenu=Menu(self.menu,tearoff=0)
        helpmenu=Menu(self.menu,tearoff=0)

        self.menu.add_command(label='Help',command=self.help_)
        self.menu.add_command(label='Exit',command=self.master.destroy)
       
        self.frame_up=Frame(self.master)
        self.frame_up.pack()

        self.frame_down=Frame(self.master)
        self.frame_down.pack()

        self.frame_for_down=Frame(self.frame_down)
        self.frame_for_down.pack(side=BOTTOM)

        self.frame_for_down_temp=Frame(self.frame_for_down)
        self.frame_for_down_temp.pack()
        self.frame_for_down_temp.pack_forget()

        self.frame_for_button=Frame(self.frame_down)
        self.frame_for_button.pack(side=RIGHT)

        self.frame_for_in_entry=Frame(self.frame_up)
        self.frame_for_in_entry.pack(side=TOP)

        self.frame_for_button_one=Frame(self.frame_for_button)
        self.frame_for_button_one.pack(side=LEFT)

        self.frame_for_button_two=Frame(self.frame_for_button)
        self.frame_for_button_two.pack(side=RIGHT)

        self.in_entry=Text(self.frame_for_in_entry,height=2,width=120)
        self.in_entry.pack(side=LEFT,ipadx=10,ipady=5,padx=10,pady=5)

        self.in_entry_mid_left=Text(self.frame_up,height=29,width=60)
        self.in_entry_mid_left.pack(side=LEFT,fill = "both", expand = "yes",ipadx=10,ipady=5,padx=10,pady=5)

        self.in_entry_mid_right=Text(self.frame_up,height=29,width=60)
        self.in_entry_mid_right.pack(side=RIGHT,fill = "both", expand = "yes",ipadx=10,ipady=5,padx=10,pady=5)

        self.in_entry_down=Text(self.frame_down,height=3,width=97)
        self.in_entry_down.pack(side=LEFT,ipadx=10,ipady=5,padx=10,pady=5)

        self.button_ps = Button(self.frame_for_button_one, text='Parse', width=10,command=self.razbor)
        self.button_ps.pack(padx=10,pady=5)

        self.button_test = Button(self.frame_for_button_two, text='Test', width=10,command=self.test)
        self.button_test.pack(padx=10,pady=5)

        self.button_edit_config = Button(self.frame_for_button_two, text='Edit_config', width=10,command=self.edit_config)
        self.button_edit_config.pack(padx=10,pady=5)

        self.button_save_config = Button(self.frame_for_button_two, text='Save_config', width=10,command=self.save_config)
        self.button_save_config.pack(padx=10,pady=5)
        self.button_save_config.pack_forget()

        self.button_rn = Button(self.frame_for_button, text='Rank', width=10,command=self.rank)
        self.button_rn.pack(padx=10,pady=5)

        self.button_sop=Button(self.frame_for_button, text='Show options', width=10,command=self.show_option)
        self.button_sop.pack(padx=10,pady=5)

        self.button_hop=Button(self.frame_for_button, text='Hide options', width=10,command=self.hide_option)
        self.button_hop.pack(padx=10,pady=5)
        self.button_hop.pack_forget()

        self.button_pic = Button(self.frame_for_button_one, text='Picture', width=10,command=self.picture)
        self.button_pic.pack(padx=10,pady=5)

        self.button_cl = Button(self.frame_for_in_entry, text='Clean', width=12,command=self.clean)
        self.button_cl.pack(padx=10,pady=5)

        self.button_ld = Button(self.frame_for_in_entry, text='Load_and_run', width=12,command=self.load_and_run)
        self.button_ld.pack(padx=10,pady=5)
        self.master.mainloop()

    def _onKeyRelease(self,event):
        ctrl  = (event.state & 0x4) != 0
        
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")

        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")

        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

    def parse_formula(self):
        try:
             text=self.in_entry.get(1.0,END).strip()
             if len(text)==0:
                 self.in_entry_down.insert(END,"Ошибка входных данных\n")
                 return 0
                
             res=make_formula_razbor([text])
             self.in_entry_mid_left.insert(END,str(res)+'\n\n')
        except:
            e_type, e_val, e_tb = sys.exc_info()
            self.in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")

    def update_levenshtein(self):
        rv=self.subprocess_cmd("Levenshtein_sim.exe")
        if rv==0:
            self.in_entry_mid_right.insert(END,'Levenshtein database is created\n')

    def show_option(self):
        self.frame_for_down_temp.pack()

        self.button_fp = Button(self.frame_for_down_temp, text='Parse formula', width=12,command=self.parse_formula)
        self.button_fp.pack(side=LEFT,padx=5,pady=5)

        self.button_ul = Button(self.frame_for_down_temp, text='Update LDB', width=12,command=self.update_levenshtein)
        self.button_ul.pack(side=LEFT,padx=5,pady=5)

        self.button_fdb = Button(self.frame_for_down_temp, text='Full DB', width=10,command=self.database)
        self.button_fdb.pack(side=LEFT,padx=5,pady=5)

        self.button_fldb = Button(self.frame_for_down_temp, text='Formula DB', width=10,command=self.formula_database)
        self.button_fldb.pack(side=LEFT,padx=5,pady=5)

        self.button_wf = Button(self.frame_for_down_temp, text='Write to file', width=10,command=self.write_to_file)
        self.button_wf.pack(side=LEFT,padx=5,pady=5)

        self.button_ext = Button(self.frame_for_down_temp, text='Extract by id', width=10,command=self.extract)
        self.button_ext.pack(side=LEFT,padx=5,pady=5)

        self.input_ext = Entry(self.frame_for_down_temp, text='Extract by id', width=5)
        self.input_ext.pack(side=LEFT,padx=5,pady=5)

        label_combo=Label(self.frame_for_down_temp,text="Amount algo \n for Test")
        label_combo.pack(side=LEFT,padx=5,pady=5)
        
        self.entry = ttk.Entry(self.frame_for_down_temp,width=5)
        self.entry.pack(side=LEFT,padx=5,pady=5)
        
        self.button_hop.pack(padx=10,pady=5)
        self.button_sop.pack_forget()

        self.open_option=1

    def hide_option(self):
        for widget in self.frame_for_down_temp.winfo_children():
            widget.destroy()
        
        self.frame_for_down_temp.pack_forget()
        self.button_sop.pack(padx=10,pady=5)
        self.button_hop.pack_forget()

        self.open_option=0

    def write_to_file(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        t=self.in_entry_mid_right.get(1.0,END)
        s=self.in_entry_mid_left.get(1.0,END)
        
        name="outfile_"+str(current_time)+".txt"
        name=name.replace(":","_")

        lst=t.split('\n')
        for i in range(len(lst)):
            if "\t" in lst[i]:
                a=lst[i].split('\t')
                a[0]=a[0].strip()
                for k in range(1,len(a)):
                    if len(a[k])!=4:
                        a[k]=a[k]+"0"

                lst[i]=a
                
        f=open(path+"\\"+name,"w",encoding="utf-8")
        f.write(s)
        for i in range(1,len(lst)):
            f.write("\t".join(lst[i])+"\n")
        f.close()
    
        self.clean()
        self.in_entry_mid_right.insert(END,'See data in '+name+'\n\n')
    
    def extract(self):
      f=open(path+'\\Database\\theorem_list.txt',"r",encoding="utf-8")
      i=0
      text=""

      for x in f:
        i=i+1
        if i==int(self.input_ext.get()):
            text=x.strip()
            break

      f.close()
      self.in_entry_mid_left.insert(END,text+'\n\n')
       
    def help_(self):
        self.clean()
        lst=[]
        f=open(path+"\\readme.txt","r",encoding="utf-8")
        for line in f:
            lst.append(line)
        f.close()

        for line in lst:
            self.in_entry_mid_right.insert(END,line)

        self.in_entry_mid_right.insert(END,'\n\n')

    def database(self):
        self.clean()
        make_database()
        self.in_entry_mid_right.insert(END,'See database files in '+path+"\Database\n\n")

    def formula_database(self):
        formulas_list=[]
        self.clean()
        extract_formula_razbor()

        f=open(path+"\\Files\\formulas_.txt","r",encoding="utf-8")

        for line in f:
            formulas_list.append(line.strip())
        f.close()

        res=make_formula_razbor(formulas_list)

        f=open(path+"\\Files\\test_razbor.txt","w",encoding="utf-8")
        for x in res:
            f.write(str(x)+'\n')
       
        f.close()

        self.in_entry_mid_right.insert(END,'See database files in '+path+"\Files\n\n")

    def test(self):
        self.clean()
        self.in_entry_mid_right.insert(END,'--- Test for ranking function ---\n\n')
        self.in_entry_mid_left.insert(END,'--- Test for ranking function ---\n\n')

        if self.open_option==1 and self.entry.get() in ["7","6","5","4","3","2","1"]:
            amount_of_algo=int(self.entry.get())
        else:
            amount_of_algo=7

        text_list=['Algo #1: Treepath+Jaccard  (tree,standart): ','Algo #2: Treepath+Jaccard  (tree,modify): ',
                   'Algo #3: Treepath+Jaccard  (pure syntax tree,standart): ',
                   'Algo #4: Keyword Search  (text): ','Algo #5: Edit Distance  (text): ',
                   'Algo #6: Cos similarity  (text): ','Algo #7: Jaccard similarity  (text): ']

        result=[]

        for i in range(amount_of_algo):
            result.append('0')
            result[i]=test_general_sub_main(path_db+"theorem_list.txt",i)
            self.in_entry_mid_left.insert(END,text_list[i]+str(avg(result[i]))+'\n\n')

        check_best_in_line_list=[]
        tmp=[]
        str1=""
        
        for i in range(len(result[0])):
            for k in range(amount_of_algo):
                check_best_in_line_list.append(result[k][i])
                tmp.append(result[k][i])
                str1=str1+'\t'+str(result[k][i])

            check_best_in_line=max(check_best_in_line_list)
            index_of_best_inline='0'

            for k in range(len(tmp)):
                if tmp[k]==check_best_in_line:
                    index_of_best_inline=str(k+1)
                    break
        
            self.in_entry_mid_right.insert(END,str(i+1)+'. '+str1+'\n')
            #self.in_entry_mid_left.insert(END,index_of_best_inline+" | "+str(check_best_in_line)+'\n')
            self.in_entry_mid_right.insert(END,'\n\n')

            str1=""
            tmp=[]
            check_best_in_line_list=[]


        #self.in_entry_mid_right.insert(END,'--- Test_of_predicate_module_and_ranking ---')
        '''
        self.in_entry_mid_right.insert(END,'\n\n')
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

        self.in_entry_mid_left.insert(END,"Test_of_predicate_module_and_ranking\n\n")
    
        for line in lst_:
             self.in_entry_mid_left.insert(END,str(line)+'\n\n')

        for i in range(len(lst)):
             lst[i]=lst[i].split('\t')
             self.in_entry_mid_right.insert(END,str(i+1)+'\t'+str(lst[i][0])+'\t'+str(lst[i][1])+'\n\n')
        '''
         
    def load_and_run(self):
       self.clean()
       lst=[]

       f=open(path+"\Infile.txt","r",encoding="utf-8")
       for line in f:
         lst.append(line.strip())
       f.close()

       tl,rl,el=make_razbor(lst)
       self.write_parse_result(tl,rl,el)
       

    def edit_config(self):
        self.button_save_config.pack(padx=10,pady=5)
        self.button_edit_config.pack_forget()
  
        self.clean()
        config_file_path=path+"\\Files\\config.ini"
        f=open(config_file_path,"r",encoding="utf-8")

        for line in f:
            self.in_entry_mid_right.insert(END,line)
        f.close()
    
    def save_config(self):
        self.button_edit_config.pack(padx=10,pady=5)
        self.button_save_config.pack_forget()
   
        config_file_path=path+"\\Files\\config.ini"
        t=self.in_entry_mid_right.get(1.0,END)

        f=open(config_file_path,"w",encoding="utf-8")
        if len(t)>0:
            f.write(t)
        f.close()
  
    def rank(self):
        self.clean()
        try:
            text=self.in_entry.get(1.0,END)
            if text[0]=="[":
                 text=eval(text.strip())
            else:
                 text=text.strip()

            text=make_razbor(text)
            query,ranking_arr=make_ranking(text)
            self.in_entry_mid_left.insert(END,str(query))
            self.in_entry_mid_left.insert(END,'\n\n')
            self.in_entry_mid_left.insert(END,'----------\n\n')
        
            for i in range(len(ranking_arr)):
                 self.in_entry_mid_right.insert(END,str(ranking_arr[i][0])+'\t'+str(ranking_arr[i][1]))
                 self.in_entry_mid_right.insert(END,'\n')

                 self.in_entry_mid_left.insert(END,str(ranking_arr[i][2]))
                 self.in_entry_mid_left.insert(END,'\n\n')    
        except:
            e_type, e_val, e_tb = sys.exc_info()
            self.in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")
       
    
    def clean(self):
        #in_entry.delete(1.0,END)
        self.in_entry_mid_left.delete(1.0,END)
        self.in_entry_mid_right.delete(1.0,END)
        self.in_entry_down.delete(1.0,END)
     
    def razbor(self):
        self.clean()
        formula_text=""

        text=self.in_entry.get(1.0,END)
        if text[0]=="[":
            text=eval(text.strip())
            formula_text=""
        else:
            text=[text.strip()]
            formula_text=text

        t1,r1,e1=make_razbor(text)
        self.write_parse_result(t1,r1,e1)
        A=plot_tree(text,"pic_1","")
        A.main("formula")
        
   
    def picture(self):
        text=self.in_entry.get(1.0,END)
        if text.strip()=="":
            self.in_entry_down.insert(END,"Нет входных данных")
            return 0
        else:
            try:
                text=eval(text)
                A=plot_tree(text,"pic_1","")
                A.main("formula")
                t = Toplevel()
                img_ = PhotoImage(file=path+'\\Tree\\pic_1.png')
                self.label=Label(t,image=img_)
                self.label.image=img_
                self.label.pack()
            except Exception as e:    
                e_type, e_val, e_tb = sys.exc_info()
                self.in_entry_down.insert(END,str(e_type)+"\n"+str(e_val)+"\n")

    def write_parse_result(self,tl,rl,el):
       for i in range(len(tl)):
            self.in_entry_mid_right.insert(END,str(i+1)+"."+str(tl[i]))
            self.in_entry_mid_right.insert(END,'\n\n')

       for line in rl:
            self.in_entry_mid_left.insert(END,str(line))
            self.in_entry_mid_left.insert(END,'\n\n')

       if len(el)==0:
           self.in_entry_down.insert(END,'Ошибок не произошло')
           self.in_entry_down.insert(END,'\n\n')
       else:
           for line in el:
                self.in_entry_down.insert(END,line)
                self.in_entry_down.insert(END,'\n\n')
  

A=Graphic_interface()
A.create()

