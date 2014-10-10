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
	print "splitting files"
	for line in open(feature_matrix_file):
		record = eval(line)
		docs[record['id']] = record['feature_vector']
	#i++
	total =len(docs)
	global train
	global test
	#print total
	train_length = floor(total*.8)
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
	with open('./pre_processing.csv', 'rB') as f:
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
	print "Training the data now"
	train_time = datetime.now()
	with open('./pre_processing.csv', 'rB') as f:
		
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
	#get all topics
	global docs_topics
	topicsfp ={}
	topicsfn ={}
	topicstp ={}
	topicstn ={}
	print len(docs_topics)
	for key in docs_topics:
		t=docs_topics[key]
		#print t
		if t != '':
			t = t.split(' ')
			for val in t:
				topicsfp[val]=0
				topicsfn[val]=0
				topicstp[val]=0
				topicstn[val]=0


	print "Testing the data now"
	test_time = datetime.now()
	success = float(0)
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
	total = float(0)
	for key in test:
		#try:
			#print key
			#print test.get(key)
		topics = docs_topics.get(key)
		if topics != '':
			total=total+1
			topics = topics.split(' ')
			A = np.array(map(int,list(test.get(key))))	
			test_topic = clf.predict(A)
			test_topic =  ''.join(test_topic)
			#print test_topic
				#no result
			for x in topics:
				
				#y_pred.append(test_topic)
				#y_true.append(x)
				if x == test_topic and x != '':
				#	print "match"
				#	print x
					topicstp[x]=topicstp[x]+1
					success+=1
					
				else:
					#falsenegative
					topicsfn[x]=topicsfn[x]+1
					##falsepositive
					topicsfp[test_topic]=topicsfp[test_topic]+1
		
		#except Exception,e:
			#print e
	
		i = i+1

	print "offline cost"
	print str(datetime.now()-test_time)
	print "test docs"
	print total
	print "total predicted correct"
	print success
	print "accuracy is"
	print float((success/total)*100)
	#print topicstp
	#print topicsfn
	#print topicsfp
	avg = float(0)
	precision = float(0)
	i=float(0)
	for x in topicstp:
		#print x
		try:
			#print topicstp[x]
			#print topicsfp[x]
			#print topicsfn[x]
			precision = topicstp[x]/(topicstp[x]+topicsfp[x])
			i = float(i+1)
		except:
			pass
		avg+=precision
		#print precision
	#print avg
	#print i
	print "precision"
	print float((avg/i)*100)


load_docs()        
split()
train_data()
test_docs()

