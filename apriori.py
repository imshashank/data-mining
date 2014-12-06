from __future__ import division
from collections import defaultdict
import sys

def compare_list(list1, list2):
    sub = list1[-1] - list2[-1]
    #Note. We want items with higher confidence/support to come first
    # i.e. decending order
    if (sub < 0):
        return 1
    elif (sub > 0):
        return -1
    #print "confidence is same. Comparing support"
    sub = list1[-2] - list2[-2]
    if (sub < 0):
        return 1
    elif (sub > 0):
        return -1
    else:
        return 0

rules = []
def createRuleList(rule_file):
    rule_file
    with open(rule_file) as f:
    #with open('output_hello3') as f:
        for line in f:
            line = line.rstrip('\n')
            label = line.split('<-');
            label[1] = label[1].translate(None, ',()').split()
            confidence = float(label[1].pop(-1));
            support = float(label[1].pop(-1));
            label.append(support);
            label.append(confidence);
            rules.append(label);
    f.close()
    rules.sort(cmp=compare_list)
    #sorted(rules, cmp=compare_list)
    #for rule in rules:
     #   print rule



def check(rule_file,filename):
    createRuleList(rule_file)
    doc_file ={}

    i = 0

    same = 0

    docs = defaultdict(list)

    #docs={}
    total = 0
    lines = open(filename).read().splitlines()
    for l in lines:
        doc = l.strip().rsplit(' ', 1)[0]
       
        temp= l.split(" ")
        #print temp[-1]
        t =  docs[doc]
        if temp[-1].strip() not in t:
            docs[doc].append(temp[-1])
        total = total + 1
        #print "hash table value"
        #print docs[doc]

    right =0
    for key in docs:
        print key
        true_val = docs[key]
        print "true labels"
        print true_val
        size = len(docs[key])
        print "labels to find"
        print size
        labels = []

        temp = {}
        for x in key.split(" "):
            temp[x] = True

        for rule in rules:
            if rule[0].strip() not in labels:
                flag = True
                test_rule = rule[1]
              #  print "testing rule"
               # print test_rule

                for t in test_rule:
                    if t in temp:
                        pass
                    else:
                        flag = False
                        break

                if flag == True:
                    print "rule applied"
                    print rule
                    labels.append(rule[0].strip())
                    size = size -1

                if size == 0:
                    print "all rule found"
                    print key
                    print "labels found"
                    print labels
                    print set(labels) & set(true_val)
                    t =  set(labels) & set(true_val)
                    print "right"
                    print len(t)
                    right = right + len(t)          
                    print "\n"
                    break
            else:
                pass
        if size >0:
            print "some rules found"
            print key
            print "some labels found"
            print labels
            print set(labels) & set(true_val)
            t =  set(labels) & set(true_val)
            print "right"
            print len(t)
            right = right + len(t)          
            print "\n"


    print "total docs"
    print total
    print "Total Correct"
    print right
    print "correct percentage"
    print (right/total)*100


rule_file = sys.argv[1]
docs_file = sys.argv[2]

#output_hello3
#check("inputFile.txt")

check(rule_file,docs_file)
'''
            print rule
            print l[-1]
            print rule[0]

            if l[-1].strip() == rule[0].strip():
                print l[-1]
                correct = correct +1
                print "correct prediction"
            else:
                print "wrong"
                wrong = wrong + 1
            break
    prev = l.rsplit(' ', 1)[0]
'''
'''
lines = open(filename).read().splitlines()
for l in lines:

    same = False
    print l
    
    l = l.strip().split(" ")
    if l = prev:
        same = same +1
    temp = {}
    for x in l:
        temp[x] = True

    for rule in rules:
        flag = True
        test_rule = rule[1]
      #  print "testing rule"
       # print test_rule

        for t in test_rule:
            if t in temp:
                pass
            else:
                flag = False
                break
        if flag == True:
            print "rule found"
            print l
            print rule
            print l[-1]
            print rule[0]
            if l[-1].strip() == rule[0].strip():
                print l[-1]
                correct = correct +1
                print "correct prediction"
            else:
                print "wrong"
                wrong = wrong + 1
            break
    prev = l.rsplit(' ', 1)[0]

        
print "Total Correct"
print correct
print "Totoal wrong"
print wrong
print correct + wrong
'''

