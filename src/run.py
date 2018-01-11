import fetch_data as fd
import svm
from random import shuffle

categories = ['acq','earn','corn','crude']
numberOfTraining = [114,152,38,76]
numberOfTesting = [25,40,15,10]


categories = ['corn','crude','acq']
numberOfTraining = [5,5,5]
numberOfTesting = [5,3,5]


trainData,trainLabels, testData,testLabel = fd.loadData(categories,numberOfTraining,numberOfTesting)

n = 1 # Length of subsequence
l = 0.5 # Lambda value

 # Generate a classifier that we can use for prediction.
clf = svm.generateClassifier( trainData, trainLabels, n, l)
print('\n Classifier built')

res = svm.predict(testData,clf,n,l)

print('\n Prediction done')
print(res)

svm.score(res,testLabel)
