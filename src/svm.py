import numpy as np
import kernel
from sklearn.svm import SVC
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report

# Takes set of all possible labels, and creates a sparse(?) matrix of 1/0 representations of class	
def _labelMaker(labels,categories):
	return MultiLabelBinarizer(classes=categories).fit_transform(labels)

def _giveK(s,t,n,l,kern):
	K = []
	if kern == 'r':
		K = kernel.recursive_kernel(s,t,n,l)
	elif kern == 'a':
		K = kernel.approximative_kernel(s,t,n,l)
	elif kern == 'wk':
		K = kernel.wk(s,t)
	elif kern == 'ngk':
		K = kernel.ngk(s,t,n)
	return K
	'''
		This uses sklearn SVM kit using a one vs rest approach.
		One-vs-one is more computationally intensive than One-vs-all (n(n-1)/2 vs n)
		but less sensitive to imbalanced data (which we do have, big time). This might have to bee looked at
	'''


def generateClassifier(features, labels, n, l,cat,kern):

	### Generate label representation from ex: 'corn' and 'earn'
	Y = _labelMaker(labels,cat)

	## Generate Kernel matrix module
	K = _giveK(features,features,n,l,kern)

	clf = OneVsRestClassifier(SVC(kernel='precomputed',decision_function_shape = 'ovr',class_weight = 'balanced'))
	# Return the classifier, god I love how easy this is in python
	return clf.fit(K,Y)

def predict(features,control, classifier, n,l,kern):
	K = _giveK(features,control,n,l,kern)	
	return classifier.predict(K)


def score(prediction,labels,categories):
		print(classification_report(_labelMaker(labels,categories),prediction))