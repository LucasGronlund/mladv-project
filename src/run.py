import fetch_data as fd
import svm

categories = ['acq','earn','corn','crude']
numberOfTraining = [114,152,38,76]
numberOfTesting = [25,40,15,10]


#categories = ['earn','crude','acq']
#numberOfTraining = [10,10,30]
#numberOfTesting = [7,2,3]


trainData,trainLabels, testData,testLabel = fd.loadData(categories,numberOfTraining,numberOfTesting)

n = 4 # Length of subsequence
l = 0.5 # Lambda value

    #------------------------------------------------------#
    # Choose Kernel method for svm						   # 
    # Options:     										   #
    # r is recursive Kernel.                               #
    # a is approximative Kernel.                           #
    # wk is the word kernel                	               #           
    # ngk is the ngk Kernel				                   #
    #------------------------------------------------------#

kernel_method = 'ngk' 

print('\n Building Classifier')
 # Generate a classifier that we can use for prediction.
clf = svm.generateClassifier( trainData, trainLabels, n, l,categories,kernel_method)
print('\n Classifier built')


res = svm.predict(testData,trainData,clf,n,l,kernel_method)
print(res)
print('\n Prediction done \n\n Score Card:') 

svm.score(res,testLabel,categories)
