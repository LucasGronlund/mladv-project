import os
import numpy as np

def getData(fileName):

    cwd = os.getcwd()+'\..\data\clean_data';

    txt=np.loadtxt(cwd+'\{}'.format(fileName),delimiter=",",dtype=str)

    return txt
