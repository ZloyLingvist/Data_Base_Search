import re

class formula_simplifier:
    def __init__(self,s):
        self.arr=['\displaystyle','\textstyle','\right','\left','\limits','\nolimits','\quad','\,','\!','\;',"\Bigg","\bigl","\bigr"]
        self.arr1=[["\{","\}","\set","(",")"],["[","]","\closedinterval","(",")"],['||','||','\norm','(',')'],["\|","\|","\abs","(",")"],["|","|","\abs","(",")"]]
        self.arr2=[["\mathrm {","}","","",""],["\mathbb {","}","\mathbb","(",")"],["\mathcal {","}","","",""],
                   ["\mathbf {","}","","",""],["\widehat {","}","\widehat","(",")"],
                   ["\sqrt {","}","\sqrt","(",")"]]
        
        self.arr3={"\\lbrace":"{","\\rbrace":"}","\langle":"{","\\rangle":"}","\\mid":"\\vert","\\cdot":"*","\\over":"/","\\ast":"*"}
        self.arr4={".}":"}",",}":"}","{ }":""," |":"|","{ (}":"(","{ )}":")"}
        
        self.str=self.str_to_raw(s)
        self.str=re.sub(r'\s+', ' ',self.str).strip()
        
        for i in range(len(self.arr1)):
            self.arr1[i][0]=self.str_to_raw(self.arr1[i][0])
            self.arr1[i][1]=self.str_to_raw(self.arr1[i][1])
            self.arr1[i][2]=self.str_to_raw(self.arr1[i][2])
                   
        for i in range(len(self.arr)):
             self.arr[i]=self.str_to_raw(self.arr[i])

        
    def str_to_raw(self,s):
        raw_map = {8:r'\b', 7:r'\a', 12:r'\f', 10:r'\n', 13:r'\r', 9:r'\t', 11:r'\v'}
        return r''.join(i if ord(i) > 32 else raw_map.get(ord(i), i) for i in s)

    def find_between(self,first, last):
        try:
            start = self.str.index( first ) + len( first )
            i=0
            while (i<len(self.str)):
                end = self.str.index( last, start)
                end=end+i
                if self.str[start:end].count("{")!=self.str[start:end].count("}"):
                    end = self.str.index( last, start)
                else:
                    break
                
                i=i+1

            return self.str[start:end]
        
        except ValueError:
            return ""

    def replacement(self):
        #### обнуление ####
        for i in range(len(self.arr)):
             if self.arr[i] in self.str:
                 self.str=self.str.replace(self.arr[i],"")

        ###замена на эквиваленты
        for x in self.arr3:
            x=self.str_to_raw(x)
            if x in self.str:
                self.str=self.str.replace(x,self.arr3[x])

    
    def equivalent_replacement(self,arr_):
        i=0
        while i<len(arr_):
            if arr_[i][0]==arr_[i][1]: ##если элементы одинаковые например обозначение модуля
                if self.str.count(arr_[i][0])%2!=0:
                    break
                
            if arr_[i][0] in self.str and arr_[i][1] in self.str:
               eq=self.find_between(arr_[i][0],arr_[i][1])
               self.str=self.str.replace(arr_[i][0]+eq+arr_[i][1],arr_[i][2]+arr_[i][3]+eq+arr_[i][4])
            else:
                i=i+1

        self.str=self.str.replace("\\"," \\")

    def insert_elements(self):
        self.str=re.sub(r"((?:\d+)|(?:[a-zA-Z]\w*\(\w+\)))((?:[a-zA-Z]\w*)|\()", r"\1*\2", self.str)

    def phantom_node(self):
        if "\\lim" in self.str:
            a=self.find_between("\\lim _{","}")
            if "\lim _{"+a+"}" in self.str:
                self.str=self.str.replace("\lim _{"+a+"}","\lim _{"+a+"}")

        arr=['\sum','\int']
        for i in range(len(arr)):
            if arr[i] in self.str:
                a=self.find_between(arr[i]+" _{","}")
                b=self.find_between(arr[i]+" _{"+a+"}^{","}")
                if b.strip()!="":
                     self.str=self.str.replace(arr[i]+" _{"+a+"}^{"+b+"}",arr[i]+" _{"+a+"}^{"+b+"}")
                else:
                     self.str=self.str.replace(arr[i]+" _{"+a+"}",arr[i]+" _{"+a+"}")
                    

            

    def main(self):
        self.replacement()
        self.equivalent_replacement(self.arr1)
        self.equivalent_replacement(self.arr2)
        self.insert_elements()
        self.str=re.sub(r'\s+', ' ',self.str).strip()
        self.str=re.sub(r'< ', '<',self.str).strip()
        self.str=re.sub(r'> ', '>',self.str).strip()
        self.str=re.sub(r'= ', '=',self.str).strip()

        #self.phantom_node()
     
        for x in self.arr4:
            if x in self.str:
                self.str=self.str.replace(x,self.arr4[x])

        re_list=["\w+\*\w+\^{\w+}","\w+\*\w+\^\w+","\w+\/\w+\^{\w+}","\w+\/\w+\^\w+"]
        for i in range(len(re_list)):
            if i==0 or i==1:
                delim="*"
            if i==2 or i==3:
                delim="/"

            c=re.findall(re_list[i],self.str)
            if c==[]:
                continue

            temp=c[0].split(delim)
            temp[0],temp[1]=temp[1],temp[0]
            r=delim.join(temp)
            self.str=self.str.replace(c[0],r)

        for i in range(len(self.str)):
            if self.str[i]=="_" or self.str[i]=="^":
                if len(self.str[i+1].strip())==0:
                       self.str=self.str[:i+1]+self.str[i+2:]
                  
                if self.str[i+1]!="\\" and self.str[i+1]!="{" and len(self.str[i+1].strip())>0:
                    self.str=self.str[:i+1]+"{"+self.str[i+1]+"}"+self.str[i+2:]
                    
                if self.str[i+1]=="\\" and self.str[i+1]!="{":
                    cr=re.compile(r'[^za-zA-Z]')
                    k=i+2
                    str2=""

                    while (k<len(self.str)):
                        a=cr.search(self.str[k])
                        if a!=None:
                            break

                        str2=str2+self.str[k]
                        k=k+1

                    self.str=self.str.replace("\\"+str2,"{\\"+str2+"}")
       
        return self.str

