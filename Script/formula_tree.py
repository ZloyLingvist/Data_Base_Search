from formula_simplifier import *
from utilities import *
import tatsu
import re
import os

'''модуль преобразования формулы
Пример использования
A=Formula_Tree()
A.main(text)
text - формула, которую нужно разобрать
'''

'''Класс CalcSemantics - используется библиотекой Tatsu для преобразования формулы'''

parent_directory=os.path.dirname(os.path.dirname(__file__))
grammar_path=parent_directory+'\\Files\\grammar.ebnf'

class CalcSemantics(object):
    def punc(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        for i in range(len(ast)-1,-1,-1):
            if ast[i]==",":
                del ast[i]
                
        return ast
    
    def function(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        for i in range(len(ast)):
            if ast[i]=="^":
                ast[i]=[ast[i],ast[i+1]]
                ast[i+1]=[]

        ast=clean_from_empty(ast)
        return ast
    
    def limit(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        ast[1]=[ast[1],ast[2]]
        ast[2]=[]
        ast=clean_from_empty(ast)
        return ast
    
    def integral(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        ast=modifier_integral_summ(ast)
        return ast
    
    def sum(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        ast=modifier_integral_summ(ast)
        return ast

    def expression(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        op=["=","\\leq",">"]
        if type(ast)==list:
            for i in range(len(ast)):
                if type(ast[i])==list:
                    if ast[i][0] in op and len(ast[i])>1:
                        if len(ast[i][1][0])==1:
                            continue #страховка от случая когда равно часть показателя
                        oper=ast[i][0]
                        tmp=[]
                        count=0
                        for k in range(i): ##копируем все что было до разделителя
                            tmp.append(ast[k])
                            count=count+1
                            
                        tmp.append(ast[i][1])
                        ast=ast[count:]
                        ast[0]=ast[0][2:][0]
                        ast.insert(0,oper)
                        ast.insert(1,tmp)
                                                
                        
            if ast[0]=="\\int":
                for k in range(len(ast)):
                    if type(ast[k])==str and re.search(r'^d',ast[k]):
                        ast[k]=[ast[k]]

        return ast

    def addition(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        ast=swap_to_first(ast,"+")
        ast=equalizer(ast,1)
        return ast
    
    def subtraction(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        ast=swap_to_first(ast,"-")
        ast=equalizer(ast,1)
        return ast

    def multiplication(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        ast=swap_to_first(ast,"*")
        ast=equalizer(ast,1)
        return ast

    def division(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        ast=swap_to_first(ast,"/")
        ast=equalizer(ast,1)
        return ast

    def brackets(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        if len(ast)==3:
            if ast[0]=="(" and ast[2]==")":
                if type(ast[1])==str:
                    ast=[ast[1]]
                else:
                    ast=ast[1]

            if ast[0]=="{" and ast[2]=="}":
                if type(ast[1])==str:
                    ast=[ast[1]]
                else:
                    ast=ast[1]
          
        return ast
                
    def operation_three(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        arr=["\\leq","\\geq"]
        ast=swap_(arr,ast)
        ast[1]=[ast[1],ast[2]]
        ast[2]=[]
        ast=clean_from_empty(ast)
            
        return ast
    

    def operation_one(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        arr=["\\cap","\\cup","\\subset","\\subseteq","\\to","\\in"]
        ast=swap_(arr,ast)
            
        ast=clean_from_empty(ast)
        return ast


    def operation_two(self,ast):
        if type(ast)!=str:
            ast=list(ast)

        arr=["<","=",">"]
        ast=swap_(arr,ast)
        ast=equalizer(ast,1)
        return ast
   
    

class Formula_Tree:
    def __init__(self):
        self.grammar_path=grammar_path

    def main_formula(self,str1):
        ls={'...':'\ldot','\colon:':':','\cdot':'*','\to':'\\to','\v':"\\v",'\a':'\\a','\f':'\\f','\n':'\\n','\b':'\\b','\\tfrac':'\\frac','\ \\':"\\",
            '\geqslant':'\geq','\leqslant':'\leq','arrow':'\\rightarrow'}

        grammar = open(self.grammar_path).read()
        parser = tatsu.compile(grammar,asmodel=True)
      
        for x in ls:
            if x in str1:
                str1=str1.replace(x,ls[x])

        try:
            if not '#' in str1:
                a=parser.parse(str1,semantics=CalcSemantics())
                return a
        except:
                return []

    def main(self,str1):
        ls={' >':'>','\\,':' ',' <':'<',' =':'=',' dx':'dx'}
        for x in ls:
            if x in str1:
                str1=str1.replace(x,ls[x])
                
        A=formula_simplifier(str1)
        str1=A.main()
        grammar = open(self.grammar_path).read()
        parser = tatsu.compile(grammar,asmodel=True)
        a=parser.parse(str1,semantics=CalcSemantics())
       
        a=str(a)
        a=a.replace("(","[")
        a=a.replace(")","]")
        a=eval(a)
        return a



