import csv,re, operator
from nltk import PorterStemmer
#from stemming.porter2 import stem

file_name = 'out_file.csv'
words = 'words_out.csv'

word_out = open(words, 'w')

count = 0
total  = 0

articles = {} 
i = 0
for line in open(file_name):
	i = i +1
	record = eval(line)
	#print record
	body = re.sub('[^A-Za-z]+', ' ', record['body']).split()
	title = re.sub('[^A-Za-z]+', ' ', record['title']).split()
	body  = body + title
	#current = {}
	for x in body:
		#body.remove(x)
		x = PorterStemmer().stem_word(x)
		
		if x not in articles.keys():
			#print x
			articles[x]=1
			count = count + 1
			total=total + 1
		else:
			#print x
			total=total + 1
			articles[x]= articles[x] +1
	#current.clear()
	print i
	print "unique words"
	print count
	print "total words"
	print total
	#if i > 2:
		#break
	#	break
sorted_x = sorted(articles.iteritems(), key=operator.itemgetter(1), reverse=True)
for x in sorted_x:
	print x

#articles =sorted(articles.values(),reverse=True)

for x in sorted_x:
	print >>word_out, x


	
