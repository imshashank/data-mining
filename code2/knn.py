import re, os, glob, math,csv
from xml.dom.minidom import parse, parseString
from sklearn.neighbors import NearestNeighbors
import numpy as np
from datetime import datetime
try:
    from collections import Counter
except ImportError:
    from wpull.backport.collections import Counter
  
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
         
def loadDocs(wordList, lVal, rVal, numDocs):
    
    finalSet = []
    effCount = 0
    tempValue = wordList['reuter']
    #print (wordList['reuter'])
    lowerThreshold = int(tempValue * lVal / 100)
    upperThreshold = int(tempValue * rVal / 100)
    for key, value in wordList.items():
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
    

def findUnique(body_Tokens):
    tempSet = []
    for word in body_Tokens:
        tempSet.append(PorterStemmer().stem_word(word))
        set = {}
    map(set.__setitem__, tempSet, [])
    return set.keys()

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

    
def findUnique(seq):
    set = {}
    map(set.__setitem__, seq, [])
    return set.keys()

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


def getBagOfWords(trimWord):
    print "Cleaning up the documents"
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

start_time=datetime.now()
path = ''
counter = 0
tempdocData = ""
print "Lets load documents all *.sgm files in current folder"
for infile in glob.glob(os.path.join(path,'*.sgm')):
    textfile = open(infile, 'r')
    udata = ""
    with open (infile, "r") as myfile:
        udata = ' '.join([line.replace('\n', '') for line in myfile.readlines()])
    udata = re.sub(r'&#','' ,udata)
    data = re.sub(r'[^\x00-\x7F]', '', udata)
    data = data.lower()
    splitData = re.findall('<reuters.*?</reuters>', data)

    print (str(len(splitData)) + " documents in file: " + infile)
    totalDocuments += len(splitData)
    #print(str(splitData))#ravi
    for info in splitData:
        dom2 = parseString(info)
        tempDocData = info.replace("\n","")
        tempDoc = re.findall('newid="(.*?)">',tempDocData)
        docId.append(tempDoc[0])
        topicTemp = ''
        for node in dom2.getElementsByTagName('topics'):
            topicTemp = ''.join(node.toxml())
        topicTemp = re.sub(r'<.?topics>',' ',topicTemp)        
        topicTemp = re.sub(r'<topics/>',' ',topicTemp)
        topicTemp = re.sub(r'<d>','',topicTemp)
        topicTemp = topicTemp.strip(' \t\n\r')
        topicTempList = topicTemp.split('</d>')
        topicTempList = trimSpace(topicTempList)
        topicTempList = findUnique(topicTempList)
        for topicWord in topicTempList:
            if topicWord not in topicDict:
                topicDict[topicWord] = 1
        reuterTopics.append(topicTempList)
    
        titleTemp = ''
        for node in dom2.getElementsByTagName('title'):
            titleTemp = node.toxml()
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
        placeTemp = ''
        for node in dom2.getElementsByTagName('places'):
            placeTemp = node.toxml()
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
        bodyTemp = ''
        for node in dom2.getElementsByTagName('body'):
            bodyTemp = node.toxml()
        bodyTemp = re.sub(r'([0-9]),([0-9])','\1\2', bodyTemp)
        bodyTemp = re.sub(r'<.?body>','',bodyTemp)

        cTest = ''.join(bodyTemp)
        cTest = cTest.strip(' \t\n\r')
        body_Tokens = re.findall(r'[a-z]+', cTest)
        body_Tokens = findUnique(body_Tokens)
        bodySet = []
        for word in body_Tokens:
            if word not in newBody_dict:
                newBody_dict[word] = 1
            else:
                newBody_dict[word] += 1 
        reuterBodySet.append(body_Tokens)


totalCount = 0
effCount = loadDocs(newBody_dict, 1, 80, totalDocuments)

def splitDocs():
    print "We split the files in 60 and 40 "
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

def getTopicsFromIndices(indexList):
    topicList=[]
    for indexes in indexList:
        for index in indexes:
            topicList.append(trainingTopicSet[index])
    return topicList

#the freq vector
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




# The KNN classifier
def predictDocs():
    print "Training the data"
    X=np.array(trainingBodySet)
    Y=trainingTopicSet
    train_time = datetime.now()
    nbrs=NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X)
    
    
    for vector in testingBodySet:
        distance, indices = nbrs.kneighbors(vector)
        predictedDistance.append(distance)
        predictedTopics.append(getTopicsFromIndices(indices))
    train_time = datetime.now()-start_time
   # print("The total time of the training  is " +str(train_time), "seconds")




def getPredictedClasses():
    print "Testing the data"
    for classes1, classes2 in zip(predictedTopics, testingTopicSet):
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


def findAccuracy():
    success=0
    test_time= datetime.now()
    for actualClass, predictedClass in zip(testingTopicSet, predictedClassesActual):
        if len(set(actualClass) & set(predictedClass))>0: 
            success += 1
    print "total test"
    print len(testingTopicSet)
    print "success"
    print success
    accuracy = float((success*100)/len(testingTopicSet))
    print("The accuracy is %0.2f"%(accuracy))
    print("The total running  is " +str(datetime.now()-start_time), "seconds")


#the main file
getTermVector(effCount)
splitDocs()
predictDocs()
getPredictedClasses()
findAccuracy()