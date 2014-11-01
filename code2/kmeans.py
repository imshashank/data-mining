import numpy as np
import time, csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab as pl
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.datasets.samples_generator import make_blobs
from sklearn import metrics


filename = 'graph_coord.pytext'
X=[]
labels={}

print "loading docs"
i = 0
with open('foo.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print i
        X.append(list(row))
        i = i+1
        if i>1200:
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
		if labels.get(record['lab_id']) != '':
			labels(record['lab_id']) = labels.get(record['lab_id']) + 1
		else:
			labels(record['lab_id']) = 1
		if i > 1461:
			break
		i =i+1

X = np.array(X,dtype=float)
print X

print "docs loaded building cluster"
#labels_true = np.array(labels)
#print labels_true
#print labels_true.shape


batch_size = 45
centers = [[1, 1], [-1, -1], [1, -1],[0, 0],[0, 1]]
n_clusters = len(centers)


k_means = KMeans(init='k-means++', n_clusters=n_clusters,verbose=True)
t0 = time.time()
k_means.fit(X)
t_batch = time.time() - t0
k_means_labels = k_means.labels_
k_means_cluster_centers = k_means.cluster_centers_
k_means_labels_unique = np.unique(k_means_labels)

mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, batch_size=batch_size,verbose=True)
t0 = time.time()
mbk.fit(X)
t_mini_batch = time.time() - t0
mbk_means_labels = mbk.labels_
mbk_means_cluster_centers = mbk.cluster_centers_
mbk_means_labels_unique = np.unique(mbk_means_labels)


# Plot result

fig = pl.figure()
colors = ['#4EACC5', '#FF9C34', '#4E9A06']

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

print k_means.labels_

print k_means.labels_.shape


print np.amax(k_means.labels_)
#entropy

#find total labels and docs in each label
#find label distribution in each cluster
#find entropy






