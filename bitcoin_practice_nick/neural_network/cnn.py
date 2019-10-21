import numpy as np
from os import listdir
from PIL import Image


class CNN:
    def __init__(self, labels, imageSize=(120, 120)):
        self.labels = labels
        self.imageSize = imageSize
        self.imageDir = "../images/"
        self.train_data = []
        self.test_data = []

    def labelImage(self, filename):
        label = filename[0:filename.find("_")]
        return [1 if spot.find(label) != -1 else 0 for spot in self.labels]

    def create_training_data(self):
        for query in self.labels:
            path = self.imageDir + query
            filenames = listdir(path)
            for filename in filenames:
                label = self.labelImage(filename)
                print(label)
                img = Image.open(path + "/" + filename)
                img = img.convert("L")  # grayscale
                img = img.resize(self.imageSize, Image.ANTIALIAS)
                self.train_data.append([np.array(img), np.array(label)])

        np.random.shuffle(self.train_data)
        np.save("./npy_data/train_whole_data.npy", self.train_data)

    def create_testing_data(self):
        for query in self.labels:
            path = self.imageDir + query
            filenames = listdir(path)
            for filename in filenames:
                label = self.labelImage(filename)
                test_num = filename.split("_")[1]
                print(label)
                img = Image.open(path + "/" + filename)
                img = img.convert("L")  # grayscale
                img = img.resize(self.imageSize, Image.ANTIALIAS)
                self.test_data.append([np.array(img), test_num])

        np.random.shuffle(self.test_data)
        np.save("./npy_data/test_whole_data.npy", self.test_data)


labels = ["marin", "ventura"]
cnn = CNN(labels)
cnn.create_training_data()
print(cnn.train_data)
