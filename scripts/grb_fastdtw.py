import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from scipy.spatial.distance import euclidean
from scipy.cluster.hierarchy import dendrogram
from fastdtw import fastdtw
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


grbs=pd.read_csv("../simulation/grbs.csv")


i=0
j=1

datgrb=grbs.values[:,0:-1]
labels = grbs.values[:,-1]


maxgrb=np.amax(datgrb,1)
datgrb/=maxgrb[:, None]


distance,path = fastdtw(datgrb[i],datgrb[j],dist=euclidean)

path=np.asarray(path)

fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2,gridspec_kw={'height_ratios': [2, 1], 'width_ratios':[1,2]})
ax1.plot(datgrb[i],np.arange(147),color='gray',linewidth=2)
ax1.set_ylim(0,146)
ax1.grid()
ax1.invert_xaxis()
ax4.plot(np.arange(147),datgrb[j],color='gray',linewidth=2)
ax4.set_xlim(0,146)
ax4.grid()
x=path[:,0]
y=path[:,1]
ax2.plot(x,y,'ro',ms=2)
ax2.set_ylim(0,146)
ax2.set_ylim(0,146)
ax2.grid()
ax3.set_visible(False)
plt.tight_layout()


N=len(datgrb)
dist_mat = np.zeros([N,N])
for i in range(N):
    n=i+1
    if n==N:
        break
    for j in range(n,N):
        dis,path = fastdtw(datgrb[i],datgrb[j])
        dist_mat[i,j]=dis
        dist_mat[j,i]=dis
        

print(dist_mat)
clustering = DBSCAN(eps=7, min_samples=5,metric='precomputed').fit(dist_mat)
print(clustering.labels_)


clustering = AgglomerativeClustering(linkage='complete',affinity='precomputed',compute_distances=True).fit(dist_mat)
print(clustering.labels_)

plt.figure()
plot_dendrogram(clustering, truncate_mode='level', p=3)
plt.show()
