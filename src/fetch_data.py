from nltk.corpus import reuters, stopwords
import random, re

def cleanData(txt):
	#lowercase
	txt = txt.lower()
	#keep only words with letters (because f*ck numbers amirite?!)
	txt = re.sub('[^a-z]',' ',txt)
	txt = re.sub(' +', ' ',txt) # remove multiple blank spaces
	#get rid of stopwords in stopwordslist
	txt_list = [w for w in txt.split(' ') if w not in stopwords.words('english')]
	return ' '.join(txt_list)

def loadData(categories, nrTrain, nrTest, shuffle = True):
	testData = []
	trainingData = [] 
	for i, cat in enumerate(categories):
		ids = reuters.fileids(cat)
		if shuffle:
			random.shuffle(ids)
		k = 0
		while(len(trainingData) < sum(nrTrain[:i+1]) or len(testData) < sum(nrTest[:i+1])):
			if ids[k].startswith('train') and len(trainingData) < sum(nrTrain[:i+1]): 
				trainingData.append([ cleanData(reuters.raw(ids[k])), cat])
			elif ids[k].startswith('test') and len(testData) < sum(nrTest[:i+1]):
				testData.append([ cleanData(reuters.raw(ids[k])), cat]) 
			k += 1
	return trainingData, testData



categories = ['acq','earn','corn','crude']
numberOfTraining = [114,152,38,76]
numberOfTesting = [25,40,15,10]
train, test = loadData(categories,numberOfTraining,numberOfTesting)
print(len(train), len(test))
