import fetch_data as fd
import numpy as np
import os

def createCleanedCSV():

    trainData,trainLabels, testData,testLabel = fd.fullData()

    cwd = os.getcwd()+'\..\data\clean_data';

    train = os.path.join(cwd,'cleanedTrainingData.csv')
    np.savetxt(train, trainData, delimiter=",",fmt='%s')

    test = os.path.join(cwd,'cleanedTestData.csv')
    np.savetxt(test, testData, delimiter=",",fmt='%s')

    trainLbls = os.path.join(cwd,'cleanedTrainingLabels.csv')
    np.savetxt(trainLbls, trainLabels, delimiter=",",fmt='%s')

    testLbls = os.path.join(cwd,'cleanedTestLabels.csv')
    np.savetxt(testLbls, testLabel, delimiter=",",fmt='%s')
