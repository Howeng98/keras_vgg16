# -*- coding: utf-8 -*-
"""Cifar10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lZPGlN_fV894xGCJLQ-WlTSjvml3BVa4
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.client import device_lib
from tensorflow import keras
from keras.datasets import cifar10
from keras.utils import np_utils,plot_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split

tf.test.gpu_device_name()
device_lib.list_local_devices()

(x_train,y_train),(x_test,y_test) = cifar10.load_data()
x_train = x_train.astype('float32')/255.0
x_test = x_test.astype('float32')/255.0


y_train = np_utils.to_categorical(y_train,1000)
y_test = np_utils.to_categorical(y_test,1000)

# Variables
batch_size = 64
num_classes = 10
epochs = 10


# my model - VGG16
model = keras.Sequential()
# Block 1
model.add(keras.layers.Conv2D(64,  kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.Conv2D(64,  kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2),strides=(2,2)))
# Block 2
model.add(keras.layers.Conv2D(128, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.Conv2D(128, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2),strides=(2,2)))
# Block 3
model.add(keras.layers.Conv2D(256, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.Conv2D(256, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.Conv2D(256, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2),strides=(2,2)))
# Block 4
model.add(keras.layers.Conv2D(512, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.Conv2D(512, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.Conv2D(512, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2),strides=(2,2)))
# Block 5
model.add(keras.layers.Conv2D(512, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.Conv2D(512, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.Conv2D(512, kernel_size=(3,3),strides=(1,1), activation='relu',input_shape=(32,32,3),padding='same'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2),strides=(2,2)))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(4096, activation='relu'))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(4096, activation='relu'))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(1000, activation='softmax'))

model.summary()
plot_model(model, to_file='model.png')

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
history = model.fit(x_train,y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test,y_test))

# Saving the model
save_dir = 'drive/My Drive/Colab Notebooks'
model_name = 'cifar10.h5'
model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('Saved trained model at %s ' % model_path)

# Evaluate
test_loss, test_acc = model.evaluate(x_test,y_test)
print('Test Accuracy',test_acc)

# Plotting the metrics
fig = plt.figure()
#plt.subplot(2,1,1)
plt.plot()
# plt.scatter(history.history['accuracy'],history.history['val_accuracy'])
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')
plt.savefig('model_accuracy.png')
plt.show()

#plt.subplot(2,1,2)
plt.plot()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.savefig('model_loss.png')
plt.show()

# Predict
# 0 = Airplane, 1 = Automobile, 2 = Bird, 3 = Cat, 4 = Deer
# 5 = Dog, 6 = Frog, 7 = Horse, 8 = Ship, 9 = Truck
from random import randint

for i in range(10):  
    plt.subplot(2,5,i+1)
    plt.rcParams["figure.figsize"] = (20,9)
    index = randint(0,9999)
    plt.imshow(x_train[index])
    plt.xticks([])
    plt.yticks([])
    prediction = model.predict_classes(x_train[index].reshape(1,32,32,3))
    plt.title(prediction)
    plt.savefig('test_set.png')
plt.show()