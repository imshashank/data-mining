import re, os, glob, math,csv
from xml.dom.minidom import parse, parseString
#from nltk.stem.wordnet import WordNetLemmatizer
#from stemming.porter2 import stem
from sklearn.neighbors import NearestNeighbors# KNeighborsClassifier
import numpy as np
from collections import Counter
from datetime import datetime

#global variables
train_time = datetime.now()
topicDict = {}
topicsData = []
newTopics = []
reuterTopics = []
reuterTitle = []
titleDict = {}
newBody_dict = {}
newBodyData = []
docId = []
bodySetWithTopics=[]
totalTopics=[]
trainingBodySet=[]
testingBodySet=[]
trainingTopicSet=[]
testingTopicSet=[]
testBody_dict = {}
totalDocuments = 0
reuterBodySet = []
reuterPlaces = []
placeDict = {}
predictedDistance=[]
predictedTopics=[]
predictedClasses=[]
predictedClassesActual=[]

def findUnique(seq):
    set = {}
    map(set.__setitem__, seq, [])
    return set.keys()

def findUniqueAfterStemming(bodyTokenize):
    tempSet = []
    for word in bodyTokenize:
        tempSet.append(PorterStemmer().stem_word(word))
        set = {}
    map(set.__setitem__, tempSet, [])
    return set.keys()
        
    
def trimSet(wordDict, lVal, rVal, numDocs):
    finalSet = []
    effCount = 0
    tempValue = wordDict['reuter']
    print (wordDict['reuter'])
    lowerThreshold = int(tempValue * lVal / 100)
    upperThreshold = int(tempValue * rVal / 100)
    for key, value in wordDict.items():
        #fVal = (totalDocuments*1.0)/value
    #effVal = value * 100.0 / numDocs
        #print key + " "+ str(value) +" " +str(fVal)
        #if effVal > 1 and effVal < 90:
        if value >= lowerThreshold and value <= upperThreshold:
            finalSet.append(key)
    stop_words= {}

    with open('stop_words.csv', 'rB') as f_stop:
        reader = csv.reader(f_stop)
        for row in reader:
            #stopwords = row['0'].strip() 
            stop_words[row[0]] = True
            #print row[0]
    stopwords = [word.strip() for word in stop_words]
    return set(finalSet).difference(set(stopwords))
'''
    f = open('stopWord', 'r')
    data = f.readlines()
    #for word in data:
    #stop
    stopwords = [word.strip() for word in data]
''' 
    #print stopwords
    
    

def printMatrix(trimWord):
    bodySet = reuterBodySet
    f = open('termVector', 'w')
    countDoc = 0

    while countDoc != len(docId):
        document = []
        document.append(docId[countDoc])
    
        body = reuterBodySet[countDoc]
        tempDocument = []
        for word in trimWord:
            if word in body:
                tempDocument.append(1)
            else:
                tempDocument.append(0)

        title = reuterTitle[countDoc]
    
        for word in trimWord:
            if word in title:
                tempDocument.append(1)
            else:
                tempDocument.append(0)

        document.append(','.join(str(n) for n in tempDocument))

        tempDocument = []
        for key in reuterTopics[countDoc]:

            if key in topicDict:

                tempDocument.append(key)
        #tempDocument += ","
    
        document.append(','.join(str(n) for n in tempDocument))

        tempDocument = []
        for key in reuterPlaces[countDoc]:
            if key in placeDict:
                tempDocument.append(key)

        document.append(','.join(str(n) for n in tempDocument))
        countDoc += 1
        f.write(str(document))
        f.write("\n")

    f.close()

def trimSpace(newList):
    tempList = []
    counter = 0
    for word in newList:
        counter += 1
        if counter != 1 and word != '':
            tempList.append(word.strip(' \t\n\r'))
        elif counter == 1:
            tempList.append(word.strip(' \t\n\r'))
    return tempList


def printBagOfWords(trimWord):
    f = open('transactionalVector', 'w')
    bodySet = reuterBodySet


    countDoc = 0
    while countDoc != len(docId):
        document = []
        document.append(docId[countDoc])
    
        body = reuterBodySet[countDoc]
        tempDocument = []
        for word in body:
            if word in trimWord:
                tempDocument.append(word)

        title = reuterTitle[countDoc]
    
        for word in title:
            if word in trimWord:
                tempDocument.append(word)

        document.append(','.join(str(n) for n in tempDocument))

        tempDocument = []
        for key in reuterTopics[countDoc]:

            if key in topicDict:

                tempDocument.append(key)
        #tempDocument += ","
    
        document.append(','.join(str(n) for n in tempDocument))

        tempDocument = []
        for key in reuterPlaces[countDoc]:
            if key in placeDict:
                tempDocument.append(key)

        document.append(','.join(str(n) for n in tempDocument))

        countDoc += 1

    
        f.write(str(document))
        f.write("\n")
    #print document
    f.close()


