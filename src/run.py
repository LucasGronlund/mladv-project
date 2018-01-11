import fetch_data as fd
import svm

categories = ['acq','earn','corn','crude']
numberOfTraining = [114,152,38,76]
numberOfTesting = [25,40,15,10]


categories = ['corn','crude','earn']
numberOfTraining = [3,3,3]
numberOfTesting = [3,3,3]

trainData,trainLabels, testData,testLabel = fd.loadData(categories,numberOfTraining,numberOfTesting)
print(len(trainData), len(testData))
trainLabels[0].append('crude')

#print('Using fullData() takes a long time. We should maybe create a data dump for this?')
#train, test = fullData()
#print(len(train), len(test))

n = 1 # Length of subsequence
l = 0.5 # Lambda value

 # Generate a classifier that we can use for prediction.
clf = svm.generateClassifier( trainData, trainLabels, n, l)
print('Classifier built')
res = svm.predict(testData,clf)
print('prediction done')
score = svm.score(res,testLabel)
print(score)