from __future__ import division
import numpy as np
import time, csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab as pl
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.datasets.samples_generator import make_blobs
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import math


filename = 'graph_coord.pytext'
X=[]
labels={}
docs_labels={}
print "loading docs"
i = 0
with open('foo.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if i%100 == 0:
			print i
        X.append(list(row))
        i = i+1
       	if i>120:
       		break

'''

for line in open(filename):
		record = eval(line)
		temp =[]
		temp.append(record['x'])
		temp.append(record['y'])
		X.append(temp)
'''	
filename = 'label_id.pytext'
i=0
for line in open(filename):
		record = eval(line)
		docs_labels[record['id']] = record['lab_id']
		if labels.get(record['lab_id']) != None:
			labels[record['lab_id']] = labels.get(record['lab_id']) +1
		else:
			labels[record['lab_id']] = 1
		#if i > 1461:
		#	break
		i =i+1

filename = 'label_id.pytext'
i=0
for line in open(filename):
		record = eval(line)
		docs_labels[record['id']] = (record['lab_id']) 
		if i > 1461:
			break
		i =i+1

X = np.array(X,dtype=float)
print X

print "docs loaded building cluster"
#labels_true = np.array(labels)
#print labels_true
#print labels_true.shape

#DBScan
batch_size = 45
#k = 10

#centers = [[50, 100], [100, 200], [50, 50],[150, 150]]
#centers=np.random.randint(size=(k,2),low=20,high=200)

#n_clusters = len(centers)

t0 = time.time()

#db = DBSCAN(eps=5, min_samples=5, metric='manhattan').fit(X)
X_scaled = StandardScaler().fit_transform(X)

db = DBSCAN(eps=5, min_samples=2, metric='euclidean', algorithm='auto', leaf_size=30).fit(X_scaled)
#k_means = KMeans(init='k-means++', n_clusters=n_clusters,verbose=True)

#k_means.fit(X)
t_batch = time.time() - t0
#k_means_labels = k_means.labels_
db_labels = db.labels_
#copying example:
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels_db = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels_db)) - (1 if -1 in labels_db else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print('Labels: ')
print labels_db
##############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels_db)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k in (unique_labels):
	col = cm.spectral(float(k) / n_clusters_, 1)
	if k == -1:
		col = 'k'
		# Black used for noise.
		
	class_member_mask = (labels_db == k)
	xy = X[class_member_mask & core_samples_mask]
	plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
	xy = X[class_member_mask & ~core_samples_mask]
	plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()

##Shashank's Entropy code:
#entropy

#n_clusters
#labels
#docs_labels

ent = {}
size_cl={}
for k in range(n_clusters_):
	temp_cl = {}
	len_c = 0
	i = 0
	for x in labels_db:
		#cluster
		if x == k:
			l = docs_labels.get(i)
			if temp_cl.get(l) != None:
				temp_cl[l] = temp_cl.get(l) + 1
			else:
				temp_cl[l] = 1
			len_c =len_c  +1
		i = i+1
	#finding cluster entropy
	e = 0
	print "cluster number "
	print k
	size_cl[k]=len_c
	total = len_c
	print "total docs in cluster"
	print total
	for key, value in temp_cl.iteritems():
		val = value/total
		#print "Total"
		#print total
		#print "count of label"
		#print value
		
		#print value/total
		log_val= math.log(val,2)
		#print log_val
		#print val*log_val
		#print '\n'
		e = e + (val*log_val)
	e = e * -1
	print "entropy for cluster"
	print k
	print e
	ent[k]=e



total = len(X)
print '\n'
print "total"
print total
fin_e=0

tot = 0
for keys in ent:
	print keys
	tot = tot + size_cl.get(keys)
	print size_cl.get(keys)
	fin_e = fin_e + (size_cl.get(keys)/total)*(ent.get(keys))
	
print "total"
print total
print "valid points"
print tot
print "fin_e"
print fin_e

#k_means_cluster_centers = k_means.cluster_centers_
#k_means_labels_unique = np.unique(k_means_labels)


#mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, batch_size=batch_size,verbose=True)
#t0 = time.time()
#mbk.fit(X)
#t_mini_batch = time.time() - t0
#mbk_means_labels = mbk.labels_
#mbk_means_cluster_centers = mbk.cluster_centers_
#mbk _means_labels_unique = np.unique(mbk_means_labels)
"""
# Plot result

fig = pl.figure()
colors = ['#4EACC5', '#FF9C34', '#4E9A06']
....
# We want to have the same colors for the same cluster from the
# MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
# closest one.

distance = euclidean_distances(k_means_cluster_centers,
                               mbk_means_cluster_centers,
                               squared=True)
order = distance.argmin(axis=1)

# KMeans
ax = fig.add_subplot(1, 3, 1)
for k in range(n_clusters):
	col = cm.spectral(float(k) / n_clusters, 1)
	my_members = k_means_labels == k
	cluster_center = k_means_cluster_centers[k]
	ax.plot(X[my_members, 0], X[my_members, 1], 'w',markerfacecolor=col, marker='.')
	ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=6)
ax.set_title('KMeans')
pl.text(-3.5, 2.7,  'train time: %.2fs' % t_batch)

# MiniBatchKMeans
ax = fig.add_subplot(1, 3, 2)
for k in range(n_clusters):
	col = cm.spectral(float(k) / n_clusters, 1)
	my_members = mbk_means_labels == order[k]
	cluster_center = mbk_means_cluster_centers[order[k]]
	ax.plot(X[my_members, 0], X[my_members, 1], 'w',markerfacecolor=col, marker='.')
	ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=6)
ax.set_title('MiniBatchKMeans')
pl.text(-3.5, 2.7,  'train time: %.2fs' % t_mini_batch)

# Initialise the different array to all False
different = (mbk_means_labels == 4)
ax = fig.add_subplot(1, 3, 3)

for l in range(n_clusters):
    different += ((k_means_labels == k) != (mbk_means_labels == order[k]))

identic = np.logical_not(different)
ax.plot(X[identic, 0], X[identic, 1], 'w',
        markerfacecolor='#bbbbbb', marker='.')
ax.plot(X[different, 0], X[different, 1], 'w',
        markerfacecolor='m', marker='.')
ax.set_title('Difference')

pl.show()



plt.xlabel('n_init')
plt.ylabel('inertia')
n_runs = 5
#plt.legend(plots, legends)
plt.title("Mean inertia for various k-means init across %d runs" % n_runs)
fig = plt.figure()
for k in range(n_clusters):
	my_members = k_means.labels_ == k
	color = cm.spectral(float(k) / n_clusters, 1)
	plt.plot(X[my_members, 0], X[my_members, 1], 'o', marker='.', c=color)
	cluster_center = k_means.cluster_centers_[k]
	plt.plot(cluster_center[0], cluster_center[1], 'o',markerfacecolor=color, markeredgecolor='k', markersize=6)
	plt.title("Example cluster allocation with a single random init\n" "with MiniBatchKMeans")
plt.show()


print k_means.labels_

print k_means.labels_.shape


print np.amax(k_means.labels_)
#entropy

#n_clusters
#labels
#docs_labels
i = 0
ent = {}
size_cl={}
for k in range(n_clusters):
	temp_cl = {}
	len_c = 0
	for x in k_means.labels_:
		#cluster
		if x == k:
			l = docs_labels.get(i)
			if temp_cl.get(l) != None:
				temp_cl[l] = temp_cl.get(l) + 1
			else:
				temp_cl[l] = 1
			len_c =len_c  +1
		i = i+1
	#finding cluster entropy
	e = 0
	print "cluster number "
	print k
	size_cl[k]=len_c
	total = len_c
	print "total docs in cluster"
	print total
	for key, value in temp_cl.iteritems():
		val = value/total
		#print "Total"
		#print total
		#print "count of label"
		#print value
		
		#print value/total
		log_val= math.log(val,2)
		#print log_val
		#print val*log_val
		#print '\n'
		e = e + (val*log_val)
	e = e * -1
	print "entropy for cluster"
	print k
	print e
	ent[k]=e



total = len(X)
print '\n'
print "total"
print total
fin_e=0

for keys in ent:
	print keys
	print size_cl.get(keys)
	fin_e = fin_e + (size_cl.get(keys)/total)*(ent.get(keys))
	
print "fin_e"
print fin_e


		

#hashtable labels has all labels and count of docs in it
#for each cluster find 

#find total labels and docs in each label
#find label distribution in each cluster
#find entropy

"""



