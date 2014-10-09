#creating the feature vector

import operator,csv
from datetime import datetime
from sklearn.metrics import precision_score


from nltk import PorterStemmer
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from math import floor

import numpy as np

#global
feature_matrix_file = 'feature_matrix.pytext'

docs_topics={}
docs= {}
train={}
test={}
X = []
Y= []
clf = GaussianNB()
#clf = BernoulliNB()
#clf = MultinomialNB()

#create topics file with IDs

	#print record['id']

	#split data


def split():		
	i=0
	for line in open(feature_matrix_file):
		record = eval(line)
		docs[record['id']] = record['feature_vector']
	#i++
	total =len(docs)
	global train
	global test
	#print total
	train_length = floor(total*.6)
	#print train_length
	i=0
	for x in docs:
		if 	i < train_length:
			train[x]=docs.get(x)
		else:
			test[x]=docs.get(x)
		
		i=i+1
	print "total docs"
	print total
	#print len(train)
	#print len(test)

	
	#train = dict(docs.items()[len(docs)/.8:])
	#print train
	#test = dict(docs.items()[:len(docs)/.2])

def load_docs():
	with open('./files/pre_processing.csv', 'rB') as f:
		#writer = csv.writer(open("out_file", 'w'))
		#features_file = open("feature_file.csv", 'w')
		#opic_file = open("topic_file.csv", 'w')

		global docs_topics
		reader = csv.reader(f)
		#docs_body = {}
		#i=0
		for row in reader:
			#print row
			#try:
			docs_topics[row[0]] = row[3].strip()
		#	print row[0]
		#	print row[3]
	#print len(docs_topics)


def train_data():
	train_time = datetime.now()
	with open('./files/pre_processing.csv', 'rB') as f:
		
		global X
		global Y
		global test
		global train
		global docs

		reader = csv.reader(f)
		article = {}
		i=0
		skips = 0
		notopic = 0
		for row in reader:
		#replace multiple spaces
		#['newId', ' TITLE', ' DATE', ' TOPICS', ' PLACES', ' BODY']
			
			#print row
			#try:
			article['id'] = row[0]
			article['title'] = row[1]
			article['date'] = row[2]
			article['topics'] = row[3]
			article['places'] = row[4]
			topics = []

			
			#find the feature_vector of id
			
			
			#write feature vector in features and topics in file topics
			if article['topics'].strip() != '':
				topics = article['topics'].strip().lower().split(' ')
			
				
			#	print "topics"
		#		print topics
				for n in topics :
					if n != '' :
						
						#print n
						#temp.append()
						#print list(docs[article['id']])
						#print docs.get(article['id'])
						try:
							X.append(list(train.get(article['id'])))
							temp = []

							temp.append(str(n))

							Y.append(str(n))
						
						except:
							#print "skip its test data"
							skips = skips + 1
					else:
						notopic = notopic+1

						
						#print list(docs.get(article['id']))
						
			else:
				#print "skipping no topics"
				notopic = notopic+1

				
				#i = i+1
				#if i >8 :
				#	break
			#except Exception, e:
				#print e
		#print X

		#print (x)
		X = np.array(X,dtype=int)
		#print X
		#print len(X)
		#print X.shape

		#print Y
		print "total trainset"
		print len(docs)-notopic-skips
		#print "total skips for test data"
		#print skips
		Y = np.array(Y,dtype=str)
		#print Y.shape
		global clf
		clf.fit(X, Y)
		#print "average precision"
		#print clf.score(X, Y, sample_weight=None)
		print "offline cost"
		print str(datetime.now()-train_time)
	


def test_docs():
	test_time = datetime.now()
	success = 0
	global clf
	global test
	global docs
	
	y_true= []
	y_pred = []
	true_positive = 0
	false_positive = 0
	false_negative = 0
	true_negative = 0
	#print temp
	#print(clf.predict(temp))
	i=0
	total = 0
	for key in test:
		try:
			#print key
			#print test.get(key)
			topics = docs_topics.get(key)
			if topics != '':
				total=total+1
				topics = topics.split(' ')
				A = np.array(map(int,list(test.get(key))))	
				test_topic = clf.predict(A)
				
					#no result
				for x in topics:
					if test_topic == '' and x!= '':
						false_negative+=1
					y_pred.append(test_topic)
					y_true.append(x)
					if x == test_topic and x != '':
					#	print "match"
					#	print x
						success+=1
						true_positive +=1
					else:
						true_negative +=1
		
		except Exception,e:
			print e
	
		i = i+1

	print "offline cost"
	print str(datetime.now()-test_time)
	print "test docs"
	print total
	print "total success"
	print success
	print "fn"
	print false_negative
	print "tp"
	print true_positive
	print "tn"
	print true_negative
	#print y_true
	#print y_pred
	print precision_score(y_true, y_pred, average='weighted')

'''
precision = tp+(tp+fp)
recall
false_negative : predict different class but there was class

coco
tn: predicted topic of a doc 

predicted actual
11 tp
00 tn
01 fn
10 fp

80 - 20
precision for gauss
0.467621540429

BernoulliNB
0.538304716295

multionomail
0.549270703289
'''



load_docs()        
split()
train_data()
test_docs()

