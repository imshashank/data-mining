Data Mining Project for CSE OSU CLass
===========
By
Shashank Agarwal (agarwal.202@osu.edu)
Anurag Kalra (kalra.25@osu.edu)

##Instructions

1) First we extracted all files from the sgm files and saved it in a csv called "data.csv"
input= .sgm files		file=cleanXML.jar	 	output=files/pre_processing.csv

2) We then used this to remove all the stop words and saved the file to "out_file.csv"
input=data.csv 		file = read.py 		output=out_file.csv

3) Now we do stemming and create two files 
	a) Frequency of each word across all documents : word_out_2.csv
	b) Number of documents where the word is present: word_out.csv
input=out_file.csv 		file=read_py.py 		output=word_out.csv & word_out_2.csv

4) We then calculated the tf-idf of each word and saved it to the file 'tdidf.csv'

input= word_out.csv & word_out_2.csv 		file=tdidf.py 		output = tdidf.csv

5) We use only the words with tf-idf of greate than 0.01, which results in 2823 words
input=tdidf.csv			file=feature.py			output=final_tdidf.csv

6) We then create the feature vector using the list of words as one axis and the document body as the other. Final results are stored in 'final_tdidf.csv'
input = final_tdidf.csv, data.csv		file=create_feature.py 		output=feature_matrix.pytext



Using the Make File:

To execute all steps just run "make All"

To execute a specific step from the above list follow these commands:

for step1 (create a csv file from sgm files)
make step1

for step2 (remove stop words)
make step2

for step3 (stemming and counting words)
make step3a
make step3b

for step4 (calculate tf-idf)
make step4

for step5 (get top keywords with tf-idf > 0.1)
make step5

for step6 (create feature vector)
make step6

to clean all csv files use (please use this with caution as data generation takes a lot of time)
make clean











