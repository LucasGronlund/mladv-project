import numpy as np
import itertools as it
from tqdm import tqdm
from math import sqrt

##### NAIVE KERNEL #####

def naive_kernel(data,k,l):
    
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

def _k_prime(s,t,n,l,cutoff):

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
    #
    #----NEW-----
    #
    #cutoff is the maximum length of the string that will be checked.

    newT = min(cutoff+1,len(t)+1);
    
    #start by creating the empty matrices.
    kp = np.zeros([n,len(s)+1,newT]);
    kpp = np.zeros([n,len(s)+1,newT]);
    #initialize
    kp[0][:][:] = 1;
    for i in range(1,n):
        for j in range(i,len(s)):
            for k in range(i,newT):
                #check whether 'x occurs in u' as described in the paper
                if(s[j-1]!=t[k-1]):
                    kpp[i][j][k]=l*kpp[i][j][k-1];
                #if not, do the other calcs.
                else:
                    kpp[i][j][k]=l*(kpp[i][j][k-1]+l*kp[i-1][j-1][k-1]);
                
                #finally calculate kp
                kp[i][j][k-1]=l*kp[i][j-1][k-1]+kpp[i][j][k-1];
                
    return kp;


def _k(s,t,n,l,kp,cutoff):
    
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
            if s[i] == t[j] : 
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
    kss = [ _k(i,i,n,l,_k_prime(i,i,n,l)) for i in s]
    if hash(tuple(s)) != hash(tuple(t)):
        print('Number of strings are not equal, reverting to slower, non-square, computation of K')
        K = np.zeros([len(s),len(t)])        
        ktt = [ _k(i,i,n,l,_k_prime(i,i,n,l)) for i in t]
        for i,ss in enumerate(tqdm(s)):
            for j,tt in enumerate(tqdm(t)):
                kst = _k(ss,tt,n,l,_k_prime(ss,tt,n,l))
                #Compute Kernel matrix K, we need to precompute it for
                K[i,j] = kst/sqrt(kss[i]*ktt[j])
        return K

    N = len(s)
    K = np.identity(N)
    
    for i in tqdm(range(N)):
        for j in tqdm(range(i+1,N)):
            kstP = _k_prime(s[i],t[j],n,l);
            kst = _k(s[i],t[j],n,l,kstP)
            #Compute Kernel matrix K, we need to precompute it for
            k = kst/sqrt(kss[i]*kss[j])
            K[i,j] = k
            K[j,i] = k # Using this method to compute half of K and using that the matrix is semi definite

    return K


#### APPROXIMATIVE KERNEL IMPLEMENTATION #####

def approximative_kernel(x,z,s,n,l,cutoff):
    N = len(x)
    kss = [ _k(i,i,n,l,_k_prime(i,i,n,l,cutoff),cutoff) for i in tqdm(s)]
    kxx = [ _k(i,i,n,l,_k_prime(i,i,n,l,cutoff),cutoff) for i in tqdm(x)]
    kxs = kernelValuesListChptr6(x,s,n,l,cutoff)    
    if hash(tuple(x)) == hash(tuple(z)):
        K = np.identity(N)
        print('Square kernel matrix generated')
        for i,xx in enumerate(x):
            for j in range(i+1,N):
                for k,ss in enumerate(s):
                    k = (kxs[i][k]*kxs[j][k])/(kss[k]*sqrt(kxx[j]*kxx[i]))
                    K[i,j] += k
                    K[j,i] += k
        return K   

    K = np.zeros([N,len(z)])
    kzz = [ _k(i,i,n,l,_k_prime(i,i,n,l,cutoff)) for i in z]
    kzs = kernelValuesListChptr6(z,s,n,l,cutoff)
    for i,xx in enumerate(tqdm(x)):
        for j,zz in enumerate(tqdm(z)):
            for k,ss in enumerate(tqdm(s)):
                K[i,j] += (kxs[i][k]*kxz[j][k])/(kss[k]*sqrt(kzz[j]*kxx[i]))
    return K

def kernelValuesList(x,n,l):
    kVal = [_k(i,i,n,l,_k_prime(i,i,n,l,cutoff)) for i in x]
    return kVal

def kernelValuesListChptr6(x,s,n,l,cutoff):
    Kxs = np.zeros([len(x),len(s)]);
    for i in tqdm(range(len(x))):
        for j in range(len(s)):
            Kxs[i][j]=_k(x[i],s[j],n,l,_k_prime(x[i],s[j],n,l,cutoff),cutoff)
    return Kxs



