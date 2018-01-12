import numpy as np
import kernel
from sklearn.svm import SVC
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import precision_recall_fscore_support

# Takes set of all possible labels, and creates a sparse(?) matrix of 1/0 representations of class	
def _labelMaker(labels,categories):
	return MultiLabelBinarizer(classes=categories).fit_transform(labels)

def labelMaker(labels,categories):
	return LabelEncoder().fit_transform(labels)

	'''
		This uses sklearn SVM kit using a one vs rest approach.
		One-vs-one is more computationally intensive than One-vs-all (n(n-1)/2 vs n)
		but less sensitive to imbalanced data (which we do have, big time). This might have to bee looked at
	'''


def generateClassifier(features, labels, n, l,cat):

	### Generate label representation from ex: 'corn' and 'earn'
	Y = _labelMaker(labels,cat)
	print(Y)
	## Generate Kernel matrix module
	K = kernel.recursive_kernel(features,features,n,l)

	clf = OneVsRestClassifier(SVC(kernel='precomputed',probability = True))

	# Return the classifier, god I love how easy this is in python
	return clf.fit(K,Y)

def predict(features,control, classifier, n,l):
	K = kernel.recursive_kernel(features,control,n,l)
	return classifier.predict(K)


def score(prediction,labels,categories):
		print('Scores: ' + str(precision_recall_fscore_support(_labelMaker(labels,categories),prediction)))