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
