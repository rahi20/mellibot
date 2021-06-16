import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import pandas as pd
import spacy
import random
from kerastuner.tuners import RandomSearch
import kerastuner as kt
import tensorflow as tf
from keras.utils import np_utils
import preprocess as pr
import seaborn as sns
import pickle
import os

def model_builder(hp):
  model = keras.Sequential()
  model.add(keras.layers.Flatten(input_shape=(X_train.shape[1],)))

  # Tune the number of units in the first Dense layer
  # Choose an optimal value between 32-512
  hp_units = hp.Int('units', min_value=300, max_value=1000, step=10)
  activ = hp.Choice('activation', values = ['relu', 'sigmoid', 'softmax', 'tanh'])
  model.add(Dense(units=hp_units, activation=activ))
  
  #2nd layer
  hp_units2 = hp.Int('units2', min_value=30, max_value = hp_units, step = 10)
  activ2 = hp.Choice('activation2', values = ['relu', 'sigmoid', 'softmax', 'tanh'])
  model.add(Dense(units=hp_units2, activation=activ2))
  #output layer 
  model.add(Dense(len(classes), activation='sigmoid'))

  # Tune the learning rate for the optimizer
  # Choose an optimal value from 0.01, 0.001, or 0.0001
  hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])

  model.compile(optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
                loss=keras.losses.CategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

  return model

dfc = pd.read_csv("data/intents.csv").sample(frac=1, random_state=42).reset_index(drop=True)
df2 = dfc[["text","intent"]]

df2 = df2.fillna("")

classes = dfc.intent.unique().tolist()
df2['intent'] = df2['intent'].apply(classes.index)

val_label_cor = pd.concat(
    {
        "intent_val" : df2['intent'],
        "intent_label" : dfc['intent']
    },
    axis = 1
)

val_label_cor = val_label_cor.drop_duplicates().reset_index(drop=True)

X = np.stack(df2["text"].apply(pr.wordvec).to_numpy(), axis=0)
y = df2.intent.to_numpy()

X_train = X[:int(0.7*X.shape[0])]
y_train = y[:int(0.7*y.shape[0])]
X_test = X[int(0.7*X.shape[0]):]
y_test = y[int(0.7*y.shape[0]):]

#preparer les labels
y_train = y_train.tolist()
y_test = y_test.tolist()

def to_vec(val):
    vec = [0] * len(classes)
    vec[val] = 1
    return vec

y_train = np.array(list(map(to_vec, y_train)))
y_test = np.array(list(map(to_vec, y_test)))


tuner = kt.Hyperband(model_builder,
                     objective='val_accuracy',
                     max_epochs=50,
                     factor=3,
                     directory='keras-model',
                     project_name='hyperpara_tuning')

stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

tuner.search(X_train, y_train, epochs=200, validation_split=0.2, callbacks=[stop_early])

# Get the optimal hyperparameters
best_hps=tuner.get_best_hyperparameters(num_trials=1)[0]

model = tuner.hypermodel.build(best_hps)
history = model.fit(X_train, y_train, epochs=200, validation_split=0.2)

val_acc_per_epoch = history.history['val_accuracy']
best_epoch = val_acc_per_epoch.index(max(val_acc_per_epoch)) + 1

hypermodel = tuner.hypermodel.build(best_hps)

# Retrain the model with the best epochs
hypermodel.fit(X_train, y_train, epochs=best_epoch, validation_split=0.2)

eval_result = hypermodel.evaluate(X_test, y_test)
print("[test loss, test accuracy]:", eval_result)

hypermodel.summary()

#save the model
hypermodel.save("saved_models_vars/bot_hypermodel.h5")

#save the classes
pickle.dump(val_label_cor, open(os.path.join('saved_models_vars','val_label_cor.pckl'), 'wb'))