start_time=datetime.now()
#lmtzr = WordNetLemmatizer()
path = ''

#topicsData and newTopics both contains the same information: remove one of them 
#new_dict contains the indexing of unique topics
#######global topic set###########




counter = 0
tempdocData = ""
for infile in glob.glob(os.path.join(path,'*.sgm')):
    textfile = open(infile, 'r')
    udata = ""
    with open (infile, "r") as myfile:
        udata = ' '.join([line.replace('\n', '') for line in myfile.readlines()])
    #data = textfile.read()
    udata = re.sub(r'&#','' ,udata)
    data = re.sub(r'[^\x00-\x7F]', '', udata)
    #data = udata.decode('latin-1')
    data = data.lower()
    splitData = re.findall('<reuters.*?</reuters>', data)
    print (str(len(splitData)) + " reuters in " + infile)
    totalDocuments += len(splitData)
    #print(str(splitData))#ravi
    for info in splitData:
        dom2 = parseString(info)


    
    ############doc id parser  NEWID="1"###########################
        tempDocData = info.replace("\n","")
        #print (tempDocData)
        tempDoc = re.findall('newid="(.*?)">',tempDocData)
        #print (tempDoc)
        docId.append(tempDoc[0])

    ###########topic data parser#############################
        topicTemp = ''
        for node in dom2.getElementsByTagName('topics'):
            topicTemp = ''.join(node.toxml())
        #cTest = ''.join(topicTemp)
        #topicsData.append(topicTemp)
    
    #remove tags
        #tempTopics = re.sub(r'<.*?>',' ',cTest)
        #tempTopics = tempTopics.strip(' \t\n\r')

        topicTemp = re.sub(r'<.?topics>',' ',topicTemp)        
        topicTemp = re.sub(r'<topics/>',' ',topicTemp)
        topicTemp = re.sub(r'<d>','',topicTemp)
        topicTemp = topicTemp.strip(' \t\n\r')
        topicTempList = topicTemp.split('</d>')
        #print(topicTempList)
        topicTempList = trimSpace(topicTempList)
        topicTempList = findUnique(topicTempList)
        #print(len(topicTempList))#ravi

        for topicWord in topicTempList:
            if topicWord not in topicDict:
                topicDict[topicWord] = 1
    
        reuterTopics.append(topicTempList)
    
        
    ##############title data parser########################
        titleTemp = ''
        for node in dom2.getElementsByTagName('title'):
            titleTemp = node.toxml()

    #removing tags
        titleTemp = re.sub(r'<.*?>',' ',titleTemp)
        titleTemp = titleTemp.strip(' \t\n\r')
    
        titleTempList = titleTemp.split(' ')
    
        titleTempList = findUnique(titleTempList)
        for word in titleTempList:
            if word not in newBody_dict:
                newBody_dict[word] = 1
            else:
                newBody_dict[word] += 1

        reuterTitle.append(titleTempList)
    
    ############places data parser#####################
        placeTemp = ''
        for node in dom2.getElementsByTagName('places'):
            placeTemp = node.toxml()

    #removing tags
        placeTemp = re.sub(r'<.?places>',' ',placeTemp)
        placeTemp = re.sub(r'<places/>',' ',placeTemp)
        placeTemp = re.sub(r'<d>','',placeTemp)
        placeTemp = placeTemp.strip(' \t\n\r')
        placesTempList = placeTemp.split('</d>')
    
        placesTempList = trimSpace(placesTempList)
        placesTempList = findUnique(placesTempList)
        for placesWord in placesTempList:
            if placesWord not in placeDict:
                placeDict[placesWord] = 1
        
        reuterPlaces.append(placesTempList)


    ###########body data parsing#############
        bodyTemp = ''
        for node in dom2.getElementsByTagName('body'):
            bodyTemp = node.toxml()

    #deleting unwanted information
        bodyTemp = re.sub(r'([0-9]),([0-9])','\1\2', bodyTemp)
        bodyTemp = re.sub(r'<.?body>','',bodyTemp)

        cTest = ''.join(bodyTemp)
        cTest = cTest.strip(' \t\n\r')

    
        bodyTokenize = re.findall(r'[a-z]+', cTest)

    
        bodyTokenize = findUnique(bodyTokenize)
    

    #find document frequency
        bodySet = []
        for word in bodyTokenize:
            if word not in newBody_dict:
                newBody_dict[word] = 1
        
            else:
                newBody_dict[word] += 1 
    
        reuterBodySet.append(bodyTokenize)




