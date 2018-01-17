import numpy as np
import kernel
import MostFrequentFeatures as mff
import os
import csv
from io import StringIO
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
		x = mff.mostFrequentFeatures(t,n,100)
		K = kernel.approximative_kernel(s,t,x,n,l)
	elif kern == 'wk':
		K = kernel.wk(s,t)
	elif kern == 'ngk':
		K = kernel.ngk(s,t,n)
	elif kern == 'cppr':
		K = kernel.cpp_recursive_kernel(s,t,n,l)
	elif kern == 'cppa':
		if n == 3:
			cwd = os.getcwd()+'/../data/clean_data/10000features3k.csv'
		elif n == 4:
			cwd = os.getcwd()+'/../data/clean_data/10000features4k.csv'
		elif n == 5:
			cwd = os.getcwd()+'/../data/clean_data/10000features5k.csv'
		else:
			print('Not correct number of K with precleaned data.')
			return 0

		x =[]
		with open(cwd,newline='') as csvfile:
			rdr = csv.reader(csvfile, delimiter=',', quotechar='|')
			for i in rdr:
				x.append(i[0])
		feat = 3000
		print('Number of feature vectors in s: ' + str(feat))
		x = x[0:feat]

		K = kernel.cpp_approximative_kernel(s,t,x,n,l) 
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
	c = 1.0	
	print(' C = ' + str(c))
	clf = OneVsRestClassifier(SVC(C = c, kernel='precomputed',decision_function_shape = 'ovo',class_weight = 'balanced'))
	# Return the classifier, god I love how easy this is in python
	return clf.fit(K,Y)

def classifier_precomputed(K_train, K_test,Train_labels,test_labels,cat):

	### Generate label representation from ex: 'corn' and 'earn'
	Y = _labelMaker(Train_labels,cat)

	## Generate Kernel matrix module
	c = 1	
	print(' C = ' + str(c))
	clf = OneVsRestClassifier(SVC(C = c, kernel='precomputed',decision_function_shape = 'ovo',class_weight = 'balanced'))
	# Return the classifier, god I love how easy this is in python
	pred = clf.fit(K_train,Y).predict(K_test)
	print(classification_report(_labelMaker(test_labels,cat),pred,target_names=cat))


def predict(features,control, classifier, n,l,kern):
	K = _giveK(features,control,n,l,kern)	
	return classifier.predict(K)


def score(prediction,labels,categories):
		print(classification_report(_labelMaker(labels,categories),prediction,target_names = categories))
