import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

bkg=pd.read_csv("../simulation/bkg.csv")
grbs=pd.read_csv("../simulation/grbs_dtw.csv")


n=9

datbkg=bkg.values
datgrb=grbs.values[:,0:-1]
labels = grbs.values[:,-1]

plt.figure()
#plt.plot(np.arange(147),datbkg[241])
#plt.plot(np.arange(147),datgrb[n],label=labels[n])
#plt.legend()

maxbkg=np.amax(datbkg,1)
datbkg/=maxbkg[:, None]

maxgrb=np.amax(datgrb[:,80:],1)
datgrb/=maxgrb[:, None]

plt.figure()
plt.plot(np.arange(147),datbkg[241],label='Bkg',color='gray')
plt.plot(np.arange(147),datgrb[n],label='GRB example',color='red')
plt.grid()
plt.legend()
plt.xlabel("Time Bin")

#min_val = tf.reduce_min(datbkg,keepdims=True)
#max_val = tf.reduce_max(datbkg,keepdims=True)

#datbkg = (datbkg-min_val)/(max_val-min_val)
#datgrb = (datgrb-min_val)/(max_val-min_val)

#plt.figure()
#plt.plot(np.arange(147),datbkg[541])
#plt.plot(np.arange(147),datgrb[27])


plt.show()
