from anomaly_det import AnomalyDetector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

df = pd.read_csv('../simulation/bkg.csv')

data = df.values

labels = np.ones(len(data))

train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2,random_state=21)

#Normalize data between [0,1]
max_val=np.amax(train_data,1)
train_data = train_data/max_val[:,None]
#min_val = tf.reduce_min(train_data)
#max_val = tf.reduce_max(train_data)

max_val=np.amax(test_data,1)
test_data = test_data/max_val[:,None]

train_data = tf.cast(train_data,tf.float32)
test_data = tf.cast(test_data,tf.float32)


autoencoder = AnomalyDetector()

autoencoder.compile(optimizer='adam', loss='mae')

history = autoencoder.fit(train_data,train_data,
            epochs = 20,
            batch_size=512,
            validation_data=(test_data,test_data),
            shuffle=True)

plt.figure()
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.legend()

plt.figure()
reconstructions = autoencoder.predict(train_data)
train_loss = tf.keras.losses.mae(reconstructions, train_data)
threshold = np.mean(train_loss) + np.std(train_loss)



n,b,p=plt.hist(train_loss[None,:], bins=50,label="train",range=(0,0.1),alpha=0.7)
plt.vlines(threshold,0,max(n),'red')
plt.xlabel("Loss")
plt.ylabel("No of examples")

df_grbs = pd.read_csv("../simulation/grbs.csv")
data_grbs = df_grbs.values[:,0:-1]
name_grbs = df_grbs.values[:,-1]
labels_grbs = np.zeros(len(data_grbs))

max_val=np.amax(data_grbs[:,80:],1)
data_grbs = data_grbs/max_val[:,None]
print(max_val)
print(data_grbs)
data_grbs = np.asarray(data_grbs).astype(np.float32)

reconstructions = autoencoder.predict(data_grbs)
grb_loss = tf.keras.losses.mae(reconstructions,data_grbs)
plt.hist(grb_loss[None,:], bins=50,label='real',range=(0,0.1),alpha=0.7)
plt.yscale('log')
plt.grid()
plt.show()
