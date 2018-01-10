import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score as a_s

def _labelMaker(labels):
	# Init labeling machine
	mlb = MultiLabelBinarizer()
	# Takes set of all possible labels, and creates a sparse(?) matrix of 1/0 representations of class
	return mlb.fit_transform(set(labels))

def generateClassifier(features, labels):
	'''
		This uses sklearn SVM kit using a one vs one approach.
		One-vs-one is more computationally intensive than One-vs-all (n(n-1)/2 vs n)
		but less sensitive to imbalanced data (which we do have, big time)
	'''

	Y = _labelMaker(labels)

	#Compute Kernel matrix K, we need to precompute it for 
	K = []

	clf = SVC(kernel='precomputed')

	# Return the classifier, god I love how easy this is in python

	return clf.fit(K,Y)

def predict(features, classifier):
	return classifier.predict(features)


def score(prediction,labels):
	return a_s(_labelMaker(labels),prediction)
