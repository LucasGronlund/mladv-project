import fetch_data as fd
import svm

categories = ['acq','earn','corn','crude']
numberOfTraining = [114,152,38,76]
numberOfTesting = [25,40,15,10]


categories = ['earn','crude']
numberOfTraining = [10,10]
numberOfTesting = [7,2]


trainData,trainLabels, testData,testLabel = fd.loadData(categories,numberOfTraining,numberOfTesting)

n = 2 # Length of subsequence
l = 0.5 # Lambda value

 # Generate a classifier that we can use for prediction.
clf = svm.generateClassifier( trainData, trainLabels, n, l,categories)
print('\n Classifier built')


res = svm.predict(testData,trainData,clf,n,l)

print('\n Prediction done')
print(res)

svm.score(res,testLabel,categories)
