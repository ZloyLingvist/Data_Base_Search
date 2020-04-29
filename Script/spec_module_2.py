from processing import *
from formula_tree import *
from ranger import *
from text_tree import *
from draw_graph import *
from utilities import *
from stamford import *
from testing_block import *

import sys

path = os.path.dirname(os.path.dirname(__file__))
path_old=path

text="Если  {\displaystyle F (x)} – любая первообразная функции {\displaystyle f (x)},  то справедливо равенство {\displaystyle \int \limits _{a}^{x} f(t)\,dt=F(x)-F(a)} ."

def make_razbor(theorem):
    '''
    если theorem - утверждение теоремы в текстовом виде (строка), то преобразуем его к таблице с синтаксическим разбором.
                 - утверждение теоремы уже в виде таблицы с синтаксическим разбором, то ничего не делаем
         представление в виде таблицы с синтаксическим разбором подаем на вход модуля преобразования на язык логики предикатов.
         затем подставляем в него разобранные формулы.
    '''
    if type(theorem)==str:
        a=preprocessing(theorem.strip(),path_old)
    else:
        a=theorem

    A=Stamford()
    c=A.main(a,1)
    print(c)
    #c=combine_formula_and_text(c,path_old)
    #return c

make_razbor(text)
