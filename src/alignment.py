
# coding: utf-8

# In[21]:
import numpy as np


def alignment(A, B):
    # A and B must have identical dimensions! dont be stupid trying anything else boi
    if A.shape != B.shape:
        print("Dimension error")
        return 0
    
    AB = forbenius(A,B)
    AA = forbenius(A,A)
    BB = forbenius(B,B)
    
    return AB/np.sqrt(AA*BB)

def forbenius(A, B):
    if A.shape != B.shape:
        print("Dimension error")
        return 0
    
    res = 0
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            res += A[i,j]*B[i,j]            
    return res

