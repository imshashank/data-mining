import threading
import time

#number of docs
#n = 11000
n = 11000
#length of feature vector
s_n = 2974

#value of k
k=10


time1 = time.time()
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



sigs = []
documents = []

for i in range(0, n):
  #temp =[]
  #for x in range (0,k):
  #  temp.append(minhash(x, i))
  
  #print "Signature of document", i+1, ":", temp
  #print "Signature of document", i+1, ":", minhash(0, i), minhash(1, i), minhash(2, i),minhash(3, i),minhash(4, i),minhash(5, i)
  #sigs.append([minhash(0, i), minhash(1, i), minhash(2, i),minhash(3, i),minhash(4, i),minhash(5, i)])
  #sigs.append(temp)

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



out = [[0 for x in range(n)] for x in range(n)] 

file_name = open('jaccard_dist.pytext', 'w')
for ii in range(0, n):
  print ii
  for jj in range(ii, n):
    if ii != jj:
      temp ={}
      temp['ii']=ii
      temp['jj']=jj
      temp['val']=jaccard(documents[ii], documents[jj])
      print>> file_name, temp
      out[ii][jj]=jaccard(documents[ii], documents[jj])
      
      #print "Doc", ii+1, "and doc", jj+1, "estimation", jaccard_estimate(sigs[ii], sigs[jj]), "actual", jaccard(documents[ii], documents[jj])
print "out"
print out

time2 = time.time()

print ' Program took %0.3f ms' % ((time2-time1)*1000.0)

'''
sum
200.461768888
SSE
0.932380320409
'''


