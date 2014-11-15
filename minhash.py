
#number of docs
n = 21579

#length of feature vector
s_n = 2974

#value of k
k=32

#loading feature vector
s= []
filename = 'feature_matrix.pytext'

i=0
for line in open(filename):
    #print i
    record = eval(line)
    #if i%100 == 0:
    # print i

    temp = map(int, list(record['feature_vector']))
    s.append(temp)
    
    if i >= n-1:
      break
    i =i+1

#hashing function    
def h(x,i):
  return (i*x + i*2 ) % s_n



#creating permutations
permutations =[[]]*k

for x in range(0,k):
  temp =[]
  for i in range(0, s_n):
    temp.append(h(x,i))
  permutations[x]=temp

#finding minhash
def minhash (permutation, document):
  foundindex = 9999
  permutation = permutations[permutation]
  #print len(permutation)
  #print permutation[2973]
  for ii in range(0, s_n):
    if s[document][ii] == 1:
      if permutation[ii] < foundindex:
        foundindex = permutation[ii]
  return foundindex

sigs = []
documents = []

for i in range(0, n):
  temp =[]
  for x in range (0,k):
    temp.append(minhash(x, i))
  
  print "Signature of document", i+1, ":", temp
  #print "Signature of document", i+1, ":", minhash(0, i), minhash(1, i), minhash(2, i),minhash(3, i),minhash(4, i),minhash(5, i)
  #sigs.append([minhash(0, i), minhash(1, i), minhash(2, i),minhash(3, i),minhash(4, i),minhash(5, i)])
  sigs.append(temp)

  # also build s as sets
  documents.append(set())
  for jj in range(0, s_n -1):
    if s[i][jj] == 1:
      documents[i] |= set([jj])

def jaccard (a, b):
  try:
    return float(len(a & b)) / float(len(a | b))
  except:
    return 1.0

def jaccard_estimate (a, b):
  same = 0
  try:
    for i in range(0, k):
      if a[i] == b[i]: same += 1
    return float(same) / k
  except:
    return 1.0

print "signatures:", sigs
print "documents:", documents

for ii in range(0, n):
  for jj in range(ii, n):
    if ii != jj:  
      print "Doc", ii+1, "and doc", jj+1, "estimation", jaccard_estimate(sigs[ii], sigs[jj]), "actual", jaccard(documents[ii], documents[jj])

sum_val = 0
for ii in range(0, n):
  for jj in range(ii, n):
    if ii != jj:
      pred=jaccard_estimate(sigs[ii], sigs[jj])
      original=jaccard(documents[ii], documents[jj])
      err=  abs((original-pred)**(2))
      sum_val = sum_val + err
fin =sum_val/n
print "SSE"
print fin



