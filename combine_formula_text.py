from formula_tree import *
from text_tree import *
from utilities import *
import pickle

class combine_formula_and_text:
    def __init__(self,arr,formulaname,fileout):
        self.formulaname=formulaname
        #self.filename=filename
        self.fileout=fileout
        self.big_tmp=arr[0]
        self.root=arr[1]
        self.formula_list={}
        self.create_filelist()
        self.F=Formula_Tree("","","grammar")

    def find_root(self):
        for x in self.big_tmp:
            if x[3]=="0":
                return x[0]
            
    def search_and_replace(self,text_list):
        for i,elem in enumerate(text_list):
            if not isinstance(elem,str):         
                text_list[i]=self.search_and_replace(elem)
            else:
                for x in self.formula_list.keys():
                    if elem==x and not "#" in self.formula_list[x]:
                        try:
                            text_list[i]=self.F.run(self.formula_list[x])
                        except:
                            text_list[i]=self.formula_list[x].strip('\n')
                        
                    if elem==x and "#" in self.formula_list[x]:
                        text_list[i]=self.formula_list[x].strip('\n')

        return text_list
      
    def create_filelist(self):
        tmp=[]
        f=open(self.formulaname+".txt","r",encoding="utf8")

        i=0
        for line in f:
            self.formula_list["formula_"+str(i+1)]=line.strip()
            i=i+1
        f.close()

        '''
        f=open(self.filename+".txt","r",encoding="utf8")
        for line in f:
            str1=line.split('\t')
            if str1!=['\n']:
                tmp.append([str1[0],str1[1],str1[2],str1[5],str1[6].strip()])
            
            if line=="\n":
                if tmp!=[]:
                    self.big_tmp.append(tmp)
                    tmp=[]

        if tmp!=[]:
            self.big_tmp.append(tmp)

        f.close()
        '''

    def main(self):
        result=[]
        A=Text_analyzer(self.big_tmp,self.root)
        text=A.make_tree()
        formula=self.search_and_replace(text)
        result.append(formula)

        if self.fileout!="":
            with open(self.fileout+".db", 'ab') as filehandle:
                pickle.dump(formula, filehandle)
                pickle.dump('\n',filehandle)

        return result
            

