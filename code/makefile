All: step6

step1:
	java -jar cleanXML.jar FirstTry 

step2: step1
	python read.py
	
step3a: step2
	python read_py.py

step3b: step2
	python readb_py.py

step4: step3a step3b
	python tdidf.py

step5: step4
	python feature.py

step6: step5
	python create_feature.py

clean:
	rm -rf *.csv hello