totalCount = 0

effCount = trimSet(newBody_dict, 1, 80, totalDocuments)

# Method to break the data into training and testing data in the
# ratio of 80:20
#
#return type: null
def splitDocs():
    noOfTopics=len(totalTopics)
    temp=int(math.floor((60*noOfTopics)/100))
    counter=0
    while counter != noOfTopics:
        if counter<temp:
            trainingBodySet.append(bodySetWithTopics[counter])
            trainingTopicSet.append(totalTopics[counter])
        else:
            testingBodySet.append(bodySetWithTopics[counter])
            testingTopicSet.append(totalTopics[counter])
        counter += 1

# Method to create the frequency Vector from the effective word set
# for each document.
#
# return type: null
def getTermVector(trimWord):
    bodySet=reuterBodySet
    counter=0
    while counter != len(docId):
        if reuterTopics[counter][0]!='':    
            tempBody=[]
            body=bodySet[counter]
            for word in trimWord:
                if word in body:
                    tempBody.append(1)
                else:
                    tempBody.append(0)
            title=reuterTitle[counter]
            for word in trimWord:
                if word in title:
                    tempBody.append(1)
                else:
                    tempBody.append(0)
            bodySetWithTopics.append(tempBody)
            totalTopics.append(reuterTopics[counter])   
        counter += 1



# Method to create the KNN classifier and train the classifier using
# training data set
#
# return type: null
def predictDocs():
    X=np.array(trainingBodySet)
    Y=trainingTopicSet
    train_time = datetime.now()
    nbrs=NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X)
    
    
    for vector in testingBodySet:
        distance, indices = nbrs.kneighbors(vector)
        predictedDistance.append(distance)
        predictedTopics.append(getTopicsFromIndices(indices))
    train_time = datetime.now()-start_time
    print("The total time of the training  is " +str(train_time), "seconds")
    #print("The total time of the testing  is " +str(datetime.now()-train_time), "seconds")
     
    

# Method to fetch topics from the training topic set of the K nearest 
# neighbors.
#
# return type: List of list of topics
def getTopicsFromIndices(indexList):
    topicList=[]
    for indexes in indexList:
        for index in indexes:
            topicList.append(trainingTopicSet[index])
    return topicList

# Method to predict the classes from the classes of the predicted neighbors.
# Topics are predicted according to the distance and repetetions.
#
# return type: null
def getPredictedClasses():
    for classes1, classes2 in zip(predictedTopics, testingTopicSet):
    #actualLength
        classLabels=[]
        for class1, class2 in zip(classes1, classes2):
            for topic1, topic2 in zip(class1, class2):
                actualLength=(len(classes2))
                classLabels.append(topic1)   
            predictedClasses.append(((Counter(classLabels)).most_common(actualLength)))
        for topics in predictedClasses:
            topicWithoutFrequency=set()
        for topic in topics:
            for subtopic in topic:
                if isinstance(subtopic, int):
                    pass
                else:
                    topicWithoutFrequency.add((subtopic))
        predictedClassesActual.append(list(topicWithoutFrequency))

# Method to calculate accuracy of the model as the percentage of the 
# correctly predicted classes from the actual classes.
#
# return type: null
def getAccuracy():

    success=0
    test_time= datetime.now()
    for actualClass, predictedClass in zip(testingTopicSet, predictedClassesActual):
        if len(set(actualClass) & set(predictedClass))>0: 
            success += 1
    print "total test"
    print len(testingTopicSet)
    print "success"
    print success
    print("The accuracy of the system is %0.2f"%((success*100)/len(testingTopicSet)))
    print("The total time of the test  is " +str(datetime.now()-start_time), "seconds")

getTermVector(effCount)
splitDocs()
predictDocs()
getPredictedClasses()
getAccuracy()