"""
Utility functions for the web app
"""
import os
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
from config import loaded_model
from flask import jsonify

# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

classification_classes = {
    0: 'Alzheimer\'s Disease',  # Updated to match frontend expectations
    1: 'Normal',
    2: 'Parkinson\'s Disease',  # Updated to match frontend expectations
}

def preprocess_image(image) -> np.array:
    """
    Here the input image is preprocessed for classification
    Parameters: 
    image (PIL.image): This is the input image to be preprocessed
    It returns the preprocessed images as a Numpy array - np.array
    """
    image = Image.open(image).convert("RGB").resize((224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    # Normalize pixel values to [0,1] range (common for many models)
    image = image / 255.0
    return image

def classify_image(image: np.array) -> dict:
    
    classification = loaded_model.predict(image, verbose=0)[0]
    classified_label = classification_classes[np.argmax(classification)]
    
    print(f"Raw predictions: {classification}")
    print(f"Prediction shape: {classification.shape}")
    print(f"Classified as: {classified_label}")
    
    return {
        "classification": classified_label,
        "Alzheimer": round(float(classification[0]), 6),
        "Normal": round(float(classification[1]), 6),
        "Parkinson": round(float(classification[2]), 6),
    }
