import numpy as np
import cv2
from tensorflow.keras.models import load_model
import imutils
import matplotlib.pyplot as plt
import base64

def crop_brain_contour(image, plot=False):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]            
    
    return new_image


def preprocess_image_base64(base64_string, target_size=(240, 240)):
    image_data = base64.b64decode(base64_string)
    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    image = crop_brain_contour(image, True)
    image = cv2.resize(image, target_size)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def predict_tumor(base64_string, model_path='./MIA/tumour_detect.h5'):
    model = load_model(model_path)
    preprocessed_image = preprocess_image_base64(base64_string)
    prediction = model.predict(preprocessed_image)

    accuracy = 1.0 - abs(prediction - 0.5) * 2

    if prediction < 0.5:
        return {
            'prediction': False,
            'accuracy': float(accuracy),
        }
    else:
        return {
            'prediction': True,
            'accuracy': float(accuracy),
        }