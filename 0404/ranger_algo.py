# create N tuples that will serve as permutation functions
# these permutation values are used to hash all input sets
from random import randint
N=1000
max_val=100000
perms = [ (randint(0,max_val), randint(0,max_val)) for i in range(N)]

# initialize a sample minhash vector of length N
# each record will be represented by its own vec
vec = [float('inf') for i in range(N)]

def minhash(s, prime=4294967311):
  '''
  Given a set `s`, pass each member of the set through all permutation
  functions, and set the `ith` position of `vec` to the `ith` permutation
  function's output if that output is smaller than `vec[i]`.
  '''
  # initialize a minhash of length N with positive infinity values
  vec = [float('inf') for i in range(N)]

  for val in s:

    # ensure s is composed of integers
    if not isinstance(val, int): val = hash(val)

    # loop over each "permutation function"
    for perm_idx, perm_vals in enumerate(perms):
      a, b = perm_vals

      # pass `val` through the `ith` permutation function
      output = (a * val + b) % prime

      # conditionally update the `ith` value of vec
      if vec[perm_idx] > output:
        vec[perm_idx] = output

  # the returned vector represents the minimum hash of the set s
  return vec

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
        dict1={}
        for x in tmp:
            temp.append(x.split(' '))

        for i in range(len(temp)):
            for j in range(len(temp[i])):
                if len(temp[i][j])==1:
                    if temp[i][j] in dict1.keys():
                        temp[i][j]=dict1[temp[i][j]]

        return temp

def algorithm_three_func(a,b):
    value=0
    ind=[]
    i,j=0,0
    a=simplifier_algo_three(a)
    b=simplifier_algo_three(b)
    
    for x in a:
        i=i+1
        for y in b:
            j=j+1
            c=jaccard_coeff_algo_three(x,y)
            value=value+c*i/len(a)

    return value         
            
