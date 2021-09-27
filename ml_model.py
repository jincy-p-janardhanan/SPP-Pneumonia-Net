from tensorflow import keras
import cv2
import numpy as np

model = keras.models.load_model('saved_model_11')

input_height = 128
input_width = 128
n_channels = 1

class_no=3
labels = {0:'Normal', 1:'Bacterial Pneumonia', 2:'Viral Pneumonia'}

def get_prediction(image_path):

    # load and transform image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (input_height, input_width), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # To convert colormap from BGR to GRAY
    #Normalize the image - convert the each pixel value between 0 and 1
    img = img / 255
    img = np.reshape(img, (1, input_height, input_width, n_channels))

    # predict result
    prediction = model.predict(img)
    result = np.argmax(prediction)
    label = labels[result]
    confidence = prediction[0][result] * 100

    return label, confidence