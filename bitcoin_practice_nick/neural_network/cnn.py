from __future__ import absolute_import, division, print_function, unicode_literals

import os
import numpy as np
from os import listdir
from PIL import Image

import tensorflow as tf
import matplotlib.pyplot as plt
from neural_network.image_processor import label_brand, known_brands


class CNN:
    def __init__(self, labels, image_size=120):
        self.labels = labels
        self.imageSize = (image_size, image_size)
        self.num_brands = 0

        self.train_data = []
        self.test_data = []

        self.train_data_dir = "./test_data/"
        self.test_data_dir = "./test_data/"

        data_path = os.getcwd() + "/npy_data/"
        try:
            os.mkdir(data_path)
        except OSError:
            print("Could not create npy_data folder")  # do nothing

        self.create_training_data()
        self.create_testing_data()

    def labelImage(self, filename):
        label = filename[0:filename.find("_")]
        for i in range(len(self.labels)):
            if self.labels[i].find(label) != -1:
                return i

        return -1
        # return [1 if spot.find(label) != -1 else 0 for spot in self.labels]

    def create_np_info(self, filename, path, brand):
        label = self.labelImage(filename)
        img = Image.open(path + "/" + filename)
        img = img.convert("L")  # grayscale
        img = img.resize(self.imageSize, Image.ANTIALIAS)
        return [np.array(img), label, brand]

    def create_training_data(self):
        seen_brands = []
        for query in self.labels:
            brand = label_brand(query)
            if brand not in seen_brands:
                seen_brands.append(brand)
                self.num_brands += 1

            path = self.train_data_dir + query
            for filename in listdir(path):
                self.train_data.append(self.create_np_info(filename, path, brand))

        np.random.shuffle(self.train_data)
        np.save("./npy_data/train_whole_data.npy", self.train_data)

    def create_testing_data(self):
        for query in self.labels:
            brand = label_brand(query)
            path = self.test_data_dir + query
            for filename in listdir(path):
                self.test_data.append(self.create_np_info(filename, path, brand))

        np.random.shuffle(self.test_data)
        np.save("./npy_data/test_whole_data.npy", self.test_data)

    def run_network(self):
        model = self.create_model()
        images, targets, test_images, test_targets = self.reshape_images()
        history = model.fit(images, targets, epochs=10,
                            validation_data=(test_images, test_targets))

        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label='val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')

        test_loss, test_acc = model.evaluate(test_images, test_targets, verbose=2)
        print("Test loss: " + str(test_loss))
        print("Test accuracy: " + str(test_acc))

    def create_model(self):
        layers = tf.keras.layers
        dropout_rate = 0.2

        model = tf.keras.models.Sequential()
        model.add(layers.Conv2D(64, (4, 4), activation='relu', input_shape=(self.imageSize[0], self.imageSize[1], 1)))
        model.add(layers.MaxPooling2D((3, 3)))
        # model.add(layers.BatchNormalization())

        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        # model.add(layers.BatchNormalization())
        # model.add(layers.Dense(self.num_brands, activation='softmax'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        # model.add(layers.BatchNormalization())

        model.add(layers.Flatten())
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dropout(dropout_rate))

        model.add(layers.Dense(len(self.labels), activation='softmax'))
        model.summary()
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        return model

    def reshape_images(self):
        # training input tensor
        x_inputs = np.array([i[0] for i in self.train_data]).reshape((-1, self.imageSize[0], self.imageSize[1], 1))
        # expected output
        y_train_targets = np.array([i[1] for i in self.train_data])
        print(y_train_targets)

        # testing input tensor
        x_test = np.array([i[0] for i in self.test_data]).reshape((-1, self.imageSize[0], self.imageSize[1], 1))
        # expected output
        y_test_targets = np.array([i[1] for i in self.test_data])

        return x_inputs, y_train_targets, x_test, y_test_targets
