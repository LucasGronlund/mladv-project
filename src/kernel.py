import numpy as np
import itertools as it
from tqdm import tqdm
from math import sqrt

##### NAIVE KERNEL #####

def naiveKernel(data,k,l):
    
    #create all 'good' permutations, that is those which are possible
    perms=[];
    for i in data:
        tmpPerms = list(it.combinations(i,k));
        for j in tmpPerms:
            if(j not in perms):
                perms.append(j);
    
    #init the result matrix
    fi = np.zeros([len(data),len(perms)]);
    
    #calculate each fi_u for each string
    for row in range(len(data)):
        for c, prm in enumerate(perms):
            tmpSum = [];
            indices = [];
            
            #create a vector containing the indexes of the current permutation letters
            for i in range(k):
                indices.append(list(_find(data[row],prm[i])))
            
            #calculate all the values, recursively because i couldn't figure out
            #how to generalize otherwise.
            for i in indices[0]:
                tmpSum = _recursiveShit(indices[1:],i,i,k-2,tmpSum);
            
            #calculate the current fi_u value
            for i in tmpSum:
                fi[row,c] += np.sum(l**(np.array([i])));
                
    return fi;

                

def _recursiveShit(currInd,topVal,prevVal,k,tmpSum):
    #bad recursion, but it works
    
    #base case, check if it's an approved permutation,
    #if yes -> return the sum
    if(k==0):
        for i in currInd[0]:
            if(i>prevVal):
                tmpSum.append(i-topVal+1);
        return tmpSum;
    
    #if not yet at the 'bottom' of the recursion, continue
    else:
        for i in currInd[0]:
            if(i>prevVal):
                tmpSum = _recursiveShit(currInd[1:],topVal,i,k-1,tmpSum);
        return tmpSum
            
            
    

def _find(str, ch):
    #_find indexes of characters in string
    
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i


#### DYNAMIC PROGRAMMING KERNEL #####

def _k_prime(s,t,n,l):

    #-------------------------------------------------------------------------------------#
    # Basically what's happening here is that we are succesively looping through both of  #
    # the strings and updating the kernel matrix accordingly while refering to previously #
    # computed values. This will give us time complexity O(n|s||t|) in the end.           #
    #-------------------------------------------------------------------------------------#
    
    
    #Variables:
    #
    #s is a string
    #t is a string
    #n is the length of the substring
    #l is the lambda value
    #kp is refering to k'
    #kpp is refering to k'' 
    
    #start by creating the empty matrices.
    kp = np.zeros([n,len(s)+1,len(t)+1]);
    kpp = np.zeros([n,len(s)+1,len(t)+1]);
    
    #initialize
    kp[0][:][:] = 1;
    
    for i in range(1,n):
        for j in range(i,len(s)):
            for k in range(i,len(t)+1):

                #check whether 'x occurs in u' as described in the paper
                if(s[j-1]!=t[k-1]):
                    kpp[i][j][k]=l*kpp[i][j][k-1];
                #if not, do the other calcs.
                else:
                    kpp[i][j][k]=l*(kpp[i][j][k-1]+l*kp[i-1][j-1][k-1]);
                
                #finally calculate kp
                kp[i][j][k-1]=l*kp[i][j-1][k-1]+kpp[i][j][k-1];
                
    return kp;


def _k(s,t,n,l,kp):
    
    #--------------------------------------------------#
    # This takes in an already computed k_prime kernel #
    # and calculates the overall kernel as per the     #
    # paper. The last part of Def. 2                   #
    #--------------------------------------------------#

    #Variables:
    #
    #s is a string
    #t is a string
    #n is the length of the substring
    #l is the lambda value
    #kp is refering to k'
    #ksum is refering to the kernel value.
    
    ksum = 0;
    
    #Loop over all values in the computed k_prime matrix and 
    #pick out the values where x = j, as mentioned in the paper.
    #
    #There is no recursion necessary here since we already did it
    #when computing k_prime, the last 'layer' of k_prime
    #contains all the necessary values.
    
    for i in range(kp.shape[1]-1):
        for j in range(kp.shape[2]-1):
            if(s[i]==t[j]):
                ksum += kp[n-1][i][j];
                
    return l**2*ksum;

def _get_normed_kernel_values(s,t,n,l):
    
    #------------------------------------------------------#
    # This returns the normalized values for the kernel    # 
    # using the normalization mentioned in the paper.      #
    # s is a string.                                       #
    # t is a string.                                       #
    # n is the substring length                            #           
    # l is the lambda value, the 'weight'                  #
    #------------------------------------------------------#
    
    kstP = _k_prime(s,t,n,l);
    kssP = _k_prime(s,s,n,l);
    kttP = _k_prime(t,t,n,l);

    kst = _k(s,t,n,l,kstP)
    kss = _k(s,s,n,l,kssP);
    ktt = _k(t,t,n,l,kttP);
    
    return kst/sqrt(kss*ktt)

def recursive_kernel(s,t,n,l):
    if len(s) != len(t):
        print('s != t , Kernel Matrix not square. This code is not adapted for that')
        return 0

    N = len(s)
    K = np.identity(N)
    
    for i in tqdm(range(N)):
        for j in tqdm(range(i+1,N)):
            #Compute Kernel matrix K, we need to precompute it for
            k = _get_normed_kernel_values(s[i],t[j],n,l) 
            K[i,j] = k
            K[j,i] = k # Using this method to compute half of K and using that the matrix is semi definite

    return K
