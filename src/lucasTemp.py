import numpy as np
import itertools as it
from tqdm import tqdm
from math import sqrt
from alignment import alignment as align

def precomputedKernelComparions(Kdp,Kxs,Kss,Kxx,least=False,random=False):
    
    #-----------------------------------------#
    # Returns a vectors with frobenius values #
    # for the approximation and DP kernels.   #
    #                                         #
    # Variables:                              #
    #                                         #
    # Kdp - Precomputed DP-kernel             #
    #                                         #
    # Kxs - Precomputed kernel between docum- #
    #       ents and 3-grams                  #
    #                                         #
    # Kss - Precomputed kernel between 3-grams#
    #                                         #
    # Kxx - Precomputed kernel between docum- #
    #       ents                              #
    #-----------------------------------------#

    #kMatrices = np.zeros([89,Kdp.shape[0],Kdp.shape[0]]);
    kMatrices = np.zeros([len(Kss),Kdp.shape[0],Kdp.shape[0]]);

    if(least):
        Kss = Kss[::-1]
        Kxs = np.flip(Kxs,1)
    if(random):
        randomize = np.arange(len(Kss));
        np.random.shuffle(randomize);
        Kss = Kss[randomize];
        Kxs = Kxs[:,randomize];
    
    for i in tqdm(range(Kdp.shape[0])):
        for j in range(Kdp.shape[1]):
            c=0;
            kTemp=0;
            for s in range(len(Kss)):
                kTemp += Kxs[i][s]*Kxs[j][s]/(Kss[s]*sqrt(Kxx[i]*Kxx[j]))
                if(s%1==0 and s<=200):
                    kMatrices[c][i][j] = kTemp;
                    c = c+1;
                elif(s%1==0 and s>200):
                    kMatrices[c][i][j] = kTemp;
                    c = c+1;
    frobValues = np.zeros(kMatrices.shape[0])
    
    for ind,m in enumerate(tqdm(kMatrices)):
        frobValues[ind] = align(m,Kdp);

    return frobValues

