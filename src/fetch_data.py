from nltk.corpus import reuters, stopwords
import random, re
import sys

def _cleanData(txt):
	#lowercase
	txt = txt.lower()
	#keep only words with letters (because f*ck numbers amirite?!)
	txt = re.sub('[^a-z]',' ',txt)
	txt = re.sub('\s\s+', ' ',txt) # remove multiple blank spaces
	#get rid of stopwords in stopwordslist
	txt_list = [w for w in txt.split(' ') if w not in stopwords.words('english')]
	return ' '.join(txt_list)

def loadData(categories, nrTrain, nrTest, shuffle = True):
	testData = []
	trainingData = [] 
	trainingLabel = []
	testLabel = []
	for i, cat in enumerate(categories):
		ids = reuters.fileids(cat)
		if shuffle:
			random.shuffle(ids)
		k = 0
		while(len(trainingData) < sum(nrTrain[:i+1]) or len(testData) < sum(nrTest[:i+1])):
			if ids[k].startswith('train') and len(trainingData) < sum(nrTrain[:i+1]): 
				trainingData.append( _cleanData(reuters.raw(ids[k])))
				trainingLabel.append([cat])
				# trainingLabel = [i for i in cat if i in reuters.categories(ids[k])] # Jag tror att denna kan göra så att vi klarar multiklass för även mindre dataset
			elif ids[k].startswith('test') and len(testData) < sum(nrTest[:i+1]):
				testData.append( _cleanData(reuters.raw(ids[k]))) 
				testLabel.append([cat])
			k += 1
	return trainingData, trainingLabel, testData, testLabel

def fullData():
	trainingData =[]
	testData =[] 
	testLabel = []
	trainingLabel = []
	ids = reuters.fileids()
	c=0
	for i in ids:
		if i.startswith('train'):
			trainingData.append(_cleanData(reuters.raw(i)))
			trainingLabel.append(reuters.categories(i))
		elif i.startswith('test'):
			testData.append(_cleanData(reuters.raw(i)))
			testLabel.append(reuters.categories(i))
		c=c+1;
		sys.stdout.write(repr(len(ids)-c)+'\r')
		sys.stdout.flush()

	return trainingData, trainingLabel, testData, testLabel

def nrData(nr):
	data =[]
	ids = reuters.fileids()
	c=0
	for i in ids:

                data.append(_cleanData(reuters.raw(i)))

                if(len(data)==nr): break
                c=c+1;
                sys.stdout.write(repr(nr-c)+'\r')
                sys.stdout.flush()
                
	return data
