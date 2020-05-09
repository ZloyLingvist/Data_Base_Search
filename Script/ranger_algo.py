import re

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def jaccard_coeff_algo_three(tmp1,tmp2):
        S1=set(i for i in tmp1)
        S2=set(i for i in tmp2)
        intersection = len(list(S1.intersection(S2)))
        union = (len(S1) + len(S2)) - intersection
        if union!=0:
            res=float(intersection) / union
        else:
            res=0

        return res

            
def path_to_leaves_algo_three(l,tmp,str1):
        for i,elem in enumerate(l):
            if not isinstance(elem,str):         
                l[i]=path_to_leaves_algo_three(elem,tmp,str1)
            else:
                if str1=="":
                    str1=elem
                else:
                    str1=str1+' '+elem
                tmp.append(str1)
                
        return l
    
def simplifier_algo_three(a):
        str1=""
        tmp=[]
        path_to_leaves_algo_three(a,tmp,str1)
        temp=[]

        result=[]
       
        for x in tmp:
            temp.append(x.split(' '))

        '''
        for i in range(len(temp)-1,-1,-1):
                for j in range(len(temp[i])-1,-1,-1):
                        if has_cyrillic(temp[i][j])==True:
                                del temp[i][j]
        '''
        for i in range(len(temp)-1,-1,-1):
            result.append([1,temp[i]])
            for j in range(len(temp)-1,i+1,-1):
                if temp[i]==temp[j]:
                    for k in range(len(result)):
                        if result[k][1]==temp[j]:
                            result[k][0]=result[k][0]+1
                            break
                        
                    del temp[j]

        return temp,result

def algorithm_three_func(a,b):
    value=0
    ind=[]
    i,j=0,0
    coeff=1
    a,r1=simplifier_algo_three(a)
    b,r2=simplifier_algo_three(b)

    for x in a:
        i=i+1
        coeff=1
        for m in range(len(b)):
            mult=0
            
            for k in range(len(r1)):
                if r1[k][1]==x:
                    mult=r1[k][0]
                    break

            for k in range(len(r2)):
                if r2[k][1]==x:
                    mult=mult+r2[k][0]
                    break
            
            coeff=coeff+mult*jaccard_coeff_algo_three(x,b[m])
                
        value=value+coeff*(i/len(a))


    return value

'''
def main(a,b):
    A=algorithm_three_func(a,b)
    B=algorithm_three_func(a,a)
    C=algorithm_three_func(b,a)
    D=algorithm_three_func(b,b)
    return (A/B+C/D)*0.5
'''    

'''
a=[['if', ['&', ['C', ['f'], ['1'], [['closed_interval', ['a'], ['b']]], ['values'], ['и'], ['конец'], ['его'], ['знак'], ['разный']], ['closed_interval', ['a'], ['b']], ['function', 'f']]], ['then', ['&', ['exists', ['closed_interval'], ['внутри'], ['a']], ['point', 'a'], ['обращаться', ['point'], ['f'], ['0']]]]]
b=[['if', ['&', ['C', ['f'], ['1'], [['f']], ['segment'], ['values'], ['и'], ['конец'], ['свой'], ['знак'], ['разный']], ['function', ['f']]]], ['then', ['&', ['exists', 'point', 'такой', 'formula_', '102', ['point', 'formula_']], ['принадлежать', ['отрезка'], ['этот']], ['отрезка', 'formula_129']]]]
c=[['if', ['&', ['C', ['f'], ['1'], [['closed_interval', ['a'], ['b']]], ['values'], ['и'], ['конец'], ['closed_interval'], ['этот'], ['знак'], ['разный']], ['closed_interval', ['a'], ['b']]]], ['then', ['&', ['exists', ['{\\displaystyle \\int \\limits _{a}}^{b}} f(x) dx=f(\\xi)\\cdot (b-a)}'], ['a', 'b'], ['point', ['{\\displaystyle \\int \\limits _{a}}^{b}} f(x) dx=f(\\xi)\\cdot (b-a)}']]], ['open_interval', ['a', 'b']], ['point', ['a', 'b']], ['0', ['open_interval'], ['значение'], ['function'], ['equal']]]]]

r=main(a,b)
print(r)
'''
