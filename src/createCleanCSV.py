import fetch_data as fd
import MostFrequentFeaturesWithRemoval as mff
import numpy as np
import os

def createCleanedDataCSV():

    #trainData,trainLabels, testData,testLabel = fd.fullData()

    #cwd = os.getcwd()+'\..\data\clean_data';

    #train = os.path.join(cwd,'cleanedTrainingData.csv')
    #np.savetxt(train, trainData, delimiter=",",fmt='%s')

    #test = os.path.join(cwd,'cleanedTestData.csv')
    #np.savetxt(test, testData, delimiter=",",fmt='%s')

    #trainLbls = os.path.join(cwd,'cleanedTrainingLabels.csv')
    #np.savetxt(trainLbls, trainLabels, delimiter=",",fmt='%s')

    #testLbls = os.path.join(cwd,'cleanedTestLabels.csv')
    #np.savetxt(testLbls, testLabel, delimiter=",",fmt='%s')


def createMostFreqFeatures():
    
    #cwd = os.getcwd()+'\..\data\clean_data';

    #cleanedDataset = np.loadtxt(cwd+'\cleanedTrainingData.csv',delimiter=",",dtype=str);
    
    #f3,s3 = mff.mostFrequentFeatures(cleanedDataset,3,10000)

    #features3k = os.path.join(cwd,'10000features3k.csv')
    #np.savetxt(features3k, f3, delimiter=",",fmt='%s')
    
    #f4,s4 = mff.mostFrequentFeatures(cleanedDataset,4,10000)

    #features4k = os.path.join(cwd,'10000features4k.csv')
    #np.savetxt(features4k, f4, delimiter=",",fmt='%s')
    
    #f5,s5 = mff.mostFrequentFeatures(cleanedDataset,5,10000)

    #features5k = os.path.join(cwd,'10000features5k.csv')
    #np.savetxt(features5k, f5, delimiter=",",fmt='%s')
