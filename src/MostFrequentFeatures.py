
# coding: utf-8

# In[100]:


import itertools as it
import numpy as np
from tqdm import tqdm 

def mostFrequentFeatures(dataset, k, numbTop,prints = False):
    if prints == True:
        print('You just asked for ' + str(27**k) + ' features. Get ready!')
        
        print('Generating features...')
        # Generate all features of length k and store in features
        alphabet = 'abcdefghijklmnopqrstuvwxyz '
        tempFeatures = it.product(alphabet,repeat = k) # results in ('a','a') etc

        # Need to concatinate to 'aa' etc
        features = []
        for index, feature in tqdm(enumerate(tempFeatures)):
            currentFeature = ''
            for w in feature:
                currentFeature += w
            features.append(currentFeature)
        print('Done')
        
        print('Counting feature occurance in all documents...')
        # Some place to store number of occurances and finaly the most frequent features
        scores = np.zeros(len(alphabet)**k)

        # Calculate occurance of each feature in dataset
        for document in tqdm(dataset,desc = 'Document'):    
            for index, feature in tqdm(enumerate(features)):
                scores[index] += document.count(feature)
        print('Done')
        
        print('Findning top features...')
        # Find the most occuring features and return these in order
        topFeatures = []
        topFeatureScores =  []
        for i in tqdm(range(numbTop)):
            maxIndex = np.argmax(scores) #finds most frequent feature
            topFeatures.append(features[maxIndex]) 
            topFeatureScores.append(max(scores)) #score of that feature
            scores[maxIndex] = -1 # makes sure same feature does not come up again
        print('Done')
        
        print(topFeatures)
        print(topFeatureScores)
        
        
    if prints == False:
        
        # Generate all features of length k and store in features
        alphabet = 'abcdefghijklmnopqrstuvwxyz '
        tempFeatures = it.product(alphabet,repeat = k) # results in ('a','a') etc

        # Need to concatinate to 'aa' etc
        features = []
        for index, feature in enumerate(tempFeatures):
            currentFeature = ''
            for w in feature:
                currentFeature += w
            features.append(currentFeature)

        # Some place to store number of occurances and finaly the most frequent features
        scores = np.zeros(len(alphabet)**k)

        # Calculate occurance of each feature in dataset
        for document in dataset:    
            for index, feature in enumerate(features):
                scores[index] += document.count(feature)

        # Find the most occuring features and return these in order
        topFeatures = []
        topFeatureScores =  []
        for i in range(numbTop):
            maxIndex = np.argmax(scores)
            topFeatures.append(features[maxIndex]) #finds most frequent feature
            topFeatureScores.append(max(scores)) #score of that feature
            scores[maxIndex] = -1 # makes sure same feature does not come up again

    
    return topFeatures, topFeatureScores