#### WK ####

def wk(s,t):
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

    vec = CountVectorizer(analyzer = 'word')
    transformer = TfidfTransformer(smooth_idf = True)


    t_wk = transformer.fit_transform(vec.fit_transform(t).toarray()).toarray()
    s_wk = transformer.fit_transform(vec.transform(s).toarray()).toarray()

    K = np.zeros((len(s),len(t)))
    for i in range(len(s)):
        for j in range(len(t)):
            K[i][j] = s_wk[i].dot(t_wk[j])
    return K

#### NGK ####

def ngk(s,t,n): 
    
    #Normalize
    K = np.zeros((len(s),len(t))).astype(float)
    
    def _normalize(s,t,n):
        p1 = set([s[i:i+n] for i in range(len(s)-n+1)])
        p2 = set([t[i:i+n] for i in range(len(t)-n+1)])

        same = 0.0;
        unique = 0.0;

        same = float(len(p1 & p2))
        unique = float(len(p1 | p2))
        if unique == 0.0:
            return 1.0
        return same/unique

    for i in range(len(s)):
        
        for j in range(len(t)):
            
            K[i][j] = _normalize(s[i],t[j],n)
    return K


#### C++ RECURSIVE KERNEL ####

def _parseMatrix(matrix):
        num_rows = int(matrix[0])
        num_cols = int(matrix[1])
        K = np.zeros([num_rows,num_cols])
        counter = 2
        for i in range(num_rows):
            for j in range(num_cols):
                K[i,j] = float(matrix[counter])
                counter = counter + 1
        return K

def cpp_recursive_kernel(s,t,n,l):
    import subprocess
    import io
    test = subprocess.Popen(["g++","fast_recursive_kernel.cpp","-o","fast_recursive_kernel.out"], stdout=subprocess.PIPE)
    output_compile = test.communicate()[0]


    the_strings = b''
    the_args = bytes(str(len(s)),'ascii')+ b' ' + bytes(str(len(t)),'ascii')+ b' '
    for i in s:
        the_strings = the_strings + bytes(i,'ascii')
        the_args = the_args + bytes(str(len(i)),'ascii') + b' '
    for i in t:
        the_strings = the_strings + bytes(i,'ascii')
        the_args = the_args + bytes(str(len(i)),'ascii') + b' '
    the_args = the_args + bytes(str(n), 'ascii')+ b' ' + bytes(str(l), 'ascii')
    fast_kernel = subprocess.Popen(["./fast_recursive_kernel.out"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output_test = fast_kernel.communicate(input=b'1 '+the_args+the_strings)[0]
    output_test_list = output_test.decode('utf-8').split()
    K = _parseMatrix(output_test_list)
    return K


def cpp_approximative_kernel(x,z,s,n,lmda):
    import subprocess
    import io
    test = subprocess.Popen(["g++","fast_approximative_kernel.cpp","-o","fast_approximative_kernel.out"], stdout=subprocess.PIPE)
    output_compile = test.communicate()[0]

    the_strings = b''
    if hash(tuple(x)) == hash(tuple(z)):
        equal_hash = b'1 '
    else:
        equal_hash = b'0 '
    the_args = bytes(str(len(x)),'ascii')+ b' ' + bytes(str(len(z)),'ascii')+ b' ' + bytes(str(len(s)),'ascii')+ b' '
    for i in x:
        the_strings = the_strings + bytes(i,'ascii')
        the_args = the_args + bytes(str(len(i)),'ascii') + b' '
    for i in z:
        the_strings = the_strings + bytes(i,'ascii')
        the_args = the_args + bytes(str(len(i)),'ascii') + b' '
    for i in s:
        the_strings = the_strings + bytes(i,'ascii')
        the_args = the_args + bytes(str(len(i)),'ascii') + b' '
    the_args = the_args + bytes(str(n), 'ascii')+ b' ' + bytes(str(lmda), 'ascii')
    fast_kernel = subprocess.Popen(["./fast_approximative_kernel.out"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output_test = fast_kernel.communicate(input=equal_hash+the_args+the_strings)[0]
#     print(output_test.decode('utf-8'))
    output_test_list = output_test.decode('utf-8').split()
    K = _parseMatrix(output_test_list)
    return K
