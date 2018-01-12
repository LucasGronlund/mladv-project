import numpy as np
import kernel
from sklearn.svm import SVC
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, f1_score


def _labelMaker(labels):
	# Init labeling machine
	mlb = MultiLabelBinarizer()
	# Takes set of all possible labels, and creates a sparse(?) matrix of 1/0 representations of class	
	return mlb.fit_transform(labels)



	'''
		This uses sklearn SVM kit using a one vs rest approach.
		One-vs-one is more computationally intensive than One-vs-all (n(n-1)/2 vs n)
		but less sensitive to imbalanced data (which we do have, big time). This might have to bee looked at
	'''


def generateClassifier(features, labels, n, l):

	### Generate label representation from ex: 'corn' and 'earn'
	Y = _labelMaker(labels)

	## Generate Kernel matrix module
	K = kernel.recursive_kernel(features,features,n,l)

	clf = OneVsRestClassifier(SVC(kernel='precomputed'))
	
	# Return the classifier, god I love how easy this is in python
	return clf.fit(K,Y)

def predict(features,control, classifier, n,l):
	K = kernel.recursive_kernel(features,control,n,l)
	print('\n'*3)
	print(K.shape)
	return classifier.predict(K)


def score(prediction,labels):
		print('Accuracy: ' + str(accuracy_score(_labelMaker(labels),prediction)))
