import numpy as np
import random
import math

sF=10.0


def parallelOptimization_K(K):
  print(K)
  stepFactor=sF
  n = 800 #multiple of 4
  eta = stepFactor * np.log(n*K) / (n*K)
  e1 = []
  e2 = []

  for rep in range(reps):
    e1.append(singleShuffle(eta, n, K))
    e2.append(singleShuffle_Flipping(eta, n, K))

  
  d1_75=np.percentile(e1, 75, interpolation = 'midpoint')
  d1_25=np.percentile(e1, 25, interpolation = 'midpoint') 
  d2_75=np.percentile(e2, 75, interpolation = 'midpoint') 
  d2_25=np.percentile(e2, 25, interpolation = 'midpoint')
  return [np.median(e1), d1_75, d1_25, np.median(e2), d2_75, d2_25, K]


def singleShuffle(eta, n, K):
  x=math.log(3)+np.random.normal(0,1)
  
  # r = np.random.permutation(np.concatenate((-np.zeros(3*int(n/4)), np.ones(int(n/4)))))  
  r=np.concatenate((-np.zeros(3*int(n/4)), np.ones(int(n/4))))
  random.shuffle(r)
  for i in range(1, K+1):
    for j in range(0, n):
      x = x - eta/(1+math.exp(-x)) + eta*r[j] # The gradient step.
  return (x+math.log(3))**2 # This is the error, since the minimizer is x=-log 3

def singleShuffle_Flipping(eta, n, K):
  x=math.log(3)+np.random.normal(0,1)
  
  # r = np.random.permutation(np.concatenate((-np.zeros(3*int(n/4)), np.ones(int(n/4)))))  
  r=np.concatenate((-np.zeros(3*int(n/4)), np.ones(int(n/4))))
  random.shuffle(r)
  for i in range(1, int(K/2)+1):
    for j in range(0, n):
      x = x - eta/(1+math.exp(-x)) + eta*r[j] # The gradient step.

    for j in range(0, n):
      x = x - eta/(1+math.exp(-x)) + eta*r[n-1-j] # The gradient step.

  return (x+math.log(3))**2 # This is the error, since the minimizer is x=-log 3


reps = 10
K_beg=30 # should be even
K_end=300
x_list=[]
l1=[];l2=[];l3=[]
# pool = multiprocessing.Pool(16)
K_range = range(K_beg,K_end,4)
results=[]
for k in K_range:
  results.append(parallelOptimization_K(k))

f = open('plotdatanew/SS', 'w') # Replace with desired output file name
f.write("\n".join([",".join([str(r) for r in res]) for res in results]))
