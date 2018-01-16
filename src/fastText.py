import fasttext
import fetch_data as fd
import numpy as np
import MostFrequentFeatures as MF

path = '/Users/Viktor/GitHub/mladv-project/data/clean_data/'

categories = ['earn','acq','crude','corn']
numberOfTraining = [1,1,1,1]
numberOfTesting = [10,10,10,10]
trainData, trainLabels, testData, testLabels = fd.loadData(categories,numberOfTraining,numberOfTesting)

print(trainData)
trainMF = []
for text in trainData:
	temp, trash = MF.mostFrequentFeatures(text,3,10)
	sentence = ''
	for word in temp:
		sentence += word +' '
	trainMF.append(sentence)	

print(trainMF)

if(False):
	# make data into txt file with labels after __label__ 
	modTrainData = trainData
	for index, text in enumerate(trainData):
		modTrainData[index] = '__label__' + trainLabels[index][0] + ' ' + modTrainData[index]

	modTestData = testData
	for index, test in enumerate(testData):
		modTestData[index] = '__label__' + testLabels[index][0] + ' ' + modTestData[index]

	np.savetxt(path + 'fastTextTrainData.txt',modTrainData, delimiter =',',fmt = '%s')
	np.savetxt(path + 'fastTextTestData.txt',modTestData, delimiter =',',fmt = '%s')

classifier = fasttext.supervised(path + 'fastTextTrainData.txt', 'model', dim = 100, epoch = 25, lr = 0.9, word_ngrams = 1)

result = classifier.test(path + 'fastTextTestData.txt',4)
labs = classifier.predict_proba(path + 'fastTextTestData.txt')

correct = 0
for i, trash in enumerate(testLabels):
	print(labs[i], testLabels[i])
	if labs[i][0] == testLabels[i][0]: correct +=1

print('P@4:', result.precision)
print('R@4:', result.recall)
print('F1: ', 2*result.precision * result.recall / (result.recall + result.precision))
print('Number of examples:', result.nexamples)
