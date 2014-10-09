import csv,re

stop_words= {}
with open('stop_words.csv', 'rB') as f_stop:
	reader = csv.reader(f_stop)
	for row in reader:
		stop_words[row[0]] = True
		print row[0]


def read():
	with open('./files/pre_processing.csv', 'rB') as f:
		#writer = csv.writer(open("out_file", 'w'))
		out_f = open("out_file.csv", 'w')
		reader = csv.reader(f)
		article = {}
		for row in reader:
		#replace multiple spaces
		#['newId', ' TITLE', ' DATE', ' TOPICS', ' PLACES', ' BODY']
			for x in row:
				x = re.sub(' +',' ',str(x))
			print row
			try:
				article['id'] = row[0]
				article['title'] = row[1]
				article['date'] = row[2]
				article['topics'] = row[3]
				article['places'] = row[4]

				title = row[1].lower().split()
				filtered = title[:]

				for x in title:
					if x in stop_words or len(x) < 3:
						try:
							#print "remove"
							#print x
							filtered.remove(x)
						except Exception,e:
							print e
				
				article['title'] = ' '.join(filtered)
				#print article['body']

				body = row[5].lower().split()
				filtered = body[:]

				for x in body:
					if x in stop_words or len(x) < 3:
						try:
							#print "remove"
							#print x
							filtered.remove(x)
						except Exception,e:
							print e
				
				article['body'] = ' '.join(filtered)
				print article['body']
				print >>out_f,  article
				
			except Exception, e:
				print e
	        #out_f.flush()
read()