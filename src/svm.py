import numpy as np
import kernel
from sklearn.svm import SVC
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score as a_s

def _labelMaker(labels):
	# Init labeling machine
	mlb = MultiLabelBinarizer()
	# Takes set of all possible labels, and creates a sparse(?) matrix of 1/0 representations of class
	return mlb.fit_transform(labels)

def generateClassifier(features, labels, n, l):
	'''
		This uses sklearn SVM kit using a one vs one approach.
		One-vs-one is more computationally intensive than One-vs-all (n(n-1)/2 vs n)
		but less sensitive to imbalanced data (which we do have, big time)
	'''

	### Generate label representation from ex: 'corn' and 'earn'
	Y = _labelMaker(labels)
	#print(Y.classes_)
	print(Y)
	## Generate Kernel matrix module
	K = kernel.recursive_kernel(features,features,n,l)

	clf = SVC(kernel='precomputed')

	# Return the classifier, god I love how easy this is in python

	print(K)
	return clf.fit(K,Y)

def predict(features, classifier):
	return classifier.predict(features)


def score(prediction,labels):
	return a_s(_labelMaker(labels),prediction)
