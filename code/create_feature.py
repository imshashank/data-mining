#creating the feature vector

import operator
from nltk import PorterStemmer
#import numpy as np


final_tditf = 'final_tdidf.csv'
out_file = 'out_file.csv'
feature_matrix_file = open('feature_matrix.pytext','w')

keywords = {}
for line in open(final_tditf):
	record = eval(line)
	keywords[record[0]]= True
#a1 = np.array(keywords)

#sorted_keywords = sorted(keywords.iteritems(), key=operator.itemgetter(1), reverse=True)



#find words in article body
for line in open(out_file):
	try:
		record = eval(line)

		identifier = record['id']
		body = record['body'].lower().split()
		article_body = {}
		#the id of the record
		print identifier
		#stem all body words
		for y in body:
			y = PorterStemmer().stem_word(y)
			article_body[y] = True
		feature_matrix = {}
		feature_matrix[identifier] = ''
		
		for x in keywords:
			if x in article_body.keys():
				#print x
				feature_matrix[identifier] = str(feature_matrix[identifier]) +str(1)

				#if identifier in feature_matrix.keys():
			#		feature_matrix[identifier] = str(feature_matrix[identifier]) +str(1)
			#	else:
			#		feature_matrix[identifier] = 1
					
			else:
				feature_matrix[identifier] = str(feature_matrix[identifier]) +str(0)
				#print "nothing"
				#if identifier in feature_matrix.keys():
			#		feature_matrix[identifier] = str(feature_matrix[identifier]) +str(0)
			#	else:
			#		feature_matrix[identifier] = 0
		temp= {}
		temp['id']= identifier
		temp['feature_vector'] =feature_matrix[identifier]
		print >> feature_matrix_file,temp
		#feature_matrix.flush()

		#body = ' '.join(body)
		#print body
		#print identifier
		#print feature_matrix[identifier]
	except Exception as e:
		print e

#for x in feature_matrix:
#	print >> feature_matrix,x
	#print "\n"
	#print int(feature_matrix[identifier], 2)
	#break





