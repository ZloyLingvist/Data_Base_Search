class help_class:
    def __init__(self,in_,formula_name,out):
        self.name0=in_+".txt"
        self.name1=formula_name+".txt"
        self.name2=out+".txt"

    def counter(self):
        f=open(self.name0,"r",encoding="utf-8")
        count=0
        for line in f:
            if line=="\n":
                count=count+1
        f.close()
        print(count)

    def clean(self):
        ## чистим
        f=open(self.name1,"w",encoding="utf-8")
        f.close()

        f=open(self.name2,"w",encoding="utf-8")
        f.close()

    def main(self):
        f=open(self.name0,"r",encoding="utf-8")
        lst=[]
        lst_=""

        for line in f:
            if line=="\n":
                lst.append(lst_)
                lst_=""

            lst_=lst_+line

        if lst!="":
            lst.append(lst_)
    
        f.close()

        for i in range(len(lst)):
            self.file_in(lst[i])

        print('finished\n')


    def file_in(self,line):
        ######## считываем из базы формул #####
        lst_gl=[]
        lst=[]
        str1=""
        str2=""
        match=0

        try:
            f=open(self.name1,"r",encoding="utf-8")
            for line_ in f:
                lst_gl.append(line_.strip())
            f.close()
        except:
            0
   
        for i in range(len(line)):
            if line[i]=="{":
                match=match+1

            if line[i]=="}":
                match=match-1
                
            if match>0:
                str1=str1+line[i]
           
            if match==0:
                if line[i]!="}":
                    str2=str2+line[i] ##строка, содержащая текстовую часть

                if str1!="":
                    str1=str1+"}"
                    if not str1 in lst_gl: ##если формула где-то была в базе формул, то дать ее индекс
                        lst.append(str1)
                        lst=list(set(lst))
                        str2=str2+"formula_"+str(len(lst)+len(lst_gl))
                    else:
                        for k in range(len(lst_gl)):
                            if lst_gl[k]==str1:
                                str2=str2+"formula_"+str(k+1)
                    str1=""

        f=open(self.name1,"a",encoding="utf-8")
        for i in range(len(lst)):
            f.write(lst[i].strip()+'\n')
        f.close()

        str2=" ".join(str2.splitlines()).strip().replace("."," . ").replace(","," ,")
        
        f=open(self.name2,"a",encoding="utf-8")
        f.write(str2+'\n\n')
        f.close()


    def xml_parse(self,name,out):
        from bs4 import BeautifulSoup
        f=open(name+".xml","r",encoding="utf-8")
        y=f.read()
        f.close()
        soup = BeautifulSoup(y,'xml')
        ##установить lxml
        titles = soup.find_all('sentence_element')
        arr=[]
        p=""
        n=""

        for title in titles:
            if title.syntactic_parent!=None:
                p=title.syntactic_parent["word_id"]
                u = soup.find_all('sentence_element')
                for t in u:
                    if t["id"]==p:
                        p=str(int(t.order.get_text())-1)
                        break
            else:
                p="_"
            
            a=title.get_text().split('\n')
            if len(a)>6:
                str_=a[3]+'\t'+a[4]+'\t'+a[11]
                str_2=""
                for i in range(11,len(a)):
                    if a[i]=="":
                        str_=str_+'\t'+str_2.strip()+'\t'+p+'\t'+a[i+1]
                        break
    
                    str_2=str_2+" "+a[i]

                arr.append(str_)
            else:
                arr.append(a[3]+'\t'+a[3]+'\t'+'SENT'+'\t'+'SENT'+'\t'+p+'\t'+'punc')

        del arr[0] 
        for i in range(len(arr)):
            arr[i]=(str(i+1)+'\t'+arr[i]).split('\t')

        dict_1={'Preposition':'PR','Verb':'V','Noun':'S','Adjective':'A','Conjunction':'CONJ'}
        for x in dict_1:
            for i in range(len(arr)):
                if arr[i][5]=="0" and arr[i][6]!="Predicate":
                    for k in range(len(arr)):
                        if arr[k][5]=="0" and arr[k][6]=="Predicate":
                            arr[i][5]=str(k+1)
                            break
                    
                if arr[i][3]==x:
                    arr[i][3]=dict_1[x]

        f=open(out+".txt","w",encoding="utf-8")
        k=0
        for i in range(len(arr)):
            if arr[i][1]!="Verb":
                if arr[i][1]=="быть":
                    arr[i][2]="быть"
                    arr[i][1]="есть"

                if arr[i][3]=="":
                    arr[i][3]="_"

                if arr[i][4]=="":
                    arr[i][4]="_"
                    
                if arr[i][5]!="_":
                    f.write(str(k+1)+'\t'+arr[i][1]+'\t'+arr[i][2]+'\t'+arr[i][3]+'\t'+arr[i][4]+'\t'+arr[i][5]+'\t'+arr[i][6]+'\n')
                else:
                    f.write(str(k+1)+'\t'+arr[i][1]+'\t'+arr[i][2]+'\t'+arr[i][3]+'\t'+arr[i][4]+'\t'+str(k)+'\t'+arr[i][6]+'\n')

                k=k+1
                
            if arr[i][1]==".":
                k=0
                f.write('\n')
        
        f.close()

#A=help_class("FULL_IN","ALL_FORMULAS_","ALL_TASK")
A=help_class("test_in","formulas_","file3")
#A.counter()
#A.clean()
#A.main()
A.xml_parse("Result","testset")

