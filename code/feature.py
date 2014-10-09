#filtering the td-idf word list

word_out = 'tdidf.csv'
#only using the words with td-idf > 0.01
final_tditf = open('final_tdidf.csv', 'w')

for line in open(word_out):
	record = eval(line)
	print record
	if record[1] >0.006:
		print>> final_tditf, record
