#calculating the td-idf for each word in the documents

import math, operator
from decimal import *

getcontext().prec = 6

total_words = 31545.00 
total_docs= 21578.00  

#this signifies how many documents have any given word.
unique_words = {}

for line in open('words_out_2.csv'):
	record = eval(line)
	unique_words[record[0]]=record[1]

#this signifies the total occurences of the word in all the documents.
word_freq = {}
for line in open('words_out.csv'):
	record = eval(line)
	word_freq[record[0]]=record[1]



tdidf={}

tdidf_out = open('tdidf.csv', 'w')
for word in unique_words.keys():
	#print word
	try:
		#print word_freq[word]

		#print unique_words[word]

		tdidf_value = (word_freq[word]/total_words) * math.log(total_docs/unique_words[word])
		tdidf[word] = tdidf_value
		print word
		
	except Exception,e:
		print e


sorted_x = sorted(tdidf.iteritems(), key=operator.itemgetter(1), reverse=True)

for x in sorted_x:
	print>> tdidf_out,x
for x in sorted_x[:20]:
	print x
