import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import glob
from PIL import Image

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    labels1=[]
    images1=[]
    folder_path0 = data_dir # the path to the folder that contains the images
    for i in range(43):
        labels0=[]
        images0=[]
        folder_path1=folder_path0+'\\'+str(i)
        #file_names = glob.glob(folder_path1 + '/*.ppm')  a list of file names or paths that end with .jpg
        file_names = os.listdir(folder_path1)
        for file_name in file_names: # loop over the file names
            img = Image.open(os.path.join(folder_path1, file_name)) # read the image as a PIL image object
            img = np.array(img) # convert the image to an array
            res = Image.fromarray(img) # convert the image back to a PIL image object
            res = res.resize((IMG_WIDTH, IMG_HEIGHT)) # resize the image
            res = np.array(res)
            images1.append(res)
            labels1.append(i)
    return(images1,labels1)
        


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create a convolutional neural network
    model = tf.keras.models.Sequential([

        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        tf.keras.layers.Conv2D(
            30, (3, 3), activation="relu", input_shape=(30, 30, 3)
        ),

        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # Convolutional layer. Learn 32 filters using a 3x3 kernel n2
        tf.keras.layers.Conv2D(
            30, (3, 3), activation="relu", input_shape=(30, 30, 3)
        ),

        # Max-pooling layer, using 2x2 pool size n2
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(190, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # Add an output layer with output units for all 10 digits
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model



if __name__ == "__main__":
    main()
