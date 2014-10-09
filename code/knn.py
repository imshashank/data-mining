#creating the feature vector

import operator
from nltk import PorterStemmer
from sklearn.naive_bayes import GaussianNB

import numpy as np
#import numpy as np

feature_matrix_file = 'feature_matrix.pytext'

docs= {}
temp={}
i=0

for line in open(feature_matrix_file):
	record = eval(line)
	temp ={}
	temp['id']=record['id']
	#print record['id']
	temp['feature_vector'] =record['feature_vector']
	#print record['id']
	docs[i] = temp
	i= i+1


X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])

Y = np.array([1, 1, 1, 2, 2, 2])

clf = GaussianNB()
clf.fit(X, Y)
GaussianNB()
print(clf.predict([[2.8, 1]]))


print i
a =i
#15839

#compare each doc with each other
for x in range (15839,a-1):
	top_k = {}
	try:
		for y in range(0,15838):
			print docs[x]['id']
			print docs[y]['id']
			#print x_val
			count = 0
			for i in range (0,len(docs[x]['feature_vector'])):
					if docs[x]['feature_vector'][i] == docs[y]['feature_vector'][i] and docs[x]['feature_vector'][i] == '1':
						count = count + 1
			print "count "
			top_k[docs[y]['id']] = count
			print count
		sorted_topk = sorted(top_k.iteritems(), key=operator.itemgetter(1), reverse=True)
		file_name = 'topk/%s.pytext'% docs[x]['id']
		print file_name
		top_k_file = open(file_name,'w')

		for x in sorted_topk[0:200]:
			print x
			temp['id']=x[0]
			temp['score']=x[1]
			print >> top_k_file, x
	except Exception,e:
		print e

#	break
		
	#break

			#print x_val & y_val
