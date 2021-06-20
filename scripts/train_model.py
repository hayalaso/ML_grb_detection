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
min_val = tf.reduce_min(train_data)
max_val = tf.reduce_max(train_data)

train_data = (train_data - min_val)/(max_val - min_val)
test_data = (test_data - min_val) /(max_val - min_val)

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

plt.hist(train_loss[None,:], bins=50)
plt.xlabel("Train loss")
plt.ylabel("No of examples")


plt.show()
