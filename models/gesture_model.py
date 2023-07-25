"""
Gesture prediction Module
"""

from tensorflow.keras.models import load_model
import cv2
import numpy as np

model = load_model("./gesture_detection_model.h5")

categories = {"down": 0, "neutral": 1, "up": 2, "other": 3}


def fetch_gesture(img):
    """
    Return the predicted gesture of the image:
    input : Image
    output : Gesture label
    """
    img = cv2.resize(img, (50, 50))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)  # Add a batch dimension

    predicted_probabilities = model.predict(img)
    predicted_label = np.argmax(predicted_probabilities)

    gesture_label = None
    for label, value in categories.items():
        if value == predicted_label:
            gesture_label = label
            break

    print("Predicted gesture label for the new image:", gesture_label)
    return gesture_label


# fetch_gesture(cv2.imread("test/hand_5.png"))